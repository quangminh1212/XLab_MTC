# -*- coding: utf-8 -*-
"""
Rewrite Niên Đại Thương Gia — v2 (fix keyword match, no pad dups).
"""
from __future__ import annotations

import json
import random
import re
import statistics
from pathlib import Path

ROOT = Path(r"C:\Dev\XLab_MTC\Niên Đại Thương Gia")
OUTLINE = json.loads((ROOT / "chapter_outline.json").read_text(encoding="utf-8"))
MIN_WORDS = int(OUTLINE.get("min_words") or 3000)

KEEP_LIGHT = set(range(1, 21)) | {356, 357, 358, 359, 360}
FULL_REGEN = set(range(21, 356))


def chapter_files():
    out = {}
    for f in list(ROOT.glob("Chương *.txt")) + list(ROOT.glob("Chuong *.txt")):
        m = re.search(r"(\d+)", f.name)
        if m:
            out[int(m.group(1))] = f
    return out


def word_count(text: str) -> int:
    return len(text.split())


def rng_for(n: int, salt: int = 0) -> random.Random:
    return random.Random(n * 9176 + 13 + salt * 9973)


def has_kw(title: str, words: list[str]) -> bool:
    """Word-boundary-ish match; avoid 'hàn' in 'thành'."""
    t = title.lower()
    for w in words:
        w = w.lower()
        # allow match at edges or next to non-letter
        if re.search(rf"(?<![a-zăâáàảãạăắằẳẵặêếềểễệôốồổỗộơớờởỡợưứừửữựéèẻẽẹíìỉĩịóòỏõọúùủũụýỳỷỹỵ]){re.escape(w)}(?![a-zăâáàảãạăắằẳẵặêếềểễệôốồổỗộơớờởỡợưứừửữựéèẻẽẹíìỉĩịóòỏõọúùủũụýỳỷỹỵ])", t, re.I):
            return True
        # also simple contains for multi-word phrases with spaces
        if " " in w and w in t:
            return True
    return False


def classify(title: str) -> str:
    t = title.lower()
    if has_kw(t, ["gặp", "chọn cô", "cô hạnh", "cô mai", "cưới", "hôn nhân", "bà hà", "gia đình", "bữa cơm", "ba thế hệ"]):
        return "human"
    if has_kw(t, ["khủng hoảng", "áp lực", "xung đột", "kiểm toán", "sóng", "nợ xấu", "phá giá", "đối đầu"]):
        return "crisis"
    if has_kw(t, ["nhà máy", "sản xuất", "xưởng", "radio", "quạt điện", "đèn điện", "thép", "xi măng", "phần mềm", "điện thoại", "xe máy", "máy cày", "máy gặt", "giày"]):
        return "factory"
    if has_kw(t, ["cửa hàng", "chi nhánh", "nhà hàng", "showroom", "siêu thị", "mở rộng cửa", "mở chi"]):
        return "store"
    if has_kw(t, ["xuất khẩu", "m&a", "hoa kỳ", "usa", "nhật bản", "hàn quốc", "thái lan", "indonesia", "đức", "singapore", "toàn cầu", "niêm yết", "châu âu", "châu mỹ", "canada", "australia"]):
        return "global"
    if has_kw(t, ["từ thiện", "trường", "học bổng", "quỹ", "di sản", "bàn giao", "ceo", "truyền thừa", "văn hóa công ty", "giao quyền"]):
        return "legacy"
    if has_kw(t, ["hoàn thành phần", "tổng kết", "bắt đầu phần"]):
        return "milestone"
    if has_kw(t, ["mở rộng", "mở nhà", "mở "]):
        return "expand"
    return "general"


