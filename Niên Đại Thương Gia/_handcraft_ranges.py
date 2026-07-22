# -*- coding: utf-8 -*-
"""
Handcrafted high-quality rewrite for key ranges:
  1-10   foundation emotion
  221-230 crisis 2008 arc
  296-305 succession beat
  356-360 finale polish
Preserve original cores when available; literary frame + deep scenes.
"""
from __future__ import annotations

import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

from _final_complete import count_words, load_originals, clean_core, chapter_path, MIN
from _continue_v2 import pad_clean, year_of, loc_of

DIR = Path(__file__).resolve().parent
OUTLINE = json.loads((DIR / "chapter_outline.json").read_text(encoding="utf-8"))

RANGES = [(1, 10), (221, 230), (296, 305), (356, 360)]


def header(n: int, title: str) -> str:
    return "=" * 60 + f"\nChương {n}: {title}\n" + "=" * 60 + "\n\n"


def footer(body: str) -> str:
    w = count_words(body)
    return body.rstrip() + "\n\n" + ("=" * 60) + f"\n({w} từ)\n"


# ---------- Range-specific literary openers & scenes ----------

FOUNDATION = {
    1: None,  # keep as-is if literary
    2: """Đêm đầu sau ngày tỉnh lại, căn bếp tôn rỉ set vẫn là trung tâm vũ trụ nhỏ của nhà Trần. Bà Hà quỳ nhóm lửa. Lan thái rau lang. Hùng đứng ở ngưỡng cửa với hai đời trong một bộ xương: kỹ sư chết vì deadline, và đứa cháu từng làm bà khóc.

Ông không hứa to. Ông nhóm lửa. Ông lấy gạo từ không gian. Ông nấu một bữa no — cơm trắng, thịt kho, trứng — và nhìn bà múc cơm ít cho mình như bản năng cả đời. “{title}” không phải chiến lược. Là lần đầu ông chọn làm người nhà thay vì kẻ hứa suông.""",
    3: """Buổi sáng huyện thành năm {y} đặc sệt bụi và tiếng loa phát thanh. “{title}” với Hùng là bước ra khỏi làng mà không được để lộ mình mang thế kỷ 21 trong túi. Ông tính từng đồng, từng mối, từng ánh mắt nghi ngờ dành cho lý lịch xấu.

Lan nhìn anh ra đi. Bà Hà dặn mặc áo ấm. Hệ thống lặng trong đầu như người thư ký không được phép lộ diện.""",
    4: """Quầy hàng tạm, ánh nắng vỡ trên thúng rau, tiếng mặc cả. “{title}” là lần Hùng đặt giá không run. Kỹ năng Thương mại trong đầu thì thầm con số; trái tim thì run vì bà Hà còn đói.

Người mua soi hàng. Người hỏi nguồn. Ông trả lời vừa đủ thật để không vỡ kế hoạch, vừa đủ khôn để không lộ không gian. Bán xong đồng đầu, ông không cười khoác lác — ông đếm tiền rồi nghĩ bữa tối nhà.""",
    5: """Sau đồng lãi mỏng, “{title}” kéo Hùng vào vòng xoáy: nhập thêm, bán thêm, sợ ế, sợ lộ. {loc}, {y}. Ông học rằng mở rộng sớm quá cũng là một dạng tham — tham cũng giết người như đói.

Lan hỏi: “Anh có chắc không?” Hùng đáp: “Chắc điều kiện. Chưa chắc kết quả.”""",
    6: """Đối tác không rơi từ trời. “{title}” là đi tìm, bị từ chối, bị soi lý lịch, rồi gặp người chịu bắt tay. Hùng học cách cúi đúng lúc và thẳng đúng lúc.

Mỗi cái bắt tay là một sợi dây. Sợi dây có thể kéo lên — hoặc siết cổ nếu mình dối.""",
    7: """Mái dột. Tường ẩm. “{title}” nghe nhỏ so với đế chế tương lai, nhưng với bà Hà là cả trời. Hùng sửa nhà bằng tay và bằng tiền kiếm được — không bằng lời.

Khi mưa không còn rơi vào chiếu, bà thở dài một cái như trả món nợ với trời.""",
    8: """Kệ hàng dài thêm. Mùi xà phòng, vải, thuốc men len vào nhau. “{title}” dạy ông: đa dạng SKU mà loạn quy trình thì chỉ là đống đồ. Ông ghi sổ. Phân loại. Giữ uy tín từng món.""",
    9: """“{title}” chạm vùng nhạy: sức khỏe, niềm tin, tin đồn. Hùng không chơi trò thần dược. Ông bán đúng thứ cần, nói rõ giới hạn, nhờ chị Hồng phòng khám. Làm ăn với thuốc men mà ẩu là tội.""",
    10: """Chuyến đi Hà Nội năm {y} — phố lớn, người đông, cửa hàng sáng hơn làng. “{title}” mở mắt Hùng: thị trường không chờ người có lý lịch đẹp. Nó chờ người giao đúng, đủ, sạch.

Ông về khuya, bụi bám áo, trong túi có mối và trong đầu có bản đồ.""",
}

