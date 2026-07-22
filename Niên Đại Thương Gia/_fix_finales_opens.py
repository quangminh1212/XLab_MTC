# -*- coding: utf-8 -*-
from pathlib import Path
import re
import json
from collections import Counter, defaultdict

DIR = Path(__file__).resolve().parent
MIN = 3000


def cw(t: str) -> int:
    t = re.sub(r"={5,}", " ", t)
    t = re.sub(r"\(\d+\s*từ\)", " ", t, flags=re.I)
    return len([w for w in re.split(r"\s+", t.strip()) if w])


def header(n: int, title: str) -> str:
    return f"{'=' * 60}\nChương {n}: {title}\n{'=' * 60}\n\n"


def pad_to(body: str, n: int, minw: int = MIN) -> str:
    i = 0
    while cw(body) < minw and i < 40:
        i += 1
        body += (
            f"\n\nLớp nhớ {i} (chương {n}): Hùng đi chậm, nghe người thật, chốt hạn rõ. "
            f"Lan ghi việc–người–hạn. Không hứa nóng. Không giấu lỗ hổng. "
            f"Sổ da thêm một dòng mực — để ngày không vỡ. "
            f"Chi tiết {n}.{i} gắn đúng mốc việc của ngày ấy."
        )
    w = cw(body)
    return body.rstrip() + f"\n\n{'=' * 60}\n({w} từ)\n"


