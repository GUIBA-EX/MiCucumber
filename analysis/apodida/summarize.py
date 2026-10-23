from pathlib import Path
import csv,json,collections
p=Path(__file__).resolve().parent;r=p.parent;o=r.parent/'results';o.mkdir(exist_ok=True)
def read(path):return list(csv.DictReader(path.open(),delimiter='\t'))
c=json.loads((p/'candidates.json').read_text());hh=read(p/'independent_hits.tsv');old=read(r/'independent_hits.tsv');meta={x['accession']:x for x in read(r/'metadata.tsv')};tax={x['accession']:x['order'] for x in read(r/'target_taxonomy.tsv')};panel=json.loads((r/'common_panel.json').read_text())['ids'];counts=collections.Counter(meta[k]['organism'] for k in panel);w={k:1/len(counts)/counts[meta[k]['organism']] for k in panel};apo={k for k in panel if tax[k]=='Apodida'}
def hit(rows,n,role,model,key):return {x['accession'] for x in rows if x['name'] in n and x['role']==role and x['model']==model and x[key]=='1'}
results=[];seq=[]
for s in json.loads((r/'portfolio_selected.json').read_text()):
 if s['mode']!='separate':continue
 names=s['allowed_pair_names'];covered=hit(old,names,'target','WC','le2last3');wc=hit(old,names,'background','WC','le3');gt=hit(old,names,'background','GT','le2');wc4=hit(old,names,'background','WC','le4');selected=[]
 pool=[x for x in c if x['locus']==s['locus'] and x['hairpin_max']<55 and x['Tm_difference']<=5]
 while pool:
  ranked=[]
  for x in pool:
   name=[x['name']];t=hit(hh,name,'target','WC','le2last3');a=hit(hh,name,'background','WC','le3');b=hit(hh,name,'background','GT','le2')
   if len(wc|a)>5 or len(gt|b)>5:continue
   gain=sum(w.get(k,0) for k in t-covered);apgain=len((t-covered)&apo)
   if gain>0:ranked.append((apgain,gain,-len(a|b),x['name'],x,t,a,b))
  if not ranked:break
  *_,x,t,a,b=max(ranked,key=lambda z:z[:4]);selected.append(x);covered|=t;wc|=a;gt|=b;wc4|=hit(hh,[x['name']],'background','WC','le4');pool.remove(x)
 results.append(dict(scheme=s['name']+'-Apodida',additional_pairs=len(selected),total_pairs=4+len(selected),coverage_pct=100*sum(w[k] for k in panel if k in covered),Apodida_panel_records=len(apo),Apodida_hit_records=len(apo&covered),Apodida_coverage_pct=100*sum(w[k] for k in apo&covered)/sum(w[k] for k in apo),WC3=len(wc),GT2=len(gt),WC4=len(wc4)))
 for x in selected:seq.append(dict(scheme=s['name']+'-Apodida',**x))
for name,data in [('apodida_comparison.csv',results),('apodida_additional_pairs.csv',seq)]:
 with (o/name).open('w',encoding='utf-8-sig',newline='') as f:
  wr=csv.DictWriter(f,fieldnames=list(data[0]));wr.writeheader();wr.writerows(data)
(p/'selected.json').write_text(json.dumps(seq,indent=2));print(json.dumps(results,indent=2));print('selected',len(seq))