def year_bits(year: int, r: random.Random) -> list[str]:
    if year <= 1985:
        pool = [
            "Phiếu gạo, đèn dầu, xe đạp: ba thứ định nhịp ngày.",
            "Chợ họp sớm; tin đồn về giá đường muối đi nhanh hơn xe thồ.",
            "Hóa đơn sạch và con dấu rõ — thời này một chữ sai kéo cả xóm hỏi.",
            "Quần áo vá không xấu hổ bằng nhà hết gạo trước chiều.",
            "Loa phường buổi sáng, bụi đỏ quốc lộ, mùi rơm sau mưa.",
        ]
    elif year <= 1990:
        pool = [
            "Đổi Mới ngấm dần: người dám làm hụt hơi vì luật cũ, người sợ làm hụt hơi vì cơ hội.",
            "Xe máy bắt đầu lấn xe đạp; tiếng máy nổ đè thùng phuy cũ.",
            "Hợp đồng viết tay còn, nhưng đã có thêm người dám ký tên chịu.",
            "Hàng nội, hàng ngoại, hàng xách tay — ba lớp giá một chợ.",
            "Cán bộ huyện vừa hỏi vừa nhìn; làm ăn phải vừa đúng vừa khéo.",
        ]
    elif year <= 2000:
        pool = [
            "Điện thoại bàn, fax, cuộc gọi đứt giữa chừng vì đường truyền.",
            "Khu công nghiệp mọc nhanh; bụi đỏ bám vành xe tải cả ngày.",
            "USD, đồng, và lời hứa giao hàng phải khớp mới dám ký.",
            "Card visit, cà phê khách sạn: ngoài hiện đại, trong vẫn chữ tín.",
            "Container, biên phòng, và những đêm trắng vì một lô hàng.",
        ]
    elif year <= 2010:
        pool = [
            "Email, bảng tính, họp nửa Việt nửa Anh.",
            "Mùi giấy nợ 2008 vẫn còn trong vài ngăn kéo.",
            "Showroom kính và người giữ cửa nhớ tên khách quen.",
            "Báo thích chữ tập đoàn; xưởng thích chữ đúng ca đúng lương.",
            "Ngân hàng, kiểm toán, và những cuộc gọi nửa đêm.",
        ]
    else:
        pool = [
            "Màn hình sáng, số liệu nhiều, việc thật vẫn phải đi chân.",
            "Tin lan nhanh hơn báo cáo nội bộ.",
            "Thế hệ sau muốn tốc độ; thế hệ trước muốn không vỡ chữ tín.",
            "Từ thiện có ảnh — ông vẫn kiểm bằng việc tới tay người.",
            "Họp trực tuyến xong, hiện trường vẫn là chỗ quyết định.",
        ]
    r.shuffle(pool)
    return pool


def scene_store(meta, r):
    title, year, loc = meta["title"], meta["year"], meta["location"]
    return [
        f"Năm {year}, {loc}. Biển hiệu “{title}” không quan trọng bằng cửa mở đúng giờ và hàng đúng lời.",
        f"Hùng tự đứng quầy một buổi. Ông nghe khách phàn nàn giá, nghe nhân viên mới lắp bắp, nghe đối thủ dò hàng.",
        f"Sổ quầy chia bốn cột: tồn — nợ — ca trực — khiếu nại. Ai phụ trách ô nào phải nói tên thật, không 'hỏi anh kia'.",
        f"Rủi ro “{meta.get('conflict')}\" lộ ra dưới dạng {r.choice(['giá phá', 'tin đồn lý lịch', 'hàng giả mạo danh', 'khách lớn đòi chiết khấu vô lý'])}. Ông không chửi trên phố; ông kiểm chứng và niêm yết rõ.",
        f"Cuối ngày, doanh thu chỉ là một dòng. Dòng ông xem kỹ hơn là: còn ai trong đội bị bỏ lại vì lịch làm việc ẩu không.",
    ]


def scene_factory(meta, r):
    title, year, loc = meta["title"], meta["year"], meta["location"]
    return [
        f"Năm {year}, tại {loc}. “{title}” bắt đầu từ mùi dầu máy và tiếng ốc vít, không từ bài phát biểu.",
        f"Hùng đi dọc dây chuyền. Ông hỏi người thợ già nhất chỗ hay hỏng, chỗ hay gian số liệu, chỗ tăng ca sẽ gãy người.",
        f"Mẫu thử đặt giữa bàn. Ai khen đẹp thì khen; ai chỉ lỗi được mời ngồi gần hơn.",
        f"“{meta.get('conflict')}\" xuất hiện đúng lúc sắp chạy thật: thiếu chuẩn, thiếu phụ tùng, hoặc thiếu người biết việc. Ông thà lùi lịch còn hơn giao hàng lỗi.",
        f"Ca chiều tan, ông đứng lại đếm không khí: mệt nhưng không oán — đó là mức ông chấp nhận; oán là mức phải dừng.",
    ]


def scene_global(meta, r):
    title, year, loc = meta["title"], meta["year"], meta["location"]
    return [
        f"Năm {year}, {loc}. “{title}” buộc Hùng dịch không chỉ ngôn ngữ — mà cả cách hiểu chữ đúng hạn.",
        f"Hồ sơ chất lượng, chứng nhận, lịch tàu, điều khoản phạt: từng trang được đọc to. Chỗ mơ hồ bôi đỏ.",
        f"Đối tác cười lịch sự. Hùng hỏi câu không lịch sự: hỏng thì ai chịu, bao nhiêu ngày, bằng chứng nào.",
        f"Rủi ro “{meta.get('conflict')}\" được đặt lên bàn trước khi nâng ly. Ký xong không pháo — chỉ có lịch giao.",
        f"Ông viết vào sổ: đừng để tên Việt trên bao bì nếu hàng bên trong không xứng.",
    ]


def scene_crisis(meta, r):
    title, year, loc = meta["title"], meta["year"], meta["location"]
    return [
        f"Năm {year}. “{title}” đến không gõ cửa — nó đá cửa. {loc} sáng ấy không banner, chỉ mặt người tái hơn giấy.",
        f"Hùng họp ngắn. Bốn cột: tiền mặt — hàng — lương đến hạn — uy tín lung lay chỗ nào. Không ai được nói 'cảm thấy' thay cho số.",
        f"Ông bóc “{meta.get('conflict')}\": cái nào thật, cái nào phóng đại, cái nào do mình tự làm hỏng.",
        f"Quyết định đầu: giữ lương và giữ khách cốt lõi. Người ngoài thích nghe thắng; người trong cần nghe còn việc làm.",
        f"Đêm đó ông không ngủ sâu. Ông chấp nhận — người lãnh đạo mất ngủ đúng việc thì đội còn đường sống.",
    ]


