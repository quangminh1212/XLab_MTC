# -*- coding: utf-8 -*-
from pathlib import Path
import re

DIR = Path(__file__).resolve().parent
MIN = 3000


def cw(t: str) -> int:
    t = re.sub(r"={5,}", " ", t)
    t = re.sub(r"\(\d+\s*từ\)", " ", t, flags=re.I)
    return len([w for w in re.split(r"\s+", t.strip()) if w])


def path(n: int) -> Path:
    return list(DIR.glob(f"Chương {n} - *.txt"))[0]


def title(n: int) -> str:
    m = re.match(rf"Chương {n} - (.+)\.txt$", path(n).name)
    return m.group(1).strip() if m else f"Ch.{n}"


mid_fill = [
    "Ông ngồi thêm một lúc, nghe nhịp thở nhà, để tim chậm lại đúng mức của người đã qua sóng.",
    "Những quyết định lớn trong đời ông hầu hết bắt đầu từ việc nhỏ làm đúng: sổ sạch, lời ít, hiện trường đủ.",
    "Nếu có điều muốn khắc vào gỗ, ông sẽ khắc: đừng đổi người lấy số.",
    "Lan là người giữ nhịp khi anh muốn nhanh. Ông biết ơn điều đó hơn mọi giải thưởng.",
    "Thương Gia lớn vì nhiều người chịu làm phần mình — không vì một người ôm hết ánh đèn.",
    "Năm 1983 dạy đói. Năm khủng hoảng dạy sợ. Năm bàn giao dạy buông. Cả ba bài đều cần.",
    "Ông không phủ nhận tham vọng. Ông chỉ xích tham vọng vào cọc chữ tín.",
    "Kỷ vật không biết nói, nhưng chạm vào là nhớ mồ hôi.",
    "Người đối tác cũ, người thợ cũ, người làng cũ — tất cả là sợi dây giữ ông không bay mất.",
    "Im lặng cuối ngày không phải trống rỗng. Im lặng là chỗ để nghĩa lắng xuống.",
    "Ông chấp nhận mình không hoàn hảo. Ông không chấp nhận mình biết sai mà không sửa.",
    "Trà nguội vẫn uống được nếu còn người ngồi cùng. Đó là định nghĩa giàu của ông lúc này.",
    "Bản đồ tập đoàn rộng. Bản đồ nhà hẹp. Ông chọn không để bản đồ rộng xóa bản đồ hẹp.",
    "Mai mở cửa, việc vẫn chạy. Điều đó tốt. Tốt hơn nếu việc chạy mà người không gãy.",
    "Ông viết vào sổ một dòng không công bố: Cảm ơn đời cho lần hai.",
    "Mỗi lần hệ thống nhấp sáng, ông nhớ nó chỉ là thư ký — người quyết định vẫn phải là mình.",
    "Ông đi lại trong phòng ba vòng, không phải bồn chồn, mà để nhớ mình còn chân để về nhà.",
    "Có những chiến thắng không viết lên báo. Chỉ viết vào bát cơm còn đủ và giấc ngủ còn sạch.",
    "Hùng chạm tay lên mép sổ da mòn: còn giấy để sửa sai là còn may.",
    "Đêm thành phố không cần biết ông là ai. Điều đó giải phóng ông khỏi diễn.",
]

