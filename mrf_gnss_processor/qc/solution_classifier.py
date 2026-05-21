from pathlib import Path
from typing import Dict

QUALITY_CODES = {"1": "FIX", "2": "FLOAT", "4": "DGPS", "5": "SINGLE"}


def classify_pos_file(pos_path: str) -> Dict[str, float | str | int]:
    counts = {"FIX": 0, "FLOAT": 0, "DGPS": 0, "SINGLE": 0, "INVALID": 0}
    total = 0
    path = Path(pos_path)
    if not path.exists():
        return {"solution": "SEM SOLUÇÃO", "epochs": 0, "fix_percent": 0.0}
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if not line.strip() or line.startswith("%"):
                continue
            parts = line.split()
            if len(parts) < 6:
                continue
            q = parts[5]
            sol = QUALITY_CODES.get(q, "INVALID")
            counts[sol] += 1
            total += 1
    fix_percent = (counts["FIX"] / total * 100.0) if total else 0.0
    if total == 0:
        solution = "SEM SOLUÇÃO"
    elif fix_percent >= 80:
        solution = "FIX"
    elif counts["FLOAT"] > 0:
        solution = "FLOAT"
    elif counts["SINGLE"] > 0 or counts["DGPS"] > 0:
        solution = "BAIXA QUALIDADE"
    else:
        solution = "SEM SOLUÇÃO"
    return {"solution": solution, "epochs": total, "fix_percent": round(fix_percent, 2), **counts}
