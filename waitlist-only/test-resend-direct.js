import { Resend } from "resend";

// Test Resend directly with your API key
const resend = new Resend("re_FtW9uwHE_P3NtJbmWAZumfHUNeKKHTUs9");

async function testResendDirect() {
  console.log("🧪 Testing Resend API directly...\n");

  try {
    console.log("📤 Sending simple test email...");

    const { data, error } = await resend.emails.send({
      from: "onboarding@resend.dev",
      to: ["myytagent@icloud.com"],
      subject: "Test Email from MYTA Waitlist",
      html: "<h1>Test Email</h1><p>This is a test email to verify Resend is working.</p>",
      text: "Test Email - This is a test email to verify Resend is working.",
    });

    if (error) {
      console.error("❌ Resend API Error:", error);
      return;
    }

    console.log("✅ Email sent successfully!");
    console.log("📧 Email ID:", data.id);
    console.log("📊 Response data:", JSON.stringify(data, null, 2));
  } catch (error) {
    console.error("❌ Error testing Resend:", error.message);
    console.error("Full error:", error);
  }
}

// Test getting domains
async function testResendDomains() {
  console.log("\n🌐 Checking verified domains...");

  try {
    const { data: domains, error } = await resend.domains.list();

    if (error) {
      console.error("❌ Error getting domains:", error);
      return;
    }

    console.log("📋 Verified domains:", domains);

    if (domains && domains.length > 0) {
      domains.forEach((domain) => {
        console.log(`  - ${domain.name}: ${domain.status}`);
      });
    } else {
      console.log("  No custom domains found. Using resend.dev for testing.");
    }
  } catch (error) {
    console.error("❌ Error checking domains:", error.message);
  }
}

async function main() {
  await testResendDomains();
  await testResendDirect();
}

main().catch(console.error);
