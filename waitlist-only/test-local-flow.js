import { createClient } from "@supabase/supabase-js";
import dotenv from "dotenv";
import { Resend } from "resend";

// Load environment variables
dotenv.config({ path: ".env.local" });

const supabase = createClient(
  process.env.VITE_SUPABASE_URL,
  process.env.VITE_SUPABASE_ANON_KEY
);

const resend = new Resend(process.env.RESEND_API_KEY);

async function testFullWaitlistFlow() {
  console.log("🧪 Testing Full Waitlist Flow Locally...\n");

  // Test data - using the verified email address for Resend testing
  const testEmail = "myytagent@icloud.com";
  const testData = {
    email: testEmail,
    name: "Test User",
    youtube_channel_name: "Test Channel",
    subscriber_range: "1k-10k",
    content_niche: "tech",
    signup_source: "landing_page",
  };

  try {
    console.log("1️⃣ Testing Supabase connection...");

    // Test Supabase connection
    const { data: testConnection, error: connectionError } = await supabase
      .from("waitlist")
      .select("count")
      .limit(1);

    if (connectionError) {
      console.error("❌ Supabase connection failed:", connectionError);
      return;
    }
    console.log("✅ Supabase connection successful");

    console.log("\n2️⃣ Testing email sending...");

    // Test email sending
    const emailResult = await resend.emails.send({
      from: "MYTA Team <onboarding@resend.dev>",
      to: [testEmail],
      subject: "🎉 Test Welcome to MYTA Waitlist!",
      html: `
        <h1>Welcome to MYTA!</h1>
        <p>Hi Test User!</p>
        <p>This is a test email to verify the waitlist system is working.</p>
        <p>If you receive this, the email system is functioning correctly!</p>
      `,
      text: "Welcome to MYTA! This is a test email to verify the waitlist system is working.",
    });

    if (emailResult.error) {
      console.error("❌ Email sending failed:", emailResult.error);
      return;
    }

    console.log("✅ Email sent successfully!");
    console.log("📧 Email ID:", emailResult.data.id);

    console.log("\n3️⃣ Testing database insertion...");

    // Test database insertion
    const waitlistData = {
      email: testEmail,
      name: testData.name,
      youtube_channel_name: testData.youtube_channel_name,
      subscriber_range: testData.subscriber_range,
      content_niche: testData.content_niche,
      signup_source: testData.signup_source,
      ip_address: "127.0.0.1",
      user_agent: "test-agent",
      status: "active",
      welcome_email_sent: true,
      welcome_email_sent_at: new Date().toISOString(),
      created_at: new Date().toISOString(),
    };

    const { data: insertResult, error: insertError } = await supabase
      .from("waitlist")
      .upsert([waitlistData], { onConflict: "email" })
      .select();

    if (insertError) {
      console.error("❌ Database insertion failed:", insertError);
      return;
    }

    console.log("✅ Database insertion successful!");
    console.log("📊 Waitlist ID:", insertResult[0].id);

    console.log("\n🎉 Full waitlist flow test completed successfully!");
    console.log("📧 Check your email for the test message.");
  } catch (error) {
    console.error("❌ Test failed:", error);
  }
}

async function checkEnvironmentVariables() {
  console.log("🔍 Checking Environment Variables...\n");

  const requiredVars = [
    "VITE_SUPABASE_URL",
    "VITE_SUPABASE_ANON_KEY",
    "RESEND_API_KEY",
  ];

  let allPresent = true;

  requiredVars.forEach((varName) => {
    const value = process.env[varName];
    if (value) {
      console.log(`✅ ${varName}: ${value.substring(0, 20)}...`);
    } else {
      console.log(`❌ ${varName}: NOT SET`);
      allPresent = false;
    }
  });

  if (!allPresent) {
    console.log("\n❌ Some environment variables are missing!");
    console.log("Please check your .env.local file.");
    return false;
  }

  console.log("\n✅ All environment variables are set!");
  return true;
}

async function main() {
  const envOk = await checkEnvironmentVariables();
  if (envOk) {
    await testFullWaitlistFlow();
  }
}

main().catch(console.error);
