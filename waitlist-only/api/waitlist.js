import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.VITE_SUPABASE_URL,
  process.env.VITE_SUPABASE_ANON_KEY
);

export default async function handler(req, res) {
  // Handle CORS
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader(
    "Access-Control-Allow-Methods",
    "GET, POST, PUT, DELETE, OPTIONS"
  );
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const {
      email,
      name,
      youtube_channel_name,
      youtube_channel_url,
      subscriber_count,
      subscriber_range,
      content_niche,
      signup_source = "landing_page",
      utm_source,
      utm_medium,
      utm_campaign,
      referral_code,
    } = req.body;

    // Validate required fields
    if (!email) {
      return res.status(400).json({ error: "Email is required" });
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({ error: "Invalid email format" });
    }

    // Get client info
    const clientIP =
      req.headers["x-forwarded-for"] ||
      req.connection.remoteAddress ||
      "unknown";
    const userAgent = req.headers["user-agent"] || "";

    // Prepare waitlist data
    const waitlistData = {
      email: email.toLowerCase().trim(),
      name: name?.trim() || null,
      youtube_channel_name: youtube_channel_name?.trim() || null,
      youtube_channel_url: youtube_channel_url?.trim() || null,
      subscriber_count: subscriber_count || null,
      subscriber_range: subscriber_range || null,
      content_niche: content_niche || null,
      signup_source: signup_source,
      utm_source: utm_source || null,
      utm_medium: utm_medium || null,
      utm_campaign: utm_campaign || null,
      referral_code: referral_code || null,
      ip_address: clientIP,
      user_agent: userAgent,
      status: "active",
      created_at: new Date().toISOString(),
    };

    // Insert into database
    const { data, error } = await supabase
      .from("waitlist")
      .insert([waitlistData])
      .select();

    if (error) {
      // Handle duplicate email
      if (error.code === "23505" || error.message.includes("duplicate key")) {
        return res.status(200).json({
          success: true,
          message: "You're already on our waitlist! We'll keep you updated.",
          already_subscribed: true,
        });
      }

      console.error("Database error:", error);
      return res.status(500).json({ error: "Failed to save signup" });
    }

    const waitlistId = data[0].id;

    // Send welcome email
    try {
      const emailResponse = await fetch(
        "https://waitlist.myytagent.app/api/send-email",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email,
            template: "welcome",
            waitlist_id: waitlistId,
            name: name,
          }),
        }
      );

      if (emailResponse.ok) {
        // Update database to mark email as sent
        await supabase
          .from("waitlist")
          .update({
            welcome_email_sent: true,
            welcome_email_sent_at: new Date().toISOString(),
          })
          .eq("id", waitlistId);
      } else {
        console.error(
          "Failed to send welcome email:",
          await emailResponse.text()
        );
      }
    } catch (emailError) {
      console.error("Email sending error:", emailError);
      // Don't fail the signup if email fails
    }

    return res.status(200).json({
      success: true,
      message:
        "Successfully joined the waitlist! Check your email for a welcome message.",
      waitlist_id: waitlistId,
    });
  } catch (error) {
    console.error("Waitlist signup error:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
}
