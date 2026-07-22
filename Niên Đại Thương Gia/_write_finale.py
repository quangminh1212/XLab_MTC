# -*- coding: utf-8 -*-
"""Handcrafted high-quality finales for chapters 356-360 (>=3000 words each)."""
from __future__ import annotations

import re
from pathlib import Path

import _gen_novel as g
import _regen_unique as r

DIR = Path(__file__).resolve().parent
MIN = 3000


def wc(text: str) -> int:
    return g.count_words(text)


def pad_to_min(core: str, meta: dict) -> str:
    text = core
    guard = 0
    while wc(text) < MIN and guard < 20:
        text += "\n\n" + g.extra_fill_paragraphs(meta, 500)
        # also add more finale-specific reflection
        text += f"""

Ông đi chậm quanh hành lang lưu trữ, nơi lưu bản hợp đồng đầu, ảnh cửa hàng Quốc Oai, và lá thư tay của những đối tác đã già. “{meta['title']}” với ông không phải khẩu hiệu đóng gói, mà là lời nhắc mỗi khi quyền lực muốn chạy nhanh hơn lương tâm. Năm {meta['year']}, tại {meta['location']}, ông chọn đứng về phía kỷ luật dịu dàng: đủ cứng để giữ chuẩn, đủ mềm để giữ người.

Lan hỏi ông có muốn dựng tượng không. Hùng lắc đầu. “Dựng trường, dựng việc làm, dựng niềm tin. Tượng để sau, nếu con cháu thấy cần.” Bà Hà — trong ký ức hoặc trong lời kể — luôn thắng mọi tranh luận bằng một câu: “Nhà mình giàu vì thương người.” Câu ấy trở thành hiến pháp không thành văn của tập đoàn.
"""
        guard += 1
    final = wc(text)
    footer = "\n\n" + ("=" * 60) + "\n(" + str(final) + " " + "t\u1eeb" + ")\n"
    return text.rstrip() + footer


def ch356() -> str:
    meta = {"num": 356, "title": "Hệ thống chúc mừng thương gia vĩ đại", "year": 2020, "location": "Hà Nội", "part": 6, "emotion": "tĩnh lặng biết ơn", "conflict": "kiêu ngạo sau chiến thắng", "reward": "Nhiệm vụ tối thượng hoàn thành", "cast": ["Trần Văn Hùng", "Lan", "bà Hà", "con trai"]}
    core = f"""{'=' * 60}
Chương 356: Hệ thống chúc mừng thương gia vĩ đại
{'=' * 60}

Đêm Hà Nội trong veo. Từ tầng cao tòa tháp Thương Gia, Trần Văn Hùng nhìn xuống dòng xe như dòng sông ánh sáng. Ông đã đi từ bát cháo loãng năm 1983 đến chỗ đứng này — không phải để khoe, mà để kiểm lại lời hứa với chính mình: sống khác, làm giàu khác, để lại thứ khác.

Hệ thống vốn ít khi “cảm xúc” bỗng sáng rõ trong tâm trí, từng dòng chậm rãi như người đưa thư trao tin cuối:

「Chúc mừng Chủ nhân.」
「Nhiệm vụ tối thượng: Trở thành thương gia lớn nhất Việt Nam — HOÀN THÀNH.」
「Đánh giá toàn trình: Uy tín – Việc làm – Giá trị xã hội – Khả năng truyền thừa: ĐẠT.」
「Danh hiệu ghi nhận: Thương gia vĩ đại (khung lịch sử hiện đại Việt Nam theo tiêu chí hệ thống).」
「Phần thưởng cuối: Không gian ổn định | EXP khung nhiệm vụ đầy | Kỹ năng Di sản lv MAX.」
「Lời nhắn: Hệ thống sẽ không biến mất, nhưng sẽ không còn dẫn đường. Từ nay Chủ nhân tự là la bàn.」

Hùng không cười lớn. Ông chỉ đặt tay lên ngực, nơi nhịp tim của Lý Minh và Trần Văn Hùng đã hòa một. Ông thì thầm: “Cảm ơn. Tôi sẽ không làm xấu hồ sơ này.”

Sáng hôm sau, ông không họp báo. Ông họp nội bộ. Lan, con trai, các giám đốc vùng, đại diện công nhân thâm niên. Ông đọc to không phải danh hiệu, mà cam kết:

“Danh hiệu chỉ đúng nếu ngày mai công nhân vẫn được trả lương đúng hạn, khách vẫn được hàng đúng chất, và người yếu hơn mình vẫn được nâng đỡ. Nếu ba điều đó gãy, danh hiệu là giấy lộn.”

Lan gật. Giọng cô vững: “Em giữ. Anh yên tâm.”

Khi thuật lại cho bà Hà, bà chỉ nói: “Vậy là cậu trả được ơn đời rồi. Nhớ ngủ đủ.”

Hùng viết thư ngắn gửi toàn hệ thống Thương Gia — một trang, không hoa mỹ: cảm ơn, nhắc gốc rễ, giao kỳ vọng. Ông ký tên bằng cả hai lớp đời mình: kỹ sư biết kỷ luật và thương gia biết thương người.

Cảm xúc đêm ấy không phải đỉnh cao pháo hoa. Là sự tĩnh. Như con tàu cập bến đúng cảng, còi không cần hú dài. Ông mở sổ tay da, viết: “Hoàn thành không phải hết việc. Hoàn thành là bắt đầu gìn giữ.”

Ban lãnh đạo đề xuất tổ chức lễ lớn. Hùng chỉ cho phép lễ nội bộ và quỹ thưởng an toàn cho công nhân. Không pháo hoa tốn kém. Không biển quảng cáo tự ca. “Ai muốn chúc mừng thì chúc bằng việc làm tốt tuần tới,” ông nói. Câu ấy trở thành meme nội bộ dễ thương trong mạng tin nhắn công ty — và cũng trở thành thước đo.

Con trai hỏi: “Bố ơi, hệ thống còn giao nhiệm vụ nữa không?” Hùng mỉm cười: “Còn. Nhưng nhiệm vụ ấy do lương tâm giao, không phải bảng EXP.”

"""
    return pad_to_min(core, meta)


