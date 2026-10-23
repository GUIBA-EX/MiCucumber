from pathlib import Path
import json,shutil
p=Path(__file__).resolve().parent;rr=json.loads((p/'v4_refined_pairs.json').read_text());assert rr
archive=p/'initial_round';archive.mkdir(exist_ok=True)
for name in ['shortlist_fast.json','target_summary.tsv','target_detail.tsv','common_panel.json','pair_thermodynamics.tsv','independent_validation.json','background_class_summary.tsv','independent_hits.tsv']:
 if not (archive/name).exists():shutil.copy2(p/name,archive/name)
ss=json.loads((archive/'shortlist_fast.json').read_text());existing={(s['F'],s['R']) for s in ss};pool=[r for r in rr if (r['F'],r['R']) not in existing];chosen=[]
for ranking in [sorted(pool,key=lambda r:(r['WC_le3']+r['GT_le2'],-r['coverage'],r['WC_le4'])),sorted(pool,key=lambda r:(-r['coverage'],r['WC_le3']+r['GT_le2'],r['WC_le4']))]:
 n=0
 for r in ranking:
  if (r['F'],r['R']) in {(s['F'],s['R']) for s in chosen}:continue
  chosen.append(r);n+=1
  if n==4:break
for i,r in enumerate(chosen,1):ss.append(dict(r,name=f'MC_v4_refined_{i}',group='v4_refined',band='short',strict_gate=r['WC_le3']==r['GT_le2']==0))
(p/'shortlist_fast.json').write_text(json.dumps(ss,indent=2));ss+=json.loads((p/'baselines.json').read_text());(p/'independent_primers.tsv').write_text(''.join(f'{s["name"]}\t{s["F"]}\t{s["R"]}\n' for s in ss));print('refined appended',len(chosen),'all with baselines',len(ss));print(chosen[:2])
