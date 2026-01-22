"""
Utility functions for report generation.
"""

import base64
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import zipfile
import io

# Placeholder for ampersand - used to preserve & in docxtpl paragraph loops
# docxtpl strips & in {% for %} loops, so we use a placeholder and post-process
AMP_PLACEHOLDER = '___AMP___'


def replace_amp_with_placeholder(text: str) -> str:
    """Replace & with placeholder for docxtpl rendering.
    
    docxtpl strips & in paragraph loops ({% for %}), so we use a placeholder
    that gets replaced back to &amp; after the DOCX is generated.
    """
    if not text:
        return text
    return str(text).replace('&', AMP_PLACEHOLDER)


def format_date(date_input) -> str:
    """Format a date for display in reports.
    
    Args:
        date_input: Can be datetime, string, or None
        
    Returns:
        Formatted date string (e.g., "22 January 2026")
    """
    if not date_input:
        return datetime.now(timezone.utc).strftime('%d %B %Y')
    
    if isinstance(date_input, datetime):
        return date_input.strftime('%d %B %Y')
    
    if isinstance(date_input, str):
        # Try parsing common date formats
        for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%SZ']:
            try:
                dt = datetime.strptime(date_input.split('.')[0].replace('Z', ''), fmt.replace('.%f', '').replace('Z', ''))
                return dt.strftime('%d %B %Y')
            except ValueError:
                continue
        return date_input
    
    return str(date_input)


def format_assessment_date(date_input) -> str:
    """Format assessment date for display."""
    return format_date(date_input)


def create_heatmap_for_template(heatmap_bytes: bytes) -> str:
    """Convert heatmap bytes to base64 data URL for HTML templates."""
    if not heatmap_bytes:
        return ''
    base64_data = base64.b64encode(heatmap_bytes).decode('utf-8')
    return f"data:image/png;base64,{base64_data}"


def post_process_ampersands(docx_bytes: bytes) -> bytes:
    """Replace ampersand placeholders with proper XML entity in DOCX.
    
    After docxtpl renders the template, we need to replace our placeholder
    with the proper XML-escaped ampersand (&amp;).
    """
    try:
        # Open the DOCX as a ZIP file
        input_buffer = io.BytesIO(docx_bytes)
        output_buffer = io.BytesIO()
        
        with zipfile.ZipFile(input_buffer, 'r') as zip_in:
            with zipfile.ZipFile(output_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                for item in zip_in.infolist():
                    data = zip_in.read(item.filename)
                    
                    # Only process XML files
                    if item.filename.endswith('.xml'):
                        try:
                            text = data.decode('utf-8')
                            # Replace placeholder with XML-escaped ampersand
                            text = text.replace(AMP_PLACEHOLDER, '&amp;')
                            data = text.encode('utf-8')
                        except UnicodeDecodeError:
                            pass  # Keep binary data as-is
                    
                    zip_out.writestr(item, data)
        
        output_buffer.seek(0)
        return output_buffer.getvalue()
        
    except Exception as e:
        print(f"Warning: Failed to post-process ampersands: {e}")
        return docx_bytes


def calculate_tier(percentage: float, assessment_type: str = 'System') -> str:
    """Calculate maturity tier based on percentage score.
    
    Args:
        percentage: Score as percentage (0-100)
        assessment_type: Type of assessment for tier thresholds
        
    Returns:
        Tier name (e.g., "Leading", "Established", "Developing", "Foundational")
    """
    if assessment_type == 'Awareness':
        return calculate_awareness_tier(percentage)
    elif assessment_type == 'Readiness':
        return calculate_readiness_tier(percentage)
    elif assessment_type == 'Orgwide':
        return calculate_orgwide_tier(percentage)
    else:
        return calculate_system_tier(percentage)


def calculate_awareness_tier(percentage: float) -> str:
    """Calculate tier for Awareness assessments."""
    if percentage >= 75:
        return 'Leading'
    elif percentage >= 50:
        return 'Established'
    elif percentage >= 25:
        return 'Developing'
    else:
        return 'Foundational'


def calculate_readiness_tier(percentage: float) -> str:
    """Calculate tier for Readiness assessments."""
    if percentage >= 75:
        return 'Leading'
    elif percentage >= 50:
        return 'Established'
    elif percentage >= 25:
        return 'Developing'
    else:
        return 'Foundational'


def calculate_orgwide_tier(percentage: float) -> str:
    """Calculate tier for Org-wide assessments."""
    if percentage >= 75:
        return 'Leading'
    elif percentage >= 50:
        return 'Established'
    elif percentage >= 25:
        return 'Developing'
    else:
        return 'Foundational'


def calculate_system_tier(percentage: float) -> str:
    """Calculate tier for System assessments."""
    if percentage >= 75:
        return 'Leading'
    elif percentage >= 50:
        return 'Established'
    elif percentage >= 25:
        return 'Developing'
    else:
        return 'Foundational'


def get_tier_for_score(score: float) -> str:
    """Get tier based on raw score (1-4 scale)."""
    if score >= 3.5:
        return 'Leading'
    elif score >= 2.5:
        return 'Established'
    elif score >= 1.5:
        return 'Developing'
    else:
        return 'Foundational'


def get_maturity_description(score: float) -> str:
    """Get description for maturity level based on score."""
    if score >= 3.5:
        return "Leading practices with continuous improvement"
    elif score >= 2.5:
        return "Established processes with room for optimization"
    elif score >= 1.5:
        return "Developing capabilities with foundational elements in place"
    else:
        return "Foundational stage with significant improvement opportunities"


# Domain color mapping
DOMAIN_COLORS = {
    'Fairness': '#FF6B6B',
    'Transparency': '#4ECDC4', 
    'Explainability': '#45B7D1',
    'Accountability': '#96CEB4',
    'Data Integrity': '#FFEAA7',
    'Reliability': '#DDA0DD',
    'Security': '#98D8C8',
    'Privacy': '#F7DC6F',
    'Safety': '#BB8FCE',
    'Inclusivity': '#85C1E9',
    'Sustainability': '#82E0AA'
}
