"""Render the manuscript using pandoc and Chrome/Chromium (set CHROME if needed)."""
import os,json
from pypdf import PdfReader,PdfWriter
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

out=Path(__file__).resolve().parent
c=json.loads((out/'release.json').read_text())
from tables import synchronize
import hashlib
manuscript=out/'MiCucumber_preprint.md'
manuscript.write_text(synchronize(manuscript.read_text()))
working_revision='**Working revision · ' in manuscript.read_text()
for gene in ('12S','COI'):
    shutil.copyfile(out.parent/f'markers/12S_COI/figures/positions_{gene}.en.png',out/f'figures/{gene}_positions.png')
provenance_file=out/'preprint_provenance.json'
provenance=json.loads(provenance_file.read_text())
sources=set(provenance['inputs'])|{'publications/tables.py','publications/release.json'}
sources.update(f'markers/12S_COI/figures/positions_{gene}.en.png' for gene in ('12S','COI'))
diagnostic=out.parent/'results/anth28s_evaluation'
sources.update(str(f.relative_to(out.parent)) for f in diagnostic.rglob('*') if f.is_file() and '__pycache__' not in str(f) and f.suffix in ('.csv','.json','.png','.svg','.py','.cpp'))
lineage=out.parent/'results/lineage_evaluation'
sources.update(str(f.relative_to(out.parent)) for f in lineage.iterdir()
               if f.is_file() and f.suffix in ('.csv','.json','.py'))
sources.update(str(f.relative_to(out.parent)) for f in (out.parent/'results/marker_complementarity').iterdir()
               if f.is_file() and f.suffix in ('.csv','.py','.md'))
sources.update(str(f.relative_to(out.parent)) for f in (out.parent/'results/external_panel').iterdir()
               if f.is_file() and f.suffix in ('.csv','.json','.fasta','.txt','.md','.py'))
sources.update(f'figures/base_matching_{name}.svg' for name in ('SD-Dendrochirotida','LD-Elasipodida'))
provenance.update(date=c['date'],working_revision=working_revision,source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=out.parent,text=True).strip())
provenance['inputs']={name:hashlib.sha256((out.parent/name).read_bytes()).hexdigest() for name in sorted(sources)}
provenance_file.write_text(json.dumps(provenance,indent=2)+'\n')
article=subprocess.check_output(['pandoc','--from=gfm','--to=html5',str(out/'MiCucumber_preprint.md')],text=True)
def source_link(match):
    path=(out/match[1]).resolve()
    if working_revision:
        return f'href="{path.as_uri()}"'
    return f'href="https://github.com/GUIBA-EX/MiCucumber/blob/preprint-v{c["version"]}/{path.relative_to(out.parent)}"'
article=re.sub(r'href="(?!https?:|#)([^"]+)"',source_link,article)
article=re.sub(r'(<p><img\b[^>]*></p>|<figure>.*?</figure>)\s*(<p><strong>Figure.*?</p>)',r'<div class=figure-block>\1\2</div>',article,flags=re.S)
article=article.replace('′','&#39;')
css="""h2[id^="table-1-"]+p+table{break-inside:auto}p:has(+table){break-after:avoid}thead{display:table-header-group}@page{size:A4;margin:17mm 18mm 18mm;@bottom-left{content:'MiCucumber · Fei Xia · Computational preprint';font:8pt 'Avenir Next';color:#54635c}@bottom-right{content:counter(page);font:8pt 'Avenir Next'}}.figure-block{break-inside:avoid}body{font:10.5pt/1.38 'Avenir Next',sans-serif;color:#172b27}h1{font-size:21pt;text-align:center;line-height:1.18}h2{font-size:15pt}h3{font-size:12pt}h2,h3{break-after:avoid}p{margin:6pt 0 9pt;orphans:3;widows:3}img{width:100%;display:block}img[src$="_binding.svg"]{width:86%;margin:auto}figure{margin:8pt 0;break-inside:avoid;break-after:avoid}figcaption{display:none}table{break-inside:auto;border-collapse:collapse;width:100%;font:8.7pt/1.4 'Avenir Next'}td,th{padding:3pt;border-bottom:1px solid #cfdfda}th{background:#deede8}tr{break-inside:avoid}a{color:#216459}h2[id^=table]{break-before:page}code{font-family:'Avenir Next',sans-serif}p:has(>strong:first-child){break-before:avoid}h2#references~p{font-size:9pt;line-height:1.2;margin:3pt 0}h2[id^="table-1-"]+p+table{font-size:8pt;line-height:1.1}h2[id^="table-1-"]+p+table td,h2[id^="table-1-"]+p+table th{padding:1.5pt}"""
chrome=os.environ.get('CHROME') or shutil.which('chromium') or '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
css+='h2[id^="table-"]{break-before:auto}h2[id^="table-1-"],h2[id^="table-7-"],h2[id^="table-10-"]{break-before:page}table{break-inside:avoid}p:has(+table){break-after:avoid}'
with tempfile.TemporaryDirectory() as t:
    doc=Path(t)/'paper.html'
    doc.write_text(f'<!doctype html><meta charset=utf-8><base href="{out.as_uri()}/"><title>MiCucumber · Fei Xia</title><style>{css}</style>{article}')
    subprocess.run([chrome,'--headless','--disable-gpu','--allow-file-access-from-files','--no-pdf-header-footer',f'--user-data-dir={t}/profile',f'--print-to-pdf={out}/MiCucumber_preprint.pdf',doc.as_uri()],check=True)

pdf=out/'MiCucumber_preprint.pdf'
writer=PdfWriter(clone_from=PdfReader(pdf));writer.add_metadata({'/Author':'Fei Xia','/Title':c['title'],'/Subject':('Working revision of ' if working_revision else '')+f"computational preprint v{c['version']}"})
with pdf.open('wb') as f:writer.write(f)
