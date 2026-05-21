from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class PPPParseResult:
    source: Path
    status: str = "Pendente"
    message: str = "Parser PDF será implementado na próxima etapa."


def parse_ppp_ibge_pdf(pdf_path: str) -> PPPParseResult:
    """Placeholder for PPP-IBGE PDF parser."""
    return PPPParseResult(source=Path(pdf_path), status="Pendente")
