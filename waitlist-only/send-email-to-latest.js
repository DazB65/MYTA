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
  // .env.local doesn't exist, use process.env
}

const supabase = createClient(
  envVars.VITE_SUPABASE_URL || process.env.VITE_SUPABASE_URL,
  envVars.VITE_SUPABASE_ANON_KEY || process.env.VITE_SUPABASE_ANON_KEY
);

async function sendEmailToLatestSignup() {
  console.log("🔍 Finding the latest waitlist signup...\n");

  try {
    // Get the most recent signup
    const { data: latestSignup, error: fetchError } = await supabase
      .from("waitlist")
      .select("*")
      .order("created_at", { ascending: false })
      .limit(1)
      .single();

    if (fetchError) {
      console.error("❌ Error fetching latest signup:", fetchError.message);
      return;
    }

    if (!latestSignup) {
      console.log("❌ No signups found in the database.");
      return;
    }

    console.log("✅ Latest signup found:");
    console.log(`   Email: ${latestSignup.email}`);
    console.log(`   Name: ${latestSignup.name || "Not provided"}`);
    console.log(
      `   Signed up: ${new Date(latestSignup.created_at).toLocaleString()}`
    );
    console.log(
      `   Previous welcome email sent: ${
        latestSignup.welcome_email_sent ? "✅ Yes" : "❌ No"
      }`
    );
    console.log("");

    // Send welcome email using the corrected API
    console.log("📧 Sending welcome email...");

    const emailPayload = {
      email: latestSignup.email,
      template: "welcome",
      waitlist_id: latestSignup.id,
      name: latestSignup.name,
    };

    // Use the deployed Vercel API endpoint
    const emailResponse = await fetch(
      "https://earlyaccess.myytagent.app/api/send-email",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(emailPayload),
      }
    );

    if (emailResponse.ok) {
      const result = await emailResponse.json();
      console.log("✅ Email sent successfully!");
      console.log(`   Email ID: ${result.email_id}`);

      // Update database to mark email as sent
      await supabase
        .from("waitlist")
        .update({
          welcome_email_sent: true,
          welcome_email_sent_at: new Date().toISOString(),
        })
        .eq("id", latestSignup.id);

      console.log("✅ Database updated with email status");
    } else {
      const errorText = await emailResponse.text();
      console.error("❌ Failed to send email:", errorText);
    }
  } catch (error) {
    console.error("❌ Error:", error.message);
  }
}

// Main execution
sendEmailToLatestSignup().catch(console.error);
