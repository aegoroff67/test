# FAIRA Complete Variables with Detailed Scoring Options

This document provides the complete list of all variables with their full scoring details.

---

## A1_1

**Question:** What is the primary function of the AI system?

- **Type:** `multiselect`
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** `Impact`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Automate routine tasks | Impact: 1 |
| Support human decision-making | Impact: 2 |
| Make autonomous decisions | Impact: 3 |
| Predict outcomes | Impact: 2 |
| Generate content | Impact: 1 |
| Classify or categorize data | Impact: 1 |
| Detect anomalies or patterns | Impact: 2 |
| Other | Impact: 1 |

---

## A1_2

**Question:** What version is the AI system currently at?

- **Type:** `text`
- **Domains:** Accountability
- **Scoring:** None (descriptive/metadata field)

---

## A1_3

**Question:** Which AI features or capabilities does the system include?

- **Type:** `multiselect`
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** `Impact`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Natural language processing | Impact: 1 |
| Computer vision | Impact: 1 |
| Recommendation engine | Impact: 2 |
| Predictive modeling | Impact: 2 |
| Anomaly detection | Impact: 2 |
| Speech recognition | Impact: 1 |
| Automated content generation | Impact: 1 |
| Optimization algorithms | Impact: 2 |
| Reinforcement learning | Impact: 3 |
| Other | Impact: 1 |

---

## A1_4

**Question:** What types of decisions or problems does the AI system address?

- **Type:** `multiselect`
- **Domains:** Accountability, Fairness
- **Target Metric:** `Impact`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Operational efficiency | Impact: 1 |
| Resource allocation | Impact: 2 |
| Risk assessment | Impact: 3 |
| Customer interactions | Impact: 2 |
| Compliance and regulatory | Impact: 3 |
| Safety monitoring | Impact: 3 |
| Quality control | Impact: 2 |
| Strategic planning | Impact: 2 |
| Personnel management | Impact: 3 |

---

## A1_5

**Question:** What tangible benefits does the AI system provide?

- **Type:** `multiselect`
- **Domains:** Accountability
- **Target Metric:** `Impact`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Cost reduction | Impact: -1 |
| Time savings | Impact: -1 |
| Improved accuracy | Impact: -2 |
| Enhanced user experience | Impact: -1 |
| Scalability | Impact: -1 |
| Better decision-making | Impact: -2 |
| Risk mitigation | Impact: -2 |
| Compliance support | Impact: -2 |

---

## A1_6

**Question:** Does the system convert its outputs directly into actions without human intervention?

- **Type:** `yes_no`
- **Domains:** Accountability, Reliability and Safety
- **Target Metric:** `Likelihood`
- **Special Computation:** `AutonomyFactor`

**Scoring Options:**

- **No:**
  - base: 1.0
- **Yes:**
  - Has sub-question (see schema for details)

**Notes:** AutonomyFactor = base × max(action_multipliers). This modifies Total Likelihood in final calculation.

---

## A1_7

**Question:** What type(s) of AI model or algorithm does the system use?

- **Type:** `multiselect`
- **Domains:** Transparency and Explainability, Accountability
- **Target Metric:** `Impact`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Rule-based system | Impact: 1 |
| Linear/logistic regression | Impact: 1 |
| Decision trees | Impact: 1 |
| Random forest | Impact: 1 |
| Neural networks | Impact: 2 |
| Deep learning | Impact: 2 |
| Ensemble methods | Impact: 2 |
| Generative AI | Impact: 3 |
| Reinforcement learning | Impact: 3 |
| Other | Impact: 1 |

---

## A1_8

**Question:** Where did the AI system or model originate?

- **Type:** `multiselect`
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** `Impact`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Developed in-house | Impact: 2 |
| Third-party vendor | Impact: 3 |
| Open-source model | Impact: 2 |
| Cloud-based service | Impact: 2 |
| Pre-trained model (customized) | Impact: 2 |
| Pre-trained model (used as-is) | Impact: 3 |

---

## A1_9

