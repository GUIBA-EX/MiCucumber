from pathlib import Path
import csv,json,subprocess,collections,sys,math
p=Path(__file__).resolve().parent;root=p.parents[1];sys.path.insert(0,str(root/'outputs/MiCucumber/scripts'))
from xs_raw_helpers import fa,rc,scan
out=root/'outputs/MiCucumber_taxon_optimization';sel=json.loads((p/'selection.json').read_text());v=p/'verify';src=root/'work/micucumber_nondegenerate/independent_scan.cpp';subprocess.run(['c++','-O3','-std=c++17',str(src),'-o',str(v/'independent_scan')],check=True);subprocess.run([str(v/'independent_scan'),str(v)],check=True)
h=collections.defaultdict(set)
for r in csv.DictReader((v/'independent_hits.tsv').open(),delimiter='\t'):
 for flag in ['exact','le2last3','le2','le3','le4']:
  if r[flag]=='1':h[r['name'],r['role'],r['model'],flag].add(r['accession'])
panel=list(csv.DictReader((root/'work/micucumber_terminal/panel.csv').open()));labels=collections.defaultdict(list)
for r in panel:labels[r['organism']].append(r)
orders=sorted({r['order'] for r in panel});target=fa(root/'work/micucumber_terminal/target.fasta');background=fa(root/'work/micucumber_terminal/background.fasta');comparison=[];byorder=[];labelrows=[];templates=[];checks=[]
for x in sel:
 name=x['name'];F,R=x['F'],x['R'];actual=collections.defaultdict(set)
 for role,db in [('target',{r['accession']:target[r['accession']] for r in panel}),('background',background)]:
  for acc,s in db.items():
   for model in (['WC'] if role=='target' else ['WC','GT']):
    cv=False;ex=False;found=[]
    for orientation,t in [('+',s),('-',rc(s))]:
     ff=scan(t,F,False,2,model=='GT');rr=scan(t,R,True,2,model=='GT')
     for fp,fm,fl in ff:
      for rp,rm,rl in rr:
       inner=rp-fp-len(F);total=rp+len(R)-fp
       valid=(inner>=50 and 150<=total<=500) if role=='target' else 0<=inner<=1000
       if not valid:continue
       ex|=fm==0 and rm==0;cv|=not fl and not rl
       if role=='target' and not fl and not rl:found.append((fm+rm,total,fp,rp,orientation,t[fp:fp+len(F)],rc(t[rp:rp+len(R)])))
    if ex:actual[role,model,'exact'].add(acc)
    if cv:actual[role,model,'le2last3'].add(acc)
    if found:
     a=min(found);templates.append(dict(name=name,accession=acc,F_template=a[5],R_template=a[6],product_bp=a[1],orientation=a[4]))
  print('PYTHON',name,role,'done',flush=True)
 ids={r['accession'] for r in panel}
 for flag in ['exact','le2last3']:assert actual['target','WC',flag]==h[name,'target','WC',flag]&ids,(name,flag)
 for model in ['WC','GT']:
  for flag in ['exact','le2last3']:assert actual['background',model,flag]==h[name,'background',model,flag],(name,model,flag)
 checks.append(dict(name=name,target_checks=len(ids)*2,background_set_checks=4,disagreements=0))
 row={k:x[k] for k in ['name','region','F','R','degeneracy_F','degeneracy_R']};obs=[]
 for lab,rr in sorted(labels.items()):
  ids={r['accession'] for r in rr};cv=len(ids&h[name,'target','WC','le2last3']);ex=len(ids&h[name,'target','WC','exact']);d=dict(name=name,taxon_label=lab,order=rr[0]['order'],reference_count=len(ids),coverage_hits=cv,exact_hits=ex,coverage_state='full' if cv==len(ids) else 'partial' if cv else 'none');obs.append(d);labelrows.append(d)
 for flag,col in [('coverage_hits','coverage'),('exact_hits','exact')]:
  row['taxon_'+col+'_pct']=100*sum(r[flag]>0 for r in obs)/len(obs);row['order_'+col+'_pct']=sum(100*sum(r[flag]>0 for r in obs if r['order']==o)/sum(r['order']==o for r in obs) for o in orders)/len(orders)
 row['covered_labels']=sum(r['coverage_hits']>0 for r in obs);row['exact_labels']=sum(r['exact_hits']>0 for r in obs);row['fully_covered_labels']=sum(r['coverage_state']=='full' for r in obs)
 for o in orders:
  rr=[r for r in obs if r['order']==o];byorder.append(dict(name=name,order=o,labels=len(rr),covered_labels=sum(r['coverage_hits']>0 for r in rr),exact_labels=sum(r['exact_hits']>0 for r in rr)))
 for model,flag,col in [('WC','le3','WC3'),('GT','le2','GT2'),('WC','le4','WC4'),('WC','le2last3','strict_WC'),('GT','le2last3','strict_GT')]:row[col]=len(h[name,'background',model,flag]);assert row[col]==x[col],(name,col,row[col],x[col])
 row['prediction_coverage_delta_pp']=row['order_coverage_pct']-x['pred_order_coverage'];row['prediction_exact_delta_pp']=row['order_exact_pct']-x['pred_order_exact'];comparison.append(row)
 print('CONFIRMED',name,row['order_coverage_pct'],row['order_exact_pct'],flush=True)
def write(f,rr):
 with f.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rr[0]),lineterminator='\n');w.writeheader();w.writerows(rr)
for name,rr in [('verified_comparison.csv',comparison),('by_order.csv',byorder),('by_taxon.csv',labelrows),('verified_base_templates.csv',templates),('independent_checks.csv',checks)]:write(out/name,rr)
(out/'verification.json').write_text(json.dumps(dict(target_checks=sum(r['target_checks'] for r in checks),background_set_checks=sum(r['background_set_checks'] for r in checks),disagreements=0,methods=['C++ exhaustive raw-sequence paired scan','Python bit-parallel raw-sequence paired scan'],background_metric_checks=len(sel)*5,background_disagreements=0),indent=2)+'\n')
print('ALL VERIFIED',len(sel),flush=True)
