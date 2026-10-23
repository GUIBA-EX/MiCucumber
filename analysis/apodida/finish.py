from pathlib import Path
import json,csv,sys,zipfile
p=Path(__file__).resolve().parent;o=p.parents[1]/'results'
import primer3
ss=json.loads((p/'selected.json').read_text());out=[]
for s in ss:
 kw=dict(mv_conc=50,dv_conc=1.5,dntp_conc=.6,dna_conc=50)
 mx=max(primer3.calc_homodimer(s['F'],**kw).tm,primer3.calc_homodimer(s['R'],**kw).tm,primer3.calc_heterodimer(s['F'],s['R'],**kw).tm)
 assert mx<55,(s['name'],mx)
 out.append(dict(name=s['name'],scheme=s['scheme'],max_dimer_Tm=mx,AAAA=s['AAAA']))
with (o/'apodida_thermodynamics.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print('PASS',len(out),'pair structure checks')
