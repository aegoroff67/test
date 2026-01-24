"""
Chart generation module for reports.
Contains functions for generating heatmaps, bar charts, and radar charts.
"""

import io
from typing import Dict, Any, List
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def get_maturity_color(score: int) -> str:
    """Get color for maturity score (1-4 scale)."""
    if score == 1:
        return '#FF0000'  # Red - Foundational
    elif score == 2:
        return '#FFC000'  # Orange - Developing
    elif score == 3:
        return '#FFFF00'  # Yellow - Established
    elif score == 4:
        return '#00B050'  # Green - Leading
    else:
        return '#CCCCCC'  # Gray - No score/unanswered


def generate_awareness_heatmap(report_data: Dict[str, Any]) -> bytes:
    """Generate heatmap image for Awareness assessments (5 domains, 5 questions each)."""
    heatmap_data = report_data.get('heatmap_data', {})
    domains = heatmap_data.get('domains', [])
    
    if not domains:
        domains = [{'name': 'No Data', 'questions': [{'code': 'N/A', 'score': 0} for _ in range(5)]}]
    
    # Create figure - sized for 5x5 grid
    fig, ax = plt.subplots(figsize=(10, 7))
    
    num_domains = len(domains)
    num_questions = 5  # Fixed at 5 questions per domain for Awareness
    
    for i, domain in enumerate(domains):
        domain_name = domain.get('name', 'Unknown')
        questions = domain.get('questions', [])
        
        # Calculate percentage score
        answered_questions = [q for q in questions if q.get('score', 0) > 0]
        total_possible = len(answered_questions) * 4 if answered_questions else 1
        total_actual = sum(q.get('score', 0) for q in answered_questions)
        percentage = (total_actual / total_possible * 100) if total_possible > 0 else 0
        
        # Only draw cells for actual questions (max 5)
        row_pos = num_domains - 1 - i
        for j, question in enumerate(questions[:num_questions]):
            score = question.get('score', 0)
            question_code = question.get('code', 'N/A')
            
            color = get_maturity_color(score)
            rect = patches.Rectangle((j, row_pos), 1, 1, 
                                   linewidth=1, edgecolor='white', facecolor=color)
            ax.add_patch(rect)
            
            if question_code != 'N/A':
                ax.text(j+0.5, row_pos+0.5, question_code, 
                       ha='center', va='center', color='white', 
                       fontsize=9, fontweight='bold')
        
        # Add domain name and percentage on the left
        ax.text(-0.2, row_pos+0.5, f"{domain_name} ({percentage:.0f}%)", 
               ha='right', va='center', fontsize=10, fontweight='normal')
    
    # Set axis properties - limit to exactly 5 columns
    ax.set_xlim(-4.5, num_questions)
    ax.set_ylim(-1.5, num_domains)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Add legend at bottom
    legend_y = -1.0
    legend_items = [
        ('#FF0000', 'Foundational (1)'),
        ('#FFC000', 'Developing (2)'),
        ('#FFFF00', 'Established (3)'),
        ('#00B050', 'Leading (4)')
    ]
    
    legend_start_x = 0
    for idx, (color, label) in enumerate(legend_items):
        x_pos = legend_start_x + (idx * 1.5)
        rect = patches.Rectangle((x_pos, legend_y), 0.3, 0.3, facecolor=color, edgecolor='gray')
        ax.add_patch(rect)
        ax.text(x_pos + 0.4, legend_y + 0.15, label, fontsize=8, va='center')
    
    plt.tight_layout()
    
    # Save to bytes
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
               facecolor='white', edgecolor='none', pad_inches=0.2)
    plt.close(fig)
    buffer.seek(0)
    
    return buffer.getvalue()


