# Complete question data from AMAISAFE_Qs_and_As.csv spreadsheet
# This contains all 88 questions across 11 domains with complete explanations and pre-defined answers

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
        "explanation": "AI systems learn from the data they are trained on. If the data lacks representation from certain demographics, the system might perform poorly or unfairly for those groups. This question assesses your practices for ensuring training data is diverse and representative of the populations the AI will interact with.\n\nFor example, if a facial recognition system is trained primarily on images of light-skinned individuals, it might not accurately recognize darker-skinned individuals. To address this, you might source data from multiple demographic groups and evaluate its representativeness.",
        "ideal_answer": "Conduct demographic analysis and source additional data to address gaps in representation.",
        "good_answer": "Use synthetic data to improve representation where demographic gaps exist.",
        "basic_answer": "Use third-party data sources but perform minimal validation for demographic representation.",
        "non_ideal_answer": "No specific actions are taken to ensure demographic representation.",
        "domain_order": 1,
        "order": 2
    },
    {
        "code": "FA-3",
        "text": "Have you evaluated the system's outputs for potential disparities across user groups?",
        "explanation": "This question focuses on whether you've analyzed the AI system's outputs to identify if certain groups experience unequal treatment or outcomes.\n\nFor instance, a loan approval system might disproportionately deny loans to specific racial or gender groups. Evaluating outputs involves comparing decision rates, accuracy, or other metrics across groups to identify disparities. Tools such as disparity analysis or fairness dashboards can assist in uncovering issues during testing or post-deployment.",
        "ideal_answer": "Conduct detailed quantitative analysis and qualitative testing with diverse focus groups to identify disparities.",
        "good_answer": "Regularly monitor outputs during operation for potential discrepancies across groups.",
        "basic_answer": "Limited evaluation performed only during system testing phases.",
        "non_ideal_answer": "No evaluations have been conducted.",
        "domain_order": 1,
        "order": 3
    },
    {
        "code": "FA-4",
        "text": "How do you measure fairness in your AI system's outputs?",
        "explanation": "Fairness is a multifaceted concept that varies depending on the context. This question asks you to define and measure fairness within your use case.\n\nFor example, in healthcare, fairness might mean equal diagnostic accuracy across demographics, while in credit scoring, it might mean equal access to credit opportunities. Common fairness metrics include demographic parity, equal opportunity, and predictive parity. By defining measurable fairness objectives, you create a clear benchmark for evaluation.",
        "ideal_answer": "Use fairness metrics such as demographic parity or equal opportunity and conduct regular evaluations against these benchmarks.",
        "good_answer": "Conduct statistical comparisons across user groups to identify potential inequities.",
        "basic_answer": "Monitor fairness qualitatively through user feedback and sporadic reviews.",
        "non_ideal_answer": "No specific fairness metrics are defined or monitored.",
        "domain_order": 1,
        "order": 4
    },
    {
        "code": "FA-5",
        "text": "Have you tested the system for potential biases in real-world scenarios?",
        "explanation": "AI systems can behave differently in controlled environments versus real-world applications. This question ensures that your system has been tested in the environments it is intended for, to identify hidden biases.\n\nFor example, an AI chatbot might work equally well across demographics during development but fail to understand slang or dialects used by certain groups in practice. Testing in real-world scenarios helps uncover such gaps and ensures fairness in deployment.",
        "ideal_answer": "Conduct comprehensive testing with real-world data and scenarios before deployment.",
        "good_answer": "Perform pilot programs in controlled real-world environments to assess biases.",
        "basic_answer": "Conduct periodic testing post-deployment but limited pre-deployment analysis.",
        "non_ideal_answer": "No real-world bias testing has been conducted.",
        "domain_order": 1,
        "order": 5
    },
    {
        "code": "FA-6",
        "text": "Are you using any frameworks or tools (e.g., Fairlearn) to assess and mitigate bias?",
        "explanation": "Frameworks and tools like Fairlearn, Aequitas, or IBM's AI Fairness 360 can help automate bias detection and mitigation, providing actionable insights. This question evaluates whether you've leveraged such resources to enhance your AI system's fairness.\n\nFor example, Fairlearn offers disparity metrics and bias mitigation algorithms, allowing you to iteratively refine your model to reduce bias. Using these tools demonstrates a structured approach to fairness.",
        "ideal_answer": "Use frameworks like Fairlearn, Aequitas, or IBM AI Fairness 360 to identify and mitigate biases systematically.",
        "good_answer": "Use in-house frameworks or processes for bias detection and mitigation.",
        "basic_answer": "Researching frameworks but have not yet implemented any tools.",
        "non_ideal_answer": "No frameworks or tools are being used at this time.",
        "domain_order": 1,
        "order": 6
    },
    {
        "code": "FA-7",
        "text": "How do you ensure fairness in decision-making for minority or underserved groups?",
        "explanation": "AI systems can inadvertently perpetuate systemic inequalities, making it critical to safeguard fairness for minority or underserved populations. This question examines whether your design and evaluation processes prioritize equitable treatment for such groups.\n\nFor instance, a job-matching platform might weigh features differently for candidates from underserved communities to account for historical disadvantages. Tailored fairness policies or post-processing adjustments to outputs can address such disparities.",
        "ideal_answer": "Introduce fairness weights or adjustments during model training and evaluate outputs specifically for underserved groups.",
        "good_answer": "Perform targeted testing and involve stakeholders from minority communities during the design and evaluation phases.",
        "basic_answer": "Review decisions occasionally for fairness but lack structured measures for minority groups.",
        "non_ideal_answer": "No specific measures are implemented to ensure fairness for underserved groups.",
        "domain_order": 1,
        "order": 7
    },
    {
        "code": "FA-8",
        "text": "Is fairness embedded in your AI model's design process, or is it addressed post-deployment?",
        "explanation": "Embedding fairness into the design phase is more effective and cost-efficient than addressing it after deployment. This question explores whether fairness considerations are integral to your AI lifecycle or if they are treated as reactive fixes.\n\nFor example, you might incorporate fairness objectives during data collection, model selection, and training. Conversely, addressing fairness post-deployment might involve auditing outputs and retrofitting models with mitigation strategies. Proactively embedding fairness minimizes risks and ensures a more ethical AI system.",
        "ideal_answer": "Fairness considerations are embedded throughout the design and development process.",
        "good_answer": "Address fairness primarily during pre-deployment testing and adjustments.",
        "basic_answer": "Evaluate fairness reactively, post-deployment, as issues arise.",
        "non_ideal_answer": "Fairness is not currently a structured consideration in the workflow.",
        "domain_order": 1,
        "order": 8
    },
    # Transparency Domain (TR-1 to TR-8) - Domain order 2
    {
        "code": "TR-1",
        "text": "What level of detail about the AI system's functionality and limitations is communicated to users or stakeholders?",
        "explanation": "Transparency involves making the capabilities and boundaries of your AI system clear to all relevant parties. This question seeks to understand how much information you share with users and stakeholders about what the AI can and cannot do.\n\nFor example, if you're using an AI chatbot, do users know when the bot might escalate to a human? Clearly communicating limitations—such as restricted language understanding or potential biases—helps manage expectations and build trust. Providing user guides, FAQs, or disclosure statements can be effective ways to address this.",
        "ideal_answer": "Detailed user guides and technical documentation, including functionality and limitations, are provided to all relevant stakeholders.",
        "good_answer": "Key functionalities and limitations are highlighted in FAQs or disclosure statements.",
        "basic_answer": "High-level overviews are shared without detailed explanations.",
        "non_ideal_answer": "Minimal or no information is shared about the AI system's functionality or limitations.",
        "domain_order": 2,
        "order": 1
    },
    {
        "code": "TR-2",
        "text": "How do you document the data sources, algorithms, and processes used in your AI system?",
        "explanation": "Documentation is critical for accountability and auditability. This question assesses whether you maintain detailed records of your data sources, algorithms, and processes.\n\nFor instance, if your AI system recommends medical treatments, can you trace the data sources and algorithm logic behind each recommendation? Proper documentation includes maintaining version histories, recording preprocessing methods, and noting data transformations, making it easier to explain how decisions are made and to troubleshoot issues.",
        "ideal_answer": "Comprehensive documentation of data sources, preprocessing steps, algorithms, and processes is maintained and regularly updated.",
        "good_answer": "Data sources and algorithms are documented at a high level without extensive detail.",
        "basic_answer": "Documentation exists but is incomplete or outdated.",
        "non_ideal_answer": "No formal documentation process is in place.",
        "domain_order": 2,
        "order": 2
    },
    {
        "code": "TR-3",
        "text": "Are there mechanisms for external parties (e.g., regulators or customers) to understand how your AI system works?",
        "explanation": "External parties, such as regulators or customers, often need insights into your AI system to ensure compliance and accountability. This question asks whether you provide tools, interfaces, or documentation to help external stakeholders understand your AI system.\n\nFor example, a financial institution might share audit logs or offer sandbox environments for regulators to test the system's behavior. Mechanisms like model interpretability reports or interactive dashboards can also help external parties verify compliance with ethical or legal standards.",
        "ideal_answer": "Provide transparency reports, detailed system documentation, or interactive dashboards for external review.",
        "good_answer": "Share limited insights or high-level summaries upon request from regulators or key customers.",
        "basic_answer": "Offer minimal explanations to external parties, such as one-off presentations.",
        "non_ideal_answer": "No mechanisms are available for external parties to understand the system.",
        "domain_order": 2,
        "order": 3
    },
    {
        "code": "TR-4",
        "text": "How is information about your AI system shared with internal teams and external stakeholders?",
        "explanation": "Effective communication ensures alignment and accountability within and outside your organization. This question examines how you share AI-related information across teams and with external stakeholders.\n\nFor example, do internal developers and business users have access to detailed design documentation, or do customers receive user-friendly descriptions of how the system operates? Using channels like training sessions, technical briefs, or customer-facing transparency portals can help ensure everyone understands the system's functionality.",
        "ideal_answer": "Information is shared through structured processes, including regular presentations, training sessions, and detailed documentation.",
        "good_answer": "Information is shared selectively with internal teams and stakeholders based on their needs.",
        "basic_answer": "Information is only shared reactively, often when specifically requested.",
        "non_ideal_answer": "No structured process exists for sharing AI-related information.",
        "domain_order": 2,
        "order": 4
    },
    {
        "code": "TR-5",
        "text": "Are there any \"black-box\" components in your system that could impede transparency?",
        "explanation": "Black-box models, where decision-making processes are opaque, can undermine trust and accountability. This question investigates whether your system contains such components and what measures you've taken to mitigate their impact.\n\nFor instance, a deep learning model used for credit scoring might be difficult to interpret. To address this, you could implement supplementary tools like SHAP or LIME to explain the factors influencing specific outcomes. Minimizing reliance on black-box components wherever feasible can enhance transparency.",
        "ideal_answer": "No, the system is fully explainable with no black-box components.",
        "good_answer": "The system includes black-box components, but explainability tools (e.g., SHAP, LIME) are used to enhance transparency.",
        "basic_answer": "Black-box components exist, but no measures are in place to explain their behavior.",
        "non_ideal_answer": "Unsure about the presence of black-box components.",
        "domain_order": 2,
        "order": 5
    },
    {
        "code": "TR-6",
        "text": "How do you disclose the sources of data and algorithms used in the AI system?",
        "explanation": "Disclosing data and algorithm sources provides context for the decisions your AI system makes and builds stakeholder trust. This question assesses whether you're transparent about where your data comes from and how algorithms are designed.\n\nFor example, if you're using third-party datasets, do you inform users of their origin and any associated limitations? Similarly, do you disclose whether the algorithms are proprietary, open-source, or modified from existing frameworks? Ensuring clear disclosures avoids misunderstandings and promotes accountability.",
        "ideal_answer": "Fully disclose data sources and algorithmic details, including limitations and provenance, to stakeholders.",
        "good_answer": "Provide high-level descriptions of data and algorithm sources without detailed explanations.",
        "basic_answer": "Data and algorithms are treated as proprietary and shared only selectively.",
        "non_ideal_answer": "No practice exists for disclosing data and algorithm sources.",
        "domain_order": 2,
        "order": 6
    },
    {
        "code": "TR-7",
        "text": "Are users made aware when they are interacting with an AI system?",
        "explanation": "It's essential for users to know when they're engaging with an AI system rather than a human, as it affects their expectations and trust. This question ensures you have mechanisms in place to inform users about AI interactions.\n\nFor instance, a customer support chatbot could include a message such as, \"I'm an AI assistant here to help.\" Clearly distinguishing AI from human interactions ensures users understand the nature of their engagement and can act accordingly.",
        "ideal_answer": "Users are clearly notified through explicit messages or labels (e.g., \"This is an AI system\").",
        "good_answer": "Users can infer they are interacting with AI based on the context but are not explicitly informed.",
        "basic_answer": "Users are rarely or inconsistently informed about AI interactions.",
        "non_ideal_answer": "Users are not informed when interacting with an AI system.",
        "domain_order": 2,
        "order": 7
    },
    {
        "code": "TR-8",
        "text": "Do you publish any transparency reports or documentation for regulators or customers?",
        "explanation": "Transparency reports or similar documentation provide stakeholders with a comprehensive overview of how your AI system operates and its compliance with ethical, legal, or performance standards. This question assesses whether you regularly publish such reports.\n\nFor example, an organization deploying facial recognition technology might release annual transparency reports detailing error rates, privacy safeguards, and usage scenarios. These reports can be tailored for regulators to demonstrate compliance or for customers to build trust.",
        "ideal_answer": "Publish regular, comprehensive transparency reports detailing system functionality, performance, and compliance.",
        "good_answer": "Provide transparency documentation selectively upon request from specific audiences.",
        "basic_answer": "Publish limited transparency reports on an ad hoc basis.",
        "non_ideal_answer": "No transparency reports or documentation are published.",
        "domain_order": 2,
        "order": 8
    }
    # Explainability Domain (EX-1 to EX-8) - Domain order 3
    {
        "code": "EX-1",
        "text": "How do you decide the level of explainability required for your AI system?",
        "explanation": "The level of explainability required for an AI system depends on its use case, stakeholders, and potential impact. This question asks how you determine the depth and complexity of explanations needed.\n\nFor example, a medical diagnosis AI system may require detailed explanations to help doctors trust its recommendations, while a simple AI-driven shopping assistant might only need basic reasoning for its suggestions. Consider who interacts with the system (e.g., end-users, regulators, or internal teams) and the consequences of its decisions when defining explainability requirements.",
        "ideal_answer": "Explainability requirements are determined based on the criticality of the AI system, potential impacts, and stakeholder needs, with clear criteria established.",
        "good_answer": "Explainability is tailored to regulatory requirements and specific user groups (e.g., technical vs. non-technical stakeholders).",
        "basic_answer": "Explainability needs are addressed reactively, focusing on feedback or complaints from users.",
        "non_ideal_answer": "Explainability is not currently a formal consideration in system design.",
        "domain_order": 3,
        "order": 1
    },
    {
        "code": "EX-2",
        "text": "What methods are used to test whether explanations are understandable by non-technical users?",
        "explanation": "Explainability isn't just about providing an explanation; it's about ensuring the explanation is accessible to its intended audience. This question examines how you test whether non-technical users can comprehend the explanations provided by the system.\n\nFor instance, you might use user testing sessions where participants evaluate the clarity of explanations. An AI system used in loan applications, for example, could include reasons for denial in plain language, such as \"Your credit score is below the required threshold,\" rather than presenting technical metrics.",
        "ideal_answer": "Conduct user testing with diverse, non-technical participants and iterate based on their feedback to ensure clarity.",
        "good_answer": "Collect feedback from end-users during system trials or pilot programs and adjust explanations as needed.",
        "basic_answer": "Use internal reviews and heuristic evaluations to gauge understandability.",
        "non_ideal_answer": "No testing is conducted to determine whether explanations are understandable.",
        "domain_order": 3,
        "order": 2
    },
    {
        "code": "EX-3",
        "text": "Do you provide explanations in different formats (e.g., visualizations, text summaries) for different audiences?",
        "explanation": "Different audiences may require explanations in varying formats to suit their needs and expertise. This question assesses whether you tailor your system's explainability features accordingly.\n\nFor example, a financial AI system might use visualizations like bar graphs to show how different factors influence loan approvals for analysts, while providing simple text summaries for customers. Offering multiple formats ensures that both technical and non-technical stakeholders can understand the system's reasoning.",
        "ideal_answer": "Provide multiple explanation formats (e.g., graphs for analysts, text summaries for end-users) tailored to the needs of diverse audiences.",
        "good_answer": "Offer explanations in at least one format designed for the primary audience of the system.",
        "basic_answer": "Explanations are limited to a single, general-purpose format.",
        "non_ideal_answer": "Explanations are not currently provided in any format.",
        "domain_order": 3,
        "order": 3
    },
    {
        "code": "EX-4",
        "text": "How do you evaluate the accuracy and completeness of the explanations provided?",
        "explanation": "Explanations must accurately reflect the system's decision-making process and include all relevant details. This question ensures you have processes to validate the accuracy and completeness of your explanations.\n\nFor example, if an AI model predicts a customer's likelihood to churn, the explanation should detail all contributing factors, such as reduced spending or lower engagement. Regular audits and user feedback can help identify gaps or inaccuracies in explanations and improve their quality.",
        "ideal_answer": "Regularly validate explanations through user feedback, audits, and comparison with the system's decision logic.",
        "good_answer": "Conduct periodic reviews of explanations and refine them based on stakeholder input.",
        "basic_answer": "Perform ad hoc evaluations of explanations without structured processes.",
        "non_ideal_answer": "No formal evaluation process for explanation accuracy is in place.",
        "domain_order": 3,
        "order": 4
    },
    {
        "code": "EX-5",
        "text": "Are there trade-offs between model complexity and explainability in your system design?",
        "explanation": "Complex AI models, such as deep learning, often provide better performance but are harder to explain, while simpler models are more interpretable but may sacrifice accuracy. This question explores how you manage these trade-offs in your system's design.\n\nFor instance, you might use a simpler, interpretable model for high-stakes applications like loan approvals, where explainability is critical, while deploying more complex models for lower-risk tasks like product recommendations. Balancing performance and explainability ensures the system meets both operational and ethical requirements.",
        "ideal_answer": "Explicitly balance complexity and explainability, simplifying models or using interpretable methods where appropriate.",
        "good_answer": "Leverage tools like SHAP or LIME to explain complex models without simplifying them.",
        "basic_answer": "Recognize the trade-off but prioritize model performance over explainability.",
        "non_ideal_answer": "No trade-offs are considered; explainability is not prioritized.",
        "domain_order": 3,
        "order": 5
    },
    {
        "code": "EX-6",
        "text": "How do you ensure the decisions made by your AI system are interpretable by users?",
        "explanation": "Interpretability refers to making it clear why the AI system made a specific decision. This question asks how you design the system to provide explanations that users can understand and trust.\n\nFor example, an AI system used in hiring could highlight the key skills and experiences from a candidate's profile that influenced its ranking. Designing interfaces that clearly present the reasoning behind decisions can help users trust and engage with the system.",
        "ideal_answer": "Provide user-friendly interfaces that present clear reasoning and key factors influencing decisions.",
        "good_answer": "Incorporate explainability tools to help users interpret decisions.",
        "basic_answer": "Offer explanations only in technical terms, requiring domain knowledge to interpret.",
        "non_ideal_answer": "No specific measures are taken to ensure decision interpretability.",
        "domain_order": 3,
        "order": 6
    },
    {
        "code": "EX-7",
        "text": "What tools or techniques (e.g., SHAP, LIME) do you use to make complex models more explainable?",
        "explanation": "Explainability tools like SHAP (SHapley Additive exPlanations) or LIME (Local Interpretable Model-Agnostic Explanations) help make complex models understandable. This question evaluates whether you're using these or similar tools to enhance explainability.\n\nFor instance, SHAP can show the contribution of each feature to a model's prediction, helping users understand why an AI system made a certain decision. Employing such tools demonstrates your commitment to transparency and accountability.",
        "ideal_answer": "Use advanced tools like SHAP, LIME, or similar techniques to systematically explain model outputs.",
        "good_answer": "Develop in-house tools or techniques tailored to specific models to enhance explainability.",
        "basic_answer": "Use basic rule-based approaches or manual interpretation to explain decisions.",
        "non_ideal_answer": "No tools or techniques are currently used for improving explainability.",
        "domain_order": 3,
        "order": 7
    },
    {
        "code": "EX-8",
        "text": "Are there specific groups (e.g., end-users, regulators, or internal teams) for whom explanations of AI outputs are tailored?",
        "explanation": "Different groups interacting with your AI system may require explanations tailored to their needs and expertise. This question examines whether you customize explanations based on the audience.\n\nFor example, regulators may need detailed documentation of how the system complies with laws, while end-users may need simple, actionable reasons for outputs. Tailoring explanations ensures that all stakeholders, regardless of technical background, can understand and engage with the system effectively.",
        "ideal_answer": "Explanations are customized for each group (e.g., simplified for end-users, detailed for regulators, and actionable for internal teams).",
        "good_answer": "Explanations are tailored for at least one key audience, such as end-users or regulators.",
        "basic_answer": "Explanations are standardized and not customized for specific groups.",
        "non_ideal_answer": "No explanations are provided for any group.",
        "domain_order": 3,
        "order": 8
    },
    # Accountability Domain (AC-1 to AC-8) - Domain order 4
    {
        "code": "AC-1",
        "text": "How is accountability for AI system failures managed within your organization?",
        "explanation": "Accountability ensures that there are clear processes and responsible parties to address AI system failures. This question assesses your organization's ability to identify and resolve issues when things go wrong.\n\nFor example, if an AI-driven hiring system rejects qualified candidates due to a bias in its algorithm, who is responsible for investigating and resolving the issue? Effective management involves documenting failure protocols, assigning roles, and ensuring all stakeholders know their responsibilities when a failure occurs.",
        "ideal_answer": "Clear accountability protocols are established, with designated teams responsible for identifying, resolving, and documenting failures.",
        "good_answer": "General guidelines for managing failures exist, but roles and responsibilities are not explicitly assigned.",
        "basic_answer": "Failures are addressed on an ad hoc basis without formal protocols.",
        "non_ideal_answer": "There is no process in place to manage AI system failures.",
        "domain_order": 4,
        "order": 1
    },
    {
        "code": "AC-2",
        "text": "What governance structures (e.g., AI oversight boards) are in place to monitor AI outcomes?",
        "explanation": "Governance structures are critical for overseeing AI systems and ensuring they operate within ethical, legal, and performance standards. This question examines whether you have mechanisms like AI oversight boards, committees, or policies in place to regularly review the outcomes of your AI systems.\n\nFor instance, a financial services company might establish a governance board to review algorithmic fairness and compliance with regulatory requirements. These structures provide a framework for accountability and continuous improvement.",
        "ideal_answer": "A dedicated AI oversight board or committee is in place to regularly review and monitor system outcomes.",
        "good_answer": "Governance structures exist but operate informally or without regular reviews.",
        "basic_answer": "Governance responsibilities are delegated to individual teams without overarching oversight.",
        "non_ideal_answer": "No governance structures are in place to monitor AI outcomes.",
        "domain_order": 4,
        "order": 2
    },
    {
        "code": "AC-3",
        "text": "Are there policies for escalating issues identified in the AI system?",
        "explanation": "Not all issues can be resolved at the operational level; some may require escalation to higher authorities or specialized teams. This question ensures you have clear escalation policies in place for handling significant issues.\n\nFor example, if a critical safety flaw is detected in an AI-powered autonomous vehicle system, does your escalation policy ensure rapid communication to executives and external regulators? Having defined escalation paths helps prevent delays in addressing high-stakes problems.",
        "ideal_answer": "Formal escalation policies are documented, with clear paths for resolving critical issues efficiently.",
        "good_answer": "Escalation policies exist but are inconsistently applied or understood.",
        "basic_answer": "Issues are escalated informally, relying on individual discretion.",
        "non_ideal_answer": "There are no policies in place for escalating issues.",
        "domain_order": 4,
        "order": 3
    },
    {
        "code": "AC-4",
        "text": "How do you handle customer complaints or disputes related to AI outputs?",
        "explanation": "Customer complaints or disputes over AI decisions must be handled transparently and efficiently to maintain trust. This question evaluates whether you have processes for addressing such concerns.\n\nFor example, if a customer disputes a credit denial made by your AI system, do you offer a clear path for appeal or manual review? Providing explanations for decisions and offering a human review option when disputes arise ensures accountability and user satisfaction.",
        "ideal_answer": "A structured process is in place for addressing complaints, including a clear escalation path and manual review options.",
        "good_answer": "Customer complaints are reviewed and addressed, but processes are informal or inconsistent.",
        "basic_answer": "Complaints are handled reactively on a case-by-case basis without formal procedures.",
        "non_ideal_answer": "There is no process in place for handling customer complaints or disputes.",
        "domain_order": 4,
        "order": 4
    },
    {
        "code": "AC-5",
        "text": "Are roles and responsibilities for AI governance clearly defined across teams?",
        "explanation": "AI governance requires collaboration across technical, legal, and operational teams, and clearly defined roles are essential for accountability. This question seeks to determine whether responsibilities, such as monitoring outcomes, managing data, or ensuring compliance, are allocated and understood.\n\nFor instance, does the data science team oversee model accuracy, while the compliance team monitors adherence to regulations? Clarity in roles minimizes confusion and ensures that accountability is shared appropriately.",
        "ideal_answer": "Roles and responsibilities are clearly defined, documented, and regularly reviewed to ensure alignment across teams.",
        "good_answer": "Roles and responsibilities are defined but not consistently communicated or updated.",
        "basic_answer": "Governance responsibilities are loosely defined, often leading to overlap or confusion.",
        "non_ideal_answer": "Roles and responsibilities for AI governance are not defined.",
        "domain_order": 4,
        "order": 5
    },
    {
        "code": "AC-6",
        "text": "Who is responsible for monitoring and managing the AI system throughout its lifecycle?",
        "explanation": "AI systems require ongoing monitoring and management to address changes in data, usage, or external conditions. This question examines whether you have designated individuals or teams to oversee the system's performance and compliance over time.\n\nFor example, an e-commerce AI recommendation system may need periodic updates to reflect changes in customer behavior. Assigning lifecycle management responsibilities ensures consistent performance and mitigates risks such as model drift or outdated assumptions.",
        "ideal_answer": "Dedicated teams or individuals are assigned to monitor and manage the AI system at all stages of its lifecycle.",
        "good_answer": "Monitoring and management responsibilities are assigned but may lack clear handoffs between lifecycle stages.",
        "basic_answer": "Monitoring and management occur sporadically or only when issues arise.",
        "non_ideal_answer": "No one is explicitly responsible for lifecycle monitoring and management.",
        "domain_order": 4,
        "order": 6
    },
    {
        "code": "AC-7",
        "text": "Are there audit trails or logs that document the AI system's decision-making process?",
        "explanation": "Audit trails and logs provide a record of how the AI system made specific decisions, which is essential for accountability and troubleshooting. This question assesses whether you maintain comprehensive logs that can be used to explain decisions, identify errors, or respond to regulatory inquiries.\n\nFor example, an AI fraud detection system might log the features and thresholds that flagged a transaction as suspicious. Well-maintained audit trails enhance transparency and make it easier to address disputes or investigate failures.",
        "ideal_answer": "Comprehensive audit trails and logs are maintained, regularly reviewed, and easily accessible for investigations or compliance.",
        "good_answer": "Audit trails and logs are maintained but reviewed inconsistently or not readily accessible.",
        "basic_answer": "Some logs are kept, but they are incomplete or not systematically reviewed.",
        "non_ideal_answer": "No audit trails or logs are maintained.",
        "domain_order": 4,
        "order": 7
    },
    {
        "code": "AC-8",
        "text": "What mechanisms are in place to address disputes or concerns about the system's outcomes?",
        "explanation": "Disputes or concerns about an AI system's outcomes require clear mechanisms for resolution to maintain stakeholder trust. This question examines whether you have processes, such as appeals or review boards, to address such issues.\n\nFor instance, if an AI system used for employee performance reviews produces an unfair evaluation, do you provide a process for employees to contest the results? Implementing mechanisms like manual reviews or appeals processes ensures that users and stakeholders have recourse when issues arise.",
        "ideal_answer": "Established mechanisms, such as appeals processes or review boards, are in place to address disputes and ensure resolution.",
        "good_answer": "Disputes are reviewed and resolved, but processes are informal or inconsistently applied.",
        "basic_answer": "Disputes are handled reactively on a case-by-case basis without structured mechanisms.",
        "non_ideal_answer": "No mechanisms exist to address disputes or concerns.",
        "domain_order": 4,
        "order": 8
    }
]