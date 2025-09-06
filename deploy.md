# Deploy MYTA to myytagent.app

## Quick Deployment Steps

### Option 1: Vercel (Recommended)

1. **Go to Vercel**
   - Visit [vercel.com](https://vercel.com)
   - Sign up/login with GitHub

2. **Import Project**
   - Click "New Project"
   - Select your GitHub repo: `DazB65/Vidalytics`
   - Set **Root Directory** to: `frontend-nuxt4`
   - Click "Deploy"

3. **Add Custom Domain**
   - Go to Project Settings → Domains
   - Add domain: `myytagent.app`
   - Add domain: `www.myytagent.app`

4. **Update DNS Records**
   In your domain registrar:
   ```
   Type: A
   Name: @
   Value: 76.76.19.61

   Type: CNAME  
   Name: www
   Value: cname.vercel-dns.com
   ```

### Option 2: Netlify

1. **Go to Netlify**
   - Visit [netlify.com](https://netlify.com)
   - Connect GitHub repo

2. **Build Settings**
   - Base directory: `frontend-nuxt4`
   - Build command: `npm run build`
   - Publish directory: `.output/public`

3. **Add Domain**
   - Go to Domain settings
   - Add `myytagent.app`

## Environment Variables (if needed)

```
NODE_ENV=production
NUXT_PUBLIC_API_BASE=https://api.myytagent.app
```

## Build Commands

```bash
# Test build locally
cd frontend-nuxt4
npm install
npm run build
npm run preview
```

Your waitlist page will be live at: https://myytagent.app
