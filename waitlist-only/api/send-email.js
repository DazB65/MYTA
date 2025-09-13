import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

// Email templates
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
        .feature { margin: 20px 0; padding: 15px; background: #fef3e2; border-left: 4px solid #f97316; border-radius: 6px; }
        .btn { display: inline-block; background: #f97316; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: 600; margin: 10px 5px; }
        .footer { background: #f8fafc; padding: 30px; text-align: center; color: #64748b; font-size: 14px; }
        .unsubscribe { color: #94a3b8; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 Welcome to MYTA!</h1>
            <p>You're now on the waitlist for the future of YouTube content creation</p>
        </div>

        <div class="content">
            <h2>Thanks for joining us! 🚀</h2>

            <p>Hi${data.name ? ` ${data.name}` : ""}!</p>

            <p>We're thrilled to have you on the MYTA waitlist! You're among the first to discover our revolutionary AI-powered YouTube content creation platform.</p>

            <div class="feature">
                <strong>🤖 What is MYTA?</strong><br>
                MYTA is your AI-powered YouTube Agent Team that handles everything from content ideation to optimization, letting you focus on what you do best - creating amazing content.
            </div>

            <div class="feature">
                <strong>🎯 What's Next?</strong><br>
                • We'll keep you updated on our development progress<br>
                • You'll get exclusive early access when we launch<br>
                • Special founder pricing just for waitlist members
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="https://x.com/myytagent" class="btn">Follow Us on X</a>
            </div>

            <p>Questions? Just reply to this email - we read every message!</p>

            <p>Best regards,<br><strong>The MYTA Team</strong></p>
        </div>

        <div class="footer">
            <p>© 2024 MYTA. All rights reserved.</p>
            <p class="unsubscribe">
                Don't want these emails? <a href="${
                  process.env.VERCEL_URL || "https://myta-waitlist.vercel.app"
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

Follow us: https://x.com/myytagent

Questions? Just reply to this email - we read every message!

Best regards,
The MYTA Team

---
© 2024 MYTA. All rights reserved.
Unsubscribe: ${
      process.env.VERCEL_URL || "https://myta-waitlist.vercel.app"
    }/api/unsubscribe?id=${data.waitlist_id}
`,
  },

  update: {
    subject: "🔥 MYTA Development Update - We're Getting Closer!",
    html: (data) => `
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MYTA Development Update</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8fafc; }
        .container { max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
        .header { background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 40px 30px; text-align: center; }
        .header h1 { margin: 0; font-size: 28px; font-weight: 700; }
        .content { padding: 40px 30px; }
        .content h2 { color: #3b82f6; margin-top: 0; }
        .progress { background: #eff6ff; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .progress-bar { background: #e5e7eb; height: 8px; border-radius: 4px; overflow: hidden; }
        .progress-fill { background: #3b82f6; height: 100%; width: 75%; border-radius: 4px; }
        .feature { margin: 20px 0; padding: 15px; background: #fef3e2; border-left: 4px solid #f97316; border-radius: 6px; }
        .btn { display: inline-block; background: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: 600; margin: 10px 5px; }
        .footer { background: #f8fafc; padding: 30px; text-align: center; color: #64748b; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 Development Update</h1>
            <p>MYTA is taking shape - here's what we've been building</p>
        </div>

        <div class="content">
            <h2>We're Making Great Progress! 🚀</h2>

            <p>Hi${data.name ? ` ${data.name}` : ""}!</p>

            <p>We wanted to share some exciting updates on MYTA's development. Our AI agents are getting smarter every day!</p>

            <div class="progress">
                <h3>Development Progress</h3>
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <p><strong>75% Complete</strong> - We're in the final stretch!</p>
            </div>

            <div class="feature">
                <strong>✅ What's Ready:</strong><br>
                • AI Content Ideation Engine<br>
                • YouTube Analytics Integration<br>
                • Automated Thumbnail Generation<br>
                • Content Calendar Management
            </div>

            <div class="feature">
                <strong>🔨 Currently Building:</strong><br>
                • Advanced Video Optimization<br>
                • Multi-Agent Collaboration<br>
                • Custom Brand Voice Training<br>
                • Performance Prediction Models
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="https://x.com/myytagent" class="btn">Follow Us on X</a>
            </div>

            <p><strong>Early Access Coming Soon!</strong> Waitlist members will get first access in the next few weeks.</p>

            <p>Stay tuned for more updates!</p>

            <p>Best regards,<br><strong>The MYTA Team</strong></p>
        </div>

        <div class="footer">
            <p>© 2024 MYTA. All rights reserved.</p>
            <p class="unsubscribe">
                <a href="${
                  process.env.VERCEL_URL || "https://myta-waitlist.vercel.app"
                }/api/unsubscribe?id=${data.waitlist_id}">Unsubscribe</a>
            </p>
        </div>
    </div>
</body>
</html>`,
    text: (data) => `
🔥 MYTA Development Update

Hi${data.name ? ` ${data.name}` : ""}!

We wanted to share some exciting updates on MYTA's development. Our AI agents are getting smarter every day!

Development Progress: 75% Complete - We're in the final stretch!

✅ What's Ready:
• AI Content Ideation Engine
• YouTube Analytics Integration
• Automated Thumbnail Generation
• Content Calendar Management

🔨 Currently Building:
• Advanced Video Optimization
• Multi-Agent Collaboration
• Custom Brand Voice Training
• Performance Prediction Models

Early Access Coming Soon! Waitlist members will get first access in the next few weeks.

Follow us: https://x.com/myytagent

Stay tuned for more updates!

Best regards,
The MYTA Team

---
© 2024 MYTA. All rights reserved.
Unsubscribe: ${
      process.env.VERCEL_URL || "https://myta-waitlist.vercel.app"
    }/api/unsubscribe?id=${data.waitlist_id}
`,
  },

  early_access: {
    subject: "🎊 Your MYTA Early Access is Ready!",
    html: (data) => `
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MYTA Early Access</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8fafc; }
        .container { max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
        .header { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 40px 30px; text-align: center; }
        .header h1 { margin: 0; font-size: 28px; font-weight: 700; }
        .content { padding: 40px 30px; }
        .content h2 { color: #10b981; margin-top: 0; }
        .access-code { background: #f0fdf4; border: 2px dashed #10b981; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0; }
        .access-code code { font-size: 24px; font-weight: bold; color: #10b981; letter-spacing: 2px; }
        .feature { margin: 20px 0; padding: 15px; background: #fef3e2; border-left: 4px solid #f97316; border-radius: 6px; }
        .btn { display: inline-block; background: #10b981; color: white; padding: 15px 30px; text-decoration: none; border-radius: 6px; font-weight: 600; margin: 10px 5px; font-size: 18px; }
        .footer { background: #f8fafc; padding: 30px; text-align: center; color: #64748b; font-size: 14px; }
        .urgent { background: #fef2f2; border: 1px solid #fecaca; padding: 15px; border-radius: 6px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎊 You're In!</h1>
            <p>Your exclusive MYTA early access is ready</p>
        </div>

        <div class="content">
            <h2>Welcome to the Future of YouTube! 🚀</h2>

            <p>Hi${data.name ? ` ${data.name}` : ""}!</p>

            <p>The moment you've been waiting for is here! As a valued waitlist member, you now have exclusive early access to MYTA.</p>

            <div class="access-code">
                <p><strong>Your Early Access Code:</strong></p>
                <code>EARLY-${
                  data.waitlist_id?.slice(-8).toUpperCase() || "ACCESS"
                }</code>
                <p><small>Use this code during signup for founder pricing</small></p>
            </div>

            <div class="urgent">
                <strong>⏰ Limited Time:</strong> Early access is limited to the first 100 waitlist members. Your spot is reserved for 48 hours.
            </div>

            <div class="feature">
                <strong>🎁 Founder Benefits:</strong><br>
                • 50% off your first year<br>
                • Priority support & feature requests<br>
                • Exclusive founder badge<br>
                • Direct access to our development team
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="https://x.com/myytagent" class="btn">Follow Us on X</a>
            </div>

            <p><strong>Need help getting started?</strong> Our team is standing by to help you set up your first AI agent team.</p>

            <p>Welcome to the MYTA family!</p>

            <p>Best regards,<br><strong>The MYTA Team</strong></p>
        </div>

        <div class="footer">
            <p>© 2024 MYTA. All rights reserved.</p>
            <p class="unsubscribe">
                <a href="${
                  process.env.VERCEL_URL || "https://myta-waitlist.vercel.app"
                }/api/unsubscribe?id=${data.waitlist_id}">Unsubscribe</a>
            </p>
        </div>
    </div>
</body>
</html>`,
    text: (data) => `
🎊 Your MYTA Early Access is Ready!

Hi${data.name ? ` ${data.name}` : ""}!

The moment you've been waiting for is here! As a valued waitlist member, you now have exclusive early access to MYTA.

Your Early Access Code: EARLY-${
      data.waitlist_id?.slice(-8).toUpperCase() || "ACCESS"
    }
Use this code during signup for founder pricing.

⏰ Limited Time: Early access is limited to the first 100 waitlist members. Your spot is reserved for 48 hours.

🎁 Founder Benefits:
• 50% off your first year
• Priority support & feature requests
• Exclusive founder badge
• Direct access to our development team

Follow us: https://x.com/myytagent

Need help getting started? Our team is standing by to help you set up your first AI agent team.

Welcome to the MYTA family!

Best regards,
The MYTA Team

---
© 2024 MYTA. All rights reserved.
Unsubscribe: ${
      process.env.VERCEL_URL || "https://myta-waitlist.vercel.app"
    }/api/unsubscribe?id=${data.waitlist_id}
`,
  },
};

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    // Debug: Check if API key is available
    console.log("RESEND_API_KEY available:", !!process.env.RESEND_API_KEY);
    console.log(
      "RESEND_API_KEY starts with re_:",
      process.env.RESEND_API_KEY?.startsWith("re_")
    );

    const { email, template, waitlist_id, name } = req.body;

    if (!email || !template || !waitlist_id) {
      return res.status(400).json({ error: "Missing required fields" });
    }

    if (!templates[template]) {
      return res.status(400).json({ error: "Invalid template" });
    }

    const templateData = { waitlist_id, name };
    const emailTemplate = templates[template];

    console.log("Attempting to send email to:", email);

    const { data, error } = await resend.emails.send({
      from: "MYTA Team <noreply@myytagent.app>", // Using verified domain
      to: [email],
      subject: emailTemplate.subject,
      html: emailTemplate.html(templateData),
      text: emailTemplate.text(templateData),
    });

    if (error) {
      console.error("Resend error:", error);
      return res
        .status(500)
        .json({ error: "Failed to send email", details: error });
    }

    console.log("Email sent successfully:", data.id);

    return res.status(200).json({
      success: true,
      message: "Email sent successfully",
      email_id: data.id,
    });
  } catch (error) {
    console.error("Email sending error:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
}
