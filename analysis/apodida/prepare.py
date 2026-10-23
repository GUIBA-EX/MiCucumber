from pathlib import Path
import csv,json,os
p=Path(__file__).resolve().parent; rr=list(csv.DictReader((p/'diagnostic.tsv').open(),delimiter='\t'));groups={}
for r in rr:groups.setdefault((r['locus'],r['accession']),{})[r['side']]=r
pairs=[];seen=set()
for (loc,acc),d in groups.items():
 if set(d)!={'F','R'} or any(not d[x]['Tm'] for x in d):continue
 f,r=d['F'],d['R'];key=(loc,f['sequence'],r['sequence'])
 if key in seen:continue
 seen.add(key);pairs.append(dict(name='AP'+str(len(pairs)+1).zfill(3),locus=loc,F=f['sequence'],R=r['sequence'],source_accession=acc,AAAA=f['AAAA']=='True' or r['AAAA']=='True',Tm_difference=abs(float(f['Tm'])-float(r['Tm'])),hairpin_max=max(float(f['hairpin']),float(r['hairpin']))))
(p/'candidates.json').write_text(json.dumps(pairs,indent=2));(p/'independent_primers.tsv').write_text(''.join(f"{r['name']}\t{r['F']}\t{r['R']}\n" for r in pairs))
for n in ['target.fasta','background.fasta']:
 if not (p/n).exists():(p/n).symlink_to('../'+n)
print(len(pairs))
