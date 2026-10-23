from pathlib import Path
import json,csv,itertools,sys,collections,functools
from Bio.Data.IUPACData import ambiguous_dna_values as I
p=Path(__file__).resolve().parent
import primer3
@functools.lru_cache(None)
def variants(q):return [''.join(t) for t in itertools.product(*(I[c] for c in q))]
@functools.lru_cache(None)
def dimer(a,b,c):
 kw=dict(mv_conc=50,dv_conc=1.5,dntp_conc=.6,dna_conc=c)
 return (primer3.calc_homodimer(a,**kw) if a==b else primer3.calc_heterodimer(a,b,**kw)).tm
rows=[]
for s in json.loads((p/'portfolio_selected.json').read_text()):
 if s['mode']!='pool':continue
 for scenario in ['unique_variant50nM','direction200nM_equal_oligo']:
  conc=collections.defaultdict(float);side={}
  for direction in ['F','R']:
   qs=s[direction+'_sequences']
   for q in qs:
    vs=variants(q)
    for v in vs:
     side.setdefault(v,set()).add(direction)
     if scenario=='unique_variant50nM':conc[v]=50
     else:conc[v]+=200/len(qs)/len(vs)
  vs=sorted(conc);best=(-1e9,'','');hp=-1e9;tms=[]
  for v in vs:
   kw=dict(mv_conc=50,dv_conc=1.5,dntp_conc=.6,dna_conc=conc[v]);hp=max(hp,primer3.calc_hairpin(v,**kw).tm);tms.append(primer3.calc_tm(v,**kw))
  for i,a in enumerate(vs):
   for b in vs[i:]:
    tm=dimer(a,b,round(max(conc[a],conc[b]),9))
    if tm>best[0]:best=(tm,a,b)
  rows.append(dict(name=s['name'],scenario=scenario,n_unique_concrete_variants=len(vs),Tm_min=min(tms),Tm_max=max(tms),hairpin_max=hp,all_pool_dimer_max=best[0],worst_sequence_A=best[1],worst_sequence_B=best[2],max_variant_nM=max(conc.values()),unequal_concentration_rule='Primer3 scalar concentration=max(conc_A,conc_B), approximate conservative sensitivity; not an experimental recipe',structure_gate=max(hp,best[0])<55))
  print(s['name'],scenario,'variants',len(vs),'max_dimer',best[0],flush=True)
with (p/'portfolio_thermodynamics.tsv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
