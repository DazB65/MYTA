# MYTA Authentication Setup Guide

## Overview

Complete authentication system with email verification and password reset functionality.

## 🎯 Features Implemented

### ✅ Email Verification
- Verification email sent on registration
- 6-digit verification code + token link
- Resend verification email endpoint
- Welcome email after verification

### ✅ Password Reset
- Request password reset via email
- Secure token-based reset (1-hour expiry)
- Email enumeration protection
- Password reset confirmation

### ✅ Email Service
- Resend API integration
- Professional email templates (HTML + TXT)
- Development mode (logs instead of sending)
- SMTP fallback support

## 📋 Database Migration Required

Before using the authentication features, run this migration:

```bash
# Apply the verification_code migration
psql $DATABASE_URL -f supabase/migrations/20241008_add_verification_code.sql
```

Or in Supabase Dashboard:
1. Go to SQL Editor
2. Run the contents of `supabase/migrations/20241008_add_verification_code.sql`

## 🔧 API Endpoints

### 1. Register User
**POST** `/api/auth/register`

```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "User registered successfully. Please check your email to verify your account.",
  "user": { ... },
  "token": "...",
  "expires_in": 28800,
  "requires_verification": true
}
```

### 2. Verify Email
**POST** `/api/auth/verify-email`

**Option A - Using Token (from email link):**
```json
{
  "token": "verification_token_from_email"
}
```

**Option B - Using Code (6-digit):**
```json
{
  "code": "123456"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Email verified successfully",
  "user": {
    "id": "...",
    "email": "user@example.com",
    "name": "John Doe",
    "is_verified": true
  }
}
```

### 3. Resend Verification Email
**POST** `/api/auth/send-verification-email`

Requires authentication token in header.

**Response:**
```json
{
  "status": "success",
  "message": "Verification email sent successfully"
}
```

### 4. Request Password Reset
**POST** `/api/auth/request-password-reset`

```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "If an account exists with that email, a password reset link has been sent"
}
```

*Note: Always returns success to prevent email enumeration attacks.*

### 5. Reset Password
**POST** `/api/auth/reset-password`

```json
{
  "token": "reset_token_from_email",
  "new_password": "NewSecurePass123!",
  "confirm_password": "NewSecurePass123!"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Password reset successfully"
}
```

## 📧 Email Templates

All templates are in `backend/App/email_templates/`:

1. **email_verification.html/.txt** - Sent on registration
   - Contains verification link and 6-digit code
   - Variables: `user_name`, `verification_url`, `verification_code`

2. **password_reset.html/.txt** - Sent on password reset request
   - Contains reset link (1-hour expiry)
   - Variables: `user_name`, `reset_url`

3. **welcome.html/.txt** - Sent after email verification
   - Introduces the 6 AI agents
   - Quick start guide
   - Variables: `user_name`, `dashboard_url`, `help_url`

4. **email_change_confirmation.html/.txt** - For future email change feature
   - Variables: `user_name`, `old_email`, `new_email`, `confirmation_url`

## 🔐 Security Features

### Rate Limiting
- Registration: 5 requests/minute
- Email verification: 10 requests/hour
- Resend verification: 3 requests/hour
- Password reset request: 3 requests/hour
- Password reset confirm: 5 requests/hour

### Token Security
- Verification tokens: 32-byte URL-safe tokens
- Reset tokens: 32-byte URL-safe tokens with 1-hour expiry
- Verification codes: 6-digit numeric codes

### Email Enumeration Protection
- Password reset always returns success
- No indication if email exists or not

## 🧪 Testing

### Test Email Service
```bash
cd backend
python3 simple_email_test.py
```

### Test Registration Flow
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!",
    "confirm_password": "TestPass123!",
    "name": "Test User"
  }'
```

### Test Email Verification
```bash
# Using code
curl -X POST http://localhost:8000/api/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{"code": "123456"}'

# Using token
curl -X POST http://localhost:8000/api/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{"token": "your_verification_token"}'
```

## 🚀 Production Checklist

### Email Configuration
- [ ] Verify domain in Resend dashboard
- [ ] Add DNS records (SPF, DKIM, DMARC)
- [ ] Update `FROM_EMAIL` to `noreply@myta.app`
- [ ] Test email delivery to multiple providers (Gmail, Outlook, etc.)

### Environment Variables
```bash
# Required
RESEND_API_KEY=re_your_production_key
FROM_EMAIL=noreply@myta.app
FROM_NAME=MYTA Team
BASE_URL=https://myta.app

# Optional (for SMTP fallback)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### Database
- [ ] Run verification_code migration
- [ ] Verify indexes are created
- [ ] Test RLS policies for users table

### Frontend Integration
- [ ] Add verification prompt after registration
- [ ] Create email verification page
- [ ] Add "Resend verification email" button
- [ ] Create password reset request page
- [ ] Create password reset confirmation page
- [ ] Show verification status in user profile

## 📝 Next Steps

1. **Run Database Migration** - Add verification_code column
2. **Test Email Flow** - Register and verify a test account
3. **Frontend Integration** - Build verification and reset pages
4. **Domain Verification** - Set up production email domain
5. **Monitoring** - Add email delivery tracking

## 🐛 Troubleshooting

### Emails Not Sending
- Check `RESEND_API_KEY` is set correctly
- Verify domain is authenticated in Resend
- Check logs for email service errors
- Try using `onboarding@resend.dev` for testing

### Verification Not Working
- Ensure migration was run successfully
- Check verification_code column exists
- Verify indexes are created
- Check token hasn't expired

### Password Reset Issues
- Tokens expire after 1 hour
- Check reset_token and reset_token_expires columns
- Verify email was sent (check logs)

## 📚 Related Documentation

- [Email Service Setup](./EMAIL_SERVICE_SETUP.md)
- [Resend Documentation](https://resend.com/docs)
- [Supabase Auth](https://supabase.com/docs/guides/auth)