def generate_system_heatmap(report_data: Dict[str, Any]) -> bytes:
    """Generate heatmap image for System assessments (11 domains, 8 questions each)."""
    heatmap_data = report_data.get('heatmap_data', {})
    domains = heatmap_data.get('domains', [])
    
    if not domains:
        # Create minimal empty heatmap
        domains = [{'name': 'No Data', 'questions': [{'code': 'N/A', 'score': 0} for _ in range(8)]}]
    
    # Create figure with optimized height for compact rows
    fig, ax = plt.subplots(figsize=(12, 6.5))
    
    # Create the heatmap grid
    num_domains = len(domains)
    
    for i, domain in enumerate(domains):
        domain_name = domain['name']
        questions = domain['questions']
        
        # Calculate percentage score for left side
        total_possible = len([q for q in questions if q['code'] != 'N/A']) * 4  # 1-4 scale
        total_actual = sum(q['score'] for q in questions if q['code'] != 'N/A')
        percentage = (total_actual / total_possible * 100) if total_possible > 0 else 0
        
        for j, question in enumerate(questions[:8]):  # Only 8 questions per domain
            score = question['score']
            question_code = question['code']
            
            # Draw colored rectangle (invert i so lowest scores are at top)
            row_pos = num_domains - 1 - i
            color = get_maturity_color(score)
            rect = patches.Rectangle((j, row_pos), 1, 1, 
                                   linewidth=1, edgecolor='white', facecolor=color)
            ax.add_patch(rect)
            
            # Add question code text (white text on colored background)
            if question_code != 'N/A':
                ax.text(j+0.5, row_pos+0.5, question_code, 
                       ha='center', va='center', color='white', 
                       fontsize=10, fontweight='bold')
        
        # Add domain name above percentage with minimal spacing
        ax.text(-1.9, row_pos+0.65, domain_name, 
               ha='left', va='center', fontsize=9, fontweight='normal')
        ax.text(-1.9, row_pos+0.35, f'({percentage:.1f}%)', 
               ha='left', va='center', fontsize=7, color='gray')
    
    # Set axis properties for compact layout
    ax.set_xlim(-2.2, 8)
    ax.set_ylim(0, num_domains)
    # Note: Do NOT use set_aspect('equal') here - it forces the output to be square
    # which makes the heatmap look like a radar chart. The figsize should control dimensions.
    
    # Remove ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(left=0.2)
    
    # Save to bytes
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', 
               facecolor='white', edgecolor='none')
    img_buffer.seek(0)
    img_bytes = img_buffer.getvalue()
    plt.close(fig)
    
    return img_bytes


def generate_heatmap(report_data: Dict[str, Any], assessment_type: str) -> bytes:
    """Generate heatmap image based on assessment type."""
    print(f"DEBUG generate_heatmap: assessment_type={assessment_type}")
    if assessment_type == 'Awareness':
        print("DEBUG: Routing to generate_awareness_heatmap")
        return generate_awareness_heatmap(report_data)
    else:
        print("DEBUG: Routing to generate_system_heatmap")
        return generate_system_heatmap(report_data)


