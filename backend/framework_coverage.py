"""
Framework Coverage Calculator

This module calculates how comprehensively the AM AI SAFE assessment covers
various AI governance frameworks based on question alignment and assessment scores.

Coverage is calculated as:
- For frameworks WITH alignedControls data: unique controls addressed / total controls in registry
- For frameworks WITHOUT alignedControls data: questions with alignment / total questions (legacy)
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
        registry_path = Path(__file__).parent / "data" / "master_control_registry.json"
    
    if not registry_path.exists():
        return {"frameworkCounts": {}, "controls": []}
    
    with open(registry_path, 'r') as f:
        _registry_cache = json.load(f)
    
    return _registry_cache


def get_framework_control_count(framework_id: str) -> int:
    """Get the total number of controls for a framework from the master registry."""
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


def has_aligned_controls_data(framework_data: Dict[str, Any]) -> bool:
    """Check if framework data has alignedControls populated"""
    for alignment_info in framework_data.values():
        if alignment_info.get("alignedControls"):
            return True
    return False


def count_unique_controls(framework_data: Dict[str, Any]) -> Dict[str, int]:
    """
    Count unique controls addressed by the assessment questions.
    Uses alignedControls arrays to count distinct framework controls.
    """
    full_align_controls = set()
    partial_align_controls = set()
    
    for question_code, alignment_info in framework_data.items():
        aligned_controls = alignment_info.get("alignedControls", [])
        
        for control in aligned_controls:
            control_id = control.get("controlId") or control.get("nativeId")
            if control_id:
                ctrl_alignment = control.get("alignmentType", "full")
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
    
    If alignedControls data exists: coverage = unique controls addressed / total controls in registry
    If no alignedControls data: coverage = questions with alignment / total questions (legacy)
    """
    use_control_based = has_aligned_controls_data(framework_data)
    
    if use_control_based:
        # NEW: Control-based calculation using registry totals
        total_controls = get_framework_control_count(framework_id)
        control_counts = count_unique_controls(framework_data)
        
        full_align_count = control_counts["full"]
        partial_align_count = control_counts["partial"]
        total_addressed = control_counts["total_unique"]
        not_addressed = max(0, total_controls - total_addressed)
        
        return {
            "strong": round((full_align_count / total_controls) * 100, 1) if total_controls > 0 else 0,
            "moderate": round((partial_align_count / total_controls) * 100, 1) if total_controls > 0 else 0,
            "weak": 0,
            "none": round((not_addressed / total_controls) * 100, 1) if total_controls > 0 else 0,
            "calculation_method": "control_based",
            "total_controls": total_controls,
            "controls_addressed": total_addressed
        }
    else:
        # LEGACY: Question-based calculation
        full_align_count = 0
        partial_align_count = 0
        no_align_count = 0
        
        for question_code, alignment_info in framework_data.items():
            alignment_type = alignment_info.get("alignmentType", "No Alignment")
            if alignment_type == "Fully Aligns":
                full_align_count += 1
            elif alignment_type == "Partially Aligns":
                partial_align_count += 1
            else:
                no_align_count += 1
        
        mapped_questions = len(framework_data)
        unmapped_questions = max(0, TOTAL_QUESTIONS - mapped_questions)
        no_align_count += unmapped_questions
        
        total = TOTAL_QUESTIONS
        
        return {
            "strong": round((full_align_count / total) * 100, 1) if total > 0 else 0,
            "moderate": round((partial_align_count / total) * 100, 1) if total > 0 else 0,
            "weak": 0,
            "none": round((no_align_count / total) * 100, 1) if total > 0 else 0,
            "calculation_method": "question_based",
            "total_controls": get_framework_control_count(framework_id),
            "controls_addressed": None
        }


