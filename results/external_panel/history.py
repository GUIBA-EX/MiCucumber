"""Index recorded MiCucumber design inputs and earlier challenge sequences."""
import hashlib
import sys
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT.parents[1]
FASTA = {'.fasta', '.fa', '.fna', '.fas'}
ACCESSION = re.compile(r'(?<![A-Z0-9])[A-Z]{1,6}_?[0-9]{5,12}(?:\.\d+)?(?![A-Z0-9])')
RC = str.maketrans('ACGTURYSWKMBDHVN', 'TGCAAYRSWMKVHDBN')


def accession_key(value):
    return value.split('.')[0]


def canonical(sequence):
    return min(sequence, sequence.translate(RC)[::-1])


def index():
    ids, sequences, sources = set(), set(), {}
    def ingest(label, data, is_fasta):
        sources[label] = hashlib.sha256(data).hexdigest()
        if not is_fasta:
            ids.update(accession_key(x) for x in ACCESSION.findall(data.decode(errors='replace')))
            return
        for block in data.split(b'>')[1:]:
            title, _, body = block.partition(b'\n')
            ids.update(accession_key(x) for x in ACCESSION.findall(title.decode(errors='replace')))
            sequence = b''.join(body.split()).decode(errors='replace').upper().replace('-', '').replace('U', 'T')
            if len(sequence) >= 150 and set(sequence) <= set('ACGTRYSWKMBDHVN'):
                sequences.add(canonical(sequence))
    folders = [ROOT/'markers/12S_COI', ROOT/'results/species_qc', ROOT/'results/computational_evaluation/inputs']
    folders.extend(p for p in (WORKSPACE/'work').glob('micucumber*')
                   if p.is_dir() and p.name not in ('micucumber_external_20261111', 'micucumber_literature_comparison'))
    folders.extend(p for p in (WORKSPACE/'outputs').glob('MiCucumber_reef*') if p.is_dir())
    for folder in sorted(folders):
        for p in sorted(folder.rglob('*')):
            if not p.is_file() or any(part in ('deps','venv','__pycache__') for part in p.parts):
                continue
            if p.suffix.lower() in FASTA or p.name=='downloaded_accessions.txt':
                ingest(str(p.relative_to(WORKSPACE)), p.read_bytes(), p.suffix.lower() in FASTA)
    for archive in sorted((ROOT/'reproducibility/frozen').glob('*.zip')):
        with zipfile.ZipFile(archive) as z:
            for member in z.namelist():
                p = Path(member)
                if p.suffix.lower() in FASTA or p.name in ('metadata.tsv','target_taxonomy.tsv','panel.csv'):
                    ingest(str(archive.relative_to(WORKSPACE))+'!'+member, z.read(member), p.suffix.lower() in FASTA)
    return ids, sequences, sources


if __name__ == '__main__':
    ids, sequences, sources = index()
    scratch = Path(sys.argv[1])
    (scratch/'historical_accessions.txt').write_text('\n'.join(sorted(ids))+'\n')
    (scratch/'historical_sequences.txt').write_text('\n'.join(sorted(sequences))+'\n')
    (scratch/'historical_inputs.json').write_text(json.dumps(sources,indent=2)+'\n')
    print(len(ids), 'accessions;',len(sequences), 'sequences;',len(sources),'sources')
