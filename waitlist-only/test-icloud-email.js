import dotenv from "dotenv";
import nodemailer from "nodemailer";

// Load environment variables
dotenv.config();

async function testICloudEmail() {
  console.log("🧪 Testing iCloud Email Setup...\n");

  // Check environment variables
  if (!process.env.ICLOUD_EMAIL) {
    console.error("❌ ICLOUD_EMAIL not set in .env file");
    return;
  }

  if (!process.env.ICLOUD_APP_PASSWORD) {
    console.error("❌ ICLOUD_APP_PASSWORD not set in .env file");
    console.log(
      "📝 You need to create an App Password at: https://appleid.apple.com"
    );
    return;
  }

  console.log(`📧 Using email: ${process.env.ICLOUD_EMAIL}`);
  console.log(
    `🔑 App password: ${process.env.ICLOUD_APP_PASSWORD.substring(0, 4)}****\n`
  );

  // Create transporter - try different iCloud SMTP settings
  const transporter = nodemailer.createTransport({
    host: "smtp.mail.me.com",
    port: 587,
    secure: false,
    requireTLS: true,
    auth: {
      user: process.env.ICLOUD_EMAIL,
      pass: process.env.ICLOUD_APP_PASSWORD,
    },
    tls: {
      ciphers: "SSLv3",
    },
  });

  try {
    // Test connection
    console.log("🔌 Testing SMTP connection...");
    await transporter.verify();
    console.log("✅ SMTP connection successful!\n");

    // Send test email
    console.log("📤 Sending test email...");
    const info = await transporter.sendMail({
      from: `"MYTA Team" <${process.env.ICLOUD_EMAIL}>`,
      to: process.env.ICLOUD_EMAIL, // Send to yourself for testing
      subject: "🧪 MYTA Email Test - Success!",
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
          <h1 style="color: #f97316;">🎉 Email Test Successful!</h1>
          <p>Your iCloud email setup is working perfectly!</p>
          <p><strong>From:</strong> ${process.env.ICLOUD_EMAIL}</p>
          <p><strong>Time:</strong> ${new Date().toLocaleString()}</p>
          <div style="background: #f0fdf4; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <p style="margin: 0; color: #16a34a;"><strong>✅ Ready for production!</strong></p>
          </div>
        </div>
      `,
      text: `
🎉 Email Test Successful!

Your iCloud email setup is working perfectly!

From: ${process.env.ICLOUD_EMAIL}
Time: ${new Date().toLocaleString()}

✅ Ready for production!
      `,
    });

    console.log("✅ Test email sent successfully!");
    console.log(`📧 Message ID: ${info.messageId}`);
    console.log(`📬 Check your inbox: ${process.env.ICLOUD_EMAIL}\n`);

    console.log("🚀 Your email system is ready to use!");
  } catch (error) {
    console.error("❌ Email test failed:", error.message);

    if (error.code === "EAUTH") {
      console.log("\n💡 Authentication failed. Please check:");
      console.log("1. Your iCloud email address is correct");
      console.log(
        "2. You created an App Password at: https://appleid.apple.com"
      );
      console.log("3. Two-factor authentication is enabled on your Apple ID");
      console.log("4. The App Password is entered correctly (no spaces)");
    }
  }
}

testICloudEmail();
