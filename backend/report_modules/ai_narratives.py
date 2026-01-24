"""
AI Narrative Generation Module for Reports.

This module handles all AI-generated narrative content for assessment reports
using OpenAI GPT-4o-mini via the Emergent LLM integration.

Supports all four assessment types:
- Awareness
- Readiness
- Orgwide (Organisation-wide)
- System

Each type has specific narrative generators with tailored prompts.
"""

import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone


# =============================================================================
# CORE UTILITIES
# =============================================================================

async def call_llm(prompt: str, system_message: str = "", session_id: str = "", api_key: Optional[str] = None) -> str:
    """
    Call the LLM with a prompt and return the response.
    
    Args:
        prompt: The user prompt to send
        system_message: Optional system message for context
        session_id: Optional session ID for tracking
        api_key: Optional API key (uses environment variable if not provided)
        
    Returns:
        The LLM response text
    """
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    
    if not api_key:
        api_key = os.environ.get('EMERGENT_LLM_KEY', 'sk-emergent-01d3a5f175e7fB507B')
    
    chat = LlmChat(
        api_key=api_key,
        session_id=session_id or f"narrative_{id(prompt)}",
        system_message=system_message
    ).with_model("openai", "gpt-4o-mini")
    
    response = await chat.send_message(UserMessage(text=prompt))
    return response.strip() if response else ""


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
        lines.append(f"- {d['name']}: {d['percentage']:.0f}%")
    return "\n".join(lines)


def calculate_tier(percentage: float, assessment_type: str = 'System') -> str:
    """Calculate tier from percentage score."""
    if percentage >= 75:
        return 'Leading'
    elif percentage >= 50:
        return 'Established'
    elif percentage >= 25:
        return 'Developing'
    else:
        return 'Foundational'


# =============================================================================
# AWARENESS NARRATIVES
# =============================================================================

