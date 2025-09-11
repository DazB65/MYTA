// Test the deployed API to see what's happening
async function testDeployedAPI() {
  console.log("🧪 Testing Deployed Waitlist API...\n");

  const testData = {
    email: "test-" + Date.now() + "@example.com", // Using a unique test email
    youtube_channel_name: "Test Channel",
    subscriber_range: "1k-10k",
    signup_source: "landing_page",
  };

  try {
    console.log("📤 Testing waitlist signup...");
    console.log("Data:", JSON.stringify(testData, null, 2));

    const response = await fetch(
      "https://myta-waitlist.vercel.app/api/waitlist",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(testData),
      }
    );

    console.log(
      `\n📥 Response Status: ${response.status} ${response.statusText}`
    );

    const responseText = await response.text();
    console.log("📄 Response Body:", responseText);

    if (response.ok) {
      try {
        const responseData = JSON.parse(responseText);
        console.log(
          "✅ Parsed Response:",
          JSON.stringify(responseData, null, 2)
        );

        // If successful, check if email was sent
        if (responseData.waitlist_id) {
          console.log("\n📧 Testing email sending directly...");
          await testEmailEndpoint(responseData.waitlist_id);
        }
      } catch (e) {
        console.log("⚠️  Response is not valid JSON");
      }
    } else {
      console.log("❌ Waitlist API request failed");
    }
  } catch (error) {
    console.error("❌ Error testing waitlist API:", error.message);
  }
}

async function testEmailEndpoint(waitlistId) {
  const emailData = {
    email: "myytagent@icloud.com",
    template: "welcome",
    waitlist_id: waitlistId,
    name: "Test User",
  };

  try {
    const response = await fetch(
      "https://myta-waitlist.vercel.app/api/send-email",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(emailData),
      }
    );

    console.log(
      `📧 Email API Status: ${response.status} ${response.statusText}`
    );

    const responseText = await response.text();
    console.log("📧 Email API Response:", responseText);

    if (response.ok) {
      console.log("✅ Email sent successfully!");
    } else {
      console.log("❌ Email sending failed");
    }
  } catch (error) {
    console.error("❌ Error testing email endpoint:", error.message);
  }
}

testDeployedAPI().catch(console.error);
