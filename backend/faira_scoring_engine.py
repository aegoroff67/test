"""
FAIRA Risk Assessment Scoring Engine

Calculates domain-level Impact, Likelihood, Control Effectiveness, and Risk scores
based on assessment form data and the scoring schema.

Formula: Domain_Risk = (Domain_Impact × Domain_Likelihood) / Domain_Control_Effectiveness
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
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

# Domain mapping between schema domains and radar chart domains
DOMAIN_MAPPING = {
    # Schema domain -> Radar chart domain (short label)
    "Reliability and Safety": "Reliability",
    "Accountability": "Accountability",
    "Transparency and Explainability": "Transparency",
    "Fairness": "Fairness",
    "Human, Societal and Environmental Wellbeing": "Wellbeing",
    "Human-centred Values": "Human",
    "Privacy Protection and Security": "Privacy",
    "Contestability": "Contestability",
}

# All 8 radar chart domains with full names (matching Part B sections)
FAIRA_DOMAINS = [
    {"id": "B1", "shortLabel": "Wellbeing", "fullName": "Human, Societal and Environmental Wellbeing"},
    {"id": "B2", "shortLabel": "Human", "fullName": "Human-Centred Values"},
    {"id": "B3", "shortLabel": "Fairness", "fullName": "Fairness"},
    {"id": "B4", "shortLabel": "Privacy", "fullName": "Privacy Protection and Security"},
    {"id": "B5", "shortLabel": "Reliability", "fullName": "Reliability and Safety"},
    {"id": "B6", "shortLabel": "Transparency", "fullName": "Transparency and Explainability"},
    {"id": "B7", "shortLabel": "Contestability", "fullName": "Contestability"},
    {"id": "B8", "shortLabel": "Accountability", "fullName": "Accountability"},
]

# Baseline Control Effectiveness for each domain
BASELINE_CE = {
    "Wellbeing": 10.0,
    "Transparency": 10.0,
    "Fairness": 10.0,
    "Robustness": 10.0,
    "Testing": 10.0,
    "Oversight": 10.0,
    "Privacy": 10.0,
    "Accountability": 10.0,
}


def normalize_field_name(field_name: str) -> str:
    """Convert field names like 'a1_1' or 'A1.1' to schema format 'A1_1'"""
    # Handle various formats
    normalized = field_name.upper().replace('.', '_').replace('-', '_')
    return normalized


def get_form_value(form_data: Dict, field_name: str) -> Any:
    """Get a value from form data, trying various field name formats"""
    # Try exact match first
    if field_name in form_data:
        return form_data[field_name]
    
    # Try lowercase
    lower_field = field_name.lower()
    if lower_field in form_data:
        return form_data[lower_field]
    
    # Try with dots instead of underscores
    dot_field = field_name.replace('_', '.')
    if dot_field in form_data:
        return form_data[dot_field]
    
    dot_field_lower = dot_field.lower()
    if dot_field_lower in form_data:
        return form_data[dot_field_lower]
    
    return None


def calculate_question_scores(
    question_config: Dict,
    form_data: Dict
) -> Dict[str, Dict[str, float]]:
    """
    Calculate Impact, Likelihood, and CE modifiers for a single question.
    Returns: {domain: {"Impact": x, "Likelihood": y, "Control_Effectiveness": z}}
    """
    result = {}
    
    if not question_config.get("scoring"):
        return result
    
    question_id = question_config.get("id", "")
    question_type = question_config.get("type", "")
    scoring = question_config.get("scoring", {})
    domains = question_config.get("domains", [])
    
    # Get the form value for this question
    form_value = get_form_value(form_data, question_id)
    
    if form_value is None:
        return result
    
    # Initialize result for each domain this question affects
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
    
    elif question_type == "rating_multi":
        _process_rating_multi(scoring, form_value, form_data, domains, result)
    
    elif question_type == "multi_rating":
        _process_multi_rating(scoring, form_value, form_data, domains, result)
    
    elif question_type == "yes_no_with_rating":
        _process_yes_no_with_rating(scoring, form_value, form_data, question_id, domains, result)
    
    elif question_type == "yes_unknown_no_with_options":
        _process_yes_unknown_no_with_options(scoring, form_value, form_data, question_id, domains, result)
    
    elif question_type == "multiselect_with_rating":
        _process_multiselect_with_rating(scoring, form_value, form_data, question_id, domains, result)
    
    elif question_type == "yes_no_with_subsections":
        _process_yes_no_with_subsections(scoring, form_value, form_data, question_id, domains, result)
    
    return result


def _process_multiselect(scoring: Dict, form_value: Any, domains: List[str], result: Dict):
    """Process multiselect question type"""
    options = scoring.get("options", {})
    
    # form_value should be a list of selected options
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
    
    # Normalize yes/no value
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
        
        # Apply base scores
        for schema_domain in domains:
            radar_domain = DOMAIN_MAPPING.get(schema_domain)
            if radar_domain and radar_domain in result:
                for metric in ["Impact", "Likelihood", "Control_Effectiveness"]:
                    if metric in option_config:
                        result[radar_domain][metric] += option_config[metric]
        
        # Process sub-options if Yes
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
    
    # Convert to string key
    rating_key = str(form_value)
    
    if rating_key in rating_scale:
        rating_scores = rating_scale[rating_key]
        for schema_domain in domains:
            radar_domain = DOMAIN_MAPPING.get(schema_domain)
            if radar_domain and radar_domain in result:
                for metric, value in rating_scores.items():
                    if metric in result[radar_domain]:
                        result[radar_domain][metric] += value


def _process_rating_multi(scoring: Dict, form_value: Any, form_data: Dict, 
                          domains: List[str], result: Dict):
    """Process rating multi (multiple dimension ratings) question type"""
    dimensions = scoring.get("dimensions", {})
    
    total_rating = 0
    count = 0
    
    for dim_name, dim_config in dimensions.items():
        field = dim_config.get("field", "")
        dim_value = get_form_value(form_data, field)
        
        if dim_value is not None:
            try:
                total_rating += float(dim_value)
                count += 1
            except (ValueError, TypeError):
                pass
    
    if count > 0:
        # Calculate DataQualityFactor: 6 - average rating
        avg_rating = total_rating / count
        quality_factor = 6 - avg_rating
        
        # Apply to Likelihood
        for schema_domain in domains:
            radar_domain = DOMAIN_MAPPING.get(schema_domain)
            if radar_domain and radar_domain in result:
                result[radar_domain]["Likelihood"] += quality_factor


def _process_multi_rating(scoring: Dict, form_value: Any, form_data: Dict, 
                          domains: List[str], result: Dict):
    """Process multi rating (categories with positive/neutral/negative) question type"""
    categories = scoring.get("categories", {})
    
    for cat_name, cat_config in categories.items():
        field = cat_config.get("field", "")
        cat_value = get_form_value(form_data, field)
        
        if cat_value and "options" in cat_config:
            if cat_value in cat_config["options"]:
                cat_scores = cat_config["options"][cat_value]
                for schema_domain in domains:
                    radar_domain = DOMAIN_MAPPING.get(schema_domain)
                    if radar_domain and radar_domain in result:
                        for metric, value in cat_scores.items():
                            if metric in result[radar_domain]:
                                result[radar_domain][metric] += value


def _process_yes_no_with_rating(scoring: Dict, form_value: Any, form_data: Dict,
                                 question_id: str, domains: List[str], result: Dict):
    """Process yes/no with rating sub-question type"""
    options = scoring.get("options", {})
    
    answer = "Yes" if str(form_value).lower() in ["yes", "true", "1"] else "No"
    
    if answer in options:
        option_config = options[answer]
        
        # Apply base scores
        for schema_domain in domains:
            radar_domain = DOMAIN_MAPPING.get(schema_domain)
            if radar_domain and radar_domain in result:
                for metric in ["Impact", "Likelihood", "Control_Effectiveness"]:
                    if metric in option_config:
                        result[radar_domain][metric] += option_config[metric]
        
        # Process rating if Yes
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
    """Process yes/unknown/no with options type"""
    options = scoring.get("options", {})
    
    # Map form value to option key
    answer = str(form_value).capitalize()
    if answer not in options:
        answer = "Unknown"
    
    if answer in options:
        option_config = options[answer]
        
        # Apply base scores
        for schema_domain in domains:
            radar_domain = DOMAIN_MAPPING.get(schema_domain)
            if radar_domain and radar_domain in result:
                for metric in ["Impact", "Likelihood", "Control_Effectiveness"]:
                    if metric in option_config:
                        result[radar_domain][metric] += option_config[metric]
        
        # Process affected groups if Yes
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


def _process_multiselect_with_rating(scoring: Dict, form_value: Any, form_data: Dict,
                                      question_id: str, domains: List[str], result: Dict):
    """Process multiselect with rating parts question type"""
    # Process part_a (impact types)
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
                                    result[radar_domain][metric] += value


def _process_yes_no_with_subsections(scoring: Dict, form_value: Any, form_data: Dict,
                                      question_id: str, domains: List[str], result: Dict):
    """Process yes/no with subsections (like A5_10 with commonwealth/state laws)"""
    options = scoring.get("options", {})
    
    answer = "Yes" if str(form_value).lower() in ["yes", "true", "1"] else "No"
    
    if answer in options:
        option_config = options[answer]
        
        # Apply base scores
        for schema_domain in domains:
            radar_domain = DOMAIN_MAPPING.get(schema_domain)
            if radar_domain and radar_domain in result:
                for metric in ["Impact", "Likelihood", "Control_Effectiveness"]:
                    if metric in option_config:
                        result[radar_domain][metric] += option_config[metric]
        
        # Process subsections if Yes
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


def calculate_domain_scores(form_data: Dict) -> Dict[str, Dict[str, float]]:
    """
    Calculate all domain scores from FAIRA form data.
    
    Returns:
    {
        "Wellbeing": {"Impact": x, "Likelihood": y, "Control_Effectiveness": z, "Risk": r},
        "Transparency": {...},
        ...
    }
    """
    schema = load_scoring_schema()
    questions = schema.get("questions", {})
    
    # Initialize domain totals
    domain_totals = {}
    for domain_info in FAIRA_DOMAINS:
        short_label = domain_info["shortLabel"]
        domain_totals[short_label] = {
            "Impact": 0.0,
            "Likelihood": 0.0,
            "Control_Effectiveness": BASELINE_CE.get(short_label, 10.0),
        }
    
    # Process each question
    for question_id, question_config in questions.items():
        try:
            question_scores = calculate_question_scores(question_config, form_data)
            
            # Add scores to domain totals
            for domain, scores in question_scores.items():
                if domain in domain_totals:
                    domain_totals[domain]["Impact"] += scores.get("Impact", 0)
                    domain_totals[domain]["Likelihood"] += scores.get("Likelihood", 0)
                    domain_totals[domain]["Control_Effectiveness"] += scores.get("Control_Effectiveness", 0)
        except Exception as e:
            logger.warning(f"Error processing question {question_id}: {e}")
    
    # Calculate Risk for each domain
    for domain, scores in domain_totals.items():
        impact = max(scores["Impact"], 0.1)  # Minimum to avoid zero
        likelihood = max(scores["Likelihood"], 0.1)
        ce = max(scores["Control_Effectiveness"], 1.0)  # Minimum to avoid division by zero
        
        # Raw risk calculation
        raw_risk = (impact * likelihood) / ce
        
        # Normalize to 0-100 scale (cap at 100)
        # Assuming typical max raw risk ~50, scale appropriately
        normalized_risk = min(raw_risk * 2, 100)
        
        scores["Risk"] = round(normalized_risk, 1)
        
        # Also normalize other metrics to 0-100 for display
        scores["Impact"] = min(round(scores["Impact"] * 5, 1), 100)
        scores["Likelihood"] = min(round(scores["Likelihood"] * 5, 1), 100)
        scores["Control_Effectiveness"] = min(round(scores["Control_Effectiveness"] * 5, 1), 100)
    
    return domain_totals


def get_radar_chart_data(form_data: Dict) -> Dict[str, List[Dict]]:
    """
    Get formatted radar chart data for all 4 charts.
    
    Returns:
    {
        "domainImpact": [{"domain": "Wellbeing", "fullName": "...", "score": 45}, ...],
        "domainLikelihood": [...],
        "domainControlEffectiveness": [...],
        "domainRisk": [...]
    }
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


