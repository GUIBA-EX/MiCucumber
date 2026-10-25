"""Summarize taxonomic breadth separately from within-label sequence matching.

Uses frozen taxonomic labels without inferring missing taxonomy. Pair unions are
formed within each accession before labels are aggregated, so F and R must hit
the same reference. No primer sequences are changed.
"""
from pathlib import Path
import csv,json,collections,math
P=Path(__file__).resolve().parents[1]
def read(f,delimiter=','):return list(csv.DictReader(f.open(),delimiter=delimiter))
def write(f,rows):
 with f.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 panel=read(P/'results/matching/panel.csv');pairs=read(P/'results/current/primer_pairs.csv');old=read(P/'results/current/comparison.csv');hits=collections.defaultdict(set)
 for f in [P/'results/current/independent_hits.tsv',P/'results/xs/independent_hits.tsv']:
  for r in read(f,'\t'):
   if r['role']=='target' and r['model']=='WC':
    for flag in ['le2last3','exact']:
     if r[flag]=='1':hits[r['name'],flag].add(r['accession'])
 groups=collections.defaultdict(list)
 for r in panel:groups[r['organism']].append(r)
 for name,rr in groups.items():assert len({r['order'] for r in rr})==1,(name,'conflicting order labels')
 summary=[];detail=[];byorder=[]
 for c in old:
  component=[r['name'] for r in pairs if r['scheme']==c['scheme']];sets={flag:set().union(*(hits[n,flag] for n in component)) for flag in ['le2last3','exact']};states={}
  for name,rr in sorted(groups.items()):
   ids={r['accession'] for r in rr};cv=len(ids&sets['le2last3']);ex=len(ids&sets['exact']);assert ex<=cv
   state=dict(scheme=c['scheme'],taxon_label=name,order=rr[0]['order'],reference_count=len(ids),coverage_hits=cv,exact_hits=ex,coverage_state='full' if cv==len(ids) else 'partial' if cv else 'none',within_label_coverage_pct=100*cv/len(ids),within_label_exact_pct=100*ex/len(ids));states[name]=state;detail.append(state)
  for scope in ['all_target','non_Apodida']:
   scoped=[r for r in states.values() if scope=='all_target' or r['order']!='Apodida'];orders=sorted({r['order'] for r in scoped});o=[]
   for order in orders:
    rr=[r for r in scoped if r['order']==order];d=dict(scheme=c['scheme'],scope=scope,order=order,taxon_labels=len(rr),covered_labels=sum(r['coverage_hits']>0 for r in rr),exact_labels=sum(r['exact_hits']>0 for r in rr),fully_covered_labels=sum(r['coverage_state']=='full' for r in rr),uncovered_labels=sum(r['coverage_state']=='none' for r in rr));d.update(taxon_coverage_pct=100*d['covered_labels']/len(rr),taxon_exact_pct=100*d['exact_labels']/len(rr));byorder.append(d);o.append(d)
   summary.append(dict(scheme=c['scheme'],region=c['region'],scope=scope,taxon_labels=len(scoped),covered_labels=sum(r['coverage_hits']>0 for r in scoped),exact_labels=sum(r['exact_hits']>0 for r in scoped),taxon_coverage_pct=100*sum(r['coverage_hits']>0 for r in scoped)/len(scoped),taxon_exact_pct=100*sum(r['exact_hits']>0 for r in scoped)/len(scoped),order_balanced_coverage_pct=sum(r['taxon_coverage_pct'] for r in o)/len(o),order_balanced_exact_pct=sum(r['taxon_exact_pct'] for r in o)/len(o),represented_orders=len(o),covered_orders=sum(r['covered_labels']>0 for r in o),fully_covered_labels=sum(r['coverage_state']=='full' for r in scoped),partially_covered_labels=sum(r['coverage_state']=='partial' for r in scoped),uncovered_labels=sum(r['coverage_state']=='none' for r in scoped),mean_within_label_coverage_pct=sum(r['within_label_coverage_pct'] for r in scoped)/len(scoped),mean_within_label_exact_pct=sum(r['within_label_exact_pct'] for r in scoped)/len(scoped)))
   # Old 'coverage' is the average within-label sequence match, not taxon breadth.
   d=summary[-1];prefix='all_target_' if scope=='all_target' else ''
   assert math.isclose(d['mean_within_label_coverage_pct'],float(c[prefix+'coverage_pct']),abs_tol=1e-8)
   assert math.isclose(d['mean_within_label_exact_pct'],float(c[prefix+'exact_pct']),abs_tol=1e-8)
 out=P/'results/taxonomic_coverage';out.mkdir(exist_ok=True);write(out/'comparison.csv',summary);write(out/'by_order.csv',byorder);write(out/'by_taxon.csv',detail);write(out/'uncovered_taxa.csv',[r for r in detail if r['coverage_state']=='none']);write(P/'results/current/taxonomic_comparison.csv',summary)
 (out/'definitions.json').write_text(json.dumps(dict(version=1,taxon_unit='Frozen organism/name label; not necessarily a validated species',taxon_coverage='100 * labels with at least one covered reference / all labels in scope',taxon_exact='100 * labels with at least one paired zero-mismatch reference / all labels in scope',order_balanced_coverage='Arithmetic mean of within-order taxon coverage percentages, including zero-covered represented orders',order_balanced_exact='Arithmetic mean of within-order taxon exact percentages',coverage_hit='Both primers on the same accession: <=2 mismatches each, terminal 3 nt IUPAC-compatible',exact_hit='Both primers on the same accession: zero mismatches',scope_all_target='All frozen labels, including Apodida',scope_non_Apodida='Secondary comparison only; excludes Apodida',legacy_coverage_pct='Mean within-label haplotype matching percentage; retained in original CSV for reproduction compatibility',taxonomy_limit='Frozen order labels include Aspidochirotida; they do not establish seven-order modern taxonomic coverage'),indent=2)+'\n')
 print('PASS: 14 portfolios, two scopes, per-order/per-label coverage; legacy weighted metrics independently reconciled')
 for r in summary:
  if r['scope']=='all_target' and r['scheme'] in ['XS','SD','MD','LD','XLD']:
   print(r['scheme'],f"taxa {r['covered_labels']}/{r['taxon_labels']}={r['taxon_coverage_pct']:.2f}%; order-balanced={r['order_balanced_coverage_pct']:.2f}%; exact taxa={r['taxon_exact_pct']:.2f}%")
if __name__=='__main__':main()
