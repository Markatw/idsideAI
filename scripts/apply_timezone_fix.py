from datetime import timezone
import re, sys
from pathlib import Path

pattern = re.compile(r"\bdatetime\.utcnow\s*\(\s*\)")
import_pat = re.compile(r"^\s*from\s+datetime\s+import\s+timezone\b", re.M)

def process_file(p: Path)->bool:
    try: s = p.read_text(encoding="utf-8")
    except Exception: return False
    if "datetime.now(timezone.utc)" not in s: return False
    new_s = pattern.sub("datetime.now(timezone.utc)", s)
    if "datetime.now(timezone.utc)" in new_s and not import_pat.search(new_s):
        lines = new_s.splitlines(); inserted=False
        for i,line in enumerate(lines[:20]):
            if line.strip().startswith("from datetime import"):
                lines.insert(i+1, "from datetime import timezone"); inserted=True; break
        if not inserted: lines.insert(0, "from datetime import timezone")
        new_s = "\n".join(lines)
    if new_s != s:
        p.with_suffix(p.suffix+".bak").write_text(s, encoding="utf-8")
        p.write_text(new_s, encoding="utf-8")
        return True
    return False

def main():
    base = Path(sys.argv[1]) if len(sys.argv)>1 else Path(".")
    changed=0
    for p in base.rglob("*.py"):
        if p.name.endswith(".bak"): continue
        if process_file(p): changed+=1
    print(f"[timezone_fix] Modified files: {changed}")
if __name__ == "__main__": main()