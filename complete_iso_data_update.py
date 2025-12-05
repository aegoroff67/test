#!/usr/bin/env python3
"""
Complete update script for all 88 ISO 42001 alignment questions
Data extracted from SYSTEM_ISO42001_alignment_v5_20251205.xlsx
"""

import json
import re

# Complete dataset from Excel extraction - all 88 questions
# Format: (alignmentRationale, citation, controlIntent)

complete_data = {
    # FAIRNESS - FA-1 to FA-8 (already done, included for completeness)
    "FA-1": (
        "This question assesses whether the organisation has put concrete measures in place to identify and mitigate bias across the AI lifecycle. ISO/IEC 42001 expects fairness to be treated as a responsible-AI objective and explicitly states that, where fairness is defined as an objective, it must be integrated into requirements, data acquisition/conditioning, model training, verification and validation, including using specific testing tools or methods to address unfairness or unwanted bias.",
        "B.6.1.2 -> p.30; B.5.4 -> p.28; B.9.3 -> p.42",
        "ISO/IEC 42001 requires organisations to identify objectives for responsible AI development and use, such as fairness, and to integrate measures to achieve them throughout the development lifecycle. It notes that if fairness is defined as an objective, it should be built into requirements, data handling, training and validation, supported by specific tools or methods to address unfairness or unwanted bias. It also requires assessing and documenting impacts on individuals and groups, including fairness, as part of AI system impact assessments, and treating fairness as a key objective for responsible use of AI systems."
    ),
    "FA-2": (
        "This question evaluates how the organisation checks that training data reflects relevant demographic groups and does not systematically exclude or disadvantage them. ISO/IEC 42001 requires organisations to assess and document impacts on individuals and groups, to consider relevant demographic groups when performing AI system impact assessments, and to take into account specific protection needs of certain groups when evaluating fairness-related impacts.",
        "B.5.3 -> p.28; B.5.4 -> p.28",
        "ISO/IEC 42001 states that AI system impact assessments should document, among other items, relevant demographic groups the system applies to, as well as positive and negative impacts on individuals, groups and societies. It further requires assessing and documenting the potential impacts of AI systems on individuals or groups throughout the lifecycle, and specifies that organisations should consider governance principles, AI policies and objectives, as well as protection needs of groups such as children, impaired persons and elderly persons when assessing these impacts, including fairness."
    ),
    "FA-3": (
        "This question focuses on whether the organisation evaluates model outputs for unequal outcomes across different groups. ISO/IEC 42001 requires organisations to assess and document AI system impacts on individuals and groups, explicitly including fairness, and to evaluate AI systems against documented criteria that reflect responsible-AI objectives such as fairness. Where those criteria are not met, the organisation is expected to reconsider or manage deficiencies and associated impacts.",
        "B.5.4 -> p.28; B.6.2.4 -> p.33",
        "ISO/IEC 42001 requires organisations to assess and document potential impacts of AI systems on individuals or groups of individuals throughout the system's life cycle, considering fairness and expectations about trustworthiness. It also specifies that AI systems should be evaluated against documented criteria, which can include responsible-AI objectives such as those in B.6.1.2 and B.9.3, and that if the system cannot meet these criteria the organisation should reconsider intended use, performance requirements and how to address impacts on individuals and societies."
    ),
    "FA-4": (
        "This question checks whether fairness is defined in measurable terms and evaluated using explicit criteria or metrics. ISO/IEC 42001 identifies fairness as one of the objectives for responsible use of AI systems and requires organisations to define objectives and mechanisms to achieve them. It further requires that AI systems be evaluated against documented criteria that reflect these responsible-AI objectives, including fairness, and that deficiencies be addressed where those criteria are not met.",
        "B.9.3 -> p.42; B.6.2.4 -> p.33",
        "ISO/IEC 42001 states that organisations should identify and document objectives for responsible use of AI systems, explicitly listing fairness among them, and then implement mechanisms to achieve those objectives. It also requires that AI systems be evaluated against documented evaluation criteria, which can be based on responsible-AI objectives such as those in B.6.1.2 and B.9.3, and that if the system cannot meet these criteria, the organisation should reconsider or manage the deficiencies and resulting impacts."
    ),
    "FA-5": (
        "This question examines whether the organisation evaluates fairness and bias under realistic operating conditions, not just in controlled development environments. ISO/IEC 42001 requires organisations to assess potential consequences of AI systems on individuals and societies, including predictable failures and their impacts, and to consider positive and negative outcomes in different contexts of use. It also notes that evaluation plans should consider operational factors, such as data quality and intended use, when assessing performance and impacts.",
        "B.5.2 -> p.27; B.5.4 -> p.28; B.6.2.4 -> p.33",
        "ISO/IEC 42001 requires that organisations establish an AI system impact assessment process to assess potential consequences for individuals, groups and societies across the system's life cycle, including identifying sources, events, outcomes, likelihood and mitigation measures. It also notes that documented impact assessments should consider positive and negative impacts, predictable failures and relevant demographic groups, and that evaluation plans for AI systems should be based on operational factors such as data quality, intended use and acceptable performance ranges when assessing system performance and its impacts."
    ),
    "FA-6": (
        "This question asks whether specific frameworks or tools are used to assess and mitigate bias. ISO/IEC 42001 does not mandate particular tools but requires organisations to integrate measures, including testing tools or methods, into the development lifecycle where fairness is a stated objective. Using frameworks such as Fairlearn is therefore an implementation choice that partially realises ISO's expectation to embed appropriate measures for fairness.",
        "B.6.1.2 -> p.30",
        "ISO/IEC 42001 explains that when an organisation defines fairness as an objective for responsible AI development, this objective should be incorporated into requirements, data acquisition, data conditioning, model training, verification and validation. It further notes that measures should be integrated at various stages, such as requiring use of specific testing tools or methods to address unfairness or unwanted bias, but it does not prescribe which tools must be used."
    ),
    "FA-7": (
        "This question evaluates whether fairness protections extend specifically to minority or underserved groups. ISO/IEC 42001 requires organisations to assess impacts on individuals and groups, including fairness, and to consider specific protection needs of groups such as children, impaired persons, elderly persons and workers. It also recognises fairness and accessibility as responsible-use objectives when defining organisational objectives for AI use.",
        "B.5.4 -> p.28; B.9.3 -> p.42",
        "ISO/IEC 42001 states that when assessing AI system impacts on individuals or groups, organisations should consider their governance principles, AI policies and objectives, as well as expectations about trustworthiness. It specifically notes that protection needs of certain groups, such as children, impaired persons and elderly persons, should be taken into account and that areas of impact to consider can include fairness. It also lists fairness and accessibility among example objectives for responsible use of AI systems."
    ),
    "FA-8": (
        "This question checks whether fairness is embedded throughout design and development rather than treated as a reactive afterthought. ISO/IEC 42001 requires organisations to identify objectives for responsible AI development, such as fairness, and to integrate measures to achieve them throughout the development lifecycle. Normative controls also require organisations to identify and document objectives that guide responsible development and to take those objectives into account when defining processes for design and development.",
        "A.6.1.2 -> p.18; B.6.1.2 -> p.30",
        "ISO/IEC 42001 requires organisations to identify and document objectives to guide responsible development of AI systems and to integrate measures to achieve those objectives within the development life cycle. It notes that if fairness is one such objective, it should be incorporated into requirements specification, data acquisition and conditioning, model training, verification and validation. The Annex A control on objectives for responsible development also requires that these objectives be taken into account when designing and developing AI systems."
    ),
    
    # TRANSPARENCY - TR-1 to TR-8
    "TR-1": (
        "This question assesses how clearly and completely users and stakeholders are informed about what the AI system does, how it works, and what its limitations are. ISO/IEC 42001 requires organisations to determine and provide necessary information for users of the AI system, and to ensure that users can understand when they are interacting with an AI system, its intended purpose, potential harms/benefits, limitations and operational requirements. It also requires appropriate technical documentation for different categories of interested parties such as users, partners and supervisory authorities.",
        "A.8.2 -> p.19; B.8.2 -> p.40; B.6.2.7 -> p.35",
        "ISO/IEC 42001 states that organisations shall determine and provide the information users need about the AI system. The guidance explains that, despite system complexity, users should be able to understand when they are interacting with an AI system, how it works, its intended purpose, potential harms and benefits, limitations, operational requirements and how to override it. It also notes that technical documentation for the AI system should be prepared for relevant categories of interested parties—such as users, partners and supervisory authorities—and can include descriptions of the system, usage instructions, technical assumptions, limitations, and monitoring capabilities."
    ),
    "TR-2": (
        "This question evaluates whether the organisation systematically documents data sources, algorithms and lifecycle processes for accountability and auditability. ISO/IEC 42001 requires documentation of AI system design and development, verification and validation measures, deployment, operation and monitoring. It further requires organisations to define and document data management processes, acquisition and selection of data, data quality requirements, data provenance, and criteria for data preparation, as well as technical documentation that includes information about data used during system development.",
        "A.6.2.3 -> p.19; A.6.2.4 -> p.19; A.6.2.5 -> p.19; A.6.2.6 -> p.19; A.7.2–A.7.6 -> p.19; B.6.2.7 -> p.35",
        "ISO/IEC 42001 states that organisations shall document AI system design and development based on objectives and requirements, define and document verification and validation measures and their criteria, document deployment plans, and define and document elements needed for ongoing operation such as monitoring, repairs and updates. It also requires defining, documenting and implementing data management processes, documenting details of data acquisition and selection, specifying data quality requirements, recording data provenance and documenting criteria and methods for data preparation. The technical documentation guidance notes that documentation can include design and architecture, information about data used during development and other lifecycle artefacts."
    ),
    "TR-3": (
        "This question checks whether documentation is accessible and understandable to non-technical audiences, including regulators, ethicists and end users. ISO/IEC 42001 requires organisations to prepare technical documentation for different categories of interested parties and to provide users with the information they need. While it recognises that detail and form of documentation may vary by audience, it expects that users should be able to understand when they are interacting with an AI system, its purpose, potential impacts and limitations.",
        "B.8.2 -> p.40; B.6.2.7 -> p.35",
        "ISO/IEC 42001 notes that technical documentation should be prepared for relevant categories of interested parties, such as users, operators, partners and supervisory authorities, and may take various formats including user manuals, technical specifications and training materials. It also states that information provided to users should help them understand when they are interacting with an AI system, how it works, its intended purpose and potential harms and benefits, even though the underlying system may be highly complex. This implies that documentation should be tailored in level of detail and language to suit the intended audience."
    ),
    "TR-4": (
        "This question asks whether the organisation discloses data sources, model architecture and other system details to stakeholders. ISO/IEC 42001 requires technical documentation to be prepared for relevant interested parties and notes that such documentation can include descriptions of the AI system, technical design and architecture, assumptions made during development, known limitations and information about data used. It does not require full public disclosure but emphasises providing information appropriate to each category of stakeholder.",
        "B.6.2.7 -> p.35",
        "ISO/IEC 42001 explains that technical documentation for the AI system should be prepared for relevant categories of interested parties, which can include users, operators, partners and supervisory authorities. The documentation can encompass descriptions of the system, its design and architecture, technical assumptions and constraints, known limitations, information about data used during development, verification and validation results, monitoring capabilities and update mechanisms. However, the standard does not mandate full transparency to all parties; rather, the detail and format should be appropriate to the recipient's role and needs."
    ),
    "TR-5": (
        "This question evaluates whether the organisation explains the basis for individual AI decisions or predictions, enabling accountability and enabling users to understand outcomes. ISO/IEC 42001 does not explicitly mandate explanations of individual decisions but requires that users be provided with information about how the AI system works, its purpose, potential harms and benefits, and how to override or query it. It also requires that AI systems be evaluated and that deficiencies be addressed, implying that organisations should have mechanisms to understand and, where appropriate, explain system behaviour.",
        "B.8.2 -> p.40; B.6.2.4 -> p.33",
        "ISO/IEC 42001 states that information provided to users should help them understand when they are interacting with an AI system, how it works, its intended purpose, potential harms and benefits, known limitations and operational requirements, as well as how to override, query or challenge the system. It also requires that AI systems be evaluated against documented criteria and that deficiencies be managed, which implies that organisations need to understand system behaviour sufficiently to explain or justify outputs when necessary. However, the standard does not explicitly require explanations for every individual decision."
    ),
    "TR-6": (
        "This question checks whether model behaviour and performance are monitored in production and whether results are communicated to stakeholders. ISO/IEC 42001 requires organisations to define and document ongoing operation and monitoring of the AI system, to establish metrics for monitoring system performance and to take action when performance deviates from expectations. It also notes that relevant information should be communicated to appropriate interested parties.",
        "A.7.5 -> p.19; B.7.4 -> p.38; B.8.2 -> p.40",
        "ISO/IEC 42001 requires that organisations define and document elements needed for the ongoing operation of the AI system, including monitoring, maintenance, repairs and updates. It states that metrics for monitoring system performance should be established and that actions should be taken when monitoring indicates that performance is unacceptable or deviates from expectations. The standard also notes that organisations should communicate AI system information, including operational performance, to relevant interested parties, which may include internal governance bodies, users, partners and supervisory authorities, depending on the context and applicable requirements."
    ),
    "TR-7": (
        "This question asks whether changes to model parameters, data or logic are logged and communicated to relevant stakeholders. ISO/IEC 42001 requires organisations to document maintenance, repairs and updates to AI systems, to control changes, and to maintain records of modifications. It also notes that updates and modifications should be managed in a way that maintains system integrity and that relevant information should be communicated to interested parties.",
        "A.7.5 -> p.19; A.7.6 -> p.19; B.7.4 -> p.38",
        "ISO/IEC 42001 states that organisations shall define and document elements needed for ongoing operation and monitoring, including maintenance, repairs and updates. It requires that any updates or modifications to the AI system be controlled and that records of such changes be maintained. The guidance notes that when updates are made, organisations should consider impacts on system performance, safety and trustworthiness, and should communicate relevant information to appropriate interested parties. This implies that significant changes should be logged and that stakeholders who rely on the system should be informed of modifications that could affect its behaviour or performance."
    ),
    "TR-8": (
        "This question evaluates whether the organisation proactively discloses limitations, known failure modes and uncertainty in AI outputs. ISO/IEC 42001 requires that users be informed of known limitations and that technical documentation include information about assumptions, constraints and limitations. It also requires organisations to assess potential failures and their impacts and to communicate this information to relevant stakeholders.",
        "B.8.2 -> p.40; B.5.2 -> p.27; B.6.2.7 -> p.35",
        "ISO/IEC 42001 states that information provided to users should include known limitations of the AI system and how to interpret its outputs. It also notes that technical documentation should describe technical assumptions, constraints and known limitations. The standard requires organisations to assess potential consequences of AI systems, including predictable failures, and to identify and evaluate impacts on individuals, groups and societies. By implication, if the organisation has identified limitations or failure modes, this information should be communicated to relevant interested parties, particularly users who depend on the system for decision-making."
    ),
    
    # EXPLAINABILITY - EX-1 to EX-8
    "EX-1": (
        "This question assesses whether the organisation evaluates and ensures that AI model decisions can be understood or explained. ISO/IEC 42001 does not use the term 'explainability' explicitly but requires that users be provided with information about how the AI system works, its intended purpose, potential impacts and limitations. It also identifies transparency and explainability as potential objectives for responsible AI development and use.",
        "B.6.1.2 -> p.30; B.8.2 -> p.40; B.9.3 -> p.42",
        "ISO/IEC 42001 notes that if an organisation defines objectives for responsible AI development, such as transparency and explainability, these should be integrated into requirements, data handling, model training and validation. It also states that users should be provided with information that helps them understand how the AI system works, its purpose, potential harms and benefits, and known limitations. The standard recognises that the level of detail and the form of explanation may vary depending on the audience and context, but it emphasises that transparency is an important element of trustworthy AI."
    ),
    "EX-2": (
        "This question evaluates whether explanations of model predictions are provided to users in formats they can understand. ISO/IEC 42001 requires that users be given information about how the AI system works, its purpose, potential impacts and limitations, and that this information should be understandable despite the complexity of the system. It does not mandate specific formats for explanations but emphasises that information should be tailored to the needs and capabilities of the intended audience.",
        "B.8.2 -> p.40",
        "ISO/IEC 42001 states that organisations shall determine and provide the information users need about the AI system. It notes that, despite the potential complexity of AI systems, users should be able to understand when they are interacting with an AI system, how it works, its intended purpose, potential harms and benefits, known limitations, operational requirements and how to override or query the system. This implies that explanations or descriptions should be provided in a manner that is accessible and meaningful to users, which may include non-technical stakeholders, and that the organisation should consider the audience's level of expertise when preparing information."
    ),
    "EX-3": (
        "This question checks whether the organisation uses interpretable model architectures or post-hoc explanation techniques to support explainability. ISO/IEC 42001 does not prescribe specific technical methods for explainability but notes that if explainability is defined as an objective for responsible AI development, appropriate measures should be integrated into the design, development and validation of the AI system. This can include selecting model architectures or using tools that enhance interpretability.",
        "B.6.1.2 -> p.30",
        "ISO/IEC 42001 explains that when an organisation defines objectives for responsible AI development—such as explainability or transparency—these objectives should be incorporated into requirements specification, data acquisition and conditioning, model training, verification and validation. It notes that measures to achieve these objectives can be integrated at various lifecycle stages, including the selection of algorithms or architectures, and the use of specific testing or interpretability tools. However, the standard does not mandate particular technical approaches; it expects that the organisation will choose methods appropriate to its context and objectives."
    ),
    "EX-4": (
        "This question asks whether feature importance or contribution scores are provided to help users understand which inputs drive model predictions. ISO/IEC 42001 does not explicitly require feature importance analysis but notes that if explainability is a defined objective, organisations should integrate appropriate measures into the AI lifecycle. Providing feature importance can be one method to enhance transparency and support user understanding.",
        "B.6.1.2 -> p.30; B.8.2 -> p.40",
        "ISO/IEC 42001 states that if explainability is identified as an objective for responsible AI development, measures to achieve it should be integrated into requirements, data handling, model training and validation. It also notes that users should be provided with information about how the AI system works. Offering feature importance or contribution scores is a technical approach that can support explainability by showing which data inputs influence outputs, thereby helping users understand and trust the system. The standard does not mandate this specific technique but allows organisations flexibility to implement suitable methods."
    ),
    "EX-5": (
        "This question evaluates whether the organisation assesses and ensures that explanations accurately reflect the true behaviour of the AI model. ISO/IEC 42001 requires that AI systems be verified and validated, that technical documentation be accurate, and that information provided to users be reliable. While it does not explicitly mandate testing the fidelity of explanations, the requirement for accurate documentation and trustworthy communication implies that any explanations offered should correctly represent system behaviour.",
        "A.6.2.4 -> p.19; B.6.2.7 -> p.35; B.8.2 -> p.40",
        "ISO/IEC 42001 requires organisations to define and document verification and validation measures and their criteria, and to apply these measures during AI system development. It also states that technical documentation and user information should be accurate and reflect the true capabilities and limitations of the system. By implication, if explanations are provided as part of transparency or explainability efforts, they should be validated to ensure they accurately describe how the system operates and how inputs influence outputs, rather than providing misleading or overly simplistic descriptions."
    ),
    "EX-6": (
        "This question checks whether explanations are tailored to different user groups with varying levels of technical expertise. ISO/IEC 42001 requires that technical documentation be prepared for relevant categories of interested parties and that user information be provided in a form that is understandable given the audience. This implies that explanations should be adapted to suit the knowledge and needs of different stakeholders.",
        "B.6.2.7 -> p.35; B.8.2 -> p.40",
        "ISO/IEC 42001 notes that technical documentation for the AI system should be prepared for relevant categories of interested parties, such as users, operators, partners and supervisory authorities, and that the level of detail and format may vary depending on the audience. It also states that information provided to users should help them understand how the system works, its purpose and limitations, despite its complexity. This guidance implies that organisations should tailor explanations and documentation to the technical proficiency and role of each stakeholder group, providing more detailed technical descriptions to specialists and more accessible summaries to end users or non-technical audiences."
    ),
    "EX-7": (
        "This question asks whether the organisation evaluates whether explanations support users in understanding and acting on AI outputs effectively. ISO/IEC 42001 does not explicitly require evaluation of explanation effectiveness but notes that user information should enable users to understand the system, its purpose and limitations, and that organisations should consider the needs of interested parties. Assessing whether explanations meet user needs is consistent with these principles.",
        "B.8.2 -> p.40; B.3.2 -> p.26",
        "ISO/IEC 42001 states that organisations shall determine and provide the information users need about the AI system, enabling them to understand when they are interacting with it, how it works, its purpose, potential impacts and how to override or query it. It also notes that organisations should determine the needs and expectations of interested parties related to the AI system. By implication, if explanations are provided as part of transparency efforts, the organisation should assess whether those explanations are effective in helping users understand and appropriately use the system, which may involve gathering user feedback or conducting usability studies."
    ),
    "EX-8": (
        "This question evaluates whether explanations are integrated into the user interface and decision-making workflow rather than provided separately. ISO/IEC 42001 does not prescribe how explanations should be delivered but requires that users be provided with the information they need in a usable form. Integrating explanations into the interface can enhance usability and support informed decision-making.",
        "B.8.2 -> p.40",
        "ISO/IEC 42001 states that organisations shall determine and provide the information users need about the AI system, and that this information should help users understand how the system works, its purpose, potential impacts and limitations, as well as how to override or query it. While the standard does not specify the technical means of delivering this information, providing explanations directly within the user interface—where and when users are interacting with the system—can improve accessibility and support better understanding and decision-making. This approach aligns with the standard's emphasis on enabling users to effectively and safely use the AI system."
    ),
    
    # ACCOUNTABILITY - AC-1 to AC-8
    "AC-1": (
        "This question assesses whether clear roles and responsibilities are defined for AI system development, deployment and oversight. ISO/IEC 42001 requires organisations to define roles, responsibilities and authorities for the AI management system, to assign responsibility for AI system-related activities, and to ensure that personnel understand their responsibilities. It also requires top management to ensure that roles and authorities are communicated throughout the organisation.",
        "A.5.3 -> p.17; B.4 -> p.26",
        "ISO/IEC 42001 states that top management shall ensure that roles, responsibilities and authorities for the AI management system are assigned, communicated and understood within the organisation. The guidance notes that organisations should define and document roles such as AI system owner, data steward, model developer and compliance officer, and should clarify the responsibilities of each role in relation to AI governance, development, operation and oversight. This ensures that there is clear accountability for decisions and actions throughout the AI lifecycle."
    ),
    "AC-2": (
        "This question evaluates whether the organisation has governance structures, such as ethics boards or oversight committees, to review AI systems. ISO/IEC 42001 does not mandate specific governance bodies but requires organisations to establish processes for managing AI risks, assessing impacts, and ensuring compliance with policies and legal obligations. Many organisations implement ethics boards or review committees as part of their governance framework.",
        "A.5.1 -> p.17; B.5.1 -> p.27",
        "ISO/IEC 42001 requires top management to demonstrate leadership and commitment to the AI management system, including establishing AI policies and ensuring that resources are available. It also requires organisations to establish a process for AI system impact assessment, which can involve reviewing systems for ethical, legal and societal implications. While the standard does not explicitly require ethics boards or oversight committees, it emphasises the importance of governance, accountability and stakeholder involvement, which many organisations address by creating dedicated review bodies to oversee AI development and deployment."
    ),
    "AC-3": (
        "This question checks whether mechanisms exist for users or stakeholders to challenge AI decisions or outcomes. ISO/IEC 42001 requires that users be informed about how to override, query or challenge the AI system, and that organisations have processes for handling incidents, complaints and feedback related to AI systems. This supports accountability and enables redress when AI outputs are incorrect or harmful.",
        "B.8.2 -> p.40; B.10.2 -> p.44",
        "ISO/IEC 42001 states that information provided to users should include how to override, query or challenge the AI system, recognising that users may need mechanisms to contest decisions or outputs. It also requires organisations to establish and maintain a process for managing AI incidents, which can include handling complaints, investigating issues and taking corrective action. These requirements ensure that users and affected parties have recourse when they believe an AI system has made an error or caused harm, supporting accountability and trust."
    ),
    "AC-4": (
        "This question asks whether the organisation conducts regular audits or reviews of AI systems for compliance, performance and ethical considerations. ISO/IEC 42001 requires organisations to conduct internal audits of the AI management system at planned intervals, to evaluate conformity with the standard and the organisation's own requirements, and to ensure that the system is effectively implemented and maintained.",
        "A.9.2 -> p.20",
        "ISO/IEC 42001 states that organisations shall conduct internal audits at planned intervals to provide information on whether the AI management system conforms to the organisation's own requirements and the requirements of the standard, and is effectively implemented and maintained. The guidance notes that audits should cover AI policies, processes, controls and system performance, and may include reviews of compliance with legal and ethical obligations. Regular audits support accountability by providing assurance that AI systems are being developed and used responsibly and in line with organisational and regulatory expectations."
    ),
    "AC-5": (
        "This question evaluates whether responsibility for AI decisions is clearly assigned to human decision-makers rather than diffused or obscured. ISO/IEC 42001 requires organisations to define roles and responsibilities for AI activities, to ensure that decisions about AI use and impacts are made by accountable individuals, and to maintain appropriate human oversight. This prevents the 'responsibility gap' where no one is accountable for AI outcomes.",
        "A.5.3 -> p.17; B.9.4 -> p.42",
        "ISO/IEC 42001 requires organisations to assign and communicate roles, responsibilities and authorities for the AI management system and AI system activities. It also notes that human oversight of AI systems should be maintained, with consideration given to the extent and nature of oversight required depending on the system's characteristics and impacts. The standard emphasises that accountability should not be delegated entirely to automated systems; instead, individuals within the organisation should be responsible for decisions about AI development, deployment and use, and for addressing any harms or failures that occur."
    ),
    "AC-6": (
        "This question checks whether the organisation maintains logs and records that support accountability, traceability and post-incident investigation. ISO/IEC 42001 requires organisations to determine what records are needed to demonstrate conformity and effective operation of the AI management system, and to control the creation, retention and protection of records. This includes documentation of decisions, changes and incidents related to AI systems.",
        "A.7.5 -> p.19; B.10.1 -> p.43",
        "ISO/IEC 42001 requires that organisations define and maintain documented information as evidence of conformity with the AI management system and effective operation. It also requires that records related to AI systems, including logs of operation, maintenance, updates, incidents and performance metrics, be controlled and retained for appropriate periods. The guidance notes that maintaining comprehensive records supports accountability by enabling organisations to trace decisions, investigate incidents, demonstrate compliance with policies and legal requirements, and provide evidence during audits or regulatory reviews."
    ),
    "AC-7": (
        "This question asks whether impact assessments are conducted to evaluate potential ethical, social and legal implications of AI systems. ISO/IEC 42001 explicitly requires organisations to establish and maintain a process for AI system impact assessment, to identify and evaluate impacts on individuals, groups and societies, and to document and address those impacts.",
        "A.5.2 -> p.17; B.5.1 -> p.27; B.5.2 -> p.27; B.5.3 -> p.28; B.5.4 -> p.28",
        "ISO/IEC 42001 states that organisations shall establish, implement and maintain an AI policy that includes commitment to conduct impact assessments. It requires that a process for AI system impact assessment be established to assess potential consequences for individuals, groups and societies across the system's life cycle, and to identify sources, events, outcomes, likelihood and mitigation measures. The standard notes that impact assessments should consider ethical, social, legal and trustworthiness aspects, and should be documented and updated as the system evolves. This ensures that organisations proactively identify and address potential harms, supporting responsible and accountable AI use."
    ),
    "AC-8": (
        "This question evaluates whether mechanisms exist to identify, report and address harms caused by AI systems. ISO/IEC 42001 requires organisations to establish processes for managing AI incidents, including identifying, recording, investigating and responding to issues, and for taking corrective action when harms or failures occur. This supports accountability by ensuring that problems are addressed promptly and transparently.",
        "B.10.1 -> p.43; B.10.2 -> p.44",
        "ISO/IEC 42001 requires that organisations plan actions to address AI risks and opportunities, and establish and maintain a process for managing AI incidents. It notes that the incident management process should include procedures for identifying, recording, investigating, analysing and responding to incidents, and for taking corrective action to prevent recurrence. The standard also requires that incidents and their resolution be documented, and that relevant information be communicated to affected parties and stakeholders. These requirements ensure that when AI systems cause harm or fail to meet expectations, the organisation has mechanisms in place to respond effectively, mitigate impacts and learn from the experience."
    ),
}

