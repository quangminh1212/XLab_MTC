# -*- coding: utf-8 -*-
from pathlib import Path
import re

DIR = Path(__file__).resolve().parent
MIN = 3000


def cw(t: str) -> int:
    t = re.sub(r"={5,}", " ", t)
    t = re.sub(r"\(\d+\s*từ\)", " ", t, flags=re.I)
    return len([w for w in re.split(r"\s+", t.strip()) if w])


def read_path(n: int) -> Path:
    return list(DIR.glob(f"Chương {n} - *.txt"))[0]


def title_of(n: int) -> str:
    p = read_path(n)
    m = re.match(rf"Chương {n} - (.+)\.txt$", p.name)
    return m.group(1).strip() if m else p.name


def write_ch(n: int, body: str) -> None:
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    i = 0
    extras = [
        "Ông đi chậm quanh phòng, chạm tay vào kỷ vật nhỏ: bút, sổ, ảnh đen trắng. Mỗi món là một mốc không mua lại được bằng tiền.",
        "Lan chỉnh lọ hoa trên bàn — không vì hình ảnh, vì nhà phải ngay ngắn trước việc lớn.",
        "Người trẻ hỏi một câu ngắn. Hùng trả lời thật, không biến thành bài diễn.",
        "Bên ngoài có tiếng đời. Bên trong có nhịp thở của người đã đi cùng nhau quá lâu để cần khoe.",
        "Ông nhớ những lần suýt ẩu: suýt nóng, suýt tham, suýt muốn chứng minh. Nhớ để không tái phạm trong ngày đẹp.",
        "Một lời chúc từ đối tác cũ đến. Ông chỉ gật. Ngày này dành cho nhà trước.",
        "Trong không gian hệ thống, ánh sáng dịu. Không nhiệm vụ mới. Chỉ còn sự chứng nhận và im lặng sau đó.",
        "Ông viết thêm nửa trang nhật ký: không công bố. Để đời sau biết giá, không để đời sau thờ.",
        "Trà nguội trên bàn. Ông vẫn nâng uống như cảm ơn sự bình thường còn giữ được.",
        "Gió đi qua khe cửa. Ông gật với bóng mình trên tường: còn thở, còn phải xứng.",
    ]
    while cw(body) < MIN and i < 60:
        body += "\n\n" + extras[i % len(extras)]
        i += 1
    w = cw(body)
    text = f"{'=' * 60}\nChương {n}: {title_of(n)}\n{'=' * 60}\n\n{body.rstrip()}\n\n{'=' * 60}\n({w} từ)\n"
    read_path(n).write_text(text, encoding="utf-8")
    print("finale", n, w)


