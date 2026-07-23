"""Full logic quality + consistency audit for Niên Đại Thương Gia (360 chapters)."""
import re, os, json, sys
from collections import Counter, defaultdict
from pathlib import Path

P = Path(r'C:/Dev/XLab_MTC/Niên Đại Thương Gia')

# ── helpers ──
def read_ch(n):
    f = P / f'Chương {n} - *.txt'
    matches = list(P.glob(f'Chương {n} - *.txt'))
    if len(matches) != 1:
        return None, f"MATCH PROBLEM: {len(matches)} files for ch{n}"
    return matches[0].read_text(encoding='utf-8'), None

def cw(text):
    """Approximate word count."""
    return len(re.split(r'\s+', text.strip()))

def extract_years(text):
    """Find all years mentioned."""
    return [int(y) for y in re.findall(r'\b(19|20)\d{2}\b', text)]

PAD_MARKERS = [
    'Thêm một lớp rà soát cho',
    'không còn dòng đỏ bỏ quên',
    '(Nhịp chương',
    'Hùng ghi thêm vào sổ sau',
    'Lần rà soát bổ sung',
    'Ê-kíp chia việc quanh',
    'Ba câu trước khi ngủ',
    'được viết lại bằng lời thợ cũng hiểu',
    'Nhịp bổ sung',
    '(Nhịp đời',
    '(Nhịp N.)',
]

PAD_TAIL = [
    'Hùng ghi sổ trước khi ngủ',
    'Hùng ghi sổ tay giấy vàng ố',
    'Một đồng lời sạch đáng hơn',
    'Người ngoài bàn tán',
    'thì thầm ông lớn',
    'Đêm gió đi qua',
    'Đêm, tiếng dế',
    'Uy tín đi trước tiếng rao',
    'Khi mệt, ông nhớ bát cháo',
    'Trên đường, bụi đỏ bám ống quần',
    'Lan giữ nhịp sổ và người',
    'Thất bại nhỏ được mang ra bàn',
    'Hiện trường dạy nhiều hơn phòng điều hành',
    'Ông gấp sổ. Nghe nhà thở. Ngủ như người còn việc.',
]

ANACHRONISMS = [
    ('seoul', 'Seoul'), ('london', 'London'), ('paris', 'Paris'),
    ('singapore', 'Singapore'), ('mercedes', 'Mercedes'), ('facebook', 'Facebook'),
    ('slide', 'slide'), ('kpi', 'KPI'), ('dashboard', 'dashboard'),
    ('app store', 'App Store'), ('iphone', 'iPhone'), ('android', 'Android'),
    ('wifi', 'WiFi'), ('internet', 'Internet'), ('smartphone', 'smartphone'),
    ('email', 'email'), ('gmail', 'Gmail'),
]

MILESTONES = {
    1: (0, 1000), 5: (120, 1200), 10: (350, 1200), 20: (900, 1600),
    30: (1800, 2000), 40: (3200, 2500), 50: (5200, 3000), 60: (7800, 3500),
    75: (11000, 4200), 89: (14500, 5000), 100: (16500, 5500), 112: (18000, 5900),
    130: (19500, 6200), 155: (24000, 8000), 175: (30000, 10000),
    200: (38000, 12000), 221: (43000, 15000), 240: (52000, 20000),
    270: (62000, 25000), 279: (72000, 35000), 300: (80000, 45000),
    330: (81000, 45000), 355: (95000, 55000), 360: (98500, 60000),
}


def find_in_text(text, patterns):
    found = []
    lower = text.lower()
    for pat, label in patterns:
        if pat in lower:
            found.append(label)
    return found


def has_system_panel(text):
    return bool(re.search(r'Hệ thống[^：:]*:[^：:]*(?:EXP|Không gian)', text, re.IGNORECASE))


def find_exp_space(text):
    """Extract any EXP and space numbers."""
    exp = re.findall(r'EXP[:\s]*(?:Total\s+)?(\d[\d,.]*)', text, re.IGNORECASE)
    space = re.findall(r'(?:Không gian|space|km?\s*m?\s*2?)[^：:]*(:?\s*[-–]\s*)?(.+?)(?:\s*$|\n)', text, re.IGNORECASE | re.MULTILINE)
    m2 = re.findall(r'(\d[\d,.]*)\s*m\s*2', text)
    return exp, m2


# ── MAIN AUDIT ──
results = []
errors = {'short': [], 'maxrep_5': [], 'no_panel': [], 'anachronism': [], 'missing_milestone': [], 'milestone_wrong': [], 'pad_tail': [], 'dup_open': []}

# Track opening words for dup detection
openings = {}

print("=== LOGIC QUALITY AUDIT: Niên Đại Thương Gia (360 chapters) ===")
print(f"Path: {P}\n")

