"""Anth-28S-inspired diagnostics on frozen MiCucumber references; no primer selection.
Run from any directory: python3 results/anth28s_evaluation/run.py
Requires C++17; numerical summaries otherwise use the Python standard library.
"""
import collections,csv,hashlib,json,statistics,subprocess,tempfile,zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'results';OUT.mkdir(exist_ok=True)
INPUTS=set()
def source(p):
    p=ROOT/p;INPUTS.add(str(p.relative_to(ROOT)));return p
def rows(p):
    with p.open() as f:return list(csv.DictReader(f))
def readfa(p):
    d={}
    for line in p.open():
        if line.startswith('>'):
            k=line[1:].split()[0].removeprefix('_R_');assert k not in d;d[k]=''
        else:d[k]+=line.strip().upper()
    return d
def save(name,data,fields=None):
    with (OUT/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(data[0]));w.writeheader();w.writerows(data)
def median(v):return statistics.median(v) if v else ''
summary=[];order_summary=[];identity_summary=[];barcode_rows=[];checks=[];pair_count=0
with tempfile.TemporaryDirectory() as temp:
    temp=Path(temp);exe=temp/'scan'
    subprocess.run(['c++','-O3','-std=c++17',str(HERE/'scan.cpp'),'-o',str(exe)],check=True)
    for gene in ('16S','12S','COI'):
        if gene=='16S':
            pairs=rows(source('sequences/primer_pairs.csv'))
            coords={r['locus']:r for r in rows(source('figures/current_region_coordinates.csv'))}
            for p in pairs:p.update(window=p['region'],**coords[p['region']])
            target=source('results/species_qc/representatives.fasta')
            with zipfile.ZipFile(source('reproducibility/frozen/xs_inputs.zip')) as z:
                bg=temp/'background.fasta';bg.write_bytes(z.read('background.fasta'))
            alignment=readfa(source('results/species_qc/curated_alignment.fasta'))
            meta=rows(source('results/species_qc/panel.csv'))
            for m in meta:m['species']=m['organism']
            panels={w:rows(source(f'results/species_qc/panel_{w}.csv')) for w in coords}
            panelids={w:{m['accession'] for m in panel} for w,panel in panels.items()}
            official={r['name']:r for r in rows(source('results/current_primers/comparison.csv'))}
            anchor='AB525437.1'
        else:
            base=f'markers/12S_COI/{gene}'
            pairs=rows(source(base+'/pairs.csv'))
            target=source(base+'/target.fasta');bg=source(base+'/background.fasta')
            alignment=readfa(source(base+'/aligned.fasta'));meta=rows(source(base+'/target_panel.csv'))
            anchor=source(base+'/anchor.txt').read_text().strip();official={p['name']:p for p in pairs}
            panelids={}
        ref=alignment[anchor];cols=[i for i,b in enumerate(ref) if b!='-']
        metadata={m['accession']:m for m in meta};assert len(metadata)==len(meta)
        assert len({m['species'] for m in meta})==len(meta)
        if gene!='16S':
            for p in pairs:
                a,b,c,d=[cols[int(p[k])-1] for k in ('F_start','F_end','R_start','R_end')]
                panelids[p['window']]={m['accession'] for m in meta if (s:=alignment[m['accession']]) and len(s)-len(s.lstrip('-'))<=a and len(s.rstrip('-'))>d and set(s[a:b+1]+s[c:d+1])<=set('ACGT-')}
        config=temp/'pairs.tsv'
        config.write_text(''.join(f"{p['name']}\t{p['F']}\t{p['R']}\t{20 if gene=='16S' and p['window']=='XS' else 50}\t{70 if gene=='16S' and p['window']=='XS' else (150 if gene=='16S' else 100)}\n" for p in pairs))
        hitsfile=OUT/f'{gene}_hits.csv';lengthfile=OUT/f'{gene}_lengths.csv'
        subprocess.run([str(exe),str(target),str(bg),str(config),str(hitsfile),str(lengthfile)],check=True,stderr=subprocess.DEVNULL)
        hits=rows(hitsfile);bg_n=len(readfa(bg));assert bg_n=={'16S':5600,'12S':438,'COI':2216}[gene]
        window_by_name={p['name']:p['window'] for p in pairs}
        lengths=[r for r in rows(lengthfile) if r['role']=='background' or r['accession'] in panelids[window_by_name[r['name']]]]
        save(f'{gene}_lengths.csv',lengths,['name','role','accession','threshold','span'])
        lookup={(r['name'],r['role'],r['accession']):r for r in hits}
        for p in pairs:
            pair_count+=1;n=p['name'];ids=panelids[p['window']]
            for role,allowed,denom in [('target',ids,len(ids)),('background',None,bg_n)]:
                hh=[r for r in hits if r['name']==n and r['role']==role and (allowed is None or r['accession'] in allowed)]
                for k in (0,1,2):
                    for terminal in (False,True):
                        field='min_max_terminal_compatible' if terminal else 'min_max_mismatches'
                        passed=[r for r in hh if int(r[field])<=k]
                        summary.append(dict(gene=gene,name=n,window=p['window'],role=role,threshold=k,terminal3_required=int(terminal),n=denom,matched=len(passed),percent=100*len(passed)/denom))
                        if role=='target':
                            for order in sorted({metadata[a]['order'] for a in ids}):
                                oo={a for a in ids if metadata[a]['order']==order}
                                order_summary.append(dict(gene=gene,name=n,order=order,threshold=k,terminal3_required=int(terminal),n=len(oo),matched=sum(r['accession'] in oo for r in passed)))
                        # Released exact/strict Watson-Crick scores are independent cross-checks.
                        if k==0 and not terminal or k==2 and terminal:
                            old=official[n]
                            key=('exact_labels' if k==0 else 'covered_labels') if gene=='16S' else ('exact' if k==0 else 'covered')
                            if role=='target':expected=int(old[key])
                            elif k==2:expected=int(old['strict_WC' if gene=='16S' else 'WC'])
                            else:continue
                            assert len(passed)==expected,(gene,n,role,k,len(passed),expected)
                            checks.append(dict(gene=gene,name=n,role=role,threshold=k,matched=expected))
            print(gene,n,'scan verified',flush=True)
        # Aligned primer-free inserts, one representative per species; ordinary/D share a window.
        windows={p['window']:p for p in pairs}
        for window,p in windows.items():
            left,right=cols[int(p['F_end'])-1]+1,cols[int(p['R_start'])-1]
            inserts=[]
            for a in panelids[window]:
                s=alignment[a][left:right];ungapped=s.replace('-','')
                if not ungapped or set(ungapped)-set('ACGT'):continue
                m=metadata[a];inserts.append(dict(gene=gene,window=window,accession=a,species=m['species'],order=m['order'],genus=m['species'].split()[0],sequence=ungapped,aligned=s,length=len(ungapped)))
            inserts.sort(key=lambda r:(r['order'],r['genus'],r['species'],r['accession']))
            barcode_rows.extend(inserts)
            pairrows=[];dist=collections.defaultdict(list);conflicts=0
            for i,x in enumerate(inserts):
                for j in range(i+1,len(inserts)):
                    y=inserts[j];compared=matches=gaps=0
                    for a,b in zip(x['aligned'],y['aligned']):
                        if a==b=='-':continue
                        assert a in 'ACGT-' and b in 'ACGT-'
                        compared+=1;matches+=a==b;gaps+=(a=='-' or b=='-')
                    assert compared>0
                    identity=100*matches/compared
                    relation='same_genus' if x['genus']==y['genus'] else ('same_order_other_genus' if x['order']==y['order'] else 'different_order')
                    identical=x['sequence']==y['sequence'];conflicts+=identical
                    dist[relation].append(identity)
                    pairrows.append(dict(i=i,j=j,accession_a=x['accession'],accession_b=y['accession'],species_a=x['species'],species_b=y['species'],relationship=relation,compared_columns=compared,gap_columns=gaps,identity_pct=identity,identical_insert=int(identical)))
            save(f'{gene}_{window}_identity.csv',pairrows)
            groups=collections.Counter(x['sequence'] for x in inserts)
            identity_summary.append(dict(gene=gene,window=window,n=len(inserts),unique_species=sum(groups[x['sequence']]==1 for x in inserts),identical_species_pairs=conflicts,insert_min=min(x['length'] for x in inserts),insert_max=max(x['length'] for x in inserts),same_genus_pairs=len(dist['same_genus']),same_genus_median_identity=median(dist['same_genus']),same_order_other_genus_pairs=len(dist['same_order_other_genus']),same_order_other_genus_median_identity=median(dist['same_order_other_genus']),different_order_pairs=len(dist['different_order']),different_order_median_identity=median(dist['different_order'])))
            print(gene,window,'identity',len(inserts),'species',flush=True)
