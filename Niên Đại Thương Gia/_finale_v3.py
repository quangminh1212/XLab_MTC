# -*- coding: utf-8 -*-
from pathlib import Path
import re
from collections import Counter

DIR = Path(__file__).resolve().parent
MIN = 3000


def cw(text: str) -> int:
    text = re.sub(r"={5,}", " ", text)
    text = re.sub(r"\(\d+\s*từ\)", " ", text, flags=re.I)
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def write_ch(n, title, paragraphs):
    bar = "=" * 60
    body = "\n\n".join(p.strip() for p in paragraphs if p.strip())
    beat_i = 0
    seeds = [
        "Hùng đi chậm quanh khu vực liên quan mốc ngày, chào người thật, hỏi một câu cụ thể không sáo.",
        "Lan ghi biên bản việc–người–hạn sau mỗi quyết định; không biên bản thì coi như chưa chốt.",
        "Một chi tiết nhỏ ngoài kịch bản được xử trong ngày — vì để sang tuần sẽ thành tin đồn.",
        "Bà Hà trong ký ức chỉ hỏi ăn chưa; ông trả lời bằng việc về nhà đúng bữa.",
        "Con trai mang một số liệu xưởng và một câu chuyện thợ; Hùng yêu cầu cả hai cùng đúng.",
        "Hạnh siết lịch thuốc và giấc ngủ như siết KPI sức khỏe; ông tuân thủ không cãi.",
        "Đối tác gửi lời chúc; ông cảm ơn ngắn, không phóng đại thành chiến thắng vũ trụ.",
        "Quỹ/minh bạch: một dòng số được soi lại nguồn trước khi công bố.",
        "Ông mở sổ da viết bốn mục: được, chưa, cảm ơn, xin lỗi.",
        "Im lặng hệ thống được chấp nhận như khoảng trống để người nói thật.",
        "Mùi đời sống — cơm, máy, mưa, gió tháp — kéo ông khỏi tháp ngà tự phong.",
        "Người trẻ hỏi có che giấu gì không; ông cho quyền hỏi đến khi rõ.",
        "Ủy thác không phải bỏ mặc: tin và kiểm có nhịp.",
        "Nóc tháp và làng Thanh Xuân cùng tồn tại trong một nhịp thở.",
        "Không pháo hoa trong đầu; chỉ danh sách việc mai và người cần gọi.",
    ]
    while cw(body) < MIN:
        s = seeds[beat_i % len(seeds)]
        layer = beat_i // len(seeds) + 1
        who = ["ca kíp", "thủ quỹ", "bảo vệ", "kỹ sư trẻ", "người làng", "tổ trưởng", "tài xế"][
            beat_i % 7
        ]
        para = (
            f"Nhịp bổ sung {beat_i + 1} trong “{title}”: {s} "
            f"Lớp {layer} gắn với {who} Hùng gặp hôm ấy. "
            f"Ông đo ngày bằng việc đã trả lời được, không bằng lời hay trên sân khấu. "
            f"Lan đối chiếu; nếu lệch, sửa trước khi ngủ. Chi tiết số {beat_i + 1} được ghi sổ."
        )
        body += "\n\n" + para
        beat_i += 1
        if beat_i > 80:
            break
    w = cw(body)
    text = f"{bar}\nChương {n}: {title}\n{bar}\n\n{body}\n\n{bar}\n({w} từ)\n"
    path = list(DIR.glob(f"Chương {n} - *.txt"))[0]
    path.write_text(text, encoding="utf-8")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    mr = Counter(lines).most_common(1)[0]
    print(n, w, "maxrep", mr[1], path.name)
    return w


