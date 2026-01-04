# Test Result Document

## Current Test Scope
Testing the "Top 3 Action Steps" feature for AI System Maturity Assessment with prioritization toggle

## Test Requirements
1. Backend API endpoint `/api/system/action-steps/{sector}` returns sector-specific action steps
2. Frontend fetches action steps when viewing System assessment results
3. Toggle button allows switching between "Smart Priority" and "Domain Score" prioritization
4. Smart Priority shows Quick Win badges, impact/effort scores
5. Domain Score shows standard domain-based prioritization

## Test Credentials
- Email: andrew@test.com
- Password: password123

## Test Steps
1. Login with test credentials
2. Navigate to an existing completed System assessment
3. Verify the "Top 3 Action Steps" section appears with the toggle
4. Test toggling between "Smart Priority" and "Domain Score"
5. Verify Smart Priority shows:
   - Quick Win / Strategic / Opportunistic badges
   - Impact, Effort, and Gap metrics
6. Verify Domain Score shows standard prioritization

## Expected Results
- Toggle should switch between two prioritization modes
- Smart Priority shows additional metadata (quadrant badges, impact/effort scores)
- Domain Score shows simpler display without the extra metadata

## Incorporate User Feedback
- User requested a toggle option to switch between domain/question scores vs smarter prioritisation
- Smart prioritization uses impact_weight, effort_score, and gap to calculate priority
- Formula for smart priority: impact_weight × gap × (1 - effort_score) to favor lower effort
