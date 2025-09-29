#!/usr/bin/env python3

# Build complete questions file from CSV data
import re

def parse_predefined_answers(answers_text):
    """Parse the pre-defined answers text into separate components"""
    lines = answers_text.strip().split('\n')
    answers = {
        'ideal': '',
        'good': '',
        'basic': '',
        'non_ideal': ''
    }
    
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

# Domain mapping
domain_mapping = {
    "Fairness": 1, "Transparency": 2, "Explainability": 3, "Accountability": 4,
    "Data Integrity": 5, "Reliability": 6, "Security": 7, "Privacy": 8,
    "Safety": 9, "Inclusivity": 10, "Sustainability": 11
}

# Sample data structure - we need to complete this with all 88 questions
questions = []

# Complete FA-1 as template
fa1_data = {
    "domain": "Fairness",
    "code": "FA-1",
    "text": "What measures have you implemented to identify and mitigate biases in your AI system?",
    "explanation": "Bias in AI systems can lead to unfair treatment or exclusion of certain groups, undermining the credibility and effectiveness of the system. This question seeks to determine what proactive steps you've taken to identify and reduce biases. Measures might include bias detection tools, manual data reviews, or conducting fairness audits throughout the development lifecycle.\n\nFor example, if an AI system is used for hiring, it could favor certain demographics based on historical biases in the training data. Mitigation strategies could involve rebalancing datasets, removing biased features, or incorporating fairness constraints into model training.",
    "predefined_answers": "Ideal: Regularly audit datasets for imbalances or biases and use tools like Fairlearn to detect and mitigate issues.\nGood: Implement fairness constraints during model training and review model outcomes for biases before deployment.\nBasic: Conduct ad hoc reviews of the system to check for fairness concerns.\nNon-Ideal: No specific measures have been implemented yet.\nOther: (Please specify.)"
}

def format_question(data):
    """Format question data into Python dict structure"""
    answers = parse_predefined_answers(data['predefined_answers'])
    order = int(data['code'].split('-')[1])
    domain_order = domain_mapping[data['domain']]
    
    return {
        "code": data['code'],
        "text": data['text'],
        "explanation": data['explanation'],
        "ideal_answer": answers['ideal'],
        "good_answer": answers['good'],
        "basic_answer": answers['basic'],
        "non_ideal_answer": answers['non_ideal'],
        "domain_order": domain_order,
        "order": order
    }

# Test with FA-1
result = format_question(fa1_data)
print("FA-1 formatted correctly:")
print(f"Code: {result['code']}")
print(f"Ideal: {result['ideal_answer']}")
print("Ready to build full dataset!")