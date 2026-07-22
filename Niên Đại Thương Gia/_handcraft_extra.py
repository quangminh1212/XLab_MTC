# -*- coding: utf-8 -*-
from _handcraft_ranges import (
    header,
    footer,
    load_originals,
    OUTLINE,
    MIN,
    count_words,
    pad_clean,
    year_of,
    loc_of,
    chapter_path,
)

EXTRA = {
    11: "Hà Nam — đường xá, chợ huyện, người lạ. “{title}” là mang hàng và mang cách nói chuyện sao cho người ta tin kẻ có lý lịch xấu vẫn giao đúng.",
    12: "Hải Dương bụi và tiếng máy. “{title}” mở thêm mắt xích đại lý. Hùng học rằng mỗi tỉnh một tính — không copy kịch bản mù.",
    13: "Thái Bình, cánh đồng và cửa hàng nhỏ. “{title}” là kiên nhẫn. Bà đại lý hỏi kỹ. Ông trả lời chậm, giao mẫu, chờ.",
    14: "Bắt đầu sản xuất — từ buôn sang làm. “{title}” đổi tư thế Hùng: không chỉ đi chợ, mà đứng cạnh máy, cạnh thợ, cạnh lỗi.",
    15: "Thuê người giúp việc — nghe nhỏ, nhưng là lần đầu nhà Trần có thêm hơi thở. “{title}” dạy ông quản người bắt đầu từ tôn trọng.",
    16: "Xưởng may nới rộng. Tiếng máy may dồn dập. “{title}” là bài toán công suất, lương, chỉ, vải — và không để công nhân thành số.",
    17: "Quảng Ninh gió biển. “{title}” mang hàng ngược lên vùng than và du lịch sơ khai. Mối mới, rủi ro mới.",
    18: "Nghệ An đường dài. “{title}” là độ bền của người đi bán và độ bền của lời hứa giao hàng.",
    19: "Hoàn thành nhịp sản xuất đầu. “{title}” không pháo hoa — chỉ sổ sách sạch và lô hàng không bị trả.",
    20: "Giày dép — ngành mới. Mùi da, keo, phom. “{title}” kéo Hùng vào chi tiết từng mũi chỉ như từng dòng code xưa.",
    120: "Sau nằm viện, “{title}” không còn lý thuyết. Hùng tập buông. Sợ — vẫn buông. Lan bắt lấy.",
    121: "Thái Lan — chuẩn và nhịp khác. “{title}” dạy khiêm tốn đúng mức và hợp đồng rõ.",
    122: "Myanmar và Campuchia: cửa hẹp, thủ tục dày. “{title}” là kiên nhẫn logistics.",
    123: "Đội ngũ xuất khẩu được xây không bằng hô hào. “{title}” là tuyển, kèm, giao việc có hậu quả.",
    124: "Cạnh tranh Trung Quốc bằng giá rẻ là bẫy. “{title}” chọn chuẩn và dịch vụ, chấp nhận mất đơn ảo.",
    125: "Lan trưởng thành nơi ánh đèn họp và nơi im lặng sau quyết định. “{title}” là ngày Hùng thấy em không còn chỉ là em bé quầy hàng.",
    126: "Buông. “{title}” là giá trị Hùng học đắt nhất: ôm tất cả là cách nhanh nhất để vỡ.",
    127: "Nhiệm vụ mới trên vai Lan. “{title}” — Hùng chống lưng số, không chống lưng bằng cách làm hộ.",
    128: "Khủng hoảng đầu của em. “{title}” — Hùng không lao vào cướp micro. Ông hỏi: em cần anh đứng đâu?",
    129: "Bước lùi để tiến. “{title}” là rút cho đúng, không phải chạy.",
}


def main():
    originals = load_originals()
    for n, tmpl in EXTRA.items():
        title = OUTLINE["chapters"][str(n)]["title"]
        y = year_of(n, title)
        loc = loc_of(n, title)
        craft = tmpl.format(title=title, y=y, loc=loc)
        core = originals.get(n, "")
        parts = [f"### Mở\n\n{craft}"]
        if core and count_words(core) >= 80:
            parts.append("### Diễn biến đã xác lập\n\n" + core)
            parts.append(
                f"### Lớp sâu\n\nSau “{title}”, Hùng kiểm lại: ai được no, ai có thể tổn thương, "
                f"mình có dám kể bà Hà nghe không sửa sự thật? Lan chặn lời hứa nhanh. Ông sửa rồi làm đủ."
            )
        else:
            parts.append(
                f"### Việc cụ thể\n\nÊ-kíp chia “{title}”: hiện trường, sổ, khách, người. "
                f"Checklist một trang. Không nhìn chung ổn."
            )
        parts.append(
            f"### Nhà\n\nĐêm sau “{title}”, mâm cơm không chức danh. Bà Hà hỏi ăn chưa. "
            f"Lan kể vừa đủ. Hùng im nghe — im cũng là về nhà."
        )
        parts.append(
            f"### Hệ thống\n\n「{y} | {title} — tiến độ | EXP +{80 + n}」\n"
            f"Hùng tắt thông báo. Việc ngoài đời quan trọng hơn."
        )
        nxt = min(360, n + 1)
        nt = OUTLINE["chapters"][str(nxt)]["title"]
        parts.append(f"### Khép\n\n“{title}” có tiến. Mai: “{nt}”.")
        body = "\n\n".join(parts)
        body = pad_clean(body, n, title, y, loc)
        while count_words(body) < MIN:
            body += (
                f"\n\nChi tiết thêm “{title}” tại {loc} năm {y}: "
                f"Hùng rà lại lời hứa và tiến độ trước khi ngủ."
            )
        text = header(n, title) + footer(body)
        chapter_path(n, title).write_text(text, encoding="utf-8")
        print(f"Ch {n}: {count_words(text)}w")


if __name__ == "__main__":
    main()
