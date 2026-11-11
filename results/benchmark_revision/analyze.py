"""Recompute equal-denominator comparisons and positional diagnostics from frozen inputs."""
from collections import defaultdict
import csv
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'results/marker_complementarity'))
from compare import accepted, fa, marker, rc, read, read_inputs, seed_patterns, sites

WINDOWS = ('XS', 'S', 'M', 'L', 'XL')
DIAG = 'results/anth28s_evaluation/results'
CLASSES = ('Asteroidea', 'Crinoidea', 'Echinoidea', 'Ophiuroidea')


def write(name, rows):
    with (HERE / name).open('w') as handle:
        writer = csv.DictWriter(handle, list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def barcode_groups(rows):
    groups = defaultdict(set)
    for row in rows:
        groups[row['sequence']].add(accepted(row['species']))
    return groups


def marker_comparisons():
    output = []
    barcodes = read(f'{DIAG}/barcodes.csv')
    for gene in ('12S', 'COI'):
        _, meta, _, pairs, eligible, compatible, exact = marker(gene)
        by_window = {w: [r for r in barcodes if r['gene'] == gene and r['window'] == w] for w in WINDOWS}
        windows = {w: next(eligible[r['name']] for r in pairs if r['window'] == w) for w in WINDOWS}
        representatives = {}
        for acc in sorted(meta, key=lambda a: (-sum(a in ids for ids in windows.values()),
                                               -int(meta[a]['length']), a)):
            representatives.setdefault(accepted(meta[acc]['species']), acc)
        retained = set(representatives.values())
        for panel, names in [('all_windows', WINDOWS), ('short_windows', WINDOWS[:3]), ('available', WINDOWS)]:
            common = set.intersection(*(windows[w] for w in names))
            for p in pairs:
                w, assay = p['window'], p['name']
                if w not in names:
                    continue
                selected = (eligible[assay] if panel == 'available' else common) & retained
                records = by_window[w]
                groups = barcode_groups(records)
                unique = {r['accession'] for r in records if len(groups[r['sequence']]) == 1}
                hits = compatible[assay] & selected
                assert unique <= eligible[assay]
                output.append(dict(gene=gene, panel=panel, window=w, assay=assay, span=p['span'],
                                   n=len(selected), covered=len(hits), exact=len(exact[assay] & selected),
                                   covered_unique=len(hits & unique), background_wc=p['WC'], background_gt=p['GT']))
    return output


def taxonomy():
    qc = ROOT / 'results/species_qc'
    taxa = json.loads((qc / 'gbif_accepted.json').read_text())
    for row in json.loads((qc / 'gbif_matches.json').read_text()):
        match = row['match']
        if match.get('rank') == 'SPECIES' and match.get('status') == 'ACCEPTED' and match.get('class') == 'Holothuroidea':
            taxa.setdefault(str(match['usageKey']), match)
    families_by_genus = defaultdict(set)
    for match in taxa.values():
        if match.get('genus') and match.get('family'):
            families_by_genus[match['genus']].add(match['family'])
    panel = {}
    for row in read('results/species_qc/panel.csv'):
        species = row['organism']
        genus = species.split()[0]
        families = families_by_genus[genus]
        family = taxa.get(row['species_key'], {}).get('family')
        panel[species] = {'genus': genus, 'family': family or (next(iter(families)) if len(families) == 1 else None)}
    barcodes = read('results/computational_evaluation/results/barcodes.csv')
    output, collisions = [], []
    for w in WINDOWS:
        groups = barcode_groups(r for r in barcodes if r['region'] == w)
        qualified = defaultdict(set)
        unique = defaultdict(set)
        for sequence, names in sorted(groups.items()):
            annotations = {rank: {panel[n].get(rank) for n in names} for rank in ('genus', 'family')}
            for rank in ('genus', 'family'):
                labels = annotations[rank]
                if None not in labels:
                    qualified[rank].add(sequence)
                    if len(labels) == 1:
                        unique[rank].add(sequence)
            if len(names) == 1:
                unique['species'].add(sequence)
            else:
                genera, families = annotations['genus'], annotations['family']
                kind = ('within genus' if sequence in unique['genus'] else 'within family'
                        if sequence in unique['family'] and None not in genera else 'across families'
                        if None not in families and len(families) > 1 else 'unresolved taxonomy')
                collisions.append(dict(window=w, classification=kind, species='; '.join(sorted(names))))
        output.append(dict(window=w, barcode_groups=len(groups), species_unique=len(unique['species']),
                           genus_evaluable=len(qualified['genus']), genus_unique=len(unique['genus']),
                           family_evaluable=len(qualified['family']), family_unique=len(unique['family']),
                           conflicting_groups=sum(len(v) > 1 for v in groups.values())))
    return output, collisions


def terminal_positions(sequence, forwards, reverses, min_span, min_inner):
    """Return every supported position among geometrically admissible limited hits."""
    results = set()
    for strand in (sequence, rc(sequence)):
        hits = []
        for reverse, primers in [(False, forwards), (True, reverses)]:
            found = []
            for primer in primers:
                allowed, _ = seed_patterns(primer, reverse, False, 2)
                for start, _, _ in sites(strand, primer, reverse, False, 2):
                    tail = [i + 1 for i in range(3)
                            if strand[start + (i if reverse else len(primer) - 1 - i)]
                            not in allowed[i if reverse else len(primer) - 1 - i]]
                    if 1 not in tail and len(tail) <= 1:
                        found.append((start, len(primer), tail))
            hits.append(found)
        for f, lf, tf in hits[0]:
            for r, lr, tr in hits[1]:
                if r - f - lf >= min_inner and min_span <= r + lr - f <= 500 and len(tf) + len(tr) == 1:
                    results.add(f'{"F" if tf else "R"} −{(tf or tr)[0]}')
    return sorted(results)


def mismatch_changes():
    _, pools = read_inputs()
    primer = {(g, r['name']): ([r['F']], [r['R']])
              for g in ('16S', '12S', 'COI')
              for r in read('sequences/primer_pairs.csv' if g == '16S' else f'markers/12S_COI/{g}/pairs.csv')}
    primer.update({('16S', n): (p['F'], p['R']) for n, p in pools.items()})
    frozen = {g: fa(ROOT / ('results/species_qc/representatives.fasta' if g == '16S' else f'markers/12S_COI/{g}/target.fasta'))
              for g in ('16S', '12S', 'COI')}
    external = {g: fa(ROOT / f'results/external_panel/{g}_target.fasta') for g in frozen}
    labels = {r['accession']: r['organism'] for r in read('results/species_qc/panel.csv')}
    for gene in ('12S', 'COI'):
        labels.update({r['accession']: r['species'] for r in read(f'markers/12S_COI/{gene}/target_panel.csv')})
    focus = read('results/marker_complementarity/added_hits.csv')
    external_rows = read('results/external_panel/predictions.csv')
    new = [('design', r) for r in focus if r['role'] == 'target']
    new += [('external', r) for r in external_rows if r['role'] == 'target' and r['strict'] == '0' and r['limited'] == '1']
    output = []
    for panel, r in new:
        gene, assay, acc = (r[k] for k in ('gene', 'assay', 'accession'))
        size, insert = (70, 20) if (gene, assay) == ('16S', 'XS') else (150 if gene == '16S' else 100, 50)
        seqs = frozen if panel == 'design' else external
        positions = terminal_positions(seqs[gene][acc], *primer[gene, assay], size, insert)
        assert positions, (gene, assay, acc)
        if panel == 'design':
            model = next(x for x in read('results/marker_complementarity/mismatch_sensitivity.csv')
                         if (x['gene'], x['assay'], x['role']) == (gene, assay, 'background'))
            bg_n = int(model['n'])
            bg_added = int(model['limited_relaxed']) - int(model['strict'])
        else:
            bg = [x for x in external_rows if (x['gene'], x['assay'], x['role']) == (gene, assay, 'background')]
            bg_n = len(bg)
            bg_added = sum(x['strict'] == '0' and x['limited'] == '1' for x in bg)
        output.append(dict(panel=panel, gene=gene, assay=assay, species=accepted(r.get('species') or labels[acc]),
                           accession=acc, position=' / '.join(positions), added_background=bg_added, background_n=bg_n))
    return output


def near_relative_background():
    output = []
    for gene in ('12S', 'COI'):
        base = f'markers/12S_COI/{gene}'
        meta = read(f'{base}/background_panel.csv')
        hits = {(r['name'], r['accession']): r for r in read(f'{DIAG}/{gene}_hits.csv') if r['role'] == 'background'}
        released = defaultdict(set)
        for row in read(f'{base}/hits.csv'):
            if row['role'] == 'background' and row['covered'] == '1':
                released[row['name'], row['model']].add(row['accession'])
        for taxon in CLASSES:
            ids = {r['accession'] for r in meta if taxon in r['lineage'].split(';')}
            for p in read(f'{base}/pairs.csv'):
                n = p['name']
                wc = {acc for acc in ids if int(hits.get((n, acc), {}).get('min_max_terminal_compatible', 3)) <= 2}
                assert wc == released[n, 'WC'] & ids
                output.append(dict(gene=gene, assay=n, background_class=taxon, records=len(ids),
                                   strict_wc=len(wc), strict_gt=len(released[n, 'GT'] & ids)))
    return output


if __name__ == '__main__':
    write('marker_comparison.csv', marker_comparisons())
    by_rank, collisions = taxonomy()
    write('resolution_by_rank.csv', by_rank)
    write('barcode_collisions_by_rank.csv', collisions)
    write('limited_mismatch_changes.csv', mismatch_changes())
    write('near_relative_background.csv', near_relative_background())
