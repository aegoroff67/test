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
            assessment_data: Assessment data including scores and recommendations (from fetch_assessment_data)
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
    
    async def fetch_assessment_data(self, assessment_id: str, db, current_user):
        """
        Fetch and prepare assessment data from database.
        This replicates the logic from the old report_generator.py
        """
        logger.info(f"Fetching assessment data for ID: {assessment_id}")
        
        # Get assessment
        assessment = await db.assessments.find_one({"id": assessment_id, "org_id": current_user.org_id})
        
        if not assessment:
            raise Exception(f"Assessment not found for user org_id: {current_user.org_id}")
        
        if assessment.get("status") != "COMPLETED":
            raise Exception(f"Assessment must be completed before generating report. Current status: {assessment.get('status')}")
        
        logger.info(f"Assessment found: status={assessment.get('status')}")
        
        # Get all answers for this assessment
        answers = await db.answers.find({"assessment_id": assessment_id}).to_list(length=None)
        logger.info(f"Found {len(answers)} answers")
        
        # Get all domains 
        domains = await db.domains.find().to_list(length=None)
        logger.info(f"Found {len(domains)} domains")
        
        # Get all questions
        questions = await db.questions.find().to_list(length=None)
        logger.info(f"Found {len(questions)} questions")
        
        # Import complete questions data
        from complete_questions import COMPLETE_QUESTIONS_DATA
        logger.info(f"Loaded {len(COMPLETE_QUESTIONS_DATA)} complete questions")
        
        # Load recommendations lookup
        import json
        recommendations_lookup_path = self.backend_dir / "AMAI_SAFE_recommendations_lookup.json"
        with open(recommendations_lookup_path, 'r') as f:
            recommendations_data = json.load(f)
        logger.info(f"Loaded {len(recommendations_data)} recommendations from lookup")
        
        # Create mappings
        questions_by_code = {q.get('code'): q for q in COMPLETE_QUESTIONS_DATA if q.get('code')}
        question_uuid_to_code = {q["id"]: q["code"] for q in questions}
        domains_by_id = {domain["id"]: domain for domain in domains}
        
        # Domain mapping
        domain_mapping = {
            "FA": "Fairness", "TR": "Transparency", "EX": "Explainability", 
            "AC": "Accountability", "DI": "Data Integrity", "RE": "Reliability",
            "SE": "Security", "PR": "Privacy", "SA": "Safety", 
            "IN": "Inclusivity", "SU": "Sustainability"
        }
        
        # Process answers and build domain scores
        domain_scores = {}
        question_scores = []
        
        for answer in answers:
            question_uuid = answer.get("question_id", "")
            question_code = question_uuid_to_code.get(question_uuid)
            
            if question_code:
                question_details = questions_by_code.get(question_code)
                if question_details:
                    domain_prefix = question_code.split("-")[0] if "-" in question_code else ""
                    domain_name = domain_mapping.get(domain_prefix, "Unknown")
                    
                    # Get score from answer - field is 'numeric_score' not 'score'
                    score = answer.get("numeric_score", 0)
                    
                    # Debug: Log first few scores
                    if len(question_scores) < 5:
                        logger.info(f"  Question {question_code}: score={score}, numeric_score={answer.get('numeric_score')}")
                    
                    if domain_name not in domain_scores:
                        domain_scores[domain_name] = []
                    domain_scores[domain_name].append(score)
                    
                    question_scores.append({
                        'code': question_code,
                        'domain': domain_name,
                        'score': score,
                        'text': question_details.get('text', '')
                    })
        
        logger.info(f"Processed {len(question_scores)} question scores")
        
        # Calculate overall score
        all_scores = [q['score'] for q in question_scores]
        overall_score = (sum(all_scores) / (len(all_scores) * 3) * 100) if all_scores else 0
        logger.info(f"Score calculation: sum={sum(all_scores)}, count={len(all_scores)}, max_possible={len(all_scores) * 3}")
        logger.info(f"Calculated overall score: {overall_score:.1f}%")
        
        # Get recommendations based on scores
        recommendations = []
        recommendations_dict = recommendations_data.get("recommendations", {})
        
        for question in question_scores:
            question_code = question['code']
            score = question['score']
            
            # Get recommendation from lookup (structure is: recommendations[question_code][default_recommendation])
            if question_code in recommendations_dict:
                rec_text = recommendations_dict[question_code].get("default_recommendation", "")
                if rec_text:
                    recommendations.append({
                        'domain': question['domain'],
                        'question_code': question_code,
                        'score': score,
                        'recommendation_text': rec_text
                    })
        
        logger.info(f"Found {len(recommendations)} recommendations")
        
        return {
            'assessment': assessment,
            'overall_score': overall_score,
            'domain_scores': domain_scores,
            'question_scores': question_scores,
            'recommendations': recommendations
        }
    
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
        
        # Debug logging
        logger.info(f"Template context prepared:")
        logger.info(f"  - Organization: {org_name}")
        logger.info(f"  - Overall Score: {overall_score:.1f}%")
        logger.info(f"  - Maturity Tier: {overall_tier}")
        logger.info(f"  - High Priority Actions: {len(actions_by_priority.get('high', []))}")
        logger.info(f"  - Medium Priority Actions: {len(actions_by_priority.get('medium', []))}")
        logger.info(f"  - Low Priority Actions: {len(actions_by_priority.get('low', []))}")
        
        return context
    
    def _render_markdown_template(self, context: dict) -> str:
        """Render Markdown template with Jinja2."""
        
        # Read template
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Create Jinja2 environment with custom comment delimiters
        # Use {## ##} for comments to avoid conflict with markdown {#anchor#}
        from jinja2 import Environment
        env = Environment(
            block_start_string='{%',
            block_end_string='%}',
            variable_start_string='{{',
            variable_end_string='}}',
            comment_start_string='{##',
            comment_end_string='##}'
        )
        
        # Create template
        template = env.from_string(template_content)
        
        # Render template
        rendered = template.render(**context)
        
        return rendered
    
    def _convert_to_docx(self, markdown_content: str) -> bytes:
        """Convert Markdown to DOCX using Pandoc with reference document for styling."""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as md_file:
            md_file.write(markdown_content)
            md_file_path = md_file.name
        
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as docx_file:
            docx_file_path = docx_file.name
        
        try:
            # Path to reference DOCX template for styling
            reference_docx = self.backend_dir / "templates" / "docx" / "reference.docx"
            
            # Run Pandoc command with reference document
            cmd = [
                'pandoc',
                md_file_path,
                '-o', docx_file_path,
                '--from', 'markdown+pipe_tables',
                '--to', 'docx',
                '--reference-doc', str(reference_docx)
            ]
            
            logger.info(f"Running Pandoc with reference doc: {reference_docx}")
            
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
            
            logger.info(f"DOCX generated successfully, size: {len(docx_bytes)} bytes")
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
            # Map question score to priority
            score = rec.get('score', 2)
            
            if score == 0:
                priority = 'high'
            elif score == 1:
                priority = 'medium'
            else:  # score 2 or 3
                priority = 'low'
            
            recommendation_item = {
                'domain': rec.get('domain', 'N/A'),
                'question_id': rec.get('question_code', 'N/A'),
                'text': rec.get('recommendation_text', 'No recommendation available')
            }
            
            categorized[priority].append(recommendation_item)
        
        return categorized