def generate_bar_chart(report_data: Dict[str, Any], assessment_type: str) -> bytes:
    """Generate stacked bar chart based on assessment type."""
    overall = report_data.get('overall', {})
    score = overall.get('score', 0)
    sector_average = report_data.get('sector_average')
    sector_name = report_data.get('sector_name', '')
    
    # Define tiers based on assessment type
    if assessment_type == 'Awareness':
        tiers = [
            {'name': 'Established', 'min': 86, 'max': 100, 'color': '#00B050', 'percentage': 15},
            {'name': 'Developing', 'min': 66, 'max': 85, 'color': '#FFFF00', 'percentage': 20},
            {'name': 'Emerging', 'min': 41, 'max': 65, 'color': '#FFC000', 'percentage': 25},
            {'name': 'Introductory', 'min': 0, 'max': 40, 'color': '#FF0000', 'percentage': 40}
        ]
        default_tier = 'Introductory'
        assessment_label = 'AI Awareness'
    else:
        tiers = [
            {'name': 'Leading', 'min': 86, 'max': 100, 'color': '#00B050', 'percentage': 15},
            {'name': 'Established', 'min': 66, 'max': 85, 'color': '#FFFF00', 'percentage': 20},
            {'name': 'Developing', 'min': 41, 'max': 65, 'color': '#FFC000', 'percentage': 25},
            {'name': 'Foundational', 'min': 0, 'max': 40, 'color': '#FF0000', 'percentage': 40}
        ]
        default_tier = 'Foundational'
        if assessment_type == 'System':
            assessment_label = 'AI System Maturity'
        elif assessment_type == 'Orgwide':
            assessment_label = 'Org-wide AI Maturity'
        else:
            assessment_label = 'AI Readiness'
    
    # Determine current tier
    current_tier = default_tier
    for tier in tiers:
        if tier['min'] <= score <= tier['max']:
            current_tier = tier['name']
            break
    
    # Create figure
    fig, ax = plt.subplots(figsize=(4, 3))
    
    # Draw stacked bar (vertical)
    bar_width = 0.8
    bar_x = 0.5
    current_y = 0
    
    # Draw from bottom to top
    for tier in reversed(tiers):
        height = tier['percentage']
        rect = patches.Rectangle(
            (bar_x - bar_width/2, current_y), 
            bar_width, 
            height,
            facecolor=tier['color'],
            edgecolor='#333333',
            linewidth=1
        )
        ax.add_patch(rect)
        
        # Add tier label
        ax.text(bar_x, current_y + height/2, tier['name'], 
               ha='center', va='center', fontsize=8, fontweight='bold',
               color='#333333')
        
        current_y += height
    
    # Determine user arrow color
    if sector_average is not None:
        if score > sector_average:
            user_arrow_color = '#00B050'  # Green - above average
        elif score < sector_average:
            user_arrow_color = '#FF0000'  # Red - below average
        else:
            user_arrow_color = '#FFC000' if assessment_type != 'Awareness' else '#000000'
    else:
        if assessment_type == 'Awareness':
            user_arrow_color = '#000000'
        elif score >= 66:
            user_arrow_color = '#00B050'
        else:
            user_arrow_color = '#FF0000'
    
    # User score arrow on RIGHT side
    arrow_y = score
    ax.annotate('', xy=(bar_x + bar_width/2, arrow_y), 
               xytext=(bar_x + bar_width/2 + 0.3, arrow_y),
               arrowprops=dict(arrowstyle='->', color=user_arrow_color, lw=2))
    
    # Sector average arrow on LEFT side (black)
    if sector_average is not None and (assessment_type != 'Awareness' or sector_average != score):
        ax.annotate('', xy=(bar_x - bar_width/2, sector_average), 
                   xytext=(bar_x - bar_width/2 - 0.3, sector_average),
                   arrowprops=dict(arrowstyle='->', color='#000000', lw=2))
        if sector_name:
            ax.text(bar_x - bar_width/2 - 0.35, sector_average - 8, f'{sector_average:.0f}%', 
                   ha='right', va='center', fontsize=10, fontweight='bold', color='#000000')
            ax.text(bar_x - bar_width/2 - 0.35, sector_average - 16, f'({sector_name}', 
                   ha='right', va='center', fontsize=7, color='#666666')
            ax.text(bar_x - bar_width/2 - 0.35, sector_average - 22, 'sector average)', 
                   ha='right', va='center', fontsize=7, color='#666666')
    
    # Add score and tier text on right side
    ax.text(bar_x + bar_width/2 + 0.5, arrow_y, f'{score:.0f}%', 
           ha='left', va='center', fontsize=12, fontweight='bold', color=user_arrow_color)
    ax.text(bar_x + bar_width/2 + 0.5, arrow_y - 8, f'{current_tier}', 
           ha='left', va='center', fontsize=9, color='#666666')
    ax.text(bar_x + bar_width/2 + 0.5, arrow_y - 15, assessment_label, 
           ha='left', va='center', fontsize=9, color='#666666')
    
    # Set axis limits and remove axes
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-20, 105)
    ax.axis('off')
    
    plt.tight_layout()
    
    # Save to bytes
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
               facecolor='white', edgecolor='none', pad_inches=0.1)
    plt.close(fig)
    buffer.seek(0)
    
    return buffer.getvalue()