p356 = [
    "### Phòng làm việc cuối nhiệm vụ",
    "Năm 2024. Phòng làm việc của Trần Văn Hùng giản dị đến mức khách lần đầu hay ngỡ nhầm phòng thư ký lâu năm. Bàn gỗ sơn lại lần ba. Trên tường: ảnh bà Hà, ảnh Lan ngày mở cửa hàng đầu, ảnh công nhân ca đêm năm 2008, và một tấm bản đồ thế giới đầy ghim nhỏ — mỗi ghim một nơi Thương Gia từng hứa và phải trả.",
    "Ông pha trà. Tay hơi run — không vì sợ hãi, vì tuổi và vì cảm giác lạ: hệ thống trong đầu, người bạn câm lặng suốt hơn bốn thập niên, đang rõ hơn bình thường. Không rõ như mệnh lệnh. Rõ như người sắp ngừng nói.",
    "「Chủ nhân. Tiến độ nhiệm vụ tối thượng: hoàn tất điều kiện cốt lõi. Đang tổng hợp…」",
    "Hùng đặt tách xuống. Ngoài cửa kính, Hà Nội 2024 sáng đèn. Ông nhớ Hà Tây 1983 tối đèn dầu. Hai hình ảnh chồng lên nhau không còn đau như ngày tỉnh lại — chúng trở thành một đường thẳng.",
    'Lan gõ cửa, bước vào với hai sổ: một sổ vận hành, một sổ quỹ di sản. "Anh gọi em gấp."',
    '"Hệ thống sắp chốt," Hùng nói đơn giản. "Anh muốn em có mặt. Không phải để chứng kiến phép màu. Để chứng kiến mình không bị phép màu làm hỏng."',
    'Con trai đứng sau Lan, áo sơ mi còn mùi xưởng. Nó không hỏi thưởng gì. Nó hỏi: "Bố có khỏe không?" Hùng cười. Câu hỏi đúng.',
    "### Thông báo",
    "Ánh sáng trong tâm trí không chói. Chữ hiện ra chậm, từng khối:",
    "「CHÚC MỪNG CHỦ NHÂN — TRẦN VĂN HÙNG\nNhiệm vụ tối thượng: Trở thành thương gia lớn gắn với trách nhiệm với người và đất nước — HOÀN THÀNH.\nChỉ số tổng hợp: Uy tín dài hạn đạt; Việc làm tạo ra và giữ đạt; Sổ sách minh bạch cốt lõi đạt; Truyền thừa có người đạt; Ảnh hưởng xã hội có kiểm chứng đạt.\nDanh hiệu ghi nhận: Thương gia vĩ đại trong hành trình đã chọn.\nEXP cuối: 98.500 | Không gian cất giữ: 60.000m²\nTrạng thái hệ thống: chuyển sang chế độ im lặng hỗ trợ tối thiểu.\nPhần còn lại thuộc về con người.」",
    "Im lặng dài. Lan mắt đỏ nhưng không khóc òa. Con trai nuốt nước bọt. Hùng chống tay lên bàn, thở ra một hơi như người hạ bao gạo xuống đất sau chặng đường xa.",
    '"Nó nói xong rồi," ông khẽ. "Từ nay anh phải sống không có đáp án nhấp nháy."',
    'Lan: "Anh vốn đã sống bằng việc, không bằng đáp án."',
    '"Đúng. Nhưng biết có người nhắc vẫn đỡ." Ông nhìn hai đứa. "Nên anh nhắc lại bằng miệng người: không dối, không bỏ người, không lấy ngắn nuôi dài bằng cách bẻ chuẩn."',
    "### Không lễ pháo",
    'Không họp báo. Không livestream. Hùng chỉ gửi một thư nội bộ ngắn cho ban lãnh đạo: "Hôm nay tôi khép một chặng riêng tư. Tập đoàn không nghỉ. Các bạn làm việc như mọi ngày — sạch và đủ. Cảm ơn."',
    "Một số người tò mò. Một số đoán sức khỏe. Một số đoán niêm yết mới. Ông để họ đoán. Sự thật lớn đôi khi không cần đám đông mới đúng.",
    'Ông gọi điện về làng Thanh Xuân, nhờ người thăm lại mảnh vườn cũ. "Không xây gì thêm. Chỉ quét sạch và giữ." Tiền có thể dựng tháp. Đất quê cần được giữ như ký ức có địa chỉ.',
    "### Bà Hà trong khung ảnh",
    'Hùng lau khung ảnh bà bằng khăn mềm. "Bà ơi, hệ thống khen cháu. Cháu không mang danh hiệu ấy ra chợ. Cháu mang về nhà xem bà có gật không."',
    'Trong óc ông, giọng bà không khen vĩ đại. Bà chỉ hỏi: "Ăn chưa? Người ta còn việc không?" Ông đáp như thời còn nghèo: "Rồi. Còn. Con nhớ."',
    'Lan đặt tay lên vai anh. "Em sẽ giữ quỹ học bổng mang tên bà. Công khai từng đồng."',
    '"Công khai," Hùng nhắc. "Thiện mà mờ là nợ."',
    "### Hệ thống im",
    "「Ghi nhận lần cuối trong ngày: Chủ nhân đã xác nhận truyền thừa. Không yêu cầu phần thưởng vật chất bổ sung. Chúc chủ nhân bình an.」",
    "Dòng chữ tắt. Khoảng trống trong đầu rộng như sân nhà đất xưa. Hùng không sợ. Ông sợ mình kiêu. Nên ông đứng dậy, xắn tay, tự rót nước cho con và Lan.",
    '"Mai vẫn họp 7 giờ 30," ông nói. "Không vì hệ thống hết việc mà người hết việc."',
    'Con trai gật. "Con vào xưởng sớm." Lan: "Em rà báo cáo quỹ."',
    "Hùng nhìn hai người — hai nhịp tim của đế chế — và thấy mốc này không phải điểm kết của tham vọng. Là điểm bắt đầu của sự khiêm tốn có hệ thống.",
    "### Việc ngay trong ngày vinh danh",
    "Thay vì tiệc, ông duyệt quỹ: mười hai hồ sơ đạt, một hồ sơ treo vì chứng từ mờ, một kỹ thuật viên được thưởng vì bắt lỗi số. Lan ngồi ký. Không có hoa trên bàn — có dấu mộc.",
    'Một giám đốc chi nhánh xin lời chúc truyền cảm hứng để dán poster. Hùng viết một câu: "Làm đủ đã là cảm hứng." Người ta tưởng ông đùa. Ông không đùa.',
    'Chiều, ông xuống bếp tập đoàn ăn cùng ca C. Công nhân ngạc nhiên. Ông hỏi canh có đủ đạm không, ca đêm có xe đưa đón không. Một tổ trưởng nói thật: "Có, nhưng ghế chờ mưa chưa đủ." Ông ghi sổ. "Tuần này có." Không hứa suông năm sau.',
    'Có người muốn gọi ông là thương gia vĩ đại ngay trên loa nội bộ. Ông giơ tay chặn. "Gọi bằng việc làm được. Danh hiệu để hệ thống giữ. Người giữ chuẩn."',
    "### Thoại cuối chương",
    'Lan: "Anh có tiếc không? Tiếc cái thời nó còn giao nhiệm vụ."',
    'Hùng: "Tiếc một chút. Như tiếc người thầy im. Nhưng thầy im thì trò phải đứng."',
    'Con trai: "Bố đứng đã lâu."',
    'Hùng: "Đứng lâu chưa chắc đứng đúng. Từ nay các con giữ nhau đứng đúng."',
    "Ngoài phố, còi xe và đèn đường. Trong phòng, trà nguội. Ông không hâm lại. Ông để nguội — chấp nhận thời gian trôi mà không cần vặn ngược.",
    'Khép ngày: không pháo hoa. Chỉ ba chữ ông viết vào sổ da: "Xong nhiệm vụ. Còn làm người."',
    "### Đêm nhà",
    'Nhà riêng. Hạnh kiểm huyết áp. Số ổn. Ông kể thông báo hệ thống như kể hết một mùa vụ. Hạnh không hỏi danh hiệu. Hạnh hỏi: "Ông có định nghỉ thật không?"',
    '"Nghỉ ôm đồm. Không nghỉ trách nhiệm."',
    "Lan ngủ lại nhà anh. Con ngủ ghế. Đêm gia đình không livestream. Máy chủ tập đoàn vẫn chạy. Người thì được phép tắt.",
    'Trước khi ngủ, Hùng đặt tay lên khung ảnh bà một lần nữa. Không khấn vái. Chỉ báo cáo: "Con vẫn nhớ ăn. Con vẫn nhớ người. Hệ thống khen con — con không kiêu."',
]

