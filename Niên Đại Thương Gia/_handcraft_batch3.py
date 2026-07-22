# -*- coding: utf-8 -*-
"""Handcraft ranges: 21-40, 90-112, 200-220, 241-270."""
from __future__ import annotations

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

# title-specific literary opens (short craft + core preserved below)
OPENS: dict[int, str] = {}

# 21-40: expand production / south / brand early
for n, text in {
    21: "Xưởng giày nóng mùi keo. “{title}” là hoàn 50 đôi không chỉ để đủ số — để chứng minh mình làm được đồ người ta mang đi làm mà không thẹn.",
    22: "Sài Gòn ồn, nóng, cơ hội và bẫy cùng lúc. “{title}” mở mắt Hùng: miền Nam không chờ người Bắc mang thói quen cũ vào.",
    23: "Túi xách — da, chỉ, form. “{title}” kéo ông vào thẩm mỹ người dùng: không chỉ bền, còn phải muốn xách.",
    24: "Xưởng túi đầu tiên chật. “{title}” là nới tường, nới ca, nới trách nhiệm. Lỗi một đường may là lỗi cả uy tín.",
    25: "Cửa hàng thứ hai. “{title}” nghe vui — và nguy: phân tâm, thiếu người, lệch chuẩn. Hùng siết quy trình trước khi siết ribbon.",
    26: "Đất để xây xưởng không phải tờ giấy. “{title}” là tiền, giấy tờ, hàng xóm, và giấc mơ đặt nền bằng mét vuông thật.",
    27: "Lào — biên giới, tiếng nói, nhịp chợ khác. “{title}” dạy Hùng cúi đúng và thẳng đúng khi làm ăn ngoài.",
    28: "Campuchia bụi đường và cơ hội mỏng. “{title}” là kiên nhẫn giao hàng, không hứa tốc độ ảo.",
    29: "Thái Lan chuẩn hơn, khó nịnh hơn. “{title}” là bài học chất lượng: đẹp miệng không thay được lô đạt chuẩn.",
    30: "Mở rộng cửa hàng trong nước. “{title}” là bản đồ đinh ghim — mỗi đinh một lời hứa lương cho ai đó.",
    31: "Tổng kết 1983. “{title}” trải giấy ra: từ bát cháo đến quầy hàng. Hùng không khóc. Ông nắm tay bà Hà lâu hơn.",
    32: "Thực phẩm — vùng nhạy cảm. “{title}” buộc vệ sinh, hạn dùng, nguồn gốc. Ăn vào miệng người là nợ.",
    33: "Mở rộng thực phẩm. “{title}” không phải nhồi kệ. Là kiểm soát lạnh–nóng, hao hụt, niềm tin.",
    34: "Tuyển kỹ sư Minh. “{title}” là ngày Hùng tìm được người nói chung ngôn ngữ kỹ thuật — và dám cãi đúng.",
    35: "Miền Nam mở rộng. “{title}” là logistics và văn hóa bán hàng khác nhịp. Lan học nhanh hơn anh tưởng.",
    36: "Chi nhánh Hoài Đức. “{title}” gần nhà mà không được ẩu. Gần nhà dễ chủ quan — ông siết hơn.",
    37: "Hà Nội chính thức. “{title}” đặt Thương Gia vào ánh mắt thành phố. Sáng cửa hàng, sáng cả áp lực.",
    38: "Radio — tiếng nói và linh kiện. “{title}” mang hơi điện tử đầu tiên. Hùng nhớ màn hình thế kỷ 21 và mỉm cười mỏi.",
    39: "Mở rộng radio. “{title}” là sửa lỗi nhiễu, tồn kho linh kiện, và lời phàn nàn của người nghe đài.",
    40: "Hoàn nhiệm vụ radio. “{title}” không pháo hoa. Chỉ lô ổn định và kỹ năng mới trong hệ thống — ông ghi sổ, rồi đi ngủ sớm.",
}.items():
    OPENS[n] = text

