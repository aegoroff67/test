"""
AM AI SAFE Report Generator - Modular Components Package

This package contains refactored components extracted from the monolithic
report_generator.py file for better maintainability.

Modules:
- charts: Chart generation (heatmap, bar chart, radar chart)
- utils: Utility functions (formatting, tier calculations, etc.)
- ai_narratives: AI-generated narrative content

Usage:
    from report_modules.charts import generate_heatmap, generate_radar_chart
    from report_modules.utils import format_date, replace_amp_with_placeholder
    from report_modules.ai_narratives import generate_system_narratives
"""

from . import charts
from . import utils
from . import ai_narratives

__all__ = ['charts', 'utils', 'ai_narratives']