save('mismatch_summary.csv',summary);save('mismatch_by_order.csv',order_summary)
save('identity_summary.csv',identity_summary);save('barcodes.csv',barcode_rows)
save('released_score_checks.csv',checks)
# Internal invariants and independent published-summary agreement.
for gene in ('16S','12S','COI'):
    for n in {r['name'] for r in summary if r['gene']==gene}:
        for role in ('target','background'):
            for t in (0,1):
                seq=[r['matched'] for r in summary if r['gene']==gene and r['name']==n and r['role']==role and r['terminal3_required']==t]
                assert seq==sorted(seq)
            for k in (0,1,2):
                v={r['terminal3_required']:r['matched'] for r in summary if r['gene']==gene and r['name']==n and r['role']==role and r['threshold']==k}
                assert v[1]<=v[0]
INPUTS.update(str(f.relative_to(ROOT)) for f in (HERE/'run.py',HERE/'scan.cpp'))
manifest=dict(reference='McCartin et al. (2024), doi:10.7717/peerj.18607, pp.6,11–13, Fig.3',pair_count=pair_count,independent_released_score_checks=len(checks),status='PASS',input_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(INPUTS)},interpretation='Mismatch thresholds apply separately to each primer. Watson–Crick only; optional terminal-three compatibility. Background denominators are records, targets are evaluable one-species representatives. Identity counts single gaps as differences, ignores double gaps, excludes ambiguous inserts; this is not empirical identification accuracy or an intraspecific barcoding-gap test.')
(OUT/'validation.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('PASS',pair_count,'pairs;',len(checks),'independent released-score checks')