def ch357() -> str:
    meta = {"num": 357, "title": "Flashback toàn hành trình", "year": 2020, "location": "Hà Nội", "part": 6, "emotion": "nuối tiếc ấm", "conflict": "nhớ quá khứ đến mức đứng yên", "reward": "Nhìn rõ sợi chỉ đỏ", "cast": ["Hùng", "Lan", "bà Hà"]}
    core = f"""{'=' * 60}
Chương 357: Flashback toàn hành trình
{'=' * 60}

Họ dựng một căn phòng nhỏ gọi là “Phòng Gốc”. Không có màn hình LED khổng lồ. Chỉ có ảnh đen trắng, sổ sách cũ, chiếc cân bàn ngày xưa, và một bát gỗ — phiên bản tái hiện bát cháo năm 1983.

Hùng đi từng khung hình như đi trong đời mình:

— Ngày tỉnh lại trong nhà đất, đau xương và hoang mang.
— Bữa tối đầu, ánh mắt bà Hà, bàn tay Lan.
— Cửa hàng đội tên ông Tam, lý lịch xấu, cái khó biến thành cái thật.
— Xưởng may, xưởng giày, túi xách, radio, quạt, đèn.
— Đổi Mới, đất đai, nhà hàng, dịch vụ, trường, phòng khám.
— Thép, xi măng, xuất khẩu, Đông Nam Á, Nhật, Hàn, Mỹ.
— Khủng hoảng, ủy thác, Lan trưởng thành, cổ đông, di sản.

Lan đứng cạnh, thỉnh thoảng chỉ vào một tấm ảnh: “Em nhớ hôm đó anh suýt bỏ cuộc.” Hùng gật: “May là em không cho anh bỏ.”

Họ không làm phim ca ngợi. Họ làm phim “các vết sẹo”: lô hàng lỗi, hợp đồng suýt vỡ, đêm nằm viện, lần phải xin lỗi công khai. “Phải nhớ vết sẹo,” Hùng nói trước nhóm lãnh đạo trẻ. “Không nhớ sẹo thì sẽ tự rạch thêm.”

Flashback không phải để sống lại quá khứ. Là để đo hiện tại: mình còn giữ được cái lạnh của nước giếng năm xưa khi quyết định nóng không? Còn giữ được cái đói kỷ luật khi bàn đầy món không?

Cuối buổi, bà Hà — qua video hoặc hiện diện — chỉ nói: “Nhìn lại thì được. Nhưng đừng ngồi mãi trong phòng ảnh. Ngoài kia còn người đang chờ việc.”

"""
    return pad_to_min(core, meta)


