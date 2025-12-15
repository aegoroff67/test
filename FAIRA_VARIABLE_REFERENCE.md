# FAIRA Risk Assessment - Complete Variable Reference (CORRECTED)

## Master Formula

```
Raw Risk Score = (Total Impact × Total Likelihood) ÷ Control Effectiveness
```

Where:
- **Total Likelihood** is modified by three special computed factors:
  - AutonomyFactor (from A1.6)
  - DataQualityFactor (from A2.5)  
  - ExpertiseFactor (from A3.2)

---

## Special Computed Factors

### 1. AutonomyFactor (A1.6)
**Question**: Does the system convert its outputs directly into actions without human intervention?
- **If No**: Factor = 1.0
- **If Yes**: Factor = 2.0 × max(selected action multipliers)
  - Notifications only: 1.0
  - Data updates: 1.2
  - Workflow triggers: 1.3
  - Financial transactions: 1.8
  - Access control changes: 1.5
  - Content publication: 1.4
  - Equipment control: 1.9
  - Other: 1.1

**Formula**: `AutonomyFactor = base × max(action_multipliers)`

**Modifies**: Total Likelihood

---

### 2. DataQualityFactor (A2.5)
**Question**: Rate the quality of input data on the following dimensions (1-5 scale)
- Dimensions:
  - Accuracy (A2_5_accuracy)
  - Completeness (A2_5_completeness)
  - Reliability (A2_5_reliability)
  - Relevance (A2_5_relevance)
  - Timeliness (A2_5_timeliness)

**Formula**: `DataQualityFactor = 6 - average(5 quality ratings)`

**Range**: 1.0 (perfect quality, all ratings = 5) to 5.0 (very poor quality, all ratings = 1)

**Modifies**: Total Likelihood

---

### 3. ExpertiseFactor (A3.2)
**Question**: Rate the typical expertise of users interacting with the system (1-5 scale)
- Dimensions:
  - Technical expertise (A3_2_technical)
  - Domain expertise (A3_2_domain)
  - AI literacy (A3_2_ai_literacy)

**Formula**: `ExpertiseFactor = 6 - average(3 expertise ratings)`

**Range**: 1.0 (expert users, all ratings = 5) to 5.0 (novice users, all ratings = 1)

**Modifies**: Total Likelihood

---

## Impact Variables

### Section A1: AI Solution Fundamentals
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| A1_1 | Primary function | Automate tasks: +1, Support decisions: +2, Autonomous decisions: +3, Predict: +2, Generate content: +1, Classify: +1, Detect patterns: +2, Other: +1 | Accountability, Transparency |
| A1_3 | AI features | NLP: +1, Computer vision: +1, Recommendation: +2, Predictive modeling: +2, Anomaly detection: +2, Speech: +1, Content gen: +1, Optimization: +2, RL: +3, Other: +1 | Accountability, Transparency |
| A1_4 | Decision types | Operational: +1, Resource: +2, Risk: +3, Customer: +2, Compliance: +3, Safety: +3, Quality: +2, Strategic: +2, Personnel: +3 | Accountability, Fairness |
| A1_5 | Tangible benefits (negative modifiers) | Cost: -1, Time: -1, Accuracy: -2, UX: -1, Scalability: -1, Better decisions: -2, Risk mitigation: -2, Compliance: -2 | Accountability |
| A1_7 | AI model type | Rule-based: +1, Linear: +1, Decision trees: +1, Random forest: +1, Neural nets: +2, Deep learning: +2, Ensemble: +2, Generative: +3, RL: +3, Other: +1 | Transparency, Accountability |
| A1_8 | AI source | In-house: +2, Third-party: +3, Open-source: +2, Cloud: +2, Pre-trained custom: +2, Pre-trained as-is: +3 | Accountability, Transparency |

### Section A2: Data and Inputs
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| A2_4 | Data types | Personal: +3, Financial: +3, Health: +3, Operational: +1, Transactional: +2, Behavioral: +2, Environmental: +1, Public: +1, Other: +1 | Privacy, Data Integrity |
| A2_6 | Input BIL | BIL-0: +1, BIL-1: +2, BIL-2: +3, BIL-3: +4, BIL-4: +5 | Privacy, Security |
| A2_7 | Regulated data | No: 0, Yes: +3 | Privacy, Compliance |

### Section A3: Human Interface and Impact
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| A3_3 | Impacted groups | Staff: +2, Customers: +2, Third-party: +2, Regulatory: +3, Public: +3, Vulnerable: +4, Other: +1 | Fairness, Accountability |
| A3_5 | Staff impacts (with severity multiplier) | Job role: 2, Workload: 1, Monitoring: 2, Career: 3, Job security: 4, Skills: 2, No impact: 0. Formula: sum(base) × (severity/3) | Fairness, Accountability |
| A3_6 | Group impacts (with severity multiplier) | Service quality: 2, Access: 3, Financial: 3, Privacy: 3, Trust: 2, Legal: 4, No impact: 0. Formula: sum(base) × (severity/2) | Fairness, Accountability |

