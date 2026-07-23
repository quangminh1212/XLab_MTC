"""Final canonical audit. Ignores formatting separators; flags real prose repetition."""
import json,re,hashlib
from pathlib import Path
from collections import Counter,defaultdict
P=Path(r'C:/Dev/XLab_MTC/Niên Đại Thương Gia')
L=json.loads((P/'system_ledger.json').read_text(encoding='utf-8'))['chapters']
files={}
for f in P.glob('Chương *.txt'):
 m=re.match(r'Chương (\d+) - ',f.name)
 if m: files.setdefault(int(m.group(1)),[]).append(f)
issues=[]; shorts=[]; panels=[]; internal=[]; prose_map=defaultdict(list)
IGNORE=lambda s: not s or set(s)<=set('=-_*# ') or s.startswith(('Chương ','「Hệ thống —','Năm:','Tổng EXP:','Không gian kho:','Kỹ năng trọng yếu:','Ghi chú:'))
for n in range(1,361):
 fs=files.get(n,[])
 if len(fs)!=1: issues.append(('file',n,len(fs))); continue
 t=fs[0].read_text(encoding='utf-8'); w=len(re.split(r'\s+',t.strip()))
 if w<3000: shorts.append((n,w))
 ms=list(re.finditer(r'「Hệ thống — (?:CỘT MỐC|GHI NHẬN) ch\.(\d+)」',t))
 if not ms: panels.append((n,'missing')); continue
 p=t[ms[-1].start():]
 def val(pat):
  m=re.search(pat,p); return int(m.group(1).replace(',','')) if m else None
 got=(val(r'Năm:\s*(\d{4})'),val(r'Tổng EXP:\s*([\d,]+)'),val(r'Không gian kho:\s*([\d,]+)m²'))
 d=L[str(n)]; want=(d['year'],d['exp_total'],d['space_m2'])
 if got!=want: panels.append((n,got,want))
 lines=[]
 for line in t.splitlines():
  s=' '.join(line.split())
  if IGNORE(s) or len(s)<80: continue
  lines.append(s)
  prose_map[hashlib.sha1(s.encode()).hexdigest()].append((n,s))
 c=Counter(lines)
 for s,k in c.items():
  if k>=3: internal.append((n,k,s[:120]))
# identical long prose reused across >=3 chapters
cross=[]
for locs in prose_map.values():
 chapters=sorted(set(n for n,_ in locs))
 if len(chapters)>=3: cross.append((chapters,locs[0][1][:150]))
# keys and timeline head drift
head_drift=[]
for n in range(1,361):
 if n not in files or len(files[n])!=1: continue
 t=files[n][0].read_text(encoding='utf-8'); head='\n'.join(t.splitlines()[3:])[:1000]
 ys=[int(x) for x in re.findall(r'\b((?:19|20)\d{2})\b',head)]
 ys=[y for y in ys if not(n<20 and y>=2000)]
 if ys and abs(ys[0]-L[str(n)]['year'])>3 and n not in (1,263,357): head_drift.append((n,ys[0],L[str(n)]['year']))
t1=files[1][0].read_text(encoding='utf-8'); t360=files[360][0].read_text(encoding='utf-8')
keys=('Đau. Đau như thể' in t1[:500], 'Tôi đã làm được' in t360, 'Về nhà' in t360[-1500:])
result={'file_issues':issues,'shorts':shorts,'panel_issues':panels,'timeline_head_drift':head_drift,'internal_repetition':internal,'cross_chapter_repetition_count':len(cross),'cross_samples':cross[:30],'keys':keys}
print(json.dumps(result,ensure_ascii=False,indent=2))
if issues or shorts or panels or head_drift or internal or cross or not all(keys): raise SystemExit(2)
print('FINAL_AUDIT_OK')
