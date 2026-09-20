"""Root conftest for Project 04.

Adds the project directory to sys.path so the 'app' package is importable
when running tests from the repository root.
"""

import sys
from pathlib import Path

_PROJECT_ROOT = str(Path(__file__).parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
