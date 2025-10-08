"""
AM AI SAFE Report Generator
Generates DOCX and PDF reports from assessment data using templates.
"""

import os
import io
import tempfile
import base64
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches, Pt, RGBColor
import requests
import subprocess
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS


class AMReportGenerator:
    """Generates AM AI SAFE assessment reports in DOCX and PDF formats."""
    
    def __init__(self, template_path: Optional[str] = None):
        """Initialize the report generator."""
        self.template_path = template_path or self._get_default_template_path()
        self.domain_colors = {
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
    
    def _get_default_template_path(self) -> str:
        """Get the default template path - using v9 template updated 10/07/2025."""  
        backend_dir = Path(__file__).parent
        return str(backend_dir / "templates" / "docx" / "AM_AI_SAFE_Report_TEMPLATE_v9_10072025.docx")
    
    def _get_html_template_path(self) -> str:
        """Get the HTML template path for PDF generation."""
        backend_dir = Path(__file__).parent
        return str(backend_dir / "templates" / "html" / "pdf_report_template.html")
    
    def format_date(self, date_input) -> str:
        """Format date for the template."""
        try:
            if isinstance(date_input, str):
                # Try different date formats
                for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f']:
                    try:
                        date_obj = datetime.strptime(date_input, fmt)
                        return date_obj.strftime('%d %B %Y')
                    except ValueError:
                        continue
                # If parsing fails, return as-is
                return str(date_input)
            elif hasattr(date_input, 'strftime'):
                return date_input.strftime('%d %B %Y')
            else:
                return str(date_input)
        except:
            return str(date_input)
    
    def _format_assessment_date(self, date_input) -> str:
        """Format assessment date for JSON structure."""
        try:
            if isinstance(date_input, str):
                return date_input  # Already a string, return as-is
            elif hasattr(date_input, 'strftime'):
                return date_input.strftime('%Y-%m-%d')
            else:
                return str(date_input)
        except:
            return str(date_input)
    
    async def generate_report(self, assessment_id: str, assessment_data: Dict[str, Any], 
                            user_data: Dict[str, Any]) -> Tuple[bytes, bytes]:
        """
        Generate DOCX and PDF reports from assessment data.
        
        Args:
            assessment_id: The assessment ID
            assessment_data: Raw assessment data from database
            user_data: User information
            
        Returns:
            Tuple of (docx_bytes, pdf_bytes)
        """
        # Transform data to match report model
        report_data = self._transform_assessment_data(assessment_data, user_data)
        
        # Generate heatmap image
        heatmap_image = self._generate_heatmap_image(report_data)
        
        # Generate DOCX report
        docx_bytes = self._generate_docx_report(report_data, heatmap_image)
        
        # Generate PDF using HTML-to-PDF conversion (WeasyPrint)
        try:
            pdf_bytes = self._generate_html_pdf(report_data)
            print("DEBUG: Using HTML-to-PDF conversion successfully")
        except Exception as e:
            print(f"WARNING: HTML-to-PDF failed ({str(e)}), falling back to LibreOffice conversion")
            # Fallback to LibreOffice conversion
            pdf_bytes = self._convert_docx_to_pdf(docx_bytes)
        
        return docx_bytes, pdf_bytes
    
    def _generate_html_pdf(self, report_data: Dict[str, Any]) -> bytes:
        """Generate PDF directly from HTML template using WeasyPrint."""
        try:
            html_template_path = self._get_html_template_path()
            
            if not os.path.exists(html_template_path):
                raise Exception(f"HTML template not found: {html_template_path}")
            
            # Set up Jinja2 environment
            template_dir = os.path.dirname(html_template_path)
            template_name = os.path.basename(html_template_path)
            
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template(template_name)
            
            # Generate heatmap as data URL for embedding in HTML
            heatmap_data_url = self._generate_heatmap_data_url(report_data)
            
            # Prepare template context (same as DOCX)
            template_context = self._prepare_template_context(report_data)
            template_context['heatmap_image_src'] = heatmap_data_url
            
            # Render HTML
            html_content = template.render(**template_context)
            
            print("DEBUG: HTML template rendered successfully")
            # Check if placeholders are being replaced
            if '{{ org.name }}' in html_content:
                print("WARNING: Template placeholders not being replaced!")
                print(f"Sample content: {html_content[:500]}")
            else:
                print("DEBUG: Template placeholders successfully replaced")
            
            # Convert HTML to PDF using WeasyPrint
            html_doc = HTML(string=html_content)
            pdf_bytes = html_doc.write_pdf()
            
            print(f"HTML-to-PDF conversion successful. Generated {len(pdf_bytes)} bytes")
            return pdf_bytes
            
        except Exception as e:
            print(f"ERROR: HTML-to-PDF conversion failed: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Failed to generate PDF from HTML: {str(e)}")

    def _generate_heatmap_data_url(self, report_data: Dict[str, Any]) -> str:
        """Generate heatmap and return as data URL for HTML embedding."""
        try:
            # Generate heatmap image bytes
            heatmap_bytes = self._generate_heatmap_image(report_data)
            
            # Convert to data URL
            import base64
            encoded = base64.b64encode(heatmap_bytes).decode('utf-8')
            data_url = f"data:image/png;base64,{encoded}"
            
            return data_url
            
        except Exception as e:
            print(f"ERROR: Failed to generate heatmap data URL: {str(e)}")
            # Return placeholder data URL
            return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

    def _prepare_template_context(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare template context for both DOCX and HTML templates."""
        # Transform the report data to the expected template format
        transformed_data = self._transform_assessment_data(report_data, report_data.get('user_data', {}))
        
        # Debug output to see what we're passing to template
        print("DEBUG: Template context data:")
        print(f"  org.name: {transformed_data.get('org', {}).get('name', 'NOT SET')}")
        print(f"  overall.score: {transformed_data.get('overall', {}).get('score', 'NOT SET')}")
        print(f"  overall.tier: {transformed_data.get('overall', {}).get('tier', 'NOT SET')}")
        print(f"  assessment.date: {transformed_data.get('assessment', {}).get('date', 'NOT SET')}")
        print(f"  actions.high count: {len(transformed_data.get('actions', {}).get('high', []))}")
        print(f"  actions.medium count: {len(transformed_data.get('actions', {}).get('medium', []))}")
        print(f"  actions.low count: {len(transformed_data.get('actions', {}).get('low', []))}")
        
        return transformed_data
    
    def _convert_docx_to_pdf(self, docx_bytes: bytes) -> bytes:
        """Convert DOCX to PDF. First try LibreOffice, then fallback to returning DOCX."""
        
        try:
            # Create temporary files
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as docx_file:
                docx_file.write(docx_bytes)
                docx_path = docx_file.name
            
            # Try multiple LibreOffice locations
            libreoffice_paths = [
                '/usr/lib/libreoffice/program/soffice',
                '/usr/bin/libreoffice',
                '/usr/bin/soffice',
                'libreoffice',
                'soffice'
            ]
            
            libreoffice_path = None
            for path in libreoffice_paths:
                if os.path.exists(path) or (not path.startswith('/') and subprocess.run(['which', path], capture_output=True).returncode == 0):
                    libreoffice_path = path
                    break
            
            if not libreoffice_path:
                print("WARNING: LibreOffice not found. Returning DOCX content as PDF (user will get DOCX file)")
                return docx_bytes
            
            # Create output directory
            output_dir = tempfile.mkdtemp()
            
            cmd = [
                libreoffice_path, '--headless', '--convert-to', 'pdf',
                '--outdir', output_dir, docx_path
            ]
            
            print(f"DEBUG: Using LibreOffice path: {libreoffice_path}")
            print(f"DEBUG: Running command: {' '.join(cmd)}")
            
            # Set up environment for LibreOffice
            env = os.environ.copy()
            env['HOME'] = '/tmp'
            env['TMPDIR'] = '/tmp'
            
            # Try the conversion with timeout
            result = subprocess.run(cmd, check=True, capture_output=True, timeout=60, env=env)
            print(f"LibreOffice conversion successful. Output: {result.stdout.decode()}")
            
            # Find the generated PDF
            pdf_filename = os.path.splitext(os.path.basename(docx_path))[0] + '.pdf'
            pdf_path = os.path.join(output_dir, pdf_filename)
            
            if not os.path.exists(pdf_path):
                print(f"WARNING: PDF not found at {pdf_path}. Returning DOCX content.")
                return docx_bytes
                
            with open(pdf_path, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()
                
            print(f"PDF conversion successful. Generated {len(pdf_bytes)} bytes")
            return pdf_bytes
            
        except Exception as e:
            print(f"WARNING: PDF conversion failed ({str(e)}). Returning DOCX content as fallback.")
            # Fallback: return DOCX content
            return docx_bytes
        finally:
            # Clean up temporary directory
            import shutil
            if 'output_dir' in locals():
                try:
                    shutil.rmtree(output_dir)
                except:
                    pass
            # Clean up temporary DOCX file
            if 'docx_path' in locals():
                try:
                    os.unlink(docx_path)
                except:
                    pass
    
    def _transform_assessment_data(self, assessment_data: Dict[str, Any], 
                                 user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform raw assessment data to match the report JSON model.
        
        Args:
            assessment_data: Raw assessment data including questions, answers, summary
            user_data: User information
            
        Returns:
            Transformed data matching report_model_example.json structure
        """
        # Extract core data
        questions_data = assessment_data.get('questions_data', [])
        summary_data = assessment_data.get('summary', {})
        assessment_info = assessment_data.get('assessment', {})
        
        # Calculate overall score and tier
        overall_percentage = summary_data.get('overall_percentage', 0)
        overall_tier = self._calculate_tier(overall_percentage)
        
        # Generate actions based on priority mapping rules
        actions = self._generate_actions_from_questions(questions_data)
        
        # Create report data structure matching the JSON model
        report_data = {
            "org": {
                "name": user_data.get('organization_name', 'Organization')
            },
            "assessment": {
                "date": self._format_assessment_date(assessment_info.get('created_at', datetime.now(timezone.utc))),
                "version": "1.0.0"
            },
            "overall": {
                "score": round(overall_percentage, 1),
                "tier": overall_tier
            },
            "assets": {
                "heatmapUrl": None  # Will be set when we generate the image
            },
            "actions": actions,
            "heatmap_data": self._prepare_heatmap_data(questions_data)
        }
        
        return report_data
    
    def _calculate_tier(self, percentage: float) -> str:
        """Calculate the maturity tier based on percentage score.
        
        Categories:
        1. Excellent (91–100%) 
        2. Good (81–90%) 
        3. Moderate (61–80%) 
        4. Low (41–60%) 
        5. Basic (0–40%)
        """
        if percentage >= 91:
            return "Excellent"
        elif percentage >= 81:
            return "Good"
        elif percentage >= 61:
            return "Moderate"
        elif percentage >= 41:
            return "Low"
        else:
            return "Basic"
    
    def _load_recommendations_lookup(self) -> Dict[str, Any]:
        """Load recommendations lookup from JSON file."""
        import json
        backend_dir = Path(__file__).parent
        recommendations_path = backend_dir / "AMAI_SAFE_recommendations_lookup.json"
        
        try:
            with open(recommendations_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load recommendations lookup: {e}")
            return {"recommendations": {}}
    
    def _get_recommendation_text(self, question_code: str, recommendations_lookup: Dict[str, Any], domain_name: str) -> str:
        """Get specific recommendation text for a question code."""
        recommendations = recommendations_lookup.get("recommendations", {})
        
        if question_code in recommendations:
            return recommendations[question_code].get("default_recommendation", f"Implement comprehensive {domain_name.lower()} improvements to achieve best practices.")
        else:
            # Fallback to generic recommendation
            return f"Implement comprehensive {domain_name.lower()} improvements to achieve best practices in this area."
    
    def _generate_actions_from_questions(self, questions_data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate prioritized actions based on question scores using the priority mapping rules.
        
        Priority Mapping Rules (as per specification):
        - Score 0 (Non-Ideal) → High Priority → actions.high
        - Score 1 (Basic) → Medium Priority → actions.medium  
        - Score 2 (Good) → Low Priority → actions.low
        - Score 3 (Best) → not included in report
        
        Ordering: Recommendations are sorted by domain score (lowest first), then by question within domain.
        """
        actions = {
            "high": [],
            "medium": [],
            "low": []
        }
        
        # Load recommendations lookup
        recommendations_lookup = self._load_recommendations_lookup()
        
        # Calculate domain scores for sorting
        domain_scores = {}
        for domain in questions_data:
            domain_name = domain["domain"]["name"]
            questions = domain["questions"]
            total_score = sum(q["answer"]["numeric_score"] for q in questions if q.get("answer"))
            domain_scores[domain_name] = total_score
        
        # Generate recommendations based on question scores
        for domain in questions_data:
            domain_name = domain["domain"]["name"]
            domain_score = domain_scores.get(domain_name, 0)
            
            for question in domain["questions"]:
                score = question["answer"]["numeric_score"] if question.get("answer") else None
                question_code = question.get("code", "N/A")
                
                if score is not None and score < 3:  # Only include non-perfect scores
                    # Determine priority based on score
                    if score == 0:
                        priority = "high"
                    elif score == 1:
                        priority = "medium"
                    elif score == 2:
                        priority = "low"
                    else:
                        continue  # Skip score 3 (best practice)
                    
                    # Get specific recommendation from lookup or create default
                    recommendation_text = self._get_recommendation_text(question_code, recommendations_lookup, domain_name)
                    
                    # Remove the prefix if present
                    prefix = "Implement the following to meet AM AI SAFE expectations: "
                    if recommendation_text.startswith(prefix):
                        recommendation_text = recommendation_text[len(prefix):]
                    
                    recommendation = {
                        "domain": domain_name,
                        "domain_score": domain_score,  # Add for sorting
                        "question_id": question_code,
                        "text": recommendation_text
                    }
                    
                    actions[priority].append(recommendation)
        
        # Sort by domain score (lowest first), then by question_id within domain
        for priority in actions:
            actions[priority] = sorted(actions[priority], key=lambda x: (x["domain_score"], x["domain"], x["question_id"]))
            # Remove domain_score from final output (it was just for sorting)
            for action in actions[priority]:
                action.pop("domain_score", None)
        
        # No artificial limits - include all recommendations
        # This ensures all high/medium/low priority items are reported
        
        return actions
    
    def _prepare_heatmap_data(self, questions_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prepare heatmap data exactly matching the results summary format."""
        # Collect all domain data with scores
        domains_with_scores = []
        
        for domain_data in questions_data:
            domain_name = domain_data.get('domain', {}).get('name', 'Unknown')
            questions = domain_data.get('questions', [])
            
            # Collect question scores with codes
            question_scores = []
            total_score = 0
            
            for question in questions:
                score = 0
                if question.get('answer'):
                    score = question['answer'].get('numeric_score', 0)
                
                question_code = question.get('code', 'Q-?')
                question_scores.append({
                    'code': question_code,
                    'score': score,
                    'question_id': question.get('id', '')
                })
                total_score += score
            
            # Sort questions by score (lowest first, as shown in heatmap)
            question_scores.sort(key=lambda x: x['score'])
            
            # Pad to 8 questions if needed
            while len(question_scores) < 8:
                question_scores.append({'code': 'N/A', 'score': 0, 'question_id': ''})
            
            # Take only first 8 questions
            question_scores = question_scores[:8]
            
            domains_with_scores.append({
                'name': domain_name,
                'questions': question_scores,
                'total_score': total_score,
                'avg_score': total_score / len(questions) if questions else 0
            })
        
        # Sort domains by total score (lowest first, as shown in heatmap)
        domains_with_scores.sort(key=lambda x: x['total_score'])
        
        return {
            'domains': domains_with_scores,
            'matrix': [[q['score'] for q in domain['questions']] for domain in domains_with_scores]
        }
    
    def _generate_heatmap_image(self, report_data: Dict[str, Any]) -> bytes:
        """Generate heatmap image exactly matching the results summary format."""
        heatmap_data = report_data.get('heatmap_data', {})
        domains = heatmap_data.get('domains', [])
        
        if not domains:
            # Create minimal empty heatmap
            domains = [{'name': 'No Data', 'questions': [{'code': 'N/A', 'score': 0} for _ in range(8)]}]
        
        # Create figure with optimized height for compact rows
        fig, ax = plt.subplots(figsize=(12, 6.5))
        
        # Define colors exactly matching the screenshot
        def get_color(score):
            if score == 0:
                return '#DC3545'  # Red - matches screenshot
            elif score == 1:
                return '#FD7E14'  # Orange - matches screenshot
            elif score == 2:
                return '#FFC107'  # Yellow - matches screenshot
            else:  # score == 3
                return '#28A745'  # Green - matches screenshot
        
        # Create the heatmap grid exactly like the screenshot
        num_domains = len(domains)
        
        for i, domain in enumerate(domains):
            domain_name = domain['name']
            questions = domain['questions']
            
            # Calculate percentage score for left side (like in screenshot)
            total_possible = len([q for q in questions if q['code'] != 'N/A']) * 3
            total_actual = sum(q['score'] for q in questions if q['code'] != 'N/A')
            percentage = (total_actual / total_possible * 100) if total_possible > 0 else 0
            
            for j, question in enumerate(questions[:8]):  # Only 8 questions per domain
                score = question['score']
                question_code = question['code']
                
                # Draw colored rectangle (invert i so lowest scores are at top)
                row_pos = num_domains - 1 - i
                color = get_color(score)
                rect = patches.Rectangle((j, row_pos), 1, 1, 
                                       linewidth=1, edgecolor='white', facecolor=color)
                ax.add_patch(rect)
                
                # Add question code text (white text on colored background)
                # Score numbers removed as color coding makes them redundant
                if question_code != 'N/A':
                    ax.text(j+0.5, row_pos+0.5, question_code, 
                           ha='center', va='center', color='white', 
                           fontsize=10, fontweight='bold')
            
            # Add domain name above percentage with minimal spacing to keep rows compact
            ax.text(-1.9, row_pos+0.65, domain_name, 
                   ha='left', va='center', fontsize=9, fontweight='normal')
            ax.text(-1.9, row_pos+0.35, f'({percentage:.1f}%)', 
                   ha='left', va='center', fontsize=7, color='gray')
        
        # Set axis properties for compact layout
        ax.set_xlim(-2.2, 8)
        ax.set_ylim(0, num_domains)
        ax.set_aspect('equal')
        
        # Remove ticks and labels
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        
        # Adjust layout to match screenshot
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
    
    def _generate_comprehensive_executive_summary(self, report_data: Dict[str, Any]) -> str:
        """Generate a comprehensive multi-paragraph executive summary."""
        org_name = report_data.get('org', {}).get('name', 'Organization')
        overall_score = report_data.get('overall', {}).get('score', 0)
        overall_tier = report_data.get('overall', {}).get('tier', 'Basic')
        
        actions = report_data.get('actions', {})
        high_count = len(actions.get('high', []))
        medium_count = len(actions.get('medium', []))
        low_count = len(actions.get('low', []))
        
        return f"""The AM AI SAFE Framework Assessment for {org_name} has been completed, representing a comprehensive evaluation of the organization's artificial intelligence systems against 88 detailed questions spanning 11 critical domains of AI safety, ethics, and governance. This assessment provides {org_name} with a thorough analysis of their current AI maturity level and a strategic roadmap for improvement.

ASSESSMENT SCOPE AND METHODOLOGY:
The evaluation encompasses the complete spectrum of AI governance, examining Fairness, Transparency, Explainability, Accountability, Data Integrity, Reliability, Security, Privacy, Safety, Inclusivity, and Sustainability. Each domain contains 8 targeted questions designed to assess current practices against industry best practices and regulatory expectations.

KEY FINDINGS SUMMARY:
{org_name} has achieved an overall AI maturity score of {overall_score}%, positioning the organization within the {overall_tier} maturity category. This assessment reveals both areas of strength and significant opportunities for improvement across the AI safety framework.

The evaluation has identified {high_count + medium_count + low_count} specific recommendations for enhancement, categorized by priority and implementation timeline:
• {high_count} High Priority actions addressing critical gaps requiring immediate attention and resource allocation
• {medium_count} Medium Priority initiatives for systematic improvement over the next 6-12 months
• {low_count} Low Priority strategic enhancements for long-term competitive advantage and industry leadership

STRATEGIC IMPLICATIONS:
The assessment results indicate that {org_name} has established foundational AI practices but requires focused investment in key areas to achieve industry-leading AI governance standards. The identified recommendations provide a clear pathway for systematic improvement, risk mitigation, and competitive advantage in AI deployment.

This report serves as both a comprehensive audit of current capabilities and a strategic roadmap for AI excellence, enabling {org_name} to prioritize investments, allocate resources effectively, and implement systematic improvements that will enhance AI safety, ethical compliance, and operational excellence."""
    
    def _generate_assessment_methodology(self) -> str:
        """Generate detailed assessment methodology description."""
        return """ASSESSMENT METHODOLOGY AND FRAMEWORK:

The AM AI SAFE Framework Assessment employs a rigorous, multi-dimensional evaluation approach designed to provide comprehensive insights into organizational AI maturity across 11 critical domains. Each assessment question is evaluated using a standardized 4-point scoring scale:

• Score 0 (Non-Ideal): Indicates fundamental gaps or absence of required practices, representing critical risks that demand immediate attention and corrective action.

• Score 1 (Basic): Demonstrates initial awareness and basic implementation of AI safety practices, but lacks comprehensive coverage or systematic approach.

• Score 2 (Good): Shows solid implementation of AI safety practices with systematic approaches, though opportunities remain for enhancement and optimization.

• Score 3 (Best Practice): Represents industry-leading implementation with comprehensive coverage, proactive management, and continuous improvement processes.

The assessment methodology ensures objective evaluation through standardized criteria, comprehensive coverage of AI safety domains, and actionable recommendations aligned with regulatory expectations and industry best practices. Results provide both current state analysis and forward-looking guidance for systematic improvement."""
    
    def _generate_domain_analysis(self, report_data: Dict[str, Any]) -> str:
        """Generate detailed domain-by-domain analysis."""
        heatmap_data = report_data.get('heatmap_data', {})
        domains = heatmap_data.get('domains', [])
        
        analysis = "DOMAIN-SPECIFIC PERFORMANCE ANALYSIS:\n\n"
        
        for domain in domains:
            domain_name = domain.get('name', 'Unknown')
            questions = domain.get('questions', [])
            scores = [q.get('score', 0) for q in questions if q.get('code') != 'N/A']
            
            if scores:
                avg_score = sum(scores) / len(scores)
                max_score = max(scores)
                min_score = min(scores)
                
                # Determine domain maturity level
                if avg_score >= 2.5:
                    maturity = "High"
                elif avg_score >= 1.5:
                    maturity = "Moderate"
                elif avg_score >= 0.5:
                    maturity = "Developing"
                else:
                    maturity = "Foundational"
                
                analysis += f"{domain_name} Domain ({maturity} Maturity):\n"
                analysis += f"Average Score: {avg_score:.1f}/3.0 | Range: {min_score}-{max_score} | Questions Evaluated: {len(scores)}\n"
                
                # Add domain-specific insights
                if avg_score < 1.0:
                    analysis += f"Critical Focus Area: {domain_name} requires immediate attention with systematic capability building and resource investment.\n"
                elif avg_score < 2.0:
                    analysis += f"Development Opportunity: {domain_name} shows foundational practices with clear opportunities for systematic enhancement.\n"
                else:
                    analysis += f"Strength Area: {domain_name} demonstrates solid practices with opportunities for optimization and industry leadership.\n"
                
                analysis += "\n"
        
        return analysis
    
    def _generate_key_findings(self, report_data: Dict[str, Any]) -> str:
        """Generate key findings and insights."""
        overall_score = report_data.get('overall', {}).get('score', 0)
        actions = report_data.get('actions', {})
        
        findings = "KEY FINDINGS AND STRATEGIC INSIGHTS:\n\n"
        
        findings += "1. OVERALL AI MATURITY ASSESSMENT:\n"
        if overall_score >= 75:
            findings += "The organization demonstrates advanced AI maturity with comprehensive governance frameworks and systematic risk management practices.\n\n"
        elif overall_score >= 50:
            findings += "The organization shows moderate AI maturity with established foundational practices and clear pathways for systematic improvement.\n\n"
        elif overall_score >= 25:
            findings += "The organization exhibits developing AI maturity with basic practices in place but requiring focused investment in key capability areas.\n\n"
        else:
            findings += "The organization is in the foundational stage of AI maturity, requiring comprehensive capability building and systematic framework implementation.\n\n"
        
        findings += "2. PRIORITY FOCUS AREAS:\n"
        
        high_actions = actions.get('high', [])
        if high_actions:
            findings += f"Critical Gaps Identified: {len(high_actions)} high-priority areas require immediate attention to address fundamental risks and compliance requirements.\n"
        
        medium_actions = actions.get('medium', [])
        if medium_actions:
            findings += f"Systematic Improvements: {len(medium_actions)} medium-priority initiatives will strengthen foundational capabilities and enhance operational excellence.\n"
        
        low_actions = actions.get('low', [])
        if low_actions:
            findings += f"Strategic Enhancements: {len(low_actions)} low-priority opportunities will drive competitive advantage and industry leadership positioning.\n\n"
        
        findings += "3. IMPLEMENTATION SUCCESS FACTORS:\n"
        findings += "• Executive leadership commitment and resource allocation for systematic AI governance improvement\n"
        findings += "• Cross-functional collaboration between IT, legal, compliance, and business stakeholders\n"
        findings += "• Phased implementation approach with clear milestones and success metrics\n"
        findings += "• Continuous monitoring and improvement processes to maintain and enhance AI safety standards\n"
        
        return findings
    
    def _generate_implementation_roadmap(self, report_data: Dict[str, Any]) -> str:
        """Generate implementation roadmap and next steps."""
        actions = report_data.get('actions', {})
        
        roadmap = "IMPLEMENTATION ROADMAP AND STRATEGIC RECOMMENDATIONS:\n\n"
        
        roadmap += "PHASE 1: IMMEDIATE ACTIONS (0-3 months)\n"
        roadmap += "Priority: Address critical gaps and compliance requirements\n"
        high_actions = actions.get('high', [])
        if high_actions:
            roadmap += f"Focus Areas: {len(high_actions)} high-priority recommendations addressing fundamental risks\n"
            roadmap += "Success Metrics: Risk mitigation, compliance adherence, foundational capability establishment\n\n"
        
        roadmap += "PHASE 2: SYSTEMATIC IMPROVEMENTS (3-12 months)\n"
        roadmap += "Priority: Build comprehensive AI governance capabilities\n"
        medium_actions = actions.get('medium', [])
        if medium_actions:
            roadmap += f"Focus Areas: {len(medium_actions)} medium-priority initiatives for systematic enhancement\n"
            roadmap += "Success Metrics: Process maturity, operational excellence, stakeholder confidence\n\n"
        
        roadmap += "PHASE 3: STRATEGIC OPTIMIZATION (12+ months)\n"
        roadmap += "Priority: Achieve industry leadership and competitive advantage\n"
        low_actions = actions.get('low', [])
        if low_actions:
            roadmap += f"Focus Areas: {len(low_actions)} strategic enhancements for market differentiation\n"
            roadmap += "Success Metrics: Industry recognition, innovative practices, sustainable competitive advantage\n\n"
        
        roadmap += "CONTINUOUS IMPROVEMENT FRAMEWORK:\n"
        roadmap += "• Quarterly assessment reviews and progress monitoring\n"
        roadmap += "• Annual comprehensive re-evaluation and strategic planning\n"
        roadmap += "• Ongoing stakeholder engagement and feedback integration\n"
        roadmap += "• Emerging technology and regulatory landscape monitoring\n"
        
        return roadmap
    
    def _load_recommendations_lookup(self) -> Dict[str, Any]:
        """Load recommendations lookup from JSON file."""
        import json
        backend_dir = Path(__file__).parent
        recommendations_path = backend_dir / "AMAI_SAFE_recommendations_lookup.json"
        
        try:
            with open(recommendations_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load recommendations lookup: {e}")
            return {"recommendations": {}}
    
    def _get_recommendation_text(self, question_code: str, recommendations_lookup: Dict[str, Any], domain_name: str) -> str:
        """Get specific recommendation text for a question code."""
        recommendations = recommendations_lookup.get("recommendations", {})
        
        if question_code in recommendations:
            return recommendations[question_code].get("default_recommendation", f"Implement comprehensive {domain_name.lower()} improvements to achieve best practices.")
        else:
            # Fallback to generic recommendation
            return f"Implement comprehensive {domain_name.lower()} improvements to achieve best practices in this area."
    
    def _create_heatmap_for_template(self, heatmap_bytes: bytes) -> str:
        """Create a heatmap representation for the template."""
        if not heatmap_bytes:
            return 'HEATMAP_IMAGE_PLACEHOLDER'
        
        # For now, we'll use a placeholder since InlineImage was causing issues
        # In the future, this can be enhanced to properly embed the image
        return f'[HEATMAP IMAGE - {len(heatmap_bytes)} bytes generated]'
    
    def _generate_executive_summary(self, report_data: Dict[str, Any], user_data: Dict[str, Any]) -> str:
        """Generate comprehensive executive summary."""
        org_name = user_data.get('organization_name', 'Organization')
        overall_score = report_data.get('overall', {}).get('score', 0)
        overall_tier = report_data.get('overall', {}).get('tier', 'Basic')
        
        # Count recommendations by priority
        high_count = len(report_data.get('actions', {}).get('high', []))
        medium_count = len(report_data.get('actions', {}).get('medium', []))
        low_count = len(report_data.get('actions', {}).get('low', []))
        
        summary = f"""The AM AI SAFE Framework Assessment for {org_name} has been completed, evaluating the organization's artificial intelligence systems against 88 questions across 11 critical domains of AI safety and ethics.

The assessment methodology follows the AM AI SAFE framework, examining key areas including Fairness, Transparency, Explainability, Accountability, Data Integrity, Reliability, Security, Privacy, Safety, Inclusivity, and Sustainability.

KEY FINDINGS:
• Overall AI Maturity Score: {overall_score}%
• AI Maturity Category: {overall_tier}
• Total Assessment Questions: 88 questions across 11 domains
• Identified Recommendations: {high_count + medium_count + low_count} actionable items

ASSESSMENT OVERVIEW:
{org_name} demonstrates {self._get_maturity_description(overall_score)} level of AI maturity. The assessment revealed specific areas of strength and opportunities for improvement across the AI safety framework.

PRIORITY RECOMMENDATIONS:
• {high_count} High Priority actions addressing critical gaps requiring immediate attention
• {medium_count} Medium Priority initiatives for moderate-term enhancement 
• {low_count} Low Priority strategic improvements for long-term development

The detailed assessment results, including the AI Maturity Heatmap and comprehensive recommendations, provide {org_name} with a clear roadmap for enhancing their AI safety and ethical practices."""

        return summary
    
    def _generate_assessment_results(self, report_data: Dict[str, Any]) -> str:
        """Generate detailed assessment results section."""
        overall_score = report_data.get('overall', {}).get('score', 0)
        overall_tier = report_data.get('overall', {}).get('tier', 'Basic')
        
        # Analyze domain performance
        heatmap_data = report_data.get('heatmap_data', {})
        domains = heatmap_data.get('domains', [])
        
        highest_domain = max(domains, key=lambda x: x['avg_score']) if domains else None
        lowest_domain = min(domains, key=lambda x: x['avg_score']) if domains else None
        
        results = f"""The comprehensive assessment of AI systems has yielded an overall AI maturity score of {overall_score}%, placing the organization within the {overall_tier} category.

PERFORMANCE ANALYSIS:
The assessment evaluated 88 specific questions across 11 domains, with each question scored on a 4-point scale (0=Non-Ideal, 1=Basic, 2=Good, 3=Best Practice).

DOMAIN PERFORMANCE HIGHLIGHTS:"""

        if highest_domain and lowest_domain:
            results += f"""
• Highest Performing Domain: {highest_domain['name']} ({highest_domain['avg_score']:.1f}/3.0 average)
• Area for Greatest Improvement: {lowest_domain['name']} ({lowest_domain['avg_score']:.1f}/3.0 average)"""

        results += """

HEATMAP VISUALIZATION:
The AI Maturity Heatmap below provides a visual representation of performance across all domains and questions. The heatmap is organized with:
• Rows representing the 11 AI safety domains, sorted by total score (lowest performing at the top)
• Columns representing the 8 questions within each domain, arranged by score (lowest scores on the left)
• Color coding indicating performance levels: Red (critical gaps), Orange (below average), Yellow (moderate performance), Green (high performance)

Each cell represents the score for a specific question, enabling identification of precise areas requiring attention and those demonstrating strong performance."""

        return results
    
    def _generate_statistics(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive statistics for the report."""
        actions = report_data.get('actions', {})
        heatmap_data = report_data.get('heatmap_data', {})
        domains = heatmap_data.get('domains', [])
        
        # Count questions by score level
        score_counts = {'non_ideal': 0, 'basic': 0, 'good': 0, 'best': 0}
        total_questions = 0
        
        for domain in domains:
            for question in domain.get('questions', []):
                total_questions += 1
                score = question.get('score', 0)
                if score == 0:
                    score_counts['non_ideal'] += 1
                elif score == 1:
                    score_counts['basic'] += 1
                elif score == 2:
                    score_counts['good'] += 1
                elif score == 3:
                    score_counts['best'] += 1
        
        return {
            'total_questions': total_questions,
            'total_domains': len(domains),
            'score_distribution': score_counts,
            'recommendations_count': {
                'high': len(actions.get('high', [])),
                'medium': len(actions.get('medium', [])),
                'low': len(actions.get('low', []))
            }
        }
    
    def _get_maturity_description(self, score: float) -> str:
        """Get descriptive text for maturity level."""
        if score >= 90:
            return "an excellent"
        elif score >= 75:
            return "a high to excellent"
        elif score >= 60:
            return "a moderate to high"
        elif score >= 40:
            return "a low to moderate"
        elif score >= 25:
            return "a basic to low"
        else:
            return "a basic"
    
    def _populate_recommendation_tables(self, doc: DocxTemplate, report_data: Dict[str, Any]) -> None:
        """
        Programmatically populate the recommendation tables with multiple rows.
        This fixes the issue where Jinja2 loops don't properly create table rows in Word.
        """
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        
        # Get the underlying python-docx Document object
        docx_doc = doc.docx
        
        # Find the three recommendation tables (they should be the last 3 tables in the document)
        tables = docx_doc.tables
        if len(tables) < 3:
            print(f"Warning: Expected at least 3 tables in template, found {len(tables)}")
            return
        
        # Get the last 3 tables (High, Medium, Low priority)
        high_table = tables[-3]
        medium_table = tables[-2]
        low_table = tables[-1]
        
        # Get recommendations from report_data
        actions = report_data.get('actions', {})
        high_actions = actions.get('high', [])
        medium_actions = actions.get('medium', [])
        low_actions = actions.get('low', [])
        
        print(f"Populating tables: High={len(high_actions)}, Medium={len(medium_actions)}, Low={len(low_actions)}")
        
        # Populate each table
        self._populate_table_with_actions(high_table, high_actions)
        self._populate_table_with_actions(medium_table, medium_actions)
        self._populate_table_with_actions(low_table, low_actions)
    
    def _populate_table_with_actions(self, table, actions: List[Dict[str, Any]]) -> None:
        """
        Populate a table with action recommendations, creating one row per action.
        Creates rows with exactly 3 cells by copying header row structure.
        """
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        from copy import deepcopy
        
        # Remove all rows except header
        while len(table.rows) > 1:
            self._remove_row(table, 1)
        
        # Get the header row to copy its structure
        header_row = table.rows[0]
        header_tr = header_row._tr
        
        # Get table element
        tbl = table._element
        
        # Add rows with exactly 3 cells for each action
        for action in actions:
            # Clone the header row structure to get proper column widths
            tr = deepcopy(header_tr)
            
            # Clear the text from the cloned cells and set new values
            cells = tr.findall('.//w:tc', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
            
            # We should have at least 3 cells from the header
            if len(cells) >= 3:
                values = [
                    action.get('domain', ''),
                    action.get('question_id', ''),
                    action.get('text', '')
                ]
                
                for i in range(3):
                    cell = cells[i]
                    
                    # Remove cell shading (background color) from header
                    tcPr = cell.find('.//w:tcPr', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
                    if tcPr is not None:
                        shd = tcPr.find('.//w:shd', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
                        if shd is not None:
                            tcPr.remove(shd)
                    
                    # Clear existing content
                    for p in cell.findall('.//w:p', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
                        cell.remove(p)
                    
                    # Add new paragraph with text
                    p = OxmlElement('w:p')
                    
                    if values[i]:
                        r = OxmlElement('w:r')
                        rPr = OxmlElement('w:rPr')
                        
                        # Set font
                        rFonts = OxmlElement('w:rFonts')
                        rFonts.set(qn('w:ascii'), 'Arial')
                        rFonts.set(qn('w:hAnsi'), 'Arial')
                        rPr.append(rFonts)
                        
                        # Set font size
                        sz = OxmlElement('w:sz')
                        sz.set(qn('w:val'), '20')  # 10pt = 20 half-points
                        rPr.append(sz)
                        
                        r.append(rPr)
                        
                        t = OxmlElement('w:t')
                        t.text = values[i]
                        r.append(t)
                        p.append(r)
                    
                    cell.append(p)
                
                # Remove extra cells beyond the first 3
                for i in range(3, len(cells)):
                    tr.remove(cells[i])
            
            # Append row to table
            tbl.append(tr)
        
        print(f"DEBUG: Added {len(actions)} rows with 3 cells each (copied from header structure)")
    
    def _remove_row(self, table, row_idx: int) -> None:
        """Remove a row from a table."""
        from docx.oxml.table import CT_Row
        tbl = table._tbl
        tr = table.rows[row_idx]._tr
        tbl.remove(tr)
    
    def _generate_docx_report(self, report_data: Dict[str, Any], heatmap_image: bytes) -> bytes:
        """Generate DOCX report using template and data while preserving all styles."""
        try:
            # Load the template
            doc = DocxTemplate(self.template_path)
            
            # Create inline image for heatmap - set to requested width
            heatmap_inline = InlineImage(doc, io.BytesIO(heatmap_image), width=Inches(6.27))
            
            # Prepare template context matching the exact template structure and placeholders
            template_context = {
                # Organization information
                'org': {
                    'name': report_data.get('org', {}).get('name', 'Organization')
                },
                
                # Assessment information (date will be formatted by formatDate function)
                'assessment': {
                    'date': report_data.get('assessment', {}).get('date', '2025-01-01'),
                    'version': report_data.get('assessment', {}).get('version', '1.0.0')
                },
                
                # Overall scores
                'overall': {
                    'score': report_data.get('overall', {}).get('score', 0),
                    'tier': report_data.get('overall', {}).get('tier', 'Basic')
                },
                
                # Assets (heatmap image) - generate and embed properly  
                'assets': {
                    'heatmapUrl': self._create_heatmap_for_template(heatmap_image) if heatmap_image else 'HEATMAP_IMAGE_PLACEHOLDER'
                },
                
                # Heatmap image for direct placeholder replacement
                'heatmap_image': heatmap_inline,
                
                # Actions for working template with separate priority arrays
                'actions': {
                    'high': report_data.get('actions', {}).get('high', []),
                    'medium': report_data.get('actions', {}).get('medium', []),
                    'low': report_data.get('actions', {}).get('low', [])
                },
                
                # Add comprehensive content sections that will make the report much longer
                'executive_summary': self._generate_comprehensive_executive_summary(report_data),
                'assessment_methodology': self._generate_assessment_methodology(),
                'domain_analysis': self._generate_domain_analysis(report_data),
                'key_findings': self._generate_key_findings(report_data),
                'implementation_roadmap': self._generate_implementation_roadmap(report_data),
                
            }
            
            # Debug output for troubleshooting
            print("Generated report data structure:")
            print(f"  Organization: {template_context['org']['name']}")
            print(f"  Overall score: {template_context['overall']['score']}")
            print(f"  High priority actions: {len(template_context['actions']['high'])}")
            print(f"  Medium priority actions: {len(template_context['actions']['medium'])}")
            print(f"  Low priority actions: {len(template_context['actions']['low'])}")
            
            # Show sample actions for debugging
            if template_context['actions']['high']:
                sample_high = template_context['actions']['high'][0]
                print(f"  Sample high action: {sample_high.get('domain', 'N/A')} | {sample_high.get('question_id', 'N/A')}")
            
            # Helper function for date formatting in template
            template_context['formatDate'] = self.format_date
            
            # Render the template - this will preserve all original fonts, colors, margins, layout
            doc.render(template_context)
            
            # Populate recommendation tables programmatically (for v7 template)
            self._populate_recommendation_tables(doc, report_data)
            
            # Save to bytes
            output_buffer = io.BytesIO()
            doc.save(output_buffer)
            output_buffer.seek(0)
            
            return output_buffer.getvalue()
            
        except Exception as e:
            print(f"Error generating DOCX report: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Failed to generate DOCX report: {str(e)}")
    
    async def generate_report_for_assessment(self, assessment_id: str, db, current_user) -> Tuple[bytes, str]:
        """
        Generate report for a specific assessment ID.
        
        Args:
            assessment_id: Assessment ID to generate report for
            db: Database connection
            current_user: Current user object
            
        Returns:
            Tuple of (docx_bytes, filename)
        """
        print(f"DEBUG: Generating report for assessment_id: {assessment_id}")
        print(f"DEBUG: Current user org_id: {getattr(current_user, 'org_id', 'NOT SET')}")
        print(f"DEBUG: Current user: {current_user}")
        
        # Get assessment data
        assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
        print(f"DEBUG: Assessment found: {assessment is not None}")
        
        if not assessment:
            # Try to find assessment without org_id restriction for debugging
            assessment_debug = await db.assessments.find_one({"id": assessment_id})
            print(f"DEBUG: Assessment exists without org_id filter: {assessment_debug is not None}")
            if assessment_debug:
                print(f"DEBUG: Assessment org_id: {assessment_debug.get('org_id', 'NOT SET')}")
                print(f"DEBUG: Assessment status: {assessment_debug.get('status', 'NOT SET')}")
            raise Exception(f"Assessment not found for user org_id: {current_user.org_id}")
        
        if assessment.get("status") != "COMPLETED":
            print(f"DEBUG: Assessment status: {assessment.get('status')}")
            raise Exception(f"Assessment must be completed before generating report. Current status: {assessment.get('status')}")
        
        # Get actual data from the real database structure
        # Get all answers for this assessment
        answers = await db.answers.find({"assessment_id": assessment_id}).to_list(length=None)
        
        # Get all domains 
        domains = await db.domains.find().to_list(length=None)
        
        # Get all questions to map UUIDs to codes
        questions = await db.questions.find().to_list(length=None)
        
        # Import COMPLETE_QUESTIONS_DATA to get full question details
        from complete_questions import COMPLETE_QUESTIONS_DATA
        
        # Create mapping from question code to question details
        questions_by_code = {}
        for question_data in COMPLETE_QUESTIONS_DATA:
            code = question_data.get('code')
            if code:
                questions_by_code[code] = question_data
        
        # Create mapping from question UUID to question code
        question_uuid_to_code = {}
        for question in questions:
            question_uuid_to_code[question["id"]] = question["code"]
        
        # Create questions structure from answers (since questions collection is empty)
        # Group answers by domain
        domains_by_id = {domain["id"]: domain for domain in domains}
        
        # Get all unique question patterns from answers to reconstruct question structure
        questions_by_domain = {}
        
        processed_answers = 0
        for answer in answers:
            # Get question UUID and map to code using questions collection
            question_uuid = answer.get("question_id", "")
            
            # Get question code from UUID
            question_code = question_uuid_to_code.get(question_uuid)
            
            if question_code:
                processed_answers += 1
                # Get full question details from COMPLETE_QUESTIONS_DATA
                question_details = questions_by_code.get(question_code)
                
                if question_details:
                    # Extract domain from question code (e.g., FA-1 -> Fairness domain)
                    domain_prefix = question_code.split("-")[0] if "-" in question_code else ""
                    
                    # Map domain prefixes to domain names
                    domain_mapping = {
                        "FA": "Fairness", "TR": "Transparency", "EX": "Explainability", 
                        "AC": "Accountability", "DI": "Data Integrity", "RE": "Reliability",
                        "SE": "Security", "PR": "Privacy", "SA": "Safety", 
                        "IN": "Inclusivity", "SU": "Sustainability"
                    }
                    
                    domain_name = domain_mapping.get(domain_prefix, "Unknown")
                    
                    # Find matching domain in database
                    matching_domain = None
                    for domain in domains:
                        if domain["name"] == domain_name:
                            matching_domain = domain
                            break
                    
                    if matching_domain:
                        domain_id = matching_domain["id"]
                        
                        if domain_id not in questions_by_domain:
                            questions_by_domain[domain_id] = []
                        
                        # Create question object with correct data
                        question = {
                            "id": question_uuid,
                            "code": question_code,
                            "text": question_details.get('text', f'Question {question_code}'),
                            "domain_id": domain_id,
                            "answer": {
                                "numeric_score": answer.get("numeric_score", 0),
                                "text": answer.get("option", ""),
                                "question_id": question_uuid
                            }
                        }
                        questions_by_domain[domain_id].append(question)
        
        
        print(f"DEBUG: Processed answers: {processed_answers}/{len(answers)}")
        print(f"DEBUG: Domains in heatmap: {len(questions_by_domain)}")
        for domain_id in list(questions_by_domain.keys())[:3]:  # Show first 3 domains
            domain = domains_by_id.get(domain_id, {"name": "Unknown"})
            questions = questions_by_domain[domain_id]
            print(f"  Domain: {domain['name']} - Questions: {len(questions)}")
            for question in questions[:2]:  # Show first 2 questions per domain
                print(f"    Question {question.get('code', 'N/A')}: Score {question.get('answer', {}).get('numeric_score', 'N/A')}")
        # Calculate summary data since summaries collection is empty
        total_score = 0
        total_possible = 0
        domain_scores = []
        
        for domain_id, questions in questions_by_domain.items():
            domain = domains_by_id.get(domain_id, {"name": "Unknown"})
            domain_total = sum(q["answer"]["numeric_score"] for q in questions)
            domain_possible = len(questions) * 3
            domain_percentage = (domain_total / domain_possible * 100) if domain_possible > 0 else 0
            
            domain_scores.append({
                "domain_id": domain_id,
                "percentage": domain_percentage
            })
            
            total_score += domain_total
            total_possible += domain_possible
        
        overall_percentage = (total_score / total_possible * 100) if total_possible > 0 else 0
        
        # Calculate maturity tier
        # Categories: Excellent (91–100%), Good (81–90%), Moderate (61–80%), Low (41–60%), Basic (0–40%)
        if overall_percentage >= 91:
            overall_maturity = "Excellent"
        elif overall_percentage >= 81:
            overall_maturity = "Good"
        elif overall_percentage >= 61:
            overall_maturity = "Moderate"
        elif overall_percentage >= 41:
            overall_maturity = "Low"
        else:
            overall_maturity = "Basic"
        
        summary_data = {
            "overall_percentage": overall_percentage,
            "overall_maturity": overall_maturity,
            "domain_scores": domain_scores
        }
        
        # The questions_by_domain structure is already built above, no need to recreate it
        
        # Use the already-built questions_by_domain structure from above
        # questions_by_domain = {}  # Already built above
        # domains_by_id is already available from earlier in the method
        
        # Skip this loop since questions_by_domain is already built above
        pass
        
        # Create structured questions data
        questions_data = []
        for domain_id, questions in questions_by_domain.items():
            domain_info = domains_by_id.get(domain_id, {"name": "Unknown Domain"})
            questions_data.append({
                "domain": domain_info,
                "questions": sorted(questions, key=lambda q: q.get("order", 0))
            })
        
        # Prepare assessment data for report generation
        assessment_data = {
            "assessment": assessment,
            "questions_data": questions_data,
            "summary": summary_data
        }
        
        user_data = {
            "organization_name": current_user.organization_name
        }
        
        # Generate the report
        docx_bytes, pdf_bytes = await self.generate_report(assessment_id, assessment_data, user_data)
        
        # Generate filename
        safe_org_name = "".join(c for c in current_user.organization_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_org_name = safe_org_name.replace(' ', '_') if safe_org_name else "Organization"
        filename = f"AM_AI_SAFE_Assessment_{safe_org_name}_{assessment.get('created_at', datetime.now(timezone.utc)).strftime('%Y-%m-%d')}.docx"
        
        return docx_bytes, filename
    
    async def generate_report_full(self, assessment_id: str, db, current_user) -> Tuple[bytes, bytes]:
        """
        Generate both DOCX and PDF reports for a specific assessment ID.
        
        Args:
            assessment_id: Assessment ID to generate report for
            db: Database connection
            current_user: Current user object
            
        Returns:
            Tuple of (docx_bytes, pdf_bytes)
        """
        # Get assessment data (reuse the existing logic)
        assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
        if not assessment:
            raise Exception("Assessment not found")
        
        if assessment.get("status") != "COMPLETED":
            raise Exception("Assessment must be completed before generating report")
        
        # Get actual data from the real database structure
        # Get all answers for this assessment
        answers = await db.answers.find({"assessment_id": assessment_id}).to_list(length=None)
        
        # Get all domains 
        domains = await db.domains.find().to_list(length=None)
        
        # Get all questions to map UUIDs to codes
        questions = await db.questions.find().to_list(length=None)
        
        # Import COMPLETE_QUESTIONS_DATA to get full question details
        from complete_questions import COMPLETE_QUESTIONS_DATA
        
        # Create mapping from question code to question details
        questions_by_code = {}
        for question_data in COMPLETE_QUESTIONS_DATA:
            code = question_data.get('code')
            if code:
                questions_by_code[code] = question_data
        
        # Create mapping from question UUID to question code
        question_uuid_to_code = {}
        for question in questions:
            question_uuid_to_code[question["id"]] = question["code"]
        
        # Create questions structure from answers (since questions collection is empty)
        # Group answers by domain
        domains_by_id = {domain["id"]: domain for domain in domains}
        
        # Get all unique question patterns from answers to reconstruct question structure
        questions_by_domain = {}
        
        processed_answers = 0
        for answer in answers:
            # Get question UUID and map to code using questions collection
            question_uuid = answer.get("question_id", "")
            
            # Get question code from UUID
            question_code = question_uuid_to_code.get(question_uuid)
            
            if question_code:
                processed_answers += 1
                # Get full question details from COMPLETE_QUESTIONS_DATA
                question_details = questions_by_code.get(question_code)
                
                if question_details:
                    # Extract domain from question code (e.g., FA-1 -> Fairness domain)
                    domain_prefix = question_code.split("-")[0] if "-" in question_code else ""
                    
                    # Map domain prefixes to domain names
                    domain_mapping = {
                        "FA": "Fairness", "TR": "Transparency", "EX": "Explainability", 
                        "AC": "Accountability", "DI": "Data Integrity", "RE": "Reliability",
                        "SE": "Security", "PR": "Privacy", "SA": "Safety", 
                        "IN": "Inclusivity", "SU": "Sustainability"
                    }
                    
                    domain_name = domain_mapping.get(domain_prefix, "Unknown")
                    
                    # Find matching domain in database
                    matching_domain = None
                    for domain in domains:
                        if domain["name"] == domain_name:
                            matching_domain = domain
                            break
                    
                    if matching_domain:
                        domain_id = matching_domain["id"]
                        
                        if domain_id not in questions_by_domain:
                            questions_by_domain[domain_id] = []
                        
                        # Create question object with correct data
                        question = {
                            "id": question_uuid,
                            "code": question_code,
                            "text": question_details.get('text', f'Question {question_code}'),
                            "domain_id": domain_id,
                            "answer": {
                                "numeric_score": answer.get("numeric_score", 0),
                                "text": answer.get("option", ""),
                                "question_id": question_uuid
                            }
                        }
                        questions_by_domain[domain_id].append(question)
        
        
        print(f"DEBUG: Processed answers: {processed_answers}/{len(answers)}")
        print(f"DEBUG: Domains in heatmap: {len(questions_by_domain)}")
        for domain_id in list(questions_by_domain.keys())[:3]:  # Show first 3 domains
            domain = domains_by_id.get(domain_id, {"name": "Unknown"})
            questions = questions_by_domain[domain_id]
            print(f"  Domain: {domain['name']} - Questions: {len(questions)}")
            for question in questions[:2]:  # Show first 2 questions per domain
                print(f"    Question {question.get('code', 'N/A')}: Score {question.get('answer', {}).get('numeric_score', 'N/A')}")
        # Calculate summary data since summaries collection is empty
        total_score = 0
        total_possible = 0
        domain_scores = []
        
        for domain_id, questions in questions_by_domain.items():
            domain = domains_by_id.get(domain_id, {"name": "Unknown"})
            domain_total = sum(q["answer"]["numeric_score"] for q in questions)
            domain_possible = len(questions) * 3
            domain_percentage = (domain_total / domain_possible * 100) if domain_possible > 0 else 0
            
            domain_scores.append({
                "domain_id": domain_id,
                "percentage": domain_percentage
            })
            
            total_score += domain_total
            total_possible += domain_possible
        
        overall_percentage = (total_score / total_possible * 100) if total_possible > 0 else 0
        
        # Calculate maturity tier
        # Categories: Excellent (91–100%), Good (81–90%), Moderate (61–80%), Low (41–60%), Basic (0–40%)
        if overall_percentage >= 91:
            overall_maturity = "Excellent"
        elif overall_percentage >= 81:
            overall_maturity = "Good"
        elif overall_percentage >= 61:
            overall_maturity = "Moderate"
        elif overall_percentage >= 41:
            overall_maturity = "Low"
        else:
            overall_maturity = "Basic"
        
        summary_data = {
            "overall_percentage": overall_percentage,
            "overall_maturity": overall_maturity,
            "domain_scores": domain_scores
        }
        
        # The questions_by_domain structure is already built above, no need to recreate it
        
        # Use the already-built questions_by_domain structure from above
        # questions_by_domain = {}  # Already built above
        # domains_by_id is already available from earlier in the method
        
        # Skip this loop since questions_by_domain is already built above
        pass
        
        # Create structured questions data
        questions_data = []
        for domain_id, questions in questions_by_domain.items():
            domain_info = domains_by_id.get(domain_id, {"name": "Unknown Domain"})
            questions_data.append({
                "domain": domain_info,
                "questions": sorted(questions, key=lambda q: q.get("order", 0))
            })
        
        # Prepare assessment data for report generation
        assessment_data = {
            "assessment": assessment,
            "questions_data": questions_data,
            "summary": summary_data
        }
        
        user_data = {
            "organization_name": current_user.organization_name
        }
        
        # Generate both DOCX and PDF
        return await self.generate_report(assessment_id, assessment_data, user_data)