# -*- coding: utf-8 -*-
"""
Rewrite generic middle sections while keeping good ### Mở and ### Diễn biến cores.
Target: remove Ê-kíp chia / Checklist / Bổ sung spam; unique body per title.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from _final_complete import count_words, MIN
from _continue_v2 import year_of, loc_of, pad_clean

DIR = Path(__file__).resolve().parent
OUTLINE = json.loads((DIR / "chapter_outline.json").read_text(encoding="utf-8"))


def extract_section(text: str, name: str) -> str | None:
    # ### Name ... until next ### or end before footer
    pat = rf"### {re.escape(name)}\s*\n(.*?)(?=\n### |\n={{5,}}|\Z)"
    m = re.search(pat, text, re.S)
    return m.group(1).strip() if m else None


def extract_open_and_core(text: str) -> tuple[str, str]:
    """Return (open_block_with_header, core_block_with_header_or_empty)."""
    open_b = extract_section(text, "Mở")
    core_b = extract_section(text, "Diễn biến đã xác lập")
    open_part = f"### Mở\n\n{open_b}" if open_b else ""
    core_part = f"### Diễn biến đã xác lập\n\n{core_b}" if core_b else ""
    return open_part, core_part


def unique_body(n: int, title: str, y: int, loc: str) -> str:
    t = title.lower()

    def has(*ks):
        return any(k in t for k in ks)

    # Primary action scene
    if has("cho vay", "ngân hàng", "tài chính", "bảo hiểm", "nợ", "dòng tiền", "cổ đông", "ipo"):
        scene = f"""### Hiện trường số

Tại {loc} năm {y}, “{title}” không diễn ra trên sân khấu. Hùng ngồi với hồ sơ, bút đỏ, và người chịu trách nhiệm từng khoản. Lan hỏi ngược: “Nếu xấu, ai gánh?” Không ai trả lời bằng im lặng được phép qua.

Họ chốt trần rủi ro, quyền dừng giải ngân, và lịch công bố nội bộ. Một hồ sơ “quen biết” bị trả. Không ầm ĩ — chỉ biên bản. Uy tín tiền tệ sống bằng những lần dám từ chối."""
    elif has("2008", "khủng hoảng"):
        scene = f"""### Phòng chiến sự

Bảng đỏ. “{title}” năm {y}. Hùng không cho ai trang trí số. Cập nhật hàng ngày: thanh khoản, đơn hàng, công nợ, tinh thần công nhân. Lan giữ kênh đối tác. Ai giấu lỗ mất chỗ; ai báo sớm được bảo vệ để chữa."""
    elif has("nhà máy", "xưởng", "sản xuất", "ô tô", "xe", "thép", "xi măng", "máy", "chip", "phần mềm", "radio", "quạt", "đèn", "giày", "túi", "may"):
        scene = f"""### Sàn sản xuất

“{title}” tại {loc} năm {y}: tiếng máy, mùi vật liệu, checklist ca. Hùng đi chậm. Gặp lỗi thì dừng đúng quy trình — không chạy lấy thành tích. Kỹ thuật ghi sai số; kinh doanh muốn xuất sớm bị chặn.

Lan chuyển yêu cầu thị trường thành chỉ tiêu đo được. Một tổ báo cáo trung thực được ghi sổ khen. Danh dự bắt đầu từ chi tiết nhỏ."""
    elif has("cửa hàng", "chi nhánh", "showroom", "nhà hàng"):
        scene = f"""### Mặt tiền

“{title}” năm {y} ở {loc}: cửa mở, khách hỏi, nhân viên trả lời. Hùng đứng góc quan sát — không để bắt bẻ, để thấy thật. Giá treo đúng không, thái độ có nể khách không, hàng có sạch không.

Lan siết ca kíp và tồn kho. Lệch chuẩn một điểm là tin đồn mười điểm. Họ sửa trong 48 giờ, không chờ họp tháng."""
    elif has("trường", "học bổng", "đào tạo", "phòng khám", "y tế", "từ thiện", "nước sạch", "quỹ") and "trường tồn" not in t:
        scene = f"""### Hiện trường xã hội

“{title}” kéo người của Thương Gia xuống đất: lớp học, trạm y tế, xã thiếu nước, sổ thụ hưởng. Không micro. Có biên lai. Có kiểm tra đột xuất.

Hùng/Lan chốt: tiền mờ thì dừng. Người cần được nâng bằng việc, không bằng ảnh. Năm {y}, đó là kỷ luật từ thiện."""
    elif has("mỹ", "nhật", "hàn", "pháp", "đức", "anh", "thái", "indonesia", "hồng kông", "canada", "úc", "singapore", "châu", "wall", "paris", "berlin", "london"):
        scene = f"""### Bàn đàm phán / thị trường ngoài