def calculate_overall_risk(form_data: Dict) -> Dict[str, Any]:
    """
    Calculate overall risk summary.
    
    Returns:
    {
        "overall_risk_score": 58.5,
        "overall_risk_level": "Medium",
        "domain_scores": {...},
        "top_risk_areas": [...]
    }
    """
    domain_scores = calculate_domain_scores(form_data)
    
    # Calculate overall risk as average of domain risks
    total_risk = sum(scores.get("Risk", 0) for scores in domain_scores.values())
    overall_risk_score = round(total_risk / len(domain_scores), 1) if domain_scores else 0
    
    # Determine risk level
    if overall_risk_score >= 75:
        risk_level = "Critical"
    elif overall_risk_score >= 50:
        risk_level = "High"
    elif overall_risk_score >= 25:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    # Get top 3 risk areas
    sorted_domains = sorted(
        domain_scores.items(),
        key=lambda x: x[1].get("Risk", 0),
        reverse=True
    )[:3]
    
    top_risk_areas = []
    for domain_name, scores in sorted_domains:
        domain_info = next((d for d in FAIRA_DOMAINS if d["shortLabel"] == domain_name), None)
        risk_score = scores.get("Risk", 0)
        
        if risk_score >= 75:
            concern_level = "Critical"
        elif risk_score >= 50:
            concern_level = "High"
        elif risk_score >= 25:
            concern_level = "Medium"
        else:
            concern_level = "Low"
        
        top_risk_areas.append({
            "domain": domain_name,
            "fullName": domain_info["fullName"] if domain_info else domain_name,
            "risk_score": risk_score,
            "concern_level": concern_level
        })
    
    return {
        "overall_risk_score": overall_risk_score,
        "overall_risk_level": risk_level,
        "domain_scores": domain_scores,
        "top_risk_areas": top_risk_areas
    }
