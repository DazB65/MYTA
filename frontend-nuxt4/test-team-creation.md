# Team Creation Testing Guide

## How to Test Team Creation in MYTA

### 1. **Access the Settings Page**
- Navigate to `/settings` in your browser
- Click on the "Team" tab
- You should see a "No Team Yet" section with a "Create Team" button

### 2. **Open Team Creation Modal**
- Click the "Create Team" button
- A modal should open with the title "Create Team"
- The modal should have:
  - Team Name input field
  - Maximum Team Size dropdown (3, 5, 10, 25 members)
  - Description textarea (optional)
  - Features list showing team benefits
  - Cancel and Create Team buttons

### 3. **Test Form Validation**
- Try submitting without a team name - should show error
- Try entering a very short name (1 character) - should show error
- Try entering a very long name (50+ characters) - should show error
- Valid names should pass validation

### 4. **Test Team Creation**
- Enter a valid team name (e.g., "My Content Team")
- Select a team size (default is 5)
- Optionally add a description
- Click "Create Team"

### 5. **Expected Behavior**

#### **If Backend is Running:**
- Team should be created via API
- Success message should appear
- Modal should close after 1.5 seconds
- Settings page should refresh and show the new team

#### **If Backend is NOT Running (Demo Mode):**
- Should show "Creating team in demo mode" message briefly
- Then show "Demo team created! 🎉" success message
- Modal should close and show the demo team in settings
- Team should appear with mock data

### 6. **Verify Team Display**
After successful creation, the settings page should show:
- Team name and details
- Team member count (1 member - you as owner)
- Available seats
- "Edit Team" and "Invite Member" buttons
- Your user listed as team owner

### 7. **Test Error Scenarios**
- If not logged in: Should show authentication error
- If subscription doesn't support teams: Should show subscription error
- Network errors: Should show appropriate error messages

## Troubleshooting

### **Modal Doesn't Open**
- Check browser console for JavaScript errors
- Ensure all imports are correct in settings.vue
- Verify TeamCreationModal.vue exists

### **Form Validation Issues**
- Check that reactive form data is properly bound
- Verify validation logic in handleSubmit method

### **Team Creation Fails**
- Check network tab for API calls
- Verify authentication token is present
- Check backend logs if running
- Demo mode should work even without backend

### **Success But No Team Shows**
- Check that handleTeamCreated method is called
- Verify fetchMyTeam is working
- Check currentTeam state in useTeamManagement

## Demo Mode Features

When backend is not available, the system will:
1. Create a mock team with realistic data
2. Show the team in the settings interface
3. Allow basic team management operations
4. Provide a smooth demo experience

This ensures the frontend works perfectly even during development or when the backend is unavailable.
