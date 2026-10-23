"""Check exported compact portfolios and repository checksums (no new PCR scan)."""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'results/compact'
def rows(name, delimiter=','):
    with (DATA / name).open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))

selection = json.loads((DATA / 'selection.json').read_text())
assert len(selection) == 8
assert {(s['locus'], s['count']) for s in selection} == {
    (f'MiCucumber-{locus}', count) for locus in ('v4opt', 'S', 'M', 'L') for count in (1, 2)
}
pairs = rows('primer_pairs.csv')
comparison = rows('comparison.csv')
assert len(pairs) == 12 and len(comparison) == 16
expected_fasta = {}
for scheme in selection:
    selected = [r for r in pairs if r['scheme'] == scheme['name']]
    assert len(selected) == scheme['count']
    assert {r['pair_id'] for r in selected} == set(scheme['pair_names'])
    assert len({r['reaction'] for r in selected}) == len(selected)
    for row in selected:
        for direction in ('F', 'R'):
            assert set(row[direction]) <= set('ACGTRYSWKMBDHVN')
            key = f"{row['version']}|{row['pairs']}pairs|PCR{row['reaction']}|{direction}|{row['pair_id']}"
            expected_fasta[key] = row[direction]
    summary = [r for r in comparison if r['scheme'] == scheme['name']]
    assert {r['panel'] for r in summary} == {'common', 'own_region'}
    for row in summary:
        assert int(row['count']) == len(selected)
        assert int(row['WC_le3']) <= 5 and int(row['GT_le2']) <= 5
        assert 0 <= float(row['exact_pct']) <= float(row['coverage_pct']) <= 100
        if row['panel'] == 'common':
            assert (int(row['n_labels']), int(row['n_haplotypes']), int(row['non_Apodida_labels'])) == (151, 351, 145)
fasta = {}
for line in (DATA / 'primers.fasta').read_text().splitlines():
    if line.startswith('>'):
        key = line[1:]
        assert key not in fasta
        fasta[key] = ''
    elif line:
        fasta[key] += line.strip()
assert fasta == expected_fasta
validation = json.loads((DATA / 'validation.json').read_text())
assert validation['status'] == 'PASS' and validation['checks'] == 21036
thermal = rows('thermodynamics.tsv', '\t')
assert len(thermal) == 16
assert Counter(r['name'] for r in thermal) == Counter({r['pair_id']: 2 for r in pairs})
structure_keys = [k for k in thermal[0] if 'hairpin' in k or 'dimer' in k]
maximum = max(float(r[k]) for r in thermal for k in structure_keys)
assert maximum < 55 and abs(maximum - validation['thermal_max_structure_C']) < 1e-8
for path in [* (ROOT / 'evidence').glob('*.zip'), *DATA.glob('*.zip')]:
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None, path
for name, digest in json.loads((ROOT / 'SHA256SUMS.json').read_text()).items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
print('PASS: eight portfolios, twelve reaction rows, FASTA, comparison, thermal evidence, ZIP integrity and SHA256')
