#!/usr/bin/env python3
"""
Script to create Singapore MAF alignment JSON data from extracted Excel data.
Note: This dataset has 83 questions (missing EX-3, EX-5, EX-7)
"""
import json

# Data extracted from the Excel file
alignment_data = {
    "FA-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses bias identification and mitigation, which is core to the Framework's Data dimension. Data is a core element of model development. It significantly impacts the quality of the model output... there is a need to ensure data quality.",
        "citation": "(p.10)"
    },
    "FA-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Aligns with ensuring representative training data as emphasized in the Data dimension. Facilitating Access to Quality Data... it would be good discipline for AI developers to undertake data quality control measures and adopt general best practices in data governance.",
        "citation": "(p.11)"
    },
    "FA-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Matches evaluation of system outputs for disparities, which aligns with the Testing and Assurance dimension. Testing and Assurance... Third-party testing will also benefit from comprehensive and consistent standards around AI evaluations.",
        "citation": "(p.20)"
    },
    "FA-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Aligns with evaluation methodologies discussed in the Testing dimension. How to Test — Standardisation... setting common benchmarks and methodologies.",
        "citation": "(p.20)"
    },
    "FA-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Real-world testing for bias aligns with Trusted Development and Deployment. Safety best practices need to be implemented by model developers and application deployers across the AI development lifecycle, around development, disclosure and evaluation.",
        "citation": "(p.13)"
    },
    "FA-6": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "While tools are mentioned in the framework, specific tools like Fairlearn aren't referenced. Development — Baseline Safety Practices... model developers and application deployers are best placed to determine what to use.",
        "citation": "(p.13)"
    },
    "FA-7": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly aligns with ensuring fairness for underserved groups, a key aspect of Data dimension. Governments can also consider working with their local communities to curate a repository of representative training datasets for their specific context.",
        "citation": "(p.11)"
    },
    "FA-8": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "The framework implies but doesn't explicitly state fairness should be embedded from design rather than post-deployment. Trusted Development and Deployment... best practices in development, evaluation, and thereafter 'food label'-type transparency and disclosure.",
        "citation": "(p.3)"
    },
    "TR-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly aligns with transparency around functionality and limitations. Disclosure — 'Food Labels'... Transparency around these safety measures undertaken, that form the core of the AI model's make-up is then key.",
        "citation": "(p.13)"
    },
    "TR-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Documentation of data sources and processes is explicitly mentioned. Relevant areas of disclosure may include: a) Data Used: An overview of the types of training data sources and how data was processed before training.",
        "citation": "(p.14)"
    },
    "TR-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "External party understanding aligns with Testing and Assurance dimension. Third-party testing and assurance often play a complementary role in a trusted ecosystem.",
        "citation": "(p.20)"
    },
    "TR-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Information sharing is covered in the framework's transparency discussions. Disclosure — 'Food Labels'...providing relevant information to downstream users.",
        "citation": "(p.13)"
    },
    "TR-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "The framework addresses the need to reduce \"black box\" components through transparency. Today, however, there is a lack of information on the approaches being taken to ensure trustworthy models.",
        "citation": "(p.13)"
    },
    "TR-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Explicitly mentioned in disclosure recommendations. Relevant areas of disclosure may include: a) Data Used: An overview of the types of training data sources and how data was processed before training.",
        "citation": "(p.14)"
    },
    "TR-7": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "While transparency is emphasized, specific disclosure of AI interaction isn't explicitly stated. Content Provenance... Digital watermarking and cryptographic provenance both aim to label and provide additional information, and are used to flag content created with or modified by AI.",
        "citation": "(p.24)"
    },
    "TR-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Publishing transparency reports aligns with the disclosure principles. Relevant areas of disclosure may include... c) Evaluation Results: Overview of evaluations done and key results.",
        "citation": "(p.14)"
    },
    "EX-1": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Explainability is implied but not specifically addressed with levels. Going forward, it is important that the industry coalesces around best practices in development and safety evaluation.",
        "citation": "(p.13)"
    },
    "EX-2": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Testing for non-technical user understanding is implied but not explicitly addressed. By providing relevant information to downstream users, they can make more informed decisions.",
        "citation": "(p.13)"
    },
    "EX-4": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Evaluation of explanations is implied in Testing dimension but not explicitly. Greater emphasis should therefore be placed on setting common benchmarks and methodologies.",
        "citation": "(p.20)"
    },
    "EX-6": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Interpretability is implied but not explicitly addressed. Disclosure — 'Food Labels'... By providing relevant information to downstream users, they can make more informed decisions.",
        "citation": "(p.13-14)"
    },
    "EX-8": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Tailored explanations are implied but not explicitly addressed. The level of detail disclosed can be calibrated based on the need to be transparent vis-à-vis protecting proprietary information.",
        "citation": "(p.14)"
    },
    "AC-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Directly addresses AI system failure accountability. Accountability is a key consideration in fostering a trusted ecosystem. Players along the AI development chain need to be responsible towards end-users.",
        "citation": "(p.7)"
    },
    "AC-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Governance structures align with the Accountability dimension. Responsibility can be allocated based on the level of control that each stakeholder has in the generative AI development chain, so that the able party takes necessary action to protect end-users.",
        "citation": "(p.7)"
    },
    "AC-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Issue escalation policies align with Incident Reporting dimension. After incidents happen, organisations need internal processes to report the incident for timely notification and remediation.",
        "citation": "(p.17)"
    },
    "AC-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Customer complaints handling aligns with accountability principles. Shared responsibility models serve as an important foundation for accountability — they provide clarity on redress when issues occur.",
        "citation": "(p.8)"
    },
    "AC-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Clear roles and responsibilities are emphasized. Accountability is a key consideration... Players along the AI development chain need to be responsible towards end-users.",
        "citation": "(p.7)"
    },
    "AC-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Lifecycle responsibility management directly aligns with Accountability. The AI shared responsibility approach may also need to consider different model types... given the different levels of control that application deployers have for each model type.",
        "citation": "(p.7)"
    },
    "AC-7": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Audit trails align with Incident Reporting dimension. Incident reporting is an established practice... Establishing structures and processes to enable incident reporting is therefore key.",
        "citation": "(p.17)"
    },
    "AC-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Dispute resolution mechanisms directly mentioned. It is therefore useful to consider updating legal frameworks to make them more flexible, and to allow emerging risks to be easily and fairly addressed.",
        "citation": "(p.8)"
    },
    "DI-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Data validation directly addressed in Data dimension. It is also important to ensure the integrity of available datasets.",
        "citation": "(p.10)"
    },
    "DI-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Data lineage tracking aligns with Data dimension. ...it would be good discipline for AI developers to undertake data quality control measures and adopt general best practices in data governance.",
        "citation": "(p.11)"
    },
    "DI-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Governance policies for data align with Data dimension. ...adopt general best practices in data governance, including annotating training datasets consistently and accurately.",
        "citation": "(p.11)"
    },
    "DI-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Ensuring up-to-date data directly aligns with Data dimension. Developing a model well requires good quality data, and in some circumstances, representative data.",
        "citation": "(p.10)"
    },
    "DI-5": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Handling missing data is implied but not explicitly addressed. ...adopt general best practices in data governance, including annotating training datasets consistently and accurately, and using data analysis tools to facilitate data cleaning.",
        "citation": "(p.11)"
    },
    "DI-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Data preprocessing directly mentioned. ...using data analysis tools to facilitate data cleaning (e.g., debiasing and removing inappropriate content).",
        "citation": "(p.11)"
    },
    "DI-7": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Third-party data source evaluation is implied but not explicitly addressed. In such cases, it is important to recognise competing concerns, ensure fair treatment, and to do so in a pragmatic way.",
        "citation": "(p.10)"
    },
    "DI-8": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Data lineage tracing implied but not explicitly addressed. ...it would be good discipline for AI developers to undertake data quality control measures and adopt general best practices in data governance.",
        "citation": "(p.11)"
    },
    "RE-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Testing under different conditions aligns with Testing and Assurance. Testing and Assurance... Third-party testing will also benefit from comprehensive and consistent standards around AI evaluations.",
        "citation": "(p.20)"
    },
    "RE-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Stress testing aligns with Evaluation section. There are generally two main approaches to evaluate generative AI today — (i) benchmarking tests models against datasets of questions and answers to assess performance and safety; and (ii) red teaming.",
        "citation": "(p.14)"
    },
    "RE-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Model drift monitoring aligns with Incident Reporting. This, in turn, supports the continuous improvement of AI systems through insights, remediation and patching.",
        "citation": "(p.17)"
    },
    "RE-4": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Success metrics implied but not explicitly addressed for reliability. Greater emphasis should therefore be placed on setting common benchmarks and methodologies.",
        "citation": "(p.20)"
    },
    "RE-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Failure point identification aligns with Security dimension. What mechanisms are in place to detect malfunctions before they are noticed by end-users.",
        "citation": "(p.17)"
    },
    "RE-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Consistent performance under varying conditions aligns with Testing. Testing under different conditions aligns with Testing and Assurance.",
        "citation": "(p.20)"
    },
    "RE-7": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Error detection mechanisms align with Incident Reporting. AI developers can apply this similar concept, by allowing reporting channels for uncovered safety vulnerabilities in their AI systems.",
        "citation": "(p.17)"
    },
    "RE-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Model retraining frequency aligns with continuous improvement. This, in turn, supports the continuous improvement of AI systems through insights, remediation and patching.",
        "citation": "(p.17)"
    },
    "SE-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Protection from unauthorized access directly aligns with Security. Security-by-design is a fundamental security concept. It seeks to minimise system vulnerabilities and reduce the attack surface through designing security into every phase of the systems development life cycle.",
        "citation": "(p.22)"
    },
    "SE-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Handling adversarial risks directly addressed. What measures are in place to protect the system against adversarial attacks (e.g., input manipulation).",
        "citation": "(p.22)"
    },
    "SE-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Security audits align with Security dimension. Develop New Security Safeguards.",
        "citation": "(p.22)"
    },
    "SE-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Securing AI models throughout lifecycle directly addressed. Security-by-design is a fundamental security concept. It seeks to minimise system vulnerabilities and reduce the attack surface through designing security into every phase of the systems development life cycle (SDLC).",
        "citation": "(p.22)"
    },
    "SE-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Preventing unauthorized modifications directly addressed. Protect against data poisoning attacks.",
        "citation": "(p.10, footnote 14)"
    },
    "SE-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Protection against adversarial attacks explicitly mentioned. New tools have to be developed and may include: a) Input Filters: Input moderation tools detect unsafe prompts (e.g., blocking malicious code).",
        "citation": "(p.22)"
    },
    "SE-7": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Protection of sensitive data aligns with Data and Security dimensions. An emerging group of technologies, known collectively as Privacy Enhancing Technologies (PETs), has the potential to allow data to be used in the development of AI models while protecting data confidentiality and privacy.",
        "citation": "(p.10)"
    },
    "SE-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Regular vulnerability assessments align with Security dimension. AI developers can use these to support risk assessment and threat modelling, and to identify useful tools or processes.",
        "citation": "(p.22)"
    },
    "PR-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Compliance with privacy laws directly addressed. As personal data operates within existing legal regimes, a useful starting point is for policymakers to articulate how existing personal data laws apply to generative AI.",
        "citation": "(p.10)"
    },
    "PR-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Privacy enhancing technologies directly mentioned. An emerging group of technologies, known collectively as Privacy Enhancing Technologies (PETs), has the potential to allow data to be used in the development of AI models while protecting data confidentiality and privacy.",
        "citation": "(p.10)"
    },
    "PR-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "User consent management directly addressed. This will facilitate the use of personal data in a manner that still protects the rights of individuals. For example, policymakers and regulators can clarify consent requirements or applicable exceptions.",
        "citation": "(p.10)"
    },
    "PR-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Data purpose limitation directly addressed. This will facilitate the use of personal data in a manner that still protects the rights of individuals.",
        "citation": "(p.10)"
    },
    "PR-5": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Effectiveness evaluation implied but not explicitly addressed. The understanding of how PETs can be applied to AI will be an important area to advance.",
        "citation": "(p.10)"
    },
    "PR-6": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Privacy violation monitoring implied but not explicitly addressed. The collection and use of personal data is already protected under many existing data regimes.",
        "citation": "(p.10, footnote 15)"
    },
    "PR-7": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Privacy risk evaluation throughout lifecycle is implied but not explicitly addressed. Trusted Use of Personal Data section implies privacy considerations throughout lifecycle.",
        "citation": "(p.10)"
    },
    "PR-8": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Low",
        "alignmentRationale": "Cross-border data protection compliance implied but not explicitly addressed. policymakers and regulators can clarify consent requirements or applicable exceptions, and provide guidance on good business practices for data use in AI.",
        "citation": "(p.10)"
    },
    "SA-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Safety impact assessment aligns with Trusted Development. A crucial step for safety is also to consider the context of the use case and conduct a risk assessment.",
        "citation": "(p.13)"
    },
    "SA-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Preventing unintended harm aligns with Safety and Alignment R&D. Safety techniques, and evaluation tools today do not fully address all potential risks... Given the speed of model advancement, there is a need to ensure that human capacity to align and control generative AI keeps pace with the potential risks.",
        "citation": "(p.27)"
    },
    "SA-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Real-time safety monitoring aligns with Incident Reporting. This should also be complemented by ongoing monitoring efforts to detect malfunctions before they are noticed by end-users.",
        "citation": "(p.17)"
    },
    "SA-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Human safety requirements aligns with Safety and Alignment R&D. One broad area of research entails the development of more aligned models (also known by some as 'forward alignment').",
        "citation": "(p.27)"
    },
    "SA-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Emergency protocols align with Incident Reporting. After incidents happen, organisations need internal processes to report the incident for timely notification and remediation.",
        "citation": "(p.17)"
    },
    "SA-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Risk identification and mitigation directly addressed. For example, further fine-tuning or using user interaction techniques (such as input and output filters) can help to reduce harmful output.",
        "citation": "(p.13)"
    },
    "SA-7": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Fail-safe mechanisms align with Incident Reporting. Implementing an incident management system for timely notification, remediation and continuous improvements, as no AI system is foolproof.",
        "citation": "(p.5)"
    },
    "SA-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Safety testing in high-risk scenarios aligns with Evaluation. There are generally two main approaches to evaluate generative AI today — (i) benchmarking tests models against datasets of questions and answers to assess performance and safety; and (ii) red teaming, where a red team acts as an adversarial user to 'break' the model.",
        "citation": "(p.14)"
    },
    "IN-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Ensuring accessibility aligns with AI for Public Good. Democratising Access to Technology - All members of society should have access to generative AI, done in a trusted manner.",
        "citation": "(p.29)"
    },
    "IN-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Diverse perspectives in design aligns with AI for Public Good. Governments can also consider working with their local communities to curate a repository of representative training datasets for their specific context.",
        "citation": "(p.11)"
    },
    "IN-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Auditing for exclusionary outcomes aligns with Testing and Evaluation. This helps to improve the availability of quality datasets that reflect the cultural and social diversity of a country, which in turn supports the development of safer and more culturally representative models.",
        "citation": "(p.11)"
    },
    "IN-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Accessibility requirements align with AI for Public Good. designing applications to elicit the intended social and human outcomes is key.",
        "citation": "(p.29)"
    },
    "IN-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Diverse stakeholder involvement aligns with AI for Public Good. The aim is to establish a global Digital Commons — a place with common rules-of-the-road and equal opportunities for all citizens to flourish, regardless of their geographical location.",
        "citation": "(p.29)"
    },
    "IN-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Serving underrepresented communities aligns with AI for Public Good. Governments can partner companies and communities on digital literacy initiatives to encourage safe and responsible AI use.",
        "citation": "(p.29)"
    },
    "IN-7": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Cultural differences consideration aligns with Data dimension. This helps to improve the availability of quality datasets that reflect the cultural and social diversity of a country.",
        "citation": "(p.11)"
    },
    "IN-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Evaluation for unintentional exclusion aligns with Testing. This helps to improve the availability of quality datasets that reflect the cultural and social diversity of a country, which in turn supports the development of safer and more culturally representative models.",
        "citation": "(p.11)"
    },
    "SU-1": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Environmental impact directly addressed. The resource requirements of generative AI (e.g., energy and water) are non-trivial and will likely impact sustainability goals.",
        "citation": "(p.30)"
    },
    "SU-2": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Algorithm optimization for efficiency directly addressed. Stakeholders in the generative AI ecosystem therefore need to work together to develop suitable technology (e.g., energy efficient compute) in support of our climate responsibilities.",
        "citation": "(p.30)"
    },
    "SU-3": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Renewable energy sources directly addressed. AI workloads can be hosted in data centres that drive best-in-class energy-efficient practices, with green energy sources or pathways.",
        "citation": "(p.30)"
    },
    "SU-4": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Carbon footprint estimation directly mentioned. To inform such plans, the carbon footprint of generative AI (e.g., for model training and inference) will also need to be tracked and measured.",
        "citation": "(p.30)"
    },
    "SU-5": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Algorithm optimization directly addressed. AI developers and equipment manufacturers are better placed to conduct R&D on green computing techniques and adopt energy-efficient hardware.",
        "citation": "(p.30)"
    },
    "SU-6": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Energy-efficient platforms directly mentioned. AI workloads can be hosted in data centres that drive best-in-class energy-efficient practices, with green energy sources or pathways.",
        "citation": "(p.30)"
    },
    "SU-7": {
        "alignmentType": "Partially Aligns",
        "confidenceLevel": "Medium",
        "alignmentRationale": "Balancing sustainability with performance implied but not explicitly addressed. The resource requirements of generative AI (e.g., energy and water) are non-trivial and will likely impact sustainability goals.",
        "citation": "(p.30)"
    },
    "SU-8": {
        "alignmentType": "Fully Aligns",
        "confidenceLevel": "High",
        "alignmentRationale": "Tracking environmental impact directly mentioned. To inform such plans, the carbon footprint of generative AI (e.g., for model training and inference) will also need to be tracked and measured.",
        "citation": "(p.30)"
    }
}

# Write to JSON file
with open('/app/frontend/src/data/singaporeMafAlignmentData.json', 'w', encoding='utf-8') as f:
    json.dump(alignment_data, f, indent=2, ensure_ascii=False)

print(f"✅ Successfully created singaporeMafAlignmentData.json")
print(f"📊 Processed {len(alignment_data)} question alignments")

# Print summary
fully_aligns = sum(1 for v in alignment_data.values() if v['alignmentType'] == 'Fully Aligns')
partially_aligns = sum(1 for v in alignment_data.values() if v['alignmentType'] == 'Partially Aligns')

print(f"\n📋 Alignment summary:")
print(f"  • Fully Aligns: {fully_aligns} questions")
print(f"  • Partially Aligns: {partially_aligns} questions")
print(f"\n⚠️  Note: This dataset has {len(alignment_data)} out of 88 questions (missing EX-3, EX-5, EX-7)")
