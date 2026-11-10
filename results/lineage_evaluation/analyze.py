"""Summarize the verified S and L lineage supplements on the existing 16S panels."""
import csv
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from xs_raw_helpers import I, fa, rc

BACKGROUND = {
    'strict_WC': ('WC', 'le2last3'), 'strict_GT': ('GT', 'le2last3'),
    'WC3': ('WC', 'le3'), 'GT2': ('GT', 'le2'), 'WC4': ('WC', 'le4'),
}
COORDS = ('F_start', 'F_end', 'R_start', 'R_end')
BASES = frozenset('ACGT')
SOURCE = 'results/species_qc/'
EVALUATION = 'results/computational_evaluation/results/'
S_SOURCE = 'results/lineage_exploration/shortlist.json'
L_SOURCE = 'results/lineage_pool/ld_verification_input.json'
SD_SOURCE = 'results/current_primers/S/SD_independent_hits.tsv'
ANCHOR = 'AB525437.1'


def read(path, delimiter=','):
    with (ROOT / path).open() as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def write(path, records):
    with (HERE / path).open('w') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(records)


def binding(sequence, columns, bounds, reverse=False):
    start, stop = bounds
    motif = sequence[columns[start - 1]:columns[stop - 1] + 1].replace('-', '')
    return rc(motif) if reverse else motif


def read_inputs():
    coords = {r['locus']: tuple(int(r[k]) for k in COORDS)
              for r in read('figures/current_region_coordinates.csv')}
    sd = next(r for r in json.loads((ROOT / S_SOURCE).read_text())
              if (r['assay'], r['position'], r['background']) == ('SD', 'same', 'strict-neutral'))
    s = read(SD_SOURCE, '\t')
    schemes = {
        'SD': dict(F=sd['F'], R=sd['R'][:1],
                   **{key: {r['accession'] for r in s if r['role'] == 'target' and r[flag] == '1'}
                      for key, flag in [('covered', 'le2last3'), ('exact', 'exact')]},
                   background={key: {r['accession'] for r in s if r['role'] == 'background'
                                     and r['model'] == model and r[flag] == '1'}
                               for key, (model, flag) in BACKGROUND.items()}),
        'SD-Dendrochirotida': dict(F=sd['F'], R=sd['R'], covered=set(sd['target_coverage']),
                                 exact=set(sd['target_exact']),
                                 background={key: set(ids) for key, ids in sd['background_accessions'].items()}),
    }
    for row in json.loads((ROOT / L_SOURCE).read_text()):
        schemes[row['scheme']] = dict(F=row['F'], R=row['R'], covered=set(row['covered']),
                                     exact=set(row['exact']),
                                     background={key: set(ids) for key, ids in row['background'].items()})
    for r in read('sequences/primer_pairs.csv'):
        if r['name'] in ('SD', 'LD'):
            assay = schemes[r['name']]
            assert (assay['F'], assay['R']) == ([r['F']], [r['R']])
    for name, assay in schemes.items():
        f_start, f_end, r_start, r_end = coords[name[0]]
        assert all(len(f) == f_end - f_start + 1 for f in assay['F'])
        assert all(len(r) == r_end - r_start + 1 for r in assay['R'])
        assert assay['exact'] <= assay['covered']
    return coords, schemes


