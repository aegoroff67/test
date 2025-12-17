"""
FAIRA Risk Assessment Scoring Engine

Comprehensive scoring methodology for calculating:
- Total Impact, Likelihood, Control Effectiveness
- Overall Risk (Raw and Normalized)
- Domain-level scores for radar charts
- Key derived indicators
- Assurance readiness indicators
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# Load scoring schema
SCHEMA_PATH = Path(__file__).parent / "faira_scoring_schema.json"

def load_scoring_schema() -> Dict:
    """Load the FAIRA scoring schema from JSON file"""
    try:
        with open(SCHEMA_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load scoring schema: {e}")
        return {"questions": {}}


# ============================================================================
# CONSTANTS
# ============================================================================

# Domain mapping between schema domains and radar chart domains
DOMAIN_MAPPING = {
    "Reliability and Safety": "Reliability",
    "Accountability": "Accountability",
    "Transparency and Explainability": "Transparency",
    "Fairness": "Fairness",
    "Human, Societal and Environmental Wellbeing": "Wellbeing",
    "Human-centred Values": "Values",
    "Privacy Protection and Security": "Privacy",
    "Contestability": "Contestability",
}

# All 8 radar chart domains with full names (matching Part B sections)
FAIRA_DOMAINS = [
    {"id": "B1", "shortLabel": "Wellbeing", "fullName": "Human, Societal and Environmental Wellbeing"},
    {"id": "B2", "shortLabel": "Values", "fullName": "Human-Centred Values"},
    {"id": "B3", "shortLabel": "Fairness", "fullName": "Fairness"},
    {"id": "B4", "shortLabel": "Privacy", "fullName": "Privacy Protection and Security"},
    {"id": "B5", "shortLabel": "Reliability", "fullName": "Reliability and Safety"},
    {"id": "B6", "shortLabel": "Transparency", "fullName": "Transparency and Explainability"},
    {"id": "B7", "shortLabel": "Contestability", "fullName": "Contestability"},
    {"id": "B8", "shortLabel": "Accountability", "fullName": "Accountability"},
]

# Baseline Control Effectiveness (prevents division instability)
BASELINE_CE = 5.0

# Domain CE Target for normalization (used in Domain_CE_Display calculation)
DOMAIN_CE_TARGET = 25.0

# Normalization constant for risk score
MAX_EXPECTED_RAW_RISK = 120.0

# Risk Rating Bands
RISK_BANDS = {
    "Very Low": (0, 20),
    "Low": (20, 35),
    "Medium": (35, 55),
    "High": (55, 75),
    "Very High": (75, 100),
}

# Governance thresholds for assurance readiness
GOVERNANCE_THRESHOLD_HIGH = 15
GOVERNANCE_THRESHOLD_MED = 8

# Target CE for control coverage calculation
TARGET_CE = 20.0


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def normalize_field_name(field_name: str) -> str:
    """Convert field names like 'a1_1' or 'A1.1' to schema format 'A1_1'"""
    normalized = field_name.upper().replace('.', '_').replace('-', '_')
    return normalized


def get_form_value(form_data: Dict, field_name: str) -> Any:
    """Get a value from form data, trying various field name formats"""
    if field_name in form_data:
        return form_data[field_name]
    
    lower_field = field_name.lower()
    if lower_field in form_data:
        return form_data[lower_field]
    
    dot_field = field_name.replace('_', '.')
    if dot_field in form_data:
        return form_data[dot_field]
    
    dot_field_lower = dot_field.lower()
    if dot_field_lower in form_data:
        return form_data[dot_field_lower]
    
    return None


def get_risk_rating(score: float) -> str:
    """Get risk rating label based on normalized score"""
    if score < 20:
        return "Very Low"
    elif score < 35:
        return "Low"
    elif score < 55:
        return "Medium"
    elif score < 75:
        return "High"
    else:
        return "Very High"


# ============================================================================
# SPECIAL FACTOR CALCULATIONS
# ============================================================================

def calculate_autonomy_factor(form_data: Dict) -> float:
    """
    AutonomyFactor from A1.6
    Higher autonomy = higher likelihood of risk
    """
    a1_6 = get_form_value(form_data, 'A1_6')
    a1_6_actions = get_form_value(form_data, 'A1_6_actions') or []
    
    factor = 0.0
    
    if a1_6 == 'Yes':
        # Base factor for having autonomous capabilities
        factor += 2.0
        
        # Additional factors based on specific actions
        high_risk_actions = [
            'Initiates actions without approval',
            'Modifies own parameters',
            'Operates outside normal hours unsupervised',
            'Accesses external systems autonomously'
        ]
        
        for action in a1_6_actions:
            if action in high_risk_actions:
                factor += 1.0
            else:
                factor += 0.5
    
    return factor


def calculate_data_quality_factor(form_data: Dict) -> float:
    """
    DataQualityFactor from A2.5
    Lower data quality = higher likelihood
    Formula: DataQualityFactor = 6 - average_rating
    """
    # A2.5 is typically a rating scale 1-5 for data quality dimensions
    quality_fields = ['A2_5', 'A2_5_completeness', 'A2_5_accuracy', 'A2_5_timeliness', 'A2_5_consistency']
    
    total = 0.0
    count = 0
    
    for field in quality_fields:
        value = get_form_value(form_data, field)
        if value is not None:
            try:
                total += float(value)
                count += 1
            except (ValueError, TypeError):
                pass
    
    if count > 0:
        avg_quality = total / count
        # Lower quality = higher factor (inverse relationship)
        return max(0, 6 - avg_quality)
    
    return 2.5  # Default middle value


def calculate_expertise_factor(form_data: Dict) -> float:
    """
    ExpertiseFactor from A3.2
    Lower user expertise = higher likelihood of misuse/errors
    """
    a3_2 = get_form_value(form_data, 'A3_2')
    
    # Map expertise levels to factors
    expertise_factors = {
        'Expert/Specialist': 0.0,
        'Trained Professional': 1.0,
        'General Staff': 2.0,
        'Public/End Users': 3.0,
        'Vulnerable Groups': 4.0,
    }
    
    if isinstance(a3_2, list):
        # If multiple user types, use the highest factor (lowest expertise)
        max_factor = 0.0
        for user_type in a3_2:
            factor = expertise_factors.get(user_type, 2.0)
            max_factor = max(max_factor, factor)
        return max_factor
    elif a3_2 in expertise_factors:
        return expertise_factors[a3_2]
    
    return 2.0  # Default middle value


# ============================================================================
# KEY DERIVED INDICATORS
# ============================================================================

def calculate_autonomy_indicator(form_data: Dict) -> Dict[str, Any]:
    """
    Autonomy_Level = IF AutonomyFactor >= 3 THEN "High Autonomy" ELSE "Human-in-the-loop"
    """
    factor = calculate_autonomy_factor(form_data)
    return {
        "factor": factor,
        "level": "High Autonomy" if factor >= 3 else "Human-in-the-loop",
        "is_high": factor >= 3
    }


def calculate_sensitive_data_indicator(form_data: Dict) -> Dict[str, Any]:
    """
    Sensitive_Data_Flag = TRUE if A2.7 = Yes
    """
    a2_7 = get_form_value(form_data, 'A2_7')
    return {
        "has_sensitive_data": a2_7 == 'Yes',
        "data_types": get_form_value(form_data, 'A2_7_data_types') or []
    }


def calculate_high_risk_context_indicator(form_data: Dict) -> Dict[str, Any]:
    """
    High_Risk_Context = TRUE if B5.3 environments include high-risk areas
    """
    b5_3_environments = get_form_value(form_data, 'B5_3_environments') or []
    
    high_risk_environments = [
        'Democratic processes',
        'Critical infrastructure',
        'Law enforcement',
        'Health services',
        'Education',
        'Employment',
        'Financial services',
        'Immigration/border control'
    ]
    
    detected_high_risk = [env for env in b5_3_environments if env in high_risk_environments]
    
    return {
        "is_high_risk": len(detected_high_risk) > 0,
        "high_risk_contexts": detected_high_risk,
        "all_contexts": b5_3_environments
    }


def calculate_governance_score(form_data: Dict, schema: Dict) -> Dict[str, Any]:
    """
    Governance_Score = Σ(CE from A5.x and B8.x questions)
    """
    questions = schema.get("questions", {})
    governance_score = 0.0
    
    # Sum CE modifiers from A5.x and B8.x questions
    for question_id, question_config in questions.items():
        if question_id.startswith('A5_') or question_id.startswith('B8_'):
            scoring = question_config.get("scoring", {})
            form_value = get_form_value(form_data, question_id)
            
            if form_value and "options" in scoring:
                option_key = str(form_value)
                if option_key in scoring["options"]:
                    ce_value = scoring["options"][option_key].get("Control_Effectiveness", 0)
                    governance_score += ce_value
    
    # Determine assurance readiness level
    if governance_score >= GOVERNANCE_THRESHOLD_HIGH:
        readiness_level = "Strong"
    elif governance_score >= GOVERNANCE_THRESHOLD_MED:
        readiness_level = "Moderate"
    else:
        readiness_level = "Weak"
    
    return {
        "score": governance_score,
        "readiness_level": readiness_level
    }


# ============================================================================
# QUESTION SCORING
# ============================================================================

def calculate_question_scores(
    question_config: Dict,
    form_data: Dict
) -> Dict[str, Dict[str, float]]:
    """Calculate Impact, Likelihood, and CE modifiers for a single question."""
    result = {}
    
    if not question_config.get("scoring"):
        return result
    
    question_id = question_config.get("id", "")
    question_type = question_config.get("type", "")
    scoring = question_config.get("scoring", {})
    domains = question_config.get("domains", [])
    
    form_value = get_form_value(form_data, question_id)
    
    if form_value is None:
        return result
    
    # Initialize result for each domain
    for schema_domain in domains:
        radar_domain = DOMAIN_MAPPING.get(schema_domain)
        if radar_domain and radar_domain not in result:
            result[radar_domain] = {"Impact": 0, "Likelihood": 0, "Control_Effectiveness": 0}
    
    # Handle different question types
    if question_type == "multiselect":
        _process_multiselect(scoring, form_value, domains, result)
    elif question_type == "single_select":
        _process_single_select(scoring, form_value, domains, result)
    elif question_type in ["yes_no", "yes_no_with_text"]:
        _process_yes_no(scoring, form_value, domains, result)
    elif question_type == "yes_no_with_options":
        _process_yes_no_with_options(scoring, form_value, form_data, question_id, domains, result)
    elif question_type == "rating_scale":
        _process_rating_scale(scoring, form_value, domains, result)
    elif question_type == "multiselect_with_rating":
        _process_multiselect_with_rating(scoring, form_value, form_data, question_id, domains, result)
    elif question_type == "yes_no_with_subsections":
        _process_yes_no_with_subsections(scoring, form_value, form_data, question_id, domains, result)
    elif question_type == "yes_no_with_rating":
        _process_yes_no_with_rating(scoring, form_value, form_data, question_id, domains, result)
    elif question_type == "yes_unknown_no_with_options":
        _process_yes_unknown_no_with_options(scoring, form_value, form_data, question_id, domains, result)
    
    return result


def _process_multiselect(scoring: Dict, form_value: Any, domains: List[str], result: Dict):
    """Process multiselect question type"""
    options = scoring.get("options", {})
    selected = form_value if isinstance(form_value, list) else [form_value]
    
    for option in selected:
        if option in options:
            option_scores = options[option]
            for schema_domain in domains:
                radar_domain = DOMAIN_MAPPING.get(schema_domain)
                if radar_domain and radar_domain in result:
                    for metric, value in option_scores.items():
                        if metric in result[radar_domain]:
                            result[radar_domain][metric] += value


def _process_single_select(scoring: Dict, form_value: Any, domains: List[str], result: Dict):
    """Process single select question type"""
    options = scoring.get("options", {})
    
    if form_value in options:
        option_scores = options[form_value]
        for schema_domain in domains:
            radar_domain = DOMAIN_MAPPING.get(schema_domain)
            if radar_domain and radar_domain in result:
                for metric, value in option_scores.items():
                    if metric in result[radar_domain]:
                        result[radar_domain][metric] += value


def _process_yes_no(scoring: Dict, form_value: Any, domains: List[str], result: Dict):
    """Process yes/no question type"""
    options = scoring.get("options", {})
    answer = "Yes" if str(form_value).lower() in ["yes", "true", "1"] else "No"
    
    if answer in options:
        option_scores = options[answer]
        for schema_domain in domains:
            radar_domain = DOMAIN_MAPPING.get(schema_domain)
            if radar_domain and radar_domain in result:
                for metric, value in option_scores.items():
                    if metric in result[radar_domain]:
                        result[radar_domain][metric] += value


def _process_yes_no_with_options(scoring: Dict, form_value: Any, form_data: Dict, 
                                  question_id: str, domains: List[str], result: Dict):
    """Process yes/no with sub-options question type"""
    options = scoring.get("options", {})
    answer = "Yes" if str(form_value).lower() in ["yes", "true", "1"] else "No"
    
    if answer in options:
        option_config = options[answer]
        
        for schema_domain in domains:
            radar_domain = DOMAIN_MAPPING.get(schema_domain)
            if radar_domain and radar_domain in result:
                for metric in ["Impact", "Likelihood", "Control_Effectiveness"]:
                    if metric in option_config:
                        result[radar_domain][metric] += option_config[metric]
        
        if answer == "Yes" and "actions" in option_config:
            sub_field = option_config.get("sub_question", f"{question_id}_actions")
            sub_value = get_form_value(form_data, sub_field)
            
            if sub_value:
                selected_actions = sub_value if isinstance(sub_value, list) else [sub_value]
                for action in selected_actions:
                    if action in option_config["actions"]:
                        action_scores = option_config["actions"][action]
                        for schema_domain in domains:
                            radar_domain = DOMAIN_MAPPING.get(schema_domain)
                            if radar_domain and radar_domain in result:
                                for metric, value in action_scores.items():
                                    if metric in result[radar_domain]:
                                        result[radar_domain][metric] += value


def _process_rating_scale(scoring: Dict, form_value: Any, domains: List[str], result: Dict):
    """Process rating scale question type"""
    rating_scale = scoring.get("rating_scale", {})
    rating_key = str(form_value)
    
    if rating_key in rating_scale:
        rating_scores = rating_scale[rating_key]
        for schema_domain in domains:
            radar_domain = DOMAIN_MAPPING.get(schema_domain)
            if radar_domain and radar_domain in result:
                for metric, value in rating_scores.items():
                    if metric in result[radar_domain]:
                        result[radar_domain][metric] += value


def _process_multiselect_with_rating(scoring: Dict, form_value: Any, form_data: Dict,
                                      question_id: str, domains: List[str], result: Dict):
    """Process multiselect with rating (A3.5, A3.6) - applies severity weighting"""
    severity_multiplier = 1.0
    if "part_b" in scoring:
        part_b = scoring["part_b"]
        severity_field = part_b.get("severity_field", f"{question_id}b_severity")
        severity_value = get_form_value(form_data, severity_field)
        
        if severity_value is not None:
            severity_key = str(severity_value)
            multipliers = part_b.get("severity_multiplier") or part_b.get("severity_weight", {})
            severity_multiplier = float(multipliers.get(severity_key, 1.0))
    
    if "part_a" in scoring:
        part_a = scoring["part_a"]
        sub_field = part_a.get("sub_question", f"{question_id}a_impact_types")
        sub_value = get_form_value(form_data, sub_field)
        
        if sub_value and "impact_types" in part_a:
            selected = sub_value if isinstance(sub_value, list) else [sub_value]
            for item in selected:
                if item in part_a["impact_types"]:
                    item_scores = part_a["impact_types"][item]
                    for schema_domain in domains:
                        radar_domain = DOMAIN_MAPPING.get(schema_domain)
                        if radar_domain and radar_domain in result:
                            for metric, value in item_scores.items():
                                if metric in result[radar_domain]:
                                    weighted_value = value * severity_multiplier
                                    result[radar_domain][metric] += weighted_value


def _process_yes_no_with_subsections(scoring: Dict, form_value: Any, form_data: Dict,
                                      question_id: str, domains: List[str], result: Dict):
    """Process yes/no with subsections (A5_10)"""
    options = scoring.get("options", {})
    answer = "Yes" if str(form_value).lower() in ["yes", "true", "1"] else "No"
    
    if answer in options:
        option_config = options[answer]
        
        for schema_domain in domains:
            radar_domain = DOMAIN_MAPPING.get(schema_domain)
            if radar_domain and radar_domain in result:
                for metric in ["Impact", "Likelihood", "Control_Effectiveness"]:
                    if metric in option_config:
                        result[radar_domain][metric] += option_config[metric]
        
        if answer == "Yes" and "subsections" in option_config:
            for section_name, section_config in option_config["subsections"].items():
                field = section_config.get("field", "")
                section_value = get_form_value(form_data, field)
                
                if section_value and "options" in section_config:
                    selected = section_value if isinstance(section_value, list) else [section_value]
                    for item in selected:
                        if item in section_config["options"]:
                            item_scores = section_config["options"][item]
                            for schema_domain in domains:
                                radar_domain = DOMAIN_MAPPING.get(schema_domain)
                                if radar_domain and radar_domain in result:
                                    for metric, value in item_scores.items():
                                        if metric in result[radar_domain]:
                                            result[radar_domain][metric] += value


def _process_yes_no_with_rating(scoring: Dict, form_value: Any, form_data: Dict,
                                 question_id: str, domains: List[str], result: Dict):
    """Process yes/no with rating sub-question"""
    options = scoring.get("options", {})
    answer = "Yes" if str(form_value).lower() in ["yes", "true", "1"] else "No"
    
    if answer in options:
        option_config = options[answer]
        
        for schema_domain in domains:
            radar_domain = DOMAIN_MAPPING.get(schema_domain)
            if radar_domain and radar_domain in result:
                for metric in ["Impact", "Likelihood", "Control_Effectiveness"]:
                    if metric in option_config:
                        result[radar_domain][metric] += option_config[metric]
        
        if answer == "Yes" and "rating_scale" in option_config:
            sub_field = option_config.get("sub_question", f"{question_id}_rating")
            rating_value = get_form_value(form_data, sub_field)
            
            if rating_value is not None:
                rating_key = str(rating_value)
                if rating_key in option_config["rating_scale"]:
                    rating_scores = option_config["rating_scale"][rating_key]
                    for schema_domain in domains:
                        radar_domain = DOMAIN_MAPPING.get(schema_domain)
                        if radar_domain and radar_domain in result:
                            for metric, value in rating_scores.items():
                                if metric in result[radar_domain]:
                                    result[radar_domain][metric] += value


def _process_yes_unknown_no_with_options(scoring: Dict, form_value: Any, form_data: Dict,
                                          question_id: str, domains: List[str], result: Dict):
    """Process yes/unknown/no with options"""
    options = scoring.get("options", {})
    answer = str(form_value).capitalize()
    if answer not in options:
        answer = "Unknown"
    
    if answer in options:
        option_config = options[answer]
        
        for schema_domain in domains:
            radar_domain = DOMAIN_MAPPING.get(schema_domain)
            if radar_domain and radar_domain in result:
                for metric in ["Impact", "Likelihood", "Control_Effectiveness"]:
                    if metric in option_config:
                        result[radar_domain][metric] += option_config[metric]
        
        if answer == "Yes" and "affected_groups" in option_config:
            sub_field = option_config.get("sub_question", f"{question_id}_groups")
            groups_value = get_form_value(form_data, sub_field)
            
            if groups_value:
                selected_groups = groups_value if isinstance(groups_value, list) else [groups_value]
                for group in selected_groups:
                    if group in option_config["affected_groups"]:
                        group_scores = option_config["affected_groups"][group]
                        for schema_domain in domains:
                            radar_domain = DOMAIN_MAPPING.get(schema_domain)
                            if radar_domain and radar_domain in result:
                                for metric, value in group_scores.items():
                                    if metric in result[radar_domain]:
                                        result[radar_domain][metric] += value


# ============================================================================
# MAIN CALCULATION FUNCTIONS
# ============================================================================

def calculate_totals(form_data: Dict) -> Dict[str, float]:
    """
    Calculate Total Impact, Likelihood, and Control Effectiveness.
    
    Total_Impact = Σ(Impact modifiers) + Σ(severity-weighted A3.5, A3.6)
    Total_Likelihood = Σ(Likelihood modifiers) + AutonomyFactor + DataQualityFactor + ExpertiseFactor
    Total_CE = Baseline_CE + Σ(CE modifiers)
    """
    schema = load_scoring_schema()
    questions = schema.get("questions", {})
    
    total_impact = 0.0
    total_likelihood = 0.0
    total_ce = BASELINE_CE
    
    # Process all questions
    for question_id, question_config in questions.items():
        try:
            question_scores = calculate_question_scores(question_config, form_data)
            
            for domain, scores in question_scores.items():
                total_impact += scores.get("Impact", 0)
                total_likelihood += scores.get("Likelihood", 0)
                total_ce += scores.get("Control_Effectiveness", 0)
        except Exception as e:
            logger.warning(f"Error processing question {question_id}: {e}")
    
    # Add special factors to likelihood
    autonomy_factor = calculate_autonomy_factor(form_data)
    data_quality_factor = calculate_data_quality_factor(form_data)
    expertise_factor = calculate_expertise_factor(form_data)
    
    total_likelihood += autonomy_factor + data_quality_factor + expertise_factor
    
    return {
        "total_impact": max(total_impact, 0),
        "total_likelihood": max(total_likelihood, 0),
        "total_control_effectiveness": max(total_ce, BASELINE_CE),
        "autonomy_factor": autonomy_factor,
        "data_quality_factor": data_quality_factor,
        "expertise_factor": expertise_factor
    }


def calculate_overall_risk(form_data: Dict) -> Dict[str, Any]:
    """
    Calculate overall risk score and all indicators.
    
    Raw_Risk_Score = (Total_Impact × Total_Likelihood) / Total_CE
    Normalised_Risk = min(100, (Raw_Risk_Score / Max_Expected_Raw_Risk) × 100)
    """
    schema = load_scoring_schema()
    totals = calculate_totals(form_data)
    
    # Calculate raw risk
    impact = max(totals["total_impact"], 0.1)
    likelihood = max(totals["total_likelihood"], 0.1)
    ce = max(totals["total_control_effectiveness"], 1.0)
    
    raw_risk = (impact * likelihood) / ce
    
    # Normalize to 0-100
    normalized_risk = min(100, (raw_risk / MAX_EXPECTED_RAW_RISK) * 100)
    
    # Get risk rating
    risk_rating = get_risk_rating(normalized_risk)
    
    # Calculate domain scores
    domain_scores = calculate_domain_scores(form_data)
    
    # Get top risk areas (sorted by domain risk)
    top_risk_areas = []
    for domain_info in FAIRA_DOMAINS:
        short_label = domain_info["shortLabel"]
        if short_label in domain_scores:
            risk_score = domain_scores[short_label].get("Risk", 0)
            top_risk_areas.append({
                "domain": short_label,
                "fullName": domain_info["fullName"],
                "risk_score": risk_score,
                "concern_level": get_risk_rating(risk_score)
            })
    
    top_risk_areas.sort(key=lambda x: x["risk_score"], reverse=True)
    
    # Key derived indicators
    autonomy_indicator = calculate_autonomy_indicator(form_data)
    sensitive_data_indicator = calculate_sensitive_data_indicator(form_data)
    high_risk_context = calculate_high_risk_context_indicator(form_data)
    governance = calculate_governance_score(form_data, schema)
    
    # Control coverage
    control_coverage = min((totals["total_control_effectiveness"] / TARGET_CE), 1.0) * 100
    
    return {
        # Risk scores
        "raw_risk_score": round(raw_risk, 2),
        "overall_risk_score": round(normalized_risk, 1),
        "overall_risk_level": risk_rating,
        
        # Totals
        "total_impact": round(totals["total_impact"], 1),
        "total_likelihood": round(totals["total_likelihood"], 1),
        "total_control_effectiveness": round(totals["total_control_effectiveness"], 1),
        
        # Special factors
        "autonomy_factor": round(totals["autonomy_factor"], 1),
        "data_quality_factor": round(totals["data_quality_factor"], 1),
        "expertise_factor": round(totals["expertise_factor"], 1),
        
        # Domain scores
        "domain_scores": domain_scores,
        "top_risk_areas": top_risk_areas[:3],
        
        # Key indicators
        "autonomy_indicator": autonomy_indicator,
        "sensitive_data_indicator": sensitive_data_indicator,
        "high_risk_context": high_risk_context,
        
        # Governance
        "governance_score": governance["score"],
        "assurance_readiness": governance["readiness_level"],
        
        # Control coverage
        "control_coverage_percent": round(control_coverage, 1)
    }


def calculate_domain_scores(form_data: Dict) -> Dict[str, Dict[str, float]]:
    """
    Calculate domain-level scores for radar charts.
    
    Domain_Impact(D) = Σ(Impact modifiers from questions mapped to domain D)
    Domain_Likelihood(D) = Σ(Likelihood modifiers from questions mapped to domain D)
    Domain_CE_Raw = Σ(CE modifiers mapped to domain)
    Domain_CE_Display = clamp((Domain_CE_Raw / DOMAIN_CE_TARGET) × 100, 0, 100)
    Domain_Risk(D) = (Domain_Impact × Domain_Likelihood) / Domain_CE
    """
    schema = load_scoring_schema()
    questions = schema.get("questions", {})
    
    # Initialize domain totals (no baseline for CE - just sum of modifiers)
    domain_totals = {}
    for domain_info in FAIRA_DOMAINS:
        short_label = domain_info["shortLabel"]
        domain_totals[short_label] = {
            "Impact": 0.0,
            "Likelihood": 0.0,
            "Control_Effectiveness": 0.0,  # No baseline - just raw modifiers
        }
    
    # Process each question
    for question_id, question_config in questions.items():
        try:
            question_scores = calculate_question_scores(question_config, form_data)
            
            for domain, scores in question_scores.items():
                if domain in domain_totals:
                    domain_totals[domain]["Impact"] += scores.get("Impact", 0)
                    domain_totals[domain]["Likelihood"] += scores.get("Likelihood", 0)
                    domain_totals[domain]["Control_Effectiveness"] += scores.get("Control_Effectiveness", 0)
        except Exception as e:
            logger.warning(f"Error processing question {question_id}: {e}")
    
    # Calculate Risk for each domain and normalize for display
    for domain, scores in domain_totals.items():
        impact = max(scores["Impact"], 0.1)
        likelihood = max(scores["Likelihood"], 0.1)
        
        # Store raw CE for risk calculation (use minimum of 1 to avoid division by zero)
        raw_ce = scores["Control_Effectiveness"]
        ce_for_risk = max(raw_ce, 1.0)
        
        # Raw domain risk
        raw_risk = (impact * likelihood) / ce_for_risk
        
        # Normalize risk to 0-100
        normalized_risk = min(100, (raw_risk / MAX_EXPECTED_RAW_RISK) * 100)
        
        scores["Risk"] = round(normalized_risk, 1)
        
        # Normalize Impact and Likelihood to 0-100 for display
        scores["Impact"] = max(0, min(round(scores["Impact"] * 5, 1), 100))
        scores["Likelihood"] = max(0, min(round(scores["Likelihood"] * 5, 1), 100))
        
        # Domain CE Display = clamp((Domain_CE_Raw / DOMAIN_CE_TARGET) × 100, 0, 100)
        domain_ce_display = (raw_ce / DOMAIN_CE_TARGET) * 100
        scores["Control_Effectiveness"] = max(0, min(round(domain_ce_display, 1), 100))
    
    return domain_totals


def get_radar_chart_data(form_data: Dict) -> Dict[str, List[Dict]]:
    """
    Get formatted radar chart data for all 4 charts.
    """
    domain_scores = calculate_domain_scores(form_data)
    
    result = {
        "domainImpact": [],
        "domainLikelihood": [],
        "domainControlEffectiveness": [],
        "domainRisk": []
    }
    
    for domain_info in FAIRA_DOMAINS:
        short_label = domain_info["shortLabel"]
        full_name = domain_info["fullName"]
        scores = domain_scores.get(short_label, {})
        
        result["domainImpact"].append({
            "domain": short_label,
            "fullName": full_name,
            "score": scores.get("Impact", 0),
            "fullMark": 100
        })
        
        result["domainLikelihood"].append({
            "domain": short_label,
            "fullName": full_name,
            "score": scores.get("Likelihood", 0),
            "fullMark": 100
        })
        
        result["domainControlEffectiveness"].append({
            "domain": short_label,
            "fullName": full_name,
            "score": scores.get("Control_Effectiveness", 0),
            "fullMark": 100
        })
        
        result["domainRisk"].append({
            "domain": short_label,
            "fullName": full_name,
            "score": scores.get("Risk", 0),
            "fullMark": 100
        })
    
    return result
