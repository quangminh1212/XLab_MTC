"""Inject system panels + fix milestones + fix anachronisms for Niên Đại Thương Gia."""
import re, json
from pathlib import Path

P = Path(r'C:/Dev/XLab_MTC/Niên Đại Thương Gia')

# Load system_ledger for accurate per-chapter EXP/Space
ledger_path = P / 'system_ledger.json'
if ledger_path.exists():
    with open(ledger_path, 'r', encoding='utf-8') as f:
        # It's JSON; load the full data
        raw = json.load(f)
    print(f"Ledger loaded: {type(raw)}")
else:
    print("No system_ledger.json found!")
    raw = None

# Parse milestones from info.json
milestones = {}
info_path = P / 'info.json'
with open(info_path, 'r', encoding='utf-8') as f:
    content = f.read()
    # Find milestone blocks
    m = re.findall(r'"(\d+)":\s*\{\s*"exp":\s*(\d+),\s*"space":\s*(\d+)\s*\}', content)
    for num, exp, sp in m:
        milestones[int(num)] = int(exp), int(sp)

print(f"Milestones found: {len(milestones)} keys")
for k in sorted(milestones.keys())[:10]:
    print(f"  {k}: EXP={milestones[k][0]}, Space={milestones[k][1]}m²")

# ── System panel templates ──
def build_system_panel(ch_num, target_exp=None, target_space=None):
    """Build a proper system panel for any chapter."""
    year_map = get_year_for_chapter(ch_num)
    
    lines = [
        "",
        "========== HỆ THỐNG THƯƠNG GIA ==========",
        f"ch.{ch_num} · CỘT MỐC",
        f"Năm: {year_map}",
    ]
    if target_exp is not None:
        lines.append(f"Tổng EXP: {target_exp:,}")
    if target_space is not None:
        lines.append(f"Không gian kho: {target_space:,}m²")
    lines.append("Ghi nhận tiến độ hiện tại")
    lines.append("========== SYSTEM END ==========")
    return "\n".join(lines)


def get_year_for_chapter(n):
    """Determine year based on chapter number bands matching outline."""
    if n <= 10: return 1983
    if n <= 20: return 1983
    if n <= 30: return 1983
    if n <= 40: return 1984
    if n <= 50: return 1984
    if n <= 60: return 1985
    if n <= 70: return 1985
    if n <= 80: return 1986
    if n <= 90: return 1986
    if n <= 100: return 1987
    if n <= 110: return 1987
    if n <= 120: return 1988
    if n <= 130: return 1988
    if n <= 140: return 1989
    if n <= 150: return 1990
    if n <= 160: return 1990
    if n <= 170: return 1991
    if n <= 180: return 1992
    if n <= 190: return 1992
    if n <= 200: return 1993
    if n <= 210: return 1994
    if n <= 220: return 1995
    if n <= 230: return 1998
    if n <= 240: return 1999
    if n <= 250: return 2000
    if n <= 260: return 2002
    if n <= 270: return 2005
    if n <= 280: return 2007
    if n <= 290: return 2009
    if n <= 300: return 2010
    if n <= 310: return 2012
    if n <= 320: return 2013
    if n <= 330: return 2015
    if n <= 340: return 2017
    if n <= 350: return 2019
    if n <= 360: return 2024
    return 1983


# Read a sample chapter to understand structure
sample_text = (P / 'Chương 2 - Bữa tối đầu tiên.txt').read_text(encoding='utf-8')
first_lines = sample_text.split('\n')[:5]
last_lines = sample_text.split('\n')[-15:]
print("\n=== Sample chapter structure ===")
print("First 5 lines:")
for l in first_lines:
    print(f"  |{l}|")
print("Last 15 lines:")
for l in last_lines:
    print(f"  |{l}|")


# Check if any existing panel exists
panel_re = re.compile(r'HỆ THỐNG|Thông báo.*Hệ thống|CỘT MỐC')
found_panels = []
for n in range(1, 361):
    path = list(P.glob(f'Chương {n} - *.txt'))
    if not path:
        continue
    text = path[0].read_text(encoding='utf-8')
    if panel_re.search(text):
        found_panels.append(n)

print(f"\nChapters already containing a system panel: {len(found_panels)} out of 360")
print(f"Need panels: {360-len(found_panels)}")
if found_panels:
    print(f"Sample panel chapters: {found_panels[:10]}")

# Fix anachronisms
anach_fixes = {
    'Facebook': lambda m: '[mạng xã hội]',
    'Singapore': lambda m: 'một thành phố trong khu vực',
}

print("\n\n=== Starting fixes ===")

fixed_count = 0
missing_panel_count = 0

for n in range(1, 361):
    paths = list(P.glob(f'Chương {n} - *.txt'))
    if not paths:
        print(f"  Ch{n}: SKIPPED (no file)")
        continue
    
    filepath = paths[0]
    text = filepath.read_text(encoding='utf-8')
    original = text
    changes_made = []
    
    # 1. Fix anachronisms
    lower = text.lower()
    if 'facebook' in lower:
        text = re.sub(r'\bFacebook\b', 'mạng xã hội', text, flags=re.IGNORECASE)
        changes_made.append('Facebook→mạng xã hội')
    if re.search(r'\bSingapore\b', text, re.IGNORECASE) and n < 25:
        # Only fix if contextually wrong era (early chapters shouldn't reference Singapore by name)
        text = re.sub(r'\bSingapore\b', 'một thành phố trong khu vực', text, flags=re.IGNORECASE)
        changes_made.append('Singapore→thành phố khu vực')
    
    # 2. Add system panel near end (before closing section)
    has_panel = bool(panel_re.search(text))
    if not has_panel:
        target_exp = milestones.get(n, (None, None))[0]
        target_space = milestones.get(n, (None, None))[1]
        
        panel_text = build_system_panel(n, target_exp, target_space)
        
        # Insert before final closing section or at end
        # Look for closing markers
        close_markers = ['### Khép', 'Khép lại', 'Kết ', 'Kết luận']
        insert_pos = len(text)
        
        for marker in close_markers:
            pos = text.rfind(marker)
            if pos > -1:
                insert_pos = pos
                break
        
        text = text[:insert_pos] + '\n' + panel_text + '\n' + text[insert_pos:]
        changes_made.append(f'Added system panel')
        missing_panel_count += 1
    
    # Write back
    if changes_made:
        filepath.write_text(text, encoding='utf-8')
        fixed_count += 1
        if n % 100 == 0:
            print(f"  Processed {n}/360...")

print(f"\n=== DONE ===")
print(f"Fixed chapters: {fixed_count}")
print(f"Added missing panels: {missing_panel_count}")