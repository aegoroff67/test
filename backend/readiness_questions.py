# AI Readiness Assessment Questions
# 8 Domains, 48 Questions Total
# Scoring: Foundational (0), Developing (1), Established (2), Leading (3)

READINESS_QUESTIONS_DATA = [
    # Domain 1: Strategic Alignment & Awareness (6 questions)
    {
        "code": "SA-01",
        "text": "How well does your organisation's overall strategy recognise and plan for the opportunities and risks of AI adoption?",
        "explanation": "Context: Strategic awareness ensures that AI adoption supports—not surprises—the organisation's mission and objectives. This question evaluates whether AI is acknowledged in your strategic or digital transformation plans and if leadership understands both its potential value and associated risks. Example: A council's Digital Strategy includes an \"Emerging Technologies\" section describing how AI could improve service delivery, while committing to ethical use, data privacy, and staff upskilling.",
        "domain_order": 1,
        "order": 1,
        "foundational": "AI is not referenced in strategic or digital plans; leadership has limited awareness of its relevance.",
        "developing": "AI opportunities are discussed informally or appear in isolated initiatives but lack formal planning.",
        "established": "AI is referenced within digital or corporate strategies with defined objectives, benefits, and risk awareness.",
        "leading": "AI is embedded across enterprise strategy, guided by ethical principles and measured through KPIs and review cycles.",
        "additional_guide": """Embedding AI within corporate strategy aligns innovation with purpose and accountability.
• **Start with Vision and Values:** Articulate how AI supports organisational goals-efficiency, service quality, community engagement-while upholding ethics and transparency.
• **Link to Risk Management:** Address potential harms such as bias, privacy breaches, or reputational impact.
• **Define Roadmaps:** Set short-term exploration goals and long-term capability building milestones.
• **Secure Executive Ownership:** Assign responsibility to a senior leader or steering committee.
• **Review Regularly:** Re-evaluate strategic AI priorities annually as technology and regulation evolve.
A well-defined AI strategy ensures initiatives are intentional, value-driven, and aligned with organisational capacity.""",
        "evidence_types": """To demonstrate alignment, provide artefacts showing that AI is considered strategically, not just tactically.

**Key Evidence Types:**

• **Strategic Plans:** Corporate, ICT, or Digital Strategies referencing AI objectives, ethics, or readiness.
• **Board or Executive Minutes:** Discussions of AI as part of strategic planning or transformation.
• **Briefing Papers:** Presentations or whitepapers assessing AI opportunities and risks.
• **Performance Frameworks:** KPIs or outcome measures tracking AI progress.
• **Risk Registers:** Strategic entries acknowledging AI impacts or dependencies.
• **Stakeholder Engagement:** Workshops or consultations on AI vision and values.

**In short:** show that AI is visible in strategic intent and actively managed as part of corporate planning."""
    },
    {
        "code": "SA-02",
        "text": "How effectively does leadership demonstrate understanding and sponsorship of AI initiatives or readiness efforts?",
        "explanation": "Context: Leadership commitment is critical to safe and sustainable AI adoption. Without visible sponsorship, AI exploration can stall or proceed without proper oversight. This question assesses whether senior leaders actively champion responsible AI, allocate resources, and set expectations for ethical use. Example: A CEO or Director General includes \"responsible AI innovation\" in corporate goals, funds exploratory pilots, and participates in briefings to understand associated risks and opportunities.",
        "domain_order": 1,
        "order": 2,
        "foundational": "Leadership has limited understanding of AI; no visible support or guidance for AI-related initiatives.",
        "developing": "Senior leaders express interest but engagement is informal or inconsistent.",
        "established": "Leadership demonstrates clear sponsorship through communications, resource allocation, or participation in AI oversight forums.",
        "leading": "Executives champion responsible AI organisation-wide, integrating it into strategy, KPIs, and culture with ongoing review of outcomes.",
        "additional_guide": """Effective leadership drives responsible innovation.
• **Educate and Engage:** Provide briefings or workshops for executives on AI's potential, ethical implications, and governance frameworks (e.g., ISO 42001, NIST AI RMF).
• **Define Strategic Roles:** Assign a senior leader as AI sponsor accountable for readiness, ethics, and compliance.
• **Integrate AI into Corporate Messaging:** Include responsible AI in vision statements, board reports, and stakeholder communications.
• **Provide Resources:** Allocate funding for training, pilot projects, or governance activities to demonstrate tangible commitment.
• **Measure and Review:** Evaluate leadership engagement through regular progress reports or maturity assessments.
Visible, informed leadership signals that AI is a strategic priority aligned with organisational values.""",
        "evidence_types": """Provide proof that leaders actively support AI readiness and governance.

**Key Evidence Types:**

• **Leadership Communications:** CEO or executive statements referencing responsible AI adoption.
• **Strategic Plans & Reports:** Inclusion of AI goals or ethical commitments endorsed by leadership.
• **Meeting Minutes:** Evidence of executive participation in AI governance or risk committees.
• **Budget Allocations:** Funding for AI training, pilots, or governance functions.
• **Performance Documents:** Executive KPIs tied to AI readiness or digital transformation.
• **Briefings & Workshops:** Records of leadership attendance or sponsorship of AI capability sessions.

**In short:** show that leadership is not merely aware of AI but is visibly leading and resourcing its responsible use."""
    },
    {
        "code": "SA-03",
        "text": "How clearly are the organisation's AI goals, benefits, and success measures defined and communicated?",
        "explanation": "Context: Clear objectives ensure AI adoption aligns with measurable outcomes and public value. Without defined goals or success criteria, AI exploration risks becoming unfocused or misaligned with organisational priorities. This question assesses whether your organisation has articulated what it aims to achieve through AI and how progress will be tracked and communicated. Example: A council defines three AI objectives—improve service responsiveness, reduce manual workloads, and enhance citizen engagement—supported by measurable performance indicators such as response time reductions or customer satisfaction improvements.",
        "domain_order": 1,
        "order": 3,
        "foundational": "AI goals are undefined or limited to ad hoc experimentation with no clear success measures.",
        "developing": "General objectives exist but are qualitative, inconsistently communicated, or lack defined metrics.",
        "established": "AI goals are documented, linked to business outcomes, and supported by defined performance indicators.",
        "leading": "AI goals are organisation-wide, measurable, regularly reviewed, and transparently communicated to stakeholders.",
        "additional_guide": """Establishing clear goals for AI readiness builds accountability and alignment.
• **Start with Purpose:** Identify specific problems AI can solve-efficiency, customer experience, or data-driven decision-making.
• **Link to Organisational Outcomes:** Tie AI goals to strategic KPIs or service delivery benchmarks.
• **Define Success Metrics:** Use measurable indicators such as time saved, accuracy improvements, or stakeholder satisfaction.
• **Communicate Broadly:** Ensure staff and stakeholders understand why AI is being explored and what success looks like.
• **Review and Adapt:** Assess AI outcomes annually and refine objectives based on lessons learned.
Clear, measurable goals ensure AI remains purposeful, transparent, and value-driven rather than purely experimental.""",
        "evidence_types": """Demonstrate that AI objectives and measures of success are defined, tracked, and shared across the organisation.

**Key Evidence Types:**

• **Strategy Documents:** Digital or Corporate Plans outlining AI goals and benefits.
• **Performance Frameworks:** KPIs or scorecards linked to AI initiatives.
• **Project Charters:** Business cases articulating AI success measures and expected outcomes.
• **Communications:** Internal newsletters, briefings, or dashboards explaining AI objectives.
• **Review Reports:** Post-implementation or pilot reviews assessing success against KPIs.
• **Stakeholder Feedback:** Surveys or engagement summaries validating communicated goals.

**In short:** show that AI objectives are purposeful, measurable, and visible across the organisation."""
    },
    {
        "code": "SA-04",
        "text": "How well are AI initiatives aligned with the organisation's ethical values, community expectations, and public trust obligations?",
        "explanation": "Context: AI adoption must reflect the organisation's ethical standards and its duty to the community it serves. Misalignment between innovation and values can undermine public confidence. This question assesses whether AI exploration considers fairness, transparency, and community impact during planning and decision-making. Example: A local council evaluating an AI-driven customer-service chatbot holds a community consultation to ensure the technology aligns with accessibility and inclusivity commitments before deployment.",
        "domain_order": 1,
        "order": 4,
        "foundational": "Ethical or community impacts of AI are not considered in planning or decision-making.",
        "developing": "Ethical discussions occur informally; limited consultation or documentation exists.",
        "established": "Ethical principles and community expectations are referenced in AI planning and procurement processes.",
        "leading": "AI initiatives are routinely reviewed for ethical alignment, with community input and transparent reporting on outcomes.",
        "additional_guide": """Public trust depends on visible alignment between AI use and organisational values.
• **Define Ethical Commitments:** Translate values such as fairness, inclusivity, and accountability into AI-specific principles.
• **Engage Stakeholders:** Consult with affected groups, employees, and the public early in AI planning.
• **Assess Impacts:** Use simple checklists or ethics impact assessments to evaluate fairness, privacy, and social effects.
• **Document Transparency:** Clearly communicate AI purpose, data use, and safeguards to maintain trust.
• **Review Regularly:** Revisit ethical alignment as technology, expectations, or legislation evolve.
Embedding ethics ensures AI enhances-not erodes-trust, helping organisations demonstrate integrity and accountability in every AI initiative.""",
        "evidence_types": """Provide evidence that AI planning and decision-making incorporate ethical and community considerations.

**Key Evidence Types:**

• **Ethics Frameworks:** Responsible AI Principles or Codes of Conduct referencing fairness, transparency, and accountability.
• **Consultation Records:** Stakeholder or community engagement notes on AI projects.
• **Impact Assessments:** Ethical, privacy, or social impact analyses for proposed AI uses.
• **Procurement Documents:** Evaluation criteria requiring ethical compliance by vendors.
• **Communication Artefacts:** Public statements or reports outlining ethical commitments in AI adoption.
• **Monitoring Reports:** Reviews or dashboards tracking ethical and community outcomes.

**In short:** demonstrate that AI decisions are guided by values, informed by stakeholders, and transparent to the community."""
    },
    {
        "code": "SA-05",
        "text": "How effectively does the organisation communicate its AI vision, goals, and ethical commitments to staff and stakeholders?",
        "explanation": "Context: Clear communication builds understanding and trust in AI adoption. Without consistent messaging, employees may resist change or misunderstand AI's purpose, and the public may perceive risk rather than benefit. This question evaluates whether the organisation proactively shares its AI vision, objectives, and principles across internal and external audiences. Example: A not-for-profit publishes a short \"AI in Our Organisation\" statement explaining how AI supports its mission, the safeguards in place, and how employees can raise ethical concerns or ideas.",
        "domain_order": 1,
        "order": 5,
        "foundational": "No communication about AI vision or values; staff and stakeholders are unaware of related initiatives.",
        "developing": "Limited or informal communication occurs, mainly within specific teams or projects.",
        "established": "AI goals and ethical principles are communicated organisation-wide through briefings, policies, or reports.",
        "leading": "A clear AI narrative is embedded in corporate messaging, reinforced through continuous engagement, updates, and feedback channels.",
        "additional_guide": """Transparent communication ensures AI adoption is understood, supported, and trusted.
• **Craft a Clear Narrative:** Explain why the organisation is exploring AI, expected benefits, and how it aligns with ethical values.
• **Use Accessible Language:** Avoid technical jargon; focus on how AI improves outcomes for staff or community.
• **Engage Early and Often:** Hold briefings, Q&A sessions, or town halls to address misconceptions and collect feedback.
• **Publish Ethical Commitments:** Make Responsible AI Principles publicly available to demonstrate transparency.
• **Create Two-Way Channels:** Encourage questions or feedback on AI use, showing accountability and openness.
Consistent, open communication builds confidence, fosters collaboration, and strengthens organisational readiness for AI.""",
        "evidence_types": """Provide documentation that AI vision and principles are shared across the organisation and with key stakeholders.

**Key Evidence Types:**

• **Internal Communications:** Staff emails, newsletters, or intranet posts explaining AI objectives and ethics.
• **Public Materials:** Website statements, brochures, or annual reports describing AI strategy and safeguards.
• **Leadership Briefings:** Presentations or videos from executives outlining the AI vision.
• **Feedback Mechanisms:** Surveys or consultation summaries gauging staff or public understanding.
• **Training & Awareness:** Sessions introducing AI goals and responsible-use expectations.
• **Measurement Reports:** Engagement metrics or feedback results showing communication reach and effectiveness.

**In short:** show that AI communication is deliberate, transparent, and builds both internal alignment and external trust."""
    },
    {
        "code": "SA-06",
        "text": "How well does the organisation evaluate and adapt its AI strategy in response to changing technologies, risks, and community expectations?",
        "explanation": "Context: AI environments evolve rapidly, and strategies must remain flexible to stay effective and trustworthy. This question examines whether your organisation periodically reviews its AI approach to reflect new technologies, emerging risks, and stakeholder expectations. Continuous evaluation ensures that AI remains aligned with organisational goals, values, and evolving regulatory landscapes. Example: A council updates its AI Readiness Roadmap annually, incorporating lessons learned from pilots, new Australian AI standards, and community feedback about responsible data use.",
        "domain_order": 1,
        "order": 6,
        "foundational": "AI plans or strategies are static and rarely reviewed; adaptation occurs only when problems arise.",
        "developing": "Occasional updates occur in response to external changes, but there is no formal review process.",
        "established": "Regular AI strategy reviews are built into planning cycles, incorporating risk, technology, and stakeholder input.",
        "leading": "Continuous improvement processes are embedded, using metrics, horizon scanning, and public feedback to refine AI strategy and governance.",
        "additional_guide": """Sustained readiness requires active monitoring and adaptation.
• **Set Review Intervals:** Align AI strategy reviews with annual corporate planning or audit cycles.
• **Monitor Emerging Trends:** Track developments in regulation, technology, and ethics (e.g., AI Safety Standard, ISO 42001).
• **Collect Feedback:** Use staff, partner, and community feedback to assess perception and impact.
• **Evaluate Outcomes:** Compare actual benefits, costs, and risks against planned objectives.
• **Document and Communicate Updates:** Share revisions transparently to maintain confidence and demonstrate responsiveness.
Embedding regular reviews fosters agility, compliance, and trust - essential for organisations adopting AI responsibly in dynamic environments.""",
        "evidence_types": """Demonstrate that AI strategy and readiness are periodically evaluated, updated, and communicated.

**Key Evidence Types:**

• **Review Schedules:** Planning calendars or policy schedules specifying AI strategy review frequency.
• **Updated Strategies:** Revised digital or AI roadmaps showing version control and change history.
• **Meeting Minutes:** Records from executive, audit, or governance meetings discussing AI reviews.
• **Risk Registers:** Updates reflecting newly identified AI threats or opportunities.
• **Feedback Reports:** Staff or community surveys informing AI strategic adjustments.
• **Audit Findings:** Internal or third-party assessments confirming continuous improvement practices.

**In short:** provide clear evidence that AI strategy is a living document - actively reviewed, adapted, and improved over time."""
    },
    # Domain 2: Governance Foundations (6 questions)
    {
        "code": "GF-01",
        "text": "How clearly defined are the organisation's AI governance structures and leadership roles?",
        "explanation": "Context: Clear AI governance ensures accountability, consistency, and responsible innovation. Without defined leadership and oversight, AI initiatives can become fragmented, increasing ethical and operational risks. This question assesses whether your organisation has formal structures—such as a Responsible AI Committee or Chief AI Officer—that guide how AI is developed, procured, and monitored. Example: A council establishes an AI Governance Committee chaired by the CIO, including Risk, Legal, HR, and Data Science members, responsible for reviewing project proposals and ethical considerations.",
        "domain_order": 2,
        "order": 1,
        "foundational": "AI responsibilities are informal or unclear, with no defined governance body or accountability.",
        "developing": "Partial oversight exists through specific roles, but governance remains fragmented or inconsistent.",
        "established": "A formal AI governance framework and defined leadership roles (e.g., Chief AI Officer, Ethics Committee) are in place and active.",
        "leading": "Enterprise-wide governance is embedded, with executive sponsorship, cross-functional representation, and periodic effectiveness reviews.",
        "additional_guide": """AI governance defines who makes decisions, how risks are managed, and how ethical standards are upheld. To strengthen this:
• **Define Roles and Accountability:** Assign a senior executive (e.g., Chief AI Officer) and define oversight responsibilities across departments.
• **Create Cross-Functional Committees:** Include Legal, Risk, Data, HR, and Communications to ensure diverse perspectives.
• **Embed into Corporate Governance:** Integrate AI governance into risk management and digital transformation programs.
• **Establish Decision Pathways:** Document who approves, audits, and escalates AI-related decisions.
• **Benchmark Regularly:** Review governance effectiveness annually against ISO 42001 or NIST AI RMF.
Effective AI governance builds transparency, aligns innovation with organisational values, and reduces reputational and compliance risks.""",
        "evidence_types": """To demonstrate compliance, provide evidence that accountability and oversight for AI are formally defined and operating effectively.

**Key Evidence Types:**

• **Policies & Frameworks:** Approved AI Governance Policy or Responsible AI Framework detailing roles, responsibilities, and decision rights.
• **Organisational Structure:** Role descriptions (e.g., Chief AI Officer, Ethics Lead) and governance committee Terms of Reference.
• **Meeting Records:** Minutes or reports from AI Governance or Ethics Committees showing project reviews or decisions.
• **Integration Evidence:** AI governance references in enterprise risk, privacy, or data policies.
• **Performance & Review:** Internal audits or scorecards evaluating AI governance effectiveness.
• **Training & Awareness:** Records of leadership training on AI responsibilities and ethics.

**In short:** show a structured, cross-functional governance model with documented oversight and active executive ownership."""
    },
    {
        "code": "GF-02",
        "text": "To what extent are AI responsibilities and decision-making roles defined across the organisation?",
        "explanation": "Context: Clearly delineating AI responsibilities prevents duplication, confusion, and unmanaged risk. This question examines whether departments understand their role in identifying opportunities, assessing risks, and approving AI-related actions. Example: A not-for-profit documents AI responsibilities in its ICT Policy, defining who can authorise pilot projects, who manages vendor risk assessments, and who ensures ethical compliance.",
        "domain_order": 2,
        "order": 2,
        "foundational": "No defined AI responsibilities; decisions are ad hoc or based on individual initiative.",
        "developing": "Some AI tasks allocated informally to ICT or data teams, but accountability remains unclear.",
        "established": "Documented responsibilities exist across relevant functions (ICT, Legal, Risk, HR).",
        "leading": "Roles are embedded organisation-wide with clear escalation paths and accountability integrated into job descriptions.",
        "additional_guide": """Define "who does what" for AI. Start by mapping responsibilities across departments-data owners, model developers, compliance officers, and senior approvers. Use a RACI matrix (Responsible, Accountable, Consulted, Informed) to formalise accountability. Link responsibilities to performance plans or KPIs to ensure sustainability.
As capability grows, create cross-functional teams that coordinate decisions, share lessons learned, and monitor emerging risks. Regularly review and update these roles to reflect new AI use cases or regulatory expectations.
Structured accountability reduces ambiguity, improves efficiency, and ensures that ethical oversight remains consistent even as staff change or projects scale.""",
        "evidence_types": """To demonstrate compliance, provide evidence that the organisation's AI vision and strategy are clearly documented, aligned with business objectives, and supported by leadership commitment.

• **Role Documents:** Position Descriptions, RACI matrices, or Governance Charters assigning AI accountabilities.
• **Committee TORs:** Clear AI decision-making roles in Ethics or Risk Committees.
• **Performance Plans:** KPIs linking job roles to AI governance.
• **Training Records:** Evidence of staff briefings on AI responsibilities.
• **Internal Audits:** Reviews confirming AI roles are known and effective.

**In short:** demonstrate that everyone from leadership to project teams knows their role in AI decisions and oversight."""
    },
    {
        "code": "GF-03",
        "text": "How effectively are AI risk and ethical considerations integrated into existing governance frameworks?",
        "explanation": "Context: Integrating AI into existing governance avoids duplication and ensures ethical oversight is consistent with corporate values. This question explores whether AI is embedded in established frameworks such as enterprise risk management, data governance, or ICT change control. Example: A council includes \"AI Risk and Ethics\" as a standing agenda item in its ICT Governance Committee to ensure all AI pilots undergo ethical review.",
        "domain_order": 2,
        "order": 3,
        "foundational": "No references to AI within governance frameworks.",
        "developing": "AI occasionally discussed but not formally integrated.",
        "established": "AI risk and ethics integrated into enterprise governance documents and processes.",
        "leading": "AI governance fully embedded across policies, committees, and reporting cycles with continuous improvement reviews.",
        "additional_guide": """Review existing frameworks-risk management, data protection, ICT change control-and identify where AI considerations fit naturally. Add AI risk categories (bias, transparency, model integrity) to risk registers. Ensure committees consider AI impacts alongside other technology risks.
Coordinate between Risk, Legal, Data Governance, and ICT to harmonise terminology and reporting. Update policies to reference responsible AI use and ethical standards.
Embedding AI into existing frameworks demonstrates maturity, reduces redundancy, and ensures AI is treated with the same rigour as other critical business activities.""",
        "evidence_types": """To demonstrate compliance, provide evidence that AI-related roles, responsibilities, and decision-making authorities are clearly defined, documented, and communicated across the organisation.

• **Risk Frameworks:** Documents showing AI categories within enterprise risk registers.
• **Committee Minutes:** Evidence that AI issues are discussed and actions tracked.
• **Policy References:** Updates in governance or data policies mentioning AI risk or ethics.
• **Audit Reports:** Assessments of how AI controls align with governance processes.
• **Integration Plans:** Documents linking AI governance to corporate risk strategy.

**In short:** provide tangible proof that AI is managed within the same frameworks that guide other strategic risks."""
    },
    {
        "code": "GF-04",
        "text": "Is there a structured process for approving, monitoring, and reviewing AI projects or pilots?",
        "explanation": "Context: Without a consistent process, AI pilots can bypass ethical or technical checks. This question evaluates whether a formal mechanism exists to assess AI initiatives before implementation and to monitor them once deployed. Example: A digital team uses a standard AI Project Intake Form that captures objectives, data sources, risks, and ethical considerations before committee approval.",
        "domain_order": 2,
        "order": 4,
        "foundational": "No formal review or approval process for AI initiatives.",
        "developing": "Some ad hoc reviews; inconsistent oversight of pilots.",
        "established": "Documented approval process with defined criteria and monitoring steps.",
        "leading": "Fully integrated, transparent AI project lifecycle governance with periodic reviews and ethics checks.",
        "additional_guide": """Create a lightweight intake process for all AI projects capturing purpose, data use, stakeholders, and risk ratings. Require approvals before deployment and schedule post-implementation reviews to assess performance and impact.
As maturity grows, establish an AI Review Board or use existing committees to evaluate submissions. Track projects in a register, noting owners, risks, and outcomes.
Embedding these controls enables accountability, reduces shadow AI initiatives, and provides auditable governance records.""",
        "evidence_types": """To demonstrate compliance, provide evidence that AI governance policies and frameworks are formally approved, consistently applied, and reviewed to ensure alignment with organisational objectives and ethical standards.

• **Process Docs:** AI pilot approval workflow or standard intake form.
• **Registers:** Active AI project register with status and review dates.
• **Meeting Records:** Minutes from committees approving or reviewing AI projects.
• **Policy Clauses:** ICT Procurement or Innovation Policies mentioning AI oversight.
• **Reports:** Post-implementation reviews documenting results and lessons learned.

**Demonstrate that AI initiatives follow an approved path from concept to review with clear accountability.**"""
    },
    {
        "code": "GF-05",
        "text": "How proactively does the organisation monitor emerging AI regulations, standards, and best practices?",
        "explanation": "Context: AI regulations and standards are evolving rapidly. This question assesses how your organisation keeps informed of new legal, ethical, and technical requirements relevant to AI governance. Example: The compliance team subscribes to government AI updates and industry newsletters to brief executives on policy changes each quarter.",
        "domain_order": 2,
        "order": 5,
        "foundational": "No formal process for tracking AI regulatory developments.",
        "developing": "Occasional awareness through informal channels or industry events.",
        "established": "Designated person or team monitors AI standards and updates policies as needed.",
        "leading": "Structured process with regular briefings, trend analysis, and policy alignment reviews.",
        "additional_guide": """Assign a compliance or governance lead to track developments from bodies such as the ACSC, OECD, ISO, and NIST. Schedule quarterly reviews to assess implications and update internal policies. Engage in industry networks and public consultations to stay ahead of emerging requirements.
Building regulatory awareness demonstrates due diligence and positions your organisation to respond to new obligations proactively rather than reactively.""",
        "evidence_types": """To demonstrate compliance, provide evidence that risk management processes for AI are established, documented, and integrated into the organisation's broader governance and assurance frameworks.

• **Briefings & Summaries:** Internal or external AI regulation updates.
• **Memberships:** Participation in industry forums or AI standards groups.
• **Policy Versions:** Documentation showing updates triggered by new standards.
• **Training:** Attendance at AI governance workshops or compliance seminars.
• **Communications:** Newsletters or memos circulating AI policy changes.

**Provide proof of continuous monitoring and integration of emerging AI requirements into corporate governance.**"""
    },
    {
        "code": "GF-06",
        "text": "Are AI governance responsibilities embedded within staff roles and performance expectations?",
        "explanation": "Context: Embedding AI accountability into roles ensures responsibility is sustained beyond individual interest. This question evaluates whether AI-related responsibilities are incorporated into job descriptions or performance plans. Example: A digital manager's KPI includes \"ensure ethical review for all AI pilots\" to promote consistent practice.",
        "domain_order": 2,
        "order": 6,
        "foundational": "No AI governance responsibilities defined in roles or performance plans.",
        "developing": "Informal expectations exist but are not documented or evaluated.",
        "established": "Specific AI responsibilities are embedded in relevant positions and KPIs.",
        "leading": "AI accountability is integrated organisation-wide with periodic role reviews and leadership reporting.",
        "additional_guide": """Integrate AI responsibilities into existing job frameworks to make accountability systemic. Define clear expectations for roles such as ICT managers, data stewards, procurement leads, and ethics officers. Ensure performance plans include objectives related to ethical AI use or risk management. Review these responsibilities annually to reflect changing capabilities and regulations.
This approach creates continuity, clarity, and shared ownership of responsible AI outcomes.""",
        "evidence_types": """To demonstrate compliance, provide evidence that AI governance responsibilities are formally embedded into staff roles, position descriptions, and performance management processes to ensure sustained accountability across the organisation.

• **Job Descriptions:** Documents listing AI ethics or governance responsibilities.
• **Performance Plans:** KPIs linked to AI oversight or risk management.
• **Org Charts:** Roles or teams identified as AI accountability owners.
• **Training Records:** Completion of AI ethics or governance modules by staff.
• **Review Docs:** Performance evaluation templates showing AI criteria.

**Show evidence that AI accountability is not optional but a recognised, measurable part of key roles.**"""
    },
    # Domain 3: Data Readiness (6 questions)
    {
        "code": "DR-01",
        "text": "How effectively does the organisation manage the quality, accuracy, and reliability of data used for decision-making or future AI initiatives?",
        "explanation": "Context: High-quality data is the foundation of any responsible AI capability. Poor data quality—such as duplication, inconsistency, or outdated records—can undermine analytics and lead to biased or incorrect outcomes when AI is introduced. This question assesses whether your organisation has processes to validate, clean, and maintain data used in reporting, automation, or exploratory AI projects. Example: A council introduces quarterly data-quality checks across its customer and asset systems to ensure that datasets feeding future AI tools remain complete, accurate, and up-to-date.",
        "domain_order": 3,
        "order": 1,
        "foundational": "Data quality is unmanaged; errors or inconsistencies are common and addressed only when discovered.",
        "developing": "Some cleansing or validation occurs within individual teams, but there are no shared standards or monitoring.",
        "established": "Documented data-quality procedures exist, supported by defined ownership, validation tools, and routine reporting.",
        "leading": "Data-quality management is enterprise-wide, automated where possible, and continuously improved through governance oversight and performance metrics.",
        "additional_guide": """AI success depends on reliable, trusted data.
• **Define Standards:** Establish clear quality dimensions-accuracy, completeness, timeliness, and consistency-aligned with ISO 8000 or similar guidance.
• **Assign Ownership:** Nominate data stewards or custodians responsible for quality within each domain.
• **Automate Checks:** Use validation rules, dashboards, or ETL tools to detect anomalies early.
• **Monitor and Report:** Include data-quality indicators in governance dashboards and review them quarterly.
• **Drive Continuous Improvement:** Use feedback loops from analytics or pilot projects to refine processes.
Strong data-quality practices reduce operational risk, improve decision confidence, and prepare the organisation for ethical, high-performing AI systems.""",
        "evidence_types": """Show that data-quality management is systematic, documented, and actively monitored.

**Key Evidence Types:**

• **Policies & Standards:** Data-Quality Policy or Governance Framework defining minimum thresholds and responsibilities.
• **Quality Reports:** Logs or dashboards showing accuracy, completeness, or error metrics.
• **Process Documentation:** Data-validation procedures, cleansing scripts, or ETL workflows.
• **Ownership Records:** Named data stewards or custodians in organisational charts.
• **Audit Results:** Internal or external reviews of data-quality performance.
• **Training Records:** Staff education materials on data management and quality assurance.

**In short:** provide artefacts that prove data is treated as a governed, measurable asset fit for trustworthy AI."""
    },
    {
        "code": "DR-02",
        "text": "How clearly are data ownership, stewardship, and access responsibilities defined across the organisation?",
        "explanation": "Context: Clarity around who owns, manages, and can access data ensures accountability and supports readiness for AI. When ownership is undefined, data may become duplicated, misused, or inaccessible to those who need it. This question examines whether roles and responsibilities for data stewardship are formally assigned, ensuring that data handling aligns with governance, privacy, and security standards. Example: A council's Data Governance Policy identifies business owners for each core dataset (rates, assets, HR), supported by nominated data stewards responsible for access control and data integrity.",
        "domain_order": 3,
        "order": 2,
        "foundational": "Data ownership and access rights are informal or undefined; responsibilities vary between teams.",
        "developing": "Some data custodians or system owners are known, but roles are not formally documented or consistently applied.",
        "established": "Data ownership, stewardship, and access responsibilities are defined, documented, and communicated organisation-wide.",
        "leading": "Enterprise data-governance model embedded with clear accountability, cross-functional coordination, and periodic stewardship reviews.",
        "additional_guide": """Accountability is central to responsible data management and AI readiness.
• **Assign Clear Roles:** Identify _data owners_ (decision-makers) and _stewards_ (operational custodians) for each major dataset.
• **Document Responsibilities:** Include ownership and access criteria in policies, system registers, or Terms of Reference.
• **Standardise Access Controls:** Implement role-based permissions and review them regularly.
• **Coordinate Governance Bodies:** Establish a Data Governance Committee to oversee ownership disputes or cross-domain issues.
• **Monitor Compliance:** Conduct periodic reviews to confirm ownership and access controls remain current.
Defining and maintaining stewardship ensures data accountability, traceability, and confidence-key preconditions for trustworthy AI.""",
        "evidence_types": """Demonstrate that data-ownership and access responsibilities are clearly defined, maintained, and enforced.

**Key Evidence Types:**

• **Policies & Frameworks:** Data Governance or Information Management Policy defining ownership, stewardship, and accountability.
• **Data Registers:** Inventories listing datasets, custodians, and access rights.
• **Role Descriptions:** Job profiles or KPIs specifying data-management duties.
• **Access Records:** Role-based permission logs or periodic access-review reports.
• **Committee Minutes:** Evidence of governance oversight or data-stewardship reviews.
• **Training Materials:** Induction or refresher training on data responsibilities.

**In short:** show that every critical dataset has a named owner, defined access criteria, and governance oversight to ensure consistency and accountability."""
    },
    {
        "code": "DR-03",
        "text": "How effectively does the organisation manage data privacy, protection, and ethical use to support trustworthy AI readiness?",
        "explanation": "Context: Strong privacy and data-protection practices are essential foundations for responsible AI. Without clear controls, data may be collected or shared in ways that breach legislation or erode public trust. This question assesses whether privacy, consent, and ethical-use principles are embedded in policies, systems, and staff practices, ensuring data used for AI is handled lawfully and transparently. Example: A not-for-profit conducts a privacy impact assessment before using client data in a predictive-analytics pilot, ensuring compliance with the Privacy Act 1988 (Cth) and organisational ethics guidelines.",
        "domain_order": 3,
        "order": 3,
        "foundational": "Privacy and data-protection practices are informal, reactive, or not consistently applied across systems.",
        "developing": "Basic privacy controls exist (e.g., consent forms, limited access), but coverage and enforcement are inconsistent.",
        "established": "Formal privacy and ethical-use policies are implemented, supported by training, privacy impact assessments, and breach-response procedures.",
        "leading": "Data-protection and ethical-use practices are embedded organisation-wide, proactively monitored, and regularly reviewed against evolving standards and legislation.",
        "additional_guide": """Responsible AI begins with lawful, transparent, and fair data handling.
• **Understand Legal Obligations:** Comply with the Privacy Act 1988 (Cth), Australian Privacy Principles, and sector-specific requirements.
• **Implement Privacy by Design:** Integrate consent, minimisation, and security controls into data-collection and processing systems.
• **Conduct Impact Assessments:** Perform Privacy Impact Assessments (PIAs) or Ethical Impact Reviews for new data-driven initiatives.
• **Educate Staff:** Provide ongoing training on privacy, ethics, and incident reporting.
• **Monitor Compliance:** Use regular audits, data-access logs, and breach registers to ensure ongoing adherence.
Embedding privacy and ethics into data management builds trust and readiness for compliant, responsible AI deployment.""",
        "evidence_types": """Provide proof that privacy and ethical-data-use controls are structured, enforced, and reviewed.

**Key Evidence Types:**

• **Policies & Procedures:** Privacy Policy, Data Ethics Framework, or Acceptable-Use Guidelines referencing AI or analytics.
• **Impact Assessments:** Completed PIAs or Ethical Impact Assessments for projects using personal data.
• **Training Records:** Evidence of staff training in privacy, data handling, and incident management.
• **Access Logs & Audits:** Records showing monitoring of data access and breach-response actions.
• **Communications:** Notices or consent forms explaining data use to clients or citizens.
• **Review Reports:** Internal or external audits evaluating privacy and ethical-data compliance.

**In short:** demonstrate that privacy, security, and ethical-data principles are not optional-they are embedded, measurable, and actively managed across the organisation."""
    },
    {
        "code": "DR-04",
        "text": "How consistently are data classification, storage, and retention practices applied across the organisation?",
        "explanation": "Context: Consistent data management practices protect confidentiality, integrity, and availability — all prerequisites for responsible AI. When classification or retention rules vary across departments, sensitive data may be over-exposed, under-protected, or retained longer than necessary. This question assesses whether the organisation uses structured approaches to classify, store, and securely dispose of data in line with legal, security, and ethical obligations. Example: A council classifies all datasets according to sensitivity (e.g., Public, Internal, Confidential) under its Information Security Policy and applies standardised retention schedules aligned with the Queensland State Archives requirements.",
        "domain_order": 3,
        "order": 4,
        "foundational": "No consistent classification or retention practices; storage and deletion are ad hoc.",
        "developing": "Some teams apply classification or retention rules, but implementation is inconsistent or manual.",
        "established": "Organisation-wide classification, storage, and retention standards exist and are enforced through policies or systems.",
        "leading": "Automated classification and retention processes are embedded, monitored, and periodically reviewed for compliance and efficiency.",
        "additional_guide": """Structured data-management controls ensure compliance and readiness for AI.
• **Establish Classification Standards:** Define categories based on sensitivity, regulatory impact, and business need (e.g., Public, Internal, Restricted).
• **Implement Retention Schedules:** Align with legal or records-management obligations to ensure data is not kept longer than necessary.
• **Secure Storage:** Apply encryption, access controls, and backup standards proportionate to data sensitivity.
• **Automate Where Possible:** Use metadata or data-loss-prevention tools to enforce classification and retention.
• **Audit and Review:** Regularly test compliance and update policies as laws and technologies evolve.
Consistent data-handling practices strengthen governance and reduce risk exposure ahead of AI deployment.""",
        "evidence_types": """Demonstrate that classification, storage, and retention are standardised and enforced across all systems.

**Key Evidence Types:**

• **Policies & Procedures:** Data Classification Policy, Records-Retention Schedule, or Information Security Policy.
• **System Configuration:** Screenshots or settings showing classification labels or automated retention rules.
• **Training Records:** Courses or materials covering classification and secure handling.
• **Audit Reports:** Reviews confirming compliance with retention and disposal standards.
• **Registers:** Logs of data destruction, archival, or re-classification activities.
• **Records Authority:** Approval or alignment with external archival and legal requirements.

**In short:** show that information is classified, stored, and retained according to defined standards-protecting sensitive data and supporting trustworthy AI operations."""
    },
    {
        "code": "DR-05",
        "text": "How well does the organisation ensure data is accessible, interoperable, and usable for current and future AI initiatives?",
        "explanation": "Context: Accessible and well-structured data enables effective analytics and lays the groundwork for future AI capability. When systems are siloed or data is stored in incompatible formats, valuable insights are lost and efficiency declines. This question assesses whether the organisation has mechanisms to ensure data can be shared, integrated, and used responsibly across departments and platforms. Example: A council implements a centralised data platform that consolidates key datasets from HR, finance, and operations, ensuring consistent formats and access controls that support both analytics and AI-readiness activities.",
        "domain_order": 3,
        "order": 5,
        "foundational": "Data is fragmented across systems with limited sharing or standardisation.",
        "developing": "Some data-sharing or integration occurs, but processes are manual and inconsistent.",
        "established": "Data is structured and interoperable through shared platforms, APIs, or standards supporting analytics and AI.",
        "leading": "Enterprise data architecture enables secure, automated sharing and integration, with governance ensuring ongoing accessibility, quality, and compliance.",
        "additional_guide": """Interoperable, well-managed data is the cornerstone of scalable AI systems.
• **Adopt Common Standards:** Use consistent formats, metadata, and taxonomies across systems to simplify sharing.
• **Break Down Silos:** Develop shared data repositories or data lakes with appropriate governance.
• **Enable Secure Access:** Implement role-based permissions and encryption to balance usability with protection.
• **Facilitate Integration:** Deploy APIs, ETL pipelines, or middleware to connect systems and reduce duplication.
• **Monitor and Improve:** Regularly test data accessibility, latency, and integration success.
When data flows securely and consistently across systems, organisations can build trustworthy AI solutions more efficiently and with lower risk.""",
        "evidence_types": """Provide artefacts showing structured, secure, and consistent access to data across the organisation.

**Key Evidence Types:**

• **Architectural Diagrams:** Data flow or integration maps showing system interoperability.
• **Policies & Frameworks:** Data Sharing or Interoperability Framework defining standards and roles.
• **Technical Configurations:** API documentation, integration scripts, or data platform configurations.
• **Data Catalogues:** Inventories of available datasets with metadata and access permissions.
• **Governance Records:** Meeting minutes or reports addressing data-sharing arrangements.
• **Training Materials:** Courses or guides on responsible data use and integration standards.

**In short:** demonstrate that the organisation can securely and efficiently access and combine data to enable analytics and AI initiatives."""
    },
    {
        "code": "DR-06",
        "text": "How consistently does the organisation monitor, review, and improve data governance practices to maintain AI readiness?",
        "explanation": "Context: Strong data governance is not static — it requires ongoing oversight and refinement. Without regular review, even well-designed policies can become outdated or misaligned with new technologies, regulations, or business needs. This question evaluates whether your organisation has mechanisms to assess the effectiveness of its data governance framework, ensuring continuous improvement and sustained readiness for AI. Example: A council's Data Governance Committee meets quarterly to review data incidents, quality metrics, and compliance reports, updating its governance framework and procedures annually to align with changing digital and regulatory landscapes.",
        "domain_order": 3,
        "order": 6,
        "foundational": "Data governance practices are static or informal, with no regular monitoring or review.",
        "developing": "Some ad hoc reviews occur, but improvement actions are inconsistent or undocumented.",
        "established": "Formal data governance reviews are conducted periodically with clear performance measures and improvement plans.",
        "leading": "Continuous improvement is embedded, using metrics, feedback, and audits to evolve governance in line with organisational goals and emerging AI needs.",
        "additional_guide": """Ongoing governance review ensures readiness evolves alongside technology and regulation.
• **Establish Review Cycles:** Conduct scheduled evaluations of data governance frameworks, ideally quarterly or biannually.
• **Measure Performance:** Use KPIs such as data-quality scores, incident rates, and compliance audit results.
• **Engage Stakeholders:** Involve data owners, ICT, legal, and business leaders in review sessions.
• **Act on Findings:** Translate insights into updated policies, improved tools, and enhanced training.
• **Leverage Audits and Benchmarks:** Compare governance maturity against frameworks like DAMA-DMBOK or ISO 38505.
Continuous oversight builds confidence, ensures compliance, and maintains the data integrity required for ethical and effective AI.""",
        "evidence_types": """Provide evidence that data governance is actively monitored, reviewed, and improved.

**Key Evidence Types:**

• **Meeting Minutes:** Records of governance or committee reviews discussing data performance.
• **Performance Dashboards:** Data-quality metrics, audit results, or compliance KPIs.
• **Improvement Plans:** Action logs or roadmaps documenting governance updates and outcomes.
• **Policy Revisions:** Version-controlled frameworks showing periodic updates.
• **Audit Reports:** Internal or third-party assessments with corrective actions.
• **Training Evidence:** Refresher courses or awareness sessions following governance updates.

**In short:** demonstrate that data governance is a living framework-monitored, measured, and continually enhanced to maintain trust and readiness for AI."""
    },
    # Domain 4: Technology & Infrastructure (6 questions)
    {
        "code": "TI-01",
        "text": "How capable and secure is the organisation's current technology environment in supporting data-driven or AI-related initiatives?",
        "explanation": "Context: A secure and capable technology foundation is critical for AI readiness. If systems are outdated, fragmented, or insecure, they can limit innovation and expose the organisation to cyber risk. This question assesses whether the organisation's IT environment—including servers, networks, and applications—is reliable, scalable, and protected enough to host data analytics or AI tools safely and effectively. Example: A council modernises its infrastructure by migrating to a managed cloud platform with multi-factor authentication, encryption, and regular patching to enable future AI workloads securely.",
        "domain_order": 4,
        "order": 1,
        "foundational": "Legacy or unsupported systems with minimal security; infrastructure cannot support data analytics or AI workloads.",
        "developing": "Some systems upgraded or secured, but integration gaps and inconsistent patching remain.",
        "established": "Modern, stable, and secure infrastructure with standardised platforms and defined maintenance schedules.",
        "leading": "Highly resilient, scalable, and secure environment aligned to cloud-first and zero-trust principles, supporting AI experimentation confidently.",
        "additional_guide": """AI readiness depends on a robust, well-managed IT backbone.
• **Assess Current State:** Conduct regular infrastructure and security posture reviews to identify gaps affecting data or AI workloads.
• **Prioritise Modernisation:** Replace or virtualise legacy systems; adopt cloud or hybrid solutions for flexibility.
• **Implement Security by Design:** Enforce strong authentication, encryption, and vulnerability management.
• **Enable Scalability:** Use containerisation or elastic compute to accommodate future AI workloads.
• **Standardise and Document:** Maintain configuration baselines and change-management controls.
Modern, secure infrastructure is the cornerstone of safe, efficient AI adoption, enabling innovation without compromising resilience or compliance.""",
        "evidence_types": """Provide artefacts that demonstrate your infrastructure can securely and reliably support AI-readiness activities.

**Key Evidence Types:**

• **Infrastructure Diagrams:** Network or cloud architecture showing security layers and scalability.
• **Security Policies:** IT Security Policy or Cloud Security Standard outlining encryption, access, and patching.
• **Maintenance Records:** Patch schedules, vulnerability scans, or penetration-test reports.
• **Modernisation Plans:** Cloud-migration or digital-transformation roadmaps.
• **Monitoring Reports:** Availability, uptime, or incident-response metrics.
• **Audit Findings:** Independent reviews confirming infrastructure health and security compliance.

**In short:** show that the environment is modern, secure, and capable of supporting data-driven innovation and future AI workloads."""
    },
    {
        "code": "TI-02",
        "text": "How effectively are technology systems integrated to support data sharing, interoperability, and future AI capabilities?",
        "explanation": "Context: System integration is essential for leveraging data across business units and enabling future AI applications. When systems operate in silos, opportunities for automation, analytics, and cross-functional insight are lost. This question assesses whether your organisation's technology environment supports secure and efficient data exchange between platforms, reducing duplication and improving readiness for AI-enabled processes. Example: A council connects its asset, finance, and customer systems through secure APIs, allowing consistent data exchange and analytics without compromising privacy or control.",
        "domain_order": 4,
        "order": 2,
        "foundational": "Systems are disconnected or incompatible, limiting data exchange and shared reporting.",
        "developing": "Some integration achieved via manual uploads or point-to-point links, but data flow is inconsistent or insecure.",
        "established": "Key systems integrated using APIs or middleware, with governance ensuring data accuracy and security.",
        "leading": "Enterprise integration architecture established, enabling real-time, secure interoperability and automated data flows supporting analytics and AI.",
        "additional_guide": """Integrated systems form the backbone of scalable AI capability.
• **Map Core Systems:** Identify critical data sources and dependencies across departments.
• **Adopt Standard Interfaces:** Use APIs, data pipelines, or middleware to facilitate real-time data exchange.
• **Implement Governance Controls:** Ensure consistent data standards, encryption, and audit logging.
• **Reduce Duplication:** Rationalise legacy databases and harmonise data definitions.
• **Plan for Scalability:** Design integration frameworks that can accommodate new AI or analytics tools.
Secure, well-integrated systems streamline decision-making, improve data reliability, and position the organisation to implement AI safely and efficiently.""",
        "evidence_types": """Provide documentation showing that systems are interconnected, governed, and technically ready for AI applications.

**Key Evidence Types:**

• **Integration Diagrams:** Architecture maps showing API or middleware connectivity between key systems.
• **Policies & Standards:** Data Integration or Interoperability Framework specifying standards and protocols.
• **Technical Documentation:** API specifications, data schemas, or ETL workflow designs.
• **Security Controls:** Access controls and encryption methods applied to system integrations.
• **Performance Reports:** Monitoring logs demonstrating reliability of data exchange.
• **Audit or Review Findings:** Assessments confirming secure and accurate integration practices.

**In short:** demonstrate that technology systems are securely integrated and technically equipped to support cross-functional data use and AI adoption."""
    },
    {
        "code": "TI-03",
        "text": "How effectively does the organisation manage cybersecurity controls to protect systems, data, and AI-related activities?",
        "explanation": "Context: Cybersecurity is foundational to trustworthy AI. Without robust protection, systems and datasets can be compromised, resulting in data loss, manipulation, or reputational damage. This question evaluates whether security measures—such as authentication, network segmentation, vulnerability management, and incident response—are consistently applied to safeguard both existing IT assets and any future AI workloads. Example: A regional council applies the ASD Essential Eight controls, enabling multi-factor authentication, monthly patching, and privileged-access reviews to protect its analytics and AI environments from compromise.",
        "domain_order": 4,
        "order": 3,
        "foundational": "Minimal cybersecurity controls; patching and access management are inconsistent, exposing systems to high risk.",
        "developing": "Basic controls (e.g., antivirus, firewalls) exist but lack coordination or monitoring.",
        "established": "Comprehensive cybersecurity framework in place, aligned with the ISM or Essential Eight, including defined incident-response processes.",
        "leading": "Cybersecurity is proactive and adaptive, leveraging threat intelligence, continuous monitoring, and alignment with recognised frameworks (e.g., ISO 27001, NIST CSF).",
        "additional_guide": """AI relies on secure data and resilient infrastructure.
• **Align to Standards:** Follow the Australian ISM, Essential Eight, or ISO 27001 for baseline control coverage.
• **Strengthen Access Controls:** Enforce least-privilege principles, MFA, and regular access reviews.
• **Maintain Visibility:** Use SIEM tools, vulnerability scans, and endpoint detection for continuous assurance.
• **Secure AI Pipelines:** Protect model code, data, and APIs with encryption and audit logging.
• **Test and Improve:** Conduct penetration testing and incident-response simulations regularly.
Strong cybersecurity governance not only protects current systems but builds the resilience required for responsible AI deployment.""",
        "evidence_types": """Provide evidence that cybersecurity is governed, monitored, and continuously improved.

**Key Evidence Types:**

• **Policies & Frameworks:** Information Security Policy, Cybersecurity Strategy, or ISM/Essential Eight alignment documentation.
• **Monitoring Reports:** SIEM dashboards, intrusion-detection logs, or vulnerability-scan summaries.
• **Access Control Records:** MFA enforcement, privilege reviews, or authentication configurations.
• **Incident Management:** Response plans, breach logs, or after-action reports.
• **Training Records:** Staff awareness or phishing-simulation results.
• **Audit Findings:** Internal or third-party reviews of cyber-maturity.

**In short:** show that security controls are documented, actively monitored, and aligned to national standards-creating a trustworthy foundation for AI innovation."""
    },
    {
        "code": "TI-04",
        "text": "How resilient are the organisation's systems and infrastructure in maintaining continuity during incidents or disruptions affecting AI-related operations?",
        "explanation": "Context: Resilience ensures that critical systems—and future AI capabilities—remain available and recoverable during outages, cyber incidents, or disasters. Without continuity planning, even minor disruptions can halt essential services or corrupt valuable data. This question assesses whether the organisation's IT environment and recovery processes are designed to withstand and quickly recover from disruptions. Example: A council's ICT Continuity Plan includes tested backup and recovery procedures for analytics and AI platforms, ensuring that essential models and datasets can be restored within acceptable timeframes.",
        "domain_order": 4,
        "order": 4,
        "foundational": "No formal business-continuity or disaster-recovery plans; resilience depends on individual system backups.",
        "developing": "Some backup and recovery processes exist but are inconsistent or untested.",
        "established": "Documented continuity and recovery plans are in place, tested periodically, and include AI or data-analytics environments.",
        "leading": "Organisation-wide resilience strategy implemented, integrating redundancy, real-time replication, and continuous testing aligned to risk and AI criticality.",
        "additional_guide": """Resilience planning preserves operational trust during crises.
• **Define Critical Assets:** Identify systems, datasets, and models essential to service delivery or decision-making.
• **Implement Redundancy:** Use high-availability infrastructure, replication, and automated failover where feasible.
• **Back Up Intelligently:** Schedule regular, encrypted backups stored securely off-site or in separate cloud zones.
• **Test and Validate:** Conduct recovery exercises at least annually to verify restoration times and data integrity.
• **Integrate with Risk Frameworks:** Link continuity metrics (e.g., RTO/RPO) with enterprise risk and AI governance programs.
Effective resilience ensures that technology disruptions do not compromise reliability, data integrity, or public confidence in AI systems.""",
        "evidence_types": """Provide evidence that system and data-recovery processes are formalised, tested, and integrated into governance.

**Key Evidence Types:**

• **Plans & Procedures:** ICT Business Continuity or Disaster Recovery Plans covering AI or analytics environments.
• **Test Reports:** Results from recovery or failover exercises, including lessons learned.
• **Backup Logs:** Automated backup schedules and verification records.
• **Architecture Diagrams:** Redundancy or replication configurations demonstrating resilience design.
• **Risk Registers:** Entries describing continuity controls and RTO/RPO targets.
• **Audit Findings:** Internal or external assurance reports on continuity effectiveness.

**In short:** show that recovery capabilities are documented, tested, and resilient enough to maintain trust and functionality in AI-enabled operations."""
    },
    {
        "code": "TI-05",
        "text": "How effectively does the organisation manage technology lifecycle planning to ensure systems remain current, secure, and ready for AI adoption?",
        "explanation": "Context: Lifecycle management ensures technology remains reliable, supported, and capable of handling new workloads such as AI or advanced analytics. Outdated or unsupported systems can introduce security vulnerabilities, integration issues, and data-quality risks. This question assesses whether your organisation has structured processes for technology procurement, maintenance, and replacement to maintain operational efficiency and future readiness. Example: A council maintains a rolling three-year Technology Refresh Plan aligned with its Digital Strategy, retiring legacy systems annually and prioritising investments that enable automation and data-driven decision-making.",
        "domain_order": 4,
        "order": 5,
        "foundational": "No formal technology-lifecycle planning; upgrades occur reactively when systems fail.",
        "developing": "Some systems are reviewed or replaced periodically, but planning is inconsistent or informal.",
        "established": "Documented lifecycle and procurement plans exist, linking system refresh, maintenance, and support schedules to business needs.",
        "leading": "Enterprise lifecycle management embedded, integrating asset planning, vendor governance, and technology-roadmap alignment with AI and innovation strategies.",
        "additional_guide": """Lifecycle planning ensures sustainability and security.
• **Create a Technology Roadmap:** Map major systems with planned refresh or end-of-support dates.
• **Align with Strategy:** Prioritise investments that support automation, data integration, or AI readiness.
• **Standardise Procurement:** Evaluate vendors based on longevity, interoperability, and compliance with data-protection requirements.
• **Implement Monitoring:** Use asset-management tools to track versioning, patching, and renewal milestones.
• **Review Annually:** Adjust refresh cycles to reflect budget, emerging threats, and evolving AI requirements.
Proactive lifecycle management reduces technical debt, ensures consistent performance, and builds the resilience needed for secure, future-ready AI adoption.""",
        "evidence_types": """Provide artefacts showing structured lifecycle and technology-planning practices.

**Key Evidence Types:**

• **Technology Roadmaps:** Documented lifecycle or refresh schedules showing end-of-support tracking.
• **Procurement Policies:** Procedures incorporating lifecycle, interoperability, and security criteria.
• **Asset Registers:** Inventories with system versions, patch levels, and renewal dates.
• **Budget or Planning Papers:** Approved funding for scheduled replacements or upgrades.
• **Review Reports:** Annual or quarterly lifecycle assessments and improvement recommendations.
• **Audit Findings:** Independent reviews confirming lifecycle compliance and risk reduction.

**In short:** demonstrate that your organisation anticipates change, maintains modern technology, and invests strategically to remain AI-ready and secure."""
    },
    {
        "code": "TI-06",
        "text": "How well does the organisation support innovation, experimentation, and safe testing of AI or emerging technologies within its IT environment?",
        "explanation": "Context: Innovation-readiness allows an organisation to explore emerging technologies safely and responsibly. Without secure environments for experimentation, staff may use unsanctioned tools or external platforms, creating governance and data risks. This question assesses whether the organisation has processes, infrastructure, and guardrails that enable innovation while maintaining compliance, security, and oversight. Example: A council establishes a controlled \"AI sandbox\" within its secure cloud environment, allowing staff to prototype AI applications using de-identified data under supervision from ICT and data-governance teams.",
        "domain_order": 4,
        "order": 6,
        "foundational": "No structured approach to innovation or AI testing; experimentation occurs informally or without oversight.",
        "developing": "Limited experimentation occurs within isolated teams; governance or security controls are minimal.",
        "established": "Controlled environments and approval processes support safe AI or technology trials with defined risk and compliance checks.",
        "leading": "Innovation is embedded in strategy; sandbox environments, governance frameworks, and ethical-review processes enable safe, scalable AI experimentation.",
        "additional_guide": """Encouraging innovation while maintaining control is key to AI readiness.
• **Establish Safe Environments:** Create isolated sandboxes or test environments separate from production systems.
• **Define Governance Pathways:** Require approvals and risk assessments for all AI or automation pilots.
• **Use Synthetic or De-Identified Data:** Protect privacy while enabling experimentation.
• **Foster Collaboration:** Encourage cross-functional project teams involving ICT, Risk, Legal, and Business stakeholders.
• **Monitor and Learn:** Capture lessons from pilots to refine governance and technical standards.
Responsible innovation allows organisations to explore AI opportunities confidently-balancing creativity with compliance, ethics, and trust.""",
        "evidence_types": """Provide documentation showing that AI innovation and experimentation are structured, governed, and risk-aware.

**Key Evidence Types:**

• **Innovation Policies:** Frameworks defining approval, risk, and ethical-review requirements for pilots.
• **Sandbox Documentation:** Architecture or configurations of test environments separated from production.
• **Pilot Registers:** Logs of AI or automation trials, including approvals and review outcomes.
• **Governance Minutes:** Evidence of oversight by risk, ethics, or innovation committees.
• **Data-Protection Controls:** Use of de-identified, synthetic, or anonymised data in testing.
• **Post-Trial Reports:** Evaluations or lessons-learned summaries following AI experiments.

**In short:** demonstrate that innovation is deliberate, supported, and securely managed-enabling exploration of AI while maintaining compliance and public trust."""
    },
    # Domain 5: People & Culture (6 questions)
    {
        "code": "PC-01",
        "text": "How aware are staff of AI concepts, potential benefits, and associated ethical or operational risks?",
        "explanation": "Context: AI awareness across the workforce builds a foundation for responsible adoption. When staff lack understanding, AI initiatives can face resistance, misuse, or ethical oversights. This question assesses whether employees have been introduced to what AI is, how it may affect their work, and the importance of responsible, transparent use. Example: A council runs introductory AI awareness sessions for all employees, explaining practical examples such as chatbots or automation, and discussing topics like bias, data privacy, and accountability.",
        "domain_order": 5,
        "order": 1,
        "foundational": "Staff have little or no awareness of AI; no training or internal communication has occurred.",
        "developing": "Basic awareness exists through informal discussions or isolated presentations; understanding is inconsistent.",
        "established": "Organisation provides structured AI-awareness training or communication campaigns to build understanding of AI's value and risks.",
        "leading": "AI literacy is embedded in culture through continuous learning, practical examples, and leadership reinforcement across all business areas.",
        "additional_guide": """Awareness ensures that AI adoption is informed and ethical.
• **Start with Plain Language:** Explain what AI means in the context of your organisation-focus on relevance, not jargon.
• **Promote Responsible Use:** Highlight topics such as data privacy, fairness, and accountability.
• **Use Real Examples:** Demonstrate how AI supports efficiency or service improvement.
• **Encourage Dialogue:** Allow staff to raise concerns or ideas through workshops or forums.
• **Measure Understanding:** Use surveys or feedback to gauge awareness and adjust training.
A well-informed workforce supports innovation while safeguarding ethical and operational standards, helping to normalise responsible AI adoption.""",
        "evidence_types": """Provide artefacts that show AI awareness is being built systematically.

**Key Evidence Types:**

• **Training Records:** Attendance logs for AI awareness or digital literacy sessions.
• **Communication Materials:** Intranet posts, newsletters, or videos introducing AI concepts.
• **Surveys or Feedback:** Results from staff AI-awareness or ethics questionnaires.
• **Learning Modules:** Online or in-person courses explaining AI basics and responsible-use principles.
• **Workshop Summaries:** Notes or outcomes from AI information sessions or Q&A forums.
• **Leadership Endorsements:** Executive messages promoting AI education and responsible innovation.

**In short:** demonstrate that AI awareness is not incidental-it is an intentional, measurable part of organisational learning and culture."""
    },
    {
        "code": "PC-02",
        "text": "How effectively does the organisation build staff capability and skills to engage with or manage AI-related initiatives?",
        "explanation": "Context: Developing staff capability is essential for sustainable, responsible AI adoption. Without relevant skills, employees may struggle to interpret data insights, evaluate AI outputs, or manage associated risks. This question examines whether your organisation provides structured upskilling, professional development, or role-specific training that prepares staff to participate confidently in AI-related projects. Example: A local government delivers short courses on data literacy and responsible automation for managers, helping them evaluate vendor proposals and identify ethical or operational issues early.",
        "domain_order": 5,
        "order": 2,
        "foundational": "No formal AI-related training or skill-development activities are offered.",
        "developing": "Some informal or ad-hoc training occurs, often limited to technical teams.",
        "established": "Structured learning programs exist for relevant roles, covering AI fundamentals, data ethics, and governance.",
        "leading": "Continuous capability development is embedded in workforce planning, with tailored learning pathways, certifications, and performance metrics for AI competence.",
        "additional_guide": """Building AI-ready capability ensures staff can make informed, ethical decisions.
• **Assess Current Skills:** Use capability assessments or role mapping to identify knowledge gaps.
• **Tailor Training:** Design courses for both technical and non-technical roles-covering governance, data literacy, and responsible use.
• **Leverage External Expertise:** Partner with training providers, universities, or industry groups for specialist content.
• **Integrate Learning into Roles:** Include AI competency in job descriptions and performance plans.
• **Encourage Continuous Learning:** Offer micro-credentials, webinars, and peer-learning sessions to maintain momentum.
A structured, evolving skills framework strengthens organisational resilience and ensures staff are confident custodians of AI technology.""",
        "evidence_types": """Show evidence that AI skills and competencies are being developed systematically.

**Key Evidence Types:**

• **Training Plans:** Annual or role-specific development programs including AI or data-literacy modules.
• **Attendance Records:** Participation logs for courses, workshops, or conferences.
• **Competency Frameworks:** Documents outlining required AI-related skills per role.
• **Partnership Agreements:** MOUs or contracts with training or academic institutions.
• **Learning Outcomes:** Assessment results, certifications, or completion statistics.
• **Budget Allocations:** Funding approvals for capability-building initiatives.

**In short:** demonstrate that AI skills development is planned, resourced, and linked to career growth and governance maturity."""
    },
    {
        "code": "PC-03",
        "text": "How effectively does the organisation foster a culture of innovation, collaboration, and openness toward responsible AI adoption?",
        "explanation": "Context: A culture that values innovation and ethical curiosity enables safe, forward-looking AI exploration. If staff fear change or lack empowerment to experiment responsibly, adoption efforts can stagnate. This question assesses whether your organisation promotes collaboration, learning, and trust—encouraging staff to explore AI opportunities within structured governance and ethical boundaries. Example: A council launches an internal \"Innovation Lab\" encouraging teams to propose AI-related ideas. Each proposal is reviewed for alignment with ethical principles, ensuring creativity and accountability coexist.",
        "domain_order": 5,
        "order": 3,
        "foundational": "Little encouragement for innovation or collaboration; staff avoid new technologies due to uncertainty or risk aversion.",
        "developing": "Some teams trial new ideas, but innovation is informal and lacks strategic support or governance.",
        "established": "Innovation is encouraged through defined processes, cross-functional collaboration, and ethical review mechanisms.",
        "leading": "A mature culture of responsible innovation exists—supported by leadership, resources, and recognition programs promoting creative, ethical AI use.",
        "additional_guide": """Fostering innovation while maintaining accountability is vital for AI readiness.
• **Set the Tone from the Top:** Leadership should champion safe experimentation and reward creative problem-solving.
• **Create Structures for Collaboration:** Establish innovation hubs, idea challenges, or cross-departmental teams.
• **Empower Within Guardrails:** Allow experimentation in sandboxed or low-risk environments under governance oversight.
• **Recognise and Share Success:** Highlight responsible AI achievements to reinforce positive behaviours.
• **Measure Engagement:** Track participation, idea submissions, and outcomes to gauge cultural maturity.
A healthy innovation culture attracts talent, accelerates transformation, and ensures creativity operates within ethical and compliance boundaries.""",
        "evidence_types": """Provide evidence that innovation and collaboration are actively promoted within a responsible governance framework.

**Key Evidence Types:**

• **Policies & Frameworks:** Innovation or Digital Transformation Policy referencing AI experimentation and governance.
• **Program Records:** Innovation lab documentation, hackathon outcomes, or pilot project registers.
• **Recognition Schemes:** Awards or incentives encouraging ethical technology use.
• **Communications:** Internal campaigns celebrating innovation success stories.
• **Training:** Workshops on creative problem-solving and responsible AI exploration.
• **Committee Minutes:** Governance records showing oversight of innovation initiatives.

**In short:** demonstrate that innovation is actively encouraged, collaborative, and balanced by responsible AI governance."""
    },
    {
        "code": "PC-04",
        "text": "How effectively does the organisation promote ethical awareness and shared responsibility for the outcomes of AI use?",
        "explanation": "Context: Ethical awareness ensures that AI adoption reflects organisational values and public trust obligations. When staff view ethics as someone else's responsibility, risks such as bias, discrimination, or misuse of data can go unnoticed. This question evaluates whether ethical thinking is embedded in day-to-day decision-making, helping employees recognise the broader social and operational impacts of AI. Example: A council runs workshops on responsible data use and fairness in algorithms, enabling employees—from HR to customer service—to understand how their actions influence ethical AI outcomes.",
        "domain_order": 5,
        "order": 4,
        "foundational": "No initiatives promote ethical awareness; staff are unaware of potential social or organisational AI impacts.",
        "developing": "Ethics discussed occasionally or confined to specific teams (e.g., legal, compliance).",
        "established": "Ethical awareness programs and guidance materials are in place, helping staff identify and address AI-related risks.",
        "leading": "Ethics and accountability are integrated across policies, training, and performance expectations—creating a shared culture of responsible AI use.",
        "additional_guide": """Ethical literacy transforms AI governance from a policy requirement into a lived value.
• **Educate Broadly:** Train staff on fairness, transparency, and accountability, not just compliance.
• **Promote Shared Responsibility:** Clarify that ethical AI is a collective duty-not limited to technical teams.
• **Provide Decision Aids:** Supply checklists or ethics-assessment templates to guide day-to-day choices.
• **Use Real Scenarios:** Demonstrate how bias, misinformation, or privacy breaches can occur and be mitigated.
• **Reinforce Through Leadership:** Ensure executives and managers model ethical decision-making in their own projects.
Embedding ethics across all levels ensures AI systems are developed, procured, and operated with integrity and human accountability.""",
        "evidence_types": """Provide evidence that ethics and accountability are actively promoted and understood.

**Key Evidence Types:**

• **Training Records:** Attendance logs for AI ethics, bias, or data-responsibility sessions.
• **Guidance Materials:** Ethics toolkits, decision guides, or checklists used in projects.
• **Communications:** Internal campaigns promoting fairness, transparency, or human oversight.
• **Policy References:** Codes of Conduct, Responsible AI Principles, or HR policies referencing ethics.
• **Feedback Surveys:** Employee surveys measuring ethical awareness or confidence in raising concerns.
• **Governance Oversight:** Committee minutes or reports discussing ethical implications of AI.

**In short:** demonstrate that ethical responsibility is embedded, measurable, and understood across all levels of the organisation."""
    },
    {
        "code": "PC-05",
        "text": "How well does the organisation support change management and workforce adaptation as AI and automation technologies are introduced?",
        "explanation": "Context: AI and automation can transform roles, workflows, and required skills. Without structured change management, staff may feel threatened, disengaged, or unprepared. This question evaluates whether the organisation has mechanisms to manage workforce impacts, communicate changes early, and ensure employees are supported as tasks evolve or new technologies are introduced. Example: A council implementing automated document processing conducts impact assessments, provides staff retraining opportunities, and runs town-hall meetings to discuss how AI will complement—not replace—existing roles.",
        "domain_order": 5,
        "order": 5,
        "foundational": "No formal change-management approach; staff learn of AI initiatives only when implementation begins.",
        "developing": "Some communication or training occurs reactively, but workforce impacts are not systematically managed.",
        "established": "Structured change-management processes exist, including communication plans, staff consultation, and reskilling opportunities.",
        "leading": "Change management is proactive and embedded—anticipating workforce impacts, providing career pathways, and fostering a culture of continuous adaptation to AI.",
        "additional_guide": """Successful AI adoption depends on people understanding and embracing change.
• **Plan Early:** Integrate workforce-impact assessments into AI project planning.
• **Communicate Transparently:** Explain objectives, timelines, and expected changes in roles or workflows.
• **Provide Reskilling Opportunities:** Offer upskilling, redeployment, or mentoring programs for affected staff.
• **Engage Unions or Staff Representatives:** Collaborate on transition planning to maintain trust.
• **Celebrate Adaptation:** Recognise teams that successfully integrate AI into operations.
Structured change management mitigates fear, maintains morale, and ensures technology enhances rather than disrupts organisational capability.""",
        "evidence_types": """Provide artefacts showing that workforce adaptation and change management are embedded into AI planning.

**Key Evidence Types:**

• **Change-Management Plans:** Documents outlining communication, engagement, and training activities for technology projects.
• **Impact Assessments:** Workforce or organisational-change analyses identifying affected roles.
• **Training & Reskilling Programs:** Course materials or enrolment records for transitioning staff.
• **Consultation Records:** Meeting notes or feedback from staff forums or unions.
• **Communications:** Announcements, newsletters, or FAQs addressing workforce changes.
• **Metrics:** Surveys measuring staff confidence or readiness for automation.

**In short:** demonstrate that change is anticipated, communicated, and supported-ensuring employees remain empowered and engaged through AI transformation."""
    },
    {
        "code": "PC-06",
        "text": "How effectively does the organisation promote diversity, inclusion, and accessibility in its AI-related initiatives and workforce practices?",
        "explanation": "Context: Diversity and inclusion strengthen AI governance by ensuring multiple perspectives inform design, decision-making, and ethical evaluation. Homogeneous teams risk reinforcing bias or overlooking accessibility needs. This question assesses whether your organisation considers gender, cultural, and ability diversity in AI planning and ensures accessibility for both employees and end users of AI systems. Example: A council ensures its AI ethics committee includes representatives from diverse departments and communities, and tests its chatbot interface for accessibility compliance with WCAG standards.",
        "domain_order": 5,
        "order": 6,
        "foundational": "No active consideration of diversity or accessibility in AI or digital initiatives.",
        "developing": "Some awareness of diversity or accessibility, but efforts are informal and inconsistently applied.",
        "established": "Diversity and accessibility are addressed through policies, inclusive design practices, and diverse project teams.",
        "leading": "Diversity, inclusion, and accessibility are embedded in strategy, workforce planning, and AI governance—measured and reported organisation-wide.",
        "additional_guide": """Inclusive design enhances fairness, trust, and performance in AI.
• **Integrate Early:** Include diversity and accessibility in AI planning and procurement checklists.
• **Broaden Perspectives:** Involve staff or stakeholders from different genders, cultural backgrounds, and abilities in AI reviews.
• **Apply Accessible Design:** Follow WCAG, ISO 9241, and local accessibility standards for AI interfaces.
• **Promote Workforce Diversity:** Align recruitment, retention, and professional development with inclusion goals.
• **Measure and Report:** Track diversity metrics and accessibility compliance across projects.
Embedding inclusion and accessibility ensures AI technologies are equitable, transparent, and reflective of the communities they serve.""",
        "evidence_types": """Provide evidence that AI initiatives and workforce practices incorporate diversity, inclusion, and accessibility.

**Key Evidence Types:**

• **Policies & Frameworks:** Diversity, Equity, and Inclusion Policy or Accessibility Strategy referencing AI or digital transformation.
• **Recruitment Records:** Evidence of diverse hiring panels or inclusive job descriptions.
• **Project Documentation:** Accessibility testing reports or inclusive design reviews.
• **Committee Memberships:** Representation from diverse backgrounds in AI governance groups.
• **Training Materials:** Programs on inclusive design, bias awareness, or accessibility.
• **Performance Reports:** Metrics tracking diversity and accessibility outcomes in AI projects.

**In short:** demonstrate that diversity and accessibility are deliberate, measurable priorities shaping both your workforce and AI-enabled services."""
    },
    # Domain 6: Policy & Compliance Readiness (6 questions)
    {
        "code": "PR-01",
        "text": "How clearly defined are the organisation's policies and procedures for governing the responsible use of AI and data-driven technologies?",
        "explanation": "Context: Clear, well-structured policies provide the foundation for responsible AI governance. Without them, employees may rely on informal judgement, increasing the risk of bias, privacy breaches, or regulatory non-compliance. This question assesses whether your organisation has formalised policies or frameworks guiding AI and data-driven decision-making, including ethical principles, risk management, and compliance requirements. Example: A council publishes a Responsible AI Policy outlining principles of fairness, accountability, transparency, and human oversight. The policy references supporting documents such as the Privacy Policy, Data Governance Framework, and ICT Security Standard.",
        "domain_order": 6,
        "order": 1,
        "foundational": "No policies or procedures exist specifically addressing AI or data-driven technologies.",
        "developing": "Some related policies exist (e.g., privacy, ICT security) but do not address AI or are inconsistently applied.",
        "established": "A Responsible AI Policy or equivalent framework exists, aligned with organisational values and applicable legislation.",
        "leading": "Integrated, enterprise-wide governance framework covers AI ethics, data governance, and compliance—regularly reviewed and benchmarked against national or international standards.",
        "additional_guide": """Policies set the guardrails for ethical innovation.
• **Start with Principles:** Define organisational commitments to fairness, accountability, transparency, and human oversight.
• **Align with Existing Policies:** Reference data governance, privacy, and ICT security frameworks to ensure consistency.
• **Include Scope and Applicability:** Clarify which systems, projects, and staff roles are covered.
• **Embed Review Cycles:** Commit to periodic updates as laws and technology evolve.
• **Ensure Accessibility:** Publish policies internally (and externally where appropriate) to promote transparency and trust.
A clearly articulated AI Policy demonstrates readiness, accountability, and commitment to ethical technology adoption.""",
        "evidence_types": """Provide evidence that policies governing AI and data-driven technologies are formalised, current, and accessible.

**Key Evidence Types:**

• **Governance Policies:** Approved Responsible AI Policy, AI Ethics Framework, or AI Use Standard.
• **Supporting Documents:** Privacy, Data Governance, ICT Security, or Risk Management Policies referencing AI.
• **Approval Records:** Executive or board endorsement of policy frameworks.
• **Version Control:** Policy review schedules or document registers showing regular updates.
• **Communications:** Intranet or public announcements sharing policy content with staff or stakeholders.
• **Training Records:** Staff awareness or onboarding sessions covering AI policy requirements.

**In short:** demonstrate that responsible AI is governed by approved, integrated policies reflecting ethical principles and legal obligations."""
    },
    {
        "code": "PR-02",
        "text": "How effectively does the organisation ensure compliance with relevant AI, data-protection, and privacy legislation or standards?",
        "explanation": "Context: Compliance with privacy and AI-related laws is essential to maintain trust, transparency, and regulatory assurance. Without structured compliance processes, the organisation risks breaching obligations under the Privacy Act 1988 (Cth), Australian Privacy Principles, or sector-specific requirements. This question evaluates whether the organisation proactively identifies, monitors, and addresses legal or regulatory obligations related to data use, automation, or AI systems. Example: A Queensland council maintains a compliance register referencing the Privacy Act 1988 (Cth), Information Privacy Act 2009 (Qld), and Australian Government AI Ethics Principles, with annual reviews by the governance team to ensure ongoing alignment.",
        "domain_order": 6,
        "order": 2,
        "foundational": "No formal compliance processes for privacy, AI, or data governance; obligations managed reactively.",
        "developing": "Basic compliance coverage exists (e.g., privacy notices, consent forms) but lacks monitoring or accountability.",
        "established": "Compliance obligations are documented, monitored, and reviewed; privacy and AI controls integrated into governance processes.",
        "leading": "Comprehensive compliance framework embedded, including continuous monitoring, audits, and alignment with evolving AI, privacy, and data-ethics standards.",
        "additional_guide": """Compliance is not static-it must evolve with new regulation and technology.
• **Map Obligations:** Identify applicable laws and frameworks (Privacy Act, _Information Privacy Act 2009 (Qld)_, _Voluntary AI Safety Standard_).
• **Maintain a Compliance Register:** Document key obligations, controls, and responsible owners.
• **Integrate into Risk Management:** Include legal and regulatory risks in enterprise registers.
• **Conduct Regular Reviews:** Audit compliance annually and update policies when legislation changes.
• **Educate Staff:** Train employees on privacy principles, lawful data use, and ethical AI requirements.
• **Monitor Trends:** Track global and national AI-regulatory developments to anticipate future obligations.
A structured compliance process safeguards the organisation from legal exposure and strengthens stakeholder confidence in AI activities.""",
        "evidence_types": """Provide documentation that demonstrates structured compliance with AI and privacy requirements.

**Key Evidence Types:**

• **Compliance Registers:** Logs mapping legal obligations to policies and controls.
• **Audit Reports:** Internal or external reviews of privacy or data-handling compliance.
• **Privacy Impact Assessments:** Completed PIAs for AI or data-driven projects.
• **Policies & Procedures:** Privacy, Information Security, and AI Governance policies referencing relevant laws.
• **Training Records:** Completion rates for privacy and compliance training modules.
• **Incident Logs:** Records of data breaches, remedial actions, and regulator notifications.
• **Board or Committee Minutes:** Evidence of oversight of compliance performance and legislative updates.

**In short:** show that compliance with AI and privacy laws is proactive, documented, and continuously reviewed-not reactive or assumed."""
    },
    {
        "code": "PR-03",
        "text": "How well does the organisation manage third-party and vendor compliance when procuring or implementing AI-related technologies?",
        "explanation": "Context: Third-party risk management is critical to maintaining accountability when AI components or data services are supplied externally. Vendors may use opaque algorithms, offshore data storage, or inconsistent ethical standards, exposing the organisation to reputational and legal risk. This question assesses whether your organisation evaluates and monitors supplier compliance with security, privacy, and responsible-AI requirements throughout the procurement lifecycle. Example: A council adds a \"Responsible AI Checklist\" to its procurement process, requiring vendors to disclose data sources, model-testing practices, and compliance with privacy and accessibility standards before contract approval.",
        "domain_order": 6,
        "order": 3,
        "foundational": "Vendor and supplier compliance for AI or data services is unmanaged or based on trust alone.",
        "developing": "Some supplier assessments occur (e.g., basic privacy or security checks) but are inconsistent or lack ongoing monitoring.",
        "established": "Procurement and contract-management processes include defined AI, ethics, and data-protection clauses with periodic reviews.",
        "leading": "Comprehensive third-party-risk program ensures continuous assurance of vendor security, privacy, and responsible-AI performance, aligned to ISO 27036 or NIST SP 800-161.",
        "additional_guide": """Third-party relationships must extend governance and accountability beyond organisational boundaries.
• **Embed Due Diligence Early:** Include AI-specific ethical and data-handling questions in RFPs or tenders.
• **Define Contractual Obligations:** Mandate clauses for privacy, transparency, explainability, and data-sovereignty.
• **Assess Regularly:** Conduct security or compliance reviews, certifications (e.g., ISO 27001), or SOC 2 reports.
• **Monitor Performance:** Use scorecards or dashboards tracking vendor adherence to AI-governance requirements.
• **Plan Exit Strategies:** Define procedures for data return, deletion, and knowledge transfer when partnerships end.
Effective third-party oversight ensures that vendor behaviour aligns with your ethical, legal, and technical expectations for trustworthy AI.""",
        "evidence_types": """Provide proof that vendor compliance and AI-related risk are actively governed.

**Key Evidence Types:**

• **Procurement Templates:** RFPs, RFQs, or contract templates including AI-ethics or data-protection clauses.
• **Due-Diligence Reports:** Supplier-risk assessments, background checks, or compliance questionnaires.
• **Contract Registers:** Evidence of executed agreements referencing AI governance or data-handling terms.
• **Audit Records:** Vendor-audit reports or third-party assurance attestations (SOC 2, ISO 27001).
• **Performance Monitoring:** KPIs or dashboards measuring supplier compliance over time.
• **Governance Committee Minutes:** Oversight discussions of vendor or outsourcing risks.

**In short:** demonstrate that third-party AI risk is assessed, contractually controlled, and continually monitored-not left to vendor discretion."""
    },
    {
        "code": "PR-04",
        "text": "How effectively does the organisation align its internal policies and practices with recognised AI governance frameworks or standards?",
        "explanation": "Context: Alignment with established AI frameworks demonstrates maturity, accountability, and commitment to best practice. Without benchmarking against recognised standards, organisations may overlook critical governance or ethical gaps. This question assesses whether your organisation has mapped its policies and practices to national or international AI governance frameworks such as ISO/IEC 42001, NIST AI RMF, or Australia's Voluntary AI Safety Standard. Example: A council compares its Responsible AI Policy to ISO/IEC 42001 requirements, identifying opportunities to strengthen documentation, audit processes, and stakeholder transparency.",
        "domain_order": 6,
        "order": 4,
        "foundational": "No awareness or adoption of AI-specific standards or governance frameworks.",
        "developing": "Some reference to AI or ethics frameworks exists, but alignment is informal or incomplete.",
        "established": "Internal policies and processes are mapped against one or more recognised frameworks (e.g., ISO 42001, NIST AI RMF).",
        "leading": "Organisation actively benchmarks and updates its AI governance model against multiple standards, demonstrating continuous improvement and external assurance.",
        "additional_guide": """Framework alignment strengthens credibility and ensures readiness for future regulation.
• **Identify Relevant Frameworks:** Prioritise standards appropriate to your sector and scale-e.g., ISO 42001 (AI Management Systems), NIST AI RMF, OECD AI Principles, or Australia's AI Ethics Principles.
• **Perform a Gap Analysis:** Compare existing policies and procedures against framework controls.
• **Integrate Results:** Update documentation, training, and assurance processes to close identified gaps.
• **Seek External Validation:** Engage auditors or independent experts to verify alignment maturity.
• **Iterate Regularly:** Reassess alignment annually as standards and regulatory expectations evolve.
Framework alignment embeds consistency, improves defensibility, and reinforces trust in AI governance outcomes.""",
        "evidence_types": """Provide evidence showing deliberate mapping and application of AI governance frameworks.

**Key Evidence Types:**

• **Mapping Documents:** Crosswalks comparing internal policies to ISO 42001, NIST AI RMF, or similar standards.
• **Gap-Assessment Reports:** Findings and action plans addressing areas for improvement.
• **Updated Policies:** Revised Responsible AI or Data Governance Policies reflecting framework alignment.
• **Audit Reports:** Internal or external assessments confirming compliance with selected frameworks.
• **Training Materials:** Sessions or briefings introducing staff to framework principles.
• **Committee Minutes:** Governance or risk committee discussions reviewing framework adoption progress.

**In short:** demonstrate that AI governance is guided by-and continuously compared to-globally recognised standards, ensuring maturity and defensibility."""
    },
    {
        "code": "PR-05",
        "text": "How effectively does the organisation monitor and review compliance with its AI, data, and technology policies?",
        "explanation": "Context: Policies have little value if not actively monitored and enforced. Regular review ensures that controls remain relevant, effective, and aligned with evolving technologies and regulations. This question evaluates whether your organisation has mechanisms to track compliance with AI, data, and ICT-related policies, and to take corrective action where gaps are identified. Example: A council's internal audit team conducts annual reviews of the Data Governance Policy and AI Ethics Framework, tracking non-compliance issues and reporting them to the executive governance committee for remediation.",
        "domain_order": 6,
        "order": 5,
        "foundational": "Policies exist but are not monitored or enforced; compliance depends on individual discretion.",
        "developing": "Some monitoring occurs through informal reviews or audits, but findings are not systematically tracked.",
        "established": "Formal compliance reviews are conducted on a scheduled basis, with outcomes documented and actions assigned.",
        "leading": "Continuous monitoring and assurance processes are embedded, supported by metrics, internal audits, and executive oversight ensuring accountability and improvement.",
        "additional_guide": """Effective policy governance ensures consistent behaviour and continuous improvement.
• **Define Review Cycles:** Schedule annual or biennial reviews for all AI and data-related policies.
• **Assign Ownership:** Nominate policy owners responsible for tracking compliance and reporting results.
• **Use Multiple Assurance Layers:** Combine self-assessments, audits, and system-based controls for validation.
• **Track and Report Findings:** Maintain an issue register with remediation timelines and accountability.
• **Benchmark and Improve:** Evaluate results against frameworks such as ISO 9001, ISO 27001, or ISO 42001.
Regular monitoring builds transparency, maintains compliance, and supports a cycle of governance maturity that evolves alongside AI capabilities.""",
        "evidence_types": """Provide documentation showing that policy compliance is actively monitored, reported, and improved.

**Key Evidence Types:**

• **Audit Reports:** Internal or external audit findings covering AI, data, or ICT policies.
• **Review Schedules:** Calendars or registers documenting planned policy reviews.
• **Compliance Registers:** Logs tracking adherence, non-compliance, and corrective actions.
• **Committee Minutes:** Records of executive or governance meetings discussing policy performance.
• **Performance Dashboards:** Metrics showing compliance rates or policy adoption levels.
• **Remediation Evidence:** Completed action plans addressing policy gaps or audit findings.

**In short:** demonstrate that policy compliance is not assumed-it is verified, measured, and continuously strengthened through structured oversight."""
    },
    {
        "code": "PR-06",
        "text": "How effectively does the organisation communicate and enforce policies related to AI, data governance, and responsible technology use?",
        "explanation": "Context: Policies only achieve their purpose when employees understand and follow them. Without active communication, enforcement, and accountability, even well-written AI or data-governance policies may go unnoticed or inconsistently applied. This question evaluates whether your organisation actively promotes awareness of relevant policies, ensures they are accessible, and applies consistent enforcement when breaches or non-compliance occur. Example: A council launches an internal communications campaign introducing its Responsible AI Policy, hosts short \"policy spotlight\" sessions for teams, and integrates compliance checks into its ICT onboarding and annual refresher training.",
        "domain_order": 6,
        "order": 6,
        "foundational": "Policies exist but are poorly communicated or inaccessible; staff are unaware of their responsibilities.",
        "developing": "Policies are shared internally, but awareness and enforcement are inconsistent.",
        "established": "Policies are communicated organisation-wide, reinforced through induction, training, and regular updates.",
        "leading": "Policy communication and enforcement are proactive, supported by leadership endorsement, accessible repositories, and consistent disciplinary or corrective processes.",
        "additional_guide": """Transparency and accountability make governance real for staff.
• **Centralise Access:** Maintain a single, searchable repository for all AI, data, and ICT policies.
• **Educate Through Training:** Include AI governance, data protection, and ethical use in induction and annual refresher programs.
• **Use Multi-Channel Communication:** Share updates via newsletters, intranet, and leadership briefings.
• **Demonstrate Leadership Support:** Ensure executives visibly endorse responsible-technology policies.
• **Enforce Consistently:** Apply disciplinary or corrective measures when breaches occur, supported by documented procedures.
Consistent communication and enforcement ensure staff know, understand, and uphold responsible AI and data-governance standards.""",
        "evidence_types": """Provide artefacts showing that AI, data, and technology policies are well communicated and consistently enforced.

**Key Evidence Types:**

• **Training Records:** Completion reports for policy-awareness or compliance-training modules.
• **Communication Materials:** Newsletters, intranet posts, or leadership messages promoting policy understanding.
• **Policy Repository:** Screenshots or documentation of centralised policy access points.
• **Enforcement Logs:** Records of policy breaches, investigations, and corrective actions.
• **Surveys or Feedback:** Staff awareness assessments or post-training evaluation results.
• **Committee Oversight:** Minutes from governance or HR meetings addressing policy adherence.

**In short:** demonstrate that policy compliance is reinforced through communication, education, and consistent accountability across all levels of the organisation."""
    },
    # Domain 7: Risk & Ethics Awareness (6 questions)
    {
        "code": "RE-01",
        "text": "How well does the organisation identify, assess, and document potential risks associated with AI and data-driven technologies?",
        "explanation": "Context: AI introduces unique risks that differ from traditional ICT or operational risks — such as bias, data misuse, explainability challenges, and reputational harm. Without structured risk assessment, organisations can overlook ethical and operational impacts that emerge during AI exploration or deployment. This question evaluates whether your organisation systematically identifies, records, and manages AI-related risks within existing or dedicated risk frameworks. Example: A council integrates \"AI and algorithmic risk\" into its corporate risk register, categorising potential impacts such as fairness, transparency, and accountability breaches alongside traditional ICT risks.",
        "domain_order": 7,
        "order": 1,
        "foundational": "AI-related risks are not identified or documented; any consideration occurs informally.",
        "developing": "Some AI or data-related risks are recognised, but documentation and mitigation are inconsistent.",
        "established": "AI risks are documented within the organisation's risk framework, with defined controls and accountable owners.",
        "leading": "Comprehensive AI risk management integrated across all projects, supported by continuous monitoring, ethics review, and alignment with frameworks like ISO 31000 and NIST AI RMF.",
        "additional_guide": """AI risk management ensures emerging technologies are adopted responsibly.
• **Expand Risk Categories:** Include algorithmic bias, model drift, privacy, explainability, and reputational risk in enterprise registers.
• **Standardise Assessment:** Apply existing risk-rating matrices and control hierarchies to AI initiatives.
• **Engage Cross-Functional Teams:** Involve Risk, Legal, ICT, and Ethics representatives when reviewing AI projects.
• **Monitor Continuously:** Regularly reassess AI risks as data, models, and regulations evolve.
• **Document Transparently:** Maintain evidence of decisions, mitigations, and control ownership.
Embedding AI risks into enterprise governance demonstrates accountability and strengthens assurance for leadership and stakeholders.""",
        "evidence_types": """Provide artefacts showing that AI-related risks are formally identified, recorded, and managed.

**Key Evidence Types:**

• **Risk Registers:** Entries referencing AI, data, or automation-related risks.
• **Risk Frameworks:** Enterprise or project-level frameworks incorporating AI risk criteria.
• **Assessment Templates:** Standardised risk-assessment forms or checklists for emerging technologies.
• **Meeting Minutes:** Governance or risk-committee discussions of AI-related risks.
• **Audit or Review Reports:** Evaluations of AI risk controls or management practices.
• **Training Materials:** Staff guidance or workshops on identifying AI-specific risks.

**In short:** demonstrate that AI risk is visible, documented, and managed through the same disciplined processes applied to all critical business risks."""
    },
    {
        "code": "RE-02",
        "text": "How effectively does the organisation identify and mitigate potential bias or discrimination in data, algorithms, or AI-driven decisions?",
        "explanation": "Context: Bias in AI systems can lead to unfair or discriminatory outcomes, damaging community trust and breaching ethical or legal standards. Bias may originate from data imbalances, model design, or deployment context. This question assesses whether your organisation understands these risks and has implemented strategies to detect, evaluate, and mitigate bias before and after AI implementation. Example: A council performing data analysis for a customer-prioritisation system checks for demographic representation and engages an ethics advisor to review potential bias impacts on service delivery.",
        "domain_order": 7,
        "order": 2,
        "foundational": "No awareness or controls exist for detecting bias or discrimination in data or algorithms.",
        "developing": "Some discussions or ad hoc reviews occur, but bias detection and mitigation lack structure or documentation.",
        "established": "Bias and fairness checks are embedded into project workflows, supported by governance oversight and diverse review teams.",
        "leading": "Comprehensive bias management program in place, using fairness metrics, diverse datasets, stakeholder consultation, and regular model audits.",
        "additional_guide": """Bias mitigation is fundamental to ethical AI.
• **Assess Data Sources:** Examine datasets for demographic representation and potential exclusion.
• **Implement Fairness Metrics:** Apply measures such as demographic parity, equal opportunity, or error-rate balance.
• **Diversify Review Teams:** Involve staff or community representatives from different backgrounds in evaluations.
• **Document Decisions:** Record identified risks, testing results, and mitigation actions for transparency.
• **Monitor Continuously:** Reassess fairness as data and models evolve or new use cases emerge.
Embedding structured bias management builds fairness, trust, and accountability into AI initiatives.""",
        "evidence_types": """Provide documentation proving that AI bias risks are identified, managed, and monitored.

**Key Evidence Types:**

• **Data Audits:** Reports analysing demographic balance or representation in datasets.
• **Testing Records:** Bias-testing outputs, fairness metrics, or validation scripts.
• **Governance Oversight:** Ethics or review committee minutes discussing bias risks.
• **Policies & Guidelines:** Fairness and Inclusion Policy or AI Bias Mitigation Standard.
• **Training Records:** Staff participation in workshops on bias awareness and mitigation.
• **Remediation Actions:** Logs of bias issues identified and corrective measures applied.

**In short:** demonstrate that the organisation understands, measures, and mitigates bias to ensure equitable and ethical AI outcomes."""
    },
    {
        "code": "RE-03",
        "text": "How effectively does the organisation ensure transparency and explainability in AI or data-driven decision-making?",
        "explanation": "Context: Transparency and explainability build trust by helping stakeholders understand how and why AI or analytics systems reach decisions. Without this, the organisation risks eroding confidence, inviting scrutiny, or breaching regulatory obligations. This question assesses whether your organisation can clearly describe data sources, model logic, and human oversight for any AI-assisted processes. Example: A council using an AI model to prioritise maintenance requests documents how the model weighs factors such as location, urgency, and safety, and includes a clear explanation in public reports.",
        "domain_order": 7,
        "order": 3,
        "foundational": "Decisions supported by data or algorithms are opaque; no documentation or explanation is available.",
        "developing": "Some transparency exists (e.g., project notes or summaries), but explanations are technical or incomplete.",
        "established": "Processes, data sources, and model logic are documented and communicated to relevant stakeholders.",
        "leading": "Explainability is embedded—human-readable explanations, stakeholder engagement, and audit trails demonstrate clarity and accountability across all AI systems.",
        "additional_guide": """Transparency is critical to ethical and defensible AI.
• **Document Thoroughly:** Record datasets, assumptions, and decision rules for all AI projects.
• **Design for Explainability:** Choose interpretable models or provide model-agnostic tools (e.g., LIME, SHAP) to explain outcomes.
• **Communicate Clearly:** Translate technical outputs into accessible language for non-technical stakeholders.
• **Engage Stakeholders:** Provide opportunities for users or affected groups to question or challenge AI-assisted decisions.
• **Audit Regularly:** Review documentation and explanations to ensure ongoing clarity as systems evolve.
Embedding explainability reinforces trust, supports accountability, and ensures compliance with transparency expectations in emerging AI standards.""",
        "evidence_types": """Provide artefacts showing that AI or analytics processes are transparent and explainable.

**Key Evidence Types:**

• **Project Documentation:** Model design documents, decision logs, and feature-importance reports.
• **Public Statements:** Published explainability summaries or FAQs for AI systems affecting the community.
• **Governance Records:** Committee or ethics-review minutes addressing transparency requirements.
• **Technical Tools:** Outputs from explainability frameworks such as LIME, SHAP, or model cards.
• **Training Materials:** Staff sessions on communicating AI decisions responsibly.
• **Audit Reports:** Reviews verifying that AI decisions are traceable and understandable.

**In short:** demonstrate that AI decision-making is visible, explainable, and documented-ensuring stakeholders can understand and trust organisational use of AI."""
    },
    {
        "code": "RE-04",
        "text": "How effectively does the organisation ensure accountability and human oversight of AI-assisted decisions?",
        "explanation": "Context: Clear accountability and human oversight ensure that AI remains a tool supporting—not replacing—responsible decision-making. Without defined roles for human review, errors or ethical issues may go unnoticed, leading to reputational or legal consequences. This question evaluates whether the organisation maintains clear lines of responsibility for AI decisions, ensuring humans retain authority over outcomes. Example: A council implementing an AI tool for traffic optimisation requires human review and sign-off before any automated recommendations are applied to public-safety operations.",
        "domain_order": 7,
        "order": 4,
        "foundational": "No defined oversight or accountability; AI-assisted decisions occur without human review or documentation.",
        "developing": "Some human oversight exists informally, but responsibilities and escalation pathways are unclear.",
        "established": "Human oversight is formalised through defined approval processes, accountability roles, and review mechanisms.",
        "leading": "Organisation-wide accountability model ensures humans retain final authority, supported by audit trails, training, and ethical-review checkpoints.",
        "additional_guide": """AI governance relies on clear human authority.
• **Define Decision Boundaries:** Specify which AI outputs require human review before implementation.
• **Assign Responsibility:** Identify accountable officers for each AI system, ideally within governance or operational teams.
• **Document Oversight Procedures:** Record who approves, audits, and escalates AI-related decisions.
• **Train Reviewers:** Equip staff with knowledge to interpret AI outputs and challenge anomalies confidently.
• **Ensure Traceability:** Maintain logs linking each AI decision to its human reviewer and rationale.
Embedding human oversight ensures accountability, prevents automation bias, and maintains public confidence in AI-supported operations.""",
        "evidence_types": """Provide evidence that accountability and human oversight are clearly established for AI use.

**Key Evidence Types:**

• **Governance Policies:** Documents defining roles and approval authorities for AI-assisted decisions.
• **Process Maps:** Diagrams or workflows showing human checkpoints before AI outcomes are applied.
• **Decision Logs:** Records of human review and approval for AI-generated recommendations.
• **Training Records:** Evidence of staff education on AI oversight responsibilities.
• **Audit Trails:** System logs showing manual intervention or sign-off in AI processes.
• **Ethics or Risk Committee Minutes:** Discussions verifying oversight effectiveness and accountability gaps.

**In short:** demonstrate that human oversight is active, documented, and central to how your organisation uses AI-ensuring responsibility never shifts to the system itself."""
    },
    {
        "code": "RE-05",
        "text": "How effectively does the organisation engage stakeholders to understand, assess, and address ethical or societal impacts of AI use?",
        "explanation": "Context: Meaningful stakeholder engagement ensures that AI initiatives align with community expectations, social values, and ethical obligations. Without consultation, organisations risk deploying systems that unintentionally harm trust, equity, or accessibility. This question assesses whether your organisation involves internal and external stakeholders—such as staff, customers, and community groups—in shaping, reviewing, or validating AI use and governance. Example: Before trialling a predictive service-demand model, a council hosts workshops with community representatives and privacy advocates to discuss transparency, fairness, and potential unintended impacts.",
        "domain_order": 7,
        "order": 5,
        "foundational": "Stakeholders are not consulted on AI or data initiatives; ethical or societal impacts are not considered.",
        "developing": "Engagement occurs occasionally but is reactive, informal, or limited to specific projects.",
        "established": "Stakeholder engagement is structured and documented, with feedback used to inform AI governance or project decisions.",
        "leading": "Ongoing, transparent engagement embedded in governance processes; stakeholder input shapes policy, ethics reviews, and public communication on AI use.",
        "additional_guide": """Engagement promotes trust, inclusion, and legitimacy.
• **Identify Key Stakeholders:** Include employees, community representatives, regulators, and advocacy groups.
• **Consult Early and Often:** Engage stakeholders at planning, design, and review stages-not after deployment.
• **Use Accessible Language:** Communicate AI purpose, benefits, and risks clearly.
• **Integrate Feedback Loops:** Record feedback, track responses, and incorporate recommendations into governance.
• **Disclose Outcomes:** Publish consultation summaries or ethics-review findings to maintain transparency.
Structured, ongoing engagement ensures AI is socially aligned and trusted, strengthening ethical accountability.""",
        "evidence_types": """Provide evidence that stakeholder engagement on AI ethics and impacts is planned, inclusive, and transparent.

**Key Evidence Types:**

• **Engagement Plans:** Frameworks outlining consultation methods, frequency, and participants.
• **Workshop Records:** Meeting notes, attendance lists, or summaries from ethics or community discussions.
• **Feedback Reports:** Documents showing stakeholder concerns and organisational responses.
• **Governance Minutes:** Committee discussions referencing stakeholder input in AI decisions.
• **Public Disclosures:** Reports or website updates summarising engagement outcomes.
• **Surveys or Questionnaires:** Feedback instruments used to gauge community trust or expectations.

**In short:** demonstrate that your organisation listens, documents, and responds to stakeholder input to guide the ethical use of AI and data."""
    },
    {
        "code": "RE-06",
        "text": "How effectively does the organisation monitor, review, and learn from ethical incidents or AI-related risk events?",
        "explanation": "Context: Ongoing monitoring and learning from incidents strengthens organisational resilience and ethical maturity. Without a structured process, lessons from data breaches, algorithmic errors, or community complaints may be overlooked and repeated. This question evaluates whether your organisation tracks AI-related incidents, investigates root causes, and applies improvements to governance, training, or technology controls. Example: After a public concern about bias in an automated eligibility tool, a council conducts an ethics review, updates its model-testing procedures, and publishes a summary of corrective actions to maintain transparency and accountability.",
        "domain_order": 7,
        "order": 6,
        "foundational": "AI or ethical incidents are handled reactively, with limited documentation or learning.",
        "developing": "Some incidents are reviewed, but processes are informal and improvements are inconsistently applied.",
        "established": "Formal procedures exist for reporting, investigating, and addressing AI-related ethical or risk incidents.",
        "leading": "Continuous improvement framework embedded—tracking AI incidents, analysing trends, sharing lessons learned, and updating governance accordingly.",
        "additional_guide": """Incident management is a key feedback loop for AI governance.
• **Define What Constitutes an Incident:** Include ethical breaches, bias findings, model failures, or data-privacy events.
• **Create a Reporting Pathway:** Enable confidential staff reporting and escalation through governance or ethics committees.
• **Conduct Root-Cause Analysis:** Identify system, process, or training gaps contributing to incidents.
• **Document and Share Lessons:** Publish de-identified summaries internally to promote learning.
• **Embed Continuous Improvement:** Integrate findings into updated policies, training, and audit programs.
A structured response to ethical incidents transforms mistakes into progress, strengthening trust, accountability, and long-term AI governance capability.""",
        "evidence_types": """Provide documentation showing that AI-related incidents are tracked, reviewed, and used for continuous improvement.

**Key Evidence Types:**

• **Incident Logs:** Registers documenting ethical or AI-risk events, investigations, and resolutions.
• **Policies & Procedures:** Incident-response or ethics-review frameworks referencing AI.
• **Root-Cause Reports:** Analyses detailing contributing factors and remedial actions.
• **Committee Minutes:** Governance or ethics-board discussions reviewing incident trends.
• **Training Updates:** Revisions to content or guidance following lessons learned.
• **Audit Findings:** Verification that corrective actions were implemented and effective.

**In short:** demonstrate that the organisation treats every AI or ethical incident as an opportunity to learn, improve, and strengthen governance maturity."""
    },
    # Domain 8: Continuous Learning & Improvement (6 questions)
    {
        "code": "CL-01",
        "text": "How effectively does the organisation capture and apply lessons learned from AI or data-driven projects to improve future initiatives?",
        "explanation": "Context: Continuous learning ensures that AI capability evolves responsibly and efficiently. When lessons from projects are not collected or shared, mistakes are repeated and good practices remain isolated. This question evaluates whether your organisation systematically reviews completed or pilot AI projects, documents outcomes, and integrates findings into future planning, governance, and training activities. Example: After completing a proof-of-concept chatbot, a council conducts a post-implementation review documenting challenges with data accuracy and user accessibility, then updates its AI Governance Framework and training program accordingly.",
        "domain_order": 8,
        "order": 1,
        "foundational": "Lessons from AI or digital projects are not recorded or shared; improvement occurs informally.",
        "developing": "Some project reviews occur, but findings are not consistently documented or acted upon.",
        "established": "Structured post-project reviews capture lessons, which are tracked and applied to future AI planning and governance.",
        "leading": "Organisation-wide learning culture embeds formal review, knowledge sharing, and continuous improvement loops across all AI initiatives.",
        "additional_guide": """Learning from every initiative accelerates maturity and mitigates risk.
• **Formalise Reviews:** Require post-implementation reviews for all AI or analytics projects, regardless of outcome.
• **Capture Key Insights:** Document technical, ethical, operational, and stakeholder lessons in a shared repository.
• **Assign Ownership:** Nominate governance or risk teams to track and follow up on improvement actions.
• **Share Broadly:** Present findings in cross-department forums to promote collective learning.
• **Close the Loop:** Integrate lessons into updated policies, templates, and training programs.
Embedding structured feedback mechanisms transforms individual projects into continuous organisational learning cycles, driving consistent improvement in AI governance and readiness.""",
        "evidence_types": """Provide evidence that lessons from AI or data projects are captured, shared, and acted upon.

**Key Evidence Types:**

• **Post-Implementation Reviews:** Completed review reports or "lessons learned" templates.
• **Improvement Registers:** Logs tracking actions, responsible owners, and completion status.
• **Meeting Minutes:** Records from governance or project boards discussing review outcomes.
• **Knowledge Repositories:** Shared folders, wikis, or databases storing project insights.
• **Policy Updates:** Revisions to frameworks or templates referencing implemented lessons.
• **Training Materials:** Updated guidance or learning modules incorporating prior findings.

**In short:** demonstrate that AI experiences translate into tangible improvements-creating a continuous feedback loop that strengthens governance maturity over time."""
    },
    {
        "code": "CL-02",
        "text": "How consistently does the organisation review the performance and effectiveness of its AI governance and risk-management processes?",
        "explanation": "Context: AI governance frameworks must evolve alongside technology, regulation, and organisational maturity. Without regular performance reviews, policies and controls can become outdated, ineffective, or misaligned with real-world practice. This question evaluates whether the organisation periodically assesses its AI governance structures, risk frameworks, and ethical oversight mechanisms to ensure they remain current and effective. Example: A council's Digital Governance Committee conducts an annual review of the AI Governance Framework, using findings from internal audits and project feedback to refine decision-making and oversight practices.",
        "domain_order": 8,
        "order": 2,
        "foundational": "AI governance and risk processes are static and rarely reviewed for effectiveness.",
        "developing": "Informal or occasional reviews occur, but findings are not systematically documented or implemented.",
        "established": "Regular reviews assess AI governance performance, with findings used to update policies and controls.",
        "leading": "Continuous assurance and improvement program embedded—integrating audits, KPIs, and stakeholder feedback to maintain effective AI governance.",
        "additional_guide": """Governance must be dynamic, not decorative.
• **Set Review Frequency:** Establish annual or biannual evaluations of AI governance and risk frameworks.
• **Define Metrics:** Use indicators such as policy adoption rates, audit results, or incident trends to measure effectiveness.
• **Engage Cross-Functional Input:** Include ICT, Legal, Risk, Ethics, and operational staff in reviews.
• **Incorporate Audit Results:** Integrate lessons from compliance or assurance activities into governance updates.
• **Report Outcomes Transparently:** Communicate review findings and improvements to leadership and stakeholders.
Structured governance reviews ensure the organisation continually adapts, keeping AI management aligned with both best practice and evolving obligations.""",
        "evidence_types": """Provide documentation showing that AI governance and risk processes are routinely evaluated and improved.

**Key Evidence Types:**

• **Review Reports:** Periodic assessments of AI governance and risk frameworks.
• **Performance Dashboards:** Metrics tracking policy adoption, incident response, or risk closure rates.
• **Audit Findings:** Internal or third-party reviews addressing AI governance effectiveness.
• **Committee Minutes:** Records of governance or risk discussions on framework performance.
• **Improvement Logs:** Registers documenting actions taken based on review outcomes.
• **Updated Policies:** Revised frameworks showing incorporation of review findings.

**In short:** demonstrate that AI governance is actively measured, reviewed, and refined-not left to drift as technology and risk evolve."""
    },
    {
        "code": "CL-03",
        "text": "How effectively does the organisation benchmark its AI maturity and governance practices against industry standards or peer organisations?",
        "explanation": "Context: Benchmarking helps organisations understand their relative maturity, identify improvement opportunities, and validate governance effectiveness. Without external or comparative insight, AI-readiness efforts may stagnate or remain inward-looking. This question assesses whether your organisation periodically measures its AI performance and governance practices against recognised frameworks, external benchmarks, or peer entities to drive continuous improvement. Example: A council uses the AM AI SAFE Maturity Framework and NIST AI RMF to benchmark progress annually, comparing results to similar local governments to identify leading practices and improvement priorities.",
        "domain_order": 8,
        "order": 3,
        "foundational": "No benchmarking of AI maturity or governance practices has been conducted.",
        "developing": "Some informal comparisons or self-assessments occur, but results are not analysed or applied systematically.",
        "established": "Regular benchmarking performed using structured frameworks or peer comparisons, informing improvement planning.",
        "leading": "Continuous benchmarking embedded—using formal tools, external validation, and data-driven insights to refine AI governance and demonstrate transparency.",
        "additional_guide": """Benchmarking provides evidence-based direction for AI governance evolution.
• **Select Relevant Frameworks:** Use established standards (e.g., ISO 42001, NIST AI RMF, Voluntary AI Safety Standard, AM AI SAFE).
• **Conduct Regular Assessments:** Evaluate at least annually to track progress over time.
• **Engage Independent Reviewers:** Consider third-party audits or peer evaluations for objectivity.
• **Analyse Trends:** Identify domains showing consistent improvement or recurring weaknesses.
• **Incorporate Findings:** Translate insights into concrete actions, roadmaps, or capability-building programs.
Benchmarking transforms maturity assessments from static snapshots into catalysts for long-term learning and improvement.""",
        "evidence_types": """Provide documentation that demonstrates active benchmarking and comparison of AI practices.

**Key Evidence Types:**

• **Benchmarking Reports:** Internal or external assessments comparing maturity against frameworks or peers.
• **Maturity Heatmaps:** Results from AI governance or risk self-assessments.
• **Improvement Plans:** Actions derived from benchmarking outcomes.
• **External Audit Certificates:** Evidence of conformance or independent validation.
• **Committee Minutes:** Governance discussions reviewing benchmarking insights.
• **Communications:** Reports or presentations sharing benchmarking outcomes with stakeholders.

**In short:** demonstrate that benchmarking is regular, evidence-based, and actively shapes strategic decisions and governance improvements."""
    },
    {
        "code": "CL-04",
        "text": "How effectively does the organisation incorporate feedback from staff, stakeholders, and end users into AI improvement and governance processes?",
        "explanation": "Context: Ongoing feedback ensures that AI systems and governance remain relevant, ethical, and responsive to those they affect. Without structured mechanisms to collect and act on feedback, issues may persist unnoticed, eroding trust and performance. This question evaluates whether your organisation has established channels for gathering insights from staff, community members, and external partners to refine AI practices and policies. Example: A council collects feedback from both staff and residents about its AI-powered service chatbot, using survey results and sentiment analysis to improve user experience and update ethical design guidelines.",
        "domain_order": 8,
        "order": 4,
        "foundational": "No formal mechanisms exist to gather or act on feedback related to AI systems or governance.",
        "developing": "Some feedback is collected informally, but there is no consistent process for analysis or follow-up.",
        "established": "Feedback processes exist for AI systems and governance, and responses are tracked and implemented.",
        "leading": "Continuous feedback loops embedded—covering staff, community, and stakeholder input—driving iterative AI and governance improvements.",
        "additional_guide": """Effective AI maturity relies on learning from diverse voices.
• **Establish Feedback Channels:** Create surveys, hotlines, or digital forms for internal and external input on AI performance and ethics.
• **Ensure Representation:** Engage both internal users and external stakeholders, including community and advocacy groups.
• **Analyse and Prioritise Feedback:** Review input regularly and assign responsibility for follow-up.
• **Close the Loop:** Communicate outcomes-what was heard, what was changed-to build trust and accountability.
• **Integrate into Governance:** Feed feedback insights into policy reviews, training updates, and improvement registers.
Structured feedback integration ensures that AI governance evolves collaboratively, guided by lived experience and stakeholder expectations.""",
        "evidence_types": """Provide evidence that AI feedback is systematically collected, analysed, and acted upon.

**Key Evidence Types:**

• **Feedback Reports:** Summaries of staff or stakeholder feedback on AI tools or governance.
• **Surveys or Forms:** Examples of questionnaires or online channels for AI-related feedback.
• **Improvement Registers:** Logs showing actions taken in response to received feedback.
• **Meeting Minutes:** Records of governance or ethics committees reviewing feedback trends.
• **Communications:** Updates to stakeholders outlining changes made based on their input.
• **Audit or Review Records:** Assessments confirming the effectiveness of feedback mechanisms.

**In short:** demonstrate that feedback on AI use is continuous, inclusive, and directly drives governance and performance improvements."""
    },
    {
        "code": "CL-05",
        "text": "How effectively does the organisation use audits, assurance reviews, and performance metrics to drive AI governance improvement?",
        "explanation": "Context: Audits and performance measurement provide objective insight into the health of AI governance. Without structured assurance, organisations risk overlooking weaknesses or failing to verify that ethical and operational controls are effective. This question assesses whether your organisation conducts internal or external reviews of AI readiness, using findings and metrics to strengthen governance, risk, and compliance practices. Example: A council commissions an annual internal audit assessing AI governance maturity against ISO/IEC 42001 requirements, tracks non-conformances, and reports on improvements through its Risk and Audit Committee.",
        "domain_order": 8,
        "order": 5,
        "foundational": "No formal audits or performance metrics are applied to AI or governance processes.",
        "developing": "Some ad hoc audits or reviews occur, but results are not systematically followed up or measured.",
        "established": "Regular AI governance audits and performance reporting occur, with corrective actions tracked and implemented.",
        "leading": "Continuous assurance model in place—combining audits, KPIs, dashboards, and third-party validation to guide measurable improvement.",
        "additional_guide": """Structured assurance turns AI governance from reactive to proactive.
• **Integrate with Audit Programs:** Include AI governance and ethics within annual internal audit plans.
• **Define KPIs:** Track metrics such as data-quality scores, bias findings, training completion, or policy compliance rates.
• **Close Audit Loops:** Assign actions, owners, and due dates for audit recommendations.
• **Engage Independent Review:** Use third-party assurance for objectivity and benchmarking.
• **Report Transparently:** Share results with leadership, governance committees, and stakeholders.
Embedding assurance and measurement ensures AI governance is tested, evidence-based, and continually strengthened over time.""",
        "evidence_types": """Provide documentation showing that AI governance is audited and measured for performance improvement.

**Key Evidence Types:**

• **Audit Reports:** Internal or external reviews addressing AI governance or ethical-risk controls.
• **Performance Dashboards:** KPIs or scorecards tracking AI governance outcomes.
• **Improvement Registers:** Logs of actions arising from audits or performance assessments.
• **Committee Minutes:** Risk, Audit, or Governance Committee discussions reviewing AI performance.
• **Assurance Plans:** Schedules including AI-related audits or monitoring activities.
• **Follow-up Reports:** Evidence that audit findings have been remediated or verified.

**In short:** demonstrate that AI governance is validated through structured, data-driven assurance processes that deliver measurable, sustained improvement."""
    },
    {
        "code": "CL-06",
        "text": "How effectively does the organisation foster a learning mindset and culture of continuous improvement in relation to AI and digital innovation?",
        "explanation": "Context: A learning culture ensures that AI readiness is not a one-time goal but an ongoing journey. When teams lack curiosity or fear experimentation, innovation stalls and valuable insights go unrealised. This question evaluates whether the organisation encourages reflection, experimentation, and professional growth to continually improve its approach to AI and responsible technology adoption. Example: A council establishes an internal \"Digital Learning Hub,\" offering workshops on AI ethics, automation, and data storytelling, and rewards teams who share innovations or lessons that strengthen organisational capability.",
        "domain_order": 8,
        "order": 6,
        "foundational": "Continuous learning and improvement are not prioritised; staff receive limited opportunities to build digital or AI knowledge.",
        "developing": "Some ad hoc learning opportunities exist, but they are not structured or linked to AI readiness goals.",
        "established": "Regular training, forums, and knowledge-sharing activities promote ongoing AI learning and organisational improvement.",
        "leading": "A proactive learning culture embedded—continuous reflection, innovation, and experimentation are encouraged, recognised, and integrated into strategic and workforce planning.",
        "additional_guide": """Sustainable AI maturity depends on a growth mindset and shared responsibility for improvement.
• **Empower Learning:** Provide access to training, professional development, and innovation resources related to AI and digital ethics.
• **Encourage Reflection:** Integrate "what worked / what didn't" discussions into project closeouts and team meetings.
• **Reward Curiosity:** Recognise staff who propose creative, responsible technology solutions.
• **Promote Collaboration:** Support communities of practice that connect staff across departments to share experiences.
• **Integrate into Strategy:** Embed continuous learning into workforce, digital, and AI-readiness plans.
Embedding lifelong learning transforms AI governance from a compliance exercise into a culture of curiosity, capability, and adaptive resilience.""",
        "evidence_types": """Provide evidence that the organisation encourages, supports, and sustains a culture of AI learning and improvement.

**Key Evidence Types:**

• **Training Programs:** Records of staff participation in AI, data, or innovation learning activities.
• **Professional Development Plans:** Inclusion of AI or digital-skills goals in employee objectives.
• **Innovation Platforms:** Internal forums, communities of practice, or ideation challenges.
• **Recognition Schemes:** Awards or incentives promoting continuous learning and innovation.
• **Survey Results:** Staff feedback showing engagement in learning and openness to digital transformation.
• **Strategic Documents:** Workforce or digital strategies referencing learning culture and AI capability development.

**In short:** demonstrate that AI readiness is sustained through an organisational culture that values learning, reflection, and continuous improvement."""
    }
]
