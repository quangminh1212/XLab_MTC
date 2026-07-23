"""Logic consistency audit: years body vs ledger, character ages, intro order, milestones."""
import re, json
from pathlib import Path
from collections import defaultdict

P = Path(r'C:/Dev/XLab_MTC/Niên Đại Thương Gia')
with open(P / 'system_ledger.json', 'r', encoding='utf-8') as f:
    LEDGER = json.load(f)
CH = LEDGER['chapters']

issues = []

def read(n):
    paths = list(P.glob(f'Chương {n} - *.txt'))
    return paths[0].read_text(encoding='utf-8') if paths else ''

def years_in(text):
    return [int(x) for x in re.findall(r'\b((?:19|20)\d{2})\b', text)]

def panel_fields(text):
    y = re.search(r'Năm:\s*(\d{4})', text)
    exp = re.search(r'Tổng EXP:\s*([\d,]+)', text)
    sp = re.search(r'Không gian kho:\s*([\d,]+)\s*m', text)
    return (
        int(y.group(1)) if y else None,
        int(exp.group(1).replace(',', '')) if exp else None,
        int(sp.group(1).replace(',', '')) if sp else None,
    )

# 1) Panel vs ledger for ALL chapters
panel_mismatch = 0
missing_panel = 0
for n in range(1, 361):
    t = read(n)
    py, pe, ps = panel_fields(t)
    d = CH[str(n)]
    if py is None or pe is None or ps is None:
        missing_panel += 1
        issues.append(f'Ch{n}: missing panel fields year={py} exp={pe} space={ps}')
        continue
    if pe != d['exp_total'] or ps != d['space_m2'] or py != d['year']:
        panel_mismatch += 1
        if panel_mismatch <= 15:
            issues.append(
                f"Ch{n}: panel year/exp/sp={py}/{pe}/{ps} vs ledger {d['year']}/{d['exp_total']}/{d['space_m2']}"
            )

# 2) Body year vs ledger year (allow ±2 for flashback/memory)
year_drift = []
for n in range(1, 361):
    t = read(n)
    # only first 800 chars of body for "present" year
    body = re.sub(r'={2,}.*?={2,}', '', t, count=1, flags=re.DOTALL)
    head = body[:900]
    ys = years_in(head)
    ledger_y = CH[str(n)]['year']
    # ignore 2024 memory in early ch if rebirth memory
    present = [y for y in ys if not (n < 20 and y >= 2000)]
    if present:
        # take most common or first
        main = present[0]
        if abs(main - ledger_y) > 3 and n not in (1, 357, 263):  # flashbacks ok
            year_drift.append((n, main, ledger_y, present[:5]))

# 3) Character first-mention order
first_mention = {}
chars = {
    'Lan': r'\bLan\b',
    'bà Hà': r'bà Hà|Bà Hà',
    'Hạnh': r'\bcô Hạnh\b|\bHạnh\b',
    'Minh kỹ sư': r'kỹ sư Minh|\bMinh\b(?!h)',  # weak
    'Sato': r'\bSato\b',
    'Tanaka': r'\bTanaka\b',
}
for n in range(1, 361):
    t = read(n)
    for name, pat in chars.items():
        if name not in first_mention and re.search(pat, t):
            first_mention[name] = n

# 4) Age mentions for Hùng
age_mentions = []
for n in [1, 50, 93, 95, 96, 118, 182, 251, 299, 343, 360]:
    t = read(n)
    ages = re.findall(r'(?:Hùng|ông)\s+(?:được\s+)?(\d{2})\s*tuổi|tuổi\s+(\d{2})|năm\s+(\d{4}).{0,40}(?:sinh|tuổi)', t)
    age_mentions.append((n, ages[:5], CH[str(n)]['year']))

# 5) Milestone numbers exact
ms_ok = 0
ms_bad = []
for k, v in LEDGER['milestones'].items():
    n = int(k)
    t = read(n)
    py, pe, ps = panel_fields(t)
    if pe == v['exp'] and ps == v['space']:
        ms_ok += 1
    else:
        ms_bad.append((n, pe, ps, v))

# 6) Keys
t1 = read(1)
t360 = read(360)
key1 = 'Đau. Đau như thể' in t1[:400]
key360 = 'Tôi đã làm được' in t360
about_home = 'Về nhà' in t360

# 7) Word floor
shorts = []
for n in range(1, 361):
    t = read(n)
    w = len(re.split(r'\s+', t.strip()))
    if w < 3000:
        shorts.append((n, w))

print('=== LOGIC AUDIT ===')
print(f'panel missing: {missing_panel}')
print(f'panel vs ledger mismatches: {panel_mismatch}')
print(f'milestones OK: {ms_ok}/{len(LEDGER["milestones"])} bad={ms_bad[:5]}')
print(f'year drifts (>3y body vs ledger): {len(year_drift)}')
for row in year_drift[:20]:
    print(' ', row)
print('first mentions:', first_mention)
print('age samples:', age_mentions)
print(f'Ch1 key: {key1} | Ch360 key: {key360} | Về nhà: {about_home}')
print(f'shorts <3000: {len(shorts)} {shorts[:10]}')
if issues[:10]:
    print('sample issues:')
    for i in issues[:10]:
        print(' ', i)
