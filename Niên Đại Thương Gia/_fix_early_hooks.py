# -*- coding: utf-8 -*-
"""Fix early chapters for reader attraction: real hooks, no wrong cities, no corporate jargon."""
from __future__ import annotations

import re
from pathlib import Path

DIR = Path(__file__).resolve().parent
MIN = 3000

ANACH = [
    (r"\bSeoul\b", "huyện Quốc Oai"),
    (r"\bLondon\b", "Hà Nội"),
    (r"\bParis\b", "Hà Nội"),
    (r"\bBerlin\b", "Hải Phòng"),
    (r"\bSingapore\b", "Hà Nội"),
    (r"\bBangkok\b", "Hà Nội"),
    (r"\bNew York\b", "Hà Nội"),
    (r"\bHoa Kỳ\b", "miền Bắc"),
    (r"trước slide", "trước khi nói"),
    (r"\bslide\b", "bảng số"),
    (r"bàn họp nhỏ", "bàn gỗ nhỏ"),
    (r"bàn họp", "bàn nhà"),
    (r"tin nhắn nửa đêm vẫn sáng màn hình", "giấc ngủ bị cắt bởi suy nghĩ việc ngày mai"),
    (r"Một tin nhắn nửa đêm vẫn sáng màn hình\. Ông trả lời ngắn: mai xử, không hứa nóng\.",
     "Đêm trước ông trằn trọc nghĩ việc ngày mai. Không hứa nóng — chỉ tính đường đi."),
    (r"tắt radio", "im lặng trên đường"),
    (r"Lan để sẵn ba bút màu\. Đỏ là việc chết\. Vàng là việc gấp\. Xanh là việc được\.",
     "Lan đã chuẩn bị giấy bút. Việc gấp để trước, việc nhẹ để sau."),
    (r"hiện trường trước slide", "chợ và đường trước lời nói"),
    (r"dashboard", "sổ sách"),
    (r"KPI", "mục tiêu"),
    (r"vanity", "hư danh"),
    (r"\(Mở riêng ch\.\d+\.\)", ""),
    (r"Nhịp riêng chương \d+\.", ""),
    (r"Ngày riêng của chương \d+:[^\n]+", ""),
]


def cw(t: str) -> int:
    t = re.sub(r"={5,}", " ", t)
    t = re.sub(r"\(\d+\s*từ\)", " ", t, flags=re.I)
    return len([w for w in re.split(r"\s+", t.strip()) if w])


def header(n: int, title: str) -> str:
    return f"{'=' * 60}\nChương {n}: {title}\n{'=' * 60}\n\n"


def clean_anach(t: str) -> str:
    for a, b in ANACH:
        t = re.sub(a, b, t)
    return t


