#!/bin/bash

echo "🚀 Deploying MYTA Waitlist with Custom Domain..."

# Test domain first
echo "🧪 Testing domain setup..."
node test-domain-email.js

# Ask user if domain test passed
echo ""
read -p "Did the domain test pass? (y/n): " domain_ready

if [ "$domain_ready" != "y" ]; then
    echo "❌ Please complete domain verification first"
    echo "1. Add myytagent.app to Resend dashboard"
    echo "2. Add DNS records to your domain registrar"
    echo "3. Wait for verification"
    echo "4. Run this script again"
    exit 1
fi

echo "✅ Domain verified! Deploying to Vercel..."

# Deploy to Vercel
vercel --prod

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "🧪 Test your waitlist:"
echo "1. Go to your deployed URL"
echo "2. Sign up with any email address"
echo "3. Check that email for the welcome message"
echo ""
echo "✅ Your waitlist can now send emails to any signup address!"
