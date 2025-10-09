# MYTA Email Service Setup Guide

This guide will help you set up the email service for MYTA using Resend (recommended) or SMTP.

## 📋 Overview

MYTA's email service handles:
- ✅ Email verification for new users
- ✅ Password reset emails
- ✅ Welcome emails after verification
- ✅ Email change confirmations
- ✅ Team invitation emails
- ✅ Team collaboration notifications

## 🚀 Quick Start (Resend - Recommended)

### Step 1: Create Resend Account

1. Go to [resend.com](https://resend.com)
2. Sign up for a free account (3,000 emails/month free)
3. Verify your email address

### Step 2: Get API Key

1. Go to [API Keys](https://resend.com/api-keys)
2. Click "Create API Key"
3. Name it "MYTA Production" (or similar)
4. Select permissions: "Sending access"
5. Copy the API key (starts with `re_`)

### Step 3: Configure Domain (Production)

For production, you need to verify your domain:

1. Go to [Domains](https://resend.com/domains)
2. Click "Add Domain"
3. Enter your domain: `myta.app`
4. Add the DNS records shown to your domain provider:
   - SPF record
   - DKIM records
   - DMARC record (optional but recommended)
5. Wait for verification (usually 5-15 minutes)

**For Development**: You can use `onboarding@resend.dev` as the from address without domain verification.

### Step 4: Set Environment Variables

Add to your `.env` file:

```bash
# Email Service - Resend
USE_RESEND=true
RESEND_API_KEY=re_your_actual_api_key_here

# Email Sender (use your verified domain)
FROM_EMAIL=noreply@myta.app
FROM_NAME=MYTA Team

# Base URL for email links
BASE_URL=https://app.myytagent.app
```

### Step 5: Install Dependencies

```bash
cd backend
pip install resend>=0.8.0 aiosmtplib>=3.0.0 jinja2>=3.1.0
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### Step 6: Test Email Sending

Create a test script `test_email.py`:

```python
import asyncio
from backend.App.email_service import send_verification_email

async def test():
    result = await send_verification_email(
        user_email="your-email@example.com",
        user_name="Test User",
        verification_token="test-token-123",
        verification_code="123456"
    )
    print(f"Email sent: {result}")

asyncio.run(test())
```

Run it:
```bash
python test_email.py
```

## 🔧 Alternative: SMTP Setup

If you prefer to use SMTP instead of Resend:

### Gmail SMTP

1. Enable 2-factor authentication on your Google account
2. Generate an App Password:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Click "2-Step Verification"
   - Scroll to "App passwords"
   - Generate password for "Mail"
3. Configure `.env`:

```bash
USE_RESEND=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password-here
FROM_EMAIL=your-email@gmail.com
FROM_NAME=MYTA Team
```

### Other SMTP Providers

**SendGrid**:
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
```

**AWS SES**:
```bash
SMTP_HOST=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USERNAME=your-ses-smtp-username
SMTP_PASSWORD=your-ses-smtp-password
```

## 📧 Email Templates

All email templates are located in `backend/App/email_templates/`:

- `email_verification.html` / `.txt` - Email verification
- `password_reset.html` / `.txt` - Password reset
- `welcome.html` / `.txt` - Welcome email
- `email_change_confirmation.html` / `.txt` - Email change
- `team_invitation.html` / `.txt` - Team invites
- `invitation_accepted.html` / `.txt` - Invite accepted
- `welcome_to_team.html` / `.txt` - Team welcome
- `member_removed.html` / `.txt` - Member removed

See `backend/App/email_templates/README.md` for detailed documentation.

## 🧪 Testing

### Development Mode

For local development without sending real emails:

```bash
# In .env - leave SMTP credentials empty
USE_RESEND=false
SMTP_USERNAME=
SMTP_PASSWORD=
```

Emails will be logged to console instead of being sent.

### Test All Email Types

```python
import asyncio
from backend.App.email_service import (
    send_verification_email,
    send_password_reset_email,
    send_welcome_email,
    send_email_change_confirmation
)

async def test_all_emails():
    test_email = "your-email@example.com"
    
    # Test verification email
    await send_verification_email(
        user_email=test_email,
        user_name="Test User",
        verification_token="test-token",
        verification_code="123456"
    )
    
    # Test password reset
    await send_password_reset_email(
        user_email=test_email,
        user_name="Test User",
        reset_token="reset-token"
    )
    
    # Test welcome email
    await send_welcome_email(
        user_email=test_email,
        user_name="Test User"
    )
    
    # Test email change
    await send_email_change_confirmation(
        new_email=test_email,
        user_name="Test User",
        old_email="old@example.com",
        confirmation_token="change-token"
    )
    
    print("All test emails sent!")

asyncio.run(test_all_emails())
```

## 🔒 Security Best Practices

1. **Never commit API keys**: Always use `.env` file (in `.gitignore`)
2. **Use environment-specific keys**: Different keys for dev/staging/production
3. **Implement rate limiting**: Prevent email spam
4. **Validate email addresses**: Use proper email validation
5. **Use HTTPS URLs**: All email links should use HTTPS in production
6. **Set up SPF/DKIM/DMARC**: Improve deliverability and prevent spoofing
7. **Monitor email sending**: Track bounces and complaints
8. **Implement unsubscribe**: For marketing emails (not transactional)

## 📊 Monitoring

### Resend Dashboard

Monitor your emails at [resend.com/emails](https://resend.com/emails):
- Delivery status
- Open rates (if tracking enabled)
- Bounce rates
- Spam complaints

### Application Logs

Email sending is logged in the application:

```python
# Success
logger.info(f"Email sent successfully via Resend to {to_email}")

# Failure
logger.error(f"Failed to send email via Resend to {to_email}: {error}")
```

## 🚨 Troubleshooting

### Emails Not Sending

1. **Check API key**: Ensure `RESEND_API_KEY` is correct
2. **Check domain**: Verify domain is verified in Resend dashboard
3. **Check logs**: Look for error messages in application logs
4. **Check rate limits**: Ensure you haven't exceeded Resend limits
5. **Check from address**: Must match verified domain

### Emails Going to Spam

1. **Verify domain**: Add SPF, DKIM, DMARC records
2. **Warm up domain**: Start with low volume, gradually increase
3. **Check content**: Avoid spam trigger words
4. **Monitor reputation**: Check domain reputation with mail-tester.com
5. **Use proper from address**: Don't use generic addresses like noreply@gmail.com

### Template Rendering Errors

1. **Check template syntax**: Ensure Jinja2 syntax is correct
2. **Check variables**: Ensure all required variables are passed
3. **Check file paths**: Ensure template files exist
4. **Check permissions**: Ensure templates directory is readable

## 📈 Production Checklist

- [ ] Resend account created and verified
- [ ] Domain verified in Resend
- [ ] SPF, DKIM, DMARC records added to DNS
- [ ] Production API key generated
- [ ] Environment variables set in production
- [ ] Dependencies installed (`resend`, `aiosmtplib`, `jinja2`)
- [ ] Test emails sent successfully
- [ ] Email templates reviewed and tested
- [ ] Rate limiting configured
- [ ] Monitoring set up
- [ ] Error handling tested
- [ ] Bounce handling implemented
- [ ] Unsubscribe links added (if needed)

## 🔗 Resources

- [Resend Documentation](https://resend.com/docs)
- [Resend Python SDK](https://github.com/resendlabs/resend-python)
- [Email Design Best Practices](https://www.campaignmonitor.com/dev-resources/guides/coding/)
- [SPF/DKIM/DMARC Guide](https://www.cloudflare.com/learning/email-security/dmarc-dkim-spf/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)

## 💬 Support

If you encounter issues:
1. Check the logs in `backend/App/email_service.py`
2. Review Resend dashboard for delivery status
3. Test with development mode first
4. Contact Resend support if needed

---

**Next Steps**: After email service is configured, proceed to implement email verification and password reset endpoints in the authentication router.