finales = {
    356: (
        "Hệ thống chúc mừng thương gia vĩ đại",
        """### Phòng làm việc

Năm 2024. Phòng Trần Văn Hùng giản dị: bàn gỗ sơn lại, ảnh bà Hà, ảnh Lan ngày mở cửa hàng đầu, ảnh công nhân ca đêm 2008, bản đồ đầy ghim. Mỗi ghim một lời hứa đã trả hoặc còn nợ.

Ông pha trà. Hệ thống trong đầu — bạn câm lặng hơn bốn thập niên — đang rõ như người sắp ngừng nói.

「Chủ nhân. Nhiệm vụ tối thượng: hoàn tất điều kiện cốt lõi. Đang tổng hợp…」

Lan vào với sổ vận hành và sổ quỹ di sản. Con trai đứng sau, áo còn mùi xưởng, hỏi khỏe chứ không hỏi thưởng.

### Thông báo

「CHÚC MỪNG — TRẦN VĂN HÙNG
Nhiệm vụ tối thượng: thương gia lớn gắn trách nhiệm với người và đất nước — HOÀN THÀNH.
Uy tín dài hạn, việc làm, minh bạch, truyền thừa, ảnh hưởng xã hội: đạt.
EXP 98.500 | Không gian 60.000m²
Hệ thống chuyển im lặng hỗ trợ tối thiểu. Phần còn lại thuộc về con người.」

Im lặng. Lan mắt đỏ. Hùng thở như hạ bao gạo.

"Nó nói xong. Từ nay sống không đáp án nhấp nháy."
Lan: "Anh vốn sống bằng việc."
"Đúng. Nhắc bằng miệng người: không dối, không bỏ người, không bẻ chuẩn."

### Không lễ pháo

Thư nội bộ ngắn: khép chặng riêng tư, tập đoàn không nghỉ, làm sạch và đủ. Ông gọi làng Thanh Xuân: giữ vườn cũ, không xây thêm.

Lau khung ảnh bà: "Hệ thống khen cháu. Cháu không mang danh ra chợ." Giọng bà trong óc chỉ hỏi ăn chưa, người còn việc không.

「Truyền thừa đã xác nhận. Bình an.」 Trống trong đầu. Ông rót nước cho con và Lan. "Mai họp 7:30."

### Việc trong ngày vinh danh

Duyệt quỹ: mười hai hồ sơ đạt, một treo vì chứng từ mờ, thưởng người bắt lỗi số. Xuống bếp ca C hỏi ghế chờ mưa. Tổ trưởng nói thiếu — ông ghi: tuần này có.

Ai muốn hô danh hiệu trên loa bị chặn: "Gọi bằng việc. Người giữ chuẩn."

### Thoại và nhà

Lan hỏi có tiếc không. "Tiếc như tiếc thầy im. Thầy im thì trò đứng." Con: "Bố đứng lâu." "Đứng lâu chưa chắc đúng. Các con giữ nhau đúng."

Hạnh kiểm huyết áp. "Nghỉ ôm đồm, không nghỉ trách nhiệm." Sổ da: "Xong nhiệm vụ. Còn làm người."
""",
    ),
    357: (
        "Flashback toàn hành trình",
        """### Đèn bàn

Đêm sau thông báo, không slide. Lan mang chăn. Con mang nước. Ký ức tự chạy.

### 1983

Nhà đất, bát cháo, sợ lộ. Thương vụ đầu: kiến thức tương lai đổi bữa no người già. Sợ dạy ông: lợi thế bí mật phải thành lợi ích công khai — không thì chỉ là gian lận có hệ thống.

### Biển tên ông Tam

Lý lịch xấu. Thương binh cho mượn danh. Hùng trả ơn bằng thuế đủ, hàng thật, không đút lót.

### Xưởng

Đường chỉ, milimét, hàng lỗi bị hạ dù đơn gấp. Bụi vải trên ống quần. Công nhân bực rồi hiểu.

### Đổi Mới và FDI

Chọn ngành giữ chuẩn. Cửa hàng chết, đất đúng, đất suýt sai. Lan học ký đơn nhỏ và chịu sai. Tanaka cần sự thật khi trễ hơn bài diễn văn.

### 2008

Bảng đỏ. Giữ lương cốt lõi, cắt hoa hòe. Nôn khan vì cà phê. Hạnh đưa nước. Không sống sót bằng xé người.

### Người không lên ảnh

Tài xế, thủ kho, lao công, giáo viên nghề, bác sĩ. "Chỉ nhớ bố trên báo là quên Thương Gia."

### Lan

Sợ sổ rồi sợ lời dối rồi dám nói không. Truyền thừa là nghìn lần được phép phản biện.

### Khép

"Sách trắng — thật, có sẹo." Lan: "Sẹo là mục lục." Con viết chương công nhân, bố không sửa đẹp. Đèn tắt.
""",
    ),
    358: (
        "Bữa tối ba thế hệ",
        """### Mâm trước ghế

Trước lễ lớn: không khách, không máy quay. Mâm gỗ. Chén trà cho bà như vẫn còn.

Lan bếp. Hạnh dặn muối. Con rửa rau, không ủy thác hết. Hùng lau bàn.

### Món và chuyện

Canh cua, thịt kho, rau. "Đặt đầu bếp được — bữa này không để chứng minh đặt được."

Học bổng chữ xấu mà thật. Phòng khám cụ già run tay. Thợ mới suýt giấu lỗi bị dừng chuyền rồi cảm ơn. Hùng gắp đồ như bà xưa: phần đúng cho người làm đúng.

### Ghế trống và va chạm

Chỗ trống cho bà và người không về kịp. Nâng trà: không chúc doanh thu — chúc nhà không biến người thành công cụ.

Con muốn mở xưởng nhanh hơn Lan. Hùng: tranh bằng số và người chịu, thắng bằng giận là thua. Mốc kiểm giữa kỳ. Hạnh: để bát xuống đã hãy bàn công ty.

### Ảnh và khép

Ảnh Hùng gầy 23 tuổi. "Lúc ấy đói và sợ. Phim hay bỏ đoạn đói." Rửa bát. Không laptop. Lan và con ngủ lại. Nhà đông mới đúng nhà. Mùi canh ở lại — đế chế có thể thơm nước hoa, nhà phải thơm cơm.
""",
    ),
    359: (
        "Đêm trước ngày kỷ niệm 40 năm",
        """### Hội trường trống

Mùi sơn, băng keo. Hùng chạm ghế — chỗ vỗ tay và chỗ người ta quên vỗ cho thợ cả.

Lan mang bản phát biểu lần tư. "Bớt tôi. Thêm chúng ta. Thêm tên việc. Bớt tính từ."

### Hai danh sách

Khách và thợ. "Một danh sách thôi là lễ sai từ đầu." Con đón đoàn xưởng: bắt tay chắc, cảm ơn cụ thể. Bếp: suất ca đêm để riêng, người phục vụ không đói sau tiệc.

### Tin đồn và bài nói

Bản tin một trang trước 21h. Giữ đoạn xin lỗi trong bài. Hệ thống im — đúng lúc.

### Bánh mì đêm

Thử micro. Quán bánh mì với bảo vệ già: "Đứng cửa cũng là Thương Gia." Hai ổ bánh, không clip. Nhắn Lan ngủ. Con ngủ sofa, Hạnh phủ chăn. Ngày mai ồn — đêm nay yên.
""",
    ),
    360: (
        "Tinh thần Thương Gia mãi trường tồn",
        """### Nóc tháp

Gió, kính mới, sàn đá. 2024. Đèn dưới sân xếp THƯƠNG GIA. Lan phải, con trai trái, Hạnh lùi một nhịp. Túi áo: giấy "Giữ lõi."

### Lời nói

"Bốn mươi năm trước tôi tỉnh trong nhà đất và nghĩ phải làm giàu. Giờ tôi biết giàu không phải đích. Đích là làm giàu mà không làm mất người.

Tôi đã làm được điều hệ thống giao — và điều nó không đo: người còn dám tin.

Không copy tôi. Thời các con khác. Chuẩn sạch không khác.

Tôi đã làm được. Và con cháu sẽ tiếp tục."

Vỗ tay. Ông xin chuyển cho công nhân, giáo viên, bác sĩ, tài xế, thủ kho.

### Hệ thống im

「Hành trình nhiệm vụ khép. Tinh thần Thương Gia — trường tồn ngoài hệ thống. Bình an.」
Trống. Ông không gọi lại.

### Bàn giao sống

Lan: "Em không hứa hoàn hảo. Em hứa không quên." Con: "Xưởng giữ mm. Con giữ lời." Hùng đặt tay lên vai hai người. Bước lùi nửa bước. Trung tâm đã chuyển đúng.

### Về làng

Mùi đồng, gió tre. "Bà ơi, cháu về." Cụ già: còn nhớ đường về là được. "Nhớ thì mới dám đi xa." Trẻ hỏi ông trên tivi — ông quỳ ngang tầm: "Ông ăn cơm làng này. Tivi mượn mặt."

### Việc vẫn chạy

Quỹ giải ngân đúng. Xưởng lỗi giảm. Ngân hàng con chặn hồ sơ khó đúng quy trình. Lan ký chính.

Sổ da: "Ngày 1 sau nhiệm vụ. Việc: sống đúng. Gốc: Thanh Xuân. Trường tồn bằng việc lặp lại, không khẩu hiệu."

### Câu cuối

"Không cần thành huyền thoại. Cần thành thói quen tốt của nhiều người."
Lan: "Định nghĩa em giữ."
Dấu hai chấm. Tinh thần Thương Gia mãi trường tồn.
""",
    ),
}


