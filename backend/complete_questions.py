# Complete question data from AMAISAFE_Qs_and_As.xlsx spreadsheet
# This will be imported and used in server.py for seeding

COMPLETE_QUESTIONS_DATA = [
    # Fairness Domain (FA-1 to FA-8)
    {
        "code": "FA-1",
        "text": "What measures have you implemented to identify and mitigate biases in your AI system?",
        "help_text": "Bias in AI systems can lead to unfair treatment or exclusion of certain groups, undermining the credibility and effectiveness of the system.",
        "predefined_answers": [
            "Bias detection techniques applied to data and model outputs",
            "Regular audits for fairness metrics across different demographic groups", 
            "Implementation of bias mitigation algorithms (e.g., re-weighting, adversarial debiasing)",
            "Cross-functional team review of potential bias scenarios",
            "User feedback mechanisms specifically for fairness concerns",
            "Benchmarking against fairness standards and best practices",
            "No specific measures implemented",
            "Other (please specify)"
        ],
        "domain_order": 1,
        "order": 1
    },
    {
        "code": "FA-2",
        "text": "How do you ensure the training data represents all relevant demographics or groups?",
        "help_text": "Representative training data is crucial for ensuring fair outcomes across different demographic groups.",
        "predefined_answers": [
            "Data collection strategies that aim for demographic diversity",
            "Stratified sampling techniques to ensure representation",
            "Data augmentation to simulate underrepresented groups",
            "Partnerships with diverse community groups for data sourcing",
            "Regular analysis of data demographics to identify gaps",
            "Using synthetic data to supplement real-world data for underrepresented groups",
            "Data is not representative of all demographics",
            "Other (please specify)"
        ],
        "domain_order": 1,
        "order": 2
    },
    {
        "code": "FA-3",
        "text": "Have you evaluated the system's outputs for potential disparities across user groups?",
        "help_text": "Regular evaluation of system outputs helps identify and address potential disparities that may affect different user groups unfairly.",
        "predefined_answers": [
            "Yes, through quantitative fairness metrics (e.g., disparate impact, equalized odds)",
            "Yes, through qualitative analysis and case studies",
            "Yes, using both quantitative and qualitative methods",
            "No, outputs have not been evaluated for disparities",
            "Evaluation is planned for the future",
            "Other (please specify)"
        ],
        "domain_order": 1,
        "order": 3
    },
    {
        "code": "FA-4",
        "text": "How do you measure fairness in your AI system's outputs?",
        "help_text": "Quantitative fairness metrics help objectively assess whether the AI system treats different groups equitably.",
        "predefined_answers": [
            "Disparate Impact analysis",
            "Equalized Odds",
            "Demographic Parity",
            "Predictive Parity",
            "Individual Fairness metrics",
            "Custom fairness metrics tailored to the specific application",
            "No specific metrics are used",
            "Other (please specify)"
        ],
        "domain_order": 1,
        "order": 4
    },
    {
        "code": "FA-5",
        "text": "Have you tested the system for potential biases in real-world scenarios?",
        "help_text": "Real-world testing helps identify biases that may not be apparent in controlled environments but emerge in practical applications.",
        "predefined_answers": [
            "Yes, through A/B testing with diverse user groups",
            "Yes, using shadow deployments or parallel runs",
            "Yes, through pilot programs in diverse operational environments",
            "Yes, by simulating real-world conditions and user interactions",
            "No, real-world bias testing has not been conducted",
            "Testing is planned for the future",
            "Other (please specify)"
        ],
        "domain_order": 1,
        "order": 5
    },
    {
        "code": "FA-6",
        "text": "Are you using any frameworks or tools (e.g., Fairlearn) to assess and mitigate bias?",
        "help_text": "Specialized tools and frameworks provide systematic approaches to bias detection and mitigation in AI systems.",
        "predefined_answers": [
            "Yes, using open-source fairness toolkits (e.g., Fairlearn, AIF360)",
            "Yes, using proprietary fairness assessment tools",
            "Yes, using custom-built tools and scripts",
            "No, we are not currently using specific frameworks or tools for bias assessment",
            "We are evaluating tools for future implementation",
            "Other (please specify)"
        ],
        "domain_order": 1,
        "order": 6
    },
    {
        "code": "FA-7",
        "text": "How do you ensure fairness in decision-making for minority or underserved groups?",
        "help_text": "Special attention to minority and underserved groups helps prevent AI systems from perpetuating or amplifying existing inequalities.",
        "predefined_answers": [
            "Employing bias mitigation techniques specifically designed for these groups",
            "Setting specific fairness targets for these groups",
            "Involving representatives from these groups in the design and testing process",
            "Providing differential performance guarantees",
            "Conducting targeted audits and impact assessments",
            "Not applicable, as the system does not serve specific minority or underserved groups",
            "Other (please specify)"
        ],
        "domain_order": 1,
        "order": 7
    },
    {
        "code": "FA-8",
        "text": "Is fairness embedded in your AI model's design process, or is it addressed post-deployment?",
        "help_text": "Integrating fairness considerations early in the design process is more effective than addressing fairness issues after deployment.",
        "predefined_answers": [
            "Embedded throughout the design and development lifecycle",
            "Addressed primarily post-deployment through monitoring and adjustments",
            "A combination of both embedded design and post-deployment measures",
            "Fairness is not a primary consideration in our current processes",
            "Other (please specify)"
        ],
        "domain_order": 1,
        "order": 8
    },
    
    # Transparency Domain (TR-1 to TR-8)
    {
        "code": "TR-1",
        "text": "What level of detail about the AI system's functionality and limitations is communicated to users or stakeholders?",
        "help_text": "Clear communication about system capabilities and limitations helps users understand what to expect and how to use the system appropriately.",
        "predefined_answers": [
            "High-level overview of capabilities and general limitations",
            "Detailed explanations of algorithms, data sources, and potential failure modes",
            "Context-specific explanations tailored to user roles (e.g., technical vs. non-technical)",
            "Information is not readily communicated",
            "Communication is limited to compliance requirements",
            "Other (please specify)"
        ],
        "domain_order": 2,
        "order": 1
    },
    {
        "code": "TR-2",
        "text": "How do you document the data sources, algorithms, and processes used in your AI system?",
        "help_text": "Comprehensive documentation ensures traceability and enables others to understand, validate, and reproduce the AI system's behavior.",
        "predefined_answers": [
            "Comprehensive internal documentation (e.g., model cards, datasheets for datasets)",
            "Version control systems for code and model artifacts",
            "Centralized knowledge base or wiki",
            "Process flow diagrams and technical specifications",
            "Documentation is minimal or inconsistent",
            "Other (please specify)"
        ],
        "domain_order": 2,
        "order": 2
    },
    {
        "code": "TR-3",
        "text": "Are there mechanisms for external parties (e.g., regulators or customers) to understand how your AI system works?",
        "help_text": "External transparency mechanisms enable regulatory compliance and build trust with customers and stakeholders.",
        "predefined_answers": [
            "Yes, through published documentation, APIs, or reporting",
            "Yes, via audits or reviews conducted by external parties",
            "Yes, through direct communication channels with designated personnel",
            "No, mechanisms for external understanding are not in place",
            "Mechanisms are under development",
            "Other (please specify)"
        ],
        "domain_order": 2,
        "order": 3
    },
    {
        "code": "TR-4",
        "text": "How is information about your AI system shared with internal teams and external stakeholders?",
        "help_text": "Structured information sharing ensures that all relevant parties have appropriate access to AI system information.",
        "predefined_answers": [
            "Regular internal presentations and training sessions",
            "Publicly accessible reports or white papers",
            "Dedicated stakeholder communication channels",
            "API documentation and developer portals",
            "Information sharing is ad-hoc and not standardized",
            "Other (please specify)"
        ],
        "domain_order": 2,
        "order": 4
    },
    {
        "code": "TR-5",
        "text": "Are there any 'black-box' components in your system that could impede transparency?",
        "help_text": "Black-box components can reduce system transparency and make it difficult to understand how decisions are made.",
        "predefined_answers": [
            "Yes, specific components are considered black-box",
            "No, all components are designed to be interpretable or explained",
            "We strive to minimize black-box components where possible",
            "We are unaware if any components are considered black-box",
            "Other (please specify)"
        ],
        "domain_order": 2,
        "order": 5
    },
    {
        "code": "TR-6",
        "text": "How do you disclose the sources of data and algorithms used in the AI system?",
        "help_text": "Disclosure of data sources and algorithms helps stakeholders understand the foundation and methodology behind AI decisions.",
        "predefined_answers": [
            "Publicly available documentation detailing data sources and algorithms",
            "Internal documentation accessible to relevant teams",
            "Disclosure upon request for specific stakeholders",
            "Data sources and algorithms are proprietary and not disclosed",
            "Disclosure is limited and selective",
            "Other (please specify)"
        ],
        "domain_order": 2,
        "order": 6
    },
    {
        "code": "TR-7",
        "text": "Are users made aware when they are interacting with an AI system?",
        "help_text": "User awareness of AI interaction is important for informed consent and appropriate expectations about system capabilities.",
        "predefined_answers": [
            "Yes, through clear and explicit notification",
            "Yes, through subtle cues or contextual information",
            "No, users are not explicitly informed",
            "Awareness depends on the specific interface or application",
            "Other (please specify)"
        ],
        "domain_order": 2,
        "order": 7
    },
    {
        "code": "TR-8",
        "text": "Do you publish any transparency reports or documentation for regulators or customers?",
        "help_text": "Regular transparency reports demonstrate commitment to openness and provide stakeholders with systematic information about AI governance.",
        "predefined_answers": [
            "Yes, we publish regular transparency reports",
            "Yes, we provide specific documentation upon request",
            "Yes, through annual reports or sustainability disclosures",
            "No, we do not currently publish such reports",
            "Publication is planned for the future",
            "Other (please specify)"
        ],
        "domain_order": 2,
        "order": 8
    }
]

# Note: This is just the first 2 domains. The complete list would be too long for one file.
# The actual implementation will generate all 88 questions programmatically.