### Section A4: Outputs and Actions
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| A4_1 | Primary outputs | Recommendations: +2, Classifications: +2, Predictions: +2, Risk scores: +3, Automated decisions: +4, Content: +2, Insights: +1, Alerts: +2, Reports: +1, Other: +1 | Accountability, Transparency |
| A4_3 | Output BIL | Official: 0, Official Sensitive: +1, Protected: +2, Highly Protected: +3, Secret: +4, Top Secret: +5 | Privacy Protection & Security |
| A4_5 | Output risks (dual: Impact & Likelihood) | If Yes: Misrouted: +2/+2, Excessive exposure: +3/+3, Sensitive attributes: +4/+4, Incorrect system: +3/+3, Injection: +4/+4 | Privacy Protection & Security, Reliability & Safety |
| A4_6 | Regulated output data | Personal: +2, Sensitive: +3, Financial: +3, Health: +4, Child: +5, Law enforcement: +5, Indigenous: +5, Gov confidential: +4, Operational: +3 | Privacy Protection & Security, Fairness |

### Section B1: Human, Societal and Environmental Wellbeing
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| B1_2 | Negative impacts | Privacy: +3, Bias: +3, Transparency: +2, Safety: +4, Employment: +2, Social harm: +3, Environmental: +2, Accessibility: +2, Legal: +2, Trust: +2 | Human, Societal & Environmental Wellbeing |
| B1_3 | Employee employment | Yes: +2, Unknown: +1, No: 0 | Human, Societal & Environmental Wellbeing |

### Section B2: Human-Centered Values
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| B2_2_rights | Human Rights rating | Positive: -1, Neutral: 0, Negative: +2, Unknown: +1 | Human-Centered Values |
| B2_2_diversity | Diversity rating | Positive: -1, Neutral: 0, Negative: +2, Unknown: +1 | Human-Centered Values |
| B2_2_autonomy | Individual Autonomy rating | Positive: -1, Neutral: 0, Negative: +2, Unknown: +1 | Human-Centered Values |
| B2_3 | Diverse perspectives | No: +2, Yes: -2 + perspectives. Each perspective: -0.5 (Disabilities, Cultural, Gender, Age, Indigenous, Socioeconomic) | Human-Centered Values |

### Section B3: Fairness
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| B3_1 | Bias testing | No: +2, Yes: -2 + methods. Each method: -1 (Statistical parity, Disparate impact, Dataset bias, Interpretability, Human panels, Synthetic testing, Accessibility, Security, Vendor tests, Informal) | Fairness |
| B3_2 | Discrimination possible | No: 0, Unknown: +2, Yes: +3 + groups. Each group: +1 (Age, Disabilities, Racial/ethnic, Religious, Gender, Sexual orientation, Socioeconomic) | Fairness |

### Section B4: Privacy Protection and Security
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| B4_2 | Personal info used | No: 0, Yes: +2 + types. Identifiable: +1, Sensitive: +2, Health: +3, Financial: +3, Biometric: +3 | Privacy Protection & Security |

### Section B5: Reliability and Safety
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| B5_3 | High-risk environment (dual: Impact & Likelihood) | If Yes: Essential services: +3/+1, Critical infra: +4/+2, Health: +4/+1, Education: +2/0, Law enforcement: +4/+1, Justice admin: +4/0, Democratic: +5/+1 | Reliability & Safety |

---

## Likelihood Variables

### Section A1: AI Solution Fundamentals
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| A1_6 | Autonomy level | See AutonomyFactor (special computation) | Accountability, Reliability & Safety |
| A1_9 | Integration | Standalone: +1, Embedded: +2, Part of system: +2, API/cloud: +2, Mobile/edge: +3, Real-time: +3 | Reliability & Safety |

### Section A2: Data and Inputs
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| A2_5 | Data quality | See DataQualityFactor (special computation) | Data Integrity, Reliability & Safety |
| A2_8 | User inputs required | No: 0, Yes: +2 | Data Integrity, Reliability & Safety |

### Section A3: Human Interface and Impact
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| A3_1 | Interface types | Dashboard: +1, Recommendation: +2, Decision support: +2, Alerts: +2, Chatbot: +2, Direct integration: +3, Other: +1 | Explainability, Accountability |
| A3_2 | User expertise | See ExpertiseFactor (special computation) | Accountability, Explainability |

