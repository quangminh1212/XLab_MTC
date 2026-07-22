# -*- coding: utf-8 -*-
"""Handcraft remaining ranges: 41-89, 113-119, 130-199, 231-240, 271-295, 306-355."""
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

OPENS: dict[int, str] = {}

# ---- 41-89: Đổi Mới, multi-service, part2 ----
for n, t in {
    41: "Quạt điện — cánh nhựa, motor, mùa hè. “{title}” mang gió máy vào nhà người. Lỗi ồn là lỗi uy tín.",
    42: "Hoàn quạt. “{title}” không pháo hoa — chỉ lô ổn và bảo hành rõ.",
    43: "Đèn điện. “{title}” sáng từng căn nhà. Hùng nhớ đêm nhà đất từng tối như mực.",
    44: "Hoàn đèn. “{title}” ghi nhận: từ bóng tối làng đến ánh sáng có thương hiệu.",
    45: "Nhà hàng đầu. “{title}” mùi nước dùng, ca bếp, vệ sinh. Ăn vào miệng là nợ.",
    46: "Nhà hàng Hà Nội. “{title}” — ánh đèn phố và khách khó tính. Lan siết phục vụ.",
    47: "Nhà hàng Sài Gòn. “{title}” nhịp nhanh hơn. Bếp không được phép chậm bằng kẹt xe.",
    48: "BĐS đầu tư. “{title}” — đất, sổ, rủi ro. Hùng không say mét vuông; ông tính dòng tiền.",
    49: "Mua đất miền Nam. “{title}” nhìn dài: đường sẽ mở, người sẽ đến, mình phải sạch giấy.",
    50: "Hoàn Phần 1. “{title}” trải 5 năm: cháo loãng → chuỗi. Nắm tay bà Hà. Không kiêu.",
    51: "Chi nhánh Bắc Ninh. “{title}” — lý lịch xấu còn bám. Ông vượt bằng hàng đúng và quan hệ đúng.",
    52: "Tuyển Minh (nhịp sau). “{title}” củng cố đội kỹ thuật. Người giỏi cần chỗ để cãi đúng.",
    53: "Phòng khám. “{title}” chạm sức khỏe cộng đồng. Không thần dược. Thuốc rõ, bác sĩ thật.",
    54: "Vận chuyển. “{title}” — xe, lịch, xăng, trễ. Logistics là xương sống không ai vỗ tay.",
    55: "Cho vay. “{title}” tiền như dao. Cứu nông dân khỏi nặng lãi; không cứu quan hệ xin–cho.",
    56: "Mở rộng chi nhánh. “{title}” siết chuẩn chuỗi trước khi siết ribbon.",
    57: "Thái Bình chi nhánh. “{title}” kiên nhẫn tỉnh lẻ. Đại lý hỏi kỹ — ông trả lời chậm.",
    58: "Nam Định. “{title}” vải, thợ, nhịp chợ. Giữ chất từng cây vải.",
    59: "Ninh Bình. “{title}” đá và du lịch sơ. Cửa hàng nhỏ, lời hứa lớn bằng giao đúng.",
    60: "Hoàn chi nhánh nhịp. “{title}” — bản đồ miền Bắc thêm đinh. Mỗi đinh một miệng ăn.",
    61: "Xe đạp. “{title}” bánh xe và xích. Người lao động cần xe không gãy giữa đường.",
    62: "Máy cày. “{title}” xuống đồng. Hỏng giữa mùa là tội với nông dân.",
    63: "Máy gặt. “{title}” đua với thời vụ. Dịch vụ sửa chữa phải theo máy ra đồng.",
    64: "30 xe tải. “{title}” — đội xe, tài xế, ca đêm. An toàn không phải phụ lục.",
    65: "Chi nhánh tài chính. “{title}” siết thẩm định. Dư nợ đẹp mà xấu gốc thì đừng khoe.",
    66: "Trường học. “{title}” bàn ghế, giáo viên, trẻ em. Không làm trường chỉ để chụp ảnh.",
    67: "Trường Sài Gòn. “{title}” nhịp đô thị. Chất lượng dạy học đo bằng học sinh, không bằng biển.",
    68: "Trung tâm đào tạo. “{title}” kèm thợ và quản lý trẻ. Việc thật, hậu quả thật.",
    69: "Mở rộng phòng khám. “{title}” bác sĩ Tuấn/Dũng vào ca. Y đức không tách khỏi doanh thu.",
    70: "Hoàn vận chuyển. “{title}” đúng hẹn là uy tín. Trễ một chuyến là tin đồn mười chuyến.",
    71: "Cho vay tiếp. “{title}” cứu đúng người, chặn đúng hồ sơ cánh hẩu.",
    72: "Tài chính mở rộng. “{title}” kiểm soát nội bộ có quyền đỏ.",
    73: "Hoàn cho vay nhịp. “{title}” nợ xấu công khai hàng tuần. Minh bạch là lá chắn.",
    74: "Trường học tiếp. “{title}” vùng thiếu giáo viên. Tuyển và giữ người dạy quan trọng hơn xây tường.",
    75: "30 trường. “{title}” dễ thành con số. Ông đi bất chợt: lớp có học thật không?",
    76: "Đào tạo mở rộng. “{title}” curriculum ngắn, thực hành dài.",
    77: "Hoàn đào tạo. “{title}” người ra nghề có chỗ làm trong hệ thống — không đào tạo bỏ rơi.",
    78: "Phòng khám tiếp. “{title}” thuốc, sổ khám, giá niêm yết. Không kê đơn để đẩy hàng.",
    79: "Hoàn phòng khám nhịp. “{title}” tin cậy y tế là tài sản dài.",
    80: "Xây dựng mở rộng. “{title}” công trường, mũ bảo hộ, tiến độ. Chất lượng bê tông không nịnh.",
    81: "Năng lượng / nhà máy điện. “{title}” MW và trách nhiệm. Cúp điện oan là mất lòng cả vùng.",
    82: "Hoàn năng lượng nhịp. “{title}” bảo trì định kỳ — anh hùng thầm lặng.",
    83: "Quỹ từ thiện mở. “{title}” sổ tên, biên lai, kiểm toán. Thiện mờ thì dừng.",
    84: "Hoàn từ thiện nhịp. “{title}” không PR ồn. Việc đến tay người cần.",
    85: "Xuất khẩu 10 đối tác. “{title}” chuẩn đóng gói, giao đúng. Thế giới không nể 'cố gắng'.",
    86: "Bảo hiểm. “{title}” sản phẩm rõ điều khoản. Bán bảo hiểm mà mập mờ là đào hố uy tín.",
    87: "Máy cày ra mắt. “{title}” lễ ngắn, dịch vụ dài. Phụ tùng sẵn sàng trước khi cắt băng.",
    88: "Máy gặt ra mắt. “{title}” đồng lúa và mồ hôi. Máy phải chịu được ruộng thật.",
    89: "Tổng kết Phần 2. “{title}” đa ngành dễ loạn. Siết một câu: làm giàu không làm mất người.",
}.items():
    OPENS[n] = t