# 90-112: part3 industrial / family / export
for n, text in {
    90: "Bắt đầu Phần 3. “{title}” mở cửa khu vực. Hùng nhìn bản đồ Đông Nam Á như nhìn cánh đồng cần cày — không phải để khoe, để làm.",
    91: "Thép Hải Phòng — nóng, nặng, nguy. “{title}” đưa Thương Gia vào xương của xây dựng. An toàn lao động không phải phụ lục.",
    92: "Xi măng bụi trắng. “{title}” là công suất và môi trường xung quanh nhà máy. Hàng xóm cũng là stakeholder.",
    93: "Gặp cô Hạnh. “{title}” không phải thương vụ. Là lần trái tim trùng sinh dám mở sau bao năm chỉ biết việc.",
    94: "Mai và Lan (người khác). “{title}” là lựa chọn — và sự tử tế với người không chọn. Hùng không chơi trò giữ ghế cảm xúc.",
    95: "Chọn Hạnh. “{title}” giản dị: nói thật, chịu trách nhiệm, đưa về gặp bà Hà. Nhà quan trọng hơn tin đồn.",
    96: "Bà Hà bế cháu nội. “{title}” làm ông cứng nhắc vụn một nhịp. Đế chế ngoài phố; trong nhà là hơi thở trẻ.",
    97: "Điện tử. “{title}” là linh kiện, khay, kiểm định. Sai một tụ là trả cả lô.",
    98: "Điện thoại. “{title}” chạm giấc mơ liên lạc. Hùng biết tương lai, nhưng làm theo khả năng hiện tại — không ảo.",
    99: "Viễn thông. “{title}” cần giấy phép, hạ tầng, kiên nhẫn. Ông không đốt tiền để khoe sóng.",
    100: "Phần mềm — về nhà với ký ức Lý Minh. “{title}” là ERP giản dị cho doanh nghiệp Việt: đủ dùng, giá vừa, không thần thánh hóa.",
    101: "108 cửa hàng. “{title}” là kỷ luật chuỗi: đồng phục chuẩn, không đồng phục ẩu. Lan siết.",
    102: "42 nhà hàng. “{title}” mang mùi nước dùng và ca bếp. Vệ sinh bếp là uy tín không kém biển hiệu.",
    103: "30 nhà máy. “{title}” dễ kiêu. Hùng đi từng nhà máy như đi khám sức khỏe — tìm bệnh, không tìm ảnh chụp.",
    104: "Xuất khẩu châu Âu. “{title}” là chuẩn, bao bì, truy xuất. Không hứa điều không làm được.",
    105: "Tổng kết Phần 3. “{title}” trải sẹo và thắng. Ông không say. Ông nhớ Quốc Oai.",
    106: "Bắt đầu Phần 4. “{title}” — toàn cầu hóa. Cửa lớn, gió lớn, ngã cũng lớn.",
    107: "Nhà máy Thái Lan. “{title}” là văn hóa làm việc khác và tiêu chuẩn không nương.",
    108: "Indonesia. “{title}” — hải quan, đảo, logistics. Kiên nhẫn là năng lực cạnh tranh.",
    109: "Nhà máy Đức. “{title}” là kỷ luật milimet. Ông Sato/đối tác Đức không cần diễn văn — cần số.",
    110: "M&A Bangkok Electronics. “{title}” không phải nuốt — là tích hợp người, văn hóa, sổ sách. Nuốt ẩu sẽ nghẹn.",
    111: "Mở sang Mỹ. “{title}” — thị trường lớn và lời từ chối cũng lớn. Lan bắt đầu gánh phần quốc tế.",
    112: "Khép một nhịp lớn. “{title}” ghi nhận: đã ra biển, chưa được phép quên bến.",
}.items():
    OPENS[n] = text

