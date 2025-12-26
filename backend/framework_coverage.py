"""
Framework Coverage Calculator

This module calculates how comprehensively the AM AI SAFE assessment covers
various AI governance frameworks based on question alignment and assessment scores.

Coverage percentages are calculated using the total control counts from the
Master Control Registry as the denominator, providing accurate representation
of how much of each framework is addressed.
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


def count_unique_controls_addressed(framework_data: Dict[str, Any]) -> Dict[str, int]:
    """
    Count unique controls addressed by the assessment questions.
    
    Uses the alignedControls arrays to count distinct framework controls
    that are mapped to assessment questions.
    
    Returns:
        Dictionary with counts of fully and partially aligned unique controls
    """
    full_align_controls = set()
    partial_align_controls = set()
    
    for question_code, alignment_info in framework_data.items():
        aligned_controls = alignment_info.get("alignedControls", [])
        alignment_type = alignment_info.get("alignmentType", "No Alignment")
        
        for control in aligned_controls:
            control_id = control.get("controlId") or control.get("nativeId")
            if control_id:
                # Check control-level alignment if available, otherwise use question-level
                ctrl_alignment = control.get("alignmentType", "full" if alignment_type == "Fully Aligns" else "partial")
                
                if ctrl_alignment == "full":
                    full_align_controls.add(control_id)
                else:
                    partial_align_controls.add(control_id)
    
    # Remove partial controls that are also fully aligned
    partial_align_controls -= full_align_controls
    
    return {
        "full": len(full_align_controls),
        "partial": len(partial_align_controls),
        "total_unique": len(full_align_controls) + len(partial_align_controls)
    }


def calculate_inherent_coverage(framework_data: Dict[str, Any], framework_id: str) -> Dict[str, Any]:
    """
    Calculate inherent coverage (design-time) for a framework.
    
    This represents how well the assessment questions cover the framework controls
    by design, regardless of how the user answers.
    
    Coverage is calculated as a percentage of the TOTAL CONTROLS in the framework
    (from master registry), not just the number of questions.
    
    Returns percentages for:
    - Strong Coverage: Controls with "Fully Aligns" questions
    - Moderate Coverage: Controls with "Partially Aligns" questions
    - No Coverage: Controls not addressed by any question
    """
    # Get total controls from master registry
    total_controls = get_framework_control_count(framework_id)
    
    # Count unique controls addressed
    control_counts = count_unique_controls_addressed(framework_data)
    
    full_align_count = control_counts["full"]
    partial_align_count = control_counts["partial"]
    total_addressed = control_counts["total_unique"]
    
    # Controls not addressed
    not_addressed = max(0, total_controls - total_addressed)
    
    return {
        "strong": round((full_align_count / total_controls) * 100, 1) if total_controls > 0 else 0,
        "moderate": round((partial_align_count / total_controls) * 100, 1) if total_controls > 0 else 0,
        "weak": 0,  # Reserved - inherent coverage doesn't have "weak"
        "none": round((not_addressed / total_controls) * 100, 1) if total_controls > 0 else 0,
        "total_controls": total_controls,
        "controls_addressed": total_addressed,
        "full_align_controls": full_align_count,
        "partial_align_controls": partial_align_count
    }


def calculate_achieved_coverage(
    framework_data: Dict[str, Any], 
    answers: List[Dict[str, Any]],
    framework_id: str
) -> Dict[str, Any]:
    """
    Calculate achieved coverage based on assessment answers.
    
    This represents the actual coverage achieved based on how well
    the user answered each question. Coverage is calculated against
    the total number of controls in the framework (from master registry).
    
    Logic:
    - A control with "full" alignment + high score (3-4) = Strong Coverage
    - A control with "full" alignment + medium score (2) = Moderate Coverage
    - A control with "full" alignment + low score (1) = Weak Coverage
    - A control with "partial" alignment + high score (3-4) = Moderate Coverage
    - A control with "partial" alignment + medium score (2) = Weak Coverage
    - A control with "partial" alignment + low score (1) = No Coverage
    - Unanswered or unmapped controls = No Coverage
    """
    # Get total controls from master registry
    total_controls = get_framework_control_count(framework_id)
    
    # Create lookup for answers by question code
    answer_lookup = {}
    for answer in answers:
        question_code = answer.get("question_code")
        if question_code:
            answer_lookup[question_code] = answer.get("numeric_score", 0)
        else:
            question_id = answer.get("question_id", "")
            if "-" in question_id and len(question_id) <= 6:
                answer_lookup[question_id] = answer.get("numeric_score", 0)
    
    # Track coverage by control
    control_coverage = {}  # control_id -> coverage_level (strong/moderate/weak/none)
    
    for question_code, alignment_info in framework_data.items():
        aligned_controls = alignment_info.get("alignedControls", [])
        question_alignment = alignment_info.get("alignmentType", "No Alignment")
        score = answer_lookup.get(question_code, 0)
        
        for control in aligned_controls:
            control_id = control.get("controlId") or control.get("nativeId")
            if not control_id:
                continue
            
            # Get control-level alignment, default to derived from question alignment
            ctrl_alignment = control.get("alignmentType", "full" if question_alignment == "Fully Aligns" else "partial")
            
            # Calculate coverage level for this control based on alignment and score
            if ctrl_alignment == "full":
                if score >= STRONG_SCORE_THRESHOLD:
                    coverage_level = "strong"
                elif score >= MODERATE_SCORE_THRESHOLD:
                    coverage_level = "moderate"
                elif score >= WEAK_SCORE_THRESHOLD:
                    coverage_level = "weak"
                else:
                    coverage_level = "none"
            else:  # partial alignment
                if score >= STRONG_SCORE_THRESHOLD:
                    coverage_level = "moderate"
                elif score >= MODERATE_SCORE_THRESHOLD:
                    coverage_level = "weak"
                else:
                    coverage_level = "none"
            
            # Keep the best coverage level if control is addressed by multiple questions
            current = control_coverage.get(control_id, "none")
            coverage_priority = {"strong": 4, "moderate": 3, "weak": 2, "none": 1}
            if coverage_priority.get(coverage_level, 0) > coverage_priority.get(current, 0):
                control_coverage[control_id] = coverage_level
    
    # Count controls by coverage level
    strong_count = sum(1 for level in control_coverage.values() if level == "strong")
    moderate_count = sum(1 for level in control_coverage.values() if level == "moderate")
    weak_count = sum(1 for level in control_coverage.values() if level == "weak")
    
    # Controls not addressed at all
    addressed_count = len(control_coverage)
    not_addressed = max(0, total_controls - addressed_count)
    no_coverage_count = sum(1 for level in control_coverage.values() if level == "none") + not_addressed
    
    return {
        "strong": round((strong_count / total_controls) * 100, 1) if total_controls > 0 else 0,
        "moderate": round((moderate_count / total_controls) * 100, 1) if total_controls > 0 else 0,
        "weak": round((weak_count / total_controls) * 100, 1) if total_controls > 0 else 0,
        "none": round((no_coverage_count / total_controls) * 100, 1) if total_controls > 0 else 0,
        "total_controls": total_controls,
        "controls_with_strong": strong_count,
        "controls_with_moderate": moderate_count,
        "controls_with_weak": weak_count,
        "controls_with_none": no_coverage_count
    }


def get_framework_coverage(
    framework_id: str,
    answers: Optional[List[Dict[str, Any]]] = None
) -> Optional[Dict[str, Any]]:
    """
    Get complete framework coverage data for a single framework.
    
    Returns inherent and achieved coverage percentages based on
    the total control counts from the master registry.
    """
    framework_data = load_framework_data(framework_id)
    if not framework_data:
        return None
    
    config = FRAMEWORK_CONFIG[framework_id]
    inherent = calculate_inherent_coverage(framework_data, framework_id)
    achieved = calculate_achieved_coverage(framework_data, answers or [], framework_id)
    
    return {
        "framework_id": framework_id,
        "title": config["title"],
        "registry_id": config.get("registry_id"),
        "total_controls": inherent.get("total_controls", TOTAL_QUESTIONS),
        "controls_addressed": inherent.get("controls_addressed", 0),
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
