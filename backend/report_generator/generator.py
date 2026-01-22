"""
AM AI SAFE Report Generator - Main Module
This module serves as a facade that imports from the legacy monolith
while progressively migrating to modular components.

The refactoring strategy:
1. Keep the original report_generator.py working as-is
2. Create new modular components (charts, utils, ai_narratives, etc.)
3. Update this file to import from new modules
4. Eventually, this file will orchestrate all modular components

Current status:
- charts.py: Extracted (heatmap, bar chart, radar chart)
- utils.py: Extracted (formatting, ampersand handling, tier calculations)
- ai_narratives.py: TODO
- template_context.py: TODO
"""

# For now, re-export from the legacy monolith to maintain API compatibility
import sys
from pathlib import Path

# Add backend to path for imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Import the main class from legacy monolith
from report_generator_legacy import AMReportGenerator

# Also expose the new modular components for gradual migration
from . import charts
from . import utils

__all__ = [
    'AMReportGenerator',
    'charts',
    'utils',
]
