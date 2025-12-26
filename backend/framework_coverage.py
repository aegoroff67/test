"""
Framework Coverage Calculator

This module calculates how comprehensively the AM AI SAFE assessment covers
various AI governance frameworks based on question alignment and assessment scores.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

# Framework configuration - maps framework IDs to their data files, display names, and registry IDs
FRAMEWORK_CONFIG = {
    "iso42001": {
        "file": "iso42001AlignmentData.json",
        "title": "AS ISO/IEC 42001:2023",
        "registry_id": "ISO42001"
    },
    "au_ethics": {
        "file": "auEthicsAlignmentData.json",
        "title": "Australian AI Ethics Principles (2024)",
        "registry_id": "AEP"
    },
    "au_guidance": {
        "file": "auGuidanceAlignmentData.json",
        "title": "Australian Guidance for AI Adoption (2025)",
        "registry_id": "GAA-I"
    },
    "au_assurance": {
        "file": "auAssuranceAlignmentData.json",
        "title": "Australian National Framework for the Assurance of AI in Government (2024)",
        "registry_id": "AU-ASS"
    },
    "eu_ai_act": {
        "file": "euAiActAlignmentData.json",
        "title": "EU AI Act (2024 final)",
        "registry_id": "EU-AIA"
    },
    "nist_rmf": {
        "file": "nistAlignmentData.json",
        "title": "NIST AI RMF (2023)",
        "registry_id": "NIST-RMF"
    },
    "oecd": {
        "file": "oecdPrinciplesAlignmentData.json",
        "title": "OECD Principles (2019)",
        "registry_id": "OECD"
    },
    "singapore_maf": {
        "file": "singaporeMafAlignmentData.json",
        "title": "Singapore MAF (2024)",
        "registry_id": "SG-MAF"
    }
}

# Total number of questions in the assessment
TOTAL_QUESTIONS = 88

# Score thresholds for coverage classification
# Leading (4) or Established (3) = Strong coverage achieved
# Developing (2) = Moderate coverage achieved  
# Foundational (1) = Weak coverage achieved
# No answer or 0 = No coverage achieved
STRONG_SCORE_THRESHOLD = 3  # Score >= 3 (Established/Leading)
MODERATE_SCORE_THRESHOLD = 2  # Score == 2 (Developing)
WEAK_SCORE_THRESHOLD = 1  # Score == 1 (Foundational)

# Cache for master control registry
_registry_cache = None


def load_master_registry() -> Dict[str, Any]:
    """Load the master control registry from file (with caching)"""
    global _registry_cache
    
    if _registry_cache is not None:
        return _registry_cache
    
    registry_path = Path(__file__).parent / "master_control_registry.json"
    
    if not registry_path.exists():
        # Fallback to data folder
        registry_path = Path(__file__).parent / "data" / "master_control_registry.json"
    
    if not registry_path.exists():
        # Return empty structure if registry not found
        return {"frameworkCounts": {}, "controls": []}
    
    with open(registry_path, 'r') as f:
        _registry_cache = json.load(f)
    
    return _registry_cache


def get_framework_control_count(framework_id: str) -> int:
    """
    Get the total number of controls for a framework from the master registry.
    
    Args:
        framework_id: The framework ID as used in FRAMEWORK_CONFIG (e.g., 'iso42001')
    
    Returns:
        Total control count from registry, or TOTAL_QUESTIONS as fallback
    """
    if framework_id not in FRAMEWORK_CONFIG:
        return TOTAL_QUESTIONS
    
    registry_id = FRAMEWORK_CONFIG[framework_id].get("registry_id")
    if not registry_id:
        return TOTAL_QUESTIONS
    
    registry = load_master_registry()
    framework_counts = registry.get("frameworkCounts", {})
    
    return framework_counts.get(registry_id, TOTAL_QUESTIONS)


def load_framework_data(framework_id: str) -> Optional[Dict[str, Any]]:
    """Load alignment data for a specific framework"""
    if framework_id not in FRAMEWORK_CONFIG:
        return None
    
    data_dir = Path(__file__).parent / "framework_data"
    file_path = data_dir / FRAMEWORK_CONFIG[framework_id]["file"]
    
    if not file_path.exists():
        return None
    
    with open(file_path, 'r') as f:
        return json.load(f)


def calculate_inherent_coverage(framework_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculate inherent coverage (design-time) for a framework.
    
    This represents how well the assessment questions cover the framework controls
    by design, regardless of how the user answers.
    
    Returns percentages for:
    - Strong Coverage: Questions with "Fully Aligns"
    - Moderate Coverage: Questions with "Partially Aligns"
    - Weak Coverage: (Reserved for future use)
    - No Coverage: Questions with "No Alignment" or not mapped
    """
    full_align_count = 0
    partial_align_count = 0
    no_align_count = 0
    
    # Count questions by alignment type
    for question_code, alignment_info in framework_data.items():
        alignment_type = alignment_info.get("alignmentType", "No Alignment")
        
        if alignment_type == "Fully Aligns":
            full_align_count += 1
        elif alignment_type == "Partially Aligns":
            partial_align_count += 1
        else:
            no_align_count += 1
    
    # Questions not in the framework data are considered "No Coverage"
    mapped_questions = len(framework_data)
    unmapped_questions = max(0, TOTAL_QUESTIONS - mapped_questions)
    no_align_count += unmapped_questions
    
    total = TOTAL_QUESTIONS
    
    return {
        "strong": round((full_align_count / total) * 100, 1) if total > 0 else 0,
        "moderate": round((partial_align_count / total) * 100, 1) if total > 0 else 0,
        "weak": 0,  # Reserved - inherent coverage doesn't have "weak"
        "none": round((no_align_count / total) * 100, 1) if total > 0 else 0
    }


