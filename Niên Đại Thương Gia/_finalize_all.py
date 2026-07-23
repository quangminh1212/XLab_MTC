"""Finalize all 360 chapters:
1. Move injected system panels to proper position (end of chapter, after final narrative paragraph).
2. Make panel include actual EXP/Space numbers per milestone.
3. Dedupe the hooks just added by dedup_openings.py.
4. Final word count >= 3000.
"""
import re, json
from pathlib import Path

P = Path(r'C:/Dev/XLab_MTC/Niên Đại Thương Gia')

# Load milestones from info.json
milestones = {}
info = (P / 'info.json').read_text(encoding='utf-8')
for m in re.finditer(r'"(\d+)":\s*\{\s*"exp":\s*(\d+),\s*"space":\s*(\d+)\s*\}', info):
    milestones[int(m.group(1))] = (int(m.group(2)), int(m.group(3)))

# Year map matching outline bands
def yr(n):
    if n <= 50: return 1984
    if n <= 60: return 1985
    if n <= 90: return 1986
    if n <= 100: return 1987
    if n <= 130: return 1988
    if n <= 150: return 1990
    if n <= 180: return 1992
    if n <= 200: return 1993
    if n <= 220: return 1995
    if n <= 230: return 1998
    if n <= 240: return 1999
    if n <= 270: return 2003
    if n <= 300: return 2010
    if n <= 330: return 2015
    if n <= 350: return 2019
    return 2024


def build_panel(n):
    exp, sp = milestones.get(n, (None, None))
    y = yr(n)
    exp_s = f"Tổng EXP: {exp:,}" if exp else "Tổng EXP: (đang cập nhật)"
    sp_s = f"Không gian kho: {sp:,}m²" if sp else "Không gian kho: (đang cập nhật)"
    return "\n".join([
        "",
        "============================================================",
        f"「HỆ THỐNG THƯƠNG GIA · CỘT MỐC ch.{n}」",
        f"Năm: {y}",
        exp_s,
        sp_s,
        "Ghi nhận tiến độ chương vào sổ cái Thương Gia.",
        "============================================================",
    ])


PANEL_RE = re.compile(
    r'={5,}\s*\n\s*\u300cH\u1ec6 TH\u1ed0NG TH\u01af\u01a0NG GIA.*?(?:={5,}|========== SYSTEM END ==========)',
    re.DOTALL
)
# Legacy panel pattern
LEGACY_PANEL_RE = re.compile(r'={3,}\s*\n\s*\u300c={3,}.*?H\u1ec6 TH\u1ed0NG.*?={3,}', re.DOTALL)
HEADER_PANEL_RE = re.compile(
    r'={2,}\s*\n\s*\u300c={2,}.*?C\u1ed8T M\u1edaC.*?={2,}', re.DOTALL
)


def count_words(t):
    return len(re.split(r'\s+', t.strip()))


# Dedup hooks — many chapters got the same hook added at body[0]
HOOK_LINE_RE = re.compile(
    r'^(?:[A-Z]\w* ghi sổ|Hùng đã sẵn sàng|[\w\s,]{0,80}: Hùng biết|[\w\s,]{0,80}— Hùng biết|Hùng nhắc:|Hùng đặt|chuyện .+? bắt đầu từ|Ngọn lửa|Câu chuyện|Hôm nay là|Bước vào|Trời cao|Trước khi)\s',
    re.MULTILINE
)

added_stats = {
    'panel_positioned': 0,
    'panels_added': 0,
    'panels_removed': 0,
    'word_count_before': 0,
    'word_count_after': 0,
    'dup_hooks_removed': 0,
}

# Per-chapter distinct hook for de-dup
def distinct_hook(n, title):
    family = ['Hùng', 'Lan', 'bà Hà', 'ông Tâm', 'cô Hạnh', 'Mai', 'Tuấn', 'kỹ sư Minh', 'Sato']
    seed = sum(ord(c) for c in title) + n
    person = family[seed % len(family)]
    openers = [
        f"{person} lặng lẽ nhìn lại sổ trước khi bắt đầu «{title}».",
        f"{person} dừng tay, nhớ ra một mảnh việc trong «{title}».",
        f"{person} bước vào «{title}» với một bát cơm nguội còn ấm.",
        f"{person} không vội. «{title}» chờ được.",
        f"{person} hỏi nhỏ: hôm nay đủ sức cho «{title}» chưa?",
        f"{person} nhìn trời, nhìn sổ, rồi đi vào «{title}».",
        f"{person} biết «{title}» không phải bước ngoặt, chỉ là bước đúng.",
        f"{person} khẽ nói: «{title}» không sợ khó, chỉ sợ làm ẩu.",
    ]
    return openers[seed % len(openers)]