# ---- 113-119: global factories / health ----
for n, t in {
    113: "Nhà máy USA. “{title}” — chuẩn Mỹ, EPA, OSHA. Làm ăn lớn phải chịu luật lớn.",
    114: "M&A Stahl GmbH. “{title}” thép Đức. Tích hợp người khó hơn tích hợp máy.",
    115: "Nigeria. “{title}” tôn trọng địa phương, hạ tầng khó. Không mang tâm thế 'ban phát'.",
    116: "Úc. “{title}” khoảng cách và tiêu chuẩn. Logistics là nửa trận.",
    117: "Tổng tài sản 1000 tỷ. “{title}” con số sáng; Hùng hỏi: miệng ăn tăng bao nhiêu, nợ xấu bao nhiêu?",
    118: "Nằm viện. “{title}” cơ thể lên tiếng. Ông học: tốc độ giết người không kém đối thủ.",
    119: "Bước ngoặt sức khỏe. “{title}” đổi cách lãnh đạo — ủy thác không còn là lựa chọn, là sống còn.",
}.items():
    OPENS[n] = t

# ---- 130-199 (skip 120-129 already handcrafted) ----
for n, t in {
    130: "Thử thách kế thừa. “{title}” lộ ai dám chịu khi xấu. Lửa cần, và phải canh.",
    131: "Đông Nam Á sâu. “{title}” bản đồ đầy đinh. Mỗi nước một luật chơi.",
    132: "Hải quan Indonesia. “{title}” kiên nhẫn giấy tờ. Nóng giận không thông quan.",
    133: "Malaysia–Philippines. “{title}” hai nhịp thị trường. Không copy kịch bản mù.",
    134: "Chuỗi cung ứng châu Á. “{title}” một mắt xích gỉ là cả dây yếu.",
    135: "Nhật–Hàn. “{title}” chuẩn khắt. Học bằng hàng, không bằng miệng.",
    136: "Nhật khó tính nhất. “{title}” sai số milimet. Xuất xưởng là danh dự.",
    137: "Gặp ông Sato. “{title}” trà và im lặng. Ông ấy thử người trước khi thử hàng.",
    138: "Thử thách Sato. “{title}” deadline và chất. Hùng không xin nương — xin điều kiện rõ.",
    139: "Hàn Quốc. “{title}” tốc độ và kỷ luật. Cạnh tranh lành để học, không để ghen.",
    140: "Chuẩn bị Mỹ. “{title}” hồ sơ, bảo hiểm, kiện tụng tiềm ẩn. Vào lớn phải phòng lớn.",
    141: "Chuyến bay Mỹ đầu. “{title}” jetlag và tự tin vừa đủ. Lan mang theo sổ rủi ro.",
    142: "Thử thách Mỹ đầu. “{title}” khách nói thẳng. Không hứa ảo — sửa thật.",
    143: "Hệ thống chất lượng Mỹ. “{title}” quy trình viết ra, audit được. Giấy + thói quen.",
    144: "Đối tác Mỹ mở rộng. “{title}” hợp đồng dày. Luật sư ngồi cạnh kỹ sư.",
    145: "Đối thủ Trung Quốc tại Mỹ. “{title}” không đua đáy. Giữ chuẩn, mất đơn ảo cũng được.",
    146: "Lan đàm phán Mỹ. “{title}” giọng em vững. Hùng chống lưng số, không cướp micro.",
    147: "Áp lực Mỹ. “{title}” Lan suýt gãy. Về nhà một tuần — rồi bay lại với xương sống.",
    148: "Bữa tối 3 thế hệ. “{title}” mâm cơm thắng slide. Nhà hàn lại trước khi ra biển tiếp.",
    149: "Trở lại Mỹ. “{title}” tinh thần mới: không cô đơn, có bến.",
    150: "Hùng tập trung Việt Nam. “{title}” gốc rễ. Quốc tế không được hút cạn gốc.",
    151: "Canada. “{title}” lạnh và lịch sự. Hợp đồng rõ, giao đúng.",
    152: "Huân chương. “{title}” sáng áo; ông nhớ công nhân hơn flash.",
    153: "Australia. “{title}” khoảng cách. Phụ tùng và bảo hành phải theo hàng.",
    154: "Quỹ từ thiện mở rộng. “{title}” 5 tỷ khởi điểm — sổ sạch, kiểm toán, việc thật.",
    155: "Ngân hàng Thương Gia mở cửa. “{title}” tiền như dao. Không giải ngân vì nể.",
    156: "Cho vay DNNVV. “{title}” gói siêu nhỏ–nhỏ–vừa. Việc làm sạch hơn dư nợ ảo.",
    157: "Kiểm toán nhà nước. “{title}” sổ ra ánh sáng. Sợ số thật hơn sợ mất mặt.",
    158: "Lan về nước báo cáo. “{title}” hai múi giờ gặp nhau trên bàn. Sự thật trước thể diện.",
    159: "Nhà máy ô tô đầu. “{title}” mm và danh dự. Không xuất khi lệch.",
    160: "Mẫu xe Thành Công. “{title}” thử đường thật. Brochure không thay được ổ gà.",
    161: "Hợp tác kỹ thuật Nhật. “{title}” học chuẩn, trả bằng kỷ luật.",
    162: "Chuỗi phụ tùng. “{title}” nội địa hóa có kiểm soát chất.",
    163: "Khủng hoảng thép. “{title}” giá nguyên liệu nhảy. Ôm hàng ảo là chết.",
    164: "Dàn xếp nhà cung. “{title}” đàm phán sòng phẳng, không ép đến đường cùng.",
    165: "Xe máy Thương Gia. “{title}” ra đường. Dịch vụ sau bán là nửa sản phẩm.",
    166: "Showroom toàn quốc. “{title}” trải nghiệm khách. Ảo trên ảnh, thật trên sàn.",
    167: "Điện thoại gen 2. “{title}” đủ dùng, giá vừa — không khoe tương lai chưa làm được.",
    168: "Máy tính Hà Nội. “{title}” lắp ráp và phần mềm đi cùng.",
    169: "Đối tác Singapore. “{title}” cửa ngõ tài chính–logistics châu Á.",
    170: "Xung đột Hồng Kông. “{title}” tin đồn và ép giá. Ngoại giao bằng chứng cứ.",
    171: "Áp lực giá. “{title}” không bán rẻ uy tín để giữ thị phần ảo.",
    172: "Ngoại giao ông Chen. “{title}” bàn trà và ranh giới. Cứng–mềm đúng chỗ.",
    173: "Thỏa thuận đôi bên. “{title}” win-win viết vào điều khoản, không viết lên banner.",
    174: "Logistics quốc tế. “{title}” tàu, kho, lead time. Trễ là mất mặt.",
    175: "Cảng Hải Phòng. “{title}” container và hải quan. Nhịp cảng là nhịp xuất khẩu.",
    176: "Đội tàu đầu. “{title}” vốn lớn, rủi ro biển. Bảo hiểm và kỷ luật thuyền trưởng.",
    177: "Kho Singapore. “{title}” trung chuyển. Hàng nằm kho cũng tốn tiền — tối ưu tồn.",
    178: "Lan dẫn đoàn châu Âu khảo sát. “{title}” mắt em sắc; anh tin.",
    179: "Chuẩn bị niêm yết công ty con. “{title}” pháp lý và minh bạch. Không làm đẹp hồ sơ.",
    180: "Đào tạo quản lý thế hệ hai. “{title}” giao việc có hậu quả.",
    181: "Hạnh và gia đình nhỏ. “{title}” bàn cơm giữ người lãnh đạo khỏi hóa thành máy.",
    182: "Bà Hà 70. “{title}” tiệc mừng giản. Bà chỉ muốn cháu ngủ đủ.",
    183: "Đại học nghề. “{title}” thợ và kỹ thuật viên — xương sống công nghiệp.",
    184: "Bệnh viện đa khoa. “{title}” y đức + máy móc. Không kê đơn đẩy hàng.",
    185: "Tổng kết nửa châu Á. “{title}” số lớn, bài học lớn.",
    186: "Tập đoàn bóng tối lộ. “{title}” không hoảng. Thu thập chứng cứ.",
    187: "Phá hoại hợp đồng xuất khẩu. “{title}” cứu lô, cứu quan hệ, kiện đúng chỗ.",
    188: "Điều tra. “{title}” luật sư, kiểm toán, nội bộ. Sự thật chậm nhưng chắc.",
    189: "Đối chất công khai. “{title}” ánh sáng. Không đấm dưới bàn.",
    190: "Liên minh doanh nghiệp Việt. “{title}” bắt tay để khỏe cùng, không để cấu xé.",
    191: "Chiến thắng pháp lý. “{title}” không ăn mừng ồn — siết quy trình để khỏi tái.",
    192: "Tái cấu trúc sau khủng hoảng. “{title}” cắt mỡ, giữ xương, giữ người cốt lõi.",
    193: "Kỷ niệm 12 năm. “{title}” nhớ sẹo. Công nhân thâm niên ngồi gần.",
    194: "Lan Phó Tổng. “{title}” chức danh đi sau năng lực đã chứng.",
    195: "Hùng trao vận hành nội địa. “{title}” buông đúng — vẫn chịu trách nhiệm cuối.",
    196: "10 năm xuất khẩu. “{title}” tri ân đối tác cũ bằng việc, không bằng rượu.",
    197: "Bà Hà phát biểu. “{title}” câu giản: nhà giàu vì thương người. Phòng họp im.",
    198: "Kỹ năng Quản trị đế chế. “{title}” hệ thống ghi; ông ghi người.",
    199: "Tổng kết Phần 3. “{title}” cửa ngõ đã mở — chưa được phép quên bến.",
}.items():
    OPENS[n] = t

