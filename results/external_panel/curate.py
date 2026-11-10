"""Freeze accession-audited external mitochondrial reference features before scoring."""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

from Bio import SeqIO
from Bio.SeqFeature import ExactPosition

from history import RC, accession_key, canonical

HERE = Path(__file__).resolve().parent
GROUPS = ('Holothuroidea','Echinoidea','Asteroidea','Ophiuroidea','Crinoidea','Gastropoda',
          'Malacostraca','Anthozoa','Nemertea','Actinopteri','Actinopterygii')
GENES = ('16S','12S','COI')


def features(record):
    found = {}
    for feature in record.features:
        if feature.type not in ('rRNA','CDS','gene'):
            continue
        fields = feature.qualifiers
        gene = ' '.join(fields.get('gene', [])).lower()
        product = ' '.join(fields.get('product', [])).lower()
        if feature.type == 'rRNA' and (re.search(r'\b16s\b|large subunit', product) or gene in ('rrnl','lrrna')):
            name = '16S'
        elif feature.type == 'rRNA' and (re.search(r'\b12s\b|small subunit', product) or gene in ('rrns','srrna')):
            name = '12S'
        elif feature.type in ('CDS','gene') and (gene in ('cox1','coi','co1','mt-co1','cox i')
             or re.search(r'cytochrome c oxidase subunit (?:i|1)\b',product)):
            name = 'COI'
        else:
            continue
        sequence = str(feature.extract(record.seq)).upper()
        whole = (len(record) >= 12000 and isinstance(feature.location.start, ExactPosition)
                 and isinstance(feature.location.end, ExactPosition))
        candidate = (whole, sequence, str(feature.location))
        if name not in found or (whole,len(sequence)) > (found[name][0],len(found[name][1])):
            found[name] = candidate
    names = {'16S': r'\b16S\b|large subunit ribosomal RNA',
             '12S': r'\b12S\b|small subunit ribosomal RNA',
             'COI': r'\bCOI\b|\bCO1\b|cytochrome (?:c )?oxidase subunit (?:I|1)\b'}
    if len(record) <= 3000 and not found:
        labels = [name for name,pattern in names.items() if re.search(pattern,record.description,re.I)]
        if len(labels) == 1:
            found[labels[0]] = (False,str(record.seq).upper(),f'[0:{len(record)}](+)')
    return found


def mitochondrial(record):
    organelles = [
        value for feature in record.features if feature.type == 'source'
        for value in feature.qualifiers.get('organelle', [])
    ]
    annotation = ' '.join([record.description, *organelles])
    return bool(re.search(r'\bmitochondri\w*', annotation, re.I))


def write(path, data, headers=None):
    with path.open('w') as f:
        w=csv.DictWriter(f,headers or list(data[0]),lineterminator='\n')
        w.writeheader()
        w.writerows(data)


def main(scratch):
    history=set((scratch/'historical_accessions.txt').read_text().splitlines())
    prior=set((scratch/'historical_sequences.txt').read_text().splitlines())
    ids=json.loads((scratch/'candidate_sources.json').read_text())
    accepted=[]; audit=[]; fetched=set()
    for file in sorted(scratch.glob('genbank_*.gb')):
        for r in SeqIO.parse(file,'genbank'):
            if r.id not in ids or r.id in fetched:
                continue
            fetched.add(r.id)
            assert accession_key(r.id) not in history
            tax=r.annotations.get('taxonomy',[])
            group=next((g for g in GROUPS if g in tax),'')
            species=r.annotations.get('organism','')
            role='target' if group=='Holothuroidea' else 'background'
            named=re.fullmatch(r'[A-Z][a-z]+ [a-z][a-z-]+',species)
            annotated=features(r)
            if not annotated:
                audit.append(dict(accession=r.id,gene='',role=role,group=group,species=species,length=len(r),
                                  complete_feature=0,location='',query_groups=';'.join(ids[r.id]),
                                  status='no_supported_feature'))
            for gene,(whole,seq,location) in sorted(annotated.items()):
                item=dict(accession=r.id,gene=gene,role=role,group=group,species=species,
                          length=len(seq),complete_feature=int(whole),location=location,
                          query_groups=';'.join(ids[r.id]),status='')
                if not group or not named or species.split()[-1] in ('sp','aff','cf'):
                    item['status']='taxon_unresolved'
                elif not mitochondrial(r):
                    item['status']='mitochondrial_origin_unconfirmed'
                elif len(seq)<150 or set(seq)-set('ACGTRYSWKMBDHVN'):
                    item['status']='sequence_quality'
                elif role=='background' and not whole:
                    item['status']='background_incomplete_feature'
                elif canonical(seq) in prior:
                    item['status']='exact_historical_sequence'
                else:
                    # Exclude identical historical fragments covering at least 85% of the longer sequence.
                    reverse=seq.translate(RC)[::-1]
                    if any(min(len(old),len(seq))*100>=85*max(len(old),len(seq)) and
                           (old in seq or seq in old or old in reverse or reverse in old) for old in prior):
                        item['status']='historical_exact_containment'
                    else:
                        accepted.append((item,seq))
                audit.append(item)
    assert fetched == ids.keys(), sorted(ids.keys()-fetched)
    best={}
    for item,seq in sorted(accepted,key=lambda x:(-x[0]['complete_feature'],-x[0]['length'],
                                                  sum(ch not in 'ACGT' for ch in x[1]),x[0]['accession'])):
        key=item['role'],item['gene'],item['species']
        item['status']='same_species_alternate' if key in best else 'retained'
        if key not in best:
            best[key]=(item,seq)
    manifest=[]
    for gene in GENES:
        for role in ('target','background'):
            subset=[(row,seq) for (rr,gg,_),(row,seq) in sorted(best.items()) if (rr,gg)==(role,gene)]
            (HERE/f'{gene}_{role}.fasta').write_text(''.join(f">{row['accession']} {row['species']}\n{seq}\n" for row,seq in subset))
            manifest.extend(row for row,_ in subset)
    write(HERE/'panel.csv',manifest)
    write(HERE/'selection_audit.csv',audit)
    (HERE/'query_manifest.json').write_text(json.dumps(
        {f.stem:json.loads(f.read_text()) for f in sorted(scratch.glob('*.json'))
         if 'query' in json.loads(f.read_text()) and json.loads(f.read_text()).get('querytranslation')},indent=2)+'\n')
    (HERE/'historical_inputs.json').write_bytes((scratch/'historical_inputs.json').read_bytes())
    (HERE/'historical_accessions.txt').write_bytes((scratch/'historical_accessions.txt').read_bytes())
    (HERE/'candidate_sources.json').write_bytes((scratch/'candidate_sources.json').read_bytes())
    hash_file=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    (HERE/'curation_provenance.json').write_text(json.dumps(dict(
        unique_candidate_accessions=len(fetched),retained_marker_references=len(manifest),
        historical_accession_count=len(history),historical_sequence_count=len(prior),
        historical_sequence_index_sha256=hash_file(scratch/'historical_sequences.txt'),
        genbank_batches={p.name:hash_file(p) for p in sorted(scratch.glob('genbank_*.gb'))}),
        indent=2)+'\n')
    print('Fetched',len(fetched),'records; selected',len(manifest),'marker references')

if __name__=='__main__':
    main(Path(sys.argv[1]))