async def generate_awareness_executive_snapshot(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate executive snapshot for Awareness assessments."""
    overall = report_data.get('overall', {})
    score = overall.get('score', 0)
    tier = overall.get('tier', 'Unknown')
    
    awareness_info = report_data.get('awareness_info', {})
    org_name = awareness_info.get('org_name') or report_data.get('org', {}).get('name', 'the organization')
    industry = awareness_info.get('industry', 'Unknown')
    
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating an executive snapshot for an AI Awareness Assessment report."
    
    prompt = f"""Write a concise executive snapshot (150-200 words) for {org_name}'s AI Awareness assessment.

Context:
- Overall Score: {score:.0f}%
- Maturity Tier: {tier}
- Industry: {industry}

Top Performing Domains:
{format_domain_summary(domain_data['top_3'])}

Areas Needing Attention:
{format_domain_summary(domain_data['bottom_3'])}

Requirements:
1. Summarize the current AI awareness maturity state
2. Highlight key strengths and opportunities
3. Provide actionable context for leadership
4. Use British English spelling
5. Be specific and avoid generic statements

Do not include headings or formatting."""

    return await call_llm(prompt, system_prompt, f"awareness_exec_{id(report_data)}", api_key)


async def generate_awareness_context_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate context interpretation for Awareness assessments."""
    awareness_info = report_data.get('awareness_info', {})
    org_name = awareness_info.get('org_name', 'the organization')
    industry = awareness_info.get('industry', 'Unknown')
    org_size = awareness_info.get('org_size', 'Unknown')
    leadership_interest = awareness_info.get('leadership_ai_interest', 'Unknown')
    
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating context interpretation for an AI Awareness Assessment."
    
    prompt = f"""Write a context interpretation (120-150 words) analyzing the organizational context.

Context:
- Organization: {org_name}
- Industry: {industry}
- Size: {org_size}
- Leadership AI Interest: {leadership_interest}

Domain Performance:
{format_domain_summary(domain_data['sorted_domains'], 5)}

Requirements:
1. Interpret how organizational context affects AI awareness
2. Identify sector-specific considerations
3. Explain leadership readiness implications
4. Use British English spelling

Do not include headings or formatting."""

    return await call_llm(prompt, system_prompt, f"awareness_context_{id(report_data)}", api_key)


async def generate_awareness_governance_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate governance interpretation for Awareness assessments."""
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating a governance interpretation for an AI Awareness Assessment."
    
    prompt = f"""Write a governance interpretation (120-150 words).

Domain Scores:
{format_domain_summary(domain_data['sorted_domains'], 5)}

Requirements:
1. Assess current governance awareness and structures
2. Identify governance gaps and risks
3. Recommend governance maturity improvements
4. Use British English spelling

Do not include headings or formatting."""

    return await call_llm(prompt, system_prompt, f"awareness_gov_{id(report_data)}", api_key)


async def generate_awareness_readiness_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate readiness interpretation for Awareness assessments."""
    overall = report_data.get('overall', {})
    score = overall.get('score', 0)
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating a readiness interpretation for an AI Awareness Assessment."
    
    prompt = f"""Write a readiness interpretation (120-150 words).

Overall Score: {score:.0f}%

Domain Performance:
{format_domain_summary(domain_data['sorted_domains'], 5)}

Requirements:
1. Interpret the organization's readiness for AI adoption
2. Identify readiness gaps and prerequisites
3. Recommend preparation steps
4. Use British English spelling

Do not include headings or formatting."""

    return await call_llm(prompt, system_prompt, f"awareness_ready_{id(report_data)}", api_key)


async def generate_awareness_domain_patterns(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate domain patterns analysis for Awareness assessments."""
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating a domain patterns analysis for an AI Awareness Assessment."
    
    prompt = f"""Write a domain patterns analysis (150-200 words).

Domain Scores:
{format_domain_summary(domain_data['sorted_domains'], len(domain_data['sorted_domains']))}

Requirements:
1. Identify patterns across domains
2. Highlight interdependencies between domains
3. Suggest strategic focus areas based on patterns
4. Use British English spelling

Do not include headings or formatting."""

    return await call_llm(prompt, system_prompt, f"awareness_patterns_{id(report_data)}", api_key)


async def generate_awareness_action_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate action interpretation for Awareness assessments."""
    actions = report_data.get('actions', {})
    high_count = len(actions.get('high', []))
    medium_count = len(actions.get('medium', []))
    low_count = len(actions.get('low', []))
    
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating an action interpretation for an AI Awareness Assessment."
    
    prompt = f"""Write an action interpretation (120-150 words).

Priority Actions:
- High: {high_count}
- Medium: {medium_count}
- Low: {low_count}

Lowest Performing Domains:
{format_domain_summary(domain_data['bottom_3'])}

Requirements:
1. Interpret the action priorities in context
2. Suggest sequencing and dependencies
3. Provide implementation guidance
4. Use British English spelling

Do not include headings or formatting."""

    return await call_llm(prompt, system_prompt, f"awareness_actions_{id(report_data)}", api_key)


async def generate_awareness_next_focus(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate next focus recommendation for Awareness assessments."""
    overall = report_data.get('overall', {})
    tier = overall.get('tier', 'Unknown')
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating a next focus recommendation for an AI Awareness Assessment."
    
    prompt = f"""Write a next focus recommendation (80-100 words).

Current Tier: {tier}

Top Focus Areas:
{format_domain_summary(domain_data['bottom_3'])}

Requirements:
1. Identify the single most impactful next step
2. Explain why this should be prioritized
3. Set clear expectations for outcomes
4. Use British English spelling

Do not include headings or formatting."""

    return await call_llm(prompt, system_prompt, f"awareness_focus_{id(report_data)}", api_key)


# =============================================================================
# READINESS NARRATIVES
# =============================================================================

async def generate_readiness_executive_snapshot(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate executive snapshot for Readiness assessments."""
    overall = report_data.get('overall', {})
    tier = overall.get('tier', 'Foundational')
    score = overall.get('score', 0)
    
    readiness_info = report_data.get('readiness_info') or {}
    org_name = readiness_info.get('org_name') or report_data.get('org', {}).get('name', 'The organisation')
    industry = readiness_info.get('industry') or report_data.get('sector_name', '')
    sector_average = report_data.get('sector_average', 0)
    
    domains = report_data.get('domains', [])
    strengths = []
    gaps = []
    domain_results = []
    
    for d in domains:
        d_score = d.get('percentage', d.get('score', 0))
        if isinstance(d_score, str):
            d_score = float(d_score.replace('%', ''))
        d_name = d.get('domain_name', d.get('name', 'Unknown'))
        d_tier = calculate_tier(d_score, 'Readiness')
        domain_results.append(f"- {d_name}: {d_score:.0f}% ({d_tier})")
        if d_score >= 70:
            strengths.append(f"{d_name} ({d_score:.0f}%)")
        elif d_score < 60:
            gaps.append(f"{d_name} ({d_score:.0f}%)")
    
    strengths_summary = ', '.join(strengths) if strengths else 'No domains currently at established level'
    gaps_summary = ', '.join(gaps) if gaps else 'All domains above 60%'
    
    system_prompt = "You are generating the Executive Snapshot narrative for an AI Readiness Assessment report."
    
    prompt = f"""Explain the organisation's overall AI readiness position in clear, executive-level language.

CRITICAL RULES:
- Do NOT state or imply that "no critical gaps exist" unless all domain scores exceed 70%.
- If foundational domains score below 60%, explicitly describe these as readiness constraints.
- Avoid language that could be interpreted as approval to proceed with AI implementation.

INPUT DATA:
- Organisation: {org_name}
- AI Readiness tier: {tier}
- AI Readiness score: {score:.0f}%
- Sector: {industry}
- Sector average: {sector_average}%
- Strengths: {strengths_summary}
- Gaps: {gaps_summary}

Domain scores:
{chr(10).join(domain_results)}

OUTPUT: 140-200 words for senior leadership. Structure:
1. What the current readiness tier indicates practically
2. Contrast internal readiness with sector context
3. Balance between enabling signals and constraints
4. One sentence on risk of proceeding at current readiness level

Use British English. No headings."""

    return await call_llm(prompt, system_prompt, f"readiness_exec_{id(report_data)}", api_key)


async def generate_readiness_context_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate context interpretation for Readiness assessments."""
    readiness_info = report_data.get('readiness_info') or {}
    org_name = readiness_info.get('org_name', 'The organisation')
    industry = readiness_info.get('industry', '')
    org_size = readiness_info.get('org_size', '')
    
    system_prompt = "You are generating Context Interpretation for an AI Readiness Assessment."
    
    prompt = f"""Explain how organisational context shapes the AI readiness baseline.

Context:
- Organisation: {org_name}
- Industry: {industry}
- Size: {org_size}

Write 100-140 words covering:
1. How size and sector context influence readiness expectations
2. What industry factors are most relevant
3. Key contextual considerations for AI adoption

Use British English. No headings."""

    return await call_llm(prompt, system_prompt, f"readiness_context_{id(report_data)}", api_key)


async def generate_readiness_governance_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate governance interpretation for Readiness assessments."""
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating Governance Interpretation for an AI Readiness Assessment."
    
    prompt = f"""Explain governance readiness signals and gaps.

Domain Scores:
{format_domain_summary(domain_data['sorted_domains'], 5)}

Write 100-140 words covering:
1. Current governance structure readiness
2. Policy and oversight gaps
3. Governance prerequisites for AI adoption

Use British English. No headings."""

    return await call_llm(prompt, system_prompt, f"readiness_gov_{id(report_data)}", api_key)


async def generate_readiness_data_tech_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate data and technology interpretation for Readiness assessments."""
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating Data & Technology Interpretation for an AI Readiness Assessment."
    
    prompt = f"""Explain data and technology readiness signals.

Domain Scores:
{format_domain_summary(domain_data['sorted_domains'], 5)}

Write 100-140 words covering:
1. Data infrastructure readiness
2. Technology capability gaps
3. Integration considerations

Use British English. No headings."""

    return await call_llm(prompt, system_prompt, f"readiness_data_{id(report_data)}", api_key)


async def generate_readiness_domain_patterns(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate domain patterns for Readiness assessments."""
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating Domain Patterns analysis for an AI Readiness Assessment."
    
    prompt = f"""Analyze patterns across readiness domains.

Domain Scores:
{format_domain_summary(domain_data['sorted_domains'], len(domain_data['sorted_domains']))}

Write 120-160 words covering:
1. Patterns observed across domains
2. Interdependencies between capability areas
3. Strategic implications of the pattern

Use British English. No headings."""

    return await call_llm(prompt, system_prompt, f"readiness_patterns_{id(report_data)}", api_key)


async def generate_readiness_sector_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate sector interpretation for Readiness assessments."""
    sector_name = report_data.get('sector_name', '')
    sector_average = report_data.get('sector_average', 0)
    overall_score = report_data.get('overall', {}).get('score', 0)
    
    system_prompt = "You are generating Sector Interpretation for an AI Readiness Assessment."
    
    prompt = f"""Explain sector context and benchmarking implications.

Context:
- Sector: {sector_name}
- Organisation Score: {overall_score:.0f}%
- Sector Average: {sector_average}%

Write 100-140 words covering:
1. How the organisation compares to sector peers
2. Sector-specific readiness considerations
3. Competitive implications

Use British English. No headings."""

    return await call_llm(prompt, system_prompt, f"readiness_sector_{id(report_data)}", api_key)


async def generate_readiness_action_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate action interpretation for Readiness assessments."""
    actions = report_data.get('actions', {})
    high_count = len(actions.get('high', []))
    medium_count = len(actions.get('medium', []))
    
    system_prompt = "You are generating Action Interpretation for an AI Readiness Assessment."
    
    prompt = f"""Explain the prioritized action recommendations.

Actions:
- High Priority: {high_count}
- Medium Priority: {medium_count}

Write 100-140 words covering:
1. Rationale for action prioritization
2. Sequencing recommendations
3. Expected outcomes from addressing priorities

Use British English. No headings."""

    return await call_llm(prompt, system_prompt, f"readiness_actions_{id(report_data)}", api_key)


async def generate_readiness_pathway_rationale(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate pathway rationale for Readiness assessments."""
    overall = report_data.get('overall', {})
    tier = overall.get('tier', 'Foundational')
    score = overall.get('score', 0)
    
    system_prompt = "You are generating Pathway Rationale for an AI Readiness Assessment."
    
    prompt = f"""Explain the recommended maturity pathway.

Current State:
- Tier: {tier}
- Score: {score:.0f}%

Write 100-140 words covering:
1. Logical progression from current state
2. Key milestones to target
3. Dependencies that influence sequencing

Use British English. No headings."""

    return await call_llm(prompt, system_prompt, f"readiness_pathway_{id(report_data)}", api_key)


# =============================================================================
# ORGWIDE NARRATIVES
# =============================================================================

async def generate_orgwide_executive_snapshot(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate executive snapshot for Orgwide assessments."""
    overall = report_data.get('overall', {})
    tier = overall.get('tier', 'Foundational')
    
    orgwide_info = report_data.get('orgwide_info') or {}
    org_name = orgwide_info.get('org_name') or report_data.get('org', {}).get('name', 'The organisation')
    industry = report_data.get('sector_name') or orgwide_info.get('industry', '')
    org_size = orgwide_info.get('org_size', '')
    ai_project_count = orgwide_info.get('ai_project_count', '')
    ai_sourcing_model = orgwide_info.get('ai_sourcing_model', '')
    
    strengths_summary = report_data.get('strengths_summary', '')
    gaps_summary = report_data.get('gaps_summary', '')
    
    system_prompt = """You are generating narrative content for an Organisation-wide AI Maturity Assessment report.

Global rules:
- Do NOT assess individual AI systems
- Do NOT claim compliance or certification
- Do NOT repeat tables or scores shown elsewhere
- Avoid excessive hedging unless uncertainty is explicit
- Focus on cause-and-effect relationships
- Reflect maturity (consistency and embedment), not readiness
- Assume an executive audience with limited time"""

    prompt = f"""Write a concise executive interpretation of {org_name}'s organisation-wide AI maturity posture.

Context:
- Sector: {industry}
- Size: {org_size}
- Maturity tier: {tier}
- Key strengths: {strengths_summary}
- Key gaps: {gaps_summary}
- AI scale: {ai_project_count}, {ai_sourcing_model}

Guidance:
- Focus on implications for leadership, scalability, and risk oversight
- Clearly articulate what this maturity level enables and constrains
- 1-2 paragraphs, approximately 100 words

No headings or formatting."""

    return await call_llm(prompt, system_prompt, f"orgwide_exec_{id(report_data)}", api_key)


async def generate_orgwide_landscape(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate AI landscape summary for Orgwide assessments."""
    orgwide_info = report_data.get('orgwide_info') or {}
    ai_project_count = orgwide_info.get('ai_project_count', '')
    ai_sourcing_model = orgwide_info.get('ai_sourcing_model', '')
    
    system_prompt = "You are generating AI Landscape narrative for an Organisation-wide AI Maturity Assessment."
    
    prompt = f"""Explain how the AI landscape increases or reduces governance complexity.

Context:
- AI project count: {ai_project_count}
- AI sourcing model: {ai_sourcing_model}

Write 80-120 words covering:
1. Current AI footprint complexity
2. Governance implications of scale
3. Risk considerations from landscape

No headings."""

    return await call_llm(prompt, system_prompt, f"orgwide_landscape_{id(report_data)}", api_key)


async def generate_orgwide_gov_oversight(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate governance and oversight narrative for Orgwide assessments."""
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating Governance & Oversight narrative for an Organisation-wide AI Maturity Assessment."
    
    prompt = f"""Explain governance and oversight maturity signals.

Domain Scores:
{format_domain_summary(domain_data['sorted_domains'], 5)}

Write 80-120 words covering:
1. Governance structure maturity
2. Oversight mechanism presence
3. Accountability patterns

No headings."""

    return await call_llm(prompt, system_prompt, f"orgwide_gov_{id(report_data)}", api_key)


async def generate_orgwide_risk_policy(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate risk and policy narrative for Orgwide assessments."""
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating Risk & Policy narrative for an Organisation-wide AI Maturity Assessment."
    
    prompt = f"""Explain risk management and policy maturity signals.

Domain Scores:
{format_domain_summary(domain_data['sorted_domains'], 5)}

Write 80-120 words covering:
1. Risk management framework maturity
2. Policy coverage and gaps
3. Compliance posture signals

No headings."""

    return await call_llm(prompt, system_prompt, f"orgwide_risk_{id(report_data)}", api_key)


async def generate_orgwide_culture_capability(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate culture and capability narrative for Orgwide assessments."""
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating Culture & Capability narrative for an Organisation-wide AI Maturity Assessment."
    
    prompt = f"""Explain organizational culture and capability maturity.

Domain Scores:
{format_domain_summary(domain_data['sorted_domains'], 5)}

Write 80-120 words covering:
1. AI culture maturity signals
2. Capability and skills readiness
3. Change management considerations

No headings."""

    return await call_llm(prompt, system_prompt, f"orgwide_culture_{id(report_data)}", api_key)


async def generate_orgwide_domain_patterns(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate domain patterns for Orgwide assessments."""
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating Domain Patterns analysis for an Organisation-wide AI Maturity Assessment."
    
    prompt = f"""Analyze maturity patterns across domains.

Domain Scores:
{format_domain_summary(domain_data['sorted_domains'], len(domain_data['sorted_domains']))}

Write 100-140 words covering:
1. Cross-domain maturity patterns
2. Domain interdependencies
3. Strategic focus implications

No headings."""

    return await call_llm(prompt, system_prompt, f"orgwide_patterns_{id(report_data)}", api_key)


async def generate_orgwide_sector_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate sector interpretation for Orgwide assessments."""
    sector_name = report_data.get('sector_name', '')
    sector_average = report_data.get('sector_average', 0)
    overall_score = report_data.get('overall', {}).get('score', 0)
    
    system_prompt = "You are generating Sector Interpretation for an Organisation-wide AI Maturity Assessment."
    
    prompt = f"""Explain sector context and comparative positioning.

Context:
- Sector: {sector_name}
- Organisation Score: {overall_score:.0f}%
- Sector Average: {sector_average}%

Write 80-120 words covering:
1. Positioning relative to sector peers
2. Sector-specific maturity expectations
3. Competitive implications

No headings."""

    return await call_llm(prompt, system_prompt, f"orgwide_sector_{id(report_data)}", api_key)


async def generate_orgwide_pathway_rationale(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate pathway rationale for Orgwide assessments."""
    overall = report_data.get('overall', {})
    tier = overall.get('tier', 'Foundational')
    score = overall.get('score', 0)
    domain_data = extract_domain_data(report_data)
    
    system_prompt = "You are generating Pathway Rationale for an Organisation-wide AI Maturity Assessment."
    
    prompt = f"""Explain the recommended maturity pathway.

Current State:
- Tier: {tier}
- Score: {score:.0f}%

Lowest Domains:
{format_domain_summary(domain_data['bottom_3'])}

Write 100-140 words covering:
1. Logical progression from current state
2. Priority areas based on patterns
3. Dependencies influencing sequencing

No headings."""

    return await call_llm(prompt, system_prompt, f"orgwide_pathway_{id(report_data)}", api_key)


# =============================================================================
# SYSTEM NARRATIVES
# =============================================================================

async def generate_system_executive_snapshot(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate executive snapshot for System assessments."""
    overall = report_data.get('overall', {})
    tier = overall.get('tier', 'Foundational')
    score = overall.get('score', 0)
    
    system_info = report_data.get('system_info') or {}
    system_name = system_info.get('system_name') or system_info.get('systemName', 'The system')
    lifecycle = system_info.get('lifecycle', '')
    criticality = system_info.get('criticality', '')
    industry = system_info.get('industry', '') or system_info.get('sector', '')
    sector_average = report_data.get('sector_average', None)
    
    if sector_average is not None:
        if score > sector_average + 5:
            sector_comparison = "sits above"
        elif score < sector_average - 5:
            sector_comparison = "sits below"
        else:
            sector_comparison = "sits broadly aligned with"
    else:
        sector_comparison = "sits within"
    
    system_prompt = """You are generating a concise executive maturity narrative for an AI System Maturity Assessment.

You must:
- Use "indicative" or "typical range" language when referencing sector context
- Use neutral positioning language such as "sits" rather than evaluative verbs

You must NOT:
- Assert effectiveness, sufficiency, safety, or outcomes
- Use evaluative language (e.g. "robust", "effective", "mature")
- Include recommendations or future-oriented advice
- Reference frameworks, compliance, or regulatory readiness

Tone: neutral, factual, executive-appropriate
Length: maximum 120 words"""

    prompt = f"""Write a single paragraph executive summary for:

- System: {system_name}
- Overall AI System Maturity score: {score}% ({tier})
- Lifecycle stage: {lifecycle}
- Business criticality: {criticality}
- Industry: {industry}
- Sector comparison: The score {sector_comparison} the typical maturity range observed for AI systems in the {industry} industry

Maximum 120 words, no headings."""

    return await call_llm(prompt, system_prompt, f"system_exec_{id(report_data)}", api_key)


async def generate_system_gov_oversight(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate governance and oversight narrative for System assessments."""
    system_info = report_data.get('system_info') or {}
    system_name = system_info.get('system_name') or system_info.get('systemName', 'The system')
    lifecycle = system_info.get('lifecycle', '')
    criticality = system_info.get('criticality', '')
    
    domain_data = extract_domain_data(report_data)
    accountability = next((d for d in domain_data['domain_scores'] if 'accountability' in d['name'].lower()), None)
    acc_score = accountability['percentage'] if accountability else 0
    
    system_prompt = """You are generating governance narrative for an AI System Maturity Assessment.
Use neutral, factual language. Do not make recommendations or assertions about adequacy.
Length: maximum 100 words"""

    prompt = f"""Write a governance narrative for:
- System: {system_name}
- Lifecycle: {lifecycle}
- Criticality: {criticality}
- Accountability domain score: {acc_score:.0f}%

Maximum 100 words, no headings."""

    return await call_llm(prompt, system_prompt, f"system_gov_{id(report_data)}", api_key)


async def generate_system_data_privacy_security(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate data, privacy and security narrative for System assessments."""
    system_info = report_data.get('system_info') or {}
    system_name = system_info.get('system_name') or system_info.get('systemName', 'The system')
    
    domain_data = extract_domain_data(report_data)
    data_integrity = next((d for d in domain_data['domain_scores'] if 'data integrity' in d['name'].lower()), None)
    privacy = next((d for d in domain_data['domain_scores'] if 'privacy' in d['name'].lower()), None)
    security = next((d for d in domain_data['domain_scores'] if 'security' in d['name'].lower()), None)
    
    system_prompt = """You are generating data/privacy/security narrative for an AI System Maturity Assessment.
Use neutral, factual language. Do not make recommendations.
Length: maximum 100 words"""

    prompt = f"""Write a data/privacy/security narrative for:
- System: {system_name}
- Data Integrity: {data_integrity['percentage']:.0f}% if data_integrity else 'N/A'
- Privacy: {privacy['percentage']:.0f}% if privacy else 'N/A'
- Security: {security['percentage']:.0f}% if security else 'N/A'

Maximum 100 words, no headings."""

    return await call_llm(prompt, system_prompt, f"system_data_{id(report_data)}", api_key)


async def generate_system_reliability_safety(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate reliability and safety narrative for System assessments."""
    system_info = report_data.get('system_info') or {}
    system_name = system_info.get('system_name') or system_info.get('systemName', 'The system')
    
    domain_data = extract_domain_data(report_data)
    reliability = next((d for d in domain_data['domain_scores'] if 'reliability' in d['name'].lower()), None)
    safety = next((d for d in domain_data['domain_scores'] if 'safety' in d['name'].lower()), None)
    
    system_prompt = """You are generating reliability/safety narrative for an AI System Maturity Assessment.
Use neutral, factual language. Do not make recommendations.
Length: maximum 100 words"""

    prompt = f"""Write a reliability/safety narrative for:
- System: {system_name}
- Reliability: {reliability['percentage']:.0f}% if reliability else 'N/A'
- Safety: {safety['percentage']:.0f}% if safety else 'N/A'

Maximum 100 words, no headings."""

    return await call_llm(prompt, system_prompt, f"system_rel_{id(report_data)}", api_key)


async def generate_system_transparency_explainability(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate transparency and explainability narrative for System assessments."""
    system_info = report_data.get('system_info') or {}
    system_name = system_info.get('system_name') or system_info.get('systemName', 'The system')
    
    domain_data = extract_domain_data(report_data)
    transparency = next((d for d in domain_data['domain_scores'] if 'transparency' in d['name'].lower()), None)
    explainability = next((d for d in domain_data['domain_scores'] if 'explainability' in d['name'].lower()), None)
    
    system_prompt = """You are generating transparency/explainability narrative for an AI System Maturity Assessment.
Use neutral, factual language. Do not make recommendations.
Length: maximum 100 words"""

    prompt = f"""Write a transparency/explainability narrative for:
- System: {system_name}
- Transparency: {transparency['percentage']:.0f}% if transparency else 'N/A'
- Explainability: {explainability['percentage']:.0f}% if explainability else 'N/A'

Maximum 100 words, no headings."""

    return await call_llm(prompt, system_prompt, f"system_trans_{id(report_data)}", api_key)


async def generate_system_fairness_inclusivity(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate fairness and inclusivity narrative for System assessments."""
    system_info = report_data.get('system_info') or {}
    system_name = system_info.get('system_name') or system_info.get('systemName', 'The system')
    
    domain_data = extract_domain_data(report_data)
    fairness = next((d for d in domain_data['domain_scores'] if 'fairness' in d['name'].lower()), None)
    inclusivity = next((d for d in domain_data['domain_scores'] if 'inclusivity' in d['name'].lower()), None)
    
    system_prompt = """You are generating fairness/inclusivity narrative for an AI System Maturity Assessment.
Use neutral, factual language. Do not make recommendations.
Length: maximum 100 words"""

    prompt = f"""Write a fairness/inclusivity narrative for:
- System: {system_name}
- Fairness: {fairness['percentage']:.0f}% if fairness else 'N/A'
- Inclusivity: {inclusivity['percentage']:.0f}% if inclusivity else 'N/A'

Maximum 100 words, no headings."""

    return await call_llm(prompt, system_prompt, f"system_fair_{id(report_data)}", api_key)


async def generate_system_domain_patterns(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate domain patterns narrative for System assessments."""
    domain_data = extract_domain_data(report_data)
    
    system_prompt = """You are generating domain patterns analysis for an AI System Maturity Assessment.
Use neutral, analytical language. Do not make recommendations.
Length: maximum 120 words"""

    prompt = f"""Analyze domain patterns:

{format_domain_summary(domain_data['sorted_domains'], len(domain_data['sorted_domains']))}

Maximum 120 words, no headings."""

    return await call_llm(prompt, system_prompt, f"system_patterns_{id(report_data)}", api_key)


async def generate_system_pathway_rationale(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate pathway rationale narrative for System assessments."""
    overall = report_data.get('overall', {})
    tier = overall.get('tier', 'Foundational')
    score = overall.get('score', 0)
    domain_data = extract_domain_data(report_data)
    
    system_prompt = """You are generating maturity pathway rationale for an AI System Maturity Assessment.
Use neutral language. Frame as observations, not prescriptions.
Length: maximum 120 words"""

    prompt = f"""Generate pathway rationale for:
- Current tier: {tier}
- Score: {score}%

Lowest scoring domains:
{format_domain_summary(domain_data['bottom_3'])}

Maximum 120 words, no headings."""

    return await call_llm(prompt, system_prompt, f"system_pathway_{id(report_data)}", api_key)


# =============================================================================
# ORCHESTRATORS - Main entry points for each assessment type
# =============================================================================

async def generate_awareness_narratives(
    report_data: Dict[str, Any],
    assessment: Dict[str, Any],
    db,
    api_key: str
) -> Dict[str, str]:
    """Generate all AI narratives for Awareness assessments."""
    narratives = {}
    assessment_id = assessment.get('id')
    cached_narratives = assessment.get('ai_narratives', {})
    
    generators = [
        ('executive_snapshot', generate_awareness_executive_snapshot),
        ('context_interpretation', generate_awareness_context_interpretation),
        ('governance_interpretation', generate_awareness_governance_interpretation),
        ('readiness_interpretation', generate_awareness_readiness_interpretation),
        ('domain_patterns', generate_awareness_domain_patterns),
        ('action_interpretation', generate_awareness_action_interpretation),
        ('next_focus', generate_awareness_next_focus),
    ]
    
    for key, generator in generators:
        if cached_narratives.get(key):
            narratives[key] = cached_narratives[key]
            print(f"DEBUG: Using cached AI {key} narrative (Awareness)")
        else:
            try:
                narratives[key] = await generator(report_data, api_key)
                print(f"DEBUG: Generated new AI {key} narrative (Awareness) ({len(narratives[key])} chars)")
            except Exception as e:
                print(f"ERROR generating AI {key} (Awareness): {e}")
                narratives[key] = ""
    
    # Cache to database
    if db and assessment_id and narratives:
        try:
            await db.assessments.update_one(
                {'id': assessment_id},
                {'$set': {'ai_narratives': {**cached_narratives, **narratives}}}
            )
            print("DEBUG: Cached AI narratives to database (Awareness)")
        except Exception as e:
            print(f"WARNING: Failed to cache AI narratives: {e}")
    
    return narratives


async def generate_readiness_narratives(
    report_data: Dict[str, Any],
    assessment: Dict[str, Any],
    db,
    api_key: str
) -> Dict[str, str]:
    """Generate all AI narratives for Readiness assessments."""
    narratives = {}
    assessment_id = assessment.get('id')
    cached_narratives = assessment.get('ai_narratives', {})
    
    generators = [
        ('r_executive_snapshot', generate_readiness_executive_snapshot),
        ('r_context_interpretation', generate_readiness_context_interpretation),
        ('r_governance_interpretation', generate_readiness_governance_interpretation),
        ('r_data_tech_interpretation', generate_readiness_data_tech_interpretation),
        ('r_domain_patterns', generate_readiness_domain_patterns),
        ('r_sector_interpretation', generate_readiness_sector_interpretation),
        ('r_action_interpretation', generate_readiness_action_interpretation),
        ('r_pathway_rationale', generate_readiness_pathway_rationale),
    ]
    
    for key, generator in generators:
        if cached_narratives.get(key):
            narratives[key] = cached_narratives[key]
            print(f"DEBUG: Using cached AI {key} narrative (Readiness)")
        else:
            try:
                narratives[key] = await generator(report_data, api_key)
                print(f"DEBUG: Generated new AI {key} narrative (Readiness) ({len(narratives[key])} chars)")
            except Exception as e:
                print(f"ERROR generating AI {key} (Readiness): {e}")
                narratives[key] = ""
    
    # Cache to database
    if db and assessment_id and narratives:
        try:
            await db.assessments.update_one(
                {'id': assessment_id},
                {'$set': {'ai_narratives': {**cached_narratives, **narratives}}}
            )
            print("DEBUG: Cached AI narratives to database (Readiness)")
        except Exception as e:
            print(f"WARNING: Failed to cache AI narratives: {e}")
    
    return narratives


async def generate_orgwide_narratives(
    report_data: Dict[str, Any],
    assessment: Dict[str, Any],
    db,
    api_key: str
) -> Dict[str, str]:
    """Generate all AI narratives for Orgwide assessments."""
    narratives = {}
    assessment_id = assessment.get('id')
    cached_narratives = assessment.get('ai_narratives', {})
    
    generators = [
        ('o_executive_snapshot', generate_orgwide_executive_snapshot),
        ('o_landscape', generate_orgwide_landscape),
        ('o_gov_oversight', generate_orgwide_gov_oversight),
        ('o_risk_policy', generate_orgwide_risk_policy),
        ('o_culture_capability', generate_orgwide_culture_capability),
        ('o_domain_patterns', generate_orgwide_domain_patterns),
        ('o_sector_interpretation', generate_orgwide_sector_interpretation),
        ('o_pathway_rationale', generate_orgwide_pathway_rationale),
    ]
    
    for key, generator in generators:
        if cached_narratives.get(key):
            narratives[key] = cached_narratives[key]
            print(f"DEBUG: Using cached AI {key} narrative (Orgwide)")
        else:
            try:
                narratives[key] = await generator(report_data, api_key)
                print(f"DEBUG: Generated new AI {key} narrative (Orgwide) ({len(narratives[key])} chars)")
            except Exception as e:
                print(f"ERROR generating AI {key} (Orgwide): {e}")
                narratives[key] = ""
    
    # Cache to database
    if db and assessment_id and narratives:
        try:
            await db.assessments.update_one(
                {'id': assessment_id},
                {'$set': {'ai_narratives': {**cached_narratives, **narratives}}}
            )
            print("DEBUG: Cached AI narratives to database (Orgwide)")
        except Exception as e:
            print(f"WARNING: Failed to cache AI narratives: {e}")
    
    return narratives


async def generate_system_narratives(
    report_data: Dict[str, Any],
    assessment: Dict[str, Any],
    db,
    api_key: str
) -> Dict[str, str]:
    """Generate all AI narratives for System assessments."""
    narratives = {}
    assessment_id = assessment.get('id')
    cached_narratives = assessment.get('ai_narratives', {})
    
    generators = [
        ('s_executive_snapshot', generate_system_executive_snapshot),
        ('s_gov_oversight', generate_system_gov_oversight),
        ('s_data_privacy_security', generate_system_data_privacy_security),
        ('s_reliability_safety_performance', generate_system_reliability_safety),
        ('s_transparency_explainability_contestability', generate_system_transparency_explainability),
        ('s_fairness_bias_inclusivity', generate_system_fairness_inclusivity),
        ('s_domain_patterns', generate_system_domain_patterns),
        ('s_pathway_rationale', generate_system_pathway_rationale),
    ]
    
    for key, generator in generators:
        if cached_narratives.get(key):
            narratives[key] = cached_narratives[key]
            print(f"DEBUG: Using cached AI {key} narrative (System)")
        else:
            try:
                narratives[key] = await generator(report_data, api_key)
                print(f"DEBUG: Generated new AI {key} narrative (System) ({len(narratives[key])} chars)")
            except Exception as e:
                print(f"ERROR generating AI {key} (System): {e}")
                narratives[key] = ""
    
    # Cache to database
    if db and assessment_id and narratives:
        try:
            await db.assessments.update_one(
                {'id': assessment_id},
                {'$set': {'ai_narratives': {**cached_narratives, **narratives}}}
            )
            print("DEBUG: Cached AI narratives to database (System)")
        except Exception as e:
            print(f"WARNING: Failed to cache AI narratives: {e}")
    
    return narratives


# =============================================================================
# FAIRA NARRATIVES (32 AI Narrative Placeholders)
# =============================================================================

# FAIRA Global Guardrails - Applied to ALL FAIRA narrative prompts
FAIRA_GLOBAL_GUARDRAILS = """You are generating narrative content for a FAIRA (Framework for the Assurance of AI in Government) risk assessment report.

STRICT RULES:
- Base your response ONLY on the provided variables.
- Do NOT introduce new facts, assumptions, or external references.
- Do NOT state or imply compliance or non-compliance.
- Do NOT assign blame, fault, or responsibility to individuals.
- Do NOT use prescriptive language (e.g. "must", "should", "ensure").
- Do NOT recommend specific controls unless explicitly instructed.
- Treat all scores as normalised and relative.
- Use neutral, professional, assurance-oriented language.
- Output plain text only (no headings, no bullet lists)."""


def get_faira_domain_scores(report_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Extract domain scores from FAIRA report data."""
    domain_scores = report_data.get('domain_scores', {})
    if not domain_scores:
        # Try to build from ethics_scores
        ethics_scores = report_data.get('ethics_scores', [])
        for score in ethics_scores:
            domain_name = score.get('short_label', score.get('domain', ''))
            domain_scores[domain_name] = {
                'Impact': score.get('impact', 0),
                'Likelihood': score.get('likelihood', 0),
                'Inherent_Risk': score.get('inherent_risk', 0),
                'Control_Effectiveness': score.get('control_effectiveness', 0),
                'Risk': score.get('risk_score', score.get('risk', 0))
            }
    return domain_scores


def get_faira_form_value(report_data: Dict[str, Any], key: str, default: str = "Not specified") -> str:
    """Get a value from the FAIRA form responses."""
    faira_form = report_data.get('faira_form', {})
    if not faira_form:
        faira_form = report_data.get('form_responses', {})
    value = faira_form.get(key, default)
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) if value else default
    return str(value) if value else default


def get_faira_top_domains(report_data: Dict[str, Any], n: int = 3) -> str:
    """Get top N risk domains formatted as a string."""
    top_risks = report_data.get('top_risk_areas', [])
    if not top_risks:
        domain_scores = get_faira_domain_scores(report_data)
        sorted_domains = sorted(
            [(k, v.get('Risk', 0)) for k, v in domain_scores.items()],
            key=lambda x: x[1],
            reverse=True
        )
        top_risks = [{'domain': d[0], 'risk_score': d[1]} for d in sorted_domains[:n]]
    
    return ", ".join([f"{r.get('domain', r.get('fullName', 'Unknown'))} ({r.get('risk_score', 0):.0f})" for r in top_risks[:n]])


def get_faira_recommended_controls(report_data: Dict[str, Any], domain: str) -> str:
    """Get recommended controls for a specific domain."""
    controls = report_data.get('recommended_controls', {})
    if isinstance(controls, dict):
        domain_controls = controls.get(domain, [])
    else:
        domain_controls = [c for c in controls if domain in c.get('domains', [])]
    
    if not domain_controls:
        return "No specific controls recommended"
    
    if isinstance(domain_controls, list):
        return "; ".join([c.get('title', c) if isinstance(c, dict) else str(c) for c in domain_controls[:3]])
    return str(domain_controls)


# -----------------------------------------------------------------------------
# Section 1: Executive and Overview Narratives
# -----------------------------------------------------------------------------

async def generate_faira_executive_snapshot(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_executive_snapshot}} - Executive summary narrative."""
    system_name = get_faira_form_value(report_data, 'A1_2', report_data.get('system_name', 'the AI system'))
    assessment_scope = get_faira_form_value(report_data, 'A1_4', 'Not specified')
    deployment_context = get_faira_form_value(report_data, 'A4_3', 'Not specified')
    overall_risk_level = report_data.get('overall_risk_level', 'Medium')
    overall_risk_score = report_data.get('overall_risk_score', 50)
    top_domains = get_faira_top_domains(report_data)
    
    prompt = f"""Using the FAIRA assessment results for {system_name}, generate a concise executive summary narrative.

Base the narrative ONLY on:
- Assessment scope: {assessment_scope}
- Deployment context: {deployment_context}
- Overall risk level: {overall_risk_level}
- Overall risk score: {overall_risk_score}
- Domains identified as top risk areas: {top_domains}

Explain what the overall risk level represents in relative terms, how system context influences the risk profile, and how the assessment supports informed decision-making.

Do not restate tables, charts, or individual domain scores.
Limit the output to a maximum of two short paragraphs."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_exec_{id(report_data)}", api_key)


async def generate_faira_risk_profile_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_risk_profile_interpretation}} - Risk profile interpretation."""
    overall_impact = report_data.get('overall_impact_score', report_data.get('total_impact', 50))
    overall_likelihood = report_data.get('overall_likelihood_score', report_data.get('total_likelihood', 50))
    overall_control = report_data.get('overall_control_effectiveness_score', report_data.get('total_control_effectiveness', 50))
    overall_risk = report_data.get('overall_risk_score', 50)
    
    prompt = f"""Interpret the overall FAIRA risk profile using the following normalised scores:
- Impact: {overall_impact}
- Likelihood: {overall_likelihood}
- Control effectiveness: {overall_control}
- Residual risk: {overall_risk}

Explain how these dimensions interact and why residual risk may remain even where controls are present.

Do not reference individual domains.
Do not provide recommendations."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_risk_profile_{id(report_data)}", api_key)


async def generate_faira_methodology_interpretation(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_methodology_interpretation}} - Methodology explanation."""
    system_name = get_faira_form_value(report_data, 'A1_2', report_data.get('system_name', 'the AI system'))
    methodology = report_data.get('assessment_methodology', 'FAIRA Framework v1.0 - Queensland Government AI Risk Assessment')
    scoring_method = report_data.get('scoring_method', 'Risk Score = (Impact × Likelihood) / Control Effectiveness')
    normalisation = report_data.get('normalisation_notes', 'Scores normalised to 0-100 scale for comparability')
    
    prompt = f"""Explain the FAIRA assessment methodology as applied to {system_name}.

Base the explanation ONLY on:
- Methodology description: {methodology}
- Scoring approach: {scoring_method}
- Normalisation approach: {normalisation}

Explain how impact, likelihood, and control effectiveness are combined to produce relative residual risk scores.

Do not justify or defend the methodology.
Do not compare to other frameworks."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_methodology_{id(report_data)}", api_key)


# -----------------------------------------------------------------------------
# Section 2: Context Notes (Part A Sections)
# -----------------------------------------------------------------------------

async def generate_faira_system_overview_notes(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_system_overview_notes}} - System overview narrative."""
    system_desc = get_faira_form_value(report_data, 'A1_1')
    primary_function = get_faira_form_value(report_data, 'A1_2')
    decision_role = get_faira_form_value(report_data, 'A1_3')
    
    prompt = f"""Provide a narrative overview of the assessed AI system.

Base the narrative ONLY on:
- System description: {system_desc}
- Primary function: {primary_function}
- Decision support role: {decision_role}

Explain the system's role and purpose in context without evaluating effectiveness or suitability."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_sys_overview_{id(report_data)}", api_key)


async def generate_faira_data_context_notes(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_data_context_notes}} - Data context summary."""
    data_sources = get_faira_form_value(report_data, 'A2_1')
    data_types = get_faira_form_value(report_data, 'A2_2')
    sensitive_data = get_faira_form_value(report_data, 'A2_5')
    data_storage = get_faira_form_value(report_data, 'A2_7')
    
    prompt = f"""Summarise the data context relevant to the assessed AI system.

Base the summary ONLY on:
- Data sources: {data_sources}
- Data types: {data_types}
- Sensitive or regulated data indicators: {sensitive_data}
- Data storage and retention context: {data_storage}

Explain how data characteristics influence risk context without assessing safeguards."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_data_context_{id(report_data)}", api_key)


async def generate_faira_user_stakeholder_notes(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_user_stakeholder_context_notes}} - User/stakeholder context."""
    user_groups = get_faira_form_value(report_data, 'A3_1')
    stakeholder_groups = get_faira_form_value(report_data, 'A3_5')
    user_expertise = get_faira_form_value(report_data, 'A3_3')
    
    prompt = f"""Summarise the user and stakeholder context for the assessed AI system.

