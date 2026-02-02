# AM AI SAFE - AI Maturity & Risk Assessment Platform

## Original Problem Statement
Build a full-stack application for managing and generating AI maturity and risk assessment reports. The platform supports multiple assessment types (Awareness, Readiness, System, Orgwide, FAIRA) with DOCX/PDF report generation.

## Architecture
```
/app/
├── backend/
│   ├── server.py               # FastAPI main app
│   ├── report_generator.py     # DOCX/PDF generation (docxtpl)
│   ├── faira_scoring_engine.py # FAIRA risk calculations
│   ├── report_modules/
│   │   ├── charts.py           # Chart generation
│   │   ├── utils.py            # Utility functions
│   │   └── ai_narratives.py    # AI narrative generation
│   └── templates/docx/         # DOCX templates
└── frontend/
    └── src/
        └── pages/              # React pages
```

## What's Been Implemented

### 2025-02-02 - FAIRA Gaps Table Bug Fix
**Status: FIXED (Pending User Validation)**
- Root cause: `faira_risk_summary` only calculated when `use_ai=True`
- Fix: Added explicit FAIRA calculation block in `generate_report_for_assessment` (line 5536-5570)
- Now calculates `faira_risk_summary` for ALL FAIRA assessments regardless of `use_ai` flag

### Previous Work
- FAIRA template debugging (v0.37 to v0.46) - RESOLVED
- Ampersand handling in reports - FIXED
- Declaration field autofill removal - DONE
- FAIRA domain name capitalization in AI narratives - DONE
- Debug endpoints created: `/api/debug/template-check/{type}`, `/api/debug/gaps-data/{id}`

## Prioritized Backlog

### P0 (Critical)
- ✅ ~~FAIRA gaps table empty~~ - Fixed 2025-02-02

### P1 (High)
- [ ] Clarify B7.2 question type (radio vs dropdown)
- [ ] Implement `report_downloaded` logging event
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

## Key Endpoints
- `GET /api/assessments/{id}/report` - Generate DOCX report
- `GET /api/debug/template-check/{type}` - Check template structure
- `GET /api/debug/gaps-data/{id}` - Inspect assessment data

## Test Credentials
- User: `andrew@test.com`
- Password: `password123`

## 3rd Party Integrations
- OpenAI GPT-4o-mini (via Emergent LLM Key)
- docxtpl (DOCX templating)
- matplotlib (charts)
- WeasyPrint (PDF)
- Playwright (PDF generation)

## Known Issues
- Debug endpoints are public (should be secured in production)
- DOCX template fragility - strict authoring guidelines recommended
