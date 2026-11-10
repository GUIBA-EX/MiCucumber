"""Test 5′ shortening of the shared MD reverse oligo for a balanced F pool."""
import argparse
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

from search import ROOT, BACKGROUND, fa, rc, rows, matches, terminal, thermal, weighted_thermal, read_hits, write
from verify_shortlist import flags


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output.resolve()
    md=max((r for r in json.loads((out/'shortlist.json').read_text())
            if r['assay']=='MD' and r['side']=='F' and r['background']=='all-neutral'),
           key=lambda r:(r['covered'],r['exact']))
    f,r=tuple(md['F']),md['R'][0]
    ratios=[dict(original_F_fraction=fraction,**weighted_thermal(f,(r,),'F',fraction)[1])
            for fraction in (.5,.8,.88,.9,.92,.95,.97)]
    write(out/'md_ratio_sensitivity.csv',ratios)
    trims=[dict(trim_5prime=trim,R=r[trim:],terminal_pass=terminal(r[trim:]),
                thermal=thermal(f,(r[trim:],))) for trim in range(1,4)]
    panel={x['accession']:x for x in rows(ROOT/'results/species_qc/panel_M.csv')}
    target={a:s for a,s in fa(ROOT/'results/species_qc/representatives.fasta').items() if a in panel}
    with tempfile.TemporaryDirectory() as tmp:
        work=Path(tmp)
        (work/'target.fasta').symlink_to(ROOT/'results/species_qc/representatives.fasta')
        with zipfile.ZipFile(ROOT/'reproducibility/frozen/xs_inputs.zip') as z:
            (work/'background.fasta').write_bytes(z.read('background.fasta'))
        bg=fa(work/'background.fasta')
        assert len(bg)==5600 and len(target)==len(panel)==174
        eligible=[x for x in trims if x['terminal_pass'] and all(t['passes'] for t in x['thermal'])]
        (work/'independent_primers.tsv').write_text(
            f'base\t{f[0]}\t{r}\n'+''.join(f'{x["trim_5prime"]}_{i}\t{q}\t{x["R"]}\n'
                                            for x in eligible for i,q in enumerate(f)))
        subprocess.run(['c++','-std=c++17','-O3',str(ROOT/'scripts/xs_independent_scan.cpp'),
                        '-o',str(work/'scan')],check=True)
        subprocess.run([str(work/'scan'),str(work),'50','150'],check=True,stderr=subprocess.DEVNULL)
        scan=read_hits(work/'independent_hits.tsv',panel)
        base=scan['base']
        coords=next(x for x in rows(ROOT/'figures/current_region_coordinates.csv') if x['locus']=='M')
        alignment=fa(ROOT/'results/species_qc/curated_alignment.fasta')
        ref=[i for i,b in enumerate(alignment['AB525437.1']) if b!='-']
        for trial in eligible:
            n=trial['trim_5prime']
            expected={k:scan[f'{n}_0'][k]|scan[f'{n}_1'][k] for k in ('coverage','exact',*BACKGROUND)}
            actual={k:set() for k in expected}
            for accession,seq in target.items():
                match=flags((seq,rc(seq)),f,(trial['R'],),False,2,'M',True)
                if 'le2last3' in match:
                    actual['coverage'].add(accession)
                if 'exact' in match:
                    actual['exact'].add(accession)
            for accession,seq in bg.items():
                match={model:flags((seq,rc(seq)),f,(trial['R'],),model=='GT',limit,'M',False)
                       for model,limit in [('WC',4),('GT',2)]}
                for key,(model,flag) in BACKGROUND.items():
                    if flag in match[model]:
                        actual[key].add(accession)
            for k in expected:
                assert actual[k]==expected[k],(n,k,actual[k]^expected[k])
            start,end=int(coords['R_start']),int(coords['R_end'])-n
            anchored=set()
            for accession,s in alignment.items():
                if accession not in panel:
                    continue
                ft=s[ref[int(coords['F_start'])-1]:ref[int(coords['F_end'])-1]+1].replace('-','')
                rt=rc(s[ref[start-1]:ref[end-1]+1].replace('-',''))
                if matches(trial['R'],rt) and any(matches(q,ft) for q in f):
                    anchored.add(accession)
            gain=actual['coverage']-base['coverage']
            trial.update(F=list(f),R_start=start,R_end=end,n=len(panel),background_n=len(bg),
                         covered=len(actual['coverage']),exact=len(actual['exact']),
                         original_covered=len(base['coverage']),original_exact=len(base['exact']),
                         gained=sorted(gain),lost=sorted(base['coverage']-actual['coverage']),
                         gained_at_other_sites=sorted(gain-anchored),
                         new_background={k:sorted(actual[k]-base[k]) for k in BACKGROUND},
                         coverage_matches_untrimmed_pool=actual['coverage']==set(md['target_coverage']),
                         exact_matches_untrimmed_pool=actual['exact']==set(md['target_exact']),
                         accession_disagreements=0)
            print(f'MD shared R 5′ trim {n}: {trial["covered"]}/{len(panel)}, '
                  f'{trial["exact"]} exact, zero disagreements',flush=True)
    (out/'md_balanced_pool.json').write_text(json.dumps(trims,indent=2)+'\n')


if __name__=='__main__':
    main()