# Domain name mapping for benchmark matching
DOMAIN_NAME_MAPPING = {
    # Awareness domains
    'Awareness & Understanding': ['Awareness & Understanding', 'Awareness'],
    'Governance & Trust Foundations': ['Governance & Trust Foundations', 'Governance'],
    'People & Skills': ['People & Skills', 'People'],
    'Leadership & Vision': ['Leadership & Vision', 'Leadership Vision', 'Leadership'],
    'Data & Digital Readiness': ['Data & Digital Readiness', 'Digital Readiness', 'Data'],
    # System domains
    'Fairness': ['Fairness'],
    'Transparency': ['Transparency'],
    'Explainability': ['Explainability'],
    'Accountability': ['Accountability'],
    'Data Integrity': ['Data Integrity'],
    'Reliability': ['Reliability'],
    'Security': ['Security'],
    'Privacy': ['Privacy'],
    'Safety': ['Safety'],
    'Inclusivity': ['Inclusivity'],
    'Sustainability': ['Sustainability'],
    # Orgwide domains
    'Accountability & Ethics': ['Accountability & Ethics', 'Accountability'],
    'Continuous Improvement & Assurance': ['Continuous Improvement & Assurance', 'Continuous Improvement'],
    'Culture & Capability': ['Culture & Capability', 'Culture'],
    'Data Stewardship & Security': ['Data Stewardship & Security', 'Data Stewardship'],
    'Fairness & Inclusivity': ['Fairness & Inclusivity'],
    'Governance & Oversight': ['Governance & Oversight', 'Governance'],
    'Privacy & Legal Compliance': ['Privacy & Legal Compliance', 'Privacy'],
    'Reliability & Safety': ['Reliability & Safety'],
    'Risk Management': ['Risk Management', 'Risk'],
    'Transparency & Explainability': ['Transparency & Explainability'],
}