### Section A4: Outputs and Actions
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| A4_2 | External outputs without review | No: 0, Yes: +2 | Accountability, Reliability & Safety |
| A4_5 | Output risks (dual) | See Impact section above | Privacy Protection & Security, Reliability & Safety |

### Section A5: Governance and Oversight
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| A5_11 | Deployment location (dual: Likelihood & CE) | Internal only: 0/0, Internal+partners: +1/-1, Public: +2/-1, Citizen high-sensitivity: +3/-2, Embedded: +2/-1, Multi-channel: +3/-2 | Accountability, Reliability & Safety, Human/Societal/Environmental Wellbeing |

### Section B5: Reliability and Safety
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| B5_3 | High-risk environment (dual) | See Impact section above | Reliability & Safety |

---

## Control Effectiveness Variables

### Section A2: Data and Inputs
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| A2_1 | Data tracking | Data catalog: -2, Lineage: -2, Quality metrics: -3, Version control: -1, Transformations: -2, No tracking: 0 | Data Integrity, Transparency |
| A2_3 | Data safeguards | Validation: -2, Manual review: -1, Cleansing: -2, Anomaly detection: -3, Access controls: -1, Audits: -2, No safeguards: 0 | Data Integrity, Reliability & Safety |

### Section A3: Human Interface and Impact
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| A3_4 | Notification methods | Explicit disclosure: -3, Terms of service: -1, On-demand explanation: -2, Training/docs: -2, No notification: 0 | Transparency, Accountability |

### Section A4: Outputs and Actions
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| A4_4 | Output tracking | Database: -2, Audit system: -3, CRM: -2, Activity logs: -2, Policy retention: -1, Not tracked: 0 | Accountability, Contestability |

### Section A5: Governance and Oversight
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| A5_1 | Accountability role | Product owner: -2, System owner: -3, Executive sponsor: -2, Service manager: -3, Data custodian: -3, Gov committee: -4, AI oversight board: -4 | Accountability |
| A5_3 | Monitoring processes | System audits: -3, Continuous monitoring: -4, User feedback: -2, Stakeholder reviews: -2, Independent eval: -4 | Reliability & Safety, Accountability |
| A5_4 | Monitoring frequency | Weekly: -4, Monthly: -3, Quarterly: -2, Annually: -1, Event-driven: -3 | Reliability & Safety |
| A5_5 | Independent review | Yes: -2, No: 0 | Accountability, Transparency |
| A5_6 | Monitoring roles | ICT Ops: -2, Data Science: -2, Risk/Compliance: -3, Business Owner: -2, Vendor: -1, Customer-facing: -1, External auditor: -4 | Accountability |
| A5_7 | Stakeholder engagement | Workshops: -2, Public consultation: -3, Union: -2, Focus groups: -2, User feedback: -1, Accessibility: -3, None: 0 | Human-centred values, Fairness |
| A5_8 | Harm detection | Alerting: -3, User complaints: -1, Human triggers: -3, Automated anomaly: -4, Escalation: -3, Incident team: -4, No contingencies: 0 | Reliability & Safety, Human/Societal/Environmental Wellbeing |
| A5_9 | Values & principles | AU AI Ethics: -1, Human Rights Act: -2, Data governance: -2, WHS: -1, Accessibility: -2, Agency ethics: -1, Privacy principles: -3, Risk framework: -3 | Accountability, Transparency |
| A5_10 | Regulatory obligations | Complex multi-part. See detailed breakdown in A5_10 section | Accountability, Privacy Protection & Security |
| A5_11 | Deployment location (dual) | See Likelihood section above | Accountability, Reliability & Safety, Human/Societal/Environmental Wellbeing |

### Section B2: Human-Centered Values
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| B2_1 | HRIA completed | Yes: -2, No: +1 | Human-Centered Values |

### Section B4: Privacy Protection and Security
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| B4_1 | PIA completed | Yes: -2, No: +2 | Privacy Protection & Security |
| B4_3 | Security measures | Access controls: -1, Encryption: -2, Security testing: -2, Anonymisation: -2, PETs: -2 | Privacy Protection & Security |

### Section B5: Reliability and Safety
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| B5_1 | Reliability testing | No: 0, Yes: 0 + rating. Rating 1: -0.5, 2: -1, 3: -1.5, 4: -2, 5: -3 | Reliability & Safety |
| B5_2 | Disengagement mechanism | Yes: -2, No: +2 | Reliability & Safety |

### Section B6: Transparency and Explainability
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| B6_1 | Transparency (1-5 rating) | 1: 0, 2: -0.5, 3: -1, 4: -1.5, 5: -2 | Transparency & Explainability |
| B6_2 | Explainability (1-5 rating) | 1: 0, 2: -0.5, 3: -1, 4: -1.5, 5: -2 | Transparency & Explainability |
| B6_4 | Explainability limitations | Yes: +2, No: 0 | Transparency & Explainability |