Base the summary ONLY on:
- User groups: {user_groups}
- Stakeholder groups: {stakeholder_groups}
- User expertise levels: {user_expertise}

Explain how user and stakeholder characteristics influence system interaction and risk context."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_user_context_{id(report_data)}", api_key)


async def generate_faira_deployment_context_notes(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_deployment_context_notes}} - Deployment context summary."""
    deployment_model = get_faira_form_value(report_data, 'A4_1')
    operational_env = get_faira_form_value(report_data, 'A4_3')
    integration_context = get_faira_form_value(report_data, 'A4_4')
    
    prompt = f"""Summarise the deployment and operational context for the assessed AI system.

Base the summary ONLY on:
- Deployment model: {deployment_model}
- Operational environment: {operational_env}
- System integration context: {integration_context}

Explain how deployment characteristics influence AI risk exposure without assessing technical design."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_deploy_context_{id(report_data)}", api_key)


async def generate_faira_impact_context_notes(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_impact_context_notes}} - Impact context summary."""
    impact_scale = get_faira_form_value(report_data, 'A5_1')
    impact_severity = get_faira_form_value(report_data, 'A5_2')
    affected_parties = get_faira_form_value(report_data, 'A5_3')
    
    prompt = f"""Summarise the potential impact context associated with the assessed AI system.