def main():
    coords, schemes = read_inputs()
    metadata = {r['accession']: r for r in read(SOURCE + 'panel.csv')}
    panels = {w: {r['accession'] for r in read(SOURCE + f'panel_{w}.csv')}
              for w in ('XS', 'S', 'M', 'L', 'XL')}
    common = set.intersection(*panels.values())
    assert len(common) == 151 and len(metadata) == 174
    all_orders = sorted({m['order'] for m in metadata.values()})
    nearest = {(r['region'], r['accession']): int(r['nearest_edit_distance'])
               for r in read(EVALUATION + 'nearest_neighbors.csv')}

    summary, by_order, gains, gain_species, background_hits = [], [], [], [], []
    for name, assay in schemes.items():
        window = name[0]
        base = schemes[name.split('-')[0]]
        added_oligos = len(assay['F']) + len(assay['R']) - len(base['F']) - len(base['R'])
        assert base['covered'] & panels[window] <= assay['covered'] & panels[window]
        assert base['exact'] & panels[window] <= assay['exact'] & panels[window]
        for key in BACKGROUND:
            assert base['background'][key] <= assay['background'][key]
        for accession in sorted(set.union(*assay['background'].values())):
            background_hits.append(dict(assay=name, accession=accession,
                                        **{k: int(accession in ids) for k, ids in assay['background'].items()},
                                        **{'new_' + k: int(accession in ids - base['background'][k])
                                           for k, ids in assay['background'].items()}))
        for panel, ids in [('available', panels[window]), ('common', common)]:
            covered, exact = assay['covered'] & ids, assay['exact'] & ids
            base_covered, base_exact = base['covered'] & ids, base['exact'] & ids
            new, new_exact = covered - base_covered, exact - base_exact

            def counts(group):
                distances = {a: nearest[window, a] for a in group if (window, a) in nearest}
                unique = {a for a, dist in distances.items() if dist > 0}
                return dict(n=len(group), covered=len(group & covered), exact=len(group & exact),
                            barcode_n=len(distances), barcode_unique=len(unique),
                            covered_unique=len(covered & unique),
                            barcode_nearest_one=sum(d == 1 for d in distances.values()))

            total = counts(ids)
            groups = []
            for order in all_orders:
                group = {a for a in ids if metadata[a]['order'] == order}
                groups.append(dict(assay=name, panel=panel, order=order, **counts(group),
                                   added_coverage=len(new & group), added_exact=len(new_exact & group)))
            assert all(sum(row[key] for row in groups) == total[key] for key in total)
            by_order.extend(groups)
            summary.append(dict(assay=name, panel=panel, **total,
                                **{key: len(records) for key, records in assay['background'].items()}))
            if not added_oligos:
                continue
            gains.append(dict(assay=name, panel=panel, n=len(ids), added_oligos=added_oligos,
                              base_covered=len(base_covered), covered=len(covered), added_coverage=len(new),
                              base_exact=len(base_exact), exact=len(exact), added_exact=len(new_exact),
                              **{'new_' + key: len(records - base['background'][key])
                                 for key, records in assay['background'].items()}))
            for accession in sorted(new | new_exact):
                gain_species.append(dict(assay=name, panel=panel, accession=accession,
                                         species=metadata[accession]['organism'], order=metadata[accession]['order'],
                                         added_coverage=int(accession in new), added_exact=int(accession in new_exact)))

    for row in read(EVALUATION + 'panel_comparison.csv'):
        if row['name'] not in ('SD', 'LD'):
            continue
        expected = next(r for r in summary if r['assay'] == row['name']
                        and r['panel'] == {'own': 'available', 'common': 'common'}[row['panel']])
        for key, source in [('n', 'n'), ('covered', 'covered'), ('exact', 'exact'),
                            ('covered_unique', 'covered_identity_unique')]:
            assert expected[key] == int(row[source])

    alignment = fa(ROOT / SOURCE / 'curated_alignment.fasta')
    columns = [i for i, base in enumerate(alignment[ANCHOR]) if base != '-']
    variants = []
    for name, side in [('SD-Dendrochirotida', 'R'), ('LD-Synallactida-Elasipodida', 'F')]:
        window = name[0]
        index = 2 if side == 'R' else 0
        bounds = coords[window][index:index + 2]
        motifs = Counter(binding(alignment[a], columns, bounds, side == 'R') for a in panels[window])
        for oligo, primer in enumerate(schemes[name][side], 1):
            for bases in itertools.product(*(I[code] for code in primer)):
                variant = ''.join(bases)
                variants.append(dict(assay=name, side=side, oligo=oligo, primer=primer, sequence=variant,
                                     exact_site_species=motifs[variant]))

    union = []
    s = 'SD-Dendrochirotida'
    for l in ('LD-Elasipodida', 'LD-Synallactida-Elasipodida'):
        for panel, ids in [('available', panels['S'] & panels['L']), ('common', common)]:
            union.append(dict(s_assay=s, l_assay=l, panel=panel, n=len(ids),
                              **{key: len((schemes[s][key] | schemes[l][key]) & ids)
                                 for key in ('covered', 'exact')}))
    write('summary.csv', summary)
    write('by_order.csv', by_order)
    write('lineage_gains.csv', gains)
    write('lineage_gain_species.csv', gain_species)
    write('lineage_variants.csv', variants)
    write('separate_assay_union.csv', union)
    write('background_hits.csv', background_hits)

    inputs = [S_SOURCE, L_SOURCE, SD_SOURCE, 'figures/current_region_coordinates.csv',
              'sequences/primer_pairs.csv', SOURCE + 'curated_alignment.fasta', SOURCE + 'panel.csv',
              EVALUATION + 'panel_comparison.csv', EVALUATION + 'nearest_neighbors.csv',
              *(SOURCE + f'panel_{w}.csv' for w in panels)]
    (HERE / 'comparison_checks.json').write_text(json.dumps(
        dict(status='PASS', common_species=len(common), available_species=len(metadata),
             input_sha256={path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in inputs}),
        indent=2) + '\n')
    print(f'PASS: {len(schemes)} S/L schemes on {len(common)} shared species')


if __name__ == '__main__':
    main()
