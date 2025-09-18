# MYTA Dashboard

Private admin dashboard for monitoring MYTA production metrics.

## 🔐 Access

- **URL:** dashboard.myytagent.app
- **Authentication:** Secure password-based access via backend API
- **Setup:** Configure `DASHBOARD_PASSWORD_HASH` environment variable

## 🚀 Development

```bash
cd dashboard
npm install
npm run dev
```

## 📊 Features (Coming Soon)

- Real-time user analytics
- AI agent performance metrics
- YouTube integration stats
- System health monitoring
- Error tracking and alerts

## 🔧 Deployment

Automatically deployed to Vercel when pushed to main branch.

## 🛡 Security Setup

### Production Configuration

1. **Set Dashboard Password Hash:**

   ```bash
   # Generate password hash (replace 'your-secure-password' with actual password)
   echo -n 'your-secure-password' | sha256sum

   # Set environment variable
   export DASHBOARD_PASSWORD_HASH="your-generated-hash"
   ```

2. **Set JWT Secret (optional):**
   ```bash
   export DASHBOARD_JWT_SECRET="your-random-secret-key"
   ```

### Development Fallback

- If no `DASHBOARD_PASSWORD_HASH` is set, defaults to `admin123` for development
- **⚠️ Never use default password in production!**

### Security Features

- Password protected access with secure hashing
- JWT-based session tokens with expiration
- Rate limiting on authentication attempts
- Separate subdomain from main app
- Admin-only access controls
