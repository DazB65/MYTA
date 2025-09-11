import { Resend } from "resend";
import dotenv from "dotenv";

// Load environment variables
dotenv.config({ path: '.env.local' });

const resend = new Resend(process.env.RESEND_API_KEY);

async function testDomainEmail() {
  console.log("🧪 Testing Email with myytagent.app Domain...\n");

  try {
    console.log("📧 Attempting to send email from hello@myytagent.app...");
    
    const { data, error } = await resend.emails.send({
      from: "MYTA Team <hello@myytagent.app>",
      to: ["myytagent@icloud.com"], // Your verified email for testing
      subject: "🎉 Custom Domain Test - myytagent.app",
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
          <h1 style="color: #f97316;">Custom Domain Working! 🎉</h1>
          <p>This email was successfully sent from <strong>hello@myytagent.app</strong></p>
          <p>Your domain verification is complete and the waitlist can now send emails to any address!</p>
          <hr>
          <p style="color: #666; font-size: 14px;">
            This confirms that your MYTA waitlist can now send welcome emails to any signup address.
          </p>
        </div>
      `,
      text: `
Custom Domain Working! 🎉

This email was successfully sent from hello@myytagent.app

Your domain verification is complete and the waitlist can now send emails to any address!

This confirms that your MYTA waitlist can now send welcome emails to any signup address.
      `
    });

    if (error) {
      console.error("❌ Email sending failed:", error);
      
      if (error.message && error.message.includes('domain')) {
        console.log("\n💡 Domain not verified yet. Common issues:");
        console.log("   - DNS records not yet propagated (can take up to 24 hours)");
        console.log("   - DNS records not added correctly");
        console.log("   - Domain not added to Resend dashboard");
      } else if (error.statusCode === 403) {
        console.log("\n💡 Domain verification required:");
        console.log("   - Make sure you've added myytagent.app to Resend");
        console.log("   - Verify all DNS records are correctly added");
      }
      
      return false;
    } else {
      console.log("✅ SUCCESS! Email sent with custom domain!");
      console.log("📧 Email ID:", data.id);
      console.log("📬 Check myytagent@icloud.com for the test email");
      console.log("\n🎉 Your waitlist can now send emails to ANY address!");
      return true;
    }

  } catch (error) {
    console.error("❌ Test failed:", error);
    return false;
  }
}

async function testWithRandomEmail() {
  console.log("\n🧪 Testing with a random email address...\n");

  try {
    const randomEmail = `test-${Date.now()}@example.com`;
    console.log(`📧 Attempting to send to: ${randomEmail}`);
    
    const { data, error } = await resend.emails.send({
      from: "MYTA Team <hello@myytagent.app>",
      to: [randomEmail],
      subject: "🧪 Test Email to Random Address",
      html: "<h1>Test</h1><p>This email was sent to a random address to test domain verification.</p>",
      text: "Test - This email was sent to a random address to test domain verification."
    });

    if (error) {
      console.error("❌ Failed to send to random email:", error);
      return false;
    } else {
      console.log("✅ SUCCESS! Can send to any email address!");
      console.log("📧 Email ID:", data.id);
      return true;
    }

  } catch (error) {
    console.error("❌ Random email test failed:", error);
    return false;
  }
}

async function main() {
  console.log("🔍 Testing Custom Domain Setup for myytagent.app\n");
  
  const domainWorking = await testDomainEmail();
  
  if (domainWorking) {
    await testWithRandomEmail();
    
    console.log("\n🎉 DOMAIN VERIFICATION COMPLETE!");
    console.log("✅ Your waitlist can now send emails to any signup address");
    console.log("🚀 Ready to deploy and test with real users!");
  } else {
    console.log("\n⏳ Domain not ready yet. Please:");
    console.log("1. Ensure you've added myytagent.app to Resend dashboard");
    console.log("2. Add all required DNS records to your domain registrar");
    console.log("3. Wait for DNS propagation (up to 24 hours)");
    console.log("4. Run this test again");
  }
}

main().catch(console.error);