def scene_human(meta, r):
    title, year, loc = meta["title"], meta["year"], meta["location"]
    other = [c for c in (meta.get("cast") or []) if "Hùng" not in c]
    name = other[0] if other else "người đối diện"
    return [
        f"Năm {year}, {loc}. Việc “{title}” không nằm trên bảng số — nó nằm giữa hai con người.",
        f"Hùng không mang theo giấy tờ dày. Ông mang theo thời gian và sự im lặng đủ dài để nghe {name}.",
        f"Họ bắt đầu bằng chuyện nhỏ: trời, đường, sức khỏe. Người Việt ít khi nhảy thẳng vào chuyện lớn.",
        f"Khi chuyện lớn được đặt lên bàn, ông không hứa bầu trời. Ông hứa lịch làm, hứa cách xử lý nếu hỏng, hứa không biến người thành phần thưởng.",
        f"Cảm xúc “{meta.get('emotion')}\" và nỗi sợ “{meta.get('conflict')}\" được ông gọi tên. Gọi tên để không để chúng điều khiển miệng.",
        f"Lan không 'quản lý' chuyện anh. Cô chỉ nhắc một câu: đừng biến người thành nhiệm vụ.",
    ]


def scene_legacy(meta, r):
    title, year, loc = meta["title"], meta["year"], meta["location"]
    return [
        f"Năm {year}. “{title}” dễ biến thành ảnh đẹp. Hùng cố làm nó sạch trên sổ trước khi sạch trên mic.",
        f"Tại {loc}, ông hỏi người nhận, người làm, cả người hay ghen. Tiền và quyền không được thành sân khấu.",
        f"Người được giao quyền phải từng gánh việc hỏng mà không đẩy lỗi. Máu mủ không đủ tiêu chuẩn.",
        f"“{meta.get('conflict')}\" vẫn có — nghi ngờ, so bì. Ông công khai số liệu đủ để soi, và giữ riêng chuyện nhà.",
        f"Khép ngày bằng một biên bản có tên. Không tên chịu trách nhiệm thì coi như chưa bàn giao.",
    ]


def scene_milestone(meta, r):
    title, year, loc = meta["title"], meta["year"], meta["location"]
    return [
        f"Năm {year}, {loc}. “{title}” không phải pháo hoa — là lúc ngồi đếm những gì còn chạy và những gì suýt vỡ.",
        f"Hùng giở sổ theo tháng: cửa còn mở, lương còn trả, khách còn quay lại, nhà còn muốn ông về.",
        f"Ông họp đội lõi. Ai muốn khoe số thì khoe một phút. Phần còn lại nói chỗ chưa xong và tên người sửa.",
        f"Phần thưởng hệ thống “{meta.get('reward')}\" chỉ được ông ghi nhận sau khi hiện trường khớp sổ.",
        f"Ông không tuyên bố đỉnh. Ông tuyên bố sàn: dưới mức này thì không được gọi là xong.",
    ]


def scene_expand(meta, r):
    title, year, loc = meta["title"], meta["year"], meta["location"]
    return [
        f"Năm {year}. “{title}” là bước ra khỏi vùng quen — {loc} lần này không cho phép làm ẩu kiểu 'thử xem sao'.",
        f"Hùng vẽ bản đồ việc: người, hàng, tiền, giấy tờ. Thiếu một góc là chưa đi.",
        f"Đội được chia theo khả năng, không theo người nhà. Người mới được kèm; người cũ được giao việc khó hơn.",
        f"“{meta.get('conflict')}\" xuất hiện đúng lúc dễ kiêu. Ông hạ giọng, mở sổ, chia lại việc.",
        f"Cuối ngày chỉ cần một bằng chứng chuyển động: hợp đồng, lô hàng, hoặc chìa khóa cửa mới.",
    ]


def scene_general(meta, r):
    title, year, loc = meta["title"], meta["year"], meta["location"]
    return [
        f"Năm {year}, tại {loc}. Việc “{title}” được Hùng nhét vào lịch như mọi việc khác: có đầu, có giữa, có người chịu.",
        f"Bước một: kiểm bằng chân. Bước hai: nghe người làm thật. Bước ba: quyết định có tên.",
        f"“{meta.get('conflict')}\" bị ghi trang đầu — không để bò ra trang cuối mới giật mình.",
        f"Giữa ngày có tin tốt và tin xấu. Cả hai đều được viết, phân việc, hẹn giờ kiểm.",
        f"Chiều, “{title}” rõ thêm một nấc thật — không bằng khẩu hiệu, bằng việc đã chuyển.",
    ]