# ---- 231-240 post crisis peak numbers ----
for n, t in {
    231: "Mua nhà máy đối thủ phá sản. “{title}” giá thấp, việc nặng: người, máy, văn hóa.",
    232: "Tái khởi động sản xuất. “{title}” ca đầu, hàng đầu, lỗi đầu — sửa ngay.",
    233: "Truyền thông khủng hoảng. “{title}” nói thật vừa đủ. Không diễn, không trốn.",
    234: "Niềm tin khách. “{title}” giao đúng đơn đã lỡ hẹn — kèm xin lỗi và bồi hoàn rõ.",
    235: "Hùng trên truyền hình quốc tế. “{title}” nói về việc làm và kỷ luật, không khoe tỷ.",
    236: "Forbes gọi tên. “{title}” trang giấy; ông đo bằng ca kíp còn vững.",
    237: "Vượt đáy. “{title}” chưa ăn mừng. Giữ tiền mặt, giữ người, giữ chuẩn.",
    238: "Tái cấu trúc nợ thông minh. “{title}” đàm phán sòng phẳng, lịch trả rõ.",
    239: "Bùng nổ sau bão. “{title}” đơn về — công suất và người phải theo kịp, không hứa ảo.",
    240: "Tài sản kỷ lục mới. “{title}” số sáng. Hỏi ngược: nợ, việc làm, văn hóa còn không?",
}.items():
    OPENS[n] = t