for n in range(1, 361):
    text, err = read_ch(n)
    if err or not text:
        errors['short'].append((n, f'MISSING: {err}'))
        print(f"  Ch{n}: MISSING/ERROR: {err}")
        continue

    wc = cw(text)
    maxrep = 0
    rep_lines = []
    lines = text.split('\n')
    line_counts = Counter(lines)
    for line, cnt in line_counts.most_common(1):
        if len(line.strip()) > 30 and cnt > 3:
            maxrep = cnt
            rep_lines.append(line.strip()[:100])

    opens = text.split('\n')[2:6] if len(text.split('\n')) > 5 else []
    first_line = text.strip().split('\n')[0]
    open_key = ' '.join(first_line.split()[:8]).lower().strip('=:█▌|')
    
    years = set(extract_years(text))
    ana = find_in_text(text, ANACHRONISMS)
    panels = has_system_panel(text)
    exp_nums, m2_nums = find_exp_space(text)
    pad_hits = sum(1 for t in PAD_MARKERS if t in text)
    pad_tail_hits = sum(1 for t in PAD_TAIL if t in text)
    
    # Check milestone
    milestone_err = []
    if n in MILESTONES:
        target_exp, target_space = MILESTONES[n]
        # Look for the milestone panel
        milev_re = re.search(
            rf'(?:Tổng\s+)?EXP\s*:?\s*(\d[\d,.]*)\s*\(', 
            text, re.IGNORECASE
        )
        sp_re = re.search(rf'(\d[\d,.]*)\s*m\s*2', text)
        
        if milev_re:
            actual_exp = int(milev_re.group(1).replace(',','').replace('.',''))
            diff = abs(actual_exp - target_exp)
            if diff > target_exp * 0.1:
                milestone_err.append(f'EXP={actual_exp} target={target_exp}')
        else:
            milestone_err.append('No EXP panel found')
            
        if sp_re:
            actual_sp = int(sp_re.group(1).replace(',','').replace('.',''))
        elif target_space <= 60000:
            milestone_err.append(f'No space number (target {target_space})')
    
    ch_result = {
        'num': n,
        'words': wc,
        'maxrep': maxrep,
        'years': sorted(years),
        'ana': ana,
        'has_panel': panels,
        'exp_found': exp_nums,
        'm2_found': m2_nums,
        'pad_markers': pad_hits,
        'pad_tails': pad_tail_hits,
        'milestone_issues': milestone_err,
    }
    results.append(ch_result)
    
    # Collect errors
    if wc < 3000:
        errors['short'].append((n, wc))
    if maxrep >= 5:
        errors['maxrep_5'].append((n, maxrep, rep_lines[:2]))
    if not panels:
        errors['no_panel'].append(n)
    if ana and n < 25:
        errors['anachronism'].append((n, ana, years))
    if milestone_err:
        errors['missing_milestone'].append((n, milestone_err))
    if pad_tail_hits > 2:
        errors['pad_tail'].append((n, pad_tail_hits))
    
    if open_key in openings:
        errors['dup_open'].append((n, openings[open_key], open_key[:60]))
    openings.setdefault(open_key, n)
    
    # Progress
    if n % 50 == 0:
        print(f"  Processed {n}/360...")

# ── SUMMARY ──
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
all_words = [r['words'] for r in results]
avg_wc = sum(all_words)/len(all_words)
print(f"Avg word count: {avg_wc:.0f} (min: {min(all_words)}, max: {max(all_words)})")
print(f"Chapters <3000 words: {len(errors['short'])}")
print(f"Chapters with maxrep>=5: {len(errors['maxrep_5'])}")
print(f"Chapters without system panel: {len(errors['no_panel'])}")
print(f"Chapters with anachronisms (<ch25): {len(errors['anachronism'])}")
print(f"Milestone issues: {len(errors['missing_milestone'])}")
print(f"Pad tail issues (>2 hits): {len(errors['pad_tail'])}")
print(f"Duplicate openings: {len(errors['dup_open'])}")

# Year range per chapter band
band_years = defaultdict(set)
for r in results:
    b = min(r['num']//10*10, 10)*10 // 10 if r['num']>10 else 10
    band_years[b].update(r['years'])
print("\nYear ranges by decade-band:")
for band in sorted(band_years.keys()):
    yrs = sorted(band_years[band])
    print(f"  Ch{band}s: {yrs[:20]}{'...' if len(yrs)>20 else ''} ({len(yrs)} unique)")

# Part boundary chapters check
part_boundaries = [1, 50, 60, 89, 100, 112, 130, 155, 200, 221, 240, 270, 300, 330, 355, 360]
print("\nPart boundary details:")
for pb in part_boundaries:
    if pb <= 360:
        res = [r for r in results if r['num']==pb]
        if res:
            r = res[0]
            print(f"  Ch{pb}: words={r['words']} panel={r['has_panel']} milestone={r['milestone_issues']} years={r['years']}")

# Top offenders
print("\n--- TOP ISSUES ---")
if errors['short']:
    print(f"\nSHORT (<3000 words): {len(errors['short'])}")
    for n, wc in errors['short'][:30]:
        print(f"  Ch{n}: {wc}w")

if errors['maxrep_5']:
    print(f"\nMAXREP≥5: {len(errors['maxrep_5'])}")
    for n, mr, lines_s in errors['maxrep_5'][:20]:
        print(f"  Ch{n}: maxrep={mr}, sample: {lines_s[0][:80] if lines_s else '?'}")

if errors['no_panel']:
    print(f"\nNO SYSTEM PANEL: {len(errors['no_panel'])}")
    if len(errors['no_panel']) > 20:
        chunks = [errors['no_panel'][i:i+20] for i in range(0, len(errors['no_panel']), 20)]
        for i, chunk in enumerate(chunks):
            print(f"  Chunk {i+1}: {chunk}")
    else:
        print(f"  {errors['no_panel']}")

if errors['anachronism']:
    print(f"\nANACHRONISMS: {len(errors['anachronism'])}")
    for n, ana, yrs in errors['anachronism'][:30]:
        print(f"  Ch{n}: ana={ana} years={yrs}")

if errors['missing_milestone']:
    print(f"\nMILESTONE ISSUES: {len(errors['missing_milestone'])}")
    for n, iss in errors['missing_milestone'][:20]:
        print(f"  Ch{n}: {iss}")

if errors['pad_tail']:
    print(f"\nPAD TAILS: {len(errors['pad_tail'])}")
    for n, h in errors['pad_tail'][:20]:
        print(f"  Ch{n}: {h} hits")

print("\n=== DONE ===")
sys.stdout.flush()