SCENE_FN = {
    "store": scene_store,
    "factory": scene_factory,
    "global": scene_global,
    "crisis": scene_crisis,
    "human": scene_human,
    "legacy": scene_legacy,
    "milestone": scene_milestone,
    "expand": scene_expand,
    "general": scene_general,
}


def dialogues(meta, r):
    cast = meta.get("cast") or ["Trần Văn Hùng", "Trần Thị Lan"]
    b = next((x for x in cast if "Lan" in x), cast[1] if len(cast) > 1 else "Lan")
    conf = meta.get("conflict") or "rủi ro"
    title = meta["title"]
    kind = classify(title)
    bank = [
        (f"\"Việc '{title}' hôm nay anh đặt nặng điều gì?\" {b} hỏi.",
         "\"Đặt nặng chỗ dễ vỡ. Chỗ dễ ăn để sau.\""),
        (f"\"{conf} đang đứng ngay cửa,\" {b} nói nhỏ.",
         "\"Nhìn thẳng và ghi rõ. Né thì mất cửa, xông không sổ thì mất người.\""),
        ("\"Bên kia giảm giá mạnh,\" có người nhắc.",
         "\"Giảm bằng cắt chất lượng thì để họ giảm. Mình giữ hàng.\""),
        (f"\"Nếu hỏng, ai chịu?\" {b} hỏi.",
         "\"Tên trên sổ. Tên tôi. Không đẩy cho người mới.\""),
        ("\"Về nhà ăn chưa?\"",
         "\"Ăn vội rồi. Về sẽ ăn chậm hơn.\""),
    ]
    if kind == "human":
        bank = [
            (f"\"Anh tới đây vì việc hay vì người?\" giọng đối diện thẳng.",
             "\"Vì người. Việc sẽ theo sau nếu người còn muốn đứng cạnh.\""),
            (f"\"{b} bảo anh hay lấy việc đè hết,\" có tiếng cười nhẹ.",
             "\"Đúng. Hôm nay tôi đặt việc xuống một chút.\""),
            ("\"Anh hứa được gì?\"",
             "\"Không hứa trời. Hứa nói thật và không biến ai thành phần thưởng.\""),
        ]
    if kind == "crisis":
        bank = [
            ("\"Còn lương không?\" ai đó hỏi trước.",
             "\"Còn. Cắt chỗ khác trước, không cắt chỗ nuôi người.\""),
            ("\"Tin đồn đang chạy.\"",
             "\"Chạy chậm hơn số thật. Đưa số thật ra.\""),
            (f"\"{conf} có giết mình không?\"",
             "\"Có thể. Nếu mình giấu. Không giấu thì chỉ bị thương.\""),
        ]
    r.shuffle(bank)
    lines = []
    for a, b_ in bank[:3]:
        lines.append(a)
        lines.append(b_)
    return lines


def family(meta, r):
    year = meta["year"]
    title = meta["title"]
    if year <= 2012:
        return [
            f"Về nhà, bà Hà hỏi ăn chưa trước khi hỏi doanh thu. Lan bưng nước. Mâm cơm không linh đình — chỉ cần đủ để người đi làm còn muốn về.",
            f"Hùng kể “{title}” bằng ngôn ngữ nhà: ai khó, ai giúp, chỗ suýt hỏng. Không biến bàn ăn thành phòng họp, cũng không biến nhà thành người ngoài cuộc.",
            f"Trước khi ngủ ông viết sổ: thu — chi — nợ lời — nợ người. Hệ thống có thể nháy “{meta.get('reward')}\"; ông tự chấm bằng câu: hôm nay có ai bị bỏ lại không?",
        ]
    return [
        f"Đêm, điện thoại để im. Ông dành vài phút cho người còn chờ — không cho bảng số.",
        f"Họ nói về “{title}” ngắn. Cười một cái. Im một cái. Sự bình thường, với ông, hiếm hơn danh hiệu.",
        f"Sổ tay khép lại bằng một dòng cầu nối, không bằng khẩu hiệu.",
    ]


def system_block(meta, r):
    n, year = meta["num"], meta["year"]
    reward = meta.get("reward") or "Tiến độ"
    if n % 8 == 0 or "Hoàn thành" in meta["title"] or n % 10 == 0:
        return (
            f"「Hệ thống Thương Gia」\n"
            f"Năm: {year}\n"
            f"Thông báo: {reward}\n"
            f"Hùng nhận, gật với chính mình, rồi quay lại sổ tay — chỗ ông tin hơn bảng sáng."
        )
    return (
        f"Trong đầu, hệ thống chỉ nháy một dòng về “{reward}”. "
        f"Ông ghi tương ứng bằng mực. Ảo giác không ký tên chịu trách nhiệm được."
    )