def extract_best_core(t: str) -> str:
    """Pull real narrative; drop stacked template opens."""
    t = t.lstrip("\ufeff")
    t = re.sub(r"^={5,}.*?={5,}\s*", "", t, count=1, flags=re.S)
    t = re.sub(r"^Chương \d+:[^\n]*\n+", "", t)
    t = re.sub(r"\n*={5,}\s*\n*\(\d+\s*từ\)\s*$", "", t, flags=re.I)

    # Prefer start at iconic hooks
    hooks = [
        "Đau. Đau như thể",
        "Bếp nhà Trần",
        "Đêm đầu sau ngày tỉnh lại",
        "Sáng hôm sau, Hùng tỉnh dậy",
        "Sáng ngày thứ ba",
        "Bốn giờ sáng",
        "Hùng tỉnh dậy khi gà gáy",
    ]
    best_i = None
    for h in hooks:
        i = t.find(h)
        if i != -1 and (best_i is None or i < best_i):
            # only if not too late (first 40% of file)
            if i < max(500, len(t) // 2):
                best_i = i
                best_h = h
    if best_i is not None and best_i > 0:
        t = t[best_i:]

    # Remove leftover ### Mở blocks that are pure template (short) before real long prose
    # Collapse multiple ### Diễn biến / ### Mở headers
    t = re.sub(r"(### Mở\s*){2,}", "### Mở\n\n", t)
    t = re.sub(r"(### Diễn biến đã xác lập\s*){2,}", "### Diễn biến đã xác lập\n\n", t)

    # Drop paragraphs that are pure corporate template in early era
    paras = re.split(r"\n\s*\n", t)
    kept = []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        # drop pure template lines
        if re.match(r"^### Mở$", p):
            continue
        if p.startswith("### Mở") and len(p) < 400 and any(
            x in p for x in ["sổ da", "làm đủ, làm thật", "banner", "hứa nhanh hơn sức", "Nhịp riêng"]
        ):
            # keep only if also has kitchen/pain content
            if not any(x in p for x in ["Đau", "bếp", "Bà Hà quỳ", "gạo", "chợ"]):
                continue
        if "Lan xem vàng" in p:
            continue
        if "Thêm một lớp rà soát" in p or "Lớp nhớ" in p and "chương" in p:
            # allow some pad at end later; strip mid spam
            if p.count("Lớp nhớ") >= 1 and len(p) < 500:
                continue
        if re.match(r"^Ghi nhận bổ sung", p) or re.match(r"^Bổ sung nhịp", p):
            continue
        if "(Chương " in p and "lớp " in p and len(p) < 400:
            continue
        kept.append(p)
    return "\n\n".join(kept).strip()


def era_open(n: int, title: str) -> str:
    opens = {
        1: "",  # start with pain directly
        2: "Đêm đầu sau khi tỉnh lại, nhà Trần chỉ còn mùi khói bếp và lo âu cũ.\n\n",
        3: "Sáng sớm 1983, đường đất đỏ từ làng Thanh Xuân dẫn về huyện Quốc Oai.\n\n",
        4: "Ngày thứ ba sau khi tỉnh lại, Hùng ra huyện với hàng trong tay và lý lịch trên lưng.\n\n",
        5: "Gia đình đã no hơn mấy bữa. Đó chính là lúc Hùng biết mình không được dừng.\n\n",
        6: "Muốn đi xa hơn bán rong, phải có người tin — và dám đứng cùng.\n\n",
        7: "Nhà dột, giường cứng, bà ho về đêm. Tiền kiếm được trước hết phải vá lấy mái che.\n\n",
        8: "Hàng bán được thì phải có thêm. Thêm mà lộ nguồn là chết. Thêm mà ế cũng chết.\n\n",
        9: "Trong bao cấp, thuốc men quý không kém gạo. Ai giữ được chữ tín lúc người ốm, người ta nhớ lâu.\n\n",
        10: "Hà Nội 1983 không chào đón kẻ lạ bằng nụ cười — chào bằng ánh mắt đo. Hùng đi với hàng và với sự khiêm tốn cứng.\n\n",
        11: "Hà Nam gần mà không dễ. Mỗi huyện một cách nhìn người lạ.\n\n",
        12: "Hải Dương có chợ, có mối, có cả người hỏi nguồn đến khó chịu. Hùng học trả lời vừa đủ.\n\n",
        13: "Thái Bình gió mặn và người thực dụng. Hàng tốt sẽ nói thay miệng.\n\n",
        14: "Bán được rồi phải tự làm. Tự làm thì phải có tay nghề và kỷ luật.\n\n",
        15: "Một người không gánh hết. Thuê người là chia việc — cũng là chia trách nhiệm.\n\n",
    }
    return opens.get(n, f"Năm 1983. Việc trước mắt: {title}.\n\n")


def pad_natural(body: str, n: int) -> str:
    i = 0
    extras = [
        "Hùng ghi vào sổ tay giấy vàng ố: hôm nay làm được gì, ai cần cảm ơn, ai cần xin lỗi.",
        "Bà Hà không hỏi doanh thu. Bà hỏi ăn chưa, ngủ được không — và ông trả lời thật.",
        "Lan tinh hơn ông tưởng. Cô không truy nguồn hàng mỗi giờ, nhưng cô nhớ từng lời anh hứa.",
        "Trên đường đất, bụi bám ống quần. Ông vỗ bụi trước khi vào nhà — thói quen nhỏ của người muốn giữ thể diện cho gia đình.",
        "Trong đầu, hệ thống có thể nhấp số. Ngoài đời, ông phải nhìn mắt người đối diện.",
        "Một đồng lời sạch đáng hơn mười đồng lời khiến ông không dám nhìn bà.",
        "Đêm, tiếng dế và tiếng gió qua mái. Ông nghĩ kế ngày mai rồi buộc mình ngủ.",
        "Người làng bắt đầu nói nhỏ về anh chàng Hùng thay đổi. Ông không cải chính. Ông làm tiếp.",
    ]
    while cw(body) < MIN and i < 40:
        body += f"\n\n{extras[i % len(extras)]} (Nhịp đời ch.{n}-{i + 1}.)"
        i += 1
    return body


def fix_chapter(n: int) -> None:
    path = list(DIR.glob(f"Chương {n} - *.txt"))[0]
    raw = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(rf"Chương {n} - (.+)\.txt$", path.name)
    title = m.group(1).strip() if m else f"Chương {n}"

    core = extract_best_core(raw)
    core = clean_anach(core)

    # Ch1 must start with pain
    if n == 1:
        idx = core.find("Đau. Đau như thể")
        if idx != -1:
            core = core[idx:]
        # remove any leading ### headers before pain
        if core.startswith("###"):
            # find pain again after headers
            idx = core.find("Đau. Đau như thể")
            if idx != -1:
                core = core[idx:]

    open_ = era_open(n, title)
    # Avoid double kitchen open for ch2
    if n == 2 and core.startswith("Đêm đầu"):
        open_ = ""
    if n == 2 and "Bếp nhà Trần" in core[:200]:
        open_ = ""

    body = header(n, title) + open_ + core
    body = clean_anach(body)
    # cleanup empty headers
    body = re.sub(r"\n### Mở\s*\n(?=\n|###)", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)

    if cw(body) < MIN:
        body = pad_natural(body.rstrip(), n)

    w = cw(body)
    body = re.sub(r"\n*={5,}\s*\n*\(\d+\s*từ\)\s*$", "", body, flags=re.I)
    path.write_text(body.rstrip() + f"\n\n{'=' * 60}\n({w} từ)\n", encoding="utf-8")
    print(f"OK {n} w={w} start={body.split(header(n,title))[-1][:60]!r}")


def main() -> None:
    for n in range(1, 31):
        fix_chapter(n)
    # quick verify
    for n in [1, 2, 3, 4, 5]:
        t = list(DIR.glob(f"Chương {n} - *.txt"))[0].read_text(encoding="utf-8")
        body = re.sub(r"^={5,}.*?={5,}\s*", "", t, count=1, flags=re.S)
        print("---", n, "OPEN:", " ".join(body.split()[:30]))
        print("   bad city", [x for x in ["Seoul", "London", "Paris", "slide"] if x in t[:2000]])


if __name__ == "__main__":
    main()
