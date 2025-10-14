"""
Pandoc-based report generator for AM AI SAFE assessments.
Uses Markdown templates with Jinja2 templating to generate DOCX and PDF reports.
"""

import logging
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from jinja2 import Template
import base64

logger = logging.getLogger(__name__)

class PandocReportGenerator:
    """Generate assessment reports using Pandoc from Markdown templates."""
    
    def __init__(self):
        self.backend_dir = Path(__file__).parent
        self.templates_dir = self.backend_dir / "templates" / "markdown"
        self.template_path = self.templates_dir / "AM_AI_SAFE_Report_TEMPLATE_v9.md"
    
    def generate_docx_report(self, assessment_data: dict, user_data: dict) -> bytes:
        """
        Generate DOCX report from Markdown template using Pandoc.
        
        Args:
            assessment_data: Assessment data including scores and recommendations
            user_data: User information
            
        Returns:
            bytes: DOCX file content
        """
        try:
            logger.info("Starting DOCX report generation with Pandoc")
            
            # Prepare template context
            context = self._prepare_template_context(assessment_data, user_data)
            
            # Render Markdown template
            markdown_content = self._render_markdown_template(context)
            
            # Convert Markdown to DOCX using Pandoc
            docx_bytes = self._convert_to_docx(markdown_content)
            
            logger.info("DOCX report generated successfully")
            return docx_bytes
            
        except Exception as e:
            logger.error(f"Error generating DOCX report: {str(e)}", exc_info=True)
            raise
    
    def generate_pdf_report(self, assessment_data: dict, user_data: dict) -> bytes:
        """
        Generate PDF report from Markdown template using Pandoc.
        
        Args:
            assessment_data: Assessment data including scores and recommendations
            user_data: User information
            
        Returns:
            bytes: PDF file content
        """
        try:
            logger.info("Starting PDF report generation with Pandoc")
            
            # Prepare template context
            context = self._prepare_template_context(assessment_data, user_data)
            
            # Render Markdown template
            markdown_content = self._render_markdown_template(context)
            
            # Convert Markdown to PDF using Pandoc
            pdf_bytes = self._convert_to_pdf(markdown_content)
            
            logger.info("PDF report generated successfully")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Error generating PDF report: {str(e)}", exc_info=True)
            raise
    
    def _prepare_template_context(self, assessment_data: dict, user_data: dict) -> dict:
        """Prepare context data for template rendering."""
        
        # Extract organization name
        org_name = user_data.get('organization_name', 'Organization')
        
        # Get overall score and tier
        overall_score = assessment_data.get('overall_score', 0)
        overall_tier = self._get_maturity_tier(overall_score)
        
        # Format assessment date
        assessment_date = datetime.now().strftime("%B %d, %Y")
        
        # Generate heatmap
        heatmap_image = self._generate_heatmap_markdown(assessment_data)
        
        # Prepare recommendations by priority
        actions_by_priority = self._categorize_recommendations(assessment_data)
        
        context = {
            'org': {
                'name': org_name
            },
            'assessment': {
                'date': assessment_date
            },
            'overall': {
                'score': f"{overall_score:.1f}",
                'tier': overall_tier
            },
            'heatmap_image': heatmap_image,
            'actions': actions_by_priority
        }
        
        return context
    
    def _render_markdown_template(self, context: dict) -> str:
        """Render Markdown template with Jinja2."""
        
        # Read template
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Create Jinja2 template
        template = Template(template_content)
        
        # Render template
        rendered = template.render(**context)
        
        return rendered
    
    def _convert_to_docx(self, markdown_content: str) -> bytes:
        """Convert Markdown to DOCX using Pandoc."""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as md_file:
            md_file.write(markdown_content)
            md_file_path = md_file.name
        
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as docx_file:
            docx_file_path = docx_file.name
        
        try:
            # Run Pandoc command
            cmd = [
                'pandoc',
                md_file_path,
                '-o', docx_file_path,
                '--from', 'markdown+pipe_tables',
                '--to', 'docx'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                logger.error(f"Pandoc error: {result.stderr}")
                raise RuntimeError(f"Pandoc conversion failed: {result.stderr}")
            
            # Read generated DOCX file
            with open(docx_file_path, 'rb') as f:
                docx_bytes = f.read()
            
            return docx_bytes
            
        finally:
            # Cleanup temp files
            Path(md_file_path).unlink(missing_ok=True)
            Path(docx_file_path).unlink(missing_ok=True)
    
    def _convert_to_pdf(self, markdown_content: str) -> bytes:
        """Convert Markdown to PDF using Pandoc with LaTeX."""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as md_file:
            md_file.write(markdown_content)
            md_file_path = md_file.name
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
            pdf_file_path = pdf_file.name
        
        try:
            # Run Pandoc command with PDF engine
            cmd = [
                'pandoc',
                md_file_path,
                '-o', pdf_file_path,
                '--from', 'markdown+pipe_tables',
                '--to', 'pdf',
                '--pdf-engine', 'pdflatex',
                '-V', 'geometry:margin=1in'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                logger.error(f"Pandoc PDF error: {result.stderr}")
                raise RuntimeError(f"Pandoc PDF conversion failed: {result.stderr}")
            
            # Read generated PDF file
            with open(pdf_file_path, 'rb') as f:
                pdf_bytes = f.read()
            
            return pdf_bytes
            
        finally:
            # Cleanup temp files
            Path(md_file_path).unlink(missing_ok=True)
            Path(pdf_file_path).unlink(missing_ok=True)
    
    def _get_maturity_tier(self, score: float) -> str:
        """Determine maturity tier based on score."""
        if score >= 90:
            return "Advanced"
        elif score >= 75:
            return "Mature"
        elif score >= 60:
            return "Developing"
        elif score >= 40:
            return "Basic"
        else:
            return "Initial"
    
    def _generate_heatmap_markdown(self, assessment_data: dict) -> str:
        """Generate heatmap placeholder for Markdown."""
        # For now, return a placeholder
        # In a real implementation, you would generate an actual heatmap image
        # and embed it as base64 or save it to a temp file
        return "![Heatmap](heatmap.png)"
    
    def _categorize_recommendations(self, assessment_data: dict) -> dict:
        """Categorize recommendations by priority."""
        
        recommendations = assessment_data.get('recommendations', [])
        
        categorized = {
            'high': [],
            'medium': [],
            'low': []
        }
        
        for rec in recommendations:
            priority = rec.get('priority', 'medium').lower()
            
            # Map question score to priority if not explicitly set
            score = rec.get('score', 2)
            if priority == 'medium':  # Default, determine from score
                if score == 0:
                    priority = 'high'
                elif score == 1:
                    priority = 'medium'
                else:
                    priority = 'low'
            
            recommendation_item = {
                'domain': rec.get('domain', 'N/A'),
                'question_id': rec.get('question_code', 'N/A'),
                'text': rec.get('recommendation_text', 'No recommendation available')
            }
            
            if priority in categorized:
                categorized[priority].append(recommendation_item)
        
        return categorized