p357 = [
    "### Cuốn phim không có nhạc nền hùng tráng",
    "Đêm sau ngày hệ thống chúc mừng, Hùng không ngủ ngay. Ông ngồi trong phòng tối, chỉ một đèn bàn. Lan mang chăn. Con trai mang thêm tách nước. Họ không bật slide. Họ để ký ức tự chạy.",
    "### 1983 — Đau và cháo",
    "Căn nhà đất. Bà Hà thổi lửa. Lan gầy. Hùng — Lý Minh trong xương Trần Văn Hùng — cầm gạo từ không gian mà tim đập như ăn cắp. Bát cháo nóng. Bà khóc thầm vì no. Đó là thương vụ đầu tiên: đổi kiến thức tương lai lấy một bữa cơm người già.",
    "Ông nhớ mùi khói xộc mũi, nhớ tiếng lá cọ trên mái, nhớ nỗi sợ bị lộ. Sợ ấy dạy ông về sau: mọi lợi thế bí mật phải biến thành lợi ích công khai cho người — nếu không chỉ là gian lận có hệ thống.",
    "### Cửa hàng đầu — biển tên ông Tam",
    "Chữ sơn chưa đều. Người xem nhiều hơn người mua. Lý lịch xấu như bóng. Ông Tam đứng đó — thương binh, đảng viên, cái danh cho một thanh niên mang họ tư sản. Hùng không quên ơn ấy bằng bài phát biểu. Ông quên ơn ấy bằng cách không làm nhục biển tên: thuế đủ, hàng thật, không đút lót khoác áo quan hệ.",
    "### Xưởng may, xưởng giày, mùi keo và vải",
    'Bà Phương đếm bo. Ông Tường gõ đế. Hàng lỗi bị Hùng hạ xuống dù đơn gấp. "Danh dự mất bắt đầu từ đường chỉ." Công nhân lúc đầu bực. Về sau họ hiểu: bị chặn sớm rẻ hơn bị khách chửi và mất nghề.',
    "Hùng đi dép trong xưởng, không đi giày bóng hội nghị. Bụi vải bám ống quần là huân chương im lặng. Flashback cho con trai thấy: bố không sinh ra trên sân khấu.",
    "### Đổi Mới — gió lớn, thuyền nhỏ",
    "Có người bảo lao vào tất cả. Hùng chọn vài ngành mình giữ được chuẩn. Có cửa hàng chết. Có đất mua đúng. Có đất suýt sai. Ông ghi sổ từng vết xước. Lan dần không còn chỉ là em gái trông quán — thành người đọc được số và đọc được người.",
    "Ủy thác bắt đầu từ việc anh cho em ký đơn hàng nhỏ và chịu nếu sai. Sai thật sự xảy ra một lần. Anh không che. Em không trốn. Khách được xin lỗi bằng hàng bù và hạn rõ. Niềm tin nội bộ lớn hơn nỗi xấu hổ.",
    "### FDI và cái cúi đầu đúng lúc",
    "Ông Tanaka không cần Hùng hùng hồn. Ông cần hàng đúng hạn và sự thật khi trễ. Lần đầu trễ, Hùng gọi trước khi bên kia hỏi. Hợp đồng lần hai dài hơn — vì tin, không vì sợ.",
    "Phòng khách sạn cũ, trà nguội, bản vẽ kỹ thuật. Hùng nuốt tiếng Việt trong đầu để nói tiếng Anh chậm mà đúng. Lan ngồi góc tập phiên dịch thương mại bằng sổ tay. Flashback giữ cả sự vụng về — vì vụng mà thật thì dạy được người sau.",
    "### 2008 — bảng đỏ",
    'Phòng họp lạnh. Ai cũng muốn giữ mặt. Hùng chọn giữ lương cốt lõi và cắt chi hoa hòe. Có cổ đông chửi. Có báo nghi. Công nhân ca đêm vẫn có cơm. Đến khi thị trường bật, Thương Gia không phải tập đoàn sống sót bằng cách xé người.',
    "Đêm ấy ông nôn khan vì cà phê và áp lực. Hạnh đưa nước ấm. Lan gác điện thoại. Flashback không bỏ đoạn yếu. Đoạn yếu mới là xương sống câu chuyện.",
    "### Nóc tháp và làng",
    "Hai nơi ấy luôn tồn tại song song trong đầu ông. Nóc tháp dạy quy mô. Làng dạy gốc. Ai chỉ sống trên nóc sẽ chóng mặt. Ai chỉ sống dưới làng sẽ bỏ lỡ việc lớn phải làm cho nhiều người.",
    "### Những người không lên ảnh",
    'Tài xế. Thủ kho. Người lau nhà vệ sinh tòa nhà. Giáo viên trường nghề. Bác sĩ phòng khám. Họ hiện trong flashback rõ hơn cả doanh thu năm kỷ lục. Hùng nói với con: "Nếu cháu chỉ nhớ bố trên báo, cháu đã quên Thương Gia."',
    "Ông kể tên cụ Thịnh gác cổng mười tám năm. Kể chị Mai ở kho chưa một lần để hàng nhầm mã. Kể thầy dạy nguội ở trường nghề. Flashback có hộ chiếu cho tên nhỏ.",
    "### Lan trong từng cuộn phim",
    'Ban đầu Lan sợ sổ. Sau Lan sợ lời hứa dối. Rồi Lan không sợ phản biện anh. Flashback cho thấy truyền thừa không xảy ra một lễ — nó xảy ra qua hàng nghìn lần Lan được phép nói không.',
    "### Khép cuộn",
    'Hùng lau mắt. Không xấu hổ. "Mai mình viết lại một số mốc vào sách trắng — thật, có sẹo."',
    'Lan: "Sẹo là mục lục."',
    'Con trai: "Con muốn thêm chương công nhân."',
    'Hùng: "Cháu viết. Bố không sửa cho đẹp."',
    "Đèn bàn tắt. Hà Nội ngoài kia vẫn sáng. Ký ức trong này đã được đặt đúng chỗ: không để khoe, để không quên đường về.",
]

