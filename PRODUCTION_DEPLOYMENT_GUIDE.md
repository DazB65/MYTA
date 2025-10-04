# 🚀 MYTA Production Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ Security Configuration Complete
- [x] Development authentication bypass removed
- [x] .env files properly gitignored
- [x] Production environment template created
- [ ] New production API keys generated
- [ ] Production environment variables configured

### 🔑 API Keys to Generate (Production Only)
1. **OpenAI**: https://platform.openai.com/api-keys
2. **Anthropic**: https://console.anthropic.com/
3. **Google Cloud**: https://console.cloud.google.com/
4. **Stripe**: https://dashboard.stripe.com/apikeys
5. **Supabase**: https://app.supabase.com/

## 🏗️ Infrastructure Setup

### Backend Hosting Options
1. **Railway** (Recommended)
   - Easy deployment from GitHub
   - Built-in PostgreSQL and Redis
   - Automatic SSL certificates

2. **Render**
   - Free tier available
   - Managed databases
   - Auto-deploy from GitHub

3. **VPS** (Advanced)
   - Full control
   - Requires manual setup
   - Use Docker compose

### Frontend Hosting
- **Vercel** (User Preference)
  - Deploy from `frontend-nuxt4` directory
  - Domain: `myytagent.app`
  - Environment variables via Vercel dashboard

## 🗄️ Database Migration

### From SQLite to PostgreSQL
```bash
# 1. Export current data
python scripts/export_sqlite_data.py

# 2. Set up PostgreSQL database
# 3. Import data to PostgreSQL
python scripts/import_to_postgresql.py
```

## 🔧 Environment Variables Setup

### For Backend (Railway/Render)
Copy from `.env.production.template` and set:
- All API keys with production values
- DATABASE_URL (provided by hosting service)
- REDIS_URL (provided by hosting service)
- CORS_ORIGINS with actual domain

### For Frontend (Vercel)
Set in Vercel dashboard:
- `NODE_ENV=production`
- `NUXT_PUBLIC_API_BASE=https://api.myytagent.app`
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`
- `NUXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`

## 🌐 Domain Configuration

### DNS Records
```
Type: A
Name: @
Value: [Vercel IP]

Type: CNAME
Name: www
Value: cname.vercel-dns.com

Type: CNAME
Name: api
Value: [Backend hosting URL]
```

## 🧪 Testing Checklist

### Pre-Launch Testing
- [ ] Authentication flow works
- [ ] All AI agents respond correctly
- [ ] YouTube OAuth integration works
- [ ] Stripe payments process correctly
- [ ] All API endpoints respond
- [ ] Database connections stable
- [ ] Redis caching works

### Load Testing
```bash
# Test API endpoints
npm install -g artillery
artillery quick --count 10 --num 5 https://api.myytagent.app/health
```

## 📊 Monitoring Setup

### Error Tracking
- Set up Sentry for error monitoring
- Configure alerts for critical errors

### Uptime Monitoring
- Use UptimeRobot or similar
- Monitor both frontend and backend

### Performance Monitoring
- Set up application performance monitoring
- Monitor database query performance

## 🚀 Deployment Steps

### 1. Backend Deployment
1. Create account on Railway/Render
2. Connect GitHub repository
3. Set environment variables
4. Deploy from `backend` directory
5. Run database migrations
6. Test API endpoints

### 2. Frontend Deployment
1. Connect Vercel to GitHub
2. Set root directory to `frontend-nuxt4`
3. Configure environment variables
4. Deploy to production
5. Configure custom domain

### 3. DNS Cutover
1. Update DNS records
2. Wait for propagation (up to 24 hours)
3. Test all functionality
4. Monitor for issues

## 🔄 Post-Deployment

### Immediate Actions
- [ ] Test all critical user flows
- [ ] Verify monitoring is working
- [ ] Check error logs
- [ ] Test performance under load

### Ongoing Maintenance
- [ ] Set up automated backups
- [ ] Schedule security updates
- [ ] Monitor performance metrics
- [ ] Review error logs regularly

## 🆘 Rollback Plan

If issues occur:
1. Revert DNS to previous configuration
2. Check error logs for issues
3. Fix issues in staging environment
4. Re-deploy when ready

## 📞 Support Contacts

- **Hosting Issues**: Railway/Render support
- **Domain Issues**: Domain registrar support
- **SSL Issues**: Hosting provider support
- **Application Issues**: Check logs and monitoring
