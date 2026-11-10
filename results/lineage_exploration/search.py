"""Explore one-end supplements for the 16S XS, S, M and XL windows."""
import argparse
import itertools
import json
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'lineage_pool'))
from design import ROOT, BACKGROUND, fa, rc, rows, matches, thermal, terminal, single, expand, hetero, write
from xs_raw_helpers import I

MASK = {base: 1 << i for i, base in enumerate('ACGT')}
CODES = {sum(MASK[b] for b in bases): symbol for symbol, bases in I.items()}
WINDOWS = {'XS': 'XS', 'S': 'SD', 'M': 'MD', 'XL': 'XLD'}
QUOTA = 30  # Scan at most this many candidates per side and position class.


def observed_candidates(templates):
    """Observed exact motifs and pairwise consensus within the 3′ half."""
    motifs = sorted(set(templates))
    by_prefix = defaultdict(list)
    split = len(motifs[0]) // 2
    for motif in motifs:
        by_prefix[motif[:split]].append(motif)
    result = set(motifs)
    for group in by_prefix.values():
        for a, b in itertools.combinations(group, 2):
            if sum(x != y for x, y in zip(a, b)) <= 3:
                result.add(''.join(CODES[MASK[x] | MASK[y]] for x, y in zip(a, b)))
    return sorted(q for q in result if terminal(q))


@lru_cache(None)
def weighted_thermal(f, r, variable, fraction):
    if fraction == .5:
        return thermal(f, r)
    # Same two Primer3 conditions, with the original oligo assigned a larger fraction
    # of the 200 nM on the variable side. The 50 nM per-variant test is unchanged.
    equal = thermal(f, r)[0]
    midpoints, molecules = {}, defaultdict(float)
    for side, primers in [('F', f), ('R', r)]:
        midpoints[side] = []
        weights = (fraction, 1-fraction) if side == variable else (1,)
        for primer, weight in zip(primers, weights):
            variants = expand(primer)
            concentration = 200 * weight / len(variants)
            values = [single(q, concentration)[0] for q in variants]
            midpoints[side].append((min(values)+max(values))/2)
            for q in variants:
                molecules[q] += concentration
    delta = max(abs(a-b) for a,b in itertools.product(midpoints['F'],midpoints['R']))
    structure = max([single(q,c)[1] for q,c in molecules.items()] +
                    [hetero(a,b,max(molecules[a],molecules[b]))
                     for a,b in itertools.combinations(molecules,2)])
    return [equal, dict(scenario='200 nM per direction',max_duplex_midpoint_delta_C=round(delta,6),
                        max_structure_tm_C=round(structure,6),passes=delta<=5 and structure<55)]


def candidates(pair, site, align, columns, panel):
    for variable in 'FR':
        common = 'R' if variable == 'F' else 'F'
        original = pair[variable]
        fixed_start, fixed_end = [int(site[f'{common}_{p}']) for p in ('start','end')]
        start, end = [int(site[f'{variable}_{p}']) for p in ('start','end')]
        def binding(acc, low, high, side):
            seq = align[acc]
            a, b = columns[low-1], columns[high-1]
            if a < limits[acc][0] or b > limits[acc][1]:
                return ''
            motif = seq[a:b+1].replace('-','')
            return rc(motif) if side == 'R' else motif
        limits = {acc: (len(align[acc])-len(align[acc].lstrip('-')),
                         len(align[acc].rstrip('-'))-1) for acc in panel}
        fixed = {a for a in panel if matches(pair[common], binding(a,fixed_start,fixed_end,common))}
        original_hits = {a for a in fixed if matches(original,binding(a,start,end,variable))}
        gain_pool = sorted(fixed-original_hits)
        for u in range(start-5,start+6):
            for v in range(end-5,end+6):
                if abs(v-u+1-len(original))>3:
                    continue
                table = {a:binding(a,u,v,variable) for a in gain_pool}
                table = {a:q for a,q in table.items() if len(q)==v-u+1 and set(q)<=set(MASK)}
                if not table:
                    continue
                templates = np.array([[MASK[b] for b in q] for q in table.values()],dtype=np.uint8)
                for q in observed_candidates(table.values()):
                    if q == original:
                        continue
                    qmask = [sum(MASK[b] for b in I[symbol]) for symbol in q]
                    mismatches = (templates & qmask) == 0
                    ok = (mismatches.sum(axis=1)<=2) & ~mismatches[:,-3:].any(axis=1)
                    hit = {a for a,present in zip(table,ok) if present}
                    if len(hit)>=2:
                        yield dict(side=variable,start=u,end=v,primer=q,anchored=hit,
                                   shift=abs(u-start)+abs(v-end),site_exact=sum(not x.any() for x in mismatches))


