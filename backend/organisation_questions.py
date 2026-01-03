# Organisation-wide AI Maturity Assessment Questions
# 10 Domains, 80 Questions Total
# Scoring: Foundational (1), Developing (2), Established (3), Leading (4)

ORGANISATION_QUESTIONS_DATA = [
    {
        "code": """AE-01""",
        "text": """How does the organisation define and uphold accountability for AI outcomes?""",
        "explanation": """AI accountability ensures that humans—not algorithms—remain responsible for outcomes and decisions. Without explicit accountability, it becomes unclear who owns errors, ethical breaches, or unintended consequences. This question evaluates whether your organisation has clearly assigned accountability for AI decision-making, outcomes, and impacts across leadership, development, and operational teams.

Example: A council’s Responsible AI Policy assigns accountability for each AI project to a nominated business owner, who must ensure ethical reviews, compliance checks, and performance monitoring are completed and documented.""",
        "domain_order": 1,
        "order": 1,
        "foundational": """Accountability for AI decisions or impacts is undefined or informal.""",
        "developing": """Some accountability exists but is inconsistently applied across projects.""",
        "established": """Clear accountability for AI outcomes is documented in policies and assigned to responsible officers.""",
        "leading": """Enterprise-wide accountability is embedded through governance frameworks, KPIs, and public reporting on AI performance.""",
        "additional_guide": """Additional Guidance - Establishing AI Accountability

Accountability ensures ethical integrity and legal defensibility. To strengthen it:  
• **Assign Ownership:** Nominate accountable officers for every AI system, covering design, deployment, and monitoring.  
• **Define Roles:** Clarify distinctions between decision-makers, reviewers, and system operators.  
• **Document Responsibilities:** Include AI accountability in job descriptions, policy statements, and governance charters.  
• **Enable Oversight:** Require periodic reporting to executives or ethics committees on AI performance and compliance.  
• **Establish Escalation Paths:** Ensure issues can be raised quickly to leadership.  
• **Promote Transparency:** Communicate accountability structures internally and, where appropriate, externally.  
Clear, documented accountability demonstrates leadership ownership of AI impacts and fosters stakeholder confidence.""",
        "evidence_types": """To comply with **AE-01 ("Define and uphold accountability for AI outcomes")**, provide documentation proving explicit assignment of responsibility.  
**Key Evidence Types:**  
• **Policies & Frameworks:** Responsible AI Policy or AI Governance Framework outlining accountability principles.  
• **Role Documents:** Job descriptions or delegation instruments identifying accountable officers.  
• **Registers:** AI system accountability registers linking projects to responsible owners.  
• **Reports:** Executive or committee minutes discussing AI performance and accountability.  
• **Performance Evidence:** KPIs or scorecards tracking accountability measures.  
• **Public Transparency:** Published statements or reports on AI accountability and ethics.  
**In short:** show that AI outcomes are owned by clearly identified leaders who are answerable for decisions and impacts.""",
    },
    {
        "code": """AE-02""",
        "text": """How does the organisation define and apply ethical principles to guide AI development and use?""",
        "explanation": """Ethical principles form the foundation of responsible AI. Without clear guidance, teams may unintentionally design or deploy systems that conflict with community values or legal obligations. This question assesses whether your organisation has defined a set of ethical principles—such as fairness, transparency, accountability, and human oversight—and consistently applies them across AI projects.

Example: A council adopts an “AI Ethics Charter” aligned with Australia’s AI Ethics Principles. It requires all projects to demonstrate compliance with these principles before approval and includes an ethics checklist in project templates.""",
        "domain_order": 1,
        "order": 2,
        "foundational": """No defined ethical principles or guidance exist for AI use.""",
        "developing": """Ethical principles are mentioned in policy documents but not consistently applied.""",
        "established": """Ethical principles are clearly defined, communicated, and embedded in AI governance and project processes.""",
        "leading": """Ethical principles are operationalised through measurable standards, mandatory reviews, and public transparency reporting.""",
        "additional_guide": """Additional Guidance - Defining and Applying Ethical Principles

Ethical frameworks ensure AI aligns with community expectations and organisational integrity. To strengthen ethical governance:  
• **Define Principles:** Adopt core ethics themes-fairness, accountability, transparency, privacy, and human-centred design.  
• **Align with Standards:** Reference recognised frameworks such as Australia's AI Ethics Principles, NIST AI RMF, or OECD AI Principles.  
• **Operationalise in Practice:** Translate principles into decision criteria, checklists, and approval workflows.  
• **Provide Ethics Training:** Build awareness of ethical dilemmas and best practice among staff and leadership.  
• **Review Regularly:** Refresh principles as technology, regulation, and social norms evolve.  
Embedding ethics into daily processes helps ensure responsible innovation and strengthens trust between the organisation and the public.""",
        "evidence_types": """To comply with **AE-02 ("Define and apply ethical principles for AI")**, provide documentation demonstrating adoption and practical use of ethical frameworks.  
**Key Evidence Types:**  
• **Ethics Charter or Policy:** Approved document outlining the organisation's AI ethics principles.  
• **Governance Frameworks:** Procedures mapping ethical principles to project approval or risk review steps.  
• **Checklists & Templates:** Ethics review forms or assessment tools referencing adopted principles.  
• **Training Materials:** Records of staff or leadership ethics training sessions.  
• **Communication Evidence:** Intranet pages, awareness campaigns, or public statements about AI ethics commitments.  
• **Audit or Review Reports:** Evaluations confirming ethical principles are applied consistently across projects.  
**In short:** demonstrate that AI ethics are clearly defined, formally adopted, and embedded in all stages of AI decision-making and oversight.""",
    },
    {
        "code": """AE-03""",
        "text": """How does the organisation ensure appropriate human oversight of AI systems and decisions?""",
        "explanation": """Human oversight safeguards against automation bias and unintended harm. Without clear oversight mechanisms, AI systems may operate unchecked, making opaque or unethical decisions. This question evaluates whether the organisation ensures human review, intervention, and approval at key stages of AI design, deployment, and operation.

Example: A council mandates that AI recommendations affecting citizens—such as service eligibility or resource allocation—require human validation before implementation, with decision logs recorded for accountability and audit purposes.""",
        "domain_order": 1,
        "order": 3,
        "foundational": """AI systems operate autonomously with minimal or no human review.""",
        "developing": """Some human oversight exists but is informal or inconsistently applied.""",
        "established": """Defined oversight procedures require human review and approval for critical AI decisions.""",
        "leading": """Human oversight is embedded organisation-wide, supported by training, escalation protocols, and audit verification.""",
        "additional_guide": """Additional Guidance - Strengthening Human Oversight

Human involvement ensures accountability and ethical balance in AI outcomes. To strengthen oversight:  
• **Define Oversight Thresholds:** Identify which AI decisions require human review (e.g., high-impact or citizen-facing systems).  
• **Establish Intervention Rights:** Ensure humans can override, pause, or modify AI outputs.  
• **Document Oversight Procedures:** Include review steps in operational workflows and project plans.  
• **Train Staff:** Educate reviewers on AI limitations, interpretability, and bias recognition.  
• **Log Decisions:** Record oversight actions for auditability and transparency.  
• **Review Regularly:** Reassess oversight adequacy as AI complexity and risk evolve.  
Consistent human oversight prevents blind reliance on automation, promoting ethical, defensible, and citizen-centric decision-making.""",
        "evidence_types": """To comply with **AE-03 ("Ensure appropriate human oversight of AI systems and decisions")**, provide artefacts showing structured human involvement and review.  
**Key Evidence Types:**  
• **Policies & Procedures:** AI Oversight or Human-in-the-Loop guidelines defining intervention points.  
• **Operational Records:** Logs showing human validation of AI recommendations or overrides.  
• **Workflow Documentation:** Flowcharts illustrating manual checkpoints within automated processes.  
• **Training Records:** Evidence of staff training on oversight responsibilities and escalation protocols.  
• **Governance Artefacts:** Committee minutes or assurance reports reviewing oversight effectiveness.  
• **Audit Findings:** Internal or external reviews confirming active human involvement.  
**In short:** demonstrate that humans remain meaningfully engaged in reviewing, approving, and taking responsibility for AI-driven outcomes.""",
    },
    {
        "code": """AE-04""",
        "text": """How does the organisation identify and manage conflicts of interest in AI governance and decision-making?""",
        "explanation": """Conflicts of interest can undermine trust and fairness in AI decision-making, particularly when individuals or departments stand to benefit from certain outcomes. Without defined management processes, bias and undue influence may distort ethical reviews or project approvals. This question assesses whether the organisation proactively identifies, declares, and mitigates potential conflicts within AI governance structures and project teams.

Example: A council’s AI Governance Committee requires members to complete annual conflict-of-interest declarations and recuse themselves from reviews of projects in which they have a personal or departmental interest.""",
        "domain_order": 1,
        "order": 4,
        "foundational": """Conflicts of interest are unmanaged or addressed informally on a case-by-case basis.""",
        "developing": """Some declarations exist, but processes are inconsistent or poorly enforced.""",
        "established": """Formal conflict-of-interest policies cover AI projects and governance bodies, supported by disclosure records.""",
        "leading": """Conflicts are actively monitored, with transparent disclosures, recusal protocols, and independent review mechanisms.""",
        "additional_guide": """Additional Guidance - Managing Conflicts of Interest in AI Governance

Proactive conflict management safeguards objectivity and integrity. To strengthen governance:  
• **Define Policy Requirements:** Extend organisational conflict-of-interest policies to include AI activities and ethical review committees.  
• **Mandate Disclosure:** Require all participants in AI decision-making to declare relevant personal, financial, or departmental interests.  
• **Record and Maintain Registers:** Keep up-to-date conflict registers for committees and project teams.  
• **Establish Recusal Procedures:** Ensure members abstain from decisions where impartiality may be compromised.  
• **Provide Training:** Educate staff on recognising and disclosing conflicts.  
• **Enable Independent Oversight:** Assign neutral reviewers for sensitive or high-impact projects.  
Transparent conflict management reinforces confidence in the fairness and independence of AI governance processes.""",
        "evidence_types": """To comply with **AE-04 ("Identify and manage conflicts of interest in AI governance")**, provide documentation demonstrating structured conflict management.  
**Key Evidence Types:**  
• **Policies & Procedures:** Conflict-of-interest policies referencing AI governance and project participation.  
• **Disclosure Forms:** Signed declarations from AI governance members or project teams.  
• **Conflict Registers:** Logs recording identified conflicts and management actions.  
• **Meeting Records:** Minutes showing recusals or independent review assignments.  
• **Training Materials:** Evidence of awareness sessions or e-learning on conflict management.  
• **Audit or Oversight Reports:** Reviews verifying compliance with disclosure and recusal procedures.  
**In short:** demonstrate that AI governance operates with transparency, impartiality, and documented mechanisms to detect and manage potential conflicts of interest.""",
    },
    {
        "code": """AE-05""",
        "text": """How are ethical reviews conducted for AI projects and decisions?""",
        "explanation": """Ethical reviews ensure AI projects align with organisational values, community expectations, and regulatory standards. Without a structured review process, potential harms—such as bias, discrimination, or privacy violations—may go undetected. This question evaluates whether the organisation conducts formal ethical assessments for AI systems, including documented reviews, approval criteria, and decision-making transparency.

Example: A council requires all AI projects to undergo an Ethics Impact Assessment before deployment. The results are reviewed by a cross-functional committee that includes Legal, Risk, and Community representatives.""",
        "domain_order": 1,
        "order": 5,
        "foundational": """Ethical considerations are informal or addressed only after deployment.""",
        "developing": """Some AI projects undergo ethics discussions, but reviews are inconsistent or undocumented.""",
        "established": """A formal ethical review process is in place, with structured templates, decision criteria, and review records.""",
        "leading": """Ethical reviews are mandatory for all AI projects, integrated with risk and governance workflows, and results are transparently reported.""",
        "additional_guide": """Additional Guidance - Conducting AI Ethical Reviews

Ethical reviews ensure AI systems respect fairness, accountability, and public trust. To mature your review process:  
• **Define Review Triggers:** Mandate ethics reviews for all new, high-risk, or citizen-impacting AI systems.  
• **Create Review Templates:** Standardise documentation capturing ethical principles, potential harms, and mitigation actions.  
• **Form Ethics Committees:** Establish multi-disciplinary groups to evaluate submissions objectively.  
• **Integrate with Risk Management:** Align ethical reviews with AI risk and compliance processes.  
• **Document Decisions:** Record findings, recommendations, and approval conditions.  
• **Report Transparently:** Communicate review outcomes to leadership or publicly for high-impact systems.  
Structured ethical reviews ensure AI deployments are deliberate, defensible, and aligned with community values.""",
        "evidence_types": """To comply with **AE-05 ("Conduct ethical reviews for AI projects")**, provide artefacts showing that ethical review mechanisms are defined, documented, and operational.  
**Key Evidence Types:**  
• **Ethical Review Policy:** Document mandating ethics assessments for AI projects.  
• **Templates & Checklists:** Standardised AI Ethics Review or Impact Assessment forms.  
• **Committee Records:** Minutes or reports from ethics committee meetings.  
• **Decision Logs:** Records of ethics approvals, rejections, or conditional clearances.  
• **Training & Awareness:** Materials on conducting or supporting ethical reviews.  
• **Transparency Reports:** Published summaries of ethical review outcomes for high-profile AI systems.  
**In short:** demonstrate that AI ethical reviews are systematic, documented, and embedded into the broader project governance lifecycle.""",
    },
    {
        "code": """AE-06""",
        "text": """How are ethical issues or breaches in AI use escalated and resolved?""",
        "explanation": """Ethical issues may arise during AI design, deployment, or operation—such as bias, unfair outcomes, or data misuse. Without a defined escalation pathway, these issues can be ignored or mishandled, eroding public trust. This question assesses whether the organisation has formal mechanisms for reporting, investigating, and resolving ethical concerns related to AI systems.

Example: A council introduces an “AI Ethics Hotline” allowing staff or the public to report concerns. Reported issues are reviewed by the AI Governance Committee, which determines corrective actions and tracks outcomes through to resolution.""",
        "domain_order": 1,
        "order": 6,
        "foundational": """Ethical issues are handled informally, with no clear reporting or resolution process.""",
        "developing": """Some escalation occurs through general complaints or HR processes but lacks AI-specific procedures.""",
        "established": """Defined processes exist for raising, investigating, and resolving AI ethical issues, with documented outcomes.""",
        "leading": """A dedicated AI ethics escalation framework enables confidential reporting, independent investigation, and transparent resolution tracking.""",
        "additional_guide": """Additional Guidance - Escalating and Resolving AI Ethical Issues

Ethical escalation frameworks promote transparency, accountability, and organisational learning. To strengthen them:  
• **Define Reporting Channels:** Establish confidential mechanisms (e.g., whistleblower line, ethics portal) for staff and stakeholders.  
• **Set Clear Procedures:** Outline steps for logging, investigating, and resolving AI-related ethical concerns.  
• **Assign Responsibility:** Appoint an AI Ethics Officer or Committee to oversee investigations.  
• **Protect Whistleblowers:** Guarantee anonymity and non-retaliation for those reporting issues.  
• **Track and Analyse Trends:** Record incidents and identify recurring ethical challenges.  
• **Report Outcomes:** Share resolution summaries with leadership and, where appropriate, the public.  
A defined escalation and resolution process demonstrates integrity, builds trust, and drives continuous improvement in ethical AI governance.""",
        "evidence_types": """To comply with **AE-06 ("Escalate and resolve AI ethical issues")**, provide documentation demonstrating structured reporting and resolution mechanisms.  
**Key Evidence Types:**  
• **Policies & Procedures:** AI Ethics Escalation or Incident Management Policy detailing reporting and investigation processes.  
• **Reporting Channels:** Evidence of hotlines, web portals, or email addresses for submitting concerns.  
• **Incident Logs:** Records of raised issues, investigations, and outcomes.  
• **Governance Records:** Committee minutes showing review and decision-making on ethics cases.  
• **Training Materials:** Awareness sessions on how to identify and report ethical issues.  
• **Transparency Reports:** Public or internal summaries of ethical issues handled and lessons learned.  
**In short:** demonstrate that AI ethical issues are reported, investigated, and resolved through formal, documented, and trusted mechanisms.""",
    },
    {
        "code": """AE-07""",
        "text": """How does the organisation promote an ethical culture and awareness around AI use?""",
        "explanation": """An ethical culture ensures responsible AI practices become part of everyday decision-making rather than a compliance afterthought. Without cultural reinforcement, even well-written policies may be ignored in practice. This question evaluates whether the organisation actively builds awareness, provides training, and fosters dialogue around ethical AI principles across all levels of staff and leadership.

Example: A council runs quarterly “Responsible AI Awareness” sessions for executives and staff, highlighting case studies on bias and accountability, and embedding ethical considerations into project planning templates.""",
        "domain_order": 1,
        "order": 7,
        "foundational": """Ethical AI awareness is minimal; staff receive no formal training or guidance.""",
        "developing": """Ethics awareness activities occur occasionally but lack consistent structure or leadership endorsement.""",
        "established": """Regular training and communications promote AI ethics, supported by management participation and internal campaigns.""",
        "leading": """Ethical AI culture is embedded enterprise-wide, with leadership modelling behaviour, mandatory training, and continuous engagement.""",
        "additional_guide": """Additional Guidance - Building an Ethical AI Culture

A strong ethical culture drives consistent, values-based decisions. To cultivate one:  
• **Provide Regular Training:** Develop ethics modules covering fairness, accountability, privacy, and responsible design.  
• **Lead by Example:** Ensure executives champion and participate in ethics activities.  
• **Create Discussion Platforms:** Hold forums or workshops to discuss ethical dilemmas in AI use.  
• **Communicate Consistently:** Share updates, success stories, and lessons learned via newsletters or intranet.  
• **Incentivise Good Practice:** Recognise teams demonstrating responsible innovation.  
• **Embed in Onboarding:** Introduce AI ethics principles to new staff.  
Embedding ethics into culture ensures awareness translates into daily practice and organisational integrity.""",
        "evidence_types": """To comply with **AE-07 ("Promote ethical culture and awareness around AI use")**, provide documentation showing structured education, communication, and engagement.  
**Key Evidence Types:**  
• **Training Records:** Logs of AI ethics workshops, e-learning, or induction programs.  
• **Communications:** Internal newsletters, intranet posts, or leadership messages promoting responsible AI.  
• **Event Materials:** Agendas and attendance lists from ethics awareness sessions or panel discussions.  
• **Policy References:** Inclusion of ethics training in staff development or compliance programs.  
• **Survey Results:** Staff feedback demonstrating awareness of AI ethical principles.  
• **Recognition Evidence:** Awards, commendations, or performance metrics reinforcing ethical behaviour.  
**In short:** demonstrate that AI ethics awareness is embedded across the organisation, supported by leadership commitment and ongoing engagement.""",
    },
    {
        "code": """AE-08""",
        "text": """How does the organisation demonstrate external transparency and public accountability in its use of AI?""",
        "explanation": """External transparency reinforces trust by allowing the public and stakeholders to understand how and why AI is used. Without open communication, organisations risk suspicion, reputational damage, and reduced community confidence. This question evaluates whether the organisation discloses information about AI systems, decisions, and impacts in a clear and accessible way.

Example: A council publishes an online “AI Register” describing each active AI system, its purpose, decision scope, ethical review status, and contact details for public inquiries.""",
        "domain_order": 1,
        "order": 8,
        "foundational": """The organisation provides little or no public information on AI use.""",
        "developing": """Limited transparency through ad-hoc media releases or project summaries.""",
        "established": """Regular public reporting describes AI systems, purposes, and governance measures.""",
        "leading": """Comprehensive transparency framework includes an AI register, ethical summaries, impact reports, and public engagement processes.""",
        "additional_guide": """Additional Guidance - Enhancing External Transparency and Accountability

Public transparency strengthens legitimacy and fosters informed dialogue about responsible AI use. To enhance it:  
• **Publish AI Information:** Maintain a public AI Register or webpage detailing system purposes, owners, and ethical safeguards.  
• **Provide Accessible Language:** Use non-technical explanations to describe decision-making and impacts.  
• **Disclose Governance Practices:** Outline how AI projects are reviewed, approved, and monitored.  
• **Engage the Public:** Conduct consultations for high-impact AI initiatives.  
• **Report Outcomes:** Include AI governance metrics and ethical review summaries in annual reports.  
• **Update Regularly:** Keep disclosures current as systems evolve.  
Transparent communication demonstrates ethical leadership and reinforces public confidence in organisational integrity.""",
        "evidence_types": """To comply with **AE-08 ("Demonstrate external transparency and public accountability in AI use")**, provide evidence showing proactive public disclosure and engagement.  
**Key Evidence Types:**  
• **AI Register:** Publicly accessible list of AI systems, their purposes, and governance details.  
• **Transparency Reports:** Annual or sustainability reports including AI ethics and risk summaries.  
• **Web Content:** Dedicated webpages explaining AI principles, governance, and impact assessments.  
• **Community Engagement Records:** Consultation materials or feedback summaries from AI-related initiatives.  
• **Media or Public Statements:** Official communications addressing AI ethics or responsible innovation.  
• **Audit or Assurance Reports:** Third-party reviews verifying completeness and accuracy of AI disclosures.  
**In short:** demonstrate that AI transparency is systematic, accessible, and fosters public accountability through consistent reporting and community engagement.""",
    },
    {
        "code": """CA-01""",
        "text": """How does the organisation track performance and improvement of its AI governance framework over time?""",
        "explanation": """Continuous performance tracking ensures AI governance remains effective and aligned with organisational goals. Without measurement, progress toward responsible AI adoption cannot be demonstrated or improved. This question assesses whether the organisation defines key performance indicators (KPIs) and metrics to monitor AI maturity, governance effectiveness, and risk mitigation outcomes.

Example: A council defines quarterly AI Governance KPIs—including policy compliance rate, model assurance completion, and fairness review coverage—and reports these to its Executive Risk Committee.""",
        "domain_order": 2,
        "order": 1,
        "foundational": """No KPIs or metrics exist for AI governance performance.""",
        "developing": """Some performance measures exist but are informal or inconsistently applied.""",
        "established": """AI governance KPIs and metrics are defined, tracked, and reported regularly to leadership.""",
        "leading": """Continuous performance measurement drives improvement, with KPIs linked to organisational outcomes and external assurance benchmarks.""",
        "additional_guide": """Additional Guidance - Tracking AI Governance Performance

Performance measurement enables data-driven improvement and accountability. To mature capability:  
• **Define KPIs:** Establish quantitative and qualitative metrics (e.g., compliance rates, audit findings, stakeholder satisfaction).  
• **Align with Objectives:** Link indicators to organisational strategy and AI ethics goals.  
• **Collect and Analyse Data:** Use dashboards or reports to monitor progress.  
• **Report Regularly:** Share results with leadership and governance bodies.  
• **Review Trends:** Identify areas for targeted improvement.  
• **Refine KPIs:** Adjust metrics as maturity evolves.  
Tracking AI governance performance ensures accountability, transparency, and measurable improvement.""",
        "evidence_types": """To comply with **CA-01 ("Track performance and improvement of AI governance")**, provide artefacts showing structured measurement and reporting.  
**Key Evidence Types:**  
• **KPI Dashboards:** AI governance or maturity performance dashboards.  
• **Performance Reports:** Quarterly or annual summaries tracking AI KPIs.  
• **Policies & Frameworks:** Documents defining AI performance metrics and responsibilities.  
• **Governance Records:** Meeting minutes discussing KPI trends and actions.  
• **Improvement Plans:** Plans or logs showing actions based on KPI outcomes.  
• **Audit Findings:** Independent reviews confirming metric accuracy and improvement tracking.  
**In short:** demonstrate that AI governance performance is measured, reported, and used to drive continuous improvement across the organisation.""",
    },
    {
        "code": """CA-02""",
        "text": """How does the organisation integrate AI governance into internal audit and assurance activities?""",
        "explanation": """Internal audit plays a key role in verifying AI compliance, effectiveness, and control maturity. Without alignment, AI risks may go unaudited or outside normal assurance cycles. This question assesses whether AI systems, governance processes, and risk controls are incorporated into internal audit planning, execution, and follow-up reviews.

Example: A council’s Internal Audit team includes AI governance within its annual audit plan, reviewing policy compliance, data integrity, and fairness testing outcomes across active AI projects.""",
        "domain_order": 2,
        "order": 2,
        "foundational": """AI risks and governance controls are not considered within internal audit activities.""",
        "developing": """Some AI-related audits occur but are informal or limited in scope.""",
        "established": """AI governance and control reviews are integrated into the internal audit program.""",
        "leading": """A structured AI assurance program ensures regular audits, independent validation, and executive oversight of AI governance outcomes.""",
        "additional_guide": """Additional Guidance - Aligning AI Governance with Internal Audit

Embedding AI within internal audit strengthens oversight and assurance. To enhance maturity:  
• **Integrate AI in Audit Planning:** Include AI systems and risks in annual audit plans.  
• **Define Audit Scope:** Cover governance, ethics, data, and model management controls.  
• **Use Specialist Skills:** Engage auditors trained in AI and data analytics.  
• **Perform Independent Reviews:** Validate fairness, accuracy, and compliance controls.  
• **Report Findings:** Share results with leadership and track remediation progress.  
• **Coordinate with Governance Teams:** Align audit outcomes with AI policy improvements.  
Systematic assurance confirms AI governance effectiveness and continuous compliance.""",
        "evidence_types": """To comply with **CA-02 ("Integrate AI governance into internal audit and assurance")**, provide documentation showing structured alignment and audit coverage.  
**Key Evidence Types:**  
• **Audit Plans:** Annual or strategic audit plans including AI systems and governance.  
• **Audit Reports:** Findings and recommendations on AI compliance or control effectiveness.  
• **Policies & Frameworks:** Internal Audit Charter or AI Assurance Framework referencing AI scope.  
• **Training Records:** Evidence of auditor upskilling in AI and data governance.  
• **Remediation Logs:** Records of corrective actions from AI-related audit findings.  
• **Executive Reports:** Briefings summarising audit outcomes and assurance trends.  
**In short:** demonstrate that AI governance is subject to systematic audit, independent validation, and continuous assurance oversight.""",
    },
    {
        "code": """CA-03""",
        "text": """How does the organisation benchmark its AI governance and practices against external standards and frameworks?""",
        "explanation": """Benchmarking enables organisations to measure their AI maturity and compliance against recognised best practices. Without external comparison, governance may stagnate or diverge from evolving standards. This question assesses whether the organisation regularly compares its AI policies and processes against frameworks such as ISO/IEC 42001, NIST AI RMF, OECD AI Principles, or Australia’s AI Ethics Principles.

Example: A council conducts an annual self-assessment against the NIST AI RMF and Australia’s Voluntary AI Safety Standard, identifying improvement priorities for integration into its AI Governance Roadmap.""",
        "domain_order": 2,
        "order": 3,
        "foundational": """No benchmarking is performed against external AI standards or frameworks.""",
        "developing": """Occasional comparisons occur but without structure or follow-through.""",
        "established": """Regular benchmarking aligns AI governance with recognised frameworks and informs improvement planning.""",
        "leading": """Continuous benchmarking integrates global standards into AI policies, supported by external validation and transparent reporting.""",
        "additional_guide": """Additional Guidance - Benchmarking AI Governance Against Standards

External benchmarking ensures alignment with recognised best practices. To strengthen maturity:  
• **Identify Relevant Frameworks:** Select those appropriate to your sector and jurisdiction (e.g., ISO 42001, NIST AI RMF).  
• **Conduct Structured Assessments:** Compare internal policies and controls against framework criteria.  
• **Engage Experts:** Use external reviewers or certification bodies for independent evaluation.  
• **Document Findings:** Record alignment status, gaps, and action plans.  
• **Integrate Results:** Update governance frameworks and training accordingly.  
• **Communicate Progress:** Report benchmarking results to leadership and stakeholders.  
Regular benchmarking demonstrates accountability, maturity, and commitment to responsible AI.""",
        "evidence_types": """To comply with **CA-03 ("Benchmark AI governance against external standards and frameworks")**, provide artefacts showing structured benchmarking and follow-up.  
**Key Evidence Types:**  
• **Benchmark Reports:** Self-assessments or external reviews comparing practices to AI standards.  
• **Gap Analyses:** Documents outlining deviations and planned remediation.  
• **Improvement Plans:** Roadmaps informed by benchmarking outcomes.  
• **Framework Mappings:** Cross-references to standards (e.g., ISO 42001 vs internal controls).  
• **Certification Evidence:** Accreditation or third-party validation reports.  
• **Governance Records:** Meeting minutes noting benchmarking findings and responses.  
**In short:** demonstrate that AI governance is regularly benchmarked against recognised external frameworks, with findings used to drive measurable improvement.""",
    },
    {
        "code": """CA-04""",
        "text": """How does the organisation engage in external review or independent assurance of its AI governance practices?""",
        "explanation": """Independent assurance provides credibility and objectivity in evaluating AI governance maturity. Without external review, blind spots or biases in internal processes may persist. This question assesses whether the organisation seeks independent validation of its AI frameworks, risk management, and compliance controls through external audits, peer reviews, or certifications.

Example: A council commissions an annual independent AI governance review by a third-party assessor to validate alignment with ISO/IEC 42001 and national AI ethics guidelines, incorporating findings into its continuous improvement roadmap.""",
        "domain_order": 2,
        "order": 4,
        "foundational": """No external assurance or independent review of AI governance is conducted.""",
        "developing": """External reviews occur occasionally but lack structure or formal follow-up.""",
        "established": """Independent reviews are conducted regularly, with findings informing policy and framework updates.""",
        "leading": """External assurance is embedded into AI governance cycles, supported by transparent reporting and certification against recognised standards.""",
        "additional_guide": """Additional Guidance - Leveraging External Assurance for AI Governance

External assurance strengthens accountability and transparency. To mature capability:  
• **Engage Independent Reviewers:** Appoint qualified auditors or AI governance experts.  
• **Define Review Scope:** Include ethics, privacy, risk, and technical performance.  
• **Schedule Regular Reviews:** Align assurance with audit or compliance cycles.  
• **Act on Findings:** Integrate recommendations into improvement plans.  
• **Report Outcomes:** Share summaries with leadership and stakeholders.  
• **Pursue Certification:** Consider recognised standards such as ISO/IEC 42001 for validation.  
External assurance demonstrates integrity, objectivity, and continual commitment to trustworthy AI governance.""",
        "evidence_types": """To comply with **CA-04 ("Engage in external review or independent assurance of AI governance")**, provide documentation showing structured external validation and review processes.  
**Key Evidence Types:**  
• **Review Reports:** Third-party AI governance or ethics assessment outcomes.  
• **Engagement Agreements:** Contracts or terms of reference for independent assessors.  
• **Certification Records:** Evidence of compliance with external standards (e.g., ISO 42001).  
• **Improvement Logs:** Actions taken in response to review findings.  
• **Audit Committee Minutes:** Records of discussions and responses to external assurance results.  
• **Public Disclosures:** Published summaries or assurance statements.  
**In short:** demonstrate that independent experts regularly review and validate AI governance effectiveness, with findings transparently integrated into improvement cycles.""",
    },
    {
        "code": """CA-05""",
        "text": """How does the organisation capture lessons learned and embed continuous learning into AI governance?""",
        "explanation": """Capturing lessons learned from AI projects, incidents, and audits ensures that mistakes are not repeated and that practices evolve over time. Without a structured learning process, insights remain siloed and improvement opportunities are lost. This question assesses whether the organisation systematically records, analyses, and integrates lessons into governance frameworks, training, and risk management processes.

Example: A council maintains an “AI Lessons Register” documenting post-project reviews, audit outcomes, and near-miss events, which feed into policy updates and staff training programs every six months.""",
        "domain_order": 2,
        "order": 5,
        "foundational": """Lessons from AI projects or incidents are not recorded or shared.""",
        "developing": """Lessons are occasionally documented but rarely acted upon or shared.""",
        "established": """Lessons learned are systematically captured and integrated into governance updates and staff training.""",
        "leading": """Continuous learning is embedded organisation-wide, supported by feedback loops, shared registers, and governance reviews driving measurable improvement.""",
        "additional_guide": """Additional Guidance - Embedding Continuous Learning in AI Governance

Learning from experience drives maturity and resilience. To strengthen capability:  
• **Establish Review Processes:** Conduct post-implementation and post-incident reviews for all AI initiatives.  
• **Maintain Lessons Registers:** Record findings, actions, and responsible owners.  
• **Share Insights:** Disseminate lessons across teams through briefings or newsletters.  
• **Integrate Findings:** Feed insights into training, policy, and risk management updates.  
• **Track Improvement:** Monitor implementation of lessons over time.  
• **Promote a Learning Culture:** Encourage open discussion of challenges and successes.  
Systematic learning transforms experience into tangible governance improvement.""",
        "evidence_types": """To comply with **CA-05 ("Capture lessons learned and embed continuous learning into AI governance")**, provide artefacts showing structured review and improvement activities.  
**Key Evidence Types:**  
• **Lessons Learned Registers:** Centralised documentation of findings and actions.  
• **Post-Implementation Reviews:** Reports summarising project outcomes and recommendations.  
• **Audit and Incident Reviews:** Records capturing issues, lessons, and corrective measures.  
• **Training Updates:** Evidence of revised learning materials or refreshed content.  
• **Policy Amendments:** Documented changes informed by captured lessons.  
• **Meeting Minutes:** Governance discussions on lessons integration and improvement tracking.  
**In short:** demonstrate that insights from AI operations are systematically captured, shared, and embedded into governance and capability improvement processes.""",
    },
    {
        "code": """CA-06""",
        "text": """How does the organisation track external trends and emerging best practices in AI governance?""",
        "explanation": """AI technologies and governance expectations evolve rapidly. Without monitoring external trends, the organisation risks falling behind regulatory, ethical, or technological developments. This question assesses whether the organisation actively tracks emerging best practices, research, and standards to adapt its AI governance framework and maintain leadership in responsible AI adoption.

Example: A council’s AI Governance Team subscribes to government and standards body updates, participates in national AI working groups, and incorporates emerging global best practices into policy reviews and staff briefings.""",
        "domain_order": 2,
        "order": 6,
        "foundational": """The organisation does not monitor external AI governance or industry developments.""",
        "developing": """Some monitoring occurs but is informal and not integrated into policy updates.""",
        "established": """Emerging trends and best practices are regularly reviewed and used to inform AI governance improvements.""",
        "leading": """A formal process continuously scans, evaluates, and integrates emerging global AI best practices, standards, and research into policy, training, and strategy.""",
        "additional_guide": """Additional Guidance - Tracking Emerging AI Governance Trends

Staying informed ensures governance frameworks remain current and credible. To strengthen maturity:  
• **Monitor Key Sources:** Follow updates from standards bodies (ISO, IEEE, NIST) and regulators.  
• **Engage in Networks:** Participate in professional forums and working groups.  
• **Review Regularly:** Conduct quarterly or biannual horizon scans of new trends.  
• **Document Findings:** Summarise insights and implications for the organisation.  
• **Update Frameworks:** Incorporate relevant developments into governance and training.  
• **Communicate Insights:** Share updates with leadership and key stakeholders.  
Tracking trends supports agility, innovation, and compliance in a fast-changing AI landscape.""",
        "evidence_types": """To comply with **CA-06 ("Track external trends and emerging best practices in AI governance")**, provide artefacts showing structured horizon scanning and policy adaptation.  
**Key Evidence Types:**  
• **Trend Reports:** Internal summaries or external bulletins highlighting new AI developments.  
• **Membership Records:** Participation in AI governance or ethics networks.  
• **Meeting Minutes:** Records of reviews discussing new trends or standards.  
• **Policy Updates:** Evidence of governance changes triggered by emerging practices.  
• **Training Materials:** Revised content reflecting new frameworks or guidance.  
• **Stakeholder Briefings:** Communications outlining external developments and organisational responses.  
**In short:** demonstrate that external AI trends are actively monitored, evaluated, and integrated into organisational policy and governance practices.""",
    },
    {
        "code": """CA-07""",
        "text": """How does the organisation use metrics, benchmarking, and feedback to drive continuous improvement in AI governance?""",
        "explanation": """Metrics and benchmarking translate insights into measurable progress. Without defined indicators and feedback loops, the organisation cannot assess whether improvements are effective or sustained. This question evaluates whether the organisation uses quantitative and qualitative measures—such as KPIs, benchmarking scores, and stakeholder feedback—to guide strategic enhancements in AI governance, ethics, and compliance.

Example: A council compiles quarterly AI performance dashboards, combining KPI trends, user feedback, and benchmarking results against ISO 42001 principles to identify priority areas for policy refinement and training.""",
        "domain_order": 2,
        "order": 7,
        "foundational": """No metrics or feedback are used to measure AI governance improvement.""",
        "developing": """Some metrics or feedback mechanisms exist but are inconsistently applied.""",
        "established": """Regular metrics, feedback, and benchmarking are used to inform AI governance improvement plans.""",
        "leading": """A data-driven improvement program integrates metrics, feedback, and benchmarking into governance dashboards and continuous enhancement cycles.""",
        "additional_guide": """Additional Guidance - Leveraging Metrics and Feedback for Improvement

Measurement ensures improvement efforts are targeted and evidence-based. To mature practices:  
• **Define Improvement Metrics:** Include compliance scores, incident trends, or audit closure rates.  
• **Integrate Feedback Channels:** Collect insights from staff, users, and external stakeholders.  
• **Use Dashboards:** Visualise trends to support decision-making.  
• **Benchmark Performance:** Compare results against peers or recognised frameworks.  
• **Link to Planning:** Align findings with AI strategy and resource allocation.  
• **Report Outcomes:** Share improvement progress transparently with leadership.  
Structured measurement drives accountability and demonstrable maturity growth.""",
        "evidence_types": """To comply with **CA-07 ("Use metrics, benchmarking, and feedback to drive continuous improvement")**, provide artefacts showing systematic performance tracking and feedback integration.  
**Key Evidence Types:**  
• **Governance Dashboards:** Reports visualising KPI and trend data.  
• **Benchmarking Reports:** Comparisons against internal targets or external standards.  
• **Feedback Records:** Surveys, focus-group results, or stakeholder submissions.  
• **Improvement Logs:** Actions and outcomes linked to performance insights.  
• **Meeting Minutes:** Leadership reviews discussing KPI trends and feedback responses.  
• **Policy Updates:** Documentation of improvements derived from metric analysis.  
**In short:** demonstrate that AI governance improvement is guided by defined metrics, ongoing benchmarking, and structured feedback from all relevant stakeholders.""",
    },
    {
        "code": """CA-08""",
        "text": """How does the organisation maintain continuous assurance through review, re-assessment, and re-certification of AI governance?""",
        "explanation": """Continuous assurance ensures that AI governance remains effective as systems evolve and new regulations emerge. Without structured re-assessment, previously certified or compliant frameworks may degrade over time. This question evaluates whether the organisation conducts periodic reviews, internal and external re-assessments, and formal re-certification to sustain trust and accountability in AI operations.

Example: A council conducts biennial AI Governance re-assessments using internal audit tools and engages an external assessor every three years to validate continued compliance with ISO/IEC 42001 and national AI assurance frameworks.""",
        "domain_order": 2,
        "order": 8,
        "foundational": """No ongoing assurance or re-assessment of AI governance occurs after initial implementation.""",
        "developing": """Periodic reviews occur, but processes for re-assessment or certification are informal or irregular.""",
        "established": """Regular internal reviews and re-assessments verify AI governance effectiveness and compliance.""",
        "leading": """Continuous assurance integrates internal monitoring, scheduled re-certification, and independent verification of ongoing AI governance maturity.""",
        "additional_guide": """Additional Guidance - Maintaining Continuous AI Assurance

Continuous assurance safeguards long-term reliability and compliance. To enhance maturity:  
• **Schedule Regular Reviews:** Conduct internal re-assessments at least annually.  
• **Use Standardised Frameworks:** Apply recognised models such as ISO 42001, NIST AI RMF, or equivalent.  
• **Engage Independent Validators:** Seek third-party or peer verification.  
• **Track Certification Status:** Maintain evidence of compliance renewals and audit results.  
• **Integrate Results:** Use findings to update governance frameworks and improvement plans.  
• **Report to Leadership:** Ensure executives review and endorse re-assessment outcomes.  
Structured, repeatable assurance cycles demonstrate enduring accountability and trustworthiness in AI governance.""",
        "evidence_types": """To comply with **CA-08 ("Maintain continuous assurance through review, re-assessment, and re-certification of AI governance")**, provide artefacts showing sustained verification and re-assessment activities.  
**Key Evidence Types:**  
• **Re-Assessment Reports:** Documentation of periodic internal or external reviews.  
• **Certification Records:** Current ISO 42001 or equivalent assurance certificates.  
• **Audit Schedules:** Calendars outlining review and re-certification cycles.  
• **Improvement Logs:** Records showing updates following assurance reviews.  
• **Governance Committee Minutes:** Evidence of oversight and endorsement of results.  
• **External Validation Reports:** Independent verifier findings confirming continued compliance.  
**In short:** demonstrate that AI governance effectiveness is continuously validated through structured internal and external assurance mechanisms.""",
    },
    {
        "code": """CC-01""",
        "text": """How does the organisation promote awareness and understanding of AI opportunities, risks, and governance across staff?""",
        "explanation": """AI awareness enables employees to recognise both the benefits and challenges of responsible AI adoption. Without organisational understanding, staff may misuse AI tools, overlook risks, or resist innovation. This question assesses whether the organisation promotes AI literacy through education, communication, and engagement initiatives across all levels.

Example: A council conducts quarterly “AI Awareness Sessions” for staff and managers, explaining key AI concepts, organisational policies, and examples of ethical and unsafe AI practices.""",
        "domain_order": 3,
        "order": 1,
        "foundational": """Little or no awareness of AI governance, opportunities, or risks across staff.""",
        "developing": """Basic awareness exists through informal discussions or isolated communications.""",
        "established": """Structured awareness programs communicate AI principles, policies, and governance requirements.""",
        "leading": """AI literacy and governance awareness are embedded enterprise-wide through campaigns, leadership endorsement, and ongoing communication.""",
        "additional_guide": """Additional Guidance - Promoting AI Awareness and Understanding

AI awareness forms the foundation for responsible adoption. To strengthen maturity:  
• **Develop Awareness Campaigns:** Share accessible materials explaining AI purpose, governance, and risks.  
• **Engage Leadership:** Ensure executives model and promote responsible AI use.  
• **Use Multiple Channels:** Leverage intranet articles, videos, and learning sessions.  
• **Connect to Policy:** Explain how awareness links to AI ethics and compliance requirements.  
• **Assess Understanding:** Survey staff to measure awareness progress.  
• **Refresh Regularly:** Update messaging as technologies and regulations evolve.  
An informed workforce supports safe, transparent, and value-aligned AI implementation.""",
        "evidence_types": """To comply with **CC-01 ("Promote awareness and understanding of AI opportunities, risks, and governance")**, provide documentation showing structured communication and awareness efforts.  
**Key Evidence Types:**  
• **Communication Plans:** AI awareness or literacy campaign materials.  
• **Training Presentations:** Slide decks or recordings from awareness sessions.  
• **Intranet Content:** Articles or newsletters explaining responsible AI principles.  
• **Survey Results:** Assessments measuring staff understanding of AI governance.  
• **Leadership Endorsements:** Statements or videos supporting responsible AI use.  
• **Event Records:** Attendance logs or feedback summaries from awareness activities.  
**In short:** demonstrate that AI awareness and understanding are actively promoted through structured, ongoing communication and leadership engagement.""",
    },
    {
        "code": """CC-02""",
        "text": """How does the organisation provide staff training and upskilling to support responsible AI adoption?""",
        "explanation": """Building AI capability ensures that employees can use, manage, and oversee AI technologies safely and effectively. Without targeted training, staff may lack the knowledge to identify risks, interpret AI outputs, or apply governance requirements. This question assesses whether the organisation delivers structured training and upskilling programs that develop technical, ethical, and operational AI competencies.

Example: A council delivers a tiered AI training program: introductory awareness for all employees, advanced technical modules for data teams, and governance workshops for leadership and risk staff.""",
        "domain_order": 3,
        "order": 2,
        "foundational": """No formal AI-related training or skill development programs exist.""",
        "developing": """Some AI or digital skills training occurs but is ad hoc or unaligned with governance objectives.""",
        "established": """Structured AI training programs address technical, ethical, and governance skills across key staff groups.""",
        "leading": """Organisation-wide AI upskilling integrates into professional development plans, supported by leadership and continuous learning pathways.""",
        "additional_guide": """Additional Guidance - Developing AI Training and Upskilling Programs

Upskilling empowers staff to implement and manage AI responsibly. To enhance capability:  
• **Define Learning Objectives:** Align training to organisational AI strategy and risk appetite.  
• **Offer Tiered Training:** Provide tailored modules for executives, practitioners, and general staff.  
• **Include Ethics and Governance:** Emphasise bias, fairness, and responsible AI decision-making.  
• **Leverage Partnerships:** Collaborate with universities or industry for specialised learning.  
• **Track Participation:** Maintain training records and completion rates.  
• **Foster Lifelong Learning:** Refresh content regularly as technologies evolve.  
Structured training develops confident, competent teams ready for responsible AI adoption.""",
        "evidence_types": """To comply with **CC-02 ("Provide staff training and upskilling for responsible AI adoption")**, provide artefacts showing structured learning programs and participation.  
**Key Evidence Types:**  
• **Training Plans:** AI capability development strategy or curriculum outline.  
• **Course Materials:** Presentation decks, e-learning modules, or workshop content.  
• **Attendance Records:** Logs showing staff participation and completion rates.  
• **Certification Evidence:** Records of achieved AI, ethics, or governance credentials.  
• **Evaluation Reports:** Feedback or assessments of training effectiveness.  
• **Budget & Planning Documents:** Evidence of ongoing investment in AI capability-building.  
**In short:** demonstrate that structured, role-specific training equips staff with the knowledge and skills needed for responsible AI development and oversight.""",
    },
    {
        "code": """CC-03""",
        "text": """How does the organisation embed ethical AI competence and responsible decision-making skills across staff?""",
        "explanation": """Embedding ethical competence ensures employees can recognise and address ethical challenges in AI use. Without this, decisions may prioritise efficiency or innovation over fairness, transparency, or accountability. This question assesses whether the organisation integrates ethical reasoning, governance awareness, and scenario-based learning into staff training and decision-making processes.

Example: A council conducts interactive workshops where staff analyse real AI case studies involving bias, privacy, and explainability challenges to develop critical thinking and ethical decision-making skills.""",
        "domain_order": 3,
        "order": 3,
        "foundational": """Ethical considerations in AI decision-making are absent or left to individual discretion.""",
        "developing": """Some staff receive ethics-related training, but content is generic or inconsistent.""",
        "established": """Ethical AI principles are embedded into staff training, supported by role-specific guidance and decision frameworks.""",
        "leading": """Ethical competence is an organisational capability, reinforced through continuous learning, leadership modelling, and AI ethics performance measures.""",
        "additional_guide": """Additional Guidance - Developing Ethical AI Competence

Ethical decision-making builds accountability and public trust. To strengthen capability:  
• **Provide Scenario-Based Training:** Use practical examples to explore ethical dilemmas in AI use.  
• **Embed Ethical Frameworks:** Reference organisational AI ethics or governance policies.  
• **Promote Reflective Practice:** Encourage teams to assess decisions through fairness and transparency lenses.  
• **Integrate into Performance Goals:** Include ethical competence in staff KPIs and appraisals.  
• **Foster Leadership Example:** Senior leaders model ethical behaviour and reinforce governance principles.  
• **Review Regularly:** Refresh ethical training based on new laws, technologies, and lessons learned.  
Embedding ethical competence transforms responsible AI from theory into daily practice.""",
        "evidence_types": """To comply with **CC-03 ("Embed ethical AI competence and decision-making skills")**, provide documentation showing structured ethics education and integration into governance.  
**Key Evidence Types:**  
• **Training Materials:** AI ethics or responsible decision-making course content.  
• **Attendance Logs:** Records of staff participation in ethics workshops.  
• **Policies & Frameworks:** AI Ethics Policy or Code of Conduct referencing AI use.  
• **Decision Frameworks:** Tools or checklists guiding ethical AI decisions.  
• **Performance Records:** KPIs or appraisal templates including ethical conduct.  
• **Leadership Communications:** Evidence of executives promoting ethical AI principles.  
**In short:** demonstrate that ethical reasoning and decision-making are trained, practised, and reinforced organisation-wide as core AI capabilities.""",
    },
    {
        "code": """CC-04""",
        "text": """How does the organisation’s leadership foster a culture of responsible AI innovation and governance?""",
        "explanation": """Leadership plays a critical role in shaping organisational culture around AI use. Without visible support and clear messaging, responsible AI practices may be viewed as optional rather than essential. This question assesses whether leaders actively promote ethical AI adoption, model responsible behaviour, and integrate governance into innovation strategies.

Example: A council’s executive team publicly endorses its Responsible AI Charter, regularly communicates progress on AI governance initiatives, and recognises staff who demonstrate ethical innovation practices.""",
        "domain_order": 3,
        "order": 4,
        "foundational": """Leadership involvement in AI governance or culture-building is minimal.""",
        "developing": """Some leaders support AI initiatives, but governance messaging is inconsistent.""",
        "established": """Leadership actively endorses responsible AI principles and integrates them into business planning.""",
        "leading": """Responsible AI culture is driven from the top through consistent messaging, accountability, and recognition of ethical innovation.""",
        "additional_guide": """Additional Guidance - Fostering Leadership in Responsible AI

Leadership commitment ensures responsible AI becomes embedded in organisational values. To enhance maturity:  
• **Communicate Vision:** Leaders articulate the importance of ethical and transparent AI.  
• **Model Behaviour:** Executives demonstrate compliance with AI policies and principles.  
• **Embed in Strategy:** Integrate AI governance objectives into business and innovation plans.  
• **Recognise Good Practice:** Reward teams applying responsible innovation.  
• **Maintain Accountability:** Link leadership KPIs to AI governance outcomes.  
• **Engage Externally:** Represent the organisation in AI ethics and governance forums.  
Strong leadership signals that responsible AI is both a cultural and strategic priority.""",
        "evidence_types": """To comply with **CC-04 ("Foster a culture of responsible AI innovation and governance")**, provide artefacts showing visible and sustained leadership engagement.  
**Key Evidence Types:**  
• **Leadership Statements:** Communications or speeches endorsing responsible AI practices.  
• **Strategic Plans:** Documents integrating AI ethics and governance into organisational objectives.  
• **Governance Records:** Executive meeting minutes discussing AI accountability.  
• **Recognition Programs:** Awards or acknowledgements for ethical AI innovation.  
• **KPIs or Scorecards:** Leadership performance measures linked to AI culture outcomes.  
• **Public Engagements:** Participation in AI ethics panels, conferences, or community outreach.  
**In short:** demonstrate that leaders actively champion, communicate, and reinforce a culture of responsible and ethical AI adoption across the organisation.""",
    },
    {
        "code": """CC-05""",
        "text": """How does the organisation encourage cross-functional collaboration and knowledge sharing in AI projects?""",
        "explanation": """Effective AI governance requires collaboration across technical, operational, legal, and ethical domains. Without structured communication and shared learning, teams may operate in silos, increasing risks of bias, duplication, or misalignment. This question assesses whether the organisation fosters collaboration and knowledge exchange between diverse disciplines involved in AI development, deployment, and oversight.

Example: A council’s AI Governance Committee includes representatives from IT, Legal, Risk, and Community Engagement who meet monthly to share insights, review projects, and align on governance priorities.""",
        "domain_order": 3,
        "order": 5,
        "foundational": """AI projects operate in isolation with minimal collaboration or knowledge exchange.""",
        "developing": """Some cross-functional communication occurs but lacks structure or continuity.""",
        "established": """Formal collaboration mechanisms, committees, and documentation enable regular AI knowledge sharing.""",
        "leading": """Collaboration is embedded in AI governance, supported by shared platforms, multi-disciplinary teams, and continuous learning cycles.""",
        "additional_guide": """Additional Guidance - Building Cross-Functional Collaboration in AI

Collaboration promotes balanced decision-making and shared accountability. To strengthen practices:  
• **Establish Governance Forums:** Include diverse disciplines in AI oversight and project planning.  
• **Create Shared Repositories:** Centralise documentation, datasets, and lessons learned.  
• **Encourage Knowledge Exchange:** Host cross-team workshops or "AI learning labs."  
• **Document Decisions:** Record multi-disciplinary input and agreed actions.  
• **Reward Collaboration:** Recognise teams that demonstrate cross-functional innovation.  
• **Use Collaboration Tools:** Support shared dashboards and digital platforms for AI tracking.  
Cross-functional collaboration drives better outcomes and stronger governance alignment.""",
        "evidence_types": """To comply with **CC-05 ("Encourage cross-functional collaboration and knowledge sharing in AI projects")**, provide artefacts showing structured coordination and information-sharing practices.  
**Key Evidence Types:**  
• **Governance Committee Records:** Meeting minutes or membership lists from multi-disciplinary AI bodies.  
• **Collaboration Platforms:** Evidence of shared AI documentation or repositories.  
• **Workshop Materials:** Agendas or attendance logs from cross-functional sessions.  
• **Policies & Frameworks:** Collaboration or governance documents mandating cross-team involvement.  
• **Communication Records:** Newsletters, reports, or intranet posts sharing AI updates.  
• **Recognition Programs:** Awards or acknowledgements for collaborative innovation.  
**In short:** demonstrate that AI development and oversight are inclusive, collaborative, and supported by mechanisms for continuous knowledge exchange across disciplines.""",
    },
    {
        "code": """CC-06""",
        "text": """How does the organisation foster innovation and responsible experimentation in AI?""",
        "explanation": """A culture of responsible experimentation encourages innovation while managing risk. Without structured guidance, staff may either avoid using AI due to uncertainty or adopt it recklessly without proper oversight. This question assesses whether the organisation provides safe, supported environments—such as sandboxes or pilot frameworks—for testing AI ideas in alignment with governance and ethical standards.

Example: A council establishes an “AI Innovation Sandbox” where teams can experiment with AI tools under governance oversight, applying clear ethical, privacy, and safety guardrails before production deployment.""",
        "domain_order": 3,
        "order": 6,
        "foundational": """AI experimentation occurs informally, without structure or governance oversight.""",
        "developing": """Some pilot projects are conducted, but risk management and documentation are limited.""",
        "established": """Responsible AI experimentation follows structured processes, with defined approval, monitoring, and review.""",
        "leading": """Innovation is actively encouraged through supported sandboxes, ethical review, and governance-aligned experimentation frameworks.""",
        "additional_guide": """Additional Guidance - Encouraging Responsible AI Innovation

Responsible experimentation enables innovation with assurance. To mature practices:  
• **Create Safe Test Environments:** Establish controlled sandboxes for AI development and piloting.  
• **Define Approval Processes:** Require ethical, risk, and privacy review before pilots.  
• **Support Iterative Learning:** Encourage experimentation that informs governance improvements.  
• **Provide Resources:** Allocate budget and technical infrastructure for testing.  
• **Recognise Successes:** Celebrate responsible innovation and knowledge gained from experimentation.  
• **Integrate Lessons Learned:** Apply insights to future policies and deployments.  
Embedding responsible experimentation nurtures innovation while maintaining trust and compliance.""",
        "evidence_types": """To comply with **CC-06 ("Foster innovation and responsible experimentation in AI")**, provide artefacts showing structured, governed innovation processes.  
**Key Evidence Types:**  
• **Innovation Frameworks:** Policies defining experimentation, pilot approval, and governance guardrails.  
• **Sandbox Records:** Documentation of AI test environments, participants, and results.  
• **Ethics Review Logs:** Records of ethical or risk assessments for pilot projects.  
• **Project Reports:** Evaluation of lessons learned and scalability outcomes.  
• **Budget and Planning Documents:** Evidence of investment in AI innovation initiatives.  
• **Recognition Materials:** Awards or communications highlighting responsible AI innovation.  
**In short:** demonstrate that AI experimentation is encouraged, supported, and conducted safely within defined ethical and governance boundaries.""",
    },
    {
        "code": """CC-07""",
        "text": """How does the organisation measure AI capability and workforce readiness for responsible AI adoption?""",
        "explanation": """Understanding workforce capability helps identify skill gaps and readiness for responsible AI implementation. Without measurement, organisations may overestimate their preparedness or underinvest in training and governance. This question assesses whether the organisation evaluates AI literacy, technical competence, and governance awareness to guide capability development.

Example: A council conducts an annual “AI Readiness Survey” across all departments, assessing AI knowledge, ethical awareness, and confidence in applying governance principles, then tailors training and resource plans accordingly.""",
        "domain_order": 3,
        "order": 7,
        "foundational": """AI capability and readiness are not assessed or measured.""",
        "developing": """Some skill assessments occur informally or within limited teams.""",
        "established": """Regular workforce assessments identify AI capability gaps and inform training and resourcing plans.""",
        "leading": """Continuous AI capability monitoring integrates with HR analytics and organisational planning to drive targeted upskilling and governance improvement.""",
        "additional_guide": """Additional Guidance - Measuring AI Capability and Readiness

Capability assessment supports data-driven workforce planning. To strengthen maturity:  
• **Define Competency Frameworks:** Identify key skills across technical, governance, and ethical domains.  
• **Conduct Assessments:** Use surveys, self-assessments, or skills matrices to gauge readiness.  
• **Analyse Gaps:** Compare results to desired AI maturity benchmarks.  
• **Integrate with HR Planning:** Align results with professional development and recruitment.  
• **Track Over Time:** Measure progress annually to evaluate improvement.  
• **Report Findings:** Share insights with leadership to prioritise investment.  
Systematic measurement ensures the workforce is equipped and ready for responsible AI adoption.""",
        "evidence_types": """To comply with **CC-07 ("Measure AI capability and workforce readiness")**, provide artefacts showing structured assessments and analysis processes.  
**Key Evidence Types:**  
• **Readiness Assessments:** Results of AI literacy or capability surveys.  
• **Competency Frameworks:** Documents outlining required AI skills and governance competencies.  
• **Gap Analyses:** Reports identifying workforce strengths and weaknesses.  
• **Training Plans:** Development roadmaps based on capability assessment findings.  
• **HR Integration Records:** Evidence linking assessment results to workforce planning.  
• **Progress Reports:** Year-on-year comparisons showing capability improvement.  
**In short:** demonstrate that AI capability and readiness are regularly measured, analysed, and used to inform workforce development strategies.""",
    },
    {
        "code": """CC-08""",
        "text": """How does the organisation embed continuous learning and AI literacy across the workforce?""",
        "explanation": """Continuous learning ensures staff stay informed about evolving AI technologies, ethical standards, and governance practices. Without sustained education, knowledge quickly becomes outdated, limiting innovation and compliance readiness. This question assesses whether the organisation promotes lifelong AI learning through structured programs, accessible resources, and ongoing reinforcement of responsible AI principles.

Example: A council maintains an online “AI Learning Hub” offering short courses, policy updates, and real-world case studies. Staff are encouraged to complete annual AI literacy refreshers as part of mandatory professional development.""",
        "domain_order": 3,
        "order": 8,
        "foundational": """AI learning is ad hoc and dependent on individual interest.""",
        "developing": """Some ongoing learning occurs, but opportunities are inconsistent or untracked.""",
        "established": """Continuous learning is structured through regular training, digital learning platforms, and refresher courses.""",
        "leading": """Organisation-wide AI literacy is embedded into professional development, supported by adaptive learning and leadership-driven knowledge-sharing initiatives.""",
        "additional_guide": """Additional Guidance - Embedding Continuous AI Learning

Ongoing education supports safe and informed AI adoption. To strengthen maturity:  
• **Establish Learning Platforms:** Provide access to e-learning, webinars, and knowledge resources.  
• **Integrate with Career Development:** Include AI literacy in professional growth plans.  
• **Encourage Peer Learning:** Promote communities of practice and knowledge-sharing forums.  
• **Update Content Regularly:** Reflect new legislation, technologies, and best practices.  
• **Track Participation:** Monitor engagement and completion rates.  
• **Involve Leadership:** Have executives champion and participate in learning initiatives.  
Continuous AI education ensures organisational agility and resilience in an evolving digital environment.""",
        "evidence_types": """To comply with **CC-08 ("Embed continuous learning and AI literacy across the workforce")**, provide documentation demonstrating structured, ongoing learning initiatives.  
**Key Evidence Types:**  
• **Learning Platforms:** Screenshots or descriptions of AI learning portals and training modules.  
• **Training Records:** Logs showing participation in refresher or micro-learning courses.  
• **Professional Development Plans:** Integration of AI learning into HR or performance frameworks.  
• **Content Updates:** Evidence of regularly refreshed materials and new learning topics.  
• **Peer Learning Evidence:** Meeting notes or communications from communities of practice.  
• **Leadership Endorsement:** Executive communications promoting continuous AI learning.  
**In short:** demonstrate that AI literacy and ongoing education are embedded in professional development, supported by leadership and continuous improvement.""",
    },
    {
        "code": """DS-01""",
        "text": """How does the organisation ensure data used for AI is accurate, complete, and fit for purpose?""",
        "explanation": """AI systems depend on high-quality data. Inaccurate, incomplete, or poorly curated datasets can lead to flawed predictions, unfair outcomes, and reputational harm. This question assesses whether the organisation applies structured processes to validate, cleanse, and monitor data before it is used for AI development or decision-making.

Example: A council’s Data Governance Team implements automated validation scripts and manual quality checks before sharing datasets with AI developers, ensuring accuracy, completeness, and relevance to the intended use case.""",
        "domain_order": 4,
        "order": 1,
        "foundational": """Data quality is not systematically assessed; errors or gaps are discovered post-deployment.""",
        "developing": """Some quality checks exist but are manual or inconsistently applied.""",
        "established": """Data validation, cleansing, and review processes ensure datasets meet defined quality standards.""",
        "leading": """Comprehensive data-quality management uses automated controls, continuous monitoring, and documented data-fitness criteria.""",
        "additional_guide": """Additional Guidance - Maintaining Data Quality for AI

Reliable AI outcomes depend on rigorous data-quality assurance. To strengthen governance:  
• **Define Quality Criteria:** Set thresholds for accuracy, completeness, timeliness, and consistency.  
• **Implement Validation Rules:** Apply automated checks and anomaly detection before ingestion.  
• **Maintain Metadata:** Document data provenance, transformation steps, and quality metrics.  
• **Assign Data Stewards:** Give responsibility for verifying and approving datasets used in AI models.  
• **Review Regularly:** Audit data sources and refresh outdated or low-quality data.  
• **Monitor Continuously:** Use dashboards or alerts to detect data drift or integrity issues.  
Consistent validation processes reduce bias, enhance reliability, and underpin defensible AI decision-making.""",
        "evidence_types": """To comply with **DS-01 ("Ensure AI data is accurate, complete, and fit for purpose")**, provide documentation showing structured data-quality management.  
**Key Evidence Types:**  
• **Policies & Standards:** Data-Quality Policy or AI Data Governance Framework defining quality requirements.  
• **Quality Reports:** Logs of validation checks, error rates, and remediation actions.  
• **Metadata Repositories:** Records describing data lineage, source verification, and transformation steps.  
• **Audit Findings:** Internal reviews of dataset accuracy or completeness.  
• **Stewardship Records:** Data steward approvals or sign-off forms confirming dataset readiness.  
• **Monitoring Dashboards:** Automated alerts or reports showing continuous data-quality tracking.  
**In short:** demonstrate that AI datasets are verified, traceable, and maintained under a controlled quality-assurance process before use.""",
    },
    {
        "code": """DS-02""",
        "text": """How are data governance roles and responsibilities defined for AI-related activities?""",
        "explanation": """Clear data governance roles ensure accountability and consistency across all AI projects. Without defined ownership, data can be mismanaged, creating security gaps, quality issues, and compliance risks. This question assesses whether the organisation has assigned formal responsibilities for managing, approving, and protecting data used in AI systems.

Example: A council designates Data Stewards within each department responsible for dataset quality and security. The Chief Data Officer oversees alignment with organisational policies and chairs the Data Governance Committee.""",
        "domain_order": 4,
        "order": 2,
        "foundational": """Data management responsibilities are unclear or distributed informally.""",
        "developing": """Some roles exist but are inconsistently defined or not linked to AI governance.""",
        "established": """Formal data governance roles and responsibilities are defined, assigned, and communicated across departments.""",
        "leading": """Data governance roles are enterprise-wide, supported by clear accountability frameworks, charters, and performance measures.""",
        "additional_guide": """Additional Guidance - Defining Data Governance Roles

Defined roles ensure accountability and efficient data stewardship. To mature your approach:  
• **Establish Data Governance Structure:** Formally appoint a Chief Data Officer or equivalent role.  
• **Assign Data Stewards:** Designate departmental stewards responsible for data accuracy, security, and access control.  
• **Create Supporting Committees:** Include cross-functional representatives to oversee AI data practices.  
• **Document Responsibilities:** Embed data-related duties in role descriptions and governance charters.  
• **Integrate with AI Governance:** Ensure coordination between AI, risk, and data governance teams.  
• **Monitor Performance:** Use KPIs to evaluate stewardship effectiveness and compliance with data standards.  
Defined, empowered roles create clear accountability and strengthen overall data integrity and trustworthiness.""",
        "evidence_types": """To comply with **DS-02 ("Define data governance roles and responsibilities for AI")**, provide documentation showing that ownership and stewardship are formally assigned and operational.  
**Key Evidence Types:**  
• **Policies & Frameworks:** Data Governance Policy or Charter defining roles, responsibilities, and reporting lines.  
• **Organisational Charts:** Visuals identifying data-related roles (e.g., Chief Data Officer, Data Steward, Custodian).  
• **Role Descriptions:** Position statements including data-governance or AI-related accountabilities.  
• **Committee Terms of Reference:** Evidence of cross-functional data governance or AI-data oversight bodies.  
• **Meeting Minutes:** Records of governance discussions or approvals related to data stewardship.  
• **Performance Metrics:** Reports tracking compliance with data ownership and quality obligations.  
**In short:** demonstrate that data governance roles are clearly defined, assigned, and actively managed across all AI-related activities.""",
    },
    {
        "code": """DS-03""",
        "text": """How does the organisation classify and manage data sensitivity for AI systems?""",
        "explanation": """Data classification ensures that sensitive or confidential information used in AI systems is handled appropriately. Without clear classification rules, AI projects may expose personal or restricted data to unauthorised access or misuse. This question assesses whether the organisation applies consistent data classification and handling procedures aligned with legal, privacy, and information security standards.

Example: A council applies a four-tier data classification scheme—Public, Internal, Sensitive, and Confidential—and enforces corresponding access and encryption controls for all AI datasets.""",
        "domain_order": 4,
        "order": 3,
        "foundational": """Data used for AI is not classified or handled according to sensitivity.""",
        "developing": """Some classification occurs, but practices vary by project or department.""",
        "established": """Formal classification levels and handling rules apply consistently to AI data.""",
        "leading": """Classification and handling controls are automated, continuously enforced, and aligned with national privacy and security standards.""",
        "additional_guide": """Additional Guidance - Classifying and Managing Data Sensitivity

Accurate data classification protects confidentiality and supports compliance. To mature practices:  
• **Define Classification Levels:** Establish categories (e.g., Public, Internal, Sensitive, Confidential).  
• **Align with Standards:** Base classifications on frameworks such as ISM, ISO 27001, or organisational information-security policies.  
• **Implement Handling Procedures:** Define storage, transmission, retention, and disposal requirements per classification level.  
• **Automate Controls:** Use metadata tagging, encryption, and access-control automation where possible.  
• **Educate Staff:** Train personnel on identifying and protecting sensitive data.  
• **Monitor Compliance:** Audit AI projects regularly for correct classification and data handling.  
Consistent classification ensures sensitive data used in AI systems is safeguarded from unauthorised access or misuse.""",
        "evidence_types": """To comply with **DS-03 ("Classify and manage data sensitivity for AI systems")**, provide artefacts showing formal classification and handling processes.  
**Key Evidence Types:**  
• **Policies & Standards:** Information Classification Policy or Data Handling Guidelines referencing AI datasets.  
• **Classification Registers:** Records of datasets labelled by sensitivity level.  
• **Technical Controls:** Evidence of encryption, access restrictions, or data-tagging automation.  
• **Training Records:** Materials or attendance logs for data classification awareness sessions.  
• **Audit Findings:** Reports validating classification accuracy and control enforcement.  
• **Procedural Documents:** Instructions defining retention, destruction, or anonymisation based on sensitivity.  
**In short:** demonstrate that AI datasets are classified, protected, and managed according to their confidentiality and regulatory requirements.""",
    },
    {
        "code": """DS-04""",
        "text": """How does the organisation control and authorise access to data used in AI systems?""",
        "explanation": """Access control ensures that only authorised personnel can view or modify data used in AI models. Without strict authorisation measures, sensitive information can be exposed or manipulated, increasing privacy, security, and compliance risks. This question assesses whether data access for AI development and use is governed by role-based permissions, authentication controls, and monitoring processes.

Example: A council enforces role-based access control (RBAC) for AI datasets, requiring multi-factor authentication and periodic access reviews by data stewards and system owners.""",
        "domain_order": 4,
        "order": 4,
        "foundational": """AI data access is uncontrolled or relies on ad-hoc permissions.""",
        "developing": """Access controls exist but are inconsistently applied or not regularly reviewed.""",
        "established": """Role-based access and approval processes govern all AI data access, supported by authentication and audit logs.""",
        "leading": """Automated access management with least-privilege enforcement, continuous monitoring, and integration with identity governance frameworks.""",
        "additional_guide": """Additional Guidance - Enforcing AI Data Access Controls

Strong access governance reduces the risk of data leaks or misuse. To improve maturity:  
• **Apply Least Privilege:** Restrict AI data access to those with a demonstrable business need.  
• **Use Role-Based Access Control (RBAC):** Define roles and permissions aligned to job functions.  
• **Implement Authentication Controls:** Enforce multi-factor authentication for privileged accounts.  
• **Maintain Access Logs:** Record who accessed what, when, and for what purpose.  
• **Review Regularly:** Conduct periodic access reviews and revoke unused privileges.  
• **Automate Where Possible:** Use identity governance tools to manage access lifecycle and policy compliance.  
Effective access control protects data integrity, privacy, and accountability across AI environments.""",
        "evidence_types": """To comply with **DS-04 ("Control and authorise access to data used in AI systems")**, provide documentation and records confirming structured access management.  
**Key Evidence Types:**  
• **Access Control Policy:** Enterprise or AI-specific access management policy defining principles and authorisation steps.  
• **Access Logs:** Records showing dataset access history and privileged account monitoring.  
• **User Permissions Reports:** Role and permission listings reviewed by data owners or stewards.  
• **Review Records:** Audit trails of access reviews and revocation actions.  
• **Authentication Evidence:** Proof of MFA, SSO, or privileged access management implementations.  
• **Audit Findings:** Reports verifying compliance with access control requirements.  
**In short:** demonstrate that AI data access is formally authorised, limited to necessary roles, continuously monitored, and periodically reviewed for compliance.""",
    },
    {
        "code": """DS-05""",
        "text": """What security controls protect data used and generated by AI systems?""",
        "explanation": """Robust data security controls prevent unauthorised access, tampering, or loss of sensitive information used in AI. Inadequate protection exposes the organisation to breaches, manipulation of training data, and reputational harm. This question evaluates whether technical and procedural safeguards—such as encryption, segregation, and monitoring—are applied throughout the AI data lifecycle.

Example: A council enforces encryption-at-rest and in-transit for all AI datasets, stores them in segregated environments, and monitors data transfer logs for suspicious activity.""",
        "domain_order": 4,
        "order": 5,
        "foundational": """Minimal or inconsistent security measures protect AI data.""",
        "developing": """Some encryption or security tools are implemented but lack consistent application or monitoring.""",
        "established": """AI data is protected by defined security controls including encryption, access logs, and network safeguards.""",
        "leading": """Comprehensive, layered data security controls are implemented, automated, and validated through continuous monitoring and testing.""",
        "additional_guide": """Additional Guidance - Implementing Data Security for AI Systems

Security controls safeguard data integrity and confidentiality across all AI processes. To strengthen protection:  
• **Apply Encryption:** Protect data in transit and at rest using approved algorithms.  
• **Segment Data Environments:** Isolate AI development and production networks.  
• **Implement Logging and Monitoring:** Track data access, transfer, and modification activities.  
• **Use Secure Storage:** Restrict export, backup, or transfer of AI datasets without authorisation.  
• **Conduct Vulnerability Testing:** Regularly test storage, APIs, and endpoints.  
• **Automate Alerts:** Use security information and event management (SIEM) systems for real-time monitoring.  
Proactive security measures ensure data confidentiality, integrity, and trustworthiness throughout the AI lifecycle.""",
        "evidence_types": """To comply with **DS-05 ("Implement security controls protecting AI data")**, provide artefacts showing the application and monitoring of layered security measures.  
**Key Evidence Types:**  
• **Security Policies:** Information Security Policy or AI Data Protection Standard specifying encryption and access requirements.  
• **Technical Configurations:** Screenshots or reports confirming encryption, firewall, or data segregation settings.  
• **Monitoring Logs:** SIEM or audit logs showing data activity and alerts.  
• **Testing Results:** Vulnerability scans, penetration tests, or control validation reports.  
• **Change Records:** Authorised change requests for AI data storage or access environments.  
• **Audit Findings:** Independent reviews confirming compliance with data security controls.  
**In short:** demonstrate that AI data is systematically protected through technical safeguards, monitoring, and verification of security effectiveness.""",
    },
    {
        "code": """DS-06""",
        "text": """How does the organisation manage data retention and secure disposal for AI datasets?""",
        "explanation": """AI datasets often contain sensitive or regulated information that must not be retained longer than necessary. Without defined retention and disposal processes, outdated or redundant data can create unnecessary privacy, compliance, and storage risks. This question assesses whether the organisation applies clear policies for retaining, archiving, and securely destroying AI-related data in accordance with legal and operational requirements.

Example: A council enforces a 24-month retention policy for AI training data. Datasets are automatically archived and securely deleted after the retention period, with deletion certificates stored in the governance system.""",
        "domain_order": 4,
        "order": 6,
        "foundational": """No formal retention or disposal controls exist for AI data.""",
        "developing": """Some retention practices exist but are inconsistent or not documented.""",
        "established": """AI data retention and disposal follow formal schedules, with documented procedures and verification.""",
        "leading": """Automated retention and disposal processes are embedded, auditable, and aligned with legal and ethical requirements.""",
        "additional_guide": """Additional Guidance - Managing AI Data Retention and Disposal

Effective data lifecycle management reduces privacy exposure and ensures compliance. To mature your approach:  
• **Define Retention Schedules:** Align AI dataset retention with organisational and legislative requirements (e.g., privacy, records acts).  
• **Document Disposal Procedures:** Outline steps for secure deletion, sanitisation, or anonymisation.  
• **Automate Where Possible:** Use retention tools or scripts to enforce policies.  
• **Verify Disposal:** Record deletion evidence and retain certificates or logs.  
• **Include in Policy Frameworks:** Reference AI data lifecycle requirements in data and information governance policies.  
• **Train Staff:** Ensure custodians and developers understand disposal obligations.  
Strong retention and disposal practices minimise data risk and uphold responsible information stewardship.""",
        "evidence_types": """To comply with **DS-06 ("Manage retention and secure disposal of AI datasets")**, provide documentation showing formal lifecycle and destruction controls.  
**Key Evidence Types:**  
• **Retention Schedules:** Approved data retention and disposal schedules covering AI datasets.  
• **Policies & Procedures:** Information Lifecycle or AI Data Retention Policy specifying retention periods and deletion methods.  
• **Deletion Logs:** Evidence of data destruction or anonymisation (e.g., certificates, audit trails).  
• **Automation Evidence:** System settings or workflows enforcing automated retention.  
• **Audit Findings:** Records verifying compliance with retention and disposal requirements.  
• **Training Records:** Evidence of staff training on data lifecycle management.  
**In short:** demonstrate that AI datasets are retained only as long as necessary and securely destroyed under verifiable, policy-driven controls.""",
    },
    {
        "code": """DS-07""",
        "text": """How does the organisation ensure AI data handling complies with privacy and data protection obligations?""",
        "explanation": """AI systems often process personal or sensitive data. Without strong privacy controls, organisations risk breaching legislation, losing public trust, and enabling unintended harm. This question assesses whether privacy-by-design principles, consent management, and legal compliance measures are embedded into AI development and operations.

Example: A council integrates Privacy Impact Assessments (PIAs) into its AI project lifecycle, ensuring personal information is minimised, anonymised where possible, and processed in line with the Privacy Act 1988 (Cth) and local data-protection policies.""",
        "domain_order": 4,
        "order": 7,
        "foundational": """Privacy obligations are not considered in AI development or data use.""",
        "developing": """Some privacy reviews occur, but controls and assessments are inconsistent.""",
        "established": """Privacy-by-design practices and PIAs are standard for AI systems handling personal data.""",
        "leading": """Comprehensive privacy governance integrates consent, minimisation, and automated compliance monitoring.""",
        "additional_guide": """Additional Guidance - Embedding Privacy and Data Protection in AI

Responsible AI relies on strong privacy safeguards. To mature your approach:  
• **Apply Privacy-by-Design:** Integrate privacy controls at each stage of AI system design and deployment.  
• **Conduct PIAs:** Require assessments for all projects using personal or identifiable data.  
• **Minimise Data Use:** Limit collection to what is necessary; anonymise or pseudonymise when possible.  
• **Manage Consent:** Implement transparent consent mechanisms for data subjects.  
• **Comply with Laws:** Align processes with the Privacy Act 1988 (Cth), APPs, and any relevant international standards (e.g., GDPR).  
• **Monitor Continuously:** Audit AI data practices for ongoing compliance.  
Embedding privacy from the outset reduces legal exposure and fosters public trust in responsible AI use.""",
        "evidence_types": """To comply with **DS-07 ("Ensure AI data handling complies with privacy and data-protection obligations")**, provide artefacts demonstrating structured privacy governance and assurance.  
**Key Evidence Types:**  
• **Policies & Frameworks:** Privacy Policy, Data-Protection Framework, or AI Privacy-by-Design Guidelines.  
• **Privacy Impact Assessments:** Completed PIAs for AI systems processing personal data.  
• **Consent Records:** Logs showing consent capture, withdrawal, and audit tracking.  
• **Technical Controls:** Evidence of data-minimisation, anonymisation, or pseudonymisation measures.  
• **Audit Reports:** Internal or external reviews confirming compliance with privacy legislation.  
• **Training Records:** Staff completion of privacy and responsible-data-use training.  
**In short:** demonstrate that AI systems follow structured privacy-by-design processes, supported by compliance reviews, documentation, and continuous oversight.""",
    },
    {
        "code": """DS-08""",
        "text": """How does the organisation govern third-party data access and sharing for AI systems?""",
        "explanation": """Third-party data access and sharing introduce significant privacy, security, and ethical risks. Without proper governance, external partners or vendors may mishandle data or breach contractual obligations. This question assesses whether the organisation applies structured controls, agreements, and oversight to manage external data sharing and AI collaborations.

Example: A council implements a Third-Party Data Governance Framework requiring all AI vendors to sign data-use agreements, undergo security assessments, and demonstrate compliance with the council’s privacy and ethical standards.""",
        "domain_order": 4,
        "order": 8,
        "foundational": """Third-party data access and sharing occur informally, without agreements or oversight.""",
        "developing": """Some data-sharing agreements exist but lack consistent privacy or security provisions.""",
        "established": """Formal agreements and due diligence govern all third-party AI data sharing, with compliance monitoring in place.""",
        "leading": """Comprehensive third-party governance integrates risk assessments, contractual controls, and continuous compliance verification.""",
        "additional_guide": """Additional Guidance - Governing Third-Party Data Access

Robust third-party governance ensures shared data is protected and responsibly used. To mature your approach:  
• **Establish Formal Agreements:** Require contracts specifying permitted data uses, retention, and destruction.  
• **Conduct Due Diligence:** Assess third-party security, privacy, and ethical practices before engagement.  
• **Implement Data-Sharing Policies:** Define approval processes and minimum protection standards.  
• **Monitor Compliance:** Review vendor performance and data handling periodically.  
• **Restrict Data Transfers:** Ensure cross-border transfers comply with applicable privacy laws.  
• **Require Assurance Evidence:** Obtain security certifications, SOC 2 reports, or independent audit results.  
Effective governance maintains control over AI-related data flows and protects organisational and public trust.""",
        "evidence_types": """To comply with **DS-08 ("Govern third-party data access and sharing for AI systems")**, provide documentation demonstrating oversight, agreements, and verification processes.  
**Key Evidence Types:**  
• **Data-Sharing Agreements:** Contracts outlining use limitations, retention terms, and confidentiality clauses.  
• **Vendor Assessments:** Security and privacy due-diligence questionnaires or audit results.  
• **Policies & Procedures:** Third-Party Risk Management or Data-Sharing Framework referencing AI use.  
• **Monitoring Reports:** Records of vendor compliance checks and review outcomes.  
• **Approval Workflows:** Documentation of internal authorisation for external data sharing.  
• **Audit Findings:** Independent assurance confirming third-party adherence to data governance obligations.  
**In short:** demonstrate that all AI data-sharing and third-party arrangements are governed by formal agreements, continuous oversight, and risk-based assurance processes.""",
    },
    {
        "code": """FI-01""",
        "text": """How does the organisation ensure AI systems are designed and implemented to promote fairness and avoid discrimination?""",
        "explanation": """Fairness ensures AI systems do not produce outcomes that disadvantage individuals or groups based on factors such as gender, race, disability, or socioeconomic status. Without deliberate fairness measures, bias in data or design can lead to inequitable results. This question evaluates whether fairness is embedded across the AI lifecycle—from data collection to deployment and monitoring.

Example: A council applies fairness metrics such as demographic parity and equal opportunity to evaluate its AI models, ensuring no demographic group is disproportionately impacted by automated decisions.""",
        "domain_order": 5,
        "order": 1,
        "foundational": """Fairness is not considered in AI design or evaluation.""",
        "developing": """Some fairness considerations exist but are informal or inconsistent.""",
        "established": """Fairness objectives, metrics, and reviews are defined and applied to AI projects.""",
        "leading": """Fairness is systematically built into AI governance, using measurable indicators, audits, and community consultation.""",
        "additional_guide": """Additional Guidance - Embedding Fairness in AI Systems

Fairness requires deliberate design, testing, and review across the AI lifecycle. To strengthen fairness practices:  
• **Define Fairness Principles:** Establish organisational definitions and goals for fairness and inclusion.  
• **Assess Bias Early:** Identify and address potential data and model bias before deployment.  
• **Use Fairness Metrics:** Apply statistical fairness tests (e.g., demographic parity, disparate impact ratio).  
• **Engage Stakeholders:** Consult affected communities to validate fairness assumptions.  
• **Document Findings:** Record fairness evaluations and mitigation strategies.  
• **Monitor Continuously:** Track fairness outcomes after deployment.  
Integrating fairness safeguards ensures equitable AI outcomes and upholds social responsibility.""",
        "evidence_types": """To comply with **FI-01 ("Promote fairness and avoid discrimination in AI systems")**, provide documentation showing structured fairness testing and governance.  
**Key Evidence Types:**  
• **Fairness Policy:** Principles or standards defining fairness and non-discrimination in AI.  
• **Bias Assessment Reports:** Results from fairness testing tools or independent evaluations.  
• **Dataset Audits:** Analyses of demographic representation and sampling balance.  
• **Model Evaluation Logs:** Documentation of fairness metrics and corrective actions.  
• **Stakeholder Engagement Records:** Consultation summaries or community feedback reports.  
• **Audit Findings:** Internal or external reviews of fairness performance.  
**In short:** demonstrate that fairness is measured, documented, and continuously improved across all AI projects.""",
    },
    {
        "code": """FI-02""",
        "text": """How does the organisation ensure diversity and representativeness in data used for AI systems?""",
        "explanation": """Diverse and representative data reduces the risk of biased or inaccurate AI outcomes. When datasets lack sufficient coverage of demographic or contextual variation, AI models may underperform for certain groups or produce inequitable results. This question assesses whether the organisation actively sources, evaluates, and maintains diverse datasets reflecting the populations or contexts its AI systems affect.

Example: A council reviews all AI training datasets to ensure representation across age, gender, ethnicity, and geography, supplementing underrepresented groups with additional data sources.""",
        "domain_order": 5,
        "order": 2,
        "foundational": """Data diversity is not evaluated or managed; datasets reflect existing biases.""",
        "developing": """Some efforts to improve data diversity exist but are informal or project-specific.""",
        "established": """Processes exist to evaluate and enhance dataset representativeness before model training.""",
        "leading": """Diversity is a formal requirement for all AI datasets, supported by metrics, audits, and stakeholder input.""",
        "additional_guide": """Additional Guidance - Ensuring Diverse and Representative Datasets

Representative data improves fairness, reliability, and inclusion. To strengthen practices:  
• **Audit Dataset Composition:** Assess demographic and contextual coverage before AI training.  
• **Define Inclusion Standards:** Establish thresholds for minimum diversity representation.  
• **Supplement Data Sources:** Address gaps by collecting or synthesising underrepresented data.  
• **Validate Performance Equitably:** Test models across demographic segments to detect disparities.  
• **Engage Stakeholders:** Involve domain experts or affected communities in reviewing dataset balance.  
• **Document Diversity Assessments:** Maintain reports detailing how representation was achieved.  
Systematic diversity management ensures AI systems reflect and serve all communities fairly.""",
        "evidence_types": """To comply with **FI-02 ("Ensure diversity and representativeness in AI data")**, provide artefacts demonstrating data diversity evaluation and improvement activities.  
**Key Evidence Types:**  
• **Dataset Diversity Reports:** Documentation of demographic representation analyses.  
• **Data Governance Policies:** Requirements for inclusive and representative data collection.  
• **Audit Results:** Reviews confirming adequate diversity in AI training datasets.  
• **Performance Metrics:** Model testing results segmented by demographic group.  
• **Stakeholder Consultation Records:** Evidence of engagement with diverse community groups or experts.  
• **Corrective Action Logs:** Records showing how data imbalances were addressed.  
**In short:** demonstrate that AI datasets are intentionally diverse, regularly audited, and aligned with fairness and inclusion objectives.""",
    },
    {
        "code": """FI-03""",
        "text": """How does the organisation detect and mitigate bias in AI models and decision-making processes?""",
        "explanation": """Bias in AI can lead to unfair or discriminatory outcomes that erode trust and expose the organisation to legal or ethical risk. Without proactive detection, biases in data, algorithms, or processes may go unnoticed. This question evaluates whether systematic tools and methods are used to identify, measure, and mitigate bias throughout the AI lifecycle.

Example: A council uses bias-detection frameworks such as IBM AI Fairness 360 to analyse model predictions, identifying disparities between demographic groups and retraining models to improve fairness outcomes.""",
        "domain_order": 5,
        "order": 3,
        "foundational": """No formal bias detection or mitigation processes exist.""",
        "developing": """Bias testing occurs sporadically or only after AI deployment.""",
        "established": """Structured bias detection and mitigation processes are integrated into AI model development.""",
        "leading": """Continuous bias detection, auditing, and mitigation are embedded organisation-wide using standardised tools and metrics.""",
        "additional_guide": """Additional Guidance - Detecting and Mitigating AI Bias

Bias management ensures fairness and compliance with ethical standards. To enhance maturity:  
• **Define Bias Metrics:** Establish quantitative indicators (e.g., disparate impact ratio, false-positive parity).  
• **Use Detection Tools:** Implement libraries such as Fairlearn or AI Fairness 360.  
• **Review Model Pipelines:** Analyse training data, feature selection, and model outputs for bias.  
• **Apply Mitigation Techniques:** Rebalance datasets, adjust weighting, or use bias-correction algorithms.  
• **Conduct Periodic Audits:** Review fairness performance regularly post-deployment.  
• **Document Results:** Record findings, mitigations, and residual risk.  
Structured bias detection and mitigation reduce inequity and improve accountability in AI-driven decisions.""",
        "evidence_types": """To comply with **FI-03 ("Detect and mitigate bias in AI models and decisions")**, provide documentation confirming structured bias identification and remediation practices.  
**Key Evidence Types:**  
• **Bias Testing Reports:** Outputs from fairness evaluation tools or frameworks.  
• **Policies & Procedures:** AI Fairness or Bias Mitigation Guidelines.  
• **Model Documentation:** Records showing fairness metrics and mitigation actions.  
• **Audit Results:** Periodic reviews validating bias control effectiveness.  
• **Training Records:** Evidence of staff education on AI bias and mitigation methods.  
• **Continuous Monitoring Logs:** Automated fairness dashboards tracking bias trends over time.  
**In short:** demonstrate that AI bias is systematically identified, measured, and mitigated throughout the model lifecycle.""",
    },
    {
        "code": """FI-04""",
        "text": """How does the organisation ensure inclusivity and accessibility are embedded into AI system design and deployment?""",
        "explanation": """Inclusivity and accessibility ensure AI systems can be effectively used and understood by all individuals, including those from diverse backgrounds or with disabilities. Without intentional design, AI may unintentionally exclude or disadvantage specific groups. This question assesses whether inclusive design principles, accessibility standards, and user testing are built into the AI development process.

Example: A council designs its AI-powered customer service chatbot following WCAG accessibility guidelines, testing with users from different linguistic and disability backgrounds to ensure equitable interaction.""",
        "domain_order": 5,
        "order": 4,
        "foundational": """AI systems are designed without consideration for inclusivity or accessibility.""",
        "developing": """Some accessibility or inclusivity checks occur, but they are inconsistent or optional.""",
        "established": """Inclusive design principles and accessibility testing are incorporated into AI projects.""",
        "leading": """Inclusivity and accessibility are embedded organisation-wide, with continuous testing, community input, and policy integration.""",
        "additional_guide": """Additional Guidance - Embedding Inclusivity and Accessibility

Inclusive AI ensures equitable participation and access. To strengthen practices:  
• **Adopt Accessibility Standards:** Follow WCAG, ISO 9241-210, or relevant national guidelines.  
• **Conduct Diverse User Testing:** Include participants from varied demographic and ability groups.  
• **Apply Universal Design Principles:** Ensure AI interfaces are intuitive, adaptable, and inclusive by default.  
• **Collaborate with Experts:** Engage accessibility specialists or advocacy organisations.  
• **Document Adjustments:** Record design improvements and accessibility compliance results.  
• **Monitor Continuously:** Evaluate inclusivity post-deployment through feedback and audits.  
Embedding inclusivity ensures AI benefits are shared fairly and equitably across all user groups.""",
        "evidence_types": """To comply with **FI-04 ("Embed inclusivity and accessibility into AI system design")**, provide documentation showing structured design, testing, and review processes.  
**Key Evidence Types:**  
• **Policies & Standards:** Accessibility or Inclusive Design Policy referencing AI systems.  
• **Testing Reports:** Records of usability and accessibility testing across diverse user groups.  
• **Design Documentation:** Wireframes, prototypes, or interface guidelines demonstrating inclusive design.  
• **Stakeholder Engagement:** Consultation summaries with accessibility or diversity representatives.  
• **Compliance Records:** Certifications or audit results verifying accessibility compliance.  
• **Training Materials:** Staff education on inclusive design and accessibility practices.  
**In short:** demonstrate that inclusivity and accessibility are deliberately incorporated, tested, and maintained throughout AI system design and implementation.""",
    },
    {
        "code": """FI-05""",
        "text": """How does the organisation consult with stakeholders and communities to ensure fair and inclusive AI outcomes?""",
        "explanation": """Community and stakeholder consultation ensures AI systems reflect diverse perspectives and align with societal values. Without engagement, AI initiatives risk overlooking the needs or impacts on vulnerable groups. This question evaluates whether stakeholder input is systematically sought, documented, and used to guide ethical and fair AI decision-making.

Example: A council holds community forums before deploying an AI resource-allocation model, gathering input from advocacy groups and residents to identify potential equity concerns and adjust model criteria accordingly.""",
        "domain_order": 5,
        "order": 5,
        "foundational": """No consultation occurs with stakeholders or communities affected by AI use.""",
        "developing": """Some engagement occurs but is limited, informal, or project-specific.""",
        "established": """Stakeholder and community consultation is a formal step in AI planning and deployment.""",
        "leading": """Ongoing, structured consultation ensures diverse voices continuously shape AI policy, design, and governance.""",
        "additional_guide": """Additional Guidance - Consulting for Fair AI Outcomes

Engagement builds legitimacy, fairness, and community trust. To enhance consultation:  
• **Identify Stakeholders:** Include community groups, customers, regulators, and advocacy organisations.  
• **Plan Early:** Integrate consultation into the AI lifecycle-before design, during testing, and after deployment.  
• **Use Multiple Channels:** Conduct surveys, workshops, and focus groups to gather broad input.  
• **Record and Analyse Feedback:** Document concerns and incorporate them into design or policy revisions.  
• **Provide Feedback Loops:** Communicate how input influenced decisions.  
• **Review Regularly:** Assess engagement effectiveness and inclusivity.  
Meaningful consultation ensures AI decisions reflect shared values and equitable outcomes.""",
        "evidence_types": """To comply with **FI-05 ("Consult stakeholders and communities for fair AI outcomes")**, provide artefacts showing structured engagement and integration of feedback.  
**Key Evidence Types:**  
• **Engagement Frameworks:** Policies outlining community and stakeholder consultation processes.  
• **Consultation Records:** Meeting minutes, surveys, or forum summaries documenting stakeholder input.  
• **Impact Assessments:** Records showing consultation outcomes incorporated into AI design or policy.  
• **Communication Evidence:** Reports or statements explaining how feedback influenced AI projects.  
• **Audit or Review Reports:** Independent reviews of engagement completeness and effectiveness.  
• **Diversity Representation Data:** Evidence showing inclusion of varied stakeholder groups.  
**In short:** demonstrate that consultation is systematic, inclusive, and directly influences how AI systems are designed and governed.""",
    },
    {
        "code": """FI-06""",
        "text": """How does the organisation measure and monitor fairness in AI outcomes over time?""",
        "explanation": """Fairness must be continuously evaluated to ensure AI systems do not unintentionally disadvantage certain groups after deployment. Without ongoing monitoring, models may drift or become biased due to changing data or operational contexts. This question assesses whether fairness metrics and reviews are built into post-deployment monitoring and performance management processes.

Example: A council monitors the outcomes of its AI-driven service eligibility tool, comparing decisions across demographics quarterly and adjusting parameters when fairness metrics fall below defined thresholds.""",
        "domain_order": 5,
        "order": 6,
        "foundational": """Fairness is not tracked after AI systems are deployed.""",
        "developing": """Fairness reviews occur occasionally but lack consistency or defined metrics.""",
        "established": """Regular fairness monitoring uses defined indicators and comparative analysis across groups.""",
        "leading": """Continuous fairness monitoring is automated and integrated into governance dashboards, with corrective actions triggered by thresholds.""",
        "additional_guide": """Additional Guidance - Monitoring Fairness Over Time

Continuous fairness measurement ensures equitable outcomes are sustained. To strengthen practices:  
• **Define Metrics:** Establish fairness KPIs (e.g., demographic parity difference, disparate impact ratio).  
• **Set Thresholds:** Define acceptable variance limits for AI outcomes.  
• **Automate Monitoring:** Integrate fairness tracking into performance dashboards.  
• **Review Regularly:** Schedule fairness audits aligned with model retraining cycles.  
• **Investigate Deviations:** Analyse and correct fairness anomalies immediately.  
• **Report Transparently:** Communicate findings to leadership and affected stakeholders.  
Ongoing fairness monitoring promotes accountability and long-term trust in AI outcomes.""",
        "evidence_types": """To comply with **FI-06 ("Measure and monitor fairness in AI outcomes over time")**, provide artefacts proving structured, repeatable fairness monitoring.  
**Key Evidence Types:**  
• **Monitoring Dashboards:** Tools or reports tracking fairness KPIs over time.  
• **Metrics Documentation:** Definitions and threshold settings for fairness indicators.  
• **Audit Reports:** Periodic fairness evaluation findings and corrective actions.  
• **Meeting Minutes:** Governance discussions on fairness trends and performance.  
• **Review Schedules:** Documented cadence for post-deployment fairness assessments.  
• **Change Records:** Logs of model adjustments following fairness reviews.  
**In short:** demonstrate that fairness is measured continuously, reported transparently, and used to improve AI systems throughout their lifecycle.""",
    },
    {
        "code": """FI-07""",
        "text": """How does the organisation ensure fairness and inclusivity requirements are applied to procured or vendor-provided AI solutions?""",
        "explanation": """Vendors supplying AI systems must meet the organisation’s fairness and inclusivity standards. Without clear procurement requirements, external solutions may introduce bias, ethical risks, or non-compliance. This question evaluates whether fairness and inclusivity are embedded into procurement processes, vendor assessments, and contractual agreements for AI products and services.

Example: A council includes fairness, bias testing, and explainability requirements in all AI vendor contracts, requiring suppliers to provide evidence of independent fairness audits and demographic performance testing.""",
        "domain_order": 5,
        "order": 7,
        "foundational": """AI procurement lacks fairness or inclusivity considerations.""",
        "developing": """Some fairness clauses are included in vendor contracts, but enforcement is limited.""",
        "established": """Fairness and inclusivity requirements are part of procurement templates and vendor evaluation criteria.""",
        "leading": """Procurement processes mandate verifiable fairness testing, audits, and continuous compliance from all AI vendors.""",
        "additional_guide": """Additional Guidance - Fairness in AI Procurement and Vendor Governance

Fairness must extend across the supply chain. To improve oversight:  
• **Embed Fairness in Procurement Policies:** Define fairness and bias testing requirements in RFPs and contracts.  
• **Assess Vendors Pre-Selection:** Evaluate suppliers' ethical AI frameworks and diversity practices.  
• **Request Evidence:** Require fairness testing results, bias audits, and documentation.  
• **Include Contractual Obligations:** Mandate reporting, remediation, and transparency commitments.  
• **Monitor Vendor Performance:** Review compliance throughout the contract lifecycle.  
• **Promote Collaboration:** Support vendors in improving fairness practices through shared frameworks.  
Fair procurement ensures external AI systems align with organisational ethics and inclusion goals.""",
        "evidence_types": """To comply with **FI-07 ("Apply fairness and inclusivity requirements to vendor AI solutions")**, provide documentation demonstrating procurement integration and vendor assurance.  
**Key Evidence Types:**  
• **Procurement Policies:** Clauses or frameworks referencing fairness and inclusivity in AI acquisitions.  
• **RFP Templates:** Standard request-for-proposal documents including fairness and bias criteria.  
• **Vendor Assessments:** Evaluation reports reviewing supplier fairness and diversity compliance.  
• **Contracts:** AI vendor agreements with fairness and audit obligations.  
• **Compliance Reports:** Vendor-provided fairness audit results or demographic performance analyses.  
• **Performance Reviews:** Records of vendor oversight and remediation actions.  
**In short:** demonstrate that fairness and inclusivity standards apply equally to all externally sourced AI systems and suppliers.""",
    },
    {
        "code": """FI-08""",
        "text": """How does the organisation review and continuously improve its fairness and inclusivity practices in AI governance?""",
        "explanation": """Fairness and inclusivity must evolve with societal expectations, new data sources, and emerging regulations. Without regular review, even well-designed frameworks can become outdated or ineffective. This question assesses whether the organisation periodically evaluates its fairness practices, benchmarks performance, and updates policies and models to reflect continuous learning.

Example: A council performs annual fairness audits across all AI projects, benchmarks its framework against ISO 42001 and national AI ethics guidelines, and updates its Responsible AI Policy accordingly.""",
        "domain_order": 5,
        "order": 8,
        "foundational": """Fairness and inclusivity practices are static and rarely reviewed.""",
        "developing": """Reviews occur irregularly and are reactive to issues or incidents.""",
        "established": """Regular reviews and updates ensure fairness processes stay relevant and effective.""",
        "leading": """Continuous improvement is embedded, using metrics, benchmarking, and stakeholder input to refine fairness practices.""",
        "additional_guide": """Additional Guidance - Continuous Improvement of Fairness Practices

Fairness governance requires periodic reflection and evolution. To enhance maturity:  
• **Conduct Regular Reviews:** Schedule annual evaluations of fairness frameworks and outcomes.  
• **Benchmark Against Standards:** Compare practices to frameworks such as ISO 42001 or OECD AI Principles.  
• **Use Performance Metrics:** Track improvements across bias reduction, diversity, and inclusion indicators.  
• **Gather Feedback:** Incorporate insights from users, staff, and affected communities.  
• **Update Policies:** Reflect lessons learned in the Responsible AI or Fairness Policy.  
• **Report Outcomes:** Communicate improvements through internal or public reporting.  
Continuous improvement ensures fairness practices remain adaptive, measurable, and credible.""",
        "evidence_types": """To comply with **FI-08 ("Review and continuously improve fairness and inclusivity practices")**, provide documentation demonstrating structured review, benchmarking, and refinement.  
**Key Evidence Types:**  
• **Review Reports:** Annual fairness and inclusivity evaluation or audit summaries.  
• **Benchmarking Analyses:** Comparisons against national or international AI standards.  
• **Improvement Logs:** Records of updates made to fairness policies, metrics, or governance processes.  
• **Meeting Minutes:** Committee discussions on lessons learned and framework revisions.  
• **Stakeholder Feedback:** Surveys or consultations informing fairness improvements.  
• **Performance Dashboards:** Metrics showing fairness and inclusion trend data.  
**In short:** demonstrate that fairness and inclusivity frameworks are reviewed systematically and improved through measurable, evidence-based actions.""",
    },
    {
        "code": """GO-01""",
        "text": """How clearly defined are the organisation’s AI governance structures and leadership roles?""",
        "explanation": """Clear AI governance ensures accountability, consistency, and responsible innovation. Without defined leadership and oversight, AI initiatives can become fragmented, increasing ethical and operational risks. This question assesses whether your organisation has formal structures—such as a Responsible AI Committee or Chief AI Officer—that guide how AI is developed, procured, and monitored.

Example: A council establishes an AI Governance Committee chaired by the CIO, including Risk, Legal, HR, and Data Science members, responsible for reviewing project proposals and ethical considerations.""",
        "domain_order": 6,
        "order": 1,
        "foundational": """AI responsibilities are informal or unclear, with no defined governance body or accountability.""",
        "developing": """Partial oversight exists through specific roles, but governance remains fragmented or inconsistent.""",
        "established": """A formal AI governance framework and defined leadership roles (e.g., Chief AI Officer, Ethics Committee) are in place and active.""",
        "leading": """Enterprise-wide governance is embedded, with executive sponsorship, cross-functional representation, and periodic effectiveness reviews.""",
        "additional_guide": """Additional Guidance - Establishing AI Governance Structures

AI governance defines who makes decisions, how risks are managed, and how ethical standards are upheld. To strengthen this:  
• **Define Roles and Accountability:** Assign a senior executive (e.g., Chief AI Officer) and define oversight responsibilities across departments.  
• **Create Cross-Functional Committees:** Include Legal, Risk, Data, HR, and Communications to ensure diverse perspectives.  
• **Embed into Corporate Governance:** Integrate AI governance into risk management and digital transformation programs.  
• **Establish Decision Pathways:** Document who approves, audits, and escalates AI-related decisions.  
• **Benchmark Regularly:** Review governance effectiveness annually against ISO 42001 or NIST AI RMF.  
Effective AI governance builds transparency, aligns innovation with values, and reduces reputational and compliance risks.""",
        "evidence_types": """To demonstrate compliance with **GO-01 ("Ensure the organisation's AI governance structures and leadership roles are clearly defined")**, provide evidence that accountability and oversight for AI are formally defined and operating effectively.  
**Key Evidence Types:**  
• **Policies & Frameworks:** Approved AI Governance Policy or Responsible AI Framework detailing roles, responsibilities, and decision rights.  
• **Organisational Structure:** Role descriptions (e.g., Chief AI Officer, Ethics Lead) and governance committee Terms of Reference.  
• **Meeting Records:** Minutes or reports from AI Governance or Ethics Committees showing project reviews or decisions.  
• **Integration Evidence:** AI governance references in enterprise risk, privacy, or data policies.  
• **Performance & Review:** Internal audits or scorecards evaluating AI governance effectiveness.  
• **Training & Awareness:** Records of leadership training on AI responsibilities and ethics.  
**In short:** show a structured, cross-functional governance model with documented oversight and active executive ownership.""",
    },
    {
        "code": """GO-02""",
        "text": """To what extent are AI initiatives aligned with the organisation’s strategic objectives and values?""",
        "explanation": """AI delivers sustainable value only when aligned with the organisation’s mission, ethical principles, and community outcomes. Uncoordinated or experimental projects risk wasted investment, ethical missteps, or public distrust. This question assesses whether AI initiatives are strategically governed—ensuring each project demonstrably supports organisational goals, values, and risk appetite.

Example: A local council links every AI proposal to its “Smart and Inclusive City” strategy, requiring departments to show how each project advances accessibility, sustainability, or transparency before approval.""",
        "domain_order": 6,
        "order": 2,
        "foundational": """AI initiatives occur in silos without alignment to strategy, values, or ethics principles.""",
        "developing": """Some initiatives reference strategic goals, but ethical or societal alignment is inconsistent.""",
        "established": """Formal review ensures AI initiatives align with strategy, values, and responsible-AI commitments before approval.""",
        "leading": """AI is embedded in enterprise strategy, with defined success metrics, ethical KPIs, and transparent reporting to leadership.""",
        "additional_guide": """Additional Guidance - Strategic Alignment of AI Initiatives

Strategic alignment ensures AI investments deliver measurable public and organisational value. To improve alignment:  
• **Integrate AI into Strategy:** Reference AI as a strategic enabler in corporate, digital, or innovation roadmaps.  
• **Create Approval Gateways:** Require AI proposals to pass a _Strategic Fit and Ethics Impact_ assessment.  
• **Define Alignment Criteria:** Evaluate projects against organisational priorities (e.g., sustainability, inclusion, service efficiency).  
• **Connect to Risk Appetite:** Clarify acceptable AI risk thresholds and escalation routes.  
• **Track and Communicate Outcomes:** Link AI performance to KPIs and report achievements to executives and stakeholders.  
Embedding AI into strategic planning builds accountability, maximises impact, and demonstrates ethical alignment to boards and the public.""",
        "evidence_types": """To comply with **GO-02 ("Ensure AI initiatives align with strategic objectives and values")**, provide evidence that AI planning and approvals link to enterprise strategy and ethical frameworks.  
**Key Evidence Types:**  
• **Strategic Documents:** Corporate, Digital, or Innovation Strategies referencing responsible AI principles.  
• **Governance Artefacts:** Project-initiation or business-case templates requiring alignment to organisational objectives and ethics commitments.  
• **Portfolio Records:** Registers mapping AI initiatives to strategic outcomes and performance indicators.  
• **Leadership Evidence:** Meeting minutes or executive briefings confirming AI projects reviewed for strategic alignment.  
• **Performance Reporting:** Dashboards or reports measuring AI contributions to strategic KPIs.  
• **Training & Culture:** Staff communications or workshops reinforcing AI's strategic role and ethical boundaries.  
**In short:** evidence should show that AI initiatives are approved, monitored, and evaluated as integral components of the organisation's strategy and value system.""",
    },
    {
        "code": """GO-03""",
        "text": """Does the organisation maintain an AI policy or equivalent governance document?""",
        "explanation": """An AI policy provides a clear framework for responsible development, procurement, and use of AI across the organisation. Without one, AI projects risk inconsistent practices, ethical breaches, and non-compliance with emerging regulations. This question assesses whether your organisation has a formally approved, regularly reviewed AI policy—or equivalent governance document—that defines roles, principles, and expectations for responsible AI.

Example: A city council adopts a “Responsible AI Policy” that defines ethical principles, assigns accountability to a Chief Data Officer, and requires all new AI systems to complete an ethics and risk review prior to deployment.""",
        "domain_order": 6,
        "order": 3,
        "foundational": """No AI policy or governance framework exists; practices are informal or project-specific.""",
        "developing": """A draft or informal AI policy exists but lacks endorsement, communication, or active implementation.""",
        "established": """An approved AI Policy defines governance, ethics, and responsibilities, and is implemented organisation-wide.""",
        "leading": """The AI Policy is embedded into corporate governance, reviewed annually, and aligned to emerging laws and standards.""",
        "additional_guide": """Additional Guidance - Developing and Embedding an AI Policy

An AI policy formalises how your organisation governs AI to ensure accountability, fairness, and transparency. To strengthen policy maturity:  
• **Define Scope and Purpose:** Clarify what constitutes "AI" and the policy's objectives (risk control, ethical assurance, compliance).  
• **Adopt Global Principles:** Align with frameworks such as Australia's AI Ethics Principles, NIST AI RMF, or ISO/IEC 42001.  
• **Assign Accountability:** Nominate executive owners (e.g., Chief AI Officer) and outline review and escalation pathways.  
• **Integrate with Existing Policies:** Link to privacy, cybersecurity, procurement, and data-governance frameworks.  
• **Operationalise the Policy:** Provide templates, checklists, and training to support compliance.  
• **Review and Update:** Evaluate policy effectiveness annually and after major regulatory or technological changes.  
A well-defined, living AI Policy demonstrates leadership commitment and builds trust with regulators, staff, and the community.""",
        "evidence_types": """To comply with **GO-03 ("Maintain an approved AI policy or governance framework")**, provide evidence that the policy is formalised, endorsed, and applied in practice.  
**Key Evidence Types:**  
• **Policy Documentation:** Approved AI Policy or Responsible AI Framework endorsed by executive leadership, with clear principles and scope.  
• **Integration Records:** References to the AI Policy within risk management, privacy, and procurement documents.  
• **Governance Artefacts:** Committee minutes showing policy review, endorsement, or monitoring activities.  
• **Operational Evidence:** Completed AI Impact Assessments, Ethics Review checklists, or project templates aligned to policy requirements.  
• **Communication & Training:** Staff briefings, e-learning records, or policy acknowledgment logs demonstrating awareness.  
• **Audit & Review:** Internal or third-party audits confirming the policy is implemented and reviewed regularly.  
**In short:** demonstrate that a formal AI policy exists, is endorsed at the executive level, integrated across governance processes, and actively maintained through regular review and training.""",
    },
    {
        "code": """GO-04""",
        "text": """How is oversight of AI risks and compliance maintained across departments?""",
        "explanation": """AI introduces new forms of operational, ethical, and reputational risk. Without consistent oversight, departments may manage AI risks independently, leading to blind spots and regulatory exposure. This question examines whether AI-related risks and compliance obligations are centrally monitored and coordinated, ensuring visibility across the organisation.

Example: A council’s Risk and Assurance team maintains a consolidated AI risk register. Departmental AI leads submit monthly updates, and results are reviewed by the enterprise risk committee to ensure consistent controls and reporting.""",
        "domain_order": 6,
        "order": 4,
        "foundational": """AI risks are tracked informally, with no central oversight or reporting mechanism.""",
        "developing": """Departments identify AI risks independently; limited cross-functional coordination exists.""",
        "established": """A central function monitors AI risks and compliance, consolidating registers and reporting to leadership.""",
        "leading": """Enterprise-wide oversight integrates AI risk into corporate risk systems, with continuous monitoring and automated reporting.""",
        "additional_guide": """Additional Guidance - Cross-Departmental Risk Oversight

Centralised oversight ensures that AI risks are visible, prioritised, and managed consistently. To mature your approach:  
• **Integrate with ERM:** Embed AI risk categories (ethical, technical, reputational) within the enterprise risk management framework.  
• **Establish Ownership:** Assign a central Risk or Compliance function to coordinate risk capture, analysis, and escalation.  
• **Maintain Unified Registers:** Require departments to document AI risks in a standard format and submit updates periodically.  
• **Define Reporting Cadence:** Provide regular reports to executive risk committees and governance boards.  
• **Monitor Compliance:** Track adherence to AI policy, privacy laws, and security standards (e.g., ISM, ISO 27001).  
• **Automate Where Possible:** Use dashboards or risk tools for real-time monitoring.  
Effective oversight creates transparency, avoids duplicated effort, and ensures AI activities remain lawful, ethical, and accountable.""",
        "evidence_types": """To comply with **GO-04 ("Maintain central oversight of AI risks and compliance")**, provide proof of coordinated, documented risk management.  
**Key Evidence Types:**  
• **Risk Registers:** Consolidated AI risk register or integrated enterprise risk log including ethical, legal, and operational risk categories.  
• **Governance Records:** Committee minutes or dashboards showing review of AI risk trends, issues, or mitigations.  
• **Policies & Frameworks:** Enterprise Risk Management Policy referencing AI risks and cross-departmental reporting obligations.  
• **Monitoring Artefacts:** Compliance tracking reports, internal control testing, or data-drift and bias monitoring logs.  
• **Escalation Evidence:** Records of issue escalation and remediation actions coordinated by central Risk or Compliance functions.  
• **Audit Reports:** Internal or external audits verifying effectiveness of AI risk oversight.  
**In short:** evidence should show that AI risks are systematically identified, centrally managed, and regularly reported to executive leadership for continuous assurance.""",
    },
    {
        "code": """GO-05""",
        "text": """Are AI governance responsibilities incorporated into existing management structures?""",
        "explanation": """Embedding AI governance into existing management structures ensures oversight is sustainable and not dependent on ad-hoc committees or individuals. When AI accountability sits outside normal governance channels, risks may go unmonitored, and ethical review becomes inconsistent. This question evaluates whether AI governance is integrated into established corporate processes, roles, and committees.

Example: A council incorporates AI oversight into its existing Risk and Governance Committee charter. Department managers report AI-related issues as part of standard quarterly reviews rather than through separate, isolated processes.""",
        "domain_order": 6,
        "order": 5,
        "foundational": """AI governance operates informally or separately from established management structures.""",
        "developing": """AI accountability is recognised but only partially reflected in job roles or committee agendas.""",
        "established": """AI responsibilities are integrated into management roles, policies, and performance reporting.""",
        "leading": """AI governance is institutionalised across all levels, with oversight embedded in executive KPIs and board charters.""",
        "additional_guide": """Additional Guidance - Embedding AI Governance into Operations

Integrating AI oversight into everyday governance makes responsible AI a routine part of business operations. To strengthen integration:  
• **Update Governance Charters:** Add AI oversight duties to existing committees (e.g., Risk, Audit, ICT Steering).  
• **Assign Line Accountability:** Reflect AI responsibilities in role descriptions, performance plans, and management KPIs.  
• **Link to Corporate Reporting:** Include AI risk and ethics indicators in quarterly and annual reports.  
• **Use Existing Review Cycles:** Evaluate AI controls during standard internal audits and risk reviews.  
• **Promote Executive Ownership:** Ensure executives sponsor AI initiatives and track compliance through standing agenda items.  
Embedding AI within core management functions prevents duplication, sustains accountability, and ensures ethical practices are maintained even as personnel or projects change.""",
        "evidence_types": """To comply with **GO-05 ("Integrate AI governance into management structures")**, provide evidence showing that AI oversight is built into existing governance, not managed separately.  
**Key Evidence Types:**  
• **Governance Charters:** Updated board or committee terms of reference including AI oversight responsibilities.  
• **Role Descriptions:** Position statements for executives and managers referencing AI ethics, risk, or compliance duties.  
• **Performance Evidence:** KPIs or scorecards measuring adherence to AI policy or ethical standards.  
• **Meeting Records:** Minutes showing AI topics discussed in regular management or audit meetings.  
• **Reporting Frameworks:** Integration of AI metrics in enterprise dashboards or corporate performance reports.  
• **Audit Trail:** Internal or external reviews confirming AI governance is embedded in management processes.  
**In short:** demonstrate that AI governance is not isolated but woven into existing organisational decision-making, accountability, and reporting mechanisms.""",
    },
    {
        "code": """GO-06""",
        "text": """How does the organisation ensure cross-functional participation in AI governance?""",
        "explanation": """Effective AI governance requires collaboration across disciplines to balance technical, legal, ethical, and social perspectives. Without diverse participation, decisions may overlook compliance, fairness, or community impact. This question assesses whether the organisation actively involves multiple departments—such as Legal, HR, Risk, and Communications—in AI governance activities and decision-making.

Example: A local council’s AI Ethics Committee includes representatives from Data Science, Legal, HR, and Community Engagement. Together, they review AI proposals, assess ethical risks, and ensure inclusion of citizen perspectives before approval.""",
        "domain_order": 6,
        "order": 6,
        "foundational": """AI governance discussions are limited to technical or IT staff.""",
        "developing": """Occasional consultation occurs with other functions but participation is inconsistent or informal.""",
        "established": """A multi-disciplinary group meets regularly to review AI projects and advise on ethical, legal, and operational issues.""",
        "leading": """Cross-functional participation is formalised, ensuring continuous input from diverse stakeholders and community representatives.""",
        "additional_guide": """Additional Guidance - Building Cross-Functional Collaboration

Diverse perspectives strengthen AI governance by identifying risks early and ensuring balanced decisions. To enhance participation:  
• **Form a Multi-Disciplinary Committee:** Include Legal, Risk, HR, Communications, IT, Data, and Service Delivery representatives.  
• **Define Roles and Input Points:** Clarify how each function contributes-e.g., Legal for compliance, HR for workforce impact, Communications for transparency.  
• **Embed Collaboration in Policy:** Mandate multi-departmental review for all new AI use cases.  
• **Encourage Inclusion:** Invite external advisors or community voices for projects affecting citizens directly.  
• **Track Participation:** Record attendance, decisions, and follow-up actions to demonstrate active engagement.  
Cross-functional governance promotes ethical awareness, builds organisational consensus, and ensures AI decisions reflect diverse expertise and stakeholder values.""",
        "evidence_types": """To comply with **GO-06 ("Ensure cross-functional participation in AI governance")**, provide artefacts showing that AI oversight involves multiple disciplines and perspectives.  
**Key Evidence Types:**  
• **Committee Composition:** Membership lists showing representation from Legal, HR, Risk, Technology, and community or diversity officers.  
• **Meeting Records:** Minutes evidencing cross-departmental discussions, ethical reviews, and decision-making processes.  
• **Policy References:** AI Policy or Governance Framework specifying multi-disciplinary review requirements.  
• **Consultation Logs:** Documentation of stakeholder or expert consultations during AI development or deployment.  
• **Training Records:** Cross-functional workshops or ethics training promoting shared understanding of AI governance.  
• **Outcome Reports:** Summaries showing how cross-functional feedback influenced AI decisions or mitigations.  
**In short:** show that AI governance is collaborative, structured, and consistently informed by multiple perspectives rather than confined to a single department.""",
    },
    {
        "code": """GO-07""",
        "text": """What mechanisms exist to monitor and review AI governance effectiveness?""",
        "explanation": """AI governance should evolve with organisational growth, regulatory updates, and emerging technologies. Without structured monitoring and review, policies and committees risk becoming outdated or symbolic. This question assesses whether your organisation regularly evaluates the effectiveness of its AI governance framework, identifies improvement areas, and acts on lessons learned.

Example: A council conducts an annual AI governance review aligned with ISO 42001. Findings are presented to the executive team, resulting in updated roles, training, and clearer reporting lines for AI accountability.""",
        "domain_order": 6,
        "order": 7,
        "foundational": """No formal process exists to monitor or review AI governance activities.""",
        "developing": """Reviews occur occasionally but lack clear metrics, documentation, or follow-up.""",
        "established": """Regular, structured reviews assess AI governance effectiveness, with findings tracked and reported.""",
        "leading": """Continuous monitoring uses defined KPIs, benchmarking, and audits to drive measurable governance improvement.""",
        "additional_guide": """Additional Guidance - Reviewing Governance Effectiveness

Periodic review ensures AI oversight remains relevant, evidence-based, and aligned with best practice. To strengthen monitoring:  
• **Define Review Frequency:** Conduct annual or bi-annual AI governance assessments tied to audit or risk cycles.  
• **Set Metrics and KPIs:** Track measures such as policy compliance, ethical review completion rates, and risk closure timelines.  
• **Benchmark Externally:** Compare performance against standards like ISO 42001, NIST AI RMF, or national AI assurance frameworks.  
• **Assign Responsibility:** Nominate a Risk, Compliance, or Governance function to coordinate reviews and track actions.  
• **Close the Loop:** Document recommendations, assign owners, and verify completion.  
Continuous improvement demonstrates accountability, ensures transparency, and keeps AI governance adaptive to organisational and regulatory change.""",
        "evidence_types": """To comply with **GO-07 ("Monitor and review AI governance effectiveness")**, provide documentation showing structured evaluation and improvement cycles.  
**Key Evidence Types:**  
• **Review Reports:** Formal AI governance evaluation or maturity-assessment reports with findings and action plans.  
• **Audit Records:** Internal or external audit results covering AI risk, ethics, or compliance controls.  
• **Performance Dashboards:** KPIs tracking policy compliance, training coverage, or issue remediation.  
• **Meeting Minutes:** Executive or committee records discussing governance performance and improvement outcomes.  
• **Action Registers:** Logs of corrective actions, owners, and completion status following governance reviews.  
• **Benchmarking Evidence:** Comparative analysis or certification aligning AI governance with recognised standards.  
**In short:** demonstrate that AI governance effectiveness is regularly assessed, results are documented, and improvements are actively implemented across the organisation.""",
    },
    {
        "code": """GO-08""",
        "text": """How does leadership ensure transparency and accountability in AI decision-making?""",
        "explanation": """Transparency and accountability are essential for building trust in AI-enabled decisions. Without clear visibility into how AI systems are used and who is responsible for their outcomes, organisations risk reputational damage and regulatory scrutiny. This question evaluates whether leadership promotes transparent reporting, traceability, and clear ownership of AI-related decisions and outcomes.

Example: A council publishes an annual “Responsible AI Report” outlining approved AI projects, ethical review results, and identified risks, ensuring public transparency and reinforcing leadership accountability.""",
        "domain_order": 6,
        "order": 8,
        "foundational": """AI decision-making lacks visibility; accountability and documentation are unclear.""",
        "developing": """Some AI reporting exists, but ownership of decisions and outcomes is inconsistent.""",
        "established": """Leadership maintains clear traceability of AI decisions and regularly communicates accountability outcomes.""",
        "leading": """Transparency and accountability are core principles, supported by public reporting, documented ethics reviews, and independent oversight.""",
        "additional_guide": """Additional Guidance - Promoting Transparency and Accountability

Transparency ensures stakeholders understand how AI is applied, while accountability clarifies who is responsible for outcomes. To strengthen both:  
• **Define Decision Ownership:** Assign accountable officers for every AI project, specifying who approves, monitors, and reports outcomes.  
• **Implement Audit Trails:** Maintain records of AI system approvals, performance monitoring, and ethical review outcomes.  
• **Publish Transparency Statements:** Regularly communicate AI use cases, purposes, and impacts to staff and the public.  
• **Integrate Ethical Oversight:** Require leadership or independent committees to review and sign off on high-impact AI systems.  
• **Report Outcomes:** Include AI governance metrics in annual or sustainability reports.  
Visible, well-documented accountability reinforces stakeholder trust and demonstrates a mature, responsible approach to AI governance.""",
        "evidence_types": """To comply with **GO-08 ("Ensure transparency and accountability in AI decision-making")**, provide artefacts proving leadership visibility, decision traceability, and public reporting.  
**Key Evidence Types:**  
• **Governance Policies:** Documents defining roles and accountabilities for AI-related decision-making.  
• **Decision Records:** Audit trails, approval logs, or AI system registries linking decisions to accountable officers.  
• **Transparency Reports:** Annual or public-facing reports disclosing AI usage, ethical reviews, and assurance results.  
• **Meeting Minutes:** Leadership or board minutes demonstrating oversight of AI impacts and accountability discussions.  
• **Performance Evidence:** Internal dashboards tracking decision ownership and incident resolution.  
• **External Assurance:** Independent reviews or certifications validating AI accountability practices.  
**In short:** demonstrate that AI-related decisions are traceable, leadership accountability is explicit, and stakeholders are informed through transparent and verifiable reporting mechanisms.""",
    },
    {
        "code": """PL-01""",
        "text": """How does the organisation identify and comply with privacy and data protection laws relevant to AI use?""",
        "explanation": """AI systems often process sensitive personal data, making legal compliance with privacy and data-protection requirements critical. Without formal processes, organisations risk breaching legislation and losing public trust. This question assesses whether privacy obligations—such as those under the Privacy Act 1988 (Cth) or international frameworks—are systematically identified, implemented, and reviewed within AI initiatives.

Example: A council maps all AI data flows against the Australian Privacy Principles (APPs), conducts Privacy Impact Assessments (PIAs), and maintains compliance evidence for audit readiness.""",
        "domain_order": 7,
        "order": 1,
        "foundational": """Privacy and data-protection requirements are not identified or applied to AI activities.""",
        "developing": """Some privacy obligations are addressed, but approaches vary across projects.""",
        "established": """Privacy laws and data-protection requirements are consistently identified, implemented, and monitored for AI projects.""",
        "leading": """A comprehensive compliance framework integrates privacy laws, regulatory changes, and AI-specific legal obligations organisation-wide.""",
        "additional_guide": """Additional Guidance - Managing AI Privacy and Legal Compliance

Compliance ensures lawful, ethical AI data use. To strengthen maturity:  
• **Map Legal Requirements:** Identify privacy and data-protection laws relevant to AI use cases.  
• **Conduct Privacy Impact Assessments (PIAs):** Assess data risks before deployment.  
• **Maintain Data Inventories:** Record what personal data is used, where it's stored, and how it's protected.  
• **Assign Accountability:** Nominate privacy officers responsible for AI compliance monitoring.  
• **Review Regularly:** Update processes as laws evolve (e.g., Privacy Act reforms, GDPR equivalents).  
• **Train Staff:** Ensure teams understand obligations under privacy legislation.  
Embedding privacy compliance in AI governance reduces legal exposure and reinforces community trust.""",
        "evidence_types": """To comply with **PL-01 ("Identify and comply with privacy and data protection laws for AI use")**, provide artefacts showing structured compliance management.  
**Key Evidence Types:**  
• **Compliance Registers:** Listings of applicable privacy and data-protection laws.  
• **Privacy Impact Assessments:** Completed PIAs for AI projects using personal data.  
• **Policies & Frameworks:** Privacy and Legal Compliance Frameworks referencing AI obligations.  
• **Audit Reports:** Independent assessments confirming privacy compliance.  
• **Training Records:** Evidence of staff awareness and compliance training.  
• **Monitoring Logs:** Ongoing tracking of legislative updates and implementation actions.  
**In short:** demonstrate that privacy and legal requirements are identified, documented, and embedded into every stage of AI system design and governance.""",
    },
    {
        "code": """PL-02""",
        "text": """How does the organisation manage consent and uphold individual rights when using personal data in AI systems?""",
        "explanation": """Managing consent and respecting individuals’ rights are central to lawful and ethical AI operation. Without clear consent mechanisms, AI systems may process data unlawfully or without transparency. This question assesses whether the organisation obtains, records, and manages consent appropriately, and whether individuals can access, correct, or withdraw their data used in AI applications.

Example: A council’s AI data platform includes built-in consent tracking, allowing residents to view, modify, or withdraw their data permissions at any time, in accordance with the Australian Privacy Principles.""",
        "domain_order": 7,
        "order": 2,
        "foundational": """Consent and data subject rights are not managed or documented for AI data use.""",
        "developing": """Some consent is collected, but rights management and withdrawal processes are inconsistent.""",
        "established": """Consent and individual rights processes are formalised, documented, and consistently applied to AI systems.""",
        "leading": """Comprehensive consent management integrates automated tracking, user access controls, and transparent withdrawal options.""",
        "additional_guide": """Additional Guidance - Managing Consent and Individual Rights

Strong consent management builds transparency and trust. To strengthen governance:  
• **Define Consent Requirements:** Align collection with APPs, GDPR, or equivalent standards.  
• **Use Informed Consent:** Explain how data is used in plain language.  
• **Track and Record:** Log consent, purpose, and withdrawal in a central system.  
• **Enable Individual Rights:** Allow access, correction, and deletion requests for AI-related data.  
• **Automate Workflows:** Use tools for consent versioning and withdrawal notifications.  
• **Educate Users and Staff:** Provide clarity on privacy rights and responsibilities.  
Embedding consent and rights management ensures compliance, fairness, and ethical data handling.""",
        "evidence_types": """To comply with **PL-02 ("Manage consent and uphold individual rights for AI systems")**, provide artefacts demonstrating structured consent and rights management.  
**Key Evidence Types:**  
• **Consent Policies:** Documents defining consent and rights procedures for AI use.  
• **Consent Logs:** Digital records tracking data subject permissions and withdrawals.  
• **Privacy Notices:** Clear communication of AI data-use purposes and rights.  
• **Access Request Records:** Logs of access, correction, or deletion requests handled.  
• **Training Records:** Staff education on privacy rights and consent requirements.  
• **Audit Reports:** Reviews confirming compliance with consent and rights obligations.  
**In short:** demonstrate that consent and individual rights are clearly defined, traceable, and actively managed across all AI data-handling processes.""",
    },
    {
        "code": """PL-03""",
        "text": """How does the organisation conduct legal reviews and ensure accountability for AI projects?""",
        "explanation": """AI introduces new legal risks, including liability for automated decisions, intellectual property, and discrimination. Without legal oversight, projects may violate existing laws or lack clear accountability. This question evaluates whether the organisation conducts structured legal reviews of AI initiatives and assigns accountability for ensuring compliance with contractual, ethical, and regulatory obligations.

Example: A council’s Legal Services team reviews all proposed AI projects using a dedicated checklist covering privacy, bias, transparency, and contract requirements before deployment approval.""",
        "domain_order": 7,
        "order": 3,
        "foundational": """AI projects are launched without legal review or clear accountability.""",
        "developing": """Legal input is sought occasionally but not consistently across projects.""",
        "established": """Formal legal review is required for all AI projects, with accountability documented in governance records.""",
        "leading": """Legal oversight is embedded in all AI governance processes, with ongoing monitoring, accountability tracking, and audit documentation.""",
        "additional_guide": """Additional Guidance - Ensuring Legal Oversight and Accountability

Legal review strengthens compliance and risk management. To improve maturity:  
• **Define Review Triggers:** Require legal review for all AI procurements, designs, and deployments.  
• **Use Checklists:** Assess privacy, liability, IP, and discrimination risks.  
• **Assign Legal Ownership:** Appoint accountable legal advisors or officers to each project.  
• **Maintain Documentation:** Record approvals, advice, and risk assessments.  
• **Collaborate Cross-Functionally:** Engage Legal, Risk, and Governance teams in project oversight.  
• **Conduct Periodic Reviews:** Update legal risk assessments as regulations evolve.  
Consistent legal oversight ensures AI projects are compliant, transparent, and defensible under current and emerging laws.""",
        "evidence_types": """To comply with **PL-03 ("Conduct legal reviews and ensure accountability for AI projects")**, provide documentation showing formal legal assessment and approval processes.  
**Key Evidence Types:**  
• **Legal Review Checklists:** Templates addressing privacy, IP, and discrimination risks.  
• **Approval Records:** Signed legal clearances or advice memos for AI projects.  
• **Policies & Procedures:** Governance policies requiring legal review prior to implementation.  
• **Governance Minutes:** Records showing legal input into AI project decisions.  
• **Accountability Registers:** Documentation linking legal officers to specific projects.  
• **Audit or Compliance Reports:** Verification that legal reviews are consistently performed.  
**In short:** demonstrate that all AI projects undergo structured legal review, with accountability clearly assigned and documented.""",
    },
    {
        "code": """PL-04""",
        "text": """How does the organisation monitor and adapt to emerging AI regulations and compliance requirements?""",
        "explanation": """AI regulations are evolving rapidly across jurisdictions. Without continuous monitoring, the organisation may fail to meet new legal or ethical obligations. This question assesses whether the organisation tracks emerging AI-specific laws, standards, and guidelines—and updates policies, processes, and risk assessments accordingly.

Example: A council’s Compliance team maintains a legislative tracker that monitors new AI-related policies, including Australia’s Safe and Responsible AI Framework, and updates internal procedures to ensure ongoing regulatory compliance.""",
        "domain_order": 7,
        "order": 4,
        "foundational": """The organisation is unaware of or unprepared for emerging AI regulations.""",
        "developing": """Some monitoring occurs, but updates to policies and processes are ad hoc.""",
        "established": """Emerging AI regulations are tracked and regularly incorporated into governance frameworks.""",
        "leading": """A proactive compliance program continuously scans, analyses, and embeds new regulatory and ethical requirements across the organisation.""",
        "additional_guide": """Additional Guidance - Monitoring and Adapting to AI Regulations

Staying informed ensures the organisation remains legally and ethically aligned. To strengthen processes:  
• **Establish Monitoring Functions:** Assign responsibility to Legal, Risk, or Compliance teams.  
• **Use Trusted Sources:** Monitor updates from government, standards bodies (ISO, NIST), and regulators.  
• **Maintain a Regulatory Register:** Record relevant laws, guidelines, and response actions.  
• **Update Frameworks:** Revise AI governance, risk, and privacy policies as new requirements emerge.  
• **Engage Externally:** Participate in regulatory consultations or industry forums.  
• **Communicate Internally:** Share updates and train staff on new obligations.  
Proactive monitoring ensures compliance readiness and builds organisational resilience in a shifting regulatory landscape.""",
        "evidence_types": """To comply with **PL-04 ("Monitor and adapt to emerging AI regulations and compliance requirements")**, provide artefacts showing ongoing tracking and integration processes.  
**Key Evidence Types:**  
• **Regulatory Registers:** Logs tracking AI-related laws, standards, and policy updates.  
• **Compliance Reports:** Summaries of actions taken to address new regulations.  
• **Policy Updates:** Records of revised policies or frameworks reflecting emerging obligations.  
• **Training Materials:** Staff communications or sessions explaining regulatory changes.  
• **Meeting Minutes:** Evidence of governance or compliance discussions on AI regulation.  
• **External Engagement Records:** Participation in policy consultations or industry forums.  
**In short:** demonstrate that AI regulatory developments are actively monitored, assessed, and incorporated into governance and compliance frameworks.""",
    },
    {
        "code": """PL-05""",
        "text": """How does the organisation ensure third-party AI vendors comply with privacy, legal, and ethical requirements?""",
        "explanation": """Third-party AI vendors often process or access sensitive data, creating potential compliance and reputational risks. Without strong oversight, vendor practices may breach privacy laws or ethical standards. This question assesses whether the organisation enforces privacy, security, and legal requirements through procurement, contracts, and ongoing assurance processes.

Example: A council includes privacy and ethical compliance clauses in all AI vendor contracts, requiring independent audit certification and annual reporting on adherence to privacy and data-protection obligations.""",
        "domain_order": 7,
        "order": 5,
        "foundational": """No privacy or compliance requirements are applied to third-party AI vendors.""",
        "developing": """Some contractual clauses exist but oversight and verification are limited.""",
        "established": """AI vendor agreements include defined privacy, legal, and ethical compliance obligations with periodic assurance.""",
        "leading": """A comprehensive third-party compliance framework enforces contractual safeguards, audits, and continuous monitoring for all AI vendors.""",
        "additional_guide": """Additional Guidance - Governing Vendor Privacy and Legal Compliance

Effective third-party management reduces compliance risk and ensures ethical consistency. To strengthen oversight:  
• **Embed Requirements in Contracts:** Include clauses for privacy, ethics, and regulatory compliance.  
• **Conduct Due Diligence:** Assess vendor compliance maturity before procurement.  
• **Mandate Independent Audits:** Require certifications such as ISO 27001, SOC 2, or AI ethics attestations.  
• **Monitor Continuously:** Review vendor reports and performance annually.  
• **Establish Escalation Processes:** Define corrective actions for non-compliance.  
• **Align with Organisational Policy:** Ensure third-party governance reflects internal AI and privacy standards.  
Comprehensive vendor compliance ensures consistent legal, ethical, and data-protection practices across the AI supply chain.""",
        "evidence_types": """To comply with **PL-05 ("Ensure third-party AI vendors comply with privacy, legal, and ethical requirements")**, provide artefacts confirming structured vendor governance and verification.  
**Key Evidence Types:**  
• **Vendor Contracts:** Clauses specifying privacy, security, and ethics obligations.  
• **Due Diligence Reports:** Assessments of vendor compliance and risk profiles.  
• **Audit Certificates:** External assurance (e.g., ISO, SOC, privacy compliance).  
• **Monitoring Logs:** Records of vendor performance reviews and compliance checks.  
• **Procurement Policies:** Guidelines for AI-specific third-party risk management.  
• **Remediation Records:** Actions taken in response to vendor non-compliance.  
**In short:** demonstrate that AI vendor relationships are governed through enforceable contracts, assurance mechanisms, and continuous compliance monitoring.""",
    },
    {
        "code": """PL-06""",
        "text": """How does the organisation manage intellectual property (IP) rights for AI systems and their outputs?""",
        "explanation": """AI systems may generate or rely on content, code, or datasets subject to intellectual property rights. Without clear ownership and licensing processes, the organisation risks infringement or disputes over AI-generated outputs. This question evaluates whether IP rights are identified, documented, and managed across the AI lifecycle—from data acquisition to deployment and commercialisation.

Example: A council ensures all AI models and datasets undergo IP review before deployment, confirming licensing terms for training data and clarifying ownership of generated insights or outputs.""",
        "domain_order": 7,
        "order": 6,
        "foundational": """IP ownership and licensing are unmanaged or undocumented for AI projects.""",
        "developing": """Some IP reviews occur, but coverage and documentation are inconsistent.""",
        "established": """IP rights are identified, reviewed, and documented for all AI systems and outputs.""",
        "leading": """Comprehensive IP governance covers data, algorithms, and AI-generated outputs, supported by regular audits and legal oversight.""",
        "additional_guide": """Additional Guidance - Managing IP in AI Systems

Clear IP management prevents infringement and ensures proper attribution. To enhance maturity:  
• **Identify IP Assets:** Catalogue all data, models, and outputs with potential IP implications.  
• **Review Licensing Terms:** Verify dataset and software licences permit intended AI use.  
• **Clarify Ownership:** Define who owns AI-generated outputs, including code, insights, or models.  
• **Engage Legal Counsel:** Require IP review for AI procurements, partnerships, or contracts.  
• **Document and Track:** Maintain an IP register for AI-related assets.  
• **Educate Teams:** Provide training on copyright, open data, and AI content ownership.  
Effective IP governance protects the organisation's rights and mitigates legal exposure.""",
        "evidence_types": """To comply with **PL-06 ("Manage intellectual property rights for AI systems and outputs")**, provide documentation showing structured IP governance.  
**Key Evidence Types:**  
• **IP Register:** Records listing AI models, datasets, and related ownership details.  
• **Licensing Agreements:** Contracts confirming data and software usage rights.  
• **Legal Review Reports:** Evidence of IP due diligence for AI projects.  
• **Policies & Procedures:** Intellectual Property or AI Governance Policy covering IP management.  
• **Audit Findings:** Reviews verifying compliance with licensing and ownership requirements.  
• **Training Materials:** Staff awareness programs on IP responsibilities in AI development.  
**In short:** demonstrate that all AI assets and outputs are governed by clear, documented IP ownership and licensing frameworks.""",
    },
    {
        "code": """PL-07""",
        "text": """How does the organisation identify, manage, and respond to legal risks or incidents involving AI systems?""",
        "explanation": """AI incidents—such as bias, system failure, or misuse—can create legal liability and reputational harm. Without a defined legal risk and response framework, the organisation may struggle to manage disputes or regulatory investigations. This question evaluates whether legal risks are systematically identified, monitored, and managed through documented escalation and incident response processes.

Example: A council integrates AI-specific legal risks into its enterprise risk register and activates an incident response plan when potential breaches occur, coordinating between Legal, Risk, and IT teams to resolve issues and notify affected parties.""",
        "domain_order": 7,
        "order": 7,
        "foundational": """Legal risks and incidents related to AI are unmanaged or handled reactively.""",
        "developing": """Some legal risk management occurs, but processes are ad hoc or incomplete.""",
        "established": """Defined frameworks exist for identifying and responding to AI-related legal risks and incidents.""",
        "leading": """A proactive legal risk program integrates monitoring, rapid response, and regulatory reporting mechanisms across all AI operations.""",
        "additional_guide": """Additional Guidance - Managing AI Legal Risks and Incidents

Preparedness minimises liability and supports rapid recovery. To strengthen processes:  
• **Integrate Legal Risk into ERM:** Classify AI-related legal exposures (bias, misuse, data breach).  
• **Establish Escalation Protocols:** Define steps for notification, investigation, and response.  
• **Coordinate Functions:** Engage Legal, Risk, Privacy, and IT in joint response teams.  
• **Maintain Documentation:** Record root cause analyses and resolution outcomes.  
• **Engage Regulators Early:** Notify authorities as required by law.  
• **Review and Learn:** Incorporate lessons into updated governance frameworks.  
A defined legal risk and response structure ensures accountability and resilience following AI-related incidents.""",
        "evidence_types": """To comply with **PL-07 ("Identify, manage, and respond to legal risks or incidents involving AI")**, provide artefacts demonstrating structured legal risk management and escalation.  
**Key Evidence Types:**  
• **Incident Response Plans:** AI-specific legal or regulatory response procedures.  
• **Risk Registers:** Entries capturing AI-related legal exposures.  
• **Investigation Reports:** Documentation of incident handling and corrective actions.  
• **Governance Records:** Meeting minutes showing legal risk discussions or escalations.  
• **Regulatory Notifications:** Copies of formal reports or notifications to oversight bodies.  
• **Audit Findings:** Reviews assessing effectiveness of legal incident management.  
**In short:** demonstrate that AI legal risks are proactively identified, tracked, and managed through coordinated, well-documented response processes.""",
    },
    {
        "code": """PL-08""",
        "text": """How does the organisation maintain recordkeeping, auditability, and evidence preservation for AI systems?""",
        "explanation": """Robust recordkeeping ensures AI decisions, data use, and compliance actions can be audited and defended. Without proper documentation, the organisation may be unable to demonstrate accountability or respond to legal, regulatory, or public scrutiny. This question assesses whether records of AI design, data handling, decisions, and reviews are maintained in accordance with legal and organisational requirements.

Example: A council maintains an AI Audit Log capturing all training datasets, model configurations, and decision records, with retention aligned to the Queensland Public Records Act 2002 and internal governance policies.""",
        "domain_order": 7,
        "order": 8,
        "foundational": """AI-related records are incomplete, inconsistent, or not retained.""",
        "developing": """Some AI documentation exists, but auditability and retention are ad hoc.""",
        "established": """Structured recordkeeping supports auditability and traceability across AI systems.""",
        "leading": """Comprehensive recordkeeping ensures full traceability, evidentiary integrity, and compliance with legal and audit standards.""",
        "additional_guide": """Additional Guidance - Ensuring AI Recordkeeping and Auditability

Accurate, secure records demonstrate accountability and support transparency. To strengthen governance:  
• **Define Record Requirements:** Identify documentation to be retained for each AI project (e.g., data sources, model logic, decisions).  
• **Follow Legal Obligations:** Align with public records or evidence laws (e.g., Records Act, Privacy Act).  
• **Maintain Audit Logs:** Track access, changes, and system activities.  
• **Secure Storage:** Use tamper-evident repositories with controlled access.  
• **Enable Traceability:** Link records across datasets, models, and outcomes.  
• **Schedule Reviews:** Periodically verify completeness and retention compliance.  
Effective recordkeeping ensures AI decisions are explainable, verifiable, and legally defensible.""",
        "evidence_types": """To comply with **PL-08 ("Maintain recordkeeping, auditability, and evidence preservation for AI systems")**, provide artefacts showing structured, secure documentation practices.  
**Key Evidence Types:**  
• **Records Management Policy:** Guidelines covering AI-related data and decision documentation.  
• **Audit Logs:** System-generated logs of access, changes, and decision events.  
• **Retention Schedules:** Legal or organisational requirements for record duration.  
• **Storage Evidence:** Proof of secure, tamper-proof data repositories.  
• **Audit Reports:** Reviews assessing completeness and traceability of AI records.  
• **Training Materials:** Staff guidance on AI documentation and audit compliance.  
**In short:** demonstrate that all AI systems maintain structured, secure, and verifiable records suitable for legal, ethical, and operational accountability.""",
    },
    {
        "code": """RS-01""",
        "text": """How does the organisation ensure AI systems are reliable, robust, and perform consistently under expected conditions?""",
        "explanation": """Reliability ensures AI systems function as intended, producing stable and accurate outcomes over time. Without validation and performance monitoring, AI tools may generate inconsistent or unsafe results. This question assesses whether the organisation defines, tests, and verifies AI reliability through structured design, validation, and operational controls.

Example: A council tests its AI traffic-optimisation system across varying data inputs and environmental conditions to ensure consistent performance before integrating it into live traffic control systems.""",
        "domain_order": 8,
        "order": 1,
        "foundational": """AI reliability is assumed but not tested or documented.""",
        "developing": """Some testing occurs, but validation and monitoring lack structure or consistency.""",
        "established": """Reliability is defined and verified through documented testing, validation, and ongoing performance monitoring.""",
        "leading": """Reliability engineering principles and continuous validation are embedded across all AI systems, supported by automated testing and assurance frameworks.""",
        "additional_guide": """Additional Guidance - Building Reliable and Robust AI Systems

Reliability underpins safety, trust, and performance assurance. To strengthen reliability practices:  
• **Define Reliability Criteria:** Establish expected performance thresholds and uptime targets.  
• **Conduct Rigorous Testing:** Validate AI across varied data, scenarios, and edge conditions.  
• **Implement Monitoring Systems:** Track real-time performance and error rates.  
• **Plan for Failures:** Include fallback modes and safe shutdown mechanisms.  
• **Document Results:** Maintain validation reports and reliability benchmarks.  
• **Continuously Improve:** Reassess reliability after updates, retraining, or data changes.  
Systematic reliability assurance ensures AI operates consistently and predictably in all intended environments.""",
        "evidence_types": """To comply with **RS-01 ("Ensure AI systems are reliable, robust, and perform consistently")**, provide artefacts showing defined testing and assurance activities.  
**Key Evidence Types:**  
• **Testing Reports:** Documentation of validation, stress, and reliability testing.  
• **Policies & Frameworks:** AI Reliability or Quality Assurance Frameworks.  
• **Monitoring Dashboards:** Real-time system performance tracking.  
• **Incident Logs:** Records of system errors, failures, and resolutions.  
• **Maintenance Records:** Logs showing retraining or recalibration cycles.  
• **Audit Findings:** Reviews verifying AI reliability controls and outcomes.  
**In short:** demonstrate that AI systems are rigorously tested, continuously monitored, and consistently perform to defined reliability standards.""",
    },
    {
        "code": """RS-02""",
        "text": """How does the organisation validate and assure the quality of AI systems before deployment?""",
        "explanation": """Validation confirms that AI systems meet their intended purpose and perform accurately, safely, and reliably. Without structured quality assurance, undetected errors can lead to poor performance, ethical breaches, or safety incidents. This question assesses whether the organisation conducts systematic validation and quality assurance (QA) testing before AI systems are approved for live use.

Example: A council’s AI Governance Framework mandates pre-deployment validation that includes accuracy, bias, explainability, and performance testing, with results reviewed and signed off by the AI Assurance Committee.""",
        "domain_order": 8,
        "order": 2,
        "foundational": """AI systems are deployed with minimal or no formal validation or quality checks.""",
        "developing": """Some testing occurs pre-deployment, but scope and documentation are inconsistent.""",
        "established": """Formal validation and QA testing are conducted before deployment, with documented results and approvals.""",
        "leading": """Comprehensive, risk-based AI assurance integrates validation, peer review, and independent audit prior to deployment.""",
        "additional_guide": """Additional Guidance - Validating and Assuring AI Quality

Structured validation ensures AI systems are safe, effective, and compliant. To mature assurance practices:  
• **Define QA Criteria:** Establish validation requirements for accuracy, fairness, and robustness.  
• **Test Against Objectives:** Confirm models meet operational and ethical expectations.  
• **Use Independent Review:** Engage internal or external reviewers for critical systems.  
• **Document Evidence:** Maintain validation results, sign-offs, and version control.  
• **Adopt Risk-Based Testing:** Apply more rigorous assurance to higher-impact systems.  
• **Integrate Governance:** Link QA reviews with project approval gates.  
Validation before deployment ensures AI quality, reliability, and stakeholder confidence.""",
        "evidence_types": """To comply with **RS-02 ("Validate and assure AI system quality before deployment")**, provide artefacts showing structured QA and validation processes.  
**Key Evidence Types:**  
• **Validation Reports:** Documentation of test results, success criteria, and approvals.  
• **QA Frameworks:** Policies defining validation and sign-off processes for AI systems.  
• **Testing Logs:** Records of model performance, reliability, and fairness testing.  
• **Approval Records:** Evidence of pre-deployment governance or committee review.  
• **Independent Reviews:** Third-party or peer assurance reports.  
• **Change Control Records:** Documentation of version testing and sign-off.  
**In short:** demonstrate that AI systems are thoroughly validated and quality-assured before release into production environments.""",
    },
    {
        "code": """RS-03""",
        "text": """How does the organisation monitor AI system performance and detect incidents or anomalies post-deployment?""",
        "explanation": """AI systems can degrade or behave unpredictably over time due to changing data, user behaviour, or environmental factors. Without continuous monitoring, these issues may go unnoticed, leading to performance drift or harm. This question assesses whether the organisation has defined processes, tools, and escalation pathways to detect and respond to AI anomalies or failures in real time.

Example: A council deploys continuous monitoring dashboards for its AI-based resource allocation tool, automatically flagging anomalies in prediction accuracy or data quality and triggering incident alerts to system owners.""",
        "domain_order": 8,
        "order": 3,
        "foundational": """AI systems are not monitored for performance or anomalies after deployment.""",
        "developing": """Monitoring occurs manually or periodically, with limited incident detection.""",
        "established": """AI performance is continuously monitored, with defined thresholds and escalation procedures.""",
        "leading": """Automated monitoring and real-time alerting detect anomalies and trigger structured incident responses across all AI systems.""",
        "additional_guide": """Additional Guidance - Monitoring AI Performance and Detecting Incidents

Continuous monitoring ensures AI reliability, safety, and accountability. To enhance maturity:  
• **Define Monitoring Metrics:** Track accuracy, precision, recall, and data drift indicators.  
• **Automate Detection:** Use dashboards or AIOps tools for real-time anomaly alerts.  
• **Set Escalation Criteria:** Define triggers for review, rollback, or incident response.  
• **Document Findings:** Maintain logs of detected issues and resolutions.  
• **Integrate Governance:** Link incident alerts to risk and assurance committees.  
• **Review Regularly:** Reassess thresholds as models evolve.  
Monitoring safeguards against silent degradation and strengthens confidence in AI performance.""",
        "evidence_types": """To comply with **RS-03 ("Monitor AI performance and detect incidents post-deployment")**, provide artefacts demonstrating structured monitoring and response mechanisms.  
**Key Evidence Types:**  
• **Monitoring Dashboards:** Tools tracking real-time performance and anomaly detection.  
• **Incident Logs:** Records of detected issues, resolutions, and root-cause analyses.  
• **Policies & Procedures:** AI Monitoring or Incident Detection Policy defining responsibilities.  
• **Alert Records:** Notifications and escalation logs from automated monitoring systems.  
• **Performance Reports:** Periodic summaries of AI performance and corrective actions.  
• **Audit Findings:** Independent reviews confirming monitoring effectiveness.  
**In short:** demonstrate that AI performance is continuously monitored, anomalies are detected early, and incidents are managed through structured, documented processes.""",
    },
    {
        "code": """RS-04""",
        "text": """How does the organisation ensure AI systems are resilient and include redundancy or fail-safe mechanisms?""",
        "explanation": """AI system resilience ensures continuity and safety when failures, cyberattacks, or abnormal conditions occur. Without redundancy or fail-safes, system disruptions can lead to service outages, incorrect outputs, or harm to users. This question assesses whether the organisation designs AI systems with built-in recovery, backup, and fallback mechanisms to maintain safe operations.

Example: A council’s predictive maintenance AI includes automated failover to manual control during network loss, ensuring uninterrupted service for public infrastructure monitoring.""",
        "domain_order": 8,
        "order": 4,
        "foundational": """AI systems have no resilience or recovery measures; failures cause service disruption.""",
        "developing": """Some recovery measures exist but lack full testing or consistency across systems.""",
        "established": """AI systems include defined redundancy, backup, and fail-safe mechanisms tested periodically.""",
        "leading": """Comprehensive resilience frameworks ensure continuous operation, automated recovery, and proven fail-safe testing across all AI deployments.""",
        "additional_guide": """Additional Guidance - Building AI Resilience and Fail-Safe Mechanisms

Resilience protects system integrity and user safety. To enhance resilience:  
• **Design for Continuity:** Incorporate redundancy and backup capabilities into AI architectures.  
• **Implement Fail-Safes:** Enable systems to revert to manual or default modes when failures occur.  
• **Conduct Recovery Testing:** Simulate outages and validate response times.  
• **Secure Backup Data:** Maintain encrypted, verified backups for critical datasets.  
• **Automate Alerts:** Notify operators of failures or fallback activations.  
• **Document Procedures:** Record test outcomes and recovery actions.  
Resilient AI systems minimise disruption and maintain public trust during adverse events.""",
        "evidence_types": """To comply with **RS-04 ("Ensure AI systems are resilient and include redundancy or fail-safe mechanisms")**, provide documentation demonstrating resilience design and testing.  
**Key Evidence Types:**  
• **Resilience Framework:** Policy defining redundancy, continuity, and fail-safe requirements.  
• **Architecture Diagrams:** Documentation of backup and recovery components.  
• **Testing Reports:** Results from resilience and failover simulations.  
• **Incident Logs:** Records of fail-safe activations and responses.  
• **Backup Records:** Evidence of data replication and restoration testing.  
• **Audit Findings:** Independent reviews confirming operational resilience.  
**In short:** demonstrate that AI systems are designed, tested, and verified to continue operating safely under failure or disruption conditions.""",
    },
    {
        "code": """RS-05""",
        "text": """How does the organisation detect and manage model drift or system degradation in AI performance over time?""",
        "explanation": """Model drift occurs when AI performance declines due to changes in data, behaviour, or operating environments. Without monitoring and retraining, decisions may become inaccurate or unsafe. This question assesses whether the organisation actively tracks model performance, detects drift, and applies retraining or recalibration strategies to maintain reliability.

Example: A council’s AI demand-forecasting model is monitored monthly for data drift indicators. When accuracy falls below the defined threshold, the system automatically triggers retraining using updated datasets and validation testing.""",
        "domain_order": 8,
        "order": 5,
        "foundational": """No monitoring for model drift or degradation is in place.""",
        "developing": """Performance is reviewed occasionally but without defined drift thresholds.""",
        "established": """Regular monitoring detects drift using defined metrics and triggers retraining processes.""",
        "leading": """Automated drift detection and adaptive retraining maintain continuous model reliability and compliance.""",
        "additional_guide": """Additional Guidance - Managing Model Drift and Degradation

Drift management sustains accuracy and accountability. To improve maturity:  
• **Define Drift Metrics:** Monitor accuracy, input data distribution, and prediction variance.  
• **Set Thresholds:** Establish acceptable performance limits and trigger points for review.  
• **Automate Detection:** Use dashboards or MLOps pipelines for continuous monitoring.  
• **Retrain Responsively:** Update models with new or corrected data when drift is detected.  
• **Validate Retrained Models:** Confirm improved performance before redeployment.  
• **Document Changes:** Record drift detection, retraining, and testing outcomes.  
Active drift management ensures models remain reliable, transparent, and safe over time.""",
        "evidence_types": """To comply with **RS-05 ("Detect and manage model drift or system degradation")**, provide documentation showing structured drift monitoring and maintenance processes.  
**Key Evidence Types:**  
• **Monitoring Dashboards:** Tools tracking accuracy, input data changes, and output variance.  
• **Threshold Definitions:** Documentation of drift criteria and retraining triggers.  
• **Retraining Logs:** Records of model updates and version control.  
• **Validation Reports:** Results confirming restored performance post-retraining.  
• **Policies & Procedures:** Model Lifecycle Management or MLOps Governance documents.  
• **Audit Findings:** Reviews verifying adherence to drift management protocols.  
**In short:** demonstrate that AI model performance is continuously tracked, drift is promptly detected, and models are retrained or recalibrated to maintain operational reliability.""",
    },
    {
        "code": """RS-06""",
        "text": """How does the organisation assess and mitigate safety risks associated with AI systems?""",
        "explanation": """AI systems can introduce safety risks if they malfunction, behave unpredictably, or produce harmful outcomes. Without formal safety assessments, such risks may remain undetected until an incident occurs. This question evaluates whether the organisation conducts structured safety risk assessments, identifies potential hazards, and applies controls to protect users, staff, and the community.

Example: A council conducts a safety risk assessment for its AI-enabled traffic management system, modelling potential failure scenarios and implementing automatic overrides to prevent unsafe signal changes.""",
        "domain_order": 8,
        "order": 6,
        "foundational": """AI safety risks are not identified or assessed.""",
        "developing": """Some safety risks are considered, but assessments are informal or incomplete.""",
        "established": """Formal safety risk assessments and mitigations are conducted for all AI projects.""",
        "leading": """A comprehensive AI safety framework integrates hazard analysis, mitigation planning, and continuous risk monitoring.""",
        "additional_guide": """Additional Guidance - Assessing and Mitigating AI Safety Risks

Safety assurance is vital for protecting people and critical operations. To enhance maturity:  
• **Identify Hazards:** Map potential safety impacts from AI errors, misuse, or failure.  
• **Conduct Structured Assessments:** Use risk matrices or hazard analysis methods (e.g., FMEA, Bowtie).  
• **Implement Controls:** Introduce technical and procedural safeguards (redundancies, alerting, overrides).  
• **Review Periodically:** Reassess safety risks during retraining or system updates.  
• **Engage Experts:** Involve safety engineers or domain specialists in assessments.  
• **Document Outcomes:** Maintain safety case files and mitigation records.  
Structured risk assessment ensures AI systems operate safely and responsibly.""",
        "evidence_types": """To comply with **RS-06 ("Assess and mitigate safety risks associated with AI systems")**, provide documentation demonstrating structured risk identification and control processes.  
**Key Evidence Types:**  
• **Safety Risk Assessments:** Reports identifying hazards, likelihoods, and mitigations.  
• **Safety Frameworks:** Policies defining AI safety assurance requirements.  
• **Control Documentation:** Records of implemented safety features or overrides.  
• **Incident Logs:** Evidence of safety-related events and corrective actions.  
• **Expert Reviews:** Independent safety evaluations or certification reports.  
• **Audit Findings:** Reviews confirming safety assurance compliance.  
**In short:** demonstrate that AI safety risks are systematically assessed, mitigated, and reviewed to prevent harm and ensure safe operation across all environments.""",
    },
    {
        "code": """RS-07""",
        "text": """How does the organisation test and validate AI systems under adverse or edge conditions?""",
        "explanation": """AI systems must remain stable when exposed to unusual, extreme, or unexpected inputs. Without testing for edge cases, systems may fail or behave unpredictably under real-world stress. This question assesses whether the organisation conducts stress testing, scenario modelling, and edge-condition validation to confirm AI robustness and safe recovery behaviour.

Example: A council tests its AI-based flood prediction model using synthetic extreme weather data and historical anomalies to confirm reliability under rare but high-impact conditions.""",
        "domain_order": 8,
        "order": 7,
        "foundational": """AI systems are not tested for performance under adverse or edge conditions.""",
        "developing": """Some stress testing occurs, but methods and coverage are inconsistent.""",
        "established": """AI systems undergo structured stress and scenario testing before deployment.""",
        "leading": """Comprehensive validation includes automated stress testing, edge-case simulation, and resilience benchmarking across all critical AI systems.""",
        "additional_guide": """Additional Guidance - Testing AI Under Adverse Conditions

Robust testing ensures AI reliability in real-world scenarios. To strengthen maturity:  
• **Identify Edge Cases:** Analyse potential outlier scenarios, extreme values, or environmental anomalies.  
• **Simulate Adverse Conditions:** Use synthetic or historical data to model unusual events.  
• **Conduct Stress Testing:** Evaluate AI performance under high data loads or degraded inputs.  
• **Validate Recovery Mechanisms:** Confirm systems return to safe, stable states after disruption.  
• **Document Test Results:** Record outcomes, thresholds, and corrective actions.  
• **Repeat Periodically:** Retest after system updates or retraining.  
Edge-condition testing ensures AI remains safe, resilient, and predictable under all circumstances.""",
        "evidence_types": """To comply with **RS-07 ("Test and validate AI systems under adverse or edge conditions")**, provide artefacts showing structured resilience and stress testing.  
**Key Evidence Types:**  
• **Test Plans:** Documentation of edge-condition and stress-test methodologies.  
• **Simulation Data:** Synthetic datasets used to model extreme or rare events.  
• **Testing Reports:** Results of adverse-condition validation and corrective actions.  
• **Recovery Logs:** Evidence of system recovery and fail-safe activation.  
• **Frameworks & Policies:** AI Testing or Reliability Framework referencing edge-case validation.  
• **Audit Findings:** Independent reviews confirming adequacy of robustness testing.  
**In short:** demonstrate that AI systems are tested and validated under extreme, rare, or unexpected conditions to ensure safe and reliable operation.""",
    },
    {
        "code": """RS-08""",
        "text": """How does the organisation review and improve AI reliability and safety based on incidents and lessons learned?""",
        "explanation": """Continuous improvement ensures AI reliability and safety evolve with new insights, incidents, and technologies. Without structured review processes, lessons from failures or near-misses may be lost, allowing risks to recur. This question assesses whether the organisation systematically analyses AI incidents, captures lessons learned, and updates policies, models, or controls accordingly.

Example: A council’s AI Safety Committee reviews every AI-related incident and publishes a quarterly “Lessons Learned Report,” outlining corrective actions and updates to the AI Governance and Reliability Framework.""",
        "domain_order": 8,
        "order": 8,
        "foundational": """AI incidents are not reviewed or used to improve reliability and safety.""",
        "developing": """Some post-incident reviews occur, but lessons are not systematically applied.""",
        "established": """AI incidents are reviewed, with outcomes informing model improvements and governance updates.""",
        "leading": """Continuous improvement processes embed lessons learned into all AI systems, supported by trend analysis and ongoing framework refinement.""",
        "additional_guide": """Additional Guidance - Learning from AI Incidents and Near Misses

Structured review and improvement strengthen AI safety culture. To mature your process:  
• **Establish Review Protocols:** Define processes for analysing AI incidents and failures.  
• **Capture Root Causes:** Identify contributing factors such as data, design, or oversight gaps.  
• **Implement Corrective Actions:** Apply findings to update systems and controls.  
• **Document and Share:** Record outcomes in lessons-learned registers and communicate organisation-wide.  
• **Track Trends:** Monitor recurring issues to prioritise long-term improvements.  
• **Review Policies:** Update AI reliability and safety frameworks based on evidence.  
Systematic learning drives resilience, maturity, and continuous improvement across all AI operations.""",
        "evidence_types": """To comply with **RS-08 ("Review and improve AI reliability and safety based on incidents and lessons learned")**, provide artefacts demonstrating structured learning and continuous improvement processes.  
**Key Evidence Types:**  
• **Lessons Learned Registers:** Records of incidents, causes, and improvement actions.  
• **Incident Review Reports:** Documentation of analyses and corrective measures.  
• **Policy Updates:** Revised reliability or safety frameworks incorporating findings.  
• **Meeting Minutes:** Evidence of committee review and approval of improvements.  
• **Trend Analyses:** Aggregated reports highlighting recurring issues or improvements.  
• **Audit Findings:** Independent reviews verifying implementation of lessons learned.  
**In short:** demonstrate that AI reliability and safety continuously improve through systematic review, documented learning, and proactive governance updates.""",
    },
    {
        "code": """RM-01""",
        "text": """How are AI-related risks identified and categorised within the organisation’s risk management framework?""",
        "explanation": """AI introduces ethical, technical, operational, and reputational risks that may not fit neatly within traditional risk frameworks. This question assesses whether the organisation systematically identifies, defines, and categorises AI-specific risks—such as bias, data drift, explainability gaps, and regulatory non-compliance—within its enterprise risk management (ERM) processes.

Example: A council expands its corporate risk taxonomy to include “AI and Algorithmic Risk,” defining risk types such as model bias, automation failure, and privacy breach, ensuring AI exposures are visible alongside financial or cyber risks.""",
        "domain_order": 9,
        "order": 1,
        "foundational": """AI risks are not explicitly defined or captured in risk registers.""",
        "developing": """Some AI risks are documented informally but lack consistent categorisation or ownership.""",
        "established": """AI risks are formally defined within the enterprise risk framework, with categories, owners, and controls identified.""",
        "leading": """AI risk taxonomy is embedded organisation-wide, reviewed regularly, and aligned to frameworks such as NIST AI RMF or ISO 42001.""",
        "additional_guide": """Additional Guidance - Identifying and Categorising AI Risks

Integrating AI risk into existing ERM processes ensures consistent oversight and accountability. To mature your approach:  
• **Define AI Risk Categories:** Include ethical bias, data integrity, model accuracy, regulatory compliance, and reputational impact.  
• **Standardise Terminology:** Align categories and likelihood/impact scoring with enterprise risk matrices.  
• **Assign Ownership:** Nominate accountable executives for each AI risk class and maintain a cross-functional risk register.  
• **Use Scenario Analysis:** Evaluate "what-if" outcomes-e.g., erroneous automated decisions, data leakage, or discrimination.  
• **Link to Controls:** Map AI risks to mitigating policies, controls, and monitoring mechanisms.  
• **Review Regularly:** Re-assess categories annually or following major regulatory or technological changes.  
Formal categorisation helps leadership quantify AI exposure and direct resources effectively.""",
        "evidence_types": """To comply with **RM-01 ("Identify and categorise AI risks")**, provide documentation showing AI-specific risks are defined and integrated into enterprise risk practices.  
**Key Evidence Types:**  
• **Risk Registers:** Updated registers with explicit AI categories, risk descriptions, impact ratings, and assigned owners.  
• **Policies & Frameworks:** Enterprise Risk Management Policy or AI Risk Framework referencing AI-specific taxonomy.  
• **Risk Assessment Templates:** Standard forms including AI-related fields or checkboxes.  
• **Governance Artefacts:** Committee minutes discussing AI risk identification or categorisation updates.  
• **Guidance Documents:** Internal definitions or examples of AI risk types distributed to departments.  
• **Review Records:** Audit or assurance reports validating completeness of AI risk coverage.  
**In short:** show that AI risks are formally recognised, consistently described, and embedded into the same system used for managing all organisational risks.""",
    },
    {
        "code": """RM-02""",
        "text": """How are AI-related risks assessed and evaluated for likelihood and impact?""",
        "explanation": """AI risks vary widely—from technical failures and data bias to reputational and legal impacts. A structured assessment process helps quantify these risks and determine appropriate mitigation. This question evaluates whether the organisation applies consistent methods to assess AI risk likelihood and consequence using measurable criteria aligned with enterprise standards.

Example: A council applies its existing corporate risk matrix to evaluate AI risks, rating potential data-bias incidents as “high likelihood, major impact” and integrating results into its enterprise risk register.""",
        "domain_order": 9,
        "order": 2,
        "foundational": """AI risk assessments are ad-hoc, qualitative, or undocumented.""",
        "developing": """Some AI projects use risk ratings, but no consistent evaluation criteria exist.""",
        "established": """AI risk likelihood and impact are assessed systematically using enterprise risk methodologies.""",
        "leading": """AI risks are quantitatively assessed, modelled, and continuously updated using defined metrics and assurance reviews.""",
        "additional_guide": """Additional Guidance - Assessing and Evaluating AI Risks

Consistent assessment ensures AI risks are visible and comparable across projects. To strengthen evaluation:  
• **Adopt a Common Framework:** Apply enterprise risk matrices to AI, defining scales for ethical, operational, and reputational impact.  
• **Include Cross-Disciplinary Input:** Involve Legal, Risk, and Technical teams when rating AI risks.  
• **Use Quantitative Indicators:** Employ key risk indicators such as model accuracy deviation, data drift rate, or fairness metrics.  
• **Conduct Scenario Analysis:** Model worst-case outcomes (e.g., mis-classification affecting service eligibility).  
• **Document and Approve:** Record risk scores, rationales, and sign-offs in the risk register.  
• **Review Periodically:** Reassess likelihood and impact after system updates or policy changes.  
Structured assessment improves comparability, supports decision-making, and provides evidence for regulatory compliance and internal assurance.""",
        "evidence_types": """To comply with **RM-02 ("Assess and evaluate AI-related risks")**, provide artefacts showing consistent, repeatable evaluation practices.  
**Key Evidence Types:**  
• **Risk Assessments:** Completed AI-specific risk assessment forms with likelihood/impact ratings and mitigation actions.  
• **Framework Documents:** Risk evaluation criteria within the Enterprise Risk or AI Governance Framework.  
• **Registers and Logs:** Entries in enterprise risk registers showing AI-related scoring and residual risk tracking.  
• **Workshop Records:** Minutes or reports from cross-functional AI risk evaluation sessions.  
• **Metrics Dashboards:** Quantitative indicators (e.g., accuracy drift, bias ratio) used to reassess AI risk levels.  
• **Review Reports:** Periodic reviews verifying consistency of AI risk evaluation across departments.  
**In short:** evidence should demonstrate that AI risks are evaluated using structured, repeatable methods aligned to the organisation's broader risk-management approach.""",
    },
    {
        "code": """RM-03""",
        "text": """How are AI risks mitigated through defined controls and treatment plans?""",
        "explanation": """Identifying AI risks is only effective if followed by appropriate treatment. Without defined controls or mitigation plans, risks such as bias, data misuse, or system failure may persist unchecked. This question evaluates whether the organisation establishes, implements, and monitors mitigation strategies to manage AI risks to an acceptable level.

Example: A council’s AI Governance Committee maintains a central treatment plan that maps each AI risk—such as data quality or explainability gaps—to specific controls, owners, and review timelines.""",
        "domain_order": 9,
        "order": 3,
        "foundational": """AI risks are acknowledged but lack formal mitigation plans or assigned control owners.""",
        "developing": """Some risks have basic treatments, but controls are inconsistent or untested.""",
        "established": """Documented AI risk treatment plans include defined controls, owners, and periodic reviews.""",
        "leading": """AI controls are fully embedded, continuously monitored, and optimised using assurance testing and feedback loops.""",
        "additional_guide": """Additional Guidance - Mitigating and Controlling AI Risks

Risk treatment transforms identification into actionable management. To strengthen your mitigation approach:  
• **Create Structured Plans:** Define control objectives, owners, and due dates for each identified AI risk.  
• **Integrate with Existing Systems:** Use enterprise risk or GRC tools to track AI control effectiveness.  
• **Implement Diverse Controls:** Combine technical safeguards (bias testing, explainability tools) with procedural ones (ethics reviews, audits).  
• **Test Regularly:** Validate controls through simulations, internal audits, or external assurance reviews.  
• **Document Residual Risk:** Reassess remaining risk after control application.  
• **Report to Leadership:** Summarise key mitigation activities and control status in governance meetings.  
Effective mitigation ensures AI systems remain compliant, fair, and resilient as technologies evolve and risks change.""",
        "evidence_types": """To comply with **RM-03 ("Mitigate AI risks through defined controls and treatment plans")**, provide documentation demonstrating structured, ongoing control management.  
**Key Evidence Types:**  
• **Treatment Plans:** AI risk treatment or control matrices listing risks, controls, owners, and due dates.  
• **Policies & Procedures:** AI Risk Management or Control Implementation Guidelines.  
• **Control Evidence:** Records of technical controls (e.g., fairness audits, model retraining) and procedural safeguards (e.g., ethics reviews).  
• **Monitoring Reports:** Control testing results, residual risk evaluations, or assurance dashboards.  
• **Governance Records:** Committee minutes approving mitigation plans or reviewing control effectiveness.  
• **Audit Findings:** Internal or third-party reviews verifying AI control adequacy.  
**In short:** show that AI risks are actively managed through documented controls, clear accountability, and continuous verification of control performance.""",
    },
    {
        "code": """RM-04""",
        "text": """How are ownership and accountability for AI risks defined and maintained?""",
        "explanation": """Clear ownership ensures that AI risks are actively managed rather than left diffuse across technical or operational teams. When accountability is unclear, risk treatment often stalls, and incidents go unresolved. This question evaluates whether the organisation assigns explicit ownership for AI risks, defines responsibilities for oversight, and maintains accountability through documented governance channels.

Example: A council designates departmental AI Risk Owners who update mitigation progress monthly. The Chief Risk Officer consolidates all AI risks and reports outcomes to the Executive Risk and Governance Committee.""",
        "domain_order": 9,
        "order": 4,
        "foundational": """No defined AI risk owners or accountability mechanisms exist.""",
        "developing": """Some roles have partial responsibility, but ownership is unclear or inconsistently documented.""",
        "established": """Each AI risk has an assigned owner responsible for oversight, reporting, and remediation.""",
        "leading": """AI risk ownership is formally embedded in governance structures, with accountability tracked through KPIs and performance reviews.""",
        "additional_guide": """Additional Guidance - Establishing AI Risk Ownership

Assigning ownership ensures AI risks receive timely attention and resources. To enhance accountability:  
• **Define Roles and Responsibilities:** Identify AI Risk Owners at both operational and executive levels.  
• **Document Ownership:** Capture responsibilities in the risk register, policies, or governance charters.  
• **Integrate with Performance Management:** Link AI risk oversight to role KPIs or leadership scorecards.  
• **Establish Escalation Paths:** Define when risks are escalated to the AI Governance or Executive Committee.  
• **Enable Transparency:** Report ownership assignments and progress in risk dashboards.  
• **Maintain Continuity:** Update ownership when staff changes occur to avoid orphaned risks.  
Effective ownership embeds responsibility into decision-making, ensuring AI risks remain visible and well-managed throughout their lifecycle.""",
        "evidence_types": """To comply with **RM-04 ("Define and maintain ownership of AI risks")**, provide documentation confirming clear assignment and accountability.  
**Key Evidence Types:**  
• **Risk Registers:** Entries listing each AI risk with named owners, reviewers, and escalation contacts.  
• **Governance Charters:** Committee or policy documents specifying accountability roles for AI risk management.  
• **Role Descriptions:** Position statements for executives, system owners, or risk coordinators referencing AI responsibilities.  
• **Reporting Artefacts:** Dashboards or reports showing ownership status and progress updates.  
• **Performance Evidence:** KPI or performance-review templates linking AI risk management to leadership metrics.  
• **Audit Records:** Findings verifying that AI risk owners are identified and fulfilling obligations.  
**In short:** demonstrate that AI risk ownership is defined, visible, and enforced through formal governance mechanisms and performance accountability.""",
    },
    {
        "code": """RM-05""",
        "text": """How are AI risks monitored and reported to leadership and governance bodies?""",
        "explanation": """Regular monitoring and reporting ensure AI risks remain visible and are acted upon promptly. Without structured reporting, emerging risks—such as data drift, bias, or system misuse—may go undetected until significant harm occurs. This question assesses whether AI risk information is consistently tracked, summarised, and reported to management or executive oversight bodies for timely review and action.

Example: A council’s Risk and Assurance team compiles a quarterly AI Risk Report summarising incidents, control gaps, and emerging risks. The report is reviewed by the Executive Governance Committee and used to guide investment in mitigation initiatives.""",
        "domain_order": 9,
        "order": 5,
        "foundational": """AI risks are not formally monitored or reported to leadership.""",
        "developing": """Some AI risk information is shared, but reporting is ad-hoc or inconsistent.""",
        "established": """AI risk reports are produced regularly and reviewed by governance or executive bodies.""",
        "leading": """Continuous monitoring with automated reporting provides real-time visibility of AI risks to leadership.""",
        "additional_guide": """Additional Guidance - Monitoring and Reporting AI Risks

Effective monitoring enables proactive management of AI exposures and assurance for decision-makers. To strengthen oversight:  
• **Define Reporting Frequency:** Require AI risk reporting monthly, quarterly, or aligned to governance cycles.  
• **Standardise Formats:** Use consistent templates or dashboards to ensure comparability.  
• **Establish Key Risk Indicators (KRIs):** Track measures such as model drift, bias detection, or data-quality deviations.  
• **Use Technology Tools:** Employ GRC systems or analytics dashboards for centralised tracking.  
• **Escalate Critical Issues:** Define thresholds for immediate escalation to executives or boards.  
• **Provide Trend Analysis:** Report on emerging risks and control performance over time.  
Regular, structured reporting ensures leadership visibility, supports evidence-based decisions, and demonstrates a proactive risk culture.""",
        "evidence_types": """To comply with **RM-05 ("Monitor and report AI risks to leadership")**, provide artefacts showing structured monitoring, data collection, and reporting processes.  
**Key Evidence Types:**  
• **Risk Reports:** Periodic AI risk or assurance reports shared with executives or committees.  
• **Dashboards:** Real-time or summary dashboards showing AI risk indicators, control performance, and emerging issues.  
• **Meeting Minutes:** Records of risk discussions and decisions from governance or risk committee meetings.  
• **Escalation Logs:** Documentation of critical risk escalations and remedial actions.  
• **Policies & Procedures:** Defined reporting schedules and escalation thresholds within the risk management framework.  
• **Audit or Review Records:** Evidence verifying consistent risk reporting practices across departments.  
**In short:** demonstrate that AI risks are continuously monitored, analysed, and reported to leadership through structured, transparent, and repeatable processes.""",
    },
    {
        "code": """RM-06""",
        "text": """How are AI risks integrated into the organisation’s enterprise risk management (ERM) processes?""",
        "explanation": """Integrating AI risks into the broader enterprise risk framework ensures consistent visibility, prioritisation, and treatment alongside other strategic and operational risks. Without integration, AI-related issues may remain isolated within technical teams and overlooked by executive oversight. This question assesses whether AI risks are embedded within the organisation’s ERM processes, policies, and reporting mechanisms.

Example: A council integrates AI risk into its corporate risk register, aligning scoring, ownership, and reporting frequency with all other enterprise risks. The inclusion ensures AI exposure is reviewed at every executive risk committee meeting.""",
        "domain_order": 9,
        "order": 6,
        "foundational": """AI risks are managed separately and not included in enterprise risk processes.""",
        "developing": """Some AI risks appear in risk registers, but integration with ERM is incomplete.""",
        "established": """AI risks are fully integrated into enterprise risk management, using common tools, scoring, and review cycles.""",
        "leading": """AI risk integration is mature, enabling aggregated reporting, predictive analysis, and organisation-wide visibility.""",
        "additional_guide": """Additional Guidance - Integrating AI Risks into ERM

Integration ensures AI risk management benefits from established governance, assurance, and reporting channels. To mature integration:  
• **Align Frameworks:** Incorporate AI risks into ERM policies, taxonomies, and risk matrices.  
• **Use Common Tools:** Manage AI risks through the same registers and software used for enterprise risk.  
• **Standardise Scoring:** Apply consistent likelihood and impact criteria across all risk types.  
• **Establish Cross-Functional Input:** Involve Risk, IT, Legal, and Ethics teams in ERM discussions.  
• **Consolidate Reporting:** Include AI risks in enterprise-level dashboards and executive reports.  
• **Ensure Board Visibility:** Present aggregated AI risk summaries to the Audit and Risk Committee.  
Integration embeds AI oversight into existing governance, providing efficiency, consistency, and transparency across the organisation.""",
        "evidence_types": """To comply with **RM-06 ("Integrate AI risks into enterprise risk management")**, provide documentation showing AI risks are part of standard ERM processes.  
**Key Evidence Types:**  
• **Risk Registers:** Enterprise risk registers containing AI-related entries with consistent scoring and owners.  
• **ERM Policies:** Documents referencing AI or algorithmic risk as a core category.  
• **Reporting Artefacts:** Executive dashboards or consolidated risk reports including AI risks.  
• **Meeting Minutes:** Audit, Risk, or Governance Committee minutes showing AI risk discussions.  
• **Templates & Tools:** Standard risk assessment forms and GRC systems capturing AI-related fields.  
• **Audit Findings:** Reviews confirming integration of AI risks into corporate ERM.  
**In short:** demonstrate that AI risks are managed and reported through the same frameworks, tools, and oversight structures as all other enterprise risks.""",
    },
    {
        "code": """RM-07""",
        "text": """How are AI-related risk incidents and escalations managed and responded to?""",
        "explanation": """Even well-governed AI systems can fail, behave unexpectedly, or generate harmful outcomes. Without clear escalation and response processes, incidents may go unaddressed or repeat across projects. This question assesses whether the organisation has structured procedures for detecting, escalating, and resolving AI-related risk incidents—such as model bias, privacy breaches, or automation failures.

Example: A council establishes an AI Incident Response Procedure requiring teams to log incidents within 24 hours, escalate high-risk events to the AI Governance Committee, and document corrective and preventative actions.""",
        "domain_order": 9,
        "order": 7,
        "foundational": """No formal process exists to identify, escalate, or manage AI-related incidents.""",
        "developing": """Some incidents are logged or discussed, but escalation procedures are informal or inconsistent.""",
        "established": """Documented AI incident and escalation processes define responsibilities, timeframes, and corrective actions.""",
        "leading": """AI incident management is fully integrated with enterprise response frameworks, enabling rapid resolution, lessons learned, and continual improvement.""",
        "additional_guide": """Additional Guidance - Managing AI Risk Incidents and Escalations

Timely detection and escalation of AI incidents protect organisational integrity and stakeholder trust. To enhance readiness:  
• **Define Incident Types:** Classify AI-related events (e.g., data bias, model drift, security breach, ethical non-compliance).  
• **Establish Response Procedures:** Include incident logging, prioritisation, escalation thresholds, and resolution timelines.  
• **Integrate with Existing Systems:** Align with cybersecurity, privacy, and safety incident response processes.  
• **Assign Ownership:** Specify roles for technical responders, governance committees, and communications teams.  
• **Analyse Root Causes:** Perform post-incident reviews to identify control gaps.  
• **Document Lessons Learned:** Feed improvements back into risk registers, policies, and training.  
Effective escalation and response demonstrate accountability and continuous learning in managing AI risks.""",
        "evidence_types": """To comply with **RM-07 ("Manage and respond to AI-related incidents and escalations")**, provide evidence of formal procedures, reporting mechanisms, and follow-up actions.  
**Key Evidence Types:**  
• **Incident Response Plans:** Documents defining AI incident types, response steps, and escalation protocols.  
• **Incident Logs:** Recorded AI-related events, root cause analyses, and corrective actions.  
• **Integration Evidence:** References to AI in enterprise incident or crisis management frameworks.  
• **Committee Records:** Meeting minutes showing review and oversight of AI incident handling.  
• **Training Records:** Staff training or simulations on AI incident identification and escalation.  
• **Post-Incident Reports:** Lessons-learned summaries feeding into risk treatment plans.  
**In short:** demonstrate that AI incidents are identified, escalated, and resolved through structured, documented processes aligned with the broader organisational response framework.""",
    },
    {
        "code": """RM-08""",
        "text": """How does the organisation review and improve its AI risk management processes over time?""",
        "explanation": """AI risks evolve rapidly as technologies, regulations, and societal expectations change. Without continuous improvement, existing controls and risk frameworks can become outdated or ineffective. This question assesses whether the organisation periodically reviews, updates, and strengthens its AI risk management practices based on lessons learned, incidents, audits, or emerging standards.

Example: A council conducts an annual AI Risk Review to evaluate its framework against ISO 42001. Findings drive updates to its AI policy, staff training, and risk treatment plans, ensuring ongoing alignment with evolving governance requirements.""",
        "domain_order": 9,
        "order": 8,
        "foundational": """AI risk processes are static and rarely reviewed or improved.""",
        "developing": """Some reviews occur following incidents or audits, but they are informal or infrequent.""",
        "established": """Regular reviews and updates of AI risk processes occur, informed by audits and lessons learned.""",
        "leading": """Continuous improvement is embedded, using benchmarking, performance metrics, and regulatory horizon scanning.""",
        "additional_guide": """Additional Guidance - Continuous Improvement of AI Risk Management

Ongoing review ensures AI risk management remains relevant and effective. To embed continuous improvement:  
• **Schedule Regular Reviews:** Conduct annual or biannual assessments of AI risk processes.  
• **Use Feedback Loops:** Incorporate lessons from incidents, audits, and assurance reviews.  
• **Benchmark Against Standards:** Compare current practices to frameworks such as ISO 42001 or NIST AI RMF.  
• **Monitor Regulatory Changes:** Track emerging legislation and ethical guidelines to update frameworks proactively.  
• **Engage Stakeholders:** Involve Risk, Legal, Data, and Ethics teams in review discussions.  
• **Measure Progress:** Use KPIs to evaluate control performance and maturity improvements.  
Embedding improvement into governance ensures resilience, transparency, and confidence in managing AI-related risks.""",
        "evidence_types": """To comply with **RM-08 ("Review and improve AI risk management processes")**, provide artefacts showing structured evaluation, updates, and benchmarking activities.  
**Key Evidence Types:**  
• **Review Reports:** Annual AI risk management review or framework evaluation reports.  
• **Action Plans:** Improvement logs or registers capturing recommendations and progress.  
• **Benchmarking Evidence:** Comparisons against national or international AI governance frameworks.  
• **Audit Findings:** Internal or third-party reviews verifying updates to AI risk processes.  
• **Governance Records:** Meeting minutes documenting review outcomes and improvement decisions.  
• **Training or Communications:** Evidence of updated procedures shared across teams following framework revisions.  
**In short:** demonstrate that AI risk management is a living process, continually refined through evidence, feedback, and evolving best practice.""",
    },
    {
        "code": """TE-01""",
        "text": """How does the organisation ensure transparency in how AI systems are developed and used?""",
        "explanation": """Transparency enables stakeholders to understand how AI systems function, what data they use, and how decisions are made. Without it, trust erodes and accountability weakens. This question assesses whether your organisation provides visibility into AI development processes, governance decisions, and system deployments.

Example: A council publishes an “AI Project Register” describing each AI system’s purpose, data sources, and ethical review outcomes, allowing citizens and internal stakeholders to understand how AI supports public services.""",
        "domain_order": 10,
        "order": 1,
        "foundational": """AI operations are opaque, with little to no disclosure or documentation.""",
        "developing": """Some AI documentation or communications exist but are incomplete or technical.""",
        "established": """AI systems and decisions are transparently documented and communicated to stakeholders.""",
        "leading": """Enterprise-wide transparency includes detailed disclosures, accessible documentation, and public reporting on AI governance.""",
        "additional_guide": """Additional Guidance - Building Organisational Transparency in AI

Transparency fosters understanding, accountability, and ethical confidence. To improve transparency:  
• **Document AI Systems:** Record purpose, datasets, owners, risks, and performance metrics for all AI initiatives.  
• **Create an AI Register:** Maintain internal or public-facing inventories detailing system use.  
• **Communicate Decisions:** Share project rationales, ethical assessments, and governance outcomes with relevant audiences.  
• **Use Accessible Language:** Avoid technical jargon when engaging non-technical stakeholders.  
• **Review Regularly:** Ensure published information remains current and accurate.  
• **Align with Frameworks:** Follow global transparency principles (ISO 42001, NIST AI RMF, OECD AI Principles).  
Structured transparency demonstrates openness and helps stakeholders trust how AI impacts operations and decisions.""",
        "evidence_types": """To comply with **TE-01 ("Ensure transparency in AI development and use")**, provide documentation showing visible, consistent communication about AI activities.  
**Key Evidence Types:**  
• **AI Register:** Internal or public listing of AI systems with metadata (purpose, owner, risk rating).  
• **Governance Records:** Committee minutes or reports summarising AI system reviews.  
• **Policies:** Transparency or Responsible AI Policy defining disclosure requirements.  
• **Communication Materials:** Public reports, web pages, or press releases describing AI use.  
• **Documentation Templates:** Standard forms capturing AI system details for publication.  
• **Audit Reports:** Reviews confirming accuracy and completeness of AI disclosures.  
**In short:** demonstrate that AI operations are visible, documented, and communicated clearly to foster public and internal trust.""",
    },
    {
        "code": """TE-02""",
        "text": """How does the organisation ensure AI decisions and outputs are explainable and understandable to stakeholders?""",
        "explanation": """Explainability enables people to understand how and why AI systems produce particular outcomes. Without it, accountability and user confidence are weakened. This question assesses whether the organisation uses interpretable models, explanation tools, and communication strategies to make AI decisions comprehensible to both technical and non-technical audiences.

Example: A council uses explainability techniques such as SHAP visualisations to interpret model decisions and provides plain-language summaries of AI recommendations in public reports and staff dashboards.""",
        "domain_order": 10,
        "order": 2,
        "foundational": """AI systems produce results without explanation or rationale.""",
        "developing": """Some explainability methods are used, but explanations are technical and limited to experts.""",
        "established": """AI decisions are consistently explained using accessible tools, documentation, and human review.""",
        "leading": """Explainability is enterprise-wide, combining interpretable models, transparent communication, and audience-specific explanations.""",
        "additional_guide": """Additional Guidance - Ensuring AI Explainability

Explainability strengthens trust, supports accountability, and meets ethical and legal obligations. To mature your approach:  
• **Adopt Interpretable Models:** Prefer models that provide traceable reasoning where accuracy trade-offs are acceptable.  
• **Use Explanation Tools:** Apply frameworks like SHAP, LIME, or surrogate models for interpretability.  
• **Provide Contextual Summaries:** Translate technical explanations into plain language for non-technical audiences.  
• **Integrate Oversight:** Require human review and documentation for complex or high-impact AI decisions.  
• **Document Model Logic:** Maintain records describing features, weighting, and data relationships.  
• **Engage Stakeholders:** Offer transparent communications explaining how AI supports decisions.  
Consistent explainability practices enhance public confidence and reduce the risk of opaque or biased AI behaviour.""",
        "evidence_types": """To comply with **TE-02 ("Ensure AI decisions and outputs are explainable")**, provide artefacts showing active use of interpretability and explanation mechanisms.  
**Key Evidence Types:**  
• **Explainability Documentation:** Model summaries, logic flowcharts, or explanation guides for each AI system.  
• **Technical Tools:** Records of SHAP, LIME, or similar explainability analyses.  
• **Communication Materials:** Plain-language summaries explaining AI outcomes to users or the public.  
• **Policy References:** Requirements for explainability within the Responsible AI or Data Governance Policy.  
• **Review Records:** Meeting minutes documenting explainability assessments or approvals.  
• **Audit Reports:** Reviews verifying adequacy and accessibility of AI explanations.  
**In short:** demonstrate that AI decisions are interpretable, documented, and clearly communicated to technical and non-technical stakeholders alike.""",
    },
    {
        "code": """TE-03""",
        "text": """How does the organisation communicate the limitations, assumptions, and risks of its AI systems?""",
        "explanation": """Transparent communication of AI limitations and risks allows stakeholders to interpret results appropriately and maintain informed trust. Without this, users may over-rely on AI systems or misinterpret outcomes. This question assesses whether the organisation identifies and clearly communicates known constraints, assumptions, and potential failure conditions of AI models.

Example: A council attaches a “Model Fact Sheet” to each AI deployment, outlining data sources, assumptions, limitations, known risks, and appropriate contexts for system use.""",
        "domain_order": 10,
        "order": 3,
        "foundational": """AI limitations and risks are undocumented or not communicated.""",
        "developing": """Some information is shared internally but lacks structure or clarity.""",
        "established": """Limitations and risks are documented and communicated to relevant stakeholders through defined processes.""",
        "leading": """Comprehensive documentation and public communication detail assumptions, constraints, and mitigation strategies for all AI systems.""",
        "additional_guide": """Additional Guidance - Communicating AI Limitations and Risks

Being transparent about AI limitations promotes realistic expectations and accountability. To strengthen communication:  
• **Document Known Risks:** Identify technical, ethical, and operational risks within model documentation.  
• **Describe Assumptions:** Explain dataset boundaries, model purpose, and exclusion criteria.  
• **Develop Fact Sheets:** Create standardised AI system summaries accessible to all stakeholders.  
• **Communicate Clearly:** Provide non-technical explanations to avoid misinterpretation.  
• **Disclose Uncertainty:** Include accuracy metrics, confidence intervals, and limitations in outputs or reports.  
• **Update Regularly:** Revise documentation following retraining or policy changes.  
Transparent communication reduces misunderstanding and enables informed oversight of AI outcomes.""",
        "evidence_types": """To comply with **TE-03 ("Communicate limitations, assumptions, and risks of AI systems")**, provide artefacts proving structured documentation and transparent communication.  
**Key Evidence Types:**  
• **Model Documentation:** Fact sheets, model cards, or datasheets outlining assumptions and constraints.  
• **Risk Registers:** Entries identifying AI-specific risks and mitigation actions.  
• **Communication Templates:** Standardised reporting formats for internal or public use.  
• **Governance Records:** Committee minutes discussing disclosure of model limitations.  
• **Public Disclosures:** Webpages, reports, or FAQs describing AI risks and safeguards.  
• **Audit Reports:** Reviews verifying completeness and accuracy of limitation communications.  
**In short:** demonstrate that AI systems' boundaries, assumptions, and potential risks are documented, reviewed, and communicated transparently to all affected parties.""",
    },
    {
        "code": """TE-04""",
        "text": """How does the organisation ensure AI documentation is complete, accurate, and accessible to relevant stakeholders?""",
        "explanation": """Comprehensive documentation is critical for accountability, transparency, and effective governance. Without clear, consistent records, it becomes difficult to understand how AI systems were designed, trained, and validated—or to demonstrate compliance during audits or incidents. This question assesses whether the organisation maintains detailed, up-to-date documentation describing AI purpose, design, data, testing, and governance.

Example: A council maintains a central AI documentation repository containing model cards, data sheets, validation results, and governance approvals, accessible to technical staff, risk officers, and auditors.""",
        "domain_order": 10,
        "order": 4,
        "foundational": """AI documentation is incomplete, inconsistent, or unavailable to stakeholders.""",
        "developing": """Some documentation exists but is unstructured or lacks governance oversight.""",
        "established": """Comprehensive documentation is maintained and reviewed regularly for all AI systems.""",
        "leading": """AI documentation is standardised, centralised, and accessible, with version control, review cycles, and traceability built into governance.""",
        "additional_guide": """Additional Guidance - Ensuring Complete and Accessible AI Documentation

Structured documentation enhances explainability and assurance. To strengthen maturity:  
• **Define Documentation Standards:** Specify required artefacts (e.g., model cards, data sheets, validation logs).  
• **Maintain Central Repositories:** Store documentation in controlled, auditable systems.  
• **Apply Version Control:** Track model and data changes over time.  
• **Review Periodically:** Conduct governance reviews to ensure completeness and accuracy.  
• **Enable Role-Based Access:** Grant stakeholders access appropriate to their roles.  
• **Align with Frameworks:** Follow ISO/IEC 42001 and NIST AI RMF documentation principles.  
Comprehensive documentation ensures traceability, accountability, and stakeholder confidence.""",
        "evidence_types": """To comply with **TE-04 ("Ensure AI documentation is complete, accurate, and accessible")**, provide artefacts demonstrating structured, reviewed, and traceable documentation processes.  
**Key Evidence Types:**  
• **Documentation Framework:** Policies defining AI documentation requirements and ownership.  
• **Model & Data Sheets:** Artefacts outlining system design, data sources, and testing outcomes.  
• **Repository Evidence:** Proof of a centralised documentation system or database.  
• **Version Control Logs:** Records showing updates and review histories.  
• **Audit Reports:** Assessments verifying documentation completeness and accessibility.  
• **Access Control Records:** Role-based permissions and user access logs.  
**In short:** demonstrate that AI documentation is standardised, maintained, and accessible, enabling accountability, explainability, and continuous governance.""",
    },
    {
        "code": """TE-05""",
        "text": """How does the organisation document and disclose data sources used in AI systems?""",
        "explanation": """Transparency around data sources helps stakeholders understand where AI systems derive their insights and ensures accountability for data provenance. Without proper documentation or disclosure, there is a risk of bias, copyright infringement, or privacy violations. This question assesses whether the organisation tracks, validates, and communicates the origin, purpose, and licensing of all datasets used in AI systems.

Example: A council maintains a “Dataset Register” documenting all internal and external data sources used for AI development, including collection methods, usage rights, and data quality evaluations.""",
        "domain_order": 10,
        "order": 5,
        "foundational": """Data sources for AI systems are undocumented or inconsistently recorded.""",
        "developing": """Some datasets are documented, but provenance and licensing information are incomplete.""",
        "established": """All AI data sources are recorded, reviewed, and verified for quality, legality, and relevance.""",
        "leading": """Comprehensive data-source documentation and disclosure support full traceability, auditability, and public transparency.""",
        "additional_guide": """Additional Guidance - Documenting and Disclosing AI Data Sources

Data transparency enables accountability, reproducibility, and public trust. To improve maturity:  
• **Create Dataset Registers:** Catalogue all AI datasets, including origin, purpose, and data owners.  
• **Track Provenance:** Record how data was collected, cleaned, and transformed.  
• **Verify Legality and Ethics:** Check data licensing, consent, and lawful use before integration.  
• **Communicate Transparently:** Publish dataset details or summaries where appropriate.  
• **Use Metadata Standards:** Follow recognised frameworks (e.g., DCAT, ISO 19115).  
• **Update Regularly:** Review and refresh data documentation with every model retraining.  
Clear documentation ensures data use is transparent, defensible, and compliant with governance and legal requirements.""",
        "evidence_types": """To comply with **TE-05 ("Document and disclose data sources used in AI systems")**, provide artefacts showing structured provenance management and disclosure.  
**Key Evidence Types:**  
• **Dataset Registers:** Central repository documenting all AI data sources, collection methods, and ownership.  
• **Data Provenance Reports:** Records showing dataset lineage and transformations.  
• **Licensing Documentation:** Usage rights, consent forms, or contractual agreements for third-party data.  
• **Policies & Frameworks:** Data Transparency or Responsible AI Policy referencing provenance disclosure.  
• **Public Reports:** Summaries of AI datasets or open-data disclosures.  
• **Audit Findings:** Reviews verifying dataset completeness and compliance with legal and ethical standards.  
**In short:** demonstrate that every dataset used for AI is properly traced, validated, and disclosed to ensure transparency, legality, and public accountability.""",
    },
    {
        "code": """TE-06""",
        "text": """How does the organisation measure, document, and communicate AI system performance and accuracy?""",
        "explanation": """Transparent performance reporting helps stakeholders understand how reliably AI systems operate. Without defined accuracy metrics or disclosure, AI outcomes may be misunderstood or trusted beyond their capability. This question assesses whether the organisation measures AI system performance, validates results, and communicates accuracy, error rates, and confidence levels to relevant stakeholders.

Example: A council documents model accuracy and precision metrics for all deployed AI systems and publishes a summary of performance evaluations and limitations in its annual Responsible AI Report.""",
        "domain_order": 10,
        "order": 6,
        "foundational": """AI performance is not measured or reported; reliability is assumed.""",
        "developing": """Some performance testing occurs but lacks consistent metrics or transparency.""",
        "established": """AI accuracy and performance are routinely measured, validated, and documented.""",
        "leading": """Performance is continuously monitored and transparently reported through dashboards and periodic public disclosures.""",
        "additional_guide": """Additional Guidance - Reporting AI Performance and Accuracy

Performance transparency ensures AI systems are fair, reliable, and aligned with expectations. To strengthen reporting:  
• **Define Metrics:** Establish accuracy, precision, recall, and error thresholds relevant to each use case.  
• **Test Regularly:** Evaluate performance pre-deployment and during operation.  
• **Document Results:** Maintain records of evaluations, validation data, and testing environments.  
• **Communicate Clearly:** Translate metrics into accessible insights for executives and the public.  
• **Monitor Continuously:** Use dashboards to track performance drift and trigger reviews.  
• **Benchmark Externally:** Compare results against industry or regulatory standards.  
Transparent reporting fosters confidence and enables accountability for AI reliability and improvement.""",
        "evidence_types": """To comply with **TE-06 ("Measure, document, and communicate AI system performance and accuracy")**, provide documentation showing structured evaluation and disclosure processes.  
**Key Evidence Types:**  
• **Performance Reports:** Internal or public records detailing AI accuracy, error rates, or validation metrics.  
• **Testing Logs:** Documentation of pre-deployment and post-deployment evaluations.  
• **Monitoring Dashboards:** Automated tools tracking accuracy drift or model performance over time.  
• **Policies & Procedures:** AI Testing and Validation Policy referencing reporting obligations.  
• **Communication Artefacts:** Plain-language summaries or reports explaining performance results.  
• **Audit Findings:** Reviews confirming integrity and transparency of performance reporting.  
**In short:** demonstrate that AI system performance is measured objectively, documented consistently, and communicated transparently to all relevant audiences.""",
    },
    {
        "code": """TE-07""",
        "text": """How does the organisation communicate when decisions or outcomes are generated by AI rather than humans?""",
        "explanation": """Transparency about AI-generated decisions allows individuals to understand when automation is influencing outcomes that affect them. Without disclosure, users may assume human involvement, undermining consent and trust. This question assesses whether the organisation clearly informs stakeholders when AI is used in decision-making, explains its role, and provides avenues for human review or challenge.

Example: A council includes statements in citizen notifications explaining when AI tools are used to prioritise applications, clarifying that final approval is made by a human officer.""",
        "domain_order": 10,
        "order": 7,
        "foundational": """AI-generated decisions are not disclosed to those affected.""",
        "developing": """Some communication occurs, but AI involvement is unclear or inconsistent.""",
        "established": """Stakeholders are routinely informed when AI contributes to decisions and given human review options.""",
        "leading": """AI use is clearly disclosed in all interactions, supported by explainable outcomes and defined human recourse mechanisms.""",
        "additional_guide": """Additional Guidance - Disclosing AI-Driven Decision-Making

Clarity about AI involvement reinforces fairness and informed choice. To strengthen transparency:  
• **Provide Clear Notices:** Inform users whenever AI contributes to decisions affecting them.  
• **Define Human Oversight:** Explain the extent of human involvement or approval required.  
• **Ensure Accessible Language:** Avoid technical jargon; focus on clarity and impact.  
• **Offer Review Mechanisms:** Allow individuals to request human review or contest AI-generated results.  
• **Update Policies and Templates:** Embed disclosure statements in letters, forms, or online portals.  
• **Monitor Compliance:** Audit communications for completeness and consistency.  
Transparent disclosure supports trust, ethical integrity, and compliance with fairness and accountability standards.""",
        "evidence_types": """To comply with **TE-07 ("Communicate when decisions or outcomes are generated by AI")**, provide documentation showing disclosure and human review processes.  
**Key Evidence Types:**  
• **Policy Documents:** AI Transparency or Decision Disclosure Policy defining communication obligations.  
• **Communication Templates:** Letters, emails, or notifications containing AI use statements.  
• **Public Web Content:** Explanatory webpages outlining where and how AI is used in services.  
• **Review Procedures:** Process documentation for human challenge or appeal mechanisms.  
• **Audit Records:** Compliance reviews verifying disclosure of AI use.  
• **Training Materials:** Staff guidance on communicating AI involvement to citizens.  
**In short:** demonstrate that AI-generated decisions are clearly disclosed, understandable, and supported by options for human review or explanation.""",
    },
    {
        "code": """TE-08""",
        "text": """How does the organisation engage stakeholders and incorporate feedback on AI transparency and communication?""",
        "explanation": """Engaging stakeholders helps ensure AI transparency meets community expectations and builds long-term trust. Without structured feedback, organisations risk misalignment between what is disclosed and what stakeholders need to understand. This question evaluates whether the organisation collects, reviews, and responds to feedback on how AI systems are communicated and explained.

Example: A council conducts annual stakeholder workshops and surveys to evaluate public understanding of its AI Register and transparency practices, using results to update communication materials and policies.""",
        "domain_order": 10,
        "order": 8,
        "foundational": """No formal mechanisms exist to gather or act on stakeholder feedback about AI transparency.""",
        "developing": """Some informal engagement occurs but lacks structure or consistent follow-up.""",
        "established": """Regular stakeholder feedback is collected, analysed, and used to improve AI communication.""",
        "leading": """Ongoing engagement processes systematically incorporate stakeholder insights into transparency strategy and reporting.""",
        "additional_guide": """Additional Guidance - Engaging Stakeholders on AI Transparency

Stakeholder engagement ensures transparency aligns with public expectations and organisational values. To strengthen maturity:  
• **Identify Stakeholders:** Include citizens, staff, regulators, and community groups.  
• **Collect Feedback:** Use surveys, forums, or consultations to assess transparency effectiveness.  
• **Integrate into Governance:** Review feedback in AI or Ethics Committee meetings.  
• **Respond Publicly:** Communicate how feedback informed policy or disclosure improvements.  
• **Measure Engagement:** Track participation rates and satisfaction levels.  
• **Review Periodically:** Update engagement processes to reflect emerging needs.  
Ongoing stakeholder dialogue ensures that transparency practices remain relevant, trusted, and socially accountable.""",
        "evidence_types": """To comply with **TE-08 ("Engage stakeholders and incorporate feedback on AI transparency")**, provide artefacts demonstrating structured engagement and feedback integration.  
**Key Evidence Types:**  
• **Engagement Plans:** Documents outlining stakeholder consultation objectives and processes.  
• **Survey Results:** Feedback data from community or employee AI transparency assessments.  
• **Meeting Records:** Minutes showing committee review of stakeholder feedback.  
• **Policy Updates:** Evidence of changes made in response to engagement outcomes.  
• **Public Communications:** Reports summarising engagement activities and their impact.  
• **Audit Reports:** Reviews confirming inclusion of stakeholder perspectives in AI governance.  
**In short:** demonstrate that stakeholder feedback on AI transparency is regularly sought, reviewed, and meaningfully incorporated into organisational communication and reporting.""",
    }
]