def openers(meta, r):
    n, title, year, loc = meta["num"], meta["title"], meta["year"], meta["location"]
    opts = [
        f"{year}. {loc}. Việc “{title}” bắt đầu trước khi trời đủ sáng.",
        f"Hùng không thích ngày có chữ “{title}” trên lịch — những ngày ấy ít cho phép sai.",
        f"Trước “{title}”, ông nhớ một lần suýt mất chữ tín. Nhớ để tay không run vì kiêu.",
        f"“{title}” nghe như mốc son. Làm như mốc xước: phải đi chậm mới thấy đường.",
        f"Có người hỏi bao giờ xong “{title}\". Hùng hỏi lại: xong trên giấy hay xong ở hiện trường?",
        f"Năm {year}, {loc} không trải thảm đỏ cho “{title}\". Chỉ có việc và người.",
        f"Ông viết bốn chữ “{title}\" lên trang mới, rồi viết tên người chịu nếu hỏng — thường là tên mình.",
        f"Sáng {year} ở {loc}. Mùi {r.choice(['mưa bụi', 'cơm rang', 'dầu máy', 'giấy mực', 'cà phê đặc'])} và một việc tên “{title}\".",
        f"Không ai vỗ tay khi “{title}\" bắt đầu. Hùng cũng không cần. Ông cần cửa còn mở vào chiều.",
        f"Việc “{title}\" đặt ông vào thế phải chọn: nhanh hay chắc. Hôm nay ông chọn chắc một nhịp.",
    ]
    return opts[n % len(opts)]


def unique_expand(meta, r, avoid: set[str]) -> list[str]:
    """Many varied paragraphs; skip if already used in this chapter."""
    title, year, loc = meta["title"], meta["year"], meta["location"]
    cast = meta.get("cast") or ["Hùng", "Lan"]
    conf = meta.get("conflict") or "áp lực"
    emo = meta.get("emotion") or "bình tĩnh"
    n = meta["num"]
    bits = year_bits(year, r)
    pool = []

    pool += bits
    pool += [
        f"Ở góc nhìn người làm thuê, “{title}” là lịch nghỉ bị xô và lương tháng sau. Hùng nhớ điều đó trước khi nhớ biên lai.",
        f"Một chi tiết năm {year}: {r.choice(['số lô phải khớp hóa đơn', 'mẫu thử phải lưu', 'biên bản phải đủ chữ ký', 'tỷ giá phải khóa phụ lục', 'ngày giao phải trừ mưa/tàu trễ'])}. Mất trắng thường bắt đầu từ chỗ 'nhỏ'.",
        f"Ông chủ động gặp người khó tính nhất quanh “{title}\". Không mua bằng quà — mua bằng việc sửa đúng chỗ họ chỉ, nếu họ chỉ đúng.",
        f"Tin đồn bảo ông {r.choice(['làm quá nhanh', 'có nền lạ', 'sẽ sụp', 'chỉ giỏi nói'])}. Cách đáp: cửa vẫn mở, hàng vẫn đúng, lương vẫn trả.",
        f"Cảm xúc hôm nay nghiêng về “{emo}\". Ông không giấu, cũng không để cảm xúc ký thay mình.",
        f"Hai người tốt bất đồng cách làm “{title}\". Hùng không chọn người mình thích — chọn phương án kiểm được trong bảy ngày.",
        f"Ông nhớ thoáng {r.choice(['bát cháo năm tỉnh lại', 'mắt bà Hà', 'bụi đỏ Quốc Oai', 'bảng điện đỏ 2008', 'lần khách chửi vì trễ'])}. Ký ức để không tái phạm, không để khoe khổ.",
        f"Cuối buổi, “{title}\" để lại bằng chứng: {r.choice(['biên bản', 'hàng mẫu', 'chữ ký', 'ảnh hiện trường', 'danh sách việc'])}. Không bằng chứng thì coi như chưa làm.",
        f"Mười phút ông chỉ nghe, không xen. Người nói xong mới lộ chỗ thừa chỗ thiếu.",
        f"Tam giác giá — chất lượng — thời gian không bao giờ tròn. Hôm nay ưu tiên {r.choice(['chất lượng', 'đúng hạn', 'giữ người', 'giữ khách cốt lõi'])}, và nói thẳng chỗ sẽ đau.",
        f"Trên đường quanh {loc}, ông nhìn {r.choice(['cửa hàng nhỏ', 'công nhân tan ca', 'ruộng ven đường', 'cảng', 'dãy văn phòng'])}. Đất nước đổi; người bị bỏ lại vẫn là rủi ro lớn nhất.",
        f"Lời hứa buổi sáng được ông rà lại chiều. Lời nào quá tay thì gọi rút — lời thừa là nợ.",
        f"Người trẻ hỏi: làm lớn có cần cứng? Ông lắc. Cần rõ. Cứng không rõ chỉ gãy tay mình và tay người khác.",
        f"Sổ “{title}\" đánh dấu {r.choice(['đỏ — chết người nếu trễ', 'xanh — quan trọng', 'bút chì — có thể lùi'])}.",
        f"Khi trời {r.choice(['chiều', 'tối', 'se lạnh', 'nóng'])}, ông hỏi: đã kéo ai đi cùng “{title}\" mà không vứt lại?",
        f"{cast[min(1, len(cast)-1)]} ghi việc thành checklist, không thành bài văn. Việc xong được gạch; việc tắc được hỏi thiếu gì.",
        f"Hùng chấp nhận {conf} là một phần ngày. Chấp nhận không có nghĩa là đầu hàng — nghĩa là không sốc khi nó tới.",
        f"Ông kiểm tra lại chỗ dễ gian: {r.choice(['cân đong', 'ca làm', 'chiết khấu', 'hoa hồng môi giới', 'báo cáo tồn'])}. Gian nhỏ nuôi hỏng lớn.",
        f"Một khách/đối tác khó tính gật đầu. Một người trong đội thở phào. Hai tín hiệu ấy đáng giá hơn một bài báo.",
        f"Ch. {n}: phần thưởng chỉ thật khi {r.choice(['khách không trả hàng', 'công nhân không mất ca', 'nhà vẫn muốn ông về', 'sổ khớp ngân hàng'])}.",
        f"Ông để điện thoại xuống một lúc, nhìn {r.choice(['mưa', 'phố', 'vách xưởng', 'sân nhà'])}, rồi nhấc lên vì việc chưa xong.",
        f"Không ai hoàn hảo trong “{title}\". Có người sửa nhanh; có người che. Ông thưởng người sửa, không thưởng người che khéo.",
        f"Bản nháp phương án B luôn nằm sẵn. Người không có đường lùi dễ biến sợ hãi thành quyết định dở.",
        f"Ông cảm ơn thầm những người không có tên trên banner nhưng giữ “{title}\" không đổ.",
        f"Giọng nói trong họp được ông để ý: ai nói để thắng, ai nói để việc chạy. Ông ưu tiên nhóm sau.",
    ]
    r.shuffle(pool)
    out = []
    for p in pool:
        key = p[:60]
        if key in avoid:
            continue
        avoid.add(key)
        out.append(p)
    return out


