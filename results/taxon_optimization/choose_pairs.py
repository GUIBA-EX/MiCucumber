from pathlib import Path
import sys,collections
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'work/micucumber_terminal'))
from common import *
p=root/'work/micucumber_taxon_optimization';out=root/'outputs/MiCucumber_taxon_optimization';pairs=json.loads((p/'pairs.json').read_text());h=collections.defaultdict(lambda:collections.defaultdict(list))
for f in [p/'reused_background_sites.tsv',p/'sites/background_sites.tsv']:
 for n,acc,ori,gt,pos,mm,last in csv.reader(f.open(),delimiter='\t'):h[n,int(gt)][acc,ori].append((int(pos),int(mm),int(last)))
for i,r in enumerate(pairs):
 for gt,lim,col,strict in [(0,3,'WC3',False),(1,2,'GT2',False),(0,4,'WC4',False),(0,2,'strict_WC',True),(1,2,'strict_GT',True)]:
  f,b=h[r['F_id'],gt],h[r['R_id'],gt];r[col]=len({acc for acc,ori in f.keys()&b.keys() if any(fm<=lim and rm<=lim and (not strict or not fl and not rl) and 0<=rp-fp-len(r['F'])<=1000 for fp,fm,fl in f[acc,ori] for rp,rm,rl in b[acc,ori])})
 if i%1500==0:print('paired background',i,flush=True)
write(out/'candidate_comparison.csv',[{k:v for k,v in r.items() if k not in ['cv','ex']} for r in pairs]);chosen=[];audit=[];tested={}
for reg in ['S','M','L','XL']:
 for limit in [20,100,500]:
  ranked=sorted([r for r in pairs if r['region']==reg and r['WC3']<=limit and r['GT2']<=limit and max(r['strict_WC'],r['strict_GT'])<=50],key=lambda r:(r['pred_order_coverage'],r['pred_order_exact'],r['pred_taxon_coverage'],-r['degeneracy_F']-r['degeneracy_R']),reverse=True)
  for r in ranked:
   key=(r['F'],r['R'])
   if key not in tested:
    # Cheap rejection before testing every intra-/inter-primer variant dimer.
    ft,rt=oligo_thermal(r['F']),oligo_thermal(r['R']);pre=all(max(f[2],b[2])<55 and abs((f[0]+f[1]-b[0]-b[1])/2)<=5 for f,b in zip(ft,rt))
    ok,reports=thermal(r['F'],r['R']) if pre else (False,[]);tested[key]=(ok,reports)
    audit.append(dict(region=reg,F=r['F'],R=r['R'],thermal_pass=ok,precheck_pass=pre))
   ok,reports=tested[key]
   if ok:
    d={k:v for k,v in r.items() if k not in ['cv','ex']};d.update(background_limit=limit,thermal=reports);chosen.append(d);print('SELECT',reg,limit,r['pred_order_coverage'],r['pred_order_exact'],r['degeneracy_F'],r['degeneracy_R'],flush=True);break
  else:print('NO FEASIBLE',reg,limit,flush=True)
unique={}
for r in chosen:
 key=(r['region'],r['F'],r['R'])
 if key not in unique:unique[key]=dict(r,name=r['region']+'D-T'+str(len(unique)+1))
selected=list(unique.values());(p/'selection.json').write_text(json.dumps(selected,indent=2));(p/'tier_selection.json').write_text(json.dumps(chosen,indent=2));write(out/'thermal_search_audit.csv',audit)
v=p/'verify';v.mkdir(exist_ok=True)
for role in ['target','background']:
 f=v/(role+'.fasta')
 if not f.exists():f.symlink_to(root/'work/micucumber_terminal'/(role+'.fasta'))
(v/'independent_primers.tsv').write_text(''.join(f"{r['name']}\t{r['F']}\t{r['R']}\n" for r in selected));print('FINAL',len(selected),'testedthermal',len(tested),flush=True)
