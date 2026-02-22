"""
Compatibility package for noise-filter imports used by the API.
Adds the legacy 'Noise filter module' directory to sys.path so that
bare imports (from classifier, prompts, schema, etc.) resolve correctly.
"""

from pathlib import Path
import sys

_LEGACY_DIR = Path(__file__).resolve().parents[1] / "Noise filter module"
if str(_LEGACY_DIR) not in sys.path:
    sys.path.insert(0, str(_LEGACY_DIR))
