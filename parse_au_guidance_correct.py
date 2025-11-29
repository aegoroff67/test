import json
import re

# Function to parse reasoning text into rationale and citation
def parse_reasoning(reasoning_text, citation_ref):
    """
    Parse the reasoning text to separate:
    - Rationale: Text before the quoted section
    - Citation: Quoted text + citation reference
    """
    # Find quoted text using regex (text between quotes)
    quote_pattern = r'"([^"]+)"'
    match = re.search(quote_pattern, reasoning_text)
    
    if match:
        quoted_text = match.group(1)
        # Get text before the quote as rationale
        rationale = reasoning_text[:match.start()].strip()
        # Combine quoted text with citation reference
        citation = f'"{quoted_text}" {citation_ref}'
    else:
        # If no quotes found, use reasoning as rationale and citation ref only
        rationale = reasoning_text.strip()
        citation = citation_ref
    
    return rationale, citation

# All data extracted from spreadsheet
raw_data = {
    "FA-1": {
        "alignment": "Fully Aligns",
        "reasoning": 'Directly addresses bias identification and mitigation which is central to Practice 2 "AI systems can learn from and amplify existing issues such as unwanted bias in data. This can lead to unfair decisions or inappropriate generated content that could affect many people."',
        "citation_ref": "(Foundations, Practice 2, p.6)"
    },
    "FA-2": {
        "alignment": "Fully Aligns",
        "reasoning": 'Aligns with requirements for representative data "For each AI use case: Define and document the data quality, data/model provenance and data preparation requirements."',
        "citation_ref": "(Implementation Practice 5.4.2a, p.34)"
    },
    "FA-3": {
        "alignment": "Fully Aligns",
        "reasoning": 'Directly relates to evaluating outputs for disparities across user groups "For each AI system, engage stakeholders to identify and document the potential benefits and harms to different types of stakeholders, including... risks of unwanted bias or discriminatory outputs"',
        "citation_ref": "(Implementation Practice 2.1.5b, p.23)"
    },
    "FA-4": {
        "alignment": "Fully Aligns",
        "reasoning": 'Aligns with measuring fairness in AI outputs "Carry out a stakeholder impact assessment. Identify the groups and types of people your AI systems may affect... Assess all potential impacts, such as unfair decisions"',
        "citation_ref": "(Foundations, Practice 2.1, p.6)"
    },
    "FA-5": {
        "alignment": "Fully Aligns",
        "reasoning": 'Testing for biases in real-world scenarios aligns with testing requirements "Test before you deploy a system. Consider how you want to use your AI system. Decide how you might test the system to ensure it is performing how you want it to, and conduct them."',
        "citation_ref": "(Foundations, Practice 5.2, p.9)"
    },
    "FA-6": {
        "alignment": "Partially Aligns",
        "reasoning": 'Use of specific frameworks like Fairlearn is not explicitly mentioned, though general fairness assessment is covered "Conduct risk assessments and create mitigation plans for each specific use case and identified impacts in that context."',
        "citation_ref": "(Foundations, Practice 3.3, p.7)"
    },
    "FA-7": {
        "alignment": "Fully Aligns",
        "reasoning": 'Ensuring fairness for minority groups aligns with guidance "Pay particular attention to vulnerable or marginalised cohorts."',
        "citation_ref": "(Foundations, Practice 2.1, p.6)"
    },
    "FA-8": {
        "alignment": "Fully Aligns",
        "reasoning": 'Embedding fairness in design aligns with guidance principles "Document and communicate the organisation\'s commitment to preventing harms to people from AI models and systems and upholding diversity, inclusion and fairness."',
        "citation_ref": "(Implementation Practice 2.1.3, p.23)"
    },
    "TR-1": {
        "alignment": "Fully Aligns",
        "reasoning": 'Directly addresses transparency about system capabilities and limitations "Identify, document and communicate AI system capabilities and limitations. Explaining these capabilities and limitations to relevant stakeholders can prevent their overreliance on or misuse of AI."',
        "citation_ref": "(Foundations, Practice 4.3, p.8)"
    },
    "TR-2": {
        "alignment": "Fully Aligns",
        "reasoning": 'Aligns with documentation requirements "Create and maintain an up-to-date, organisation-wide inventory of each AI model and system, with sufficient detail to inform key stakeholders..."',
        "citation_ref": "(Implementation Practice 4.1.1, p.29)"
    },
    "TR-3": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses transparency for external parties "Create, document, implement and communicate a policy and process for how to transparently communicate to AI users, and affected stakeholders that engage directly with AI systems"',
        "citation_ref": "(Implementation Practice 4.2.1a, p.30)"
    },
    "TR-4": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on information sharing "This should include when and how frequently to communicate, the level of detail and the level of AI knowledge of AI users and affected stakeholders."',
        "citation_ref": "(Implementation Practice 4.2.1b, p.30)"
    },
    "TR-5": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses "black box" components that impede transparency "Wherever possible choose more interpretable and explainable systems."',
        "citation_ref": "(Implementation Practice 4.2.4, p.30)"
    },
    "TR-6": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses disclosure of data sources and algorithms "Document or request from upstream providers the technical details of the system or model that may be required to meet the needs of users within the organisation or stakeholders."',
        "citation_ref": "(Implementation Practice 4.3.1, p.31)"
    },
    "TR-7": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on user awareness of AI interaction "Disclose your use of AI. Make it standard practice in your organisation to clearly communicate your use of AI to your stakeholders."',
        "citation_ref": "(Foundations, Practice 4.2, p.8)"
    },
    "TR-8": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses transparency reporting "For use cases requiring enhanced practices and GPAI systems, conduct independent (internal or external) and thorough review of testing and evaluation methodologies and results. Document and report any issues to the accountable person for the system."',
        "citation_ref": "(Implementation Practice 5.3.2, p.34)"
    },
    "EX-1": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses determining appropriate level of explainability "For each AI system, evaluate and document: the transparency and explainability system requirements and measures – including for third-party -provided systems – dependent on use case, stakeholder requirements and risks arising from disclosure."',
        "citation_ref": "(Implementation Practice 4.2.2b, p.30)"
    },
    "EX-2": {
        "alignment": "Partially Aligns",
        "reasoning": 'Testing understandability for non-technical users is implied but not explicitly detailed "Set up ways to explain AI outcomes, especially when they affect people. The detail in your explanation should match how serious the outcome is, and it should be easy for people who are affected to understand."',
        "citation_ref": "(Foundations, Practice 4.5, p.8)"
    },
    "EX-3": {
        "alignment": "Partially Aligns",
        "reasoning": 'Multiple explanation formats are implied but not explicitly detailed "Set up ways to explain AI outcomes, especially when they affect people. The detail in your explanation should match how serious the outcome is, and it should be easy for people who are affected to understand."',
        "citation_ref": "(Foundations, Practice 4.5, p.8)"
    },
    "EX-4": {
        "alignment": "Fully Aligns",
        "reasoning": 'Evaluating explanation accuracy aligns with guidance "Implement and document system-level mechanisms to enable contestability of AI use and decisions, enabling stakeholders to understand, challenge and appeal AI use and decisions."',
        "citation_ref": "(Implementation Practice 2.2.2, p.24)"
    },
    "EX-5": {
        "alignment": "Partially Aligns",
        "reasoning": 'Trade-offs between complexity and explainability are implied but not explicitly detailed "Wherever possible choose more interpretable and explainable systems."',
        "citation_ref": "(Implementation Practice 4.2.4, p.30)"
    },
    "EX-6": {
        "alignment": "Fully Aligns",
        "reasoning": 'Ensuring interpretable decisions aligns with guidance "Set up ways to explain AI outcomes, especially when they affect people. The detail in your explanation should match how serious the outcome is, and it should be easy for people who are affected to understand."',
        "citation_ref": "(Foundations, Practice 4.5, p.8)"
    },
    "EX-7": {
        "alignment": "Partially Aligns",
        "reasoning": 'Specific explainability tools like SHAP or LIME aren\'t explicitly mentioned, though explainability is emphasized "Wherever possible, provide reasonably interpretable and explainable AI systems and models to accountable people within the organisation or downstream deployers to enable them to meet their own regulatory obligations."',
        "citation_ref": "(Implementation Practice 4.2.5, p.30)"
    },
    "EX-8": {
        "alignment": "Fully Aligns",
        "reasoning": 'Tailoring explanations for specific groups aligns with guidance "The detail in your explanation should match how serious the outcome is, and it should be easy for people who are affected to understand."',
        "citation_ref": "(Foundations, Practice 4.5, p.8)"
    },
    "AC-1": {
        "alignment": "Fully Aligns",
        "reasoning": 'Directly addresses accountability for AI failures "To ensure AI systems perform as required and obligations are met, assign, document and clearly communicate who is accountable across the organisation..."',
        "citation_ref": "(Implementation Practice 1.1.1, p.20)"
    },
    "AC-2": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses governance structures for monitoring AI outcomes "Establish oversight mechanisms to review and approve testing methodologies and results, and to monitor system performance, user feedback and operational impacts post-deployment."',
        "citation_ref": "(Implementation Practice 5.1.1, p.33)"
    },
    "AC-3": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on policies for escalating AI issues "Establish and document response processes for addressing all foreseeable issues and harms during system operation."',
        "citation_ref": "(Implementation Practice 5.2.3, p.33)"
    },
    "AC-4": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses handling customer complaints about AI outputs "Create, document and communicate a process for potentially affected stakeholders to raise concerns, challenges, or requests for remediation and receive responses."',
        "citation_ref": "(Implementation Practice 2.2.1a, p.24)"
    },
    "AC-5": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses defined roles and responsibilities "For each accountable person, define and communicate the required competencies and their authority. Ensure they are staffed with appropriately skilled people and have the necessary resources."',
        "citation_ref": "(Implementation Practice 1.1.2, p.20)"
    },
    "AC-6": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on monitoring and managing AI throughout lifecycle "Identify, document and communicate accountability for shared responsibility across the AI supply chain...for monitoring and evaluation of model and system performance, quality and safety."',
        "citation_ref": "(Implementation Practice 1.2.1a, p.21)"
    },
    "AC-7": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses audit trails for decision-making "Track, document and report relevant information about serious incidents and possible corrective measures to relevant regulators and/or the public in a reasonable timeframe."',
        "citation_ref": "(Implementation Practice 3.4.1, p.28)"
    },
    "AC-8": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses mechanisms for dispute resolution "Implement and document system-level mechanisms to enable contestability of AI use and decisions, enabling stakeholders to understand, challenge and appeal AI use and decisions."',
        "citation_ref": "(Implementation Practice 2.2.2, p.24)"
    },
    "DI-1": {
        "alignment": "Fully Aligns",
        "reasoning": 'Directly addresses data validation and quality "Define and document the data quality, data/model provenance and data preparation requirements."',
        "citation_ref": "(Implementation Practice 5.4.2a, p.34)"
    },
    "DI-2": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses data lineage management "For each AI use case: Understand and document the data sources and collection processes each AI model / system relies on to function including personal and sensitive data."',
        "citation_ref": "(Implementation Practice 5.4.2b, p.35)"
    },
    "DI-3": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on data governance policies "Implement and evaluate the effectiveness of policies and procedures in addressing AI-specific risks: Data governance processes covering the use of data with AI models and systems."',
        "citation_ref": "(Implementation Practice 5.4.1a, p.34)"
    },
    "DI-4": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses ensuring data currency and accuracy "Define and document the data quality, data/model provenance and data preparation requirements."',
        "citation_ref": "(Implementation Practice 5.4.2a, p.34)"
    },
    "DI-5": {
        "alignment": "Partially Aligns",
        "reasoning": 'Handling missing data is implied but not explicitly detailed "Define and document the data quality, data/model provenance and data preparation requirements."',
        "citation_ref": "(Implementation Practice 5.4.2a, p.34)"
    },
    "DI-6": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on data preprocessing management "Define and document the data quality, data/model provenance and data preparation requirements."',
        "citation_ref": "(Implementation Practice 5.4.2a, p.34)"
    },
    "DI-7": {
        "alignment": "Partially Aligns",
        "reasoning": 'Evaluation of third-party data is implied but not explicitly detailed "Understand and document the data sources and collection processes each AI model / system relies on to function."',
        "citation_ref": "(Implementation Practice 5.4.2b, p.35)"
    },
    "DI-8": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on tracking data lineage for traceability "Put in place systems to manage the data and document the data used to train and test each AI model or systems and data used for inference."',
        "citation_ref": "(Implementation Practice 5.4.2b, p.35)"
    },
    "RE-1": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses testing for consistent performance "Test before you deploy a system. Consider how you want to use your AI system. Decide how you might test the system to ensure it is performing how you want it to, and conduct them."',
        "citation_ref": "(Foundations, Practice 5.2, p.9)"
    },
    "RE-2": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on stress testing and simulations "Stress-test your AI system to spot issues or vulnerabilities before others do. Make sure safety, security and policy controls are sound, even when someone deliberately tries to break or bypass them."',
        "citation_ref": "(Foundations, Practice 5.5, p.9)"
    },
    "RE-3": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses monitoring for model drift "Monitor your system after you deploy it. Set up a monitoring process that helps you detect changes in performance and behaviour."',
        "citation_ref": "(Foundations, Practice 5.3, p.9)"
    },
    "RE-4": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on defining success metrics "Define and communicate clear acceptance criteria and test methodologies that reflect the intended use, context and potential risks."',
        "citation_ref": "(Implementation Practice 5.1.2, p.33)"
    },
    "RE-5": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses identifying potential failure points "Define and determine: the criteria or reasons that termination of an AI model or system might need to occur, and at what point intervention should take place."',
        "citation_ref": "(Implementation Practice 6.2.1a, p.36)"
    },
    "RE-6": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on consistent performance under varying conditions "Test before you deploy a system. Consider how you want to use your AI system. Decide how you might test the system to ensure it is performing how you want it to, and conduct them."',
        "citation_ref": "(Foundations, Practice 5.2, p.9)"
    },
    "RE-7": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses mechanisms for detecting system errors "Establish and document response processes for addressing all foreseeable issues and harms during system operation."',
        "citation_ref": "(Implementation Practice 5.2.3, p.33)"
    },
    "RE-8": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses regular testing and retraining "Establish regular system performance review cycles with stakeholders and subject matter experts to evaluate testing criteria, effectiveness and outcomes."',
        "citation_ref": "(Implementation Practice 5.2.4, p.33)"
    },
    "SE-1": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses protecting AI models from unauthorized access "Define and document processes for protecting AI models and systems to address emerging cybersecurity and privacy risks."',
        "citation_ref": "(Implementation Practice 5.4.2c, p.35)"
    },
    "SE-2": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses handling adversarial risks "Conduct safety evaluations that scale with model capabilities, for example: assessment for cyber-offensive capabilities and vulnerabilities... testing for jailbreaking or prompt manipulation."',
        "citation_ref": "(Implementation Practice 5.3.1, p.34)"
    },
    "SE-3": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on security audits "Create a process for and determine whether an AI system requires regular auditing, appropriate to the level of risk identified by its risk assessment. Conduct audits when required."',
        "citation_ref": "(Implementation Practice 5.3.3, p.34)"
    },
    "SE-4": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses securing AI models throughout lifecycle "Define and document processes for protecting AI models and systems to address emerging cybersecurity and privacy risks."',
        "citation_ref": "(Implementation Practice 5.4.2c, p.35)"
    },
    "SE-5": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on preventing unauthorized modifications "Cybersecurity processes to cover the emerging and amplified risks of AI systems interaction with existing systems and data, such as AI systems unintentionally exposing sensitive information or bypassing security controls."',
        "citation_ref": "(Implementation Practice 5.4.1c, p.34)"
    },
    "SE-6": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses protection against adversarial attacks "Conduct safety evaluations that scale with model capabilities, for example: assessment for cyber-offensive capabilities and vulnerabilities...testing for jailbreaking or prompt manipulation."',
        "citation_ref": "(Implementation Practice 5.3.1, p.34)"
    },
    "SE-7": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses protection of sensitive data "Privacy policies covering the collection, use and disclosure of personal or sensitive information by AI models and systems."',
        "citation_ref": "(Implementation Practice 5.4.1b, p.34)"
    },
    "SE-8": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on regular vulnerability assessments "Create a process for and determine whether an AI system requires regular auditing, appropriate to the level of risk identified by its risk assessment. Conduct audits when required."',
        "citation_ref": "(Implementation Practice 5.3.3, p.34)"
    },
    "PR-1": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses compliance with privacy laws "Privacy policies covering the collection, use and disclosure of personal or sensitive information by AI models and systems... This needs to support teams to comply with the Australian Privacy Principles for all AI systems."',
        "citation_ref": "(Implementation Practice 5.4.1b, p.34)"
    },
    "PR-2": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses techniques for protecting personal data "Document how the Australian Privacy Principles have been applied including in models and systems developed by third parties."',
        "citation_ref": "(Implementation Practice 5.4.2e, p.35)"
    },
    "PR-3": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on managing user consent "Privacy policies covering the collection, use and disclosure of personal or sensitive information by AI models and systems."',
        "citation_ref": "(Implementation Practice 5.4.1b, p.34)"
    },
    "PR-4": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses ensuring data used within original purpose "Monitor for and detect any leakage of personal and sensitive information from AI models and systems."',
        "citation_ref": "(Implementation Practice 5.4.2g, p.35)"
    },
    "PR-5": {
        "alignment": "Partially Aligns",
        "reasoning": 'Evaluating privacy protection effectiveness is implied but not explicitly detailed "Document how the Australian Privacy Principles have been applied including in models and systems developed by third parties."',
        "citation_ref": "(Implementation Practice 5.4.2e, p.35)"
    },
    "PR-6": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on monitoring for privacy violations "Monitor for and detect any leakage of personal and sensitive information from AI models and systems."',
        "citation_ref": "(Implementation Practice 5.4.2g, p.35)"
    },
    "PR-7": {
        "alignment": "Partially Aligns",
        "reasoning": 'Evaluating privacy risks throughout lifecycle is implied but not explicitly detailed for both development and deployment "Privacy policies covering the collection, use and disclosure of personal or sensitive information by AI models and systems."',
        "citation_ref": "(Implementation Practice 5.4.1b, p.34)"
    },
    "PR-8": {
        "alignment": "Partially Aligns",
        "reasoning": 'Cross-border data protection is implied but not explicitly addressed "Document how the Australian Privacy Principles have been applied including in models and systems developed by third parties."',
        "citation_ref": "(Implementation Practice 5.4.2e, p.35)"
    },
    "SA-1": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses safety impact assessments "Carry out a stakeholder impact assessment. Identify the groups and types of people your AI systems may affect. Pay particular attention to vulnerable or marginalised cohorts."',
        "citation_ref": "(Foundations, Practice 2.1, p.6)"
    },
    "SA-2": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on preventing unintended harm "Document the scope for each AI system, including intended use cases, foreseeable misuse, capabilities, limitations and expected context."',
        "citation_ref": "(Implementation Practice 2.1.4, p.23)"
    },
    "SA-3": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses real-time monitoring for unsafe behavior "Monitor your system after you deploy it. Set up a monitoring process that helps you detect changes in performance and behaviour."',
        "citation_ref": "(Foundations, Practice 5.3, p.9)"
    },
    "SA-4": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses conflicts between system actions and safety "Build in human override points. Make sure you have clear intervention points where humans can pause, override, roll back or shut down AI systems if needed."',
        "citation_ref": "(Foundations, Practice 6.2, p.10)"
    },
    "SA-5": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on emergency shutdown protocols "Define and determine: the criteria or reasons that termination of an AI model or system might need to occur, and at what point intervention should take place."',
        "citation_ref": "(Implementation Practice 6.2.1a, p.36)"
    },
    "SA-6": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses risk identification and mitigation "Create, document and implement a risk treatment plan to prioritise, select and implement treatment options (e.g. risk avoidance, transfer, acceptance, reduction) and controls to mitigate identified risks."',
        "citation_ref": "(Implementation Practice 3.3.1, p.28)"
    },
    "SA-7": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses fail-safe mechanisms "Build in human override points. Make sure you have clear intervention points where humans can pause, override, roll back or shut down AI systems if needed."',
        "citation_ref": "(Foundations, Practice 6.2, p.10)"
    },
    "SA-8": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on safety testing in high-risk scenarios "Stress-test your AI system to spot issues or vulnerabilities before others do."',
        "citation_ref": "(Foundations, Practice 5.5, p.9)"
    },
    "IN-1": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses system accessibility "How accessibility obligations and commitments are met by implementing human-centered design."',
        "citation_ref": "(Implementation Practice 4.2.2c, p.30)"
    },
    "IN-2": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on diverse perspectives in design "Engage your stakeholders early and continue engaging them throughout the AI lifecycle, especially your staff and customers. Understand their needs, concerns and how they might be affected."',
        "citation_ref": "(Foundations, Practice 2.3, p.6)"
    },
    "IN-3": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses auditing for exclusionary outcomes "For each documented risk of harm to affected stakeholders, conduct appropriate stakeholder impact analysis."',
        "citation_ref": "(Implementation Practice 2.1.6, p.24)"
    },
    "IN-4": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on accessibility requirements "How accessibility obligations and commitments are met by implementing human-centered design."',
        "citation_ref": "(Implementation Practice 4.2.2c, p.30)"
    },
    "IN-5": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses involving diverse stakeholders "Create processes to support ongoing engagement with stakeholders about their experience of AI systems. Identify vulnerable groups and support appropriately."',
        "citation_ref": "(Implementation Practice 2.1.8, p.24)"
    },
    "IN-6": {
        "alignment": "Fully Aligns",
        "reasoning": 'Addresses serving underrepresented communities "Identify and document key types of stakeholders (such as employees and end users) that may be impacted by the organisation\'s development and deployment of AI, and their needs."',
        "citation_ref": "(Implementation Practice 2.1.1, p.23)"
    },
    "IN-7": {
        "alignment": "Partially Aligns",
        "reasoning": 'Language and cultural differences are implied but not explicitly addressed "Equip stakeholders with the skills and tools necessary to give meaningful feedback."',
        "citation_ref": "(Implementation Practice 2.1.8, p.24)"
    },
    "IN-8": {
        "alignment": "Fully Aligns",
        "reasoning": 'Focuses on evaluating exclusion of user groups "For each AI system, engage stakeholders to identify and document the potential benefits and harms to different types of stakeholders, including impacts to vulnerable groups."',
        "citation_ref": "(Implementation Practice 2.1.5a, p.23)"
    },
    "SU-2": {
        "alignment": "Partially Aligns",
        "reasoning": 'Computational efficiency is implied but not directly addressed in environmental context "Providing sufficient resources such as human effort and compute to deploy AI systems safely and responsibly over the lifecycle."',
        "citation_ref": "(Implementation Practice 1.4.2d, p.22)"
    },
    "SU-5": {
        "alignment": "Partially Aligns",
        "reasoning": 'Algorithm optimization is implied but not specifically for environmental reasons "Research, document and implement leading practices in safety measures as safeguards, as appropriate for identified risks."',
        "citation_ref": "(Implementation Practice 3.3.4, p.28)"
    }
}

# Process each entry
final_data = {}
for question_id, data in raw_data.items():
    rationale, citation = parse_reasoning(data["reasoning"], data["citation_ref"])
    final_data[question_id] = {
        "alignmentType": data["alignment"],
        "alignmentRationale": rationale,
        "citation": citation
    }

# Write to JSON file
with open('/app/frontend/src/data/auGuidanceAlignmentData.json', 'w') as f:
    json.dump(final_data, f, indent=2)

print(f"✅ Successfully updated auGuidanceAlignmentData.json")
print(f"Total questions processed: {len(final_data)}")
print(f"\nSample entry (FA-1):")
print(json.dumps(final_data["FA-1"], indent=2))