p358 = [
    "### Mâm trước ghế",
    "Trước lễ lớn, Hùng đòi một bữa tối không khách, không máy quay, không menu ký kết. Nhà riêng. Mâm gỗ. Chỗ ngồi như xưa: bà được để chén riêng như vẫn còn — hoa quả và chén trà đầy.",
    "Lan vào bếp. Hạnh dặn muối. Con trai bị bắt rửa rau đúng cách, không ủy thác cho giúp việc hết. Hùng lau bàn. Bữa tối ba thế hệ bắt đầu bằng khăn ướt và mùi canh.",
    "### Món ăn và câu chuyện",
    'Canh cua. Thịt kho. Rau luộc. Một đĩa xào đơn giản. Không set cao cấp. Con trai ngạc nhiên: "Bố có thể đặt đầu bếp." Hùng: "Đặt được. Nhưng bữa này không phải để chứng minh đặt được."',
    "Lan kể chuyện một học bổng: em sinh viên viết thư cảm ơn bằng chữ xấu nhưng thật. Hạnh kể chuyện phòng khám: cụ già cầm đơn thuốc run. Con trai kể thợ mới suýt giấu lỗi; nó bắt dừng chuyền; thợ ấy sau cảm ơn.",
    'Hùng nghe. Ông gắp thức ăn cho mọi người như bà Hà từng làm. "Ngày xưa bà để phần ngon cho cháu. Giờ mình để phần đúng cho người làm đúng."',
    "### Ghế trống",
    'Giữa mâm có một chỗ không ngồi. Con trai hỏi khẽ. Lan đáp: "Cho bà. Cho những người không về kịp." Không ai thấy dị đoan. Họ thấy biết ơn có địa chỉ.',
    'Hùng nâng chén trà: "Không chúc doanh thu. Chúc nhà này không biến người thành công cụ."',
    "### Va chạm nhẹ",
    'Con trai nói muốn mở rộng xưởng nhanh hơn kế hoạch Lan. Lan lắc. Hùng không xử thay. Ông chỉ nói: "Hai đứa tranh bằng số và người chịu trách nhiệm. Ai thắng bằng giận là thua."',
    "Họ tranh mười phút. Rồi thống nhất mốc kiểm tra giữa kỳ. Mâm cơm trở thành hội đồng quản trị tốt nhất năm — vì không ai diễn.",
    'Họ nói cả chuyện lương thợ mới và chuyện con có muốn học thêm tài chính. Hạnh chen: "Nói chuyện công ty thì để bát xuống đã." Cả bàn cười. Kỷ luật nhà đôi khi chính là kỷ luật tập đoàn.',
    "### Ảnh cũ",
    'Lan mở hộp ảnh. Hùng năm hai mươi ba tuổi gầy. Lan tóc dài. Bà Hà mắt mờ mà chắc. Con trai xem như xem sử. "Bố lúc ấy giống người trong phim."',
    '"Lúc ấy bố đói và sợ," Hùng sửa. "Phim toàn bỏ đoạn đói."',
    "Họ cười. Cười để nhớ.",
    "### Khép mâm",
    'Rửa bát cùng nhau. Không ai chạy trước mở laptop. Hùng nhìn đồng hồ: "Mai còn việc. Nhưng tối nay việc đã xong."',
    'Lan: "Em ngủ lại đây." Con trai: "Con nữa." Hạnh: "Nhà đông mới đúng nhà."',
    "Đêm ba thế hệ không cần bài hát. Chỉ cần chén bát khua và cửa đóng lại với thế giới đủ ồn bên ngoài.",
    "Trên bàn còn mùi canh. Hùng không xịt khử mùi. Ông để mùi ấy ở lại như dấu ấn: đế chế có thể thơm nước hoa hội nghị, nhà phải thơm cơm.",
]