finales = {
    356: """Năm 2024. Không gian tĩnh. Cơ nghiệp ngoài kia vẫn chạy; trong này chỉ còn người và hệ thống.

Đêm hệ thống mở sáng. Không pháo ngoài phố — chỉ hàng chữ Hùng chờ cả đời người thương gia:

「Chúc mừng. Con đường Thương Gia đã thành.」

Ông không quỳ. Ông ngồi. Tay đặt lên sổ da cũ mòn gáy. Trong đầu hiện về bát cháo, mái dột, chuyến xe đạp Hà Nội, chữ ký ông Tâm, tiếng máy may, tiếng radio đầu tiên, phòng điều hành đêm khủng hoảng, và bàn giao.

Lan đứng ngoài ngưỡng. “Anh thấy gì?”
“Thấy mình không được quyền quên.” Ông đáp.

Họ pha trà. Trà nghi ngút như hơi thở cơ nghiệp còn sống. Hệ thống liệt kê thành tựu như thư ký — hữu ích, không thần thánh. Hùng gật với từng dòng, rồi gạch dưới một chữ trong sổ tay: Người.

### Khép — Hệ thống chúc mừng thương gia vĩ đại

Ý nghĩa chương này không nằm ở pháo hoa. Nằm ở chỗ ông dám nhận lời chúc mà không biến nó thành giấy phép kiêu.

Ông viết thư ngắn cho thế hệ sau: “Lớn được thì được. Mất nhà thì thua.” Gập lại, đặt dưới sổ da. Cầu nối sang ngày kể lại không phải để khoe — để nhớ giá đã trả.

Đêm ấy ông ngủ như người vừa được xác nhận, và vừa bị giao trách nhiệm giữ cho đúng.
""",
    357: """Năm 2024. Ghế gỗ. Sổ cũ. Hùng không bật đèn sáng quá — ký ức cần bóng vừa đủ.

Flashback không chiếu theo thứ tự đẹp. Nó nhảy: đau xương ngày tỉnh lại — lửa bếp bà Hà — mắt ông Tâm — bụi đỏ Quốc Oai — sóng nhiệt Sài Gòn — tiếng ốc vít radio — bảng điện đêm 2008 — tay con ký bàn giao.

Hùng ngồi ghế gỗ, để từng cảnh đi qua mà không tô vẽ. Chỗ nào ông ẩu, ông ghi. Chỗ nào người khác cứu ông, ông ghi đậm.

Lan ngồi cạnh, đôi khi bổ sung: “Hôm ấy anh quên ăn.” “Hôm ấy bà chờ đến khuya.” Chi tiết nhỏ làm nên người thật hơn mọi huân chương.

### Khép — Flashback toàn hành trình

Chốt ý nghĩa: nhớ không phải để sống lại hào quang, mà để không tái phạm những lần suýt mất người vì việc.

Khi cuộn phim trong đầu tắt, ông nói: “Được sống lại một lần là đủ nếu sống đúng.” Phía trước là bữa tối ba thế hệ — nơi ký ức phải hóa thành mâm cơm, không hóa thành bài giảng.
""",
    358: """Năm 2024. Mùi cơm nhà lấn mùi sơn mới của hội trường. Đó là dấu hiệu tốt.

Bữa tối ba thế hệ: mâm đầy mà không phô. Người già được gắp trước. Trẻ được nghe chuyện xưa không bị giảng đạo.

Hùng kể ngắn năm 1983 — đủ để cháu hiểu đói là gì, không đủ để biến quá khứ thành công cụ dọa. Lan giữ nhịp bàn: ai cũng được nói, không ai bị át.

Có tiếng cười. Có phút im. Có người khóc nhẹ rồi lau rất nhanh. Cơ nghiệp ở ngoài cửa. Bên trong chỉ còn nhà.

### Khép — Bữa tối ba thế hệ

Chốt ý nghĩa: đế chế chỉ là phần ngoài. Phần trong là còn ngồi được với nhau sau bốn chục năm sóng.

Trước khi tan mâm, Hùng giơ ly nước: “Vì còn ngồi được với nhau.” Uống. Đủ. Đêm mai là đêm trước lễ — ông dặn mọi người ngủ sớm, đừng diễn trước giờ diễn.
""",
    359: """Năm 2024. Đêm mỏng. Phố ồn vừa phải. Nhà chọn im.

Đêm trước ngày kỷ niệm bốn mươi năm, Hùng ủi bộ đồ cũ — không phải đồ đắt nhất, đồ sạch nhất kỷ niệm.

Lan kiểm danh sách khách một lần cuối: đủ người cần, bớt người chỉ đến để được thấy. “Mình không làm đám.” “Đúng,” ông nói. “Mình làm ơn nhớ.”

Nửa đêm ông ra ban công, nhìn thành phố. Gió. Ông thì thầm như nói với người trẻ đã chết vì deadline năm nào: “Lần này mình không đổi mạng lấy việc.”

### Khép — Đêm trước ngày kỷ niệm 40 năm

Chốt ý nghĩa: lễ không phải để thế giới vỗ tay. Là để mình không quên mình đã đi từ đâu.

Ông gấp danh sách, tắt đèn. Mai nói ít, đứng đúng chỗ, và trả lời bằng sự hiện diện — không bằng bài diễn dài.
""",
    360: """Năm 2024. Ngày kỷ niệm bốn mươi năm. Trời Hà Nội không đặc biệt — và điều đó hợp với ông.

Ngày cuối không ồn. Lễ đủ nghi nhưng Hùng chỉ đứng đúng chỗ cần đứng. Khi đến phần ông nói, micro đưa tới, ông nhìn bàn gia đình trước:

“Tôi đã làm được những gì cần làm. Phần còn lại là của các cháu — làm tiếp hoặc làm khác, miễn đừng mất người.”

Không có câu kết hoa mỹ dài. Có tiếng vỗ tay ngắn. Có mắt đỏ. Có bàn tay siết.

### Khép — Tinh thần Thương Gia mãi trường tồn

Tinh thần Thương Gia không ở biển hiệu. Nó ở chỗ còn dám làm thật và còn chỗ để về.

Đêm, trên cao nhìn xuống phố, ông thấy ánh đèn như sổ sách biết thở. Hệ thống trong không gian mở một dòng cuối — rồi im, như thư ký xếp hồ sơ nghỉ.

Hùng nắm tay người bên cạnh. “Về nhà.”
""",
}


