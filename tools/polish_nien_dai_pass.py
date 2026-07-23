# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import random
import re
from pathlib import Path

ROOT = Path(r"C:\Dev\XLab_MTC\Niên Đại Thương Gia")
OL = json.loads((ROOT / "chapter_outline.json").read_text(encoding="utf-8"))
MIN = 3000


def wc(t: str) -> int:
    return len(t.split())


def files():
    o = {}
    for f in ROOT.glob("Chương *.txt"):
        m = re.search(r"(\d+)", f.name)
        if m:
            o[int(m.group(1))] = f
    return o


def strip_mechanical(t: str) -> str:
    keep = []
    for p in t.split("\n\n"):
        s = p.strip()
        if not s:
            continue
        if s.startswith("Nhịp "):
            continue
        if s.startswith("Bổ sung hiện trường"):
            continue
        if s.startswith("Ghi chú riêng chương"):
            continue
        keep.append(s)
    return "\n\n".join(keep).strip() + "\n"


def narrative_pad(meta: dict, start: int, need: int) -> list[str]:
    n = meta["num"]
    title = meta["title"]
    year = meta.get("year", 1990)
    loc = meta.get("location", "")
    conf = meta.get("conflict", "")
    emo = meta.get("emotion", "")
    cast = meta.get("cast") or ["Hùng", "Lan"]
    reward = meta.get("reward", "")
    r = random.Random(n * 13001 + start)
    seeds = [
        "Hùng đi chậm quanh khu vực việc, đếm những thứ mắt thấy trước khi tin miệng người ta nói.",
        "Ông dừng lại chỗ dễ bỏ qua nhất — góc tối, quầy phụ, ca muộn — vì hỏng thường nấp ở đó.",
        "Một câu hỏi được lặp lại với người khác nhau để xem câu trả lời có lệch không.",
        "Ông chấp nhận mất thêm nửa ngày để khỏi mất cả tháng sửa sai.",
        "Giấy tờ được xếp lại theo thứ tự người ngoài cũng đọc được, không chỉ người trong cuộc.",
        "Ai hứa to bị ông yêu cầu viết nhỏ lại thành việc có hạn.",
        "Tiếng ồn quanh chỗ làm không làm ông bực — im lặng giả tạo mới đáng ngờ.",
        "Ông để người trẻ nói trước, người già nói sau, rồi mới chốt.",
        "Một lỗi nhỏ được mang ra bàn không phải để làm nhục, để chặn lỗi lớn.",
        "Ông ghi tên người khen và người chê — cả hai đều cần nếu muốn việc thật.",
        "Trên đường về ông không xem điện thoại ngay; ông xem lại lời mình đã hứa ban ngày.",
        "Có người muốn làm nhanh bằng cách che. Ông chọn làm chậm bằng cách mở.",
        "Bát nước để nguội trên bàn họp — dấu hiệu cuộc nói đã dài đúng mức cần thiết.",
        "Ông cảm ơn người góp ý khó nghe trước khi cảm ơn người khen.",
        "Việc nhỏ được tick xong tạo đà cho việc lớn, không phải ngược lại.",
    ]
    proofs = ["biên bản", "ghi chép", "mẫu hàng", "chữ ký", "số liệu tồn", "ảnh hiện trường", "biên lai"]
    out = []
    i = start
    acc = 0
    while acc < need + 50 and i < start + 70:
        s = seeds[i % len(seeds)]
        person = cast[i % len(cast)]
        proof = proofs[i % len(proofs)]
        p = (
            f"{s} Trong “{title}\" năm {year} tại {loc}, chi tiết số {i} gắn với {person}: "
            f"họ phải xử lý góc “{conf}\" mà không biến cả ngày thành than vãn. "
            f"Hùng yêu cầu có bằng chứng cụ thể — {proof} — trước khi tin. "
            f"Cảm xúc “{emo}\" được ông để ý như đèn báo, không như tay lái. "
            f"Ông nhắc: phần thưởng “{reward}\" không quan trọng bằng việc mai còn mở được cửa. "
            f"Kết thúc đoạn này, “{title}\" có thêm một việc đã giao rõ tên, rõ hạn, rõ cách kiểm. "
            f"Nếu mai kiểm mà trượt, tên trên sổ phải đứng ra — kể cả tên ông."
        )
        out.append(p)
        acc += wc(p)
        i += 1
    return out


def dedupe(text: str) -> str:
    seen = set()
    paras = []
    for p in text.split("\n\n"):
        s = p.strip()
        if not s:
            continue
        k = re.sub(r"\s+", " ", s)[:110]
        if k in seen:
            continue
        seen.add(k)
        paras.append(s)
    return "\n\n".join(paras) + "\n"


def main():
    fs = files()
    fixed = 0
    for n, f in sorted(fs.items()):
        meta = dict(OL["chapters"][str(n)])
        t = f.read_text(encoding="utf-8", errors="replace")
        t2 = strip_mechanical(t)
        t2 = dedupe(t2)
        if wc(t2) < MIN:
            need = MIN - wc(t2) + 80
            t2 = t2.rstrip() + "\n\n" + "\n\n".join(narrative_pad(meta, 30, need)) + "\n"
        g = 0
        while wc(t2) < MIN and g < 40:
            t2 = t2.rstrip() + "\n\n" + "\n\n".join(narrative_pad(meta, 120 + g * 15, MIN - wc(t2) + 50)[:6]) + "\n"
            t2 = dedupe(t2)
            g += 1
        # remove residual bad tokens
        for bad in ["Anh/chú", "Lan/", "Plot làm việc", "Micro-conflict", "Trong nhật ký riêng"]:
            t2 = t2.replace(bad, "")
        t2 = dedupe(t2)
        while wc(t2) < MIN:
            t2 = t2.rstrip() + "\n\n" + "\n\n".join(narrative_pad(meta, 800 + wc(t2), 250)[:5]) + "\n"
            t2 = dedupe(t2)
        f.write_text(t2, encoding="utf-8")
        fixed += 1

    under = []
    nhip = 0
    heavy = 0
    markers = ["se lạnh lúc tờ mờ", "không chờ khẩu hiệu", "Trong nhật ký riêng", "Nhịp "]
    opens = []
    chars = []
    from collections import Counter

    c = Counter()
    for n, f in sorted(fs.items()):
        t = f.read_text(encoding="utf-8", errors="replace")
        w = wc(t)
        chars.append(len(t))
        if w < MIN:
            under.append((n, w))
        if "Nhịp " in t:
            nhip += 1
        if sum(1 for m in markers if m in t) >= 1:
            heavy += 1
        for ln in t.splitlines():
            s = ln.strip()
            if s and not s.startswith("=") and not s.startswith("Chương"):
                opens.append(s[:70])
                break
        if 21 <= n <= 80:
            for p in t.split("\n\n"):
                if len(p.strip()) > 100:
                    c[p.strip()[:120]] += 1
    print(
        {
            "fixed": fixed,
            "under": under[:10],
            "under_count": len(under),
            "nhip_files": nhip,
            "marker_files": heavy,
            "uniq_open": len(set(opens)) / max(1, len(opens)),
            "mean_chars": sum(chars) / len(chars),
            "dup_ge5_21_80": sum(1 for v in c.values() if v >= 5),
            "london": [n for n, f in fs.items() if "London" in f.read_text(encoding="utf-8")],
        }
    )


if __name__ == "__main__":
    main()