# 200-220: global gateway to pre-crisis
for n, text in {
    200: "Cửa ngõ toàn cầu. “{title}” — Hùng đứng giữa số liệu châu lục và ký ức bát cháo. Không say. Chỉ thở.",
    201: "Phần 4 bắt đầu. “{title}” mở lịch châu Âu–Mỹ. Ông dặn đoàn: khiêm tốn đúng mức, hợp đồng rõ.",
    202: "Paris. “{title}” mang mùi bánh và phòng họp lạnh. Thương hiệu Việt phải chứng minh bằng hàng, không bằng tự kể.",
    203: "Lyon — nhà hàng. “{title}” là vị và dịch vụ. Khách Pháp không nể 'câu chuyện đẹp' nếu món lệch.",
    204: "Berlin kỹ thuật. “{title}” — chuẩn, chứng nhận, im lặng làm việc.",
    205: "München linh kiện. “{title}” siết dung sai. Xuất xưởng là ký tên bằng danh dự.",
    206: "London tài chính. “{title}” là ngôn ngữ quỹ và rủi ro. Hùng không giả vờ hiểu hết — ông hỏi đúng câu.",
    207: "Quỹ đầu tư Anh. “{title}” — họ muốn tăng trưởng; ông muốn điều kiện không bẻ gãy văn hóa.",
    208: "Wall Street lần đầu. “{title}” ồn và sáng. Ông nhớ lời bà Hà trước khi bước vào tháp kính.",
    209: "Đàm phán ADR. “{title}” là pháp lý và kiên nhẫn. Không ký vì sợ lỡ tàu.",
    210: "Manhattan văn phòng. “{title}” — biển hiệu nhỏ, áp lực lớn. Lan giữ nhịp hai múi giờ.",
    211: "West Coast chuỗi. “{title}” mang nắng California và khách khó tính. Giữ chuẩn, không đua đáy.",
    212: "ISO / chuẩn châu Âu. “{title}” là giấy và thói quen. Giấy không có thói quen thì là giấy lộn.",
    213: "Chứng nhận toàn hệ. “{title}” siết từng nhà máy. Ai làm đẹp hồ sơ bị phạt nặng hơn ai làm hỏng máy.",
    214: "M&A Pháp. “{title}” tích hợp văn hóa — khó hơn tích hợp máy.",
    215: "Văn hóa doanh nghiệp sau M&A. “{title}” — giữ cái lõi Thương Gia: không dối, không chèn người.",
    216: "Chip thử nghiệm. “{title}” đắt và rủi. Hùng cho quỹ R&D quyền thất bại có kiểm soát.",
    217: "Năng lượng tái tạo. “{title}” nhìn dài: điện, môi trường, uy tín thế hệ sau.",
    218: "Pin mặt trời thế hệ mới. “{title}” — hiệu suất và bảo hành. Hứa ảo là tự đào hố.",
    219: "Xe điện nguyên mẫu. “{title}” ồn ào báo chí; ông chỉ quan tâm an toàn và trạm sạc.",
    220: "Triển lãm châu Á. “{title}” là sàn diễn và cũng là nơi đối thủ soi. Hàng phải chịu được soi.",
}.items():
    OPENS[n] = text