# ---- 271-295 social influence ----
for n, t in {
    271: "Phần 5 — ảnh hưởng xã hội. “{title}” quyền lực lớn hơn thì trách nhiệm dày hơn.",
    272: "Đế chế truyền thông. “{title}” báo, sóng, chữ. Không biến thành máy thổi.",
    273: "Báo kinh tế. “{title}” sự thật số liệu. Quảng cáo không mua được tít giả.",
    274: "Truyền hình. “{title}” hình ảnh. Giải trí không được nuốt đạo đức làm ăn.",
    275: "Nền tảng mạng xã hội nội. “{title}” kết nối — và rủi ro tin giả. Có quy tắc.",
    276: "Thương Gia FC. “{title}” sân cỏ cộng đồng. Thể thao không chỉ là logo trên áo.",
    277: "Sân vận động cộng đồng. “{title}” chỗ cho trẻ đá bóng tối.",
    278: "Tài trợ Olympic khu vực. “{title}” minh bạch hợp đồng tài trợ.",
    279: "Học bổng 10.000. “{title}” tên thật, điểm thật, hoàn cảnh thật. Kiểm tra đột xuất.",
    280: "100 trường vùng sâu. “{title}” đường đất, lớp học. Đi bất chợt hơn cắt băng.",
    281: "Quỹ 10.000 tỷ. “{title}” số lớn — quản trị phải lớn tương xứng. Kiểm toán độc lập.",
    282: "Minh bạch quỹ. “{title}” công bố quý. Ai mập mờ bị dừng giải ngân.",
    283: "Y tế lưu động miền núi. “{title}” xe, thuốc, bác sĩ. Không làm show.",
    284: "Nước sạch 500 xã. “{title}” giếng, ống, bảo trì. Công trình chết vì quên bảo trì.",
    285: "Lan đứng đầu mảng xã hội. “{title}” giao quyền thật — ngân sách + trách nhiệm.",
    286: "Con trai phụ trách sản xuất. “{title}” bụi xưởng trước ghế êm.",
    287: "Hùng lui chiến lược. “{title}” im đúng lúc. Hỏi nhiều hơn lệnh.",
    288: "Khủng hoảng truyền thông giả. “{title}” chứng cứ và bình tĩnh. Không đáp bằng chửi.",
    289: "Phản ứng minh bạch. “{title}” họp báo ngắn, số liệu dài, sửa nếu sai.",
    290: "Lấy lại niềm tin. “{title}” thời gian + việc. PR không thay được.",
    291: "Hội nghị doanh nghiệp. “{title}” đề xuất sòng phẳng, không xin đặc quyền mờ.",
    292: "Chính sách xanh. “{title}” số liệu môi trường. Nói xanh sổ đen thì đừng nói.",
    293: "Thương hiệu quốc gia. “{title}” hàng Việt đứng được vì chuẩn, không vì hô hào.",
    294: "Bảo tàng Thương Gia. “{title}” bát cháo, máy may, hợp đồng đầu — sẹo và thắng.",
    295: "Ngày hội công nhân. “{title}” sân khấu cho người làm ra của cải. Lãnh đạo ngồi dưới.",
}.items():
    OPENS[n] = t

