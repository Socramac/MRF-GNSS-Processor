from pathlib import Path
from typing import List

NAV_SUFFIXES = ["N", "G", "B", "L", "P", "nav", "gnav", "rnx"]


def detect_nav_files(obs_path: str) -> List[Path]:
    """Detect navigation files in the same folder, based on the observation filename stem."""
    path = Path(obs_path)
    folder = path.parent
    stem = path.stem
    candidates = []
    for p in folder.iterdir():
        if not p.is_file() or p == path:
            continue
        ext = p.suffix.lstrip(".")
        if ext.lower() in {"nav", "gnav", "rnx"}:
            candidates.append(p)
        elif len(ext) == 3 and ext[:2].isdigit() and ext[2].upper() in {"N", "G", "B", "L", "P"}:
            candidates.append(p)
        elif p.stem == stem and ext.upper() in NAV_SUFFIXES:
            candidates.append(p)
    return candidates
