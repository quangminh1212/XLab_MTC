# -*- coding: utf-8 -*-
"""Force-regenerate chapters 155-360 with unique openings and plot scenes."""
from __future__ import annotations

import re
from pathlib import Path

import _gen_novel as g

DIR = Path(__file__).resolve().parent


def location_for_fixed(n: int, title: str) -> str:
    t = " " + title.lower() + " "
    rules = [
        (r"hà nội|ha noi", "Hà Nội"),
        (r"sài gòn|hồ chí minh|tp\.?hcm", "Thành phố Hồ Chí Minh"),
        (r"hải phòng", "Hải Phòng"),
        (r"thái lan|bangkok", "Bangkok"),
        (r"indonesia|jakarta", "Jakarta"),
        (r"nhật", "Tokyo"),
        (r"hàn quốc|seoul", "Seoul"),
        (r"\bmỹ\b|usa|wall street|new york|california|manhattan|silicon", "Hoa Kỳ"),
        (r"\bpháp\b|paris|lyon", "Pháp"),
        (r"\bđức\b|berlin|münchen|munich", "Đức"),
        (r"\banh\b|london", "Anh"),
        (r"canada|toronto", "Canada"),
        (r"\búc\b|australia|sydney", "Úc"),
        (r"nigeria|lagos", "Nigeria"),
        (r"trung quốc|quảng châu", "Trung Quốc"),
        (r"hồng kông", "Hồng Kông"),
        (r"singapore", "Singapore"),
        (r"brazil|chile|nam mỹ", "Nam Mỹ"),
        (r"châu phi", "Châu Phi"),
        (r"quê|thanh xuân|quốc oai", "Làng Thanh Xuân, Quốc Oai"),
        (r"ngân hàng|cho vay|cổ đông|ipo|niêm yết", "Hà Nội"),
        (r"nhà máy|xưởng|sản xuất|ô tô|xe điện|chip", "Khu công nghiệp"),
        (r"từ thiện|học bổng|trường|bệnh viện|y tế|nước sạch|quỹ", "Hà Nội và vùng sâu"),
        (r"khủng hoảng|2008|dòng tiền|nợ", "Hà Nội – trung tâm tài chính"),
        (r"forbes|truyền hình quốc tế", "Hà Nội / quốc tế"),
        (r"city|hecta|khu công nghiệp", "Thương Gia City"),
    ]
    for pat, loc in rules:
        if re.search(pat, t, re.I):
            return loc
    cycle = ["Hà Nội", "Hà Đông", "Hải Phòng", "TP.HCM", "Đà Nẵng", "Singapore"]
    return cycle[n % len(cycle)]


OPENERS = [
    lambda m: (
        f"Năm {m['year']}, tại {m['location']}, hồ sơ mang tên “{m['title']}” được đặt lên bàn "
        f"Trần Văn Hùng trước khi trời sáng hẳn. Ông không vội gọi cấp dưới. Ông pha trà, nhìn hơi nước, "
        f"và tự hỏi: quyết định hôm nay sẽ nuôi bao nhiêu gia đình, và có thể làm tổn thương ai nếu mình vội.\n\n"
        f"Lan đã gửi tin từ đêm qua. Bà Hà dặn mang áo ấm. Hệ thống lặng lẽ hiện một dòng nhắc việc. "
        f"Hùng hít sâu, mở bút, viết chữ đầu tiên trong sổ tay da: “Làm đúng – làm đủ – làm bền.”"
    ),
    lambda m: (
        f"Tiếng chuông cửa công ty vang lên sớm hơn thường lệ. “{m['title']}” không còn là ý tưởng trên giấy — "
        f"nó đã thành lịch họp, thành ngân sách, thành áp lực trên vai hàng trăm người. Trần Văn Hùng bước vào "
        f"phòng họp tại {m['location']} năm {m['year']} với khuôn mặt điềm tĩnh của người đã đi qua quá nhiều “lần đầu”.\n\n"
        f"“Bắt đầu,” ông nói. “Ai phản biện được thì phản biện ngay từ phút này.”"
    ),
    lambda m: (
        f"Chương “{m['title']}” bắt đầu bằng một cuộc gọi lúc 5:40 sáng. Đầu dây bên kia là tin không thể trì hoãn. "
        f"Hùng ngồi dậy tại {m['location']}, năm {m['year']}, và biết hôm nay ông phải chọn giữa tốc độ và an toàn — "
        f"rồi cố lấy cả hai bằng kỷ luật.\n\n"
        f"Ông rửa mặt bằng nước lạnh, nhớ lời bà Hà: “Cậu làm lớn, nhưng đừng làm ẩu.”"
    ),
    lambda m: (
        f"Bản đồ trên tường đầy đinh ghim. Mỗi đinh là một lời hứa. “{m['title']}” là đinh mới nhất — màu đỏ, "
        f"ghim thẳng vào {m['location']}, mốc năm {m['year']}. Trần Văn Hùng đứng nhìn lâu đến mức Lan phải ho nhẹ:\n\n"
        f"“Anh ơi, nhìn nữa thì đinh cũng không tự mọc thành nhà máy.”\n\n"
        f"Hùng cười. “Anh đang tính đường rút nếu gió đổi. Rồi mình tiến.”"
    ),
    lambda m: (
        f"Mưa đầu mùa phủ {m['location']}. Trong cabin xe, Hùng đọc lại tóm tắt một trang về “{m['title']}”. "
        f"Năm {m['year']} — thời điểm đủ chín để làm lớn, cũng đủ nguy hiểm để sai một ly đi một dặm. "
        f"Ông gập giấy, bảo tài xế: “Đi chậm vào cổng. Hôm nay mình cần thấy mặt người thật, không chỉ thấy báo cáo.”"
    ),
    lambda m: (
        f"Có người đo thành công bằng doanh thu. Trần Văn Hùng đo “{m['title']}” bằng việc sau chín mươi ngày, "
        f"công nhân còn muốn gắn bó và khách hàng còn muốn đặt hàng. Năm {m['year']} ở {m['location']}, "
        f"ông họp ban lõi chỉ mười lăm phút để chốt nguyên tắc, rồi cả ngày còn lại dành cho hiện trường."
    ),
]


