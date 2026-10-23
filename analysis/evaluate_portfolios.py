from pathlib import Path
import csv,json,collections
p=Path(__file__).resolve().parent
assert json.loads((p/'independent_validation.json').read_text())['status']=='PASS'
ss=json.loads((p/'portfolio_selected.json').read_text());details=list(csv.DictReader((p/'target_detail.tsv').open(),delimiter='\t'));ind=list(csv.DictReader((p/'independent_hits.tsv').open(),delimiter='\t'));meta={r['accession']:r for r in csv.DictReader((p/'metadata.tsv').open(),delimiter='\t')};taxonomy={r['accession']:r['order'] for r in csv.DictReader((p/'target_taxonomy.tsv').open(),delimiter='\t')};ids=json.loads((p/'common_panel.json').read_text())['ids'];tab=collections.defaultdict(dict)
for r in details:
 if r['panel']=='common':tab[r['name']][r['accession']]=r
background=collections.defaultdict(list)
for r in ind:
 if r['role']=='background':background[r['name'],r['model']].append(r)
summ=[];taxout=[];bgout=[];membership=[]
for s in ss:
 names=s['allowed_pair_names'];rows=[];sizes=set()
 for k in ids:
  r=tab[names[0]][k];v=dict(accession=k,organism=r['organism'],weight=float(r['weight']))
  for metric in ['exact','le2last3','le2']:v[metric]=any(tab[n][k][metric]=='True' for n in names)
  for n in names:sizes.update(int(x) for x in tab[n][k]['sizes'].split(',') if x)
  rows.append(v)
 out=dict(name=s['name'],locus=s['locus'],mode=s['mode'],F_oligos=len(s['F_ids']),R_oligos=len(s['R_ids']),component_pairs=len(s['component_pairs']),evaluated_pairs=len(names),n_labels=len({r['organism'] for r in rows}),n_haplotypes=len(rows),product_min=min(sizes) if sizes else '',product_max=max(sizes) if sizes else '')
 for metric in ['exact','le2last3','le2']:out[metric+'_pct']=100*sum(r['weight'] for r in rows if r[metric])
 for model in ['WC','GT']:
  rr=[r for n in names for r in background[n,model]]
  for metric in (['le2','le3','le4','ambiguous'] if model=='WC' else ['le2','ambiguous']):
   records={r['accession'] for r in rr if r[metric]=='1'};out[model+'_'+metric]=len(records)
   for k in sorted(records):membership.append(dict(name=s['name'],model=model,criterion=metric,accession=k,organism=meta[k]['organism'],clade=meta[k]['clade']))
  for cl in sorted({m['clade'] for m in meta.values() if m['role']=='background'}):
   clrows=[r for r in rr if meta[r['accession']]['clade']==cl];bgout.append(dict(name=s['name'],model=model,clade=cl,**{metric:len({r['accession'] for r in clrows if r[metric]=='1'}) for metric in (['le2','le3','le4','ambiguous'] if model=='WC' else ['le2','ambiguous'])}))
 assert out['WC_le3']<=5 and out['GT_le2']<=5,(s['name'],out)
 for level in ['genus','source_order']:
  groups=collections.defaultdict(list)
  for r in rows:groups[r['organism'].split()[0] if level=='genus' else taxonomy[r['accession']]].append(r)
  for group,rr in groups.items():
   den=sum(r['weight'] for r in rr);taxout.append(dict(name=s['name'],level=level,group=group,n_labels=len({r['organism'] for r in rr}),coverage_pct=100*sum(r['weight'] for r in rr if r['le2last3'])/den))
 summ.append(out)
for name,data in [('portfolio_summary.tsv',summ),('portfolio_taxon_coverage.tsv',taxout),('portfolio_background_classes.tsv',bgout),('portfolio_offtarget_records.tsv',membership)]:
 with (p/name).open('w') as f:fields=sorted(set().union(*(r.keys() for r in data)));w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(data)
(p/'portfolio_qa.json').write_text(json.dumps(dict(status='PASS',schemes=len(ss),scope='all allowed component/cross-pair unions independently validated on original target/background sequences; <=5 confirmed records per WC3/GT2 analysis constraint; not wet-lab read fractions',common_labels=out['n_labels'],common_haplotypes=out['n_haplotypes']),indent=2));print(json.dumps(summ,indent=2))