Base the summary ONLY on:
- Impact scale: {impact_scale}
- Impact severity considerations: {impact_severity}
- Affected parties: {affected_parties}

Explain how potential impacts shape the overall risk context without implying harm has occurred."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_impact_context_{id(report_data)}", api_key)


# -----------------------------------------------------------------------------
# Section 3: Domain Analysis Narratives (Part B - 8 Ethics Domains)
# -----------------------------------------------------------------------------

async def generate_faira_domain_analysis(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_analysis}} - Overall domain patterns synthesis."""
    domain_scores = get_faira_domain_scores(report_data)
    overall_risk = report_data.get('overall_risk_score', 50)
    
    domain_summary = "\n".join([f"- {k}: Risk={v.get('Risk', 0):.0f}" for k, v in domain_scores.items()])
    
    prompt = f"""Provide a brief synthesis of overall patterns observed across FAIRA ethics domains.

Base the synthesis ONLY on:
- Domain scores summary:
{domain_summary}
- Overall risk score: {overall_risk}

Identify high-level themes without referencing individual domain narratives or controls."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_domain_analysis_{id(report_data)}", api_key)


async def generate_faira_domain_b1_analysis(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b1_analysis}} - Accountability domain analysis."""
    domain_scores = get_faira_domain_scores(report_data)
    acc = domain_scores.get('Accountability', {})
    
    prompt = f"""Analyse the Accountability domain using:
