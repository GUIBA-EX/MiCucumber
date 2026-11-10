"""Compare frozen MiCucumber marker panels and test limited near-terminal mismatches."""
import csv
import sys
import zipfile
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / 'results' / name) for name in ('lineage_evaluation', 'lineage_pool')]
from analyze import read, read_inputs, fa, rc
from verify import seed_patterns, sites

SPECIES = 'results/species_qc/'
MARKERS = 'markers/12S_COI/'
DIAGNOSTICS = 'results/anth28s_evaluation/results/'
BASE = 'results/computational_evaluation/results/'
FOCAL = {'12S': 'XLD', 'COI': 'XSD'}
# WoRMS AphiaID 242132 recognizes Chiridota heheva as a junior synonym.
ALIASES = {'Chiridota heheva': 'Chiridota hydrothermica'}


def accepted(name):
    return ALIASES.get(name, name)


def write(name, rows):
    with (HERE / name).open('w') as handle:
        writer = csv.DictWriter(handle, list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def paired_flags(sequence, forwards, reverses, min_span, min_inner, background):
    """WC only. Each end ≤2 mismatches. Relaxed mode allows one at −2/−3 per pair."""
    for strand in (sequence, rc(sequence)):
        forward_hits, reverse_hits = [], []
        for reverse, primers, output in [(False, forwards, forward_hits), (True, reverses, reverse_hits)]:
            for primer in primers:
                allowed, _ = seed_patterns(primer, reverse, False, 2)
                terminal = 0 if reverse else len(primer) - 1
                near = (1, 2) if reverse else (terminal - 1, terminal - 2)
                for start, _, _ in sites(strand, primer, reverse, False, 2):
                    if strand[start + terminal] in allowed[terminal]:
                        n = sum(strand[start + i] not in allowed[i] for i in near)
                        output.append((start, len(primer), n))
        for f, lf, nf in forward_hits:
            for r, lr, nr in reverse_hits:
                gap, span = r - f - lf, r + lr - f
                valid = 0 <= gap <= 1000 if background else gap >= min_inner and min_span <= span <= 500
                if valid and nf + nr <= 1:
                    yield nf + nr


def scan(job):
    gene, name, f, r, target, background = job
    rows = []
    for role, templates in [('target', target), ('background', background)]:
        for accession, seq in sorted(templates.items()):
            hit = min(paired_flags(seq, f, r, 150 if gene == '16S' else 100, 50, role == 'background'),
                      default=2)
            rows.append(dict(gene=gene, assay=name, role=role, accession=accession,
                             strict=int(hit == 0), limited_relaxed=int(hit < 2)))
    return rows


def marker(gene):
    base = MARKERS + gene + '/'
    meta = {r['accession']: r for r in read(base + 'target_panel.csv')}
    source = {r['accession']: r['species'] for r in read(base + 'eligible_metadata.csv') if r['role'] == 'target'}
    align = {a.removeprefix('_R_'): s for a, s in fa(ROOT / (base + 'aligned.fasta')).items()}
    anchor = (ROOT / (base + 'anchor.txt')).read_text().strip()
    cols = [i for i, ch in enumerate(align[anchor]) if ch != '-']
    pairs = read(base + 'pairs.csv')
    eligible, compatible, exact = {}, {}, {}
    hits = {(r['name'], r['accession']): r for r in read(DIAGNOSTICS + gene + '_hits.csv') if r['role'] == 'target'}
    for p in pairs:
        name = p['name']
        a, b, c, d = [cols[int(p[k]) - 1] for k in ('F_start', 'F_end', 'R_start', 'R_end')]
        eligible[name] = {acc for acc in meta if (s := align[acc]) and len(s)-len(s.lstrip('-')) <= a
                          and len(s.rstrip('-')) > d and set(s[a:b+1]+s[c:d+1]) <= set('ACGT-')}
        compatible[name] = {acc for acc in eligible[name] if int(hits.get((name, acc), {}).get('min_max_terminal_compatible', 3)) <= 2}
        exact[name] = {acc for acc in compatible[name] if hits[name, acc]['min_max_mismatches'] == '0'}
        assert (len(eligible[name]), len(compatible[name]), len(exact[name])) == tuple(int(p[k]) for k in ('evaluable', 'covered', 'exact'))
    return base, meta, source, pairs, eligible, compatible, exact


def main():
    # Exercise forward and reverse terminal indexing and the one-mismatch-per-pair ceiling.
    f, r, middle = 'ACGAGTCA', 'TGCCTAGG', 'C' * 150
    template = f + middle + rc(r)
    for index, expected in [(7, []), (6, [1]), (-8, []), (-7, [1])]:
        i = index % len(template)
        replacement = 'A' if template[i] != 'A' else 'C'
        variant = template[:i] + replacement + template[i+1:]
        assert list(paired_flags(variant, [f], [r], 150, 50, False)) == expected
    _, lineage = read_inputs()
    names = ('SD-Dendrochirotida', 'LD-Elasipodida')
    panel = {r['accession']: r for r in read(SPECIES + 'panel.csv')}
    miss = set(panel) - set.union(*(lineage[n]['covered'] for n in names))
    assert len(miss) == 9
    source_16s = fa(ROOT / SPECIES / 'representatives.fasta')
    markers = {gene: marker(gene) for gene in FOCAL}
    jobs = []
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(ROOT / 'reproducibility/frozen/xs_inputs.zip') as z:
            background = fa(Path(z.extract('background.fasta', tmp)))
    for name in names:
        assay = lineage[name]
        jobs.append(('16S', name, assay['F'], assay['R'], source_16s, background))
    for gene, (base, meta, _, pairs, eligible, _, _) in markers.items():
        p = next(p for p in pairs if p['name'] == FOCAL[gene])
        seqs = fa(ROOT / (base + 'target.fasta'))
        jobs.append((gene, p['name'], [p['F']], [p['R']], {a: seqs[a] for a in eligible[p['name']]},
                     fa(ROOT / (base + 'background.fasta'))))
    with ProcessPoolExecutor(max_workers=4) as pool:
        rows = [r for block in pool.map(scan, jobs) for r in block]
    sensitivity = {}
    new_hits = []
    for gene, name, *_ in jobs:
        for role in ('target', 'background'):
            selected = [r for r in rows if (r['gene'], r['assay'], r['role']) == (gene, name, role)]
            strict = {r['accession'] for r in selected if r['strict']}
            relaxed = {r['accession'] for r in selected if r['limited_relaxed']}
            if gene == '16S':
                expected = lineage[name]['covered'] & panel.keys() if role == 'target' else lineage[name]['background']['strict_WC']
                assert strict == expected, (name, role)
            else:
                expected = markers[gene][5][name] if role == 'target' else {
                    r['accession'] for r in read(DIAGNOSTICS + gene + '_hits.csv')
                    if r['name'] == name and r['role'] == 'background' and int(r['min_max_terminal_compatible']) <= 2}
                assert strict == expected, (gene, name, role)
            sensitivity[gene, name, role] = relaxed
            new_hits.extend(r for r in selected if r['limited_relaxed'] and not r['strict'])
    counts = Counter((r['gene'], r['assay'], r['role'], key) for r in rows
                     for key in ('n','strict','limited_relaxed') if key == 'n' or r[key])
    write('mismatch_sensitivity.csv', [
        dict(gene=g, assay=n, role=role, **{key: counts[g,n,role,key] for key in ('n','strict','limited_relaxed')})
        for g,n,*_ in jobs for role in ('target','background')])
    write('added_hits.csv', new_hits)
    missed = []
    for acc in sorted(miss, key=lambda a: (panel[a]['order'],panel[a]['organism'])):
        species = panel[acc]['organism']
        for gene, (_, meta, source, pairs, eligible, compatible, exact) in markers.items():
            other = next((a for a, m in meta.items() if accepted(m['species']) == species), '')
            tested = [p['name'] for p in pairs if other in eligible[p['name']]]
            conflicting_name = source.get(acc, '') if accepted(source.get(acc)) != species else ''
            status = ('evaluable' if tested else 'binding_region_unavailable' if other else
                      'same_accession_label_conflict' if conflicting_name else
                      'eligible_record_outside_panel' if species in map(accepted, source.values()) else 'no_eligible_reference')
            missed.append(dict(species=species, order=panel[acc]['order'], accession_16s=acc,
                               limited_16s=int(any(acc in sensitivity['16S', n, 'target'] for n in names)),
                               marker=gene, accession=other, source_name=meta[other]['species'] if other else '',
                               same_accession=int(acc == other),
                               reference_status=status, conflicting_source_name=conflicting_name, evaluable=';'.join(tested),
                               strict=';'.join(n for n in tested if other in compatible[n]),
                               exact=';'.join(n for n in tested if other in exact[n]),
                               limited_focal=int(other in sensitivity[gene, FOCAL[gene], 'target']) if FOCAL[gene] in tested else ''))
    write('missed_species.csv', missed)

    inserts = {(r['gene'],r['window'],r['accession']): r['sequence'] for r in read(DIAGNOSTICS + 'barcodes.csv')}
    collisions = {(r['region'], *sorted(r['accessions'].split(';'))) for r in read(BASE+'barcode_collisions.csv')}
    near = {(r['region'],*sorted((r['accession'], other))) for r in read(BASE+'nearest_neighbors.csv')
            if r['nearest_edit_distance']=='1' for other in r['nearest_accessions'].split(';')}
    comparisons = []
    for w,a,b in sorted(collisions | near):
        for gene, (_, meta, _, pairs, eligible, compatible, _) in markers.items():
            for window in dict.fromkeys(p['window'] for p in pairs):
                first, second = [inserts.get((gene,window,x),'') if x in meta and
                                 accepted(meta[x]['species'])==panel[x]['organism'] else '' for x in (a,b)]
                status = 'different' if first and second and first!=second else 'identical' if first and second else 'not_paired'
                both = [p['name'] for p in pairs if p['window']==window and {a,b}<=compatible[p['name']]]
                comparisons.append(dict(window_16s=w, distance_16s=int((w,a,b) not in collisions),
                                        accession_a=a, accession_b=b, species_a=panel[a]['organism'],
                                        species_b=panel[b]['organism'],marker=gene, window=window,
                                        insert_a=int(bool(first)), insert_b=int(bool(second)),
                                        same_accession_comparison=status, compatible_both=';'.join(both)))
    write('paired_barcode_collisions.csv', comparisons)


if __name__ == '__main__':
    main()
