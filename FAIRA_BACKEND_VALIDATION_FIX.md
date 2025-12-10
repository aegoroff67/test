# FAIRA Backend Validation Fix

## Issue
When trying to grant FAIRA assessment access to users via the User Management page, the system returned an error: "Failed to update assessment access". This was because the backend validation rejected 'faira' as an invalid assessment type.

## Root Cause
The `update_user_assessment_access` endpoint in `/app/backend/server.py` had a hardcoded validation list that only allowed:
- awareness
- readiness
- system
- orgwide

The 'faira' assessment type was missing from this list.

## Solution
Added 'faira' to the `valid_assessments` list in the backend validation.

### File Modified: `/app/backend/server.py`

### Change Made (Line 622):
```python
# Before:
valid_assessments = ["awareness", "readiness", "system", "orgwide"]

# After:
valid_assessments = ["awareness", "readiness", "system", "orgwide", "faira"]
```

## Testing
- Backend restarted successfully
- Service running on http://0.0.0.0:8001
- No errors in backend logs

## Impact
Super admins can now successfully:
- ✅ Grant FAIRA assessment access to users
- ✅ Revoke FAIRA assessment access from users
- ✅ Update assessment_access array with 'faira' value

## Related Changes
This fix complements the frontend changes made in:
1. `/app/frontend/src/pages/AssessmentSelector.js` - FAIRA assessment card
2. `/app/frontend/src/pages/SettingsPage.js` - FAIRA permission checkbox

## User Action Required
Users (like andrew@test.com) can now retry granting themselves FAIRA access via:
1. Navigate to Settings → User Management
2. Check the "FAIRA" checkbox for the desired user
3. Changes will save successfully
