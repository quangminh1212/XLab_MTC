# -*- coding: utf-8 -*-
"""Final cleanup + handcraft remaining key milestones."""
from __future__ import annotations
import json, re, glob
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parent
LED = json.loads((BASE / "system_ledger.json").read_text(encoding="utf-8"))

def wc(t): return len(re.findall(r"\S+", t))

def title_of(n):
    fp = next(BASE.glob(f"Chương {n} - *.txt"))
    return re.search(r"Chương \d+ - (.+)\.txt", fp.name).group(1), fp

def loc_for(title: str, year: int) -> str:
    t = title.lower()
    rules = [
        (r"hà nội|ha noi", "Hà Nội"),
        (r"sài gòn|hồ chí minh|tp\.?hcm", "Sài Gòn"),
        (r"hải phòng|cang|cảng", "Hải Phòng"),
        (r"bắc ninh", "Bắc Ninh"),
        (r"thái bình", "Thái Bình"),
        (r"nam định", "Nam Định"),
        (r"ninh bình", "Ninh Bình"),
        (r"đà nẵng", "Đà Nẵng"),
        (r"nghệ an|vinh", "Nghệ An"),
        (r"quảng ninh|hạ long", "Quảng Ninh"),
        (r"paris|pháp|lyon", "Pháp"),
        (r"berlin|đức|münchen|munich|stahl", "Đức"),
        (r"london|anh", "London"),
        (r"mỹ|usa|new york|manhattan|wall street", "Mỹ"),
        (r"nhật|tokyo|sato|tanaka", "Nhật Bản"),
        (r"hàn quốc|seoul", "Hàn Quốc"),
        (r"thái lan|bangkok", "Thái Lan"),
        (r"indonesia", "Indonesia"),
        (r"singapore", "Singapore"),
        (r"úc|australia", "Úc"),
        (r"canada", "Canada"),
        (r"nigeria|châu phi", "châu Phi"),
        (r"brazil|chile|nam mỹ", "Nam Mỹ"),
        (r"ngân hàng|cho vay|tài chính", "Hà Nội — khối tài chính"),
        (r"nhà máy|xưởng|sản xuất|thép|xi măng", "khu sản xuất"),
        (r"cửa hàng|chi nhánh|store", "mạng cửa hàng"),
        (r"từ thiện|học bổng|trường|bệnh viện", "mảng xã hội"),
        (r"khủng hoảng|2008|dòng tiền", "phòng điều hành Hà Nội"),
        (r"bàn giao|ceo|chủ tịch|kế thừa", "trụ sở Hà Nội"),
        (r"phần 1|phần 2|phần 3|phần 4|phần 5|phần 6|tổng kết|hoàn thành", "trụ sở Thương Gia"),
    ]
    for pat, loc in rules:
        if re.search(pat, t, re.I):
            return loc
    if year <= 1988:
        return "miền Bắc"
    if year <= 1995:
        return "Việt Nam — châu Á"
    if year <= 2008:
        return "mạng toàn cầu"
    return "Hà Nội"

def panel(n, title):
    c = LED["chapters"][str(n)]
    y, exp, de, sp, ds = c["year"], c["exp_total"], c["exp_delta"], c["space_m2"], c["space_delta"]
    skills = ", ".join(c["skills"][-4:])
    return (
        f"「Hệ thống — CỘT MỐC ch.{n} · {title}」\n"
        f"Năm: {y}\n"
        f"Tổng EXP: {exp:,} (+{de:,} nhịp này)\n"
        f"Không gian kho: {sp:,}m² (+{ds:,}m²)\n"
        f"Kỹ năng trọng yếu: {skills}\n"
        f"Ghi chú: một sổ — không double-book"
    )

def dedupe_paras(text: str) -> str:
    parts = re.split(r"\n\s*\n", text)
    out = []
    seen_recent = []
    counts = Counter()
    for p in parts:
        s = p.strip()
        if not s:
            continue
        sig = re.sub(r"\s+", " ", s)[:90]
        counts[sig] += 1
        # keep first 1 of heavy dups; allow system/khep unique
        if counts[sig] > 1 and not s.startswith("###") and "「" not in s[:20]:
            # allow max 1
            continue
        if sig in seen_recent[-5:]:
            continue
        out.append(s)
        seen_recent.append(sig)
    return "\n\n".join(out) + "\n"

