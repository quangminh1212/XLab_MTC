"""Fix only confirmed current-timeline errors; preserve legitimate flashbacks."""
import json, re
from pathlib import Path

P = Path(r'C:/Dev/XLab_MTC/Niên Đại Thương Gia')
with open(P / 'system_ledger.json', encoding='utf-8') as f:
    ledger = json.load(f)['chapters']

changes = []

def chapter(n):
    paths = list(P.glob(f'Chương {n} - *.txt'))
    if len(paths) != 1:
        raise RuntimeError(f'Ch{n}: expected 1 file, got {len(paths)}')
    return paths[0]

def replace_year(n, old, new, *, all_occurrences=True):
    f = chapter(n)
    text = f.read_text(encoding='utf-8')
    count = text.count(str(old))
    if not count:
        return
    if all_occurrences:
        out = text.replace(str(old), str(new))
        done = count
    else:
        out = text.replace(str(old), str(new), 1)
        done = 1
    f.write_text(out, encoding='utf-8')
    changes.append((n, f'{old}->{new}', done))

# Ch61–71 are a continuous operational arc. Every 1992 reference here describes
# the current plan/result, not a flashback. Use each chapter's canonical ledger year.
for n in range(61, 72):
    target = ledger[str(n)]['year']
    replace_year(n, 1992, target)

# 2008 crisis arc. Ch223–237 canonical 2008; Ch238–240 canonical 2009.
# Existing 2003 references describe current meetings/results, not memories.
for n in range(223, 241):
    target = ledger[str(n)]['year']
    replace_year(n, 2003, target)

# Technology / succession sequence. 2006 is stale generator year; canonical 2010.
for n in range(249, 254):
    target = ledger[str(n)]['year']
    replace_year(n, 2006, target)

# Ch155 opens the bank in the ledger's 1991 sequence. Replace current-scene 1992.
replace_year(155, 1992, ledger['155']['year'])

# Early chapters: transaction counters are not final chapter totals. Rename labels
# to prevent double-book interpretation while preserving every earned amount/event.
for n in range(3, 10):
    f = chapter(n)
    text = f.read_text(encoding='utf-8')
    out = re.sub(r'- Tổng EXP:\s*([^\n」]+)', r'- Tiến độ EXP của nhiệm vụ lúc này: \1', text)
    out = re.sub(r'Tổng EXP hôm nay:', r'EXP nhận trong giao dịch này:', out)
    if out != text:
        f.write_text(out, encoding='utf-8')
        changes.append((n, 'clarify intermediate EXP labels', 1))

print(f'changed records: {len(changes)}')
for row in changes:
    print(row)
