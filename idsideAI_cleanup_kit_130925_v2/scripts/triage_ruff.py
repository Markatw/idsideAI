"""
Create summaries from qc/ruff.json:
  - qc/ruff_summary.csv (counts by code)
  - qc/ruff_by_file.csv (E9/F821/B008 counts per file)
  - qc/ruff_todo.md (prioritized checklist with hints)
"""
import json, csv
from collections import Counter, defaultdict
from pathlib import Path

SRC = Path("qc/ruff.json")
if not SRC.exists():
    raise SystemExit("Missing qc/ruff.json. Run scripts/ruff_json_report.sh first.")

data = json.loads(SRC.read_text(encoding="utf-8"))

# Summary by code
counts = Counter(item["code"] for item in data)
with open("qc/ruff_summary.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["code", "count"])
    for code, c in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
        w.writerow([code, c])

# Per-file breakdown for criticals
crit = {"E9", "F821", "B008"}
per_file = defaultdict(lambda: Counter())
for item in data:
    code = item["code"]
    if code not in crit:
        continue
    per_file[item["filename"]][code] += 1

with open("qc/ruff_by_file.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["file", "E9", "F821", "B008", "total"])
    for file, c in sorted(per_file.items(), key=lambda kv: -(kv[1]["E9"] + kv[1]["F821"] + kv[1]["B008"])):
        total = c["E9"] + c["F821"] + c["B008"]
        w.writerow([file, c["E9"], c["F821"], c["B008"], total])

# TODO markdown with hints
def hint_for(code: str) -> str:
    return {
        "E9": "Syntax error. Open file, check around line; run `python -m py_compile <file>` to pinpoint.",
        "F821": "Undefined name. Add the missing import or define the symbol. Run scripts/suggest_imports.py for hints.",
        "B008": "Function default uses mutable or call. Run scripts/fix_b008.py .",
    }.get(code, "")

lines = ["# Ruff TODO (critical first)\n"]
grouped = defaultdict(list)
for item in data:
    code = item["code"]
    if code in crit:
        grouped[code].append(item)
for code in ["E9", "F821", "B008"]:
    items = sorted(grouped.get(code, []), key=lambda i: (i["filename"], i["location"]["row"]))
    if not items:
        continue
    lines.append(f"## {code} ({len(items)}) — {hint_for(code)}\n")
    for it in items[:2500]:  # avoid huge files
        f = it["filename"]; row = it["location"]["row"]; msg = it["message"]
        lines.append(f"- [ ] `{f}:{row}` — {msg}")
    lines.append("")
Path("qc/ruff_todo.md").write_text("\n".join(lines), encoding="utf-8")
print("Wrote qc/ruff_summary.csv, qc/ruff_by_file.csv, qc/ruff_todo.md")