Impact {acc.get('Impact', 0)},
Likelihood {acc.get('Likelihood', 0)},
Inherent risk {acc.get('Inherent_Risk', 0)},
Control effectiveness {acc.get('Control_Effectiveness', 0)},
Residual risk {acc.get('Risk', 0)}.

Explain factors influencing residual risk and the role of accountability arrangements."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_b1_{id(report_data)}", api_key)


async def generate_faira_domain_b2_analysis(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b2_analysis}} - Contestability domain analysis."""
    domain_scores = get_faira_domain_scores(report_data)
    cont = domain_scores.get('Contestability', {})
    
    prompt = f"""Analyse the Contestability domain using:
Impact {cont.get('Impact', 0)},
Likelihood {cont.get('Likelihood', 0)},
Inherent risk {cont.get('Inherent_Risk', 0)},
Control effectiveness {cont.get('Control_Effectiveness', 0)},
Residual risk {cont.get('Risk', 0)}.

Explain how review and challenge mechanisms influence residual risk."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_b2_{id(report_data)}", api_key)


async def generate_faira_domain_b3_analysis(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b3_analysis}} - Fairness domain analysis."""
    domain_scores = get_faira_domain_scores(report_data)
    fair = domain_scores.get('Fairness', {})
    data_types = get_faira_form_value(report_data, 'A2_2')
    sensitive_data = get_faira_form_value(report_data, 'A2_5')
    
    prompt = f"""Analyse the Fairness domain using:
Impact {fair.get('Impact', 0)},
Likelihood {fair.get('Likelihood', 0)},
Inherent risk {fair.get('Inherent_Risk', 0)},
Control effectiveness {fair.get('Control_Effectiveness', 0)},
Residual risk {fair.get('Risk', 0)}.

Data context: {data_types}, {sensitive_data}

Explain contextual drivers of fairness-related risk."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_b3_{id(report_data)}", api_key)


async def generate_faira_domain_b4_analysis(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b4_analysis}} - Wellbeing domain analysis."""
    domain_scores = get_faira_domain_scores(report_data)
    well = domain_scores.get('Wellbeing', {})
    impact_scale = get_faira_form_value(report_data, 'A5_1')
    impact_severity = get_faira_form_value(report_data, 'A5_2')
    
    prompt = f"""Analyse the Human, Societal & Environmental Wellbeing domain using:
Impact {well.get('Impact', 0)},
Likelihood {well.get('Likelihood', 0)},
Inherent risk {well.get('Inherent_Risk', 0)},
Control effectiveness {well.get('Control_Effectiveness', 0)},
Residual risk {well.get('Risk', 0)}.

Impact context: {impact_scale}, {impact_severity}

Explain how scale and downstream effects influence risk."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_b4_{id(report_data)}", api_key)


async def generate_faira_domain_b5_analysis(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b5_analysis}} - Human-Centred Values domain analysis."""
    domain_scores = get_faira_domain_scores(report_data)
    vals = domain_scores.get('Values', {})
    user_groups = get_faira_form_value(report_data, 'A3_1')
    user_expertise = get_faira_form_value(report_data, 'A3_3')
    
    prompt = f"""Analyse the Human-Centred Values domain using:
Impact {vals.get('Impact', 0)},
Likelihood {vals.get('Likelihood', 0)},
Inherent risk {vals.get('Inherent_Risk', 0)},
Control effectiveness {vals.get('Control_Effectiveness', 0)},
Residual risk {vals.get('Risk', 0)}.

User groups: {user_groups}
Expertise levels: {user_expertise}

Explain how user capability influences residual risk."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_b5_{id(report_data)}", api_key)


async def generate_faira_domain_b6_analysis(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b6_analysis}} - Privacy domain analysis."""
    domain_scores = get_faira_domain_scores(report_data)
    priv = domain_scores.get('Privacy', {})
    sensitive_data = get_faira_form_value(report_data, 'A2_5')
    
    prompt = f"""Analyse the Privacy Protection & Security domain using:
Impact {priv.get('Impact', 0)},
Likelihood {priv.get('Likelihood', 0)},
Inherent risk {priv.get('Inherent_Risk', 0)},
Control effectiveness {priv.get('Control_Effectiveness', 0)},
Residual risk {priv.get('Risk', 0)}.

Data sensitivity context: {sensitive_data}

Explain how data characteristics influence risk context."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_b6_{id(report_data)}", api_key)


async def generate_faira_domain_b7_analysis(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b7_analysis}} - Reliability domain analysis."""
    domain_scores = get_faira_domain_scores(report_data)
    rel = domain_scores.get('Reliability', {})
    impact_severity = get_faira_form_value(report_data, 'A5_2')
    
    prompt = f"""Analyse the Reliability & Safety domain using:
Impact {rel.get('Impact', 0)},
Likelihood {rel.get('Likelihood', 0)},
Inherent risk {rel.get('Inherent_Risk', 0)},
Control effectiveness {rel.get('Control_Effectiveness', 0)},
Residual risk {rel.get('Risk', 0)}.

Impact context: {impact_severity}

Explain how reliability expectations shape residual risk."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_b7_{id(report_data)}", api_key)


async def generate_faira_domain_b8_analysis(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b8_analysis}} - Transparency domain analysis."""
    domain_scores = get_faira_domain_scores(report_data)
    trans = domain_scores.get('Transparency', {})
    user_expertise = get_faira_form_value(report_data, 'A3_3')
    
    prompt = f"""Analyse the Transparency & Explainability domain using:
Impact {trans.get('Impact', 0)},
Likelihood {trans.get('Likelihood', 0)},
Inherent risk {trans.get('Inherent_Risk', 0)},
Control effectiveness {trans.get('Control_Effectiveness', 0)},
Residual risk {trans.get('Risk', 0)}.

User expertise context: {user_expertise}

Explain how understanding of outputs influences residual risk."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_b8_{id(report_data)}", api_key)


async def generate_faira_top_risk_areas_analysis(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_top_risk_areas_analysis}} - Top risk areas explanation."""
    top_domains = get_faira_top_domains(report_data)
    deployment_context = get_faira_form_value(report_data, 'A4_3')
    domain_scores = get_faira_domain_scores(report_data)
    
    domain_summary = "\n".join([f"- {k}: Risk={v.get('Risk', 0):.0f}" for k, v in domain_scores.items()])
    
    prompt = f"""Explain why the domains listed in {top_domains} represent the highest residual risk areas.

Base your explanation on domain score patterns and deployment context {deployment_context}."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_top_risks_{id(report_data)}", api_key)


# -----------------------------------------------------------------------------
# Section 4: Controls Overview and Domain Controls Rationale
# -----------------------------------------------------------------------------

async def generate_faira_controls_overview(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_controls_overview}} - Controls overview."""
    top_domains = get_faira_top_domains(report_data)
    overall_risk = report_data.get('overall_risk_score', 50)
    
    prompt = f"""Provide a high-level overview of the control approach used in this assessment.

Base the overview ONLY on:
- Top risk domains: {top_domains}
- Overall risk score: {overall_risk}

Explain the balance between existing controls and recommended enhancements."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_controls_overview_{id(report_data)}", api_key)


async def generate_faira_domain_b1_controls_rationale(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b1_controls_rationale}} - Accountability controls rationale."""
    system_name = get_faira_form_value(report_data, 'A1_2', report_data.get('system_name', 'the AI system'))
    domain_scores = get_faira_domain_scores(report_data)
    acc = domain_scores.get('Accountability', {})
    controls = get_faira_recommended_controls(report_data, 'Accountability')
    
    prompt = f"""Using the FAIRA results and control content provided for {system_name}, write a short rationale explaining why the recommended controls for the Accountability domain have been selected.

Use ONLY:
- Residual risk: {acc.get('Risk', 0)}
- Inherent risk: {acc.get('Inherent_Risk', 0)}
- Control effectiveness: {acc.get('Control_Effectiveness', 0)}
- Recommended controls (Accountability): {controls}

Explain:
- What risk drivers these controls are intended to reduce (in governance/oversight terms)
- Whether the emphasis is on strengthening existing arrangements versus addressing gaps
- How these controls support clearer accountability and oversight without implying deficiencies

Do NOT restate the controls verbatim. Do NOT recommend additional controls.
Limit to one short paragraph."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_b1_controls_{id(report_data)}", api_key)