### Section B7: Contestability
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| B7_2 | Challenge speed | Immediately: -2, Hours: -1, Days: 0, Weeks: +1, Longer: +2, Unknown: +1 | Contestability |

### Section B8: Accountability
| Variable | Question | Options & Modifiers | Domain |
|----------|----------|---------------------|--------|
| B8_2 | Roles established | Yes: -2, No: +2 | Accountability |
| B8_3 | Staff trained | Yes: -2, No: +2 | Accountability |
| B8_4 | Safeguards vs overreliance | No: +2, Yes: -2 + safeguards. Each safeguard: -0.5 (Human review, Confidence thresholds, Explainability req, Training, Override controls, Warnings, Quality monitoring) | Accountability |

---

## A5.10 Detailed Breakdown (Regulatory Obligations)

**Main Question**: Does the AI system operate under specific regulatory obligations or frameworks?
- No: CE 0
- Yes: CE 0 + subsections

**If Yes, four subsections** (cumulative):

### Commonwealth (Federal) Legislation (A5_10_commonwealth)
- Privacy Act 1988: -2
- APPs: -1
- NDB Scheme: -1
- Archives Act 1983: -1
- FOI Act 1982: -1
- SOCI Act: -3
- Criminal Code Act: -2

### Queensland State Legislation (A5_10_qld)
- Information Privacy Act 2009: -2
- Right to Information Act 2009: -1
- Public Records Act 2002: -1
- Child Protection Act: -3
- Domestic Violence Protection Act: -3
- Youth Justice Act: -2
- Mental Health Act: -2
- Hospital and Health Boards Act: -2
- Police Powers Act: -2

### Sector-Specific Obligations (A5_10_sector)
- Health information: -2
- Law enforcement: -3
- Education: -1
- Transport/safety-critical: -2
- Financial/taxation: -2
- Indigenous data governance: -3
- Workplace surveillance: -1
- Safety-of-life/emergency: -2
- Critical infrastructure: -3

### Frameworks, Standards, Policies (A5_10_frameworks)
- QGEA / IS18:2018: -1
- QLD AI Ethical Principles: -1
- QLD FAIRA Framework: 0
- AU AI Ethics Principles: -1
- ISO/IEC 42001: -2
- ISO/IEC 27001/27002: -1
- ISO/IEC 27701: -1
- ISO 31000: -1
- NIST AI RMF: -2

### Other (text field) (A5_10_other)
- Default modifier: -1

---

## Text Fields (Deferred for LLM Classification)

| Question | Field | Target Metric | Domain |
|----------|-------|---------------|--------|
| A1_2 | AI system version | None (reporting only) | Accountability |
| A2_2 | Environmental/external data | TBD | Data Integrity, Reliability & Safety |
| A4_7 | PII access | TBD | Privacy Protection & Security |
| A4_8 | Legal/regulatory triggers | TBD | Accountability, Compliance |
| A5_2 | Performance tracking method | TBD | Accountability, Transparency |
| B6_4_description | Explainability limitations description | None (reporting only) | Transparency & Explainability |

---

## Deferred Questions (To Be Addressed Later)

- B6.3 (entire question)
- B7.1 (entire question)
- B8.1 (entire question)

---

## Domain Summary

**All Domains in FAIRA Assessment:**
1. Accountability
2. Transparency
3. Transparency and Explainability
4. Explainability
5. Fairness
6. Privacy
7. Privacy Protection and Security
8. Security
9. Data Integrity
10. Reliability and Safety
11. Human-Centered Values
12. Human-centred values (variant spelling)
13. Human, Societal and Environmental Wellbeing
14. Contestability
15. Compliance

**Note**: Some domain names have variants (e.g., "Human-Centered Values" vs "Human-centred values"). These should be normalized in the calculation engine.

---

## Notes on Scoring Patterns

- **Negative modifiers** (e.g., -2, -1) generally **improve** control effectiveness or **reduce** risk
- **Positive modifiers** (e.g., +2, +3) generally **increase** risk or impact
- **Cumulative questions** (multiselect): All selected options add together
- **Single select questions**: Only ONE option applies
- **Two-part questions**: Main answer + conditional sub-options
- **Rating scales**: Typically 1-5, where higher ratings indicate better performance
- **Dual-metric questions**: Affect both Impact and Likelihood simultaneously

---

**Total Configured Questions**: 62 (42 in Part A, 20 in Part B)
**Deferred Questions**: 8 text fields + 3 full questions

**Generated**: FAIRA Scoring Schema v1.0