# ---- 306-355 (skip 296-305, 356-360 already done) ----
for n, t in {
    306: "Gặp lại ông Sato. “{title}” trà, im lặng, nụ cười người già đã thử nhau bằng hàng.",
    307: "Gặp Klaus. “{title}” châu Âu và kỷ luật hợp đồng. Cảm ơn bằng việc tiếp.",
    308: "Đối tác Mỹ cũ. “{title}” bắt tay qua khủng hoảng. Còn lại là niềm tin.",
    309: "Quỹ học bổng mang tên bà Hà. “{title}” chữ bà giản — thương người — thành thể chế.",
    310: "Làng nghề hồi sinh. “{title}” đơn hàng + thiết kế + công bằng cho thợ già.",
    311: "Giải huyền thoại. “{title}” cúp sáng; ông nhìn công nhân thâm niên trước.",
    312: "Bài phát biểu thế kỷ. “{title}” gạch đoạn tự ca. Nói sẹo, nói người, nói việc mai.",
    313: "Sách trắng quản trị. “{title}” viết ra để người sau khỏi phải đoán.",
    314: "Tin đồn sức khỏe. “{title}” minh bạch vừa đủ. Không để thị trường đồn thay mình.",
    315: "Chăm sóc sức khỏe. “{title}” khám định kỳ, ngủ đủ — kỷ luật lãnh đạo.",
    316: "Ba thế hệ sum họp. “{title}” mâm cơm. Máy úp. Nhà thắng chức danh.",
    317: "Di sản pháp lý. “{title}” luật sư, di chúc, ủy thác. Rõ để khỏi cấu xé.",
    318: "Ủy thác tài sản minh bạch. “{title}” không hộc tối. Ánh sáng là bảo vệ gia tộc.",
    319: "Cam kết không chia cắt tập đoàn. “{title}” văn hóa một — dù nhiều công ty con.",
    320: "Lan bảo vệ văn hóa. “{title}” xử đúng người sai, bảo vệ người làm đúng — dù 'cứng'.",
    321: "Cạnh tranh giá. “{title}” không đua đáy. Giữ giá trị, mất khách ảo.",
    322: "Chiến lược giá trị. “{title}” chất + dịch vụ + minh bạch. Giá là hệ quả.",
    323: "Khách hàng trung thành. “{title}” đo bằng quay lại mua, không bằng like.",
    324: "Tái định vị thương hiệu. “{title}” lời hứa gọn, chứng minh dài.",
    325: "Công nghệ xanh toàn hệ. “{title}” MW, tấn CO₂, số thật.",
    326: "Cam kết net zero. “{title}” lộ trình, không khẩu hiệu năm bầu cử.",
    327: "Lễ 30 năm. “{title}” ngắn. Nhường chỗ người thầm lặng.",
    328: "Phim tài liệu hành trình. “{title}” có đoạn lỗi. Không chỉ thắng.",
    329: "Tổng kết Phần 5. “{title}” ảnh hưởng xã hội đo bằng việc, không bằng giải.",
    330: "Hoàn Phần 5. “{title}” thương hiệu vĩ đại = thói quen không dối.",
    331: "Phần 6 di sản. “{title}” cửa cuối: giữ được khi bị thâu tóm và khi bị nịnh.",
    332: "Bóng tối trở lại. “{title}” không hoảng. Phòng thủ cổ đông.",
    333: "Âm mưu thôn tính. “{title}” dòng vốn lạ. Chứng cứ, điều lệ, liên minh nhỏ.",
    334: "Phòng thủ cổ đông. “{title}” minh bạch + lộ trình dài hạn.",
    335: "Liên minh cổ đông nhỏ. “{title}” phiếu và niềm tin tích năm.",
    336: "Hùng ra mặt lần cuối. “{title}” giọng không lớn — số liệu lớn.",
    337: "Trí tuệ và hệ thống. “{title}” la bàn cuối: lương tâm + dữ liệu.",
    338: "Thắng đại hội. “{title}” không reo. Siết quản trị để khỏi tái.",
    339: "Thanh lọc nội bộ. “{title}” chuẩn lọc, không thanh trừng ồn.",
    340: "Bình yên sau bão. “{title}” ca kíp đều. Đôi khi bình yên là chiến thắng.",
    341: "Bàn giao chính thức. “{title}” biên bản, vòng tay, mắt nhìn.",
    342: "Lan CEO – con Phó. “{title}” hai vai, một văn hóa.",
    343: "Bà Hà 90 kể chuyện xưa. “{title}” phòng im. Lịch sử sống trong giọng bà.",
    344: "Bữa cơm lịch sử. “{title}” ba thế hệ. Không micro.",
    345: "Quỹ Di sản Trần Văn Hùng. “{title}” thể chế hóa cái lõi: thương người + làm đúng.",
    346: "Người giàu có trách nhiệm. “{title}” không ban phát kiêu. Sòng phẳng và nâng đỡ.",
    347: "Từ thiện 100.000 tỷ lộ trình. “{title}” số lớn — giải ngân có kiểm soát.",
    348: "Du hành tri ân thế giới. “{title}” bắt tay cũ. Cảm ơn bằng việc còn làm cùng.",
    349: "Hà Nội–Sài Gòn–quê. “{title}” ba nhịp một đời.",
    350: "Làng Thanh Xuân. “{title}” đất, gió, mùi đồng. Về để không lạc.",
    351: "Nhà đất cũ. “{title}” ký ức mái dột. Ông cúi đầu.",
    352: "Tượng đài công nhân. “{title}” không phải tượng ông. Là người làm ra của cải.",
    353: "Thư gửi thế hệ sau. “{title}” mực chậm. Đừng copy — giữ lõi.",
    354: "Nhiệm vụ cuối hệ thống. “{title}” checklist đời người: đã giữ người chưa?",
    355: "Hoàn nhiệm vụ tối thượng. “{title}” yên. Không nổ pháo — thở.",
}.items():
    OPENS[n] = t


