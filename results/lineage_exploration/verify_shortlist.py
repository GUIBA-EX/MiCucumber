"""Independently verify the best all-neutral and materially stronger strict-neutral pools."""
import argparse
import json
import zipfile
from pathlib import Path

from search import ROOT, BACKGROUND, fa, rc, rows
from verify import sites


def flags(strands, forwards, reverses, wobble, limit, window, target):
    result = set()
    for seq in strands:
        fs = [(len(q), list(sites(seq, q, False, wobble, limit))) for q in forwards]
        rs = [(len(q), list(sites(seq, q, True, wobble, limit))) for q in reverses]
        for lf, forward in fs:
            for lr, reverse in rs:
                for f, fm, ft in forward:
                    for r, rm, rt in reverse:
                        gap, span = r-f-lf, r+lr-f
                        if target:
                            valid = gap >= (20 if window=='XS' else 50) and (70 if window=='XS' else 150) <= span <= 500
                        else:
                            valid = 0 <= gap <= 1000
                        if not valid:
                            continue
                        mm = max(fm,rm)
                        if mm == 0:
                            result.add('exact')
                        if mm <= 2:
                            result.add('le2')
                            if not ft and not rt:
                                result.add('le2last3')
                        if mm <= 3:
                            result.add('le3')
                        result.add('le4')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output
    source=json.loads((out/'shortlist.json').read_text())
    raw=fa(ROOT/'results/species_qc/representatives.fasta')
    bg={}
    with zipfile.ZipFile(ROOT/'reproducibility/frozen/xs_inputs.zip') as z:
        for line in z.read('background.fasta').decode().splitlines():
            if line.startswith('>'):
                accession=line[1:].split()[0]
                bg[accession]=''
            else:
                bg[accession]+=line.strip().upper()
    assert len(bg)==5600
    bg={a:(s,rc(s)) for a,s in bg.items()}
    report=[]
    for assay in ('XS','SD','MD','XLD'):
        within=[r for r in source if r['assay']==assay]
        window={'SD':'S','MD':'M','XLD':'XL'}.get(assay,assay)
        rank=lambda x:(x['covered'],x['exact'],x['position']=='same')
        all_neutral=max((r for r in within if r['background']=='all-neutral'),key=rank,default=None)
        strict=max((r for r in within if r['background']=='strict-neutral'),key=rank,default=None)
        selected=[all_neutral] if all_neutral else []
        if strict and (not all_neutral or strict['covered']>=all_neutral['covered']+5):
            selected.append(strict)
        panel=rows(ROOT/f'results/species_qc/panel_{window}.csv')
        for pool in selected:
            f,r=pool['F'],pool['R']
            actual={k:set() for k in ('coverage','exact',*BACKGROUND)}
            for accession in (x['accession'] for x in panel):
                seq=raw[accession]
                match=flags((seq,rc(seq)),f,r,False,2,window,True)
                if 'le2last3' in match:
                    actual['coverage'].add(accession)
                if 'exact' in match:
                    actual['exact'].add(accession)
            for accession,strands in bg.items():
                matches={model:flags(strands,f,r,model=='GT',limit,window,False)
                         for model,limit in [('WC',4),('GT',2)]}
                for key,(model,flag) in BACKGROUND.items():
                    if flag in matches[model]:
                        actual[key].add(accession)
            expected={'coverage':pool['target_coverage'],'exact':pool['target_exact'],**pool['background_accessions']}
            for key in actual:
                assert actual[key]==set(expected[key]),(assay,pool['primer'],key,sorted(actual[key]^set(expected[key])))
            report.append({key:pool[key] for key in ('assay','side','start','end','primer','background','position')})
            report[-1].update(target_records=len(panel),background_records=len(bg),accession_disagreements=0)
            if assay == 'SD' and pool['primer'] == 'AAGGAGATTACGCTGTTATCCCTG' and pool['position'] == 'same':
                assert len(f) == 1 and len(r) == 2 and r[-1] == pool['primer']
                (out/'sd_pool.fasta').write_text(
                    f'>MiCucumber-16S-SD_F\n{f[0]}\n'
                    f'>MiCucumber-16S-SD_R\n{r[0]}\n'
                    f'>MiCucumber-16S-SD_R-Dendrochirotida\n{r[1]}\n')
            print(assay,pool['primer'],'PASS',flush=True)
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    main()