def para_open_v2(meta: dict) -> str:
    return OPENERS[meta["num"] % len(OPENERS)](meta)


def plot_scene(meta: dict) -> str:
    title = meta["title"]
    y = meta["year"]
    loc = meta["location"]
    tl = title.lower()
    n = meta["num"]

    if any(k in tl for k in ["ngân hàng", "cho vay", "tín dụng"]):
        return (
            f"Phòng giao dịch còn thơm mùi sơn mới. Hùng đi từng quầy, hỏi nhân viên trẻ có thuộc quy trình thẩm định không, "
            f"có biết từ chối khoản vay “quen biết” như thế nào không. Ông dựng kịch bản: nông dân cần vốn mùa vụ, "
            f"chủ xưởng cần đảo nợ, doanh nghiệp sân sau muốn hạn mức đặc biệt.\n\n"
            f"“Chúng ta cho vay để nuôi việc làm, không cho vay để nuôi quan hệ,” Hùng nói. "
            f"“Ai vượt quyền phê duyệt vì nể thì lập biên bản ngay.”\n\n"
            f"Lan thiết kế gói siêu nhỏ – nhỏ – vừa, mỗi gói một trần rủi ro. Kiểm toán nội bộ có quyền đỏ dừng giải ngân. "
            f"Năm {y} tại {loc}, “{title}” là canh bạc uy tín: một khoản xấu có thể xóa sạch lời nói đẹp cả năm."
        )

    if any(k in tl for k in ["ô tô", "xe máy", "xe điện", "showroom", "trạm sạc"]):
        return (
            f"Dây chuyền kêu đều như nhịp tim công nghiệp. Hùng đội mũ bảo hộ, đi dọc lan can: hàn, sơn, phanh, chạy thử. "
            f"Kỹ sư Minh chỉ sai số 0,3mm. “Vậy 0,3mm là ranh giới danh dự. Không xuất xưởng,” Hùng đáp.\n\n"
            f"Lan lo dịch vụ sau bán: phụ tùng, bảo hành, đào tạo kỹ thuật viên tỉnh lẻ. "
            f"“{title}” không chỉ bán cỗ máy — bán sự yên tâm mỗi lần gia đình nổ máy đi làm. Địa điểm {loc}, năm {y}."
        )

    if any(k in tl for k in ["khủng hoảng", "2008", "dòng tiền", "nợ", "thanh khoản", "cứu"]):
        return (
            f"Bảng dòng tiền tuần in khổ A3 dán tường. Màu đỏ lan như vết mực. Năm {y}, tin xấu ập tới nhanh hơn báo cáo. "
            f"Hùng họp không nghỉ: “Không ai giấu lỗ hổng thanh khoản. Ai giấu, sa thải. Ai báo sớm, bảo vệ.”\n\n"
            f"Họ cắt chi không thiết yếu, giữ quỹ lương cốt lõi, đàm phán giãn nợ có điều kiện. "
            f"Lan gọi đối tác quốc tế giữa đêm. “{title}” trở thành bài kiểm tra tư cách hơn bài kiểm tra tài chính tại {loc}."
        )

    # avoid false positive: "trường tồn" / "trưởng thành"
    tl_safe = tl.replace("trường tồn", "").replace("trưởng thành", "")
    if any(k in tl_safe for k in ["từ thiện", "học bổng", "trường học", "100 trường", "bệnh viện", "y tế", "nước sạch", "quỹ từ", "quỹ di sản", "quỹ học"]):
        return (
            f"Trên bản đồ từ thiện, mỗi chấm xanh là một xã, một trường, một trạm y tế. Hùng yêu cầu mỗi đồng chi có biên lai, "
            f"có người thụ hưởng xác nhận, có kiểm tra đột xuất. “Làm từ thiện mập mờ thì xấu hơn không làm.”\n\n"
            f"Lan công bố quý. Kiểm toán bên thứ ba vào từ ngày đầu. Một hiệu trưởng già nắm tay Hùng: "
            f"“Cháu tôi được học tiếp vì học bổng.” “{title}” được vận hành như dự án, không như chiến dịch PR. {loc}, {y}."
        )

    if any(k in tl for k in ["ceo", "bàn giao", "giao quyền", "phó tổng", "chủ tịch hội đồng"]):
        return (
            f"Lễ bàn giao không phô trương. Một phòng họp, một biên bản, một vòng tay. Hùng nhìn Lan — người từng học bán hàng "
            f"sau quầy Quốc Oai — và thấy một người đủ tầm dẫn dắt.\n\n"
            f"“Em không cần thành bản sao của anh. Em cần thành phiên bản tốt hơn của Thương Gia.” "
            f"Năm {y}, quyền vận hành đổi vai, văn hóa không được đứt. Hùng lui về chiến lược: đủ gần để đỡ, đủ xa để em bay. "
            f"Địa điểm {loc}. Tiêu đề ngày ấy: “{title}”."
        )

    if any(k in tl for k in ["bóng tối", "cổ đông", "thôn tính", "đại hội", "phòng thủ"]):
        return (
            f"Phòng họp cổ đông nóng như lò. Có người gom cổ phiếu, có tin đồn, có đề xuất “tái cấu trúc” nghe như tháo dỡ. "
            f"Hùng đặt lên bàn ba thứ: báo cáo minh bạch, lộ trình lợi ích dài hạn cho cổ đông nhỏ, bằng chứng ý đồ thôn tính.\n\n"
            f"“Thương Gia không bán mình cho kẻ chỉ biết xẻ thịt. Ai muốn cùng xây thì cửa mở.” "
            f"Lan điều phối liên minh cổ đông nhỏ. “{title}” là trận đánh bằng trí tuệ và niềm tin tại {loc}, năm {y}."
        )

    if any(k in tl for k in ["kỷ niệm", "hoàn thành phần", "tổng kết", "flashback", "tinh thần", "huyền thoại", "phát biểu"]):
        return (
            f"Không khí tổng kết khác ngày thường. Có phim ngắn, số liệu, và những khuôn mặt già hơn trong ảnh. "
            f"Hùng mời công nhân thâm niên và đối tác cũ. “Chúng ta nhớ mình từ đâu tới. “{title}” không phải điểm dừng để kiêu, "
            f"mà là điểm kiểm tra để đi tiếp cho đúng.”\n\n"
            f"Năm {y} tại {loc}, con số lớn được đặt cạnh bát cháo năm xưa, cửa hàng đầu, ca bệnh viện, chữ ký quốc tế đầu. "
            f"Người nghe im lặng — im lặng của sự thấu."
        )

    if any(k in tl for k in ["nhật", "sato", "tanaka", "hàn quốc", "đức", "pháp", "anh", "mỹ", "canada", "úc", "indonesia", "thái"]):
        return (
            f"Chuyến công tác “{title}” tại {loc} năm {y} không phải du lịch doanh nhân. Hùng và đoàn mang theo mẫu hàng, "
            f"hồ sơ chất lượng, và sự khiêm tốn đúng mức. Đối tác hỏi những câu khó: truy xuất nguồn gốc, bảo hành xuyên biên giới, "
            f"xử lý khủng hoảng truyền thông.\n\n"
            f"Lan đàm phán bằng dữ liệu. Hùng chốt bằng uy tín. “Chúng tôi không hứa điều không làm được. Điều làm được, chúng tôi viết vào hợp đồng.” "
            f"Đó là câu cửa miệng giúp Thương Gia mở cửa những thị trường khó tính."
        )

    if any(k in tl for k in ["chip", "phần mềm", "ai", "dữ liệu", "công nghệ", "r&d", "điện thoại", "máy tính"]):
        return (
            f"Phòng lab sáng trắng. Màn hình đầy log. “{title}” đòi hỏi Hùng học lại tư duy kỹ sư — thứ từng thuộc về Lý Minh. "
            f"Ông không giả vờ hiểu mọi thuật ngữ; ông hỏi đúng câu: sản phẩm này giải quyết nỗi đau nào, chi phí bao nhiêu, "
            f"và nếu hỏng thì khách bị gì.\n\n"
            f"Đội R&D được quỹ riêng, deadline rõ, quyền thất bại có kiểm soát. Năm {y} ở {loc}, "
            f"công nghệ không còn là món trang trí — nó là xương sống cạnh tranh."
        )

    # default unique-ish by chapter number facts
    a = 10 + (n % 17)
    b = 3 + (n % 9)
    return (
        f"Hiện trường “{title}” tại {loc} năm {y} được chia ba vòng: kỹ thuật, thị trường, con người. "
        f"Hùng không cho vòng nào tự chạy riêng. Đội đưa phương án A an toàn, B táo bạo, C lai. "
        f"Ông chọn lai có điều kiện: làm B theo nhịp A, gắn còi báo của C.\n\n"
        f"Trong {a} ngày đầu, {b} điểm nghẽn bị bóc tách: quy trình, người, máy, hợp đồng, thông tin. "
        f"Lan chịu nhịp. Minh chịu chất lượng. Tài chính chịu trần rủi ro. Ai vượt trần phải dừng và họp lại trong 24 giờ. "
        f"Micro-conflict “{meta['conflict']}” được ghi nhận công khai, không để thành tin đồn."
    )