**Question:** How is the AI system integrated into your operations?

- **Type:** `multiselect`
- **Domains:** Reliability and Safety
- **Target Metric:** `Likelihood`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Standalone tool | Likelihood: 1 |
| Embedded in existing software | Likelihood: 2 |
| Part of a broader system | Likelihood: 2 |
| API or cloud service | Likelihood: 2 |
| Mobile or edge deployment | Likelihood: 3 |
| Real-time system | Likelihood: 3 |

---

## A2_1

**Question:** How are data sources and quality tracked?

- **Type:** `multiselect`
- **Domains:** Privacy Protection and Security, Transparency and Explainability
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| We maintain a data catalog | Control_Effectiveness: -2 |
| We track data lineage | Control_Effectiveness: -2 |
| We monitor data quality metrics | Control_Effectiveness: -3 |
| We version control datasets | Control_Effectiveness: -1 |
| We document data transformations | Control_Effectiveness: -2 |
| No formal tracking | Control_Effectiveness: 0 |

---

## A2_2

**Question:** What environmental, external, or real-time data does the system rely on?

- **Type:** `text`
- **Domains:** Reliability and Safety
- **Target Metric:** `Impact`

---

## A2_3

**Question:** What safeguards exist to ensure data quality and integrity?

- **Type:** `multiselect`
- **Domains:** Reliability and Safety
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Automated validation rules | Control_Effectiveness: -2 |
| Manual review processes | Control_Effectiveness: -1 |
| Data cleansing pipelines | Control_Effectiveness: -2 |
| Anomaly detection | Control_Effectiveness: -3 |
| Access controls | Control_Effectiveness: -1 |
| Regular audits | Control_Effectiveness: -2 |
| No safeguards | Control_Effectiveness: 0 |

---

## A2_4

**Question:** What types of data does the system process?

- **Type:** `multiselect`
- **Domains:** Privacy Protection and Security
- **Target Metric:** `Impact`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Personal information | Impact: 3 |
| Financial data | Impact: 3 |
| Health information | Impact: 3 |
| Operational metrics | Impact: 1 |
| Transactional data | Impact: 2 |
| Behavioral data | Impact: 2 |
| Environmental sensors | Impact: 1 |
| Public data | Impact: 1 |
| Other | Impact: 1 |

---

## A2_5

**Question:** Rate the quality of input data on the following dimensions (1-5 scale)

- **Type:** `rating_multi`
- **Domains:** Reliability and Safety
- **Target Metric:** `Likelihood`
- **Special Computation:** `DataQualityFactor`
- **Formula:** DataQualityFactor = 6 - (average of 5 ratings)

**Dimensions:**

- accuracy: Field `A2_5_accuracy`
- completeness: Field `A2_5_completeness`
- reliability: Field `A2_5_reliability`
- relevance: Field `A2_5_relevance`
- timeliness: Field `A2_5_timeliness`

**Notes:** Lower quality (rating=1) increases risk. Higher quality (rating=5) reduces risk. Factor ranges from 1.0 (perfect quality) to 5.0 (very poor quality).

---

## A2_6

**Question:** What is the Business Impact Level (BIL) of the input data?

- **Type:** `single_select`
- **Domains:** Privacy Protection and Security
- **Target Metric:** `Impact`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| BIL-0 (Public) | Impact: 1 |
| BIL-1 (Low) | Impact: 2 |
| BIL-2 (Medium) | Impact: 3 |
| BIL-3 (High) | Impact: 4 |
| BIL-4 (Critical) | Impact: 5 |

---

## A2_7

**Question:** Does the system process regulated or sensitive data?

- **Type:** `yes_no`
- **Domains:** Privacy Protection and Security, Accountability
- **Target Metric:** `Impact`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| No | Impact: 0 |
| Yes | Impact: 3 |

---

## A2_8

**Question:** Are user inputs required for the system to function?

- **Type:** `yes_no`
- **Domains:** Reliability and Safety
- **Target Metric:** `Likelihood`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| No | Likelihood: 0 |
| Yes | Likelihood: 2 |

