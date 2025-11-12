#!/usr/bin/env python3
"""
Script to add evidence_types tooltips to readiness_questions.py
"""

# Mapping of question codes to their evidence types tooltips
EVIDENCE_TYPES_DATA = {
    "SA-01": """To demonstrate alignment, provide artefacts showing that AI is considered strategically, not just tactically.

**Key Evidence Types:**

• **Strategic Plans:** Corporate, ICT, or Digital Strategies referencing AI objectives, ethics, or readiness.
• **Board or Executive Minutes:** Discussions of AI as part of strategic planning or transformation.
• **Briefing Papers:** Presentations or whitepapers assessing AI opportunities and risks.
• **Performance Frameworks:** KPIs or outcome measures tracking AI progress.
• **Risk Registers:** Strategic entries acknowledging AI impacts or dependencies.
• **Stakeholder Engagement:** Workshops or consultations on AI vision and values.

In short: show that AI is visible in strategic intent and actively managed as part of corporate planning.""",

    "SA-02": """Provide proof that leaders actively support AI readiness and governance.

**Key Evidence Types:**

• **Leadership Communications:** CEO or executive statements referencing responsible AI adoption.
• **Strategic Plans & Reports:** Inclusion of AI goals or ethical commitments endorsed by leadership.
• **Meeting Minutes:** Evidence of executive participation in AI governance or risk committees.
• **Budget Allocations:** Funding for AI training, pilots, or governance functions.
• **Performance Documents:** Executive KPIs tied to AI readiness or digital transformation.
• **Briefings & Workshops:** Records of leadership attendance or sponsorship of AI capability sessions.

In short: show that leadership is not merely aware of AI but is visibly leading and resourcing its responsible use.""",

    "SA-03": """Demonstrate that AI objectives and measures of success are defined, tracked, and shared across the organisation.

**Key Evidence Types:**

• **Strategy Documents:** Digital or Corporate Plans outlining AI goals and benefits.
• **Performance Frameworks:** KPIs or scorecards linked to AI initiatives.
• **Project Charters:** Business cases articulating AI success measures and expected outcomes.
• **Communications:** Internal newsletters, briefings, or dashboards explaining AI objectives.
• **Review Reports:** Post-implementation or pilot reviews assessing success against KPIs.
• **Stakeholder Feedback:** Surveys or engagement summaries validating communicated goals.

In short: show that AI objectives are purposeful, measurable, and visible across the organisation.""",

    "SA-04": """Provide evidence that AI planning and decision-making incorporate ethical and community considerations.

**Key Evidence Types:**

• **Ethics Frameworks:** Responsible AI Principles or Codes of Conduct referencing fairness, transparency, and accountability.
• **Consultation Records:** Stakeholder or community engagement notes on AI projects.
• **Impact Assessments:** Ethical, privacy, or social impact analyses for proposed AI uses.
• **Procurement Documents:** Evaluation criteria requiring ethical compliance by vendors.
• **Communication Artefacts:** Public statements or reports outlining ethical commitments in AI adoption.
• **Monitoring Reports:** Reviews or dashboards tracking ethical and community outcomes.

In short: demonstrate that AI decisions are guided by values, informed by stakeholders, and transparent to the community.""",

    "SA-05": """Provide documentation that AI vision and principles are shared across the organisation and with key stakeholders.

**Key Evidence Types:**

• **Internal Communications:** Staff emails, newsletters, or intranet posts explaining AI objectives and ethics.
• **Public Materials:** Website statements, brochures, or annual reports describing AI strategy and safeguards.
• **Leadership Briefings:** Presentations or videos from executives outlining the AI vision.
• **Feedback Mechanisms:** Surveys or consultation summaries gauging staff or public understanding.
• **Training & Awareness:** Sessions introducing AI goals and responsible-use expectations.
• **Measurement Reports:** Engagement metrics or feedback results showing communication reach and effectiveness.

In short: show that AI communication is deliberate, transparent, and builds both internal alignment and external trust.""",

    "SA-06": """Demonstrate that AI strategy and readiness are periodically evaluated, updated, and communicated.

**Key Evidence Types:**

• **Review Schedules:** Planning calendars or policy schedules specifying AI strategy review frequency.
• **Updated Strategies:** Revised digital or AI roadmaps showing version control and change history.
• **Meeting Minutes:** Records from executive, audit, or governance meetings discussing AI reviews.
• **Risk Registers:** Updates reflecting newly identified AI threats or opportunities.
• **Feedback Reports:** Staff or community surveys informing AI strategic adjustments.
• **Audit Findings:** Internal or third-party assessments confirming continuous improvement practices.

In short: provide clear evidence that AI strategy is a living document - actively reviewed, adapted, and improved over time.""",

    "GF-01": """To demonstrate compliance, provide evidence that accountability and oversight for AI are formally defined and operating effectively.

**Key Evidence Types:**

• **Policies & Frameworks:** Approved AI Governance Policy or Responsible AI Framework detailing roles, responsibilities, and decision rights.
• **Organisational Structure:** Role descriptions (e.g., Chief AI Officer, Ethics Lead) and governance committee Terms of Reference.
• **Meeting Records:** Minutes or reports from AI Governance or Ethics Committees showing project reviews or decisions.
• **Integration Evidence:** AI governance references in enterprise risk, privacy, or data policies.
• **Performance & Review:** Internal audits or scorecards evaluating AI governance effectiveness.
• **Training & Awareness:** Records of leadership training on AI responsibilities and ethics.

In short: show a structured, cross-functional governance model with documented oversight and active executive ownership.""",

    "GF-02": """To demonstrate compliance, provide evidence that the organisation's AI vision and strategy are clearly documented, aligned with business objectives, and supported by leadership commitment.

• **Role Documents:** Position Descriptions, RACI matrices, or Governance Charters assigning AI accountabilities.
• **Committee TORs:** Clear AI decision-making roles in Ethics or Risk Committees.
• **Performance Plans:** KPIs linking job roles to AI governance.
• **Training Records:** Evidence of staff briefings on AI responsibilities.
• **Internal Audits:** Reviews confirming AI roles are known and effective.

In short: demonstrate that everyone from leadership to project teams knows their role in AI decisions and oversight.""",

    "GF-03": """To demonstrate compliance, provide evidence that AI-related roles, responsibilities, and decision-making authorities are clearly defined, documented, and communicated across the organisation.

• **Risk Frameworks:** Documents showing AI categories within enterprise risk registers.
• **Committee Minutes:** Evidence that AI issues are discussed and actions tracked.
• **Policy References:** Updates in governance or data policies mentioning AI risk or ethics.
• **Audit Reports:** Assessments of how AI controls align with governance processes.
• **Integration Plans:** Documents linking AI governance to corporate risk strategy.

In short: provide tangible proof that AI is managed within the same frameworks that guide other strategic risks.""",

    "GF-04": """To demonstrate compliance, provide evidence that AI governance policies and frameworks are formally approved, consistently applied, and reviewed to ensure alignment with organisational objectives and ethical standards.

• **Process Docs:** AI pilot approval workflow or standard intake form.
• **Registers:** Active AI project register with status and review dates.
• **Meeting Records:** Minutes from committees approving or reviewing AI projects.
• **Policy Clauses:** ICT Procurement or Innovation Policies mentioning AI oversight.
• **Reports:** Post-implementation reviews documenting results and lessons learned.

Demonstrate that AI initiatives follow an approved path from concept to review with clear accountability.""",

    "GF-05": """To demonstrate compliance, provide evidence that risk management processes for AI are established, documented, and integrated into the organisation's broader governance and assurance frameworks.

• **Briefings & Summaries:** Internal or external AI regulation updates.
• **Memberships:** Participation in industry forums or AI standards groups.
• **Policy Versions:** Documentation showing updates triggered by new standards.
• **Training:** Attendance at AI governance workshops or compliance seminars.
• **Communications:** Newsletters or memos circulating AI policy changes.

Provide proof of continuous monitoring and integration of emerging AI requirements into corporate governance.""",

    "GF-06": """To demonstrate compliance, provide evidence that AI governance responsibilities are formally embedded into staff roles, position descriptions, and performance management processes to ensure sustained accountability across the organisation.

• **Job Descriptions:** Documents listing AI ethics or governance responsibilities.
• **Performance Plans:** KPIs linked to AI oversight or risk management.
• **Org Charts:** Roles or teams identified as AI accountability owners.
• **Training Records:** Completion of AI ethics or governance modules by staff.
• **Review Docs:** Performance evaluation templates showing AI criteria.

Show evidence that AI accountability is not optional but a recognised, measurable part of key roles.""",

    "DR-01": """Show that data-quality management is systematic, documented, and actively monitored.

**Key Evidence Types:**

• **Policies & Standards:** Data-Quality Policy or Governance Framework defining minimum thresholds and responsibilities.
• **Quality Reports:** Logs or dashboards showing accuracy, completeness, or error metrics.
• **Process Documentation:** Data-validation procedures, cleansing scripts, or ETL workflows.
• **Ownership Records:** Named data stewards or custodians in organisational charts.
• **Audit Results:** Internal or external reviews of data-quality performance.
• **Training Records:** Staff education materials on data management and quality assurance.

In short: provide artefacts that prove data is treated as a governed, measurable asset fit for trustworthy AI.""",

    "DR-02": """Demonstrate that data-ownership and access responsibilities are clearly defined, maintained, and enforced.

**Key Evidence Types:**

• **Policies & Frameworks:** Data Governance or Information Management Policy defining ownership, stewardship, and accountability.
• **Data Registers:** Inventories listing datasets, custodians, and access rights.
• **Role Descriptions:** Job profiles or KPIs specifying data-management duties.
• **Access Records:** Role-based permission logs or periodic access-review reports.
• **Committee Minutes:** Evidence of governance oversight or data-stewardship reviews.
• **Training Materials:** Induction or refresher training on data responsibilities.

In short: show that every critical dataset has a named owner, defined access criteria, and governance oversight to ensure consistency and accountability.""",

    "DR-03": """Provide proof that privacy and ethical-data-use controls are structured, enforced, and reviewed.

**Key Evidence Types:**

• **Policies & Procedures:** Privacy Policy, Data Ethics Framework, or Acceptable-Use Guidelines referencing AI or analytics.
• **Impact Assessments:** Completed PIAs or Ethical Impact Assessments for projects using personal data.
• **Training Records:** Evidence of staff training in privacy, data handling, and incident management.
• **Access Logs & Audits:** Records showing monitoring of data access and breach-response actions.
• **Communications:** Notices or consent forms explaining data use to clients or citizens.
• **Review Reports:** Internal or external audits evaluating privacy and ethical-data compliance.

In short: demonstrate that privacy, security, and ethical-data principles are not optional-they are embedded, measurable, and actively managed across the organisation.""",

    "DR-04": """Demonstrate that classification, storage, and retention are standardised and enforced across all systems.

**Key Evidence Types:**

• **Policies & Procedures:** Data Classification Policy, Records-Retention Schedule, or Information Security Policy.
• **System Configuration:** Screenshots or settings showing classification labels or automated retention rules.
• **Training Records:** Courses or materials covering classification and secure handling.
• **Audit Reports:** Reviews confirming compliance with retention and disposal standards.
• **Registers:** Logs of data destruction, archival, or re-classification activities.
• **Records Authority:** Approval or alignment with external archival and legal requirements.

In short: show that information is classified, stored, and retained according to defined standards-protecting sensitive data and supporting trustworthy AI operations.""",

    "DR-05": """Provide artefacts showing structured, secure, and consistent access to data across the organisation.

**Key Evidence Types:**

• **Architectural Diagrams:** Data flow or integration maps showing system interoperability.
• **Policies & Frameworks:** Data Sharing or Interoperability Framework defining standards and roles.
• **Technical Configurations:** API documentation, integration scripts, or data platform configurations.
• **Data Catalogues:** Inventories of available datasets with metadata and access permissions.
• **Governance Records:** Meeting minutes or reports addressing data-sharing arrangements.
• **Training Materials:** Courses or guides on responsible data use and integration standards.

In short: demonstrate that the organisation can securely and efficiently access and combine data to enable analytics and AI initiatives.""",

    "DR-06": """Provide evidence that data governance is actively monitored, reviewed, and improved.

**Key Evidence Types:**

• **Meeting Minutes:** Records of governance or committee reviews discussing data performance.
• **Performance Dashboards:** Data-quality metrics, audit results, or compliance KPIs.
• **Improvement Plans:** Action logs or roadmaps documenting governance updates and outcomes.
• **Policy Revisions:** Version-controlled frameworks showing periodic updates.
• **Audit Reports:** Internal or third-party assessments with corrective actions.
• **Training Evidence:** Refresher courses or awareness sessions following governance updates.

In short: demonstrate that data governance is a living framework-monitored, measured, and continually enhanced to maintain trust and readiness for AI.""",

    "TI-01": """Provide artefacts that demonstrate your infrastructure can securely and reliably support AI-readiness activities.

**Key Evidence Types:**

• **Infrastructure Diagrams:** Network or cloud architecture showing security layers and scalability.
• **Security Policies:** IT Security Policy or Cloud Security Standard outlining encryption, access, and patching.
• **Maintenance Records:** Patch schedules, vulnerability scans, or penetration-test reports.
• **Modernisation Plans:** Cloud-migration or digital-transformation roadmaps.
• **Monitoring Reports:** Availability, uptime, or incident-response metrics.
• **Audit Findings:** Independent reviews confirming infrastructure health and security compliance.

In short: show that the environment is modern, secure, and capable of supporting data-driven innovation and future AI workloads.""",

    "TI-02": """Provide documentation showing that systems are interconnected, governed, and technically ready for AI applications.

**Key Evidence Types:**

• **Integration Diagrams:** Architecture maps showing API or middleware connectivity between key systems.
• **Policies & Standards:** Data Integration or Interoperability Framework specifying standards and protocols.
• **Technical Documentation:** API specifications, data schemas, or ETL workflow designs.
• **Security Controls:** Access controls and encryption methods applied to system integrations.
• **Performance Reports:** Monitoring logs demonstrating reliability of data exchange.
• **Audit or Review Findings:** Assessments confirming secure and accurate integration practices.

In short: demonstrate that technology systems are securely integrated and technically equipped to support cross-functional data use and AI adoption.""",

    "TI-03": """Provide evidence that cybersecurity is governed, monitored, and continuously improved.

**Key Evidence Types:**

• **Policies & Frameworks:** Information Security Policy, Cybersecurity Strategy, or ISM/Essential Eight alignment documentation.
• **Monitoring Reports:** SIEM dashboards, intrusion-detection logs, or vulnerability-scan summaries.
• **Access Control Records:** MFA enforcement, privilege reviews, or authentication configurations.
• **Incident Management:** Response plans, breach logs, or after-action reports.
• **Training Records:** Staff awareness or phishing-simulation results.
• **Audit Findings:** Internal or third-party reviews of cyber-maturity.

In short: show that security controls are documented, actively monitored, and aligned to national standards-creating a trustworthy foundation for AI innovation.""",

    "TI-04": """Provide evidence that system and data-recovery processes are formalised, tested, and integrated into governance.

**Key Evidence Types:**

• **Plans & Procedures:** ICT Business Continuity or Disaster Recovery Plans covering AI or analytics environments.
• **Test Reports:** Results from recovery or failover exercises, including lessons learned.
• **Backup Logs:** Automated backup schedules and verification records.
• **Architecture Diagrams:** Redundancy or replication configurations demonstrating resilience design.
• **Risk Registers:** Entries describing continuity controls and RTO/RPO targets.
• **Audit Findings:** Internal or external assurance reports on continuity effectiveness.

In short: show that recovery capabilities are documented, tested, and resilient enough to maintain trust and functionality in AI-enabled operations.""",

    "TI-05": """Provide artefacts showing structured lifecycle and technology-planning practices.

**Key Evidence Types:**

• **Technology Roadmaps:** Documented lifecycle or refresh schedules showing end-of-support tracking.
• **Procurement Policies:** Procedures incorporating lifecycle, interoperability, and security criteria.
• **Asset Registers:** Inventories with system versions, patch levels, and renewal dates.
• **Budget or Planning Papers:** Approved funding for scheduled replacements or upgrades.
• **Review Reports:** Annual or quarterly lifecycle assessments and improvement recommendations.
• **Audit Findings:** Independent reviews confirming lifecycle compliance and risk reduction.

In short: demonstrate that your organisation anticipates change, maintains modern technology, and invests strategically to remain AI-ready and secure.""",

    "TI-06": """Provide documentation showing that AI innovation and experimentation are structured, governed, and risk-aware.

**Key Evidence Types:**

• **Innovation Policies:** Frameworks defining approval, risk, and ethical-review requirements for pilots.
• **Sandbox Documentation:** Architecture or configurations of test environments separated from production.
• **Pilot Registers:** Logs of AI or automation trials, including approvals and review outcomes.
• **Governance Minutes:** Evidence of oversight by risk, ethics, or innovation committees.
• **Data-Protection Controls:** Use of de-identified, synthetic, or anonymised data in testing.
• **Post-Trial Reports:** Evaluations or lessons-learned summaries following AI experiments.

In short: demonstrate that innovation is deliberate, supported, and securely managed-enabling exploration of AI while maintaining compliance and public trust.""",

    "PC-01": """Provide artefacts that show AI awareness is being built systematically.

**Key Evidence Types:**

• **Training Records:** Attendance logs for AI awareness or digital literacy sessions.
• **Communication Materials:** Intranet posts, newsletters, or videos introducing AI concepts.
• **Surveys or Feedback:** Results from staff AI-awareness or ethics questionnaires.
• **Learning Modules:** Online or in-person courses explaining AI basics and responsible-use principles.
• **Workshop Summaries:** Notes or outcomes from AI information sessions or Q&A forums.
• **Leadership Endorsements:** Executive messages promoting AI education and responsible innovation.

In short: demonstrate that AI awareness is not incidental-it is an intentional, measurable part of organisational learning and culture.""",

    "PC-02": """Show evidence that AI skills and competencies are being developed systematically.

**Key Evidence Types:**

• **Training Plans:** Annual or role-specific development programs including AI or data-literacy modules.
• **Attendance Records:** Participation logs for courses, workshops, or conferences.
• **Competency Frameworks:** Documents outlining required AI-related skills per role.
• **Partnership Agreements:** MOUs or contracts with training or academic institutions.
• **Learning Outcomes:** Assessment results, certifications, or completion statistics.
• **Budget Allocations:** Funding approvals for capability-building initiatives.

In short: demonstrate that AI skills development is planned, resourced, and linked to career growth and governance maturity.""",

    "PC-03": """Provide evidence that innovation and collaboration are actively promoted within a responsible governance framework.

**Key Evidence Types:**

• **Policies & Frameworks:** Innovation or Digital Transformation Policy referencing AI experimentation and governance.
• **Program Records:** Innovation lab documentation, hackathon outcomes, or pilot project registers.
• **Recognition Schemes:** Awards or incentives encouraging ethical technology use.
• **Communications:** Internal campaigns celebrating innovation success stories.
• **Training:** Workshops on creative problem-solving and responsible AI exploration.
• **Committee Minutes:** Governance records showing oversight of innovation initiatives.

In short: demonstrate that innovation is actively encouraged, collaborative, and balanced by responsible AI governance.""",

    "PC-04": """Provide evidence that ethics and accountability are actively promoted and understood.

**Key Evidence Types:**

• **Training Records:** Attendance logs for AI ethics, bias, or data-responsibility sessions.
• **Guidance Materials:** Ethics toolkits, decision guides, or checklists used in projects.
• **Communications:** Internal campaigns promoting fairness, transparency, or human oversight.
• **Policy References:** Codes of Conduct, Responsible AI Principles, or HR policies referencing ethics.
• **Feedback Surveys:** Employee surveys measuring ethical awareness or confidence in raising concerns.
• **Governance Oversight:** Committee minutes or reports discussing ethical implications of AI.

In short: demonstrate that ethical responsibility is embedded, measurable, and understood across all levels of the organisation.""",

    "PC-05": """Provide artefacts showing that workforce adaptation and change management are embedded into AI planning.

**Key Evidence Types:**

• **Change-Management Plans:** Documents outlining communication, engagement, and training activities for technology projects.
• **Impact Assessments:** Workforce or organisational-change analyses identifying affected roles.
• **Training & Reskilling Programs:** Course materials or enrolment records for transitioning staff.
• **Consultation Records:** Meeting notes or feedback from staff forums or unions.
• **Communications:** Announcements, newsletters, or FAQs addressing workforce changes.
• **Metrics:** Surveys measuring staff confidence or readiness for automation.

In short: demonstrate that change is anticipated, communicated, and supported-ensuring employees remain empowered and engaged through AI transformation.""",

    "PC-06": """Provide evidence that AI initiatives and workforce practices incorporate diversity, inclusion, and accessibility.

**Key Evidence Types:**

• **Policies & Frameworks:** Diversity, Equity, and Inclusion Policy or Accessibility Strategy referencing AI or digital transformation.
• **Recruitment Records:** Evidence of diverse hiring panels or inclusive job descriptions.
• **Project Documentation:** Accessibility testing reports or inclusive design reviews.
• **Committee Memberships:** Representation from diverse backgrounds in AI governance groups.
• **Training Materials:** Programs on inclusive design, bias awareness, or accessibility.
• **Performance Reports:** Metrics tracking diversity and accessibility outcomes in AI projects.

In short: demonstrate that diversity and accessibility are deliberate, measurable priorities shaping both your workforce and AI-enabled services.""",

    "PR-01": """Provide evidence that policies governing AI and data-driven technologies are formalised, current, and accessible.

**Key Evidence Types:**

• **Governance Policies:** Approved Responsible AI Policy, AI Ethics Framework, or AI Use Standard.
• **Supporting Documents:** Privacy, Data Governance, ICT Security, or Risk Management Policies referencing AI.
• **Approval Records:** Executive or board endorsement of policy frameworks.
• **Version Control:** Policy review schedules or document registers showing regular updates.
• **Communications:** Intranet or public announcements sharing policy content with staff or stakeholders.
• **Training Records:** Staff awareness or onboarding sessions covering AI policy requirements.

In short: demonstrate that responsible AI is governed by approved, integrated policies reflecting ethical principles and legal obligations.""",

    "PR-02": """Provide documentation that demonstrates structured compliance with AI and privacy requirements.

**Key Evidence Types:**

• **Compliance Registers:** Logs mapping legal obligations to policies and controls.
• **Audit Reports:** Internal or external reviews of privacy or data-handling compliance.
• **Privacy Impact Assessments:** Completed PIAs for AI or data-driven projects.
• **Policies & Procedures:** Privacy, Information Security, and AI Governance policies referencing relevant laws.
• **Training Records:** Completion rates for privacy and compliance training modules.
• **Incident Logs:** Records of data breaches, remedial actions, and regulator notifications.
• **Board or Committee Minutes:** Evidence of oversight of compliance performance and legislative updates.

In short: show that compliance with AI and privacy laws is proactive, documented, and continuously reviewed-not reactive or assumed.""",

    "PR-03": """Provide proof that vendor compliance and AI-related risk are actively governed.

**Key Evidence Types:**

• **Procurement Templates:** RFPs, RFQs, or contract templates including AI-ethics or data-protection clauses.
• **Due-Diligence Reports:** Supplier-risk assessments, background checks, or compliance questionnaires.
• **Contract Registers:** Evidence of executed agreements referencing AI governance or data-handling terms.
• **Audit Records:** Vendor-audit reports or third-party assurance attestations (SOC 2, ISO 27001).
• **Performance Monitoring:** KPIs or dashboards measuring supplier compliance over time.
• **Governance Committee Minutes:** Oversight discussions of vendor or outsourcing risks.

In short: demonstrate that third-party AI risk is assessed, contractually controlled, and continually monitored-not left to vendor discretion.""",

    "PR-04": """Provide evidence showing deliberate mapping and application of AI governance frameworks.

**Key Evidence Types:**

• **Mapping Documents:** Crosswalks comparing internal policies to ISO 42001, NIST AI RMF, or similar standards.
• **Gap-Assessment Reports:** Findings and action plans addressing areas for improvement.
• **Updated Policies:** Revised Responsible AI or Data Governance Policies reflecting framework alignment.
• **Audit Reports:** Internal or external assessments confirming compliance with selected frameworks.
• **Training Materials:** Sessions or briefings introducing staff to framework principles.
• **Committee Minutes:** Governance or risk committee discussions reviewing framework adoption progress.

In short: demonstrate that AI governance is guided by-and continuously compared to-globally recognised standards, ensuring maturity and defensibility.""",

    "PR-05": """Provide documentation showing that policy compliance is actively monitored, reported, and improved.

**Key Evidence Types:**

• **Audit Reports:** Internal or external audit findings covering AI, data, or ICT policies.
• **Review Schedules:** Calendars or registers documenting planned policy reviews.
• **Compliance Registers:** Logs tracking adherence, non-compliance, and corrective actions.
• **Committee Minutes:** Records of executive or governance meetings discussing policy performance.
• **Performance Dashboards:** Metrics showing compliance rates or policy adoption levels.
• **Remediation Evidence:** Completed action plans addressing policy gaps or audit findings.

In short: demonstrate that policy compliance is not assumed-it is verified, measured, and continuously strengthened through structured oversight.""",

    "PR-06": """Provide artefacts showing that AI, data, and technology policies are well communicated and consistently enforced.

**Key Evidence Types:**

• **Training Records:** Completion reports for policy-awareness or compliance-training modules.
• **Communication Materials:** Newsletters, intranet posts, or leadership messages promoting policy understanding.
• **Policy Repository:** Screenshots or documentation of centralised policy access points.
• **Enforcement Logs:** Records of policy breaches, investigations, and corrective actions.
• **Surveys or Feedback:** Staff awareness assessments or post-training evaluation results.
• **Committee Oversight:** Minutes from governance or HR meetings addressing policy adherence.

In short: demonstrate that policy compliance is reinforced through communication, education, and consistent accountability across all levels of the organisation.""",

    "RE-01": """Provide artefacts showing that AI-related risks are formally identified, recorded, and managed.

**Key Evidence Types:**

• **Risk Registers:** Entries referencing AI, data, or automation-related risks.
• **Risk Frameworks:** Enterprise or project-level frameworks incorporating AI risk criteria.
• **Assessment Templates:** Standardised risk-assessment forms or checklists for emerging technologies.
• **Meeting Minutes:** Governance or risk-committee discussions of AI-related risks.
• **Audit or Review Reports:** Evaluations of AI risk controls or management practices.
• **Training Materials:** Staff guidance or workshops on identifying AI-specific risks.

In short: demonstrate that AI risk is visible, documented, and managed through the same disciplined processes applied to all critical business risks.""",

    "RE-02": """Provide documentation proving that AI bias risks are identified, managed, and monitored.

**Key Evidence Types:**

• **Data Audits:** Reports analysing demographic balance or representation in datasets.
• **Testing Records:** Bias-testing outputs, fairness metrics, or validation scripts.
• **Governance Oversight:** Ethics or review committee minutes discussing bias risks.
• **Policies & Guidelines:** Fairness and Inclusion Policy or AI Bias Mitigation Standard.
• **Training Records:** Staff participation in workshops on bias awareness and mitigation.
• **Remediation Actions:** Logs of bias issues identified and corrective measures applied.

In short: demonstrate that the organisation understands, measures, and mitigates bias to ensure equitable and ethical AI outcomes.""",

    "RE-03": """Provide artefacts showing that AI or analytics processes are transparent and explainable.

**Key Evidence Types:**

• **Project Documentation:** Model design documents, decision logs, and feature-importance reports.
• **Public Statements:** Published explainability summaries or FAQs for AI systems affecting the community.
• **Governance Records:** Committee or ethics-review minutes addressing transparency requirements.
• **Technical Tools:** Outputs from explainability frameworks such as LIME, SHAP, or model cards.
• **Training Materials:** Staff sessions on communicating AI decisions responsibly.
• **Audit Reports:** Reviews verifying that AI decisions are traceable and understandable.

In short: demonstrate that AI decision-making is visible, explainable, and documented-ensuring stakeholders can understand and trust organisational use of AI.""",

    "RE-04": """Provide evidence that accountability and human oversight are clearly established for AI use.

**Key Evidence Types:**

• **Governance Policies:** Documents defining roles and approval authorities for AI-assisted decisions.
• **Process Maps:** Diagrams or workflows showing human checkpoints before AI outcomes are applied.
• **Decision Logs:** Records of human review and approval for AI-generated recommendations.
• **Training Records:** Evidence of staff education on AI oversight responsibilities.
• **Audit Trails:** System logs showing manual intervention or sign-off in AI processes.
• **Ethics or Risk Committee Minutes:** Discussions verifying oversight effectiveness and accountability gaps.

In short: demonstrate that human oversight is active, documented, and central to how your organisation uses AI-ensuring responsibility never shifts to the system itself.""",

    "RE-05": """Provide evidence that stakeholder engagement on AI ethics and impacts is planned, inclusive, and transparent.

**Key Evidence Types:**

• **Engagement Plans:** Frameworks outlining consultation methods, frequency, and participants.
• **Workshop Records:** Meeting notes, attendance lists, or summaries from ethics or community discussions.
• **Feedback Reports:** Documents showing stakeholder concerns and organisational responses.
• **Governance Minutes:** Committee discussions referencing stakeholder input in AI decisions.
• **Public Disclosures:** Reports or website updates summarising engagement outcomes.
• **Surveys or Questionnaires:** Feedback instruments used to gauge community trust or expectations.

In short: demonstrate that your organisation listens, documents, and responds to stakeholder input to guide the ethical use of AI and data.""",

    "RE-06": """Provide documentation showing that AI-related incidents are tracked, reviewed, and used for continuous improvement.

**Key Evidence Types:**

• **Incident Logs:** Registers documenting ethical or AI-risk events, investigations, and resolutions.
• **Policies & Procedures:** Incident-response or ethics-review frameworks referencing AI.
• **Root-Cause Reports:** Analyses detailing contributing factors and remedial actions.
• **Committee Minutes:** Governance or ethics-board discussions reviewing incident trends.
• **Training Updates:** Revisions to content or guidance following lessons learned.
• **Audit Findings:** Verification that corrective actions were implemented and effective.

In short: demonstrate that the organisation treats every AI or ethical incident as an opportunity to learn, improve, and strengthen governance maturity.""",

    "CL-01": """Provide evidence that lessons from AI or data projects are captured, shared, and acted upon.

**Key Evidence Types:**

• **Post-Implementation Reviews:** Completed review reports or "lessons learned" templates.
• **Improvement Registers:** Logs tracking actions, responsible owners, and completion status.
• **Meeting Minutes:** Records from governance or project boards discussing review outcomes.
• **Knowledge Repositories:** Shared folders, wikis, or databases storing project insights.
• **Policy Updates:** Revisions to frameworks or templates referencing implemented lessons.
• **Training Materials:** Updated guidance or learning modules incorporating prior findings.

In short: demonstrate that AI experiences translate into tangible improvements-creating a continuous feedback loop that strengthens governance maturity over time.""",

    "CL-02": """Provide documentation showing that AI governance and risk processes are routinely evaluated and improved.

**Key Evidence Types:**

• **Review Reports:** Periodic assessments of AI governance and risk frameworks.
• **Performance Dashboards:** Metrics tracking policy adoption, incident response, or risk closure rates.
• **Audit Findings:** Internal or third-party reviews addressing AI governance effectiveness.
• **Committee Minutes:** Records of governance or risk discussions on framework performance.
• **Improvement Logs:** Registers documenting actions taken based on review outcomes.
• **Updated Policies:** Revised frameworks showing incorporation of review findings.

In short: demonstrate that AI governance is actively measured, reviewed, and refined-not left to drift as technology and risk evolve.""",

    "CL-03": """Provide documentation that demonstrates active benchmarking and comparison of AI practices.

**Key Evidence Types:**

• **Benchmarking Reports:** Internal or external assessments comparing maturity against frameworks or peers.
• **Maturity Heatmaps:** Results from AI governance or risk self-assessments.
• **Improvement Plans:** Actions derived from benchmarking outcomes.
• **External Audit Certificates:** Evidence of conformance or independent validation.
• **Committee Minutes:** Governance discussions reviewing benchmarking insights.
• **Communications:** Reports or presentations sharing benchmarking outcomes with stakeholders.

In short: demonstrate that benchmarking is regular, evidence-based, and actively shapes strategic decisions and governance improvements.""",

    "CL-04": """Provide evidence that AI feedback is systematically collected, analysed, and acted upon.

**Key Evidence Types:**

• **Feedback Reports:** Summaries of staff or stakeholder feedback on AI tools or governance.
• **Surveys or Forms:** Examples of questionnaires or online channels for AI-related feedback.
• **Improvement Registers:** Logs showing actions taken in response to received feedback.
• **Meeting Minutes:** Records of governance or ethics committees reviewing feedback trends.
• **Communications:** Updates to stakeholders outlining changes made based on their input.
• **Audit or Review Records:** Assessments confirming the effectiveness of feedback mechanisms.

In short: demonstrate that feedback on AI use is continuous, inclusive, and directly drives governance and performance improvements.""",

    "CL-05": """Provide documentation showing that AI governance is audited and measured for performance improvement.

**Key Evidence Types:**

• **Audit Reports:** Internal or external reviews addressing AI governance or ethical-risk controls.
• **Performance Dashboards:** KPIs or scorecards tracking AI governance outcomes.
• **Improvement Registers:** Logs of actions arising from audits or performance assessments.
• **Committee Minutes:** Risk, Audit, or Governance Committee discussions reviewing AI performance.
• **Assurance Plans:** Schedules including AI-related audits or monitoring activities.
• **Follow-up Reports:** Evidence that audit findings have been remediated or verified.

In short: demonstrate that AI governance is validated through structured, data-driven assurance processes that deliver measurable, sustained improvement.""",

    "CL-06": """Provide evidence that the organisation encourages, supports, and sustains a culture of AI learning and improvement.

**Key Evidence Types:**

• **Training Programs:** Records of staff participation in AI, data, or innovation learning activities.
• **Professional Development Plans:** Inclusion of AI or digital-skills goals in employee objectives.
• **Innovation Platforms:** Internal forums, communities of practice, or ideation challenges.
• **Recognition Schemes:** Awards or incentives promoting continuous learning and innovation.
• **Survey Results:** Staff feedback showing engagement in learning and openness to digital transformation.
• **Strategic Documents:** Workforce or digital strategies referencing learning culture and AI capability development.

In short: demonstrate that AI readiness is sustained through an organisational culture that values learning, reflection, and continuous improvement.""",
}

print(f"Total evidence types entries: {len(EVIDENCE_TYPES_DATA)}")
print("Evidence types codes:", sorted(EVIDENCE_TYPES_DATA.keys()))
