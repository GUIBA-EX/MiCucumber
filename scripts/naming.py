"""One-pass legacy-to-current identifier mapping; nucleotide strings are unchanged."""
import re
REGIONS={'v4opt':'S','S':'M','M':'L','L':'XL'}
TOKENS={f'MiCucumber-{old}':f'MiCucumber-{new}' for old,new in REGIONS.items()}
for old,new in REGIONS.items():
 for n in (1,2):
  for t in (1,2):TOKENS[f'MiCucumber-{old}_N{n}_B5_T{t}']=f'MiCucumber-{new}-D{n}'
  TOKENS[f'MiCucumber-{old}-ND-{n}pair']=f'MiCucumber-{new}-ND{n}'
TOKENS.update({'MiCucumber-v4-original':'MiCucumber-S-original','MiCucumber_v4':'MiCucumber-S-original','original-v4':'MiCucumber-S-original'})
# ND identifiers are renamed in the same regex substitution, never through successive S->M->L steps.
PATTERN=re.compile('|'.join(map(re.escape,sorted(TOKENS,key=len,reverse=True)))+r'|ND_(?:v4opt|S|M|L)_\d+')
def text(value):
 def replace(match):
  s=match.group()
  if s in TOKENS:return TOKENS[s]
  _,region,index=s.split('_');return f'ND_{REGIONS[region]}_{index}'
 return PATTERN.sub(replace,value)
def normalize(value):
 if isinstance(value,str):return text(value)
 if isinstance(value,list):return [normalize(x) for x in value]
 if isinstance(value,dict):return {text(k):normalize(v) for k,v in value.items()}
 return value
