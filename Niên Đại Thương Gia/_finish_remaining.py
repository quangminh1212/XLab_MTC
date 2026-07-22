# -*- coding: utf-8 -*-
"""Pad shorts in remaining ranges + era fixes + full verify 1-360."""
from __future__ import annotations

import re
from pathlib import Path

from _deep_rewrite import count_words, pad_literary, year_loc, OUTLINE

DIR = Path(__file__).resolve().parent
REMAINING = list(range(31, 90)) + list(range(131, 200)) + list(range(241, 300))


def main():
    padded = []
    for n in REMAINING:
        fs = list(DIR.glob(f"Chương {n} - *.txt"))
        if not fs:
            continue
        t = fs[0].read_text(encoding="utf-8")
        # era sentence fixes
        fixes = [
            (r"\. giai đoạn ", ". Đây là giai đoạn "),
            (r"\. toàn cầu hóa:", ". Bối cảnh toàn cầu hóa:"),
            (r"\. khủng hoảng và phòng thủ:", ". Bối cảnh khủng hoảng và phòng thủ:"),
            (r"\. ảnh hưởng xã hội", ". Bối cảnh ảnh hưởng xã hội"),
            (r"\. di sản: bàn giao", ". Bối cảnh di sản: bàn giao"),
            (r"\. thời bao cấp:", ". Bối cảnh thời bao cấp:"),
            (r"\. bùng nổ khu vực:", ". Bối cảnh bùng nổ khu vực:"),
            (r"\. giai đoạn Đổi Mới", ". Đây là giai đoạn Đổi Mới"),
        ]
        for a, b in fixes:
            t = re.sub(a, b, t)

        w = count_words(t)
        title = OUTLINE["chapters"][str(n)]["title"]
        y, loc = year_loc(n, title)
        if w < 3000:
            body = re.sub(r"\n*={5,}\s*\n*\(\d+\s*từ\)\s*$", "", t, flags=re.I).rstrip()
            body = pad_literary(body, n, title, y, loc)
            w2 = count_words(body)
            t = body + "\n\n" + ("=" * 60) + f"\n({w2} từ)\n"
            padded.append((n, w, w2))
        else:
            # rewrite footer word count if we only fixed era
            body = re.sub(r"\n*={5,}\s*\n*\(\d+\s*từ\)\s*$", "", t, flags=re.I).rstrip()
            w2 = count_words(body)
            t = body + "\n\n" + ("=" * 60) + f"\n({w2} từ)\n"
        fs[0].write_text(t, encoding="utf-8")

    print("padded", padded)

    # full book verify
    short = []
    formula = 0
    cores = 0
    for n in range(1, 361):
        fs = list(DIR.glob(f"Chương {n} - *.txt"))
        t = fs[0].read_text(encoding="utf-8")
        w = count_words(t)
        if w < 3000:
            short.append((n, w))
        if "Klaus — nếu có mặt" in t or "nếu mình chỉ chạy tốc độ" in t:
            formula += 1
        if "### Diễn biến đã xác lập" in t or n == 1:
            cores += 1
    print("ALL short", short)
    print("formula", formula, "cores", cores)

    for n in (31, 50, 89, 131, 155, 199, 241, 270, 299):
        t = list(DIR.glob(f"Chương {n} - *.txt"))[0].read_text(encoding="utf-8")
        body = re.sub(r"^={5,}.*?={5,}\s*", "", t, count=1, flags=re.S)
        print(f"Ch{n}: {count_words(t)}w | {' '.join(body.split()[:28])}")


if __name__ == "__main__":
    main()
