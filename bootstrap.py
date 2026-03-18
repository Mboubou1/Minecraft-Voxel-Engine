from __future__ import annotations

import subprocess
import sys
from pathlib import Path


MARKER_FILE = ".first_launch_deps_ok"
REQUIREMENTS_CANDIDATES = ("requirements.txt", "requirment.txt")


def _find_requirements_file(base_dir: Path) -> Path | None:
    for filename in REQUIREMENTS_CANDIDATES:
        req_path = base_dir / filename
        if req_path.exists():
            return req_path
    return None


def ensure_dependencies() -> None:
    """Install project dependencies once on the very first launch."""
    base_dir = Path(__file__).resolve().parent
    marker_path = base_dir / MARKER_FILE

    if marker_path.exists():
        return

    requirements_path = _find_requirements_file(base_dir)
    if requirements_path is None:
        return

    print("[setup] Vérification des dépendances du projet...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)]
    )
    marker_path.write_text("ok\n", encoding="utf-8")
    print("[setup] Dépendances installées et validées.")