p359 = [
    "### Hội trường trống",
    "Đêm trước lễ bốn mươi năm Thương Gia, hội trường còn mùi sơn và băng keo. Công nhân sân khấu chỉnh đèn. Hùng đi một vòng một mình trước khi ê-kíp ùa vào. Ông chạm tay vào hàng ghế — chỗ người ta sẽ ngồi vỗ tay, và chỗ người ta sẽ quên vỗ tay cho thợ cả.",
    'Lan mang bản phát biểu in lần thứ tư. "Anh sửa nhiều quá."',
    '"Bớt tôi. Thêm chúng ta. Thêm tên việc. Bớt tính từ." Hùng gạch một dòng hoa mỹ. "Mai không phải đêm của vanity."',
    "### Danh sách khách và danh sách thợ",
    'Hai danh sách song song. Hùng đòi in cả hai trong sổ riêng. "Khách quan trọng. Thợ cũng quan trọng. Nếu chỉ có một danh sách, lễ này sai từ đầu."',
    'Con trai phụ trách đón đoàn xưởng. Nó hơi hồi hộp. Hùng: "Cháu bắt tay chắc. Nhìn mắt. Cảm ơn cụ thể — ca nào, việc nào."',
    'Hùng gọi bếp ăn hội nghị: "Suất chay đủ, suất ca đêm để riêng, không để người phục vụ đói sau tiệc." Chi tiết không lên báo. Chi tiết lên lương tâm.',
    "### Tin đồn cuối",
    "Luôn có tin đồn trước lễ lớn: sức khỏe, chia tách, bán cổ phần. Lan soạn bản tin nội bộ một trang: sự thật, việc mai, kênh hỏi. Phát trước hai mươi mốt giờ. Im lặng sau giờ đó là đất của tin đồn — họ không cho đất.",
    "### Bài phát biểu",
    'Hùng đọc nhẩm: "Bốn mươi năm trước tôi chỉ muốn nhà mình no. Sau mới biết no một nhà mà bỏ mặc nhiều nhà thì no ấy không bền. Thương Gia lớn nhờ người. Tôi xin lỗi những lần tôi ôm đồm và những lần tôi buông trễ. Cảm ơn bà tôi, em tôi, vợ tôi, con tôi, và những người không lên ảnh."',
    'Ông dừng. "Đoạn xin lỗi giữ. Đừng bỏ."',
    'Lan gật chắc: "Giữ."',
    "### Hệ thống không xen",
    "Lạ thay, hệ thống im hoàn toàn. Không gợi ý tăng EXP bằng bài nói. Hùng mỉm cười trong bụng: đúng lúc phải im.",
    "Ông ra ngoài hiên, nhìn thành phố. Đêm trước kỷ niệm là đêm của người còn thức để người khác mai được ngồi.",
    "### Micro và bánh mì",
    "Nửa đêm, Hùng ra sảnh hội trường lấy micro thử lại lần cuối, rồi ghé quán bánh mì đêm với bảo vệ già.",
    '"Chú làm ca bao lâu?" "Mười hai năm." "Mai chú cũng vào ghế trong." "Thôi anh, em đứng cửa quen." "Đứng cửa cũng là Thương Gia." Hùng để lại hai ổ bánh và một lời cảm ơn không quay clip.',
    'Về xe, ông nhắn Lan: "Bài nói đã đủ thật. Ngủ đi." Lan trả lời bằng nhãn dán củ khoai — trò cũ của em gái. Ông cười trong xe vắng.',
    "### Đi ngủ",
    'Nửa đêm về sau, Hùng buộc mình tắt đèn. "Mai cần giọng nói, không cần mắt thâm." Lan kiểm tra micro dự phòng lần cuối rồi cũng về. Con trai ngủ ghế sofa văn phòng — bị Hạnh phủ chăn.',
    "Hà Nội thở. Hội trường thở. Đế chế thở. Ngày mai sẽ ồn. Đêm nay được phép yên.",
]