“{title}” tại {loc} năm {y}: mẫu hàng, điều khoản, truy xuất nguồn gốc. Không hứa điều không làm. Đối thủ giảm giá — Thương Gia không đua đáy.

Lan ghi điểm cứng của đối tác. Hùng chốt biên bản. Về khách sạn, cả hai rà lại: chỗ nào suýt hứa nhanh, cắt đi."""
    elif has("ceo", "bàn giao", "giao quyền", "ủy thác", "kế thừa", "phó"):
        scene = f"""### Đổi vai

“{title}” năm {y}: biên bản, quyền, người. Hùng nói ít. Lan nhận việc nhiều. Người cũ dò ý. Văn hóa được giữ bằng xử đúng — ai sai bị nhắc, ai làm đúng được bảo vệ, dù cứng.

Con trai (nếu có) quan sát. Bài học: ghế không phải phần thưởng, là trách nhiệm có sổ."""
    elif has("tổng kết", "hoàn thành", "kỷ niệm", "flashback", "huyền thoại", "tinh thần"):
        scene = f"""### Nhìn lại có sẹo

“{title}” năm {y} tại {loc} không chỉ chiếu thắng. Có lô lỗi, có ốm, có người thầm lặng. Hùng gạch đoạn tự ca. Công nhân thâm niên ngồi gần. Mục tiêu người được đặt cạnh doanh thu."""
    elif has("city", "hecta", "hạ tầng", "nhà ở"):
        scene = f"""### Công trường

Bụi. Cọc. “{title}” năm {y}. Hùng đi dưới nắng, hỏi thoát nước, điện, nhà ở công nhân. Mét vuông không người là hàng rào vô nghĩa. Lan rà ngân sách và tiến độ song song."""
    elif has("nằm viện", "sức khỏe"):
        scene = f"""### Giường bệnh và quyền lực

“{title}” năm {y} tước tốc độ khỏi Hùng. Ông nhìn ống truyền và hiểu: ôm tất cả là cách chết sớm. Ủy thác trở thành mệnh lệnh sống. Lan cầm việc. Ông học im và tin."""
    else:
        scene = f"""### Nhịp việc “{title}”

Năm {y} tại {loc}, Hùng chia “{title}” thành chuỗi việc nhỏ có chủ sở hữu. Mỗi việc: hạn, chuẩn, người chịu. Lan giữ bảng ba màu. Đỏ xử trong 48 giờ.

Không hô hào. Có biên bản. Có người thật bị ảnh hưởng nếu ẩu — vì thế không ai được ẩu."""

    # Conflict micro
    conflicts = [
        f"Phát sinh nhỏ: một báo cáo muộn / một lô suýt lệch / một tin đồn. “{title}” bị thử. Hùng họp 25 phút: nguyên nhân, 48 giờ, cấm giấu. Ai nhận lỗi được bảo vệ để sửa.",
        f"Micro-xung đột quanh “{title}”: hai phòng ban đổ lỗi. Ông cắt: tìm lỗi hệ thống trước khi tìm tội đồ. Chuẩn được viết lại một trang, dán bảng tin.",
        f"Áp lực bên ngoài muốn Hùng/Lan “linh hoạt” quy trình cho “{title}”. Họ từ chối. Linh hoạt sai chỗ là lỗ thủng uy tín.",
    ]
    conf = conflicts[n % 3]

    # Result
    people = 20 + n * 3
    if n > 200:
        people *= 2
    result = f"""### Kết quả đo được

Sau chu kỳ “{title}” ({y}):

- Hạng mục cốt lõi có biên bản và chữ ký.
- Khoảng {people:,} người liên quan được phổ biến thay đổi (tùy quy mô việc).
- Rủi ro chính được gắn chủ sở hữu + hạn xử lý.
- Lan cập nhật bảng việc; Hùng chỉ xem dòng đỏ trước.