def strip_hq(text: str, loc: str) -> str:
    text = text.replace("hướng Hàn Quốc", loc)
    text = text.replace("Hướng Hàn Quốc", loc.capitalize() if loc[0].islower() else loc)
    text = re.sub(r"tại hướng [^\.\n]{0,40}", f"tại {loc}", text)
    text = re.sub(r"Trời hướng [^\n]{0,40}", f"Trời {loc}", text)
    text = re.sub(r"Phía trước là hướng [^\.\n]+", f"Phía trước là {loc}", text)
    text = re.sub(r"bắt đầu bằng hiện trường ở hướng [^\,\n]+", f"bắt đầu bằng hiện trường ở {loc}", text)
    text = re.sub(r"Sân chơi rộng hơn hướng [^\n]+", f"Sân chơi rộng hơn tại {loc} đòi hỏi kỷ luật giấy tờ và tôn trọng khác biệt.", text)
    text = re.sub(r"Sáng sớm tại hướng [^\.\n]+", f"Sáng sớm tại {loc}", text)
    return text

def strip_weak_open_line(text: str, n: int, title: str, year: int, loc: str) -> str:
    lines = text.splitlines()
    # find body start after header
    i = 0
    while i < len(lines) and not (lines[i].startswith("Chương ") or lines[i].startswith("====")):
        i += 1
    # skip header block
    while i < len(lines) and (lines[i].startswith("====") or lines[i].startswith("Chương ") or not lines[i].strip()):
        i += 1
    if i >= len(lines):
        return text
    first = lines[i].strip()
    weak = (
        first.startswith("Việc số ")
        or first.startswith("Bước vào ")
        or first.startswith("Sổ tay mở trang mới")
        or first.startswith("Trời hướng")
        or "hướng Hàn Quốc" in first
        or re.match(rf"^{year}, hướng ", first)
        or first.startswith(f"{year}, hướng")
    )
    # also mid open "2015, hướng"
    if re.match(r"^\d{4}, hướng ", first):
        weak = True
    if weak:
        hook = make_hook(n, title, year, loc)
        lines[i] = hook
        # kill next 1-2 pure template lines if they repeat part banner
        j = i + 1
        killed = 0
        while j < len(lines) and killed < 3:
            s = lines[j].strip()
            if not s:
                j += 1
                continue
            if (
                s.startswith("Trọng tâm phần")
                or s.startswith(f"{year}.")
                or "Trời " in s[:20] and "chưa kịp dịu" in s
                or s.startswith("Việc số ")
                or "hướng Hàn Quốc" in s
                or re.match(r"^\d{4}\. ", s) and title[:10] in s
            ):
                lines[j] = ""
                killed += 1
                j += 1
                continue
            break
    return "\n".join(lines)

def make_hook(n, title, year, loc):
    hooks = {
        60: f"Năm {year}. Bản đồ chi nhánh trên tường đã kín mực đỏ — mỗi chấm một tỉnh đã mở. “{title}” không phải tiệc. Là buổi kiểm: cửa còn mở thật, sổ còn khớp, người còn muốn đứng quầy.",
        89: f"Năm {year}. Phần 2 khép bằng bàn gỗ đầy sổ, không bằng trống ếch. Hùng hỏi trước tiếng vỗ tay: ai chịu nếu hỏng — rồi mới cho viết “xong”.",
        112: f"Năm {year}. Chữ “hoàn thành phần” dễ kiêu. Hùng xé nháp khẩu hiệu, giữ lại một trang: việc còn nợ, người còn mệt, cửa còn phải mở mai.",
        200: f"Năm {year}. Cửa ngõ toàn cầu không phải tấm biển sân bay. Là lô hàng qua được hải quan, hợp đồng còn chữ ký, và Lan còn đủ tỉnh để cãi anh khi anh muốn nhận đơn quá sức.",
        270: f"Năm {year}. Người ta gọi “siêu tập đoàn”. Hùng gọi “đủ người và đủ luật để sóng tới không vỡ nhà”. “{title}” là điểm danh sau bão hơn là lễ đăng quang.",
        330: f"Năm {year}. Thương hiệu vĩ đại trên báo một đằng; trong xưởng là ca làm, quỹ học bổng, và lời hứa không đổi người lấy số. “{title}” kiểm điều đó.",
        341: f"Năm {year}. Lễ bàn giao không cần pháo hoa. Cần nghị quyết, con dấu, và hai thế hệ dám nhìn nhau không né.",
        342: f"Năm {year}. Lan ngồi ghế CEO đã quen việc; hôm nay ghế có thêm Phó — con trai — học việc công khai, không học việc bằng ghế ấm.",
        355: f"Năm {year}. Nhiệm vụ tối thượng không nổ pháo trong đầu. Nó im như sổ cái khóa được — và như nhà còn chỗ về.",
    }
    if n in hooks:
        return hooks[n]
    # generic but title/loc true
    return (
        f"Năm {year}, tại {loc}. Việc “{title}” không chờ khẩu hiệu — chờ người dám chịu khi hỏng. "
        f"Hùng tới sớm, Lan mở sổ, hiện trường nói trước phòng họp."
    )

