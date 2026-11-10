"""Verify each selected S/L scheme against all frozen references by regex seed matching."""
import json
import sys
import tempfile
import zipfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from analyze import BACKGROUND, HERE, ROOT, SOURCE, fa, rc, read, read_inputs

sys.path.insert(0, str(ROOT / 'results/lineage_exploration'))
from verify_shortlist import flags


def verify(job):
    name, assay, targets, background = job
    f, r = assay['F'], assay['R']
    window = name[0]
    covered, exact = set(), set()
    for accession, sequence in targets.items():
        hit = flags((sequence, rc(sequence)), f, r, False, 2, window, True)
        if 'le2last3' in hit:
            covered.add(accession)
        if 'exact' in hit:
            exact.add(accession)
    assert covered == assay['covered'] & targets.keys(), (name, 'covered')
    assert exact == assay['exact'] & targets.keys(), (name, 'exact')
    bg = {key: set() for key in BACKGROUND}
    for accession, sequence in background.items():
        strands = sequence, rc(sequence)
        hits = {'WC': flags(strands, f, r, False, 4, window, False),
                'GT': flags(strands, f, r, True, 2, window, False)}
        for key, (model, flag) in BACKGROUND.items():
            if flag in hits[model]:
                bg[key].add(accession)
    assert bg == assay['background'], name
    return dict(assay=name, target_species=len(targets), background_records=len(background), disagreements=0)


def main():
    _, schemes = read_inputs()
    raw = fa(ROOT / SOURCE / 'representatives.fasta')
    targets = {w: {r['accession']: raw[r['accession']] for r in read(SOURCE + f'panel_{w}.csv')}
               for w in ('S', 'L')}
    with tempfile.TemporaryDirectory() as directory:
        with zipfile.ZipFile(ROOT / 'reproducibility/frozen/xs_inputs.zip') as archive:
            background = fa(Path(archive.extract('background.fasta', directory)))
    assert len(background) == 5600
    jobs = [(name, assay, targets[name[0]], background) for name, assay in schemes.items()]
    with ProcessPoolExecutor(max_workers=4) as executor:
        checks = list(executor.map(verify, jobs))
    report = dict(status='PASS', method='Independent Python regex seed-and-extend',
                  assays=checks, accession_flag_checks=sum(2 * r['target_species'] + 5 * r['background_records']
                                                          for r in checks))
    (HERE / 'independent_checks.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f"PASS: {len(checks)} schemes, {report['accession_flag_checks']} accession/criterion comparisons")


if __name__ == '__main__':
    main()
