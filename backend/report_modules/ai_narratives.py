"""
AI Narrative Generation Module for Reports.

This module handles all AI-generated narrative content for assessment reports
using OpenAI GPT-4o-mini via the Emergent LLM integration.

Organization:
- Core LLM helper function
- Awareness assessment narratives
- Readiness assessment narratives
- Org-wide assessment narratives
- System assessment narratives
"""

import os
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timezone


async def call_llm(prompt: str, api_key: Optional[str] = None) -> str:
    """
    Call the LLM with a prompt and return the response.
    
    Args:
        prompt: The prompt to send to the LLM
        api_key: Optional API key (uses environment variable if not provided)
        
    Returns:
        The LLM response text
    """
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    
    if not api_key:
        api_key = os.environ.get('EMERGENT_LLM_KEY', '')
    
    if not api_key:
        raise ValueError("No API key provided for LLM call")
    
    response = await (
        LlmChat(api_key)
        .add_message(UserMessage(prompt))
        .with_model("openai", "gpt-4o-mini")
        .chat_async()
    )
    
    return response.content.strip() if response and response.content else ""


def extract_domain_data(report_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and process domain score data from report_data."""
    heatmap_data = report_data.get('heatmap_data', {})
    domains = heatmap_data.get('domains', [])
    
    domain_scores = []
    all_scores = []
    
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
            all_scores.extend(scores)
    
    sorted_domains = sorted(domain_scores, key=lambda x: x['percentage'], reverse=True)
    
    return {
        'domain_scores': domain_scores,
        'sorted_domains': sorted_domains,
        'top_3': sorted_domains[:3] if len(sorted_domains) >= 3 else sorted_domains,
        'bottom_3': sorted_domains[-3:] if len(sorted_domains) >= 3 else sorted_domains,
        'all_scores': all_scores,
        'maturity_distribution': {
            'foundational': len([s for s in all_scores if s == 1]),
            'developing': len([s for s in all_scores if s == 2]),
            'established': len([s for s in all_scores if s == 3]),
            'leading': len([s for s in all_scores if s == 4])
        }
    }


def format_domain_summary(sorted_domains: List[Dict], top_n: int = 3) -> str:
    """Format top/bottom domains for prompt inclusion."""
    lines = []
    for d in sorted_domains[:top_n]:
        lines.append(f"- {d['name']}: {d['percentage']:.0f}% ({d['low_scoring_count']} low-scoring questions)")
    return "\n".join(lines)


# =============================================================================
# AWARENESS ASSESSMENT NARRATIVES
# =============================================================================

async def generate_awareness_executive_snapshot(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate executive snapshot narrative for Awareness assessments."""
    overall_score = report_data.get('overall', {}).get('score', 0)
    overall_tier = report_data.get('overall', {}).get('tier', 'Unknown')
    org_name = report_data.get('org', {}).get('name', 'the organization')
    awareness_info = report_data.get('awareness_info', {})
    industry = awareness_info.get('industry', 'Unknown')
    org_size = awareness_info.get('org_size', 'Unknown')
    
    domain_data = extract_domain_data(report_data)
    top_3 = domain_data['top_3']
    bottom_3 = domain_data['bottom_3']
    dist = domain_data['maturity_distribution']
    
    prompt = f"""You are an AI maturity assessment expert. Write a concise executive snapshot (2-3 paragraphs, max 200 words) for an AI Awareness assessment.

Context:
- Organization: {org_name}
- Industry: {industry}
- Organization Size: {org_size}
- Overall Score: {overall_score:.0f}%
- Maturity Tier: {overall_tier}

Top performing domains:
{format_domain_summary(top_3)}

Areas needing attention:
{format_domain_summary(bottom_3)}

Maturity Distribution: {dist['leading']} Leading, {dist['established']} Established, {dist['developing']} Developing, {dist['foundational']} Foundational

Write a professional narrative that:
1. Summarizes the current AI awareness maturity state
2. Highlights key strengths and opportunities
3. Provides actionable context for leadership

Use British English spelling. Be specific and avoid generic statements."""

    return await call_llm(prompt, api_key)


async def generate_awareness_context_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate context interpretation for Awareness assessments."""
    org_name = report_data.get('org', {}).get('name', 'the organization')
    awareness_info = report_data.get('awareness_info', {})
    industry = awareness_info.get('industry', 'Unknown')
    org_size = awareness_info.get('org_size', 'Unknown')
    leadership_ai_interest = awareness_info.get('leadership_ai_interest', 'Unknown')
    
    domain_data = extract_domain_data(report_data)
    
    prompt = f"""You are an AI maturity assessment expert. Write a context interpretation (2 paragraphs, ~150 words) analyzing the organizational context.

Context:
- Organization: {org_name}
- Industry: {industry}
- Organization Size: {org_size}
- Leadership interest in AI: {leadership_ai_interest}

Domain Performance:
{format_domain_summary(domain_data['sorted_domains'], 5)}

Write a professional analysis that:
1. Interprets how the organizational context affects AI awareness
2. Identifies sector-specific considerations
3. Explains leadership readiness implications

Use British English spelling. Be specific to this organization's situation."""

    return await call_llm(prompt, api_key)


async def generate_awareness_governance_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate governance interpretation for Awareness assessments."""
    org_name = report_data.get('org', {}).get('name', 'the organization')
    awareness_info = report_data.get('awareness_info', {})
    
    domain_data = extract_domain_data(report_data)
    governance_domains = [d for d in domain_data['domain_scores'] 
                         if 'governance' in d['name'].lower() or 'trust' in d['name'].lower()]
    
    prompt = f"""You are an AI governance expert. Write a governance interpretation (2 paragraphs, ~150 words).

Organization: {org_name}

Governance-related domain scores:
{format_domain_summary(governance_domains) if governance_domains else 'No specific governance domains identified'}

All domain scores:
{format_domain_summary(domain_data['sorted_domains'], 5)}

Write a professional analysis that:
1. Assesses current governance awareness and structures
2. Identifies governance gaps and risks
3. Recommends governance maturity improvements

Use British English spelling. Be actionable and specific."""

    return await call_llm(prompt, api_key)


async def generate_awareness_readiness_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate readiness interpretation for Awareness assessments."""
    overall_score = report_data.get('overall', {}).get('score', 0)
    org_name = report_data.get('org', {}).get('name', 'the organization')
    
    domain_data = extract_domain_data(report_data)
    
    prompt = f"""You are an AI readiness expert. Write a readiness interpretation (2 paragraphs, ~150 words).

Organization: {org_name}
Overall Awareness Score: {overall_score:.0f}%

Domain Performance:
{format_domain_summary(domain_data['sorted_domains'], 5)}

Maturity Distribution: {domain_data['maturity_distribution']}

Write a professional analysis that:
1. Interprets the organization's readiness for AI adoption
2. Identifies readiness gaps and prerequisites
3. Recommends preparation steps

Use British English spelling. Be practical and actionable."""

    return await call_llm(prompt, api_key)


async def generate_awareness_domain_patterns(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate domain patterns analysis for Awareness assessments."""
    domain_data = extract_domain_data(report_data)
    
    prompt = f"""You are an AI maturity analyst. Write a domain patterns analysis (2-3 paragraphs, ~200 words).

Domain Scores (sorted by performance):
{format_domain_summary(domain_data['sorted_domains'], len(domain_data['sorted_domains']))}

Maturity Distribution: {domain_data['maturity_distribution']}

Write a professional analysis that:
1. Identifies patterns across domains
2. Highlights interdependencies between domains
3. Suggests strategic focus areas based on patterns

Use British English spelling. Be analytical and insightful."""

    return await call_llm(prompt, api_key)


async def generate_awareness_action_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate action interpretation for Awareness assessments."""
    actions = report_data.get('actions', {})
    high_count = len(actions.get('high', []))
    medium_count = len(actions.get('medium', []))
    low_count = len(actions.get('low', []))
    
    domain_data = extract_domain_data(report_data)
    
    prompt = f"""You are an AI implementation strategist. Write an action interpretation (2 paragraphs, ~150 words).

Priority Actions:
- High Priority: {high_count} actions
- Medium Priority: {medium_count} actions
- Low Priority: {low_count} actions

Lowest Performing Domains:
{format_domain_summary(domain_data['bottom_3'])}

Write a professional analysis that:
1. Interprets the action priorities in context
2. Suggests sequencing and dependencies
3. Provides implementation guidance

Use British English spelling. Be practical and actionable."""

    return await call_llm(prompt, api_key)


async def generate_awareness_next_focus(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate next focus recommendation for Awareness assessments."""
    overall_tier = report_data.get('overall', {}).get('tier', 'Unknown')
    domain_data = extract_domain_data(report_data)
    
    prompt = f"""You are an AI strategy advisor. Write a next focus recommendation (1-2 paragraphs, ~100 words).

Current Maturity Tier: {overall_tier}

Top Focus Areas (lowest performing):
{format_domain_summary(domain_data['bottom_3'])}

Write a concise recommendation that:
1. Identifies the single most impactful next step
2. Explains why this should be prioritized
3. Sets clear expectations for outcomes

Use British English spelling. Be decisive and clear."""

    return await call_llm(prompt, api_key)


# =============================================================================
# AWARENESS NARRATIVE ORCHESTRATOR
# =============================================================================

async def generate_awareness_narratives(
    report_data: Dict[str, Any],
    assessment: Dict[str, Any],
    db,
    api_key: str
) -> Dict[str, str]:
    """
    Generate all AI narratives for Awareness assessments.
    Returns a dict with narrative keys that can be accessed as ai.executive_snapshot, etc.
    Caches results in the database to avoid regeneration.
    """
    narratives = {}
    assessment_id = assessment.get('id')
    
    # Check for cached narratives in database
    cached_narratives = assessment.get('ai_narratives', {})
    
    # Define narrative generators
    narrative_generators = [
        ('executive_snapshot', generate_awareness_executive_snapshot),
        ('context_interpretation', generate_awareness_context_interpretation),
        ('governance_interpretation', generate_awareness_governance_interpretation),
        ('readiness_interpretation', generate_awareness_readiness_interpretation),
        ('domain_patterns', generate_awareness_domain_patterns),
        ('action_interpretation', generate_awareness_action_interpretation),
        ('next_focus', generate_awareness_next_focus),
    ]
    
    for key, generator in narrative_generators:
        if cached_narratives.get(key):
            narratives[key] = cached_narratives[key]
            print(f"DEBUG: Using cached AI {key} narrative")
        else:
            try:
                narratives[key] = await generator(report_data, api_key)
                print(f"DEBUG: Generated new AI {key} narrative ({len(narratives[key])} chars)")
            except Exception as e:
                print(f"ERROR generating AI {key}: {e}")
                narratives[key] = ""
    
    # Cache narratives in database
    if db and assessment_id and narratives:
        try:
            await db.assessments.update_one(
                {'id': assessment_id},
                {'$set': {'ai_narratives': narratives}}
            )
            print(f"DEBUG: Cached AI narratives for assessment {assessment_id}")
        except Exception as e:
            print(f"WARNING: Failed to cache AI narratives: {e}")
    
    return narratives
