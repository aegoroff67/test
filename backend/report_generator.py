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
# from weasyprint import HTML, CSS  # Disabled - requires system libraries (pango, cairo)


class AMReportGenerator:
    """Generates AM AI SAFE assessment reports in DOCX and PDF formats."""
    
    def __init__(self, template_path: Optional[str] = None, use_test_template: bool = False, use_smart_priority: bool = False, assessment_type: str = "System"):
        """Initialize the report generator."""
        self.use_test_template = use_test_template
        self.use_smart_priority = use_smart_priority
        self.assessment_type = assessment_type
        # For test template, default to smart priority unless explicitly set to False
        if use_test_template and not use_smart_priority:
            self.use_smart_priority = True
        if template_path:
            self.template_path = template_path
        elif use_test_template:
            self.template_path = self._get_test_template_path()
        else:
            self.template_path = self._get_template_for_assessment_type(assessment_type)
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
        self._sector_actions_cache = None
        self._question_metadata_cache = None
    
    def _load_question_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Load question metadata containing impact_weight, effort_score, etc."""
        if self._question_metadata_cache is not None:
            return self._question_metadata_cache
        
        try:
            backend_dir = Path(__file__).parent
            metadata_path = backend_dir / "system_question_metadata.json"
            if metadata_path.exists():
                import json
                with open(metadata_path, 'r') as f:
                    self._question_metadata_cache = json.load(f)
                print(f"DEBUG: Loaded question metadata for {len(self._question_metadata_cache)} questions")
                return self._question_metadata_cache
        except Exception as e:
            print(f"Warning: Could not load question metadata: {e}")
        
        self._question_metadata_cache = {}
        return self._question_metadata_cache
    
    def _calculate_smart_priority(self, impact_weight: float, gap: int, effort_score: float) -> float:
        """
        Calculate smart priority score using the same formula as the frontend.
        Formula: impact_weight × gap × (1 - effort_score)
        - Higher impact = better
        - Higher gap (lower maturity score) = better
        - Lower effort = better (hence 1 - effort_score)
        """
        return impact_weight * gap * (1 - effort_score)
    
    def _get_quadrant_label(self, impact_weight: float, effort_score: float) -> str:
        """
        Determine quadrant label based on impact and effort.
        Same logic as frontend/backend results page.
        """
        if impact_weight >= 0.8 and effort_score <= 0.5:
            return "Quick win"
        elif impact_weight >= 0.8 and effort_score > 0.5:
            return "Strategic project"
        elif impact_weight < 0.8 and effort_score <= 0.5:
            return "Opportunistic improvement"
        else:
            return "Lower priority"
    
    def _load_sector_actions(self, assessment_type: str = None) -> Dict[str, Dict[str, str]]:
        """Load sector-specific action steps from JSON file based on assessment type."""
        # Use provided assessment_type or fall back to instance attribute
        effective_type = assessment_type or self.assessment_type
        
        # Use different cache key based on assessment type
        cache_key = f"_sector_actions_cache_{effective_type}"
        cached = getattr(self, cache_key, None)
        if cached is not None:
            return cached
        
        try:
            backend_dir = Path(__file__).parent
            # Choose the appropriate actions file based on assessment type
            if effective_type == 'Awareness':
                actions_path = backend_dir / "awareness_actions.json"
            else:
                actions_path = backend_dir / "system_actions.json"
            
            if actions_path.exists():
                import json
                with open(actions_path, 'r') as f:
                    result = json.load(f)
                    setattr(self, cache_key, result)
                    return result
        except Exception as e:
            print(f"Warning: Could not load sector actions for {effective_type}: {e}")
        
        setattr(self, cache_key, {})
        return {}
    
    def _get_template_for_assessment_type(self, assessment_type: str) -> str:
        """Get the appropriate template path based on assessment type."""
        backend_dir = Path(__file__).parent
        
        # Template mapping for each assessment type
        template_map = {
            'System': 'AM_AI_SAFE_Report_TEMPLATE_v9_10072025.docx',
            'Awareness': 'AM_AI_SAFE_Awareness_Report_TEMPLATE_v0.9.04_20260111.docx',
            'Readiness': 'AM_AI_SAFE_Report_TEMPLATE_v9_10072025.docx',  # Fallback to System template
            'Orgwide': 'AM_AI_SAFE_Report_TEMPLATE_v9_10072025.docx',    # Fallback to System template
            'FAIRA': 'AM_AI_SAFE_Report_TEMPLATE_v9_10072025.docx',      # Fallback to System template
        }
        
        template_filename = template_map.get(assessment_type, 'AM_AI_SAFE_Report_TEMPLATE_v9_10072025.docx')
        template_path = backend_dir / "templates" / "docx" / template_filename
        
        # Check if template exists, fallback to default if not
        if not template_path.exists():
            print(f"Warning: Template for {assessment_type} not found at {template_path}, using default")
            template_path = backend_dir / "templates" / "docx" / "AM_AI_SAFE_Report_TEMPLATE_v9_10072025.docx"
        
        print(f"DEBUG: Using template for {assessment_type}: {template_path.name}")
        return str(template_path)

    def _generate_sector_actions(self, report_data: Dict[str, Any], sector_name: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate sector-specific action steps based on assessment scores.
        
        Args:
            report_data: Report data containing questions and scores
            sector_name: The sector/industry name (e.g., "Finance / Insurance")
            
        Returns:
            Dictionary with 'high', 'medium', 'low' priority sector actions
        """
        sector_actions = {
            'high': [],
            'medium': [],
            'low': []
        }
        
        if not sector_name:
            print("DEBUG _generate_sector_actions: No sector_name provided")
            return sector_actions
        
        # Load all sector actions (will use correct file based on assessment_type)
        all_sector_actions = self._load_sector_actions()
        print(f"DEBUG _generate_sector_actions: Loaded {len(all_sector_actions)} sectors")
        
        # Get actions for this specific sector
        sector_specific = all_sector_actions.get(sector_name, {})
        if not sector_specific:
            # Try to find a partial match
            for key in all_sector_actions.keys():
                if sector_name.lower() in key.lower() or key.lower() in sector_name.lower():
                    sector_specific = all_sector_actions[key]
                    print(f"DEBUG _generate_sector_actions: Found partial match for '{sector_name}' -> '{key}'")
                    break
        
        if not sector_specific:
            print(f"DEBUG _generate_sector_actions: No sector-specific actions found for: {sector_name}")
            print(f"DEBUG _generate_sector_actions: Available sectors: {list(all_sector_actions.keys())}")
            return sector_actions
        
        print(f"DEBUG _generate_sector_actions: Found {len(sector_specific)} actions for sector '{sector_name}'")
        
        # Get questions data from report
        questions_data = report_data.get('questions_data', [])
        print(f"DEBUG _generate_sector_actions: questions_data has {len(questions_data)} domains")
        
        # Domain mapping depends on assessment type
        if self.assessment_type == 'Awareness':
            domain_mapping = {
                "AU": "Awareness & Understanding",
                "GT": "Governance & Trust Foundations",
                "PS": "People & Skills",
                "LV": "Leadership Vision",
                "DR": "Digital Readiness"
            }
        else:
            domain_mapping = {
                "FA": "Fairness", "TR": "Transparency", "EX": "Explainability", 
                "AC": "Accountability", "DI": "Data Integrity", "RE": "Reliability",
                "SE": "Security", "PR": "Privacy", "SA": "Safety", 
                "IN": "Inclusivity", "SU": "Sustainability"
            }
        
        # Iterate through questions and match with sector actions
        questions_processed = 0
        actions_generated = 0
        for domain_data in questions_data:
            domain_info = domain_data.get('domain', {})
            questions = domain_data.get('questions', [])
            
            for question in questions:
                questions_processed += 1
                question_id = question.get('question_id', question.get('code', ''))
                # Score can be in different locations depending on data structure
                score = question.get('score', 0)
                if not score and question.get('answer'):
                    score = question['answer'].get('numeric_score', 0)
                
                # Get sector-specific action for this question
                sector_action_text = sector_specific.get(question_id)
                
                if questions_processed <= 3:
                    print(f"DEBUG _generate_sector_actions: Q {question_id} score={score} has_action={bool(sector_action_text)}")
                
                if sector_action_text and score in [1, 2, 3]:
                    # Get domain name from question ID prefix
                    domain_prefix = question_id.split("-")[0] if "-" in question_id else ""
                    domain_name = domain_mapping.get(domain_prefix, domain_info.get('name', 'Unknown'))
                    
                    action_item = {
                        'domain': domain_name,
                        'question_id': question_id,
                        'sector_action': sector_action_text,
                        'score': score
                    }
                    
                    actions_generated += 1
                    if score == 1:
                        sector_actions['high'].append(action_item)
                    elif score == 2:
                        sector_actions['medium'].append(action_item)
                    elif score == 3:
                        sector_actions['low'].append(action_item)
        
        # Sort each priority list by question_id for consistency
        for priority in ['high', 'medium', 'low']:
            sector_actions[priority].sort(key=lambda x: x.get('question_id', ''))
        
        print(f"DEBUG _generate_sector_actions: Processed {questions_processed} questions, generated {actions_generated} actions")
        print(f"Generated sector actions for {sector_name}: high={len(sector_actions['high'])}, medium={len(sector_actions['medium'])}, low={len(sector_actions['low'])}")
        
        return sector_actions
    
    async def _generate_ai_enhanced_executive_summary(self, report_data: Dict[str, Any]) -> str:
        """
        Generate an AI-enhanced executive summary using LLM.
        Falls back to template-based generation if AI fails.
        Uses new test prompts when use_test_template is enabled.
        """
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            
            # Extract key data for the prompt
            overall_score = report_data.get('overall', {}).get('score', 0)
            overall_tier = report_data.get('overall', {}).get('tier', 'Unknown')
            org_name = report_data.get('org', {}).get('name', 'the organization')
            system_info = report_data.get('system_info', {})
            system_name = system_info.get('systemName', system_info.get('system_name', 'the AI system'))
            industry = system_info.get('industry', '')
            
            # Get domain scores and detailed analysis
            heatmap_data = report_data.get('heatmap_data', {})
            domains = heatmap_data.get('domains', [])
            
            # Sort to find top and bottom performers with low-scoring question counts
            domain_scores = []
            for domain in domains:
                domain_name = domain.get('name', '')
                questions = domain.get('questions', [])
                scores = [q.get('score', 0) for q in questions if q.get('score') is not None]
                low_scoring_count = len([s for s in scores if s <= 2])
                if scores:
                    avg_pct = (sum(scores) / (len(scores) * 4)) * 100
                    domain_scores.append({
                        'name': domain_name, 
                        'percentage': avg_pct,
                        'question_count': len(scores),
                        'low_scoring_count': low_scoring_count
                    })
            
            sorted_domains = sorted(domain_scores, key=lambda x: x['percentage'], reverse=True)
            top_3 = sorted_domains[:3] if len(sorted_domains) >= 3 else sorted_domains
            bottom_3 = sorted_domains[-3:] if len(sorted_domains) >= 3 else sorted_domains
            
            # Calculate maturity distribution
            all_scores = []
            for domain in domains:
                questions = domain.get('questions', [])
                for q in questions:
                    if q.get('score') is not None:
                        all_scores.append(q.get('score', 0))
            
            non_ideal = len([s for s in all_scores if s == 1])
            basic = len([s for s in all_scores if s == 2])
            good = len([s for s in all_scores if s == 3])
            advanced = len([s for s in all_scores if s == 4])
            
            # Get priority actions counts
            actions = report_data.get('actions', {})
            high_priority_count = len(actions.get('high', []))
            medium_priority_count = len(actions.get('medium', []))
            low_priority_count = len(actions.get('low', []))
            
            # Get system context
            lifecycle = system_info.get('lifecycle', system_info.get('lifecycleStage', 'Unknown'))
            criticality = system_info.get('criticality', 'Unknown')
            hosting = system_info.get('hosting', system_info.get('cloudProvider', 'Unknown'))
            data_sensitivity = system_info.get('dataSensitivity', 'Unknown')
            oversight = system_info.get('oversight', system_info.get('humanOversight', 'Unknown'))
            
            if self.use_test_template:
                # NEW TEST PROMPT - Data-driven, conservative approach
                system_prompt = """You are generating the Executive Summary section of an AI System Maturity Assessment report using the AM AI SAFE framework. Your task is to produce a clear, executive-level summary that is fully grounded in the data provided.

⚠️ Critical rules:
- Only state facts that are explicitly provided in the input data.
- Do not invent policies, controls, processes, or cultural attributes.
- If you discuss reasons or drivers, clearly label them as "likely contributors" and base them on observable patterns (e.g. domain scores, concentration of low-scoring questions, or recommendation themes).
- Do not introduce any new numbers, percentages, counts, or rankings.
- Do not reference external regulations or frameworks unless explicitly included in the input.
- Avoid absolute claims such as "fully implemented", "comprehensive", "best practice", or "full marks" unless explicitly supported by the data.
- Do not use markdown formatting - write in plain text suitable for a Word document.

Heading format requirements:
- The Executive Summary section will be inserted into a Word document that already contains H1 headings.
- Any sub-headings you generate must be formatted as H2 only.
- Use the following exact format for all sub-headings:

Heading 2: <Heading text>

- Do not use H1, H3, bullet-styled headings, markdown (##), or HTML tags.
- Do not number the headings unless explicitly instructed.
- Do not repeat the section title as a heading."""

                user_prompt = f"""Write the Executive Summary for an AI System Maturity Assessment report.

ORGANISATION DETAILS:
- Organisation: {org_name}
- Industry: {industry}

ASSESSMENT CONTEXT:
- System Name: {system_name}
- Lifecycle Stage: {lifecycle}
- Business Criticality: {criticality}
- Hosting Model: {hosting}
- Data Sensitivity: {data_sensitivity}
- Oversight Arrangements: {oversight}

OVERALL RESULTS:
- Overall Maturity Score: {overall_score:.1f}%
- Maturity Tier: {overall_tier}

DOMAIN RESULTS (sorted by score):
{chr(10).join([f"- {d['name']}: {d['percentage']:.0f}% ({d['question_count']} questions, {d['low_scoring_count']} scoring low)" for d in sorted_domains])}

MATURITY DISTRIBUTION:
- Non-Ideal (score 1): {non_ideal} questions
- Basic (score 2): {basic} questions
- Good (score 3): {good} questions
- Advanced (score 4): {advanced} questions

PRIORITY ACTIONS:
- High priority: {high_priority_count} actions
- Medium priority: {medium_priority_count} actions
- Low priority: {low_priority_count} actions

TOP 3 STRENGTHS:
{chr(10).join([f"- {d['name']}: {d['percentage']:.0f}%" for d in top_3])}

TOP 3 GAPS:
{chr(10).join([f"- {d['name']}: {d['percentage']:.0f}%" for d in bottom_3])}

Required structure - Write the Executive Summary using the following structure exactly, in professional report language. Format each section heading as "Heading 2: <heading text>":

Heading 2: Purpose of the Assessment
Briefly restate the objective of the assessment and the scope of domains assessed.

Heading 2: Assessment Context
Summarise the system context using the provided lifecycle stage, criticality, hosting model, data sensitivity, and oversight arrangements. Do not infer risk beyond what this context reasonably implies.

Heading 2: Overall Maturity Outcome
State the overall AI maturity score and tier. Explain what this tier indicates at a high level (e.g. foundational, developing, established), without adding new metrics.

Heading 2: Domain-Level Performance Overview
Identify the strongest-performing domains and lowest-performing domains based on the provided scores. Where relevant, note patterns such as concentration of low-scoring questions. Any explanation of performance must be framed as likely contributors, not confirmed causes.

Heading 2: Key Insights
Provide 4–6 concise bullet points covering:
- Overall maturity position
- Strongest domain areas
- Primary risk or gap concentration
- Volume of high-priority actions identified
- Any notable maturity distribution pattern

Heading 2: Forward-Looking Summary
Conclude with a short paragraph outlining how addressing the identified priority actions would improve AI governance and maturity over time, without promising outcomes or timelines."""

            else:
                # ORIGINAL PROMPT
                system_prompt = """You are an expert AI governance consultant writing executive summaries for AI maturity assessment reports. 
Your writing style is professional, insightful, and actionable. Write in a formal business report tone.
Do not use markdown formatting - write in plain text suitable for a Word document.
Keep paragraphs concise but comprehensive."""

                user_prompt = f"""Write a comprehensive executive summary for an AI System Maturity Assessment report.

ASSESSMENT DATA:
- Organization: {org_name}
- AI System: {system_name}
- Industry: {industry}
- Overall Maturity Score: {overall_score:.1f}%
- Maturity Tier: {overall_tier}

TOP PERFORMING DOMAINS:
{chr(10).join([f"- {d['name']}: {d['percentage']:.0f}%" for d in top_3])}

AREAS REQUIRING IMPROVEMENT:
{chr(10).join([f"- {d['name']}: {d['percentage']:.0f}%" for d in bottom_3])}

Write an executive summary that includes:
1. Assessment objective and scope (mention the 11 domains and 88 questions of the AM AI SAFE framework)
2. Overall results interpretation with context for the {overall_tier} tier
3. Key strengths analysis - explain WHY these domains are performing well
4. Areas for improvement - explain the IMPLICATIONS of lower scores in these areas
5. Strategic recommendations summary (2-3 key actions)
6. Forward-looking statement about the organization's AI governance journey

The summary should be approximately 400-500 words, written as flowing paragraphs (not bullet points)."""

            # Initialize LLM chat
            chat = LlmChat(
                api_key="sk-emergent-01d3a5f175e7fB507B",
                session_id=f"exec_summary_{id(report_data)}",
                system_message=system_prompt
            ).with_model("openai", "gpt-4o-mini")
            
            # Send message and get response
            user_message = UserMessage(text=user_prompt)
            response = await chat.send_message(user_message)
            
            print(f"Successfully generated AI-enhanced executive summary (test_template={self.use_test_template})")
            return response.strip()
            
        except Exception as e:
            print(f"AI executive summary generation failed, using template: {str(e)}")
            return self._generate_comprehensive_executive_summary(report_data)
    
    async def _generate_ai_enhanced_key_findings(self, report_data: Dict[str, Any]) -> str:
        """
        Generate AI-enhanced key findings using LLM.
        Falls back to template-based generation if AI fails.
        Uses new test prompts when use_test_template is enabled.
        """
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            
            # Extract key data
            overall_score = report_data.get('overall', {}).get('score', 0)
            overall_tier = report_data.get('overall', {}).get('tier', 'Unknown')
            org_name = report_data.get('org', {}).get('name', 'the organization')
            system_info = report_data.get('system_info', {})
            system_name = system_info.get('systemName', system_info.get('system_name', 'the AI system'))
            industry = system_info.get('industry', '')
            
            # Get system context
            lifecycle = system_info.get('lifecycle', system_info.get('lifecycleStage', 'Unknown'))
            criticality = system_info.get('criticality', 'Unknown')
            
            # Get domain analysis
            heatmap_data = report_data.get('heatmap_data', {})
            domains = heatmap_data.get('domains', [])
            
            domain_analysis = []
            all_scores = []
            for domain in domains:
                domain_name = domain.get('name', '')
                questions = domain.get('questions', [])
                scores = [q.get('score', 0) for q in questions if q.get('score') is not None]
                all_scores.extend(scores)
                if scores:
                    avg_pct = (sum(scores) / (len(scores) * 4)) * 100
                    low_scores = len([s for s in scores if s <= 2])
                    domain_analysis.append({
                        'name': domain_name, 
                        'percentage': avg_pct,
                        'questions_assessed': len(scores),
                        'low_scoring_questions': low_scores
                    })
            
            sorted_domains = sorted(domain_analysis, key=lambda x: x['percentage'], reverse=True)
            
            # Calculate maturity distribution (question-level for test prompt)
            non_ideal = len([s for s in all_scores if s == 1])
            basic = len([s for s in all_scores if s == 2])
            good = len([s for s in all_scores if s == 3])
            advanced = len([s for s in all_scores if s == 4])
            
            # Calculate domain-level maturity distribution (for original prompt)
            high_maturity = len([d for d in domain_analysis if d['percentage'] >= 75])
            moderate_maturity = len([d for d in domain_analysis if 50 <= d['percentage'] < 75])
            developing_maturity = len([d for d in domain_analysis if 25 <= d['percentage'] < 50])
            foundational_maturity = len([d for d in domain_analysis if d['percentage'] < 25])
            
            # Get priority actions with domain distribution
            actions = report_data.get('actions', {})
            high_actions = actions.get('high', [])
            medium_actions = actions.get('medium', [])
            low_actions = actions.get('low', [])
            
            # Get top 3 strengths and gaps
            top_3 = sorted_domains[:3] if len(sorted_domains) >= 3 else sorted_domains
            bottom_3 = sorted_domains[-3:] if len(sorted_domains) >= 3 else sorted_domains
            
            if self.use_test_template:
                # NEW TEST PROMPT - Data-driven key findings
                system_prompt = """You are generating the Key Findings & Risk Themes section of an AI System Maturity Assessment report using the AM AI SAFE framework. Your role is to identify data-driven findings based strictly on the assessment results provided.

⚠️ Critical rules:
- Every finding must be traceable to explicit input data (scores, distributions, question concentrations, or recommendation themes).
- Do not introduce new statistics, benchmarks, or comparisons.
- Do not reference external organisations, laws, or standards unless explicitly provided.
- Avoid speculative language unless clearly framed as risk implication or likely impact.
- Do not repeat the Executive Summary; focus on analytical insights.
- Do not use markdown formatting - write in plain text suitable for a Word document.

Heading format requirements:
- The Key Findings section will be inserted into a Word document that already contains H1 headings.
- Any sub-headings you generate must be formatted as H2 only.
- Use the following exact format for all sub-headings:

Heading 2: <Heading text>

- Do not use H1, H3, bullet-styled headings, markdown (##), or HTML tags.
- Do not number the headings unless explicitly instructed.
- Do not repeat the section title as a heading."""

                # Format high priority actions for the prompt
                high_actions_text = chr(10).join([f"- {a.get('domain', 'Unknown')}: {a.get('question_id', 'N/A')} - {a.get('text', 'N/A')[:100]}..." for a in high_actions[:10]]) if high_actions else "None identified"
                
                user_prompt = f"""Write Key Findings & Risk Themes for an AI System Maturity Assessment report.

OVERALL MATURITY:
- Score: {overall_score:.1f}%
- Tier: {overall_tier}

DOMAIN-LEVEL SCORES (sorted by performance):
{chr(10).join([f"- {d['name']}: {d['percentage']:.0f}% ({d['questions_assessed']} questions, {d['low_scoring_questions']} low-scoring)" for d in sorted_domains])}

MATURITY DISTRIBUTION (question-level):
- Non-Ideal (score 1): {non_ideal} questions
- Basic (score 2): {basic} questions
- Good (score 3): {good} questions
- Advanced (score 4): {advanced} questions

PRIORITY ACTIONS:
- High priority: {len(high_actions)} actions
- Medium priority: {len(medium_actions)} actions
- Low priority: {len(low_actions)} actions

SAMPLE HIGH PRIORITY ACTIONS:
{high_actions_text}

TOP 3 STRENGTHS:
{chr(10).join([f"- {d['name']}: {d['percentage']:.0f}%" for d in top_3])}

TOP 3 GAPS:
{chr(10).join([f"- {d['name']}: {d['percentage']:.0f}%" for d in bottom_3])}

SYSTEM CONTEXT:
- Lifecycle Stage: {lifecycle}
- Business Criticality: {criticality}

Required output format - Produce 4 to 6 findings. For each finding, use the format below. Format each finding title as "Heading 2: Finding - [Short descriptive title]":

Heading 2: Finding - [Short descriptive title]

Observation: Describe the observable pattern in the assessment results (e.g. domain performance, maturity distribution, clustering of low scores).

Evidence: Reference the specific data points that support the observation (e.g. domains involved, relative scores, concentration of high-priority actions).

Risk Implication: Explain what this pattern may imply for AI governance, operational risk, assurance, or sustainability if not addressed.

Content expectations - Across the full set of findings, ensure you cover:
- At least one finding related to overall maturity distribution
- At least one finding comparing strong vs weak domains
- At least one finding based on concentration of high-priority actions
- At least one finding informed by system lifecycle or criticality

Style guidance:
- Analytical and precise
- Neutral and non-judgemental
- Suitable for inclusion in a regulator-facing or board-level report
- Avoid marketing language or recommendations (those appear later in the report)"""

            else:
                # ORIGINAL PROMPT
                system_prompt = """You are an expert AI governance analyst writing detailed findings for AI maturity assessment reports.
Your analysis is thorough, evidence-based, and provides actionable insights.
Write in a professional consulting report style with clear structure.
Do not use markdown formatting - write in plain text suitable for a Word document.
Use numbered sections and clear paragraph breaks."""

                user_prompt = f"""Write comprehensive key findings for an AI System Maturity Assessment report.

ASSESSMENT DATA:
- Organization: {org_name}
- AI System: {system_name}
- Industry: {industry}
- Overall Score: {overall_score:.1f}%
- Maturity Tier: {overall_tier}

MATURITY DISTRIBUTION:
- High Maturity (75%+): {high_maturity} domains
- Moderate Maturity (50-74%): {moderate_maturity} domains  
- Developing Maturity (25-49%): {developing_maturity} domains
- Foundational (<25%): {foundational_maturity} domains

DOMAIN-BY-DOMAIN SCORES:
{chr(10).join([f"- {d['name']}: {d['percentage']:.0f}% ({d['questions_assessed']} questions, {d['low_scoring_questions']} scoring low)" for d in sorted_domains])}

Write detailed key findings that include:

1. OVERALL MATURITY ASSESSMENT
   - Interpretation of the {overall_score:.1f}% score in context of the {industry} industry
   - What the {overall_tier} tier means for the organization

2. DOMAIN PERFORMANCE ANALYSIS
   - Analysis of the highest performing domain ({sorted_domains[0]['name']} at {sorted_domains[0]['percentage']:.0f}%)
   - Analysis of the lowest performing domain ({sorted_domains[-1]['name']} at {sorted_domains[-1]['percentage']:.0f}%)
   - Patterns and correlations across domains

3. RISK ASSESSMENT
   - Key risk areas based on low-scoring domains
   - Potential compliance and reputational implications
   - Areas requiring immediate attention

4. ORGANIZATIONAL READINESS
   - Assessment of governance maturity
   - Capability gaps identified
   - Resource and investment implications

5. COMPARATIVE INSIGHTS
   - How technical vs governance domains compare
   - Balance between AI capability and AI safety measures

6. CRITICAL SUCCESS FACTORS
   - What needs to happen for improvement
   - Key dependencies and enablers

The findings should be approximately 600-800 words with clear section headers."""

            # Initialize LLM chat
            chat = LlmChat(
                api_key="sk-emergent-01d3a5f175e7fB507B",
                session_id=f"key_findings_{id(report_data)}",
                system_message=system_prompt
            ).with_model("openai", "gpt-4o-mini")
            
            # Send message and get response
            user_message = UserMessage(text=user_prompt)
            response = await chat.send_message(user_message)
            
            print(f"Successfully generated AI-enhanced key findings (test_template={self.use_test_template})")
            return response.strip()
            
        except Exception as e:
            print(f"AI key findings generation failed, using template: {str(e)}")
            return self._generate_key_findings(report_data)
    
    def _get_default_template_path(self) -> str:
        """Get the default template path - using v9 template updated 10/07/2025."""  
        backend_dir = Path(__file__).parent
        return str(backend_dir / "templates" / "docx" / "AM_AI_SAFE_Report_TEMPLATE_v9_10072025.docx")
    
    # ========================================
    # AWARENESS AI NARRATIVE GENERATION
    # ========================================
    
    async def _generate_awareness_ai_narratives(self, report_data: Dict[str, Any], assessment: Dict[str, Any], db) -> Dict[str, str]:
        """
        Generate all AI narratives for Awareness assessments.
        Returns a dict with narrative keys that can be accessed as ai.executive_snapshot, etc.
        Caches results in the database to avoid regeneration.
        """
        narratives = {}
        assessment_id = assessment.get('id')
        
        # Check for cached narratives in database
        cached_narratives = assessment.get('ai_narratives', {})
        
        # Generate Executive Snapshot (AI-1)
        if cached_narratives.get('executive_snapshot'):
            narratives['executive_snapshot'] = cached_narratives['executive_snapshot']
            print(f"DEBUG: Using cached AI executive_snapshot narrative")
        else:
            try:
                narratives['executive_snapshot'] = await self._generate_ai_executive_snapshot(report_data)
                print(f"DEBUG: Generated new AI executive_snapshot narrative ({len(narratives['executive_snapshot'])} chars)")
            except Exception as e:
                print(f"ERROR generating AI executive_snapshot: {e}")
                narratives['executive_snapshot'] = ""
        
        # Generate Context Interpretation (AI-2)
        if cached_narratives.get('context_interpretation'):
            narratives['context_interpretation'] = cached_narratives['context_interpretation']
            print(f"DEBUG: Using cached AI context_interpretation narrative")
        else:
            try:
                narratives['context_interpretation'] = await self._generate_ai_context_interpretation(report_data)
                print(f"DEBUG: Generated new AI context_interpretation narrative ({len(narratives['context_interpretation'])} chars)")
            except Exception as e:
                print(f"ERROR generating AI context_interpretation: {e}")
                narratives['context_interpretation'] = ""
        
        # Generate Governance Interpretation (AI-3)
        if cached_narratives.get('governance_interpretation'):
            narratives['governance_interpretation'] = cached_narratives['governance_interpretation']
            print(f"DEBUG: Using cached AI governance_interpretation narrative")
        else:
            try:
                narratives['governance_interpretation'] = await self._generate_ai_governance_interpretation(report_data)
                print(f"DEBUG: Generated new AI governance_interpretation narrative ({len(narratives['governance_interpretation'])} chars)")
            except Exception as e:
                print(f"ERROR generating AI governance_interpretation: {e}")
                narratives['governance_interpretation'] = ""
        
        # Generate Readiness Interpretation (AI-4)
        if cached_narratives.get('readiness_interpretation'):
            narratives['readiness_interpretation'] = cached_narratives['readiness_interpretation']
            print(f"DEBUG: Using cached AI readiness_interpretation narrative")
        else:
            try:
                narratives['readiness_interpretation'] = await self._generate_ai_readiness_interpretation(report_data)
                print(f"DEBUG: Generated new AI readiness_interpretation narrative ({len(narratives['readiness_interpretation'])} chars)")
            except Exception as e:
                print(f"ERROR generating AI readiness_interpretation: {e}")
                narratives['readiness_interpretation'] = ""
        
        # Generate Domain Patterns (AI-5)
        if cached_narratives.get('domain_patterns'):
            narratives['domain_patterns'] = cached_narratives['domain_patterns']
            print(f"DEBUG: Using cached AI domain_patterns narrative")
        else:
            try:
                narratives['domain_patterns'] = await self._generate_ai_domain_patterns(report_data)
                print(f"DEBUG: Generated new AI domain_patterns narrative ({len(narratives['domain_patterns'])} chars)")
            except Exception as e:
                print(f"ERROR generating AI domain_patterns: {e}")
                narratives['domain_patterns'] = ""
        
        # Generate Action Interpretation (AI-6)
        if cached_narratives.get('action_interpretation'):
            narratives['action_interpretation'] = cached_narratives['action_interpretation']
            print(f"DEBUG: Using cached AI action_interpretation narrative")
        else:
            try:
                narratives['action_interpretation'] = await self._generate_ai_action_interpretation(report_data)
                print(f"DEBUG: Generated new AI action_interpretation narrative ({len(narratives['action_interpretation'])} chars)")
            except Exception as e:
                print(f"ERROR generating AI action_interpretation: {e}")
                narratives['action_interpretation'] = ""
        
        # Generate Next Focus (AI-7)
        if cached_narratives.get('next_focus'):
            narratives['next_focus'] = cached_narratives['next_focus']
            print(f"DEBUG: Using cached AI next_focus narrative")
        else:
            try:
                narratives['next_focus'] = await self._generate_ai_next_focus(report_data)
                print(f"DEBUG: Generated new AI next_focus narrative ({len(narratives['next_focus'])} chars)")
            except Exception as e:
                print(f"ERROR generating AI next_focus: {e}")
                narratives['next_focus'] = ""
        
        # Cache all generated narratives to database
        if narratives and assessment_id and db:
            try:
                await db.assessments.update_one(
                    {"id": assessment_id},
                    {"$set": {"ai_narratives": {**cached_narratives, **narratives}}}
                )
                print(f"DEBUG: Cached AI narratives to database")
            except Exception as e:
                print(f"ERROR caching AI narratives: {e}")
        
        return narratives
    
    async def _generate_ai_executive_snapshot(self, report_data: Dict[str, Any]) -> str:
        """
        Generate AI Executive Snapshot narrative for Awareness assessments.
        Used in: Section 1 – Executive Snapshot
        Variable target: ai.executive_snapshot
        """
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            
            # Extract data from report_data
            org_name = report_data.get('organization_name', 'The organisation')
            overall = report_data.get('overall', {})
            tier = overall.get('tier', 'Unknown')
            score = overall.get('percentage', overall.get('score', 0))
            strengths = report_data.get('strengths', [])
            gaps = report_data.get('gaps', [])
            industry = report_data.get('sector_name', report_data.get('industry', 'Unknown'))
            
            # Format lists as text (top 3 each)
            strengths_text = ", ".join(strengths[:3]) if strengths else "None identified"
            gaps_text = ", ".join(gaps[:3]) if gaps else "None identified"
            
            system_prompt = """You are generating the Executive Snapshot narrative for an AI Awareness & Foundations Assessment report."""
            
            user_prompt = f"""Your task is to explain the organisation's current AI awareness level in clear, executive-friendly language.

CRITICAL RULES:
- Use only the data provided.
- Do NOT invent policies, controls, or practices.
- Do NOT speculate about causes unless clearly framed as "this suggests".
- Do NOT provide recommendations or next steps.
- Do NOT repeat numeric scores more than once.
- Do NOT use bullet points.

INPUT DATA:
- Organisation name: {org_name}
- Awareness tier: {tier}
- Awareness score: {score}%
- Key strengths: {strengths_text}
- Key gaps: {gaps_text}
- Sector: {industry}

OUTPUT REQUIREMENTS:
- 120–180 words
- Neutral, confidence-building tone
- Written for senior leadership
- Focus on what the result indicates at this stage of AI maturity

Write 1–2 short paragraphs that:
1. Explain what the current awareness tier means in practical terms
2. Describe the general balance of strengths and gaps without listing them verbatim
3. Reinforce that this assessment reflects awareness and foundations only

Do not include headings or formatting."""

            # Initialize LLM chat
            chat = LlmChat(
                api_key="sk-emergent-01d3a5f175e7fB507B",
                session_id=f"awareness_executive_snapshot_{id(report_data)}",
                system_message=system_prompt
            ).with_model("openai", "gpt-4o-mini")
            
            # Send message and get response
            response = await chat.send_message(UserMessage(text=user_prompt))
            
            return response.strip()
            
        except Exception as e:
            print(f"ERROR in _generate_ai_executive_snapshot: {e}")
            return ""

    async def _generate_ai_context_interpretation(self, report_data: Dict[str, Any]) -> str:
        """
        Generate AI Context Interpretation narrative for Awareness assessments.
        Used in: Section 2 – Organisation & Context Profile
        Variable target: ai.context_interpretation
        """
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            
            # Extract data from report_data
            awareness_info = report_data.get('awareness_info', {})
            industry = awareness_info.get('industry', report_data.get('sector_name', 'Unknown'))
            ai_familiarity = awareness_info.get('ai_familiarity', 'Unknown')
            digital_maturity = awareness_info.get('digital_maturity', 'Unknown')
            leadership_ai_interest = awareness_info.get('leadership_ai_interest', 'Unknown')
            tech_change_comfort = awareness_info.get('tech_change_comfort', 'Unknown')
            
            system_prompt = """You are generating a contextual interpretation for an AI Awareness & Foundations Assessment."""
            
            user_prompt = f"""Your task is to translate onboarding and context metadata into a short, neutral interpretation that helps the reader understand the organisation's starting point with AI.

CRITICAL RULES:
- Do NOT make recommendations.
- Do NOT judge maturity as good or bad.
- Do NOT introduce external benchmarks.
- Frame all insights as implications, not conclusions.

INPUT DATA:
- Sector: {industry}
- AI familiarity: {ai_familiarity}
- Digital transformation stage: {digital_maturity}
- Leadership interest in AI: {leadership_ai_interest}
- Comfort with technology change: {tech_change_comfort}

OUTPUT REQUIREMENTS:
- 2–3 short paragraphs
- Plain English, non-technical
- Use phrasing such as "this suggests" or "this indicates"
- Emphasise readiness for learning rather than deployment

Do not use bullet points or headings."""

            # Initialize LLM chat
            chat = LlmChat(
                api_key="sk-emergent-01d3a5f175e7fB507B",
                session_id=f"awareness_context_interpretation_{id(report_data)}",
                system_message=system_prompt
            ).with_model("openai", "gpt-4o-mini")
            
            # Send message and get response
            response = await chat.send_message(UserMessage(text=user_prompt))
            
            return response.strip()
            
        except Exception as e:
            print(f"ERROR in _generate_ai_context_interpretation: {e}")
            return ""

    async def _generate_ai_governance_interpretation(self, report_data: Dict[str, Any]) -> str:
        """
        Generate AI Governance Foundations Interpretation narrative for Awareness assessments.
        Used in: Section 3 – Foundational Controls & Readiness Signals
        Variable target: ai.governance_interpretation
        """
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            
            # Get organization name and sector from awareness_info
            awareness_info = report_data.get('awareness_info', {})
            org_name = awareness_info.get('org_name', report_data.get('organization_name', 'The organisation'))
            industry = awareness_info.get('industry', report_data.get('sector_name', 'Unknown'))
            
            # Get governance_foundations (multi-select field)
            governance_foundations = awareness_info.get('governance_foundations', [])
            
            # Format governance foundations as a readable list
            if governance_foundations and len(governance_foundations) > 0:
                # Filter out "None of the above" if other items exist
                foundations_list = [f for f in governance_foundations if f != 'None of the above']
                if foundations_list:
                    governance_foundations_text = ", ".join(foundations_list)
                else:
                    governance_foundations_text = "None currently in place"
            else:
                governance_foundations_text = "None currently in place"
            
            system_prompt = """You are generating an interpretation of existing governance foundations for an AI Awareness & Foundations Assessment."""
            
            user_prompt = f"""Your task is to explain why the identified governance foundations (or lack thereof) matter at the awareness stage.

CRITICAL RULES:
- Do NOT prescribe specific policies or controls.
- Do NOT imply non-compliance or risk exposure.
- Normalise gaps where foundations are missing.
- Keep the focus on awareness, not enforcement.

INPUT DATA:
- Organisation name: {org_name}
- Sector: {industry}
- Identified governance foundations: {governance_foundations_text}
- Assessment stage: Awareness & Foundations

OUTPUT REQUIREMENTS:
- Exactly one paragraph
- 60–100 words
- Include wording similar to "At this stage…"
- Explain how foundations support safe learning and experimentation

Do not use bullet points."""

            # Initialize LLM chat
            chat = LlmChat(
                api_key="sk-emergent-01d3a5f175e7fB507B",
                session_id=f"awareness_governance_interpretation_{id(report_data)}",
                system_message=system_prompt
            ).with_model("openai", "gpt-4o-mini")
            
            # Send message and get response
            response = await chat.send_message(UserMessage(text=user_prompt))
            
            return response.strip()
            
        except Exception as e:
            print(f"ERROR in _generate_ai_governance_interpretation: {e}")
            return ""

    async def _generate_ai_readiness_interpretation(self, report_data: Dict[str, Any]) -> str:
        """
        Generate AI Digital & Data Readiness Interpretation narrative for Awareness assessments.
        Used in: Section 3 – Digital & Data Readiness Signals
        Variable target: ai.readiness_interpretation
        """
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            
            # Get readiness signals from awareness_info
            awareness_info = report_data.get('awareness_info', {})
            digital_initiatives_level = awareness_info.get('digital_initiatives_level', 'Unknown')
            data_skill_confidence = awareness_info.get('data_skill_confidence', 'Unknown')
            openness_to_learning = awareness_info.get('openness_to_learning', 'Unknown')
            
            system_prompt = """You are generating an interpretation of digital and data readiness signals for an AI Awareness & Foundations Assessment."""
            
            user_prompt = f"""Your task is to explain what the organisation's reported readiness signals imply for the pace and style of AI awareness activities.

CRITICAL RULES:
- Do NOT suggest deploying AI systems.
- Do NOT reference specific tools or technologies.
- Focus on learning readiness, not capability gaps.

INPUT DATA:
- Digital / automation activity: {digital_initiatives_level}
- Data & digital skill confidence: {data_skill_confidence}
- Openness to AI learning: {openness_to_learning}

OUTPUT REQUIREMENTS:
- 1 short paragraph (50–80 words)
- Calm, supportive tone
- Emphasise appropriate pacing and framing of awareness initiatives

No headings or bullet points."""

            # Initialize LLM chat
            chat = LlmChat(
                api_key="sk-emergent-01d3a5f175e7fB507B",
                session_id=f"awareness_readiness_interpretation_{id(report_data)}",
                system_message=system_prompt
            ).with_model("openai", "gpt-4o-mini")
            
            # Send message and get response
            response = await chat.send_message(UserMessage(text=user_prompt))
            
            return response.strip()
            
        except Exception as e:
            print(f"ERROR in _generate_ai_readiness_interpretation: {e}")
            return ""

    async def _generate_ai_domain_patterns(self, report_data: Dict[str, Any]) -> str:
        """
        Generate AI Domain-Level Pattern Summary narrative for Awareness assessments.
        Used in: Section 4 – Awareness Assessment Results
        Variable target: ai.domain_patterns
        """
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            
            # Extract domain data from heatmap_data
            heatmap_data = report_data.get('heatmap_data', {})
            domains = heatmap_data.get('domains', [])
            
            # Build domain summary for the prompt
            domain_summaries = []
            for domain in domains:
                domain_name = domain.get('name', 'Unknown')
                questions = domain.get('questions', [])
                scores = [q.get('score', 0) for q in questions if q.get('score') is not None]
                if scores:
                    avg_score = sum(scores) / len(scores)
                    percentage = (avg_score / 4) * 100
                    tier = self._calculate_tier(percentage)
                    domain_summaries.append(f"{domain_name}: {tier} ({percentage:.0f}%)")
            
            domains_text = "\n".join([f"- {d}" for d in domain_summaries]) if domain_summaries else "No domain data available"
            
            system_prompt = """You are generating a summary of domain-level patterns for an AI Awareness & Foundations Assessment."""
            
            user_prompt = f"""Your task is to identify high-level patterns across awareness domains without restating scores or listing domains individually.

CRITICAL RULES:
- Do NOT repeat numeric scores.
- Do NOT describe each domain one by one.
- Do NOT introduce causes or recommendations.

INPUT DATA:
- Domain names, tiers, and scores:
{domains_text}

OUTPUT REQUIREMENTS:
- 100–150 words
- Analytical but accessible tone
- Focus on balance, consistency, and spread of awareness
- Highlight whether results are relatively even or uneven across domains

Do not use bullet points or headings."""

            # Initialize LLM chat
            chat = LlmChat(
                api_key="sk-emergent-01d3a5f175e7fB507B",
                session_id=f"awareness_domain_patterns_{id(report_data)}",
                system_message=system_prompt
            ).with_model("openai", "gpt-4o-mini")
            
            # Send message and get response
            response = await chat.send_message(UserMessage(text=user_prompt))
            
            return response.strip()
            
        except Exception as e:
            print(f"ERROR in _generate_ai_domain_patterns: {e}")
            return ""

    async def _generate_ai_action_interpretation(self, report_data: Dict[str, Any]) -> str:
        """
        Generate AI Action Interpretation Narrative for Awareness assessments.
        Used in: Section 5 – Prioritised Awareness Actions
        Variable target: ai.action_interpretation
        """
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            
            # Get overall tier
            overall = report_data.get('overall', {})
            tier = overall.get('tier', 'Unknown')
            
            # Get actions and extract top 5 from each priority
            actions = report_data.get('actions', {})
            high_actions = actions.get('high', [])[:5]
            medium_actions = actions.get('medium', [])[:5]
            low_actions = actions.get('low', [])[:5]
            
            # Format actions for prompt
            def format_actions(action_list):
                if not action_list:
                    return "None"
                return "; ".join([a.get('text', a.get('sector_action', 'Action'))[:100] for a in action_list])
            
            high_text = format_actions(high_actions)
            medium_text = format_actions(medium_actions)
            low_text = format_actions(low_actions)
            
            system_prompt = """You are generating a short narrative to explain the prioritised awareness actions selected for this report."""
            
            user_prompt = f"""Your task is to explain why these actions matter at the current awareness stage and how they support safe progress.

CRITICAL RULES:
- Do NOT add new actions.
- Do NOT introduce timelines or delivery commitments.
- Do NOT escalate urgency beyond awareness stage.
- Reinforce that actions are intentionally limited.

INPUT DATA:
- Awareness tier: {tier}
- High priority actions: {high_text}
- Medium priority actions: {medium_text}
- Low priority actions: {low_text}

OUTPUT REQUIREMENTS:
- 80–120 words
- Reassuring, practical tone
- Emphasise focus, momentum, and learning
- Explicitly state that additional opportunities exist beyond those shown

No bullet points or headings."""

            # Initialize LLM chat
            chat = LlmChat(
                api_key="sk-emergent-01d3a5f175e7fB507B",
                session_id=f"awareness_action_interpretation_{id(report_data)}",
                system_message=system_prompt
            ).with_model("openai", "gpt-4o-mini")
            
            # Send message and get response
            response = await chat.send_message(UserMessage(text=user_prompt))
            
            return response.strip()
            
        except Exception as e:
            print(f"ERROR in _generate_ai_action_interpretation: {e}")
            return ""

    async def _generate_ai_next_focus(self, report_data: Dict[str, Any]) -> str:
        """
        Generate AI-powered next focus statement for Awareness assessments.
        Used in: Executive Snapshot section
        Variable target: next_focus
        """
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            
            # Get overall tier and gaps
            overall = report_data.get('overall', {})
            tier = overall.get('tier', 'Developing')
            
            # Build gaps summary from domains
            heatmap_data = report_data.get('heatmap_data', {})
            domains = heatmap_data.get('domains', [])
            
            gaps = []
            for domain in domains:
                domain_name = domain.get('name', 'Unknown')
                questions = domain.get('questions', [])
                scores = [q.get('score', 0) for q in questions if q.get('score') is not None]
                if scores:
                    percentage = (sum(scores) / (len(scores) * 4)) * 100
                    if percentage < 50:
                        gaps.append(f"{domain_name} ({percentage:.0f}%)")
            
            gaps_summary = ', '.join(gaps[:3]) if gaps else 'No critical gaps identified'
            
            system_prompt = """You are generating a short "next focus" statement for an AI Awareness & Foundations Assessment executive summary."""
            
            user_prompt = f"""Generate a short "next focus" statement (6–12 words) that reflects the organisation's current AI awareness tier and top gaps.

Rules:
- One sentence fragment only
- No recommendations or timelines
- No technical language
- Suitable for an executive summary
- A short, plain-English focus statement (6–12 words)
- Action-oriented but non-prescriptive
- Aligned to the current awareness stage

Inputs:
- Awareness tier: {tier}
- Top gaps: {gaps_summary}

Output only the focus statement, nothing else."""

            # Initialize LLM chat
            chat = LlmChat(
                api_key="sk-emergent-01d3a5f175e7fB507B",
                session_id=f"awareness_next_focus_{id(report_data)}",
                system_message=system_prompt
            ).with_model("openai", "gpt-4o-mini")
            
            # Send message and get response
            response = await chat.send_message(UserMessage(text=user_prompt))
            
            return response.strip()
            
        except Exception as e:
            print(f"ERROR in _generate_ai_next_focus: {e}")
            return "Build foundational AI awareness across all domains"

    def _get_test_template_path(self) -> str:
        """Get the test template path for testing new template structure."""  
        backend_dir = Path(__file__).parent
        return str(backend_dir / "templates" / "docx" / "AM_AI_SAFE_SYSTEM_test_template.docx")
    
    def _get_test_schema_path(self) -> str:
        """Get the test schema path for validation."""
        backend_dir = Path(__file__).parent
        return str(backend_dir / "Test_System_report_schema.json")
    
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
                            user_data: Dict[str, Any], view_type: str = "heatmap", 
                            benchmark_data: Dict[str, Any] = None,
                            use_ai: bool = False) -> Tuple[bytes, bytes]:
        """
        Generate DOCX and PDF reports from assessment data.
        
        Args:
            assessment_id: The assessment ID
            assessment_data: Raw assessment data from database
            user_data: User information
            view_type: Type of visualization ('heatmap' or 'radar')
            benchmark_data: Benchmark data for radar chart comparison (optional)
            use_ai: Whether to use AI for enhanced narrative generation
            
        Returns:
            Tuple of (docx_bytes, pdf_bytes)
        """
        # Transform data to match report model
        report_data = self._transform_assessment_data(assessment_data, user_data)
        
        # Generate AI-enhanced content if requested
        if use_ai:
            print("=== GENERATING AI-ENHANCED CONTENT ===")
            try:
                ai_exec_summary = await self._generate_ai_enhanced_executive_summary(report_data)
                report_data['ai_executive_summary'] = ai_exec_summary
                print(f"AI Executive Summary generated: {len(ai_exec_summary)} chars")
            except Exception as e:
                print(f"AI Executive Summary failed: {e}")
                
            try:
                ai_key_findings = await self._generate_ai_enhanced_key_findings(report_data)
                report_data['ai_key_findings'] = ai_key_findings
                print(f"AI Key Findings generated: {len(ai_key_findings)} chars")
            except Exception as e:
                print(f"AI Key Findings failed: {e}")
        
        # Generate visualization image based on view_type
        print(f"=== VISUALIZATION GENERATION ===")
        print(f"View Type: {view_type}")
        print(f"Benchmark Data Available: {benchmark_data is not None}")
        
        if view_type == "radar" and benchmark_data:
            print("Generating radar chart WITH benchmarks")
            visualization_image = self._generate_radar_chart_with_benchmark(report_data, benchmark_data)
        elif view_type == "radar":
            print("Generating radar chart WITHOUT benchmarks")
            visualization_image = self._generate_radar_chart_image(report_data)
        else:  # default to heatmap
            print("Generating heatmap")
            visualization_image = self._generate_heatmap_image(report_data)
        
        print(f"Visualization image size: {len(visualization_image)} bytes")
        
        # Generate DOCX report
        docx_bytes = self._generate_docx_report(report_data, visualization_image)
        
        # Generate PDF using HTML-to-PDF conversion (WeasyPrint)
        try:
            pdf_bytes = self._generate_html_pdf(assessment_data, user_data)
            print("DEBUG: Using HTML-to-PDF conversion successfully")
        except Exception as e:
            print(f"WARNING: HTML-to-PDF failed ({str(e)}), falling back to LibreOffice conversion")
            # Fallback to LibreOffice conversion
            pdf_bytes = self._convert_docx_to_pdf(docx_bytes)
        
        return docx_bytes, pdf_bytes
    
    def _generate_html_pdf(self, assessment_data: Dict[str, Any], user_data: Dict[str, Any]) -> bytes:
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
            
            # Transform the assessment data to report format
            report_data = self._transform_assessment_data(assessment_data, user_data)
            
            # Generate heatmap as data URL for embedding in HTML
            heatmap_data_url = self._generate_heatmap_data_url(report_data)
            
            # Use the transformed report data directly as template context
            template_context = report_data
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

    # NOTE: _prepare_template_context method removed - now using direct template context
    
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
        
        # Get sector info from assessment data
        sector_name = assessment_data.get('sector_name', '')
        sector_actions = assessment_data.get('sector_actions', {'high': [], 'medium': [], 'low': []})
        
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
            "heatmap_data": self._prepare_heatmap_data(questions_data),
            "questions_data": questions_data,  # Pass through for sector action generation
            "sector_name": sector_name,
            "sector_actions": sector_actions,
            "system_info": assessment_data.get('system_info', {}),  # Pass system_info for template use
            "awareness_info": assessment_data.get('awareness_info', {}),  # Pass awareness_info for Awareness assessments
            "benchmark_data": self._load_benchmark_data(sector_name),  # Load sector benchmark data
            "ai_narratives": assessment_data.get('ai_narratives', {})  # Pass AI narratives for template use
        }
        
        return report_data
    
    def _load_benchmark_data(self, sector_name: str) -> Dict[str, float]:
        """Load sector benchmark data for the radar chart."""
        try:
            import json
            backend_dir = Path(__file__).parent
            
            # Choose the right benchmark file based on assessment type
            if self.assessment_type == 'Awareness':
                benchmark_path = backend_dir / "awareness_benchmarks.json"
            else:
                benchmark_path = backend_dir / "benchmarks.json"
            
            if not benchmark_path.exists():
                print(f"Benchmark file not found: {benchmark_path}")
                return {}
            
            with open(benchmark_path, 'r') as f:
                benchmarks_data = json.load(f)
            
            # Get sector-specific benchmarks
            sector_benchmarks = benchmarks_data.get("benchmarks", {}).get(sector_name, {})
            
            # If sector not found, try "Other"
            if not sector_benchmarks:
                sector_benchmarks = benchmarks_data.get("benchmarks", {}).get("Other", {})
            
            # Convert range strings (like "48-55") to mid-point values
            benchmark_values = {}
            for domain, range_str in sector_benchmarks.items():
                if isinstance(range_str, str) and '-' in range_str:
                    # Parse range and take midpoint
                    parts = range_str.split('-')
                    try:
                        low = float(parts[0])
                        high = float(parts[1])
                        benchmark_values[domain] = (low + high) / 2
                    except (ValueError, IndexError):
                        benchmark_values[domain] = 50.0  # Default
                elif isinstance(range_str, (int, float)):
                    benchmark_values[domain] = float(range_str)
                else:
                    benchmark_values[domain] = 50.0  # Default
            
            print(f"DEBUG: Loaded benchmark data for sector '{sector_name}': {benchmark_values}")
            return benchmark_values
            
        except Exception as e:
            print(f"Error loading benchmark data: {str(e)}")
            return {}
    
    def _calculate_tier(self, percentage: float) -> str:
        """Calculate the maturity tier based on percentage score.
        
        Categories (based on 1-4 scoring scale):
        1. Leading (91–100%) 
        2. Established (76–90%) 
        3. Developing (51–75%) 
        4. Foundational (0–50%)
        """
        if percentage >= 91:
            return "Leading"
        elif percentage >= 76:
            return "Established"
        elif percentage >= 51:
            return "Developing"
        else:
            return "Foundational"
    
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
        
        Priority Mapping Rules (updated for 1-4 scoring scale):
        - Score 1 (Foundational) → High Priority → actions.high
        - Score 2 (Developing) → Medium Priority → actions.medium  
        - Score 3 (Established) → Low Priority → actions.low
        - Score 4 (Leading) → not included in report
        
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
                
                if score is not None and score < 4:  # Only include non-perfect scores
                    # Determine priority based on score (1-4 scale)
                    if score == 1:
                        priority = "high"
                    elif score == 2:
                        priority = "medium"
                    elif score == 3:
                        priority = "low"
                    else:
                        continue  # Skip score 4 (leading practice)
                    
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
            
            # Only pad/limit to 8 questions for System assessments
            # Awareness assessments have 5 questions per domain
            if self.assessment_type != 'Awareness':
                # Pad to 8 questions if needed (for System assessments)
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
        """Generate heatmap image based on assessment type."""
        # Check if this is an Awareness assessment
        if self.assessment_type == 'Awareness':
            return self._generate_awareness_heatmap_image(report_data)
        else:
            return self._generate_system_heatmap_image(report_data)
    
    def _generate_awareness_bar_image(self, report_data: Dict[str, Any]) -> bytes:
        """Generate stacked bar chart image for Awareness assessments showing overall score and tier."""
        overall = report_data.get('overall', {})
        score = overall.get('score', 0)
        sector_average = report_data.get('sector_average')
        
        # Define the 4 maturity tiers for Awareness (matching frontend MaturityStackedColumn)
        tiers = [
            {'name': 'Established', 'min': 86, 'max': 100, 'color': '#00B050', 'percentage': 15},
            {'name': 'Developing', 'min': 66, 'max': 85, 'color': '#FFFF00', 'percentage': 20},
            {'name': 'Emerging', 'min': 41, 'max': 65, 'color': '#FFC000', 'percentage': 25},
            {'name': 'Introductory', 'min': 0, 'max': 40, 'color': '#FF0000', 'percentage': 40}
        ]
        
        # Determine current tier
        current_tier = 'Introductory'
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
        
        # Draw from bottom to top (Introductory to Established)
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
        
        # Add score arrow (right side, pointing left)
        arrow_y = score  # Score directly maps to y position (0-100)
        
        # Determine arrow color based on sector average comparison
        if sector_average is not None:
            if score > sector_average:
                arrow_color = '#00B050'  # Green - above average
            elif score < sector_average:
                arrow_color = '#FF0000'  # Red - below average
            else:
                arrow_color = '#000000'  # Black - equal
        else:
            arrow_color = '#000000'
        
        # Draw user score arrow (pointing left from right side)
        ax.annotate('', xy=(bar_x + bar_width/2, arrow_y), 
                   xytext=(bar_x + bar_width/2 + 0.3, arrow_y),
                   arrowprops=dict(arrowstyle='->', color=arrow_color, lw=2))
        
        # Add sector average arrow if available (left side, pointing right)
        if sector_average is not None and sector_average != score:
            ax.annotate('', xy=(bar_x - bar_width/2, sector_average), 
                       xytext=(bar_x - bar_width/2 - 0.3, sector_average),
                       arrowprops=dict(arrowstyle='->', color='#000000', lw=2))
        
        # Add score text on right
        ax.text(bar_x + bar_width/2 + 0.5, arrow_y, f'{score:.0f}%', 
               ha='left', va='center', fontsize=12, fontweight='bold', color=arrow_color)
        ax.text(bar_x + bar_width/2 + 0.5, arrow_y - 8, f'{current_tier}', 
               ha='left', va='center', fontsize=9, color='#666666')
        ax.text(bar_x + bar_width/2 + 0.5, arrow_y - 15, 'AI Awareness', 
               ha='left', va='center', fontsize=9, color='#666666')
        
        # Set axis limits and remove axes
        ax.set_xlim(-0.5, 2.5)
        ax.set_ylim(-5, 105)
        ax.axis('off')
        
        plt.tight_layout()
        
        # Save to bytes
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none', pad_inches=0.1)
        plt.close(fig)
        buffer.seek(0)
        
        return buffer.getvalue()

    def _generate_awareness_heatmap_image(self, report_data: Dict[str, Any]) -> bytes:
        """Generate heatmap image for Awareness assessments (5 domains, 5 questions each)."""
        heatmap_data = report_data.get('heatmap_data', {})
        domains = heatmap_data.get('domains', [])
        
        if not domains:
            domains = [{'name': 'No Data', 'questions': [{'code': 'N/A', 'score': 0} for _ in range(5)]}]
        
        # Create figure - sized for 5x5 grid
        fig, ax = plt.subplots(figsize=(10, 7))
        
        # Define colors for 1-4 scale
        def get_color(score):
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
                
                color = get_color(score)
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
    
    def _generate_system_heatmap_image(self, report_data: Dict[str, Any]) -> bytes:
        """Generate heatmap image for System assessments (11 domains, 8 questions each)."""
        heatmap_data = report_data.get('heatmap_data', {})
        domains = heatmap_data.get('domains', [])
        
        if not domains:
            # Create minimal empty heatmap
            domains = [{'name': 'No Data', 'questions': [{'code': 'N/A', 'score': 0} for _ in range(8)]}]
        
        # Create figure with optimized height for compact rows
        fig, ax = plt.subplots(figsize=(12, 6.5))
        
        # Define colors for 1-4 scale
        def get_color(score):
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
        
        # Create the heatmap grid exactly like the screenshot
        num_domains = len(domains)
        
        for i, domain in enumerate(domains):
            domain_name = domain['name']
            questions = domain['questions']
            
            # Calculate percentage score for left side (like in screenshot)
            total_possible = len([q for q in questions if q['code'] != 'N/A']) * 4  # 1-4 scale
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
    
    def _generate_radar_chart_image(self, report_data: Dict[str, Any]) -> bytes:
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
            
            # Domain name mapping for matching benchmark keys
            domain_name_mapping = {
                # Awareness domains
                'Awareness & Understanding': ['Awareness & Understanding', 'Awareness'],
                'Governance & Trust Foundations': ['Governance & Trust Foundations', 'Governance'],
                'People & Skills': ['People & Skills', 'People'],
                'Leadership Vision': ['Leadership & Vision', 'Leadership Vision', 'Leadership'],
                'Digital Readiness': ['Data & Digital Readiness', 'Digital Readiness', 'Data'],
                # System domains (for completeness)
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
                'Sustainability': ['Sustainability']
            }
            
            # Try to match benchmark domains to our domains
            for domain_name in domains:
                benchmark_value = None
                
                # Try direct match first
                if domain_name in benchmark_data:
                    benchmark_value = benchmark_data[domain_name]
                else:
                    # Try alternative names
                    alternatives = domain_name_mapping.get(domain_name, [domain_name])
                    for alt_name in alternatives:
                        if alt_name in benchmark_data:
                            benchmark_value = benchmark_data[alt_name]
                            break
                
                # If no specific benchmark, use a default of 50% (sector average)
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
            
            # Determine title based on assessment type
            if self.assessment_type == 'Awareness':
                title = 'AI Awareness vs Sector Benchmark'
            else:
                title = 'AI Maturity vs Sector Benchmark'
            
            # Add title (removed - will be in template)
            # ax.set_title(title, size=14, pad=20, fontweight='bold')
            
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
    
    
    def _generate_radar_chart_with_benchmark(self, report_data: Dict[str, Any], benchmark_data: Dict[str, Any]) -> bytes:
        """Generate radar chart comparing organization scores with sector benchmarks."""
        try:
            domain_scores = report_data.get('domain_scores', {})
            sector_name = benchmark_data.get('sector', 'Industry')
            benchmarks = benchmark_data.get('benchmarks', {})
            
            if not domain_scores or not benchmarks:
                # Return simple radar chart if no benchmark data
                return self._generate_radar_chart_image(report_data)
            
            # Prepare data for radar chart - match domain order from benchmarks
            domain_names = []
            user_scores = []
            benchmark_scores = []
            
            # Get domain names from benchmarks to ensure consistent ordering
            for domain_name in benchmarks.keys():
                if domain_name in domain_scores:
                    domain_names.append(domain_name)
                    
                    # Calculate user's average score for this domain
                    score_list = domain_scores[domain_name]
                    avg_score = sum(score_list) / len(score_list) if score_list else 0
                    user_percentage = (avg_score / 4) * 100  # 1-4 scale to percentage
                    user_scores.append(user_percentage)
                    
                    # Get benchmark score
                    benchmark_scores.append(benchmarks[domain_name])
            
            if not domain_names:
                # No matching domains, return simple radar chart
                return self._generate_radar_chart_image(report_data)
            
            # Number of variables
            num_vars = len(domain_names)
            
            # Compute angle for each axis
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
            
            # Complete the loop
            user_scores_plot = user_scores + user_scores[:1]
            benchmark_scores_plot = benchmark_scores + benchmark_scores[:1]
            angles_plot = angles + angles[:1]
            
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
            
            # Plot user data
            ax.plot(angles_plot, user_scores_plot, 'o-', linewidth=2.5, 
                   color='#3b82f6', label='Your Score', markersize=8)
            ax.fill(angles_plot, user_scores_plot, alpha=0.25, color='#3b82f6')
            
            # Plot benchmark data
            ax.plot(angles_plot, benchmark_scores_plot, 's--', linewidth=2, 
                   color='#10b981', label=f'{sector_name} Benchmark', markersize=6)
            ax.fill(angles_plot, benchmark_scores_plot, alpha=0.15, color='#10b981')
            
            # Fix axis to go in the right order
            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)
            
            # Set labels
            ax.set_xticks(angles)
            ax.set_xticklabels(domain_names, size=10, fontweight='bold')
            
            # Set y-axis limits and ticks
            ax.set_ylim(0, 100)
            ax.set_yticks([25, 50, 75, 100])
            ax.set_yticklabels(['25%', '50%', '75%', '100%'], size=9)
            
            # Add grid
            ax.grid(True, linestyle='--', alpha=0.7, linewidth=0.5)
            
            # Add title
            ax.set_title(f'Domain Performance vs {sector_name} Benchmark', 
                        size=14, pad=20, fontweight='bold')
            
            # Add legend
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), framealpha=0.9, fontsize=10)
            
            # Save to bytes
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=200, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            img_buffer.seek(0)
            img_bytes = img_buffer.getvalue()
            plt.close(fig)
            
            return img_bytes
            
        except Exception as e:
            print(f"Error generating radar chart with benchmark: {str(e)}")
            import traceback
            traceback.print_exc()
            # Fallback to simple radar chart
            return self._generate_radar_chart_image(report_data)

    def _format_top_3_strengths(self, report_data: Dict[str, Any]) -> list:
        """Get top 3 highest scoring domains."""
        domain_scores = report_data.get('domain_scores', {})
        
        # Calculate average percentage for each domain
        domain_percentages = []
        for domain_name, score_list in domain_scores.items():
            avg_score = sum(score_list) / len(score_list) if score_list else 0
            percentage = (avg_score / 4) * 100  # 1-4 scale
            domain_percentages.append({
                'domain': domain_name,
                'percentage': f"{percentage:.1f}%"
            })
        
        # Sort by percentage (highest first) and take top 3
        domain_percentages.sort(key=lambda x: float(x['percentage'].rstrip('%')), reverse=True)
        return domain_percentages[:3]
    
    def _format_top_3_gaps(self, report_data: Dict[str, Any]) -> list:
        """Get top 3 lowest scoring domains."""
        domain_scores = report_data.get('domain_scores', {})
        
        # Calculate average percentage for each domain
        domain_percentages = []
        for domain_name, score_list in domain_scores.items():
            avg_score = sum(score_list) / len(score_list) if score_list else 0
            percentage = (avg_score / 4) * 100  # 1-4 scale
            domain_percentages.append({
                'domain': domain_name,
                'percentage': f"{percentage:.1f}%"
            })
        
        # Sort by percentage (lowest first) and take top 3
        domain_percentages.sort(key=lambda x: float(x['percentage'].rstrip('%')))
        return domain_percentages[:3]
    
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
                analysis += f"Average Score: {avg_score:.1f}/4.0 | Range: {min_score}-{max_score} | Questions Evaluated: {len(scores)}\n"
                
                # Add domain-specific insights (updated for 1-4 scale)
                if avg_score < 2.0:
                    analysis += f"Critical Focus Area: {domain_name} requires immediate attention with systematic capability building and resource investment.\n"
                elif avg_score < 3.0:
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
The assessment evaluated 88 specific questions across 11 domains, with each question scored on a 4-point scale (1=Foundational, 2=Developing, 3=Established, 4=Leading).