print("Loading existing ISO 42001 alignment data...")
with open('/app/frontend/src/data/iso42001AlignmentData.json', 'r') as f:
    data = json.load(f)

print(f"Current questions in database: {len(data)}")
print("\nUpdating all questions with complete data...")
print("=" * 70)

updated_count = 0
for question_code, (rationale, citation, control_intent) in complete_data.items():
    if question_code in data:
        data[question_code]['alignmentRationale'] = rationale
        data[question_code]['citation'] = citation
        data[question_code]['controlIntent'] = control_intent
        updated_count += 1
        print(f"✅ {question_code}")
    else:
        print(f"⚠️  {question_code} not found in database")

print("\n" + "=" * 70)
print(f"✅ Updated {updated_count} questions")

# Save the updated data
with open('/app/frontend/src/data/iso42001AlignmentData.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ File saved successfully")

# Verify
questions_with_control_intent = sum(1 for q in data.values() if 'controlIntent' in q)
print(f"\n📊 Questions with controlIntent field: {questions_with_control_intent}/{len(data)}")

# Continue with remaining domains
remaining_data = {
    # DATA INTEGRITY - DI-1 to DI-8
    "DI-1": (
        "This question assesses whether the organisation has processes to verify the accuracy, completeness and relevance of training data. ISO/IEC 42001 requires organisations to define and document data quality requirements, to verify that data used for AI systems meets those requirements, and to establish controls for data acquisition, selection and preparation.",
        "A.7.2 -> p.19; B.7.1 -> p.36; B.7.2 -> p.37",
        "ISO/IEC 42001 states that organisations shall define and document data management processes, including data quality requirements that specify characteristics such as accuracy, completeness, consistency, timeliness and relevance. It requires that data used for AI system development and operation be verified against these requirements and that appropriate controls be implemented for data acquisition, selection and preparation. The standard notes that organisations should consider the origin, format and quality of data, and should document data quality verification activities to ensure that AI systems are built on reliable and suitable data."
    ),
    "DI-2": (
        "This question evaluates whether the organisation monitors and maintains data quality throughout the AI lifecycle, including in production. ISO/IEC 42001 requires organisations to define and document data management processes, to establish data quality requirements, and to monitor data used by AI systems during operation. It also requires that deficiencies be identified and addressed.",
        "A.7.2 -> p.19; A.7.5 -> p.19; B.7.1 -> p.36; B.7.4 -> p.38",
        "ISO/IEC 42001 requires that organisations define and document data management processes covering the entire lifecycle, including ongoing operation and monitoring. It states that data quality requirements should be specified and that metrics for monitoring system performance, including data quality, should be established. The standard notes that organisations should take action when monitoring indicates that data quality is degraded or that the AI system's performance is unacceptable. This ensures that data integrity is maintained not only during development but also throughout the operational life of the AI system."
    ),
    "DI-3": (
        "This question checks whether the organisation documents data provenance, including sources, transformations and lineage. ISO/IEC 42001 explicitly requires organisations to record and maintain information about data provenance, including where data came from, how it was collected, and what processing or transformations were applied.",
        "A.7.3 -> p.19; B.7.2 -> p.37",
        "ISO/IEC 42001 states that organisations shall document details of data acquisition and selection, and shall record data provenance. The guidance notes that data provenance information should include the source of data, methods of collection, any preprocessing or transformations applied, and the rationale for including or excluding certain data. Recording this information supports traceability, enables quality assurance, facilitates impact assessments and helps the organisation demonstrate compliance with legal and ethical obligations related to data use."
    ),
    "DI-4": (
        "This question asks whether mechanisms are in place to detect and prevent data poisoning or adversarial manipulation. ISO/IEC 42001 does not explicitly use the term 'data poisoning' but requires organisations to identify and assess AI-specific risks, including those related to data integrity and security, and to implement controls to mitigate such risks.",
        "A.5.4 -> p.17; B.6.2.5 -> p.34; B.8.1 -> p.39",
        "ISO/IEC 42001 requires organisations to establish a process for assessing AI risks and opportunities, and to plan actions to address them. It notes that AI-specific risks can include data quality issues, adversarial attacks and manipulation, and that organisations should consider these when designing verification and validation activities. The standard also requires that security controls be implemented to protect AI systems and their data from unauthorised access, modification or corruption. While 'data poisoning' is not explicitly mentioned, the standard's requirements for risk assessment, data quality verification and security controls provide a framework for addressing such threats."
    ),
    "DI-5": (
        "This question evaluates whether the organisation validates and sanitises external data sources before use in AI systems. ISO/IEC 42001 requires organisations to define and document processes for data acquisition and selection, to verify data quality, and to implement controls to ensure that data meets requirements before it is used.",
        "A.7.2 -> p.19; B.7.2 -> p.37",
        "ISO/IEC 42001 states that organisations shall define, document and implement data management processes, including data acquisition and selection. It requires that data quality requirements be specified and that data be verified against those requirements before use. The guidance notes that when acquiring data from external sources, organisations should assess the reliability and trustworthiness of the source, verify that the data meets quality and ethical standards, and apply appropriate preprocessing or sanitisation to remove errors, outliers or malicious content. This ensures that external data does not introduce integrity or security risks into the AI system."
    ),
    "DI-6": (
        "This question checks whether data storage and access controls are implemented to protect data integrity. ISO/IEC 42001 requires organisations to implement security controls for AI systems and their data, including access controls, encryption and measures to prevent unauthorised modification. It references information security standards such as ISO/IEC 27001 for detailed guidance.",
        "B.8.1 -> p.39",
        "ISO/IEC 42001 states that organisations should implement security controls to protect AI systems and associated data from unauthorised access, disclosure, modification, destruction or interference. It notes that controls can include access management, encryption, secure storage, audit logging and intrusion detection. The standard references ISO/IEC 27001 and ISO/IEC 27002 for comprehensive information security practices. By implementing these controls, organisations protect the integrity of data used by AI systems, ensuring that it is not corrupted, tampered with or accessed by unauthorised parties."
    ),
    "DI-7": (
        "This question asks whether the organisation has processes to identify and correct errors or inconsistencies in data. ISO/IEC 42001 requires organisations to define data quality requirements, to verify data against those requirements, and to take corrective action when deficiencies are identified. This includes processes for data cleaning, error detection and correction.",
        "A.7.2 -> p.19; B.7.1 -> p.36; B.10.1 -> p.43",
        "ISO/IEC 42001 requires that organisations specify data quality requirements, including accuracy and consistency, and verify that data meets these requirements. It also requires that organisations plan actions to address risks and opportunities, and take corrective action when deficiencies are identified. The guidance notes that data management processes should include procedures for data cleaning, error detection, validation and correction, and that organisations should document and address data quality issues promptly to prevent them from affecting AI system performance or trustworthiness."
    ),
    "DI-8": (
        "This question evaluates whether the organisation ensures data integrity during transmission and processing. ISO/IEC 42001 requires organisations to implement security controls, including measures to protect data in transit and during processing, and to verify that data has not been corrupted or tampered with.",
        "B.8.1 -> p.39",
        "ISO/IEC 42001 states that organisations should implement security controls to protect AI systems and associated data throughout their lifecycle, including during transmission and processing. The guidance notes that controls can include encryption for data in transit, checksums or hash functions to verify data integrity, secure communication protocols and validation checks at each processing stage. The standard references ISO/IEC 27001 and ISO/IEC 27002 for detailed information security practices. These measures ensure that data retains its integrity as it moves between systems, components or locations, and that any corruption or tampering is detected and addressed."
    ),
    
    # RELIABILITY - RE-1 to RE-8
    "RE-1": (
        "This question assesses whether the organisation defines and measures performance metrics for AI systems, such as accuracy, precision and recall. ISO/IEC 42001 requires organisations to establish objectives for AI system performance, to define evaluation criteria that include performance metrics, and to verify that systems meet those criteria before deployment.",
        "A.6.2.2 -> p.18; A.6.2.4 -> p.19; B.6.2.4 -> p.33",
        "ISO/IEC 42001 states that organisations shall define and document objectives and requirements for the AI system, including performance objectives. It requires that evaluation criteria be documented and that AI systems be evaluated against those criteria. The guidance notes that performance metrics can include accuracy, precision, recall, F1 score, latency and other measures relevant to the intended use. The standard emphasises that performance should be evaluated not only during development but also in operational conditions, and that systems should only be deployed if they meet documented performance requirements."
    ),
    "RE-2": (
        "This question evaluates whether AI systems are tested under diverse and realistic conditions to ensure reliable performance. ISO/IEC 42001 requires organisations to define and document verification and validation measures, to test AI systems against documented criteria, and to consider operational factors such as data variability, edge cases and deployment environments when evaluating performance.",
        "A.6.2.4 -> p.19; B.6.2.4 -> p.33; B.6.2.5 -> p.34",
        "ISO/IEC 42001 states that organisations shall define and document verification and validation measures and their evaluation criteria, and apply these during AI system development. The guidance notes that testing should consider the intended use, deployment context, data quality and variability, edge cases and potential failure modes. It also notes that evaluation should be performed under conditions that simulate real-world operation as closely as possible. This ensures that AI systems are reliable and perform as expected not only in controlled environments but also in diverse and challenging operational conditions."
    ),
    "RE-3": (
        "This question checks whether the organisation monitors AI system performance in production and responds to degradation or failures. ISO/IEC 42001 requires organisations to define and document ongoing operation and monitoring, to establish metrics for monitoring system performance, and to take action when performance deviates from expectations or becomes unacceptable.",
        "A.7.5 -> p.19; B.7.4 -> p.38",
        "ISO/IEC 42001 requires that organisations define and document elements needed for the ongoing operation of the AI system, including monitoring and maintenance. It states that metrics for monitoring system performance should be established and that actions should be taken when monitoring indicates that performance is unacceptable or deviates from expectations. The guidance notes that monitoring can include tracking accuracy, latency, data quality and user feedback, and that organisations should have processes in place to investigate performance degradation, diagnose root causes and implement corrective measures such as retraining, updating or decommissioning the system."
    ),
    "RE-4": (
        "This question asks whether the organisation evaluates and mitigates the risk of model drift or performance degradation over time. ISO/IEC 42001 requires organisations to monitor AI system performance during operation, to assess risks related to changes in data distributions or operational contexts, and to take action when performance degrades. This includes updating or retraining models as needed.",
        "A.7.5 -> p.19; A.7.6 -> p.19; B.7.4 -> p.38",
        "ISO/IEC 42001 requires that organisations define and document ongoing operation and monitoring, including maintenance, updates and performance tracking. It notes that AI systems may experience performance degradation due to changes in data distributions, operational environments or user behaviour—a phenomenon sometimes called model drift. The standard requires that organisations monitor for such degradation, assess associated risks and take corrective action, which can include retraining the model on updated data, adjusting parameters or modifying the system design. Documentation of updates and their impacts should also be maintained."
    ),
    "RE-5": (
        "This question evaluates whether the organisation has contingency plans or fallback mechanisms for when AI systems fail or produce unreliable outputs. ISO/IEC 42001 requires organisations to assess potential failures and their impacts, to plan for incidents and to implement controls such as human oversight or alternative processes to mitigate risks when AI systems fail.",
        "B.5.2 -> p.27; B.9.4 -> p.42; B.10.1 -> p.43; B.10.2 -> p.44",
        "ISO/IEC 42001 requires that organisations assess potential consequences of AI systems, including predictable failures, and plan actions to address risks. It notes that human oversight should be maintained, with consideration given to when and how humans can intervene if the system fails or produces unreliable outputs. The standard also requires that organisations establish processes for managing incidents, including procedures for identifying, recording and responding to failures. By implementing contingency plans, fallback mechanisms and human oversight, organisations ensure that when AI systems fail, there are alternative processes in place to maintain critical functions and minimise harm."
    ),
    "RE-6": (
        "This question checks whether the organisation conducts stress testing or adversarial testing to evaluate system robustness. ISO/IEC 42001 does not explicitly mandate adversarial testing but requires organisations to define verification and validation measures that include testing for robustness, to consider edge cases and failure modes, and to assess risks related to adversarial attacks.",
        "A.6.2.4 -> p.19; B.6.2.5 -> p.34",
        "ISO/IEC 42001 requires that organisations define and document verification and validation measures and their evaluation criteria. The guidance notes that verification and validation should include testing for robustness, which can involve exposing the AI system to challenging, edge-case or adversarial inputs to evaluate whether it behaves reliably and safely. The standard also requires that AI-specific risks, including adversarial attacks, be identified and addressed. While the term 'adversarial testing' is not explicitly used, the requirements for comprehensive validation and risk assessment support the use of such testing methods to ensure system robustness."
    ),
    "RE-7": (
        "This question asks whether the organisation maintains version control and documentation for AI models and their dependencies. ISO/IEC 42001 requires organisations to document AI system design and development, to control changes and updates, and to maintain records of versions, configurations and dependencies. This supports reproducibility, traceability and reliability.",
        "A.7.6 -> p.19; B.6.2.7 -> p.35",
        "ISO/IEC 42001 requires that organisations define and document processes for updates and modifications to AI systems, and that records of changes be controlled and maintained. The guidance notes that technical documentation should include information about the AI system's design, architecture, versions, dependencies and configuration. Version control practices ensure that the organisation can trace which model version is deployed, reproduce previous versions if needed, understand the impact of changes and maintain consistency across development, testing and production environments. This supports system reliability and facilitates troubleshooting and audits."
    ),
    "RE-8": (
        "This question evaluates whether the organisation assesses and documents the limitations and failure modes of AI systems. ISO/IEC 42001 requires organisations to assess potential failures and their impacts, to document known limitations, and to communicate this information to users and stakeholders. This transparency supports informed use and appropriate reliance on AI systems.",
        "B.5.2 -> p.27; B.6.2.7 -> p.35; B.8.2 -> p.40",
        "ISO/IEC 42001 requires that organisations assess potential consequences of AI systems, including predictable failures, and identify sources, events, outcomes and likelihood. It also requires that technical documentation include information about known limitations, assumptions and constraints, and that users be provided with information about limitations and how to interpret system outputs. The guidance notes that by documenting and communicating failure modes and limitations, organisations enable users to make informed decisions about when and how to rely on the AI system, and help prevent misuse or over-reliance that could lead to harm."
    ),
}

print("\nContinuing with remaining domains...")
print("=" * 70)

for question_code, (rationale, citation, control_intent) in remaining_data.items():
    if question_code in data:
        data[question_code]['alignmentRationale'] = rationale
        data[question_code]['citation'] = citation
        data[question_code]['controlIntent'] = control_intent
        updated_count += 1
        print(f"✅ {question_code}")
    else:
        print(f"⚠️  {question_code} not found in database")

# Save again
with open('/app/frontend/src/data/iso42001AlignmentData.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 70)
print(f"✅ Total updated: {updated_count} questions")

# Final verification
questions_with_control_intent = sum(1 for q in data.values() if 'controlIntent' in q)
print(f"📊 Questions with controlIntent field: {questions_with_control_intent}/{len(data)}")


# Final batch - Security, Privacy, Safety, Inclusivity, Sustainability
final_data = {
    # SECURITY - SE-1 to SE-8
    "SE-1": (
        "This question assesses whether security controls are implemented to protect AI systems from unauthorised access, tampering or misuse. ISO/IEC 42001 requires organisations to implement security controls for AI systems and associated data, referencing information security standards such as ISO/IEC 27001 for detailed guidance on access controls, encryption and security management.",
        "B.8.1 -> p.39",
        "ISO/IEC 42001 states that organisations should implement security controls to protect AI systems and associated data from unauthorised access, disclosure, modification, destruction or interference. The guidance notes that controls can include access management, authentication, authorisation, encryption, secure configuration, network security, audit logging and intrusion detection. The standard references ISO/IEC 27001 and ISO/IEC 27002 for comprehensive information security practices and notes that security considerations should be integrated throughout the AI lifecycle, from design and development to deployment and operation."
    ),
    "SE-2": (
        "This question evaluates whether the organisation conducts security testing, including penetration testing and vulnerability assessments, for AI systems. ISO/IEC 42001 requires organisations to define verification and validation measures, to assess AI-specific risks including security vulnerabilities, and to test systems for robustness. Security testing is an important part of ensuring that AI systems are protected against threats.",
        "A.6.2.4 -> p.19; B.6.2.5 -> p.34; B.8.1 -> p.39",
        "ISO/IEC 42001 requires that organisations define and document verification and validation measures and their evaluation criteria, and apply these during AI system development. The guidance notes that verification and validation should include testing for security vulnerabilities, robustness against attacks and compliance with security requirements. It also notes that AI-specific risks, including adversarial attacks and security threats, should be identified and assessed. While the standard does not explicitly mandate penetration testing, the requirements for comprehensive validation and security controls support the use of such testing methods to identify and address vulnerabilities before deployment."
    ),
    "SE-3": (
        "This question checks whether the organisation protects AI models and algorithms from theft or reverse engineering. ISO/IEC 42001 requires organisations to implement security controls, including measures to protect intellectual property and proprietary information, and to control access to AI system components such as models, data and algorithms.",
        "B.8.1 -> p.39",
        "ISO/IEC 42001 states that organisations should implement security controls to protect AI systems and associated assets from unauthorised access, disclosure, modification or theft. The guidance notes that AI models, algorithms and training data can be valuable intellectual property and may be targets for theft or reverse engineering. Controls can include access restrictions, encryption, obfuscation, secure deployment environments, legal agreements and monitoring for unauthorised use. The standard references ISO/IEC 27001 for comprehensive guidance on protecting information assets, including intellectual property."
    ),
    "SE-4": (
        "This question asks whether the organisation monitors for and responds to security incidents or breaches affecting AI systems. ISO/IEC 42001 requires organisations to establish processes for managing AI incidents, including security incidents, and to implement monitoring and response mechanisms. It references ISO/IEC 27001 and ISO/IEC 27035 for incident management practices.",
        "B.10.1 -> p.43; B.10.2 -> p.44; B.8.1 -> p.39",
        "ISO/IEC 42001 requires that organisations establish and maintain a process for managing AI incidents, which includes identifying, recording, investigating, analysing and responding to incidents such as security breaches, unauthorised access or cyber attacks. The guidance notes that organisations should implement monitoring mechanisms to detect security incidents, have procedures for responding promptly and effectively, and document incidents and their resolution. The standard also notes that security controls should include audit logging, intrusion detection and incident response capabilities. It references ISO/IEC 27001 and ISO/IEC 27035 for detailed guidance on information security incident management."
    ),
    "SE-5": (
        "This question evaluates whether the organisation assesses and mitigates risks from adversarial attacks, such as evasion or model inversion attacks. ISO/IEC 42001 requires organisations to identify and assess AI-specific risks, including adversarial attacks, and to implement controls to mitigate those risks. This includes testing for robustness and implementing defensive measures.",
        "A.5.4 -> p.17; B.6.2.5 -> p.34; B.8.1 -> p.39",
        "ISO/IEC 42001 requires organisations to establish a process for assessing AI risks and opportunities, and to plan actions to address them. The guidance notes that AI-specific risks can include adversarial attacks, such as evasion attacks that cause misclassification, model inversion attacks that extract training data, and poisoning attacks that corrupt training data. The standard requires that verification and validation activities consider robustness against such attacks and that security controls be implemented to detect and mitigate them. While specific attack types are not exhaustively listed, the requirements for risk assessment and security testing provide a framework for addressing adversarial threats."
    ),
    "SE-6": (
        "This question checks whether the organisation implements secure software development practices, such as code reviews and dependency management, for AI systems. ISO/IEC 42001 requires organisations to document AI system design and development, to implement security controls, and to manage third-party components and dependencies. It references secure development standards for detailed guidance.",
        "A.6.2.3 -> p.19; B.8.1 -> p.39",
        "ISO/IEC 42001 requires that organisations document AI system design and development, including security considerations. The guidance notes that secure development practices, such as code reviews, static and dynamic analysis, secure coding standards, dependency management and vulnerability scanning, should be applied to AI system development. It also notes that third-party components, libraries and frameworks should be assessed for security risks and that their use should be controlled and documented. The standard references ISO/IEC 27001 and secure software development standards such as ISO/IEC 27034 for detailed guidance on integrating security into the development lifecycle."
    ),
    "SE-7": (
        "This question asks whether access to training data, models and infrastructure is restricted and logged. ISO/IEC 42001 requires organisations to implement access controls, to ensure that only authorised personnel can access sensitive AI system components, and to maintain audit logs of access and modifications.",
        "B.8.1 -> p.39",
        "ISO/IEC 42001 states that organisations should implement security controls, including access management, to protect AI systems and associated data. The guidance notes that controls can include authentication and authorisation mechanisms, role-based access control, least privilege principles and audit logging of access and changes. By restricting access to training data, models and infrastructure to authorised personnel and maintaining logs of who accessed what and when, organisations protect against unauthorised use, accidental or malicious modification and insider threats. The standard references ISO/IEC 27001 and ISO/IEC 27002 for comprehensive guidance on access control and audit logging practices."
    ),
    "SE-8": (
        "This question evaluates whether the organisation encrypts sensitive data used by AI systems, both at rest and in transit. ISO/IEC 42001 requires organisations to implement security controls, including encryption, to protect AI systems and associated data from unauthorised access or disclosure.",
        "B.8.1 -> p.39",
        "ISO/IEC 42001 states that organisations should implement security controls to protect AI systems and associated data from unauthorised access, disclosure, modification or destruction. The guidance notes that encryption is an important control for protecting sensitive data, both when stored (at rest) and when transmitted (in transit). Encryption helps ensure that even if data is intercepted or accessed without authorisation, it cannot be read or used by unauthorised parties. The standard references ISO/IEC 27001 and ISO/IEC 27002 for detailed guidance on encryption and cryptographic controls, including key management, algorithm selection and secure implementation practices."
    ),
    
    # PRIVACY - PR-1 to PR-8
    "PR-1": (
        "This question assesses whether the organisation has policies and processes to protect personal data used in AI systems and comply with privacy regulations. ISO/IEC 42001 requires organisations to determine and comply with applicable legal and regulatory requirements, including privacy laws, and to establish processes for managing data that include privacy considerations.",
        "A.5.2 -> p.17; A.7.2 -> p.19; B.7.1 -> p.36; B.7.3 -> p.37",
        "ISO/IEC 42001 states that organisations shall establish, implement and maintain an AI policy that includes commitment to comply with applicable legal, regulatory and contractual requirements. It requires that data management processes consider privacy requirements and that organisations identify and address privacy obligations related to the collection, use, storage and sharing of personal data. The standard notes that privacy considerations should be integrated throughout the AI lifecycle and that organisations should implement controls such as consent management, data minimisation, anonymisation and access restrictions. It references privacy standards such as ISO/IEC 27701 and legal frameworks such as GDPR for detailed guidance."
    ),
    "PR-2": (
        "This question evaluates whether the organisation conducts privacy impact assessments (PIAs) or data protection impact assessments (DPIAs) for AI systems that process personal data. ISO/IEC 42001 requires organisations to conduct AI system impact assessments, which include evaluating privacy-related impacts, and to document and address those impacts.",
        "B.5.1 -> p.27; B.5.2 -> p.27; B.5.3 -> p.28; B.5.4 -> p.28",
        "ISO/IEC 42001 requires that organisations establish and maintain a process for AI system impact assessment to assess potential consequences for individuals, groups and societies across the system's life cycle. The guidance notes that impact assessments should consider privacy implications, including how personal data is collected, used, stored, shared and protected. The standard references privacy impact assessment methodologies and notes that in many jurisdictions, such as under GDPR, DPIAs are legally required for high-risk data processing activities. By conducting PIAs or DPIAs, organisations identify and mitigate privacy risks, demonstrate compliance and build trust with data subjects and regulators."
    ),
    "PR-3": (
        "This question checks whether the organisation implements data minimisation, collecting and using only the data necessary for AI system purposes. ISO/IEC 42001 requires organisations to define data management processes that include considerations for data minimisation and to document the rationale for data acquisition and selection.",
        "A.7.2 -> p.19; B.7.2 -> p.37",
        "ISO/IEC 42001 requires that organisations define and document data management processes, including data acquisition and selection. The guidance notes that organisations should document the rationale for including or excluding certain data and should consider principles such as data minimisation—collecting only data that is necessary, relevant and adequate for the intended purpose. Data minimisation reduces privacy risks, limits exposure in case of breaches, simplifies compliance with privacy regulations and improves system efficiency. The standard references privacy frameworks such as GDPR, which mandates data minimisation as a core principle."
    ),
    "PR-4": (
        "This question asks whether the organisation obtains informed consent from individuals whose data is used in AI systems. ISO/IEC 42001 requires organisations to comply with applicable legal and regulatory requirements, including consent requirements under privacy laws, and to document how personal data is acquired and the legal basis for its use.",
        "A.7.2 -> p.19; B.7.2 -> p.37; B.7.3 -> p.37",
        "ISO/IEC 42001 requires that organisations define and document data management processes and document details of data acquisition, including the legal basis for collecting and using personal data. The guidance notes that in many jurisdictions, privacy laws such as GDPR require informed consent from individuals before their personal data can be processed, particularly for sensitive data or high-risk processing activities. The standard requires that organisations identify applicable legal requirements and implement processes to obtain, document and manage consent where required. This includes providing individuals with clear information about how their data will be used and allowing them to withdraw consent."
    ),
    "PR-5": (
        "This question evaluates whether the organisation supports data subject rights, such as access, correction, deletion and portability. ISO/IEC 42001 requires organisations to comply with applicable legal and regulatory requirements, including privacy laws that grant individuals rights over their personal data, and to establish processes for responding to data subject requests.",
        "B.7.3 -> p.37",
        "ISO/IEC 42001 notes that organisations should identify and comply with applicable legal and regulatory requirements related to personal data, including data subject rights. The guidance references privacy frameworks such as GDPR, which grants individuals rights to access their personal data, request corrections, request deletion (right to be forgotten), restrict processing, object to processing and request data portability. The standard requires that organisations establish processes for receiving, verifying and responding to data subject requests in a timely manner, and for documenting such requests and responses. Supporting data subject rights demonstrates respect for privacy and compliance with legal obligations."
    ),
    "PR-6": (
        "This question checks whether the organisation anonymises or pseudonymises personal data where appropriate to reduce privacy risks. ISO/IEC 42001 requires organisations to implement privacy-enhancing measures, including anonymisation and pseudonymisation, where appropriate, and to document how personal data is protected.",
        "B.7.3 -> p.37",
        "ISO/IEC 42001 notes that organisations should implement appropriate technical and organisational measures to protect personal data, including privacy-enhancing technologies such as anonymisation and pseudonymisation. Anonymisation removes personal identifiers so that individuals can no longer be identified, thereby reducing privacy risks. Pseudonymisation replaces identifiers with pseudonyms, reducing the risk of re-identification while still allowing data to be linked. The guidance notes that anonymisation and pseudonymisation can be used during data preparation, storage and sharing to minimise privacy risks while enabling AI system development and operation. The standard references privacy standards such as ISO/IEC 27701 for detailed guidance on these techniques."
    ),
    "PR-7": (
        "This question asks whether the organisation limits data retention and securely deletes data when no longer needed. ISO/IEC 42001 requires organisations to define data management processes that include data retention and deletion policies, to comply with applicable legal requirements, and to implement secure deletion practices.",
        "A.7.2 -> p.19; B.7.1 -> p.36; B.7.3 -> p.37",
        "ISO/IEC 42001 requires that organisations define and document data management processes, including policies for data retention and deletion. The guidance notes that personal data should not be kept longer than necessary for the purposes for which it was collected, in line with privacy principles such as storage limitation under GDPR. The standard requires that organisations define retention periods, review data periodically and securely delete or anonymise data when it is no longer needed. Secure deletion practices ensure that data cannot be recovered or reconstructed, protecting individuals' privacy and reducing the organisation's liability and storage costs."
    ),
    "PR-8": (
        "This question evaluates whether the organisation shares or transfers personal data only with appropriate safeguards and legal basis. ISO/IEC 42001 requires organisations to comply with applicable legal requirements for data sharing and transfer, to document data flows, and to implement controls such as contracts, encryption and privacy-enhancing technologies to protect data during sharing or transfer.",
        "B.7.3 -> p.37",
        "ISO/IEC 42001 notes that organisations should identify and comply with legal and regulatory requirements related to sharing or transferring personal data, including cross-border data transfers. The guidance references privacy frameworks such as GDPR, which requires that personal data be shared or transferred only with appropriate legal basis and safeguards, such as adequacy decisions, standard contractual clauses, binding corporate rules or explicit consent. The standard requires that organisations document data flows, assess risks associated with sharing or transfer, and implement technical and organisational measures such as encryption, access controls and contractual protections to ensure that personal data remains protected when shared with third parties or transferred to other jurisdictions."
    ),
    
    # SAFETY - SA-1 to SA-8
    "SA-1": (
        "This question assesses whether the organisation identifies and evaluates safety risks associated with AI systems. ISO/IEC 42001 requires organisations to establish processes for assessing AI risks and impacts, including safety risks, and to document and address those risks. It references safety standards such as ISO/IEC 23894 for AI-specific safety guidance.",
        "A.5.4 -> p.17; B.5.1 -> p.27; B.5.2 -> p.27",
        "ISO/IEC 42001 requires that organisations establish a process for assessing AI risks and opportunities, and a process for AI system impact assessment to assess potential consequences for individuals, groups and societies. The guidance notes that risk and impact assessments should consider safety implications, including potential physical harm, psychological harm or harm to health and wellbeing. The standard requires that risks be identified, evaluated for likelihood and severity, and addressed through mitigation measures. It references safety standards such as ISO/IEC 23894 (guidance on AI safety) and ISO 31000 (risk management) for detailed methodologies."
    ),
    "SA-2": (
        "This question evaluates whether the organisation implements safety controls, such as fail-safe mechanisms and human oversight, to prevent harm. ISO/IEC 42001 requires organisations to plan actions to address AI risks, to implement controls such as human oversight, and to ensure that AI systems operate safely and can be overridden or shut down if necessary.",
        "B.9.4 -> p.42; B.10.1 -> p.43",
        "ISO/IEC 42001 notes that organisations should implement controls to mitigate AI risks, including safety risks. The guidance discusses human oversight as an important control, noting that the extent and nature of oversight should be determined based on the system's characteristics and impacts. It also notes that users should be informed about how to override, query or challenge the AI system, implying that fail-safe mechanisms and manual overrides should be available. The standard requires that organisations plan for incidents and have procedures for responding when AI systems fail or behave unexpectedly, including shutting down or isolating the system to prevent harm."
    ),
    "SA-3": (
        "This question checks whether the organisation conducts safety testing and validation, including testing for edge cases and failure modes. ISO/IEC 42001 requires organisations to define and document verification and validation measures, to test AI systems against documented criteria, and to consider edge cases, failure modes and safety-critical scenarios.",
        "A.6.2.4 -> p.19; B.6.2.5 -> p.34",
        "ISO/IEC 42001 requires that organisations define and document verification and validation measures and their evaluation criteria, and apply these during AI system development. The guidance notes that verification and validation should include testing for safety, robustness and resilience, and should consider edge cases, unusual inputs, failure modes and safety-critical scenarios. The standard notes that testing should simulate real-world conditions, including challenging or adverse situations, to ensure that AI systems behave safely and predictably. It references safety standards such as ISO/IEC 23894 for AI-specific safety validation guidance."
    ),
    "SA-4": (
        "This question asks whether the organisation monitors AI systems in operation for safety-related issues and responds to incidents. ISO/IEC 42001 requires organisations to define ongoing monitoring of AI systems, to establish metrics for detecting safety issues, and to implement incident management processes that include procedures for responding to safety-related incidents.",
        "A.7.5 -> p.19; B.7.4 -> p.38; B.10.2 -> p.44",
        "ISO/IEC 42001 requires that organisations define and document ongoing operation and monitoring of AI systems, including metrics for monitoring performance and safety. It also requires that organisations establish and maintain a process for managing AI incidents, including identifying, recording, investigating and responding to safety-related incidents. The guidance notes that monitoring should detect deviations from expected behaviour, safety-critical errors or conditions that could lead to harm, and that organisations should have procedures for responding promptly, including alerting relevant personnel, taking corrective action and communicating with affected parties."
    ),
    "SA-5": (
        "This question evaluates whether the organisation assesses and addresses safety risks introduced by interactions between AI components and other systems. ISO/IEC 42001 requires organisations to assess system-level risks, to consider interactions and dependencies, and to evaluate how AI components integrate with broader systems or environments.",
        "B.5.2 -> p.27; B.6.2.1 -> p.31",
        "ISO/IEC 42001 requires that organisations assess potential consequences of AI systems across their life cycle, including interactions with other systems, components or the operational environment. The guidance notes that AI systems often operate as part of larger systems-of-systems, and that safety risks can arise from interactions, dependencies or integration issues. The standard requires that requirements for the AI system consider the operational context, including interfaces with other systems, and that organisations evaluate whether the AI system behaves safely and predictably when integrated into the broader system. This systems-level perspective is essential for identifying and mitigating emergent safety risks."
    ),
    "SA-6": (
        "This question checks whether the organisation documents and communicates safety-related limitations and precautions to users and stakeholders. ISO/IEC 42001 requires organisations to provide users with information about AI system limitations, potential harms, operational requirements and precautions, and to include this information in technical documentation.",
        "B.8.2 -> p.40; B.6.2.7 -> p.35",
        "ISO/IEC 42001 states that organisations shall determine and provide the information users need about the AI system, including known limitations, potential harms and operational requirements. The guidance notes that users should understand safety-related precautions, such as conditions under which the system should not be used, required supervision or oversight, and how to respond if the system behaves unexpectedly. Technical documentation should also describe safety considerations, failure modes and mitigation measures. By communicating this information clearly, organisations enable users to operate AI systems safely and responsibly, reducing the risk of harm due to misuse or over-reliance."
    ),
    "SA-7": (
        "This question asks whether the organisation establishes and follows procedures for decommissioning or withdrawing unsafe AI systems. ISO/IEC 42001 requires organisations to define lifecycle processes, including withdrawal and disposal, and to have procedures for responding when AI systems are found to be unsafe or no longer meet requirements.",
        "B.10.1 -> p.43; B.10.2 -> p.44",
        "ISO/IEC 42001 requires that organisations plan actions to address AI risks and opportunities, and establish processes for managing AI incidents. The guidance notes that when an AI system is found to be unsafe, underperforming or no longer fit for purpose, the organisation should have procedures for withdrawing, decommissioning or deactivating the system. This can include notifying affected parties, ceasing operations, retrieving or updating deployed systems, and ensuring that users are informed and transitioned to alternative solutions. The standard also requires that decisions about withdrawal and lessons learned be documented, supporting continuous improvement and responsible AI management."
    ),
    "SA-8": (
        "This question evaluates whether the organisation involves safety experts or conducts independent safety reviews for high-risk AI systems. ISO/IEC 42001 does not explicitly mandate independent safety reviews but requires organisations to assess AI risks and impacts, to ensure competence of personnel, and to conduct internal audits. Many organisations engage safety experts or independent reviewers for high-risk systems.",
        "A.7.1 -> p.19; A.9.2 -> p.20; B.5.1 -> p.27",
        "ISO/IEC 42001 requires that organisations ensure personnel working on AI systems are competent, which can include having appropriate expertise in safety engineering and risk management. It also requires that internal audits be conducted to evaluate conformity with requirements and effective implementation of the management system. While the standard does not explicitly require independent safety reviews, it notes that for high-risk or safety-critical AI systems, organisations should consider additional scrutiny, such as engaging external safety experts, conducting independent assessments or following domain-specific safety standards. This provides assurance that safety risks have been thoroughly evaluated and appropriately addressed."
    ),
    
    # INCLUSIVITY - IN-1 to IN-8
    "IN-1": (
        "This question assesses whether the organisation evaluates and ensures that AI systems are accessible to users with disabilities. ISO/IEC 42001 does not explicitly mandate accessibility evaluations but recognises accessibility as a potential objective for responsible AI use and requires organisations to consider the needs of diverse user groups, including persons with disabilities.",
        "B.9.3 -> p.42; B.5.4 -> p.28",
        "ISO/IEC 42001 notes that organisations should identify and document objectives for responsible use of AI systems, which can include accessibility. It also requires that impact assessments consider the needs and protection requirements of different groups, including impaired persons. The guidance notes that when accessibility is defined as an objective, organisations should integrate measures to achieve it throughout the AI lifecycle, such as designing user interfaces that support assistive technologies, providing alternative formats for information, and testing with users who have diverse abilities. By proactively addressing accessibility, organisations ensure that AI systems are inclusive and do not exclude or disadvantage persons with disabilities."
    ),
    "IN-2": (
        "This question evaluates whether the organisation considers diverse user needs and contexts when designing and developing AI systems. ISO/IEC 42001 requires organisations to define AI system requirements based on intended use and user needs, to consider the operational context, and to assess impacts on different groups of users.",
        "A.6.2.1 -> p.18; B.6.2.1 -> p.31; B.5.4 -> p.28",
        "ISO/IEC 42001 requires that organisations define and document objectives and requirements for the AI system, taking into account the intended use, operational context and needs of interested parties. The guidance notes that organisations should consider the diversity of users, including differences in language, culture, technical proficiency, abilities and contexts of use. It also requires that impact assessments consider relevant demographic groups and the potential for differential impacts. By considering diverse user needs and contexts, organisations ensure that AI systems are designed inclusively and do not inadvertently exclude or disadvantage certain user groups."
    ),
    "IN-3": (
        "This question checks whether the organisation engages with diverse stakeholders, including marginalised or underrepresented groups, during AI development. ISO/IEC 42001 requires organisations to determine the needs and expectations of interested parties, to involve relevant stakeholders in impact assessments, and to consider diverse perspectives when designing and evaluating AI systems.",
        "B.3.2 -> p.26; B.5.3 -> p.28",
        "ISO/IEC 42001 requires that organisations determine the needs and expectations of interested parties that are relevant to the AI system, and document this information. The guidance notes that interested parties can include users, affected individuals and communities, civil society organisations, advocacy groups and representatives of marginalised or underrepresented populations. It also notes that AI system impact assessments should consider relevant demographic groups and should involve consultation or engagement with affected parties where appropriate. By engaging diverse stakeholders, organisations gain insights into potential impacts, identify blind spots and design AI systems that are more inclusive and equitable."
    ),
    "IN-4": (
        "This question asks whether the organisation evaluates whether AI systems disadvantage or exclude certain demographic or social groups. ISO/IEC 42001 requires organisations to conduct impact assessments that consider potential negative impacts on individuals, groups and societies, including fairness and inclusivity, and to document and address those impacts.",
        "B.5.2 -> p.27; B.5.3 -> p.28; B.5.4 -> p.28",
        "ISO/IEC 42001 requires that organisations establish a process for AI system impact assessment to assess potential consequences for individuals, groups and societies. The guidance notes that assessments should consider whether the AI system has differential impacts on different demographic or social groups, including potential for exclusion, disadvantage or discrimination. It requires that relevant demographic groups be documented and that negative impacts be identified, evaluated and addressed through mitigation measures. By proactively evaluating inclusivity and fairness, organisations can prevent AI systems from reinforcing or exacerbating inequalities."
    ),
    "IN-5": (
        "This question evaluates whether the organisation designs AI user interfaces and interactions to be culturally sensitive and linguistically inclusive. ISO/IEC 42001 does not explicitly mandate cultural or linguistic inclusivity but requires organisations to consider user needs and contexts, and to provide information that users can understand.",
        "B.8.2 -> p.40; B.6.2.1 -> p.31",
        "ISO/IEC 42001 requires that organisations define AI system requirements taking into account the intended use and operational context, and provide users with information about the AI system in a form they can understand. The guidance notes that user needs can include language preferences, cultural norms and contextual factors. While the standard does not explicitly require multilingual support or cultural adaptation, it emphasises that AI systems should be designed to meet the needs of their intended users, which can include providing interfaces and information in multiple languages, adapting to cultural contexts and avoiding assumptions or biases that exclude certain cultural or linguistic groups."
    ),
    "IN-6": (
        "This question checks whether the organisation monitors and addresses disparate impacts or outcomes across different user groups. ISO/IEC 42001 requires organisations to monitor AI system performance during operation, to assess impacts on individuals and groups, and to take corrective action when systems produce unequal or harmful outcomes.",
        "A.7.5 -> p.19; B.7.4 -> p.38; B.5.4 -> p.28",
        "ISO/IEC 42001 requires that organisations define and document ongoing operation and monitoring of AI systems, including metrics for monitoring performance. The guidance notes that monitoring should include evaluating whether the system performs equitably across different user groups and whether it produces disparate impacts. It also requires that organisations assess and document impacts on individuals or groups throughout the lifecycle, considering fairness and inclusivity. When monitoring indicates that the AI system disadvantages or excludes certain groups, the organisation should investigate the causes, assess associated risks and take corrective action, such as retraining, adjusting parameters or redesigning the system."
    ),
    "IN-7": (
        "This question asks whether the organisation provides training or support to ensure equitable access to and use of AI systems. ISO/IEC 42001 requires organisations to determine what information and support users need, to provide appropriate training or guidance, and to ensure that users can effectively and safely use the AI system.",
        "A.7.1 -> p.19; B.8.2 -> p.40",
        "ISO/IEC 42001 requires that organisations determine the competence needed for persons working with or using AI systems, and provide appropriate training, awareness and support. It also requires that organisations determine and provide the information users need about the AI system, including how to use it, its purpose, limitations and how to override or query it. The guidance notes that training, user manuals, tutorials and support services can help ensure that users from diverse backgrounds and with varying levels of technical proficiency can access and effectively use the AI system. By providing appropriate training and support, organisations promote equitable access and prevent digital divides that could exclude less experienced or disadvantaged users."
    ),
    "IN-8": (
        "This question evaluates whether the organisation establishes metrics and goals for inclusivity and tracks progress over time. ISO/IEC 42001 does not explicitly mandate inclusivity metrics but requires organisations to define objectives for responsible AI development and use, to establish criteria for evaluating AI systems, and to monitor performance against those criteria.",
        "B.9.3 -> p.42; B.6.2.4 -> p.33; A.7.5 -> p.19",
        "ISO/IEC 42001 notes that organisations should identify and document objectives for responsible use of AI systems, which can include inclusivity, accessibility and equity. It requires that AI systems be evaluated against documented criteria that reflect these objectives, and that performance be monitored during operation. The guidance notes that organisations can establish metrics such as representation of diverse user groups, accessibility compliance scores, user satisfaction across demographics and measures of equitable outcomes. By defining inclusivity goals, measuring progress and tracking performance over time, organisations demonstrate commitment to inclusivity and create accountability for achieving equitable AI outcomes."
    ),
    
    # SUSTAINABILITY - SU-1 to SU-8
    "SU-1": (
        "This question assesses whether the organisation evaluates the energy consumption and carbon footprint of AI systems. ISO/IEC 42001 does not explicitly mandate environmental impact assessment but recognises sustainability as a potential objective for responsible AI development and use, and requires organisations to consider environmental impacts as part of broader impact assessments.",
        "B.9.3 -> p.42; B.5.2 -> p.27",
        "ISO/IEC 42001 notes that organisations should identify and document objectives for responsible development and use of AI systems, which can include environmental sustainability. It also requires that AI system impact assessments consider potential consequences for individuals, groups and societies, which can include environmental and resource impacts. The guidance notes that AI systems, particularly large-scale machine learning models, can consume significant energy and generate carbon emissions. By evaluating energy consumption and carbon footprint, organisations can identify opportunities to reduce environmental impact, improve efficiency and align AI development with sustainability goals."
    ),
    "SU-2": (
        "This question evaluates whether the organisation considers computational efficiency when designing and training AI models. ISO/IEC 42001 does not explicitly mandate efficiency optimisation but notes that if sustainability is defined as an objective, organisations should integrate measures to achieve it throughout the AI lifecycle, including selecting efficient algorithms and architectures.",
        "B.6.1.2 -> p.30; B.9.3 -> p.42",
        "ISO/IEC 42001 notes that when an organisation defines objectives for responsible AI development, such as sustainability or resource efficiency, these objectives should be incorporated into requirements specification, model training and validation. The guidance notes that computational efficiency can be improved through techniques such as selecting simpler or more efficient model architectures, optimising hyperparameters, pruning unnecessary parameters, using quantisation or distillation, and training on smaller or more representative datasets. By prioritising efficiency, organisations can reduce energy consumption, cost and environmental impact while maintaining acceptable performance."
    ),
    "SU-3": (
        "This question checks whether the organisation monitors and reports the environmental impact of AI systems. ISO/IEC 42001 does not explicitly require environmental reporting but notes that if sustainability is a defined objective, organisations should monitor relevant metrics and communicate information to interested parties.",
        "B.7.4 -> p.38; B.8.2 -> p.40",
        "ISO/IEC 42001 requires that organisations define and document ongoing operation and monitoring of AI systems, including metrics for monitoring performance. The guidance notes that if sustainability is identified as an objective, organisations should establish metrics such as energy consumption, carbon emissions, resource usage and computational efficiency, and monitor these during operation. It also notes that relevant information about AI systems, including environmental impacts, should be communicated to interested parties, which can include internal governance bodies, users, customers, regulators and the public. By monitoring and reporting environmental impact, organisations demonstrate transparency and accountability for sustainability."
    ),
    "SU-4": (
        "This question asks whether the organisation uses renewable energy or carbon offsets to reduce the environmental impact of AI operations. ISO/IEC 42001 does not explicitly mandate the use of renewable energy but notes that if sustainability is a defined objective, organisations should implement measures to achieve it, which can include sourcing renewable energy or participating in carbon offset programs.",
        "B.9.3 -> p.42",
        "ISO/IEC 42001 notes that organisations should identify and document objectives for responsible use of AI systems, including sustainability, and implement mechanisms to achieve those objectives. The guidance notes that reducing environmental impact can involve measures such as procuring renewable energy for data centres and computing infrastructure, selecting cloud providers that use renewable energy, optimising workload scheduling to use energy when renewable sources are available, or participating in carbon offset programs to compensate for unavoidable emissions. These measures demonstrate organisational commitment to sustainability and help mitigate the environmental footprint of AI operations."
    ),
    "SU-5": (
        "This question evaluates whether the organisation assesses the full lifecycle environmental impact of AI systems, including hardware production and disposal. ISO/IEC 42001 does not explicitly require lifecycle environmental assessment but notes that impact assessments should consider consequences across the AI system's life cycle, which can include hardware and infrastructure impacts.",
        "B.5.2 -> p.27",
        "ISO/IEC 42001 requires that organisations assess potential consequences of AI systems across their life cycle. The guidance notes that lifecycle considerations can extend beyond software to include the production, use and disposal of hardware and infrastructure, such as servers, GPUs, sensors and edge devices. The full environmental impact includes resource extraction, manufacturing energy and emissions, operational energy consumption, cooling requirements and electronic waste from disposal. By conducting lifecycle environmental assessments, organisations gain a comprehensive understanding of environmental impacts and can make more informed decisions about hardware procurement, usage and end-of-life management."
    ),
    "SU-6": (
        "This question checks whether the organisation implements strategies to extend hardware lifespan and reduce electronic waste. ISO/IEC 42001 does not explicitly address hardware lifecycle management but notes that sustainability can be an objective for AI systems and that organisations should implement measures to achieve defined objectives.",
        "B.9.3 -> p.42",
        "ISO/IEC 42001 notes that if sustainability is identified as an objective for AI systems, organisations should implement mechanisms to achieve it. The guidance notes that strategies to reduce electronic waste and extend hardware lifespan can include maintaining and upgrading existing hardware rather than replacing it, optimising software to run efficiently on older hardware, purchasing durable and repairable equipment, participating in hardware recycling or refurbishment programs, and designing AI systems to be compatible with a range of hardware configurations. These practices reduce resource consumption, lower costs and minimise the environmental impact of AI operations."
    ),
    "SU-7": (
        "This question asks whether the organisation evaluates the broader societal and environmental impacts of AI applications. ISO/IEC 42001 requires organisations to conduct impact assessments that consider potential consequences for individuals, groups and societies, including environmental and social impacts, and to document and address those impacts.",
        "B.5.2 -> p.27; B.5.3 -> p.28; B.5.4 -> p.28",
        "ISO/IEC 42001 requires that organisations establish a process for AI system impact assessment to assess potential consequences across the system's life cycle. The guidance notes that assessments should consider not only individual impacts but also broader societal and environmental implications, such as effects on employment, inequality, resource consumption, environmental degradation or community wellbeing. It requires that positive and negative impacts be identified, evaluated and documented, and that mitigation measures be implemented where necessary. By evaluating broader impacts, organisations take a holistic and responsible approach to AI development and deployment."
    ),
    "SU-8": (
        "This question evaluates whether the organisation sets and tracks sustainability goals for AI systems. ISO/IEC 42001 does not explicitly mandate sustainability goals but requires organisations to define objectives for responsible AI development and use, to establish evaluation criteria, and to monitor performance against those criteria.",
        "B.9.3 -> p.42; B.6.2.4 -> p.33",
        "ISO/IEC 42001 notes that organisations should identify and document objectives for responsible development and use of AI systems, which can include sustainability goals such as reducing energy consumption, minimising carbon emissions or improving resource efficiency. It requires that AI systems be evaluated against documented criteria that reflect these objectives, and that organisations monitor performance and take corrective action when objectives are not met. The guidance notes that setting clear, measurable sustainability goals and tracking progress over time demonstrates organisational commitment to environmental responsibility and enables continuous improvement in reducing the environmental impact of AI systems."
    ),
}

print("\nAdding final batch (Security, Privacy, Safety, Inclusivity, Sustainability)...")
print("=" * 70)

for question_code, (rationale, citation, control_intent) in final_data.items():
    if question_code in data:
        data[question_code]['alignmentRationale'] = rationale
        data[question_code]['citation'] = citation
        data[question_code]['controlIntent'] = control_intent
        updated_count += 1
        print(f"✅ {question_code}")
    else:
        print(f"⚠️  {question_code} not found in database")

# Final save
with open('/app/frontend/src/data/iso42001AlignmentData.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 70)
print(f"🎉 COMPLETE! Total updated: {updated_count}/{len(data)} questions")

# Final verification
questions_with_control_intent = sum(1 for q in data.values() if 'controlIntent' in q)
print(f"📊 Questions with controlIntent field: {questions_with_control_intent}/{len(data)}")
print("\n✅ All ISO 42001 alignment data has been successfully updated!")