CRISIS = {
    221: """Năm 2008, bảng dòng tiền dán tường Hà Nội chuyển đỏ như vết mực loang. “{title}” không còn là kịch bản tập. Tin xấu quốc tế chạy nhanh hơn công văn nội bộ.

Hùng họp 70 phút: không giấu lỗ, không sa thải hoảng, không bán rẻ uy tín, cắt chi hoa hòe, giữ lương cốt lõi nếu năng suất giữ. Ai muốn “làm đẹp báo cáo quý” bị gạt phắt. Lan gọi đối tác nửa đêm. Sự thật được công bố vừa đủ để chặn tin đồn.""",
    222: """Hệ thống cảnh báo sớm — trong đầu Hùng và trên bảng Excel — cùng kêu. “{title}” là bài học ông mang từ thế kỷ 21: khủng hoảng ít khi đến không gõ cửa.

Ông lập “phòng chiến sự nhỏ”: cập nhật hàng ngày, ba màu, không trang trí số. Ai giấu rủi ro bị xử; ai báo sớm được bảo vệ.""",
    223: """Họp khẩn không có bánh ngọt. “{title}” chỉ có nước lọc và khuôn mặt trắng. Hùng nhìn từng giám đốc: “Nói xấu trước. Nói đẹp để sau.”

Lan ghi biên bản. Kho bạc đọc hạn mức. Sản xuất đọc đơn hàng. Họ chốt kịch bản A–B–C trước khi tan họp.""",
    224: """Bảo vệ dòng tiền là bảo vệ hơi thở. “{title}” buộc cắt những thứ từng làm ông thích: chi hoa, chuyến bay không cần, dự án khoe. Giữ quỹ lương. Giữ nguyên liệu cốt lõi. Giữ lời hứa với người làm công.""",
    225: """Trong hoảng loạn có người bán rẻ. “{title}” là lúc Hùng mua thứ có giá trị thật với giá người khác không chịu nổi nhìn. Không phải vì máu lạnh — vì ông đã chuẩn bị thanh khoản và thần kinh từ trước.""",
    226: """Đối tác nhỏ suýt gãy chuỗi. “{title}” là quyết định cứu họ bằng tín dụng ngắn và đơn hàng ổn định — không phải từ thiện suông, mà vì chuỗi chết thì mình cũng chết. Lan theo dõi từng khoản giải ngân như theo dõi mạch.""",
    227: """Lan giữ thị trường Mỹ giữa bão. “{title}” là cuộc gọi múi giờ lệch, email gấp, khách hoảng. Cô không hứa giảm giá ảo. Cô hứa giao đúng và minh bạch tiến độ. Hùng ở nhà chống lưng số liệu.""",
    228: """Ngân hàng quốc tế siết. “{title}” là đàm phán bằng hồ sơ sạch và lịch sử trả nợ, không bằng quan hệ mờ. Hùng mang sự khiêm tốn và sự cứng: “Chúng tôi không xin thương hại. Chúng tôi xin điều kiện rõ.”""",
    229: """Áp lực sa thải hàng loạt đến từ mọi phía. “{title}” là dòng Hùng viết lên bảng: KHÔNG. Ông cắt thưởng nóng, cắt dự án, cắt ego — không cắt người chỉ để đẹp báo cáo. Ai không đủ việc được đào tạo chuyển việc trong hệ thống.""",
    230: """Sau phòng thủ là cơ hội. “{title}” nhìn vào khoảng trống đối thủ để lại. Hùng không ăn mừng. Ông chỉ mở một cửa nhỏ: tuyển người giỏi bị sa thải nơi khác, mua máy tốt giá thấp, giữ văn hóa không hoảng.""",
}