def generate_radar_chart(report_data: Dict[str, Any], assessment_type: str) -> bytes:
    """Generate radar chart showing domain scores with sector benchmarks."""
    try:
        # Try to get domain_scores from different sources
        domain_scores = report_data.get('domain_scores', {})
        
        # If domain_scores is empty, extract from heatmap_data
        if not domain_scores:
            heatmap_data = report_data.get('heatmap_data', {})
            domains_list = heatmap_data.get('domains', [])
            
            for domain in domains_list:
                domain_name = domain.get('name', 'Unknown')
                questions = domain.get('questions', [])
                scores = [q.get('score', 0) for q in questions if q.get('score', 0) > 0]
                if scores:
                    domain_scores[domain_name] = scores
        
        if not domain_scores:
            # Return empty image if no data
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            ax.axis('off')
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            plt.close(fig)
            img_buffer.seek(0)
            return img_buffer.getvalue()
        
        # Prepare data for radar chart
        domains = []
        scores = []
        
        for domain_name, score_list in domain_scores.items():
            avg_score = sum(score_list) / len(score_list) if score_list else 0
            percentage = (avg_score / 4) * 100  # 1-4 scale
            domains.append(domain_name)
            scores.append(percentage)
        
        # Get sector benchmark data
        benchmark_data = report_data.get('benchmark_data', {})
        benchmark_scores = []
        
        # Try to match benchmark domains to our domains
        for domain_name in domains:
            benchmark_value = None
            
            # Try direct match first
            if domain_name in benchmark_data:
                benchmark_value = benchmark_data[domain_name]
            else:
                # Try alternative names
                alternatives = DOMAIN_NAME_MAPPING.get(domain_name, [domain_name])
                for alt_name in alternatives:
                    if alt_name in benchmark_data:
                        benchmark_value = benchmark_data[alt_name]
                        break
            
            # If no specific benchmark, use a default of 50%
            if benchmark_value is None:
                benchmark_value = 50.0
            
            benchmark_scores.append(benchmark_value)
        
        # Number of variables
        num_vars = len(domains)
        
        # Compute angle for each axis
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        
        # Complete the loop
        scores += scores[:1]
        benchmark_scores += benchmark_scores[:1]
        angles += angles[:1]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Plot organization scores (blue filled area)
        ax.plot(angles, scores, 'o-', linewidth=2, color='#60a5fa', label='Your Score')
        ax.fill(angles, scores, alpha=0.4, color='#60a5fa')
        
        # Plot sector benchmark (green dashed line)
        ax.plot(angles, benchmark_scores, '--', linewidth=2, color='#10b981', label='Sector Benchmark')
        ax.fill(angles, benchmark_scores, alpha=0.2, color='#10b981')
        
        # Fix axis to go in the right order
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        
        # Set labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(domains, size=10)
        
        # Set y-axis limits
        ax.set_ylim(0, 100)
        ax.set_yticks([0, 20, 40, 60, 80, 100])
        ax.set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'], size=8)
        
        # Add grid
        ax.grid(True, linestyle='-', alpha=0.3)
        
        # Add legend at bottom
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=2, fontsize=10)
        
        # Save to bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        img_buffer.seek(0)
        img_bytes = img_buffer.getvalue()
        plt.close(fig)
        
        return img_bytes
        
    except Exception as e:
        print(f"Error generating radar chart: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return empty placeholder image
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.text(0.5, 0.5, 'Error generating chart', ha='center', va='center')
        ax.axis('off')
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        plt.close(fig)
        img_buffer.seek(0)
        return img_buffer.getvalue()


def generate_radar_chart_with_benchmark(report_data: Dict[str, Any], 
                                        benchmark_data: Dict[str, Any],
                                        assessment_type: str) -> bytes:
    """Generate radar chart comparing organization scores with sector benchmarks.
    
    This is a wrapper that includes the benchmark_data in report_data and calls
    the standard generate_radar_chart function.
    """
    # Add benchmark data to report_data
    report_data_with_benchmark = report_data.copy()
    if benchmark_data:
        report_data_with_benchmark['benchmark_data'] = benchmark_data.get('benchmarks', benchmark_data)
    
    return generate_radar_chart(report_data_with_benchmark, assessment_type)



def generate_risk_gauge(risk_score: float, risk_level: str = None) -> bytes:
    """
    Generate a semi-circular risk gauge image showing the overall risk score
    with a risk level description table on the right.
    
    Risk Levels:
    - Very High (81-100): Critical Risk - Dark Red
    - High (61-80): Significant Risk - Red
    - Medium (41-60): Moderate Risk - Orange
    - Low (21-40): Minor Risk - Yellow
    - Very Low (0-20): Minimal Risk - Green
    
    Args:
        risk_score: Risk score from 0-100
        risk_level: Optional risk level text
    
    Returns:
        PNG image bytes of the risk gauge
    """
    from matplotlib.patches import Wedge
    
    # Create figure - wider to accommodate the description table
    fig, (ax_gauge, ax_table) = plt.subplots(1, 2, figsize=(10, 4), 
                                              gridspec_kw={'width_ratios': [1, 1.2]})
    fig.patch.set_facecolor('white')
    
    # === LEFT: GAUGE ===
    ax_gauge.set_facecolor('white')
    ax_gauge.set_aspect('equal')
    
    # Define the 5 gauge segments (from left to right: Very Low to Very High)
    segments = [
        {'start': 144, 'end': 180, 'color': '#22c55e', 'label': 'Very Low'},   # Green (0-20)
        {'start': 108, 'end': 144, 'color': '#eab308', 'label': 'Low'},        # Yellow (21-40)
        {'start': 72, 'end': 108, 'color': '#f97316', 'label': 'Medium'},      # Orange (41-60)
        {'start': 36, 'end': 72, 'color': '#ef4444', 'label': 'High'},         # Red (61-80)
        {'start': 0, 'end': 36, 'color': '#991b1b', 'label': 'Very High'},     # Dark Red (81-100)
    ]
    
    # Draw the gauge segments
    center = (0, 0)
    outer_radius = 1.0
    inner_radius = 0.6
    
    for seg in segments:
        wedge = Wedge(center, outer_radius, seg['start'], seg['end'], 
                      width=outer_radius - inner_radius,
                      facecolor=seg['color'], edgecolor='white', linewidth=2)
        ax_gauge.add_patch(wedge)
    
    # Clamp score to 0-100
    score = max(0, min(100, risk_score))
    
    # Calculate needle angle based on risk score (0-100 maps to 180-0 degrees)
    needle_angle = 180 - (score / 100) * 180
    angle_rad = np.radians(needle_angle)
    
    # Draw the needle
    needle_length = 0.85
    needle_x = needle_length * np.cos(angle_rad)
    needle_y = needle_length * np.sin(angle_rad)
    
    ax_gauge.annotate('', xy=(needle_x, needle_y), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='#1f2937', lw=3))
    
    # Draw center circle
    center_circle = plt.Circle((0, 0), 0.12, color='#1f2937', zorder=5)
    ax_gauge.add_patch(center_circle)
    
    # Add risk score text
    ax_gauge.text(0, -0.35, f'{score:.0f}', ha='center', va='center', 
            fontsize=28, fontweight='bold', color='#1f2937')
    
    # Determine risk level from score if not provided
    if risk_level:
        level_text = risk_level
    else:
        if score <= 20:
            level_text = 'Very Low'
        elif score <= 40:
            level_text = 'Low'
        elif score <= 60:
            level_text = 'Medium'
        elif score <= 80:
            level_text = 'High'
        else:
            level_text = 'Very High'
    
    ax_gauge.text(0, -0.55, level_text, ha='center', va='center', 
            fontsize=14, fontweight='bold', color='#6b7280')
    
    # Add "Overall Risk" title
    ax_gauge.text(0, 1.15, 'Overall Risk', ha='center', va='center', 
            fontsize=14, fontweight='bold', color='#1f2937')
    
    ax_gauge.set_xlim(-1.3, 1.3)
    ax_gauge.set_ylim(-0.7, 1.3)
    ax_gauge.axis('off')
    
    # === RIGHT: RISK LEVEL DESCRIPTION TABLE ===
    ax_table.set_facecolor('white')
    ax_table.axis('off')
    
    # Title
    ax_table.text(0.0, 0.95, 'Risk Level Description', ha='left', va='top',
                  fontsize=14, fontweight='bold', color='#1f2937',
                  transform=ax_table.transAxes)
    
    # Risk level descriptions
    descriptions = [
        ('Very High (81-100):', 'Critical Risk', '#991b1b'),
        ('High (61-80):', 'Significant Risk', '#ef4444'),
        ('Medium (41-60):', 'Moderate Risk', '#f97316'),
        ('Low (21-40):', 'Minor Risk', '#eab308'),
        ('Very Low (0-20):', 'Minimal Risk', '#22c55e'),
    ]
    
    y_pos = 0.80
    for label, desc, color in descriptions:
        # Color indicator square
        square = plt.Rectangle((0.0, y_pos - 0.03), 0.04, 0.06, 
                               facecolor=color, transform=ax_table.transAxes,
                               clip_on=False)
        ax_table.add_patch(square)
        
        # Bold label
        ax_table.text(0.07, y_pos, label, ha='left', va='center',
                      fontsize=11, fontweight='bold', color='#1f2937',
                      transform=ax_table.transAxes)
        
        # Description
        ax_table.text(0.48, y_pos, desc, ha='left', va='center',
                      fontsize=11, color='#4b5563',
                      transform=ax_table.transAxes)
        
        y_pos -= 0.14
    
    plt.tight_layout()
    
    # Save to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none', transparent=False)
    plt.close(fig)
    buf.seek(0)
    
    return buf.getvalue()