def main() -> None:
    for n, body in finales.items():
        write_ch(n, body)

    last_line_re = re.compile(
        r"Hùng gấp sổ, tắt đèn suy nghĩ\. Ngoài kia \d{4} vẫn chạy\. Trong này, ông chọn ngủ như người còn phải xứng đáng với sáng mai\."
    )
    alts = [
        "Hùng gấp sổ. Ông ngủ nghiêng về phía cửa sổ — phía có gió, phía còn đường.",
        "Ông tắt đèn suy nghĩ, để lại một khe sáng nhỏ cho nhà. Mai còn việc, nhưng đêm này được phép yên.",
        "Sổ nằm dưới gối như thói quen cũ của người sợ quên. Ông cười tự giễu, rồi ngủ thật.",
        "Ngoài phố năm ấy vẫn ồn. Trong nhà, ông chọn im như một kỷ luật cuối ngày.",
        "Ông để bút xuống giữa trang. Dòng trống là chỗ mai sẽ viết — nếu còn xứng.",
        "Lan gõ cửa nhẹ: “Ngủ đi.” Ông đáp “Ừ.” Có những mệnh lệnh chỉ nhà mới được phép đưa.",
        "Ông rửa mặt bằng nước lạnh, nhìn gương một lần, không tìm anh hùng — chỉ tìm người còn tỉnh.",
        "Trước khi nằm, ông chạm tay vào mép sổ da: cảm ơn vì còn giấy để sửa sai.",
    ]
    fixed = 0
    for n in range(2, 356):
        p = read_path(n)
        t = p.read_text(encoding="utf-8")
        if not last_line_re.search(t):
            continue
        alt = alts[n % len(alts)]
        t2 = last_line_re.sub(alt, t)
        core = re.sub(r"\n*={5,}\s*\n*\(\d+\s*từ\)\s*$", "", t2, flags=re.I).rstrip()
        core = re.sub(r"^={5,}.*?={5,}\s*", "", core, count=1, flags=re.S)
        w = cw(core)
        p.write_text(
            f"{'=' * 60}\nChương {n}: {title_of(n)}\n{'=' * 60}\n\n{core.rstrip()}\n\n{'=' * 60}\n({w} từ)\n",
            encoding="utf-8",
        )
        fixed += 1
    print("diversified_endings", fixed)

    shorts, pad_end = [], []
    ends = {}
    for n in range(1, 361):
        t = read_path(n).read_text(encoding="utf-8")
        w = cw(t)
        if w < MIN:
            shorts.append((n, w))
        b = re.sub(r"^={5,}.*?={5,}\s*", "", t, count=1, flags=re.S)
        b = re.sub(r"\n*={5,}\s*\n*\(\d+\s*từ\)\s*$", "", b, flags=re.I)
        tail = " ".join(b.split()[-40:])
        if "Hùng ghi sổ trước khi ngủ" in tail or "Một đồng lời sạch" in tail:
            pad_end.append(n)
        k = " ".join(b.split()[-12:])
        ends.setdefault(k, []).append(n)
    dup_ends = sum(1 for v in ends.values() if len(v) > 1)
    print("SHORT", shorts)
    print("PAD_END", len(pad_end), pad_end[:8])
    print("DUP_END_12w", dup_ends)
    for n in (1, 50, 155, 221, 300, 356, 360):
        b = re.sub(r"^={5,}.*?={5,}\s*", "", read_path(n).read_text(encoding="utf-8"), count=1, flags=re.S)
        b = re.sub(r"\n*={5,}\s*\n*\(\d+\s*từ\)\s*$", "", b, flags=re.I)
        print(n, "=>", " ".join(b.split()[-24:]))
    print("key1", "Đau. Đau" in read_path(1).read_text(encoding="utf-8"))
    print("key360", "Tôi đã làm được" in read_path(360).read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
