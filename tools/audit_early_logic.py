# -*- coding: utf-8 -*-
"""Audit early chapters: pad pollution, contradictions, continuity."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"C:\Dev\XLab_MTC\Niên Đại Thương Gia")
OL = json.loads((ROOT / "chapter_outline.json").read_text(encoding="utf-8"))


def files():
    o = {}
    for f in ROOT.glob("Chương *.txt"):
        m = re.search(r"(\d+)", f.name)
        if m:
            o[int(m.group(1))] = f
    return o


PAD_MARKERS = [
    r"^### Lớp sâu",
    r"^### Nhịp",
    r"^### Thử nhỏ",
    r"^### Thoại",
    r"^### Nhà",
    r"^### Xung đột nhỏ",
    r"^### Kết quả",
    r"^### Khép",
    r"^Hùng đi chậm quanh khu vực việc",
    r"^Ông dừng lại chỗ dễ bỏ qua nhất",
    r"^Trong “.+\" năm \d{4} tại",
    r"^Chốt ý nghĩa chương này",
    r"^Lan gõ cửa nhẹ",
    r"^Ông ghi vào cuối trang:",
]


def find_pad_start(text: str) -> int:
    """Return char index where pad section likely starts, or -1."""
    best = -1
    # Prefer structural ### headers after mid-chapter
    mid = len(text) // 3
    for pat in PAD_MARKERS:
        for m in re.finditer(pat, text, re.M):
            if m.start() > mid:
                if best < 0 or m.start() < best:
                    best = m.start()
    return best


def audit_range(a: int, b: int):
    fs = files()
    report = []
    for n in range(a, b + 1):
        f = fs[n]
        t = f.read_text(encoding="utf-8")
        meta = OL["chapters"][str(n)]
        pad_i = find_pad_start(t)
        core = t[:pad_i] if pad_i > 0 else t
        pad = t[pad_i:] if pad_i > 0 else ""
        issues = []

        # money absurd for early days without business
        if n == 1 and re.search(r"Đối tác tại", pad):
            issues.append("PAD: 'Đối tác' ngày 1 khi chưa kinh doanh")
        if n == 1 and re.search(r"Tin đồn nội bộ", pad):
            issues.append("PAD: 'Tin đồn nội bộ' khi chưa có tổ chức")
        if re.search(r"Chưa từng gặp mặt", t) and re.search(r"ôm ông lên vai|nấu thịt|mười tám tuổi", t):
            issues.append("LOGIC: cha 'chưa từng gặp' vs có ký ức tuổi thơ/18 tuổi")
        # skill regression
        if re.search(r"Thương mại lv1.*Thương mại lv2|Thương mại lv2.*Thương mại lv1", t, re.S):
            if re.search(r"Thương mại lv1", pad) and re.search(r"cấp 2|lv2", core):
                issues.append("PAD: skill lv1 sau khi đã lv2")
        # location outline vs text
        if n <= 10:
            if "Hà Nội" in (meta.get("location") or "") and "huyện" in t[:800].lower():
                pass
        # system double
        sys_blocks = len(re.findall(r"「Hệ thống|Hệ thống Thương Gia", t))
        if sys_blocks >= 3 and pad_i > 0:
            issues.append(f"Nhiều block hệ thống ({sys_blocks}), có thể pad chồng")

        # year in body vs outline
        years = re.findall(r"\b(198[0-9])\b", core[:1500])
        if years and meta.get("year") and int(years[0]) != meta["year"] and n > 1:
            # only flag if clearly wrong era
            pass

        report.append(
            {
                "n": n,
                "title": meta["title"],
                "words": len(t.split()),
                "core_words": len(core.split()),
                "pad_words": len(pad.split()) if pad else 0,
                "pad_ratio": round(len(pad.split()) / max(1, len(t.split())), 2) if pad else 0,
                "issues": issues,
                "pad_preview": pad[:120].replace("\n", " | ") if pad else "",
            }
        )
    return report


if __name__ == "__main__":
    import json as J

    r = audit_range(1, 20)
    for row in r:
        print(
            f"Ch{row['n']:02d} core={row['core_words']:4d} pad={row['pad_words']:4d} "
            f"({row['pad_ratio']:.0%}) | {row['title']}"
        )
        for i in row["issues"]:
            print("   !", i)
        if row["pad_preview"]:
            print("   pad:", row["pad_preview"][:100])
    print("---")
    print("with_pad", sum(1 for x in r if x["pad_words"] > 50))
    print("with_issues", sum(1 for x in r if x["issues"]))
