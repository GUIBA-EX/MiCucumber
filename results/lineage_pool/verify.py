"""Verify every reference hit in the selected LD pools using a separate seed scan."""
import argparse
import json
import re
import zipfile
from functools import lru_cache
from pathlib import Path

from design import ROOT, BACKGROUND, fa, rc, rows, sets


@lru_cache(None)
def seed_patterns(primer, reverse, wobble, limit):
    allowed = sets(primer, reverse, wobble)
    patterns = []
    for i in range(limit + 1):
        start = i * len(primer) // (limit + 1)
        stop = (i + 1) * len(primer) // (limit + 1)
        seed = ''.join(f"[{''.join(sorted(bases))}]" for bases in allowed[start:stop])
        patterns.append((start, re.compile(f'(?={seed})')))
    return allowed, patterns


def sites(sequence, primer, reverse, wobble, limit):
    allowed, patterns = seed_patterns(primer, reverse, wobble, limit)
    starts = {m.start() - offset for offset, pattern in patterns for m in pattern.finditer(sequence)}
    for start in starts:
        stop = start + len(primer)
        if start < 0 or stop > len(sequence):
            continue
        template = sequence[start:stop]
        if set(template) - set('ACGT'):
            continue
        bad = [i for i, base in enumerate(template) if base not in allowed[i]]
        if len(bad) <= limit:
            tail = any(i < 3 if reverse else i >= len(primer)-3 for i in bad)
            yield start, len(bad), tail


def paired_flags(strands, forward, reverse, wobble, limit, target):
    flags = set()
    for sequence in strands:
        reverse_hits = list(sites(sequence, reverse, True, wobble, limit))
        if not reverse_hits:
            continue
        for primer in forward:
            for f, fm, ft in sites(sequence, primer, False, wobble, limit):
                for r, rm, rt in reverse_hits:
                    gap, span = r-f-len(primer), r+len(reverse)-f
                    if not ((gap >= 50 and 150 <= span <= 500) if target else (0 <= gap <= 1000)):
                        continue
                    mismatches = max(fm, rm)
                    if mismatches == 0:
                        flags.add('exact')
                    if mismatches <= 2:
                        flags.add('le2')
                        if not ft and not rt:
                            flags.add('le2last3')
                    if mismatches <= 3:
                        flags.add('le3')
                    flags.add('le4')
    return flags


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    out = parser.parse_args().output
    pools = json.loads((out/'ld_verification_input.json').read_text())
    panel = {x['accession'] for x in rows(ROOT/'results/species_qc/panel_L.csv')}
    target = {a:s for a,s in fa(ROOT/'results/species_qc/representatives.fasta').items() if a in panel}
    background = {}
    with zipfile.ZipFile(ROOT/'reproducibility/frozen/xs_inputs.zip') as z:
        for line in z.read('background.fasta').decode().splitlines():
            if line.startswith('>'):
                accession = line[1:].split()[0]
                background[accession] = ''
            else:
                background[accession] += line.strip().upper()
    assert len(target) == len(panel) == 174 and len(background) == 5600
    report = []
    for pool in pools:
        expected = {key:set(pool[key]) for key in ('covered','exact')}
        expected.update({key:set(value) for key,value in pool['background'].items()})
        actual = {key:set() for key in expected}
        assert len(pool['R']) == 1
        for accession, sequence in target.items():
            flags = paired_flags((sequence,rc(sequence)), pool['F'], pool['R'][0], False, 2, True)
            if 'le2last3' in flags:
                actual['covered'].add(accession)
            if 'exact' in flags:
                actual['exact'].add(accession)
        for accession, sequence in background.items():
            flags = {model:paired_flags((sequence,rc(sequence)),pool['F'],pool['R'][0],model=='GT',limit,False)
                     for model,limit in [('WC',4),('GT',2)]}
            for key,(model,flag) in BACKGROUND.items():
                if flag in flags[model]:
                    actual[key].add(accession)
        for key in expected:
            assert actual[key] == expected[key], (pool['scheme'], key, sorted(actual[key]^expected[key]))
        report.append(dict(scheme=pool['scheme'],target_records=len(target),background_records=len(background),
                           accession_disagreements=0,**{key:len(value) for key,value in actual.items()}))
        print(pool['scheme'], 'passed independent accession-level comparison', flush=True)
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__ == '__main__':
    main()
