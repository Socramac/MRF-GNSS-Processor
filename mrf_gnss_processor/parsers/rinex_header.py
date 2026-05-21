from pathlib import Path
from typing import Dict, Optional


def parse_rinex_header(obs_path: str) -> Dict[str, Optional[str]]:
    """Minimal RINEX header parser. Full implementation will be expanded in v0.2."""
    path = Path(obs_path)
    info = {"file": path.name, "version": None, "receiver": None, "antenna": None, "approx_position_xyz": None, "antenna_delta_hen": None}
    with path.open("r", encoding="latin-1", errors="ignore") as f:
        for line in f:
            label = line[60:].strip() if len(line) >= 60 else ""
            value = line[:60].strip()
            if "RINEX VERSION" in label:
                info["version"] = value.split()[0]
            elif "REC # / TYPE / VERS" in label:
                info["receiver"] = value
            elif "ANT # / TYPE" in label:
                info["antenna"] = value
            elif "APPROX POSITION XYZ" in label:
                info["approx_position_xyz"] = value
            elif "ANTENNA: DELTA H/E/N" in label:
                info["antenna_delta_hen"] = value
            elif "END OF HEADER" in label:
                break
    return info
