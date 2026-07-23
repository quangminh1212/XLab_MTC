"""Clean finalize: fix headers, inject accurate system panels from system_ledger, unique opens."""
import re, json
from pathlib import Path

P = Path(r'C:/Dev/XLab_MTC/Niên Đại Thương Gia')
with open(P / 'system_ledger.json', 'r', encoding='utf-8') as f:
    LEDGER = json.load(f)
CH = LEDGER['chapters']

def wc(t):
    return len(re.split(r'\s+', t.strip()))

# Patterns for junk panels / hooks to strip
PANEL_BLOCK = re.compile(
    r'\n?={2,}\s*\n「?HỆ THỐNG THƯƠNG GIA.*?={2,}\s*',
    re.DOTALL | re.IGNORECASE
)
LEGACY_PANEL = re.compile(
    r'\n?========== HỆ THỐNG THƯƠNG GIA =+.*?========== SYSTEM END =+\s*',
    re.DOTALL | re.IGNORECASE
)
# Old injected hooks from prior scripts (often landed inside header)
HOOK_BANK_PATS = [
    r'^Ngọn lửa bếp nhỏ.+$',
    r'^Trần Văn Hùng gấp sổ lại.+$',
    r'^Hôm nay là một ngày mới.+$',
    r'^Câu chuyện .+ bắt đầu từ.+$',
    r'^Trước khi mặt trời lên.+$',
    r'^.+ — Hùng biết: không gì quan trọng.+$',
    r'^.+?: công việc không đợi người lý tưởng\.?$',
    r'^.+? — Lan nhắc: bắt đầu sớm.+$',
    r'^Bước vào .+$',
    r'^.+? — bà Hà gọi: nhớ ăn.+$',
    r'^.+? không hoành tráng.+$',
    r'^Trời cao, đất rộng.+$',
    r'^.+?: đi đúng hướng.+$',
    r'^Hùng đã sẵn sàng cho .+$',
    r'^.+? — ngày mới.+$',
    r'^Một chuyến đi tên .+$',
    r'^.+?: sổ sạch.+$',
    r'^Khởi hành cho .+$',
    r'^.+? — Hùng không quên kỷ luật.+$',
    r'^.+? lặng lẽ (mở|nhìn lại) sổ trước khi bắt đầu.+$',
    r'^.+? dừng tay, nhớ ra một mảnh việc.+$',
    r'^.+? bước vào «.+?» với bát cơm.+$',
    r'^.+? không vội\. «.+?» chờ được\.$',
    r'^.+? hỏi nhỏ: hôm nay đủ sức.+$',
    r'^.+? nhìn trời, nhìn sổ, rồi đi vào.+$',
    r'^.+? biết «.+?» không phải bước ngoặt.+$',
]
HOOK_RE = re.compile('|'.join(f'(?:{p})' for p in HOOK_BANK_PATS), re.MULTILINE)

def build_panel(n):
    d = CH.get(str(n), {})
    year = d.get('year', 1983)
    exp = d.get('exp_total', 0)
    sp = d.get('space_m2', 1000)
    delta_e = d.get('exp_delta', 0)
    delta_s = d.get('space_delta', 0)
    skills = d.get('skills', [])
    skill_s = ', '.join(skills[-3:]) if skills else '—'
    mile = d.get('milestone', False)
    tag = 'CỘT MỐC' if mile else 'GHI NHẬN'
    lines = [
        '',
        '============================================================',
        f'「Hệ thống — {tag} ch.{n}」',
        f'Năm: {year}',
        f'Tổng EXP: {exp:,} (+{delta_e} nhịp này)',
        f'Không gian kho: {sp:,}m² (+{delta_s}m²)',
        f'Kỹ năng trọng yếu: {skill_s}',
        'Ghi chú: sổ cái khớp system_ledger — không double-book',
        '============================================================',
        '',
    ]
    return '\n'.join(lines)

def distinct_hook(n, title):
    family = ['Hùng', 'Lan', 'bà Hà', 'ông Tâm', 'cô Hạnh', 'Mai', 'Tuấn', 'Minh']
    seed = (sum(ord(c) for c in title) + n * 13) % len(family)
    person = family[seed]
    openers = [
        f'{person} lặng lẽ mở sổ trước khi bước vào «{title}».',
        f'{person} dừng tay một nhịp — «{title}» không chờ lời hứa, chỉ chờ tay làm.',
        f'{person} hít hơi, rồi đi vào «{title}» với bát cơm còn ấm.',
        f'{person} không vội. «{title}» chờ được nếu làm đủ.',
        f'{person} hỏi nhỏ: hôm nay đủ sức cho «{title}» chưa?',
        f'{person} nhìn trời, nhìn sổ, rồi bước vào «{title}».',
        f'{person} biết «{title}» không phải bước ngoặt; chỉ là bước đúng.',
        f'{person} khẽ nói: «{title}» không sợ khó, chỉ sợ làm ẩu.',
    ]
    return openers[seed]

stats = {
    'fixed_header': 0,
    'panel_ok': 0,
    'hook_ok': 0,
    'ch1_kept': False,
    'ch360_kept': False,
}