def calculate_achieved_coverage(
    framework_data: Dict[str, Any], 
    answers: List[Dict[str, Any]]
) -> Dict[str, float]:
    """
    Calculate achieved coverage based on assessment answers.
    
    This represents the actual coverage achieved based on how well
    the user answered each question.
    
    Logic:
    - A question with "Fully Aligns" + high score (3-4) = Strong Coverage
    - A question with "Fully Aligns" + medium score (2) = Moderate Coverage
    - A question with "Fully Aligns" + low score (1) = Weak Coverage
    - A question with "Partially Aligns" + high score (3-4) = Moderate Coverage
    - A question with "Partially Aligns" + medium score (2) = Weak Coverage
    - A question with "Partially Aligns" + low score (1) = No Coverage
    - Unanswered or "No Alignment" = No Coverage
    """
    # Create lookup for answers by question code
    answer_lookup = {}
    for answer in answers:
        # Use question_code if available (enriched by backend), otherwise try question_id
        question_code = answer.get("question_code")
        if question_code:
            answer_lookup[question_code] = answer.get("numeric_score", 0)
        else:
            # Fallback: try to use question_id if it looks like a code (e.g., "FA-1")
            question_id = answer.get("question_id", "")
            if "-" in question_id and len(question_id) <= 6:
                answer_lookup[question_id] = answer.get("numeric_score", 0)
    
    strong_count = 0
    moderate_count = 0
    weak_count = 0
    no_coverage_count = 0
    
    # Process each question in the framework alignment data
    for question_code, alignment_info in framework_data.items():
        alignment_type = alignment_info.get("alignmentType", "No Alignment")
        score = answer_lookup.get(question_code, 0)
        
        if alignment_type == "Fully Aligns":
            if score >= STRONG_SCORE_THRESHOLD:
                strong_count += 1
            elif score >= MODERATE_SCORE_THRESHOLD:
                moderate_count += 1
            elif score >= WEAK_SCORE_THRESHOLD:
                weak_count += 1
            else:
                no_coverage_count += 1
                
        elif alignment_type == "Partially Aligns":
            if score >= STRONG_SCORE_THRESHOLD:
                moderate_count += 1
            elif score >= MODERATE_SCORE_THRESHOLD:
                weak_count += 1
            else:
                no_coverage_count += 1
        else:
            # No Alignment
            no_coverage_count += 1
    
    # Add unmapped questions to no coverage
    mapped_questions = len(framework_data)
    unmapped_questions = max(0, TOTAL_QUESTIONS - mapped_questions)
    no_coverage_count += unmapped_questions
    
    total = TOTAL_QUESTIONS
    
    return {
        "strong": round((strong_count / total) * 100, 1) if total > 0 else 0,
        "moderate": round((moderate_count / total) * 100, 1) if total > 0 else 0,
        "weak": round((weak_count / total) * 100, 1) if total > 0 else 0,
        "none": round((no_coverage_count / total) * 100, 1) if total > 0 else 0
    }