---

## A3_1

**Question:** What types of human-AI interfaces does the system use?

- **Type:** `multiselect`
- **Domains:** Transparency and Explainability, Accountability
- **Target Metric:** `Likelihood`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Dashboard or visualization | Likelihood: 1 |
| Recommendation system | Likelihood: 2 |
| Decision support interface | Likelihood: 2 |
| Automated alerts | Likelihood: 2 |
| Chatbot or conversational AI | Likelihood: 2 |
| Direct system integration (no user interface) | Likelihood: 3 |
| Other | Likelihood: 1 |

---

## A3_2

**Question:** Rate the typical expertise of users interacting with the system (1-5 scale)

- **Type:** `rating_multi`
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** `Likelihood`
- **Special Computation:** `ExpertiseFactor`
- **Formula:** ExpertiseFactor = 6 - (average of 3 ratings)

**Dimensions:**

- technical: Field `A3_2_technical`
- domain: Field `A3_2_domain`
- ai_literacy: Field `A3_2_ai_literacy`

**Notes:** Lower expertise increases likelihood of misuse or misinterpretation. Factor ranges from 1.0 (expert users) to 5.0 (novice users).

---

## A3_3

**Question:** Which groups are impacted by the system's decisions?

- **Type:** `multiselect`
- **Domains:** Fairness, Accountability
- **Target Metric:** `Impact`

**Notes:** Each selected group contributes its Impact value to the total.

---

## A3_4

**Question:** How are affected parties notified that AI is involved in decisions?

- **Type:** `multiselect`
- **Domains:** Transparency and Explainability, Accountability
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Explicit disclosure in interface | Control_Effectiveness: -3 |
| Terms of service or policy | Control_Effectiveness: -1 |
| On-demand explanation available | Control_Effectiveness: -2 |
| Training or documentation | Control_Effectiveness: -2 |
| No notification | Control_Effectiveness: 0 |

---

## A3_5

**Question:** What impacts could the system have on staff? (Select impacts and rate severity 1-5)

- **Type:** `multiselect_with_severity`
- **Domains:** Fairness, Accountability
- **Target Metric:** `Impact`

**Notes:** Severity rating scales the cumulative impact. Rating of 3 is neutral, 5 doubles impact, 1 reduces to one-third.

---

## A3_6

**Question:** What impacts could the system have on external groups? (Select impacts and rate severity 1-3)

- **Type:** `multiselect_with_severity`
- **Domains:** Fairness, Accountability
- **Target Metric:** `Impact`

**Notes:** Severity rating scales the cumulative impact. Rating of 2 is neutral, 3 increases impact by 50%, 1 cuts it in half.

---

## A4_1

**Question:** What are the primary outputs of the AI system?

- **Type:** `multiselect`
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** `Impact`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Recommendations | Impact: 2 |
| Classifications | Impact: 2 |
| Predictions | Impact: 2 |
| Risk scores | Impact: 3 |
| Automated decisions | Impact: 4 |
| Content generation | Impact: 2 |
| Data insights | Impact: 1 |
| Alerts or notifications | Impact: 2 |
| Reports | Impact: 1 |
| Other | Impact: 1 |

---

## A4_2

**Question:** Are outputs sent to external systems without human review?

- **Type:** `yes_no`
- **Domains:** Accountability, Reliability and Safety
- **Target Metric:** `Likelihood`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| No | Likelihood: 0 |
| Yes | Likelihood: 2 |

---

## A4_3

**Question:** What is the Business Impact Level (BIL) of the system outputs?

- **Type:** `single_select`
- **Domains:** Privacy Protection and Security
- **Target Metric:** `Impact`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Official | Impact: 0 |
| Official: Sensitive | Impact: 1 |
| Protected | Impact: 2 |
| Highly Protected | Impact: 3 |
| Secret | Impact: 4 |
| Top Secret | Impact: 5 |

---

## A4_4

**Question:** How are system outputs tracked?