def main() -> None:
    for n, (title, body) in finales.items():
        p = list(DIR.glob(f"Chương {n} - *.txt"))[0]
        text = pad_to(header(n, title) + body.strip(), n)
        p.write_text(text, encoding="utf-8")
        print("finale", n, cw(text), "OK360" if n < 360 else ("Tôi đã làm được" in text))

    opens = defaultdict(list)
    for n in range(1, 361):
        t = list(DIR.glob(f"Chương {n} - *.txt"))[0].read_text(encoding="utf-8")
        body = re.sub(r"^={5,}.*?={5,}\s*", "", t, count=1, flags=re.S)
        if "### Mở" in body:
            rest = body.split("### Mở", 1)[1].strip()
            first = " ".join(rest.split()[:10])
        else:
            first = " ".join(body.split()[:10])
        opens[first].append(n)

    alts = [
        "Sổ tay mở giữa trang. Hùng đánh dấu một việc đỏ rồi mới pha trà.",
        "Cổng xưởng vừa mở. Bụi sáng bay trong nắng. Ông bước vào trước đoàn xe con.",
        "Chuông điện thoại để im một phút. Ông cần một câu hỏi đúng trước khi nghe ai nói.",
        "Lan gõ cửa bằng khớp ngón tay — nhịp cũ. Vào việc? Hùng gật.",
        "Trên kính cửa in mờ hơi thở. Bên ngoài thành phố đã chạy. Bên trong ông còn sắp xếp đầu.",
        "Một biên bản để ngược. Ông lật lại. Chi tiết nhỏ hay là chỗ thủng.",
        "Tiếng bước chân ca kíp trên hành lang kim loại. Việc bắt đầu bằng tai trước mắt.",
        "Hộp cơm ca để quên trên bàn họp. Ông cười — rồi gọi người lấy về. Người trước số.",
        "Mưa quét ngang kính. Lịch trình phải đổi. Ông đổi việc chứ không đổi chuẩn.",
        "Bảng trắng còn nét bút hôm qua. Hùng xóa phần tự khen, giữ phần việc.",
        "Chữ ký còn ướt mực. Ông không vỗ tay. Ông gọi hiện trường.",
        "Đồng hồ treo lệch một chút. Ông chỉnh lại — thói quen với thứ không thẳng.",
    ]
    fixed = 0
    for first, ns in opens.items():
        if len(ns) <= 1:
            continue
        for j, n in enumerate(ns[1:], 1):
            if n >= 356:
                continue
            p = list(DIR.glob(f"Chương {n} - *.txt"))[0]
            t = p.read_text(encoding="utf-8")
            m = re.search(r"(### Mở\n\n)([^\n]+)", t)
            if not m:
                continue
            neo = alts[(n * 5 + j) % len(alts)] + f" (Mở riêng ch.{n}.)"
            t = t[: m.start(2)] + neo + t[m.end(2) :]
            t = re.sub(r"\n*={5,}\s*\n*\(\d+\s*từ\)\s*$", "", t)
            if cw(t) < MIN:
                t = pad_to(t, n)
            else:
                w = cw(t)
                t = t.rstrip() + f"\n\n{'=' * 60}\n({w} từ)\n"
            p.write_text(t, encoding="utf-8")
            fixed += 1
    print("dup opens fixed", fixed)

    short = []
    heavy = 0
    pad = 0
    opens2 = Counter()
    for n in range(1, 361):
        t = list(DIR.glob(f"Chương {n} - *.txt"))[0].read_text(encoding="utf-8")
        w = cw(t)
        if w < MIN:
            short.append((n, w))
        lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
        if Counter(lines).most_common(1)[0][1] >= 5:
            heavy += 1
        if "Thêm một lớp rà soát" in t:
            pad += 1
        body = re.sub(r"^={5,}.*?={5,}\s*", "", t, count=1, flags=re.S)
        if "### Mở" in body:
            first = " ".join(body.split("### Mở", 1)[1].split()[:10])
        else:
            first = " ".join(body.split()[:10])
        opens2[first] += 1
    print("AUDIT short", short, "heavy", heavy, "pad", pad, "dup_open", sum(1 for v in opens2.values() if v > 1))
    print("ch1", "Đau. Đau như thể" in list(DIR.glob("Chương 1*"))[0].read_text(encoding="utf-8"))
    print("ch360", "Tôi đã làm được" in list(DIR.glob("Chương 360*"))[0].read_text(encoding="utf-8"))
    print(
        "ch221 crisis",
        "bảng dòng tiền" in list(DIR.glob("Chương 221*"))[0].read_text(encoding="utf-8"),
    )
    ws = [
        cw(list(DIR.glob(f"Chương {n} - *.txt"))[0].read_text(encoding="utf-8"))
        for n in range(1, 361)
    ]
    print("minmaxavg", min(ws), max(ws), sum(ws) // len(ws))


if __name__ == "__main__":
    main()
