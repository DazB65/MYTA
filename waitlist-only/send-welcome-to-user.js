import { createClient } from "@supabase/supabase-js";
import dotenv from "dotenv";

// Load environment variables
dotenv.config({ path: ".env.local" });

const supabase = createClient(
  process.env.VITE_SUPABASE_URL,
  process.env.VITE_SUPABASE_ANON_KEY
);

async function sendWelcomeToUser(email) {
  try {
    console.log(`🔍 Looking for user: ${email}`);

    // Find the user in the waitlist
    const { data: users, error } = await supabase
      .from("waitlist")
      .select("*")
      .eq("email", email)
      .eq("status", "active");

    if (error) {
      console.error("❌ Database error:", error);
      return;
    }

    if (!users || users.length === 0) {
      console.log("❌ User not found in waitlist");
      return;
    }

    const user = users[0];
    console.log("✅ User found:");
    console.log(`   Email: ${user.email}`);
    console.log(`   Name: ${user.name || "Not provided"}`);
    console.log(`   Signed up: ${new Date(user.created_at).toLocaleString()}`);
    console.log(
      `   Welcome email sent: ${user.welcome_email_sent ? "✅ Yes" : "❌ No"}`
    );

    if (user.welcome_email_sent) {
      console.log("⚠️  Welcome email already sent to this user");
      return;
    }

    console.log("");
    console.log("📧 Sending welcome email...");

    const emailPayload = {
      email: user.email,
      template: "welcome",
      waitlist_id: user.id,
      name: user.name,
    };

    // Send email using the deployed API
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
      const emailResult = await emailResponse.json();
      console.log("✅ Email sent successfully!");
      console.log(`📧 Email ID: ${emailResult.email_id}`);

      // Update database to mark email as sent
      const { error: updateError } = await supabase
        .from("waitlist")
        .update({
          welcome_email_sent: true,
          welcome_email_sent_at: new Date().toISOString(),
        })
        .eq("id", user.id);

      if (updateError) {
        console.error("⚠️  Failed to update database:", updateError);
      } else {
        console.log("✅ Database updated successfully");
      }
    } else {
      const errorText = await emailResponse.text();
      console.error("❌ Failed to send email:", errorText);
    }
  } catch (error) {
    console.error("❌ Error:", error);
  }
}

// Get email from command line argument or use default
const userEmail = process.argv[2] || "darren.berich@me.com";
sendWelcomeToUser(userEmail);
