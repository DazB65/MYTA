# MYTA Waitlist Setup Guide

This guide will help you set up the complete MYTA waitlist system with email automation.

## 🚀 Quick Setup

### 1. Environment Variables

Copy `.env.example` to `.env.local` and fill in your values:

```bash
cp .env.example .env.local
```

Required variables:
- `VITE_SUPABASE_URL` - Your Supabase project URL
- `VITE_SUPABASE_ANON_KEY` - Your Supabase anonymous key
- `RESEND_API_KEY` - Your Resend API key

### 2. Database Setup

Run the database migration in your Supabase SQL editor:

```sql
-- Copy and paste the contents of:
-- backend/database/migrations/create_waitlist_table.sql
```

### 3. Resend Setup

1. Sign up at [resend.com](https://resend.com)
2. Verify your domain (or use their test domain)
3. Get your API key from the dashboard
4. Update the `from` email in `api/send-email.js` to match your verified domain

### 4. Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

## 📧 Email Templates

The system includes 3 email templates:

1. **Welcome Email** - Sent immediately after signup
2. **Update Email** - Development progress updates
3. **Early Access** - Exclusive early access invitations

## 🔧 API Endpoints

### POST /api/waitlist
Handles waitlist signups.

**Request Body:**
```json
{
  "email": "user@example.com",
  "youtube_channel_name": "My Channel",
  "subscriber_range": "1k-10k",
  "signup_source": "landing_page"
}
```

### POST /api/send-email
Sends emails using templates.

**Request Body:**
```json
{
  "email": "user@example.com",
  "template": "welcome",
  "waitlist_id": "uuid"
}
```

### GET/POST /api/unsubscribe?id=uuid
Handles unsubscribe requests.

## 🧪 Testing

### Test Signup Flow

1. Open your deployed waitlist page
2. Fill out the form with a test email
3. Check your email for the welcome message
4. Verify the data appears in your Supabase `waitlist` table

### Test Email Templates

Send test emails using the API:

```bash
curl -X POST https://your-domain.vercel.app/api/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "template": "welcome",
    "waitlist_id": "test-id"
  }'
```

### Test Unsubscribe

1. Get a waitlist ID from your database
2. Visit: `https://your-domain.vercel.app/api/unsubscribe?id=WAITLIST_ID`
3. Confirm the unsubscribe process works

## 📊 Analytics

The system tracks:
- Signup source (landing page, social media, etc.)
- Device and browser information
- Geographic location
- Email engagement (opens, clicks)
- Conversion rates

Query your analytics:

```sql
-- Total signups by source
SELECT signup_source, COUNT(*) as signups
FROM waitlist 
GROUP BY signup_source;

-- Signups over time
SELECT DATE(created_at) as date, COUNT(*) as signups
FROM waitlist 
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Email engagement
SELECT 
  COUNT(*) as total_signups,
  COUNT(*) FILTER (WHERE welcome_email_sent = true) as emails_sent,
  AVG(email_opens) as avg_opens
FROM waitlist;
```

## 🔄 Email Automation

To set up automated email sequences:

1. Use a cron service (like Vercel Cron or GitHub Actions)
2. Create scheduled functions that query the waitlist
3. Send follow-up emails based on signup date

Example cron job (weekly update):

```javascript
// api/cron/weekly-update.js
export default async function handler(req, res) {
  // Get users who signed up 7 days ago
  const { data } = await supabase
    .from('waitlist')
    .select('*')
    .eq('status', 'active')
    .gte('created_at', new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString())
    .lt('created_at', new Date(Date.now() - 6 * 24 * 60 * 60 * 1000).toISOString());

  // Send update emails
  for (const user of data) {
    await sendEmail(user.email, 'update_1', user.id);
  }
}
```

## 🛡️ Security

- All emails are validated
- Rate limiting is handled by Vercel
- Unsubscribe links are secure
- No sensitive data in client-side code

## 📈 Optimization Tips

1. **A/B Test Subject Lines** - Try different email subjects
2. **Segment Users** - Send different content based on subscriber count
3. **Track Conversions** - Monitor which sources convert best
4. **Optimize Send Times** - Test different email send times

## 🚨 Troubleshooting

### Common Issues

**Emails not sending:**
- Check your Resend API key
- Verify your domain is authenticated
- Check the console logs for errors

**Form not submitting:**
- Verify Supabase credentials
- Check browser console for JavaScript errors
- Ensure CORS is configured correctly

**Database errors:**
- Run the migration script
- Check table permissions in Supabase
- Verify RLS policies if enabled

## 📞 Support

For issues or questions:
- Email: myytagent@icloud.com
- Check the browser console for error messages
- Review Vercel function logs for API issues