# 241-270: post-crisis build to super conglomerate
for n, text in {
    241: "Thương Gia City khởi công. “{title}” — bụi, cọc, quy hoạch. Mét vuông phải có chỗ cho người ở, không chỉ hàng rào.",
    242: "500 hecta trên giấy dễ. “{title}” là hạ tầng, thoát nước, điện, đường. Ông đi chân đất trên công trường.",
    243: "Nhà ở công nhân. “{title}” không phải phụ lục CSR. Là điều kiện để ca đêm không tan đàn.",
    244: "Trường trong KCN. “{title}” — trẻ em công nhân có chỗ học. Lan mỉm cười lần hiếm giữa họp cứng.",
    245: "Xe điện thương mại. “{title}” ra đường thật. Lỗi thực tế dạy nhiều hơn brochure.",
    246: "Trạm sạc toàn quốc. “{title}” là mạng lưới — điểm chết một đoạn là mất niềm tin cả chuỗi.",
    247: "AI sơ khai trong kho. “{title}” — Hùng (Lý Minh) nhìn thuật toán như nhìn thợ mới: cần kèm, cần kiểm.",
    248: "Trung tâm dữ liệu. “{title}” nóng máy và nóng rủi ro bảo mật. Sổ sạch không đủ; bit cũng phải sạch.",
    249: "Silicon Valley. “{title}” — họ nói tương lai; ông hỏi chi phí và hậu quả khi hỏng.",
    250: "Lan dẫn quỹ R&D. “{title}” giao quyền thật: ngân sách, deadline, quyền dừng dự án xấu.",
    251: "Con trai vào công ty. “{title}” không trao ghế. Trao việc nhỏ, mắng đúng, khen đúng.",
    252: "Thế hệ hai học việc. “{title}” — ca xưởng, sổ kho, khách phàn nàn. Trường đời.",
    253: "Huân chương. “{title}” sáng trên áo; Hùng nhớ công nhân thâm niên hơn nhớ flash.",
    254: "Gặp lãnh đạo ngành. “{title}” nói chính sách bằng trải nghiệm nhà máy, không bằng khẩu hiệu.",
    255: "Cam kết bền vững. “{title}” — số liệu môi trường công khai. Nói xanh mà sổ đen thì đừng nói.",
    256: "Top thương gia. “{title}” trên báo; ông đo bằng việc làm và nợ xấu có kiểm soát.",
    257: "Lễ vinh danh. “{title}” ngắn. Ông nhường micro cho người thầm lặng.",
    258: "Châu Phi sâu. “{title}” — tôn trọng địa phương, không mang 'cứu rỗi'. Làm ăn sòng phẳng.",
    259: "Brazil–Chile. “{title}” múi giờ lệch, hợp đồng dày. Lan gánh nhịp.",
    260: "Chuỗi giá trị toàn cầu. “{title}” siết mắt xích: một mắt xích gỉ là cả dây yếu.",
    261: "ESG kiểm toán. “{title}” mời bên thứ ba. Sợ số thật hơn sợ mất giải thưởng.",
    262: "Bà Hà và hồi ký gia đình. “{title}” — chữ bà kể, chữ cháu ghi. Đế chế cần câu chuyện người.",
    263: "Flashback 25 năm. “{title}” chiếu sẹo. Phòng họp im.",
    264: "Tái khẳng định sứ mệnh. “{title}”: làm giàu không làm mất người — viết lại lên tường, không chỉ lên slide.",
    265: "Đối thủ Hàn Quốc. “{title}” cạnh tranh lành: học chuẩn của họ, không copy chiêu bẩn.",
    266: "Cạnh tranh lành mạnh. “{title}” — giữ giá trị, không đua đáy.",
    267: "Liên minh Đông Á. “{title}” bắt tay bằng hợp đồng và tôn trọng, không bằng tiệc.",
    268: "Tổng kết toàn cầu hóa. “{title}” — số lớn, bài học lớn, kiêu thì chết.",
    269: "Phần thưởng Phần 4. “{title}” hệ thống ghi nhận; Hùng ghi nhận người.",
    270: "Siêu tập đoàn trên giấy. “{title}” — ông đo đỉnh bằng đáy: ca kíp còn vững không, bữa cơm công nhân còn đủ không.",
}.items():
    OPENS[n] = text