- **Type:** `multiselect`
- **Domains:** Accountability, Contestability
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Stored in database | Control_Effectiveness: -2 |
| Logged in audit system | Control_Effectiveness: -3 |
| Logged in CRM/case system | Control_Effectiveness: -2 |
| Logged in activity logs | Control_Effectiveness: -2 |
| Retention based on policy | Control_Effectiveness: -1 |
| Not currently tracked | Control_Effectiveness: 0 |

**Notes:** Output tracking improves control effectiveness and enables contestability. 'Not currently tracked' should be flagged as a risk.

---

## A4_5

**Question:** Are there risks associated with unauthorized access to system outputs?

- **Type:** `yes_no_with_options`
- **Domains:** Privacy Protection and Security, Reliability and Safety
- **Target Metric:** `Impact and Likelihood`
- **Modifier Type:** `dual`

**Scoring Options:**

- **No:**
  - Impact: 0, Likelihood: 0
- **Yes:**
  - Has sub-question (see schema for details)

**Notes:** Two-part question. If 'No', no additional risk. If 'Yes', each selected risk scenario applies both Impact and Likelihood modifiers.

---

## A4_6

**Question:** What types of regulated or sensitive data are included in system outputs?

- **Type:** `multiselect`
- **Domains:** Privacy Protection and Security, Fairness
- **Target Metric:** `Impact`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Personal | Impact: 2 |
| Sensitive | Impact: 3 |
| Financial | Impact: 3 |
| Health | Impact: 4 |
| Child-related | Impact: 5 |
| Law enforcement | Impact: 5 |
| Indigenous data | Impact: 5 |
| Confidential government data | Impact: 4 |
| Operationally sensitive data | Impact: 3 |

**Notes:** Each selected data type contributes its Impact value. Multiple selections are cumulative.

---

## A4_7

**Question:** Who has access to personally identifiable information (PII) in system outputs?

- **Type:** `text`
- **Domains:** Privacy Protection and Security
- **Target Metric:** `TBD`

**Notes:** Text response will be analyzed using LLM to determine appropriate Impact/Likelihood modifiers.

---

## A4_8

**Question:** Could system outputs trigger legal, regulatory, or compliance actions?

- **Type:** `text`
- **Domains:** Accountability
- **Target Metric:** `TBD`

**Notes:** Text response will be analyzed using LLM to determine appropriate Impact/Likelihood modifiers.

---

## A5_1

**Question:** Who is accountable for the AI system's performance and decisions?

- **Type:** `single_select`
- **Domains:** Accountability
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Product owner | Control_Effectiveness: -2 |
| System owner | Control_Effectiveness: -3 |
| Executive sponsor | Control_Effectiveness: -2 |
| Service manager | Control_Effectiveness: -3 |
| Data custodian | Control_Effectiveness: -3 |
| Governance committee | Control_Effectiveness: -4 |
| AI oversight board | Control_Effectiveness: -4 |

**Notes:** Clear accountability structures improve control effectiveness. Higher-level oversight (committees, boards) provide stronger governance.

---

## A5_10

**Question:** Does the AI system operate under specific regulatory obligations or frameworks?

- **Type:** `yes_no_with_subsections`
- **Domains:** Accountability, Privacy Protection and Security
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| No | Control_Effectiveness: 0 |
| Yes | Control_Effectiveness: 0 |

**Notes:** Multi-part question. All modifiers only apply if 'Yes' is selected. Each subsection is cumulative. Strong controls from critical infrastructure, child protection, and law enforcement obligations.

---

## A5_11

**Question:** Where will this AI solution be deployed?

- **Type:** `single_select`
- **Domains:** Accountability, Reliability and Safety, Human, Societal and Environmental Wellbeing
- **Target Metric:** `Likelihood and Control_Effectiveness`
- **Modifier Type:** `dual`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Internal use only | Likelihood: 0, Control_Effectiveness: 0 |
| Internal + selected partners | Likelihood: 1, Control_Effectiveness: -1 |
| Public-facing | Likelihood: 2, Control_Effectiveness: -1 |
| Citizen-facing high-sensitivity | Likelihood: 3, Control_Effectiveness: -2 |
| Embedded in another product | Likelihood: 2, Control_Effectiveness: -1 |
| Multi-channel deployment | Likelihood: 3, Control_Effectiveness: -2 |

