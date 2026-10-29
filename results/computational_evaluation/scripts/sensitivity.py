from pathlib import Path
import csv,collections
p=Path(__file__).resolve().parents[1];r=p/'results'
def rd(n):return list(csv.DictReader((r/n).open()))
conf=collections.defaultdict(set)
for x in rd('barcode_collisions.csv'):conf[x['region']].update(x['accessions'].split(';'))
out=[]
for row in rd('panel_comparison.csv'):
 reg=row['region'];panel=list(csv.DictReader((p/f'inputs/results/species_qc/panel_{reg}.csv').open()));ids={x['accession'] for x in panel}
 if row['panel']=='common':
  ids=set.intersection(*[{x['accession'] for x in csv.DictReader((p/f'inputs/results/species_qc/panel_{z}.csv').open())} for z in ['XS','S','M','L','XL']])
 ids-=conf[reg];hp=p/f"inputs/results/current_primers/{reg}/{row['name']}_independent_hits.tsv"
 hits={x['accession']:x for x in csv.DictReader(hp.open(),delimiter='\t') if x['role']=='target' and x['model']=='WC'} if hp.exists() else {x['accession']:x for x in rd('new_curated_XS_hits.csv')}
 cv=sum(hits.get(a,{}).get('le2last3')=='1' for a in ids);ex=sum(hits.get(a,{}).get('exact')=='1' for a in ids)
 out.append(dict(name=row['name'],panel=row['panel'],removed=int(row['n'])-len(ids),n=len(ids),covered=cv,coverage_pct=100*cv/len(ids),exact=ex,exact_pct=100*ex/len(ids)))
with (r/'conflict_exclusion_sensitivity.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print('Sensitivity only: excluded all members of identical-insert conflicts; primary inputs unchanged')
