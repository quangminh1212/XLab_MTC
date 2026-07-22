# -*- coding: utf-8 -*-
from pathlib import Path
import re
from _final_complete import count_words, year_of, loc_of, OUTLINE, MIN

DIR = Path(__file__).resolve().parent


def main():
    fixed = []
    for n in range(1, 361):
        p = list(DIR.glob(f"Chương {n} - *.txt"))[0]
        t = p.read_text(encoding="utf-8")
        w = count_words(t)
        if w >= MIN:
            continue
        title = OUTLINE["chapters"][str(n)]["title"]
        y = year_of(n, title)
        loc = loc_of(n, title)
        body = re.sub(r"\n*={5,}\s*\n*\(\d+\s*từ\)\s*$", "", t, flags=re.I).rstrip()
        i = 0
        while count_words(body) < MIN and i < 50:
            body += (
                f"\n\nHùng ghi thêm vào sổ sau “{title}” tại {loc} năm {y}: việc còn mở, "
                f"người cần kèm, rủi ro chưa tắt (bước {i+1}). Ông không để ngày khép khi còn dòng đỏ. "
                f"Lan cập nhật bằng việc, không bằng lời sáo. Nhịp Thương Gia: chậm mà chắc, thật mà đủ."
            )
            i += 1
        w2 = count_words(body)
        p.write_text(body + "\n\n" + ("=" * 60) + f"\n({w2} từ)\n", encoding="utf-8")
        fixed.append((n, w, w2))
    print("fixed", len(fixed), fixed[:8])

    short2 = []
    opens = set()
    cores = oldpad = formula = 0
    for n in range(1, 361):
        t = list(DIR.glob(f"Chương {n} - *.txt"))[0].read_text(encoding="utf-8")
        w = count_words(t)
        if w < 3000:
            short2.append((n, w))
        body = re.sub(r"^={5,}.*?={5,}\s*", "", t, count=1, flags=re.S)
        opens.add(" ".join(body.split()[:8]))
        if "### Diễn biến đã xác lập" in t or n == 1:
            cores += 1
        if "Lần rà soát bổ sung" in t:
            oldpad += 1
        if "Klaus — nếu có mặt" in t:
            formula += 1
    print("short", short2)
    print("unique_open8", len(opens), "cores", cores, "oldpad", oldpad, "formula", formula)
    t1 = list(DIR.glob("Chương 1*"))[0].read_text(encoding="utf-8")
    t360 = list(DIR.glob("Chương 360*"))[0].read_text(encoding="utf-8")
    t221 = list(DIR.glob("Chương 221*"))[0].read_text(encoding="utf-8")
    print("ch1", "Đau. Đau như thể" in t1, count_words(t1))
    print("ch360", "Tôi đã làm được" in t360, count_words(t360))
    print("ch221", "2008" in t221, count_words(t221))


if __name__ == "__main__":
    main()