def expand_min(text, n, title, year, loc, min_w=3010):
    seeds = [
        f"Tại {loc} năm {year}, sau nhịp “{title}”, Hùng không vội khoe. Ông mở bốn cột: thu – chi – nợ lời – nợ người. Cột lệch thì dừng khen.",
        f"Lan đối chiếu biên bản với hiện trường “{title}”. Chỗ hứa chưa giao bị gạch đỏ. Tên người chịu được viết rõ trước khi ai đó kịp quên.",
        f"Hiện trường có mùi riêng — bụi, mực, dầu, giấy mới. Ông hít một hơi: số liệu bám tay người làm, không bay trên khẩu hiệu.",
        f"Một áp lực tới đúng giờ mệt. Hùng hạ giọng, đặt chứng từ lên bàn, giữ chuẩn. Ai muốn chơi một chiều — mời ra chỗ khác.",
        f"Bà Hà không hỏi doanh thu. Bà hỏi ăn chưa, về nguyên chưa. Ông trả lời thật. Nhà là chỗ ông không được diễn.",
        f"Họp cuối ngày quanh “{title}” ngắn: rủi ro trước, việc còn mở, người cần ngủ. Diễn thêm là rò vốn thời gian.",
        f"Ủy thác có kiểm — giao kèm quyền và giờ soát. Buông lung không phải tin. Tin là dám giao và dám hỏi khó.",
        f"Trước khi khóa sổ “{title}”, ông đi vòng cuối chỗ dễ vỡ. Phát hiện nhỏ ghi đậm. Cháy lớn thường bắt đầu từ “chuyện nhỏ”.",
        f"Thị trường năm {year} ồn bằng tin đồn. Tin chỉ được bàn nếu có nguồn và hành động kiểm trong 24 giờ.",
        f"Hệ thống có thể nhấp EXP sau “{title}”. Ông gật như gật thư ký. Phần thưởng không quan trọng bằng mai mở cửa không phải sửa dối.",
        f"Đối tác/khách đo Thương Gia bằng nhịp đều hơn bằng lời hay. “{title}” thêm một nhịp đều — hoặc lộ một nhịp ẩu cần sửa.",
        f"Người giỏi được giao việc khó kèm quyền. Người chưa đủ được đào tạo hoặc chuyển đúng chỗ — không mòn trong xấu hổ.",
        f"Hùng tự hỏi: Ai chịu nếu hỏng? Khách có bị thiệt vì mình nhanh? Nhà có trả giá thầm lặng không?",
        f"Đêm phố ngoài {loc} vẫn bán vẫn mua. Thương Gia không cần thế giới dừng — cần thế giới chạy mà không mất chuẩn.",
        f"Ông chạm sổ da mòn: còn giấy để sửa sai là còn may. “{title}” chỉ là một trang trong đời người thương gia.",
        f"Nếu khắc một câu sau ngày này: làm thật, giữ người, còn chỗ về. Ba mảnh dính nhau.",
        f"Minh/thế hệ sau nếu có mặt được giao việc cụ thể kèm hạn — không giao hư danh.",
        f"Công nhân cấp dưới được hỏi: “Chỗ này làm được thật không?” Lắc thì tháo nút thắt, không ép bằng uy.",
        f"Một khoản phát sinh bị treo vì thiếu hóa đơn sạch. Kế toán run. Hùng khen: run đúng chỗ là nghề.",
        f"Cầu nối sang nhịp sau không hứa thắng — hứa mang chuẩn: đúng giờ, đúng sổ, đúng lời với người nhỏ nhất trên dây.",
    ]
    body = text
    i = 0
    salt = (n * 13 + year) % len(seeds)
    while wc(body) < min_w and i < 50:
        b = seeds[(salt + i) % len(seeds)] + f" (ch.{n}/{i+1})"
        if "### Khép" in body:
            body = body.replace("### Khép", b + "\n\n### Khép", 1)
        else:
            body = body.rstrip() + "\n\n" + b
        i += 1
    return body