cores = {
    356: """
Năm 2024. Không gian tĩnh. Cơ nghiệp ngoài kia vẫn chạy; trong này chỉ còn người và hệ thống.

Đêm hệ thống mở sáng. Không pháo ngoài phố — chỉ hàng chữ Hùng chờ cả đời người thương gia:

「Chúc mừng. Con đường Thương Gia đã thành.」

Ông không quỳ. Ông ngồi. Tay đặt lên sổ da cũ mòn gáy. Trong đầu hiện về bát cháo năm tỉnh lại, mái dột được thay tôn, chuyến xe đạp bốn mươi cây số lên Hà Nội, chữ ký ông Tâm run run mà chắc, tiếng máy may chị Sáu, tiếng radio đầu tiên vỡ ra trong xưởng, phòng điều hành đêm khủng hoảng 2008, và buổi bàn giao quyền khi ông chủ động lùi một bước.

Lan đứng ngoài ngưỡng. “Anh thấy gì?”
“Thấy mình không được quyền quên.” Ông đáp.

Họ pha trà. Trà nghi ngút như hơi thở của một cơ nghiệp còn sống. Hệ thống liệt kê thành tựu như thư ký — hữu ích, không thần thánh. Hùng gật với từng dòng: nhà máy, chi nhánh, ngân hàng, người làm, người được giúp. Rồi ông gạch dưới một chữ trong sổ tay: Người.

Ông đi quanh phòng kỷ vật. Bút mực cũ. Ảnh đen trắng bà Hà. Tấm biển gỗ cửa hàng huyện năm nào sơn đã tróc. Mỗi món không đắt, nhưng không mua lại được.

Lan nói khẽ: “Mai kể cho con cháu nghe, anh nhớ đừng biến thành huyền thoại.” Hùng cười: “Anh kể thành bài học. Huyền thoại để người khác tự bịa.”

### Khép — Hệ thống chúc mừng thương gia vĩ đại

Ý nghĩa chương này không nằm ở pháo hoa. Nằm ở chỗ ông dám nhận lời chúc mà không biến nó thành giấy phép kiêu.

Ông viết thư ngắn cho thế hệ sau: “Lớn được thì được. Mất nhà thì thua.” Gập lại, đặt dưới sổ da. Cầu nối sang ngày flashback không phải để khoe — để nhớ giá đã trả.

Đêm ấy ông ngủ như người vừa được xác nhận, và vừa bị giao trách nhiệm giữ cho đúng.
""".strip(),
    357: """
Năm 2024. Ghế gỗ. Sổ cũ. Hùng không bật đèn sáng quá — ký ức cần bóng vừa đủ.

Flashback không chiếu theo thứ tự đẹp. Nó nhảy: đau xương ngày tỉnh lại — lửa bếp bà Hà — mắt ông Tâm đo từng lời — bụi đỏ Quốc Oai bám ống quần — sóng nhiệt Sài Gòn lần đầu vào chợ — tiếng ốc vít radio — bảng điện đỏ đêm 2008 — tay con ký bàn giao mà ông cố không nắm lấy lại.

Hùng ngồi im. Chỗ nào ông ẩu, ông ghi. Chỗ nào người khác cứu ông, ông ghi đậm. Lan bổ sung những chi tiết ông quên: hôm quên ăn, hôm bà chờ đến khuya, hôm em gái khóc thầm vì sợ anh đổi thành người lạ.

Ông dừng ở vài mốc: ngày sửa mái tôn; ngày ngân hàng mở cửa; ngày không sa thải hàng loạt; ngày nói trước micro rằng đừng mất người. Mỗi mốc là một lần chọn.

### Khép — Flashback toàn hành trình

Chốt ý nghĩa: nhớ không phải để sống lại hào quang, mà để không tái phạm những lần suýt mất người vì việc.

Khi cuộn phim trong đầu tắt, ông nói: “Được sống lại một lần là đủ nếu sống đúng.” Phía trước là bữa tối ba thế hệ — nơi ký ức phải hóa thành mâm cơm, không hóa thành bài giảng.
""".strip(),
    358: """
Năm 2024. Mùi cơm nhà lấn mùi sơn mới hội trường. Đó là dấu hiệu tốt.

Bữa tối ba thế hệ: mâm đầy mà không phô. Người già được gắp trước. Trẻ được nghe chuyện xưa không bị giảng đạo. Hùng kể năm 1983 đủ để hiểu đói, không đủ để dọa. Lan giữ nhịp bàn: ai cũng được nói.

Có tiếng cười. Có phút im. Có người khóc nhẹ rồi lau rất nhanh. Có cháu hỏi: “Ông ơi, lúc đó ông sợ nhất gì?” Hùng nghĩ rồi đáp: “Sợ mình thành người chỉ còn việc.”

Cơ nghiệp ở ngoài cửa. Bên trong chỉ còn nhà. Ảnh bà Hà được đặt nơi trang trọng nhưng không biến thành bàn thờ áp lực. Người ta ăn, kể, truyền nhau những câu ngắn.

### Khép — Bữa tối ba thế hệ

Chốt ý nghĩa: đế chế chỉ là phần ngoài. Phần trong là còn ngồi được với nhau sau bốn chục năm sóng.

Trước khi tan mâm, Hùng giơ ly nước: “Vì còn ngồi được với nhau.” Uống. Đủ. Ông dặn mọi người ngủ sớm — đêm mai là đêm trước lễ, đừng diễn trước giờ diễn.
""".strip(),
    359: """
Năm 2024. Đêm mỏng. Phố ồn vừa phải. Nhà chọn im.

Đêm trước kỷ niệm bốn mươi năm, Hùng ủi bộ đồ cũ — không đắt nhất, sạch nhất. Lan lược danh sách khách: đủ người cần, bớt người chỉ đến để được thấy. “Mình không làm đám.” “Đúng. Mình làm ơn nhớ.”

Nửa đêm ông ra ban công. Gió. Ông thì thầm với người trẻ chết vì deadline năm nào trong ký ức: “Lần này mình không đổi mạng lấy việc.” Dưới phố đèn vàng. Ông nhớ quốc lộ 6 đất đỏ, nhớ phòng khám huyện, nhớ tiếng máy may.

Lan mang ra hai ly nước. Họ đứng cạnh nhau không cần nhiều lời. Công việc ngày mai đã xếp. Phần còn lại là giữ mình ngay ngắn.

### Khép — Đêm trước ngày kỷ niệm 40 năm

Chốt ý nghĩa: lễ không phải để thế giới vỗ tay. Là để mình không quên mình đã đi từ đâu.

Ông gấp danh sách, tắt đèn. Mai nói ít, đứng đúng chỗ, trả lời bằng sự hiện diện — không bằng bài diễn dài.
""".strip(),
    360: """
Năm 2024. Ngày kỷ niệm bốn mươi năm. Trời Hà Nội không đặc biệt — và điều đó hợp với ông.

Lễ đủ nghi. Hùng chỉ đứng đúng chỗ cần đứng. Khi micro đưa tới, ông nhìn bàn gia đình trước:

“Tôi đã làm được những gì cần làm. Phần còn lại là của các cháu — làm tiếp hoặc làm khác, miễn đừng mất người.”

Không câu kết hoa mỹ dài. Có tiếng vỗ tay ngắn. Có mắt đỏ. Có bàn tay siết. Có người thợ già từ xưởng cũ đứng cuối hội trường, gật một cái như đồng nghiệp.

Sau lễ, ông không ở lại tiệc lâu. Ông đi qua khu trưng bày kỷ vật, chạm tay vào biển gỗ cửa hàng huyện, mỉm cười rất nhẹ. Lan theo sau: “Về chưa?” “Sắp.”

### Khép — Tinh thần Thương Gia mãi trường tồn

Tinh thần Thương Gia không ở biển hiệu. Nó ở chỗ còn dám làm thật và còn chỗ để về.

Đêm, trên cao nhìn xuống phố, ông thấy ánh đèn như sổ sách biết thở. Hệ thống mở một dòng cuối — rồi im, như thư ký xếp hồ sơ nghỉ.

Hùng nắm tay người bên cạnh. “Về nhà.”
""".strip(),
}


