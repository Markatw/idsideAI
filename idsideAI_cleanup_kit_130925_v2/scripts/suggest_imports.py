"""
Generate import suggestions for Ruff F821 (undefined name).
Expects Ruff JSON at qc/ruff.json (use scripts/ruff_json_report.sh first).
Writes suggestions into qc/suggestions/<file>.imports.txt
"""
import json, os
from collections import defaultdict
from pathlib import Path

RUFF_JSON = Path("qc/ruff.json")
OUT_DIR = Path("qc/suggestions")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Common symbols -> import line suggestions (extend as needed)
SUGGEST = {
    "Request": "from fastapi import Request",
    "Depends": "from fastapi import Depends",
    "APIRouter": "from fastapi import APIRouter",
    "HTTPException": "from fastapi import HTTPException",
    "status": "from fastapi import status",
    "JSONResponse": "from fastapi.responses import JSONResponse",
    "Path": "from fastapi import Path",
    "Query": "from fastapi import Query",
    "Body": "from fastapi import Body",
    "BaseModel": "from pydantic import BaseModel",
    "Field": "from pydantic import Field",
    "Any": "from typing import Any",
    "Dict": "from typing import Dict",
    "List": "from typing import List",
    "Optional": "from typing import Optional",
    "timezone": "from datetime import timezone",
    "timedelta": "from datetime import timedelta",
    "datetime": "from datetime import datetime",
    "jwt": "import jwt",
    "pd": "import pandas as pd",
    "np": "import numpy as np",
    "PathlibPath": "from pathlib import Path as PathlibPath",
}

def main():
    if not RUFF_JSON.exists():
        print("Missing qc/ruff.json. Run scripts/ruff_json_report.sh first.")
        return
    data = json.loads(RUFF_JSON.read_text(encoding="utf-8"))
    by_file = defaultdict(lambda: defaultdict(list))  # file -> name -> messages
    for item in data:
        code = item.get("code")
        if code != "F821":
            continue
        filename = item.get("filename")
        msg = item.get("message", "")
        # Extract undefined name from message: "undefined name 'X'"
        name = None
        if "undefined name" in msg:
            parts = msg.split("'")
            if len(parts) >= 2:
                name = parts[1]
        if filename and name:
            by_file[filename][name].append(msg)
    for file, missing in by_file.items():
        out = []
        out.append(f"# Import suggestions for {file}\n")
        for name in sorted(missing.keys()):
            suggestion = SUGGEST.get(name)
            if suggestion:
                out.append(f"- {name}: `{suggestion}`")
            else:
                out.append(f"- {name}: (no mapping yet)")
        (OUT_DIR / (Path(file).name + ".imports.txt")).write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote suggestions for {len(by_file)} files into qc/suggestions/")

if __name__ == "__main__":
    main()