"""Apply verified continuity fixes, then audit canonical end panels."""
import json, re
from pathlib import Path
from collections import Counter

P = Path(r'C:/Dev/XLab_MTC/Niên Đại Thương Gia')
L = json.loads((P/'system_ledger.json').read_text(encoding='utf-8'))['chapters']
changes=[]

def file_for(n):
    fs=list(P.glob(f'Chương {n} - *.txt'))
    if len(fs)!=1: raise RuntimeError(f'Ch{n}: {len(fs)} files')
    return fs[0]

def replace_all(n, old, new):
    f=file_for(n); t=f.read_text(encoding='utf-8'); c=t.count(old)
    if c:
        f.write_text(t.replace(old,new),encoding='utf-8'); changes.append((n,old,new,c))

# Confirmed current-scene year drift.
for n in (254,255): replace_all(n,'2006','2010')
for n in (271,273,274): replace_all(n,'2010','2006')
# Ch299: born 1960, canonical year 2010 => 50.
replace_all(299,'2012','2010')
replace_all(299,'55 tuổi','50 tuổi')
f299=file_for(299)
new299=f299.with_name(f299.name.replace('Hùng 55 tuổi','Hùng 50 tuổi'))
if new299!=f299:
    if new299.exists(): raise RuntimeError(f'target exists: {new299}')
    f299.rename(new299); changes.append((299,'rename',new299.name,1))

# Clarify only intermediate transaction EXP labels; final ledger panel remains canonical.
for n in (4,6,8,9):
    f=file_for(n); t=f.read_text(encoding='utf-8')
    # Inside transaction messages, "Tổng EXP" is running balance, not chapter-end ledger.
    out=re.sub(r'(Giao dịch[^\n」]*?)(Tổng EXP:)',r'\1Số dư EXP lúc giao dịch: ',t)
    if out!=t:
        f.write_text(out,encoding='utf-8'); changes.append((n,'clarify EXP transaction','',1))

# Audit last canonical panel only.
def last_panel(t):
    ms=list(re.finditer(r'「Hệ thống — (?:CỘT MỐC|GHI NHẬN) ch\.(\d+)」',t))
    if not ms: return None
    s=ms[-1].start(); return t[s:]

def num(pattern,s):
    m=re.search(pattern,s); return int(m.group(1).replace(',','')) if m else None

nums={}; shorts=[]; panel_bad=[]; maxrep=[]
for n in range(1,361):
    f=file_for(n); nums[n]=f.name; t=f.read_text(encoding='utf-8')
    w=len(re.split(r'\s+',t.strip()))
    if w<3000: shorts.append((n,w))
    p=last_panel(t)
    if not p: panel_bad.append((n,'missing')); continue
    py=num(r'Năm:\s*(\d{4})',p); pe=num(r'Tổng EXP:\s*([\d,]+)',p); ps=num(r'Không gian kho:\s*([\d,]+)m²',p)
    d=L[str(n)]
    if (py,pe,ps)!=(d['year'],d['exp_total'],d['space_m2']): panel_bad.append((n,(py,pe,ps),(d['year'],d['exp_total'],d['space_m2'])))
    counts=Counter(x.strip() for x in t.splitlines() if len(x.strip())>40)
    mr=max(counts.values(),default=0)
    if mr>=5: maxrep.append((n,mr,counts.most_common(1)[0][0][:100]))

# Current-head year drift, excluding explicit rebirth/finale flashbacks.
year_drift=[]
for n in range(1,361):
    t=file_for(n).read_text(encoding='utf-8')
    body='\n'.join(t.splitlines()[3:])[:1000]
    ys=[int(x) for x in re.findall(r'\b((?:19|20)\d{2})\b',body)]
    ys=[y for y in ys if not (n<20 and y>=2000)]
    if ys and abs(ys[0]-L[str(n)]['year'])>3 and n not in (1,263,357): year_drift.append((n,ys[0],L[str(n)]['year']))

ch1=file_for(1).read_text(encoding='utf-8')
ch360=file_for(360).read_text(encoding='utf-8')
print('CHANGES',len(changes))
for x in changes: print(x)
print('AUDIT files',len(nums),'shorts',shorts,'panel_bad',panel_bad,'year_drift',year_drift,'maxrep',maxrep)
print('KEYS', 'Đau. Đau như thể' in ch1[:500], 'Tôi đã làm được' in ch360, 'Về nhà' in ch360[-1500:])
assert len(nums)==360 and not shorts and not panel_bad and not year_drift and not maxrep
assert 'Đau. Đau như thể' in ch1[:500] and 'Tôi đã làm được' in ch360 and 'Về nhà' in ch360[-1500:]
print('VERIFIED_OK')
