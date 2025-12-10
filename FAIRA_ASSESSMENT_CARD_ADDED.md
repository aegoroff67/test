# FAIRA Risk Assessment Card Added

## Summary
Successfully added a 5th assessment type card to the Assessment Selector page for the new FAIRA (Foundational AI Risk Assessment) framework.

## Changes Made

### 1. File Modified: `/app/frontend/src/pages/AssessmentSelector.js`

### 2. Changes Implemented:

#### Icon Import
- Added `ShieldCheck` icon from lucide-react for the FAIRA card

#### Handler Function
- Created `handleFairaAssessment()` function that:
  - Creates a new assessment with type "FAIRA"
  - Navigates to `/assessment/{id}/faira-onboarding` page
  - Handles errors and displays appropriate toasts

#### Grid Layout Update
- Changed grid layout from 4 columns to 5 columns:
  - `md:grid-cols-2` → `lg:grid-cols-3` → `xl:grid-cols-5`

#### New Card Details:
- **Position**: 5th card (after AI System Maturity Assessment)
- **Title**: FAIRA Risk Assessment
- **Badge**: "New Assessment – Available Now" (orange theme)
- **Icon**: ShieldCheck (orange)
- **Color Theme**: Orange (`border-orange-500`, `bg-orange-600`)
- **Button Text**: "Start FAIRA Assessment"

#### Content:
- **Purpose**: Evaluate an AI solution using Queensland Government's Foundational AI Risk Assessment (FAIRA) framework. Identify risks across system components, values-based impacts, and governance obligations. Generate defence-ready documentation for assurance, procurement, and compliance activities.

- **Best for**: Government agencies, councils, universities, and vendors developing or supplying AI solutions to the Queensland Government — or any organisation requiring a structured, defensible AI risk assessment aligned to public-sector expectations.

- **Outcome**: A full FAIRA report including component analysis, values-based risk ratings, automated impact/likelihood scoring, and mapped mitigation controls from FAIRA Part C. Produces an audit-ready risk summary suitable for executive review, procurement assurance, and compliance documentation.

#### Permission Handling:
- Card respects user permissions via `hasAccess('faira')` check
- Shows "Requires Permission" badge if user lacks access
- Button is disabled for users without permission
- Displays appropriate error message when clicked without permission

## Visual Appearance
- Orange color scheme differentiates it from other assessment types:
  - Green: Awareness
  - Blue: Readiness  
  - Purple: Orgwide
  - Teal: System
  - **Orange: FAIRA** (NEW)

## Build Status
- ✅ Frontend build successful
- ✅ No compilation errors
- ✅ All existing functionality preserved

## Next Steps (Backend Work Required)
To make this fully functional, the backend needs to:
1. Support "FAIRA" as a valid assessment_type in the assessments API
2. Create FAIRA onboarding page route
3. Implement FAIRA-specific questions and domains
4. Create FAIRA report generation logic

## Testing Status
- Frontend component added successfully
- Build verified
- Backend integration pending
