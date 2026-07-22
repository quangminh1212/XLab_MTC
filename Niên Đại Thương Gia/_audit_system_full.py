# -*- coding: utf-8 -*-
"""Full system + quality audit for Niên Đại Thương Gia (360 ch)."""
import os, re, json, glob
from collections import Counter, defaultdict

base = os.path.dirname(os.path.abspath(__file__))
os.chdir(base)

files = sorted(
    glob.glob("Chương *.txt"),
    key=lambda p: int(re.search(r"Chương (\d+)", p).group(1)),
)
print("count", len(files))

milestones = {
    60: dict(exp=7800, space=3500),
    130: dict(exp=19500, space=6200),
    200: dict(exp=38000, space=12000),
    270: dict(exp=62000, space=25000),
    330: dict(exp=81000, space=45000),
    360: dict(exp=98500, space=60000),
}

part_ends = {
    50: "part1 mid",
    60: "part1 end target",
    89: "part2 sum titles",
    105: "part3 sum titles",
    112: "part3 done title",
    130: "part2 end target",
    155: "bank",
    200: "part3 end",
    221: "crisis 2008",
    240: "crisis boom",
    270: "part4 end",
    300: "succession",
    330: "part5 end",
    354: "final mission",
    355: "mission complete",
    356: "system congrats",
    360: "finale",
}

pad_markers = [
    "Thêm một lớp rà soát",
    "không còn dòng đỏ bỏ quên",
    "Hùng ghi sổ trước khi ngủ",
    "Một đồng lời sạch",
    "bụi đỏ bám ống quần",
    "(Nhịp chương",
    "Ba câu trước khi ngủ",
    "Uy tín đi trước tiếng rao",
    "Khi mệt, ông nhớ bát cháo",
    "Người ngoài bàn tán",
    "Hiện trường dạy nhiều hơn phòng điều hành",
]


def to_int(s):
    if s is None:
        return None
    s = str(s).replace(".", "").replace(",", "")
    try:
        return int(s)
    except Exception:
        return None


