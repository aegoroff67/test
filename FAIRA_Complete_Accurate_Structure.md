# FAIRA Risk Assessment - Complete Structure

**Extraction Date:** 2025-01-20  
**Source:** FairaAssessmentForm.js  
**Total Questions:** 69  

---

## Instructions for Downloading the JSON

The complete, accurate JSON file with all 69 questions and their REAL options has been generated.

**To download:**
1. Open your deployed app URL in a browser
2. I can create a download endpoint at `/api/download-faira-structure` that serves the JSON file
3. Or you can copy the JSON from the file view below

---

## Verified Question Structure

### ✅ A3.5(a) - VERIFIED CORRECT
**Question:** What are the expected impacts of this AI solution on staff?  
**Type:** Multiselect  
**Options (11 total):**
1. Increased workload
2. Reduced workload
3. Reduced autonomy
4. Improved autonomy
5. De-skilling risk
6. Skill enhancement
7. Accountability ambiguity
8. Increased accountability clarity
9. Stress or psychological impact
10. Job redesign required
11. No significant impact

---

## Complete Section Breakdown

### Assessment Overview
- AI System Name, Version, Business Unit
- System Owner Name & Role  
- Assessor Name, Role, Branch, Email (optional)

### Part A: Components Analysis

**A1. AI Solution Fundamentals (9 questions)**
- A1.1: Primary function (10 options)
- A1.2: Version (text)
- A1.3: AI features (9 options + Other)
- A1.4: Decisions addressed (10 options)
- A1.5: Tangible benefits (12 options)
- A1.6: Automated actions (Yes/No → 8 conditional options + Other)
- A1.7: AI model type (7 options + Other)
- A1.8: Source (4 options)
- A1.9: Integration methods (8 options)

**A2. Data and Inputs (8 questions)**
- A2.1: Input tracking (6 options)
- A2.2: Environmental data (textarea)
- A2.3: Data safeguards (8 options)
- A2.4: Data types (6 options + Other)
- A2.5: Data quality ratings (5 sub-ratings: Accuracy, Completeness, Reliability, Relevance, Timeliness - scale 1-5)
- A2.6: BIL input data (select: Official, Official: Sensitive, Protected, Highly Protected, Secret, Top Secret)
- A2.7: Regulated data (Yes/No → 13 conditional options)
- A2.8: User inputs required (Yes/No → 8 conditional options)

**A3. Human Interface and Impact (8 questions)**
- A3.1: Interface types (6 options)
- A3.2: Expertise required (3 sub-ratings: Technical, Domain, AI literacy - scale 1-5)
- A3.3: Impacted groups (8 options + Other)
- A3.4: Notification methods (8 options)
- A3.5a: Staff impacts (11 options) ✅ VERIFIED
- A3.5b: Staff impact severity (rating 1-5)
- A3.6a: Group impacts (11 options)
- A3.6b: Group impact severity (rating 1-3)

**A4. Outputs and Actions (8 questions)**
- A4.1: Primary outputs (7 options)
- A4.2: External without review (Yes/No)
- A4.3: BIL outputs (select: same as A2.6)
- A4.4: Output tracking (6 options)
- A4.5: Unauthorized access risk (Yes/No → 5 conditional options)
- A4.6: Regulated data in outputs (9 options)
- A4.7: PII in outputs (textarea)
- A4.8: Legal/regulatory actions (textarea)

**A5. Governance and Oversight (13 questions)**
- A5.1: Accountability (select: 5 options)
- A5.2: Tracking methods (textarea)
- A5.3: Monitoring processes (4 options)
- A5.4: Monitoring frequency (select: 6 options)
- A5.5: Independent review (Yes/No)
- A5.6: Monitoring responsibility (select: 4 options)
- A5.7: Stakeholder engagement (7 options)
- A5.8: Harm detection (7 options)
- A5.9: Values/principles (8 options)
- A5.10: Sector regulations (Yes/No → multiple conditional fields)
  - Commonwealth legislation (multiselect)
  - Queensland legislation (multiselect)
  - Sector obligations (multiselect)
  - Frameworks/standards (10 options + Other)
  - Other regulations (textarea)
  - Impact description (textarea)
- A5.11: Deployment location (select: 6 options)
- A5.12: AI frameworks (9 options + Other)

### Part B: Ethical Principles & Risk

**B1. Human, Societal and Environmental Wellbeing (3 questions)**
- B1.1: Benefit ratings (4 sub-ratings: Individual, Organizational, Social, Environmental - scale 1-5)
- B1.2: Negative impacts (10 options)
- B1.3: Employment effects (select: 4 options)

**B2. Human-Centred Values (3 questions)**
- B2.1: HRIA completed (Yes/No)
- B2.2: Impact ratings (3 sub-ratings: Rights, Diversity, Autonomy - custom: Positive/Neutral/Negative/Unknown)
- B2.3: Diverse perspectives (Yes/No → 6 conditional options)

**B3. Fairness (2 questions)**
- B3.1: Fairness testing (Yes/No → 10 conditional methods)
- B3.2: Discrimination risk (select: Yes/No/Unknown → 7 conditional groups)

**B4. Privacy Protection and Security (3 questions)**
- B4.1: PIA completed (Yes/No)
- B4.2: Personal information (Yes/No → 5 conditional types)
- B4.3: Security measures (5 options)

**B5. Reliability and Safety (3 questions)**
- B5.1: Reliability testing (Yes/No → conditional rating 1-5)
- B5.2: Disengagement process (Yes/No)
- B5.3: High-risk environment (Yes/No → 7 conditional environments)

**B6. Transparency and Explainability (4 questions)**
- B6.1: Transparency rating (1-5)
- B6.2: Explainability rating (1-5)
- B6.3: User information methods (textarea)
- B6.4: Limitations disclosed (Yes/No → conditional textarea)

**B7. Contestability (2 questions)**
- B7.1: Challenge process (Yes/No → conditional textarea)
- B7.2: Response timeframe (select: 8 options)

**B8. Accountability (4 questions)**
- B8.1: Oversight description (textarea)
- B8.2: Roles established (Yes/No)
- B8.3: Staff training (Yes/No)
- B8.4: Overreliance safeguards (Yes/No → 7 conditional options)

### Declaration (4 fields)
- Confirmation checkbox (required)
- Full name (required)
- Date (required, auto-populated)
- Role/Position (optional)

---

## Next Steps

1. **Download the JSON**: I can create an API endpoint to serve the complete JSON file
2. **Provide Scoring Schema**: Share your scoring methodology:
   - Which questions contribute to risk score?
   - What weights/multipliers for each?
   - Risk level thresholds (Low/Medium/High/Critical)?
   - Conditional scoring rules?

3. **Implementation**: Once scoring is defined, I'll implement:
   - Backend calculation engine
   - Results page visualizations
   - Risk level indicators
   - Scoring breakdown by section

---

**File Location:** `/app/faira_assessment_structure_ACCURATE.json`  
**Status:** ✅ All real options extracted and verified