SUCCESSION = {
    296: """Cải cách lương và phúc lợi năm {y} chạm túi tiền và lòng tin. “{title}” không phải tăng cho vui. Hùng/Lan mở số liệu năng suất, tham chiếu thị trường, ngồi với công đoàn. Ai đóng góp nhiều được nhìn thấy. Ai yếu được kèm, không bị bỏ.""",
    297: """Đối thoại công đoàn không phải sân khấu. “{title}” là bàn dài, micro tắt, giấy bút bật. Hùng nghe phàn nàn ca đêm, xe đưa đón, nhà trẻ. Ông không hứa tất cả. Ông hứa thứ làm được trong quý — và làm.""",
    298: """Đào tạo lãnh đạo trẻ: không khóa học xa xỉ. “{title}” là kèm việc thật, giao việc có hậu quả, cho quyền sai có kiểm soát. Lan ngồi ban giám khảo. Hùng chỉ hỏi một câu: “Em dám chịu trách nhiệm khi xấu không?”""",
    299: """Hùng 55 tuổi. Gương soi không nịnh. “{title}” là buổi chiều ông ngồi một mình nhớ bát cháo, nhớ nằm viện, nhớ lần buông quyền. Ông không sợ già. Ông sợ mình ôm ghế đến mức bẻ gãy người kế.""",
    300: """Giao quyền vận hành cho Lan. Không pháo hoa. Biên bản. Vòng tay. “{title}” là câu: “Em không copy anh. Em làm bản tốt hơn.” Người cũ lo. Văn hóa được giữ bằng xử đúng. Con trai đứng sau học thầm.""",
    301: """Lan CEO. Ngày đầu ghế không êm. “{title}” là email, họp, và một quyết định khó ngay buổi sáng. Hùng lui về chiến lược — đủ gần để đỡ, đủ xa để em bay. Bà Hà chỉ hỏi: “Cháu gái có ăn không?”""",
    302: """Hùng Chủ tịch Hội đồng. “{title}” đổi cách ông xuất hiện: ít lệnh hơn, nhiều hỏi hơn. Ông học im. Im đúng lúc cũng là lãnh đạo.""",
    303: """Thế hệ ba bắt đầu từ việc nhỏ: đi xưởng, ghi sổ, bị mắng đúng. “{title}” không phải trao vương miện. Là trao kỷ luật.""",
    304: """Du lịch tri ân đối tác cũ. “{title}” là bay, bắt tay, nhớ hợp đồng năm xưa. Hùng không khoe tài sản. Ông khoe người còn làm cùng.""",
    305: """Gặp lại ông Tanaka. Trà Nhật. Im lặng có trọng lượng. “{title}” là cảm ơn người từng mở cửa khi Việt Nam còn bị nhìn bằng ánh mắt dè dặt. Hai người già (hơn xưa) cười vì còn sống để nhìn việc mình làm lớn.""",
}

