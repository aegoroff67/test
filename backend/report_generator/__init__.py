"""
AM AI SAFE Report Generator Package
Modular report generation for assessment reports.
"""

# Re-export the main class from the legacy monolith for backward compatibility
import sys
from pathlib import Path

# Ensure the backend directory is in path
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Import submodules
from . import charts
from . import utils

__all__ = ['charts', 'utils']