**Notes:** Single select - only ONE deployment location applies. Wider deployment increases likelihood of risk exposure but also may come with better controls. Citizen-facing and multi-channel deployments have highest risk exposure but strongest control requirements.

---

## A5_2

**Question:** How is system performance tracked and reported?

- **Type:** `text`
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** `TBD`

**Notes:** Text response will be analyzed using LLM to determine appropriate Control Effectiveness modifiers.

---

## A5_3

**Question:** What monitoring and evaluation processes are in place? (Select all that apply)

- **Type:** `multiselect`
- **Domains:** Reliability and Safety, Accountability
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Regular system audits | Control_Effectiveness: -3 |
| Continuous performance monitoring | Control_Effectiveness: -4 |
| User feedback collection | Control_Effectiveness: -2 |
| Periodic stakeholder reviews | Control_Effectiveness: -2 |
| Independent evaluation | Control_Effectiveness: -4 |

**Notes:** Monitoring and evaluation processes improve control effectiveness. Multiple selections are cumulative.

---

## A5_4

**Question:** How frequently will monitoring and evaluation occur?

- **Type:** `single_select`
- **Domains:** Reliability and Safety
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Weekly | Control_Effectiveness: -4 |
| Monthly | Control_Effectiveness: -3 |
| Quarterly | Control_Effectiveness: -2 |
| Annually | Control_Effectiveness: -1 |
| Event-driven | Control_Effectiveness: -3 |

**Notes:** More frequent monitoring improves control effectiveness. Weekly monitoring provides the strongest control.

---

## A5_5

**Question:** Has the system undergone independent review or audit?

- **Type:** `yes_no`
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Yes | Control_Effectiveness: -2 |
| No | Control_Effectiveness: 0 |

**Notes:** Independent review provides external validation and improves control effectiveness.

---

## A5_6

**Question:** Who is responsible for ongoing monitoring?

- **Type:** `single_select`
- **Domains:** Accountability
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| ICT Ops | Control_Effectiveness: -2 |
| Data Science team | Control_Effectiveness: -2 |
| Risk/Compliance | Control_Effectiveness: -3 |
| Business Owner | Control_Effectiveness: -2 |
| Vendor | Control_Effectiveness: -1 |
| Customer-facing staff | Control_Effectiveness: -1 |
| External auditor | Control_Effectiveness: -4 |

**Notes:** Different roles provide varying levels of control oversight. External auditors and Risk/Compliance roles provide the strongest control.

---

## A5_7

**Question:** What stakeholder engagement activities have been conducted?

- **Type:** `multiselect`
- **Domains:** Human-centred Values, Fairness
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Workshops | Control_Effectiveness: -2 |
| Public consultation | Control_Effectiveness: -3 |
| Union consultation | Control_Effectiveness: -2 |
| Focus groups | Control_Effectiveness: -2 |
| User feedback sessions | Control_Effectiveness: -1 |
| Accessibility reviews | Control_Effectiveness: -3 |
| No engagements planned | Control_Effectiveness: 0 |

**Notes:** Stakeholder engagement improves control effectiveness by incorporating diverse perspectives. Public consultation and accessibility reviews provide strong control benefits.

---

## A5_8

**Question:** What methods exist for detecting harm and responding to incidents?

- **Type:** `multiselect`
- **Domains:** Reliability and Safety, Human, Societal and Environmental Wellbeing
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Alerting and monitoring | Control_Effectiveness: -3 |
| User complaints | Control_Effectiveness: -1 |
| Human review triggers | Control_Effectiveness: -3 |
| Automated anomaly detection | Control_Effectiveness: -4 |
| Escalation procedures | Control_Effectiveness: -3 |
| Incident response team | Control_Effectiveness: -4 |
| No defined contingencies | Control_Effectiveness: 0 |