async def generate_faira_domain_b2_controls_rationale(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b2_controls_rationale}} - Contestability controls rationale."""
    system_name = get_faira_form_value(report_data, 'A1_2', report_data.get('system_name', 'the AI system'))
    domain_scores = get_faira_domain_scores(report_data)
    cont = domain_scores.get('Contestability', {})
    controls = get_faira_recommended_controls(report_data, 'Contestability')
    
    prompt = f"""Using the FAIRA results and control content provided for {system_name}, write a short rationale explaining why the recommended controls for the Contestability domain have been selected.

Use ONLY:
- Residual risk: {cont.get('Risk', 0)}
- Inherent risk: {cont.get('Inherent_Risk', 0)}
- Control effectiveness: {cont.get('Control_Effectiveness', 0)}
- Recommended controls (Contestability): {controls}

Explain:
- How the recommended controls address the ability to review, challenge, or escalate AI-supported outcomes
- Whether the controls primarily strengthen process, governance, or user-facing mechanisms
- How the controls reduce residual risk without assuming contested outcomes have occurred

Do NOT restate the controls verbatim. Do NOT prescribe appeal models or policy changes.
Limit to one short paragraph."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_b2_controls_{id(report_data)}", api_key)


async def generate_faira_domain_b3_controls_rationale(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b3_controls_rationale}} - Fairness controls rationale."""
    system_name = get_faira_form_value(report_data, 'A1_2', report_data.get('system_name', 'the AI system'))
    domain_scores = get_faira_domain_scores(report_data)
    fair = domain_scores.get('Fairness', {})
    controls = get_faira_recommended_controls(report_data, 'Fairness')
    data_types = get_faira_form_value(report_data, 'A2_2')
    sensitive_data = get_faira_form_value(report_data, 'A2_5')
    
    prompt = f"""Using the FAIRA results and control content provided for {system_name}, write a short rationale explaining why the recommended controls for the Fairness domain have been selected.

Use ONLY:
- Residual risk: {fair.get('Risk', 0)}
- Inherent risk: {fair.get('Inherent_Risk', 0)}
- Control effectiveness: {fair.get('Control_Effectiveness', 0)}
- Recommended controls (Fairness): {controls}
- Data characteristics summary: {data_types} and {sensitive_data}

Explain:
- What potential sources of fairness-related risk are being addressed (data, use context, decision impacts)
- How the recommended controls help detect or prevent unfair outcomes without asserting bias exists
- Whether the focus is on strengthening governance, monitoring, or assurance practices

Do NOT restate the controls verbatim. Do NOT claim discrimination or bias has occurred.
Limit to one short paragraph."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_b3_controls_{id(report_data)}", api_key)


async def generate_faira_domain_b4_controls_rationale(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b4_controls_rationale}} - Wellbeing controls rationale."""
    system_name = get_faira_form_value(report_data, 'A1_2', report_data.get('system_name', 'the AI system'))
    domain_scores = get_faira_domain_scores(report_data)
    well = domain_scores.get('Wellbeing', {})
    controls = get_faira_recommended_controls(report_data, 'Wellbeing')
    impact_scale = get_faira_form_value(report_data, 'A5_1')
    impact_severity = get_faira_form_value(report_data, 'A5_2')
    operational_env = get_faira_form_value(report_data, 'A4_3')
    third_party = get_faira_form_value(report_data, 'A4_5')
    
    prompt = f"""Using the FAIRA results and control content provided for {system_name}, write a short rationale explaining why the recommended controls for the Human, Societal & Environmental Wellbeing domain have been selected.

Use ONLY:
- Residual risk: {well.get('Risk', 0)}
- Inherent risk: {well.get('Inherent_Risk', 0)}
- Control effectiveness: {well.get('Control_Effectiveness', 0)}
- Recommended controls (Wellbeing): {controls}
- Impact context: {impact_scale} and {impact_severity}
- Deployment context: {operational_env} and {third_party}

Explain:
- What types of downstream or broader impacts the controls are intended to manage (in contextual terms)
- How the controls support monitoring, oversight, or safeguards proportional to context
- Whether the emphasis is on strengthening existing assurance versus introducing new mitigations

Do NOT restate the controls verbatim. Do NOT imply harm has occurred.
Limit to one short paragraph."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_b4_controls_{id(report_data)}", api_key)


async def generate_faira_domain_b5_controls_rationale(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b5_controls_rationale}} - Human-Centred Values controls rationale."""
    system_name = get_faira_form_value(report_data, 'A1_2', report_data.get('system_name', 'the AI system'))
    domain_scores = get_faira_domain_scores(report_data)
    vals = domain_scores.get('Values', {})
    controls = get_faira_recommended_controls(report_data, 'Values')
    user_groups = get_faira_form_value(report_data, 'A3_1')
    stakeholders = get_faira_form_value(report_data, 'A3_5')
    user_expertise = get_faira_form_value(report_data, 'A3_3')
    
    prompt = f"""Using the FAIRA results and control content provided for {system_name}, write a short rationale explaining why the recommended controls for the Human-Centred Values domain have been selected.

Use ONLY:
- Residual risk: {vals.get('Risk', 0)}
- Inherent risk: {vals.get('Inherent_Risk', 0)}
- Control effectiveness: {vals.get('Control_Effectiveness', 0)}
- Recommended controls (Human-Centred Values): {controls}
- Users and stakeholders: {user_groups} and {stakeholders}
- User expertise: {user_expertise}

Explain:
- How the controls support respectful, inclusive, and human-centred use in practice
- How user capability and stakeholder impacts shape the need for these controls
- Whether the controls strengthen governance/process or improve safeguards around use

Do NOT restate the controls verbatim. Do NOT assess user behaviour or organisational intent.
Limit to one short paragraph."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_b5_controls_{id(report_data)}", api_key)


async def generate_faira_domain_b6_controls_rationale(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b6_controls_rationale}} - Privacy controls rationale."""
    system_name = get_faira_form_value(report_data, 'A1_2', report_data.get('system_name', 'the AI system'))
    domain_scores = get_faira_domain_scores(report_data)
    priv = domain_scores.get('Privacy', {})
    controls = get_faira_recommended_controls(report_data, 'Privacy')
    data_sources = get_faira_form_value(report_data, 'A2_1')
    data_types = get_faira_form_value(report_data, 'A2_2')
    sensitive_data = get_faira_form_value(report_data, 'A2_5')
    storage = get_faira_form_value(report_data, 'A2_7')
    access = get_faira_form_value(report_data, 'A2_8')
    
    prompt = f"""Using the FAIRA results and control content provided for {system_name}, write a short rationale explaining why the recommended controls for the Privacy Protection & Security domain have been selected.

Use ONLY:
- Residual risk: {priv.get('Risk', 0)}
- Inherent risk: {priv.get('Inherent_Risk', 0)}
- Control effectiveness: {priv.get('Control_Effectiveness', 0)}
- Recommended controls (Privacy & Security): {controls}
- Data sources/types: {data_sources} and {data_types}
- Sensitive/regulated data indicator: {sensitive_data}
- Storage/retention/access context: {storage} and {access}

Explain:
- How the recommended controls address privacy/security risk drivers implied by the data characteristics
- Whether recommendations emphasise strengthening governance, assurance, or technical safeguards (at a high level)
- How the controls reduce residual risk without making compliance claims

Do NOT restate the controls verbatim. Do NOT state or imply legislative compliance/non-compliance.
Limit to one short paragraph."""

    return await call_llm(prompt, FAIRA_GLOBAL_GUARDRAILS, f"faira_b6_controls_{id(report_data)}", api_key)


async def generate_faira_domain_b7_controls_rationale(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b7_controls_rationale}} - Reliability controls rationale."""
    system_name = get_faira_form_value(report_data, 'A1_2', report_data.get('system_name', 'the AI system'))
    domain_scores = get_faira_domain_scores(report_data)
    rel = domain_scores.get('Reliability', {})
    controls = get_faira_recommended_controls(report_data, 'Reliability')
    operational_env = get_faira_form_value(report_data, 'A4_3')
    integration = get_faira_form_value(report_data, 'A4_4')
    consequences = get_faira_form_value(report_data, 'A5_2')
    
    system_prompt = "You are explaining control rationale for Reliability domain. Use British English. Limit to one short paragraph."
    
    prompt = f"""Using the FAIRA results and control content provided for {system_name}, write a short rationale explaining why the recommended controls for the Reliability & Safety domain have been selected.

Use ONLY:
- Residual risk: {rel.get('Risk', 0)}
- Inherent risk: {rel.get('Inherent_Risk', 0)}
- Control effectiveness: {rel.get('Control_Effectiveness', 0)}
- Recommended controls (Reliability & Safety): {controls}
- Deployment/use context: {operational_env} and {integration}
- Potential consequences context: {consequences}

Explain:
- How the recommended controls relate to performance consistency, error handling, monitoring, and safe use
- Whether controls focus on strengthening assurance/monitoring versus operational safeguards
- How the controls reduce residual risk without implying defects or unsafe operation

Do NOT restate the controls verbatim. Do NOT recommend specific engineering techniques.
Limit to one short paragraph."""

    return await call_llm(prompt, system_prompt, f"faira_b7_controls_{id(report_data)}", api_key)


