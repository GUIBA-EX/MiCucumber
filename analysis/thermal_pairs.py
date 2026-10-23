from pathlib import Path
import json,itertools,sys,csv,functools
from Bio.Data.IUPACData import ambiguous_dna_values as I
p=Path(__file__).resolve().parent

import primer3
@functools.lru_cache(None)
def variants(q):return [''.join(x) for x in itertools.product(*(I[c] for c in q))]
@functools.lru_cache(None)
def single(q,conc):
 vs=variants(q);kw=dict(mv_conc=50,dv_conc=1.5,dntp_conc=.6,dna_conc=conc)
 tm=[primer3.calc_tm(v,**kw) for v in vs];hp=max(primer3.calc_hairpin(v,**kw).tm for v in vs);homo=max(primer3.calc_homodimer(v,**kw).tm for v in vs)
 cross=max(primer3.calc_heterodimer(a,b,**kw).tm for a in vs for b in vs)
 return dict(tm_min=min(tm),tm_max=max(tm),hairpin_max=hp,homodimer_max=homo,same_side_heterodimer_max=cross)
sel=json.loads((p/'shortlist_fast.json').read_text())+json.loads((p/'baselines.json').read_text());out=[]
for s in sel:
 F,R=s['F'],s['R'];fv,rv=variants(F),variants(R)
 for scenario in ['variant50nM','direction200nM_split']:
  fc=50 if scenario=='variant50nM' else 200/len(fv);rc=50 if scenario=='variant50nM' else 200/len(rv)
  # Primer3 accepts one strand concentration. Unequal F/R sensitivity uses larger concentration conservatively, explicitly reported.
  cross=max(primer3.calc_heterodimer(a,b,mv_conc=50,dv_conc=1.5,dntp_conc=.6,dna_conc=max(fc,rc)).tm for a in fv for b in rv)
  row=dict(name=s['name'],scenario=scenario,F_degeneracy=len(fv),R_degeneracy=len(rv),F_variant_nM=fc,R_variant_nM=rc,cross_concentration_nM=max(fc,rc),FR_heterodimer_max=cross)
  for side,q,c in [('F',F,fc),('R',R,rc)]:row.update({side+'_'+k:v for k,v in single(q,c).items()})
  row['AAAA_any_variant']=any('AAAA' in v for v in fv+rv);out.append(row)
 print(s['name'],'done',flush=True)
with (p/'pair_thermodynamics.tsv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(out[0]),delimiter='\t');w.writeheader();w.writerows(out)
