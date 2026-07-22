# -*- coding: utf-8 -*-
"""Full QA: logic, quality flags, year continuity, open quality."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

DIR = Path(__file__).resolve().parent
OUTLINE = json.loads((DIR / "chapter_outline.json").read_text(encoding="utf-8"))
MIN = 3000


def cw(t: str) -> int:
    t = re.sub(r"={5,}", " ", t)
    t = re.sub(r"\(\d+\s*từ\)", " ", t, flags=re.I)
    return len([w for w in re.split(r"\s+", t.strip()) if w])


def body(t: str) -> str:
    t = re.sub(r"^={5,}.*?={5,}\s*", "", t, count=1, flags=re.S)
    t = re.sub(r"\n*={5,}\s*\n*\(\d+\s*từ\)\s*$", "", t, flags=re.I)
    return t.strip()


def main():
    short = []
    flags = Counter()
    open_prefix = Counter()
    year_by_ch = {}
    issues = []
    craft_ok = 0

    for n in range(1, 361):
        fs = list(DIR.glob(f"Chương {n} - *.txt"))
        if not fs:
            issues.append((n, "MISSING"))
            continue
        t = fs[0].read_text(encoding="utf-8", errors="replace")
        w = cw(t)
        b = body(t)
        title = OUTLINE["chapters"][str(n)]["title"]

        if w < MIN:
            short.append((n, w))

        # quality flags
        checks = {
            "klaus_boilerplate": "Klaus — nếu có mặt" in t,
            "toc_do": "nếu mình chỉ chạy tốc độ" in t,
            "nhịp_chương": "Nhịp chương" in t,
            "bước_meta": bool(re.search(r"\(bước \d+", t)),
            "checklist_generic": t.count("Checklist một trang") >= 1 and t.count("Không nhìn chung ổn") >= 1,
            "viec_cu_the_same": "Ê-kíp chia" in t and "hiện trường – sổ" in t,
            "pad_bo_sung": "Bổ sung" in t and "đối chiếu lời hứa" in t,
            "core": "### Diễn biến đã xác lập" in t or n == 1,
            "has_mo": "### Mở" in t or n == 1,
            "ong_khong_can": "không cần nó nữa" in t.lower(),
        }
        for k, v in checks.items():
            if v:
                flags[k] += 1

        # opening quality: first substantive paragraph
        paras = [p.strip() for p in re.split(r"\n\s*\n", b) if p.strip() and not p.strip().startswith("#")]
        first = paras[0] if paras else ""
        open_prefix[" ".join(first.split()[:8])] += 1
        # title should appear in first 400 chars of body ideally
        if title[:8] not in b[:500] and n != 1:
            flags["title_not_in_open"] += 1

        # years
        years = [int(x) for x in re.findall(r"(?:19|20)\d{2}", b) if 1980 <= int(x) <= 2030]
        if years:
            year_by_ch[n] = max(years[:5]) if len(years) >= 1 else years[0]
            # pick dominant recent year in head
            head_y = [int(x) for x in re.findall(r"(?:19|20)\d{2}", b[:1500]) if 1980 <= int(x) <= 2030]
            if head_y:
                year_by_ch[n] = Counter(head_y).most_common(1)[0][0]

        # generic craft detection
        if first.startswith("###") or len(first) < 40:
            flags["weak_open"] += 1
        else:
            craft_ok += 1

        # logic: crisis chapter without 2008
        if "2008" in title and "2008" not in b[:800]:
            issues.append((n, "crisis_title_no_2008_in_open"))
        # bank without money language
        if "ngân hàng" in title.lower() and not any(k in b[:600] for k in ["vay", "tiền", "hồ sơ", "dư nợ", "giải ngân", "bảng số"]):
            issues.append((n, "bank_no_money_lang"))

    # year regressions (big jumps back)
    prev = 0
    regressions = []
    for n in range(1, 361):
        y = year_by_ch.get(n)
        if y and prev and y < prev - 8:
            regressions.append((n, y, prev))
        if y:
            prev = max(prev, y)

    print("=== QA SUMMARY ===")
    print(f"short: {short}")
    print(f"craft_ok_opens: {craft_ok}")
    print("flags:")
    for k, v in flags.most_common():
        print(f"  {k}: {v}")
    print(f"year_regressions (>{8}y): {len(regressions)}")
    for r in regressions[:15]:
        print(" ", r)
    print(f"issues: {len(issues)}")
    for i in issues[:20]:
        print(" ", i)
    print("top open dups:")
    for k, v in open_prefix.most_common(12):
        if v > 2:
            print(f"  {v}x {k}")

    # score chapters needing rewrite
    need = []
    for n in range(1, 361):
        fs = list(DIR.glob(f"Chương {n} - *.txt"))
        t = fs[0].read_text(encoding="utf-8", errors="replace")
        score = 10
        if "Ê-kíp chia" in t and "Checklist một trang" in t:
            score -= 2
        if t.count("Bổ sung") >= 2:
            score -= 1
        if "Không nhìn chung ổn" in t:
            score -= 1
        if cw(t) < MIN:
            score -= 5
        # early foundation should have core
        if 2 <= n <= 40 and "### Diễn biến đã xác lập" not in t:
            score -= 2
        if score < 8:
            need.append((n, score))
    need.sort(key=lambda x: x[1])
    print(f"need_rewrite score<8: {len(need)}")
    print("worst 30:", need[:30])
    Path(DIR / "_qa_need.json").write_text(
        json.dumps({"need": need, "regressions": regressions, "flags": dict(flags)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