**Notes:** Harm detection and response mechanisms improve control effectiveness. Automated detection and dedicated response teams provide the strongest control. 'No defined contingencies' should be flagged as a significant risk.

---

## A5_9

**Question:** Which values, principles, or frameworks guide the AI system's development and use?

- **Type:** `multiselect`
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Australia's AI Ethics Principles | Control_Effectiveness: -1 |
| Human Rights Act | Control_Effectiveness: -2 |
| Data governance policies | Control_Effectiveness: -2 |
| WHS | Control_Effectiveness: -1 |
| Accessibility standards | Control_Effectiveness: -2 |
| Agency ethics statements | Control_Effectiveness: -1 |
| Privacy principles | Control_Effectiveness: -3 |
| Risk management framework | Control_Effectiveness: -3 |

**Notes:** Adherence to established values, principles, and frameworks improves control effectiveness. Privacy principles and risk management frameworks provide the strongest control benefits.

---

## B1_2

**Question:** What negative impacts could the AI system create?

- **Type:** `multiselect`
- **Domains:** Human, Societal and Environmental Wellbeing
- **Target Metric:** `Impact`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Privacy risks | Impact: 3 |
| Bias/discrimination | Impact: 3 |
| Transparency issues | Impact: 2 |
| Safety risks | Impact: 4 |
| Employment impacts | Impact: 2 |
| Social harm | Impact: 3 |
| Environmental impact | Impact: 2 |
| Accessibility issues | Impact: 2 |
| Legal/regulatory risks | Impact: 2 |
| Loss of trust | Impact: 2 |

**Notes:** Multiple selections are cumulative. Safety risks have the highest impact modifier.

---

## B1_3

**Question:** Could the AI system affect employee employment or job roles?

- **Type:** `single_select`
- **Domains:** Human, Societal and Environmental Wellbeing
- **Target Metric:** `Impact`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Yes | Impact: 2 |
| Unknown | Impact: 1 |
| No | Impact: 0 |

**Notes:** Single select - only ONE option applies. 'Unknown' reflects uncertainty about employment impacts.

---

## B2_1

**Question:** Has a Human Rights Impact Assessment (HRIA) been completed?

- **Type:** `yes_no`
- **Domains:** Human-centred Values
- **Target Metric:** `Control_Effectiveness`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Yes | Control_Effectiveness: -2 |
| No | Control_Effectiveness: 1 |

**Notes:** Completing an HRIA improves control effectiveness. Not completing one increases risk exposure.

---

## B2_2

**Question:** Rate the AI system's impact on the following dimensions:

- **Type:** `multi_rating`
- **Domains:** Human-centred Values
- **Target Metric:** `Impact`

**Categories:**

- **Human Rights** (Field: `B2_2_rights`)
  - Positive: Impact: -1
  - Neutral: Impact: 0
  - Negative: Impact: 2
  - Unknown: Impact: 1
- **Diversity** (Field: `B2_2_diversity`)
  - Positive: Impact: -1
  - Neutral: Impact: 0
  - Negative: Impact: 2
  - Unknown: Impact: 1
- **Individual Autonomy** (Field: `B2_2_autonomy`)
  - Positive: Impact: -1
  - Neutral: Impact: 0
  - Negative: Impact: 2
  - Unknown: Impact: 1

**Notes:** Each category is rated independently. Only ONE rating per category applies. All three ratings are cumulative. Positive impacts reduce risk, negative impacts increase it significantly.

---

## B2_3

**Question:** Were diverse perspectives included in the AI system's design and development?

- **Type:** `yes_no_with_options`
- **Domains:** Human-centred Values
- **Target Metric:** `Impact`

**Scoring Options:**

- **No:**
  - Impact: 2
- **Yes:**
  - Has sub-question (see schema for details)

**Notes:** Two-part question. If 'No', Impact +2. If 'Yes', Impact -2 PLUS each selected perspective adds -0.5. 'Other' option available but has no additional score modifier.

