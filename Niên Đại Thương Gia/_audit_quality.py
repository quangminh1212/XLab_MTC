# -*- coding: utf-8 -*-
"""Quality audit for all chapters."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

DIR = Path(__file__).resolve().parent


def analyze(n: int) -> dict | None:
    fs = list(DIR.glob(f"Chương {n} - *.txt"))
    if not fs:
        return None
    t = fs[0].read_text(encoding="utf-8", errors="replace")
    words = len([w for w in re.split(r"\s+", t) if w])
    flags = []
    checks = {
        "formula_open": any(
            x in t
            for x in [
                "chưa kịp sáng hẳn",
                "Làm đúng – làm đủ – làm bền",
                "hồ sơ mang tên",
                "Tiếng chuông cửa công ty vang lên sớm",
                "Bản đồ trên tường đầy đinh ghim",
                "Mưa đầu mùa phủ",
            ]
        ),
        "phan_loi": "### Phần lõi" in t,
        "extra_fill": any(
            x in t
            for x in [
                "Ở lớp sâu hơn",
                "ba vòng: kỹ thuật",
                "Không ai được giấu lỗ hổng",
                "góc nhìn công nhân và tổ trưởng",
                "Cột xanh để khen sau",
            ]
        ),
        "ong_khong_can": "không cần nó nữa" in t.lower(),
        "klaus_neu": "Klaus — nếu có mặt" in t or "Klaus - nếu có mặt" in t,
        "boilerplate_dialogue": "nếu mình chỉ chạy tốc độ" in t,
        "boilerplate_ba": "nhà này giàu vì thương người" in t
        and t.count("nhà này giàu vì thương người") >= 1
        and "### Phần" in t or "Làm đúng" in t,
    }
    for k, v in checks.items():
        if v:
            flags.append(k)
    years = sorted(set(re.findall(r"(?:19|20)\d{2}", t)))
    # opening uniqueness fingerprint
    body = re.sub(r"^={5,}.*?={5,}\s*", "", t, count=1, flags=re.S)
    first = " ".join(body.split()[:25])
    return {
        "n": n,
        "file": fs[0].name,
        "words": words,
        "flags": flags,
        "years": years[:10],
        "first": first[:140],
        "score": max(0, 10 - len(flags) * 1.5),
    }


def main():
    rows = []
    for n in range(1, 361):
        a = analyze(n)
        if a:
            rows.append(a)

    formula = [r for r in rows if "formula_open" in r["flags"] or "extra_fill" in r["flags"]]
    expanded = [r for r in rows if "phan_loi" in r["flags"]]
    low = [r for r in rows if r["score"] < 6]

    print("=== SUMMARY ===")
    print(f"Total: {len(rows)}")
    print(f"Formula-heavy: {len(formula)}")
    print(f"Expanded-with-core: {len(expanded)}")
    print(f"Low quality score (<6): {len(low)}")

    print("\n=== SAMPLE TIMELINE ===")
    for n in [1, 20, 50, 60, 90, 113, 120, 150, 154, 155, 170, 200, 221, 270, 300, 330, 356, 360]:
        r = next(x for x in rows if x["n"] == n)
        print(f"Ch{n:3d} w={r['words']:4d} score={r['score']:.1f} flags={r['flags']} years={r['years'][:6]}")
        print(f"     {r['first']}")

    # flag frequency
    c = Counter()
    for r in rows:
        c.update(r["flags"])
    print("\n=== FLAG COUNTS ===")
    for k, v in c.most_common():
        print(f"  {k}: {v}")

    # write list of chapters needing rewrite
    need = [r["n"] for r in rows if r["score"] < 7 or "formula_open" in r["flags"] or "extra_fill" in r["flags"] or "boilerplate_dialogue" in r["flags"]]
    Path(DIR / "_need_rewrite.txt").write_text(
        "\n".join(str(n) for n in need), encoding="utf-8"
    )
    print(f"\nNeed rewrite: {len(need)} chapters -> _need_rewrite.txt")

    # continuity: year jumps backward
    print("\n=== YEAR REGRESSION (heuristic first year in file) ===")
    prev = 0
    for r in rows:
        ys = [int(y) for y in r["years"] if 1980 <= int(y) <= 2030]
        if not ys:
            continue
        y0 = ys[0]
        if prev and y0 < prev - 5:
            print(f"  Ch{r['n']}: year {y0} after prev~{prev} (possible regression)")
        prev = max(prev, y0) if ys else prev


if __name__ == "__main__":
    main()