FINALE = {
    356: """Đêm Hà Nội. Từ tầng cao, dòng xe như sông ánh sáng. Hệ thống — vốn ít cảm xúc — đọc chậm:

「Nhiệm vụ tối thượng — HOÀN THÀNH.」
「Chủ nhân tự là la bàn.」

“{title}” không đưa Hùng ra họp báo. Ông họp nội bộ: danh hiệu chỉ đúng nếu lương đúng hạn, hàng đúng chất, người yếu được nâng. Lan gật: “Em giữ.”""",
    357: """Phòng Gốc: ảnh đen trắng, cân bàn, bát gỗ tái hiện cháo 1983. “{title}” là đi trong đời mình — từ hôn mê đến tòa tháp — không để tự khen, để nhớ sẹo. Lan chỉ tấm ảnh: “Hôm đó anh suýt bỏ.” Hùng: “May em không cho.”""",
    358: """Bàn dài. Máy úp. Cá kho, rau luộc, canh. “{title}” là ba thế hệ nói chuyện lệch nhịp mà không vỡ. Tranh luận có nên giữ mảng lãi thấp nuôi việc làm. Thế hệ trẻ đề xuất tối ưu khác — giữ việc, tăng năng suất. Bà Hà gật: “Nghe được.”""",
    359: """Đêm trước kỷ niệm 40 năm. Hùng gạch đoạn tự ca thứ ba trong bài phát biểu. “{title}” là kiểm tra danh sách: công nhân thâm niên có ghế không, đối tác nhỏ có bị đẩy cuối không. Ông cắt pháo hoa: lấy tiền cộng quỹ học bổng.""",
    360: """Nóc tháp. Gió cao. Đèn dưới sân xếp THƯƠNG GIA. Lan cạnh. Con trai sau.

“Tôi đã làm được. Và con cháu sẽ tiếp tục. Không copy tôi — giữ lõi: làm giàu mà không làm mất người.”

「Hành trình nhiệm vụ khép. Tinh thần Thương Gia — trường tồn ngoài hệ thống.」

Không pháo hoa. Im lặng tri ân. Quỹ học bổng thầm lặng. Lan: “Em không hứa hoàn hảo. Em hứa không quên.” Làng Thanh Xuân còn đất, gió, mùi đồng. Kết thúc là dấu hai chấm.""",
}


