# AM AI SAFE Assessment Platform - Product Requirements Document

## Original Problem Statement
Build a comprehensive AI assessment platform that generates detailed DOCX reports for "AI Awareness & Foundations" assessments. The platform includes:
1. Multiple assessment types (Awareness, Readiness, Org-wide, FAIRA, System)
2. AI-generated narrative sections for reports using GPT-4o-mini
3. Dynamic charts and visualizations (radar charts, bar charts)
4. User authentication and assessment management

## User Personas
- **Senior Leadership**: Need executive-level snapshots and insights
- **Compliance Teams**: Need detailed governance and risk assessments
- **IT/Digital Teams**: Need readiness and technical capability assessments

## Core Requirements

### Assessment Types
- [x] Awareness Assessment
- [x] Readiness Assessment (template fallback)
- [x] Org-wide Assessment (template fallback)
- [x] FAIRA Assessment (template fallback)
- [x] System Assessment

### DOCX Report Generation
- [x] Template-based generation using docxtpl
- [x] AI-generated narratives (6 sections for Awareness)
- [x] Dynamic domain tables
- [x] Radar chart visualization
- [x] Stacked bar chart image
- [x] Sector benchmark comparison

### AI Narratives (Awareness Report)
- [x] executive_snapshot
- [x] context_interpretation
- [x] governance_interpretation
- [x] readiness_interpretation
- [x] domain_patterns
- [x] action_interpretation
- [x] next_focus statement

## What's Been Implemented

### January 17, 2026
- **AI Readiness Template Variables Completed**:
  - Added `readiness_bar_image` generation (stacked bar chart showing tier and score)
  - Fixed domain mapping for 8 Readiness domains (SA, GF, DR, TI, PC, PR, RE, CL)
  - Implemented `q.selected_option_text` mapping to full answer text from options
  - Added `questions` list with full details for Readiness reports (48 questions)
  - Implemented `results_summary_text` for Readiness assessments
  - Fixed domain code mapping (PC→People & Culture, PR→Policy & Compliance Readiness)

### January 11, 2026
- **Template v0.9.10 Integration**: Successfully configured and verified
- **All 6 AI Narratives**: Working and rendering correctly in DOCX
- **Domain-Level Overview Table**: Properly displays domain names, tiers, and scores
- **Template Variable Escaping**: Ampersands (`&`) properly escaped as `&amp;`
- **Bug Fix: AI Tier "Unknown"**: Fixed missing `overall_tier` in summary_data
- **Added Awareness-specific tier calculation**: Established/Developing/Emerging/Introductory (86/66/41/0%)

### Previous Work
- Full authentication system (JWT-based)
- Assessment CRUD operations
- Evidence management system
- Frontend Results page with report download
- Framework alignment data for Australian Guidance

## Known Issues

### P1 - High Priority
- Sector benchmark radar chart needs verification

### P2 - Medium Priority
- Evidence API CRUD needs test coverage

### P3 - Lower Priority
- SU-1 question missing from Australian Guidance alignment data
- FairaAssessmentForm.js sidebar scroll-to-section needs verification

## Prioritized Backlog

### P0 - Critical (Completed)
- [x] Awareness DOCX report generation with AI narratives
- [x] AI Readiness template variables (readiness_bar_image, domain mappings, q.selected_option_text)

### P1 - High Priority
- [ ] Frontend toggle for `show_detailed_responses` parameter
- [ ] Verify sector benchmark radar chart in reports
- [ ] Create DOCX templates for Org-wide, FAIRA

### P2 - Medium Priority
- [ ] Test Evidence API CRUD endpoints
- [ ] Coverage Gap Report feature
- [ ] Print-specific CSS layout for ResultsPage

### P3 - Lower Priority
- [ ] Fix SU-1 question in alignment data
- [ ] Verify sidebar scroll-to-section in FAIRA form
- [ ] Refactor report_generator.py (currently monolithic)

### P4 - Future
- [ ] Enterprise SSO (SAML/OIDC)
- [ ] Stripe paywall for premium assessments

## Technical Architecture

### Backend
- FastAPI (Python)
- MongoDB for data persistence
- docxtpl for DOCX generation
- matplotlib for chart generation
- emergentintegrations for OpenAI GPT-4o-mini

### Frontend
- React with Tailwind CSS
- Shadcn UI components
- Results page with report download

### Key Files
- `/app/backend/report_generator.py` - Main report generation logic
- `/app/backend/templates/docx/` - DOCX templates
- `/app/frontend/src/pages/ResultsPage.js` - Report download UI

## Test Credentials
- Email: andrew@test.com
- Password: password123
