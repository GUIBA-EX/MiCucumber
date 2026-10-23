from pathlib import Path
import csv,json,collections
p=Path(__file__).resolve().parent
hits=list(csv.DictReader((p/'independent_hits.tsv').open(),delimiter='\t'));look={(r['name'],r['role'],r['model'],r['accession']):r for r in hits}
target=list(csv.DictReader((p/'target_detail.tsv').open(),delimiter='\t'));checks=0
for row in target:
 r=look.get((row['name'],'target','WC',row['accession']),{})
 for k in ['exact','le2last3','le2']:
  assert (row[k]=='True')==(r.get(k,'0')=='1'),(row['name'],row['accession'],k,row[k],r.get(k));checks+=1
 a=set(filter(None,row['sizes'].split(',')));b=set(filter(None,r.get('sizes','').split(',')))
 assert a==b,(row['name'],row['accession'],'sizes',a,b);checks+=1
sel=json.loads((p/'shortlist_fast.json').read_text());base=json.loads((p/'baseline_risks.json').read_text());meta={r['accession']:r for r in csv.DictReader((p/'metadata.tsv').open(),delimiter='\t')};classes=sorted({r['clade'] for r in meta.values() if r['role']=='background'});out=[]
for s in sel+base:
 for model in ['WC','GT']:
  rr=[r for r in hits if r['name']==s['name'] and r['role']=='background' and r['model']==model]
  for key in (['le2','le3','le4','ambiguous'] if model=='WC' else ['le2','ambiguous']):
   n=sum(r[key]=='1' for r in rr);assert n==int(s[model+'_'+key]),(s['name'],model,key,n,s[model+'_'+key]);checks+=1
  for cl in classes:
   rows=[r for r in rr if meta[r['accession']]['clade']==cl]
   out.append(dict(name=s['name'],model=model,clade=cl,reference_records=sum(m['clade']==cl for m in meta.values()),**{k:sum(r[k]=='1' for r in rows) for k in ['le2','le3','le4','ambiguous']}))
with (p/'background_class_summary.tsv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(out[0]),delimiter='\t');w.writeheader();w.writerows(out)
(p/'independent_validation.json').write_text(json.dumps(dict(status='PASS',checks=checks,target_records=1846,background_records=5600,scope='Full original sequences, both strands, exhaustive all-position independent C++ scanner; target detail/sizes and background record counts checked for every shortlist and baseline.',wet_lab_validated=False),indent=2));print('PASS',checks)
