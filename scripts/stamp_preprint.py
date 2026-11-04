"""Synchronize the GitHub preprint release across the three language editions."""
from datetime import datetime
from pathlib import Path
import re
import sys
from zoneinfo import ZoneInfo
version=sys.argv[1]
assert re.fullmatch(r'1\.\d+',version)
today=datetime.now(ZoneInfo('Asia/Shanghai')).date()
date=f'{today.day} {today:%B %Y}'
for name in ['README.md','README.zh-CN.md','CITATION.bib','CITATION.cff','publications/MiCucumber_preprint.md','publications/build_preprint.py']:
    p=Path(name);s=p.read_text()
    s=re.sub(r'preprint-v1\.\d+',f'preprint-v{version}',s)
    s=re.sub(r'(Preprint v|preprint v|预印本 v|預印本 v|version: "|version )1\.\d+',lambda m:m[1]+version,s)
    s=re.sub(r'(Preprint v[\d.]+ · |Computational preprint · )\d+ [A-Za-z]+ \d{4}',lambda m:m[1]+date,s)
    s=re.sub(r'((?:预印本|預印本) v[\d.]+ · )\d+ 年 \d+ 月 \d+ 日',lambda m:m[1]+f'{today.year} 年 {today.month} 月 {today.day} 日',s)
    s=re.sub(r'date-released: "[\d-]+"',f'date-released: "{today}"',s)
    s=re.sub(r'^  year: \d+$',f'  year: {today.year}',s,flags=re.M)
    p.write_text(s)
