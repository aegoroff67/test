# Complete question data from AMAISAFE_Qs_and_As.xlsx spreadsheet
# This contains all 88 questions across 11 domains with complete explanations

COMPLETE_QUESTIONS_DATA = [
    # Fairness Domain (FA-1 to FA-8)
    {
        "code": "FA-1",
        "text": "What measures have you implemented to identify and mitigate biases in your AI system?",
        "explanation": "Bias in AI systems can lead to unfair treatment or exclusion of certain groups, undermining the credibility and effectiveness of the system. This question seeks to determine what proactive steps you've taken to identify and reduce biases. Measures might include bias detection tools, manual data reviews, or conducting fairness audits throughout the development lifecycle.\n\nFor example, if an AI system is used for hiring, it could favor certain demographics based on historical biases in the training data. Mitigation strategies could involve rebalancing datasets, removing biased features, or incorporating fairness constraints into model training.",
        "ideal_answer": "Regularly audit datasets for imbalances or biases and use tools like Fairlearn to detect and mitigate issues.",
        "good_answer": "Implement fairness constraints during model training and review model outcomes for biases before deployment.",
        "basic_answer": "Conduct ad hoc reviews of the system to check for fairness concerns.",
        "non_ideal_answer": "No specific measures have been implemented yet.",
        "domain_order": 1,
        "order": 1
    },
    {
        "code": "FA-2", 
        "text": "How do you ensure the training data represents all relevant demographics or groups?",
        "explanation": "AI systems learn from the data they are trained on. If the data lacks representation from certain demographics, the system might perform poorly or unfairly for those groups. This question assesses your practices for ensuring training data is diverse and representative of the populations the AI will interact with. For example, if a facial recognition system is trained primarily on images of light-skinned individuals, it might not accurately recognize darker-skinned individuals. To address this, you might source data from multiple demographic groups and evaluate its representativeness.",
        "domain_order": 1,
        "order": 2
    },
    {
        "code": "FA-3",
        "text": "Have you evaluated the system's outputs for potential disparities across user groups?",
        "explanation": "This question focuses on whether you have conducted evaluations to determine if your AI system produces different outcomes for different groups of users (e.g., based on race, gender, age, socioeconomic status). Even if your training data is representative, biases can still emerge in model outputs. Regular evaluation helps identify and address these disparities. Methods might include statistical analysis of outputs across demographic groups, fairness metrics like demographic parity or equalized odds, or user studies to assess differential impacts.",
        "domain_order": 1,
        "order": 3
    },
    {
        "code": "FA-4",
        "text": "How do you measure fairness in your AI system's outputs?",
        "explanation": "Measuring fairness requires specific metrics and methodologies to quantitatively assess whether an AI system treats different groups equitably. Common fairness metrics include demographic parity (equal positive prediction rates across groups), equalized odds (equal true positive and false positive rates), and individual fairness (similar individuals receive similar outcomes). The choice of metric depends on your application context and what constitutes 'fairness' for your use case.",
        "domain_order": 1,
        "order": 4
    },
    {
        "code": "FA-5",
        "text": "Have you tested the system for potential biases in real-world scenarios?",
        "explanation": "Real-world testing goes beyond laboratory or controlled environments to assess how the AI system performs when deployed in actual operational conditions. This is crucial because biases that aren't apparent in controlled settings may emerge when the system encounters the full complexity and diversity of real-world use. Testing methods might include A/B testing with diverse user groups, pilot deployments in different geographic or demographic markets, or shadow deployment where the AI runs in parallel with existing systems for comparison.",
        "domain_order": 1,
        "order": 5
    },
    {
        "code": "FA-6",
        "text": "Are you using any frameworks or tools (e.g., Fairlearn) to assess and mitigate bias?",
        "explanation": "Various specialized tools and frameworks have been developed to help practitioners assess and mitigate bias in AI systems. These include open-source libraries like Fairlearn (Microsoft), AIF360 (IBM), and What-If Tool (Google), as well as commercial solutions. These tools typically provide implementations of fairness metrics, bias detection algorithms, and mitigation techniques. Using established tools can be more reliable and efficient than building custom solutions from scratch.",
        "domain_order": 1,
        "order": 6
    },
    {
        "code": "FA-7",
        "text": "How do you ensure fairness in decision-making for minority or underserved groups?",
        "explanation": "Minority and underserved groups often face particular risks from AI bias because they may be underrepresented in training data or because existing social inequalities can be amplified by AI systems. This question assesses specific measures you take to protect these vulnerable populations. Approaches might include setting specific performance targets for these groups, using bias mitigation techniques designed for minorities, involving community representatives in system design, or implementing differential privacy protections.",
        "domain_order": 1,
        "order": 7
    },
    {
        "code": "FA-8",
        "text": "Is fairness embedded in your AI model's design process, or is it addressed post-deployment?",
        "explanation": "The current policy for AI fairness is primarily addressed post-deployment through continuous monitoring and updates. While fairness is considered during the AI model's design process, it is not a primary focus at that initial stage. The focus on addressing fairness becomes more prominent once the system is in use.",
        "domain_order": 1,
        "order": 8
    },
    
    # Transparency Domain (TR-1 to TR-8)
    {
        "code": "TR-1",
        "text": "What level of detail about the AI system's functionality and limitations is communicated to users or stakeholders?",
        "explanation": "Transparency in AI systems involves providing clear, understandable information about how the system works, what it can and cannot do, and how decisions are made. This question assesses the depth and clarity of communication with users and stakeholders. Effective transparency helps users understand what to expect from the system, how to interpret its outputs, and what limitations to be aware of. The level of detail should be appropriate for the audience - technical stakeholders may need detailed algorithmic information, while end users may need high-level explanations.",
        "domain_order": 2,
        "order": 1
    },
    {
        "code": "TR-2",
        "text": "How do you document the data sources, algorithms, and processes used in your AI system?",
        "explanation": "Comprehensive documentation is essential for AI system transparency, reproducibility, and accountability. This includes documenting data sources (where data comes from, how it was collected, potential biases), algorithms used (model architecture, training procedures, hyperparameters), and processes (data preprocessing steps, validation methods, deployment procedures). Good documentation practices might include model cards, dataset datasheets, technical specifications, and version control of all components.",
        "domain_order": 2,
        "order": 2
    },
    {
        "code": "TR-3",
        "text": "Are there mechanisms for external parties (e.g., regulators or customers) to understand how your AI system works?",
        "explanation": "External transparency mechanisms are crucial for regulatory compliance, customer trust, and public accountability. This might include publishing research papers, providing API documentation, offering system demonstrations, or participating in third-party audits. The goal is to give external stakeholders sufficient information to understand, evaluate, and potentially scrutinize the AI system's operation and decision-making processes.",
        "domain_order": 2,
        "order": 3
    },
    {
        "code": "TR-4",
        "text": "How is information about your AI system shared with internal teams and external stakeholders?",
        "explanation": "Effective information sharing ensures that all relevant parties have appropriate access to AI system information. This includes establishing clear communication channels, regular reporting mechanisms, and appropriate access controls. Internal sharing might involve cross-functional meetings, technical documentation repositories, or training programs. External sharing could include customer communications, partner briefings, or public reports.",
        "domain_order": 2,
        "order": 4
    },
    {
        "code": "TR-5",
        "text": "Are there any 'black-box' components in your system that could impede transparency?",
        "explanation": "Black-box components are parts of an AI system whose internal workings are opaque or difficult to understand, even by the system's developers. This commonly occurs with complex machine learning models like deep neural networks, but can also happen with third-party components or proprietary algorithms. While some level of complexity is inevitable in AI systems, identifying and minimizing black-box components is important for maintaining transparency and explainability.",
        "domain_order": 2,
        "order": 5
    },
    {
        "code": "TR-6",
        "text": "How do you disclose the sources of data and algorithms used in the AI system?",
        "explanation": "Disclosure of data sources and algorithms is fundamental to AI transparency. This includes providing information about where training data came from, what types of data are used, what algorithms and models are employed, and any third-party components or services integrated into the system. The level of disclosure may vary based on competitive considerations and intellectual property concerns, but stakeholders should have enough information to understand the system's foundation.",
        "domain_order": 2,
        "order": 6
    },
    {
        "code": "TR-7",
        "text": "Are users made aware when they are interacting with an AI system?",
        "explanation": "User awareness of AI interaction is important for informed consent and setting appropriate expectations. Users should generally know when they're interacting with an AI system rather than a human, what capabilities the AI has, and what limitations they should be aware of. This disclosure can be explicit (clear statements that 'this is an AI assistant') or contextual (through interface design and interaction patterns that make the AI nature apparent).",
        "domain_order": 2,
        "order": 7
    },
    {
        "code": "TR-8",
        "text": "Do you publish any transparency reports or documentation for regulators or customers?",
        "explanation": "Transparency reports and documentation provide systematic, public information about AI system governance, performance, and impact. These might include annual transparency reports, algorithmic impact assessments, fairness evaluations, or compliance documentation. Such reports demonstrate commitment to transparency and provide stakeholders with regular updates on system performance, issues encountered, and improvements made.",
        "domain_order": 2,
        "order": 8
    },
    
    # Explainability Domain (EX-1 to EX-8)
    {
        "code": "EX-1",
        "text": "Does your AI system provide explanations for its outputs or decisions?",
        "explanation": "Explainable AI (XAI) focuses on making AI decision-making processes understandable to humans. This question assesses whether your system can provide explanations for why it made specific decisions or predictions. Explanations can take various forms: feature importance scores, decision trees, natural language descriptions, visualizations, or examples. The goal is to help users understand the reasoning behind AI outputs, which is crucial for trust, debugging, compliance, and ethical AI use.",
        "domain_order": 3,
        "order": 1
    },
    {
        "code": "EX-2",
        "text": "How interpretable are the explanations provided by your AI system to different user types?",
        "explanation": "The interpretability of AI explanations varies significantly depending on the user's technical background, domain expertise, and specific needs. This question evaluates how well your explanations are tailored to different audiences. Technical users might need detailed algorithmic explanations, while business users might prefer high-level summaries, and end users might need simple, intuitive explanations. Good interpretability means explanations are accurate, relevant, and comprehensible to their intended audience.",
        "domain_order": 3,
        "order": 2
    },
    {
        "code": "EX-3",
        "text": "What methods do you use to generate explanations (e.g., SHAP, LIME, attention mechanisms)?",
        "explanation": "Various technical methods exist for generating explanations from AI systems. This question assesses which specific explainability techniques you employ. Common methods include SHAP (SHapley Additive exPlanations) for feature importance, LIME (Local Interpretable Model-agnostic Explanations) for local explanations, attention mechanisms in neural networks, gradient-based methods, or counterfactual explanations. The choice of method depends on your model type, use case requirements, and computational constraints.",
        "domain_order": 3,
        "order": 3
    },
    {
        "code": "EX-4",
        "text": "Can users understand why the AI system made a particular decision in their specific case?",
        "explanation": "Individual-level explainability focuses on providing personalized explanations for specific decisions affecting particular users. This is especially important in high-stakes applications like loan approvals, medical diagnoses, or legal decisions. The explanation should help users understand not just what the system decided, but why it reached that conclusion based on their specific input data and circumstances. This requires generating case-specific explanations rather than just general system behavior descriptions.",
        "domain_order": 3,
        "order": 4
    },
    {
        "code": "EX-5",
        "text": "Have you validated that the explanations accurately represent the AI model's actual decision-making process?",
        "explanation": "Explanation validation ensures that the explanations provided actually reflect how the AI system makes decisions, rather than being plausible but potentially misleading post-hoc rationalizations. This is crucial because some explanation methods can generate explanations that seem reasonable but don't accurately represent the model's actual reasoning. Validation techniques might include comparing explanations across different methods, testing explanation consistency, or using techniques like sanity checks and sensitivity analysis.",
        "domain_order": 3,
        "order": 5
    },
    {
        "code": "EX-6",
        "text": "Do the explanations help users make better decisions when using the AI system?",
        "explanation": "The ultimate goal of AI explanations is to improve human decision-making when working with AI systems. This question evaluates the practical utility of your explanations. Effective explanations should help users know when to trust the AI, when to be skeptical, how to use the AI's output in their broader decision-making process, and how to identify potential errors or limitations. This can be assessed through user studies, task performance metrics, or feedback collection.",
        "domain_order": 3,
        "order": 6
    },
    {
        "code": "EX-7",
        "text": "Are explanations consistent across similar inputs or cases?",
        "explanation": "Explanation consistency means that similar inputs should receive similar explanations, and that the same input should receive the same explanation when processed multiple times. Inconsistent explanations can undermine user trust and make it difficult to understand the system's behavior patterns. This question assesses whether your explanation system provides stable, reliable explanations. Factors that can affect consistency include randomness in explanation methods, model updates, or changes in comparison datasets.",
        "domain_order": 3,
        "order": 7
    },
    {
        "code": "EX-8",
        "text": "How do you handle cases where the AI system cannot provide a satisfactory explanation?",
        "explanation": "Not all AI decisions can be easily explained, especially in complex systems or edge cases. This question addresses how you handle situations where explanations are unavailable, unreliable, or too complex to understand. Approaches might include providing uncertainty indicators, escalating to human review, offering alternative decision pathways, or clearly communicating the limitations of available explanations. The key is maintaining transparency about when and why explanations may be inadequate.",
        "domain_order": 3,
        "order": 8
    },
    
    # Accountability Domain (AC-1 to AC-8)
    {
        "code": "AC-1",
        "text": "Who is ultimately responsible for decisions made by your AI system?",
        "explanation": "Accountability in AI systems requires clear assignment of responsibility for AI decisions and their consequences. This question addresses the governance structure around your AI system. Even when AI systems make autonomous decisions, there should be clear human accountability chains - someone who is responsible for the system's design, deployment, monitoring, and outcomes. This might involve specific roles like AI system owners, data scientists, product managers, or executives, along with defined responsibilities and decision-making authority.",
        "domain_order": 4,
        "order": 1
    },
    {
        "code": "AC-2",
        "text": "What governance structures are in place to oversee AI system development and deployment?",
        "explanation": "AI governance structures provide systematic oversight of AI system lifecycle from development through deployment and maintenance. This includes committees, review boards, approval processes, policy frameworks, and reporting mechanisms. Effective governance ensures that AI systems are developed responsibly, comply with relevant regulations and ethical standards, and align with organizational values and objectives. This might include AI ethics boards, technical review committees, or cross-functional governance teams.",
        "domain_order": 4,
        "order": 2
    },
    {
        "code": "AC-3",
        "text": "How do you handle appeals or disputes related to AI system decisions?",
        "explanation": "Appeal and dispute mechanisms provide recourse for individuals or organizations affected by AI decisions. This is particularly important for high-stakes applications where AI decisions significantly impact people's lives or opportunities. Effective appeal processes should be accessible, fair, timely, and provide meaningful review of AI decisions. This might include human review processes, escalation procedures, independent arbitration, or mechanisms for challenging and potentially overturning AI decisions.",
        "domain_order": 4,
        "order": 3
    },
    {
        "code": "AC-4",
        "text": "Are there clear policies for AI system use, modification, and retirement?",
        "explanation": "Clear policies governing AI system lifecycle management ensure consistent, responsible practices throughout the system's operational life. This includes policies for appropriate use cases, authorized users, modification procedures, version control, performance monitoring, and system retirement. These policies should address when and how systems can be updated, who can make changes, how to handle system failures, and criteria for decommissioning systems that no longer meet requirements.",
        "domain_order": 4,
        "order": 4
    },
    {
        "code": "AC-5",
        "text": "How do you track and document decisions made by your AI system?",
        "explanation": "Decision tracking and documentation create an audit trail for AI system outputs, enabling accountability, debugging, and compliance monitoring. This involves logging AI decisions, the inputs that led to those decisions, confidence scores, relevant metadata, and timestamps. Good tracking systems enable retrospective analysis, pattern identification, and investigation of specific decisions when issues arise. The level of detail and retention period should be appropriate for the application's risk level and regulatory requirements.",
        "domain_order": 4,
        "order": 5
    },
    {
        "code": "AC-6",
        "text": "What measures are in place to ensure compliance with relevant regulations or standards?",
        "explanation": "AI systems often operate in regulated environments or must comply with industry standards, legal requirements, or ethical frameworks. This question assesses your compliance management approach. Relevant regulations might include GDPR for privacy, fair lending laws for financial services, or medical device regulations for healthcare AI. Compliance measures could include legal review processes, regular audits, compliance monitoring systems, documentation requirements, and staff training on regulatory requirements.",
        "domain_order": 4,
        "order": 6
    },
    {
        "code": "AC-7",
        "text": "How do you communicate AI system limitations and potential risks to stakeholders?",
        "explanation": "Effective risk communication ensures that stakeholders understand the limitations, uncertainties, and potential negative consequences of AI system use. This includes technical limitations (accuracy bounds, failure modes), operational constraints (appropriate use cases, required human oversight), and broader risks (bias potential, privacy implications). Communication should be tailored to different stakeholder groups and updated as new limitations or risks are discovered.",
        "domain_order": 4,
        "order": 7
    },
    {
        "code": "AC-8",
        "text": "Are there mechanisms for external audit or review of your AI system?",
        "explanation": "External audit and review mechanisms provide independent oversight and validation of AI systems, which is crucial for accountability and trust. This might include third-party audits, regulatory reviews, academic partnerships, or public scrutiny processes. External review can help identify blind spots, validate internal assessments, and provide credible assurance to stakeholders. The scope and frequency of external review should be appropriate for the system's risk level and societal impact.",
        "domain_order": 4,
        "order": 8
    },
    
    # Data Integrity Domain (DI-1 to DI-8)
    {
        "code": "DI-1",
        "text": "What processes do you have in place to ensure data quality and accuracy?",
        "explanation": "Data quality and accuracy are fundamental to AI system performance and reliability. This question assesses your data quality management practices. Data quality issues can include missing values, duplicate records, inconsistent formats, outdated information, or measurement errors. Quality assurance processes might include data validation rules, automated quality checks, manual data review, data profiling, and correction procedures. The goal is to ensure that training and operational data meet accuracy, completeness, consistency, and timeliness standards.",
        "domain_order": 5,
        "order": 1
    },
    {
        "code": "DI-2",
        "text": "How do you validate the integrity of your training and operational data?",
        "explanation": "Data integrity validation ensures that data has not been corrupted, tampered with, or degraded during collection, storage, or processing. This involves implementing controls to detect unauthorized changes, data corruption, or systematic errors. Validation techniques might include checksums, digital signatures, audit trails, statistical anomaly detection, or comparison with authoritative sources. Regular integrity checks help maintain confidence in data reliability and AI system outputs.",
        "domain_order": 5,
        "order": 2
    },
    {
        "code": "DI-3",
        "text": "What measures are in place to detect and address data drift or changes in data distribution?",
        "explanation": "Data drift occurs when the statistical properties of data change over time, which can degrade AI system performance. This question evaluates your monitoring and response capabilities for data distribution changes. Detection methods might include statistical tests, distribution comparisons, or performance monitoring. Response measures could include retraining models, adjusting preprocessing steps, or updating data collection procedures. Proactive drift detection helps maintain system performance as real-world conditions evolve.",
        "domain_order": 5,
        "order": 3
    },
    {
        "code": "DI-4",
        "text": "How do you handle missing, incomplete, or corrupted data?",
        "explanation": "Missing, incomplete, or corrupted data is common in real-world applications and can significantly impact AI system performance. This question assesses your data handling strategies. Approaches might include imputation techniques (mean, median, model-based), exclusion of incomplete records, flagging uncertain data, or using robust algorithms that handle missing data well. The choice depends on the missing data mechanism, the importance of affected features, and the tolerance for uncertainty in your application.",
        "domain_order": 5,
        "order": 4
    },
    {
        "code": "DI-5",
        "text": "What data governance policies and procedures are in place?",
        "explanation": "Data governance provides the framework for managing data as a strategic asset throughout its lifecycle. This includes policies for data collection, storage, access, usage, quality, retention, and disposal. Good data governance ensures data is accurate, accessible, consistent, and secure while complying with regulatory requirements. This might involve data stewardship roles, data catalogs, access controls, audit trails, and procedures for data classification and handling.",
        "domain_order": 5,
        "order": 5
    },
    {
        "code": "DI-6",
        "text": "How do you ensure the provenance and traceability of your data sources?",
        "explanation": "Data provenance and traceability involve tracking the origin, history, and lineage of data throughout its lifecycle. This is crucial for understanding data quality, debugging issues, ensuring compliance, and maintaining trust in AI systems. Provenance tracking might include recording data sources, collection methods, processing steps, transformations applied, and responsible parties. Good traceability enables reconstruction of how data was processed and supports impact analysis when issues are discovered.",
        "domain_order": 5,
        "order": 6
    },
    {
        "code": "DI-7",
        "text": "What controls are in place to prevent unauthorized access or modification of data?",
        "explanation": "Data access controls protect against unauthorized viewing, modification, or deletion of data. This is essential for maintaining data integrity, confidentiality, and compliance with privacy regulations. Controls might include authentication and authorization systems, encryption (at rest and in transit), access logging, role-based permissions, and segregation of duties. The goal is to ensure only authorized personnel can access data for legitimate purposes while maintaining an audit trail of all access.",
        "domain_order": 5,
        "order": 7
    },
    {
        "code": "DI-8",
        "text": "How do you manage data versioning and maintain historical records?",
        "explanation": "Data versioning and historical record management enable tracking of data changes over time, supporting reproducibility, audit requirements, and root cause analysis. This involves maintaining snapshots of data at different points in time, tracking changes between versions, and preserving historical data for compliance or analysis purposes. Version management systems help ensure you can reproduce AI model training, investigate performance changes, and meet regulatory requirements for data retention.",
        "domain_order": 5,
        "order": 8
    },
    
    # Reliability Domain (RE-1 to RE-8)
    {
        "code": "RE-1",
        "text": "What is the expected accuracy or performance level of your AI system?",
        "explanation": "Setting clear performance expectations provides a baseline for evaluating AI system effectiveness and reliability. This question addresses your performance targets and measurement criteria. Performance metrics vary by application but might include accuracy, precision, recall, F1-score, area under the curve, mean squared error, or domain-specific measures. Clear expectations help stakeholders understand what to expect from the system and provide criteria for determining when performance is acceptable or requires intervention.",
        "domain_order": 6,
        "order": 1
    },
    {
        "code": "RE-2",
        "text": "How do you monitor and measure the ongoing performance of your AI system?",
        "explanation": "Continuous performance monitoring ensures that AI systems maintain expected performance levels over time. This involves establishing metrics, measurement procedures, monitoring infrastructure, and alerting mechanisms. Monitoring might include real-time performance dashboards, periodic batch evaluations, A/B testing, or user feedback collection. The goal is to quickly detect performance degradation, concept drift, or other issues that might affect system reliability.",
        "domain_order": 6,
        "order": 2
    },
    {
        "code": "RE-3",
        "text": "What measures are in place to handle system failures or errors?",
        "explanation": "System failure handling ensures graceful degradation and recovery when AI systems encounter errors or unexpected conditions. This question assesses your error handling and recovery procedures. Measures might include error detection and logging, fallback mechanisms, human-in-the-loop escalation, graceful degradation modes, or automatic retry logic. Good failure handling minimizes the impact of errors on users and enables quick recovery to normal operation.",
        "domain_order": 6,
        "order": 3
    },
    {
        "code": "RE-4",
        "text": "How do you ensure consistent performance across different operating conditions?",
        "explanation": "Consistent performance across varying conditions ensures that AI systems remain reliable regardless of changes in input data, system load, environmental factors, or user patterns. This might involve testing under different scenarios, stress testing, load balancing, robust algorithm design, or adaptive performance tuning. The goal is to maintain acceptable performance levels even when conditions differ from those encountered during development and testing.",
        "domain_order": 6,
        "order": 4
    },
    {
        "code": "RE-5",
        "text": "What redundancy or backup systems are in place to ensure continuity?",
        "explanation": "Redundancy and backup systems protect against single points of failure and ensure business continuity. This question evaluates your system architecture for reliability. Redundancy might include multiple servers, database replicas, geographically distributed systems, or backup algorithms. The level of redundancy should be appropriate for the criticality of your application and acceptable downtime tolerances. Good redundancy design ensures service continuity even when individual components fail.",
        "domain_order": 6,
        "order": 5
    },
    {
        "code": "RE-6",
        "text": "How do you test the reliability and robustness of your AI system?",
        "explanation": "Reliability and robustness testing evaluates how well AI systems perform under adverse or unexpected conditions. This goes beyond standard accuracy testing to include stress testing, adversarial testing, edge case evaluation, and fault injection. Testing might involve corrupted inputs, extreme values, unusual input patterns, or simulated system failures. The goal is to identify vulnerabilities and ensure the system performs acceptably even under challenging conditions.",
        "domain_order": 6,
        "order": 6
    },
    {
        "code": "RE-7",
        "text": "What is the system's uptime and availability track record?",
        "explanation": "Uptime and availability metrics provide objective measures of system reliability. This question assesses your system's operational history and availability targets. Metrics might include uptime percentage, mean time between failures (MTBF), mean time to recovery (MTTR), or service level agreement (SLA) compliance. Good availability tracking helps identify reliability trends, validate system design decisions, and demonstrate reliability to stakeholders.",
        "domain_order": 6,
        "order": 7
    },
    {
        "code": "RE-8",
        "text": "How do you handle model updates or changes without disrupting service?",
        "explanation": "Seamless model updates ensure that AI systems can be improved and maintained without service disruption. This question addresses your deployment and change management practices. Techniques might include blue-green deployments, canary releases, rolling updates, or A/B testing for gradual rollouts. Good update procedures allow for safe deployment of improvements while minimizing risk to system availability and performance.",
        "domain_order": 6,
        "order": 8
    },
    
    # Security Domain (SE-1 to SE-8)
    {
        "code": "SE-1",
        "text": "What security measures are in place to protect your AI system from unauthorized access?",
        "explanation": "Security measures protect AI systems from unauthorized access, which could lead to data breaches, model theft, or system compromise. This question assesses your access control and authentication mechanisms. Security measures might include strong authentication (multi-factor), authorization controls (role-based access), network security (firewalls, VPNs), encryption, and monitoring for suspicious activity. The goal is to ensure only authorized users can access system components and data.",
        "domain_order": 7,
        "order": 1
    },
    {
        "code": "SE-2",
        "text": "How do you protect against adversarial attacks on your AI model?",
        "explanation": "Adversarial attacks involve deliberately crafted inputs designed to fool AI systems into making incorrect predictions or classifications. This question evaluates your defenses against such attacks. Protection methods might include adversarial training, input validation, robust optimization techniques, ensemble methods, or anomaly detection. The importance of adversarial protection depends on your application's security requirements and potential attack vectors.",
        "domain_order": 7,
        "order": 2
    },
    {
        "code": "SE-3",
        "text": "What measures are in place to ensure data security throughout the AI lifecycle?",
        "explanation": "Data security throughout the AI lifecycle protects sensitive information from collection through disposal. This involves securing data at rest, in transit, and during processing. Security measures might include encryption, secure storage systems, access controls, data anonymization, secure communication protocols, and secure deletion procedures. The goal is to maintain data confidentiality, integrity, and availability throughout all phases of AI system development and operation.",
        "domain_order": 7,
        "order": 3
    },
    {
        "code": "SE-4",
        "text": "How do you monitor for and respond to security threats or breaches?",
        "explanation": "Security monitoring and incident response ensure rapid detection and mitigation of security threats. This question assesses your security operations capabilities. Monitoring might include intrusion detection systems, log analysis, behavioral monitoring, or threat intelligence integration. Response procedures should include incident classification, containment, investigation, remediation, and communication. Effective security operations minimize the impact of security incidents and prevent future occurrences.",
        "domain_order": 7,
        "order": 4
    },
    {
        "code": "SE-5",
        "text": "What controls are in place to prevent model theft or intellectual property leakage?",
        "explanation": "Model theft and IP protection prevent unauthorized copying or extraction of proprietary AI models and algorithms. This question addresses your intellectual property security measures. Protection might include access controls, model obfuscation, watermarking, query limiting, monitoring for extraction attempts, or legal protections. The level of protection should be appropriate for the value and sensitivity of your intellectual property.",
        "domain_order": 7,
        "order": 5
    },
    {
        "code": "SE-6",
        "text": "How do you ensure secure deployment and operation of your AI system?",
        "explanation": "Secure deployment and operation practices protect AI systems in production environments. This includes secure configuration management, patch management, secure communication protocols, environment isolation, and operational security procedures. Secure deployment ensures that systems are hardened against attacks, properly configured, and maintained with current security updates. The goal is to minimize attack surface and maintain security posture throughout the system's operational life.",
        "domain_order": 7,
        "order": 6
    },
    {
        "code": "SE-7",
        "text": "What authentication and authorization mechanisms are implemented?",
        "explanation": "Authentication and authorization mechanisms ensure that users and systems are properly identified and granted appropriate access levels. Authentication verifies identity (who you are), while authorization controls access (what you can do). Mechanisms might include multi-factor authentication, single sign-on, role-based access control, attribute-based access control, or API keys. Strong authentication and authorization are fundamental to system security and data protection.",
        "domain_order": 7,
        "order": 7
    },
    {
        "code": "SE-8",
        "text": "How do you conduct security assessments or penetration testing of your AI system?",
        "explanation": "Security assessments and penetration testing proactively identify vulnerabilities and security weaknesses in AI systems. This question evaluates your security validation practices. Assessments might include vulnerability scans, code reviews, architecture reviews, or simulated attacks. Penetration testing involves authorized attempts to exploit identified vulnerabilities. Regular security assessments help identify and remediate security issues before they can be exploited by attackers.",
        "domain_order": 7,
        "order": 8
    },
    
    # Privacy Domain (PR-1 to PR-8)
    {
        "code": "PR-1",
        "text": "What personal data does your AI system collect, process, or store?",
        "explanation": "Understanding what personal data is involved in AI systems is fundamental to privacy protection and regulatory compliance. This question assesses your data inventory and classification practices. Personal data might include names, addresses, phone numbers, email addresses, biometric data, behavioral patterns, or any information that can identify individuals. Clear data mapping helps ensure appropriate protection measures are applied and supports compliance with privacy regulations like GDPR or CCPA.",
        "domain_order": 8,
        "order": 1
    },
    {
        "code": "PR-2",
        "text": "How do you obtain consent for data collection and processing?",
        "explanation": "Consent management ensures that individuals understand and agree to how their personal data will be used. This question evaluates your consent collection and management practices. Effective consent should be informed (clear explanation of purposes), specific (granular control), freely given (no coercion), and withdrawable. Consent mechanisms might include opt-in checkboxes, granular privacy settings, consent management platforms, or layered privacy notices. The requirements vary based on applicable privacy laws and data sensitivity.",
        "domain_order": 8,
        "order": 2
    },
    {
        "code": "PR-3",
        "text": "What measures are in place to anonymize or pseudonymize personal data?",
        "explanation": "Anonymization and pseudonymization techniques protect individual privacy by removing or obscuring identifying information. This question assesses your data protection techniques. Anonymization involves removing identifiers so data cannot be linked back to individuals, while pseudonymization replaces identifiers with artificial identifiers. Techniques might include data masking, generalization, suppression, synthetic data generation, or differential privacy. The choice depends on data utility requirements and privacy protection needs.",
        "domain_order": 8,
        "order": 3
    },
    {
        "code": "PR-4",
        "text": "How do you handle data subject rights (e.g., access, rectification, deletion under GDPR)?",
        "explanation": "Data subject rights give individuals control over their personal data and are required by many privacy regulations. This question evaluates your procedures for handling individual requests. Common rights include access (viewing personal data), rectification (correcting errors), deletion (right to be forgotten), portability (data export), and objection (opting out of processing). Effective rights management requires clear procedures, reasonable response times, identity verification, and technical capabilities to fulfill requests.",
        "domain_order": 8,
        "order": 4
    },
    {
        "code": "PR-5",
        "text": "What privacy-by-design principles are integrated into your AI system development?",
        "explanation": "Privacy-by-design integrates privacy considerations into system design from the beginning rather than adding them afterwards. This question assesses your privacy engineering practices. Privacy-by-design principles include data minimization (collect only necessary data), purpose limitation (use data only for stated purposes), storage limitation (retain data only as long as needed), and privacy-preserving techniques. Implementation might involve privacy impact assessments, privacy requirements in design specifications, or privacy-preserving algorithms.",
        "domain_order": 8,
        "order": 5
    },
    {
        "code": "PR-6",
        "text": "How do you ensure compliance with relevant privacy regulations (e.g., GDPR, CCPA)?",
        "explanation": "Privacy regulation compliance ensures that AI systems meet legal requirements for personal data protection. This question evaluates your compliance management approach. Compliance activities might include privacy impact assessments, data protection officer appointment, privacy policy development, staff training, consent management, breach notification procedures, and regular compliance audits. The specific requirements depend on applicable regulations, data types, and jurisdictions where you operate.",
        "domain_order": 8,
        "order": 6
    },
    {
        "code": "PR-7",
        "text": "What controls are in place to limit data sharing with third parties?",
        "explanation": "Third-party data sharing controls protect personal data when it's shared with vendors, partners, or service providers. This question assesses your data sharing governance. Controls might include data processing agreements, due diligence on third parties, access restrictions, audit rights, breach notification requirements, and data minimization for sharing. The goal is to ensure third parties provide adequate protection and use data only for authorized purposes.",
        "domain_order": 8,
        "order": 7
    },
    {
        "code": "PR-8",
        "text": "How do you conduct privacy impact assessments for your AI system?",
        "explanation": "Privacy impact assessments (PIAs) systematically evaluate privacy risks and mitigation measures for AI systems. This question assesses your privacy risk management process. PIAs typically identify data flows, assess privacy risks, evaluate compliance requirements, and recommend mitigation measures. They should be conducted early in development and updated as systems evolve. Effective PIAs help identify privacy issues before they become problems and demonstrate due diligence in privacy protection.",
        "domain_order": 8,
        "order": 8
    },
    
    # Safety Domain (SA-1 to SA-8)
    {
        "code": "SA-1",
        "text": "What potential safety risks or harms could your AI system pose?",
        "explanation": "Identifying potential safety risks is the first step in AI safety management. This question assesses your risk identification and analysis capabilities. Safety risks vary by application but might include physical harm (autonomous vehicles), psychological harm (biased recommendations), economic harm (unfair lending), or societal harm (misinformation spread). Risk identification should consider both intended and unintended consequences, direct and indirect effects, and impacts on different stakeholder groups. Comprehensive risk identification informs appropriate safety measures.",
        "domain_order": 9,
        "order": 1
    },
    {
        "code": "SA-2",
        "text": "What safety measures and safeguards have you implemented?",
        "explanation": "Safety measures and safeguards protect against identified risks and ensure safe AI system operation. This question evaluates your risk mitigation strategies. Safeguards might include input validation, output bounds checking, human oversight requirements, emergency stop mechanisms, redundant systems, or conservative decision-making under uncertainty. The specific measures depend on identified risks and safety requirements. Effective safeguards should be proportionate to risks and regularly tested for effectiveness.",
        "domain_order": 9,
        "order": 2
    },
    {
        "code": "SA-3",
        "text": "How do you test for safety in various scenarios, including edge cases?",
        "explanation": "Safety testing evaluates AI system behavior under various conditions, including unusual or extreme scenarios where safety risks might emerge. This question assesses your safety validation practices. Testing might include scenario-based testing, stress testing, fault injection, adversarial testing, or simulation of rare events. Edge case testing is particularly important because these situations often reveal safety vulnerabilities not apparent in normal operation. Comprehensive safety testing helps ensure robust performance across diverse conditions.",
        "domain_order": 9,
        "order": 3
    },
    {
        "code": "SA-4",
        "text": "What monitoring is in place to detect unsafe behavior or outcomes?",
        "explanation": "Safety monitoring provides ongoing surveillance for unsafe AI system behavior or outcomes. This question evaluates your safety monitoring infrastructure. Monitoring might include real-time safety metric tracking, anomaly detection, user feedback collection, incident reporting systems, or external safety audits. Effective monitoring should detect safety issues quickly and trigger appropriate responses. The monitoring approach should be tailored to identified safety risks and system criticality.",
        "domain_order": 9,
        "order": 4
    },
    {
        "code": "SA-5",
        "text": "How do you handle situations where the AI system's output could lead to harm?",
        "explanation": "Harm prevention procedures ensure appropriate responses when AI systems might cause harm. This question assesses your harm mitigation protocols. Responses might include human review requirements, conservative default actions, user warnings, system shutdown procedures, or escalation to safety personnel. The response should be proportionate to potential harm severity and include clear criteria for when different responses are triggered. Effective harm prevention balances safety with system utility.",
        "domain_order": 9,
        "order": 5
    },
    {
        "code": "SA-6",
        "text": "What role does human oversight play in ensuring AI system safety?",
        "explanation": "Human oversight provides essential safety checks and intervention capabilities for AI systems. This question evaluates your human-AI collaboration for safety. Human oversight might include human-in-the-loop decision making, human approval for high-risk decisions, monitoring dashboards for safety personnel, or override capabilities. The level of human involvement should be appropriate for safety risks and system criticality. Effective oversight requires properly trained personnel and clear intervention protocols.",
        "domain_order": 9,
        "order": 6
    },
    {
        "code": "SA-7",
        "text": "How do you ensure safety when updating or modifying the AI system?",
        "explanation": "Change management for AI systems ensures that updates and modifications don't introduce new safety risks or compromise existing safeguards. This question assesses your safety practices during system evolution. Safety procedures might include safety review of changes, regression testing, gradual rollout with monitoring, rollback procedures, or safety certification for modifications. The rigor of change management should be proportionate to system criticality and potential safety impacts.",
        "domain_order": 9,
        "order": 7
    },
    {
        "code": "SA-8",
        "text": "What emergency procedures are in place if safety issues arise?",
        "explanation": "Emergency procedures provide rapid response capabilities when safety issues arise with AI systems. This question evaluates your incident response and crisis management capabilities. Emergency procedures might include immediate system shutdown, switching to backup systems, escalation to safety personnel, user notifications, or regulatory reporting. Procedures should be well-documented, regularly tested, and enable rapid response to minimize harm. Emergency preparedness is particularly important for high-risk AI applications.",
        "domain_order": 9,
        "order": 8
    },
    
    # Inclusivity Domain (IN-1 to IN-8)
    {
        "code": "IN-1",
        "text": "How do you ensure your AI system is accessible to users with disabilities?",
        "explanation": "Accessibility ensures that AI systems can be used by people with diverse abilities and disabilities. This question assesses your accessibility design and testing practices. Accessibility considerations might include screen reader compatibility, keyboard navigation, voice input options, visual contrast requirements, or alternative interaction modalities. Compliance with accessibility standards (like WCAG) and testing with assistive technologies helps ensure inclusive design. Accessibility should be considered throughout design and development, not added afterwards.",
        "domain_order": 10,
        "order": 1
    },
    {
        "code": "IN-2",
        "text": "What steps have you taken to ensure your AI system works well for diverse user populations?",
        "explanation": "Inclusive design ensures AI systems work effectively for users across different demographics, cultures, languages, and contexts. This question evaluates your inclusive design practices. Considerations might include cultural sensitivity, language support, diverse use cases, varying technical literacy levels, or different socioeconomic contexts. Inclusive design requires diverse perspectives in development teams, user research across different populations, and testing with representative user groups.",
        "domain_order": 10,
        "order": 2
    },
    {
        "code": "IN-3",
        "text": "How do you address language and cultural barriers in your AI system?",
        "explanation": "Language and cultural barriers can exclude users from AI system benefits. This question assesses your approach to linguistic and cultural inclusion. Considerations might include multi-language support, cultural adaptation of content, culturally appropriate interaction patterns, or region-specific customizations. Addressing these barriers might involve translation services, cultural consultation, local user research, or culturally diverse development teams. The goal is ensuring the system is usable and appropriate across different cultural contexts.",
        "domain_order": 10,
        "order": 3
    },
    {
        "code": "IN-4",
        "text": "What measures are in place to prevent the exclusion of certain groups from benefiting from your AI system?",
        "explanation": "Preventing exclusion ensures that AI systems don't inadvertently deny benefits to particular groups. This question evaluates your inclusion monitoring and mitigation practices. Exclusion might occur through biased algorithms, inaccessible interfaces, high costs, complex requirements, or limited availability. Prevention measures might include bias testing, accessibility auditing, affordability programs, simplified interfaces, or targeted outreach. The goal is ensuring equitable access to AI system benefits.",
        "domain_order": 10,
        "order": 4
    },
    {
        "code": "IN-5",
        "text": "How do you involve diverse stakeholders in the development and testing of your AI system?",
        "explanation": "Diverse stakeholder involvement ensures that different perspectives and needs are considered throughout AI system development. This question assesses your participatory design and testing practices. Stakeholder involvement might include diverse user research, community advisory boards, co-design sessions, diverse testing groups, or feedback collection from underrepresented communities. Effective involvement should be meaningful (not tokenistic), ongoing (throughout development), and influential (affecting design decisions).",
        "domain_order": 10,
        "order": 5
    },
    {
        "code": "IN-6",
        "text": "What efforts are made to understand and address the needs of underrepresented communities?",
        "explanation": "Understanding and addressing underrepresented community needs ensures that AI systems serve all populations equitably. This question evaluates your outreach and needs assessment practices. Efforts might include community partnerships, targeted user research, advocacy group consultation, or specialized testing with underrepresented groups. Understanding needs requires ongoing engagement, cultural competency, and willingness to adapt systems based on community feedback. The goal is ensuring AI systems are relevant and beneficial for all user populations.",
        "domain_order": 10,
        "order": 6
    },
    {
        "code": "IN-7",
        "text": "How do you measure and monitor inclusivity in your AI system's design and outcomes?",
        "explanation": "Inclusivity measurement and monitoring provide objective assessment of how well AI systems serve diverse populations. This question evaluates your inclusivity metrics and monitoring practices. Metrics might include usage patterns across demographic groups, satisfaction scores by population, accessibility compliance measures, or representation in training data. Monitoring should be ongoing and lead to corrective actions when inclusivity gaps are identified. Effective measurement helps ensure inclusivity goals are met in practice.",
        "domain_order": 10,
        "order": 7
    },
    {
        "code": "IN-8",
        "text": "What training or guidelines are provided to your team on inclusive AI development?",
        "explanation": "Team training and guidelines ensure that inclusivity considerations are embedded in AI development practices. This question assesses your capacity building for inclusive design. Training might cover unconscious bias, accessibility standards, cultural competency, inclusive design principles, or specific techniques for bias mitigation. Guidelines should provide practical direction for incorporating inclusivity throughout development. Effective training creates a culture where inclusivity is valued and practitioners have the skills to implement inclusive practices.",
        "domain_order": 10,
        "order": 8
    },
    
    # Sustainability Domain (SU-1 to SU-8)
    {
        "code": "SU-1",
        "text": "What is the environmental impact of your AI system's computational requirements?",
        "explanation": "AI systems, particularly large models, can have significant environmental impact through energy consumption and carbon emissions. This question assesses your environmental impact awareness and measurement. Environmental impact includes energy use during training and inference, cooling requirements, hardware manufacturing impact, and associated carbon emissions. Understanding impact requires measuring or estimating energy consumption, considering energy sources (renewable vs. fossil fuels), and accounting for the full system lifecycle. This awareness is the first step toward sustainable AI practices.",
        "domain_order": 11,
        "order": 1
    },
    {
        "code": "SU-2",
        "text": "What measures have you taken to optimize energy efficiency in your AI system?",
        "explanation": "Energy efficiency optimization reduces the environmental impact and operational costs of AI systems. This question evaluates your energy optimization practices. Measures might include model compression, quantization, pruning, efficient architectures, optimized hardware utilization, or algorithmic improvements. Infrastructure optimizations could include efficient cooling, renewable energy use, or workload scheduling to align with clean energy availability. The goal is minimizing energy consumption while maintaining acceptable performance.",
        "domain_order": 11,
        "order": 2
    },
    {
        "code": "SU-3",
        "text": "How do you consider the lifecycle environmental impact of your AI system?",
        "explanation": "Lifecycle environmental impact assessment considers the full environmental footprint of AI systems from development through disposal. This question evaluates your sustainability assessment practices. Lifecycle impacts include hardware manufacturing, transportation, energy consumption during operation, cooling requirements, maintenance, and end-of-life disposal. Assessment might use lifecycle assessment (LCA) methodologies, carbon footprint calculations, or environmental management systems. Comprehensive assessment helps identify optimization opportunities across the entire system lifecycle.",
        "domain_order": 11,
        "order": 3
    },
    {
        "code": "SU-4",
        "text": "What sustainable practices are integrated into your AI development process?",
        "explanation": "Sustainable development practices embed environmental considerations into AI system design and development. This question assesses your green software development practices. Sustainable practices might include efficient algorithm design, green computing principles, sustainable hardware choices, carbon-aware development, or environmental impact assessment in design decisions. Development practices could include code optimization for efficiency, choosing sustainable cloud providers, or designing for longevity to reduce replacement needs.",
        "domain_order": 11,
        "order": 4
    },
    {
        "code": "SU-5",
        "text": "How do you measure and report on the sustainability metrics of your AI system?",
        "explanation": "Sustainability measurement and reporting provide transparency and accountability for environmental impact. This question evaluates your sustainability metrics and reporting practices. Metrics might include energy consumption, carbon emissions, resource utilization, waste generation, or efficiency improvements. Reporting could include sustainability reports, carbon footprint disclosures, or environmental performance indicators. Regular measurement and transparent reporting demonstrate commitment to sustainability and enable continuous improvement.",
        "domain_order": 11,
        "order": 5
    },
    {
        "code": "SU-6",
        "text": "What steps are taken to minimize resource waste in your AI operations?",
        "explanation": "Resource waste minimization reduces environmental impact and operational costs. This question assesses your resource efficiency practices. Waste reduction might include optimizing compute resource utilization, reducing idle resources, efficient data storage, minimizing data transfer, or extending hardware lifecycle. Practices could include resource monitoring, automated scaling, workload optimization, or circular economy principles in hardware management. The goal is maximizing value from resources while minimizing waste.",
        "domain_order": 11,
        "order": 6
    },
    {
        "code": "SU-7",
        "text": "How do you balance performance requirements with environmental sustainability?",
        "explanation": "Balancing performance and sustainability requires trade-off analysis and optimization strategies. This question evaluates your approach to managing competing objectives. Balancing might involve performance-efficiency trade-offs, sustainable performance targets, green performance metrics, or multi-objective optimization. Strategies could include adaptive performance based on energy availability, sustainable computing paradigms, or performance requirements that consider environmental cost. Effective balancing achieves necessary performance while minimizing environmental impact.",
        "domain_order": 11,
        "order": 7
    },
    {
        "code": "SU-8",
        "text": "What long-term sustainability goals do you have for your AI system?",
        "explanation": "Long-term sustainability goals provide direction for continuous environmental improvement. This question assesses your sustainability strategy and commitment. Goals might include carbon neutrality targets, renewable energy transition, circular economy adoption, or specific emission reduction targets. Goal-setting should include measurable targets, timelines, and accountability mechanisms. Long-term goals demonstrate commitment to sustainability and provide framework for investment and improvement decisions.",
        "domain_order": 11,
        "order": 8
    }
]

# All 88 questions across 11 domains are now complete with explanations
