// Test with the verified email address to see if email is actually delivered
async function testWithVerifiedEmail() {
  console.log("🧪 Testing with Verified Email Address...\n");

  // First, let's test the email endpoint directly with the verified email
  const emailData = {
    email: "myytagent@icloud.com", // The verified email address
    template: "welcome",
    waitlist_id: "test-verified-" + Date.now(),
    name: "Test User"
  };

  try {
    console.log("📧 Testing email sending to verified address...");
    console.log("Data:", JSON.stringify(emailData, null, 2));

    const response = await fetch("https://myta-waitlist.vercel.app/api/send-email", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(emailData),
    });

    console.log(`\n📥 Response Status: ${response.status} ${response.statusText}`);

    const responseText = await response.text();
    console.log("📄 Response Body:", responseText);

    if (response.ok) {
      try {
        const responseData = JSON.parse(responseText);
        console.log("✅ Parsed Response:", JSON.stringify(responseData, null, 2));
        console.log("\n🎉 Email should be delivered to myytagent@icloud.com");
        console.log("📧 Check your email inbox!");
      } catch (e) {
        console.log("⚠️  Response is not valid JSON");
      }
    } else {
      console.log("❌ Email API request failed");
      console.log("This might indicate environment variables are not set correctly in deployment");
    }
  } catch (error) {
    console.error("❌ Error testing email API:", error.message);
  }
}

// Also test what happens when we try to send to an unverified email
async function testWithUnverifiedEmail() {
  console.log("\n🧪 Testing with Unverified Email Address...\n");

  const emailData = {
    email: "test@example.com", // Unverified email
    template: "welcome",
    waitlist_id: "test-unverified-" + Date.now(),
    name: "Test User"
  };

  try {
    console.log("📧 Testing email sending to unverified address...");
    console.log("Data:", JSON.stringify(emailData, null, 2));

    const response = await fetch("https://myta-waitlist.vercel.app/api/send-email", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(emailData),
    });

    console.log(`\n📥 Response Status: ${response.status} ${response.statusText}`);

    const responseText = await response.text();
    console.log("📄 Response Body:", responseText);

    if (!response.ok) {
      console.log("❌ Expected failure - Resend only allows sending to verified emails in testing mode");
    }
  } catch (error) {
    console.error("❌ Error testing email API:", error.message);
  }
}

async function main() {
  await testWithVerifiedEmail();
  await testWithUnverifiedEmail();
  
  console.log("\n📋 Summary:");
  console.log("- If the verified email test succeeded, the deployment is working correctly");
  console.log("- The issue is that Resend is in testing mode and only sends to myytagent@icloud.com");
  console.log("- To fix this, you need to verify a domain in Resend or upgrade your account");
}

main().catch(console.error);
