from __future__ import annotations

import subprocess
import sys
from pathlib import Path


MARKER_FILE = ".first_launch_deps_ok"
REQUIREMENTS_CANDIDATES = ("requirements.txt", "requirment.txt")
MIN_PYTHON = (3, 10)
MAX_PYTHON_EXCLUSIVE = (3, 12)


def _is_supported_python() -> bool:
    return MIN_PYTHON <= sys.version_info[:2] < MAX_PYTHON_EXCLUSIVE


def _format_version(version: tuple[int, int]) -> str:
    return f"{version[0]}.{version[1]}"


def _find_requirements_file(base_dir: Path) -> Path | None:
    for filename in REQUIREMENTS_CANDIDATES:
        req_path = base_dir / filename
        if req_path.exists():
            return req_path
    return None


def ensure_dependencies() -> None:
    """Install project dependencies once on the very first launch."""
    if not _is_supported_python():
        current = _format_version(sys.version_info[:2])
        min_supported = _format_version(MIN_PYTHON)
        max_supported = _format_version((MAX_PYTHON_EXCLUSIVE[0], MAX_PYTHON_EXCLUSIVE[1] - 1))
        raise RuntimeError(
            "Version de Python non supportée pour ce projet. "
            f"Version détectée: {current}. "
            f"Utilisez Python entre {min_supported} et {max_supported} (inclus), puis relancez le jeu."
        )

    base_dir = Path(__file__).resolve().parent
    marker_path = base_dir / MARKER_FILE

    if marker_path.exists():
        return

    requirements_path = _find_requirements_file(base_dir)
    if requirements_path is None:
        return

    print("[setup] Vérification des dépendances du projet...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)]
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "Échec de l'installation des dépendances. "
            "Sur Windows, utilisez un environnement Python 3.10 ou 3.11 puis exécutez: "
            f'"{sys.executable} -m pip install -r {requirements_path}".'
        ) from exc

    marker_path.write_text("ok\n", encoding="utf-8")
    print("[setup] Dépendances installées et validées.")