---

## B3_1

**Question:** Has bias testing been conducted on the AI system?

- **Type:** `yes_no_with_options`
- **Domains:** Fairness
- **Target Metric:** `Impact`

**Scoring Options:**

- **No:**
  - Impact: 2
- **Yes:**
  - Has sub-question (see schema for details)

**Notes:** Two-part question. If 'No', Impact +2. If 'Yes', Impact -2 PLUS each selected testing method adds -1. 'Informal or ad-hoc checks only' should be flagged as a risk despite the -1 modifier, as it indicates lack of formal testing.

---

## B3_2

**Question:** Could the AI system discriminate against specific groups?

- **Type:** `yes_unknown_no_with_options`
- **Domains:** Fairness
- **Target Metric:** `Impact`

**Scoring Options:**

- **No:**
  - Impact: 0
- **Unknown:**
  - Impact: 2
- **Yes:**
  - Has sub-question (see schema for details)

**Notes:** Three-option question. If 'No', Impact 0. If 'Unknown', Impact +2 only. If 'Yes', Impact +3 PLUS each selected group adds +1. This identifies potential discrimination risks.

---

## B4_1

**Question:** Has a Privacy Impact Assessment (PIA) been completed?

- **Type:** `yes_no`
- **Domains:** Privacy Protection and Security
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `mixed`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Yes | Control_Effectiveness: -2 |
| No | Control_Effectiveness: 2 |

**Notes:** Completing a PIA improves control effectiveness. Not completing one increases risk exposure.

---

## B4_2

**Question:** Does the AI system use personal information?

- **Type:** `yes_no_with_options`
- **Domains:** Privacy Protection and Security
- **Target Metric:** `Impact`

**Scoring Options:**

- **No:**
  - Impact: 0
- **Yes:**
  - Has sub-question (see schema for details)

**Notes:** Two-part question. If 'No', Impact 0. If 'Yes', Impact +2 PLUS each selected PI type adds its modifier. Health, Financial, and Biometric data carry highest impact.

---

## B4_3

**Question:** What security measures are in place to protect personal information?

- **Type:** `multiselect`
- **Domains:** Privacy Protection and Security
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Access controls | Control_Effectiveness: -1 |
| Encryption | Control_Effectiveness: -2 |
| Security testing | Control_Effectiveness: -2 |
| Anonymisation | Control_Effectiveness: -2 |
| PETs | Control_Effectiveness: -2 |

**Notes:** Multiple selections are cumulative. Each security measure improves control effectiveness. Encryption, Security testing, Anonymisation, and PETs (Privacy Enhancing Technologies) provide stronger protection.

---

## B5_1

**Question:** Has the system been tested for reliability?

- **Type:** `yes_no_with_rating`
- **Domains:** Reliability and Safety
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

- **No:**
  - Control_Effectiveness: 0
- **Yes:**
  - Has sub-question (see schema for details)

**Notes:** Two-part question. If 'No', CE 0 only. If 'Yes', CE 0 but unlocks rating scale (1-5). Rating reflects robustness of testing: 1 = Minimal/ad hoc, 5 = Comprehensive/formal. Higher ratings improve control effectiveness more.

---

## B5_2

**Question:** Is there a process to disengage the system if issues arise?

- **Type:** `yes_no`
- **Domains:** Reliability and Safety
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `mixed`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Yes | Control_Effectiveness: -2 |
| No | Control_Effectiveness: 2 |

**Notes:** Having a disengagement mechanism improves control effectiveness. Lacking one increases risk exposure.

---

## B5_3

**Question:** Does the AI system operate in a high-risk environment?

- **Type:** `yes_no_with_options`
- **Domains:** Reliability and Safety
- **Target Metric:** `Impact and Likelihood`
- **Modifier Type:** `dual`

**Scoring Options:**

- **No:**
  - Impact: 0, Likelihood: 0
- **Yes:**
  - Has sub-question (see schema for details)

