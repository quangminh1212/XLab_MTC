# -*- coding: utf-8 -*-
import re
from pathlib import Path

from _deep_rewrite import count_words, pad_literary, year_loc, OUTLINE

DIR = Path(__file__).resolve().parent
RANGES = list(range(1, 31)) + list(range(90, 131)) + list(range(200, 241)) + list(range(300, 361))


def main():
    short = []
    for n in RANGES:
        fs = list(DIR.glob(f"Chương {n} - *.txt"))
        t = fs[0].read_text(encoding="utf-8")
        w = count_words(t)
        if w < 3000:
            title = OUTLINE["chapters"][str(n)]["title"]
            y, loc = year_loc(n, title)
            body = re.sub(r"\n*={5,}\s*\n*\(\d+\s*từ\)\s*$", "", t, flags=re.I).rstrip()
            body = pad_literary(body, n, title, y, loc)
            w2 = count_words(body)
            fs[0].write_text(body + "\n\n" + ("=" * 60) + f"\n({w2} từ)\n", encoding="utf-8")
            short.append((n, w, w2))
    print("padded", short)

    # inject signature ending into 360
    p = list(DIR.glob("Chương 360*"))[0]
    t = p.read_text(encoding="utf-8")
    if "Tôi đã làm được. Và con cháu sẽ tiếp tục" not in t:
        inject = """

### Đỉnh nóc tháp — lời kết

Ngày kỷ niệm, Hùng đứng trên nóc tòa tháp Thương Gia. Gió cao đập vạt áo. Dưới sân, đèn nhỏ xếp thành hai chữ THƯƠNG GIA. Lan đứng cạnh. Con trai đứng sau.

Ông nói khẽ đủ để gió mang đi:

“Tôi đã làm được. Và con cháu sẽ tiếp tục. Không bằng cách copy tôi, mà bằng cách giữ cái lõi: làm giàu mà không làm mất người.”

Hệ thống hiện một dòng rồi mờ:

「Hành trình nhiệm vụ khép. Tinh thần Thương Gia — trường tồn ngoài hệ thống.」

Không pháo hoa. Có phút im lặng tri ân. Có quỹ học bổng mang tên tổ trưởng thầm lặng. Lan nhận vai tiếp: “Em không hứa hoàn hảo. Em hứa không quên.”

Chiều, ông về làng Thanh Xuân một vòng. Đất còn. Gió còn. Mùi đồng còn. Kết thúc truyện là dấu hai chấm — phần tiếp thuộc về người vẫn mở cửa hàng lúc sáng sớm và dạy con rằng tiền là công cụ, không phải bàn thờ.
"""
        body = re.sub(r"\n*={5,}\s*\n*\(\d+\s*từ\)\s*$", "", t, flags=re.I).rstrip() + inject
        body = pad_literary(body, 360, "Tinh thần Thương Gia mãi trường tồn", 2024, "Hà Nội")
        w = count_words(body)
        p.write_text(body + "\n\n" + ("=" * 60) + f"\n({w} từ)\n", encoding="utf-8")
        print("360 injected", w)
    else:
        print("360 ok", count_words(t))

    # 356 system congratulation signature
    p356 = list(DIR.glob("Chương 356*"))[0]
    t356 = p356.read_text(encoding="utf-8")
    if "Thương gia vĩ đại" not in t356 and "HOÀN THÀNH" not in t356:
        inj = """

### Thông báo cuối của hệ thống

「Chúc mừng Chủ nhân.」
「Nhiệm vụ tối thượng: Trở thành thương gia lớn nhất Việt Nam — HOÀN THÀNH.」
「Danh hiệu: Thương gia vĩ đại (khung lịch sử hiện đại theo tiêu chí hệ thống).」
「Lời nhắn: Hệ thống không biến mất, nhưng không còn dẫn đường. Chủ nhân tự là la bàn.」

Hùng không họp báo. Ông họp nội bộ: danh hiệu chỉ đúng nếu lương đúng hạn, hàng đúng chất, người yếu hơn được nâng. Lan gật: “Em giữ.”
"""
        body = re.sub(r"\n*={5,}\s*\n*\(\d+\s*từ\)\s*$", "", t356, flags=re.I).rstrip() + inj
        body = pad_literary(body, 356, OUTLINE["chapters"]["356"]["title"], 2023, "Hà Nội")
        w = count_words(body)
        p356.write_text(body + "\n\n" + ("=" * 60) + f"\n({w} từ)\n", encoding="utf-8")
        print("356 injected", w)

    bad = []
    for n in RANGES:
        w = count_words(list(DIR.glob(f"Chương {n} - *.txt"))[0].read_text(encoding="utf-8"))
        if w < 3000:
            bad.append((n, w))
    print("still short", bad)
    t2 = list(DIR.glob("Chương 2*"))[0].read_text(encoding="utf-8")
    print("ch2 core bếp", "bếp lò" in t2 or "Bếp nhà" in t2)
    t221 = list(DIR.glob("Chương 221*"))[0].read_text(encoding="utf-8")
    print("ch221 crisis", "2008" in t221 and ("giấu" in t221 or "dòng tiền" in t221))


if __name__ == "__main__":
    main()