def compose_v2(meta: dict, base_text: str | None = None) -> str:
    n = meta["num"]
    title = meta["title"]
    meta = dict(meta)
    meta["location"] = location_for_fixed(n, title)
    header = "=" * 60 + f"\nChương {n}: {title}\n" + "=" * 60 + "\n\n"

    original_core = ""
    if base_text:
        body = re.sub(r"^={5,}.*?={5,}\s*", "", base_text, count=1, flags=re.S)
        body = re.sub(r"\n={5,}.*", "", body, flags=re.S)
        body = re.sub(r"\(\d+\s*từ\)\s*$", "", body, flags=re.I | re.M).strip()
        if "### Phần lõi" in body:
            m = re.search(
                r"### Phần lõi đã xác lập.*?\n\n(.*?)(?:\n\n### Phần mở rộng|\Z)",
                body,
                re.S,
            )
            if m:
                body = m.group(1).strip()
        # only keep original if it looks like original story not prior template
        if body and "chưa kịp sáng hẳn" not in body[:120] and "Làm đúng – làm đủ – làm bền" not in body[:200]:
            original_core = (
                "### Phần lõi đã xác lập (giữ nguyên sự kiện)\n\n"
                + body
                + "\n\n### Phần mở rộng chi tiết\n\n"
            )

    parts = [
        original_core,
        para_open_v2(meta),
        plot_scene(meta),
        g.para_action(meta),
        g.para_dialogue(meta),
        g.para_result(meta),
        g.para_family(meta),
        g.para_conflict_scene(meta),
        g.para_emotion_system(meta),
        g.para_close(meta),
    ]
    text = header + "\n\n".join(p for p in parts if p)
    w = g.count_words(text)
    if w < g.MIN_WORDS:
        text += "\n\n" + g.extra_fill_paragraphs(meta, g.MIN_WORDS - w + 80)
    guard = 0
    while g.count_words(text) < g.MIN_WORDS and guard < 12:
        text += "\n\n" + g.extra_fill_paragraphs(meta, 450)
        guard += 1
    final = g.count_words(text)
    return text.rstrip() + f"\n\n{'=' * 60}\n({final} từ)\n"


