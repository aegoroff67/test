#!/usr/bin/env python3
"""
Generate complete Australian AI Ethics Principles (2024) alignment data JSON file
"""
import json

au_ethics_data = {
    # Fairness Domain (FA-1 to FA-8) - All Fully Aligns, High confidence
    "FA-1": {
        "alignmentType": "Fully Aligns",
        "overview": "This question addresses bias identification and mitigation, core to ethical AI.",
        "relevantPrinciples": "Fairness",
        "alignmentDetails": "Directly supports the Fairness principle by ensuring AI systems avoid discrimination.",
        "confidenceLevel": "High",
        "citation": '"Measures should be taken to ensure the AI produced decisions are compliant with anti-discrimination laws." (Fairness principle, paragraph 3)'
    },
    "FA-2": {
        "alignmentType": "Fully Aligns",
        "overview": "Assesses whether AI systems use representative training data.",
        "relevantPrinciples": "Fairness",
        "alignmentDetails": "Addresses a root cause of unfair AI systems—biased training data.",
        "confidenceLevel": "High",
        "citation": '"This is particularly important given concerns about the potential for AI to perpetuate societal injustices and have a disparate impact on vulnerable and underrepresented groups including, but not limited to, groups relating to age, disability, race, sex, intersex status, gender identity and sexual orientation." (Fairness principle, paragraph 2)'
    },
    "FA-3": {
        "alignmentType": "Fully Aligns",
        "overview": "Examines whether organizations test for unequal outcomes across user groups.",
        "relevantPrinciples": "Fairness",
        "alignmentDetails": "Promotes evaluation to detect unfair discrimination in AI outputs.",
        "confidenceLevel": "High",
        "citation": '"AI systems should be inclusive and accessible, and should not involve or result in unfair discrimination against individuals, communities or groups." (Fairness principle, main statement)'
    },
    "FA-4": {
        "alignmentType": "Fully Aligns",
        "overview": "Focuses on how organizations define and measure fairness metrics.",
        "relevantPrinciples": "Fairness",
        "alignmentDetails": "Enables quantifiable assessment of fairness in AI systems.",
        "confidenceLevel": "High",
        "citation": '"Measures should be taken to ensure the AI produced decisions are compliant with anti-discrimination laws." (Fairness principle, paragraph 3)'
    },
    "FA-5": {
        "alignmentType": "Fully Aligns",
        "overview": "Assesses testing in real-world conditions to identify practical biases.",
        "relevantPrinciples": "Fairness",
        "alignmentDetails": "Ensures fairness is evaluated in actual deployment contexts.",
        "confidenceLevel": "High",
        "citation": '"This includes both appropriate consultation with stakeholders, who may be affected by the AI system throughout its lifecycle, and ensuring people receive equitable access and treatment." (Fairness principle, paragraph 1)'
    },
    "FA-6": {
        "alignmentType": "Fully Aligns",
        "overview": "Evaluates use of structured approaches for bias detection and mitigation.",
        "relevantPrinciples": "Fairness",
        "alignmentDetails": "Promotes systematic fairness assessment using established tools.",
        "confidenceLevel": "High",
        "citation": '"Measures should be taken to ensure the AI produced decisions are compliant with anti-discrimination laws." (Fairness principle, paragraph 3)'
    },
    "FA-7": {
        "alignmentType": "Fully Aligns",
        "overview": "Specifically addresses fairness for vulnerable populations.",
        "relevantPrinciples": "Fairness",
        "alignmentDetails": "Directly addresses concerns about disparate impacts on underrepresented groups.",
        "confidenceLevel": "High",
        "citation": '"This is particularly important given concerns about the potential for AI to perpetuate societal injustices and have a disparate impact on vulnerable and underrepresented groups including, but not limited to, groups relating to age, disability, race, sex, intersex status, gender identity and sexual orientation." (Fairness principle, paragraph 2)'
    },
    "FA-8": {
        "alignmentType": "Fully Aligns",
        "overview": "Examines whether fairness is proactive or reactive in the AI lifecycle.",
        "relevantPrinciples": "Fairness",
        "alignmentDetails": "Supports lifecycle approach to fairness emphasized in the principles.",
        "confidenceLevel": "High",
        "citation": '"Throughout their lifecycle, AI systems should be inclusive and accessible, and should not involve or result in unfair discrimination against individuals, communities or groups." (Fairness principle, main statement)'
    }
}

# Output JSON to stdout
print(json.dumps(au_ethics_data, indent=2))
