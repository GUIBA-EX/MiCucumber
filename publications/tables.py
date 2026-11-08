"""Generate manuscript tables directly from the released scientific CSV files."""
from pathlib import Path
import csv,re,statistics
ROOT=Path(__file__).resolve().parents[1]
def read(path):
 with (ROOT/path).open() as handle:return list(csv.DictReader(handle))
def table(headers,rows):
 return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(map(str,row))+' |' for row in rows)
def generated_tables():
 base='results/computational_evaluation/results/'
 panel=read(base+'panel_comparison.csv');own=[r for r in panel if r['panel']=='own'];common=[r for r in panel if r['panel']=='common'];n=common[0]['n']
 metrics={r['name']:r for r in read('results/current_primers/comparison.csv')};coords=read('figures/current_region_coordinates.csv')
 resolution=read(base+'resolution.csv');nearest=read(base+'nearest_neighbors.csv');folds=read(base+'cv_summary.csv')
 pairs=read('sequences/primer_pairs.csv');markers=read('markers/12S_COI/candidates.csv')
 tables={}
 tables[1]=[table(['Window','F positions','R positions','Span bp','Available species'],[[r['locus'],f"{r['F_start']}–{r['F_end']}",f"{r['R_start']}–{r['R_end']}",r['reference_span_bp'],next(x['n'] for x in own if x['region']==r['locus'])] for r in coords])]
 tables[2]=[table(['Assay','Own-panel N','Covered','Exact','Strict background hits¹'],[[r['name'],r['n'],r['covered'],r['exact'],metrics[r['name']]['strict_WC']+' / '+metrics[r['name']]['strict_GT']] for r in own])]
 tables[3]=[table(['Assay','Covered','Exact','Covered + unique'],[[r['name'],r['covered']+'/'+n,r['exact']+'/'+n,r['covered_identity_unique']+'/'+n] for r in common])]
 rr=[]
 for r in resolution:
  if r['panel']!='own':continue
  nn=[int(x['nearest_edit_distance']) for x in nearest if x['region']==r['region']]
  rr.append([r['region'],r['n'],r['identity_unique_species'],r['insert_min']+'–'+r['insert_max'],statistics.median(nn),sum(x<=1 for x in nn)])
 tables[4]=[table(['Window','N','Unique','Insert bp','Median nearest edit','Nearest ≤1'],rr)]
 tables[5]=[table(['Window','Test N','Covered','Exact'],[[r['region'],r['n'],f"{r['covered']} ({float(r['coverage_pct']):.2f}%)",f"{r['exact']} ({float(r['exact_pct']):.2f}%)"] for r in folds])]
 tables[6]=[table(['Gene','Assay','Span bp','Covered/N','Exact/N','Strict background hits¹'],[[r['gene'],r['name'],r['span'],r['covered']+'/'+r['evaluable'],r['exact']+'/'+r['evaluable'],r['WC']+'/'+r['GT']] for r in markers])]
 headers=['Assay','F, 5′–3′','R, 5′–3′','Deg F/R']
 tables[7]=[table(headers,[[r['name'],r['F'],r['R'],r['degeneracy_F']+'/'+r['degeneracy_R']] for r in pairs]),table(headers,[[r['gene']+' '+r['name'],r['F'],r['R'],r['deg_F']+'/'+r['deg_R']] for r in markers])]
 diagnostic=read('results/anth28s_evaluation/results/mismatch_summary.csv')
 def value(gene,name,threshold,terminal=0,role='target'):
  return next(r['matched'] for r in diagnostic if r['gene']==gene and r['name']==name and r['threshold']==str(threshold) and r['terminal3_required']==str(terminal) and r['role']==role)
 rr=[]
 for gene,name in dict.fromkeys((r['gene'],r['name']) for r in diagnostic):
  n=next(r['n'] for r in diagnostic if r['gene']==gene and r['name']==name and r['role']=='target')
  rr.append([gene,name,n,*[value(gene,name,k) for k in (0,1,2)],value(gene,name,2,1),value(gene,name,2,0,'background')])
 tables[8]=[table(['Gene','Assay','Species N','≤0','≤1','≤2','≤2 + terminal 3','Background ≤2'],rr)]
 identity=read('results/anth28s_evaluation/results/identity_summary.csv')
 tables[9]=[table(['Gene','Window','Unambiguous N','Unique species','Identical pairs','Insert bp'],[[r['gene'],r['window'],r['n'],r['unique_species'],r['identical_species_pairs'],r['insert_min']+'–'+r['insert_max']] for r in identity])]
 return tables
def synchronize(text):
 for number,expected in generated_tables().items():
  pattern=rf'(^## Table {number}\..*?)(?=^## Table |\Z)'
  match=re.search(pattern,text,re.M|re.S)
  if not match:raise ValueError(f'Missing Table {number}')
  section=match[0];blocks=list(re.finditer(r'^\|.*(?:\n\|.*)*',section,re.M))
  if len(blocks)!=len(expected):raise ValueError(f'Table {number}: unexpected table blocks')
  for block,new in reversed(list(zip(blocks,expected))):section=section[:block.start()]+new+section[block.end():]
  text=text[:match.start()]+section+text[match.end():]
 return text
