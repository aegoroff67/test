# FAIRA Framework Removed from AI System Maturity Assessment

## Summary
Removed all references to the FAIRA (Foundational AI Risk Assessment Framework) from the AI System Maturity Assessment flow, including the pre-assessment onboarding form, question badges, and framework alignment selector.

## Changes Made

### 1. SystemPreAssessmentForm.js
**File**: `/app/frontend/src/pages/SystemPreAssessmentForm.js`

**Removed:**
- FAIRA option from the `FRAMEWORKS` array in "Applicable frameworks / standards" section
- Import for `FairaOnboardingPanel` component
- `isFairaSelected` conditional check
- `FairaOnboardingPanel` component rendering
- FAIRA data structure from `defaultState.faira`
- `updateFaira()` and `toggleFairaArray()` helper functions

**Impact:**
- Users can no longer select FAIRA framework in the System Assessment onboarding
- FAIRA Components panel no longer appears
- FAIRA-specific data fields removed from form state

### 2. AssessmentPage.js
**File**: `/app/frontend/src/pages/AssessmentPage.js`

**Removed:**
- Import for `fairaAlignmentData.json`
- Import for `FairaAlignmentModal` component
- FAIRA entry from `FRAMEWORK_CONFIG` object
- `faira: false` from `selectedFrameworks` state initialization
- FAIRA framework check from `setSelectedFrameworks()` in `fetchAssessment()`
- FAIRA alignment badge rendering code for questions (lines 872-885)

**Impact:**
- FAIRA badges no longer appear on assessment questions
- FAIRA modal cannot be opened from question badges
- FAIRA framework not tracked in assessment state

### 3. AssessmentFrameworkView.js
**File**: `/app/frontend/src/components/AssessmentFrameworkView.js`

**Removed:**
- Import for `fairaAlignmentData.json`
- FAIRA entry from `FRAMEWORKS` array configuration

**Impact:**
- "FAIRA (QLD) (2024)" option removed from framework selector dropdown
- Users cannot view FAIRA alignment in the Framework Alignment page

## Framework Display Order (Before vs After)

### Before (with FAIRA):
1. ISO/IEC 42001 (2023)
2. Australian AI Ethics Principles (2024)
3. Australian Guidance for AI Adoption (2025)
4. AU National Framework for the Assurance of AI in Gov (2024)
5. EU AI Act (2024)
6. **FAIRA (QLD) (2024)** ❌
7. NIST AI RMF (2023)
8. OECD Principles (2019)
9. Singapore MAF (2024)

### After (FAIRA removed):
1. ISO/IEC 42001 (2023)
2. Australian AI Ethics Principles (2024)
3. Australian Guidance for AI Adoption (2025)
4. AU National Framework for the Assurance of AI in Gov (2024)
5. EU AI Act (2024)
6. NIST AI RMF (2023)
7. OECD Principles (2019)
8. Singapore MAF (2024)

## Build Status
- ✅ Frontend build successful
- ✅ File size reduced from 436.16 kB to 422.42 kB (13.74 kB saved)
- ✅ No compilation errors
- ✅ All FAIRA references cleanly removed

## Testing Checklist
- [ ] System Assessment onboarding form no longer shows FAIRA option
- [ ] FAIRA Components panel does not appear during onboarding
- [ ] Assessment questions do not show FAIRA alignment badges
- [ ] Framework Alignment page selector does not include FAIRA
- [ ] No console errors related to FAIRA data or components

## Related Changes
This change is separate from the FAIRA Risk Assessment feature, which was added as a standalone 5th assessment type in the Assessment Selector page. The FAIRA Risk Assessment remains available as its own dedicated assessment flow.

## Notes
- The FAIRA data files (`fairaAlignmentData.json`) and component (`FairaAlignmentModal.js`) still exist in the codebase but are no longer imported or used in System Assessment
- This removal only affects the AI System Maturity Assessment workflow
- The separate FAIRA Risk Assessment remains fully functional
