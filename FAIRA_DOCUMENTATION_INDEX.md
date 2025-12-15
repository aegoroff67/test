# FAIRA Assessment Documentation Index

## 📚 Complete Documentation Package

This directory contains comprehensive documentation for the FAIRA Risk Assessment scoring system, including all variables, domains, metrics, and scoring options.

---

## 📄 Document Files

### 1. **FAIRA_VARIABLES_COMPLETE_LIST.csv**
**Format:** CSV (Comma-Separated Values)  
**Purpose:** Machine-readable spreadsheet of all variables  
**Best for:** 
- Importing into Excel, Google Sheets, or database
- Data analysis and filtering
- Quick reference lookups

**Columns:**
- Question_ID
- Question_Text
- Type
- Domains
- Target_Metric
- Modifier_Type
- Special_Computation
- Options_Summary

**Total Records:** 62 questions

---

### 2. **FAIRA_VARIABLES_TABLE.md**
**Format:** Markdown with tables  
**Purpose:** Structured overview with tables and section breakdown  
**Best for:**
- GitHub/GitLab documentation
- Quick visual scanning
- Section-by-section review

**Contents:**
- Summary statistics
- Complete variable table
- Detailed breakdown by section (A1, A2, A3, A4, A5, B1-B8)

---

### 3. **FAIRA_COMPLETE_VARIABLE_DETAILS.md**
**Format:** Markdown with full details  
**Purpose:** Complete reference with all scoring options  
**Best for:**
- Understanding exact scoring logic
- Viewing all available options for each question
- Implementation reference

**Contents:**
- Full question text
- Question type and domains
- Target metrics
- **Complete scoring tables** for every option
- Rating scales
- Special computation formulas
- Notes and implementation guidance

---

### 4. **FAIRA_VARIABLE_REFERENCE.md**
**Format:** Markdown  
**Purpose:** Original comprehensive variable guide  
**Best for:**
- Detailed technical reference
- Formula developers
- System architects

**Contents:**
- All variables with metadata
- Scoring configurations
- Domain associations
- Notes and special cases

---

### 5. **FAIRA_SCHEMA_STATISTICS.md**
**Format:** Markdown with statistical analysis  
**Purpose:** Schema analytics and distribution data  
**Best for:**
- Understanding the assessment structure
- Domain coverage analysis
- Quality assurance

**Contents:**
- Questions by type (distribution)
- Target metrics distribution
- Domain usage statistics
- Modifier type breakdown
- Domain coverage analysis (which questions belong to which domains)

---

### 6. **DOMAIN_CORRECTION_SUMMARY.md**
**Format:** Markdown report  
**Purpose:** Documentation of the domain correction work  
**Best for:**
- Change tracking
- Quality assurance audit trail
- Understanding what was fixed

**Contents:**
- List of incorrect domains found
- Corrections made
- Validation results
- Impact assessment

---

## 🎯 Quick Reference Guide

### Need to...

| Task | Use This File |
|------|---------------|
| Import data into Excel/Sheets | `FAIRA_VARIABLES_COMPLETE_LIST.csv` |
| Browse all questions quickly | `FAIRA_VARIABLES_TABLE.md` |
| See exact scoring for a question | `FAIRA_COMPLETE_VARIABLE_DETAILS.md` |
| Understand domain distribution | `FAIRA_SCHEMA_STATISTICS.md` |
| Implement scoring logic | `FAIRA_COMPLETE_VARIABLE_DETAILS.md` |
| Define calculation formulas | `FAIRA_VARIABLE_REFERENCE.md` |
| Verify domain accuracy | `DOMAIN_CORRECTION_SUMMARY.md` |

---

## 📊 Summary Statistics

- **Total Questions:** 62
- **Schema Version:** 1.0
- **Sections:** 13 (A1-A5, B1-B8)
- **Official Domains:** 8
- **Total Domain References:** 90
- **Question Types:** 13 different types

### The 8 Official FAIRA Domains

1. ✅ **Human, Societal and Environmental Wellbeing**
2. ✅ **Human-centred Values**
3. ✅ **Fairness**
4. ✅ **Privacy Protection and Security**
5. ✅ **Reliability and Safety**
6. ✅ **Transparency and Explainability**
7. ✅ **Contestability**
8. ✅ **Accountability**

### Risk Calculation Formula

```
Raw Risk Score = (Total Impact × Total Likelihood) / Control Effectiveness
```

### Special Factors

- **AutonomyFactor:** Computed from A1.6 (autonomy level)
- **DataQualityFactor:** Computed from A2.5 (data quality ratings)
- **ExpertiseFactor:** Computed from A3.2 (user expertise levels)

---

## 🔍 Domain Distribution

| Domain | Questions | % |
|--------|-----------|---|
| Accountability | 30 | 48.4% |
| Transparency and Explainability | 15 | 24.2% |
| Reliability and Safety | 15 | 24.2% |
| Privacy Protection and Security | 12 | 19.4% |
| Fairness | 8 | 12.9% |
| Human-centred Values | 4 | 6.5% |
| Human, Societal and Environmental Wellbeing | 4 | 6.5% |
| Contestability | 2 | 3.2% |

---

## 📈 Target Metrics Breakdown

- **Control_Effectiveness:** 25 questions (40.3%)
- **Impact:** 23 questions (37.1%)
- **Likelihood:** 7 questions (11.3%)
- **Dual Metrics (Impact + Likelihood):** 2 questions (3.2%)
- **TBD (Text classification pending):** 3 questions (4.8%)

---

## 🔧 Source Files

### Schema Source
- **File:** `/app/backend/generate_faira_scoring_schema.py`
- **Purpose:** Python script that generates the schema
- **Status:** ✅ Corrected and validated

### Generated Schema
- **File:** `/app/backend/faira_scoring_schema.json`
- **Purpose:** Production-ready JSON schema
- **Status:** ✅ Validated (all 8 domains correct)
- **API Endpoint:** `GET /api/download-faira-structure`

---

## ✅ Validation Status

All domain data has been validated and verified:

- ✅ No invalid domains present
- ✅ All 8 official domains in use
- ✅ Correct casing (Human-centred Values)
- ✅ JSON schema valid and parseable
- ✅ API endpoint serving correct data

---

## 📝 Notes for Formula Development

When defining your risk calculation formulas, refer to:

1. **FAIRA_COMPLETE_VARIABLE_DETAILS.md** - For exact scoring values
2. **FAIRA_SCHEMA_STATISTICS.md** - For understanding which questions contribute to which metrics
3. The schema's `_meta` section for special factor formulas

### Questions with Special Computations:
- **A1.6** - AutonomyFactor (affects Likelihood)
- **A2.5** - DataQualityFactor (affects Likelihood)
- **A3.2** - ExpertiseFactor (affects Likelihood)

### Questions Pending LLM Classification (TBD):
- **A4.7** - PII access (text field)
- **A4.8** - Legal/regulatory triggers (text field)
- **A5.2** - Performance tracking method (text field)

---

**Last Updated:** December 2025  
**Schema Version:** 1.0  
**Documentation Status:** ✅ Complete and Validated
