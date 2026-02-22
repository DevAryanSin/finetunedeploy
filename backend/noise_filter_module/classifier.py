"""
Import bridge to the legacy module folder with spaces in its name.
"""

from pathlib import Path
import sys

_LEGACY_DIR = Path(__file__).resolve().parents[1] / "Noise filter module"
if str(_LEGACY_DIR) not in sys.path:
    sys.path.insert(0, str(_LEGACY_DIR))

from classifier import classify_chunks  # type: ignore  # noqa: E402,F401

