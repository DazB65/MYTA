import { createClient } from "@supabase/supabase-js";

// Load environment variables from .env.local if it exists
import { readFileSync } from "fs";

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

async function checkWaitlist() {
  console.log("🔍 Checking MYTA Waitlist Database...\n");

  try {
    // Get recent signups
    console.log("📋 Recent Waitlist Signups:");
    const { data: recentSignups, error: recentError } = await supabase
      .from("waitlist")
      .select(
        "email, name, created_at, welcome_email_sent, welcome_email_sent_at, status"
      )
      .order("created_at", { ascending: false })
      .limit(10);

    if (recentError) {
      console.error("❌ Error fetching recent signups:", recentError.message);
      return;
    }

    if (recentSignups && recentSignups.length > 0) {
      recentSignups.forEach((signup, index) => {
        const emailStatus = signup.welcome_email_sent
          ? "✅ Sent"
          : "❌ Not sent";
        const sentAt = signup.welcome_email_sent_at
          ? new Date(signup.welcome_email_sent_at).toLocaleString()
          : "N/A";

        console.log(`${index + 1}. ${signup.email}`);
        console.log(`   Name: ${signup.name || "Not provided"}`);
        console.log(
          `   Signed up: ${new Date(signup.created_at).toLocaleString()}`
        );
        console.log(`   Welcome email: ${emailStatus}`);
        if (signup.welcome_email_sent_at) {
          console.log(`   Email sent at: ${sentAt}`);
        }
        console.log(`   Status: ${signup.status}`);
        console.log("");
      });
    } else {
      console.log("No signups found in the database.");
    }

    // Get total stats
    console.log("📊 Waitlist Statistics:");
    const { count: totalCount, error: countError } = await supabase
      .from("waitlist")
      .select("*", { count: "exact", head: true });

    if (countError) {
      console.error("❌ Error getting total count:", countError.message);
    } else {
      console.log(`Total signups: ${totalCount || 0}`);
    }

    // Get email stats
    const { data: emailStats, error: emailError } = await supabase
      .from("waitlist")
      .select("welcome_email_sent")
      .eq("welcome_email_sent", true);

    if (emailError) {
      console.error("❌ Error getting email stats:", emailError.message);
    } else {
      const emailsSent = emailStats ? emailStats.length : 0;
      console.log(`Welcome emails sent: ${emailsSent}`);
      console.log(
        `Email success rate: ${
          totalCount > 0 ? ((emailsSent / totalCount) * 100).toFixed(1) : 0
        }%`
      );
    }
  } catch (error) {
    console.error("❌ Error checking waitlist:", error.message);
  }
}

// Function to check a specific email
async function checkSpecificEmail(email) {
  console.log(`\n🔍 Checking specific email: ${email}`);

  try {
    const { data, error } = await supabase
      .from("waitlist")
      .select("*")
      .eq("email", email.toLowerCase().trim())
      .single();

    if (error) {
      if (error.code === "PGRST116") {
        console.log("❌ Email not found in waitlist");
        return false;
      } else {
        console.error("❌ Error checking email:", error.message);
        return false;
      }
    }

    if (data) {
      console.log("✅ Email found in waitlist!");
      console.log(`   Name: ${data.name || "Not provided"}`);
      console.log(
        `   Signed up: ${new Date(data.created_at).toLocaleString()}`
      );
      console.log(
        `   Welcome email sent: ${data.welcome_email_sent ? "✅ Yes" : "❌ No"}`
      );
      if (data.welcome_email_sent_at) {
        console.log(
          `   Email sent at: ${new Date(
            data.welcome_email_sent_at
          ).toLocaleString()}`
        );
      }
      console.log(`   Status: ${data.status}`);
      console.log(
        `   YouTube Channel: ${data.youtube_channel_name || "Not provided"}`
      );
      console.log(`   Content Niche: ${data.content_niche || "Not provided"}`);
      console.log(
        `   Subscriber Range: ${data.subscriber_range || "Not provided"}`
      );
      return true;
    }
  } catch (error) {
    console.error("❌ Error checking specific email:", error.message);
    return false;
  }
}

// Main execution
async function main() {
  await checkWaitlist();

  // If you want to check a specific email, uncomment and modify this line:
  // await checkSpecificEmail("your-email@example.com");

  console.log(
    "\n💡 To check your specific email, modify the script and uncomment the checkSpecificEmail line."
  );
  console.log(
    "💡 If your email is in the list but no welcome email was sent, there might be an issue with the email service."
  );
}

main().catch(console.error);
