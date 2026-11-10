"""Select same-coordinate 16S pools of two or three oligos on one side."""
import argparse
import csv
import itertools
import json
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'markers/12S_COI/scripts')]
from chemistry import expand, hetero, single, terminal
from xs_raw_helpers import fa, rc, sets

WINDOWS = {'XS': 'R', 'SD': 'R', 'MD': 'F', 'LD': 'F', 'XLD': 'F'}
BACKGROUND = {
    'strict_WC': ('WC', 'le2last3'), 'strict_GT': ('GT', 'le2last3'),
    'WC3': ('WC', 'le3'), 'GT2': ('GT', 'le2'), 'WC4': ('WC', 'le4'),
}


def rows(path, delimiter=','):
    with path.open() as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def write(path, data):
    with path.open('w') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(data[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(data)


def write_ld_fasta(path, components, scheme):
    oligos = [x for x in components if x['scheme'] == scheme]
    assert oligos, scheme
    path.write_text(''.join(
        f">MiCucumber-16S-LD_{x['oligo']}\n{x['sequence_5to3']}\n" for x in oligos))


def matches(primer, site, threshold=2):
    if len(site) != len(primer) or set(site) - set('ACGT'):
        return False
    bad = [i for i, (allowed, base) in enumerate(zip(sets(primer), site)) if base not in allowed]
    return len(bad) <= threshold and all(i < len(primer) - 3 for i in bad)


@lru_cache(None)
def thermal(forward, reverse):
    """Split 200 nM per direction equally by named formulation, then by variant."""
    summaries = []
    for scenario in ('50 nM per variant', '200 nM per direction'):
        sides = []
        for primers in (forward, reverse):
            formulations = []
            for primer in primers:
                variants = expand(primer)
                conc = 50 if scenario.startswith('50') else 200 / len(primers) / len(variants)
                formulations.append([(variant, conc) for variant in variants])
            sides.append(formulations)
        by_side = []
        for side in sides:
            midpoints = []
            for formulation in side:
                tm = [single(q, c)[0] for q, c in formulation]
                midpoints.append((min(tm) + max(tm)) / 2)
            by_side.append(midpoints)
        delta = max(abs(f - r) for f, r in itertools.product(*by_side))
        # Combine duplicate molecular variants before computing interactions.
        molecules = defaultdict(float)
        for sequence, conc in itertools.chain.from_iterable(itertools.chain.from_iterable(sides)):
            molecules[sequence] += conc
        structures = [single(q, c)[1] for q, c in molecules.items()]
        structures += [hetero(a, b, max(molecules[a], molecules[b]))
                       for a, b in itertools.combinations(molecules, 2)]
        summaries.append(dict(scenario=scenario, max_duplex_midpoint_delta_C=round(delta, 6),
                              max_structure_tm_C=round(max(structures), 6),
                              passes=delta <= 5 and max(structures) < 55))
    return summaries


def target_sites(window, coords, alignment, columns):
    result = {}
    for entry in rows(ROOT / f'results/species_qc/panel_{window}.csv'):
        sequence = alignment[entry['accession']]
        binding = {}
        for side in 'FR':
            start = columns[int(coords[side + '_start']) - 1]
            end = columns[int(coords[side + '_end']) - 1]
            binding[side] = sequence[start:end+1].replace('-', '')
        binding['R'] = rc(binding['R'])
        result[entry['accession']] = (entry, binding)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    out = parser.parse_args().output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    pairs = {x['name']: x for x in rows(ROOT / 'sequences/primer_pairs.csv')}
    coords = {x['locus']: x for x in rows(ROOT / 'figures/current_region_coordinates.csv')}
    metrics = {x['name']: x for x in rows(ROOT / 'results/current_primers/comparison.csv')}
    alignment = fa(ROOT / 'results/species_qc/curated_alignment.fasta')
    columns = [i for i, base in enumerate(alignment['AB525437.1']) if base != '-']
    summary, taxon_rows, component_rows, thermal_rows, selected, audit, species_rows = [], [], [], [], [], [], []
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        scanner = work / 'scan'
        subprocess.run(['c++','-O3','-std=c++17',str(ROOT/'scripts/xs_independent_scan.cpp'),
                        '-o',str(scanner)], check=True)
        (work/'target.fasta').symlink_to(ROOT/'results/species_qc/representatives.fasta')
        with zipfile.ZipFile(ROOT/'reproducibility/frozen/xs_inputs.zip') as z:
            (work/'background.fasta').write_bytes(z.read('background.fasta'))
        for name, variable in WINDOWS.items():
            pair = pairs[name]
            region = pair['region']
            panel = target_sites(region, coords[region], alignment, columns)
            shared = 'F' if variable == 'R' else 'R'
            base, constant = pair[variable], pair[shared]
            anchor_hits = {q: {acc for acc, (_, sites) in panel.items()
                               if matches(constant, sites[shared]) and matches(q, sites[variable])}
                           for q in sorted({x[1][variable] for x in panel.values()
                                            if len(x[1][variable]) == len(base)
                                            and set(x[1][variable]) <= set('ACGT')} | {base})}
            candidates = [base] + [q for q in anchor_hits if q != base and terminal(q)
                                   and anchor_hits[q] - anchor_hits[base]]
            def pool(arms):
                return (arms, (constant,)) if variable == 'F' else ((constant,), arms)
            eligible = [q for q in candidates if q == base or
                        all(s['passes'] for s in thermal(*pool((base, q))))]
            (work/'independent_primers.tsv').write_text(''.join(
                f'{i}\t{q if variable == "F" else constant}\t{q if variable == "R" else constant}\n'
                for i, q in enumerate(eligible)))
            subprocess.run([str(scanner),str(work),*(['20','70'] if name=='XS' else ['50','150'])],
                           check=True, stderr=subprocess.DEVNULL)
            coverage, exact, background = defaultdict(set), defaultdict(set), defaultdict(lambda: defaultdict(set))
            for row in rows(work/'independent_hits.tsv', '\t'):
                q = eligible[int(row['name'])]
                acc = row['accession']
                if row['role'] == 'target' and acc in panel:
                    if row['le2last3'] == '1': coverage[q].add(acc)
                    if row['exact'] == '1': exact[q].add(acc)
                elif row['role'] == 'background':
                    for key, (model, flag) in BACKGROUND.items():
                        if row['model'] == model and row[flag] == '1': background[q][key].add(acc)
            assert (len(coverage[base]),len(exact[base])) == tuple(
                int(metrics[name][key]) for key in ('covered_labels','exact_labels')), name
            assert all(len(background[base][key]) == int(metrics[name][key]) for key in BACKGROUND), name
            clean = [q for q in eligible[1:] if (coverage[q]-coverage[base]) and
                     (coverage[q]-coverage[base]) <= anchor_hits[q] and
                     all(background[q][k] <= background[base][k] for k in BACKGROUND)]
            print(f'{name}: {len(anchor_hits)} site motifs, {len(eligible)-1} scanned additions, {len(clean)} background-neutral', flush=True)
            audit.append(dict(assay=name, variable_side=variable, site_motifs=len(anchor_hits),
                              terminal_and_gain_candidates=len(candidates)-1,
                              thermally_eligible=len(eligible)-1, background_neutral=len(clean)))
            def score(arms):
                return (len(set.union(*(coverage[q] for q in arms))),
                        len(set.union(*(exact[q] for q in arms))))
            arm_names = {base: variable}
            previous_score = (-1, -1)
            chosen_pools = []
            for size in (1, 2, 3):
                # Rank every combination at this size before checking whole-pool interactions.
                options = sorted(((base,)+extra for extra in itertools.combinations(clean,size-1)),
                                 key=lambda a: (*score(a), a), reverse=True)
                arms = next((a for a in options if all(s['passes'] for s in thermal(*pool(a)))), None)
                if arms is None or score(arms) <= previous_score:
                    break
                previous_score = score(arms)
                for q in arms:
                    if q not in arm_names:
                        gains = Counter(panel[acc][0]['order'] for acc in coverage[q] - coverage[base])
                        order = min(gains, key=lambda group: (-gains[group], group))
                        label = f'{variable}-{order}'
                        suffix = 2
                        while label in arm_names.values():
                            label = f'{variable}-{order}-{suffix}'
                            suffix += 1
                        arm_names[q] = label
                chosen_pools.append(tuple(q for q in arm_names if q in arms))
            if name == 'LD':
                # For a separate S assay, retain the Elasipodida gain with one extra F.
                elasipodida = next(q for q, label in arm_names.items() if label == 'F-Elasipodida')
                minimal = (base, elasipodida)
                assert all(s['passes'] for s in thermal(*pool(minimal)))
                if minimal not in chosen_pools:
                    chosen_pools.append(minimal)
            for arms in chosen_pools:
                hit = set.union(*(coverage[q] for q in arms))
                ex = set.union(*(exact[q] for q in arms))
                scheme = '-'.join([name, *(arm_names[q].split('-', 1)[1] for q in arms[1:])])
                summary.append(dict(scheme=scheme,window=region,variable_side=variable,
                                    variable_oligos=len(arms),n=len(panel),covered=len(hit),exact=len(ex),
                                    added_vs_current=len(hit-coverage[base]),**{k:len(background[base][k]) for k in BACKGROUND}))
                for order in sorted({e['order'] for e,_ in panel.values()}):
                    ids = {acc for acc,(e,_) in panel.items() if e['order']==order}
                    taxon_rows.append(dict(scheme=scheme,order=order,n=len(ids),covered=len(hit&ids),
                                           exact=len(ex&ids),added_vs_current=len((hit-coverage[base])&ids)))
                f,r = pool(arms)
                for side, primers in [('F',f),('R',r)]:
                    for q in primers:
                        component_rows.append(dict(scheme=scheme,oligo=arm_names[q] if side == variable else side,
                                                   sequence_5to3=q,
                                                   start=coords[region][side+'_start'],end=coords[region][side+'_end']))
                thermal_rows.extend(dict(scheme=scheme,**s) for s in thermal(f,r))
                if name == 'LD':
                    species_rows.extend(dict(scheme=scheme,accession=acc,species=entry['organism'],
                                             order=entry['order'],covered=int(acc in hit),
                                             exact=int(acc in ex),added_vs_current=int(acc in hit-coverage[base]))
                                        for acc, (entry, _) in sorted(panel.items()))
                    selected.append(dict(scheme=scheme,F=list(f),R=list(r),covered=sorted(hit),exact=sorted(ex),
                                         background={k:sorted(background[base][k]) for k in BACKGROUND}))
    write(out/'screening.csv',audit)
    write(out/'comparison.csv',summary)
    write(out/'by_order.csv',taxon_rows)
    write(out/'oligos.csv',component_rows)
    write(out/'thermal.csv',thermal_rows)
    write(out/'ld_by_species.csv',species_rows)
    largest = max(selected, key=lambda item: len(item['F']))['scheme']
    write_ld_fasta(out/'ld_pool.fasta', component_rows, largest)
    write_ld_fasta(out/'ld_elasipodida.fasta', component_rows, 'LD-Elasipodida')
    (out/'ld_verification_input.json').write_text(json.dumps(selected,indent=2)+'\n')


if __name__ == '__main__':
    main()