def read(fp):
    with open(fp, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


rows = []
early_system_lines = defaultdict(list)

for fp in files:
    n = int(re.search(r"Chương (\d+)", fp).group(1))
    text = read(fp)
    lines = text.splitlines()
    words = len(re.findall(r"\S+", text))

    exp_vals = [to_int(m.group(1)) for m in re.finditer(
        r"(?:Tổng\s*)?EXP\s*[:=]?\s*([+\-]?\d{1,3}(?:[.,]\d{3})*|\d+)", text, re.I
    )]
    exp_vals = [v for v in exp_vals if v is not None]

    exp_plus = []
    for m in re.finditer(r"EXP\s*\+\s*(\d+)|(?:\+|cộng|nhận)\s*(\d{1,6})\s*EXP", text, re.I):
        v = to_int(m.group(1) or m.group(2))
        if v is not None:
            exp_plus.append(v)

    spaces = []
    for m in re.finditer(
        r"(?:không gian|Space|space|kho không gian)[^\n]{0,80}?(\d{1,3}(?:[.,]\d{3})*|\d+)\s*m",
        text,
        re.I,
    ):
        spaces.append(to_int(m.group(1)))
    for m in re.finditer(
        r"(\d{1,3}(?:[.,]\d{3})*|\d+)\s*m[²2][^\n]{0,40}?(?:không gian|kho|Space)",
        text,
        re.I,
    ):
        spaces.append(to_int(m.group(1)))
    spaces = [s for s in spaces if s is not None]

    money_hits = re.findall(
        r"(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?)\s*(đồng|tỷ|triệu)", text
    )

    brackets = re.findall(r"[「【]([^」】]{3,100})[」】]", text)
    pad = sum(text.count(p) for p in pad_markers)

    lc = Counter(l.strip() for l in lines if l.strip() and len(l.strip()) > 20)
    maxrep = max(lc.values()) if lc else 0
    maxrep_line = lc.most_common(1)[0][0][:60] if lc else ""

    # opening: first non-empty non-header
    open_parts = []
    for l in lines:
        s = l.strip()
        if not s:
            continue
        if s.startswith("Chương ") and " - " in s[:40]:
            continue
        if s.startswith("===="):
            continue
        open_parts.append(s)
        if len(" ".join(open_parts)) > 100:
            break
    open_text = " ".join(open_parts)[:100]

    lasts = [l.strip() for l in lines if l.strip()]
    last_line = lasts[-1][:80] if lasts else ""
    has_khep = "### Khép" in text or "### Khép" in text
    has_dialogue = ('"' in text) or ("\u201c" in text) or ("«" in text) or (text.count('"') >= 2)
    family = any(k in text for k in ["bà Hà", "Bà Hà", "Lan", "Hạnh", "mâm", "bữa"])
    has_sys_kw = bool(re.search(r"HỆ THỐNG|Hệ thống|「|【Hệ", text))

    # anachronism early
    bad_early = []
    if n <= 20:
        for tok in ["Seoul", "London", "Paris", "Singapore", "slide", "KPI", "SKU", "info.json", "Facebook", "Mercedes", "billboard", "tin nhắn", "màn hình"]:
            if tok.lower() in text.lower() or tok in text:
                # allow if memory
                bad_early.append(tok)

    rows.append(
        dict(
            n=n,
            words=words,
            exp_vals=exp_vals[-8:],
            exp_n=len(exp_vals),
            last_exp=exp_vals[-1] if exp_vals else None,
            exp_plus=exp_plus[:10],
            spaces=spaces[-6:],
            last_space=spaces[-1] if spaces else None,
            space_n=len(spaces),
            money_n=len(money_hits),
            brackets=len(brackets),
            bracket_sample=brackets[:3],
            pad=pad,
            maxrep=maxrep,
            maxrep_line=maxrep_line,
            open=open_text,
            last=last_line,
            khep=has_khep,
            dialogue=has_dialogue,
            family=family,
            sys_kw=has_sys_kw,
            bad_early=bad_early,
            title=re.search(r"Chương \d+ - (.+)\.txt", fp).group(1),
        )
    )

    if n <= 25 or n in milestones or n in part_ends:
        for m in re.finditer(
            r".{0,15}(?:Tổng\s*EXP|EXP\s*[+=:]|không gian[^\n]{0,40}\d|Space[^\n]{0,30}\d|nhiệm vụ[^\n]{0,50}|Kỹ năng[^\n]{0,40}).{0,50}",
            text,
            re.I,
        ):
            early_system_lines[n].append(re.sub(r"\s+", " ", m.group(0)).strip()[:120])

print("=== SUMMARY ===")
print("words min/avg/max", min(r["words"] for r in rows), round(sum(r["words"] for r in rows) / len(rows)), max(r["words"] for r in rows))
print("short <3000", sum(1 for r in rows if r["words"] < 3000))
print("short <2800", sum(1 for r in rows if r["words"] < 2800))
print("ch with EXP number", sum(1 for r in rows if r["exp_n"] > 0))
print("ch with space m2", sum(1 for r in rows if r["space_n"] > 0))
print("ch with money digits", sum(1 for r in rows if r["money_n"] > 0))
print("ch pad>0", sum(1 for r in rows if r["pad"] > 0))
print("maxrep>=5", sum(1 for r in rows if r["maxrep"] >= 5))
print("maxrep>=3", sum(1 for r in rows if r["maxrep"] >= 3))
print("has ### Khép", sum(1 for r in rows if r["khep"]))
print("has dialogue", sum(1 for r in rows if r["dialogue"]))
print("has family", sum(1 for r in rows if r["family"]))
print("has sys kw/brackets", sum(1 for r in rows if r["sys_kw"] or r["brackets"] > 0))
print("brackets only", sum(1 for r in rows if r["brackets"] > 0))

print("\n=== EARLY EXP TRAIL 1-40 ===")
for r in rows[:40]:
    if r["exp_n"] or r["space_n"] or r["exp_plus"]:
        print(
            f"ch{r['n']:3d} w={r['words']} lastEXP={r['last_exp']} vals={r['exp_vals']} plus={r['exp_plus'][:6]} space={r['last_space']} spvals={r['spaces']} pad={r['pad']} maxrep={r['maxrep']}"
        )

print("\n=== MILESTONE / KEY CHAPTERS ===")
for n, label in sorted(part_ends.items()):
    r = next(x for x in rows if x["n"] == n)
    tgt = milestones.get(n)
    print(f"ch{n:3d} [{label}] w={r['words']} lastEXP={r['last_exp']} exp_n={r['exp_n']} space={r['last_space']} br={r['brackets']} pad={r['pad']} maxrep={r['maxrep']}")
    print(f"      title={r['title']}")
    print(f"      open={r['open'][:70]!r}")
    print(f"      last={r['last'][:70]!r}")
    if tgt:
        ok_e = r["last_exp"] == tgt["exp"] if r["last_exp"] else False
        # allow any exp val match
        any_e = tgt["exp"] in r["exp_vals"]
        any_s = tgt["space"] in r["spaces"]
        print(f"      TARGET exp={tgt['exp']} space={tgt['space']} | match_exp={any_e or ok_e} match_space={any_s}")
    if early_system_lines.get(n):
        for h in early_system_lines[n][:6]:
            print("      SYS:", h)

print("\n=== SYSTEM LINES ch1-20 (full samples) ===")
for n in range(1, 21):
    lines = early_system_lines.get(n, [])
    print(f"-- ch{n} ({len(lines)}) --")
    for h in lines[:10]:
        print(" ", h)

print("\n=== DOUBLE BOOK (conflicting Tổng EXP) ===")
for r in rows[:25]:
    totals = r["exp_vals"]
    uniq = sorted(set(totals))
    if len(uniq) >= 2:
        print(f"ch{r['n']}: unique EXP numbers in text={uniq} plus={r['exp_plus']}")

print("\n=== DUP OPENS >=3 ===")
oc = Counter(r["open"][:45] for r in rows)
for k, v in oc.most_common(20):
    if v >= 3:
        print(v, repr(k))

print("\n=== DUP LAST LINES top ===")
lc2 = Counter(r["last"][:50] for r in rows)
for k, v in lc2.most_common(15):
    print(v, repr(k))

print("\n=== SHORT CHAPTERS ===")
for r in rows:
    if r["words"] < 3000:
        print(f"ch{r['n']} w={r['words']} {r['title']}")

print("\n=== HIGH PAD / MAXREP ===")
for r in rows:
    if r["pad"] >= 2 or r["maxrep"] >= 5:
        print(f"ch{r['n']} pad={r['pad']} maxrep={r['maxrep']} line={r['maxrep_line']!r}")

print("\n=== EARLY ANACHRONISM ===")
for r in rows[:30]:
    if r["bad_early"]:
        print(f"ch{r['n']}", r["bad_early"])

print("\n=== KEY PHRASES ===")
checks = [
    (1, "Đau. Đau"),
    (1, "Đau"),
    (2, "bà Hà"),
    (360, "Tôi đã làm được"),
    (360, "Về nhà"),
    (155, "Ngân hàng"),
    (221, "2008"),
    (300, "Lan"),
    (356, "Hệ thống"),
    (355, "hoàn thành"),
]
for n, phrase in checks:
    r = next(x for x in rows if x["n"] == n)
    fp = next(f for f in files if re.search(rf"Chương {n} ", f) or re.search(rf"Chương {n} -", f))
    # fix match
    fp = [f for f in files if int(re.search(r"Chương (\d+)", f).group(1)) == n][0]
    t = read(fp)
    print(f"ch{n} {phrase!r}: {phrase in t} (ci={phrase.lower() in t.lower()})")

# outline compare
print("\n=== OUTLINE vs FILE TITLES ===")
try:
    outline = json.load(open("chapter_outline.json", encoding="utf-8"))
except Exception as e:
    print("outline load fail", e)
    outline = None

omap = {}
if isinstance(outline, list):
    for item in outline:
        if not isinstance(item, dict):
            continue
        num = item.get("n") or item.get("chapter") or item.get("ch") or item.get("id")
        title = item.get("title") or item.get("t") or item.get("name")
        if num is not None:
            omap[int(num)] = title
elif isinstance(outline, dict):
    chs = outline.get("chapters") or outline.get("chapter_list") or outline
    if isinstance(chs, list):
        for item in chs:
            if isinstance(item, dict):
                num = item.get("n") or item.get("chapter") or item.get("ch")
                title = item.get("title") or item.get("t")
                if num is not None:
                    omap[int(num)] = title
    elif isinstance(chs, dict):
        for k, v in chs.items():
            if str(k).isdigit():
                if isinstance(v, dict):
                    omap[int(k)] = v.get("title") or v.get("t") or v.get("name")
                else:
                    omap[int(k)] = str(v)[:80]

print("outline mapped", len(omap))
mismatch = []
for n, t in omap.items():
    ft = next((r["title"] for r in rows if r["n"] == n), "")
    if not t:
        continue
    ts, fs = str(t).strip(), ft.strip()
    if ts == fs or ts in fs or fs in ts:
        continue
    # token overlap
    tt = set(re.findall(r"\w+", ts.lower()))
    ff = set(re.findall(r"\w+", fs.lower()))
    if tt and ff and len(tt & ff) / max(1, len(tt)) >= 0.4:
        continue
    mismatch.append((n, fs, ts[:70]))
print("title mismatches", len(mismatch))
for x in mismatch[:40]:
    print(x)

# sample generic close patterns
print("\n=== GENERIC KHÉP / SYSTEM CLOSE patterns count ===")
patterns = [
    r"tiến độ",
    r"ghi nhận",
    r"sổ cái",
    r"Tổng EXP",
    r"EXP \+",
    r"không gian",
    r"cầu nối",
    r"### Khép",
]
for p in patterns:
    c = sum(1 for r in rows if re.search(p, read([f for f in files if int(re.search(r'Chương (\d+)', f).group(1))==r['n']][0]), re.I))
    print(p, c)

# save compact report
report = {
    "summary": {
        "chapters": len(rows),
        "words_min": min(r["words"] for r in rows),
        "words_avg": round(sum(r["words"] for r in rows) / len(rows)),
        "words_max": max(r["words"] for r in rows),
        "short_lt_3000": [r["n"] for r in rows if r["words"] < 3000],
        "with_exp": sum(1 for r in rows if r["exp_n"] > 0),
        "with_space": sum(1 for r in rows if r["space_n"] > 0),
        "with_money": sum(1 for r in rows if r["money_n"] > 0),
        "pad_gt0": sum(1 for r in rows if r["pad"] > 0),
        "maxrep_ge5": sum(1 for r in rows if r["maxrep"] >= 5),
        "khep": sum(1 for r in rows if r["khep"]),
        "title_mismatch": len(mismatch),
    },
    "milestones": {},
    "early_exp": [],
    "mismatches": mismatch[:80],
}
for n, tgt in milestones.items():
    r = next(x for x in rows if x["n"] == n)
    report["milestones"][str(n)] = {
        "target": tgt,
        "last_exp": r["last_exp"],
        "exp_vals": r["exp_vals"],
        "last_space": r["last_space"],
        "spaces": r["spaces"],
        "title": r["title"],
        "words": r["words"],
    }
for r in rows[:40]:
    report["early_exp"].append(
        {"n": r["n"], "last_exp": r["last_exp"], "vals": r["exp_vals"], "plus": r["exp_plus"], "space": r["last_space"]}
    )

with open("_audit_system_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print("\nWrote _audit_system_report.json")
