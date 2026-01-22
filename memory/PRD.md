# AM AI SAFE Assessment Platform - PRD

## Original Problem Statement
Create and debug detailed DOCX reports for four distinct assessment types:
- AI Awareness & Foundations
- AI Readiness  
- Org-wide Assessment
- AI System Maturity

This involves iteratively debugging user-provided DOCX templates, fixing complex Jinja2 syntax and rendering issues, and implementing the entire backend data pipeline in `report_generator.py`.

## User Personas
- **Assessors**: Conduct AI maturity assessments for organizations
- **Organization Admins**: Review and manage assessment results
- **Executives**: Consume high-level reports on AI maturity

## Core Requirements

### Report Generation
1. DOCX report generation for all 4 assessment types
2. AI-generated narrative sections using GPT-4o-mini
3. Dynamic charts (heatmaps, bar charts, radar charts)
4. Sector-specific benchmarking and recommendations
5. Detailed question-level response appendix (optional)

### Tech Stack
- Frontend: React
- Backend: FastAPI (Python)
- Database: MongoDB (`am_ai_safe_db`)
- AI: OpenAI GPT-4o-mini via Emergent LLM Key
- Templates: docxtpl + python-docx

---

## What's Been Implemented

### ✅ Completed (as of 2026-01-22)

#### Report Types
- **AI Awareness Report** - Fully functional with AI narratives, bar charts
- **AI Readiness Report** - Fully functional with v0.08 template
- **Org-wide Report** - Fully functional with v0.06 template, 8 AI narratives
- **AI System Maturity Report** - ✅ COMPLETED with v0.04 template, 8 AI narratives

#### Key Features
- Jinja2 template rendering with docxtpl
- AI narrative generation (8 narratives per report type)
- Sector-specific action recommendations (high/medium/low priority)
- Domain score tables with maturity tiers
- Heatmap and radar chart generation
- Framework alignment data
- Benchmark comparison (when available)

#### Template Versions
- Awareness: Default template
- Readiness: `AM_AI_SAFE_Readiness_Report_TEMPLATE_v0.08_20260118_FINAL.docx`
- Orgwide: `AM_AI_SAFE_Organisation_Report_TEMPLATE_v0.06_20260121.docx`
- System: `AM_AI_SAFE_System_Report_TEMPLATE_v0.04_FIXED.docx`

---

## Prioritized Backlog

### P0 - Critical
- [ ] **Refactor `report_generator.py`** - Currently ~7500+ lines, needs modularization

### P1 - High Priority
- [ ] Frontend toggle for `show_detailed_responses` parameter on Results page
- [ ] Verify sector benchmark radar chart in Awareness report
- [ ] FAIRA assessment DOCX templates

### P2 - Medium Priority
- [ ] Test backend CRUD API endpoints for `evidence` object
- [ ] "Coverage Gap Report" feature
- [ ] Print-specific multi-page CSS layout for ResultsPage.js

### P3 - Lower Priority
- [ ] Fix missing `SU-1` question from Australian Guidance framework
- [ ] Verify sidebar scroll-to-section in FairaAssessmentForm.js

### P4 - Future
- [ ] Enterprise SSO (SAML/OIDC)
- [ ] Stripe paywall for premium assessments

---

## Key Files Reference

### Backend
- `/app/backend/report_generator.py` - Main report generation logic (MONOLITHIC - needs refactor)
- `/app/backend/server.py` - FastAPI endpoints
- `/app/backend/templates/docx/` - DOCX templates

### Frontend
- `/app/frontend/src/pages/ResultsPage.js` - Assessment results display
- `/app/frontend/src/pages/SystemPreAssessmentForm.js` - System pre-assessment form

---

## API Endpoints

### Report Generation
- `GET /api/assessments/{assessment_id}/report` - Generate DOCX report
  - Query params: `view_type`, `use_ai`, `show_detailed_responses`

### Schema
- `GET /api/schema/system-preassessment-form` - System pre-assessment JSON schema

---

## Test Credentials
- Email: `andrew@test.com`
- Password: `password123`

## Database
- Name: `am_ai_safe_db`
- Key collections: `assessments`, `users`, `organizations`, `questions`, `domains`