def read_hits(path, panel):
    hits = defaultdict(lambda: defaultdict(set))
    for r in rows(path, '\t'):
        result = hits[r['name']]
        if r['role']=='target' and r['accession'] in panel:
            for key,flag in [('coverage','le2last3'),('exact','exact')]:
                if r[flag]=='1':
                    result[key].add(r['accession'])
        elif r['role']=='background':
            for key,(model,flag) in BACKGROUND.items():
                if r['model']==model and r[flag]=='1':
                    result[key].add(r['accession'])
    return hits


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output.resolve()
    out.mkdir(parents=True,exist_ok=True)
    alignment=fa(ROOT/'results/species_qc/curated_alignment.fasta')
    cols=[i for i,b in enumerate(alignment['AB525437.1']) if b!='-']
    pairs={r['name']:r for r in rows(ROOT/'sequences/primer_pairs.csv')}
    metrics={r['name']:r for r in rows(ROOT/'results/current_primers/comparison.csv')}
    coords={r['locus']:r for r in rows(ROOT/'figures/current_region_coordinates.csv')}
    all_trials, summaries, selected = [], [], []
    with tempfile.TemporaryDirectory() as tmp:
        work=Path(tmp)
        scanner=work/'scan'
        subprocess.run(['c++','-O3','-std=c++17',str(ROOT/'scripts/xs_independent_scan.cpp'),
                        '-o',str(scanner)],check=True)
        (work/'target.fasta').symlink_to(ROOT/'results/species_qc/representatives.fasta')
        with zipfile.ZipFile(ROOT/'reproducibility/frozen/xs_inputs.zip') as z:
            (work/'background.fasta').write_bytes(z.read('background.fasta'))
        for window,name in WINDOWS.items():
            pair=pairs[name]
            panel={x['accession']:x for x in rows(ROOT/f'results/species_qc/panel_{window}.csv')}
            ranked=sorted(candidates(pair,coords[window],alignment,cols,panel),
                          key=lambda x:(-len(x['anchored']),-x['site_exact'],x['shift'],x['primer'],x['start']))
            quotas=Counter()
            trials=[]
            used=set()
            for trial in ranked:
                side,q=trial['side'],trial['primer']
                group=(side,bool(trial['shift']))
                if quotas[group]>=QUOTA or (side,q) in used:
                    continue
                f,r=((pair['F'],q),(pair['R'],)) if side=='F' else ((pair['F'],),(pair['R'],q))
                # Test equal allocation first. The 90:10 scenario addresses dilution of the original MD F.
                fractions=(.5,.9) if name=='MD' else (.5,)
                for fraction in fractions:
                    screen=weighted_thermal(f,r,side,fraction)
                    if all(x['passes'] for x in screen):
                        trial.update(fraction=fraction,thermal=screen,F=f,R=r)
                        trials.append(trial)
                        quotas[group]+=1
                        used.add((side,q))
                        break
            print(name,'aligned candidates',len(ranked),'raw shortlisted',len(trials),flush=True)
            (work/'independent_primers.tsv').write_text(
                f'base\t{pair["F"]}\t{pair["R"]}\n'+''.join(
                f'{i}\t{t["F"][-1]}\t{t["R"][-1]}\n' for i,t in enumerate(trials)))
            subprocess.run([str(scanner),str(work),*(['20','70'] if window=='XS' else ['50','150'])],
                           check=True,stderr=subprocess.DEVNULL)
            results=read_hits(work/'independent_hits.tsv',panel)
            base=results['base']
            assert len(base['coverage'])==int(metrics[name]['covered_labels']),name
            assert len(base['exact'])==int(metrics[name]['exact_labels']),name
            assert all(len(base[k])==int(metrics[name][k]) for k in BACKGROUND),name
            retained=[]
            for i,trial in enumerate(trials):
                result=results[str(i)]
                gain=result['coverage']-base['coverage']
                intended=gain & trial['anchored']
                bg={k:len(result[k]-base[k]) for k in BACKGROUND}
                order_counts=Counter(panel[a]['order'] for a in intended)
                row=dict(assay=name,side=trial['side'],start=trial['start'],end=trial['end'],primer=trial['primer'],
                         original_fraction=trial['fraction'],n=len(panel),base_coverage=len(base['coverage']),
                         covered=len(base['coverage']|result['coverage']),exact=len(base['exact']|result['exact']),
                         intended_new=len(intended),other_site_new=len(gain-intended),
                         new_by_order='; '.join(f'{k}:{v}' for k,v in sorted(order_counts.items())),
                         **{'new_'+k:v for k,v in bg.items()})
                all_trials.append(row)
                if len(intended)>=2 and not gain-intended:
                    retained.append((row,trial,result))
            if retained:
                for position in ('same','shifted'):
                    subset=[x for x in retained if bool(x[1]['shift'])==(position=='shifted')]
                    for background in ('all-neutral','strict-neutral','maximum-gain'):
                        if background=='all-neutral':
                            valid=[x for x in subset if not any(x[0]['new_'+k] for k in BACKGROUND)]
                        elif background=='strict-neutral':
                            valid=[x for x in subset if not any(x[0]['new_'+k] for k in ('strict_WC','strict_GT'))]
                        else:
                            valid=subset
                        if not valid:
                            continue
                        row,trial,result=min(valid,key=lambda x:(-x[0]['covered'],-x[0]['exact'],
                            sum(x[0]['new_'+k] for k in BACKGROUND),x[1]['shift'],x[0]['primer']))
                        summaries.append(dict(position=position,background=background,**row))
                        if background in ('all-neutral','strict-neutral'):
                            selected.append(dict(position=position,background=background,**row,
                                F=trial['F'],R=trial['R'],thermal=trial['thermal'],
                                target_coverage=sorted(base['coverage']|result['coverage']),
                                target_exact=sorted(base['exact']|result['exact']),
                                background_accessions={k:sorted(base[k]|result[k]) for k in BACKGROUND}))
            print(name,'completed scans',flush=True)
    write(out/'scanned_candidates.csv',all_trials)
    write(out/'shortlist.csv',summaries)
    (out/'shortlist.json').write_text(json.dumps(selected,indent=2)+'\n')


if __name__=='__main__':
    main()
