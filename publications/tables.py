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
 span={r['locus']:r['reference_span_bp'] for r in coords}
 tables[1]=[table(['Assay','Span (bp)','Covered','Exact','Covered + unique','Strict background¹'],[
  [r['name'],span[r['region']],r['covered']+'/'+n,r['exact']+'/'+n,r['covered_identity_unique']+'/'+n,
   metrics[r['name']]['strict_WC']+' / '+metrics[r['name']]['strict_GT']] for r in common])]
 tables[2]=[table(['Window','F positions','R positions','Span bp','Available species'],[[r['locus'],f"{r['F_start']}–{r['F_end']}",f"{r['R_start']}–{r['R_end']}",r['reference_span_bp'],next(x['n'] for x in own if x['region']==r['locus'])] for r in coords])]
 tables[3]=[table(['Assay','Own-panel N','Covered','Exact','Strict background hits¹'],[[r['name'],r['n'],r['covered'],r['exact'],metrics[r['name']]['strict_WC']+' / '+metrics[r['name']]['strict_GT']] for r in own])]
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
 gains=read('results/lineage_evaluation/lineage_gains.csv')
 tables[10]=[table(['Assay','Added oligos','Covered','Exact','Added background'],[
  [r['assay'],r['added_oligos'],f"{r['base_covered']} → {r['covered']}",
   f"{r['base_exact']} → {r['exact']}",' / '.join(r['new_'+k] for k in ('strict_WC','strict_GT','WC3','GT2','WC4'))]
  for r in gains if r['panel']=='available'])]
 order_rows=read('results/lineage_evaluation/by_order.csv')
 selected={r['assay']:{} for r in order_rows}
 for row in order_rows:
  if row['panel']=='available':selected[row['assay']][row['order']]=row
 def changes(base,pool,order):
  return [f"{selected[base][order][k]} → {selected[pool][order][k]}" for k in ('covered','exact','covered_unique')]
 tables[11]=[table(['Order','N','S covered','S exact','S covered + unique','L covered','L exact','L covered + unique'],[
  [order,row['n'],*changes('SD','SD-Dendrochirotida',order),*changes('LD','LD-Elasipodida',order)]
  for order,row in selected['SD'].items()])]
 external={(r['gene'],r['assay'],r['role']):r for r in read('results/external_panel/summary.csv')}
 rows=[]
 for gene,assay in [('16S','SD'),('16S','SD-Dendrochirotida'),('16S','LD'),('16S','LD-Elasipodida'),
                    ('12S','XLD'),('COI','XSD'),('COI','L'),('COI','LD')]:
  target=external[gene,assay,'target'];background=external[gene,assay,'background']
  target_counts=[f"{target[k]}/{target['evaluable']}" if int(target['evaluable']) else 'NA'
                 for k in ('exact','strict','limited')]
  background_counts=' / '.join(background[k] for k in ('strict','limited','strict_GT'))
  rows.append([gene,assay,*target_counts,background['evaluable'],background_counts])
 tables[12]=[table(['Gene','Assay','Exact','Strict','Limited','Background N','Background hits¹'],rows)]
 comparisons=read('results/benchmark_revision/marker_comparison.csv')
 tables[13]=[table(['Gene','Assay','Span (bp)','Covered','Exact','Covered + unique','Strict background¹'],[
  [r['gene'],r['assay'],r['span'],*[r[key]+'/'+r['n'] for key in ('covered','exact','covered_unique')],
   r['background_wc']+' / '+r['background_gt']]
  for r in comparisons if r['panel']=='all_windows' and r['assay'].endswith('D')])]
 rank=read('results/benchmark_revision/resolution_by_rank.csv')
 tables[14]=[table(['Window','Species','Genus','Family','Shared inserts'],[
  [r['window'],r['species_unique']+'/'+r['barcode_groups'],r['genus_unique']+'/'+r['genus_evaluable'],
   r['family_unique']+'/'+r['family_evaluable'],r['conflicting_groups']] for r in rank])]
 changes=read('results/benchmark_revision/limited_mismatch_changes.csv')
 tables[15]=[table(['Panel','Gene and assay','Added target species','Accession','Position','Added background'],[
  [r['panel'],r['gene']+' '+r['assay'],'*'+r['species']+'*',r['accession'],r['position'],
   r['added_background']+'/'+r['background_n']] for r in changes])]
 return tables
def synchronize(text):
 for number,expected in generated_tables().items():
  pattern=rf'(^###? Table {number}\..*?)(?=^## |^### Table |\Z)'
  match=re.search(pattern,text,re.M|re.S)
  if not match:raise ValueError(f'Missing Table {number}')
  section=match[0];blocks=list(re.finditer(r'^\|.*(?:\n\|.*)*',section,re.M))
  if len(blocks)!=len(expected):raise ValueError(f'Table {number}: unexpected table blocks')
  for block,new in reversed(list(zip(blocks,expected))):section=section[:block.start()]+new+section[block.end():]
  text=text[:match.start()]+section+text[match.end():]
 return text
