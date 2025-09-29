#!/usr/bin/env python3

# This script processes the CSV data and creates the complete_questions.py file
csv_data = '''Domain,Question ID,Question,Explanation,Pre-defined Answers
Fairness,FA-1,What measures have you implemented to identify and mitigate biases in your AI system?,"Bias in AI systems can lead to unfair treatment or exclusion of certain groups, undermining the credibility and effectiveness of the system. This question seeks to determine what proactive steps you've taken to identify and reduce biases. Measures might include bias detection tools, manual data reviews, or conducting fairness audits throughout the development lifecycle.

For example, if an AI system is used for hiring, it could favor certain demographics based on historical biases in the training data. Mitigation strategies could involve rebalancing datasets, removing biased features, or incorporating fairness constraints into model training.","Ideal: Regularly audit datasets for imbalances or biases and use tools like Fairlearn to detect and mitigate issues.
Good: Implement fairness constraints during model training and review model outcomes for biases before deployment.
Basic: Conduct ad hoc reviews of the system to check for fairness concerns.
Non-Ideal: No specific measures have been implemented yet.
Other: (Please specify.)"'''

# Domain mapping for order
domain_mapping = {
    "Fairness": 1,
    "Transparency": 2,
    "Explainability": 3,
    "Accountability": 4,
    "Data Integrity": 5,
    "Reliability": 6,
    "Security": 7,
    "Privacy": 8,
    "Safety": 9,
    "Inclusivity": 10,
    "Sustainability": 11
}

def parse_predefined_answers(answers_text):
    """Parse the pre-defined answers text into separate components"""
    lines = answers_text.strip().split('\n')
    answers = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith('Ideal:'):
            answers['ideal'] = line[6:].strip()
        elif line.startswith('Good:'):
            answers['good'] = line[5:].strip()
        elif line.startswith('Basic:'):
            answers['basic'] = line[6:].strip()
        elif line.startswith('Non-Ideal:'):
            answers['non_ideal'] = line[10:].strip()
    
    return answers

# For testing - just show the structure for FA-1
def process_question(domain, question_id, question_text, explanation, predefined_answers):
    answers = parse_predefined_answers(predefined_answers)
    
    # Extract order from question ID (e.g., FA-1 -> 1)
    order = int(question_id.split('-')[1])
    domain_order = domain_mapping.get(domain, 1)
    
    return {
        "code": question_id,
        "text": question_text,
        "explanation": explanation,
        "ideal_answer": answers.get('ideal', ''),
        "good_answer": answers.get('good', ''),
        "basic_answer": answers.get('basic', ''),
        "non_ideal_answer": answers.get('non_ideal', ''),
        "domain_order": domain_order,
        "order": order
    }

# Test with FA-1 data
test_result = process_question(
    "Fairness",
    "FA-1", 
    "What measures have you implemented to identify and mitigate biases in your AI system?",
    "Bias in AI systems can lead to unfair treatment or exclusion of certain groups, undermining the credibility and effectiveness of the system. This question seeks to determine what proactive steps you've taken to identify and reduce biases. Measures might include bias detection tools, manual data reviews, or conducting fairness audits throughout the development lifecycle.\n\nFor example, if an AI system is used for hiring, it could favor certain demographics based on historical biases in the training data. Mitigation strategies could involve rebalancing datasets, removing biased features, or incorporating fairness constraints into model training.",
    "Ideal: Regularly audit datasets for imbalances or biases and use tools like Fairlearn to detect and mitigate issues.\nGood: Implement fairness constraints during model training and review model outcomes for biases before deployment.\nBasic: Conduct ad hoc reviews of the system to check for fairness concerns.\nNon-Ideal: No specific measures have been implemented yet.\nOther: (Please specify.)"
)

print("Test result for FA-1:")
print(f"Code: {test_result['code']}")
print(f"Ideal Answer: {test_result['ideal_answer']}")
print("Structure looks correct!")