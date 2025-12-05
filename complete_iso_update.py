#!/usr/bin/env python3
import json

# Complete mapping from Excel data extraction
# Format: question_code: (alignment_rationale, citation, control_intent)

all_updates = {
    # FAIRNESS
    "FA-1": ("This question assesses whether the organisation has put concrete measures in place to identify and mitigate bias across the AI lifecycle. ISO/IEC 42001 expects fairness to be treated as a responsible-AI objective and explicitly states that, where fairness is defined as an objective, it must be integrated into requirements, data acquisition/conditioning, model training, verification and validation, including using specific testing tools or methods to address unfairness or unwanted bias. B.6.1.2 -> p.30; B.5.4 -> p.28; B.9.3 -> p.42",
             "B.6.1.2 -> p.30; B.5.4 -> p.28; B.9.3 -> p.42",
             "ISO/IEC 42001 requires organisations to identify objectives for responsible AI development and use, such as fairness, and to integrate measures to achieve them throughout the development lifecycle. It notes that if fairness is defined as an objective, it should be built into requirements, data handling, training and validation, supported by specific tools or methods to address unfairness or unwanted bias. It also requires assessing and documenting impacts on individuals and groups, including fairness, as part of AI system impact assessments, and treating fairness as a key objective for responsible use of AI systems."),
    
    "FA-2": ("This question evaluates how the organisation checks that training data reflects relevant demographic groups and does not systematically exclude or disadvantage them. ISO/IEC 42001 requires organisations to assess and document impacts on individuals and groups, to consider relevant demographic groups when performing AI system impact assessments, and to take into account specific protection needs of certain groups when evaluating fairness-related impacts. B.5.3 -> p.28; B.5.4 -> p.28",
             "B.5.3 -> p.28; B.5.4 -> p.28",
             "ISO/IEC 42001 states that AI system impact assessments should document, among other items, relevant demographic groups the system applies to, as well as positive and negative impacts on individuals, groups and societies. It further requires assessing and documenting the potential impacts of AI systems on individuals or groups throughout the lifecycle, and specifies that organisations should consider governance principles, AI policies and objectives, as well as protection needs of groups such as children, impaired persons and elderly persons when assessing these impacts, including fairness."),
}

# Load existing data
with open('/app/frontend/src/data/iso42001AlignmentData.json', 'r') as f:
    data = json.load(f)

# Update each question
count = 0
for question_code, (rationale, citation, control_intent) in all_updates.items():
    if question_code in data:
        data[question_code]['alignmentRationale'] = rationale
        data[question_code]['citation'] = citation
        data[question_code]['controlIntent'] = control_intent
        count += 1
        print(f"✅ Updated {question_code}")

# Save updated data
with open('/app/frontend/src/data/iso42001AlignmentData.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Updated {count} questions successfully!")
