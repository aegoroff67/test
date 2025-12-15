# FAIRA Schema - Statistical Summary

## Overview
- **Total Questions:** 62
- **Schema Version:** 1.0
- **Risk Calculation Formula:** Raw Risk Score = (Total Impact × Total Likelihood) / Control Effectiveness

## Questions by Type

| Question Type | Count | Percentage |
|--------------|-------|------------|
| multiselect | 22 | 35.5% |
| yes_no | 10 | 16.1% |
| single_select | 8 | 12.9% |
| yes_no_with_options | 6 | 9.7% |
| text | 5 | 8.1% |
| rating_multi | 2 | 3.2% |
| multiselect_with_severity | 2 | 3.2% |
| rating_scale | 2 | 3.2% |
| yes_no_with_subsections | 1 | 1.6% |
| multi_rating | 1 | 1.6% |
| yes_unknown_no_with_options | 1 | 1.6% |
| yes_no_with_rating | 1 | 1.6% |
| yes_no_with_text | 1 | 1.6% |

## Target Metrics Distribution

| Target Metric | Count | Percentage |
|--------------|-------|------------|
| Control_Effectiveness | 25 | 40.3% |
| Impact | 23 | 37.1% |
| Likelihood | 7 | 11.3% |
| TBD | 3 | 4.8% |
| Impact and Likelihood | 2 | 3.2% |
| Likelihood and Control_Effectiveness | 1 | 1.6% |

## Domain Usage

| Domain | Question Count | Percentage |
|--------|---------------|------------|
| Accountability | 30 | 48.4% |
| Transparency and Explainability | 15 | 24.2% |
| Reliability and Safety | 15 | 24.2% |
| Privacy Protection and Security | 12 | 19.4% |
| Fairness | 8 | 12.9% |
| Human-centred Values | 4 | 6.5% |
| Human, Societal and Environmental Wellbeing | 4 | 6.5% |
| Contestability | 2 | 3.2% |

## Modifier Types

| Modifier Type | Count | Description |
|--------------|-------|-------------|
| standard | 34 | Standard positive scoring |
| negative | 19 | Improves control (negative values) |
| mixed | 5 | Can increase or decrease risk |
| dual | 3 | Affects multiple metrics simultaneously |

## Special Computations

Three questions use special factor calculations:

- **AutonomyFactor:** Computed from A1.6 (autonomy level)
- **DataQualityFactor:** Computed from A2.5 (data quality ratings)
- **ExpertiseFactor:** Computed from A3.2 (user expertise levels)

## Domain Coverage Analysis

### Questions Per Domain

#### Accountability
**30 questions** reference this domain:

A1_1, A1_2, A1_3, A1_4, A1_5, A1_6, A1_7, A1_8, A2_7, A3_1, A3_2, A3_3, A3_4, A3_5, A3_6, A4_1, A4_2, A4_4, A4_8, A5_1, A5_10, A5_11, A5_2, A5_3, A5_5, A5_6, A5_9, B8_2, B8_3, B8_4

#### Contestability
**2 questions** reference this domain:

A4_4, B7_2

#### Fairness
**8 questions** reference this domain:

A1_4, A3_3, A3_5, A3_6, A4_6, A5_7, B3_1, B3_2

#### Human, Societal and Environmental Wellbeing
**4 questions** reference this domain:

A5_11, A5_8, B1_2, B1_3

#### Human-centred Values
**4 questions** reference this domain:

A5_7, B2_1, B2_2, B2_3

#### Privacy Protection and Security
**12 questions** reference this domain:

A2_1, A2_4, A2_6, A2_7, A4_3, A4_5, A4_6, A4_7, A5_10, B4_1, B4_2, B4_3

#### Reliability and Safety
**15 questions** reference this domain:

A1_6, A1_9, A2_2, A2_3, A2_5, A2_8, A4_2, A4_5, A5_11, A5_3, A5_4, A5_8, B5_1, B5_2, B5_3

#### Transparency and Explainability
**15 questions** reference this domain:

A1_1, A1_3, A1_7, A1_8, A2_1, A3_1, A3_2, A3_4, A4_1, A5_2, A5_5, A5_9, B6_1, B6_2, B6_4

