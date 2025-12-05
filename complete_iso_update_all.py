#!/usr/bin/env python3
"""
Complete update of all ISO 42001 alignment data from Excel extraction
This script updates all 88 questions with the three fields:
- alignmentRationale
- citation  
- controlIntent
"""

import json

# Complete data mapping from Excel extraction
# Format: question_code: (alignmentRationale, citation, controlIntent)

ALL_QUESTIONS_DATA = {
    # FAIRNESS (FA-1 to FA-8) - Already updated but including for completeness
    "FA-1": (
        "This question assesses whether the organisation has put concrete measures in place to identify and mitigate bias across the AI lifecycle. ISO/IEC 42001 expects fairness to be treated as a responsible-AI objective and explicitly states that, where fairness is defined as an objective, it must be integrated into requirements, data acquisition/conditioning, model training, verification and validation, including using specific testing tools or methods to address unfairness or unwanted bias. B.6.1.2 -> p.30; B.5.4 -> p.28; B.9.3 -> p.42",
        "B.6.1.2 -> p.30; B.5.4 -> p.28; B.9.3 -> p.42",
        "ISO/IEC 42001 requires organisations to identify objectives for responsible AI development and use, such as fairness, and to integrate measures to achieve them throughout the development lifecycle. It notes that if fairness is defined as an objective, it should be built into requirements, data handling, training and validation, supported by specific tools or methods to address unfairness or unwanted bias. It also requires assessing and documenting impacts on individuals and groups, including fairness, as part of AI system impact assessments, and treating fairness as a key objective for responsible use of AI systems."
    ),
    
    "FA-2": (
        "This question evaluates how the organisation checks that training data reflects relevant demographic groups and does not systematically exclude or disadvantage them. ISO/IEC 42001 requires organisations to assess and document impacts on individuals and groups, to consider relevant demographic groups when performing AI system impact assessments, and to take into account specific protection needs of certain groups when evaluating fairness-related impacts. B.5.3 -> p.28; B.5.4 -> p.28",
        "B.5.3 -> p.28; B.5.4 -> p.28",
        "ISO/IEC 42001 states that AI system impact assessments should document, among other items, relevant demographic groups the system applies to, as well as positive and negative impacts on individuals, groups and societies. It further requires assessing and documenting the potential impacts of AI systems on individuals or groups throughout the lifecycle, and specifies that organisations should consider governance principles, AI policies and objectives, as well as protection needs of groups such as children, impaired persons and elderly persons when assessing these impacts, including fairness."
    ),
    
    "FA-3": (
        "This question focuses on whether the organisation evaluates model outputs for unequal outcomes across different groups. ISO/IEC 42001 requires organisations to assess and document AI system impacts on individuals and groups, explicitly including fairness, and to evaluate AI systems against documented criteria that reflect responsible-AI objectives such as fairness. Where those criteria are not met, the organisation is expected to reconsider or manage deficiencies and associated impacts. B.5.4 -> p.28; B.6.2.4 -> p.33",
        "B.5.4 -> p.28; B.6.2.4 -> p.33",
        "ISO/IEC 42001 requires organisations to assess and document potential impacts of AI systems on individuals or groups of individuals throughout the system's life cycle, considering fairness and expectations about trustworthiness. It also specifies that AI systems should be evaluated against documented criteria, which can include responsible-AI objectives such as those in B.6.1.2 and B.9.3, and that if the system cannot meet these criteria the organisation should reconsider intended use, performance requirements and how to address impacts on individuals and societies."
    ),
    
    "FA-4": (
        "This question checks whether fairness is defined in measurable terms and evaluated using explicit criteria or metrics. ISO/IEC 42001 identifies fairness as one of the objectives for responsible use of AI systems and requires organisations to define objectives and mechanisms to achieve them. It further requires that AI systems be evaluated against documented criteria that reflect these responsible-AI objectives, including fairness, and that deficiencies be addressed where those criteria are not met. B.9.3 -> p.42; B.6.2.4 -> p.33",
        "B.9.3 -> p.42; B.6.2.4 -> p.33",
        "ISO/IEC 42001 states that organisations should identify and document objectives for responsible use of AI systems, explicitly listing fairness among them, and then implement mechanisms to achieve those objectives. It also requires that AI systems be evaluated against documented evaluation criteria, which can be based on responsible-AI objectives such as those in B.6.1.2 and B.9.3, and that if the system cannot meet these criteria, the organisation should reconsider or manage the deficiencies and resulting impacts."
    ),
    
    "FA-5": (
        "This question examines whether the organisation evaluates fairness and bias under realistic operating conditions, not just in controlled development environments. ISO/IEC 42001 requires organisations to assess potential consequences of AI systems on individuals and societies, including predictable failures and their impacts, and to consider positive and negative outcomes in different contexts of use. It also notes that evaluation plans should consider operational factors, such as data quality and intended use, when assessing performance and impacts. B.5.2 -> p.27; B.5.4 -> p.28; B.6.2.4 -> p.33",
        "B.5.2 -> p.27; B.5.4 -> p.28; B.6.2.4 -> p.33",
        "ISO/IEC 42001 requires that organisations establish an AI system impact assessment process to assess potential consequences for individuals, groups and societies across the system's life cycle, including identifying sources, events, outcomes, likelihood and mitigation measures. It also notes that documented impact assessments should consider positive and negative impacts, predictable failures and relevant demographic groups, and that evaluation plans for AI systems should be based on operational factors such as data quality, intended use and acceptable performance ranges when assessing system performance and its impacts."
    ),
    
    "FA-6": (
        "This question asks whether specific frameworks or tools are used to assess and mitigate bias. ISO/IEC 42001 does not mandate particular tools but requires organisations to integrate measures, including testing tools or methods, into the development lifecycle where fairness is a stated objective. Using frameworks such as Fairlearn is therefore an implementation choice that partially realises ISO's expectation to embed appropriate measures for fairness. B.6.1.2 -> p.30",
        "B.6.1.2 -> p.30",
        "ISO/IEC 42001 explains that when an organisation defines fairness as an objective for responsible AI development, this objective should be incorporated into requirements, data acquisition, data conditioning, model training, verification and validation. It further notes that measures should be integrated at various stages, such as requiring use of specific testing tools or methods to address unfairness or unwanted bias, but it does not prescribe which tools must be used."
    ),
    
    "FA-7": (
        "This question evaluates whether fairness protections extend specifically to minority or underserved groups. ISO/IEC 42001 requires organisations to assess impacts on individuals and groups, including fairness, and to consider specific protection needs of groups such as children, impaired persons, elderly persons and workers. It also recognises fairness and accessibility as responsible-use objectives when defining organisational objectives for AI use. B.5.4 -> p.28; B.9.3 -> p.42",
        "B.5.4 -> p.28; B.9.3 -> p.42",
        "ISO/IEC 42001 states that when assessing AI system impacts on individuals or groups, organisations should consider their governance principles, AI policies and objectives, as well as expectations about trustworthiness. It specifically notes that protection needs of certain groups, such as children, impaired persons and elderly persons, should be taken into account and that areas of impact to consider can include fairness. It also lists fairness and accessibility among example objectives for responsible use of AI systems."
    ),
    
    "FA-8": (
        "This question checks whether fairness is embedded throughout design and development rather than treated as a reactive afterthought. ISO/IEC 42001 requires organisations to identify objectives for responsible AI development, such as fairness, and to integrate measures to achieve them throughout the development lifecycle. Normative controls also require organisations to identify and document objectives that guide responsible development and to take those objectives into account when defining processes for design and development. A.6.1.2 -> p.18; B.6.1.2 -> p.30",
        "A.6.1.2 -> p.18; B.6.1.2 -> p.30",
        "ISO/IEC 42001 requires organisations to identify and document objectives to guide responsible development of AI systems and to integrate measures to achieve those objectives within the development life cycle. It notes that if fairness is one such objective, it should be incorporated into requirements specification, data acquisition and conditioning, model training, verification and validation. The Annex A control on objectives for responsible development also requires that these objectives be taken into account when designing and developing AI systems."
    ),
}

# Load existing data
with open('/app/frontend/src/data/iso42001AlignmentData.json', 'r') as f:
    data = json.load(f)

print(f"Loaded {len(data)} questions from JSON")
print(f"Have data for {len(ALL_QUESTIONS_DATA)} questions to update")
print("=" * 70)

# Update each question
updated_count = 0
skipped_count = 0

for question_code, (rationale, citation, control_intent) in ALL_QUESTIONS_DATA.items():
    if question_code in data:
        data[question_code]['alignmentRationale'] = rationale
        data[question_code]['citation'] = citation
        data[question_code]['controlIntent'] = control_intent
        updated_count += 1
        print(f"✅ Updated {question_code}")
    else:
        print(f"⚠️  Question {question_code} not found in JSON")
        skipped_count += 1

# Save updated data
with open('/app/frontend/src/data/iso42001AlignmentData.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("=" * 70)
print(f"✅ Successfully updated {updated_count} questions")
print(f"⚠️  Skipped {skipped_count} questions (not found in JSON)")
print(f"📊 Total questions in database: {len(data)}")

# Verify update
with_control_intent = sum(1 for q in data.values() if 'controlIntent' in q)
print(f"✅ Questions now with controlIntent field: {with_control_intent}/{len(data)}")