def get_framework_coverage(
    framework_id: str,
    answers: Optional[List[Dict[str, Any]]] = None
) -> Optional[Dict[str, Any]]:
    """
    Get complete framework coverage data for a single framework.
    
    Returns inherent and achieved coverage percentages.
    """
    framework_data = load_framework_data(framework_id)
    if not framework_data:
        return None
    
    config = FRAMEWORK_CONFIG[framework_id]
    inherent = calculate_inherent_coverage(framework_data)
    achieved = calculate_achieved_coverage(framework_data, answers or [])
    
    # Get registry info for reference
    total_controls = get_framework_control_count(framework_id)
    
    return {
        "framework_id": framework_id,
        "title": config["title"],
        "registry_id": config.get("registry_id"),
        "total_controls": total_controls,
        "inherent_coverage": inherent,
        "achieved_coverage": achieved,
        "chart_data": [
            {
                "category": "Strong Coverage",
                "inherent": inherent["strong"],
                "achieved": achieved["strong"]
            },
            {
                "category": "Moderate Coverage", 
                "inherent": inherent["moderate"],
                "achieved": achieved["moderate"]
            },
            {
                "category": "Weak Coverage",
                "inherent": inherent["weak"],
                "achieved": achieved["weak"]
            },
            {
                "category": "No Coverage",
                "inherent": inherent["none"],
                "achieved": achieved["none"]
            }
        ]
    }


def get_all_framework_coverage(
    answers: Optional[List[Dict[str, Any]]] = None,
    selected_frameworks: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Get framework coverage data for all frameworks.
    
    Args:
        answers: List of assessment answers
        selected_frameworks: Optional list of framework titles selected in the assessment.
                           If provided, frameworks not selected will have is_selected=False.
    
    Returns list of framework coverage data sorted by framework ID.
    """
    results = []
    
    for framework_id in FRAMEWORK_CONFIG:
        coverage = get_framework_coverage(framework_id, answers)
        if coverage:
            # Check if this framework was selected in the assessment
            framework_title = FRAMEWORK_CONFIG[framework_id]["title"]
            is_selected = True
            
            if selected_frameworks is not None:
                # Flexible matching for framework selection
                is_selected = any(
                    framework_title.lower() in sel.lower() or 
                    sel.lower() in framework_title.lower() or
                    _normalize_framework_name(framework_title) == _normalize_framework_name(sel)
                    for sel in selected_frameworks
                )
            
            coverage["is_selected"] = is_selected
            results.append(coverage)
    
    return results


def get_registry_summary() -> Dict[str, Any]:
    """
    Get summary information from the master control registry.
    
    Returns version, total controls, and breakdown by framework.
    """
    registry = load_master_registry()
    
    return {
        "version": registry.get("version", "unknown"),
        "last_updated": registry.get("lastUpdated", "unknown"),
        "total_controls": registry.get("totalControls", 0),
        "framework_counts": registry.get("frameworkCounts", {})
    }


def _normalize_framework_name(name: str) -> str:
    """Remove year annotations and normalize framework names for comparison"""
    import re
    # Remove year patterns like (2023), (2024 final), etc.
    normalized = re.sub(r'\s*\(\d{4}[^)]*\)\s*', '', name).strip().lower()
    return normalized