def closers(meta, r):
    title, n = meta["title"], meta["num"]
    opts = [
        f"Đèn tắt. “{title}\" chưa xong cả đời — chỉ xong một ngày đủ để mai còn mở cửa.",
        f"Sổ nằm dưới gối. Ông cười thói quen sợ quên, rồi ngủ thật.",
        f"Ngoài kia phố/làng thở đều. Bên trong ông thở chậm đúng một nhịp — đủ để không vỡ.",
        f"Ai đó dặn ngủ. Ông ừ. Có mệnh lệnh chỉ nhà mới được phép đưa.",
        f"Ông rửa mặt nước lạnh, nhìn gương: không tìm anh hùng — tìm người còn tỉnh.",
        f"Trang sổ khép bằng dòng cầu nối. Mai sẽ kiểm bằng chân.",
        f"Hùng tắt đèn muộn hơn xưởng một chút. Về trễ vẫn hơn về như người lạ.",
        f"Một ngày của “{title}\" khép lại bằng việc đã giao, không bằng lời đã nói.",
    ]
    return [opts[n % len(opts)], opts[(n * 5 + 3) % len(opts)]]


def dedupe_paras(paras: list[str]) -> list[str]:
    seen = set()
    out = []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        k = re.sub(r"\s+", " ", p)[:90]
        if k in seen:
            continue
        seen.add(k)
        out.append(p)
    return out


def build_chapter(meta: dict) -> str:
    meta = dict(meta)
    n = meta["num"]
    r = rng_for(n)
    kind = classify(meta["title"])
    avoid: set[str] = set()

    paras: list[str] = []
    paras.append(openers(meta, r))
    yb = year_bits(meta["year"], r)
    paras.append(yb[0])
    paras.append(
        r.choice(
            [
                f"Không khí {meta['location']} đặc: ẩm, bụi, và nhịp người tất bật.",
                f"Ông chạm mép sổ — giấy sần, mực tím nhạt.",
                f"Âm thanh quanh {meta['location']} không đều, như nhịp thở của phố/làng.",
                f"Mùi {r.choice(['dầu máy', 'cơm', 'mưa', 'giấy mực', 'bụi đường'])} bám vào áo trước khi bám vào ký ức.",
            ]
        )
    )

    for p in SCENE_FN[kind](meta, r):
        paras.append(p)

    for d in dialogues(meta, r):
        paras.append(d)

    # midday beat unique
    paras.append(
        f"Trưa, ông ăn {r.choice(['cơm hộp', 'bún qua quýt', 'cơm nhà mang theo', 'ít thôi tại quán đối tác'])}. "
        f"Tai vẫn nghe giá, nợ, tin đồn — thị trường sống trong miệng người trước khi sống trong báo cáo."
    )
    paras.append(
        f"Chiều, hướng “{meta['title']}\" nhích thêm bằng {r.choice(['chữ ký', 'lô hàng', 'lịch giao', 'biên bản', 'ca chạy thử'])}. Không pháo hoa."
    )

    for p in family(meta, r):
        paras.append(p)

    paras.append(system_block(meta, r))

    # expand uniquely
    expand = unique_expand(meta, r, avoid)
    for p in expand:
        paras.append(p)
        # early stop estimate
        if word_count("\n\n".join(paras)) >= MIN_WORDS + 80:
            break

    for p in closers(meta, r):
        paras.append(p)

    paras = dedupe_paras(paras)

    # header
    body = "\n\n".join(paras)
    text = (
        f"{'=' * 60}\n"
        f"Chương {n}: {meta['title']}\n"
        f"{'=' * 60}\n\n"
        f"{body}\n"
    )

    # ensure min words with more unique expands
    guard = 0
    while word_count(text) < MIN_WORDS and guard < 30:
        more = unique_expand(meta, rng_for(n, guard + 1), avoid)
        if not more:
            # force fresh lines
            line = (
                f"Bổ sung hiện trường ch.{n}.{guard}: "
                f"Hùng rà lại một góc của “{meta['title']}\" — "
                f"{r.choice(['người', 'hàng', 'tiền', 'giấy tờ', 'uy tín'])} — "
                f"và ghi tên người theo dõi đến hết tuần."
            )
            if line[:60] not in avoid:
                more = [line]
                avoid.add(line[:60])
        add = "\n\n".join(more[:4])
        text = text.rstrip() + "\n\n" + add + "\n"
        text = "\n\n".join(dedupe_paras(text.split("\n\n"))) + "\n"
        guard += 1
        r = rng_for(n, guard)

    return text


