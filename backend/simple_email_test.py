"""
Simple standalone test for email service
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simple test using Resend directly
try:
    import resend
    resend.api_key = os.getenv('RESEND_API_KEY')
    
    async def test_simple_email():
        print("🧪 Testing MYTA Email Service (Simple Test)\n")
        print("=" * 60)
        
        # Check environment
        print("\n📋 Environment Check:")
        resend_key = os.getenv('RESEND_API_KEY', '')
        if resend_key:
            print(f"✅ RESEND_API_KEY: {resend_key[:10]}...")
        else:
            print("❌ RESEND_API_KEY: Not set")
            return
        
        from_email = os.getenv('FROM_EMAIL', 'onboarding@resend.dev')
        print(f"✅ FROM_EMAIL: {from_email}")
        
        # Get test email
        test_email = input("\n📧 Enter your email to receive a test: ").strip()
        if not test_email:
            print("❌ No email provided")
            return
        
        print(f"\n✅ Sending test email to: {test_email}")
        print("\n" + "=" * 60)
        
        # Send simple test email
        print("\n📤 Sending test email via Resend...")
        
        try:
            # Run in executor since Resend is synchronous
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: resend.Emails.send({
                    "from": f"MYTA Team <{from_email}>",
                    "to": [test_email],
                    "subject": "🎬 MYTA Email Service Test",
                    "html": """
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <style>
                            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #ffffff; background-color: #0f1419; margin: 0; padding: 20px; }
                            .container { max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #1a2f23 0%, #0f1f17 100%); border-radius: 12px; padding: 40px; border: 1px solid #2d4a37; }
                            .header { text-align: center; margin-bottom: 30px; }
                            .logo { font-size: 48px; margin-bottom: 10px; }
                            h1 { color: #f97316; margin: 0; }
                            .content { color: #e2e8f0; }
                            .success { background: #2d4a37; padding: 20px; border-radius: 8px; border-left: 4px solid #10b981; margin: 20px 0; }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <div class="logo">🎬</div>
                                <h1>Email Service Test</h1>
                            </div>
                            <div class="content">
                                <div class="success">
                                    <h2 style="color: #10b981; margin-top: 0;">✅ Success!</h2>
                                    <p>Your MYTA email service is working correctly!</p>
                                </div>
                                <p>This is a test email from the MYTA backend email service.</p>
                                <p><strong>What's working:</strong></p>
                                <ul>
                                    <li>✅ Resend API integration</li>
                                    <li>✅ HTML email templates</li>
                                    <li>✅ Email delivery</li>
                                </ul>
                                <p>You're all set to send authentication emails!</p>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    "text": """
🎬 MYTA Email Service Test

✅ Success!

Your MYTA email service is working correctly!

This is a test email from the MYTA backend email service.

What's working:
✅ Resend API integration
✅ HTML email templates
✅ Email delivery

You're all set to send authentication emails!
                    """
                })
            )
            
            print("✅ Email sent successfully!")
            print(f"   Email ID: {result.get('id', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return
        
        print("\n" + "=" * 60)
        print("\n✅ Email service test complete!")
        print("\n📬 Check your inbox for the test email.")
        print("💡 If you don't see it, check your spam folder.")
        print("\n" + "=" * 60)
    
    # Run the test
    asyncio.run(test_simple_email())
    
except ImportError:
    print("❌ Resend package not installed")
    print("Install with: pip install resend")
except Exception as e:
    print(f"❌ Error: {e}")