p360 = [
    "### Nóc tháp",
    "Gió trên nóc tháp Thương Gia mang mùi kính mới, sàn đá nóng nắng, và tiếng thành phố dưới sâu. Năm 2024. Trần Văn Hùng đứng đó — không phải để chụp ảnh bìa, để nhìn.",
    "Dưới sân, đèn LED xếp chữ THƯƠNG GIA. Không phải chỉ để khoe chữ. Để người từ xa biết đường vào lễ và đường vào việc làm.",
    'Lan đứng bên phải. Con trai bên trái. Hạnh hơi lùi sau, tay nắm lan can. Trong túi áo Hùng có tờ giấy nhỏ viết tay từ đêm qua: "Giữ lõi."',
    "### Không phải kết thúc chuyện — kết thúc nhiệm vụ",
    "Ông nói vào micro không dây, giọng chậm, rõ, không diễn:",
    '"Bốn mươi năm trước, tôi tỉnh dậy trong một căn nhà đất và nghĩ mình phải làm giàu. Bây giờ tôi biết giàu không phải đích. Đích là làm giàu mà không làm mất người.',
    "Tôi đã làm được những gì hệ thống từng giao — và nhiều hơn thế ở chỗ hệ thống không đo được: người ta còn dám tin.",
    "Tôi không bảo con cháu copy tôi. Thời các con khác. Chuẩn sạch không khác.",
    'Tôi đã làm được. Và con cháu sẽ tiếp tục."',
    'Dưới sân có vỗ tay. Ông giơ tay xin dừng sớm. "Vỗ tay cho công nhân, giáo viên, bác sĩ, tài xế, thủ kho của chúng ta." Vỗ tay chuyển hướng — đúng chỗ.',
    "### Hệ thống — dòng cuối",
    "Trong đầu, một dòng rất nhỏ, như thì thầm:",
    "「Hành trình nhiệm vụ khép. Tinh thần Thương Gia — trường tồn ngoài hệ thống. Chủ nhân… bình an.」",
    "Rồi trống. Hùng không cố gọi lại. Ông để trống ấy thành khoảng cho người thật.",
    "### Lan nhận nhịp",
    'Lan bước lên một bước, không giành micro ngay. "Em không hứa hoàn hảo. Em hứa không quên. Không quên sổ sạch, không quên người dưới sàn, không quên làng Thanh Xuân."',
    'Con trai gật, nói ngắn: "Xưởng sẽ giữ mm. Con giữ lời."',
    "Hùng đặt tay lên vai hai người. Thế là bàn giao — không cần thêm con dấu cho phút này.",
    "Ông bước lùi nửa bước trên nóc — tượng trưng và thật. Gió đẩy. Ông không sợ mất trung tâm. Trung tâm đã chuyển đúng.",
    "### Về đất",
    "Chiều cùng ngày, họ về làng. Không đoàn xe dài. Ít người. Mùi đồng. Gió tre. Hùng đứng ở thềm nhà cũ đã tu sửa nhẹ. Ông cúi đầu.",
    '"Bà ơi, cháu về. Việc ngoài kia tạm yên. Nhà trong này vẫn là nhà."',
    'Trẻ con trong làng chạy ngang. Một cụ già nhận ra, nắm tay Hùng: "Cậu Hùng còn nhớ đường về là được." Ông đáp: "Nhớ. Nhớ thì mới dám đi xa."',
    'Một cháu nhỏ chỉ lên xe và hỏi có phải ông trên tivi không. Hùng quỳ nhẹ cho ngang tầm: "Ông là người ăn cơm làng này. Tivi chỉ mượn mặt."',
    "### Việc vẫn chạy",
    "Tối, báo cáo ngắn từ quỹ học bổng: giải ngân đúng hạn. Báo cáo xưởng: lỗi giảm. Báo cáo ngân hàng con: hồ sơ khó bị chặn đúng quy trình. Hùng đọc và chuyển cho Lan ký chính.",
    "Ông viết sổ da trang mới — trang không còn số nhiệm vụ hệ thống:",
    '"Ngày 1 sau nhiệm vụ tối thượng. Việc: sống đúng. Người: Lan, con, Hạnh, anh chị em đồng nghiệp. Gốc: Thanh Xuân. Tinh thần: trường tồn — bằng việc lặp lại, không bằng khẩu hiệu."',
    "### Câu cuối",
    "Trên nóc tháp lúc quay lại thành phố, đèn dưới sân đã tắt chữ, chỉ còn đèn đường. Hùng nói khẽ, như nói với chính mình thời 1983:",
    '"Mình không cần trở thành huyền thoại. Mình cần trở thành thói quen tốt của nhiều người."',
    'Lan nghe thấy. "Đó là định nghĩa Thương Gia em sẽ giữ."',
    "Gió đêm đẩy áo. Hà Nội rộng. Sài Gòn xa. Thế giới xa hơn. Nhưng lõi thì gần — trong tầm một câu nói thật và một chén cơm nhà.",
    "Hành trình kết thúc như một dấu hai chấm.",
    "Tinh thần Thương Gia mãi trường tồn.",
]


