"""Score frozen external templates with the released geometry and both mismatch rules."""
import csv
import json
import subprocess
import sys
import tempfile
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from history import accession_key

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'results/marker_complementarity'))
from compare import fa, paired_flags, rc, read, read_inputs, sites

COORDS=('F_start','F_end','R_start','R_end')
BASES=set('ACGT')


def write(name, rows):
    with (HERE/name).open('w') as handle:
        w=csv.DictWriter(handle,list(rows[0]),lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def evaluate_limited(job):
    gene,name,assay,targets,background=job
    lo,gap=(70,20) if gene=='16S' and name=='XS' else (150,50) if gene=='16S' else (100,50)
    observed={}
    for role,templates in [('target',targets),('background',background)]:
        for a,seq in templates.items():
            code=min(paired_flags(seq,assay['F'],assay['R'],lo,gap,role=='background'),default=2)
            exact=False
            if code==0:
                for strand in (seq,rc(seq)):
                    for f in assay['F']:
                        for r in assay['R']:
                            for pos_f,_,_ in sites(strand,f,False,False,0):
                                for pos_r,_,_ in sites(strand,r,True,False,0):
                                    inner=pos_r-pos_f-len(f)
                                    span=pos_r+len(r)-pos_f
                                    exact |= (0<=inner<=1000 if role=='background' else inner>=gap and lo<=span<=500)
            observed[role,a]=code,exact
    return (gene,name),observed


def get_assays():
    coords,lineage=read_inputs()
    assays={g:{} for g in ('16S','12S','COI')}
    for row in read('sequences/primer_pairs.csv'):
        n=row['name']
        assays['16S'][n]=dict(F=[row['F']],R=[row['R']],coords=coords[row['region']])
    for n,row in lineage.items():
        if n not in assays['16S']:
            assays['16S'][n]=dict(F=row['F'],R=row['R'],coords=coords[n[0]])
    for g in ('12S','COI'):
        for r in read(f'markers/12S_COI/{g}/pairs.csv'):
            assays[g][r['name']]=dict(F=[r['F']],R=[r['R']],coords=tuple(int(r[k]) for k in COORDS))
    return assays


def align_external(gene, targets, work):
    if gene=='16S':
        template=ROOT/'results/species_qc/curated_alignment.fasta'
        anchor='AB525437.1'
    else:
        base=ROOT/f'markers/12S_COI/{gene}'
        template=base/'aligned.fasta'
        anchor=(base/'anchor.txt').read_text().strip()
    aligned=work/f'{gene}_external_alignment.fasta'
    with aligned.open('w') as output:
        subprocess.run(['mafft','--quiet','--thread','1','--keeplength','--addfragments',
                        str(HERE/f'{gene}_target.fasta'),str(template)],
                       stdout=output,stderr=subprocess.DEVNULL,check=True)
    sequences={a.removeprefix('_R_'):s for a,s in fa(aligned).items()}
    assert targets.keys()<=sequences.keys()
    assert sequences[anchor].replace('-','')==fa(template)[anchor].replace('-','')
    return sequences,[i for i,b in enumerate(sequences[anchor]) if b!='-']


def eligible(sequence, columns, coords, gene):
    lo,hi=len(sequence)-len(sequence.lstrip('-')),len(sequence.rstrip('-'))
    for first,last in (coords[:2],coords[2:]):
        a,b=columns[first-1],columns[last-1]
        motif=sequence[a:b+1].replace('-','')
        if a<lo or b>=hi or not motif or set(motif)-BASES:
            return False
        if gene=='16S' and len(motif)*10<9*(last-first+1):
            return False
    return True


def independent(gene, assays, work, exe):
    raw={}
    for small in ((False,True) if gene=='16S' else (False,)):
        config={}
        for name,assay in assays.items():
            if (gene=='16S' and name=='XS')!=small:
                continue
            for i,(f,r) in enumerate((f,r) for f in assay['F'] for r in assay['R']):
                config[f'{name}:{i}']=(f,r)
        (work/'independent_primers.tsv').write_text(''.join(f'{n}\t{f}\t{r}\n' for n,(f,r) in config.items()))
        gap,span=('20','70') if small else ('50','150' if gene=='16S' else '100')
        subprocess.run([str(exe),str(work),gap,span],check=True,stderr=subprocess.DEVNULL)
        for r in read(work/'independent_hits.tsv','\t'):
            key=(r['name'].split(':')[0],r['role'],r['accession'],r['model'])
            exact,strict=raw.get(key,(False,False))
            raw[key]=(exact or r['exact']=='1',strict or r['le2last3']=='1')
    return raw


def main():
    assays=get_assays()
    meta={(r['gene'],r['role'],r['accession']):r for r in read(HERE/'panel.csv')}
    history=set((HERE/'historical_accessions.txt').read_text().splitlines())
    assert all(accession_key(a) not in history for _,_,a in meta)
    assert all(len({r['species'] for (gg,rr,a),r in meta.items() if (gg,rr)==(g,role)})==
               sum((gg,rr)==(g,role) for gg,rr,a in meta) for g in assays for role in ('target','background'))
    jobs=[]; summaries=[]; detail=[]; backgrounds=[]; validation=0
    with tempfile.TemporaryDirectory() as temp:
        work=Path(temp)
        exe=work/'scan'
        subprocess.run(['c++','-O3','-std=c++17',str(ROOT/'scripts/xs_independent_scan.cpp'),'-o',str(exe)],check=True)
        for gene in assays:
            targets,background=(fa(HERE/f'{gene}_{role}.fasta') for role in ('target','background'))
            assert all(a in meta for a in ((gene,role,id) for role,d in [('target',targets),('background',background)] for id in d))
            sequences,cols=align_external(gene,targets,work) if targets else ({},[])
            for name,assay in assays[gene].items():
                jobs.append((gene,name,assay,targets,background))
            for role in ('target','background'):
                dst=work/f'{role}.fasta'
                dst.unlink(missing_ok=True)
                dst.symlink_to(HERE/f'{gene}_{role}.fasta')
            raw=independent(gene,assays[gene],work,exe)
            with ProcessPoolExecutor(max_workers=4) as pool:
                results=dict(pool.map(evaluate_limited,[job for job in jobs if job[0]==gene]))
            for name,assay in assays[gene].items():
                for role,templates in [('target',targets),('background',background)]:
                    matched=[]
                    for a in templates:
                        can_evaluate=role=='background' or eligible(sequences[a],cols,assay['coords'],gene)
                        exact,strict=raw.get((name,role,a,'WC'),(False,False))
                        gt=raw.get((name,role,a,'GT'),(False,False))[1] if role=='background' else ''
                        code,expected_exact=results[gene,name][role,a]
                        assert (code==0)==strict and expected_exact==exact,(gene,name,role,a)
                        assert not exact or strict
                        validation+=1
                        row=dict(gene=gene,assay=name,role=role,accession=a,species=meta[gene,role,a]['species'],
                                 group=meta[gene,role,a]['group'],evaluable=int(can_evaluate),
                                 exact=int(exact) if can_evaluate else '',strict=int(strict) if can_evaluate else '',
                                 limited=int(code<2) if can_evaluate else '',strict_GT=int(gt) if gt!='' else '')
                        detail.append(row)
                        if can_evaluate:
                            matched.append(row)
                    n=len(matched)
                    def count(k):
                        return sum(r[k] for r in matched)
                    coverage,exact,limited=(count(k) for k in ('strict','exact','limited'))
                    pct=lambda x:round(100*x/n,2) if n else ''
                    summaries.append(dict(gene=gene,assay=name,role=role,panel_n=len(templates),evaluable=n,
                                          exact=exact,exact_pct=pct(exact),strict=coverage,strict_pct=pct(coverage),
                                          limited=limited,limited_pct=pct(limited),
                                          strict_GT=count('strict_GT') if role=='background' else ''))
                    if role=='background':
                        for group in sorted({r['group'] for r in matched}):
                            rr=[r for r in matched if r['group']==group]
                            backgrounds.append(dict(gene=gene,assay=name,group=group,n=len(rr),
                                                    **{k:sum(r[k] for r in rr) for k in ('exact','strict','limited','strict_GT')}))
    write('summary.csv',summaries)
    write('predictions.csv',detail)
    write('background_by_group.csv',backgrounds)
    focus=('SD-Dendrochirotida','LD-Elasipodida')
    lookup={(r['assay'],r['accession']):r for r in detail if r['gene']=='16S' and r['role']=='target'}
    common=[a for a in {a for _,a in lookup} if all(lookup[n,a]['evaluable'] for n in focus)]
    union={key:sum(any(lookup[n,a][key] for n in focus) for a in common) for key in ('exact','strict','limited')}
    write('separate_assay_union.csv',[dict(evaluable=len(common),**union)])
    (HERE/'verification.json').write_text(json.dumps(dict(status='PASS',assays=sum(map(len,assays.values())),
        independent_strict_and_exact_accession_checks=validation,external_records_by_role_gene={
            f'{g}_{role}':sum((gg,rr)==(g,role) for gg,rr,a in meta)
            for g in assays for role in ('target','background')}),indent=2)+'\n')
    print('PASS:',validation,'independent strict accession comparisons;',len(common),'shared 16S S/L targets')

if __name__=='__main__':
    main()
