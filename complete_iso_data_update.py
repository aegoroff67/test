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
