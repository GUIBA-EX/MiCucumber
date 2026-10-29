"""Build the latest computational preprint. Run from this repository:
python3 publications/build_preprint.py
Dependencies: reportlab, matplotlib. Standard-library calculations use frozen results.
"""
from pathlib import Path
import csv,json,hashlib,subprocess,statistics,html,re,sys,tempfile,shutil,os
repo=Path(__file__).resolve().parents[1];name=repo.name
if name not in ['MiCucumber','MiLily','MiUrchin']:raise ValueError('Place in <repository>/publications/')
out=repo/'publications';out.mkdir(exist_ok=True);pack=repo/'results/computational_evaluation';res=pack/'results'
def rd(f):return list(csv.DictReader(f.open()))
def table(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(map(str,r))+' |' for r in rows)
info={'MiCucumber':('sea cucumbers','Holothuroidea','AB525437.1',1848,5600,174),'MiLily':('crinoids','Crinoidea','AF049132.1',269,7177,128),'MiUrchin':('sea urchins','Echinoidea','NC_001453.1',1401,6045,165)}
taxon,clade,ref,nt,nb,ns=info[name];lily=name=='MiLily';cmp=rd(res/'panel_comparison.csv');resol=rd(res/'resolution.csv');cv=rd(res/'cv_summary.csv');nearest=rd(res/'nearest_neighbors.csv');pairs=rd(repo/'sequences/primer_pairs.csv');co=rd(repo/'figures/current_region_coordinates.csv');coords={x['locus']:x for x in co};n=next(x['n'] for x in cmp if x['panel']=='common');conflicts=rd(res/'barcode_collisions.csv');own={x['name']:x for x in cmp if x['panel']=='own'};bestcv=max([x for x in cmp if x['panel']=='common'],key=lambda x:int(x['covered']));bestexact=max([x for x in cmp if x['panel']=='common'],key=lambda x:int(x['exact']))
# Recreate figures in a private build directory; do not rewrite the frozen analysis figures.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
figdir=out/'figures';figdir.mkdir(exist_ok=True)
plt.rcParams.update({'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
def savefig(label):
 plt.tight_layout();plt.savefig(figdir/f'{label}.png',dpi=220);plt.close()
a=[x for x in cmp if x['panel']=='common'];xs=list(range(len(a)));fig,ax=plt.subplots(figsize=(8.2,3.6));ax.bar([x-.18 for x in xs],[float(x['coverage_pct']) for x in a],.36,color='#3287a8',label='Compatible');ax.bar([x+.18 for x in xs],[float(x['exact_pct']) for x in a],.36,color='#e7a54c',label='Exact paired match');ax.set_xticks(xs,[x['name'] for x in a]);ax.set(ylim=(0,108),ylabel='Common-panel species (%)');ax.legend(fontsize=8);savefig('common_panel')
a=[x for x in resol if x['panel']=='own'];fig,ax=plt.subplots(figsize=(7.2,3.5));ax.bar([x['region'] for x in a],[float(x['unique_pct']) for x in a],color=['#51adac','#399da9','#ecb24c','#488ec0','#9867bc']);ax.set(ylim=(0,110),ylabel='Identity-unique representatives (%)')
for i,x in enumerate(a):ax.text(i,float(x['unique_pct'])+1,f"{x['identity_unique_species']}/{x['n']}",ha='center',fontsize=9)
savefig('resolution')
a=cv;xs=list(range(len(a)));fig,ax=plt.subplots(figsize=(7.2,3.5));ax.bar([x-.18 for x in xs],[float(x['coverage_pct']) for x in a],.36,color='#3287a8',label='Held-out compatible');ax.bar([x+.18 for x in xs],[float(x['exact_pct']) for x in a],.36,color='#e7a54c',label='Held-out exact');ax.set_xticks(xs,[x['region'] for x in a]);ax.set(ylim=(0,108),ylabel='Held-out species (%)');ax.legend(fontsize=8);savefig('holdout')
ct=table(['Assay','Covered','Exact','Covered + unique'],[[x['name'],f"{x['covered']}/{n}",f"{x['exact']}/{n}",f"{x['covered_identity_unique']}/{n}"] for x in cmp if x['panel']=='common'])
formal=rd(repo/'results/current_primers/comparison.csv');fm={x['name']:x for x in formal}
ot=table(['Assay','Own-panel N','Covered','Exact','Strict WC / GT'],[[x['name'],x['n'],x['covered'],x['exact'],f"{fm[x['name']]['strict_WC']} / {fm[x['name']]['strict_GT']}" if x['name'] in fm else '18 / not tabulated'] for x in cmp if x['panel']=='own'])
rr=[]
for x in resol:
 if x['panel']=='own':
  nn=[int(y['nearest_edit_distance']) for y in nearest if y['region']==x['region']];rr.append([x['region'],x['n'],x['identity_unique_species'],f"{x['insert_min']}–{x['insert_max']}",statistics.median(nn),sum(z<=1 for z in nn)])
rt=table(['Window','N','Unique','Insert bp','Median nearest edit','Nearest ≤1'],rr)
vt=table(['Window','Test N','Covered','Exact'],[[x['region'],x['n'],f"{x['covered']} ({float(x['coverage_pct']):.2f}%)",f"{x['exact']} ({float(x['exact_pct']):.2f}%)"] for x in cv])
st=table(['Assay','F, 5′–3′','R, 5′–3′','Deg F/R'],[[x['name'],x['F'],x['R'],f"{x['degeneracy_F']}/{x['degeneracy_R']}"] for x in pairs])
post=table(['Window','F positions','R positions','Span bp','Available species'],[[x['locus'],f"{x['F_start']}–{x['F_end']}",f"{x['R_start']}–{x['R_end']}",x['reference_span_bp'],next(y['n'] for y in cmp if y['region']==x['locus'] and y['panel']=='own')] for x in co])
cvnames=[x['name'] for x in cmp if x['panel']=='common' and x['covered']==bestcv['covered']];exnames=[x['name'] for x in cmp if x['panel']=='common' and x['exact']==bestexact['exact']]
summary=f"On the common {n}-species panel, the largest predicted coverage was {bestcv['covered']}/{n} ({', '.join(cvnames)}), and the largest number of exact paired matches was {bestexact['exact']}/{n} ({', '.join(exnames)})."
specific={
'MiCucumber':'''The common panel includes 151 species, compared with 166 evaluable XS species, 174 in S–L and 152 in XL. On the common panel, SD covers 115 species but has no exact paired matches; MD covers 79 with 22 exact, and LD covers 73 with 23 exact. The short XS covers 69 with no exact paired matches. These contrasts separate mismatch-tolerant breadth from exact template compatibility. In the own-window panel, LD covers 71/77 Holothuriida, 8/36 Dendrochirotida and 0/22 Elasipodida, demonstrating strong lineage dependence.''',
'MiLily':'''All five windows share 19 evaluable species. S–XL each have only 19 available species, comprising 17 Comatulida and one representative each of Cyrtocrinida and Isocrinida. Hyocrinida has no evaluable S–XL representative despite being present in the overall 128-species panel. Thus 19/19 coverage is not evidence for complete crinoid coverage. MD matches all 19 common species, but has seven exact matches; SD matches 17 with ten exact. The unchanged manually designed XS matches all 19, with 18 exact matches.''',
'MiUrchin':'''XLD covers 45/49 common-panel species, while LD has 19/49 exact matches. MD covers more common-panel species than LD (42 versus 39), reversing their ranking by own-panel coverage percentage. In the own-window panels, MD matches 0/37 Spatangoida, compared with LD's 36/38. Both miss all four evaluable Arbacioida. XS shortens the reference span by only 7 bp relative to S; size alone therefore provides little reason to prioritize one of these short windows.'''}[name]
manual='''### Manually designed XS

MiLily XS was supplied as a manual design and retained unchanged: F TTGGGGCAACCDCGAAG; R CAACATCGAGGTCGCAAAC. It was not retrospectively subjected to S–XL selection gates. Its original assessment used 27 references representing 25 labels. The new evaluation applies the curated-species window completeness rule to all 128 retained representatives, with paired raw-sequence scans independently checked by a naive position-by-position implementation. It covers 127/128 species with 114/128 exact matches. The original XS assessment reports 18 strict WC background records, including ten exact background records, and a failed structural gate. Those background and structure results are inherited from the original assessment, not recomputed on the new species panel. The original panel score and the curated-species score have distinct denominators.

''' if lily else ''
chinese=f'本研究对{name}五个线粒体16S窗口进行纯计算评价，使用每个物种一条代表的冻结参考面板。共同面板包含{n}个物种，覆盖最多的方案为{"、".join(cvnames)}（{bestcv["covered"]}/{n}），双端完全匹配最多的方案为{"、".join(exnames)}（{bestexact["exact"]}/{n}）。分析区分引物兼容性、去引物内部条码唯一性及属级条件性留出表现。折内候选不作为正式替换方案，跨物种相同条码保留来源待核查。'
s=f'''# {name}: in silico design and evaluation of mitochondrial 16S rRNA primers for environmental DNA metabarcoding of {taxon}

Fei Xia

Computational preprint · 30 October 2026

## Abstract

Taxon-focused metabarcoding requires a balance between primer compatibility, marker discrimination and non-target susceptibility. We evaluated five mitochondrial 16S rRNA windows (XS, S, M, L and XL) for {taxon} using a curated frozen panel of {ns} species. Each S–XL region contains an ordinary and low-degeneracy D pair at shared reference endpoints. {'XS is a retained single pair.' if name!='MiUrchin' else 'XS also contains ordinary and D pairs.'} {summary} We extracted primer-free homologous inserts, recorded interspecific identity conflicts and nearest-neighbor edit distances, and performed five-fold genus-blocked sequence selection. Each fold used training species only, with identical complete representatives bound to the same genus block. Region discovery preceded splitting, so the test estimates sequence-selection generalization conditional on the chosen regions. Fold candidates were not screened against formal thermal and background gates and do not replace released assays. The resulting data resource separates coverage, exact compatibility and reference-barcode discrimination while exposing lineage and reference-data limitations.

Keywords: {clade}; environmental DNA; mitochondrial 16S; primer degeneracy; barcode discrimination; grouped holdout

## 中文摘要

{chinese}

## 1. Introduction

Environmental DNA metabarcoding uses short markers to characterize biological assemblages from mixed DNA. Marker selection combines conserved primer-binding regions with informative variation between them. MiFish exemplifies this approach for fish 12S [1], while ecoPrimers formalizes the joint evaluation of taxonomic coverage and discrimination [2]. These principles motivate {clade} 16S candidate comparison without transferring performance estimates from other taxa or loci. Anthozoan 28S work additionally illustrates how lineage-specific binding-site variation can motivate controlled primer degeneracy [3].

A primer matching many database records may primarily reflect redundant sampling. A region with a high percentage of matched species can also be supported by a smaller or taxonomically different panel than another region. We therefore ask how controlled ordinary/D alternatives differ in coverage and exact matching on the same species set, how much discrimination their internal markers provide, and whether sequence selection generalizes to genera omitted from its training fold.

## 2. Materials and methods

### 2.1 Reference data and coordinates

The frozen source project contains {nt:,} target records and {nb:,} non-target records. Taxonomic and quality curation retained one representative for each of {ns} species, using sequence completeness and source classifications rather than primer-match success. The source repository provides accession-level audit and classification files. Alignments use MAFFT 7.526 [4]. Reference positions are 1-based and inclusive on ungapped mitochondrial 16S sequence {ref}; they refer to the extracted gene, not whole-mitogenome coordinates.

Binding-window evaluation requires that both windows span the reference interval, contain at least 90% of the corresponding reference-site count as concrete A/C/G/T, and contain no ambiguous nucleotide. Alignment gaps are allowed. Missing or uncertain binding windows are excluded from that region's denominator rather than scored as primer failures. The intersection of available accessions defines the common panel of {n} species. This is an available-data intersection, not a random sample of global diversity.

Table 1. Reference binding coordinates and evaluable species. Spans include both primer-binding regions; actual products vary among species.

{post}

### 2.2 Released primer design and chemical screening

Within S–XL, ordinary and D sequences share reference start and end positions. Released D oligonucleotides have no more than eight concrete variants per primer and confine ambiguity to the 3′ half. The source design excludes homotriplet ends and homopolymers longer than four nucleotides and requires a G or C within the final three positions. Primer3 [5] evaluations use 50 mM monovalent salt, 1.5 mM Mg2+ and 0.6 mM dNTP, considering 50 nM per concrete variant and 200 nM total per direction. The S–XL gates require a maximum predicted hairpin/dimer structure Tm below 55 °C and a forward/reverse duplex-Tm range midpoint difference no greater than 5 °C. Existing chemical and background screens are inherited from the frozen release; no released sequence is changed in this study.

{manual}### 2.3 Paired compatibility and panel comparison

Coverage requires no more than two mismatches per primer and IUPAC compatibility in each terminal three nucleotides. Exact matching requires zero mismatches at both binding sites. S–XL paired target scans allow total products of 150–500 bp with at least 50 bp between primers. XS scans allow 70–500 bp products with at least 20 bp between primers. Both sequence orientations are considered. Species contribute equally; per-order counts accompany aggregate values.

Released background screens allow an internal spacing of 0–1,000 bp. Strict WC and G–T models retain the terminal constraint; permissive WC≤3 and GT≤2 screens omit it. These counts describe reference records, not experimental amplification frequencies. C++ and Python implementations were previously compared on the same frozen data to check target and strict-background hit sets. Such implementation agreement is distinct from held-out reference evaluation.

### 2.4 Primer-free barcode discrimination

For each available representative, we extract homologous alignment columns strictly between the forward-primer end and reverse-primer start, remove gaps, and exclude ambiguous internal inserts. These reference inserts exclude both primers and are not assumed to be observed PCR products. Inserts are grouped by exact sequence identity independently of the formal primer's matching result. Identity uniqueness is assessed against all available unambiguous inserts for that window, including species outside the common panel. The covered-and-unique count requires both a paired primer match and an identity-unique insert, with the full comparison-panel denominator retained.

Unit-cost Levenshtein distances are calculated between all pairs of unambiguous inserts. For each species we report its nearest other-species distance and all tied accessions. Distance implementation was cross-checked against an independent dynamic-programming algorithm in the initial workflow. One representative per species cannot estimate within-species diversity or a barcode gap. Identity uniqueness therefore describes the frozen reference collection rather than empirical taxonomic-assignment accuracy. Apparent identity conflicts are preserved for source review. A sensitivity table removes all members of each same-window identity conflict without changing the primary panel.

### 2.5 Genus-blocked sequence-selection test

For each window, genera are sorted and linked when they share an identical complete representative sequence. Blocks are shuffled using Python's random generator with seed 20261030 and assigned cyclically to five folds. Consequently, no genus or identical complete representative crosses training and test sets. Fold sizes can differ substantially where genera are unevenly sampled.

Within each training fold, observed local sequences within five alignment columns of the frozen binding intervals supply candidates of fixed oligonucleotide lengths. Up to 24 frequent admissible concrete seeds per side enter deterministic greedy growth with at most three ambiguity-expansion steps. Ambiguity is confined to the 3′ half, degeneracy is limited to eight variants per oligonucleotide, a concrete G/C is required within the final three positions, and literal five-nucleotide homopolymers are excluded. Training paired coverage is maximized, followed by exact matching and lower summed degeneracy, with lexical tie-breaking. Released primer sequences and global candidate pools do not seed this training step.

Held-out species are scored by full raw-sequence paired scans with the same target size, mismatch and terminal rules. Each available species is tested once per window. Fold candidate construction failure would yield zero detections for that fold and empty sequence fields. This diagnostic selector does not repeat the original thermal or background selection gates. Region discovery and source-panel curation preceded splitting; accordingly, the test is conditional on predetermined regions and does not externally validate complete window discovery. Its fold sequences are not replacement recommendations. {'The XS fold test concerns the manually designed XS region; the supplied manual primer pair itself remains unchanged.' if lily else ''}

### 2.6 Data integrity and reproducibility

The frozen computational bundle contains input hashes, source sequences, window panels, scripts, per-species predictions, fold candidates and aggregate tables. Numerical analysis uses Python's standard library; plotting uses matplotlib. Validation checks denominators, fold sizes, genus separation, identical-sequence grouping, input hashes and summary totals. Source audits remain available in the repository. The present manuscript was generated from the committed result tables, with input hashes recorded in its provenance file.

## 3. Results

### 3.1 Released assays on their available panels

Table 2. Frozen own-panel target results and inherited strict background counts. {'The manual XS background assessment has a different original source panel; its GT value is not tabulated here.' if lily else ''}

{ot}

Own-panel proportions cannot by themselves establish a ranking across lengths because both denominator size and lineage composition differ. Strict and permissive background metrics remain distinct in the repository's released comparison table.

### 3.2 Equal-denominator comparison

Table 3. Released assay outcomes on {n} common species. Covered + unique means compatible paired primers and an identity-unique reference insert against the entire available same-window barcode set.

{ct}

{specific}

![Figure 1. Compatibility and exact paired matching on the common species panel. All bars use the same denominator.](figures/common_panel.png)

### 3.3 Reference-insert discrimination

Table 4. Unambiguous internal reference inserts. Nearest ≤1 is the number of representatives with a different species at edit distance zero or one. N can be smaller than the binding-window panel when an internal insert is ambiguous.

{rt}

The conflict inventory contains {len(conflicts)} same-window identity groups across all five regions. These are reference-set observations, not a determination of their biological cause. Taxonomic synonyms, source identification, sequence annotation and genuine marker sharing require distinct follow-up assessments. All accessions and sequences are retained in the supplemental conflict table. Reporting conflicts avoids counting every compatible template as a uniquely identifiable species. The conflict-exclusion sensitivity analysis is descriptive and does not assert that any source record is erroneous.

![Figure 2. Identity-unique species among all available unambiguous reference inserts in each window. Labels show numerator and denominator.](figures/resolution.png)

### 3.4 Conditional genus holdout

Table 5. Out-of-fold compatibility from training-selected diagnostic pairs. These are not the released assay scores in Tables 2–3.

{vt}

Each row pools five folds. Fold membership, genus counts, candidate sequences and training/test sizes are available in the computational bundle. A high compatible count can coexist with low exact matching. Because chemistry and background constraints were not applied to these diagnostic candidates, a larger test percentage is not evidence of a superior released assay. Conversely, a poor score can reflect the constrained heuristic rather than the absence of any useful primer in a region.

![Figure 3. Conditional genus-blocked test predictions. Fold-specific training sequences differ from the released ordinary/D assays.](figures/holdout.png)

## 4. Discussion

The analysis separates three questions: whether a primer pair matches the target reference, whether the paired sites match exactly, and whether the internal sequence distinguishes that reference from other named species. {summary} These properties need not favor the same design. Coverage improvements from controlled degeneracy should therefore be interpreted alongside exact matches, lineage changes and non-target susceptibility rather than a single aggregate percentage.

Reference availability is a substantive part of the result. Common-panel comparison removes changing denominators but limits the taxa represented. Own-panel analysis increases available taxonomic information while making raw percentages less directly comparable across regions. Order-level files expose which lineages contribute to each result, and nearest-neighbor distances show whether sequence uniqueness depends on very small differences. Identity conflicts should be reviewed against source records before being interpreted as biological limits of the marker.

The genus-blocked diagnostic prevents direct reuse of a genus across training and testing and binds identical full representatives together. It is nevertheless narrower than independent validation of the complete discovery pipeline: the windows and curated species collection were chosen before splitting. A fully nested region-discovery design or external accession set unused in any design stage would support broader generalization claims. Fold candidates also lack the original chemical/background selection and allow local alignment offsets; they cannot replace the fixed-coordinate formal assays on the basis of these tests.

One-reference-per-species scoring controls database redundancy but does not cover all haplotypes, populations or sequencing errors. Exact reference-insert uniqueness is not classifier accuracy, and compatibility models do not estimate competitive amplification in mixed DNA. Background libraries are finite and strongly shaped by available source data. Direct benchmarking against verified published taxon-compatible 16S primers, broader background sampling and repeated grouped splits remain additional computational analyses rather than completed results. These boundaries define the interpretation of this computational resource.

## 5. Conclusion

{name} provides five controlled mitochondrial 16S windows for computational comparison in {taxon}. Common-panel results, internal-barcode identity and conditional genus holdout reveal complementary aspects of candidate performance. The release preserves the formal primer sequences and supplies auditable results for length and degeneracy choices within the available reference coverage.

## Data and code availability

All primer sequences, frozen reference inputs, analyses and this preprint are available at https://github.com/GUIBA-EX/{name}. The computational evaluation bundle is under results/computational_evaluation; this manuscript's Markdown, PDF, build script and provenance are under publications. No new database retrieval is needed to reproduce the numerical analyses from the frozen inputs.

## Computational assistance

OpenAI Codex assisted with analysis code, manuscript organization and PDF production. Fei Xia is the sole named author. 

## Appendix. Released primer sequences

All sequences are written 5′ to 3′. Deg F/R gives the number of concrete variants per direction. Same-window ordinary and D sequences share the reference endpoints in Table 1. {'XS is the unchanged manual single pair.' if lily else 'XS is a retained single pair.' if name=='MiCucumber' else 'XS also retains an ordinary/D comparison.'}

{st}

## References

1. Miya M, et al. (2015). MiFish, a set of universal PCR primers for metabarcoding environmental DNA from fishes: detection of more than 230 subtropical marine species. Royal Society Open Science 2:150088. https://doi.org/10.1098/rsos.150088

2. Riaz T, et al. (2011). ecoPrimers: inference of new DNA barcode markers from whole genome sequence analysis. Nucleic Acids Research 39:e145. https://doi.org/10.1093/nar/gkr732

3. McCartin et al. (2024). Nuclear eDNA metabarcoding primers for anthozoan coral biodiversity assessment. PeerJ 12:e18607. https://doi.org/10.7717/peerj.18607

4. Katoh K, Standley DM (2013). MAFFT multiple sequence alignment software version 7: improvements in performance and usability. Molecular Biology and Evolution 30:772–780. https://doi.org/10.1093/molbev/mst010

5. Untergasser A, et al. (2012). Primer3—new capabilities and interfaces. Nucleic Acids Research 40:e115. https://doi.org/10.1093/nar/gks596

Copyright © 2026 Fei Xia. Existing project copyright and third-party source conditions apply; see COPYRIGHT.md at the repository root.
'''
(out/f'{name}_preprint.md').write_text(s)
# Typeset Markdown subset with ReportLab; figures are rasterized from the data at 220 dpi.
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
fontdir=Path(matplotlib.get_data_path())/'fonts/ttf'
pdfmetrics.registerFont(TTFont('Body',str(fontdir/'DejaVuSerif.ttf')));pdfmetrics.registerFont(TTFont('BodyBold',str(fontdir/'DejaVuSerif-Bold.ttf')));pdfmetrics.registerFont(TTFont('Mono',str(fontdir/'DejaVuSansMono.ttf')));pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='Paper',fontName='Body',fontSize=9.3,leading=13.3,spaceAfter=7,alignment=TA_JUSTIFY,allowWidows=0,allowOrphans=0));styles.add(ParagraphStyle(name='CJK',fontName='STSong-Light',fontSize=9.7,leading=14.5,spaceAfter=8));styles.add(ParagraphStyle(name='Cell',fontName='Body',fontSize=7.3,leading=10,wordWrap='CJK'));styles.add(ParagraphStyle(name='Seq',fontName='Mono',fontSize=6.5,leading=9));styles.add(ParagraphStyle(name='CaptionPaper',fontName='Body',fontSize=8,leading=11,spaceAfter=10));styles['Title'].fontName='BodyBold';styles['Title'].fontSize=17;styles['Title'].leading=22
for h in ['Heading1','Heading2']:styles[h].fontName='BodyBold';styles[h].fontSize=12 if h=='Heading1' else 10.5;styles[h].leading=16;styles[h].spaceBefore=12;styles[h].spaceAfter=6;styles[h].keepWithNext=True
styles.add(ParagraphStyle(name='TableCaption',parent=styles['CaptionPaper'],keepWithNext=True));styles.add(ParagraphStyle(name='Ref',fontName='Body',fontSize=8.1,leading=10.5,spaceAfter=5,allowWidows=0,allowOrphans=0))
styles.add(ParagraphStyle(name='CJKHeading',parent=styles['Heading1'],fontName='STSong-Light',keepWithNext=True))
story=[];paragraph=[];tab=[]
def flush():
 if paragraph:
  text=' '.join(paragraph);sty='CJK' if any('\u4e00'<=c<='\u9fff' for c in text) else 'Paper';sty='TableCaption' if text.startswith('Table ') else 'Ref' if re.match(r'^[1-5]\. ',text) else sty;story.append(KeepTogether([Paragraph(html.escape(text),styles[sty])]) if sty=='Ref' else Paragraph(html.escape(text),styles[sty]));paragraph.clear()
 if tab:
  data=[[c.strip() for c in line.strip('|').split('|')] for line in tab];data=data[:1]+data[2:];ncol=len(data[0]);is_seq='F, 5′' in data[0][1];widths=[42,204,204,45] if is_seq else [495/ncol]*ncol
  cells=[[Paragraph(html.escape(c),styles['Seq'] if is_seq and j in (1,2) and i else styles['Cell']) for j,c in enumerate(row)] for i,row in enumerate(data)]
  t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEABOVE',(0,0),(-1,0),.8,colors.HexColor('#284d60')),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#284d60')),('LINEBELOW',(0,-1),(-1,-1),.6,colors.HexColor('#284d60')),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eef3f5')),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));parts=[t,Spacer(1,10)];
  if story and isinstance(story[-1],Paragraph) and story[-1].style.name=='TableCaption':parts.insert(0,story.pop())
  story.append(KeepTogether(parts));tab.clear()
