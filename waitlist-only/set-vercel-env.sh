#!/bin/bash

echo "🔧 Setting Vercel Environment Variables..."

# Set Supabase URL
vercel env add VITE_SUPABASE_URL production <<< "https://eaqwlsnstnobjwfsqrxa.supabase.co"

# Set Supabase Anon Key
vercel env add VITE_SUPABASE_ANON_KEY production <<< "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVhcXdsc25zdG5vYmp3ZnNxcnhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE1NzUyNDYsImV4cCI6MjA2NzE1MTI0Nn0.fY71cSRnsDlsjgj9N7aqUsmkeJXGJBX0oCwdY4MAGSM"

# Set Resend API Key
vercel env add RESEND_API_KEY production <<< "re_FtW9uwHE_P3NtJbmWAZumfHUNeKKHTUs9"

echo "✅ Environment variables set!"
echo "🚀 Now redeploying..."

# Redeploy
vercel --prod

echo "🎉 Done! Your waitlist should now work!"