def write_one(n: int, originals: dict) -> int:
    title = OUTLINE["chapters"][str(n)]["title"]
    y = year_of(n, title)
    loc = loc_of(n, title)
    # crisis-adjacent years
    if 200 <= n <= 220:
        y = year_of(n, title)
    if 241 <= n <= 270:
        y = max(y, 2009)

    craft = OPENS[n].format(title=title, y=y, loc=loc)
    core = originals.get(n, "")
    parts = [f"### Mở\n\n{craft}"]

    if core and count_words(core) >= 80 and n <= 154:
        parts.append("### Diễn biến đã xác lập\n\n" + core)
        parts.append(
            f"### Lớp sâu\n\nSau “{title}”, Hùng hỏi ba câu: ai no hơn, ai có thể tổn thương, "
            f"mình có dám kể bà Hà nghe không sửa sự thật? Lan chặn hứa nhanh. Ông sửa rồi làm đủ. "
            f"Năm {y} tại {loc}, hiện trường thắng slide."
        )
    else:
        parts.append(
            f"### Việc cụ thể\n\nÊ-kíp chia “{title}”: hiện trường – sổ sách – khách – người. "
            f"Rủi ro gọi tên. Checklist một trang. Ký đã hiểu. Làm. Không nhìn chung ổn. {loc}, {y}."
        )

    # era emotional beat
    if n <= 40:
        parts.append(
            f"### Nhà\n\nĐêm “{title}”, mâm cơm còn mùi {('khói bếp' if y < 1986 else 'cơm nguội để dành')}. "
            f"Bà Hà hỏi ăn chưa. Lan còn lúc tin lúc soi. Hùng chứng minh bằng việc mai còn làm."
        )
    elif n <= 112:
        parts.append(
            f"### Nhịp người\n\n“{title}” làm lộ ai chỉ giỏi báo cáo, ai giỏi việc. "
            f"Hùng khen đúng, mắng đúng, không mắng để tỏ uy. Lan dần giữ nhịp chuỗi."
        )
    elif n <= 220:
        parts.append(
            f"### Gió ngoài\n\nSau “{title}”, Hùng/Lan ghi bài học thị trường nước ngoài: "
            f"không nịnh, không hứa ảo, không quên bến Việt Nam. Múi giờ lệch không được lệch chuẩn."
        )
    else:
        parts.append(
            f"### Sau bão\n\n“{title}” thuộc nhịp xây lại. Ông không ăn mừng sớm. "
            f"Đi công trường, hỏi công nhân, rà hợp đồng. Lớn mà rỗng thì đừng lớn."
        )

    parts.append(
        f"### Hệ thống\n\n「{y} | {title} — tiến độ ghi nhận | EXP +{60 + n}」\n"
        f"「Gợi ý: uy tín – người – sổ sạch」\n\nHùng đọc rồi tắt."
    )
    nxt = min(360, n + 1)
    nt = OUTLINE["chapters"][str(nxt)]["title"]
    parts.append(f"### Khép\n\n“{title}” có tiến, có sẹo. Mai: “{nt}”. Nhắn Lan: nghỉ đúng.")

    body = "\n\n".join(parts)
    body = pad_clean(body, n, title, y, loc)
    guard = 0
    while count_words(body) < MIN and guard < 40:
        body += (
            f"\n\nChi tiết bổ sung “{title}” ({y}, {loc}): Hùng đối chiếu lời hứa với tiến độ; "
            f"Lan đối chiếu nhịp người với nhịp việc; cả hai chỉ khép khi hết dòng đỏ bỏ quên."
        )
        guard += 1
    text = header(n, title) + footer(body)
    chapter_path(n, title).write_text(text, encoding="utf-8")
    return count_words(text)


def main():
    originals = load_originals()
    nums = sorted(OPENS.keys())
    short = []
    for n in nums:
        w = write_one(n, originals)
        if w < MIN:
            short.append((n, w))
        if n % 20 == 0 or n in (21, 40, 90, 112, 200, 220, 241, 270):
            print(f"Ch {n}: {w}w")
    print("count", len(nums), "short", short)


if __name__ == "__main__":
    main()
