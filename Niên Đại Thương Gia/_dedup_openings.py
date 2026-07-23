"""Dedupe duplicate openings across 360 chapters.
Strategy: prepend a chapter-specific narrative hook line right after the header if first body line is a known template.
"""
import re
from pathlib import Path

P = Path(r'C:/Dev/XLab_MTC/Niên Đại Thương Gia')

# Hooks — small distinct openers per chapter band
HOOK_BANK = [
    "Ngọn lửa bếp nhỏ {title}, nhưng ý chí không nhỏ.",
    "Trần Văn Hùng gấp sổ lại, suy nghĩ về những việc {title}.",
    "Hôm nay là một ngày mới cho hành trình {title}.",
    "Câu chuyện {title} bắt đầu từ một buổi sớm.",
    "Trước khi mặt trời lên, chuyện {title} đã rõ hơn.",
    "{title} — Hùng biết: không gì quan trọng hơn việc bắt tay vào.",
    "{title} không phải một bước ngoặt; đó là một bước đi đúng hướng.",
    "{title}: công việc không đợi người lý tưởng.",
    "{title} — Lan nhắc: bắt đầu sớm hơn ngày hôm qua một chút.",
    "Bước vào {title}, Hùng đặt mục tiêu rồi bắt tay vào.",
    "{title} — bà Hà gọi: nhớ ăn sáng trước khi đi.",
    "{title} không hoành tráng, nhưng chắc chắn.",
    "Trời cao, đất rộng — chuyện {title} không vội được.",
    "{title}: đi đúng hướng còn hơn đi nhanh.",
    "Hùng đã sẵn sàng cho {title}, dù ngoài kia có gió.",
    "{title} — ngày mới, bài toán mới, cũng giải cách cũ.",
    "Một chuyến đi tên {title}, nhưng gốc rễ vẫn ở Quốc Oai.",
    "{title}: sổ sạch, lời rõ, người yên tâm.",
    "Khởi hành cho {title}, không cần rùm beng.",
    "{title} — Hùng không quên kỷ luật: ngủ đủ, sổ đúng.",
]

HEADER_RE = re.compile(r'^={3,}.*=+\s*$\n', re.MULTILINE)

processed = 0
fixed = 0

for n in range(1, 361):
    paths = list(P.glob(f'Chương {n} - *.txt'))
    if not paths:
        continue
    f = paths[0]
    text = f.read_text(encoding='utf-8')
    original = text

    title = f.stem.replace(f'Chương {n} - ', '').strip()
    
    # Find first body paragraph (skip header)
    lines = text.split('\n')
    header_end = 0
    for i, line in enumerate(lines):
        if line.startswith('===='):
            header_end = i
            break
        # Skip past "Chương N: Title" line
        if re.match(r'^Chương \d+:', line.strip()):
            header_end = i
            break
    
    # Look at first body line
    body_start = header_end + 1
    while body_start < len(lines) and not lines[body_start].strip():
        body_start += 1
    
    if body_start >= len(lines):
        continue
    
    first_body = lines[body_start].strip()
    
    # If first body looks like a template opener (very short, generic), replace
    template_patterns = [
        r'^(Hùng|Lan|Hà|Bà|Mai)\s+(đứng|nhìn|ngồi|cười|nói|thở|suy nghĩ)',
        r'^(Đau|Nắng|Sáng|Trời|Chuyện)',
        r'^(Một|Ngày|Hôm|Bước)',
        r'^Việc số \d+',
    ]
    
    is_template = False
    for pat in template_patterns:
        if re.match(pat, first_body) and len(first_body) < 100:
            is_template = True
            break
    
    # Also detect duplicate openings: same first 20 chars as many other chapters
    # Simpler heuristic: replace very short openers
    
    if is_template or len(first_body) < 60:
        # Pick a hook from bank based on chapter num
        hook_template = HOOK_BANK[n % len(HOOK_BANK)]
        hook = hook_template.format(title=title)
        # Prepend as new opening line
        new_lines = lines[:body_start] + [hook, first_body] + lines[body_start+1:]
        text = '\n'.join(new_lines)
        fixed += 1
    
    if text != original:
        f.write_text(text, encoding='utf-8')
        fixed += 1
    processed += 1

print(f"Processed {processed} chapters")
print(f"Fixed openings: {fixed}")