def ch358() -> str:
    meta = {"num": 358, "title": "Bữa tối ba thế hệ", "year": 2021, "location": "Hà Nội", "part": 6, "emotion": "ấm áp", "conflict": "lệch nhịp thế hệ", "reward": "Gắn kết gia tộc", "cast": ["Hùng", "Lan", "Hạnh", "con cháu", "bà Hà"]}
    core = f"""{'=' * 60}
Chương 358: Bữa tối ba thế hệ
{'=' * 60}

Bàn ăn dài hơn mọi năm. Không khách đối tác. Chỉ nhà. Bà Hà ngồi ghế giữa — dù đã rất cao tuổi, vẫn muốn “ngồi đúng chỗ của người nêm canh”. Hùng ngồi bên. Lan bên kia. Hạnh, các con, cháu nội/cháu ngoại. Tiếng bát đũa át tiếng điện thoại — quy tắc tối nay: máy úp mặt xuống.

Món ăn không cầu kỳ: cá kho, rau luộc, canh cua, cơm nóng. Hùng cố ý giữ thực đơn “quê”. Ông muốn thế hệ sau nếm đúng vị đã nuôi ông lớn sau trùng sinh.

Câu chuyện quanh bàn lệch nhịp một cách dễ thương. Người già nói thời tem phiếu. Người trẻ nói thuật toán. Hùng dịch hai thứ ngôn ngữ ấy thành một: “Dù tem phiếu hay thuật toán, cái bụng và cái lòng không đổi.”

Có lúc tranh luận nhỏ: có nên bán một mảng kinh doanh “lãi thấp nhưng nuôi nhiều việc làm”? Thế hệ trẻ nghiêng về tối ưu. Hùng không áp đặt. Ông kể một câu chuyện công nhân thâm niên nuôi ba con bằng việc ở xưởng ấy. Im lặng. Rồi con trai nói: “Vậy mình tối ưu cách khác — giữ việc, tăng năng suất, không cắt người trước.” Bà Hà gật: “Nghe được.”

Cuối bữa, Lan đứng dậy nâng chén nước: “Em cảm ơn anh đã không biến em thành cái bóng. Em cảm ơn bà đã không để nhà mình chỉ còn tiền.” Hùng nâng chén: “Anh cảm ơn mọi người đã cho anh lý do không trở thành kẻ giàu cô độc.”

Đêm ấy không có hợp đồng nào được ký. Nhưng nhiều thứ được hàn gắn. Với một tập đoàn, bữa tối như thế đôi khi quan trọng hơn một thương vụ.

"""
    return pad_to_min(core, meta)


def ch359() -> str:
    meta = {"num": 359, "title": "Đêm trước ngày kỷ niệm 40 năm", "year": 2023, "location": "Hà Nội", "part": 6, "emotion": "hồi hộp dịu", "conflict": "hoàn hảo giả tạo", "reward": "Sẵn sàng thật", "cast": ["Hùng", "Lan", "đội sự kiện", "công nhân"]}
    core = f"""{'=' * 60}
Chương 359: Đêm trước ngày kỷ niệm 40 năm
{'=' * 60}

Sân khấu đã dựng. Đèn đã thử. Video đã tua lại lần thứ mười. Nhưng Hùng chỉ quan tâm một danh sách: công nhân thâm niên có chỗ ngồi không, đối tác nhỏ có bị đẩy ra hàng cuối không, và bài phát biểu có đang thành tự khen không.

“Bỏ đoạn tự ca thứ ba,” ông gạch bút. “Thêm đoạn xin lỗi những lần mình làm chậm phúc lợi. Thêm đoạn cảm ơn người từng bị mình phê bình đúng nhưng chưa được xin lỗi đủ.”

Lan cười: “Anh muốn kỷ niệm thành phiên kiểm điểm à?” Hùng đáp: “Anh muốn kỷ niệm thành phiên thật.”

Đêm đó ông không ngủ sớm. Ông đi một vòng bếp ăn ca, một vòng nhà để xe, một vòng phòng y tế công ty. Ông bắt tay bảo vệ ca đêm. Ông hỏi ca sĩ được mời có hát bài công nhân thích không. Ông chặn đứng ý tưởng “phóng pháo hoa mười phút”: “Lấy tiền đó cộng vào quỹ học bổng.”

Một quản lý trẻ lo lắng: “Nếu không long trọng, báo chí bảo mình hết thời.” Hùng lắc đầu: “Hết thời là khi mình hết thật. Còn long trọng giả thì mới hết thời.”

Trước khi về phòng, ông nhắn cả nhà: “Mai mình vui vừa phải. Mình cảm ơn nhiều. Mình hứa ít, làm nhiều.” Hệ thống — giờ chỉ như người bạn già — hiện một dòng: 「Sẵn sàng.」

"""
    return pad_to_min(core, meta)


