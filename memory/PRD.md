# AM AI SAFE - AI Maturity & Risk Assessment Platform

## Original Problem Statement
Build a full-stack application for managing and generating AI maturity and risk assessment reports. The platform supports multiple assessment types (Awareness, Readiness, Orgwide, System, FAIRA) with comprehensive DOCX/PDF report generation, tier-based user access control, and detailed logging.

## Core Requirements
1. Multi-type AI assessments with scoring engines
2. DOCX/PDF report generation with customizable templates
3. User authentication and organization-based multi-tenancy
4. Super Admin cross-tenant access
5. Comprehensive audit logging
6. AI-enhanced narrative generation (optional)

## Technology Stack
- **Frontend**: React with Shadcn/UI components
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Report Generation**: docxtpl, python-docx, WeasyPrint
- **AI Integration**: OpenAI GPT-4o-mini via Emergent LLM Key

---

## Completed Work (as of 2025-02-01)

### Session 1 - Initial Build
- Full-stack application architecture
- Assessment form components for all types
- Report generation system with DOCX/PDF support
- User management with roles

### Session 2 - FAIRA & Permissions
- FAIRA assessment progress calculation bug fix
- Super Admin permissions for cross-tenant access (logs, assessments)
- Gap analysis logic for FAIRA reports
- Application timezone configuration (default: Australia/Brisbane)
- UI/Schema text casing fixes (AI, API, FAQ uppercase)
- User management UI improvements

### Session 3 - Ampersand & Gaps Debug
- **Fixed**: Ampersand stripping in DOCX reports
  - Updated `_post_process_ampersands()` to re-escape bare `&` characters after Jinja2 rendering
- **Enhanced**: Debug logging for FAIRA gaps variable
  - Added pre-render logging to confirm gaps list population

---

## Pending Issues (Priority Order)

### P0 - Critical
- None currently

### P1 - High
- Question B7.2: Clarify if radio should be dropdown

### P2 - Medium
- FAIRA score discrepancy: 88.9 vs 81 user-recalled value

### P3-P6 - Low
- Verify sector benchmark radar chart in Awareness report
- Test evidence CRUD API endpoints
- Add missing SU-1 question from Australian Guidance framework
- Verify sidebar scroll-to-section in FairaResultsPage

---

## Upcoming Tasks

### Phase 1 - Logging & UX
- Implement `report_downloaded` logging event
- In-app walkthroughs (React Joyride)

### Phase 2 - Features
- Coverage Gap Report feature
- Print-specific multi-page CSS layout for ResultsPage

---

## Future/Backlog

- "Upgrade to Unlock" button workflow (currently UI-only/MOCKED)
- Enterprise SSO (SAML/OIDC)
- Stripe paywall for premium assessments
- Enhanced logging with performance metrics
- Real-time alerts

---

## Key Files

| File | Purpose |
|------|---------|
| `/app/backend/report_generator.py` | Main report generation logic |
| `/app/backend/server.py` | FastAPI endpoints (monolithic, needs refactoring) |
| `/app/backend/faira_scoring_engine.py` | FAIRA risk calculation |
| `/app/backend/templates/docx/` | DOCX report templates |
| `/app/frontend/src/pages/FairaAssessmentForm.js` | FAIRA form component |

---

## Test Credentials
- **User**: andrew@test.com
- **Password**: password123

---

## Notes
- `server.py` remains monolithic and needs refactoring into separate route files
- The "Upgrade to Unlock" button on the assessment selector page is MOCKED (UI-only)