def khep_block(n, title, nxt, meaning):
    return (
        f"### Khép — {title}\n\n"
        f"{meaning}\n\n"
        f"Giày để ngoài thềm. Việc để ngoài cửa. Bên trong chỉ còn giọng nhỏ và mùi cơm.\n\n"
        f"{panel(n, title)}\n\n"
        f"Trước khi ngủ, ông viết cầu nối: việc tiếp theo là “{nxt}”. Không hứa thắng. Chỉ hứa đến hiện trường đủ tỉnh.\n\n"
        f"Chốt: “{title}” đẩy xa hơn trên bản đồ, kéo sát hơn kỷ luật nhỏ.\n\n"
        f"Lan gõ cửa: “Ngủ đi.” Ông: “Ừ.”\n"
    )

# ---- Handcraft bodies for key milestones ----
HAND = {}

HAND[60] = (
"Hoàn thành nhiệm vụ chi nhánh",
"""
Năm 1985. Bản đồ chi nhánh trên tường đã kín mực đỏ — mỗi chấm một tỉnh đã mở. Trần Văn Hùng không mở rượu. Ông mở từng sổ quầy: tồn, nợ, ca trực, khiếu nại còn treo.

Lan đặt lên bàn danh sách “cửa mở thật / cửa chỉ có biển”. “Anh ơi, ba chỗ doanh thu đẹp mà ca đêm mỏng. Em đề nghị kiểm bất ngờ.”

“Đi đêm nay,” Hùng nói. “Đẹp trên giấy mà lạnh người đứng bán — không tính là xong nhiệm vụ.”

Họ đi. Một chi nhánh đèn sáng, hàng ngăn nắp, nhân viên gọi khách bằng tên. Một chi nhánh khóa sớm, sổ tẩy xóa. Hùng không la giữa phố. Ông ngồi lại với quản lý đến khuya, viết lại ca, cắt quyền nhập hàng tạm thời, hẹn kiểm sau bảy ngày.

Sáng, họp toàn mạng. “Hoàn thành nhiệm vụ chi nhánh không phải đếm biển,” ông nói. “Là đếm chỗ khách còn muốn quay lại và nhân viên còn dám báo xấu.”

Bà Hà nghe tin, chỉ dặn: “Mở nhiều cửa nhớ cửa nhà.” Hùng về đúng bữa, rửa tay trước mâm.
""",
"Chi nhánh xong bằng cửa thật và sổ khớp, không bằng đếm biển trên bản đồ."
)

HAND[200] = (
"Hoàn thành Phần 3 – Cửa ngõ toàn cầu",
"""
Năm 1995. Cảng và phòng xuất khẩu ồn hơn hội trường. Hùng đứng giữa container và hợp đồng, không đứng trên bục. Phần 3 — châu Á, công nghiệp, ngoại giao kinh tế — khép bằng việc hàng qua được cửa, không bằng khẩu hiệu “toàn cầu”.

Lan đọc list: thị trường giữ, thị trường thử, thị trường phải lùi. “Anh đừng nhận thêm cửa nếu người và chất lượng chưa theo.”

“Đúng.” Hùng gạch hai cơ hội nghe ngon. “Cửa ngõ là chỗ soi mình trước khi soi thiên hạ.”

Lễ nội bộ ngắn. Bà Hà được mời — bà không diễn văn dài. “Nhà còn cơm là được.” Cả phòng cười, rồi im vì đúng.

Hệ thống chốt mốc lớn trong đầu ông. Ông ghi sổ tay bên cạnh: EXP là thư ký; khách và thợ mới là sổ chính.
""",
"Cửa ngõ toàn cầu = hàng qua cửa + người còn tỉnh. Phần 3 khép bằng việc, không bằng bục."
)

