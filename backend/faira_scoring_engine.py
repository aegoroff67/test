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
import re
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
MAX_EXPECTED_RAW_RISK = 700.0

# Domain normalization factors (theoretical maximums from schema analysis)
DOMAIN_NORMALIZATION = {
    "Accountability": {"maxImpact": 122.00, "maxLikelihood": 86.75, "maxCE": 95.50},
    "Contestability": {"maxImpact": 34.00, "maxLikelihood": 35.75, "maxCE": 71.25},
    "Fairness": {"maxImpact": 133.00, "maxLikelihood": 22.00, "maxCE": 23.50},
    "Human, Societal and Environmental Wellbeing": {"maxImpact": 116.00, "maxLikelihood": 18.50, "maxCE": 18.00},
    "Human-centred Values": {"maxImpact": 35.00, "maxLikelihood": 13.00, "maxCE": 25.00},
    "Privacy Protection and Security": {"maxImpact": 170.00, "maxLikelihood": 100.50, "maxCE": 62.50},
    "Reliability and Safety": {"maxImpact": 112.00, "maxLikelihood": 125.50, "maxCE": 59.00},
    "Transparency and Explainability": {"maxImpact": 62.00, "maxLikelihood": 57.50, "maxCE": 102.85},
}

# Map short labels to full domain names for normalization lookup
DOMAIN_SHORT_TO_FULL = {
    "Accountability": "Accountability",
    "Contestability": "Contestability", 
    "Fairness": "Fairness",
    "Wellbeing": "Human, Societal and Environmental Wellbeing",
    "Values": "Human-centred Values",
    "Privacy": "Privacy Protection and Security",
    "Reliability": "Reliability and Safety",
    "Transparency": "Transparency and Explainability",
}

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
    Normalised_Risk = min(100, (Raw_Risk_Score / MAX_EXPECTED_RAW_RISK) × 100)
    
    Also calculates normalized indices (0-100) for display purposes.
    """
    # Overall schema maximums (for normalized indices)
    # These should match the sum of all domain maximums from DOMAIN_NORMALIZATION
    MAX_TOTAL_IMPACT = 784.0   # Sum of all domain maxImpact values
    MAX_TOTAL_LIKELIHOOD = 459.5  # Sum of all domain maxLikelihood values
    MAX_TOTAL_CE = 457.6  # Sum of all domain maxCE values (95.50+71.25+23.50+18.00+25.00+62.50+59.00+102.85)
    
    schema = load_scoring_schema()
    totals = calculate_totals(form_data)
    
    # Get raw totals
    raw_impact = max(totals["total_impact"], 0.1)
    raw_likelihood = max(totals["total_likelihood"], 0.1)
    raw_ce = max(totals["total_control_effectiveness"], 1.0)
    
    # Calculate raw risk using original formula
    raw_risk = (raw_impact * raw_likelihood) / raw_ce
    
    # Normalize to 0-100 using the normalization factor
    normalized_risk = min(100, (raw_risk / MAX_EXPECTED_RAW_RISK) * 100)
    
    # Calculate normalized indices for display (0-100 scale)
    impact_index = min(100, (raw_impact / MAX_TOTAL_IMPACT) * 100)
    likelihood_index = min(100, (raw_likelihood / MAX_TOTAL_LIKELIHOOD) * 100)
    ce_index = min(100, (raw_ce / MAX_TOTAL_CE) * 100)
    
    # Calculate inherent risk from normalized indices
    # Inherent Risk = (Impact Index × Likelihood Index) / 100
    normalized_inherent_risk = (impact_index * likelihood_index) / 100
    
    # Calculate residual risk (inherent risk reduced by control effectiveness)
    # Residual Risk = Inherent Risk × (1 - CE Index / 100)
    # This ensures residual risk is always <= inherent risk
    ce_reduction = ce_index / 100
    normalized_residual_risk = normalized_inherent_risk * (1 - ce_reduction)
    
    # Use the new residual risk calculation instead of the old formula
    # The old formula (raw_risk / MAX_EXPECTED_RAW_RISK) could give counterintuitive results
    normalized_risk = normalized_residual_risk
    
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
            inherent_score = domain_scores[short_label].get("InherentRisk", 0)
            top_risk_areas.append({
                "domain": short_label,
                "fullName": domain_info["fullName"],
                "risk_score": risk_score,
                "inherent_risk_score": inherent_score,
                "concern_level": get_risk_rating(risk_score)
            })
    
    top_risk_areas.sort(key=lambda x: x["risk_score"], reverse=True)
    
    # Key derived indicators
    autonomy_indicator = calculate_autonomy_indicator(form_data)
    sensitive_data_indicator = calculate_sensitive_data_indicator(form_data)
    high_risk_context = calculate_high_risk_context_indicator(form_data)
    governance = calculate_governance_score(form_data, schema)
    
    # Control coverage
    control_coverage = min((raw_ce / TARGET_CE), 1.0) * 100
    
    return {
        # Risk scores
        "raw_risk_score": round(raw_risk),
        "overall_risk_score": round(normalized_risk),
        "overall_inherent_risk": round(normalized_inherent_risk),
        "overall_risk_level": risk_rating,
        
        # Normalized indices (0-100) for display
        "impact_index": round(impact_index),
        "likelihood_index": round(likelihood_index),
        "ce_index": round(ce_index),
        
        # Raw totals
        "total_impact": round(raw_impact),
        "total_likelihood": round(raw_likelihood),
        "total_control_effectiveness": round(raw_ce),
        
        # Special factors
        "autonomy_factor": round(totals["autonomy_factor"]),
        "data_quality_factor": round(totals["data_quality_factor"]),
        "expertise_factor": round(totals["expertise_factor"]),
        
        # Domain scores (with normalized indices)
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
        "control_coverage_percent": round(control_coverage)
    }


def calculate_domain_scores(form_data: Dict) -> Dict[str, Dict[str, float]]:
    """
    Calculate domain-level scores for radar charts.
    
    Uses old-style formula with domain-specific normalization:
    - Raw_Domain_Risk = (Domain_Impact × Domain_Likelihood) / Domain_CE
    - Normalized indices are also calculated for display (0-100 scale)
    """
    schema = load_scoring_schema()
    questions = schema.get("questions", {})
    
    # Initialize domain totals with raw values
    domain_raw = {}
    for domain_info in FAIRA_DOMAINS:
        short_label = domain_info["shortLabel"]
        domain_raw[short_label] = {
            "raw_impact": 0.0,
            "raw_likelihood": 0.0,
            "raw_ce": 0.0,
        }
    
    # Process each question and accumulate raw scores
    for question_id, question_config in questions.items():
        try:
            question_scores = calculate_question_scores(question_config, form_data)
            
            for domain, scores in question_scores.items():
                if domain in domain_raw:
                    domain_raw[domain]["raw_impact"] += scores.get("Impact", 0)
                    domain_raw[domain]["raw_likelihood"] += scores.get("Likelihood", 0)
                    domain_raw[domain]["raw_ce"] += scores.get("Control_Effectiveness", 0)
        except Exception as e:
            logger.warning(f"Error processing question {question_id}: {e}")
    
    # Calculate normalized scores for each domain
    domain_totals = {}
    for domain_info in FAIRA_DOMAINS:
        short_label = domain_info["shortLabel"]
        full_name = DOMAIN_SHORT_TO_FULL.get(short_label, short_label)
        norms = DOMAIN_NORMALIZATION.get(full_name, {"maxImpact": 100, "maxLikelihood": 100, "maxCE": 100})
        
        raw = domain_raw[short_label]
        raw_impact = max(raw["raw_impact"], 0.1)
        raw_likelihood = max(raw["raw_likelihood"], 0.1)
        raw_ce = max(raw["raw_ce"], 1.0)
        
        # Normalize individual metrics to 0-100 index for display
        impact_index = min(100, (raw_impact / norms["maxImpact"]) * 100) if norms["maxImpact"] > 0 else 0
        likelihood_index = min(100, (raw_likelihood / norms["maxLikelihood"]) * 100) if norms["maxLikelihood"] > 0 else 0
        ce_index = min(100, (raw_ce / norms["maxCE"]) * 100) if norms["maxCE"] > 0 else 0
        
        # Calculate inherent risk from normalized indices
        # Inherent Risk = (Impact Index × Likelihood Index) / 100
        # This gives a 0-100 scale where 100 = max impact AND max likelihood
        inherent_risk = (impact_index * likelihood_index) / 100
        
        # Calculate residual risk: inherent risk reduced by control effectiveness
        # Residual Risk = Inherent Risk × (1 - CE Index / 100)
        # When CE = 100%, residual = 0. When CE = 0%, residual = inherent
        ce_reduction = ce_index / 100
        residual_risk = inherent_risk * (1 - ce_reduction)
        
        domain_totals[short_label] = {
            # Normalized indices (0-100) for display
            "Impact": round(impact_index),
            "Likelihood": round(likelihood_index),
            "Control_Effectiveness": round(ce_index),
            "InherentRisk": round(inherent_risk),
            "Risk": round(residual_risk),
            # Raw values for reference
            "raw_impact": round(raw["raw_impact"]),
            "raw_likelihood": round(raw["raw_likelihood"]),
            "raw_ce": round(raw["raw_ce"]),
        }
    
    return domain_totals


def get_radar_chart_data(form_data: Dict) -> Dict[str, List[Dict]]:
    """
    Get formatted radar chart data for all charts including inherent and residual risk.
    All values are normalized indices (0-100 scale).
    """
    domain_scores = calculate_domain_scores(form_data)
    
    result = {
        "domainImpact": [],
        "domainLikelihood": [],
        "domainControlEffectiveness": [],
        "domainInherentRisk": [],
        "domainRisk": []  # Residual risk (for backward compatibility)
    }
    
    for domain_info in FAIRA_DOMAINS:
        short_label = domain_info["shortLabel"]
        full_name = domain_info["fullName"]
        scores = domain_scores.get(short_label, {})
        
        result["domainImpact"].append({
            "domain": short_label,
            "fullName": full_name,
            "score": scores.get("Impact", 0),
            "rawValue": scores.get("raw_impact", 0),
            "fullMark": 100
        })
        
        result["domainLikelihood"].append({
            "domain": short_label,
            "fullName": full_name,
            "score": scores.get("Likelihood", 0),
            "rawValue": scores.get("raw_likelihood", 0),
            "fullMark": 100
        })
        
        result["domainControlEffectiveness"].append({
            "domain": short_label,
            "fullName": full_name,
            "score": scores.get("Control_Effectiveness", 0),
            "rawValue": scores.get("raw_ce", 0),
            "fullMark": 100
        })
        
        result["domainInherentRisk"].append({
            "domain": short_label,
            "fullName": full_name,
            "score": scores.get("InherentRisk", 0),
            "fullMark": 100
        })
        
        result["domainRisk"].append({
            "domain": short_label,
            "fullName": full_name,
            "score": scores.get("Risk", 0),
            "fullMark": 100
        })
    
    return result



# ============================================================================
# CONTROLS RECOMMENDATION ENGINE
# ============================================================================

CONTROLS_PATH = Path(__file__).parent / "faira_partc_controls_and_rules.json"

def load_controls_data() -> Dict:
    """Load the FAIRA Part C controls and rules from JSON file"""
    try:
        with open(CONTROLS_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load controls data: {e}")
        return {"controls": [], "recommendation_rules": []}


def get_risk_level_from_score(score: float) -> str:
    """Convert numeric score to risk level string"""
    if score >= 75:
        return "Very High"
    elif score >= 55:
        return "High"
    elif score >= 35:
        return "Medium"
    elif score >= 20:
        return "Low"
    return "Very Low"


def evaluate_rule_condition(rule: Dict, form_data: Dict, risk_summary: Dict, domain_scores: Dict) -> bool:
    """
    Evaluate a rule's 'when' condition against form data and risk scores.
    Returns True if the rule condition is met.
    """
    condition = rule.get("when", {})
    condition_type = condition.get("type")
    
    if condition_type == "domain_threshold":
        # Check if a specific domain's risk level meets a threshold
        metric = condition.get("metric", "domain_residual_risk_level")
        operator = condition.get("operator", ">=")
        threshold_value = condition.get("value", "High")
        target_domain = condition.get("domain")  # Optional: specific domain
        
        # Risk level ordering for comparison
        risk_order = {"Very Low": 1, "Low": 2, "Medium": 3, "High": 4, "Very High": 5}
        threshold_num = risk_order.get(threshold_value, 3)
        
        domains_to_check = []
        if target_domain:
            # Map full name to short label
            for d in FAIRA_DOMAINS:
                if d["fullName"] == target_domain or d["shortLabel"] == target_domain:
                    domains_to_check.append(d["shortLabel"])
                    break
        else:
            # Check all domains
            domains_to_check = [d["shortLabel"] for d in FAIRA_DOMAINS]
        
        for domain_label in domains_to_check:
            if domain_label in domain_scores:
                risk_score = domain_scores[domain_label].get("Risk", 0)
                risk_level = get_risk_level_from_score(risk_score)
                domain_risk_num = risk_order.get(risk_level, 0)
                
                if operator == ">=" and domain_risk_num >= threshold_num:
                    return True
                elif operator == ">" and domain_risk_num > threshold_num:
                    return True
                elif operator == "==" and domain_risk_num == threshold_num:
                    return True
        
        return False
    
    elif condition_type == "overall_threshold":
        # Check overall risk level
        operator = condition.get("operator", ">=")
        threshold_value = condition.get("value", "High")
        
        risk_order = {"Very Low": 1, "Low": 2, "Medium": 3, "High": 4, "Very High": 5}
        threshold_num = risk_order.get(threshold_value, 3)
        
        overall_level = risk_summary.get("overall_risk_level", "Medium")
        overall_num = risk_order.get(overall_level, 0)
        
        if operator == ">=" and overall_num >= threshold_num:
            return True
        elif operator == ">" and overall_num > threshold_num:
            return True
        elif operator == "==" and overall_num == threshold_num:
            return True
        
        return False
    
    elif condition_type == "question_value":
        # Check specific question answer
        question_id = condition.get("question_id", "")
        # Normalize question ID format (A5.11 -> A5_11)
        normalized_id = question_id.upper().replace('.', '_').replace('-', '_')
        operator = condition.get("operator", "equals")
        expected_values = condition.get("value")
        
        actual_value = get_form_value(form_data, normalized_id)
        
        if actual_value is None:
            return False
        
        if operator == "equals":
            return str(actual_value) == str(expected_values)
        elif operator == "in":
            if isinstance(expected_values, list):
                if isinstance(actual_value, list):
                    return any(v in expected_values for v in actual_value)
                return str(actual_value) in expected_values
            return False
        elif operator == "contains":
            if isinstance(actual_value, list):
                return expected_values in actual_value
            return expected_values in str(actual_value)
        
        return False
    
    elif condition_type == "domain_combo":
        # Complex condition: check both inherent and residual risk levels for domains
        # This is for the "high inherent but low residual" rule
        inherent_op = condition.get("domain_inherent_operator", ">=")
        inherent_value = condition.get("domain_inherent_value", "High")
        residual_op = condition.get("domain_residual_operator", "<=")
        residual_value = condition.get("domain_residual_value", "Low")
        
        risk_order = {"Very Low": 1, "Low": 2, "Medium": 3, "High": 4, "Very High": 5}
        inherent_threshold = risk_order.get(inherent_value, 4)
        residual_threshold = risk_order.get(residual_value, 2)
        
        # Check if any domain matches the combo condition
        for domain_label in domain_scores:
            risk_score = domain_scores[domain_label].get("Risk", 0)
            risk_level = get_risk_level_from_score(risk_score)
            residual_num = risk_order.get(risk_level, 0)
            
            # For inherent risk, calculate from Impact × Likelihood
            impact = domain_scores[domain_label].get("Impact", 0) / 5  # Denormalize
            likelihood = domain_scores[domain_label].get("Likelihood", 0) / 5  # Denormalize
            inherent_score = min(100, (impact * likelihood) / 1.2)  # Simplified inherent
            inherent_level = get_risk_level_from_score(inherent_score)
            inherent_num = risk_order.get(inherent_level, 0)
            
            inherent_match = (inherent_op == ">=" and inherent_num >= inherent_threshold) or \
                           (inherent_op == ">" and inherent_num > inherent_threshold)
            residual_match = (residual_op == "<=" and residual_num <= residual_threshold) or \
                            (residual_op == "<" and residual_num < residual_threshold)
            
            if inherent_match and residual_match:
                return True
        
        return False
    
    return False


def get_controls_by_ids(controls_list: List[Dict], control_ids: List[str]) -> List[Dict]:
    """Get control objects by their IDs"""
    return [c for c in controls_list if c.get("control_id") in control_ids]


def get_controls_by_domain(controls_list: List[Dict], domain: str) -> List[Dict]:
    """Get all controls that apply to a specific domain"""
    result = []
    for control in controls_list:
        control_domains = control.get("domains", [])
        if domain in control_domains:
            result.append(control)
    return result


def get_recommended_controls(form_data: Dict, top_n: int = 3) -> Dict[str, Any]:
    """
    Process rules against form data and risk scores to recommend controls.
    Returns top N controls prioritized by rule priority and relevance.
    """
    controls_data = load_controls_data()
    all_controls = controls_data.get("controls", [])
    rules = controls_data.get("recommendation_rules", [])
    
    # Calculate risk scores
    risk_summary = calculate_overall_risk(form_data)
    domain_scores = risk_summary.get("domain_scores", {})
    
    # Track matched controls with their priority and rationale
    matched_controls = {}  # control_id -> {control, priority, rationale, triggered_by}
    
    # Priority ordering
    priority_order = {"High": 3, "Medium": 2, "Low": 1}
    
    for rule in rules:
        if evaluate_rule_condition(rule, form_data, risk_summary, domain_scores):
            rule_priority = rule.get("priority", "Medium")
            then_clause = rule.get("then", {})
            
            # Get controls to recommend
            select_controls = then_clause.get("select_controls", {})
            controls_to_add = []
            
            if "control_ids" in select_controls:
                # Specific control IDs
                controls_to_add = get_controls_by_ids(all_controls, select_controls["control_ids"])
            elif select_controls.get("mode") == "by_domain":
                # Get controls by domain from triggered domains
                # For domain threshold rules, add controls for domains that triggered
                for domain_info in FAIRA_DOMAINS:
                    domain_label = domain_info["shortLabel"]
                    full_name = domain_info["fullName"]
                    if domain_label in domain_scores:
                        risk_score = domain_scores[domain_label].get("Risk", 0)
                        risk_level = get_risk_level_from_score(risk_score)
                        
                        # Check if this domain triggered the rule
                        condition = rule.get("when", {})
                        threshold_value = condition.get("value", "High")
                        risk_order = {"Very Low": 1, "Low": 2, "Medium": 3, "High": 4, "Very High": 5}
                        
                        if risk_order.get(risk_level, 0) >= risk_order.get(threshold_value, 3):
                            domain_controls = get_controls_by_domain(all_controls, full_name)
                            
                            # Apply filters if specified
                            if not select_controls.get("include_all_controls_for_domain", True):
                                control_types = select_controls.get("include_control_types", [])
                                if control_types:
                                    domain_controls = [c for c in domain_controls 
                                                      if c.get("control_type") in control_types]
                                max_per_domain = select_controls.get("max_controls_per_domain")
                                if max_per_domain:
                                    domain_controls = domain_controls[:max_per_domain]
                            
                            controls_to_add.extend(domain_controls)
            
            # Generate rationale from template
            rationale_template = then_clause.get("rationale_template", "")
            rationale = rationale_template
            
            # Replace placeholders in rationale
            rationale = rationale.replace("{overall_residual_risk_level}", risk_summary.get("overall_risk_level", ""))
            rationale = rationale.replace("{overall_risk_level}", risk_summary.get("overall_risk_level", ""))
            
            # Replace domain-specific placeholders
            for domain_info in FAIRA_DOMAINS:
                domain_label = domain_info["shortLabel"]
                full_name = domain_info["fullName"]
                if domain_label in domain_scores:
                    risk_level = get_risk_level_from_score(domain_scores[domain_label].get("Risk", 0))
                    rationale = rationale.replace("{domain_residual_risk_level}", risk_level)
                    rationale = rationale.replace("{domain_inherent_risk_level}", risk_level)
                    rationale = rationale.replace("{domain}", full_name)
            
            # Replace question value placeholders
            for placeholder in re.findall(r'\{([A-Z]\d+\.\d+)\}', rationale):
                normalized_id = placeholder.replace('.', '_')
                value = get_form_value(form_data, normalized_id)
                if value:
                    rationale = rationale.replace(f"{{{placeholder}}}", str(value))
            
            # Add controls to matched set
            for control in controls_to_add:
                control_id = control.get("control_id")
                current_priority = priority_order.get(rule_priority, 2)
                
                if control_id not in matched_controls:
                    matched_controls[control_id] = {
                        "control": control,
                        "priority": current_priority,
                        "priority_label": rule_priority,
                        "rationale": rationale,
                        "triggered_by": [rule.get("rule_id")]
                    }
                else:
                    # Update if higher priority
                    if current_priority > matched_controls[control_id]["priority"]:
                        matched_controls[control_id]["priority"] = current_priority
                        matched_controls[control_id]["priority_label"] = rule_priority
                        matched_controls[control_id]["rationale"] = rationale
                    matched_controls[control_id]["triggered_by"].append(rule.get("rule_id"))
    
    # Sort by priority (highest first) and get top N
    sorted_controls = sorted(
        matched_controls.values(),
        key=lambda x: (-x["priority"], x["control"]["control_id"])
    )
    
    top_controls = sorted_controls[:top_n]
    
    # FALLBACK: If no controls matched (e.g., low-risk assessment), 
    # provide general best-practice controls
    if not top_controls:
        # Get some general governance controls for low-risk scenarios
        # Using actual FAIRA control IDs from the schema
        fallback_control_ids = [
            "FAIRA-C-ACC-01",  # Establish AI accountability ownership
            "FAIRA-C-REL-04",  # Monitor ongoing system performance
            "FAIRA-C-TRANS-01",  # Ensure AI decision explainability
        ]
        fallback_controls = get_controls_by_ids(all_controls, fallback_control_ids)
        
        for control in fallback_controls[:top_n]:
            top_controls.append({
                "control": control,
                "priority": 1,
                "priority_label": "Low",
                "rationale": "Recommended as a general best practice for maintaining AI governance standards, even in low-risk scenarios.",
                "triggered_by": ["fallback_low_risk"]
            })
    
    # Format output
    result = {
        "top_controls": [],
        "total_matched": len(matched_controls) if matched_controls else len(top_controls),
        "risk_summary": {
            "overall_risk_level": risk_summary.get("overall_risk_level"),
            "overall_risk_score": risk_summary.get("overall_risk_score")
        }
    }
    
    for i, item in enumerate(top_controls):
        control = item["control"]
        result["top_controls"].append({
            "rank": i + 1,
            "control_id": control.get("control_id"),
            "title": control.get("title"),
            "description": control.get("description"),
            "detailed_description": control.get("detailed_description"),
            "domains": control.get("domains", []),
            "control_type": control.get("control_type"),
            "implementation_effort": control.get("implementation_effort"),
            "implementation_horizon": control.get("implementation_horizon"),
            "evidence_examples": control.get("evidence_examples", []),
            "priority": item["priority_label"],
            "rationale": item["rationale"],
            "triggered_by": item["triggered_by"]
        })
    
    return result