for line in s.splitlines():
 if line.startswith('Copyright ©'):continue
 if not line.strip():flush();continue
 if line.startswith('|'):tab.append(line);continue
 if line.startswith('#'):
  flush();level=len(line)-len(line.lstrip('#'));story.append(Paragraph(html.escape(line[level:].strip()),styles['CJKHeading' if any('\u4e00'<=c<='\u9fff' for c in line) else 'Title' if level==1 else 'Heading1' if level==2 else 'Heading2']))
 elif line.startswith('!['):
  flush();cap,rel=re.match(r'!\[(.*?)\]\((.*?)\)',line).groups();im=Image(str(out/rel));im.drawHeight=495*im.imageHeight/im.imageWidth;im.drawWidth=495;story.append(KeepTogether([im,Spacer(1,5),Paragraph(html.escape(cap),styles['CaptionPaper'])]))
 else:paragraph.append(line)
flush()
def footer(c,doc):
 c.setFont('Body',7);c.setFillColor(colors.HexColor('#53636d'));c.drawString(50,28,f'{name} | Fei Xia | Computational preprint | 30 October 2026');c.drawRightString(545,28,str(doc.page));c.setFont('Body',5.8);c.drawString(50,17,'Copyright © 2026 Fei Xia. All rights reserved. Third-party source conditions apply; see repository COPYRIGHT.md.')
pdf=out/f'{name}_preprint.pdf';doc=SimpleDocTemplate(str(pdf),pagesize=(595.28,841.89),rightMargin=50,leftMargin=50,topMargin=45,bottomMargin=48,title=f'{name}: computational primer evaluation',author='Fei Xia');doc.build(story,onFirstPage=footer,onLaterPages=footer)
inputs=['sequences/primer_pairs.csv','figures/current_region_coordinates.csv','results/current_primers/comparison.csv']+[str(f.relative_to(repo)) for f in sorted(res.glob('*.csv'))]+['results/computational_evaluation/results/manifest.json']
prov=dict(author='Fei Xia',date='2026-10-30',project=name,source_commit=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD']).decode().strip(),common_species=int(n),inputs={f:hashlib.sha256((repo/f).read_bytes()).hexdigest() for f in inputs},artifacts={pdf.name:hashlib.sha256(pdf.read_bytes()).hexdigest(),f'{name}_preprint.md':hashlib.sha256((out/f'{name}_preprint.md').read_bytes()).hexdigest()})
(out/'preprint_provenance.json').write_text(json.dumps(prov,indent=2)+'\n');print(name,'PDF and Markdown generated')
