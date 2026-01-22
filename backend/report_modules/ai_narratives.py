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
            print(f"DEBUG: Cached AI narratives to database (Awareness)")
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
            print(f"DEBUG: Cached AI narratives to database (Readiness)")
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
            print(f"DEBUG: Cached AI narratives to database (Orgwide)")
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
            print(f"DEBUG: Cached AI narratives to database (System)")
        except Exception as e:
            print(f"WARNING: Failed to cache AI narratives: {e}")
    
    return narratives
