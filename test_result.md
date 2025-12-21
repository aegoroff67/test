# Test Results - Framework Coverage Feature

## Test Scope
Testing the new Framework Coverage Overview page with real backend data integration.

## Test Cases

### 1. Backend API Endpoint
- Endpoint: `GET /api/assessments/{id}/framework-coverage`
- Returns framework coverage data with inherent and achieved percentages

### 2. Frontend Integration  
- Page: `/framework-coverage/{assessment_id}`
- Shows 8 framework cards with bar charts
- Greyed-out cards for unselected frameworks
- Real data from API displayed in charts

### 3. Key Scenarios to Test
- Assessment with some frameworks selected (ID: 96186862-9f7e-4699-96b4-009953ad285e)
  - NIST AI RMF should be active, others greyed out
- Assessment with all frameworks selected (ID: d7c2d829-554c-4354-9507-102823cc1601)
  - All 8 cards should be active with different data

## Test Credentials
- Email: andrew@test.com
- Password: password123
