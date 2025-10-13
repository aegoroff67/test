// Help content for assessment questions
// Structured as: { "QUESTION-CODE": "help text content" }

export const helpContent = {
  "FA-1": `To demonstrate compliance with **FA-1** ("Identify and mitigate bias in AI systems"), look for evidence showing both **proactive** and **reactive** bias-mitigation measures across the AI lifecycle.

**Key evidence types:**

- **Policies & Governance:** A Bias Mitigation Policy or Fairness Framework outlining responsibilities, oversight committees, and escalation processes for bias incidents.

- **Data & Model Practices:** Documentation proving datasets are diverse and representative, preprocessing steps to rebalance or anonymize data, and fairness testing or audits of models using tools such as *Fairlearn*, *AI Fairness 360*, *SHAP*, or *LIME*.

- **Training & Awareness:** Records of staff training or workshops on bias awareness and ethical AI practices.

- **Monitoring & Reporting:** Ongoing fairness monitoring, KPIs or metrics (e.g., demographic parity, equal opportunity), and regular internal or external reporting on bias management.

- **Independent Validation:** Results of third-party bias audits or fairness certifications.

**In short:** Compliance requires documented processes, technical evidence of fairness testing, clear accountability, and continuous monitoring. Gaps typically arise when bias detection is treated as a one-off activity rather than an ongoing governance commitment.`,

  "FA-2": `To comply with **FA-2** ("Ensure training data represents all relevant demographics"), look for evidence that training datasets are **diverse, representative, and regularly reviewed** for inclusivity.

**Key evidence types:**

- **Policies & Governance:** A documented *Data Representation Policy* and *Diversity Standards* outlining minimum demographic inclusion requirements, with oversight by a fairness or data governance committee.

- **Data Collection & Validation:** Proof that data is sourced from multiple regions, demographics, or contexts; validation of historical datasets for completeness and bias; and stakeholder or expert review to confirm representativeness.

- **Technical Controls:** Evidence of *data balancing*, *synthetic data generation*, and use of bias-detection tools (e.g., *Fairlearn*, *AI Fairness 360*). Metrics such as demographic parity or representation indices should be used to measure fairness.

- **Documentation & Audits:** Dataset composition reports showing demographic breakdowns, versioning with metadata, and regular internal or third-party audits assessing demographic inclusivity.

- **Training & Awareness:** Records of staff education programs on equitable data practices and awareness campaigns promoting fairness.

**In short:** Compliance requires structured policies, measurable fairness criteria, and continuous monitoring to ensure training data fairly represents all groups the AI system affects.`,

  "FA-3": `To comply with **FA-3** ("Evaluate system outputs for potential disparities across user groups"), look for **systematic evaluation, documentation, and ongoing monitoring** of fairness in AI outcomes.

**Key evidence types:**

- **Policies & Governance:** A formal *Evaluation or Fairness Policy* defining how output disparities are identified, acceptable disparity thresholds, and who is accountable for reviews.

- **Tools & Metrics:** Use of fairness tools (e.g., *Fairlearn*, *AI Fairness 360*, *What-If Tool*) and metrics such as *disparate impact*, *demographic parity*, or *equalized odds* to measure disparities.

- **Testing & Validation:** Evidence of scenario testing, demographic segmentation, edge-case analysis, and documented reports highlighting any detected disparities.

- **Monitoring & Improvement:** Ongoing audits, real-time monitoring dashboards, and feedback loops to retrain or adjust models when disparities are found.

- **Documentation & Oversight:** Records of disparity assessments, corrective actions, and oversight by an AI fairness or ethics board.

- **Independent Review:** Third-party audits or fairness certifications validating results and compliance with standards (e.g., *ISO/IEC 24027*).

**In short:** Compliance means consistently analysing and reporting AI outputs for unequal impacts, acting on findings, and maintaining transparency and accountability in fairness evaluation processes.`,

  "FA-4": `To comply with **FA-4** ("How do you measure fairness in your AI system's outputs?"), organizations must **define, quantify, and continuously monitor fairness** using clear metrics and evidence-based evaluation.

**Key evidence types:**

- **Policies & Governance:** A *Fairness Measurement Policy* that defines fairness objectives, metrics, and acceptable thresholds for the organization's AI systems.

- **Metrics & Evaluation:** Use of recognised fairness metrics---*demographic parity*, *equalized odds*, *predictive parity*, *disparate impact ratio*---and, where needed, context-specific custom metrics aligned with ethical principles.

- **Tools & Technology:** Implementation of fairness evaluation platforms (e.g., *Fairlearn*, *AI Fairness 360*, *What-If Tool*, *Responsible AI Toolbox*) and automated systems to track fairness in real time.

- **Testing & Reporting:** Documented fairness testing reports, dashboards visualizing fairness scores, and periodic reviews covering model updates, anomaly alerts, and corrective actions.

- **Stakeholder & Compliance:** Evidence of fairness review boards, staff training, stakeholder feedback, and alignment with *ISO/IEC 24027* or anti-discrimination regulations.

**In short:** Compliance requires measurable fairness standards, transparency in evaluation, and continuous monitoring to ensure outputs remain equitable, auditable, and aligned with ethical and regulatory expectations.`,

  "FA-5": `To comply with **FA-5** ("Have you tested the system for potential biases in real-world scenarios?"), look for **evidence of live environment testing, stakeholder input, and bias correction processes** beyond lab conditions.

**Key evidence types:**

- **Policies & Governance:** A *Real-World Testing Policy* outlining how and when systems are tested in operational contexts, with defined fairness thresholds and approval processes before deployment.

- **Testing Practices:** Documentation of *scenario-based testing*, *pilot deployments*, and *A/B testing* across diverse demographics, geographies, and edge cases to identify bias under real conditions.

- **Results & Analysis:** Reports detailing real-world bias testing methodologies, disparities observed, and metrics used (e.g., *demographic parity*, *equal opportunity*, *disparate impact ratio*).

- **Tools & Adjustments:** Use of fairness and explainability tools (e.g., *Fairlearn*, *AI Fairness 360*, *SHAP*, *LIME*) and evidence of model updates, retraining logs, or changelogs addressing discovered biases.

- **Feedback & Oversight:** Input from users, experts, and governance committees validating findings, with continuous monitoring and periodic bias reports.

- **Independent Review:** Third-party validation or certifications confirming fairness testing integrity.

**In short:** Compliance requires systematic real-world bias testing, transparent reporting, and continuous refinement to ensure fairness holds beyond controlled development environments.`,

  "FA-6": `To comply with **FA-6** ("Are you using any frameworks or tools to assess and mitigate bias?"), organizations should show **active, structured use of recognized AI fairness frameworks** integrated into their development and governance processes.

**Key evidence types:**

- **Tools & Frameworks:** Proof of using fairness tools such as *Fairlearn*, *IBM AI Fairness 360*, *Google's What-If Tool*, or *Microsoft's Responsible AI Toolbox* to detect, measure, and mitigate bias in datasets and models.

- **Policies & Integration:** A *Bias Mitigation Policy* or *Fairness Framework* mandating these tools as part of the AI lifecycle, with documented inclusion in development workflows or automated pipelines.

- **Reports & Outputs:** Tool-generated outputs showing detected disparities, mitigation actions, and measurable fairness improvements across demographic groups.

- **Training & Governance:** Evidence that staff are trained to use these tools and that fairness evaluations form a required approval step before deployment.

- **Continuous Monitoring:** Ongoing tool usage for real-time fairness tracking, dashboards, and audit logs showing consistent bias evaluation.

- **External Validation:** Third-party audits or certifications confirming compliance with standards such as *ISO/IEC 24027*.

**In short:** Compliance requires demonstrable, ongoing use of trusted bias-assessment tools, embedded governance processes, and documented improvements in fairness over time.`,

  "FA-7": `To comply with **FA-7** ("How do you ensure fairness in decision-making for minority or underserved groups?"), organizations must show **active measures to identify, prevent, and correct bias that could disadvantage vulnerable populations.**

**Key evidence types:**

- **Policies & Governance:** A *Fairness Policy* and *Ethics & Inclusion Guidelines* explicitly protecting minority and underserved groups, backed by oversight from a fairness review board or ethics committee.

- **Data & Model Practices:** Documentation showing diverse and representative datasets, bias audits, and use of techniques such as *oversampling*, *synthetic data generation*, or *threshold adjustments* to improve equity.

- **Metrics & Tools:** Evidence of fairness evaluation using *disparate impact ratio*, *equalized odds*, or *demographic parity*; and tools such as *Fairlearn*, *AI Fairness 360*, *What-If Tool*, or *SHAP/LIME* for explainability.

- **Monitoring & Engagement:** Continuous monitoring for disparities, incident reporting mechanisms, and stakeholder input from affected communities.

- **Training & Compliance:** Staff training on fairness principles, adherence to anti-discrimination laws, and alignment with *ISO/IEC 24027* or ethical AI standards.

**In short:** Compliance means embedding fairness for minority and underserved groups throughout the AI lifecycle --- from dataset design and testing to governance, transparency, and ongoing accountability.`,

  "FA-8": `To comply with **FA-8** ("Is fairness embedded in your AI model's design process, or is it addressed post-deployment?"), organizations must show that **fairness is built in from the start**, not treated as a reactive fix.

**Key evidence types:**

- **Policies & Frameworks:** A *Fairness-by-Design Policy* and *End-to-End Fairness Standards* embedding fairness considerations throughout the AI lifecycle---from data collection to deployment and monitoring.

- **Design Integration:** Documentation of *inclusive design practices*, *fairness checkpoints* during data preparation, model training, and validation, and approval gates requiring fairness reviews before progression.

- **Data & Model Practices:** Evidence of representative datasets, proactive bias detection, and application of bias mitigation techniques (e.g., reweighting, adversarial debiasing).

- **Tools & Oversight:** Use of fairness and explainability tools (*Fairlearn*, *AI Fairness 360*, *Responsible AI Toolbox*, *SHAP*, *LIME*) and oversight committees enforcing fairness compliance.

- **Monitoring & Reporting:** Real-time fairness monitoring, incident management logs, and documented audits or reports showing continuous improvement.

- **Training & Engagement:** Evidence of design team training, ethics workshops, and stakeholder involvement in shaping fairness standards.

**In short:** Compliance requires demonstrating a *fairness-by-design approach*---integrating equity, transparency, and accountability into every phase of AI system development and beyond.`
};