def generate_faira_domain_risk_radar(domain_scores: Dict[str, Any]) -> bytes:
    """
    Generate a radar chart showing residual risk scores across all 8 FAIRA domains.
    
    Args:
        domain_scores: Dictionary with domain names as keys, containing 'Risk' score
        
    Returns:
        PNG image bytes of the radar chart
    """
    try:
        # Define FAIRA domains in order
        faira_domains = [
            'Accountability',
            'Contestability', 
            'Fairness',
            'Wellbeing',
            'Values',
            'Privacy',
            'Reliability',
            'Transparency'
        ]
        
        # Domain display labels (shorter for chart)
        domain_labels = [
            'Accountability',
            'Contestability',
            'Fairness',
            'Wellbeing',
            'Human Values',
            'Privacy',
            'Reliability',
            'Transparency'
        ]
        
        # Extract risk scores
        scores = []
        for domain in faira_domains:
            domain_data = domain_scores.get(domain, {})
            risk_score = domain_data.get('Risk', 0)
            scores.append(risk_score)
        
        # Number of variables
        num_vars = len(faira_domains)
        
        # Compute angles
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        
        # Complete the loop
        scores += scores[:1]
        angles += angles[:1]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        fig.patch.set_facecolor('white')
        
        # Plot risk scores (red gradient based on risk level)
        ax.plot(angles, scores, 'o-', linewidth=2, color='#ef4444', label='Residual Risk')
        ax.fill(angles, scores, alpha=0.3, color='#ef4444')
        
        # Fix axis orientation
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        
        # Set labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(domain_labels, size=9, fontweight='bold')
        
        # Set y-axis limits (0-100 for risk scores)
        ax.set_ylim(0, 100)
        ax.set_yticks([0, 25, 50, 75, 100])
        ax.set_yticklabels(['0', '25', '50', '75', '100'], size=8, color='#6b7280')
        
        # Add grid
        ax.grid(True, linestyle='-', alpha=0.3, color='#d1d5db')
        
        # Title
        ax.set_title('Residual Risk by Domain', size=12, fontweight='bold', 
                     color='#1f2937', pad=20)
        
        # Save to bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close(fig)
        buf.seek(0)
        
        return buf.getvalue()
        
    except Exception as e:
        print(f"Error generating FAIRA domain risk radar: {e}")
        import traceback
        traceback.print_exc()
        # Return placeholder
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.text(0.5, 0.5, 'Error generating chart', ha='center', va='center')
        ax.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return buf.getvalue()


