from pathlib import Path
import json,csv,itertools,shutil
p=Path(__file__).resolve().parent;q=p/'same_locus';solutions=json.loads((q/'portfolio_search.json').read_text());ol={r['id']:r for r in json.loads((q/'oligos.json').read_text())};rr=json.loads((q/'rank_pair_order.json').read_text());risk=list(csv.DictReader((q/'fast_risks.tsv').open(),delimiter='\t'));lookup={}
for r,a in zip(rr,risk):r.update({k:int(v) for k,v in a.items() if k!='index'});lookup[r['F_id'],r['R_id']]=r
arc=p/'pre_portfolio';arc.mkdir(exist_ok=True)
for n in ['shortlist_fast.json','target_summary.tsv','target_detail.tsv','pair_thermodynamics.tsv','independent_validation.json','background_class_summary.tsv','final_selected.json']:
 if not (arc/n).exists():shutil.copy2(p/n,arc/n)
short=json.loads((arc/'shortlist_fast.json').read_text());names={(s['F'],s['R']):s['name'] for s in short};chosen=[]
for locus in sorted({s['locus'] for s in solutions}):
 for mode in ['separate','pool']:
  options=[s for s in solutions if s['locus']==locus and s['mode']==mode and s['budget_per_model']==5];best=max(s['coverage'] for s in options)
  pool=[s for s in options if s['coverage']>=best-.005]
  selected=min(pool,key=lambda s:(len(s['F_ids'])+len(s['R_ids']),len(s['component_pairs']),-s['coverage'],s['total_degeneracy']))
  selected=dict(selected,name=locus+('-Pool' if mode=='pool' else '-Separate'));allowed_names=[]
  for a,b in selected['allowed_pairs']:
   r=lookup[a,b];key=(r['F'],r['R'])
   if key not in names:
    name=f'MC_combo_{len(names):03d}';names[key]=name;short.append(dict(r,name=name,group='combination_component',strict_gate=r['WC_le3']==r['GT_le2']==0))
   allowed_names.append(names[key])
  selected['allowed_pair_names']=allowed_names;selected['F_sequences']=[ol[k]['sequence'] for k in selected['F_ids']];selected['R_sequences']=[ol[k]['sequence'] for k in selected['R_ids']];selected['components']=[dict(F_id=a,R_id=b,F=ol[a]['sequence'],R=ol[b]['sequence']) for a,b in selected['component_pairs']];chosen.append(selected)
(p/'portfolio_selected.json').write_text(json.dumps(chosen,indent=2));(p/'shortlist_fast.json').write_text(json.dumps(short,indent=2));allpairs=short+json.loads((p/'baselines.json').read_text());(p/'independent_primers.tsv').write_text(''.join(f'{s["name"]}\t{s["F"]}\t{s["R"]}\n' for s in allpairs));print('total pairs',len(allpairs),'portfolios',len(chosen));print([(s['name'],s['coverage'],len(s['allowed_pairs'])) for s in chosen])
