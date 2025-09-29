# Remaining domains 6-11 for complete_questions.py

remaining_questions = [
    # Reliability Domain (RE-1 to RE-8) - Domain order 6
    {
        "code": "RE-1",
        "text": "How do you test the AI system to ensure consistent performance under different conditions?",
        "explanation": "AI systems must perform reliably across varied scenarios, environments, and user interactions. This question examines your testing strategies to validate consistent performance.\n\nFor example, an AI-powered navigation system should work reliably whether it's used during rush hour or off-peak times, in different weather conditions, or across diverse geographic locations. Testing approaches might include stress testing, scenario-based testing, and simulation of edge cases to ensure the system maintains performance standards under varying conditions.",
        "ideal_answer": "Conduct comprehensive testing under diverse scenarios, including stress tests and edge cases, with automated testing frameworks.",
        "good_answer": "Perform regular testing under key operational scenarios with both manual and automated approaches.",
        "basic_answer": "Test the system occasionally or only under standard conditions.",
        "non_ideal_answer": "No testing for performance under different conditions is conducted.",
        "domain_order": 6,
        "order": 1
    },
    {
        "code": "RE-2",
        "text": "Have you conducted stress tests or simulations to evaluate the system's robustness?",
        "explanation": "Stress testing pushes an AI system beyond normal operating conditions to identify its breaking points and assess robustness. This question evaluates whether you proactively test your system's limits.\n\nFor instance, a fraud detection system might be stress-tested by simulating a sudden spike in transaction volumes or unusual attack patterns. Such testing helps identify potential failure modes and ensures the system can handle unexpected scenarios without catastrophic failure.",
        "ideal_answer": "Regularly conduct stress tests and simulations to identify failure points and validate system robustness.",
        "good_answer": "Perform stress tests periodically, focusing on key system components or scenarios.",
        "basic_answer": "Conduct stress tests occasionally or only after issues arise.",
        "non_ideal_answer": "No stress testing or robustness evaluation is performed.",
        "domain_order": 6,
        "order": 2
    },
    {
        "code": "RE-3",
        "text": "What mechanisms are in place to monitor the system for issues like model drift or degradation?",
        "explanation": "AI systems can degrade over time as real-world data patterns change, leading to model drift. This question assesses your monitoring capabilities for detecting and addressing such issues.\n\nFor example, a customer behavior prediction model trained on pre-pandemic data might become less accurate as shopping patterns change. Monitoring mechanisms could include performance metrics tracking, data distribution analysis, and automated alerts when performance falls below thresholds.",
        "ideal_answer": "Implement automated monitoring systems that detect model drift, performance degradation, and data distribution changes in real-time.",
        "good_answer": "Monitor key performance metrics regularly and investigate significant changes.",
        "basic_answer": "Perform periodic manual reviews of system performance.",
        "non_ideal_answer": "No monitoring mechanisms are in place for model drift or degradation.",
        "domain_order": 6,
        "order": 3
    },
    {
        "code": "RE-4",
        "text": "How do you define success metrics for the reliability of your AI system?",
        "explanation": "Clear success metrics provide benchmarks for measuring and maintaining AI system reliability. This question examines whether you have defined quantifiable criteria for reliability assessment.\n\nFor instance, reliability metrics for an AI customer service chatbot might include uptime percentage, response accuracy rate, and user satisfaction scores. Well-defined metrics enable you to track performance over time, identify improvement areas, and communicate system reliability to stakeholders.",
        "ideal_answer": "Define comprehensive, quantifiable reliability metrics aligned with business objectives and regularly track performance against these benchmarks.",
        "good_answer": "Establish basic reliability metrics and monitor them periodically.",
        "basic_answer": "Use informal or subjective measures to assess reliability.",
        "non_ideal_answer": "No success metrics for reliability are defined.",
        "domain_order": 6,
        "order": 4
    },
    {
        "code": "RE-5",
        "text": "Have you identified potential failure points in the system?",
        "explanation": "Proactively identifying potential failure points helps prevent system breakdowns and enables you to implement appropriate safeguards. This question assesses whether you conduct failure mode analysis for your AI system.\n\nFor example, in an autonomous vehicle system, potential failure points might include sensor malfunctions, network connectivity loss, or adverse weather conditions. By identifying these risks, you can design redundancies, failsafes, and contingency plans to maintain system reliability.",
        "ideal_answer": "Conduct systematic failure mode analysis to identify and document potential failure points, with mitigation strategies for each.",
        "good_answer": "Identify obvious failure points and implement basic safeguards.",
        "basic_answer": "Address failure points reactively as they are discovered.",
        "non_ideal_answer": "No analysis of potential failure points has been conducted.",
        "domain_order": 6,
        "order": 5
    },
    {
        "code": "RE-6",
        "text": "How do you ensure the system performs consistently under varying conditions (e.g., edge cases)?",
        "explanation": "Consistent performance under varying conditions, including edge cases, is crucial for AI system reliability. This question examines your strategies for maintaining performance across diverse scenarios.\n\nFor instance, a speech recognition system should work reliably for users with different accents, background noise levels, or speaking patterns. Approaches might include diverse training data, robustness testing, and adaptive algorithms that can handle unusual inputs gracefully.",
        "ideal_answer": "Use diverse training data, robust algorithms, and comprehensive testing to ensure consistent performance across all conditions.",
        "good_answer": "Test performance under key edge cases and implement adaptive mechanisms.",
        "basic_answer": "Address performance issues in edge cases reactively when they occur.",
        "non_ideal_answer": "No specific measures are taken to ensure performance under varying conditions.",
        "domain_order": 6,
        "order": 6
    },
    {
        "code": "RE-7",
        "text": "Are there mechanisms for detecting and addressing system downtime or errors?",
        "explanation": "Quick detection and resolution of system downtime or errors is essential for maintaining reliability. This question evaluates your incident response and monitoring capabilities.\n\nFor example, an e-commerce recommendation system might use automated monitoring to detect when the system stops responding or produces error messages, triggering immediate alerts and backup procedures. Effective mechanisms minimize downtime and ensure rapid recovery from failures.",
        "ideal_answer": "Implement automated monitoring, alerting, and recovery mechanisms to quickly detect and address downtime or errors.",
        "good_answer": "Use monitoring tools with manual response procedures for addressing issues.",
        "basic_answer": "Rely on user reports or periodic checks to identify system issues.",
        "non_ideal_answer": "No mechanisms exist for detecting or addressing system downtime or errors.",
        "domain_order": 6,
        "order": 7
    },
    {
        "code": "RE-8",
        "text": "How often is the AI model tested and retrained to maintain reliability?",
        "explanation": "Regular testing and retraining help maintain AI system reliability as data patterns and requirements evolve. This question assesses your approach to ongoing model maintenance.\n\nFor instance, a financial fraud detection model might require monthly retraining to adapt to new fraud patterns and quarterly testing to validate performance. Establishing regular maintenance schedules ensures your system remains effective and reliable over time.",
        "ideal_answer": "Follow a scheduled approach to testing and retraining based on performance metrics, data changes, and business requirements.",
        "good_answer": "Conduct testing and retraining periodically, though not on a fixed schedule.",
        "basic_answer": "Test and retrain the model occasionally or when significant issues arise.",
        "non_ideal_answer": "No regular testing or retraining schedule is followed.",
        "domain_order": 6,
        "order": 8
    },
    # Security Domain (SE-1 to SE-8) - Domain order 7
    {
        "code": "SE-1",
        "text": "What measures are in place to protect your AI models and data from unauthorized access or tampering?",
        "explanation": "AI models and their training data can be valuable targets for attackers seeking to steal intellectual property or manipulate system behavior. This question examines your security measures to prevent unauthorized access or tampering.\n\nFor example, a proprietary recommendation algorithm might be protected through encryption, access controls, and secure deployment environments. Protecting both the model and its data ensures system integrity and prevents malicious exploitation.",
        "ideal_answer": "Implement comprehensive security measures including encryption, access controls, secure deployment, and regular security audits.",
        "good_answer": "Use basic security measures like access controls and encryption for sensitive components.",
        "basic_answer": "Rely on standard IT security practices without AI-specific protections.",
        "non_ideal_answer": "No specific measures are in place to protect AI models and data.",
        "domain_order": 7,
        "order": 1
    },
    {
        "code": "SE-2",
        "text": "How do you handle adversarial risks, such as attacks designed to manipulate the AI's outputs?",
        "explanation": "Adversarial attacks attempt to manipulate AI systems by providing crafted inputs designed to cause incorrect outputs. This question assesses your defenses against such threats.\n\nFor instance, an image recognition system might be vulnerable to adversarial examples—images with imperceptible modifications that cause misclassification. Defense strategies could include adversarial training, input validation, and anomaly detection to identify and reject suspicious inputs.",
        "ideal_answer": "Implement adversarial defenses including robust training, input validation, and anomaly detection systems.",
        "good_answer": "Use basic input validation and monitoring to detect unusual patterns.",
        "basic_answer": "Address adversarial risks reactively when attacks are detected.",
        "non_ideal_answer": "No measures are in place to handle adversarial risks.",
        "domain_order": 7,
        "order": 2
    },
    {
        "code": "SE-3",
        "text": "Do you conduct regular security audits or penetration testing on your AI systems?",
        "explanation": "Regular security audits and penetration testing help identify vulnerabilities in AI systems before they can be exploited. This question evaluates your proactive security assessment practices.\n\nFor example, a penetration test on an AI-powered authentication system might reveal vulnerabilities in the model's decision-making process or implementation flaws that could be exploited. Regular audits ensure ongoing security and compliance with security standards.",
        "ideal_answer": "Conduct regular security audits and penetration testing with both internal and external security experts.",
        "good_answer": "Perform periodic security assessments focusing on key system components.",
        "basic_answer": "Conduct security reviews occasionally or only when required by compliance.",
        "non_ideal_answer": "No regular security audits or penetration testing is performed.",
        "domain_order": 7,
        "order": 3
    },
    {
        "code": "SE-4",
        "text": "How do you secure the AI model during training, deployment, and operation?",
        "explanation": "AI models face different security challenges at each stage of their lifecycle. This question examines your security measures across training, deployment, and operational phases.\n\nFor instance, during training, you might secure training data and computing resources; during deployment, you could use secure containers and encrypted communications; during operation, you might implement runtime monitoring and access controls. Comprehensive security requires protection throughout the entire lifecycle.",
        "ideal_answer": "Implement security measures tailored to each lifecycle stage, including secure training environments, encrypted deployment, and runtime protection.",
        "good_answer": "Apply security measures during key phases like deployment and operation.",
        "basic_answer": "Use basic security practices but without lifecycle-specific considerations.",
        "non_ideal_answer": "No specific security measures are applied across the AI model lifecycle.",
        "domain_order": 7,
        "order": 4
    },
    {
        "code": "SE-5",
        "text": "Are there safeguards to prevent unauthorized modifications to the AI model?",
        "explanation": "Unauthorized modifications to AI models could compromise their integrity, performance, or security. This question assesses your controls to prevent tampering with model parameters, configurations, or code.\n\nFor example, model versioning systems, digital signatures, and access controls could prevent unauthorized changes to a production model. Such safeguards ensure model integrity and maintain trust in system outputs.",
        "ideal_answer": "Use version control, digital signatures, access controls, and audit trails to prevent and detect unauthorized model modifications.",
        "good_answer": "Implement basic access controls and change tracking for model modifications.",
        "basic_answer": "Rely on general IT security practices without model-specific protections.",
        "non_ideal_answer": "No safeguards exist to prevent unauthorized model modifications.",
        "domain_order": 7,
        "order": 5
    },
    {
        "code": "SE-6",
        "text": "What measures are in place to protect the system against adversarial attacks (e.g., input manipulation)?",
        "explanation": "Adversarial attacks can exploit vulnerabilities in AI systems through carefully crafted inputs. This question examines your specific defenses against input-based attacks.\n\nFor instance, an AI system processing user uploads might validate file formats, scan for malicious content, and use adversarial training to resist manipulation attempts. Protective measures help maintain system reliability and security against sophisticated attacks.",
        "ideal_answer": "Deploy comprehensive defenses including input validation, adversarial training, and real-time attack detection.",
        "good_answer": "Use input validation and basic anomaly detection to identify suspicious inputs.",
        "basic_answer": "Implement standard input sanitization without AI-specific protections.",
        "non_ideal_answer": "No specific measures protect against adversarial attacks.",
        "domain_order": 7,
        "order": 6
    },
    {
        "code": "SE-7",
        "text": "How do you protect sensitive data in your AI pipelines (e.g., encryption, tokenization)?",
        "explanation": "AI systems often process sensitive data that requires protection throughout processing pipelines. This question evaluates your data protection measures during AI operations.\n\nFor example, a healthcare AI system might use encryption for data in transit and at rest, tokenization to replace sensitive identifiers, and secure processing environments to protect patient information. Comprehensive data protection maintains privacy and compliance while enabling AI functionality.",
        "ideal_answer": "Use encryption, tokenization, secure processing environments, and data minimization techniques to protect sensitive data.",
        "good_answer": "Implement encryption and basic data protection measures for sensitive information.",
        "basic_answer": "Use standard data protection practices without AI-specific considerations.",
        "non_ideal_answer": "No specific measures protect sensitive data in AI pipelines.",
        "domain_order": 7,
        "order": 7
    },
    {
        "code": "SE-8",
        "text": "Are there regular vulnerability assessments and penetration tests performed on the AI system?",
        "explanation": "Regular vulnerability assessments and penetration testing are essential for identifying and addressing security weaknesses in AI systems. This question examines your ongoing security evaluation practices.\n\nFor instance, automated vulnerability scans might check for known security issues, while manual penetration tests could explore AI-specific attack vectors like model inversion or membership inference attacks. Regular assessments help maintain security posture as threats evolve.",
        "ideal_answer": "Conduct regular vulnerability assessments and penetration tests using both automated tools and manual techniques.",
        "good_answer": "Perform periodic security assessments with some automated scanning.",
        "basic_answer": "Conduct security assessments occasionally or only when issues arise.",
        "non_ideal_answer": "No regular vulnerability assessments or penetration tests are performed.",
        "domain_order": 7,
        "order": 8
    },
    # Privacy Domain (PR-1 to PR-8) - Domain order 8
    {
        "code": "PR-1",
        "text": "How do you ensure compliance with data privacy laws, such as GDPR or the Australian Privacy Act?",
        "explanation": "Data privacy laws impose specific requirements on how personal data is collected, processed, and stored. This question examines your compliance practices with relevant privacy regulations.\n\nFor example, GDPR requires explicit consent for data processing, the right to data deletion, and privacy by design principles. Compliance might involve implementing consent management systems, data subject access request procedures, and privacy impact assessments. Proper compliance protects both users and your organization from legal risks.",
        "ideal_answer": "Implement comprehensive privacy compliance programs including privacy by design, consent management, and data subject rights fulfillment.",
        "good_answer": "Follow key privacy law requirements with documented procedures and regular compliance reviews.",
        "basic_answer": "Address privacy compliance reactively based on legal guidance when needed.",
        "non_ideal_answer": "No specific measures are in place to ensure privacy law compliance.",
        "domain_order": 8,
        "order": 1
    },
    {
        "code": "PR-2",
        "text": "What techniques (e.g., anonymization, pseudonymization) do you use to protect personal data in your AI workflows?",
        "explanation": "Privacy-preserving techniques help protect personal data while enabling AI functionality. This question evaluates your use of methods like anonymization, pseudonymization, or differential privacy.\n\nFor instance, a healthcare AI system might use anonymization to remove direct identifiers from patient records or pseudonymization to replace names with codes. Advanced techniques like differential privacy add mathematical guarantees about privacy protection. These methods enable AI development while minimizing privacy risks.",
        "ideal_answer": "Use advanced privacy-preserving techniques like differential privacy, secure multi-party computation, or federated learning.",
        "good_answer": "Apply anonymization and pseudonymization techniques to protect personal data in AI workflows.",
        "basic_answer": "Use basic data masking or removal of obvious identifiers.",
        "non_ideal_answer": "No specific techniques are used to protect personal data in AI workflows.",
        "domain_order": 8,
        "order": 2
    },
    {
        "code": "PR-3",
        "text": "How do you manage user consent for data collection and processing?",
        "explanation": "User consent is a fundamental principle of privacy protection, requiring clear communication about data use and genuine choice for users. This question examines your consent management practices.\n\nFor example, a mobile app using AI for personalization might present clear consent options explaining what data is collected, how it's used for AI training, and allowing users to opt out. Effective consent management includes granular controls, easy withdrawal mechanisms, and regular consent renewal processes.",
        "ideal_answer": "Implement granular consent management with clear explanations, easy withdrawal options, and regular consent validation.",
        "good_answer": "Obtain user consent with clear information about data use and basic withdrawal options.",
        "basic_answer": "Use general terms of service or basic consent notices without granular controls.",
        "non_ideal_answer": "No specific consent management processes are in place.",
        "domain_order": 8,
        "order": 3
    },
    {
        "code": "PR-4",
        "text": "How do you ensure that personal data is not used beyond its original purpose?",
        "explanation": "Purpose limitation is a key privacy principle requiring that personal data is only used for the specific purposes disclosed during collection. This question examines your controls to prevent purpose creep in AI systems.\n\nFor instance, data collected for fraud detection should not be repurposed for marketing without additional consent. Controls might include data governance policies, access restrictions based on purpose, and regular audits to ensure compliance with stated purposes. Purpose limitation builds user trust and ensures legal compliance.",
        "ideal_answer": "Implement strict purpose limitation controls with governance policies, access restrictions, and regular audits to prevent unauthorized use.",
        "good_answer": "Use data governance policies and access controls to limit data use to stated purposes.",
        "basic_answer": "Rely on informal guidelines or team awareness to limit data use.",
        "non_ideal_answer": "No specific controls prevent data use beyond its original purpose.",
        "domain_order": 8,
        "order": 4
    },
    {
        "code": "PR-5",
        "text": "What methods do you use to anonymize or pseudonymize personal data?",
        "explanation": "Anonymization and pseudonymization are important techniques for protecting privacy while enabling data analysis. This question examines your specific methods for de-identifying personal data.\n\nFor example, k-anonymity ensures that records cannot be distinguished from at least k-1 others, while pseudonymization replaces identifiers with reversible codes. The choice of method depends on your use case, risk tolerance, and regulatory requirements. Proper implementation provides privacy protection while maintaining data utility.",
        "ideal_answer": "Use sophisticated anonymization techniques like k-anonymity, l-diversity, or t-closeness based on risk assessment and regulatory requirements.",
        "good_answer": "Apply standard anonymization methods like data masking or identifier removal.",
        "basic_answer": "Use simple techniques like removing obvious identifiers without comprehensive anonymization.",
        "non_ideal_answer": "No anonymization or pseudonymization methods are used.",
        "domain_order": 8,
        "order": 5
    },
    {
        "code": "PR-6",
        "text": "How do you monitor and prevent privacy violations during system operation?",
        "explanation": "Ongoing monitoring is essential to detect and prevent privacy violations in operational AI systems. This question examines your privacy monitoring and incident response capabilities.\n\nFor instance, automated monitoring might detect unusual data access patterns, unauthorized data transfers, or policy violations. Privacy dashboards could track consent status, data retention periods, and access logs. Proactive monitoring helps prevent privacy incidents and demonstrates due diligence in privacy protection.",
        "ideal_answer": "Implement automated privacy monitoring with alerts, dashboards, and incident response procedures to detect and prevent violations.",
        "good_answer": "Use monitoring tools to track data access and basic privacy compliance metrics.",
        "basic_answer": "Perform periodic manual reviews of privacy practices and data handling.",
        "non_ideal_answer": "No monitoring is in place to detect or prevent privacy violations.",
        "domain_order": 8,
        "order": 6
    },
    {
        "code": "PR-7",
        "text": "Are privacy risks evaluated during both the development and deployment phases?",
        "explanation": "Privacy risks can emerge at different stages of AI system development and deployment, requiring ongoing evaluation and mitigation. This question examines whether you conduct privacy risk assessments throughout the system lifecycle.\n\nFor example, development phase assessments might evaluate training data privacy risks, while deployment assessments could examine operational data handling. Privacy Impact Assessments (PIAs) or Data Protection Impact Assessments (DPIAs) provide systematic frameworks for risk evaluation and mitigation.",
        "ideal_answer": "Conduct comprehensive privacy risk assessments at all lifecycle stages using frameworks like PIAs or DPIAs.",
        "good_answer": "Perform privacy risk assessments during key phases like development and initial deployment.",
        "basic_answer": "Evaluate privacy risks informally or only during development.",
        "non_ideal_answer": "No privacy risk evaluations are conducted during development or deployment.",
        "domain_order": 8,
        "order": 7
    },
    {
        "code": "PR-8",
        "text": "What steps are taken to ensure compliance with cross-border data protection laws?",
        "explanation": "Cross-border data transfers often involve multiple privacy jurisdictions with different requirements. This question examines your approach to international privacy compliance.\n\nFor instance, transferring personal data from the EU to other countries requires adequate protection levels or specific safeguards like Standard Contractual Clauses. Understanding and complying with various privacy laws (GDPR, CCPA, etc.) ensures legal operation across jurisdictions and builds global user trust.",
        "ideal_answer": "Implement comprehensive cross-border compliance programs with adequate safeguards, standard contractual clauses, and jurisdiction-specific requirements.",
        "good_answer": "Use standard contractual clauses and basic safeguards for international data transfers.",
        "basic_answer": "Address cross-border compliance reactively based on legal guidance.",
        "non_ideal_answer": "No specific steps are taken to ensure cross-border privacy compliance.",
        "domain_order": 8,
        "order": 8
    }
]