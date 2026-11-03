"""Draw per-order binding-site alignments and gene-relative primer positions."""
from pathlib import Path
import csv
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'figures'
IUPAC = dict(zip('ACGTRYSWKMBDHVN', ['A','C','G','T','AG','CT','CG','AT','GT','AC','CGT','AGT','ACT','ACG','ACGT']))
COMP = str.maketrans('ACGTRYMKSWBDHVN', 'TGCAYRKMSWVHDBN')
COLORS = dict(XS='#249395', S='#418a56', M='#d79226', L='#397abb', XL='#8458ae')
plt.rcParams.update({'svg.fonttype':'none','font.family':'DejaVu Sans'})
def read(path):
    with path.open() as f:
        return list(csv.DictReader(f))
def alignment(path):
    seqs = {}
    for line in path.read_text().splitlines():
        if line.startswith('>'):
            key = line[1:].split()[0].removeprefix('_R_')
            seqs[key] = ''
        else:
            seqs[key] += line.upper()
    return seqs

OUT.mkdir(exist_ok=True)
for gene in ('12S','COI'):
    d = ROOT / gene
    seqs = alignment(d/'aligned.fasta')
    cols = [i for i,b in enumerate(seqs[(d/'anchor.txt').read_text().strip()]) if b!='-']
    groups = defaultdict(list)
    for row in read(d/'target_panel.csv'):
        groups[row['order']].append(row)
    hits = {(h['name'],h['accession']):h for h in read(d/'hits.csv') if h['role']=='target' and h['model']=='WC'}
    assays = read(d/'pairs.csv')
    for row in assays:
        name=row['name']
        bounds=[int(row[k])-1 for k in ('F_start','F_end','R_start','R_end')]
        def templates(acc):
            seq=seqs[acc]
            def site(a,b):
                return ''.join('?' if not seq[:i+1].strip('-') or not seq[i:].strip('-') else seq[i] for i in cols[a:b+1])
            return site(*bounds[:2]),site(*bounds[2:]).translate(COMP)[::-1]
        picked=[]
        for order,group in sorted(groups.items()):
            def rank(rec):
                f,r=templates(rec['accession'])
                return (-sum(c in 'ACGT' for c in f+r),rec['accession'])
            rec=min(group,key=rank)
            acc=rec['accession'];f,r=templates(acc)
            h=hits.get((name,acc),{})
            state='exact' if h.get('exact')=='1' else 'match' if h.get('covered')=='1' else 'unknown' if '?' in f+r or set(f+r)-set('ACGT-') else 'miss'
            picked.append((order,rec['species'],acc,f,r,state))
        fig,ax=plt.subplots(figsize=(14,max(4.4,1.6+.31*len(picked))))
        offset=len(row['F'])+2
        ax.set(xlim=(-44,offset+len(row['R'])+11),ylim=(len(picked)+1.8,-2.8))
        ax.axis('off');ax.set_title(f'MiCucumber {gene} {name}   |   homologous binding sites',loc='left',weight='bold',fontsize=14)
        ax.text(-43,-.3,'Order  /  species  /  accession',fontsize=9)
        for side,start in [('F',0),('R',offset)]:
            q=row[side]
            ax.text(start,-1.65,f'{side}  5′ → 3′   {row[side+"_start"]}–{row[side+"_end"]}',fontsize=9)
            for j,c in enumerate(q):ax.text(start+j,-.3,c,ha='center',fontfamily='monospace',weight='bold',fontsize=9)
            for y,(o,sp,a,f,r,state) in enumerate(picked,1):
                if side=='F':
                    ax.text(-43,y,f'{o}  /  {sp}  /  {a}',va='center',fontsize=7)
                    ax.text(offset+len(row['R'])+1,y,state,va='center',fontsize=8)
                for j,c in enumerate(f if side=='F' else r):
                    color='#d4eee7' if c in IUPAC[q[j]] else '#f6c6a4' if c in 'ACGT' else '#ededed'
                    ax.add_patch(Rectangle((start+j-.48,y-.44),.96,.88,facecolor=color,edgecolor='none'))
                    ax.text(start+j,y,c,ha='center',va='center',fontsize=8,fontfamily='monospace')
            ax.add_patch(Rectangle((start+len(q)-3-.5,.54),3,len(picked)-.08,fill=False,edgecolor='#294559',lw=1))
        ax.text(-43,len(picked)+1.3,'Green: compatible   Orange: mismatch   Grey: gap or missing   Box: terminal 3 nt   Right: full-sequence paired scan',fontsize=8)
        fig.savefig(OUT/f'{gene}_{name}.svg',bbox_inches='tight')
        plt.close(fig)
