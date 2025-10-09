# MYTA Email Templates

This directory contains all email templates for the MYTA application. Templates are written in both HTML and plain text formats using Jinja2 templating.

## 📧 Available Templates

### Authentication Emails

1. **email_verification.html / .txt**
   - Sent when a user registers
   - Contains verification link and code
   - Expires in 24 hours

2. **password_reset.html / .txt**
   - Sent when user requests password reset
   - Contains reset link
   - Expires in 1 hour

3. **welcome.html / .txt**
   - Sent after email verification is complete
   - Introduces the AI agent team
   - Provides quick start guide

4. **email_change_confirmation.html / .txt**
   - Sent when user changes their email
   - Requires confirmation from new email
   - Expires in 24 hours

### Team Collaboration Emails

5. **team_invitation.html / .txt**
   - Sent when user is invited to join a team
   - Contains accept/decline links
   - Shows team details and role

6. **invitation_accepted.html / .txt**
   - Sent to team owner when invitation is accepted
   - Notifies about new team member

7. **welcome_to_team.html / .txt**
   - Sent to new team member after accepting
   - Welcomes them to the team

8. **member_removed.html / .txt**
   - Sent when a member is removed from team
   - Provides support contact

## 🎨 Template Variables

### Email Verification
```python
{
    "user_name": str,
    "verification_url": str,
    "verification_code": str,
    "current_year": int
}
```

### Password Reset
```python
{
    "user_name": str,
    "reset_url": str,
    "current_year": int
}
```

### Welcome Email
```python
{
    "user_name": str,
    "dashboard_url": str,
    "help_url": str,
    "current_year": int
}
```

### Email Change Confirmation
```python
{
    "user_name": str,
    "old_email": str,
    "new_email": str,
    "confirmation_url": str,
    "current_year": int
}
```

### Team Invitation
```python
{
    "invitation": TeamInvitation,
    "team_name": str,
    "invited_by_name": str,
    "invited_by_email": str,
    "role": str,
    "accept_url": str,
    "decline_url": str,
    "expires_at": str,
    "current_year": int
}
```

## 🎯 Design Guidelines

All email templates follow these design principles:

1. **Dark Theme**: Matches MYTA's brand with dark backgrounds (#0f1419, #1a2f23)
2. **Brand Colors**: 
   - Primary Orange: #f97316
   - Accent Green: #2d4a37
   - Text: #ffffff, #e2e8f0, #94a3b8
3. **Responsive**: Mobile-friendly with max-width: 600px
4. **Accessible**: High contrast, clear hierarchy, semantic HTML
5. **Professional**: Clean layout, proper spacing, branded footer

## 🔧 Usage in Code

### Sending Verification Email
```python
from backend.App.email_service import send_verification_email

await send_verification_email(
    user_email="user@example.com",
    user_name="John Doe",
    verification_token="abc123...",
    verification_code="123456"
)
```

### Sending Password Reset
```python
from backend.App.email_service import send_password_reset_email

await send_password_reset_email(
    user_email="user@example.com",
    user_name="John Doe",
    reset_token="xyz789..."
)
```

### Sending Welcome Email
```python
from backend.App.email_service import send_welcome_email

await send_welcome_email(
    user_email="user@example.com",
    user_name="John Doe"
)
```

### Sending Email Change Confirmation
```python
from backend.App.email_service import send_email_change_confirmation

await send_email_change_confirmation(
    new_email="newemail@example.com",
    user_name="John Doe",
    old_email="oldemail@example.com",
    confirmation_token="token123..."
)
```

## 🧪 Testing Templates

### Development Mode
When `SMTP_USERNAME` and `SMTP_PASSWORD` are not set, emails are logged to console instead of being sent:

```bash
# In .env
SMTP_USERNAME=
SMTP_PASSWORD=
```

### Preview Templates
You can render templates manually for testing:

```python
from jinja2 import Environment, FileSystemLoader
import os

template_dir = os.path.join(os.path.dirname(__file__), "email_templates")
env = Environment(loader=FileSystemLoader(template_dir))

template = env.get_template("welcome.html")
html = template.render(
    user_name="Test User",
    dashboard_url="http://localhost:3000/dashboard",
    help_url="http://localhost:3000/help",
    current_year=2024
)

# Save to file for browser preview
with open("preview.html", "w") as f:
    f.write(html)
```

## 📝 Adding New Templates

1. Create both `.html` and `.txt` versions
2. Follow the existing design patterns
3. Use Jinja2 template variables: `{{ variable_name }}`
4. Add method to `EmailService` class in `email_service.py`
5. Add convenience function at bottom of `email_service.py`
6. Document template variables in this README
7. Test in development mode first

## 🎨 Brand Assets

### Colors
- **Primary Orange**: `#f97316` - CTAs, links, highlights
- **Dark Orange**: `#ea580c` - Gradients, hover states
- **Dark Green**: `#2d4a37` - Cards, containers
- **Darker Green**: `#1a2f23` - Backgrounds
- **Darkest**: `#0f1419` - Base background
- **Blue Accent**: `#3b82f6` - Info boxes
- **Red Accent**: `#ef4444` - Warnings, errors
- **Text Primary**: `#ffffff` - Headings
- **Text Secondary**: `#e2e8f0` - Body text
- **Text Muted**: `#94a3b8` - Captions, hints

### Typography
- **Font Family**: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif`
- **Headings**: 600-700 weight
- **Body**: 400 weight
- **Line Height**: 1.6

### Emojis
- 🎬 - MYTA logo/brand
- 🔐 - Security/authentication
- 📧 - Email-related
- 🎯 - Boss Agent
- 📊 - Analytics (Alex)
- 🎨 - Strategy (Levi)
- ⚡ - Performance (Maya)
- 💬 - Community (Zara)
- 📈 - Trends (Kai)

## 🔒 Security Notes

- Never include sensitive data in email templates
- Always use HTTPS URLs in production
- Tokens should be cryptographically secure
- Implement rate limiting on email sending
- Log email sending for audit purposes
- Use proper email authentication (SPF, DKIM, DMARC)

## 📚 Resources

- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Email Design Best Practices](https://www.campaignmonitor.com/dev-resources/guides/coding/)
- [Resend Documentation](https://resend.com/docs)
- [MYTA Brand Guidelines](../../docs/brand-guidelines.md)

