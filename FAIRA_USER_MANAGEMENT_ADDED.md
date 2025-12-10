# FAIRA Assessment Access Added to User Management

## Summary
Added FAIRA assessment access control option in the User Management page, allowing super admins to grant or revoke FAIRA assessment permissions to users.

## Changes Made

### File Modified: `/app/frontend/src/pages/SettingsPage.js`

### Change Details:

Added a new checkbox for FAIRA assessment access in the User Management table, positioned after the System assessment checkbox.

#### Checkbox Implementation:
```javascript
<label className="flex items-center gap-1 text-xs">
  <input
    type="checkbox"
    checked={u.assessment_access?.includes('faira') || false}
    onChange={(e) => {
      const newAccess = e.target.checked
        ? [...(u.assessment_access || []), 'faira']
        : (u.assessment_access || []).filter(a => a !== 'faira');
      updateAssessmentAccess(u.id, newAccess);
    }}
    className="rounded"
  />
  <span className="text-gray-700">FAIRA</span>
</label>
```

### Features:
- **Label**: "FAIRA" (displayed in gray)
- **Position**: Below System assessment checkbox
- **Functionality**: 
  - Toggles 'faira' value in user's `assessment_access` array
  - Updates user permissions via `updateAssessmentAccess()` function
  - Respects existing permission state
- **Visibility**: Only visible to SUPER_ADMIN users

### Assessment Access Order:
1. Awareness
2. Readiness
3. Org-wide
4. System
5. **FAIRA** (NEW)

## Integration with Assessment Selector:
The FAIRA checkbox controls whether users can access the FAIRA Risk Assessment card on the Assessment Selector page:
- ✅ Checked: User can create FAIRA assessments
- ❌ Unchecked: Card shows "Requires Permission" and button is disabled

## Build Status:
- ✅ Frontend build successful
- ✅ No compilation errors
- ✅ Follows existing permission management pattern

## Backend Considerations:
The backend `updateAssessmentAccess()` API should already handle the 'faira' permission since it accepts an array of assessment types. No backend changes required unless specific validation is needed.

## Testing:
- Frontend component added successfully
- Build verified
- Follows same structure as existing assessment permission checkboxes