DOMAIN PERFORMANCE HIGHLIGHTS:"""

        if highest_domain and lowest_domain:
            results += f"""
• Highest Performing Domain: {highest_domain['name']} ({highest_domain['avg_score']:.1f}/4.0 average)
• Area for Greatest Improvement: {lowest_domain['name']} ({lowest_domain['avg_score']:.1f}/4.0 average)"""

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
    
    def _populate_awareness_sector_tables(self, doc: DocxTemplate, report_data: Dict[str, Any]) -> None:
        """
        Programmatically populate the sector action tables for Awareness assessments.
        Uses sector_actions which has question_id, domain, and sector_action fields.
        Column order: Question ID | Domain | Recommended Action
        """
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        from copy import deepcopy
        
        docx_doc = doc.docx
        tables = docx_doc.tables
        
        if len(tables) < 3:
            print(f"Warning: Expected at least 3 tables in template, found {len(tables)}")
            return
        
        # Get the last 3 tables (High, Medium, Low priority sector actions)
        high_table = tables[-3]
        medium_table = tables[-2]
        low_table = tables[-1]
        
        # Get sector_actions from report_data
        sector_actions = report_data.get('sector_actions', {'high': [], 'medium': [], 'low': []})
        high_actions = sector_actions.get('high', [])[:5]  # Top 5
        medium_actions = sector_actions.get('medium', [])[:5]
        low_actions = sector_actions.get('low', [])[:5]
        
        print(f"Populating Awareness sector tables: High={len(high_actions)}, Medium={len(medium_actions)}, Low={len(low_actions)}")
        
        # Populate each table with correct column order and field names
        self._populate_sector_table(high_table, high_actions)
        self._populate_sector_table(medium_table, medium_actions)
        self._populate_sector_table(low_table, low_actions)
    
    def _populate_sector_table(self, table, actions: List[Dict[str, Any]]) -> None:
        """
        Populate a sector actions table with the correct column order.
        Column 1: Question ID (action.question_id)
        Column 2: Domain (action.domain)
        Column 3: Recommended Action (action.sector_action)
        """
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        from copy import deepcopy
        
        # Remove all rows except header
        while len(table.rows) > 1:
            self._remove_row(table, 1)
        
        if not actions:
            print(f"DEBUG: No actions to add, keeping only header row")
            return
        
        header_row = table.rows[0]
        header_tr = header_row._tr
        tbl = table._element
        
        for action in actions:
            tr = deepcopy(header_tr)
            cells = tr.findall('.//w:tc', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
            
            if len(cells) >= 3:
                # CORRECT ORDER: Question ID, Domain, Sector Action
                values = [
                    action.get('question_id', ''),
                    action.get('domain', ''),
                    action.get('sector_action', '')
                ]
                
                for i in range(3):
                    cell = cells[i]
                    
                    # Remove header background color
                    tcPr = cell.find('.//w:tcPr', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
                    if tcPr is not None:
                        shd = tcPr.find('.//w:shd', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
                        if shd is not None:
                            tcPr.remove(shd)
                    
                    # Clear existing content
                    for p in cell.findall('.//w:p', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
                        cell.remove(p)
                    
                    # Add new paragraph
                    p = OxmlElement('w:p')
                    
                    if values[i]:
                        r = OxmlElement('w:r')
                        rPr = OxmlElement('w:rPr')
                        
                        rFonts = OxmlElement('w:rFonts')
                        rFonts.set(qn('w:ascii'), 'Arial')
                        rFonts.set(qn('w:hAnsi'), 'Arial')
                        rPr.append(rFonts)
                        
                        sz = OxmlElement('w:sz')
                        sz.set(qn('w:val'), '20')
                        rPr.append(sz)
                        
                        r.append(rPr)
                        
                        t = OxmlElement('w:t')
                        t.text = values[i]
                        r.append(t)
                        p.append(r)
                    
                    cell.append(p)
                
                # Remove extra cells
                for i in range(3, len(cells)):
                    tr.remove(cells[i])
            
            tbl.append(tr)
        
        print(f"DEBUG: Added {len(actions)} sector action rows")
    
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
    
    def _center_align_images(self, doc: DocxTemplate) -> None:
        """Center-align all paragraphs containing images in the document."""
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        
        docx_doc = doc.docx
        
        images_centered = 0
        for paragraph in docx_doc.paragraphs:
            # Check if paragraph contains an image (drawing element)
            has_image = False
            for run in paragraph.runs:
                if run._element.findall('.//a:blip', namespaces={
                    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
                }):
                    has_image = True
                    break
                # Also check for inline images
                if run._element.findall('.//w:drawing', namespaces={
                    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
                }):
                    has_image = True
                    break
            
            if has_image:
                # Center-align the paragraph
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                images_centered += 1
        
        print(f"DEBUG: Center-aligned {images_centered} paragraphs containing images")


    def _calculate_maturity_distribution(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate maturity distribution for test template schema."""
        heatmap_data = report_data.get('heatmap_data', {})
        domains = heatmap_data.get('domains', [])
        
        all_scores = []
        for domain in domains:
            questions = domain.get('questions', [])
            for q in questions:
                if q.get('score') is not None:
                    all_scores.append(q.get('score', 0))
        
        non_ideal = len([s for s in all_scores if s == 1])
        basic = len([s for s in all_scores if s == 2])
        good = len([s for s in all_scores if s == 3])
        advanced = len([s for s in all_scores if s == 4])
        total = len(all_scores) if all_scores else 1
        
        return {
            'non_ideal': non_ideal,
            'basic': basic,
            'good': good,
            'advanced': advanced,
            'total_questions': total,
            'percent': {
                'non_ideal': round((non_ideal / total) * 100, 1) if total > 0 else 0,
                'basic': round((basic / total) * 100, 1) if total > 0 else 0,
                'good': round((good / total) * 100, 1) if total > 0 else 0,
                'advanced': round((advanced / total) * 100, 1) if total > 0 else 0
            }
        }
    
    def _format_domains_for_template(self, report_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format domain results for test template schema."""
        heatmap_data = report_data.get('heatmap_data', {})
        domains = heatmap_data.get('domains', [])
        
        print(f"DEBUG _format_domains_for_template: {len(domains)} domains")
        
        result = []
        for domain in domains:
            domain_name = domain.get('name', '')
            questions = domain.get('questions', [])
            scores = [q.get('score', 0) for q in questions if q.get('score') is not None]
            
            print(f"  Domain '{domain_name}': {len(questions)} questions, {len(scores)} scores, scores={scores}")
            
            if scores:
                # For Awareness: 5 questions * 4 max = 20 points max per domain
                # For System: 8 questions * 4 max = 32 points max per domain
                avg_pct = (sum(scores) / (len(scores) * 4)) * 100
                low_scoring = [q for q in questions if q.get('score') is not None and q.get('score', 0) <= 2]
                
                print(f"    sum(scores)={sum(scores)}, len(scores)={len(scores)}, max_possible={len(scores)*4}, avg_pct={avg_pct:.1f}%")
                
                # Determine tier based on score
                if avg_pct >= 75:
                    tier = "Advanced"
                elif avg_pct >= 50:
                    tier = "Good"
                elif avg_pct >= 25:
                    tier = "Basic"
                else:
                    tier = "Non-Ideal"
                
                result.append({
                    'name': domain_name,
                    'score': round(avg_pct, 1),
                    'tier': tier,
                    'question_count': len(scores),
                    'low_scoring_question_count': len(low_scoring),
                    'top_low_questions': [
                        {
                            'question_id': q.get('code', 'N/A'),
                            'question_text': q.get('text', 'N/A')[:100],
                            'score': round((q.get('score', 0) / 4) * 100, 1)
                        }
                        for q in sorted(low_scoring, key=lambda x: x.get('score', 0))[:5]
                    ]
                })
        
        return result

    def _normalize_system_info(self, system_info: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize system_info field names for test template compatibility."""
        return {
            'lifecycle': system_info.get('lifecycle', system_info.get('lifecycleStage', 'Unknown')),
            'criticality': system_info.get('criticality', 'Unknown'),
            'ownership': system_info.get('ownership', system_info.get('systemOwnership', 'Unknown')),
            'hosting': system_info.get('hosting', system_info.get('cloudProvider', 'Unknown')),
            'dataSensitivity': system_info.get('dataSensitivity', 'Unknown'),
            'oversight': system_info.get('oversight', system_info.get('humanOversight', 'Unknown')),
            'system_name': system_info.get('system_name', system_info.get('systemName', 'AI System')),
            'system_description': system_info.get('system_description', system_info.get('systemDescription', '')),
            # Keep original fields too for backwards compatibility
            **system_info
        }
    
    def _build_actions_with_summary(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build actions structure with summary for templates.
        Provides BOTH score-based and smart priority orderings.
        """
        actions = report_data.get('actions', {})
        sector_actions = report_data.get('sector_actions', {})
        
        # Load question metadata for smart priority calculation
        question_metadata = self._load_question_metadata()
        
        print(f"DEBUG _build_actions_with_summary:")
        print(f"  - actions keys: {actions.keys() if actions else 'None'}")
        print(f"  - use_smart_priority: {self.use_smart_priority}")
        print(f"  - question_metadata loaded: {len(question_metadata)} questions")
        
        # Create lookup for sector-specific action text by question_id
        sector_action_lookup = {}
        for priority in ['high', 'medium', 'low']:
            for sa in sector_actions.get(priority, []):
                q_id = sa.get('question_id', '')
                if q_id:
                    sector_action_lookup[q_id] = sa.get('sector_action', '')
        
        # Domain to risk theme mapping
        domain_risk_themes = {
            'Fairness': 'Bias & Discrimination Risk',
            'Transparency': 'Disclosure & Communication Risk',
            'Explainability': 'Decision Interpretability Risk',
            'Accountability': 'Governance & Oversight Risk',
            'Data Integrity': 'Data Quality & Lineage Risk',
            'Reliability': 'System Performance Risk',
            'Security': 'Cybersecurity & Access Risk',
            'Privacy': 'Data Protection & Privacy Risk',
            'Safety': 'Harm Prevention Risk',
            'Inclusivity': 'Accessibility & Equity Risk',
            'Sustainability': 'Environmental & Long-term Risk'
        }
        
        # Timeframe defaults based on quadrant (for smart priority) or score-based priority
        quadrant_timeframes = {
            'Quick win': '0-30 days',
            'Strategic project': '3-6 months',
            'Opportunistic improvement': '1-3 months',
            'Lower priority': '6-12 months'
        }
        
        score_priority_defaults = {
            'high': {'timeframe': '0-90 days', 'effort_label': 'High'},
            'medium': {'timeframe': '3-6 months', 'effort_label': 'Medium'},
            'low': {'timeframe': '6-12 months', 'effort_label': 'Low'}
        }
        
        def enrich_action(action: Dict[str, Any], score_priority: str) -> Dict[str, Any]:
            """Enrich an action item with smart priority data and all fields."""
            question_id = action.get('question_id', '')
            domain = action.get('domain', 'Unknown')
            
            # Get metadata for this question
            metadata = question_metadata.get(question_id, {})
            impact_weight = metadata.get('impact_weight', 0.5)
            effort_score = metadata.get('effort_score', 0.5)
            
            # Calculate gap from score (score 1 = gap 3, score 2 = gap 2, score 3 = gap 1)
            score_map = {'high': 1, 'medium': 2, 'low': 3}
            maturity_score = score_map.get(score_priority, 2)
            gap = 4 - maturity_score
            
            # Calculate smart priority
            smart_priority_score = self._calculate_smart_priority(impact_weight, gap, effort_score)
            quadrant_label = self._get_quadrant_label(impact_weight, effort_score)
            
            # Get sector-specific recommendation if available
            sector_rec = sector_action_lookup.get(question_id, '')
            default_rec = action.get('text', 'No recommendation available')
            
            # Get action_steps from metadata if available
            metadata_action_steps = metadata.get('action_steps', '')
            
            enriched = {
                'domain': domain,
                'question_id': question_id,
                # Default AM AI SAFE recommendation
                'text': default_rec,
                # Sector-specific action step (empty string if not available)
                'sector_text': sector_rec,
                # Metadata action steps (from system_question_metadata.json)
                'metadata_action_steps': metadata_action_steps,
                # Combined: sector-specific if available, otherwise default
                'recommendation': sector_rec if sector_rec else default_rec,
                # Score-based priority (high/medium/low based on maturity score)
                'score_priority': score_priority.capitalize(),
                # Smart priority data
                'impact_weight': impact_weight,
                'impact_percent': round(impact_weight * 100),
                'effort_score': effort_score,
                'effort_percent': round(effort_score * 100),
                'gap': gap,
                'smart_priority_score': round(smart_priority_score, 3),
                'quadrant_label': quadrant_label,
                # Timeframe based on quadrant for smart priority
                'timeframe': quadrant_timeframes.get(quadrant_label, '3-6 months'),
                'timeframe_score_based': score_priority_defaults.get(score_priority, {}).get('timeframe', 'TBD'),
                # Effort label (from quadrant or score-based)
                'effort': 'High' if effort_score > 0.6 else 'Medium' if effort_score > 0.3 else 'Low',
                'effort_score_based': score_priority_defaults.get(score_priority, {}).get('effort_label', 'Unknown'),
                'risk_theme': domain_risk_themes.get(domain, 'General Risk'),
                # Additional metadata
                'regulatory_driver': metadata.get('regulatory_driver', ''),
                'risk_category': metadata.get('risk_category', ''),
                'lifecycle_phase': metadata.get('lifecycle_phase', ''),
                'effort_category': metadata.get('effort_category', '')
            }
            return enriched
        
        # Enrich all actions from score-based tiers
        all_enriched_actions = []
        for priority in ['high', 'medium', 'low']:
            for action in actions.get(priority, []):
                enriched = enrich_action(action, priority)
                all_enriched_actions.append(enriched)
        
        # Create SCORE-BASED ordering (current behavior)
        high_actions_score = [a for a in all_enriched_actions if a['score_priority'] == 'High']
        medium_actions_score = [a for a in all_enriched_actions if a['score_priority'] == 'Medium']
        low_actions_score = [a for a in all_enriched_actions if a['score_priority'] == 'Low']
        
        # Create SMART PRIORITY ordering (sorted by smart_priority_score descending)
        all_sorted_by_smart = sorted(all_enriched_actions, key=lambda x: x['smart_priority_score'], reverse=True)
        
        # Also categorize by quadrant for smart priority
        quick_wins = [a for a in all_sorted_by_smart if a['quadrant_label'] == 'Quick win']
        strategic_projects = [a for a in all_sorted_by_smart if a['quadrant_label'] == 'Strategic project']
        opportunistic = [a for a in all_sorted_by_smart if a['quadrant_label'] == 'Opportunistic improvement']
        lower_priority = [a for a in all_sorted_by_smart if a['quadrant_label'] == 'Lower priority']
        
        # Extract unique risk themes
        risk_themes = list(set([a.get('risk_theme', 'General Risk') for a in all_enriched_actions]))[:5]
        
        # Debug output
        print(f"  - Total enriched actions: {len(all_enriched_actions)}")
        print(f"  - Quick wins: {len(quick_wins)}, Strategic: {len(strategic_projects)}, Opportunistic: {len(opportunistic)}, Lower: {len(lower_priority)}")
        if all_sorted_by_smart:
            top = all_sorted_by_smart[0]
            print(f"  - Top smart priority: {top['question_id']} (score: {top['smart_priority_score']}, quadrant: {top['quadrant_label']})")
        
        # Determine which ordering to use as primary based on use_smart_priority flag
        if self.use_smart_priority:
            primary_high = quick_wins + strategic_projects  # High impact items
            primary_medium = opportunistic
            primary_low = lower_priority
        else:
            primary_high = high_actions_score
            primary_medium = medium_actions_score
            primary_low = low_actions_score
        
        return {
            # PRIMARY ordering (based on use_smart_priority flag)
            'high': primary_high,
            'medium': primary_medium,
            'low': primary_low,
            
            # SCORE-BASED ordering (always available)
            'by_score': {
                'high': high_actions_score,
                'medium': medium_actions_score,
                'low': low_actions_score
            },
            
            # SMART PRIORITY ordering (always available)
            'by_smart_priority': {
                'all': all_sorted_by_smart,
                'quick_wins': quick_wins,
                'strategic_projects': strategic_projects,
                'opportunistic': opportunistic,
                'lower_priority': lower_priority
            },
            
            # Summary statistics
            'summary': {
                'high_count': len(primary_high),
                'medium_count': len(primary_medium),
                'low_count': len(primary_low),
                'total_count': len(all_enriched_actions),
                'quick_wins_count': len(quick_wins),
                'strategic_projects_count': len(strategic_projects),
                'opportunistic_count': len(opportunistic),
                'lower_priority_count': len(lower_priority),
                'top_risk_themes': risk_themes if risk_themes else ['No specific risk themes identified'],
                'ordering_method': 'smart_priority' if self.use_smart_priority else 'score_based'
            }
        }
    
    def _calculate_evidence_stats(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate evidence statistics for test template."""
        # This would ideally pull from actual evidence records
        # For now, return placeholder values
        actions = report_data.get('actions', {})
        high_actions = actions.get('high', [])
        
        return {
            'count_total': 0,
            'count_linked_to_high_priority': 0,
            'coverage_percent': 0.0,
            'gaps_count': len(high_actions),
            'top_gaps': [
                {
                    'domain': a.get('domain', 'Unknown'),
                    'question_id': a.get('question_id', 'N/A'),
                    'reason': 'High priority action without linked evidence'
                }
                for a in high_actions[:5]
            ]
        }


    def _generate_docx_report(self, report_data: Dict[str, Any], heatmap_image: bytes) -> bytes:
        """Generate DOCX report using template and data while preserving all styles."""
        try:
            # Debug: print report_data keys
            print(f"DEBUG _generate_docx_report: report_data keys = {list(report_data.keys())}")
            if 'awareness_info' in report_data:
                print(f"DEBUG: awareness_info keys = {list(report_data.get('awareness_info', {}).keys())}")
            
            # Load the template
            doc = DocxTemplate(self.template_path)
            
            # Create inline image for heatmap - set to requested width
            heatmap_inline = InlineImage(doc, io.BytesIO(heatmap_image), width=Inches(6.27))
            
            # Generate awareness bar image (stacked bar chart) for Awareness assessments
            if self.assessment_type == 'Awareness':
                awareness_bar_bytes = self._generate_awareness_bar_image(report_data)
                awareness_bar_inline = InlineImage(doc, io.BytesIO(awareness_bar_bytes), width=Inches(2.0))
            else:
                awareness_bar_inline = heatmap_inline  # Fallback for non-Awareness
            
            # Generate radar chart image
            radar_chart_image = self._generate_radar_chart_image(report_data)
            radar_chart_inline = InlineImage(doc, io.BytesIO(radar_chart_image), width=Inches(3.5))
            
            # Get top 3 strengths and gaps
            top_3_strengths = self._format_top_3_strengths(report_data)
            top_3_gaps = self._format_top_3_gaps(report_data)
            
            # For Awareness assessments, get info from awareness_info
            awareness_info = report_data.get('awareness_info') or {}
            
            # Prepare template context matching the exact template structure and placeholders
            template_context = {
                # Organization information - populated from awareness_info for Awareness assessments
                'org': {
                    'name': awareness_info.get('org_name') or report_data.get('org', {}).get('name', 'Organization'),
                    'industry': awareness_info.get('industry', ''),
                    'size': awareness_info.get('org_size', ''),
                    'business_unit': awareness_info.get('business_unit', ''),
                },
                
                # Assessment information (date will be formatted by formatDate function)
                'assessment': {
                    'id': report_data.get('assessment', {}).get('id', 'N/A'),
                    'date': report_data.get('assessment', {}).get('date', '2025-01-01'),
                    'version': report_data.get('assessment', {}).get('version', '1.0.0'),
                    'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S'),
                    'type': 'AI System Maturity Assessment'
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
                
                # Awareness bar image (stacked bar chart for Awareness template)
                'awareness_bar_image': awareness_bar_inline,
                
                # Radar chart image for direct placeholder replacement
                'radar_chart_image': radar_chart_inline,
                
                # Top 3 strengths and gaps
                'top_3_strengths': top_3_strengths,
                'top_3_gaps': top_3_gaps,
                
                # Actions for working template with separate priority arrays and summary
                'actions': self._build_actions_with_summary(report_data),
                
                # Sector-specific action steps
                'sector_name': report_data.get('sector_name', ''),
                'sector_actions': report_data.get('sector_actions', {'high': [], 'medium': [], 'low': []}),
                
                # System info from pre-assessment onboarding with normalized field names for test template
                'system_info': self._normalize_system_info(report_data.get('system_info', {})),
                
                # Add comprehensive content sections
                # Note: AI-enhanced versions are populated separately if use_ai=True
                'executive_summary': report_data.get('ai_executive_summary') or self._generate_comprehensive_executive_summary(report_data),
                'assessment_methodology': self._generate_assessment_methodology(),
                'domain_analysis': self._generate_domain_analysis(report_data),
                'key_findings': report_data.get('ai_key_findings') or self._generate_key_findings(report_data),
                'implementation_roadmap': self._generate_implementation_roadmap(report_data),
                
                # AI-generated content in structure expected by test template schema
                'ai_generated': {
                    'executive_summary': report_data.get('ai_executive_summary') or self._generate_comprehensive_executive_summary(report_data),
                    'key_findings': report_data.get('ai_key_findings') or self._generate_key_findings(report_data)
                },
                
                # Maturity distribution for test template
                'maturity': self._calculate_maturity_distribution(report_data),
                
                # Strengths and gaps in test template format
                'strengths': {
                    'top_3': top_3_strengths
                },
                'gaps': {
                    'top_3': top_3_gaps
                },
                
                # Domain results for test template (array format)
                'domains': self._format_domains_for_template(report_data),
                
                # Evidence information for test template
                'evidence': self._calculate_evidence_stats(report_data),
                
                # Validation info for test template
                'validation': {
                    'source_hash': report_data.get('validation', {}).get('source_hash', 'N/A'),
                    'lint_passed': True,
                    'lint_messages': []
                },
                
            }
            
            # Add Awareness-specific variables if this is an Awareness assessment
            if self.assessment_type == 'Awareness':
                awareness_info = report_data.get('awareness_info') or {}
                
                # Add all awareness_info fields as top-level variables
                template_context.update({
                    # Organization and contact info
                    'org_name': awareness_info.get('org_name', ''),
                    'contact_name': awareness_info.get('contact_name', ''),
                    'contact_email': awareness_info.get('contact_email', ''),
                    
                    # Organization context
                    'industry': awareness_info.get('industry', ''),
                    'org_size': awareness_info.get('org_size', ''),
                    'business_unit': awareness_info.get('business_unit', ''),
                    
                    # AI and digital maturity indicators
                    'ai_familiarity': awareness_info.get('ai_familiarity', ''),
                    'digital_maturity': awareness_info.get('digital_maturity', ''),
                    'leadership_ai_interest': awareness_info.get('leadership_ai_interest', ''),
                    'tech_change_comfort': awareness_info.get('tech_change_comfort', ''),
                    'digital_initiatives_level': awareness_info.get('digital_initiatives_level', ''),
                    'data_skill_confidence': awareness_info.get('data_skill_confidence', ''),
                    'openness_to_learning': awareness_info.get('openness_to_learning', ''),
                    
                    # Assessment context
                    'awareness_reason': awareness_info.get('awareness_reason', ''),
                    'assessor_name': awareness_info.get('assessor_name', ''),
                    'assessment_date': awareness_info.get('assessment_date', ''),
                    'framework_version': awareness_info.get('framework_version', ''),
                    
                    # Arrays from awareness_info
                    'awareness_outcomes': awareness_info.get('awareness_outcomes', []),
                    'learning_preferences': awareness_info.get('learning_preferences', []),
                    'governance_foundations': awareness_info.get('governance_foundations', []),
                    'pre_onboarding_commentary': awareness_info.get('pre_onboarding_commentary', []),
                    
                    # Full awareness_info object for flexibility
                    'awareness_info': awareness_info,
                })
                
                # Build strengths list (domains scoring >= 70%)
                strengths = []
                for d in template_context.get('domains', []):
                    if d.get('score', 0) >= 70:
                        strengths.append(f"{d.get('name', 'Unknown')} ({d.get('score', 0):.0f}%)")
                template_context['strengths'] = strengths
                
                # Build strengths_summary as a readable string
                if strengths:
                    template_context['strengths_summary'] = ', '.join(strengths[:3])
                else:
                    template_context['strengths_summary'] = 'Building foundational awareness across all domains'
                
                # Build gaps list (domains scoring < 50%)
                gaps = []
                for d in template_context.get('domains', []):
                    if d.get('score', 0) < 50:
                        gaps.append(f"{d.get('name', 'Unknown')} ({d.get('score', 0):.0f}%)")
                template_context['gaps'] = gaps
                
                # Build gaps_summary as a readable string
                if gaps:
                    template_context['gaps_summary'] = ', '.join(gaps[:3])
                else:
                    template_context['gaps_summary'] = 'No critical gaps identified'
                
                # Build next_focus - use AI-generated version if available, otherwise fallback
                ai_narratives = report_data.get('ai_narratives', {})
                ai_next_focus = ai_narratives.get('next_focus', '')
                
                if ai_next_focus:
                    template_context['next_focus'] = ai_next_focus
                else:
                    # Fallback: Build next_focus recommendation based on tier
                    tier = template_context.get('overall', {}).get('tier', 'Developing')
                    if tier == 'Foundational':
                        template_context['next_focus'] = 'Establish basic AI awareness and governance foundations'
                    elif tier == 'Developing':
                        template_context['next_focus'] = 'Build structured awareness programs and refine governance frameworks'
                    elif tier == 'Established':
                        template_context['next_focus'] = 'Deepen AI literacy and prepare for readiness assessment'
                    else:
                        template_context['next_focus'] = 'Maintain leadership position and drive AI innovation'
                
                # Build priority_actions list with priority and text
                priority_actions = []
                for action in template_context.get('actions', {}).get('high', []):
                    priority_actions.append({
                        'priority': 'High',
                        'text': action.get('text', ''),
                        'domain': action.get('domain', ''),
                        'question_id': action.get('question_id', '')
                    })
                for action in template_context.get('actions', {}).get('medium', []):
                    priority_actions.append({
                        'priority': 'Medium',
                        'text': action.get('text', ''),
                        'domain': action.get('domain', ''),
                        'question_id': action.get('question_id', '')
                    })
                for action in template_context.get('actions', {}).get('low', []):
                    priority_actions.append({
                        'priority': 'Low',
                        'text': action.get('text', ''),
                        'domain': action.get('domain', ''),
                        'question_id': action.get('question_id', '')
                    })
                template_context['priority_actions'] = priority_actions
                
                # Build top 5 sector-specific actions for each priority level
                sector_actions = template_context.get('sector_actions', {'high': [], 'medium': [], 'low': []})
                
                # DEBUG: Print sector_actions structure
                print(f"DEBUG sector_actions structure:")
                print(f"  - sector_actions type: {type(sector_actions)}")
                print(f"  - high count: {len(sector_actions.get('high', []))}")
                print(f"  - medium count: {len(sector_actions.get('medium', []))}")
                print(f"  - low count: {len(sector_actions.get('low', []))}")
                if sector_actions.get('high'):
                    first_high = sector_actions['high'][0]
                    print(f"  - First high action keys: {list(first_high.keys())}")
                    print(f"  - First high action.domain: {first_high.get('domain')}")
                    print(f"  - First high action.question_id: {first_high.get('question_id')}")
                    print(f"  - First high action.sector_action: {first_high.get('sector_action', 'N/A')[:80]}...")
                if sector_actions.get('medium'):
                    first_med = sector_actions['medium'][0]
                    print(f"  - First MEDIUM action: question_id='{first_med.get('question_id')}', domain='{first_med.get('domain')}', sector_action='{first_med.get('sector_action', 'N/A')[:60]}...'")
                
                template_context['sector_actions_high_top5'] = sector_actions.get('high', [])[:5]
                template_context['sector_actions_medium_top5'] = sector_actions.get('medium', [])[:5]
                template_context['sector_actions_low_top5'] = sector_actions.get('low', [])[:5]
                
                # DEBUG: Confirm the top5 lists
                print(f"DEBUG sector_actions_high_top5 after assignment: {len(template_context['sector_actions_high_top5'])} items")
                print(f"DEBUG sector_actions_medium_top5 after assignment: {len(template_context['sector_actions_medium_top5'])} items")
                if template_context['sector_actions_high_top5']:
                    first = template_context['sector_actions_high_top5'][0]
                    print(f"  - First item domain: {first.get('domain')}")
                    print(f"  - First item question_id: {first.get('question_id')}")
                    print(f"  - First item sector_action: {first.get('sector_action', 'N/A')[:50]}...")
                else:
                    print(f"  sector_actions_high_top5 is EMPTY")
                if template_context['sector_actions_medium_top5']:
                    first_m = template_context['sector_actions_medium_top5'][0]
                    print(f"  MEDIUM First: question_id='{first_m.get('question_id')}', domain='{first_m.get('domain')}')")
                
                # Add AI-generated narratives if available
                ai_narratives = report_data.get('ai_narratives', {})
                template_context['ai'] = {
                    'executive_snapshot': ai_narratives.get('executive_snapshot', ''),
                    'context_interpretation': ai_narratives.get('context_interpretation', ''),
                    'governance_interpretation': ai_narratives.get('governance_interpretation', ''),
                    'readiness_interpretation': ai_narratives.get('readiness_interpretation', ''),
                    'domain_patterns': ai_narratives.get('domain_patterns', ''),
                    'action_interpretation': ai_narratives.get('action_interpretation', ''),
                }
                print(f"DEBUG: Added AI narratives to template context: {list(template_context['ai'].keys())}")
                if template_context['ai'].get('executive_snapshot'):
                    print(f"  - executive_snapshot length: {len(template_context['ai']['executive_snapshot'])} chars")
                if template_context['ai'].get('context_interpretation'):
                    print(f"  - context_interpretation length: {len(template_context['ai']['context_interpretation'])} chars")
                if template_context['ai'].get('governance_interpretation'):
                    print(f"  - governance_interpretation length: {len(template_context['ai']['governance_interpretation'])} chars")
                if template_context['ai'].get('readiness_interpretation'):
                    print(f"  - readiness_interpretation length: {len(template_context['ai']['readiness_interpretation'])} chars")
                if template_context['ai'].get('domain_patterns'):
                    print(f"  - domain_patterns length: {len(template_context['ai']['domain_patterns'])} chars")
                if template_context['ai'].get('action_interpretation'):
                    print(f"  - action_interpretation length: {len(template_context['ai']['action_interpretation'])} chars")
                
                # Build questions list with full details
                questions = []
                questions_data = report_data.get('questions_data', [])
                q_num = 1
                for domain_data in questions_data:
                    domain_name = domain_data.get('domain', {}).get('name', 'Unknown')
                    for q in domain_data.get('questions', []):
                        answer = q.get('answer', {})
                        score = answer.get('numeric_score', 0) if answer else 0
                        
                        # Determine maturity level from score
                        if score >= 4:
                            maturity_level = 'Advanced'
                        elif score >= 3:
                            maturity_level = 'Good'
                        elif score >= 2:
                            maturity_level = 'Basic'
                        else:
                            maturity_level = 'Non-Ideal'
                        
                        questions.append({
                            'number': q_num,
                            'code': q.get('code', ''),
                            'text': q.get('text', ''),
                            'domain': domain_name,
                            'selected_option_label': answer.get('selected_option', {}).get('label', 'Not answered') if answer else 'Not answered',
                            'selected_option_text': answer.get('selected_option', {}).get('text', '') if answer else '',
                            'maturity_level': maturity_level,
                            'score': score,
                            'comment': answer.get('comment', '') if answer else ''
                        })
                        q_num += 1
                template_context['questions'] = questions
                
                print(f"  Awareness-specific variables added:")
                print(f"    - org_name: {template_context.get('org_name', 'N/A')}")
                print(f"    - industry: {template_context.get('industry', 'N/A')}")
                print(f"    - strengths: {len(strengths)} items")
                print(f"    - gaps: {len(gaps)} items")
                print(f"    - priority_actions: {len(priority_actions)} items")
                print(f"    - questions: {len(questions)} items")
            print("Generated report data structure:")
            print(f"  Organization: {template_context['org']['name']}")
            print(f"  Overall score: {template_context['overall']['score']}")
            print(f"  High priority actions: {len(template_context['actions']['high'])}")
            print(f"  Medium priority actions: {len(template_context['actions']['medium'])}")
            print(f"  Low priority actions: {len(template_context['actions']['low'])}")
            print(f"  Sector: {template_context['sector_name']}")
            print(f"  Sector actions - high: {len(template_context['sector_actions']['high'])}, medium: {len(template_context['sector_actions']['medium'])}, low: {len(template_context['sector_actions']['low'])}")
            print(f"  System info keys: {list(template_context['system_info'].keys())}")
            
            # Show sample sector actions for debugging
            if template_context.get('sector_actions_high_top5'):
                sample = template_context['sector_actions_high_top5'][0]
                print(f"  Sample sector_actions_high_top5[0]: question_id={sample.get('question_id')}, domain={sample.get('domain')}, sector_action={sample.get('sector_action', 'N/A')[:50]}...")
            else:
                print(f"  sector_actions_high_top5 is EMPTY")
            
            # Show sample actions for debugging
            if template_context['actions']['high']:
                sample_high = template_context['actions']['high'][0]
                print(f"  Sample high action: {sample_high.get('domain', 'N/A')} | {sample_high.get('question_id', 'N/A')}")
            
            # Helper function for date formatting in template
            template_context['formatDate'] = self.format_date
            
            # Render the template - this will preserve all original fonts, colors, margins, layout
            doc.render(template_context)
            
            # Center-align images (heatmap and radar chart)
            self._center_align_images(doc)
            
            # Populate recommendation tables programmatically
            # Different handling for Awareness vs other assessment types
            if self.assessment_type == 'Awareness':
                # Awareness uses sector_actions tables with question_id, domain, sector_action
                self._populate_awareness_sector_tables(doc, report_data)
            elif not self.use_test_template:
                # System/other templates use actions tables with domain, question_id, text
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
    
    async def generate_report_for_assessment(self, assessment_id: str, db, current_user, view_type: str = "heatmap", use_ai: bool = False) -> Tuple[bytes, str]:
        """
        Generate report for a specific assessment ID.
        
        Args:
            assessment_id: Assessment ID to generate report for
            db: Database connection
            current_user: Current user object
            view_type: Type of visualization ('heatmap' or 'radar')
            
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
        
        # Determine if this is an Awareness assessment
        is_awareness = self.assessment_type == 'Awareness'
        
        if is_awareness:
            # For Awareness assessments, use AWARENESS_QUESTIONS_DATA
            from awareness_questions import AWARENESS_QUESTIONS_DATA
            
            # Create mapping from question code to question details
            awareness_questions_by_code = {}
            for question_data in AWARENESS_QUESTIONS_DATA:
                code = question_data.get('code')
                if code:
                    awareness_questions_by_code[code] = question_data
            
            # Awareness domain mapping
            awareness_domain_mapping = {
                "AU": "Awareness & Understanding",
                "GT": "Governance & Trust Foundations",
                "PS": "People & Skills",
                "LV": "Leadership Vision",
                "DR": "Digital Readiness"
            }
            
            for answer in answers:
                # For Awareness, question_id IS the code (e.g., "AU-01")
                question_code = answer.get("question_id", "")
                
                if question_code and question_code in awareness_questions_by_code:
                    processed_answers += 1
                    question_details = awareness_questions_by_code[question_code]
                    
                    # Extract domain from question code
                    domain_prefix = question_code.split("-")[0] if "-" in question_code else ""
                    domain_name = awareness_domain_mapping.get(domain_prefix, "Unknown")
                    
                    # Use domain name as ID for Awareness (no domain collection)
                    domain_id = domain_name
                    
                    if domain_id not in questions_by_domain:
                        questions_by_domain[domain_id] = []
                    
                    question = {
                        "id": question_code,
                        "code": question_code,
                        "text": question_details.get('text', f'Question {question_code}'),
                        "domain_id": domain_id,
                        "order": question_details.get('order', 0),
                        "answer": {
                            "numeric_score": answer.get("numeric_score", 0),
                            "text": answer.get("option", ""),
                            "question_id": question_code,
                            "selected_option": {
                                "label": answer.get("option", ""),
                                "text": answer.get("option", "")
                            },
                            "comment": answer.get("note", "")
                        }
                    }
                    questions_by_domain[domain_id].append(question)
            
            # Create domain info for Awareness
            domains_by_id = {
                "Awareness & Understanding": {"id": "Awareness & Understanding", "name": "Awareness & Understanding"},
                "Governance & Trust Foundations": {"id": "Governance & Trust Foundations", "name": "Governance & Trust Foundations"},
                "People & Skills": {"id": "People & Skills", "name": "People & Skills"},
                "Leadership Vision": {"id": "Leadership Vision", "name": "Leadership Vision"},
                "Digital Readiness": {"id": "Digital Readiness", "name": "Digital Readiness"}
            }
        else:
            # Original logic for System/other assessments
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
        # Calculate summary data
        total_score = 0
        total_possible = 0
        domain_scores = []
        
        for domain_id, questions in questions_by_domain.items():
            domain = domains_by_id.get(domain_id, {"name": "Unknown"})
            domain_total = sum(q["answer"]["numeric_score"] for q in questions)
            domain_possible = len(questions) * 4  # 1-4 scale
            domain_percentage = (domain_total / domain_possible * 100) if domain_possible > 0 else 0
            
            domain_scores.append({
                "domain_id": domain_id,
                "domain_name": domain.get("name", "Unknown"),
                "percentage": domain_percentage
            })
            
            total_score += domain_total
            total_possible += domain_possible
        
        # For Awareness assessments, prefer stored overall_percentage
        if is_awareness and assessment.get('overall_percentage'):
            overall_percentage = assessment.get('overall_percentage')
            print(f"DEBUG: Using stored overall_percentage for Awareness: {overall_percentage}")
        else:
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
        
        # Get sector/industry from assessment - differs by assessment type
        system_info = assessment.get('system_info') or {}
        awareness_info = assessment.get('awareness_info') or {}
        
        # For Awareness assessments, get industry from awareness_info
        if self.assessment_type == 'Awareness':
            sector_name = awareness_info.get('industry', '')
        else:
            sector_name = system_info.get('industry', '') if system_info else ''
        
        print(f"DEBUG: Assessment type: {self.assessment_type}")
        print(f"DEBUG: Assessment sector/industry: {sector_name}")
        
        # Generate sector-specific actions (for System and Awareness assessments with sector info)
        sector_actions = {'high': [], 'medium': [], 'low': []}
        if sector_name and self.assessment_type in ['System', 'Awareness']:
            sector_actions = self._generate_sector_actions(
                {"questions_data": questions_data},
                sector_name
            )
        
        # DEBUG: Print what sector_actions contains BEFORE passing to assessment_data
        print(f"DEBUG generate_report_for_assessment: sector_actions generated")
        print(f"  - high: {len(sector_actions.get('high', []))} items")
        print(f"  - medium: {len(sector_actions.get('medium', []))} items")
        print(f"  - low: {len(sector_actions.get('low', []))} items")
        if sector_actions.get('high'):
            first = sector_actions['high'][0]
            print(f"  - FIRST HIGH: question_id='{first.get('question_id')}', domain='{first.get('domain')}', sector_action='{first.get('sector_action', 'N/A')[:60]}...'")
        
        # Prepare assessment data for report generation
        assessment_data = {
            "assessment": assessment,
            "questions_data": questions_data,
            "summary": summary_data,
            "sector_name": sector_name,
            "sector_actions": sector_actions,
            "system_info": system_info,  # Pass system_info for template use (may be empty for non-System assessments)
            "awareness_info": assessment.get('awareness_info') or {},  # Pass awareness_info for Awareness assessments
        }
        
        # Generate AI narratives for Awareness assessments if use_ai is enabled
        if use_ai and self.assessment_type == 'Awareness':
            print("=== GENERATING AWARENESS AI NARRATIVES ===")
            try:
                # Build report_data for AI narrative generation
                awareness_info = assessment.get('awareness_info') or {}
                ai_report_data = {
                    'organization_name': awareness_info.get('org_name', current_user.organization_name),
                    'overall': {
                        'tier': summary_data.get('overall_tier', 'Unknown'),
                        'percentage': summary_data.get('overall_percentage', 0),
                        'score': summary_data.get('overall_percentage', 0),
                    },
                    'strengths': summary_data.get('top_strengths', []),
                    'gaps': summary_data.get('top_gaps', []),
                    'sector_name': awareness_info.get('industry', 'Unknown'),
                    'industry': awareness_info.get('industry', 'Unknown'),
                    'awareness_info': awareness_info,  # Pass full awareness_info for AI-2
                }
                
                ai_narratives = await self._generate_awareness_ai_narratives(ai_report_data, assessment, db)
                assessment_data['ai_narratives'] = ai_narratives
                print(f"DEBUG: AI narratives generated: {list(ai_narratives.keys())}")
            except Exception as e:
                print(f"ERROR generating Awareness AI narratives: {e}")
                assessment_data['ai_narratives'] = {}
        
        print(f"DEBUG: current_user type: {type(current_user)}")
        print(f"DEBUG: current_user.organization_name: {getattr(current_user, 'organization_name', 'NOT SET')}")
        
        user_data = {
            "organization_name": current_user.organization_name
        }
        
        print(f"DEBUG: user_data: {user_data}")
        
        # Fetch benchmark data if radar view is selected
        benchmark_data = None
        if view_type == "radar":
            # Get user's industry for benchmarking
            user_industry = getattr(current_user, 'industry', None) or getattr(current_user, 'primary_industry', None)
            if user_industry:
                print(f"DEBUG: Fetching benchmarks for industry: {user_industry}")
                # Fetch benchmark data from sector_benchmarks collection
                benchmark_record = await db.sector_benchmarks.find_one({"sector": user_industry})
                if benchmark_record:
                    benchmark_data = {
                        "sector": user_industry,
                        "benchmarks": benchmark_record.get("benchmarks", {})
                    }
                    print(f"DEBUG: Benchmark data found for {user_industry}")
                else:
                    print(f"DEBUG: No benchmark data found for {user_industry}")
            else:
                print(f"DEBUG: User has no industry set, cannot fetch benchmarks")
        
        # Generate the report
        docx_bytes, pdf_bytes = await self.generate_report(
            assessment_id, assessment_data, user_data, 
            view_type=view_type, benchmark_data=benchmark_data,
            use_ai=use_ai
        )
        
        # Generate filename - use assessment's org_name from the appropriate info object
        # The org_name is stored in different locations depending on assessment type
        assessment_org_name = ''
        if self.assessment_type == 'Awareness':
            assessment_org_name = (assessment.get('awareness_info') or {}).get('org_name', '')
        elif self.assessment_type == 'Readiness':
            assessment_org_name = (assessment.get('readiness_info') or {}).get('org_name', '')
        elif self.assessment_type == 'Orgwide':
            assessment_org_name = (assessment.get('orgwide_info') or {}).get('org_name', '')
        else:
            # System or other types - check org_info first, then system_info
            assessment_org_name = (assessment.get('org_info') or {}).get('org_name', '')
            if not assessment_org_name:
                assessment_org_name = (assessment.get('system_info') or {}).get('org_name', '')
        
        # Fallback to organization_name field if exists, then to user's organization name
        if not assessment_org_name:
            assessment_org_name = assessment.get('organization_name', '')
        if not assessment_org_name:
            assessment_org_name = current_user.organization_name
        
        safe_org_name = "".join(c for c in assessment_org_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
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
        
        # Determine if this is an Awareness assessment
        is_awareness = self.assessment_type == 'Awareness'
        
        if is_awareness:
            # For Awareness assessments, use AWARENESS_QUESTIONS_DATA
            from awareness_questions import AWARENESS_QUESTIONS_DATA
            
            # Create mapping from question code to question details
            awareness_questions_by_code = {}
            for question_data in AWARENESS_QUESTIONS_DATA:
                code = question_data.get('code')
                if code:
                    awareness_questions_by_code[code] = question_data
            
            # Awareness domain mapping
            awareness_domain_mapping = {
                "AU": "Awareness & Understanding",
                "GT": "Governance & Trust Foundations",
                "PS": "People & Skills",
                "LV": "Leadership Vision",
                "DR": "Digital Readiness"
            }
            
            for answer in answers:
                # For Awareness, question_id IS the code (e.g., "AU-01")
                question_code = answer.get("question_id", "")
                
                if question_code and question_code in awareness_questions_by_code:
                    processed_answers += 1
                    question_details = awareness_questions_by_code[question_code]
                    
                    # Extract domain from question code
                    domain_prefix = question_code.split("-")[0] if "-" in question_code else ""
                    domain_name = awareness_domain_mapping.get(domain_prefix, "Unknown")
                    
                    # Use domain name as ID for Awareness (no domain collection)
                    domain_id = domain_name
                    
                    if domain_id not in questions_by_domain:
                        questions_by_domain[domain_id] = []
                    
                    question = {
                        "id": question_code,
                        "code": question_code,
                        "text": question_details.get('text', f'Question {question_code}'),
                        "domain_id": domain_id,
                        "order": question_details.get('order', 0),
                        "answer": {
                            "numeric_score": answer.get("numeric_score", 0),
                            "text": answer.get("option", ""),
                            "question_id": question_code,
                            "selected_option": {
                                "label": answer.get("option", ""),
                                "text": answer.get("option", "")
                            },
                            "comment": answer.get("note", "")
                        }
                    }
                    questions_by_domain[domain_id].append(question)
            
            # Create domain info for Awareness
            domains_by_id = {
                "Awareness & Understanding": {"id": "Awareness & Understanding", "name": "Awareness & Understanding"},
                "Governance & Trust Foundations": {"id": "Governance & Trust Foundations", "name": "Governance & Trust Foundations"},
                "People & Skills": {"id": "People & Skills", "name": "People & Skills"},
                "Leadership Vision": {"id": "Leadership Vision", "name": "Leadership Vision"},
                "Digital Readiness": {"id": "Digital Readiness", "name": "Digital Readiness"}
            }
        else:
            # Original logic for System/other assessments
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
        # Calculate summary data
        total_score = 0
        total_possible = 0
        domain_scores = []
        
        for domain_id, questions in questions_by_domain.items():
            domain = domains_by_id.get(domain_id, {"name": "Unknown"})
            domain_total = sum(q["answer"]["numeric_score"] for q in questions)
            domain_possible = len(questions) * 4  # 1-4 scale
            domain_percentage = (domain_total / domain_possible * 100) if domain_possible > 0 else 0
            
            domain_scores.append({
                "domain_id": domain_id,
                "domain_name": domain.get("name", "Unknown"),
                "percentage": domain_percentage
            })
            
            total_score += domain_total
            total_possible += domain_possible
        
        # For Awareness assessments, prefer stored overall_percentage
        if is_awareness and assessment.get('overall_percentage'):
            overall_percentage = assessment.get('overall_percentage')
            print(f"DEBUG: Using stored overall_percentage for Awareness: {overall_percentage}")
        else:
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
        
        # Get sector/industry from assessment - differs by assessment type
        system_info = assessment.get('system_info') or {}
        awareness_info = assessment.get('awareness_info') or {}
        
        # For Awareness assessments, get industry from awareness_info
        if self.assessment_type == 'Awareness':
            sector_name = awareness_info.get('industry', '')
        else:
            sector_name = system_info.get('industry', '') if system_info else ''
        
        print(f"DEBUG: Assessment type: {self.assessment_type}")
        print(f"DEBUG: Assessment sector/industry: {sector_name}")
        
        # Generate sector-specific actions (for System and Awareness assessments with sector info)
        sector_actions = {'high': [], 'medium': [], 'low': []}
        if sector_name and self.assessment_type in ['System', 'Awareness']:
            sector_actions = self._generate_sector_actions(
                {"questions_data": questions_data},
                sector_name
            )
        
        # DEBUG: Print what sector_actions contains BEFORE passing to assessment_data
        print(f"DEBUG generate_report_for_assessment: sector_actions generated")
        print(f"  - high: {len(sector_actions.get('high', []))} items")
        print(f"  - medium: {len(sector_actions.get('medium', []))} items")
        print(f"  - low: {len(sector_actions.get('low', []))} items")
        if sector_actions.get('high'):
            first = sector_actions['high'][0]
            print(f"  - FIRST HIGH: question_id='{first.get('question_id')}', domain='{first.get('domain')}', sector_action='{first.get('sector_action', 'N/A')[:60]}...'")
        
        # Prepare assessment data for report generation
        assessment_data = {
            "assessment": assessment,
            "questions_data": questions_data,
            "summary": summary_data,
            "sector_name": sector_name,
            "sector_actions": sector_actions,
            "system_info": system_info,  # Pass system_info for template use (may be empty for non-System assessments)
            "awareness_info": assessment.get('awareness_info') or {},  # Pass awareness_info for Awareness assessments
        }
        
        print(f"DEBUG: current_user type: {type(current_user)}")
        print(f"DEBUG: current_user.organization_name: {getattr(current_user, 'organization_name', 'NOT SET')}")
        
        user_data = {
            "organization_name": current_user.organization_name
        }
        
        print(f"DEBUG: user_data: {user_data}")
        
        # Generate both DOCX and PDF
        return await self.generate_report(assessment_id, assessment_data, user_data)