"""Refresh hashes of publication outputs; verify the other archived entries."""
import hashlib,json,sys
from pathlib import Path
p=Path('SHA256SUMS.json')
expected=json.loads(p.read_text())
for f in expected:
    digest=hashlib.sha256(Path(f).read_bytes()).hexdigest()
    if f.startswith('publications/') or f in ['README.md','README.en.md','README.zh-CN.md','CITATION.bib','CITATION.cff']:
        expected[f]=digest
    else:
        assert expected[f]==digest,f
p.write_text(json.dumps(expected,indent=2,ensure_ascii=False)+'\n')
files=[Path('publications/MiCucumber_preprint.pdf'),Path('sequences/all_markers.fasta')]
Path('publications/SHA256SUMS.txt').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name+'\n' for f in files))
