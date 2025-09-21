import { createClient } from "@supabase/supabase-js";
import dotenv from "dotenv";

// Load environment variables
dotenv.config({ path: ".env.local" });

// Import the email templates directly
import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

// Email templates (updated with YouTube link)
const templates = {
  welcome: {
    subject: "🎉 Welcome to the MYTA Waitlist!",
    html: (data) => `
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to MYTA</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8fafc; }
        .container { max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
        .header { background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); color: white; padding: 40px 30px; text-align: center; }
        .header h1 { margin: 0; font-size: 28px; font-weight: 700; }
        .content { padding: 40px 30px; }
        .content h2 { color: #f97316; margin-top: 0; }
        .btn { display: inline-block; background: #f97316; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; margin: 5px; }
        .btn:hover { background: #ea580c; }
        .footer { background: #f8fafc; padding: 20px 30px; text-align: center; color: #6b7280; font-size: 14px; }
        .unsubscribe a { color: #6b7280; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 Welcome to MYTA!</h1>
        </div>

        <div class="content">
            <h2>Hi${data.name ? ` ${data.name}` : ""}!</h2>

            <p>Thanks for joining the MYTA waitlist! You're among the first to discover our revolutionary AI-powered YouTube content creation platform.</p>

            <h3>🤖 What is MYTA?</h3>
            <p>MYTA is your AI-powered YouTube Agent Team that handles everything from content ideation to optimization, letting you focus on what you do best - creating amazing content.</p>

            <h3>🎯 What's Next?</h3>
            <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                • We'll keep you updated on our development progress<br>
                • You'll get exclusive early access when we launch<br>
                • Special founder pricing just for waitlist members
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="https://x.com/myytagent" class="btn" style="margin-right: 10px;">Follow Us on X</a>
                <a href="https://youtube.com/@myytagent" class="btn" style="background: #ff0000 !important;">Subscribe on YouTube</a>
            </div>

            <p>Questions? Just reply to this email - we read every message!</p>

            <p>Best regards,<br><strong>The MYTA Team</strong></p>
        </div>

        <div class="footer">
            <p>© 2024 MYTA. All rights reserved.</p>
            <p class="unsubscribe">
                Don't want these emails? <a href="${
                  process.env.VERCEL_URL || "https://earlyaccess.myytagent.app"
                }/api/unsubscribe?id=${data.waitlist_id}">Unsubscribe</a>
            </p>
        </div>
    </div>
</body>
</html>`,
    text: (data) => `
🎬 Welcome to MYTA!

Hi${data.name ? ` ${data.name}` : ""}!

Thanks for joining the MYTA waitlist! You're among the first to discover our revolutionary AI-powered YouTube content creation platform.

🤖 What is MYTA?
MYTA is your AI-powered YouTube Agent Team that handles everything from content ideation to optimization, letting you focus on what you do best - creating amazing content.

🎯 What's Next?
• We'll keep you updated on our development progress
• You'll get exclusive early access when we launch
• Special founder pricing just for waitlist members

Follow us: 
• X (Twitter): https://x.com/myytagent
• YouTube: https://youtube.com/@myytagent

Questions? Just reply to this email - we read every message!

Best regards,
The MYTA Team

---
© 2024 MYTA. All rights reserved.
Unsubscribe: ${
      process.env.VERCEL_URL || "https://earlyaccess.myytagent.app"
    }/api/unsubscribe?id=${data.waitlist_id}
`,
  },
};

async function testUpdatedEmail() {
  try {
    console.log("🧪 Testing updated email template with YouTube link...");
    
    const testData = {
      waitlist_id: "test-123",
      name: "Test User"
    };

    const emailTemplate = templates.welcome;
    
    console.log("📤 Sending test email...");
    
    const { data, error } = await resend.emails.send({
      from: "MYTA Team <noreply@myytagent.app>",
      to: ["darren.berich@me.com"],
      subject: emailTemplate.subject,
      html: emailTemplate.html(testData),
      text: emailTemplate.text(testData),
    });

    if (error) {
      console.error("❌ Resend error:", error);
      return;
    }

    console.log("✅ Email sent successfully!");
    console.log(`📧 Email ID: ${data.id}`);
    console.log("📋 Email includes both X and YouTube links");
    
  } catch (error) {
    console.error("❌ Error:", error);
  }
}

testUpdatedEmail();