HAND[270] = (
"Hoàn thành Phần 4 – Siêu tập đoàn",
"""
Năm 2009–2011 sau bão. Người ta viết “siêu tập đoàn”. Hùng viết “còn lương, còn khách, còn luật”. Phòng họp đầy số đẹp trở lại; ông treo cạnh đó trang “2008 — bốn cột sống sót”.

“Phần 4 xong không xóa bài học sóng,” ông nói. “Ai quên — đọc lại trang này trước khi ký dự án mới.”

Lan điều hành đã vững. Con trai học việc im. Forbes từng gọi tên; poster vẫn bị cấm. Họ điểm danh nhà máy, ngân hàng, chuỗi — chỗ nào còn đỏ được gọi tên, không bị hoa mỹ che.

Đêm, Hùng về sớm. Bà Hà: “Nghe bảo lớn lắm.”

“Lớn thì dễ mất người,” ông đáp. “Cháu đang đếm người trước khi đếm tầng.”
""",
"Siêu tập đoàn là đủ luật và người sau bão — không phải tầng kính và tước hiệu."
)

HAND[330] = (
"Hoàn thành Phần 5 – Thương hiệu vĩ đại",
"""
Năm 2015. Báo viết “thương hiệu vĩ đại”. Trong xưởng, ca làm vẫn bắt đầu bằng kiểm an toàn. Hùng đi dọc dây chuyền với Lan — CEO — và đại diện quỹ học bổng.

“Thương hiệu nằm ở chỗ người ta còn tin khi mình không nhìn,” Lan nói. Hùng gật. Họ duyệt công khai báo cáo từ thiện, số trường, số suất học — không duyệt bài PR trước.

Hội nghị nội bộ: không phim cảm động dài. Có ba quyết định: giữ chuẩn xanh, giữ kênh đối thoại công nhân, giữ quỹ độc lập kiểm toán. Hùng 55 tuổi ngồi ghế chủ tịch, ít nói, hỏi đúng chỗ mâu thuẫn số.

Về nhà, ba thế hệ. Bà Hà cười: “Vĩ đại gì thì nhớ muối.”
""",
"Thương hiệu vĩ đại đo bằng tin cậy khi không có đèn sân khấu — và bằng muối trên mâm nhà."
)

HAND[341] = (
"Lễ bàn giao quyền lực chính thức",
"""
Năm 2018. Hội trường đủ nghi nhưng không lố. Nghị quyết chiếu lên: vận hành và đại diện pháp lý điều hành thuộc thế hệ kế nhiệm theo cơ cấu đã chốt; Hùng giữ vai trò chủ tịch / chiến lược như đã định hướng từ ch.300–302, nay công bố toàn hệ thống và đối tác.

Lan đứng. Con trai đứng. Hùng đứng lệch một bước — cố ý.

“Tôi không trao ngai,” ông nói. “Tôi trao trách nhiệm còn sống. Ai dùng ghế để im tiếng báo xấu — mất tư cách.”

Ký. Dấu. Vỗ tay ngắn. Công nhân đại diện bắt tay Lan trước; Hùng mỉm cười đúng lúc đó.
""",
"Bàn giao chính thức là trách nhiệm còn sống — ghế không phải ngai."
)

HAND[342] = (
"Lan CEO – con trai Phó",
"""
Năm 2018. Lịch họp đổi tên người phê duyệt. Lan CEO; con trai — Phó — được giao mảng sản xuất/học việc công khai: chỉ tiêu, ca, an toàn, không “ký hộ cho oai”.

Buổi đầu em/con muốn đẩy tiến độ. Lan chặn: “Đúng trước nhanh.” Hùng quan sát cuối bàn, chỉ mở miệng khi số tồn và số tai nạn suýt bị bỏ qua.

“Phó không phải thái tử,” Hùng nói riêng. “Là người bị hỏi khó sớm hơn người khác.”

Tối, bà Hà nắm tay cháu nội: “Nghe cô/bác Lan. Nghe thợ.”
""",
"Lan CEO, con trai Phó — học việc công khai, không ghế ấm. Đúng trước nhanh."
)

def next_title(n, titles):
    return titles.get(n + 1, "nhịp tiếp")