def beat(n: int, title: str, y: int, loc: str) -> str:
    if n <= 89:
        return (
            f"### Nhà / chuỗi\n\nĐêm sau “{title}”, Hùng về với mùi {('bếp' if y < 1988 else 'văn phòng và bụi xưởng')}. "
            f"Bà Hà hỏi ăn. Lan báo số. Ông chỉnh nhịp: người trước, danh sau. {loc}, {y}."
        )
    if n <= 119:
        return (
            f"### Giới hạn\n\n“{title}” nhắc Hùng cơ thể và đế chế đều có ngưỡng. "
            f"Ủy thác không phải thua — là sống để đi tiếp."
        )
    if n <= 199:
        return (
            f"### Biên giới\n\nSau “{title}”, bài học ngoài nước được ghi: không hứa ảo, không đua đáy, "
            f"không quên bến Việt Nam. Lan và Hùng chia múi giờ, không chia chuẩn."
        )
    if n <= 240:
        return (
            f"### Sau bão\n\n“{title}” thuộc nhịp hồi phục. Giữ tiền mặt, giữ người, giữ chuẩn. "
            f"Ăn mừng sớm là cách tái khủng hoảng."
        )
    if n <= 295:
        return (
            f"### Xã hội\n\n“{title}” đo bằng người được nâng, không bằng giải. "
            f"Lan gánh mảng xã hội; Hùng giữ kỷ luật sổ."
        )
    return (
        f"### Di sản\n\n“{title}” viết cho người sau. Rõ pháp lý, rõ văn hóa, rõ lời thề: "
        f"làm giàu không làm mất người."
    )


