# FAIRA Assessment - Complete Variable List

## Summary
- **Total Questions:** 62
- **Schema Version:** 1.0
- **Risk Formula:** Raw Risk Score = (Total Impact × Total Likelihood) / Control Effectiveness

## Questions by Section

- **A1:** 9 questions
- **A2:** 8 questions
- **A3:** 6 questions
- **A4:** 8 questions
- **A5:** 11 questions
- **B1:** 2 questions
- **B2:** 3 questions
- **B3:** 2 questions
- **B4:** 3 questions
- **B5:** 3 questions
- **B6:** 3 questions
- **B7:** 1 questions
- **B8:** 3 questions

---

## Complete Variable Table

| Question ID | Question Text | Type | Domains | Target Metric | Modifier Type | Special Computation |
|-------------|---------------|------|---------|---------------|---------------|---------------------|
| A1_1 | What is the primary function of the AI system? | multiselect | Accountability, Transparency and Explainability | Impact | Standard | N/A |
| A1_2 | What version is the AI system currently at? | text | Accountability | None | N/A | N/A |
| A1_3 | Which AI features or capabilities does the system include? | multiselect | Accountability, Transparency and Explainability | Impact | Standard | N/A |
| A1_4 | What types of decisions or problems does the AI system address? | multiselect | Accountability, Fairness | Impact | Standard | N/A |
| A1_5 | What tangible benefits does the AI system provide? | multiselect | Accountability | Impact | negative | N/A |
| A1_6 | Does the system convert its outputs directly into actions without human interven... | yes_no | Accountability, Reliability and Safety | Likelihood | Standard | AutonomyFactor |
| A1_7 | What type(s) of AI model or algorithm does the system use? | multiselect | Transparency and Explainability, Accountability | Impact | Standard | N/A |
| A1_8 | Where did the AI system or model originate? | multiselect | Accountability, Transparency and Explainability | Impact | Standard | N/A |
| A1_9 | How is the AI system integrated into your operations? | multiselect | Reliability and Safety | Likelihood | Standard | N/A |
| A2_1 | How are data sources and quality tracked? | multiselect | Privacy Protection and Security, Transparency and Explainability | Control_Effectiveness | negative | N/A |
| A2_2 | What environmental, external, or real-time data does the system rely on? | text | Reliability and Safety | Impact | Standard | N/A |
| A2_3 | What safeguards exist to ensure data quality and integrity? | multiselect | Reliability and Safety | Control_Effectiveness | negative | N/A |
| A2_4 | What types of data does the system process? | multiselect | Privacy Protection and Security | Impact | Standard | N/A |
| A2_5 | Rate the quality of input data on the following dimensions (1-5 scale) | rating_multi | Reliability and Safety | Likelihood | Standard | DataQualityFactor |
| A2_6 | What is the Business Impact Level (BIL) of the input data? | single_select | Privacy Protection and Security | Impact | Standard | N/A |
| A2_7 | Does the system process regulated or sensitive data? | yes_no | Privacy Protection and Security, Accountability | Impact | Standard | N/A |
| A2_8 | Are user inputs required for the system to function? | yes_no | Reliability and Safety | Likelihood | Standard | N/A |
| A3_1 | What types of human-AI interfaces does the system use? | multiselect | Transparency and Explainability, Accountability | Likelihood | Standard | N/A |
| A3_2 | Rate the typical expertise of users interacting with the system (1-5 scale) | rating_multi | Accountability, Transparency and Explainability | Likelihood | Standard | ExpertiseFactor |
| A3_3 | Which groups are impacted by the system's decisions? | multiselect | Fairness, Accountability | Impact | Standard | N/A |
| A3_4 | How are affected parties notified that AI is involved in decisions? | multiselect | Transparency and Explainability, Accountability | Control_Effectiveness | negative | N/A |
| A3_5 | What impacts could the system have on staff? (Select impacts and rate severity 1... | multiselect_with_severity | Fairness, Accountability | Impact | Standard | N/A |
| A3_6 | What impacts could the system have on external groups? (Select impacts and rate ... | multiselect_with_severity | Fairness, Accountability | Impact | Standard | N/A |
| A4_1 | What are the primary outputs of the AI system? | multiselect | Accountability, Transparency and Explainability | Impact | Standard | N/A |
| A4_2 | Are outputs sent to external systems without human review? | yes_no | Accountability, Reliability and Safety | Likelihood | Standard | N/A |
| A4_3 | What is the Business Impact Level (BIL) of the system outputs? | single_select | Privacy Protection and Security | Impact | Standard | N/A |
| A4_4 | How are system outputs tracked? | multiselect | Accountability, Contestability | Control_Effectiveness | negative | N/A |
| A4_5 | Are there risks associated with unauthorized access to system outputs? | yes_no_with_options | Privacy Protection and Security, Reliability and Safety | Impact and Likelihood | dual | N/A |
| A4_6 | What types of regulated or sensitive data are included in system outputs? | multiselect | Privacy Protection and Security, Fairness | Impact | Standard | N/A |
| A4_7 | Who has access to personally identifiable information (PII) in system outputs? | text | Privacy Protection and Security | TBD | Standard | N/A |
| A4_8 | Could system outputs trigger legal, regulatory, or compliance actions? | text | Accountability | TBD | Standard | N/A |
| A5_1 | Who is accountable for the AI system's performance and decisions? | single_select | Accountability | Control_Effectiveness | negative | N/A |
| A5_10 | Does the AI system operate under specific regulatory obligations or frameworks? | yes_no_with_subsections | Accountability, Privacy Protection and Security | Control_Effectiveness | negative | N/A |
| A5_11 | Where will this AI solution be deployed? | single_select | Accountability, Reliability and Safety, Human, Societal and Environmental Wellbeing | Likelihood and Control_Effectiveness | dual | N/A |
| A5_2 | How is system performance tracked and reported? | text | Accountability, Transparency and Explainability | TBD | Standard | N/A |
| A5_3 | What monitoring and evaluation processes are in place? (Select all that apply) | multiselect | Reliability and Safety, Accountability | Control_Effectiveness | negative | N/A |
| A5_4 | How frequently will monitoring and evaluation occur? | single_select | Reliability and Safety | Control_Effectiveness | negative | N/A |
| A5_5 | Has the system undergone independent review or audit? | yes_no | Accountability, Transparency and Explainability | Control_Effectiveness | negative | N/A |
| A5_6 | Who is responsible for ongoing monitoring? | single_select | Accountability | Control_Effectiveness | negative | N/A |
| A5_7 | What stakeholder engagement activities have been conducted? | multiselect | Human-centred Values, Fairness | Control_Effectiveness | negative | N/A |
| A5_8 | What methods exist for detecting harm and responding to incidents? | multiselect | Reliability and Safety, Human, Societal and Environmental Wellbeing | Control_Effectiveness | negative | N/A |
| A5_9 | Which values, principles, or frameworks guide the AI system's development and us... | multiselect | Accountability, Transparency and Explainability | Control_Effectiveness | negative | N/A |
| B1_2 | What negative impacts could the AI system create? | multiselect | Human, Societal and Environmental Wellbeing | Impact | Standard | N/A |
| B1_3 | Could the AI system affect employee employment or job roles? | single_select | Human, Societal and Environmental Wellbeing | Impact | Standard | N/A |
| B2_1 | Has a Human Rights Impact Assessment (HRIA) been completed? | yes_no | Human-centred Values | Control_Effectiveness | Standard | N/A |
| B2_2 | Rate the AI system's impact on the following dimensions: | multi_rating | Human-centred Values | Impact | Standard | N/A |
| B2_3 | Were diverse perspectives included in the AI system's design and development? | yes_no_with_options | Human-centred Values | Impact | Standard | N/A |
| B3_1 | Has bias testing been conducted on the AI system? | yes_no_with_options | Fairness | Impact | Standard | N/A |
| B3_2 | Could the AI system discriminate against specific groups? | yes_unknown_no_with_options | Fairness | Impact | Standard | N/A |
| B4_1 | Has a Privacy Impact Assessment (PIA) been completed? | yes_no | Privacy Protection and Security | Control_Effectiveness | mixed | N/A |
| B4_2 | Does the AI system use personal information? | yes_no_with_options | Privacy Protection and Security | Impact | Standard | N/A |
| B4_3 | What security measures are in place to protect personal information? | multiselect | Privacy Protection and Security | Control_Effectiveness | negative | N/A |
| B5_1 | Has the system been tested for reliability? | yes_no_with_rating | Reliability and Safety | Control_Effectiveness | negative | N/A |
| B5_2 | Is there a process to disengage the system if issues arise? | yes_no | Reliability and Safety | Control_Effectiveness | mixed | N/A |
| B5_3 | Does the AI system operate in a high-risk environment? | yes_no_with_options | Reliability and Safety | Impact and Likelihood | dual | N/A |
| B6_1 | How transparent is the AI solution's operation? (1 = Very Low, 5 = Very High) | rating_scale | Transparency and Explainability | Control_Effectiveness | negative | N/A |
| B6_2 | Can the system explain its outputs or decisions? (1 = Very Low, 5 = Very High) | rating_scale | Transparency and Explainability | Control_Effectiveness | negative | N/A |
| B6_4 | Are there known limitations to the system's explainability? | yes_no_with_text | Transparency and Explainability | Control_Effectiveness | Standard | N/A |
| B7_2 | How quickly can a decision be challenged or reviewed? | single_select | Contestability | Control_Effectiveness | mixed | N/A |
| B8_2 | Have clear roles and responsibilities been established for AI oversight? | yes_no | Accountability | Control_Effectiveness | mixed | N/A |
| B8_3 | Have staff been trained on AI system use and limitations? | yes_no | Accountability | Control_Effectiveness | mixed | N/A |
| B8_4 | Are safeguards in place to prevent overreliance on AI outputs? | yes_no_with_options | Accountability | Control_Effectiveness | negative | N/A |

---

## Detailed Breakdown by Section

### Section A1

#### A1_1
**Question:** What is the primary function of the AI system?

- **Type:** multiselect
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 8 options

#### A1_2
**Question:** What version is the AI system currently at?

- **Type:** text
- **Domains:** Accountability
- **Target Metric:** None
- **Modifier Type:** N/A
- **Options:** No scoring

#### A1_3
**Question:** Which AI features or capabilities does the system include?

- **Type:** multiselect
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 10 options

#### A1_4
**Question:** What types of decisions or problems does the AI system address?

- **Type:** multiselect
- **Domains:** Accountability, Fairness
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 9 options

#### A1_5
**Question:** What tangible benefits does the AI system provide?

- **Type:** multiselect
- **Domains:** Accountability
- **Target Metric:** Impact
- **Modifier Type:** negative
- **Options:** 8 options

#### A1_6
**Question:** Does the system convert its outputs directly into actions without human intervention?

- **Type:** yes_no
- **Domains:** Accountability, Reliability and Safety
- **Target Metric:** Likelihood
- **Modifier Type:** Standard
- **Special Computation:** AutonomyFactor
- **Options:** 1 options

#### A1_7
**Question:** What type(s) of AI model or algorithm does the system use?

- **Type:** multiselect
- **Domains:** Transparency and Explainability, Accountability
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 10 options

#### A1_8
**Question:** Where did the AI system or model originate?

- **Type:** multiselect
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 6 options

#### A1_9
**Question:** How is the AI system integrated into your operations?

- **Type:** multiselect
- **Domains:** Reliability and Safety
- **Target Metric:** Likelihood
- **Modifier Type:** Standard
- **Options:** 6 options

---

### Section A2

#### A2_1
**Question:** How are data sources and quality tracked?

- **Type:** multiselect
- **Domains:** Privacy Protection and Security, Transparency and Explainability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 6 options

#### A2_2
**Question:** What environmental, external, or real-time data does the system rely on?

- **Type:** text
- **Domains:** Reliability and Safety
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** See schema for details

#### A2_3
**Question:** What safeguards exist to ensure data quality and integrity?

- **Type:** multiselect
- **Domains:** Reliability and Safety
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 7 options

#### A2_4
**Question:** What types of data does the system process?

- **Type:** multiselect
- **Domains:** Privacy Protection and Security
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 9 options

#### A2_5
**Question:** Rate the quality of input data on the following dimensions (1-5 scale)

- **Type:** rating_multi
- **Domains:** Reliability and Safety
- **Target Metric:** Likelihood
- **Modifier Type:** Standard
- **Special Computation:** DataQualityFactor
- **Options:** 5 dimensions

#### A2_6
**Question:** What is the Business Impact Level (BIL) of the input data?

- **Type:** single_select
- **Domains:** Privacy Protection and Security
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 5 options

#### A2_7
**Question:** Does the system process regulated or sensitive data?

- **Type:** yes_no
- **Domains:** Privacy Protection and Security, Accountability
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 2 options

#### A2_8
**Question:** Are user inputs required for the system to function?

- **Type:** yes_no
- **Domains:** Reliability and Safety
- **Target Metric:** Likelihood
- **Modifier Type:** Standard
- **Options:** 2 options

---

### Section A3

#### A3_1
**Question:** What types of human-AI interfaces does the system use?

- **Type:** multiselect
- **Domains:** Transparency and Explainability, Accountability
- **Target Metric:** Likelihood
- **Modifier Type:** Standard
- **Options:** 7 options

#### A3_2
**Question:** Rate the typical expertise of users interacting with the system (1-5 scale)

- **Type:** rating_multi
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** Likelihood
- **Modifier Type:** Standard
- **Special Computation:** ExpertiseFactor
- **Options:** 3 dimensions

#### A3_3
**Question:** Which groups are impacted by the system's decisions?

- **Type:** multiselect
- **Domains:** Fairness, Accountability
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** See schema for details

#### A3_4
**Question:** How are affected parties notified that AI is involved in decisions?

- **Type:** multiselect
- **Domains:** Transparency and Explainability, Accountability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 5 options

#### A3_5
**Question:** What impacts could the system have on staff? (Select impacts and rate severity 1-5)

- **Type:** multiselect_with_severity
- **Domains:** Fairness, Accountability
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** See schema for details

#### A3_6
**Question:** What impacts could the system have on external groups? (Select impacts and rate severity 1-3)

- **Type:** multiselect_with_severity
- **Domains:** Fairness, Accountability
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** See schema for details

---

### Section A4

#### A4_1
**Question:** What are the primary outputs of the AI system?

- **Type:** multiselect
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 10 options

#### A4_2
**Question:** Are outputs sent to external systems without human review?

- **Type:** yes_no
- **Domains:** Accountability, Reliability and Safety
- **Target Metric:** Likelihood
- **Modifier Type:** Standard
- **Options:** 2 options

#### A4_3
**Question:** What is the Business Impact Level (BIL) of the system outputs?

- **Type:** single_select
- **Domains:** Privacy Protection and Security
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 6 options

#### A4_4
**Question:** How are system outputs tracked?

- **Type:** multiselect
- **Domains:** Accountability, Contestability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 6 options

#### A4_5
**Question:** Are there risks associated with unauthorized access to system outputs?

- **Type:** yes_no_with_options
- **Domains:** Privacy Protection and Security, Reliability and Safety
- **Target Metric:** Impact and Likelihood
- **Modifier Type:** dual
- **Options:** 1 options

#### A4_6
**Question:** What types of regulated or sensitive data are included in system outputs?

- **Type:** multiselect
- **Domains:** Privacy Protection and Security, Fairness
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 9 options

#### A4_7
**Question:** Who has access to personally identifiable information (PII) in system outputs?

- **Type:** text
- **Domains:** Privacy Protection and Security
- **Target Metric:** TBD
- **Modifier Type:** Standard
- **Options:** See schema for details

#### A4_8
**Question:** Could system outputs trigger legal, regulatory, or compliance actions?

- **Type:** text
- **Domains:** Accountability
- **Target Metric:** TBD
- **Modifier Type:** Standard
- **Options:** See schema for details

---

### Section A5

#### A5_1
**Question:** Who is accountable for the AI system's performance and decisions?

- **Type:** single_select
- **Domains:** Accountability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 7 options

#### A5_10
**Question:** Does the AI system operate under specific regulatory obligations or frameworks?

- **Type:** yes_no_with_subsections
- **Domains:** Accountability, Privacy Protection and Security
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 2 options

#### A5_11
**Question:** Where will this AI solution be deployed?

- **Type:** single_select
- **Domains:** Accountability, Reliability and Safety, Human, Societal and Environmental Wellbeing
- **Target Metric:** Likelihood and Control_Effectiveness
- **Modifier Type:** dual
- **Options:** 6 options

#### A5_2
**Question:** How is system performance tracked and reported?

- **Type:** text
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** TBD
- **Modifier Type:** Standard
- **Options:** See schema for details

#### A5_3
**Question:** What monitoring and evaluation processes are in place? (Select all that apply)

- **Type:** multiselect
- **Domains:** Reliability and Safety, Accountability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 5 options

#### A5_4
**Question:** How frequently will monitoring and evaluation occur?

- **Type:** single_select
- **Domains:** Reliability and Safety
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 5 options

#### A5_5
**Question:** Has the system undergone independent review or audit?

- **Type:** yes_no
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 2 options

#### A5_6
**Question:** Who is responsible for ongoing monitoring?

- **Type:** single_select
- **Domains:** Accountability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 7 options

#### A5_7
**Question:** What stakeholder engagement activities have been conducted?

- **Type:** multiselect
- **Domains:** Human-centred Values, Fairness
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 7 options

#### A5_8
**Question:** What methods exist for detecting harm and responding to incidents?

- **Type:** multiselect
- **Domains:** Reliability and Safety, Human, Societal and Environmental Wellbeing
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 7 options

#### A5_9
**Question:** Which values, principles, or frameworks guide the AI system's development and use?

- **Type:** multiselect
- **Domains:** Accountability, Transparency and Explainability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 8 options

---

### Section B1

#### B1_2
**Question:** What negative impacts could the AI system create?

- **Type:** multiselect
- **Domains:** Human, Societal and Environmental Wellbeing
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 10 options

#### B1_3
**Question:** Could the AI system affect employee employment or job roles?

- **Type:** single_select
- **Domains:** Human, Societal and Environmental Wellbeing
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 3 options

---

### Section B2

#### B2_1
**Question:** Has a Human Rights Impact Assessment (HRIA) been completed?

- **Type:** yes_no
- **Domains:** Human-centred Values
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** Standard
- **Options:** 2 options

#### B2_2
**Question:** Rate the AI system's impact on the following dimensions:

- **Type:** multi_rating
- **Domains:** Human-centred Values
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 3 categories

#### B2_3
**Question:** Were diverse perspectives included in the AI system's design and development?

- **Type:** yes_no_with_options
- **Domains:** Human-centred Values
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 1 options

---

### Section B3

#### B3_1
**Question:** Has bias testing been conducted on the AI system?

- **Type:** yes_no_with_options
- **Domains:** Fairness
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 1 options

#### B3_2
**Question:** Could the AI system discriminate against specific groups?

- **Type:** yes_unknown_no_with_options
- **Domains:** Fairness
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 2 options

---

### Section B4

#### B4_1
**Question:** Has a Privacy Impact Assessment (PIA) been completed?

- **Type:** yes_no
- **Domains:** Privacy Protection and Security
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** mixed
- **Options:** 2 options

#### B4_2
**Question:** Does the AI system use personal information?

- **Type:** yes_no_with_options
- **Domains:** Privacy Protection and Security
- **Target Metric:** Impact
- **Modifier Type:** Standard
- **Options:** 1 options

#### B4_3
**Question:** What security measures are in place to protect personal information?

- **Type:** multiselect
- **Domains:** Privacy Protection and Security
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 5 options

---

### Section B5

#### B5_1
**Question:** Has the system been tested for reliability?

- **Type:** yes_no_with_rating
- **Domains:** Reliability and Safety
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 1 options

#### B5_2
**Question:** Is there a process to disengage the system if issues arise?

- **Type:** yes_no
- **Domains:** Reliability and Safety
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** mixed
- **Options:** 2 options

#### B5_3
**Question:** Does the AI system operate in a high-risk environment?

- **Type:** yes_no_with_options
- **Domains:** Reliability and Safety
- **Target Metric:** Impact and Likelihood
- **Modifier Type:** dual
- **Options:** 1 options

---

### Section B6

#### B6_1
**Question:** How transparent is the AI solution's operation? (1 = Very Low, 5 = Very High)

- **Type:** rating_scale
- **Domains:** Transparency and Explainability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** Rating scale (1-5)

#### B6_2
**Question:** Can the system explain its outputs or decisions? (1 = Very Low, 5 = Very High)

- **Type:** rating_scale
- **Domains:** Transparency and Explainability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** Rating scale (1-5)

#### B6_4
**Question:** Are there known limitations to the system's explainability?

- **Type:** yes_no_with_text
- **Domains:** Transparency and Explainability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** Standard
- **Options:** 2 options

---

### Section B7

#### B7_2
**Question:** How quickly can a decision be challenged or reviewed?

- **Type:** single_select
- **Domains:** Contestability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** mixed
- **Options:** 6 options

---

### Section B8

#### B8_2
**Question:** Have clear roles and responsibilities been established for AI oversight?

- **Type:** yes_no
- **Domains:** Accountability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** mixed
- **Options:** 2 options

#### B8_3
**Question:** Have staff been trained on AI system use and limitations?

- **Type:** yes_no
- **Domains:** Accountability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** mixed
- **Options:** 2 options

#### B8_4
**Question:** Are safeguards in place to prevent overreliance on AI outputs?

- **Type:** yes_no_with_options
- **Domains:** Accountability
- **Target Metric:** Control_Effectiveness
- **Modifier Type:** negative
- **Options:** 1 options

---

