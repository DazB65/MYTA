import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "fs";

// Load environment variables from .env.local if it exists
let envVars = {};
try {
  const envContent = readFileSync(".env.local", "utf8");
  envContent.split("\n").forEach((line) => {
    const [key, value] = line.split("=");
    if (key && value) {
      envVars[key.trim()] = value.trim();
    }
  });
} catch (error) {
  console.log("No .env.local file found, using environment variables");
}

// Initialize Supabase client
const supabase = createClient(
  envVars.VITE_SUPABASE_URL || process.env.VITE_SUPABASE_URL,
  envVars.VITE_SUPABASE_ANON_KEY || process.env.VITE_SUPABASE_ANON_KEY
);

async function checkSpecificEmail(email) {
  console.log(`🔍 Checking if ${email} is on the waitlist...`);

  try {
    const { data, error } = await supabase
      .from("waitlist")
      .select("*")
      .eq("email", email)
      .single();

    if (error) {
      if (error.code === "PGRST116") {
        console.log(`❌ ${email} is NOT on the waitlist`);
        return false;
      }
      throw error;
    }

    console.log(`✅ ${email} IS on the waitlist!`);
    console.log(`📋 Details:`);
    console.log(`   Name: ${data.name}`);
    console.log(`   Signed up: ${new Date(data.created_at).toLocaleString()}`);
    console.log(
      `   Welcome email sent: ${data.welcome_email_sent ? "✅ Yes" : "❌ No"}`
    );
    console.log(`   Status: ${data.status}`);
    console.log(
      `   YouTube Channel: ${data.youtube_channel_name || "Not provided"}`
    );
    console.log(
      `   Subscriber Range: ${data.subscriber_range || "Not provided"}`
    );
    console.log(`   Content Niche: ${data.content_niche || "Not provided"}`);

    return true;
  } catch (error) {
    console.error("❌ Error checking email:", error.message);
    return false;
  }
}

// Get email from command line argument or use default
const emailToCheck = process.argv[2] || "myytagent@icloud.com";

checkSpecificEmail(emailToCheck);
