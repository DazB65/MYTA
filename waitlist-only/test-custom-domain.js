import { Resend } from "resend";
import dotenv from "dotenv";

// Load environment variables
dotenv.config({ path: '.env.local' });

const resend = new Resend(process.env.RESEND_API_KEY);

async function testCustomDomain() {
  console.log("🧪 Testing Custom Domain Setup...\n");

  try {
    console.log("1️⃣ Checking domain verification status...");
    
    // Check if domain is verified
    const { data: domains, error: domainError } = await resend.domains.list();
    
    if (domainError) {
      console.error("❌ Error checking domains:", domainError);
      return;
    }

    console.log("📋 Current domains:");
    if (domains && domains.length > 0) {
      domains.forEach((domain) => {
        console.log(`  - ${domain.name}: ${domain.status}`);
        if (domain.name === 'myytagent.app') {
          if (domain.status === 'verified') {
            console.log("    ✅ myytagent.app is verified!");
          } else {
            console.log("    ⚠️  myytagent.app is not yet verified");
            console.log("    📝 Make sure you've added the DNS records");
          }
        }
      });
    } else {
      console.log("  No domains found. Please add myytagent.app in Resend dashboard.");
    }

    console.log("\n2️⃣ Testing email sending with custom domain...");
    
    // Test sending email with custom domain
    const testEmail = "myytagent@icloud.com"; // Use verified email for testing
    
    const { data, error } = await resend.emails.send({
      from: "MYTA Team <hello@myytagent.app>",
      to: [testEmail],
      subject: "🧪 Test Email from Custom Domain",
      html: `
        <h1>Custom Domain Test</h1>
        <p>This email was sent from hello@myytagent.app</p>
        <p>If you receive this, your custom domain is working correctly!</p>
      `,
      text: "Custom Domain Test - This email was sent from hello@myytagent.app"
    });

    if (error) {
      console.error("❌ Email sending failed:", error);
      
      if (error.message && error.message.includes('domain')) {
        console.log("\n💡 This error suggests the domain is not verified yet.");
        console.log("   Please complete domain verification in Resend dashboard.");
      }
    } else {
      console.log("✅ Email sent successfully with custom domain!");
      console.log("📧 Email ID:", data.id);
      console.log("📬 Check myytagent@icloud.com for the test email");
    }

  } catch (error) {
    console.error("❌ Test failed:", error);
  }
}

async function showDomainSetupInstructions() {
  console.log("📋 Domain Setup Instructions:\n");
  
  console.log("1. Go to https://resend.com/domains");
  console.log("2. Click 'Add Domain'");
  console.log("3. Enter: myytagent.app");
  console.log("4. Add the DNS records Resend provides to your domain registrar");
  console.log("5. Wait for verification (can take a few minutes to 24 hours)");
  console.log("6. Run this test again to verify it's working\n");
  
  console.log("🔍 Common DNS Records you'll need to add:");
  console.log("   - TXT record for domain verification");
  console.log("   - MX record for email routing");
  console.log("   - DKIM records for authentication\n");
}

async function main() {
  await showDomainSetupInstructions();
  await testCustomDomain();
  
  console.log("\n📝 Next Steps:");
  console.log("1. Complete domain verification in Resend");
  console.log("2. Test with this script until it works");
  console.log("3. Deploy the updated code to Vercel");
  console.log("4. Test the full waitlist flow with any email address");
}

main().catch(console.error);
