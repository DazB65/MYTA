// Test the email API endpoint directly
async function testEmailAPI() {
  console.log("📧 Testing Email API Endpoint...\n");

  const testData = {
    email: "darren.berich@me.com",
    template: "welcome",
    waitlist_id: "test-id",
    name: "Test User",
  };

  try {
    console.log("📤 Sending test email...");
    console.log("Data:", JSON.stringify(testData, null, 2));

    const response = await fetch(
      "https://myta-waitlist.vercel.app/api/send-email",
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
      console.log("❌ Email API request failed");
    }
  } catch (error) {
    console.error("❌ Error testing email API:", error.message);
  }
}

testEmailAPI().catch(console.error);
