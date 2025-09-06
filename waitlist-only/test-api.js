// Test the waitlist API endpoint directly
async function testWaitlistAPI() {
  console.log("🧪 Testing Waitlist API Endpoint...\n");

  const testData = {
    email: "test2@example.com",
    name: "Test User 2",
    youtube_channel_name: "Test Channel 2",
    subscriber_range: "1k-10k",
    content_niche: "tech",
    signup_source: "landing_page",
  };

  try {
    console.log("📤 Sending test signup...");
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
      } catch (e) {
        console.log("⚠️  Response is not valid JSON");
      }
    } else {
      console.log("❌ API request failed");
    }
  } catch (error) {
    console.error("❌ Error testing API:", error.message);
  }
}

// Test with a real email (replace with your email)
async function testWithRealEmail(email) {
  console.log(`\n🧪 Testing with real email: ${email}...\n`);

  const testData = {
    email: email,
    name: "Test User",
    youtube_channel_name: "My Channel",
    subscriber_range: "1k-10k",
    content_niche: "tech",
    signup_source: "api_test",
  };

  try {
    console.log("📤 Sending real signup...");

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

        if (responseData.success) {
          console.log(
            "\n🎉 SUCCESS! Your email should now be in the waitlist."
          );
          console.log("💡 Run the check-waitlist.js script again to verify.");
        }
      } catch (e) {
        console.log("⚠️  Response is not valid JSON");
      }
    } else {
      console.log("❌ API request failed");
    }
  } catch (error) {
    console.error("❌ Error testing API:", error.message);
  }
}

// Main execution
async function main() {
  await testWaitlistAPI();

  // Uncomment and replace with your email to test:
  // await testWithRealEmail("your-email@example.com");

  console.log(
    "\n💡 To test with your real email, uncomment the testWithRealEmail line above."
  );
}

main().catch(console.error);
