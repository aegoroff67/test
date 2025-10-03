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
from docx.shared import Inches
import requests


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
        """Get the default template path - using Arial font template."""
        backend_dir = Path(__file__).parent
        return str(backend_dir / "templates" / "docx" / "AM_AI_SAFE_Report_TEMPLATE_arial_font.docx")
    
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
        
        # Convert DOCX to PDF using LibreOffice
        pdf_bytes = self._convert_docx_to_pdf(docx_bytes)
        
        return docx_bytes, pdf_bytes
    
    def _convert_docx_to_pdf(self, docx_bytes: bytes) -> bytes:
        """Convert DOCX to PDF using LibreOffice headless."""
        import subprocess
        import tempfile
        import os
        
        try:
            # Create temporary files
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as docx_file:
                docx_file.write(docx_bytes)
                docx_path = docx_file.name
            
            # Create output directory
            output_dir = tempfile.mkdtemp()
            
            # Convert using LibreOffice
            cmd = [
                'libreoffice', '--headless', '--convert-to', 'pdf',
                '--outdir', output_dir, docx_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True, timeout=30)
            
            # Read the generated PDF
            pdf_filename = os.path.splitext(os.path.basename(docx_path))[0] + '.pdf'
            pdf_path = os.path.join(output_dir, pdf_filename)
            
            with open(pdf_path, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()
            
            # Cleanup
            os.unlink(docx_path)
            os.unlink(pdf_path)
            os.rmdir(output_dir)
            
            return pdf_bytes
            
        except subprocess.CalledProcessError as e:
            print(f"LibreOffice conversion error: {e.stderr.decode()}")
            # Return DOCX bytes as fallback
            return docx_bytes
        except Exception as e:
            print(f"PDF conversion error: {str(e)}")
            # Return DOCX bytes as fallback
            return docx_bytes
    
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
                "score": int(overall_percentage),
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
        """Calculate the maturity tier based on percentage score."""
        if percentage >= 90:
            return "Excellent"
        elif percentage >= 75:
            return "High–Excellent" 
        elif percentage >= 60:
            return "Moderate–High"
        elif percentage >= 40:
            return "Low–Moderate"
        elif percentage >= 25:
            return "Basic–Low"
        else:
            return "Basic"
    
    def _generate_actions_from_questions(self, questions_data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate prioritized actions based on question scores using the priority mapping rules.
        
        Priority Mapping Rules (as per specification):
        - Score 0 (Non-Ideal) → High Priority → actions.high
        - Score 1 (Basic) → Medium Priority → actions.medium  
        - Score 2 (Good) → Low Priority → actions.low
        - Score 3 (Best) → not included in report
        """
        actions = {
            "high": [],
            "medium": [],
            "low": []
        }
        
        # Enhanced recommendation templates based on domain and question patterns
        recommendation_templates = {
            "Fairness": {
                0: "Establish comprehensive bias detection and mitigation processes for AI systems",
                1: "Enhance existing fairness practices with regular bias audits and diverse datasets",
                2: "Optimize fairness monitoring with advanced algorithmic fairness tools"
            },
            "Transparency": {
                0: "Implement comprehensive AI system documentation and explainability frameworks",
                1: "Improve transparency measures with detailed model documentation and user communication",
                2: "Enhance transparency reporting with advanced interpretability tools"
            },
            "Explainability": {
                0: "Develop comprehensive explainable AI capabilities and user-friendly explanations",
                1: "Strengthen model interpretability with improved explanation mechanisms",
                2: "Optimize explainability tools with advanced visualization and reporting"
            },
            "Accountability": {
                0: "Establish clear AI governance structures and accountability frameworks",
                1: "Enhance accountability processes with defined roles and responsibilities",
                2: "Optimize accountability mechanisms with advanced governance tools"
            },
            "Data Integrity": {
                0: "Implement comprehensive data quality management and validation processes",
                1: "Strengthen data integrity practices with enhanced validation and monitoring",
                2: "Optimize data management with advanced quality assurance tools"
            },
            "Reliability": {
                0: "Establish robust AI system reliability and performance monitoring frameworks",
                1: "Enhance system reliability with improved testing and validation processes",
                2: "Optimize reliability monitoring with advanced performance analytics"
            },
            "Security": {
                0: "Implement comprehensive AI security frameworks and threat protection measures",
                1: "Strengthen AI security practices with enhanced protection and monitoring",
                2: "Optimize security measures with advanced threat detection and response"
            },
            "Privacy": {
                0: "Establish comprehensive privacy protection and data handling frameworks for AI",
                1: "Enhance privacy practices with improved data protection and consent mechanisms",
                2: "Optimize privacy controls with advanced data anonymization and protection tools"
            },
            "Safety": {
                0: "Implement comprehensive AI safety frameworks and risk mitigation strategies",
                1: "Strengthen safety practices with enhanced risk assessment and monitoring",
                2: "Optimize safety measures with advanced risk management and testing tools"
            },
            "Inclusivity": {
                0: "Establish comprehensive inclusivity frameworks and diverse stakeholder engagement",
                1: "Enhance inclusivity practices with improved accessibility and representation",
                2: "Optimize inclusivity measures with advanced accessibility tools and diverse testing"
            },
            "Sustainability": {
                0: "Implement comprehensive environmental impact assessment and sustainable AI practices",
                1: "Enhance sustainability practices with improved energy efficiency and resource optimization",
                2: "Optimize sustainability measures with advanced environmental monitoring and green AI tools"
            }
        }
        
        for domain_data in questions_data:
            domain_name = domain_data.get('domain', {}).get('name', 'Unknown Domain')
            
            for question in domain_data.get('questions', []):
                # Get the numeric score (0-3 scale)
                score = 0
                if question.get('answer'):
                    score = question['answer'].get('numeric_score', 0)
                
                question_code = question.get('code', 'Q-?')
                question_text = question.get('text', 'Unknown question')
                
                # Apply priority mapping rules
                priority = None
                if score == 0:  # Non-Ideal → High Priority
                    priority = "high"
                elif score == 1:  # Basic → Medium Priority
                    priority = "medium"
                elif score == 2:  # Good → Low Priority
                    priority = "low"
                # Score 3 (Best) → not included
                
                if priority:
                    # Get domain-specific recommendation or use generic one
                    if domain_name in recommendation_templates and score in recommendation_templates[domain_name]:
                        recommendation_text = recommendation_templates[domain_name][score]
                    else:
                        # Generic recommendation based on score level
                        if score == 0:
                            recommendation_text = f"Address critical gap: {question_text.lower()}"
                        elif score == 1:
                            recommendation_text = f"Enhance current practices for: {question_text.lower()}"
                        else:  # score == 2
                            recommendation_text = f"Optimize existing approach to: {question_text.lower()}"
                    
                    # Create action item matching the JSON structure specification
                    action_item = {
                        "domain": domain_name,
                        "question_id": question_code,
                        "text": recommendation_text
                    }
                    
                    actions[priority].append(action_item)
        
        # Sort by domain and question_id for consistency
        for priority in actions:
            actions[priority] = sorted(actions[priority], key=lambda x: (x["domain"], x["question_id"]))
        
        # Limit recommendations to keep report manageable
        actions["high"] = actions["high"][:15]  # Max 15 high priority
        actions["medium"] = actions["medium"][:10]  # Max 10 medium priority  
        actions["low"] = actions["low"][:8]  # Max 8 low priority
        
        return actions
    
    def _prepare_heatmap_data(self, questions_data: List[Dict[str, Any]]) -> List[List[float]]:
        """Prepare heatmap data matrix from questions data."""
        heatmap_matrix = []
        
        for domain_data in questions_data:
            domain_scores = []
            for question in domain_data.get('questions', []):
                score = 0
                if question.get('answer'):
                    score = question['answer'].get('numeric_score', 0)
                # Normalize to 0-1 scale for heatmap
                normalized_score = score / 3.0
                domain_scores.append(normalized_score)
            
            # Pad or truncate to 8 questions per domain
            while len(domain_scores) < 8:
                domain_scores.append(0.0)
            domain_scores = domain_scores[:8]
            
            heatmap_matrix.append(domain_scores)
        
        return heatmap_matrix
    
    def _generate_heatmap_image(self, report_data: Dict[str, Any]) -> bytes:
        """Generate heatmap image matching the exact format shown in the report."""
        heatmap_data = report_data.get('heatmap_data', [])
        
        if not heatmap_data:
            # Create empty heatmap if no data
            heatmap_data = [[0] * 8 for _ in range(11)]
        
        # Domain names as shown in the image
        domain_names = [
            'Fairness', 'Transparency', 'Explainability', 'Accountability', 
            'Data Integrity', 'Reliability', 'Security', 'Privacy', 
            'Safety', 'Inclusivity', 'Sustainability'
        ]
        
        # Create figure matching the style in the report
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Define colors matching the report (Red, Orange, Yellow, Green)
        def get_color(score):
            if score == 0:
                return '#FF4444'  # Red
            elif score == 1:
                return '#FF8844'  # Orange  
            elif score == 2:
                return '#FFDD44'  # Yellow
            else:  # score == 3
                return '#44BB44'  # Green
        
        # Create the heatmap grid
        for i, domain_scores in enumerate(heatmap_data[:11]):  # Only 11 domains
            for j, score in enumerate(domain_scores[:8]):  # Only 8 questions per domain
                # Convert normalized score back to 0-3 scale
                actual_score = int(score * 3) if isinstance(score, float) else score
                
                # Draw colored rectangle
                color = get_color(actual_score)
                rect = patches.Rectangle((j, len(heatmap_data)-1-i), 1, 1, 
                                       linewidth=1, edgecolor='white', facecolor=color)
                ax.add_patch(rect)
                
                # Add question code and score text
                domain_code = domain_names[i][:2].upper()  # FA, TR, EX, etc.
                question_code = f'{domain_code}-{j+1}'
                
                # White text on colored background
                ax.text(j+0.5, len(heatmap_data)-1-i+0.3, question_code, 
                       ha='center', va='center', color='white', fontsize=8, fontweight='bold')
                ax.text(j+0.5, len(heatmap_data)-1-i+0.7, str(actual_score), 
                       ha='center', va='center', color='white', fontsize=8, fontweight='bold')
        
        # Add domain labels on the left
        for i, domain in enumerate(domain_names[:len(heatmap_data)]):
            ax.text(-0.1, len(heatmap_data)-1-i+0.5, domain, 
                   ha='right', va='center', fontsize=10, fontweight='normal')
        
        # Set axis properties
        ax.set_xlim(0, 8)
        ax.set_ylim(0, len(heatmap_data))
        ax.set_aspect('equal')
        
        # Remove ticks and labels
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        
        # Add title below the heatmap (as in the report)
        fig.text(0.5, 0.02, 'Figure 1. AI Maturity Heatmap', 
                ha='center', va='bottom', fontsize=12, fontweight='normal')
        
        # Adjust layout
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.1, left=0.15)
        
        # Save to bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        img_buffer.seek(0)
        img_bytes = img_buffer.getvalue()
        plt.close(fig)
        
        return img_bytes
    
    def _generate_docx_report(self, report_data: Dict[str, Any], heatmap_image: bytes) -> bytes:
        """Generate DOCX report using template and data while preserving all styles."""
        try:
            # Load the template
            doc = DocxTemplate(self.template_path)
            
            # Create inline image for heatmap - preserve original sizing in template
            heatmap_inline = InlineImage(doc, io.BytesIO(heatmap_image), width=Inches(5.5))
            
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
                
                # Assets (heatmap image)
                'assets': {
                    'heatmapUrl': heatmap_inline  # Replace URL placeholder with inline image
                },
                
                # Actions for template loops - using 'dynamic' as general loop and specific priorities
                'actions': {
                    'dynamic': report_data.get('actions', {}).get('high', []) + 
                              report_data.get('actions', {}).get('medium', []) + 
                              report_data.get('actions', {}).get('low', []),
                    'high': report_data.get('actions', {}).get('high', []),
                    'medium': report_data.get('actions', {}).get('medium', []),
                    'low': report_data.get('actions', {}).get('low', [])
                },
                
                # Helper function for date formatting in template
                'formatDate': lambda date_str: self.format_date(date_str)
            }
            
            # Render the template - this will preserve all original fonts, colors, margins, layout
            doc.render(template_context)
            
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
        # Get assessment data
        assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
        if not assessment:
            raise Exception("Assessment not found")
        
        if assessment.get("status") != "COMPLETED":
            raise Exception("Assessment must be completed before generating report")
        
        # Get questions and answers data
        questions_pipeline = [
            {"$match": {"id": assessment_id}},
            {"$lookup": {
                "from": "questions",
                "localField": "id", 
                "foreignField": "assessment_id",
                "as": "questions"
            }},
            {"$lookup": {
                "from": "answers",
                "localField": "id",
                "foreignField": "assessment_id", 
                "as": "answers"
            }},
            {"$lookup": {
                "from": "domains",
                "localField": "questions.domain_id",
                "foreignField": "id",
                "as": "domains"
            }}
        ]
        
        assessment_results = await db.assessments.aggregate(questions_pipeline).to_list(length=1)
        if not assessment_results:
            raise Exception("Could not retrieve assessment data")
        
        assessment_full = assessment_results[0]
        
        # Get summary data
        summary_pipeline = [
            {"$match": {"assessment_id": assessment_id}},
            {"$lookup": {
                "from": "domains",
                "localField": "domain_scores.domain_id",
                "foreignField": "id", 
                "as": "domain_details"
            }}
        ]
        
        summary_results = await db.summaries.aggregate(summary_pipeline).to_list(length=1)
        summary_data = summary_results[0] if summary_results else {}
        
        # Organize data by domain
        questions_by_domain = {}
        answers_by_question = {answer["question_id"]: answer for answer in assessment_full.get("answers", [])}
        domains_by_id = {domain["id"]: domain for domain in assessment_full.get("domains", [])}
        
        for question in assessment_full.get("questions", []):
            domain_id = question["domain_id"]
            if domain_id not in questions_by_domain:
                questions_by_domain[domain_id] = []
            
            # Add answer data to question
            question["answer"] = answers_by_question.get(question["id"])
            questions_by_domain[domain_id].append(question)
        
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
        
        # Get questions and answers data
        questions_pipeline = [
            {"$match": {"id": assessment_id}},
            {"$lookup": {
                "from": "questions",
                "localField": "id", 
                "foreignField": "assessment_id",
                "as": "questions"
            }},
            {"$lookup": {
                "from": "answers",
                "localField": "id",
                "foreignField": "assessment_id", 
                "as": "answers"
            }},
            {"$lookup": {
                "from": "domains",
                "localField": "questions.domain_id",
                "foreignField": "id",
                "as": "domains"
            }}
        ]
        
        assessment_results = await db.assessments.aggregate(questions_pipeline).to_list(length=1)
        if not assessment_results:
            raise Exception("Could not retrieve assessment data")
        
        assessment_full = assessment_results[0]
        
        # Get summary data
        summary_pipeline = [
            {"$match": {"assessment_id": assessment_id}},
            {"$lookup": {
                "from": "domains",
                "localField": "domain_scores.domain_id",
                "foreignField": "id", 
                "as": "domain_details"
            }}
        ]
        
        summary_results = await db.summaries.aggregate(summary_pipeline).to_list(length=1)
        summary_data = summary_results[0] if summary_results else {}
        
        # Organize data by domain
        questions_by_domain = {}
        answers_by_question = {answer["question_id"]: answer for answer in assessment_full.get("answers", [])}
        domains_by_id = {domain["id"]: domain for domain in assessment_full.get("domains", [])}
        
        for question in assessment_full.get("questions", []):
            domain_id = question["domain_id"]
            if domain_id not in questions_by_domain:
                questions_by_domain[domain_id] = []
            
            # Add answer data to question
            question["answer"] = answers_by_question.get(question["id"])
            questions_by_domain[domain_id].append(question)
        
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