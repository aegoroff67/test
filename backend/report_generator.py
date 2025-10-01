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
        """Get the default template path."""
        backend_dir = Path(__file__).parent
        return str(backend_dir / "templates" / "docx" / "AM_AI_SAFE_Report_TEMPLATE.docx")
    
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
        
        # Convert DOCX to PDF (placeholder - would need LibreOffice or similar)
        pdf_bytes = docx_bytes  # For now, return DOCX as PDF placeholder
        
        return docx_bytes, pdf_bytes
    
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
                "date": assessment_info.get('created_at', datetime.now(timezone.utc)).strftime('%Y-%m-%d'),
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
        
        Priority Mapping Rules:
        - Questions scored Non-Ideal (=0) → actions.high
        - Basic (=1) → actions.medium  
        - Good (=2) → actions.low
        - Best (=3) → not listed as a gap
        """
        actions = {
            "high": [],
            "medium": [],
            "low": []
        }
        
        # Recommendation templates based on domain and score
        recommendation_templates = {
            "high": {
                "default": "Immediate action required to address critical gap in {domain}. Implement comprehensive {domain_lower} framework and policies."
            },
            "medium": {
                "default": "Enhance {domain} practices to meet industry standards. Review and update existing {domain_lower} procedures."
            },
            "low": {
                "default": "Optimize {domain} processes for best practice alignment. Consider advanced {domain_lower} implementation strategies."
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
                
                # Apply priority mapping rules
                priority = None
                if score == 0:  # Non-Ideal
                    priority = "high"
                elif score == 1:  # Basic
                    priority = "medium"
                elif score == 2:  # Good
                    priority = "low"
                # Score 3 (Best) doesn't get listed as a gap
                
                if priority:
                    # Generate recommendation text
                    template = recommendation_templates[priority]["default"]
                    recommendation_text = template.format(
                        domain=domain_name,
                        domain_lower=domain_name.lower()
                    )
                    
                    # Create action item
                    action_item = {
                        "domain": domain_name,
                        "question_id": question_code,
                        "text": recommendation_text
                    }
                    
                    actions[priority].append(action_item)
        
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
        """Generate heatmap image from assessment data."""
        heatmap_data = report_data.get('heatmap_data', [])
        
        if not heatmap_data:
            # Create empty heatmap if no data
            heatmap_data = [[0.5] * 8 for _ in range(11)]
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Convert to numpy array
        data_array = np.array(heatmap_data)
        
        # Create heatmap
        im = ax.imshow(data_array, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
        
        # Add domain labels (y-axis)
        domain_names = [
            'Fairness', 'Transparency', 'Explainability', 'Accountability', 
            'Data Integrity', 'Reliability', 'Security', 'Privacy', 
            'Safety', 'Inclusivity', 'Sustainability'
        ]
        
        # Ensure we have the right number of labels
        y_labels = domain_names[:len(heatmap_data)]
        ax.set_yticks(range(len(y_labels)))
        ax.set_yticklabels(y_labels)
        
        # Add question number labels (x-axis)  
        ax.set_xticks(range(8))
        ax.set_xticklabels([f'Q{i+1}' for i in range(8)])
        
        # Add score text in each cell
        for i in range(len(heatmap_data)):
            for j in range(len(heatmap_data[i])):
                score = int(heatmap_data[i][j] * 3)  # Convert back to 0-3 scale
                text_color = 'white' if heatmap_data[i][j] < 0.5 else 'black'
                ax.text(j, i, f'{score}', ha='center', va='center', 
                       color=text_color, fontweight='bold', fontsize=10)
        
        # Add title and labels
        ax.set_title('AM AI SAFE Assessment Heatmap', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Questions', fontsize=12)
        ax.set_ylabel('Domains', fontsize=12)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Score (0-3 scale)', rotation=270, labelpad=20)
        cbar.set_ticks([0, 0.33, 0.67, 1.0])
        cbar.set_ticklabels(['0', '1', '2', '3'])
        
        # Adjust layout
        plt.tight_layout()
        
        # Save to bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_bytes = img_buffer.getvalue()
        plt.close(fig)
        
        return img_bytes
    
    def _generate_docx_report(self, report_data: Dict[str, Any], heatmap_image: bytes) -> bytes:
        """Generate DOCX report using template and data."""
        try:
            # Load the template
            doc = DocxTemplate(self.template_path)
            
            # Create inline image for heatmap
            heatmap_inline = InlineImage(doc, io.BytesIO(heatmap_image), width=Inches(6))
            
            # Update report data with heatmap image
            template_context = {
                'org': report_data['org'],
                'assessment': report_data['assessment'],
                'overall': report_data['overall'],
                'actions': report_data['actions'],
                'heatmap_image': heatmap_inline,
                # Helper functions for template
                'formatDate': lambda date_str: datetime.strptime(date_str, '%Y-%m-%d').strftime('%d %B %Y')
            }
            
            # Render the template
            doc.render(template_context)
            
            # Save to bytes
            output_buffer = io.BytesIO()
            doc.save(output_buffer)
            output_buffer.seek(0)
            
            return output_buffer.getvalue()
            
        except Exception as e:
            print(f"Error generating DOCX report: {str(e)}")
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