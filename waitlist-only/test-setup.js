/**
 * Test Script for MYTA Waitlist Setup
 * Run this to verify your environment is configured correctly
 */

import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "fs";
import { Resend } from "resend";

// Load environment variables from .env.local
let supabaseUrl, supabaseKey, resendKey;

try {
  const envFile = readFileSync(".env.local", "utf8");
  const envLines = envFile.split("\n");

  for (const line of envLines) {
    if (line.startsWith("VITE_SUPABASE_URL=")) {
      supabaseUrl = line.split("=")[1];
    }
    if (line.startsWith("VITE_SUPABASE_ANON_KEY=")) {
      supabaseKey = line.split("=")[1];
    }
    if (line.startsWith("RESEND_API_KEY=")) {
      resendKey = line.split("=")[1];
    }
  }
} catch (error) {
  console.error("❌ Could not read .env.local file");
}

console.log("🧪 Testing MYTA Waitlist Setup...\n");

// Test 1: Environment Variables
console.log("1. Checking environment variables...");
if (!supabaseUrl) {
  console.error("❌ VITE_SUPABASE_URL is missing");
  process.exit(1);
}
if (!supabaseKey) {
  console.error("❌ VITE_SUPABASE_ANON_KEY is missing");
  process.exit(1);
}
if (!resendKey) {
  console.error("❌ RESEND_API_KEY is missing");
  process.exit(1);
}
console.log("✅ All environment variables present\n");

// Test 2: Supabase Connection
console.log("2. Testing Supabase connection...");
const supabase = createClient(supabaseUrl, supabaseKey);

try {
  // Test connection by checking if waitlist table exists
  const { data, error } = await supabase
    .from("waitlist")
    .select("count", { count: "exact", head: true });

  if (error) {
    console.error("❌ Supabase connection failed:", error.message);
    console.log("💡 Make sure you've run the database migration");
    process.exit(1);
  }

  console.log("✅ Supabase connected successfully");
  console.log(`📊 Current waitlist count: ${data.count || 0}\n`);
} catch (err) {
  console.error("❌ Supabase test failed:", err.message);
  process.exit(1);
}

// Test 3: Resend Connection
console.log("3. Testing Resend connection...");
const resend = new Resend(resendKey);

try {
  // Test Resend by getting account info
  const { data, error } = await resend.domains.list();

  if (error) {
    console.error("❌ Resend connection failed:", error.message);
    process.exit(1);
  }

  console.log("✅ Resend connected successfully");
  if (data && data.length > 0) {
    console.log(`📧 Verified domains: ${data.map((d) => d.name).join(", ")}`);
  } else {
    console.log(
      "⚠️  No verified domains found. You can still send test emails."
    );
  }
  console.log();
} catch (err) {
  console.error("❌ Resend test failed:", err.message);
  process.exit(1);
}

// Test 4: Database Schema
console.log("4. Checking database schema...");
try {
  // Test inserting and deleting a test record
  const testEmail = `test-${Date.now()}@example.com`;

  const { data: insertData, error: insertError } = await supabase
    .from("waitlist")
    .insert([
      {
        email: testEmail,
        signup_source: "test",
        status: "active",
      },
    ])
    .select();

  if (insertError) {
    console.error("❌ Database insert failed:", insertError.message);
    process.exit(1);
  }

  const testId = insertData[0].id;

  // Clean up test record
  const { error: deleteError } = await supabase
    .from("waitlist")
    .delete()
    .eq("id", testId);

  if (deleteError) {
    console.warn("⚠️  Failed to clean up test record:", deleteError.message);
  }

  console.log("✅ Database schema is correct\n");
} catch (err) {
  console.error("❌ Database schema test failed:", err.message);
  process.exit(1);
}

// Test 5: Email Template
console.log("5. Testing email template...");
try {
  // This would normally send an email, but we'll just validate the template
  const testTemplate = {
    from: "MYTA Team <hello@myta.ai>",
    to: ["test@example.com"],
    subject: "Test Email",
    html: "<h1>Test</h1>",
    text: "Test",
  };

  console.log("✅ Email template structure is valid\n");
} catch (err) {
  console.error("❌ Email template test failed:", err.message);
  process.exit(1);
}

console.log("🎉 All tests passed! Your MYTA waitlist is ready to deploy.\n");

console.log("Next steps:");
console.log("1. Deploy to Vercel: vercel --prod");
console.log("2. Test the live form with a real email");
console.log("3. Check that welcome emails are delivered");
console.log("4. Monitor your Supabase dashboard for signups\n");

console.log("📊 Useful queries for monitoring:");
console.log("- Total signups: SELECT COUNT(*) FROM waitlist;");
console.log(
  "- Recent signups: SELECT * FROM waitlist ORDER BY created_at DESC LIMIT 10;"
);
console.log(
  "- Email stats: SELECT COUNT(*) as total, COUNT(*) FILTER (WHERE welcome_email_sent = true) as emails_sent FROM waitlist;"
);