def calculate_achieved_coverage(
    framework_data: Dict[str, Any], 
    answers: List[Dict[str, Any]],
    framework_id: str
) -> Dict[str, Any]:
    """
    Calculate achieved coverage based on assessment answers.
    
    If alignedControls data exists: track coverage per unique control
    If no alignedControls data: track coverage per question (legacy)
    """
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
    
    use_control_based = has_aligned_controls_data(framework_data)
    
    if use_control_based:
        # NEW: Control-based calculation
        total_controls = get_framework_control_count(framework_id)
        control_coverage = {}  # control_id -> best coverage level
        
        for question_code, alignment_info in framework_data.items():
            aligned_controls = alignment_info.get("alignedControls", [])
            score = answer_lookup.get(question_code, 0)
            
            for control in aligned_controls:
                control_id = control.get("controlId") or control.get("nativeId")
                if not control_id:
                    continue
                
                ctrl_alignment = control.get("alignmentType", "full")
                
                # Calculate coverage level
                if ctrl_alignment == "full":
                    if score >= STRONG_SCORE_THRESHOLD:
                        coverage_level = "strong"
                    elif score >= MODERATE_SCORE_THRESHOLD:
                        coverage_level = "moderate"
                    elif score >= WEAK_SCORE_THRESHOLD:
                        coverage_level = "weak"
                    else:
                        coverage_level = "none"
                else:  # partial
                    if score >= STRONG_SCORE_THRESHOLD:
                        coverage_level = "moderate"
                    elif score >= MODERATE_SCORE_THRESHOLD:
                        coverage_level = "weak"
                    else:
                        coverage_level = "none"
                
                # Keep best coverage level per control
                current = control_coverage.get(control_id, "none")
                priority = {"strong": 4, "moderate": 3, "weak": 2, "none": 1}
                if priority.get(coverage_level, 0) > priority.get(current, 0):
                    control_coverage[control_id] = coverage_level
        
        strong_count = sum(1 for l in control_coverage.values() if l == "strong")
        moderate_count = sum(1 for l in control_coverage.values() if l == "moderate")
        weak_count = sum(1 for l in control_coverage.values() if l == "weak")
        addressed = len(control_coverage)
        not_addressed = max(0, total_controls - addressed)
        no_coverage = sum(1 for l in control_coverage.values() if l == "none") + not_addressed
        
        return {
            "strong": round((strong_count / total_controls) * 100, 1) if total_controls > 0 else 0,
            "moderate": round((moderate_count / total_controls) * 100, 1) if total_controls > 0 else 0,
            "weak": round((weak_count / total_controls) * 100, 1) if total_controls > 0 else 0,
            "none": round((no_coverage / total_controls) * 100, 1) if total_controls > 0 else 0,
            "calculation_method": "control_based"
        }
    else:
        # LEGACY: Question-based calculation
        strong_count = 0
        moderate_count = 0
        weak_count = 0
        no_coverage_count = 0
        
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
                no_coverage_count += 1
        
        mapped_questions = len(framework_data)
        unmapped_questions = max(0, TOTAL_QUESTIONS - mapped_questions)
        no_coverage_count += unmapped_questions
        
        total = TOTAL_QUESTIONS
        
        return {
            "strong": round((strong_count / total) * 100, 1) if total > 0 else 0,
            "moderate": round((moderate_count / total) * 100, 1) if total > 0 else 0,
            "weak": round((weak_count / total) * 100, 1) if total > 0 else 0,
            "none": round((no_coverage_count / total) * 100, 1) if total > 0 else 0,
            "calculation_method": "question_based"
        }


def get_framework_coverage(
    framework_id: str,
    answers: Optional[List[Dict[str, Any]]] = None
) -> Optional[Dict[str, Any]]:
    """Get complete framework coverage data for a single framework."""
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
        "total_controls": inherent.get("total_controls"),
        "controls_addressed": inherent.get("controls_addressed"),
        "calculation_method": inherent.get("calculation_method"),
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
    """Get framework coverage data for all frameworks."""
    results = []
    
    for framework_id in FRAMEWORK_CONFIG:
        coverage = get_framework_coverage(framework_id, answers)
        if coverage:
            framework_title = FRAMEWORK_CONFIG[framework_id]["title"]
            is_selected = True
            
            if selected_frameworks is not None:
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
    """Get summary information from the master control registry."""
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
    normalized = re.sub(r'\s*\(\d{4}[^)]*\)\s*', '', name).strip().lower()
    return normalized