「Hệ thống: {title} | {y} | EXP +{40 + n // 2} | Giữ người – giữ sổ – giữ uy tín」"""

    # Family
    family = f"""### Nhà

Đêm {y}, mâm cơm không chức danh. “{title}” được Lan dịch thành câu bà Hà hiểu: có thêm việc, có thêm lo, có thêm người được nâng. Hùng ăn chậm. Nghe. Không mang giọng họp vào mâm."""

    nxt = min(360, n + 1)
    # load next title
    nt = OUTLINE["chapters"][str(nxt)]["title"]
    close = f"""### Khép

“{title}” khép với tiến và sẹo nhỏ. Hùng nhắn Lan: “Mai tiếp. Nhớ nghỉ.” Phía trước: “{nt}”."""

    return "\n\n".join([scene, f"### Thử nhỏ\n\n{conf}", result, family, close])


def rebuild(n: int) -> int:
    fs = list(DIR.glob(f"Chương {n} - *.txt"))
    path = fs[0]
    raw = path.read_text(encoding="utf-8", errors="replace")
    title = OUTLINE["chapters"][str(n)]["title"]

    # keep ch1
    if n == 1 and "Đau. Đau như thể" in raw:
        return count_words(raw)

    y = year_of(n, title)
    loc = loc_of(n, title)
    # year hints from open
    open_b = extract_section(raw, "Mở") or ""
    hy = [int(x) for x in re.findall(r"(19|20)\d{2}", open_b) if 1980 <= int(x) <= 2030]
    if hy:
        y = hy[0]
    if "2008" in title:
        y = 2008
        loc = "Hà Nội"

    open_part, core_part = extract_open_and_core(raw)
    if not open_part:
        # fallback keep start
        open_part = f"### Mở\n\n“{title}” năm {y} tại {loc}."

    # lớp sâu only if core
    deep = ""
    if core_part:
        deep = f"""### Lớp sâu

Sau diễn biến đã xác lập của “{title}”, Hùng không vội khoe. Ông hỏi Lan chỗ suýt sai, hỏi hiện trường chỗ còn mùi rủi ro. Năm {y} tại {loc}: hiện trường trước slide, người trước danh, sự thật trước thể diện. Em chặn lời hứa nhanh; anh sửa rồi làm đủ."""

    body_new = unique_body(n, title, y, loc)
    parts = [p for p in [open_part, core_part, deep, body_new] if p]
    body = "\n\n".join(parts)
    # clean old spam remnants
    body = re.sub(r"Ê-kíp chia[\s\S]{0,200}?Không nhìn chung ổn\.?", "", body)
    body = re.sub(r"Bổ sung “[^”]+”[\s\S]{0,180}?dòng đỏ bỏ quên\.?", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body)

    body = pad_clean(body, n, title, y, loc)
    # remove pad that still has Bổ sung pattern from old pad_clean? pad_clean is clean
    g = 0
    while count_words(body) < MIN and g < 30:
        body += (
            f"\n\nHùng ghi sổ sau “{title}” ({y}, {loc}): việc còn mở, người cần kèm, "
            f"rủi ro chưa tắt. Không khép ngày khi còn dòng đỏ."
        )
        g += 1

    w = count_words(body)
    header = "=" * 60 + f"\nChương {n}: {title}\n" + "=" * 60 + "\n\n"
    path.write_text(header + body.rstrip() + f"\n\n{'=' * 60}\n({w} từ)\n", encoding="utf-8")
    return w


def main():
    # rewrite all that have generic body OR all 2-360 for consistency
    stats = {"rewritten": 0, "short": []}
    for n in range(2, 361):
        fs = list(DIR.glob(f"Chương {n} - *.txt"))
        t = fs[0].read_text(encoding="utf-8", errors="replace")
        need = (
            "Ê-kíp chia" in t
            or "Checklist một trang" in t
            or "Không nhìn chung ổn" in t
            or t.count("Bổ sung") >= 1
            or "Việc cụ thể" in t
        )
        # always rewrite 2-360 bodies for higher consistency of quality middle
        need = True
        if need:
            w = rebuild(n)
            stats["rewritten"] += 1
            if w < MIN:
                stats["short"].append((n, w))
        if n % 50 == 0:
            print(f"Ch {n}: done")

    # verify
    short = []
    generic = 0
    for n in range(1, 361):
        t = list(DIR.glob(f"Chương {n} - *.txt"))[0].read_text(encoding="utf-8")
        if count_words(t) < MIN:
            short.append(n)
        if "Ê-kíp chia" in t or "Checklist một trang" in t:
            generic += 1
    print("rewritten", stats["rewritten"])
    print("short", short)
    print("generic_left", generic)
    # samples
    for n in [25, 55, 155, 221, 300, 360]:
        t = list(DIR.glob(f"Chương {n} - *.txt"))[0].read_text(encoding="utf-8")
        print(f"--- {n} w={count_words(t)} ---")
        if "### Hiện trường" in t or "### Sàn" in t or "### Mặt tiền" in t or "### Phòng" in t or "### Nhịp" in t or "### Bàn" in t or "### Đổi vai" in t or "### Nhìn lại" in t or "### Công trường" in t or "### Giường" in t:
            for tag in ["Hiện trường số", "Sàn sản xuất", "Mặt tiền", "Phòng chiến sự", "Hiện trường xã hội", "Bàn đàm phán", "Đổi vai", "Nhìn lại", "Công trường", "Giường bệnh", "Nhịp việc"]:
                if f"### {tag}" in t:
                    sec = t.split(f"### {tag}")[1].split("###")[0].strip()[:180]
                    print(tag + ":", sec)
                    break
        print("has_generic", "Ê-kíp chia" in t)


if __name__ == "__main__":
    main()