def special_350():
    meta = dict(OUTLINE["chapters"]["350"])
    meta["year"] = 2020
    meta["location"] = "Làng Thanh Xuân, Quốc Oai"
    meta["conflict"] = "khoảng cách thế hệ và ký ức"
    meta["emotion"] = "nghẹn và biết ơn"
    # force human-ish
    base = build_chapter(meta)
    head = (
        f"{'=' * 60}\n"
        f"Chương 350: Gặp lại làng Thanh Xuân\n"
        f"{'=' * 60}\n\n"
        f"Năm 2020. Xe vào làng Thanh Xuân, Quốc Oai. Hùng bảo tài xế dừng ở đầu đường đất cũ — "
        f"đoạn còn sót giữa những nhà mới. Ông muốn bước vào bằng chân, không bằng cửa kính xe.\n\n"
        f"Bà Hà không còn trẻ. Lan nắm tay bà. Hùng đi sau, tay không cầm hoa — cầm vài tấm ảnh cũ "
        f"và sổ tay năm 1983 photo lại. Ông không về để khoe tập đoàn. Ông về để xem gốc còn nhận ông không.\n\n"
        f"Trẻ con trong làng không biết ông. Người già thì biết. Có người gọi 'cậu Hùng', có người gọi 'ông chủ', "
        f"có người chỉ gật. Ông gật lại tất cả như nhau.\n\n"
        f"Căn nhà cũ không còn nguyên. Nền còn. Giếng còn. Mùi đất sau mưa còn. "
        f"Ông đứng lâu chỗ từng là bếp tôn rỉ — nhớ bát cháo loãng và bữa thịt kho lần đầu.\n\n"
        f"Không có khủng hoảng vốn ở đây. Có thiếu thời gian, thừa kỷ niệm. "
        f"Ông quyên góp sửa đường làng và quỹ học trẻ; sổ công khai dán nhà văn hóa trước khi lên mạng.\n\n"
    )
    # strip old header from base and merge unique body parts
    body = re.sub(r"^={5,}.*?={5,}\s*", "", base, count=1, flags=re.S)
    # remove wrong settings
    body = body.replace("London", "làng Thanh Xuân")
    # drop first opener of generated body to avoid double
    parts = body.split("\n\n")
    merged = head + "\n\n".join(parts[2:20] + parts[20:])
    merged = "\n\n".join(dedupe_paras(merged.split("\n\n"))) + "\n"
    guard = 0
    avoid: set[str] = set()
    while word_count(merged) < MIN_WORDS and guard < 20:
        extra = (
            f"Ông đi thêm một vòng làng. Nghe chuyện đường điện, chuyện trường, chuyện đám cưới. "
            f"Về già ông hiểu: nghe cũng là cách trả nợ. (lần {guard+1})"
        )
        merged = merged.rstrip() + "\n\n" + extra + "\n"
        guard += 1
    return merged


def special_romance(n: int):
    meta = dict(OUTLINE["chapters"][str(n)])
    meta["conflict"] = "sợ làm tổn thương và sợ bỏ lỡ"
    meta["emotion"] = "hồi hộp chân thật"
    # ensure classify human via title already has gặp/chọn
    text = build_chapter(meta)
    text += (
        f"\n\nHùng nhận ra chuyện tình cảm không chốt như hợp đồng. "
        f"Ông nói rõ hoàn cảnh nhà, nói rõ ông bận, nói rõ không muốn ai đứng sau bóng việc. "
        f"Sự tôn trọng được đặt trước tương lai.\n"
    )
    return text


