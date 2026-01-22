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

#### Report Types - ALL FUNCTIONAL
- **AI Awareness Report** - Fully functional with AI narratives, bar charts
- **AI Readiness Report** - Fully functional with v0.08 template
- **Org-wide Report** - Fully functional with v0.06 template, 8 AI narratives
- **AI System Maturity Report** - ✅ COMPLETED with v0.15 template, 8 AI narratives

#### System Report Features (Latest Fix - 2026-01-22)
- **Heatmap Bug Fixed**: Removed `ax.set_aspect('equal')` that was causing the heatmap to render as a square image (aspect ~0.93) instead of wide (aspect ~1.5)
- Results Summary text matching frontend
- Bar chart image (`readiness_bar_image`)
- Radar chart with correct sector benchmarks
- Sector-specific action recommendations (5 per priority level)
- Appendix A with 88 detailed question responses
- All 8 AI-generated narratives

#### Key Features
- Jinja2 template rendering with docxtpl
- AI narrative generation (8 narratives per report type)
- Sector-specific action recommendations (high/medium/low priority)
- Domain score tables with maturity tiers
- Heatmap and radar chart generation
- Framework alignment data
- Benchmark comparison with sector-specific data

#### Template Versions
- Awareness: Default template
- Readiness: `AM_AI_SAFE_Readiness_Report_TEMPLATE_v0.08_20260118_FINAL.docx`
- Orgwide: `AM_AI_SAFE_Organisation_Report_TEMPLATE_v0.06_20260121.docx`
- System: `AM_AI_SAFE_System_Report_TEMPLATE_v0.15_20260122.docx`

---

## Prioritized Backlog

### P0 - Critical
- [x] **Refactor `report_generator.py`** - COMPLETE ✅
  - Original: 8,359 lines → Now: 5,394 lines (35% reduction)
  - Extracted to `/app/backend/report_modules/`:
    - `charts.py`: 493 lines (heatmap, bar, radar charts)
    - `ai_narratives.py`: 1,167 lines (all 4 assessment types)
    - `utils.py`: 209 lines (formatting, utilities)
  - Total modular code: 1,893 lines

### P1 - High Priority
- [ ] Frontend toggle for `show_detailed_responses` parameter on Results page
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
- `/app/backend/report_generator.py` - Main report generation (5,394 lines - refactored)
- `/app/backend/report_modules/` - Modular components:
  - `ai_narratives.py` - AI narrative generation for all 4 assessment types (1,167 lines)
  - `charts.py` - Chart generation: heatmap, bar, radar (493 lines)
  - `utils.py` - Formatting, tier calculations, utilities (209 lines)
- `/app/backend/server.py` - FastAPI endpoints
- `/app/backend/templates/docx/` - DOCX templates
- `/app/backend/ai_maturity_benchmarks_SYSTEM.json` - System benchmark data
- `/app/backend/awareness_benchmarks.json` - Awareness benchmark data
- `/app/backend/orgwide_benchmarks.json` - Orgwide benchmark data
- `/app/backend/readiness_benchmarks.json` - Readiness benchmark data

### Frontend
- `/app/frontend/src/pages/ResultsPage.js` - Assessment results display
- `/app/frontend/src/pages/SystemPreAssessmentForm.js` - System pre-assessment form
- `/app/frontend/src/pages/FrameworkCoveragePage.js` - Framework coverage view

---

## API Endpoints

### Report Generation
- `GET /api/assessments/{assessment_id}/report` - Generate DOCX report
  - Query params: `view_type`, `use_ai`, `show_detailed_responses`

### Framework Coverage
- `GET /api/assessments/{assessment_id}/framework-coverage` - Get framework coverage analytics

### Schema
- `GET /api/schema/system-preassessment-form` - System pre-assessment JSON schema

---

## Template Variables (System Report)

### Key Variables
- `{{org_name}}` - Organization name
- `{{system_name}}` - AI system name
- `{{overall.score}}` - Overall maturity score
- `{{overall.tier}}` - Maturity tier (Leading/Established/Developing/Foundational)
- `{{results_summary_text}}` - Pre-formatted results summary
- `{{readiness_bar_image}}` - Bar chart image
- `{{radar_chart_image}}` - Radar chart with benchmarks
- `{{heatmap_image}}` - Domain heatmap

### Actions
- `{{sector_actions_high_top5}}` - Top 5 high priority actions
- `{{sector_actions_medium_top5}}` - Top 5 medium priority actions
- `{{sector_actions_low_top5}}` - Top 5 low priority actions

### AI Narratives (ai.s_*)
- `{{ai.s_executive_snapshot}}`
- `{{ai.s_gov_oversight}}`
- `{{ai.s_data_privacy_security}}`
- `{{ai.s_reliability_safety_performance}}`
- `{{ai.s_transparency_explainability_contestability}}`
- `{{ai.s_fairness_bias_inclusivity}}`
- `{{ai.s_domain_patterns}}`
- `{{ai.s_pathway_rationale}}`

### Appendix
- `{{questions}}` - List of 88 questions with details
- `{{show_detailed_responses}}` - Toggle for appendix

---

## Test Credentials
- Email: `andrew@test.com`
- Password: `password123`

## Database
- Name: `am_ai_safe_db`
- Key collections: `assessments`, `users`, `organizations`, `questions`, `domains`
