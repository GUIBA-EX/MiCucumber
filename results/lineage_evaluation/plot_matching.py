"""Draw site-by-site comparisons in primer orientation for verified rescued references."""
from html import escape

from analyze import ANCHOR, BASES, HERE, I, ROOT, SOURCE, binding, fa, read, read_inputs, write

FIGURES = ROOT / 'figures'
PANELS = (
    ('SD', 'SD-Dendrochirotida', 'R', 'Dendrochirotida'),
    ('LD', 'LD-Elasipodida', 'F', 'Elasipodida'),
)


def mismatches(primer, motif):
    return [i for i, (code, base) in enumerate(zip(primer, motif)) if base not in I[code]]


def text(x, y, value, size=13, color='#244453', weight=400, mono=False):
    family = 'monospace' if mono else 'system-ui, sans-serif'
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'fill="{color}" font-weight="{weight}">{escape(str(value))}</text>')


def rect(x, y, width, height, fill, radius=0, stroke='none'):
    return (f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}"/>')


def cells(x, y, sequence, differences):
    for i, nucleotide in enumerate(sequence):
        bad = i in differences
        fill = '#f9ded9' if bad else '#d8efe9'
        ink = '#842d26' if bad else '#125547'
        yield rect(x + 12.5 * i, y, 11.5, 21, fill, 2, '#548c92' if i >= len(sequence) - 3 else 'none')
        yield text(x + 12.5 * i + 2, y + 15, nucleotide, 12, ink, 650, True)


def draw(base, pool, side, coords, primers, examples):
    left, right = 313, 690
    width, height = 1072, 375
    side_name = 'Reverse' if side == 'R' else 'Forward'
    low, high = coords
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="title description">',
           f'<title id="title">{pool} base matching</title>',
           '<desc id="description">Target templates shown in primer orientation and compared with the original and supplementary oligonucleotides.</desc>',
           rect(0, 0, width, height, '#f7fafb', 12),
           text(25, 35, f'16S {pool}  |  {side_name} binding site', 22, '#103746', 700),
           text(25, 59, f'AB525437.1 positions {low}–{high}  •  5′ to 3′ primer orientation  •  Selected rescued species', 13),
           rect(24, 77, 1024, 233, '#ffffff', 9, '#d7e5e8'),
           text(39, 105, 'Target species and accession', 13, weight=700),
           text(left, 105, f'Original {base} {side}', 13, weight=700),
           text(right, 105, f'Supplementary {side}', 13, weight=700)]
    for x, primer in zip((left, right), primers):
        svg.extend(text(x + 12.5 * i + 2, 128, b, 12, weight=700, mono=True) for i, b in enumerate(primer))
        svg.append(text(x + 12.5 * len(primer) + 8, 128, 'MM', 10, weight=650))
    for index, row in enumerate(examples):
        y = 146 + 39 * index
        if index:
            svg.append(rect(39, y - 6, 993, 1, '#e7eff1'))
        svg.extend([text(39, y + 9, row['species'], 13, weight=620),
                    text(39, y + 25, f"{row['accession']}  •  {row['order']}", 11, '#52717d')])
        for x, primer in zip((left, right), primers):
            diff = mismatches(primer, row['binding_motif'])
            svg.extend(cells(x, y, row['binding_motif'], diff))
            svg.append(text(x + 12.5 * len(primer) + 13, y + 15, len(diff), 13, weight=680))
    svg.extend([rect(28, 331, 13, 13, '#d8efe9', 2), text(48, 342, 'Compatible base'),
                rect(182, 331, 13, 13, '#f9ded9', 2), text(202, 342, 'Mismatch'),
                rect(301, 331, 13, 13, '#ffffff', 2, '#548c92'), text(321, 342, 'Final three 3′ positions'),
                text(510, 342, 'MM = mismatches at this site. The unchanged partner is compatible for every row.', 12),
                '</svg>'])
    (FIGURES / f'base_matching_{pool}.svg').write_text('\n'.join(svg) + '\n')


def main():
    coords, schemes = read_inputs()
    aligned = fa(ROOT / SOURCE / 'curated_alignment.fasta')
    columns = [i for i, base in enumerate(aligned[ANCHOR]) if base != '-']
    gains = read(HERE / 'lineage_gain_species.csv')
    audit = []
    for base, pool, side, order in PANELS:
        site = coords[base[0]]
        index = int(side == 'R')
        bounds = site[2 * index:2 * index + 2]
        partner = schemes[base]['FR'[1 - index]][0]
        partner_bounds = site[2 * (1 - index):2 * (1 - index) + 2]
        original, supplemental = schemes[pool][side]
        candidates = []
        for row in gains:
            if row['assay'] != pool or row['panel'] != 'available' or row['added_coverage'] != '1':
                continue
            sequence = aligned[row['accession']]
            motif = binding(sequence, columns, bounds, side == 'R')
            opposite = binding(sequence, columns, partner_bounds, side == 'F')
            if (len(motif) != len(original) or len(opposite) != len(partner)
                    or (set(motif + opposite) - BASES)):
                continue
            previous = mismatches(original, motif)
            added = mismatches(supplemental, motif)
            shared = mismatches(partner, opposite)
            if len(previous) <= 2 and not any(i >= len(motif) - 3 for i in previous):
                continue
            if any(len(bad) > 2 or any(i >= n - 3 for i in bad)
                   for bad, n in [(added, len(motif)), (shared, len(opposite))]):
                continue
            candidates.append(dict(assay=pool, accession=row['accession'], species=row['species'],
                                   order=row['order'], changed_side=side, binding_motif=motif,
                                   original_mismatches=len(previous), supplement_mismatches=len(added),
                                   shared_mismatches=len(shared),
                                   original_terminal_mismatches=sum(i >= len(motif) - 3 for i in previous)))
        ranked = sorted(candidates, key=lambda r: (r['order'] != order, r['supplement_mismatches'],
                                                   -r['original_terminal_mismatches'], r['species']))
        chosen = []
        for row in ranked:
            if row['binding_motif'] not in {r['binding_motif'] for r in chosen} and len(chosen) < 4:
                chosen.append(row)
        assert len(chosen) == 4, pool
        audit.extend(chosen)
        draw(base, pool, side, bounds, (original, supplemental), chosen)
    write('matching_examples.csv', audit)


if __name__ == '__main__':
    main()
