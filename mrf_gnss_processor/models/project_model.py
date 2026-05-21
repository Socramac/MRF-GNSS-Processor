from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class PPPModel:
    source_pdf: Optional[Path] = None
    station_name: str = ""
    epoch: str = "2000.4"
    crs: str = "SIRGAS2000"
    utm_e: Optional[float] = None
    utm_n: Optional[float] = None
    h_ellipsoidal: Optional[float] = None
    h_normal: Optional[float] = None
    hgeo_hnor: Optional[float] = None
    antenna_height: Optional[float] = None


@dataclass
class ObservationFile:
    obs_path: Path
    role: str = "ROVER"  # BASE, ROVER, IGNORAR
    start_utc: str = ""
    end_utc: str = ""
    duration_seconds: int = 0
    interval_seconds: float = 1.0
    antenna_height: Optional[float] = None
    nav_files: List[Path] = field(default_factory=list)
    status: str = "Aguardando"


@dataclass
class RoverResult:
    rover_name: str
    solution: str = "Aguardando"
    fix_percent: Optional[float] = None
    epochs: int = 0
    sigma_n: Optional[float] = None
    sigma_e: Optional[float] = None
    sigma_u: Optional[float] = None
    rms_h: Optional[float] = None
    rms_v: Optional[float] = None
    pdop_mean: Optional[float] = None
    baseline_m: Optional[float] = None
    pos_file: Optional[Path] = None
    stat_file: Optional[Path] = None
    log: str = ""


@dataclass
class ProjectModel:
    name: str = "MRF_PROJETO_001"
    crs: str = "SIRGAS 2000 / UTM zone 19S"
    ppp: PPPModel = field(default_factory=PPPModel)
    observations: List[ObservationFile] = field(default_factory=list)
    results: List[RoverResult] = field(default_factory=list)
