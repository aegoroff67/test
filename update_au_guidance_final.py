import json

# Complete data from the updated CSV file
au_guidance_data = {
    "FA-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses bias identification and mitigation which is central to Practice 2",
        "citation": '"AI systems can learn from and amplify existing issues such as unwanted bias in data. This can lead to unfair decisions or inappropriate generated content that could affect many people." (Foundations, Practice 2, p.6)'
    },
    "FA-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Focuses on ensuring training data represents all relevant demographics, which is a key component of data quality requirements",
        "citation": '"For each AI use case: Define and document the data quality, data/model provenance and data preparation requirements." (Implementation Practice 5.4.2a, p.34)'
    },
    "FA-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Evaluating outputs for disparities across groups directly relates to stakeholder impact assessment",
        "citation": '"For each AI system, engage stakeholders to identify and document the potential benefits and harms to different types of stakeholders, including... risks of unwanted bias or discriminatory outputs" (Implementation Practice 2.1.5b, p.23)'
    },
    "FA-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Addresses measuring fairness in AI outputs, which supports impact assessment of unfair decisions",
        "citation": '"Carry out a stakeholder impact assessment. Identify the groups and types of people your AI systems may affect... Assess all potential impacts, such as unfair decisions" (Foundations, Practice 2.1, p.6)'
    },
    "FA-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Testing for biases in real-world scenarios aligns with pre-deployment testing requirements",
        "citation": '"Test before you deploy a system. Consider how you want to use your AI system. Decide how you might test the system to ensure it is performing how you want it to, and conduct them." (Foundations, Practice 5.2, p.9)'
    },
    "FA-6": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Use of specific frameworks like Fairlearn is not explicitly mentioned, though general assessment of bias is covered",
        "citation": '"Conduct risk assessments and create mitigation plans for each specific use case and identified impacts in that context." (Foundations, Practice 3.3, p.7)'
    },
    "FA-7": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Ensuring fairness for minority groups directly aligns with guidance focus on vulnerable populations",
        "citation": '"Pay particular attention to vulnerable or marginalised cohorts." (Foundations, Practice 2.1, p.6)'
    },
    "FA-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Embedding fairness in design aligns with organizational commitment to fairness and harm prevention",
        "citation": '"Document and communicate the organisation\'s commitment to preventing harms to people from AI models and systems and upholding diversity, inclusion and fairness." (Implementation Practice 2.1.3, p.23)'
    },
    "TR-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses transparency about system capabilities and limitations",
        "citation": '"Identify, document and communicate AI system capabilities and limitations. Explaining these capabilities and limitations to relevant stakeholders can prevent their overreliance on or misuse of AI." (Foundations, Practice 4.3, p.8)'
    },
    "TR-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Focuses on comprehensive documentation of data sources, algorithms, and processes",
        "citation": '"Create and maintain an up-to-date, organisation-wide inventory of each AI model and system, with sufficient detail to inform key stakeholders..." (Implementation Practice 4.1.1, p.29)'
    },
    "TR-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Addresses mechanisms for external parties to understand AI systems",
        "citation": '"Create, document, implement and communicate a policy and process for how to transparently communicate to AI users, and affected stakeholders that engage directly with AI systems" (Implementation Practice 4.2.1a, p.30)'
    },
    "TR-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Covers information sharing methods and practices for internal teams and external stakeholders",
        "citation": '"This should include when and how frequently to communicate, the level of detail and the level of AI knowledge of AI users and affected stakeholders." (Implementation Practice 4.2.1b, p.30)'
    },
    "TR-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Addresses interpretability issues related to \"black-box\" components",
        "citation": '"Wherever possible choose more interpretable and explainable systems." (Implementation Practice 4.2.4, p.30)'
    },
    "TR-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Focuses on disclosure of data and algorithm sources",
        "citation": '"Document or request from upstream providers the technical details of the system or model that may be required to meet the needs of users within the organisation or stakeholders." (Implementation Practice 4.3.1, p.31)'
    },
    "TR-7": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses user awareness of AI interaction",
        "citation": '"Disclose your use of AI. Make it standard practice in your organisation to clearly communicate your use of AI to your stakeholders." (Foundations, Practice 4.2, p.8)'
    },
    "TR-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Covers documentation and reporting of AI systems, though comprehensive transparency reports aren't specifically mentioned",
        "citation": '"For use cases requiring enhanced practices and GPAI systems, conduct independent (internal or external) and thorough review of testing and evaluation methodologies and results. Document and report any issues to the accountable person for the system." (Implementation Practice 5.3.2, p.34)'
    },
    "EX-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses determining the appropriate level of explainability for different use cases",
        "citation": '"For each AI system, evaluate and document: the transparency and explainability system requirements and measures – including for third-party -provided systems – dependent on use case, stakeholder requirements and risks arising from disclosure." (Implementation Practice 4.2.2b, p.30)'
    },
    "EX-2": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Testing understandability for non-technical users is implied but specific testing methods aren't detailed",
        "citation": '"Set up ways to explain AI outcomes, especially when they affect people. The detail in your explanation should match how serious the outcome is, and it should be easy for people who are affected to understand." (Foundations, Practice 4.5, p.8)'
    },
    "EX-3": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Providing multiple explanation formats is implied but not explicitly required",
        "citation": '"Set up ways to explain AI outcomes, especially when they affect people. The detail in your explanation should match how serious the outcome is, and it should be easy for people who are affected to understand." (Foundations, Practice 4.5, p.8)'
    },
    "EX-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Evaluating explanation accuracy supports contestability mechanisms",
        "citation": '"Implement and document system-level mechanisms to enable contestability of AI use and decisions, enabling stakeholders to understand, challenge and appeal AI use and decisions." (Implementation Practice 2.2.2, p.24)'
    },
    "EX-5": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Trade-offs between complexity and explainability are implied but not explicitly discussed",
        "citation": '"Wherever possible choose more interpretable and explainable systems." (Implementation Practice 4.2.4, p.30)'
    },
    "EX-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses ensuring interpretable decisions for users",
        "citation": '"Set up ways to explain AI outcomes, especially when they affect people. The detail in your explanation should match how serious the outcome is, and it should be easy for people who are affected to understand." (Foundations, Practice 4.5, p.8)'
    },
    "EX-7": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Explainability tools (SHAP, LIME) aren't explicitly mentioned, though general explainability is required",
        "citation": '"Wherever possible, provide reasonably interpretable and explainable AI systems and models to accountable people within the organisation or downstream deployers to enable them to meet their own regulatory obligations." (Implementation Practice 4.2.5, p.30)'
    },
    "EX-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Tailoring explanations for specific groups aligns with guidance on matching detail to the audience",
        "citation": '"The detail in your explanation should match how serious the outcome is, and it should be easy for people who are affected to understand." (Foundations, Practice 4.5, p.8)'
    },
    "AC-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses accountability for AI system failures and issue management",
        "citation": '"To ensure AI systems perform as required and obligations are met, assign, document and clearly communicate who is accountable across the organisation..." (Implementation Practice 1.1.1, p.20)'
    },
    "AC-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Focuses on governance structures for oversight and monitoring",
        "citation": '"Establish oversight mechanisms to review and approve testing methodologies and results, and to monitor system performance, user feedback and operational impacts post-deployment." (Implementation Practice 5.1.1, p.33)'
    },
    "AC-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Addresses policies for escalating AI issues to appropriate levels",
        "citation": '"Establish and document response processes for addressing all foreseeable issues and harms during system operation." (Implementation Practice 5.2.3, p.33)'
    },
    "AC-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly covers handling customer complaints or disputes",
        "citation": '"Create, document and communicate a process for potentially affected stakeholders to raise concerns, challenges, or requests for remediation and receive responses." (Implementation Practice 2.2.1a, p.24)'
    },
    "AC-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Focuses on clearly defined roles and responsibilities across teams",
        "citation": '"For each accountable person, define and communicate the required competencies and their authority. Ensure they are staffed with appropriately skilled people and have the necessary resources." (Implementation Practice 1.1.2, p.20)'
    },
    "AC-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Addresses lifecycle responsibility for AI system management and monitoring",
        "citation": '"Identify, document and communicate accountability for shared responsibility across the AI supply chain...for monitoring and evaluation of model and system performance, quality and safety." (Implementation Practice 1.2.1a, p.21)'
    },
    "AC-7": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Covers documentation and audit trails for decision-making",
        "citation": '"Track, document and report relevant information about serious incidents and possible corrective measures to relevant regulators and/or the public in a reasonable timeframe." (Implementation Practice 3.4.1, p.28)'
    },
    "AC-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses mechanisms for dispute resolution",
        "citation": '"Implement and document system-level mechanisms to enable contestability of AI use and decisions, enabling stakeholders to understand, challenge and appeal AI use and decisions." (Implementation Practice 2.2.2, p.24)'
    },
    "DI-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses data validation, accuracy, and quality",
        "citation": '"Define and document the data quality, data/model provenance and data preparation requirements." (Implementation Practice 5.4.2a, p.34)'
    },
    "DI-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Addresses data lineage management and tracking changes",
        "citation": '"For each AI use case: Understand and document the data sources and collection processes each AI model / system relies on to function including personal and sensitive data." (Implementation Practice 5.4.2b, p.35)'
    },
    "DI-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Focuses on data governance policies for collection, usage, retention, and disposal",
        "citation": '"Implement and evaluate the effectiveness of policies and procedures in addressing AI-specific risks: Data governance processes covering the use of data with AI models and systems." (Implementation Practice 5.4.1a, p.34)'
    },
    "DI-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Addresses maintaining data currency and accuracy",
        "citation": '"Define and document the data quality, data/model provenance and data preparation requirements." (Implementation Practice 5.4.2a, p.34)'
    },
    "DI-5": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Handling missing data is implied in data quality but not specifically detailed",
        "citation": '"Define and document the data quality, data/model provenance and data preparation requirements." (Implementation Practice 5.4.2a, p.34)'
    },
    "DI-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Covers data preprocessing management as part of data preparation",
        "citation": '"Define and document the data quality, data/model provenance and data preparation requirements." (Implementation Practice 5.4.2a, p.34)'
    },
    "DI-7": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Evaluation of third-party data sources is implied but not specifically detailed",
        "citation": '"Understand and document the data sources and collection processes each AI model / system relies on to function." (Implementation Practice 5.4.2b, p.35)'
    },
    "DI-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Focuses on data traceability across the AI lifecycle",
        "citation": '"Put in place systems to manage the data and document the data used to train and test each AI model or systems and data used for inference." (Implementation Practice 5.4.2b, p.35)'
    },
    "RE-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses testing for consistent performance under different conditions",
        "citation": '"Test before you deploy a system. Consider how you want to use your AI system. Decide how you might test the system to ensure it is performing how you want it to, and conduct them." (Foundations, Practice 5.2, p.9)'
    },
    "RE-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Focuses on stress testing and simulations for robustness",
        "citation": '"Stress-test your AI system to spot issues or vulnerabilities before others do. Make sure safety, security and policy controls are sound, even when someone deliberately tries to break or bypass them." (Foundations, Practice 5.5, p.9)'
    },
    "RE-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Addresses monitoring for model drift and performance degradation",
        "citation": '"Monitor your system after you deploy it. Set up a monitoring process that helps you detect changes in performance and behaviour." (Foundations, Practice 5.3, p.9)'
    },
    "RE-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Covers defining success metrics for system reliability",
        "citation": '"Define and communicate clear acceptance criteria and test methodologies that reflect the intended use, context and potential risks." (Implementation Practice 5.1.2, p.33)'
    },
    "RE-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Addresses identification of potential system failure points",
        "citation": '"Define and determine: the criteria or reasons that termination of an AI model or system might need to occur, and at what point intervention should take place." (Implementation Practice 6.2.1a, p.36)'
    },
    "RE-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Focuses on consistent performance under varying conditions including edge cases",
        "citation": '"Test before you deploy a system. Consider how you want to use your AI system. Decide how you might test the system to ensure it is performing how you want it to, and conduct them." (Foundations, Practice 5.2, p.9)'
    },
    "RE-7": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Covers mechanisms for detecting and addressing system downtime or errors",
        "citation": '"Establish and document response processes for addressing all foreseeable issues and harms during system operation." (Implementation Practice 5.2.3, p.33)'
    },
    "RE-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Addresses regular testing and retraining to maintain model reliability",
        "citation": '"Establish regular system performance review cycles with stakeholders and subject matter experts to evaluate testing criteria, effectiveness and outcomes." (Implementation Practice 5.2.4, p.33)'
    },
    "SE-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses protecting AI models and data from unauthorized access",
        "citation": '"Define and document processes for protecting AI models and systems to address emerging cybersecurity and privacy risks." (Implementation Practice 5.4.2c, p.35)'
    },
    "SE-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Focuses on handling adversarial risks and attacks",
        "citation": '"Conduct safety evaluations that scale with model capabilities, for example: assessment for cyber-offensive capabilities and vulnerabilities... testing for jailbreaking or prompt manipulation." (Implementation Practice 5.3.1, p.34)'
    },
    "SE-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Addresses security audits and testing, though penetration testing isn't explicitly mentioned",
        "citation": '"Create a process for and determine whether an AI system requires regular auditing, appropriate to the level of risk identified by its risk assessment. Conduct audits when required." (Implementation Practice 5.3.3, p.34)'
    },
    "SE-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Covers securing the AI model throughout its lifecycle stages",
        "citation": '"Define and document processes for protecting AI models and systems to address emerging cybersecurity and privacy risks." (Implementation Practice 5.4.2c, p.35)'
    },
    "SE-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Focuses on preventing unauthorized modifications to the AI model",
        "citation": '"Cybersecurity processes to cover the emerging and amplified risks of AI systems interaction with existing systems and data, such as AI systems unintentionally exposing sensitive information or bypassing security controls." (Implementation Practice 5.4.1c, p.34)'
    },
    "SE-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses protection against adversarial attacks",
        "citation": '"Conduct safety evaluations that scale with model capabilities, for example: assessment for cyber-offensive capabilities and vulnerabilities...testing for jailbreaking or prompt manipulation." (Implementation Practice 5.3.1, p.34)'
    },
    "SE-7": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Covers protecting sensitive data in AI pipelines",
        "citation": '"Privacy policies covering the collection, use and disclosure of personal or sensitive information by AI models and systems." (Implementation Practice 5.4.1b, p.34)'
    },
    "SE-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Addresses vulnerability assessments and system security testing",
        "citation": '"Create a process for and determine whether an AI system requires regular auditing, appropriate to the level of risk identified by its risk assessment. Conduct audits when required." (Implementation Practice 5.3.3, p.34)'
    },
    "PR-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses compliance with data privacy laws",
        "citation": '"Privacy policies covering the collection, use and disclosure of personal or sensitive information by AI models and systems... This needs to support teams to comply with the Australian Privacy Principles for all AI systems." (Implementation Practice 5.4.1b, p.34)'
    },
    "PR-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Focuses on techniques to protect personal data, which supports privacy principles",
        "citation": '"Document how the Australian Privacy Principles have been applied including in models and systems developed by third parties." (Implementation Practice 5.4.2e, p.35)'
    },
    "PR-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Addresses management of user consent for data collection and processing",
        "citation": '"Privacy policies covering the collection, use and disclosure of personal or sensitive information by AI models and systems." (Implementation Practice 5.4.1b, p.34)'
    },
    "PR-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Covers ensuring data is not used beyond its original purpose",
        "citation": '"Monitor for and detect any leakage of personal and sensitive information from AI models and systems." (Implementation Practice 5.4.2g, p.35)'
    },
    "PR-5": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Evaluating privacy protection effectiveness is implied but not explicitly detailed",
        "citation": '"Document how the Australian Privacy Principles have been applied including in models and systems developed by third parties." (Implementation Practice 5.4.2e, p.35)'
    },
    "PR-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses monitoring and preventing privacy violations",
        "citation": '"Monitor for and detect any leakage of personal and sensitive information from AI models and systems." (Implementation Practice 5.4.2g, p.35)'
    },
    "PR-7": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Evaluating privacy risks throughout the lifecycle is implied but not comprehensively detailed",
        "citation": '"Privacy policies covering the collection, use and disclosure of personal or sensitive information by AI models and systems." (Implementation Practice 5.4.1b, p.34)'
    },
    "PR-8": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Cross-border data protection is implied under general privacy principles but not explicitly addressed",
        "citation": '"Document how the Australian Privacy Principles have been applied including in models and systems developed by third parties." (Implementation Practice 5.4.2e, p.35)'
    },
    "SA-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses safety impact assessment",
        "citation": '"Carry out a stakeholder impact assessment. Identify the groups and types of people your AI systems may affect. Pay particular attention to vulnerable or marginalised cohorts." (Foundations, Practice 2.1, p.6)'
    },
    "SA-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Focuses on preventing unintended harm from AI systems",
        "citation": '"Document the scope for each AI system, including intended use cases, foreseeable misuse, capabilities, limitations and expected context." (Implementation Practice 2.1.4, p.23)'
    },
    "SA-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Addresses real-time monitoring for unsafe system behavior",
        "citation": '"Monitor your system after you deploy it. Set up a monitoring process that helps you detect changes in performance and behaviour." (Foundations, Practice 5.3, p.9)'
    },
    "SA-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Covers handling conflicts between system actions and human safety",
        "citation": '"Build in human override points. Make sure you have clear intervention points where humans can pause, override, roll back or shut down AI systems if needed." (Foundations, Practice 6.2, p.10)'
    },
    "SA-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses emergency protocols for system shutdown",
        "citation": '"Define and determine: the criteria or reasons that termination of an AI model or system might need to occur, and at what point intervention should take place." (Implementation Practice 6.2.1a, p.36)'
    },
    "SA-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Focuses on risk identification and mitigation strategies",
        "citation": '"Create, document and implement a risk treatment plan to prioritise, select and implement treatment options (e.g. risk avoidance, transfer, acceptance, reduction) and controls to mitigate identified risks." (Implementation Practice 3.3.1, p.28)'
    },
    "SA-7": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Addresses fail-safe mechanisms and redundancies for system safety",
        "citation": '"Build in human override points. Make sure you have clear intervention points where humans can pause, override, roll back or shut down AI systems if needed." (Foundations, Practice 6.2, p.10)'
    },
    "SA-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Covers safety testing in realistic or high-risk scenarios",
        "citation": '"Stress-test your AI system to spot issues or vulnerabilities before others do." (Foundations, Practice 5.5, p.9)'
    },
    "IN-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses system accessibility for diverse users including those with disabilities",
        "citation": '"How accessibility obligations and commitments are met by implementing human-centered design." (Implementation Practice 4.2.2c, p.30)'
    },
    "IN-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Focuses on incorporating diverse perspectives during design and development",
        "citation": '"Engage your stakeholders early and continue engaging them throughout the AI lifecycle, especially your staff and customers. Understand their needs, concerns and how they might be affected." (Foundations, Practice 2.3, p.6)'
    },
    "IN-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Addresses auditing for exclusionary outcomes, which supports impact analysis",
        "citation": '"For each documented risk of harm to affected stakeholders, conduct appropriate stakeholder impact analysis." (Implementation Practice 2.1.6, p.24)'
    },
    "IN-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Covers ensuring accessibility requirements are met",
        "citation": '"How accessibility obligations and commitments are met by implementing human-centered design." (Implementation Practice 4.2.2c, p.30)'
    },
    "IN-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Addresses involvement of diverse stakeholders in design and testing",
        "citation": '"Create processes to support ongoing engagement with stakeholders about their experience of AI systems. Identify vulnerable groups and support appropriately." (Implementation Practice 2.1.8, p.24)'
    },
    "IN-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Focuses on effective service to underrepresented communities",
        "citation": '"Identify and document key types of stakeholders (such as employees and end users) that may be impacted by the organisation\'s development and deployment of AI, and their needs." (Implementation Practice 2.1.1, p.23)'
    },
    "IN-7": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Language, cultural, and regional differences are implied but not explicitly addressed",
        "citation": '"Equip stakeholders with the skills and tools necessary to give meaningful feedback." (Implementation Practice 2.1.8, p.24)'
    },
    "IN-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses evaluating whether the system excludes certain user groups",
        "citation": '"For each AI system, engage stakeholders to identify and document the potential benefits and harms to different types of stakeholders, including impacts to vulnerable groups." (Implementation Practice 2.1.5a, p.23)'
    },
    "SU-2": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Computational efficiency is implied but not specifically for environmental reasons",
        "citation": '"Providing sufficient resources such as human effort and compute to deploy AI systems safely and responsibly over the lifecycle." (Implementation Practice 1.4.2d, p.22)'
    },
    "SU-5": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Algorithm optimization is implied for general purposes but not specifically for environmental impact",
        "citation": '"Research, document and implement leading practices in safety measures as safeguards, as appropriate for identified risks." (Implementation Practice 3.3.4, p.28)'
    }
}

# Write to JSON file
with open('/app/frontend/src/data/auGuidanceAlignmentData.json', 'w') as f:
    json.dump(au_guidance_data, f, indent=2)

print(f"✅ Successfully updated auGuidanceAlignmentData.json with complete data")
print(f"Total questions processed: {len(au_guidance_data)}")
print(f"\nSample entry (FA-1):")
print(json.dumps(au_guidance_data["FA-1"], indent=2))