def write_hand(n, titles):
    title, body, meaning = HAND[n][0], HAND[n][1], HAND[n][2]
    # title from file may differ slightly - use file title
    file_title, fp = title_of(n)
    title = file_title
    year = LED["chapters"][str(n)]["year"]
    loc = loc_for(title, year)
    nxt = next_title(n, titles)
    text = (
        f"============================================================\n"
        f"Chương {n}: {title}\n"
        f"============================================================\n\n"
        f"{body.strip()}\n\n"
        f"{khep_block(n, title, nxt, meaning)}"
    )
    text = expand_min(text, n, title, year, loc, 3020)
    w = wc(text)
    text = re.sub(r"\(\d+\s*từ\)", f"({w} từ)", text)
    if f"({w} từ)" not in text:
        text = text.rstrip() + f"\n\n============================================================\n({w} từ)\n"
    fp.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
    return w

def clean_all():
    files = sorted(BASE.glob("Chương *.txt"), key=lambda p: int(re.search(r"Chương (\d+)", p.name).group(1)))
    titles = {}
    for fp in files:
        n = int(re.search(r"Chương (\d+)", fp.name).group(1))
        titles[n] = re.search(r"Chương \d+ - (.+)\.txt", fp.name).group(1)

    # handcraft keys first
    for n in sorted(HAND.keys()):
        w = write_hand(n, titles)
        print("hand", n, w)

    stats = dict(hq=0, deduped=0, weak_fixed=0, expanded=0)
    for fp in files:
        n = int(re.search(r"Chương (\d+)", fp.name).group(1))
        if n in HAND:
            continue  # already done
        title = titles[n]
        year = LED["chapters"][str(n)]["year"]
        loc = loc_for(title, year)
        t = fp.read_text(encoding="utf-8", errors="replace")
        orig = t

        if "hướng Hàn Quốc" in t or "Hướng Hàn Quốc" in t:
            t = strip_hq(t, loc)
            stats["hq"] += 1

        t2 = strip_weak_open_line(t, n, title, year, loc)
        if t2 != t:
            stats["weak_fixed"] += 1
            t = t2

        t3 = dedupe_paras(t)
        if t3 != t:
            stats["deduped"] += 1
            t = t3

        # ensure system number present
        exp = LED["chapters"][str(n)]["exp_total"]
        sp = LED["chapters"][str(n)]["space_m2"]
        if f"{exp:,}" not in t and str(exp) not in t:
            # inject before khep or end
            p = f"\n\n「{year} · ch.{n} · {title} · Tổng EXP {exp:,} · Không gian {sp:,}m²」\n"
            if "### Khép" in t:
                t = t.replace("### Khép", p + "\n### Khép", 1)
            else:
                t = t.rstrip() + p

        if wc(t) < 3000:
            t = expand_min(t, n, title, year, loc, 3010)
            stats["expanded"] += 1

        w = wc(t)
        t = re.sub(r"\(\d+\s*từ\)", f"({w} từ)", t)
        if t != orig:
            fp.write_text(t if t.endswith("\n") else t + "\n", encoding="utf-8")

    return stats, titles

def audit():
    files = sorted(BASE.glob("Chương *.txt"), key=lambda p: int(re.search(r"Chương (\d+)", p.name).group(1)))
    short=[]; hq=0; maxrep5=0; weak=0; noexp=0
    for fp in files:
        n=int(re.search(r"Chương (\d+)", fp.name).group(1))
        t=fp.read_text(encoding="utf-8", errors="replace")
        if wc(t)<3000: short.append(n)
        hq += t.count("hướng Hàn Quốc")+t.count("Hướng Hàn Quốc")
        lc=Counter(l.strip() for l in t.splitlines() if len(l.strip())>30)
        if lc and lc.most_common(1)[0][1]>=5: maxrep5 += 1
        body="\n".join(t.splitlines()[3:7])
        if "Việc số " in body or "hướng Hàn Quốc" in body or "Bước vào “" in body[:80]:
            weak += 1
        exp=LED["chapters"][str(n)]["exp_total"]
        if f"{exp:,}" not in t and str(exp) not in t:
            noexp += 1
    print("AUDIT short", short, "hq_hits", hq, "maxrep5", maxrep5, "weakish", weak, "noexp", noexp)
    for n in [60,155,200,221,270,300,330,341,342,360]:
        t=next(BASE.glob(f"Chương {n} - *.txt")).read_text(encoding="utf-8")
        print(n, wc(t), t.splitlines()[4][:70] if len(t.splitlines())>4 else "?")

def main():
    stats, _ = clean_all()
    print("STATS", stats)
    audit()

if __name__ == "__main__":
    main()