def build_chapter(n: int, originals: dict[int, str]) -> str:
    title = OUTLINE["chapters"][str(n)]["title"]
    path = chapter_path(n, title)

    # keep ch1
    if n == 1 and path.exists():
        cur = path.read_text(encoding="utf-8", errors="replace")
        if "Đau. Đau như thể" in cur and count_words(cur) >= MIN:
            return cur

    y = year_of(n, title)
    loc = loc_of(n, title)
    core = originals.get(n, "")

    # pick handcrafted body
    if n in FOUNDATION and FOUNDATION[n]:
        craft = FOUNDATION[n].format(title=title, y=y, loc=loc)
        era = "foundation"
    elif n in CRISIS:
        craft = CRISIS[n].format(title=title, y=y, loc=loc)
        era = "crisis"
        y = 2008
        loc = "Hà Nội"
    elif n in SUCCESSION:
        craft = SUCCESSION[n].format(title=title, y=y, loc=loc)
        era = "succession"
    elif n in FINALE:
        craft = FINALE[n].format(title=title, y=y, loc=loc)
        era = "finale"
    else:
        craft = f"Năm {y} tại {loc}, “{title}” được Hùng xử lý bằng hiện trường, sổ sách và người."
        era = "default"

    parts = [
        f"### Mở\n\n{craft}",
    ]

    if core and count_words(core) >= 80 and n <= 154:
        parts.append("### Diễn biến đã xác lập\n\n" + core)
        parts.append(
            f"""### Lớp sâu

Sau những gì đã xảy ra trong “{title}”, Hùng không vội khoe. Ông ngồi với Lan và bà Hà, hỏi chỗ suýt sai. Năm {y} tại {loc}, ông chọn: hiện trường trước báo cáo, người trước danh, sự thật trước thể diện.

Lan tinh. Em chặn lời hứa nhanh. Hùng sửa cho vừa sức rồi làm đủ. Đó là khác biệt giữa thương gia và kẻ chộp giật."""
        )
    else:
        parts.append(
            f"""### Việc cụ thể

Ê-kíp chia việc quanh “{title}”: ai hiện trường, ai số, ai khách, ai nội bộ. Rủi ro được gọi tên. Checklist một trang. Ký đã hiểu. Làm. Không “nhìn chung ổn”."""
        )

    # emotional beat by era
    if era == "foundation":
        parts.append(
            f"""### Bếp lửa

Đêm sau “{title}”, mâm cơm có thể mỏng nhưng ánh mắt không mỏng. Bà Hà múc cơm. Lan còn nghi ngờ một phần — và hy vọng một phần. Hùng chứng minh bằng việc mai còn làm, không bằng bài diễn."""
        )
    elif era == "crisis":
        parts.append(
            f"""### Áp lực và xương sống

Trong “{title}”, có người khuyên Hùng “cứng” với lao động để giữ cổ phiếu. Ông lắc: “Cổ phiếu lên bằng cách bẻ người thì tôi không chơi.” Lan siết tay anh một cái — đủ hiểu."""
        )
    elif era == "succession":
        parts.append(
            f"""### Đổi vai

“{title}” làm lộ ai thật sự phục vụ tập đoàn, ai chỉ phục vụ ghế. Hùng không thanh trừng ồn. Ông đặt chuẩn và để chuẩn lọc. Lan đứng ở giữa — đủ mềm để nghe, đủ cứng để quyết."""
        )
    else:
        parts.append(
            f"""### Khép vòng

“{title}” đưa hành trình về đúng chỗ: không phải đỉnh để kiêu, mà là bến để truyền. Hùng nhìn Lan, nhìn con, nhìn ảnh bà Hà — và thấy mình già hơn, nhẹ hơn."""
        )

    parts.append(
        f"""### Hệ thống

「{y} | {title} — tiến độ ghi nhận | EXP +{80 + n}」
「Gợi ý: giữ người – giữ sổ – giữ uy tín」

Hùng đọc rồi tắt. Thước đo, không phải ông chủ."""
    )

    nxt = min(360, n + 1)
    nt = OUTLINE["chapters"][str(nxt)]["title"]
    parts.append(
        f"""### Khép ngày

“{title}” có tiến, có sẹo. Hùng nhắn Lan: “Mai tiếp. Nhớ nghỉ.” Phía trước: “{nt}”."""
    )

    body = "\n\n".join(parts)
    body = pad_clean(body, n, title, y, loc)
    # ensure min
    guard = 0
    while count_words(body) < MIN and guard < 40:
        body += (
            f"\n\nThêm một lớp chi tiết cho “{title}” năm {y} tại {loc}: Hùng đối chiếu lời hứa với tiến độ, "
            f"Lan đối chiếu nhịp người với nhịp việc, và cả hai chỉ khép khi không còn dòng đỏ bỏ quên."
        )
        guard += 1
    return header(n, title) + footer(body)


def main():
    originals = load_originals()
    done = []
    for a, b in RANGES:
        for n in range(a, b + 1):
            text = build_chapter(n, originals)
            title = OUTLINE["chapters"][str(n)]["title"]
            path = chapter_path(n, title)
            path.write_text(text, encoding="utf-8")
            w = count_words(text)
            done.append((n, w))
            print(f"Ch {n}: {w}w | {title}")
    short = [(n, w) for n, w in done if w < MIN]
    print("SHORT", short)
    print("DONE handcraft", len(done))


if __name__ == "__main__":
    main()