**Notes:** Two-part question with dual metrics. If 'No', Impact 0 and Likelihood 0 only. If 'Yes', unlocks environment options. Each selected environment applies both Impact and Likelihood modifiers. Democratic processes carry the highest impact.

---

## B6_1

**Question:** How transparent is the AI solution's operation? (1 = Very Low, 5 = Very High)

- **Type:** `rating_scale`
- **Domains:** Transparency and Explainability
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Rating Scale (1-5):**

| Rating | Scoring |
|--------|----------|
| 1 | Control_Effectiveness: 0 |
| 2 | Control_Effectiveness: -0.5 |
| 3 | Control_Effectiveness: -1.0 |
| 4 | Control_Effectiveness: -1.5 |
| 5 | Control_Effectiveness: -2.0 |

**Notes:** Rating scale 1-5. Higher transparency improves control effectiveness. Rating 1 (Very Low) has no effect, Rating 5 (Very High) provides strongest control benefit.

---

## B6_2

**Question:** Can the system explain its outputs or decisions? (1 = Very Low, 5 = Very High)

- **Type:** `rating_scale`
- **Domains:** Transparency and Explainability
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Rating Scale (1-5):**

| Rating | Scoring |
|--------|----------|
| 1 | Control_Effectiveness: 0 |
| 2 | Control_Effectiveness: -0.5 |
| 3 | Control_Effectiveness: -1.0 |
| 4 | Control_Effectiveness: -1.5 |
| 5 | Control_Effectiveness: -2.0 |

**Notes:** Rating scale 1-5. Higher explainability improves control effectiveness. Rating 1 (Very Low) has no effect, Rating 5 (Very High) provides strongest control benefit.

---

## B6_4

**Question:** Are there known limitations to the system's explainability?

- **Type:** `yes_no_with_text`
- **Domains:** Transparency and Explainability
- **Target Metric:** `Control_Effectiveness`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Yes | Control_Effectiveness: 2 |
| No | Control_Effectiveness: 0 |

**Notes:** If Yes, CE +2 (increases risk). Text description is captured for reporting but does not affect scoring.

---

## B7_2

**Question:** How quickly can a decision be challenged or reviewed?

- **Type:** `single_select`
- **Domains:** Contestability
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `mixed`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Immediately | Control_Effectiveness: -2 |
| Within Hours | Control_Effectiveness: -1 |
| Within Days | Control_Effectiveness: 0 |
| Within Weeks | Control_Effectiveness: 1 |
| Longer than weeks | Control_Effectiveness: 2 |
| Unknown | Control_Effectiveness: 1 |

**Notes:** Single select - only ONE option applies. Faster challenge response improves control effectiveness. Immediate and hourly responses provide strongest control. Extended timelines or unknown processes increase risk.

---

## B8_2

**Question:** Have clear roles and responsibilities been established for AI oversight?

- **Type:** `yes_no`
- **Domains:** Accountability
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `mixed`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Yes | Control_Effectiveness: -2 |
| No | Control_Effectiveness: 2 |

**Notes:** Established roles improve control effectiveness. Lack of clear roles increases risk.

---

## B8_3

**Question:** Have staff been trained on AI system use and limitations?

- **Type:** `yes_no`
- **Domains:** Accountability
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `mixed`

**Scoring Options:**

| Option | Scoring |
|--------|----------|
| Yes | Control_Effectiveness: -2 |
| No | Control_Effectiveness: 2 |

**Notes:** Staff training improves control effectiveness. Lack of training increases risk.

---

## B8_4

**Question:** Are safeguards in place to prevent overreliance on AI outputs?

- **Type:** `yes_no_with_options`
- **Domains:** Accountability
- **Target Metric:** `Control_Effectiveness`
- **Modifier Type:** `negative`

**Scoring Options:**

- **No:**
  - Control_Effectiveness: 2
- **Yes:**
  - Has sub-question (see schema for details)

**Notes:** Two-part question. If 'No', CE +2 only. If 'Yes', CE -2 PLUS each selected safeguard adds -0.5. Multiple safeguards are cumulative.

---