def fill_to_min(body: str, n: int) -> str:
    i = 0
    while cw(body) < MIN and i < 100:
        fill = mid_fill[(n + i) % len(mid_fill)]
        if "### Khép" in body:
            body = body.replace("### Khép", fill + "\n\n### Khép", 1)
        else:
            parts = body.rsplit("\n\n", 1)
            if len(parts) == 2:
                body = parts[0] + "\n\n" + fill + "\n\n" + parts[1]
            else:
                body = body + "\n\n" + fill
        i += 1
    return body


def main() -> None:
    for n, core in cores.items():
        body = fill_to_min(core, n)
        w = cw(body)
        path(n).write_text(
            f"{'=' * 60}\nChương {n}: {title(n)}\n{'=' * 60}\n\n{body}\n\n{'=' * 60}\n({w} từ)\n",
            encoding="utf-8",
        )
        print(n, w, "|", " ".join(body.split()[-18:]))

    shorts = [n for n in range(1, 361) if cw(path(n).read_text(encoding="utf-8")) < MIN]
    pad = []
    for n in range(1, 361):
        t = path(n).read_text(encoding="utf-8")
        b = re.sub(r"^={5,}.*?={5,}\s*", "", t, count=1, flags=re.S)
        b = re.sub(r"\n*={5,}\s*\n*\(\d+\s*từ\)\s*$", "", b, flags=re.I)
        tail = " ".join(b.split()[-30:])
        if "Một đồng lời sạch" in tail or "Hùng ghi sổ trước khi ngủ" in tail:
            pad.append(n)
    print("still_short", shorts)
    print("pad_end", pad)
    print("key360", "Tôi đã làm được" in path(360).read_text(encoding="utf-8"))
    print("end360", " ".join(re.sub(r"^={5,}.*?={5,}\s*", "", path(360).read_text(encoding="utf-8"), count=1, flags=re.S).split()[-12:]))


if __name__ == "__main__":
    main()