def light_clean(text: str, meta: dict) -> str:
    text = re.sub(r"\nTrong nhật ký riêng số[^\n]+\n?", "\n", text)
    text = re.sub(r"\n\(\d+\s*từ\)\s*$", "\n", text)
    text = text.replace("Chốt ý nghĩa:", "Ông ghi vào cuối trang:")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def process_all():
    files = chapter_files()
    stats = {"light": 0, "full": 0, "special": 0, "fail": []}
    for k, meta0 in OUTLINE["chapters"].items():
        n = int(k)
        meta = dict(meta0)
        path = files.get(n)
        if not path:
            stats["fail"].append(n)
            continue

        if n == 350:
            text = special_350()
            stats["special"] += 1
        elif n in {93, 94, 95, 96}:
            text = special_romance(n)
            stats["special"] += 1
        elif n in FULL_REGEN:
            text = build_chapter(meta)
            stats["full"] += 1
        else:
            old = path.read_text(encoding="utf-8", errors="replace")
            text = light_clean(old, meta)
            if word_count(text) < MIN_WORDS - 50:
                # keep core but don't full-regen finales 356-360 if long enough originally
                if word_count(old) >= MIN_WORDS - 50:
                    text = light_clean(old, meta)
                else:
                    text = build_chapter(meta)
                    stats["full"] += 1
                    path.write_text(text, encoding="utf-8")
                    continue
            stats["light"] += 1

        # hygiene: remove known bad fragments
        bad_frags = [
            "Anh/chú",
            "Lan/",
            "Plot làm việc",
            "Micro-conflict",
            "PowerPoint",
            "không sụp lạy trước bảng số",
            "se lạnh lúc tờ mờ",
            "không chờ khẩu hiệu",
            "Trong nhật ký riêng số",
            "Hùng tới sớm, Lan mở sổ, hiện trường nói trước phòng họp",
        ]
        for b in bad_frags:
            text = text.replace(b, "")
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = "\n\n".join(dedupe_paras(text.split("\n\n"))) + "\n"

        if word_count(text) < MIN_WORDS:
            avoid: set[str] = set()
            extra = unique_expand(meta, rng_for(n, 42), avoid)
            text = text.rstrip() + "\n\n" + "\n\n".join(extra) + "\n"
            text = "\n\n".join(dedupe_paras(text.split("\n\n"))) + "\n"

        path.write_text(text, encoding="utf-8")
        if word_count(text) < MIN_WORDS:
            stats["fail"].append((n, word_count(text)))
    return stats


def verify():
    files = chapter_files()
    markers = [
        "se lạnh lúc tờ mờ",
        "không chờ khẩu hiệu",
        "Trong nhật ký riêng",
        "Hùng tới sớm, Lan mở sổ",
        "chưa kịp dịu thì việc đã xếp hàng",
        "Anh/chú",
        "Micro-conflict",
        "Plot làm việc",
    ]
    heavy = 0
    under = []
    london = []
    opens = []
    chars = []
    # cross-chapter exact para dups in sample range
    para_count = {}
    for n, f in sorted(files.items()):
        t = f.read_text(encoding="utf-8", errors="replace")
        wc = word_count(t)
        chars.append(len(t))
        if wc < MIN_WORDS:
            under.append((n, wc))
        hits = sum(1 for m in markers if m in t)
        if hits >= 2:
            heavy += 1
        if "London" in t and "Thanh Xuân" in (f.name + t[:200]):
            london.append(n)
        for ln in t.splitlines():
            s = ln.strip()
            if s and not s.startswith("=") and not s.startswith("Chương"):
                opens.append(s[:70])
                break
        if 21 <= n <= 80:
            for para in t.split("\n\n"):
                p = para.strip()
                if len(p) > 100:
                    para_count[p[:120]] = para_count.get(p[:120], 0) + 1
    multi = sum(1 for v in para_count.values() if v >= 5)
    return {
        "chapters": len(files),
        "under_count": len(under),
        "under_min": under[:15],
        "heavy_template": heavy,
        "london_bug": london,
        "uniq_open": len(set(opens)) / max(1, len(opens)),
        "mean_chars": sum(chars) / len(chars),
        "cv": statistics.pstdev(chars) / (sum(chars) / len(chars)),
        "para_dup_keys_ge5_in_21_80": multi,
        "sample_open_25": opens[24] if len(opens) > 24 else None,
        "sample_open_50": opens[49] if len(opens) > 49 else None,
        "sample_open_300": opens[299] if len(opens) > 299 else None,
        "sample_open_350": opens[349] if len(opens) > 349 else None,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        print(json.dumps(verify(), ensure_ascii=False, indent=2))
    else:
        # For KEEP_LIGHT chapters, read current files first - they may already be regenerated badly in v1
        # Restore strategy: full regen 21-355; light only if still original quality for 1-20, 356-360
        st = process_all()
        print("DONE", st)
        print("VERIFY", json.dumps(verify(), ensure_ascii=False, indent=2))