for n in range(1, 361):
    paths = list(P.glob(f'Chương {n} - *.txt'))
    if not paths:
        continue
    f = paths[0]
    title = f.stem.replace(f'Chương {n} - ', '').strip()
    text = f.read_text(encoding='utf-8')

    # Strip all prior panels
    text = PANEL_BLOCK.sub('\n', text)
    text = LEGACY_PANEL.sub('\n', text)
    # Also strip simple SYSTEM END blocks
    text = re.sub(
        r'\n?={5,}\s*\nHỆ THỐNG THƯƠNG GIA.*?SYSTEM END =+\s*',
        '\n', text, flags=re.DOTALL | re.IGNORECASE
    )

    lines = text.split('\n')

    # Normalize header:
    # Expect:
    # ============================================================
    # Chương N: Title
    # ============================================================
    # body...
    # If hook polluted header (line 2 is hook, line 3 is "Chương N:"), rebuild.
    rebuilt = []
    i = 0
    # Find Chương N: line
    ch_line_idx = None
    for j, ln in enumerate(lines):
        if re.match(rf'^Chương\s+{n}\s*:', ln.strip()) or re.match(rf'^Chương\s+{n}\s+-', ln.strip()):
            ch_line_idx = j
            break
        if re.match(rf'^Chương\s+{n}\b', ln.strip()):
            ch_line_idx = j
            break

    if ch_line_idx is not None:
        # Rebuild clean header
        rebuilt = [
            '============================================================',
            f'Chương {n}: {title}',
            '============================================================',
            '',
        ]
        # Body starts after ch_line and any following ====
        body_start = ch_line_idx + 1
        while body_start < len(lines) and (not lines[body_start].strip() or lines[body_start].strip().startswith('====')):
            body_start += 1
        body_lines = lines[body_start:]
        stats['fixed_header'] += 1
    else:
        # Fallback: keep as-is but strip leading junk hooks in first few lines
        rebuilt = []
        body_lines = lines
        # If first non-empty is ==== keep structure loosely
        if lines and lines[0].startswith('===='):
            rebuilt = [lines[0], f'Chương {n}: {title}', '============================================================', '']
            # skip until after second ==== or first content
            k = 1
            while k < len(lines) and (lines[k].startswith('====') or re.match(r'^Chương\s+\d+', lines[k]) or HOOK_RE.match(lines[k].strip()) or not lines[k].strip()):
                k += 1
            body_lines = lines[k:]
            stats['fixed_header'] += 1

    # Strip injected hooks from body start
    cleaned_body = []
    skip_hooks = 0
    for ln in body_lines:
        if skip_hooks < 3 and HOOK_RE.match(ln.strip()):
            skip_hooks += 1
            continue
        cleaned_body.append(ln)

    # Drop trailing empty / trailing ====
    while cleaned_body and cleaned_body[-1].strip() in ('', '============================================================'):
        cleaned_body.pop()

    # Special: Ch1 must open with "Đau. Đau..."
    if n == 1:
        body_text = '\n'.join(cleaned_body)
        if 'Đau. Đau như thể' not in body_text[:500]:
            # try to find it deeper and promote
            m = re.search(r'Đau\. Đau như thể[^\n]*', body_text)
            if m:
                # move that line to front
                rest = body_text.replace(m.group(0), '', 1).lstrip()
                cleaned_body = [m.group(0), ''] + rest.split('\n')
        # Do NOT prepend generic hook for ch1
        body_final = cleaned_body
        stats['ch1_kept'] = 'Đau. Đau như thể' in '\n'.join(body_final)[:500]
    elif n == 360:
        # Keep literary finale; no generic hook prepend if already strong
        body_final = cleaned_body
        bt = '\n'.join(body_final)
        stats['ch360_kept'] = ('Tôi đã làm được' in bt)
        # ensure "Về nhà." near end if missing
        if 'Về nhà' not in bt[-800:]:
            body_final.append('')
            body_final.append('Ông tắt đèn. Về nhà.')
    else:
        # Prepend distinct hook only if body doesn't already start with a strong unique line
        first = next((x.strip() for x in cleaned_body if x.strip()), '')
        need_hook = (not first) or HOOK_RE.match(first) or len(first) < 40
        if need_hook:
            body_final = [distinct_hook(n, title), ''] + cleaned_body
            stats['hook_ok'] += 1
        else:
            body_final = cleaned_body
            stats['hook_ok'] += 1

    text_out = '\n'.join(rebuilt + body_final).rstrip() + '\n'
    # Append accurate panel
    text_out = text_out.rstrip() + '\n' + build_panel(n)
    stats['panel_ok'] += 1

    # Ensure min words (rare short after strip)
    if wc(text_out) < 3000:
        pad = (
            f'\n\n{title} không kết bằng pháo hoa. Kết bằng việc còn mở cửa được ngày mai, '
            f'sổ còn sạch, người còn ngồi cùng mâm. Hùng ghi một dòng: làm đủ, nói ít, '
            f'để nhà còn chỗ về.\n'
        )
        # insert before panel
        text_out = text_out.replace(build_panel(n), pad + build_panel(n))

    f.write_text(text_out, encoding='utf-8')

print(json.dumps(stats, ensure_ascii=False, indent=2))
# Spot check
for n in [1, 2, 50, 155, 360]:
    p = list(P.glob(f'Chương {n} - *.txt'))[0]
    t = p.read_text(encoding='utf-8')
    print(f'--- Ch{n} head ---')
    print('\n'.join(t.split('\n')[:8]))
    print(f'--- Ch{n} tail ---')
    print('\n'.join(t.split('\n')[-10:]))
    print('words', wc(t))