def generate_faira_inherent_risk_radar(domain_scores: Dict[str, Any]) -> bytes:
    """
    Generate a radar chart showing inherent risk scores across all 8 FAIRA domains.
    
    Args:
        domain_scores: Dictionary with domain names as keys, containing 'Inherent_Risk' score
        
    Returns:
        PNG image bytes of the radar chart
    """
    try:
        # Define FAIRA domains in order
        faira_domains = [
            'Accountability',
            'Contestability', 
            'Fairness',
            'Wellbeing',
            'Values',
            'Privacy',
            'Reliability',
            'Transparency'
        ]
        
        # Domain display labels
        domain_labels = [
            'Accountability',
            'Contestability',
            'Fairness',
            'Wellbeing',
            'Human Values',
            'Privacy',
            'Reliability',
            'Transparency'
        ]
        
        # Extract inherent risk scores
        scores = []
        for domain in faira_domains:
            domain_data = domain_scores.get(domain, {})
            inherent_risk = domain_data.get('Inherent_Risk', 0)
            scores.append(inherent_risk)
        
        # Number of variables
        num_vars = len(faira_domains)
        
        # Compute angles
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        
        # Complete the loop
        scores += scores[:1]
        angles += angles[:1]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        fig.patch.set_facecolor('white')
        
        # Plot inherent risk scores (orange/amber for inherent risk)
        ax.plot(angles, scores, 'o-', linewidth=2, color='#f97316', label='Inherent Risk')
        ax.fill(angles, scores, alpha=0.3, color='#f97316')
        
        # Fix axis orientation
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        
        # Set labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(domain_labels, size=9, fontweight='bold')
        
        # Set y-axis limits (0-100 for risk scores)
        ax.set_ylim(0, 100)
        ax.set_yticks([0, 25, 50, 75, 100])
        ax.set_yticklabels(['0', '25', '50', '75', '100'], size=8, color='#6b7280')
        
        # Add grid
        ax.grid(True, linestyle='-', alpha=0.3, color='#d1d5db')
        
        # Title
        ax.set_title('Inherent Risk by Domain', size=12, fontweight='bold', 
                     color='#1f2937', pad=20)
        
        # Save to bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close(fig)
        buf.seek(0)
        
        return buf.getvalue()
        
    except Exception as e:
        print(f"Error generating FAIRA inherent risk radar: {e}")
        import traceback
        traceback.print_exc()
        # Return placeholder
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.text(0.5, 0.5, 'Error generating chart', ha='center', va='center')
        ax.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return buf.getvalue()