def main():
    outline = g.load_outline()
    # update locations in outline
    for n in range(1, 361):
        ch = outline["chapters"][str(n)]
        ch["location"] = location_for_fixed(n, ch["title"])
    g.OUTLINE_PATH.write_text(
        __import__("json").dumps(outline, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    for n in range(155, 361):
        meta = outline["chapters"][str(n)]
        path = g.chapter_path(n, meta["title"])
        text = compose_v2(meta, base_text=None)
        path.write_text(text, encoding="utf-8")
        if n % 20 == 0 or n in (155, 156, 200, 221, 270, 301, 330, 356, 360):
            print(f"Ch {n}: {g.count_words(text)}w | {meta['location']} | {path.name}")

    # Also re-expand 2-154 to strip stacked template if any, keeping core
    for n in range(2, 155):
        meta = outline["chapters"][str(n)]
        path = g.chapter_path(n, meta["title"])
        if not path.exists():
            continue
        old = path.read_text(encoding="utf-8", errors="replace")
        # Only recompose if starts with formulaic expansion markers repeated
        if old.count("### Phần lõi") > 1 or old.count("chưa kịp sáng hẳn") > 0:
            text = compose_v2(meta, base_text=old)
            path.write_text(text, encoding="utf-8")

    v = g.verify()
    print("VERIFY good", v["good"], "missing", len(v["missing"]), "short", len(v["bad"]))
    if v["bad"]:
        print("SHORT samples", v["bad"][:10])
    if v["missing"]:
        print("MISSING", v["missing"][:20])


if __name__ == "__main__":
    main()
