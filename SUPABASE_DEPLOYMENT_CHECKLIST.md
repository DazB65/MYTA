# MYTA Supabase Deployment Checklist

## 🔧 **Required Supabase Configuration**

### **1. Database Schema Setup**

**✅ Action Required**: Run the SQL migration in Supabase

1. Go to your Supabase dashboard: https://supabase.com/dashboard
2. Select your project: `MY YT Agent (eaqwlsnstnobjwfsqrxa)`
3. Go to **SQL Editor**
4. Copy and paste the contents of `supabase_users_migration.sql`
5. Click **Run** to execute the migration

**What this creates**:
- `users` table with proper schema
- `user_sessions` table for session management
- Proper indexes for performance
- Row Level Security (RLS) policies
- Triggers for automatic updates

### **2. Environment Variables Setup**

**✅ Action Required**: Get your Supabase keys

1. In Supabase dashboard, go to **Settings** > **API**
2. Copy these values:
   - **Project URL**: `https://eaqwlsnstnobjwfsqrxa.supabase.co`
   - **Service Role Key**: `eyJ...` (the SECRET key, not anon key)

### **3. Vercel Environment Variables**

**✅ Action Required**: Set these in Vercel dashboard

For **Backend** deployment (`myta-backend.vercel.app`):
```bash
VITE_SUPABASE_URL=https://eaqwlsnstnobjwfsqrxa.supabase.co
SUPABASE_SERVICE_KEY=your_service_role_key_here
JWT_SECRET=your_generated_jwt_secret_here
```

For **Frontend** deployment (`myta-app.vercel.app`):
```bash
VITE_SUPABASE_URL=https://eaqwlsnstnobjwfsqrxa.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key_here
```

### **4. Generate JWT Secret**

**✅ Action Required**: Generate a secure JWT secret

Run this command to generate a secure secret:
```bash
openssl rand -base64 32
```

Use the output as your `JWT_SECRET` value.

## 🚀 **Deployment Steps**

### **Step 1: Supabase Setup**
1. ✅ Run `supabase_users_migration.sql` in Supabase SQL Editor
2. ✅ Verify tables are created: `users`, `user_sessions`
3. ✅ Check RLS policies are enabled

### **Step 2: Backend Deployment**
1. ✅ Set environment variables in Vercel for `myta-backend`
2. ✅ Deploy backend code to `myta-backend.vercel.app`
3. ✅ Test health endpoint: `https://myta-backend.vercel.app/health`

### **Step 3: Frontend Deployment**
1. ✅ Set environment variables in Vercel for `myta-app`
2. ✅ Deploy frontend code to `myta-app.vercel.app`
3. ✅ Test registration flow

### **Step 4: Verification**
1. ✅ Test user registration
2. ✅ Test user login
3. ✅ Verify data persists in Supabase
4. ✅ Check CORS is working

## 🔍 **Verification Queries**

After deployment, you can verify everything works by running these in Supabase SQL Editor:

```sql
-- Check if users table exists and has correct schema
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'users';

-- Check RLS policies
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual 
FROM pg_policies 
WHERE tablename = 'users';

-- After testing registration, check if users are being created
SELECT id, email, name, created_at, is_verified 
FROM users 
ORDER BY created_at DESC 
LIMIT 5;
```

## 🚨 **Security Notes**

1. **Never use the service role key in frontend code**
2. **Always use the anonymous key for frontend**
3. **RLS policies protect user data automatically**
4. **JWT secrets should be long and random**
5. **Rotate keys periodically for security**

## 📋 **Current Status**

- ✅ Backend code updated with proper Supabase integration
- ✅ Environment variables configured for both keys
- ✅ SQL migration file created
- ✅ Frontend URLs updated to correct backend
- ⏳ **NEXT**: Run SQL migration in Supabase
- ⏳ **NEXT**: Set environment variables in Vercel
- ⏳ **NEXT**: Deploy and test

## 🔗 **Important URLs**

- **Supabase Dashboard**: https://supabase.com/dashboard/project/eaqwlsnstnobjwfsqrxa
- **Backend URL**: https://myta-backend.vercel.app
- **Frontend URL**: https://myta-app.vercel.app
- **Vercel Dashboard**: https://vercel.com/dashboard