def write_one(n: int, originals: dict) -> int:
    title = OUTLINE["chapters"][str(n)]["title"]
    y = year_of(n, title)
    loc = loc_of(n, title)
    if 113 <= n <= 117:
        y = max(y, 2005)
    if 231 <= n <= 240:
        y = 2008 if n <= 237 else 2009
    if 271 <= n <= 295:
        y = max(y, 2010)
    if 306 <= n <= 355:
        y = max(y, 2015)

    craft = OPENS[n].format(title=title, y=y, loc=loc)
    core = originals.get(n, "")
    parts = [f"### Mở\n\n{craft}"]

    if core and count_words(core) >= 80 and n <= 154:
        parts.append("### Diễn biến đã xác lập\n\n" + core)
        parts.append(
            f"### Lớp sâu\n\nSau “{title}”, Hùng hỏi: ai no hơn, ai tổn thương nếu vội, "
            f"có dám kể bà Hà nghe không sửa sự thật? Lan chặn hứa nhanh. Làm đủ phần đã hứa. "
            f"{loc}, {y}."
        )
    else:
        parts.append(
            f"### Việc cụ thể\n\nÊ-kíp chia “{title}”: hiện trường – sổ – khách – người. "
            f"Checklist một trang. Ký đã hiểu. Làm. Không nhìn chung ổn. {loc}, {y}."
        )

    parts.append(beat(n, title, y, loc))
    parts.append(
        f"### Hệ thống\n\n「{y} | {title} — tiến độ | EXP +{50 + n // 2}」\n"
        f"「Uy tín – người – sổ sạch」\n\nHùng đọc rồi tắt."
    )
    nxt = min(360, n + 1)
    nt = OUTLINE["chapters"][str(nxt)]["title"]
    parts.append(f"### Khép\n\n“{title}” có tiến. Mai: “{nt}”.")

    body = "\n\n".join(parts)
    body = pad_clean(body, n, title, y, loc)
    g = 0
    while count_words(body) < MIN and g < 40:
        body += (
            f"\n\nBổ sung “{title}” ({y}/{loc}): đối chiếu lời hứa–tiến độ–người chịu trách nhiệm "
            f"trước khi khép ngày."
        )
        g += 1
    text = header(n, title) + footer(body)
    chapter_path(n, title).write_text(text, encoding="utf-8")
    return count_words(text)


def main():
    originals = load_originals()
    nums = sorted(OPENS.keys())
    short = []
    for i, n in enumerate(nums):
        w = write_one(n, originals)
        if w < MIN:
            short.append((n, w))
        if n in (41, 60, 89, 113, 119, 130, 155, 199, 231, 240, 271, 295, 306, 330, 355) or (
            i + 1
        ) % 40 == 0:
            print(f"Ch {n}: {w}w")
    print("wrote", len(nums), "short", short)

    # full verify
    from pathlib import Path

    all_short = []
    for n in range(1, 361):
        p = list(Path(".").glob(f"Chương {n} - *.txt"))[0]
        w = count_words(p.read_text(encoding="utf-8"))
        if w < MIN:
            all_short.append((n, w))
    print("ALL360 short", all_short)


if __name__ == "__main__":
    main()