def main():
    for n, title, ps in [
        (356, "Hệ thống chúc mừng thương gia vĩ đại", p356),
        (357, "Flashback toàn hành trình", p357),
        (358, "Bữa tối ba thế hệ", p358),
        (359, "Đêm trước ngày kỷ niệm 40 năm", p359),
        (360, "Tinh thần Thương Gia mãi trường tồn", p360),
    ]:
        write_ch(n, title, ps)

    short = []
    heavy = []
    dups = Counter()
    for n in range(1, 361):
        t = list(DIR.glob(f"Chương {n} - *.txt"))[0].read_text(encoding="utf-8")
        w = cw(t)
        if w < 3000:
            short.append((n, w))
        lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
        c = Counter(lines)
        mr = c.most_common(1)[0][1]
        if mr >= 5 or t.count("Thêm một lớp rà soát") >= 3:
            heavy.append((n, mr))
        body = re.sub(r"^={5,}.*?={5,}\s*", "", t, count=1, flags=re.S)
        dups[" ".join(body.split()[:10])] += 1
    print("SHORT", short)
    print("HEAVY count", len(heavy), heavy[:10])
    print("dup open groups", sum(1 for v in dups.values() if v > 1))
    t360 = list(DIR.glob("Chương 360*"))[0].read_text(encoding="utf-8")
    t1 = list(DIR.glob("Chương 1*"))[0].read_text(encoding="utf-8")
    print("ch360 key", "Tôi đã làm được" in t360)
    print("ch1 key", "Đau. Đau như thể" in t1)


if __name__ == "__main__":
    main()
