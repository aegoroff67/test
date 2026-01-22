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
