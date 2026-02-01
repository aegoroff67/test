# AM AI SAFE - AI Maturity & Risk Assessment Platform

## Original Problem Statement
Build a full-stack application for managing and generating AI maturity and risk assessment reports. The platform supports multiple assessment types (Awareness, Readiness, Orgwide, System, FAIRA) with DOCX and PDF report generation capabilities.

## Core Requirements
- Multi-type AI assessments (Awareness, Readiness, Orgwide, System, FAIRA)
- DOCX report generation using templates with docxtpl
- PDF report generation (WeasyPrint or LibreOffice fallback)
- AI-powered narrative generation for reports
- Benchmark comparisons by sector
- Gap analysis and recommendations

## Architecture

### Backend (FastAPI)
- `/app/backend/server.py` - Main FastAPI application
- `/app/backend/report_generator.py` - DOCX/PDF report generation
- `/app/backend/faira_scoring_engine.py` - FAIRA risk calculations
- `/app/backend/templates/docx/` - DOCX templates

### Frontend (React)
- `/app/frontend/src/pages/` - Page components
- `/app/frontend/src/components/ui/` - Shadcn UI components

### Database
- MongoDB via `MONGO_URL` environment variable

## What's Been Implemented

### 2025-02-01: P0 Bug Fix - FAIRA Gaps Table
- **Issue**: Gaps analysis table empty in FAIRA DOCX reports
- **Root Cause**: Template had `{%tr for...%}` and `{%tr endfor %}` in same row, breaking docxtpl's regex processing
- **Fix**: Restructured template to have each `{%tr}` tag in separate table rows
- **Also Fixed**: 8 broken Jinja variable tags with split XML formatting

## Pending Issues

### P1 - High Priority
- [ ] Question B7.2 - Clarify radio vs dropdown selection
- [ ] Implement `report_downloaded` logging event

### P2 - Medium Priority
- [ ] FAIRa assessment score discrepancy (88.9 vs reported 81)
- [ ] Test backend CRUD API endpoints for `evidence` object

### P3 - Low Priority
- [ ] Verify sector benchmark radar chart in Awareness DOCX report
- [ ] Missing SU-1 question from Australian Guidance alignment data
- [ ] Verify sidebar scroll-to-section in FairaResultsPage.js

## Backlog / Future Tasks
- In-app walkthroughs (React Joyride)
- Coverage Gap Report feature
- Print-specific multi-page CSS layout for ResultsPage.js
- Upgrade to Unlock button workflow
- Enterprise SSO (SAML/OIDC)
- Stripe paywall for premium assessments
- Performance metrics and real-time alerts for logging

## Key Technical Notes

### docxtpl {%tr} Syntax
- Each `{%tr}` tag must be in its own separate `<w:tr>` element
- Do NOT put `{%tr for...%}` and `{%tr endfor %}` in the same table row
- Working structure:
  ```
  Row 1: {%tr for item in items %}
  Row 2: {{item.field1}} | {{item.field2}}
  Row 3: {%tr endfor %}
  ```

### Template Files
- FAIRA: `AM_AI_SAFE_FAIRA_Report_TEMPLATE_v0.37_20260131.docx`
- System: `AM_AI_SAFE_System_Report_TEMPLATE_v0.15_20260122.docx`
- Awareness: `AM_AI_SAFE_Awareness_Report_TEMPLATE_v0.9.34_20260117.docx`

## Test Credentials (Preview Environment)
- Email: andrew@test.com
- Password: password123

## 3rd Party Integrations
- OpenAI GPT-4o-mini (via Emergent LLM Key)
- matplotlib for charts
- docxtpl for DOCX generation
- WeasyPrint for PDF generation