async def generate_faira_domain_b8_controls_rationale(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_domain_b8_controls_rationale}} - Transparency controls rationale."""
    system_name = get_faira_form_value(report_data, 'A1_2', report_data.get('system_name', 'the AI system'))
    domain_scores = get_faira_domain_scores(report_data)
    trans = domain_scores.get('Transparency', {})
    controls = get_faira_recommended_controls(report_data, 'Transparency')
    user_groups = get_faira_form_value(report_data, 'A3_1')
    user_expertise = get_faira_form_value(report_data, 'A3_3')
    output_comms = get_faira_form_value(report_data, 'A3_4')
    
    system_prompt = "You are explaining control rationale for Transparency domain. Use British English. Limit to one short paragraph."
    
    prompt = f"""Using the FAIRA results and control content provided for {system_name}, write a short rationale explaining why the recommended controls for the Transparency & Explainability domain have been selected.

Use ONLY:
- Residual risk: {trans.get('Risk', 0)}
- Inherent risk: {trans.get('Inherent_Risk', 0)}
- Control effectiveness: {trans.get('Control_Effectiveness', 0)}
- Recommended controls (Transparency & Explainability): {controls}
- User groups and expertise: {user_groups} and {user_expertise}
- How outputs are communicated: {output_comms}

Explain:
- How the recommended controls improve understanding of AI outputs and limitations in context
- Whether emphasis is on documentation, communication, user enablement, or governance assurance (high level)
- How the controls reduce residual risk without drifting into contestability or prescribing techniques

Do NOT restate the controls verbatim. Do NOT recommend specific explainability methods.
Limit to one short paragraph."""

    return await call_llm(prompt, system_prompt, f"faira_b8_controls_{id(report_data)}", api_key)


# -----------------------------------------------------------------------------
# Section 5: Summary and Next Steps Narratives
# -----------------------------------------------------------------------------

async def generate_faira_gap_and_next_steps_summary(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_gap_and_next_steps_summary}} - Gap and next steps summary."""
    existing_controls = report_data.get('existing_controls_summary', 'Not specified')
    identified_gaps = report_data.get('identified_gaps', 'Not specified')
    top_domains = get_faira_top_domains(report_data)
    
    system_prompt = "You are summarising gaps and next steps for a FAIRA assessment. Use British English."
    
    prompt = f"""Summarise patterns across:
- Existing controls: {existing_controls}
- Identified gaps: {identified_gaps}
- Top risk domains: {top_domains}

Explain how these patterns inform high-level next-step considerations without prescribing actions."""

    return await call_llm(prompt, system_prompt, f"faira_gaps_{id(report_data)}", api_key)


async def generate_faira_governance_assurance_posture(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_governance_assurance_posture}} - Governance posture interpretation."""
    governance_indicators = report_data.get('governance_maturity_indicators', report_data.get('governance_score', 'Not specified'))
    assurance_mechanisms = report_data.get('assurance_mechanisms', report_data.get('assurance_readiness', 'Not specified'))
    overall_risk_level = report_data.get('overall_risk_level', 'Medium')
    
    system_prompt = "You are interpreting governance posture for a FAIRA assessment. Use British English."
    
    prompt = f"""Interpret the overall governance and assurance posture using:
- Governance maturity indicators: {governance_indicators}
- Assurance mechanisms: {assurance_mechanisms}
- Overall risk level: {overall_risk_level}

Explain how these arrangements support ongoing oversight."""

    return await call_llm(prompt, system_prompt, f"faira_governance_{id(report_data)}", api_key)


async def generate_faira_decision_next_steps_summary(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_decision_next_steps_summary}} - Decision considerations summary."""
    overall_risk_level = report_data.get('overall_risk_level', 'Medium')
    risk_acceptance = report_data.get('risk_acceptance_context', 'Standard organisational risk tolerance')
    top_domains = get_faira_top_domains(report_data)
    
    system_prompt = "You are summarising decision considerations for a FAIRA assessment. Use British English."
    
    prompt = f"""Summarise decision considerations based on:
- Overall risk level: {overall_risk_level}
- Risk acceptance context: {risk_acceptance}
- Top risk domains: {top_domains}

Frame considerations without recommending specific actions."""

    return await call_llm(prompt, system_prompt, f"faira_decisions_{id(report_data)}", api_key)


async def generate_faira_supporting_artefacts_summary(report_data: Dict[str, Any], api_key: str) -> str:
    """Generate {{ai.f_supporting_artefacts_summary}} - Supporting artefacts summary."""
    artefacts = report_data.get('supporting_artefacts', report_data.get('evidence_summary', 'Not specified'))
    
    system_prompt = "You are summarising supporting artefacts for a FAIRA assessment. Use British English."
    
    prompt = f"""Provide a brief summary of supporting artefacts: {artefacts}

Describe artefact types and coverage without assessing adequacy or completeness."""

    return await call_llm(prompt, system_prompt, f"faira_artefacts_{id(report_data)}", api_key)


# -----------------------------------------------------------------------------
# FAIRA Narrative Generation Orchestrator
# -----------------------------------------------------------------------------

async def generate_faira_narratives(
    report_data: Dict[str, Any],
    assessment: Dict[str, Any],
    db,
    api_key: str
) -> Dict[str, str]:
    """
    Generate all 32 AI narratives for FAIRA assessments.
    
    Returns a dictionary with keys matching the template placeholders:
    - f_executive_snapshot
    - f_risk_profile_interpretation
    - f_methodology_interpretation
    - f_system_overview_notes
    - f_data_context_notes
    - f_user_stakeholder_context_notes
    - f_deployment_context_notes
    - f_impact_context_notes
    - f_domain_analysis
    - f_domain_b1_analysis through f_domain_b8_analysis
    - f_top_risk_areas_analysis
    - f_controls_overview
    - f_domain_b1_controls_rationale through f_domain_b8_controls_rationale
    - f_gap_and_next_steps_summary
    - f_governance_assurance_posture
    - f_decision_next_steps_summary
    - f_supporting_artefacts_summary
    """
    narratives = {}
    assessment_id = assessment.get('id')
    cached_narratives = assessment.get('ai_narratives', {})
    
    # All 32 FAIRA narrative generators
    generators = [
        # Section 1: Executive and Overview
        ('f_executive_snapshot', generate_faira_executive_snapshot),
        ('f_risk_profile_interpretation', generate_faira_risk_profile_interpretation),
        ('f_methodology_interpretation', generate_faira_methodology_interpretation),
        
        # Section 2: Context Notes (Part A)
        ('f_system_overview_notes', generate_faira_system_overview_notes),
        ('f_data_context_notes', generate_faira_data_context_notes),
        ('f_user_stakeholder_context_notes', generate_faira_user_stakeholder_notes),
        ('f_deployment_context_notes', generate_faira_deployment_context_notes),
        ('f_impact_context_notes', generate_faira_impact_context_notes),
        
        # Section 3: Domain Analysis (Part B)
        ('f_domain_analysis', generate_faira_domain_analysis),
        ('f_domain_b1_analysis', generate_faira_domain_b1_analysis),
        ('f_domain_b2_analysis', generate_faira_domain_b2_analysis),
        ('f_domain_b3_analysis', generate_faira_domain_b3_analysis),
        ('f_domain_b4_analysis', generate_faira_domain_b4_analysis),
        ('f_domain_b5_analysis', generate_faira_domain_b5_analysis),
        ('f_domain_b6_analysis', generate_faira_domain_b6_analysis),
        ('f_domain_b7_analysis', generate_faira_domain_b7_analysis),
        ('f_domain_b8_analysis', generate_faira_domain_b8_analysis),
        ('f_top_risk_areas_analysis', generate_faira_top_risk_areas_analysis),
        
        # Section 4: Controls
        ('f_controls_overview', generate_faira_controls_overview),
        ('f_domain_b1_controls_rationale', generate_faira_domain_b1_controls_rationale),
        ('f_domain_b2_controls_rationale', generate_faira_domain_b2_controls_rationale),
        ('f_domain_b3_controls_rationale', generate_faira_domain_b3_controls_rationale),
        ('f_domain_b4_controls_rationale', generate_faira_domain_b4_controls_rationale),
        ('f_domain_b5_controls_rationale', generate_faira_domain_b5_controls_rationale),
        ('f_domain_b6_controls_rationale', generate_faira_domain_b6_controls_rationale),
        ('f_domain_b7_controls_rationale', generate_faira_domain_b7_controls_rationale),
        ('f_domain_b8_controls_rationale', generate_faira_domain_b8_controls_rationale),
        
        # Section 5: Summary and Next Steps
        ('f_gap_and_next_steps_summary', generate_faira_gap_and_next_steps_summary),
        ('f_governance_assurance_posture', generate_faira_governance_assurance_posture),
        ('f_decision_next_steps_summary', generate_faira_decision_next_steps_summary),
        ('f_supporting_artefacts_summary', generate_faira_supporting_artefacts_summary),
    ]
    
    for key, generator in generators:
        if cached_narratives.get(key):
            narratives[key] = cached_narratives[key]
            print(f"DEBUG: Using cached AI {key} narrative (FAIRA)")
        else:
            try:
                narratives[key] = await generator(report_data, api_key)
                print(f"DEBUG: Generated new AI {key} narrative (FAIRA) ({len(narratives[key])} chars)")
            except Exception as e:
                print(f"ERROR generating AI {key} (FAIRA): {e}")
                narratives[key] = ""
    
    # Cache to database
    if db is not None and assessment_id and narratives:
        try:
            await db.assessments.update_one(
                {'id': assessment_id},
                {'$set': {'ai_narratives': {**cached_narratives, **narratives}}}
            )
            print("DEBUG: Cached AI narratives to database (FAIRA)")
        except Exception as e:
            print(f"WARNING: Failed to cache AI narratives: {e}")
    
    return narratives