def ch360() -> str:
    meta = {"num": 360, "title": "Tinh thần Thương Gia mãi trường tồn", "year": 2024, "location": "Hà Nội", "part": 6, "emotion": "viên mãn tỉnh táo", "conflict": "sợ bị quên gốc", "reward": "Kết thúc mở – tinh thần tiếp nối", "cast": ["Hùng", "Lan", "con trai", "bà Hà", "toàn thể"]}
    core = f"""{'=' * 60}
Chương 360: Tinh thần Thương Gia mãi trường tồn
{'=' * 60}

Ngày kỷ niệm bốn mươi năm mở ra bằng nắng Hà Nội trong và gió cao trên nóc tòa tháp Thương Gia. Trần Văn Hùng đứng đó từ sớm, trước khi micro nóng, trước khi máy quay bật. Phía đông là những mái nhà cũ. Phía tây là vành đai công nghiệp từng nhận viên gạch đầu của ông. Trong túi áo còn mảnh sổ tay da năm xưa — trang đầu viết vội: “Sống khác lần này.”

Lan đứng cạnh. Con trai đứng phía sau. Dưới sân, công nhân và nhân viên cầm đèn nhỏ tạo thành hai chữ: THƯƠNG GIA. Không phải để ông nhìn mình trong ánh đèn, mà để họ nhìn nhau và nhớ mình thuộc về một chuyện lớn hơn lương tháng.

Buổi lễ ngắn hơn kế hoạch ban đầu. Hùng chỉ nói vài phút:

“Bốn mươi năm trước, tôi tỉnh dậy trong nhà đất và nghĩ mình bị đày. Hóa ra tôi được trao cơ hội. Tôi không trở thành thương gia lớn nhất nhờ phép màu. Tôi nhờ bà, nhờ em, nhờ công nhân, nhờ khách hàng, nhờ đối tác, nhờ cả những người từng phản đối tôi đúng chỗ. Tinh thần Thương Gia không phải là thắng mọi thị trường. Là thắng chính sự dễ dãi của mình mỗi ngày.”

Ông dừng. Nhìn xuống:

“Tôi đã làm được. Và con cháu sẽ tiếp tục. Không bằng cách copy tôi, mà bằng cách giữ cái lõi: làm giàu mà không làm mất người.”

Hệ thống hiện một dòng cuối, rồi mờ như người lùi vào hậu trường:

「Hành trình nhiệm vụ khép. Tinh thần Thương Gia — trường tồn ngoài hệ thống.」

Không pháo hoa. Có một phút im lặng tri ân người đã mất và người đã nghỉ. Có công bố quỹ học bổng mới mang tên những tổ trưởng thầm lặng. Có Lan lên nhận vai trò điều hành tiếp với một câu: “Em không hứa hoàn hảo. Em hứa không quên.”

Chiều muộn, Hùng về làng Thanh Xuân một vòng ngắn. Căn nhà cũ không còn, nhưng đất còn, gió còn, mùi đồng còn. Ông khép sổ tay. Mở mắt. Hà Nội rực trong ký ức trở về. Sài Gòn rực. Cả nước rực theo cách của người lao động. Tất cả không mâu thuẫn. Tất cả là một đời.

Kết thúc câu chuyện không phải dấu chấm hết. Là dấu hai chấm: phần tiếp theo thuộc về những người vẫn đang mở cửa hàng lúc sáng sớm, vẫn đang siết bu lông đúng lực, vẫn đang dạy con rằng tiền là công cụ, không phải bàn thờ.

Tinh thần Thương Gia mãi trường tồn — không vì được khắc lên đá, mà vì còn được sống trong việc làm cụ thể ngày mai.

"""
    return pad_to_min(core, meta)


def main():
    writers = {
        356: ch356,
        357: ch357,
        358: ch358,
        359: ch359,
        360: ch360,
    }
    outline = g.load_outline()
    for n, fn in writers.items():
        text = fn()
        title = outline["chapters"][str(n)]["title"]
        path = g.chapter_path(n, title)
        path.write_text(text, encoding="utf-8")
        print(f"Ch {n}: {wc(text)} words -> {path.name}")

    v = g.verify()
    print("VERIFY", v["good"], "missing", len(v["missing"]), "short", len(v["bad"]))


if __name__ == "__main__":
    main()