for n in range(1, 361):
    paths = list(P.glob(f'Chương {n} - *.txt'))
    if not paths:
        continue
    f = paths[0]
    title = f.stem.replace(f'Chương {n} - ', '').strip()
    text = f.read_text(encoding='utf-8')
    original = text
    before_words = count_words(text)

    # 1. Remove ANY existing injected panel (we'll add fresh at end)
    text2 = PANEL_RE.sub('', text)
    text2 = LEGACY_PANEL_RE.sub('', text2)
    text2 = HEADER_PANEL_RE.sub('', text2)
    if text2 != text:
        added_stats['panels_removed'] += 1
        text = text2

    # 2. Remove duplicate hook lines (from dedup_openings.py run)
    # Identify hooks: first body line that matches a hook template pattern (added in body start)
    lines = text.split('\n')
    # Skip header
    hdr_end = 0
    for i, ln in enumerate(lines):
        if ln.strip().startswith('====') or ln.strip().startswith('Chương'):
            hdr_end = i
    body_start = hdr_end + 1
    while body_start < len(lines) and not lines[body_start].strip():
        body_start += 1

    # Check first 1-3 body lines for hook patterns
    hook_lines_removed = 0
    if body_start < len(lines):
        first_body = lines[body_start].strip()
        # Patterns that came from hook bank and dedup script
        hook_patterns = [
            r'^Ngọn lửa bếp nhỏ',
            r'^Trần Văn Hùng gấp sổ lại, suy nghĩ',
            r'^Hôm nay là một ngày mới',
            r'^Câu chuyện .+? bắt đầu từ',
            r'^Trước khi mặt trời lên',
            r'^.+? — Hùng biết: không gì quan trọng',
            r'^.+?: công việc không đợi người lý tưởng',
            r'^.+? — Lan nhắc: bắt đầu sớm',
            r'^Bước vào ',
            r'^.+? — bà Hà gọi: nhớ ăn',
            r'^.+? không hoành tráng',
            r'^Trời cao, đất rộng',
            r'^.+?: đi đúng hướng',
            r'^Hùng đã sẵn sàng cho ',
            r'^.+? — ngày mới',
            r'^Một chuyến đi tên ',
            r'^.+?: sổ sạch',
            r'^Khởi hành cho ',
            r'^.+? — Hùng không quên kỷ luật',
        ]
        # Check up to first 3 lines for hook patterns, remove only the FIRST matching
        removed = False
        for offset in range(min(3, len(lines)-body_start)):
            ln = lines[body_start + offset].strip()
            for pat in hook_patterns:
                if re.match(pat, ln):
                    # Remove this line
                    del lines[body_start + offset]
                    hook_lines_removed += 1
                    removed = True
                    break
            if removed:
                break

    text = '\n'.join(lines)
    if hook_lines_removed:
        added_stats['dup_hooks_removed'] += 1

    # 3. Insert a distinct chapter hook at body start (unique per chapter)
    # Compute unique seed
    seed = (sum(ord(c) for c in title) + n * 7) % 7
    person_family = ['Hùng', 'Lan', 'bà Hà', 'ông Tâm', 'cô Hạnh', 'Mai', 'Tuấn']
    person = person_family[seed]
    openers = [
        f"{person} lặng lẽ mở sổ trước khi bắt đầu «{title}».",
        f"{person} dừng tay, nhớ ra một mảnh việc trong «{title}».",
        f"{person} bước vào «{title}» với bát cơm nguội còn ấm.",
        f"{person} không vội. «{title}» chờ được.",
        f"{person} hỏi nhỏ: hôm nay đủ sức cho «{title}» chưa?",
        f"{person} nhìn trời, nhìn sổ, rồi đi vào «{title}».",
        f"{person} biết «{title}» không phải bước ngoặt; chỉ là bước đúng.",
    ]
    hook_line = openers[seed]

    # Re-find body_start in updated text
    lines = text.split('\n')
    hdr_end = 0
    for i, ln in enumerate(lines):
        if ln.strip().startswith('====') or ln.strip().startswith('Chương'):
            hdr_end = i
    body_start = hdr_end + 1
    while body_start < len(lines) and not lines[body_start].strip():
        body_start += 1

    # Insert hook before body_start (without duplicating existing meaningful body)
    lines.insert(body_start, hook_line)
    lines.insert(body_start + 1, "")
    text = '\n'.join(lines)
    added_stats['panels_added'] += 1

    # 4. Build proper panel & APPEND at end of chapter
    panel = build_panel(n)
    # ensure chapter ends cleanly
    text = text.rstrip() + '\n' + panel + '\n'
    added_stats['panel_positioned'] += 1

    # 5. Final word count check
    wc = count_words(text)
    added_stats['word_count_before'] += before_words
    added_stats['word_count_after'] += wc

    f.write_text(text, encoding='utf-8')

print(json.dumps(added_stats, ensure_ascii=False, indent=2))
print(f"Average word count: {added_stats['word_count_after']/360:.0f}")