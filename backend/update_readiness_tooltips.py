#!/usr/bin/env python3
"""
Script to add additional_guide tooltips to readiness_questions.py
"""

# Mapping of question codes to their additional guidance tooltips
TOOLTIP_DATA = {
    "SA-01": """Embedding AI within corporate strategy aligns innovation with purpose and accountability.
• **Start with Vision and Values:** Articulate how AI supports organisational goals-efficiency, service quality, community engagement-while upholding ethics and transparency.
• **Link to Risk Management:** Address potential harms such as bias, privacy breaches, or reputational impact.
• **Define Roadmaps:** Set short-term exploration goals and long-term capability building milestones.
• **Secure Executive Ownership:** Assign responsibility to a senior leader or steering committee.
• **Review Regularly:** Re-evaluate strategic AI priorities annually as technology and regulation evolve.
A well-defined AI strategy ensures initiatives are intentional, value-driven, and aligned with organisational capacity.""",

    "SA-02": """Effective leadership drives responsible innovation.
• **Educate and Engage:** Provide briefings or workshops for executives on AI's potential, ethical implications, and governance frameworks (e.g., ISO 42001, NIST AI RMF).
• **Define Strategic Roles:** Assign a senior leader as AI sponsor accountable for readiness, ethics, and compliance.
• **Integrate AI into Corporate Messaging:** Include responsible AI in vision statements, board reports, and stakeholder communications.
• **Provide Resources:** Allocate funding for training, pilot projects, or governance activities to demonstrate tangible commitment.
• **Measure and Review:** Evaluate leadership engagement through regular progress reports or maturity assessments.
Visible, informed leadership signals that AI is a strategic priority aligned with organisational values.""",

    "SA-03": """Establishing clear goals for AI readiness builds accountability and alignment.
• **Start with Purpose:** Identify specific problems AI can solve-efficiency, customer experience, or data-driven decision-making.
• **Link to Organisational Outcomes:** Tie AI goals to strategic KPIs or service delivery benchmarks.
• **Define Success Metrics:** Use measurable indicators such as time saved, accuracy improvements, or stakeholder satisfaction.
• **Communicate Broadly:** Ensure staff and stakeholders understand why AI is being explored and what success looks like.
• **Review and Adapt:** Assess AI outcomes annually and refine objectives based on lessons learned.
Clear, measurable goals ensure AI remains purposeful, transparent, and value-driven rather than purely experimental.""",

    "SA-04": """Public trust depends on visible alignment between AI use and organisational values.
• **Define Ethical Commitments:** Translate values such as fairness, inclusivity, and accountability into AI-specific principles.
• **Engage Stakeholders:** Consult with affected groups, employees, and the public early in AI planning.
• **Assess Impacts:** Use simple checklists or ethics impact assessments to evaluate fairness, privacy, and social effects.
• **Document Transparency:** Clearly communicate AI purpose, data use, and safeguards to maintain trust.
• **Review Regularly:** Revisit ethical alignment as technology, expectations, or legislation evolve.
Embedding ethics ensures AI enhances-not erodes-trust, helping organisations demonstrate integrity and accountability in every AI initiative.""",

    "SA-05": """Transparent communication ensures AI adoption is understood, supported, and trusted.
• **Craft a Clear Narrative:** Explain why the organisation is exploring AI, expected benefits, and how it aligns with ethical values.
• **Use Accessible Language:** Avoid technical jargon; focus on how AI improves outcomes for staff or community.
• **Engage Early and Often:** Hold briefings, Q&A sessions, or town halls to address misconceptions and collect feedback.
• **Publish Ethical Commitments:** Make Responsible AI Principles publicly available to demonstrate transparency.
• **Create Two-Way Channels:** Encourage questions or feedback on AI use, showing accountability and openness.
Consistent, open communication builds confidence, fosters collaboration, and strengthens organisational readiness for AI.""",

    "SA-06": """Sustained readiness requires active monitoring and adaptation.
• **Set Review Intervals:** Align AI strategy reviews with annual corporate planning or audit cycles.
• **Monitor Emerging Trends:** Track developments in regulation, technology, and ethics (e.g., AI Safety Standard, ISO 42001).
• **Collect Feedback:** Use staff, partner, and community feedback to assess perception and impact.
• **Evaluate Outcomes:** Compare actual benefits, costs, and risks against planned objectives.
• **Document and Communicate Updates:** Share revisions transparently to maintain confidence and demonstrate responsiveness.
Embedding regular reviews fosters agility, compliance, and trust - essential for organisations adopting AI responsibly in dynamic environments.""",

    "GF-01": """AI governance defines who makes decisions, how risks are managed, and how ethical standards are upheld. To strengthen this:
• **Define Roles and Accountability:** Assign a senior executive (e.g., Chief AI Officer) and define oversight responsibilities across departments.
• **Create Cross-Functional Committees:** Include Legal, Risk, Data, HR, and Communications to ensure diverse perspectives.
• **Embed into Corporate Governance:** Integrate AI governance into risk management and digital transformation programs.
• **Establish Decision Pathways:** Document who approves, audits, and escalates AI-related decisions.
• **Benchmark Regularly:** Review governance effectiveness annually against ISO 42001 or NIST AI RMF.
Effective AI governance builds transparency, aligns innovation with organisational values, and reduces reputational and compliance risks.""",

    "GF-02": """Define "who does what" for AI. Start by mapping responsibilities across departments-data owners, model developers, compliance officers, and senior approvers. Use a RACI matrix (Responsible, Accountable, Consulted, Informed) to formalise accountability. Link responsibilities to performance plans or KPIs to ensure sustainability.
As capability grows, create cross-functional teams that coordinate decisions, share lessons learned, and monitor emerging risks. Regularly review and update these roles to reflect new AI use cases or regulatory expectations.
Structured accountability reduces ambiguity, improves efficiency, and ensures that ethical oversight remains consistent even as staff change or projects scale.""",

    "GF-03": """Review existing frameworks-risk management, data protection, ICT change control-and identify where AI considerations fit naturally. Add AI risk categories (bias, transparency, model integrity) to risk registers. Ensure committees consider AI impacts alongside other technology risks.
Coordinate between Risk, Legal, Data Governance, and ICT to harmonise terminology and reporting. Update policies to reference responsible AI use and ethical standards.
Embedding AI into existing frameworks demonstrates maturity, reduces redundancy, and ensures AI is treated with the same rigour as other critical business activities.""",

    "GF-04": """Create a lightweight intake process for all AI projects capturing purpose, data use, stakeholders, and risk ratings. Require approvals before deployment and schedule post-implementation reviews to assess performance and impact.
As maturity grows, establish an AI Review Board or use existing committees to evaluate submissions. Track projects in a register, noting owners, risks, and outcomes.
Embedding these controls enables accountability, reduces shadow AI initiatives, and provides auditable governance records.""",

    "GF-05": """Assign a compliance or governance lead to track developments from bodies such as the ACSC, OECD, ISO, and NIST. Schedule quarterly reviews to assess implications and update internal policies. Engage in industry networks and public consultations to stay ahead of emerging requirements.
Building regulatory awareness demonstrates due diligence and positions your organisation to respond to new obligations proactively rather than reactively.""",

    "GF-06": """Integrate AI responsibilities into existing job frameworks to make accountability systemic. Define clear expectations for roles such as ICT managers, data stewards, procurement leads, and ethics officers. Ensure performance plans include objectives related to ethical AI use or risk management. Review these responsibilities annually to reflect changing capabilities and regulations.
This approach creates continuity, clarity, and shared ownership of responsible AI outcomes.""",

    "DR-01": """AI success depends on reliable, trusted data.
• **Define Standards:** Establish clear quality dimensions-accuracy, completeness, timeliness, and consistency-aligned with ISO 8000 or similar guidance.
• **Assign Ownership:** Nominate data stewards or custodians responsible for quality within each domain.
• **Automate Checks:** Use validation rules, dashboards, or ETL tools to detect anomalies early.
• **Monitor and Report:** Include data-quality indicators in governance dashboards and review them quarterly.
• **Drive Continuous Improvement:** Use feedback loops from analytics or pilot projects to refine processes.
Strong data-quality practices reduce operational risk, improve decision confidence, and prepare the organisation for ethical, high-performing AI systems.""",

    "DR-02": """Accountability is central to responsible data management and AI readiness.
• **Assign Clear Roles:** Identify _data owners_ (decision-makers) and _stewards_ (operational custodians) for each major dataset.
• **Document Responsibilities:** Include ownership and access criteria in policies, system registers, or Terms of Reference.
• **Standardise Access Controls:** Implement role-based permissions and review them regularly.
• **Coordinate Governance Bodies:** Establish a Data Governance Committee to oversee ownership disputes or cross-domain issues.
• **Monitor Compliance:** Conduct periodic reviews to confirm ownership and access controls remain current.
Defining and maintaining stewardship ensures data accountability, traceability, and confidence-key preconditions for trustworthy AI.""",

    "DR-03": """Responsible AI begins with lawful, transparent, and fair data handling.
• **Understand Legal Obligations:** Comply with the Privacy Act 1988 (Cth), Australian Privacy Principles, and sector-specific requirements.
• **Implement Privacy by Design:** Integrate consent, minimisation, and security controls into data-collection and processing systems.
• **Conduct Impact Assessments:** Perform Privacy Impact Assessments (PIAs) or Ethical Impact Reviews for new data-driven initiatives.
• **Educate Staff:** Provide ongoing training on privacy, ethics, and incident reporting.
• **Monitor Compliance:** Use regular audits, data-access logs, and breach registers to ensure ongoing adherence.
Embedding privacy and ethics into data management builds trust and readiness for compliant, responsible AI deployment.""",

    "DR-04": """Structured data-management controls ensure compliance and readiness for AI.
• **Establish Classification Standards:** Define categories based on sensitivity, regulatory impact, and business need (e.g., Public, Internal, Restricted).
• **Implement Retention Schedules:** Align with legal or records-management obligations to ensure data is not kept longer than necessary.
• **Secure Storage:** Apply encryption, access controls, and backup standards proportionate to data sensitivity.
• **Automate Where Possible:** Use metadata or data-loss-prevention tools to enforce classification and retention.
• **Audit and Review:** Regularly test compliance and update policies as laws and technologies evolve.
Consistent data-handling practices strengthen governance and reduce risk exposure ahead of AI deployment.""",

    "DR-05": """Interoperable, well-managed data is the cornerstone of scalable AI systems.
• **Adopt Common Standards:** Use consistent formats, metadata, and taxonomies across systems to simplify sharing.
• **Break Down Silos:** Develop shared data repositories or data lakes with appropriate governance.
• **Enable Secure Access:** Implement role-based permissions and encryption to balance usability with protection.
• **Facilitate Integration:** Deploy APIs, ETL pipelines, or middleware to connect systems and reduce duplication.
• **Monitor and Improve:** Regularly test data accessibility, latency, and integration success.
When data flows securely and consistently across systems, organisations can build trustworthy AI solutions more efficiently and with lower risk.""",

    "DR-06": """Ongoing governance review ensures readiness evolves alongside technology and regulation.
• **Establish Review Cycles:** Conduct scheduled evaluations of data governance frameworks, ideally quarterly or biannually.
• **Measure Performance:** Use KPIs such as data-quality scores, incident rates, and compliance audit results.
• **Engage Stakeholders:** Involve data owners, ICT, legal, and business leaders in review sessions.
• **Act on Findings:** Translate insights into updated policies, improved tools, and enhanced training.
• **Leverage Audits and Benchmarks:** Compare governance maturity against frameworks like DAMA-DMBOK or ISO 38505.
Continuous oversight builds confidence, ensures compliance, and maintains the data integrity required for ethical and effective AI.""",

    "TI-01": """AI readiness depends on a robust, well-managed IT backbone.
• **Assess Current State:** Conduct regular infrastructure and security posture reviews to identify gaps affecting data or AI workloads.
• **Prioritise Modernisation:** Replace or virtualise legacy systems; adopt cloud or hybrid solutions for flexibility.
• **Implement Security by Design:** Enforce strong authentication, encryption, and vulnerability management.
• **Enable Scalability:** Use containerisation or elastic compute to accommodate future AI workloads.
• **Standardise and Document:** Maintain configuration baselines and change-management controls.
Modern, secure infrastructure is the cornerstone of safe, efficient AI adoption, enabling innovation without compromising resilience or compliance.""",

    "TI-02": """Integrated systems form the backbone of scalable AI capability.
• **Map Core Systems:** Identify critical data sources and dependencies across departments.
• **Adopt Standard Interfaces:** Use APIs, data pipelines, or middleware to facilitate real-time data exchange.
• **Implement Governance Controls:** Ensure consistent data standards, encryption, and audit logging.
• **Reduce Duplication:** Rationalise legacy databases and harmonise data definitions.
• **Plan for Scalability:** Design integration frameworks that can accommodate new AI or analytics tools.
Secure, well-integrated systems streamline decision-making, improve data reliability, and position the organisation to implement AI safely and efficiently.""",

    "TI-03": """AI relies on secure data and resilient infrastructure.
• **Align to Standards:** Follow the Australian ISM, Essential Eight, or ISO 27001 for baseline control coverage.
• **Strengthen Access Controls:** Enforce least-privilege principles, MFA, and regular access reviews.
• **Maintain Visibility:** Use SIEM tools, vulnerability scans, and endpoint detection for continuous assurance.
• **Secure AI Pipelines:** Protect model code, data, and APIs with encryption and audit logging.
• **Test and Improve:** Conduct penetration testing and incident-response simulations regularly.
Strong cybersecurity governance not only protects current systems but builds the resilience required for responsible AI deployment.""",

    "TI-04": """Resilience planning preserves operational trust during crises.
• **Define Critical Assets:** Identify systems, datasets, and models essential to service delivery or decision-making.
• **Implement Redundancy:** Use high-availability infrastructure, replication, and automated failover where feasible.
• **Back Up Intelligently:** Schedule regular, encrypted backups stored securely off-site or in separate cloud zones.
• **Test and Validate:** Conduct recovery exercises at least annually to verify restoration times and data integrity.
• **Integrate with Risk Frameworks:** Link continuity metrics (e.g., RTO/RPO) with enterprise risk and AI governance programs.
Effective resilience ensures that technology disruptions do not compromise reliability, data integrity, or public confidence in AI systems.""",

    "TI-05": """Lifecycle planning ensures sustainability and security.
• **Create a Technology Roadmap:** Map major systems with planned refresh or end-of-support dates.
• **Align with Strategy:** Prioritise investments that support automation, data integration, or AI readiness.
• **Standardise Procurement:** Evaluate vendors based on longevity, interoperability, and compliance with data-protection requirements.
• **Implement Monitoring:** Use asset-management tools to track versioning, patching, and renewal milestones.
• **Review Annually:** Adjust refresh cycles to reflect budget, emerging threats, and evolving AI requirements.
Proactive lifecycle management reduces technical debt, ensures consistent performance, and builds the resilience needed for secure, future-ready AI adoption.""",

    "TI-06": """Encouraging innovation while maintaining control is key to AI readiness.
• **Establish Safe Environments:** Create isolated sandboxes or test environments separate from production systems.
• **Define Governance Pathways:** Require approvals and risk assessments for all AI or automation pilots.
• **Use Synthetic or De-Identified Data:** Protect privacy while enabling experimentation.
• **Foster Collaboration:** Encourage cross-functional project teams involving ICT, Risk, Legal, and Business stakeholders.
• **Monitor and Learn:** Capture lessons from pilots to refine governance and technical standards.
Responsible innovation allows organisations to explore AI opportunities confidently-balancing creativity with compliance, ethics, and trust.""",

    "PC-01": """Awareness ensures that AI adoption is informed and ethical.
• **Start with Plain Language:** Explain what AI means in the context of your organisation-focus on relevance, not jargon.
• **Promote Responsible Use:** Highlight topics such as data privacy, fairness, and accountability.
• **Use Real Examples:** Demonstrate how AI supports efficiency or service improvement.
• **Encourage Dialogue:** Allow staff to raise concerns or ideas through workshops or forums.
• **Measure Understanding:** Use surveys or feedback to gauge awareness and adjust training.
A well-informed workforce supports innovation while safeguarding ethical and operational standards, helping to normalise responsible AI adoption.""",

    "PC-02": """Building AI-ready capability ensures staff can make informed, ethical decisions.
• **Assess Current Skills:** Use capability assessments or role mapping to identify knowledge gaps.
• **Tailor Training:** Design courses for both technical and non-technical roles-covering governance, data literacy, and responsible use.
• **Leverage External Expertise:** Partner with training providers, universities, or industry groups for specialist content.
• **Integrate Learning into Roles:** Include AI competency in job descriptions and performance plans.
• **Encourage Continuous Learning:** Offer micro-credentials, webinars, and peer-learning sessions to maintain momentum.
A structured, evolving skills framework strengthens organisational resilience and ensures staff are confident custodians of AI technology.""",

    "PC-03": """Fostering innovation while maintaining accountability is vital for AI readiness.
• **Set the Tone from the Top:** Leadership should champion safe experimentation and reward creative problem-solving.
• **Create Structures for Collaboration:** Establish innovation hubs, idea challenges, or cross-departmental teams.
• **Empower Within Guardrails:** Allow experimentation in sandboxed or low-risk environments under governance oversight.
• **Recognise and Share Success:** Highlight responsible AI achievements to reinforce positive behaviours.
• **Measure Engagement:** Track participation, idea submissions, and outcomes to gauge cultural maturity.
A healthy innovation culture attracts talent, accelerates transformation, and ensures creativity operates within ethical and compliance boundaries.""",

    "PC-04": """Ethical literacy transforms AI governance from a policy requirement into a lived value.
• **Educate Broadly:** Train staff on fairness, transparency, and accountability, not just compliance.
• **Promote Shared Responsibility:** Clarify that ethical AI is a collective duty-not limited to technical teams.
• **Provide Decision Aids:** Supply checklists or ethics-assessment templates to guide day-to-day choices.
• **Use Real Scenarios:** Demonstrate how bias, misinformation, or privacy breaches can occur and be mitigated.
• **Reinforce Through Leadership:** Ensure executives and managers model ethical decision-making in their own projects.
Embedding ethics across all levels ensures AI systems are developed, procured, and operated with integrity and human accountability.""",

    "PC-05": """Successful AI adoption depends on people understanding and embracing change.
• **Plan Early:** Integrate workforce-impact assessments into AI project planning.
• **Communicate Transparently:** Explain objectives, timelines, and expected changes in roles or workflows.
• **Provide Reskilling Opportunities:** Offer upskilling, redeployment, or mentoring programs for affected staff.
• **Engage Unions or Staff Representatives:** Collaborate on transition planning to maintain trust.
• **Celebrate Adaptation:** Recognise teams that successfully integrate AI into operations.
Structured change management mitigates fear, maintains morale, and ensures technology enhances rather than disrupts organisational capability.""",

    "PC-06": """Inclusive design enhances fairness, trust, and performance in AI.
• **Integrate Early:** Include diversity and accessibility in AI planning and procurement checklists.
• **Broaden Perspectives:** Involve staff or stakeholders from different genders, cultural backgrounds, and abilities in AI reviews.
• **Apply Accessible Design:** Follow WCAG, ISO 9241, and local accessibility standards for AI interfaces.
• **Promote Workforce Diversity:** Align recruitment, retention, and professional development with inclusion goals.
• **Measure and Report:** Track diversity metrics and accessibility compliance across projects.
Embedding inclusion and accessibility ensures AI technologies are equitable, transparent, and reflective of the communities they serve.""",

    "PR-01": """Policies set the guardrails for ethical innovation.
• **Start with Principles:** Define organisational commitments to fairness, accountability, transparency, and human oversight.
• **Align with Existing Policies:** Reference data governance, privacy, and ICT security frameworks to ensure consistency.
• **Include Scope and Applicability:** Clarify which systems, projects, and staff roles are covered.
• **Embed Review Cycles:** Commit to periodic updates as laws and technology evolve.
• **Ensure Accessibility:** Publish policies internally (and externally where appropriate) to promote transparency and trust.
A clearly articulated AI Policy demonstrates readiness, accountability, and commitment to ethical technology adoption.""",

    "PR-02": """Compliance is not static-it must evolve with new regulation and technology.
• **Map Obligations:** Identify applicable laws and frameworks (Privacy Act, _Information Privacy Act 2009 (Qld)_, _Voluntary AI Safety Standard_).
• **Maintain a Compliance Register:** Document key obligations, controls, and responsible owners.
• **Integrate into Risk Management:** Include legal and regulatory risks in enterprise registers.
• **Conduct Regular Reviews:** Audit compliance annually and update policies when legislation changes.
• **Educate Staff:** Train employees on privacy principles, lawful data use, and ethical AI requirements.
• **Monitor Trends:** Track global and national AI-regulatory developments to anticipate future obligations.
A structured compliance process safeguards the organisation from legal exposure and strengthens stakeholder confidence in AI activities.""",

    "PR-03": """Third-party relationships must extend governance and accountability beyond organisational boundaries.
• **Embed Due Diligence Early:** Include AI-specific ethical and data-handling questions in RFPs or tenders.
• **Define Contractual Obligations:** Mandate clauses for privacy, transparency, explainability, and data-sovereignty.
• **Assess Regularly:** Conduct security or compliance reviews, certifications (e.g., ISO 27001), or SOC 2 reports.
• **Monitor Performance:** Use scorecards or dashboards tracking vendor adherence to AI-governance requirements.
• **Plan Exit Strategies:** Define procedures for data return, deletion, and knowledge transfer when partnerships end.
Effective third-party oversight ensures that vendor behaviour aligns with your ethical, legal, and technical expectations for trustworthy AI.""",

    "PR-04": """Framework alignment strengthens credibility and ensures readiness for future regulation.
• **Identify Relevant Frameworks:** Prioritise standards appropriate to your sector and scale-e.g., ISO 42001 (AI Management Systems), NIST AI RMF, OECD AI Principles, or Australia's AI Ethics Principles.
• **Perform a Gap Analysis:** Compare existing policies and procedures against framework controls.
• **Integrate Results:** Update documentation, training, and assurance processes to close identified gaps.
• **Seek External Validation:** Engage auditors or independent experts to verify alignment maturity.
• **Iterate Regularly:** Reassess alignment annually as standards and regulatory expectations evolve.
Framework alignment embeds consistency, improves defensibility, and reinforces trust in AI governance outcomes.""",

    "PR-05": """Effective policy governance ensures consistent behaviour and continuous improvement.
• **Define Review Cycles:** Schedule annual or biennial reviews for all AI and data-related policies.
• **Assign Ownership:** Nominate policy owners responsible for tracking compliance and reporting results.
• **Use Multiple Assurance Layers:** Combine self-assessments, audits, and system-based controls for validation.
• **Track and Report Findings:** Maintain an issue register with remediation timelines and accountability.
• **Benchmark and Improve:** Evaluate results against frameworks such as ISO 9001, ISO 27001, or ISO 42001.
Regular monitoring builds transparency, maintains compliance, and supports a cycle of governance maturity that evolves alongside AI capabilities.""",

    "PR-06": """Transparency and accountability make governance real for staff.
• **Centralise Access:** Maintain a single, searchable repository for all AI, data, and ICT policies.
• **Educate Through Training:** Include AI governance, data protection, and ethical use in induction and annual refresher programs.
• **Use Multi-Channel Communication:** Share updates via newsletters, intranet, and leadership briefings.
• **Demonstrate Leadership Support:** Ensure executives visibly endorse responsible-technology policies.
• **Enforce Consistently:** Apply disciplinary or corrective measures when breaches occur, supported by documented procedures.
Consistent communication and enforcement ensure staff know, understand, and uphold responsible AI and data-governance standards.""",

    "RE-01": """AI risk management ensures emerging technologies are adopted responsibly.
• **Expand Risk Categories:** Include algorithmic bias, model drift, privacy, explainability, and reputational risk in enterprise registers.
• **Standardise Assessment:** Apply existing risk-rating matrices and control hierarchies to AI initiatives.
• **Engage Cross-Functional Teams:** Involve Risk, Legal, ICT, and Ethics representatives when reviewing AI projects.
• **Monitor Continuously:** Regularly reassess AI risks as data, models, and regulations evolve.
• **Document Transparently:** Maintain evidence of decisions, mitigations, and control ownership.
Embedding AI risks into enterprise governance demonstrates accountability and strengthens assurance for leadership and stakeholders.""",

    "RE-02": """Bias mitigation is fundamental to ethical AI.
• **Assess Data Sources:** Examine datasets for demographic representation and potential exclusion.
• **Implement Fairness Metrics:** Apply measures such as demographic parity, equal opportunity, or error-rate balance.
• **Diversify Review Teams:** Involve staff or community representatives from different backgrounds in evaluations.
• **Document Decisions:** Record identified risks, testing results, and mitigation actions for transparency.
• **Monitor Continuously:** Reassess fairness as data and models evolve or new use cases emerge.
Embedding structured bias management builds fairness, trust, and accountability into AI initiatives.""",

    "RE-03": """Transparency is critical to ethical and defensible AI.
• **Document Thoroughly:** Record datasets, assumptions, and decision rules for all AI projects.
• **Design for Explainability:** Choose interpretable models or provide model-agnostic tools (e.g., LIME, SHAP) to explain outcomes.
• **Communicate Clearly:** Translate technical outputs into accessible language for non-technical stakeholders.
• **Engage Stakeholders:** Provide opportunities for users or affected groups to question or challenge AI-assisted decisions.
• **Audit Regularly:** Review documentation and explanations to ensure ongoing clarity as systems evolve.
Embedding explainability reinforces trust, supports accountability, and ensures compliance with transparency expectations in emerging AI standards.""",

    "RE-04": """AI governance relies on clear human authority.
• **Define Decision Boundaries:** Specify which AI outputs require human review before implementation.
• **Assign Responsibility:** Identify accountable officers for each AI system, ideally within governance or operational teams.
• **Document Oversight Procedures:** Record who approves, audits, and escalates AI-related decisions.
• **Train Reviewers:** Equip staff with knowledge to interpret AI outputs and challenge anomalies confidently.
• **Ensure Traceability:** Maintain logs linking each AI decision to its human reviewer and rationale.
Embedding human oversight ensures accountability, prevents automation bias, and maintains public confidence in AI-supported operations.""",

    "RE-05": """Engagement promotes trust, inclusion, and legitimacy.
• **Identify Key Stakeholders:** Include employees, community representatives, regulators, and advocacy groups.
• **Consult Early and Often:** Engage stakeholders at planning, design, and review stages-not after deployment.
• **Use Accessible Language:** Communicate AI purpose, benefits, and risks clearly.
• **Integrate Feedback Loops:** Record feedback, track responses, and incorporate recommendations into governance.
• **Disclose Outcomes:** Publish consultation summaries or ethics-review findings to maintain transparency.
Structured, ongoing engagement ensures AI is socially aligned and trusted, strengthening ethical accountability.""",

    "RE-06": """Incident management is a key feedback loop for AI governance.
• **Define What Constitutes an Incident:** Include ethical breaches, bias findings, model failures, or data-privacy events.
• **Create a Reporting Pathway:** Enable confidential staff reporting and escalation through governance or ethics committees.
• **Conduct Root-Cause Analysis:** Identify system, process, or training gaps contributing to incidents.
• **Document and Share Lessons:** Publish de-identified summaries internally to promote learning.
• **Embed Continuous Improvement:** Integrate findings into updated policies, training, and audit programs.
A structured response to ethical incidents transforms mistakes into progress, strengthening trust, accountability, and long-term AI governance capability.""",

    "CL-01": """Learning from every initiative accelerates maturity and mitigates risk.
• **Formalise Reviews:** Require post-implementation reviews for all AI or analytics projects, regardless of outcome.
• **Capture Key Insights:** Document technical, ethical, operational, and stakeholder lessons in a shared repository.
• **Assign Ownership:** Nominate governance or risk teams to track and follow up on improvement actions.
• **Share Broadly:** Present findings in cross-department forums to promote collective learning.
• **Close the Loop:** Integrate lessons into updated policies, templates, and training programs.
Embedding structured feedback mechanisms transforms individual projects into continuous organisational learning cycles, driving consistent improvement in AI governance and readiness.""",

    "CL-02": """Governance must be dynamic, not decorative.
• **Set Review Frequency:** Establish annual or biannual evaluations of AI governance and risk frameworks.
• **Define Metrics:** Use indicators such as policy adoption rates, audit results, or incident trends to measure effectiveness.
• **Engage Cross-Functional Input:** Include ICT, Legal, Risk, Ethics, and operational staff in reviews.
• **Incorporate Audit Results:** Integrate lessons from compliance or assurance activities into governance updates.
• **Report Outcomes Transparently:** Communicate review findings and improvements to leadership and stakeholders.
Structured governance reviews ensure the organisation continually adapts, keeping AI management aligned with both best practice and evolving obligations.""",

    "CL-03": """Benchmarking provides evidence-based direction for AI governance evolution.
• **Select Relevant Frameworks:** Use established standards (e.g., ISO 42001, NIST AI RMF, Voluntary AI Safety Standard, AM AI SAFE).
• **Conduct Regular Assessments:** Evaluate at least annually to track progress over time.
• **Engage Independent Reviewers:** Consider third-party audits or peer evaluations for objectivity.
• **Analyse Trends:** Identify domains showing consistent improvement or recurring weaknesses.
• **Incorporate Findings:** Translate insights into concrete actions, roadmaps, or capability-building programs.
Benchmarking transforms maturity assessments from static snapshots into catalysts for long-term learning and improvement.""",

    "CL-04": """Effective AI maturity relies on learning from diverse voices.
• **Establish Feedback Channels:** Create surveys, hotlines, or digital forms for internal and external input on AI performance and ethics.
• **Ensure Representation:** Engage both internal users and external stakeholders, including community and advocacy groups.
• **Analyse and Prioritise Feedback:** Review input regularly and assign responsibility for follow-up.
• **Close the Loop:** Communicate outcomes-what was heard, what was changed-to build trust and accountability.
• **Integrate into Governance:** Feed feedback insights into policy reviews, training updates, and improvement registers.
Structured feedback integration ensures that AI governance evolves collaboratively, guided by lived experience and stakeholder expectations.""",

    "CL-05": """Structured assurance turns AI governance from reactive to proactive.
• **Integrate with Audit Programs:** Include AI governance and ethics within annual internal audit plans.
• **Define KPIs:** Track metrics such as data-quality scores, bias findings, training completion, or policy compliance rates.
• **Close Audit Loops:** Assign actions, owners, and due dates for audit recommendations.
• **Engage Independent Review:** Use third-party assurance for objectivity and benchmarking.
• **Report Transparently:** Share results with leadership, governance committees, and stakeholders.
Embedding assurance and measurement ensures AI governance is tested, evidence-based, and continually strengthened over time.""",

    "CL-06": """Sustainable AI maturity depends on a growth mindset and shared responsibility for improvement.
• **Empower Learning:** Provide access to training, professional development, and innovation resources related to AI and digital ethics.
• **Encourage Reflection:** Integrate "what worked / what didn't" discussions into project closeouts and team meetings.
• **Reward Curiosity:** Recognise staff who propose creative, responsible technology solutions.
• **Promote Collaboration:** Support communities of practice that connect staff across departments to share experiences.
• **Integrate into Strategy:** Embed continuous learning into workforce, digital, and AI-readiness plans.
Embedding lifelong learning transforms AI governance from a compliance exercise into a culture of curiosity, capability, and adaptive resilience.""",
}

print(f"Total tooltip entries: {len(TOOLTIP_DATA)}")
print("Tooltip codes:", sorted(TOOLTIP_DATA.keys()))
