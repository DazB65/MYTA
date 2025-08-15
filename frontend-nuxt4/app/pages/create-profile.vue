<template>
  <div
    style="
      min-height: 100vh;
      background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 30%, #3730a3 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 40px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    "
  >
    <!-- Main Container -->
    <div
      style="
        background: #ffffff;
        border-radius: 24px;
        width: 100%;
        max-width: 1200px;
        height: 700px;
        display: grid;
        grid-template-columns: 45% 55%;
        overflow: hidden;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
      "
    >
      <!-- Left Side: Form -->
      <div style="background: white; padding: 40px; display: flex; flex-direction: column">
        <!-- Header -->
        <div style="margin-bottom: 32px">
          <button
            style="
              background: none;
              border: none;
              color: #6b7280;
              cursor: pointer;
              margin-bottom: 20px;
              font-size: 14px;
              display: flex;
              align-items: center;
              gap: 8px;
              padding: 0;
            "
          >
            ← Back
          </button>
          <h1
            style="
              font-size: 28px;
              font-weight: 700;
              color: #111827;
              margin: 0 0 8px 0;
              line-height: 1.2;
            "
          >
            Welcome to <span style="color: #ec4899">✨Vidalytics</span>
          </h1>
          <p style="color: #6b7280; font-size: 16px; margin: 0; line-height: 1.5">
            Let's set up your channel profile to get personalized AI assistance
          </p>
        </div>

        <!-- Form Fields -->
        <div style="display: flex; flex-direction: column; gap: 20px; flex: 1">
          <!-- What drives you -->
          <div>
            <label
              style="
                display: block;
                font-size: 13px;
                font-weight: 600;
                color: #374151;
                margin-bottom: 8px;
              "
            >
              WHAT DRIVES YOU AS A YOUTUBER?
            </label>
            <textarea
              v-model="formData.motivation"
              style="
                width: 100%;
                padding: 12px 16px;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                font-size: 14px;
                resize: none;
                height: 70px;
                font-family: inherit;
                background: #ffffff;
              "
              placeholder="Share what motivates you to create content..."
            />
          </div>

          <!-- Two Column Layout -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px">
            <!-- Niche -->
            <div>
              <label
                style="
                  display: block;
                  font-size: 13px;
                  font-weight: 600;
                  color: #374151;
                  margin-bottom: 8px;
                "
              >
                NICHE
              </label>
              <select
                v-model="formData.niche"
                style="
                  width: 100%;
                  padding: 12px 16px;
                  border: 1px solid #d1d5db;
                  border-radius: 8px;
                  font-size: 14px;
                  background: #ffffff;
                "
              >
                <option value="">Select</option>
                <option value="gaming">Gaming</option>
                <option value="lifestyle">Lifestyle</option>
                <option value="education">Education</option>
                <option value="tech">Technology</option>
              </select>
            </div>

            <!-- Content Type -->
            <div>
              <label
                style="
                  display: block;
                  font-size: 13px;
                  font-weight: 600;
                  color: #374151;
                  margin-bottom: 8px;
                "
              >
                CONTENT TYPE
              </label>
              <select
                v-model="formData.contentType"
                style="
                  width: 100%;
                  padding: 12px 16px;
                  border: 1px solid #d1d5db;
                  border-radius: 8px;
                  font-size: 14px;
                  background: #ffffff;
                "
              >
                <option value="">Select</option>
                <option value="tutorials">Tutorials</option>
                <option value="vlogs">Vlogs</option>
                <option value="reviews">Reviews</option>
              </select>
            </div>
          </div>

          <!-- Two Column Layout 2 -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px">
            <!-- Upload Frequency -->
            <div>
              <label
                style="
                  display: block;
                  font-size: 13px;
                  font-weight: 600;
                  color: #374151;
                  margin-bottom: 8px;
                "
              >
                UPLOAD FREQUENCY
              </label>
              <select
                v-model="formData.uploadFrequency"
                style="
                  width: 100%;
                  padding: 12px 16px;
                  border: 1px solid #d1d5db;
                  border-radius: 8px;
                  font-size: 14px;
                  background: #ffffff;
                "
              >
                <option value="">Select</option>
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </div>

            <!-- Target Goal -->
            <div>
              <label
                style="
                  display: block;
                  font-size: 13px;
                  font-weight: 600;
                  color: #374151;
                  margin-bottom: 8px;
                "
              >
                TARGET GOAL
              </label>
              <select
                v-model="formData.targetGoal"
                style="
                  width: 100%;
                  padding: 12px 16px;
                  border: 1px solid #d1d5db;
                  border-radius: 8px;
                  font-size: 14px;
                  background: #ffffff;
                "
              >
                <option value="">Select</option>
                <option value="monetization">Monetization</option>
                <option value="growth">Channel Growth</option>
                <option value="engagement">Audience Engagement</option>
                <option value="brand">Brand Building</option>
              </select>
            </div>
          </div>

          <!-- Additional Notes -->
          <div>
            <label
              style="
                display: block;
                font-size: 13px;
                font-weight: 600;
                color: #374151;
                margin-bottom: 8px;
              "
            >
              ADDITIONAL NOTES
            </label>
            <textarea
              v-model="formData.additionalNotes"
              style="
                width: 100%;
                padding: 12px 16px;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                font-size: 14px;
                resize: none;
                height: 60px;
                font-family: inherit;
                background: #ffffff;
              "
              placeholder="Tell us about your future plans..."
            />
          </div>
        </div>

        <!-- Connect YouTube Section -->
        <div style="margin-top: 24px; padding-top: 24px; border-top: 1px solid #e5e7eb">
          <h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 6px 0">
            Connect Your Youtube Channel
          </h3>
          <p style="font-size: 14px; color: #6b7280; margin: 0 0 16px 0; line-height: 1.4">
            Connect your YouTube account to automatically import your channel statistics
          </p>

          <button
            style="
              background: #ff0000;
              color: white;
              border: none;
              padding: 12px 20px;
              border-radius: 8px;
              font-size: 14px;
              font-weight: 600;
              cursor: pointer;
              display: flex;
              align-items: center;
              gap: 8px;
              margin-bottom: 8px;
              box-shadow: 0 2px 4px rgba(255, 0, 0, 0.2);
            "
          >
            Connect 📺 YouTube Account
          </button>
          <div style="color: #9ca3af; font-size: 12px">
            Optional, you can connect this later too
          </div>
        </div>

        <!-- Complete Setup Button -->
        <button
          style="
            width: 100%;
            background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
            color: white;
            border: none;
            padding: 16px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 700;
            margin-top: 24px;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 14px rgba(236, 72, 153, 0.3);
          "
          @click="completeSetup"
        >
          Complete Setup
        </button>
      </div>

      <!-- Right Side: AI Robot Illustration -->
      <div
        style="
          background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 30%, #3730a3 100%);
          position: relative;
          display: flex;
          align-items: center;
          justify-content: center;
          overflow: hidden;
        "
      >
        <!-- BossAgent Robot Image -->
        <div
          style="
            position: relative;
            z-index: 10;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
          "
        >
          <img
            src="/BossAgent.png"
            alt="AI Boss Agent Robot"
            style="
              width: 85%;
              height: 85%;
              object-fit: contain;
              filter: drop-shadow(0 25px 50px rgba(0, 0, 0, 0.4));
              transform: scale(1.1);
            "
          />
        </div>

        <!-- Floating UI Elements -->
        <div
          style="
            position: absolute;
            top: 15%;
            right: 10%;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(15px);
            padding: 16px 20px;
            border-radius: 16px;
            color: white;
            font-size: 13px;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
          "
        >
          📊 Channel Analytics
        </div>
        <div
          style="
            position: absolute;
            bottom: 25%;
            left: 10%;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(15px);
            padding: 16px 20px;
            border-radius: 16px;
            color: white;
            font-size: 13px;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
          "
        >
          🎯 Growth Insights
        </div>
        <div
          style="
            position: absolute;
            top: 45%;
            left: 8%;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            padding: 12px 16px;
            border-radius: 12px;
            color: white;
            font-size: 12px;
            font-weight: 500;
            border: 1px solid rgba(255, 255, 255, 0.2);
          "
        >
          📈 AI Predictions
        </div>
        <div
          style="
            position: absolute;
            top: 25%;
            right: 25%;
            background: rgba(96, 165, 250, 0.25);
            backdrop-filter: blur(10px);
            padding: 10px 14px;
            border-radius: 10px;
            color: white;
            font-size: 11px;
            font-weight: 500;
            border: 1px solid rgba(96, 165, 250, 0.3);
          "
        >
          🤖 AI Boss Agent
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Form data to match the Figma design
const formData = ref({
  motivation: '',
  niche: '',
  contentType: '',
  uploadFrequency: '',
  targetGoal: '',
  additionalNotes: '',
})

// Handle form submission
const completeSetup = () => {
  console.log('Form data:', formData.value)
  // Navigate to dashboard after setup
  navigateTo('/dashboard')
}
</script>
