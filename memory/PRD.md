# AM AI SAFE - AI Maturity & Risk Assessment Platform

## Original Problem Statement
Build a full-stack application for managing and generating AI maturity and risk assessment reports. The platform supports multiple assessment types (Awareness, Readiness, System, Orgwide, FAIRA) with DOCX/PDF report generation.

## Architecture
```
/app/
├── backend/
│   ├── server.py               # FastAPI main app with debug endpoints
│   ├── report_generator.py     # DOCX/PDF generation (docxtpl)
│   ├── faira_scoring_engine.py # FAIRA risk calculations
│   ├── report_modules/
│   │   ├── charts.py           # Chart generation
│   │   ├── utils.py            # Utility functions
│   │   └── ai_narratives.py    # AI narrative generation
│   └── templates/docx/         # DOCX templates
│       └── AM_AI_SAFE_FAIRA_Report_TEMPLATE_v0.47_20260202.docx  # Current FAIRA template
└── frontend/
    └── src/
        └── pages/              # React pages
```

## What's Been Implemented

### 2026-02-03 - AEST Timezone for Audit Logs ✅
**Status: IMPLEMENTED**
- Modified `logging_service.py` to add `timestamp_aest` field to all audit log entries
- UTC timestamp retained for database consistency, AEST provided for human readability
- AEST = UTC+10 (Australian Eastern Standard Time)
- Format: ISO 8601 with timezone offset (e.g., `2026-02-03T16:40:35.538387+10:00`)

### 2025-02-02 - Report Downloaded Logging ✅
**Status: IMPLEMENTED**
- Added `report_downloaded` audit and analytics logging to all report endpoints:
  - DOCX Report endpoint
  - Executive Summary PDF endpoint
  - FAIRA Results Summary PDF endpoint
  - Framework Coverage PDF endpoint
- Each log captures: user, timestamp, assessment details, file size, report type

### 2025-02-02 - FAIRA Gaps Table Bug FIXED ✅
**Status: RESOLVED**
- **Root Cause**: `_populate_recommendation_tables()` was overwriting the gaps table after Jinja2 rendering
- **Fix 1**: Added FAIRA-specific skip for programmatic table population (line ~4860 in report_generator.py)
- **Fix 2**: Template updated to use `{{gap_1.domain}}`, `{{gap_2.domain}}`, `{{gap_3.domain}}` instead of `{%tr for gap in gaps %}` loop
- **Template**: Updated to v0.47 with new gap variable structure
- **Verified**: Debug endpoint confirms gaps table now shows Reliability, Privacy, Accountability with all data

### Previous Work
- FAIRA template debugging (v0.37 to v0.47) - RESOLVED
- Ampersand handling in reports - FIXED
- Declaration field autofill removal - DONE
- FAIRA domain name capitalization in AI narratives - DONE
- Debug endpoints created for remote diagnosis

## Debug Endpoints (for troubleshooting)
- `GET /api/debug/template-check/{assessment_type}` - Check template structure
- `GET /api/debug/gaps-data/{assessment_id}` - Inspect assessment data and test on-the-fly calculation
- `GET /api/debug/generate-test-report/{assessment_id}` - Test template rendering
- `GET /api/debug/full-report-test/{assessment_id}` - Full report generation with diagnostics
- `GET /api/debug/download-test-report/{assessment_id}` - Download test report

## Prioritized Backlog

### P0 (Critical)
- ✅ ~~FAIRA gaps table empty~~ - Fixed 2025-02-02
- ✅ ~~AEST timezone for logging~~ - Fixed 2026-02-03

### P1 (High)
- ✅ ~~Implement `report_downloaded` logging event~~ - Done
- [ ] Clarify B7.2 question type (radio vs dropdown)
- [ ] Test backend CRUD API for evidence object

### P2 (Medium)
- [ ] Verify FAIRA assessment score (88.9 vs user-recalled 81)
- [ ] In-app walkthroughs (React Joyride)

### P3 (Low)
- [ ] Verify sector benchmark radar chart in Awareness DOCX
- [ ] Sidebar scroll-to-section verification in FairaResultsPage.js
- [ ] `SU-1` question from Australian Guidance framework missing

### Future
- Coverage Gap Report feature
- Print-specific multi-page CSS layout
- "Upgrade to Unlock" button workflow
- Enterprise SSO (SAML/OIDC)
- Stripe paywall for premium assessments
- Enhanced logging with performance metrics

## Key Technical Insights

### FAIRA Report Generation
- Template uses `{{gap_1.domain}}`, `{{gap_2.domain}}`, `{{gap_3.domain}}` (NOT loop-based)
- `_populate_recommendation_tables()` must be SKIPPED for FAIRA to avoid overwriting gaps table
- DotDict class provides dot-notation access for template variables
- Risk calculation done on-the-fly via `calculate_overall_risk()` if not stored in assessment

### Template Variable Flow
1. `generate_report_for_assessment()` calculates `faira_risk_summary`
2. `_transform_assessment_data()` passes it to `report_data`
3. `_generate_docx_report()` builds `template_context` with `gap_1`, `gap_2`, `gap_3`
4. `doc.render()` processes template
5. Post-processing must NOT touch gaps table for FAIRA

## Test Credentials
- User: `andrew@test.com`
- Password: `password123`

## 3rd Party Integrations
- OpenAI GPT-4o-mini (via Emergent LLM Key)
- docxtpl (DOCX templating)
- matplotlib (charts)
- WeasyPrint (PDF)
- Playwright (PDF generation)

## Known Issues / Technical Debt
- Debug endpoints are public (should be secured in production)
- DOCX template structure is sensitive to table ordering
- Multiple fallback mechanisms for gap data (could be simplified)
