from pathlib import Path
import json,csv,collections,shutil,html,hashlib
root=Path(__file__).resolve().parents[2];src=root/'outputs/MiCucumber_compact';p=root/'work/micucumber_round2/optimization';out=root/'outputs/MiCucumber_1_2pairs'
allrows=list(csv.DictReader((src/'all_tradeoffs.csv').open()));schemes={s['name']:s for s in json.load(open(src/'schemes.json'))};pairs={r['name']:r for r in json.load(open(p/'shortlist_fast.json'))};tax={r['accession']:r for r in csv.DictReader(open(p/'target_taxonomy.tsv'),delimiter='\t')};meta={r['accession']:r for r in csv.DictReader(open(p/'metadata.tsv'),delimiter='\t')};tab=collections.defaultdict(dict);hit=collections.defaultdict(dict)
for r in csv.DictReader(open(p/'target_detail.tsv'),delimiter='\t'):tab[r['name'],r['panel']][r['accession']]=r
for r in csv.DictReader(open(p/'independent_hits.tsv'),delimiter='\t'):hit[r['name'],r['role'],r['model']][r['accession']]=r
chosen=[]
for loc in ['v4opt','S','M','L']:
 for n in [1,2]:chosen.append(schemes[f'MiCucumber-{loc}_N{n}_B5_T{2 if n==2 and loc in ["v4opt","M"] else 1}'])
seq=[];miss=[];bg=[];checks=0
for s in chosen:
 for j,n in enumerate(s['pair_names'],1):seq.append(dict(version=s['locus'],pairs=s['count'],reaction=j,pair_id=n,F=pairs[n]['F'],R=pairs[n]['R'],scheme=s['name']))
 for pn in ['common','own_region']:
  groups=collections.defaultdict(list)
  for k,r in tab[s['pair_names'][0],pn].items():
   for n in s['pair_names']:
    for m in ['exact','le2last3']:assert (tab[n,pn][k][m]=='True')==(hit[n,'target','WC'].get(k,{}).get(m)=='1');checks+=1
   groups[r['organism']].append((k,any(tab[n,pn][k]['le2last3']=='True' for n in s['pair_names'])))
  for name,rr in groups.items():
   found=sum(v for k,v in rr)
   if found<len(rr):miss.append(dict(version=s['locus'],pairs=s['count'],panel=pn,organism=name,source_order=tax[rr[0][0]]['order'],haplotypes=len(rr),detected=found,status='fully_missed' if not found else 'partially_missed'))
 for mod,metric in [('WC','le3'),('WC','le4'),('GT','le2')]:
  for k in sorted({k for n in s['pair_names'] for k,r in hit[n,'background',mod].items() if r[metric]=='1'}):bg.append(dict(version=s['locus'],pairs=s['count'],model=mod,criterion=metric,accession=k,organism=meta[k]['organism'],clade=meta[k]['clade']))
def write(fn,rows):
 with (out/fn).open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
rows=[r for s in chosen for r in allrows if r['scheme']==s['name']];write('comparison.csv',rows);write('primer_pairs.csv',seq);write('missed_taxa.csv',miss);write('offtargets.csv',bg)
for loc in ['v4opt','S','M','L']:write(loc+'_1_2pairs.csv',[r for r in seq if r['version']=='MiCucumber-'+loc])
(out/'selection.json').write_text(json.dumps(chosen,indent=2))
with (out/'primers.fasta').open('w') as f:
 for r in seq:
  for side in ['F','R']:f.write(f">{r['version']}|{r['pairs']}pairs|PCR{r['reaction']}|{side}|{r['pair_id']}\n{r[side]}\n")
q=root/'work/micucumber_1_2pairs/thermal';q.mkdir(exist_ok=True);(q/'shortlist_fast.json').write_text(json.dumps([pairs[n] for n in sorted({r['pair_id'] for r in seq})]));(q/'baselines.json').write_text('[]');shutil.copy2(p/'thermal/thermal_pairs.py',q/'thermal_pairs.py')
(out/'validation.json').write_text(json.dumps(dict(status='target_union_PASS_thermal_pending',checks=checks,schemes=8,scope='Exhaustive subset selection from previously independently verified 96-pair pool; Apodida excluded from objective; <=5 WC3 and GT2 background records; separate PCRs only; no new sequences and no wet-lab validation',source_hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [src/'all_tradeoffs.csv',p/'target_detail.tsv',p/'independent_hits.tsv']}),indent=2))
print('8 schemes exported;',checks,'checks')
for r in rows:
 if r['panel']=='common':print(r['locus'],r['count'],r['non_Apodida_coverage_pct'],r['non_Apodida_exact_pct'],r['WC_le3'],r['GT_le2'],r['WC_le4'])
