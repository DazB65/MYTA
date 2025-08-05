<template>
  <div style="background-color: #f5f5f5; min-height: 100vh; display: flex; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
    
    <!-- Left Sidebar Navigation -->
    <div style="width: 280px; background-color: #2D2D2D; height: 100vh; display: flex; flex-direction: column; position: fixed;">
      
      <!-- Logo Section -->
      <div style="padding: 24px 20px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <div style="width: 28px; height: 28px; background: linear-gradient(45deg, #FF6B9D, #FF8E8E); border-radius: 6px; display: flex; align-items: center; justify-content: center;">
            <span style="color: white; font-size: 14px; font-weight: bold;">✨</span>
          </div>
          <h1 style="font-size: 18px; font-weight: 700; color: white; margin: 0;">Vidalytics</h1>
        </div>
        <p style="font-size: 12px; color: #888; margin: 4px 0 0 0;">
          Your AI Agent for Content and Growth
        </p>
      </div>

      <!-- Main Menu -->
      <div style="padding: 0 16px; flex: 1;">
        <h3 style="font-size: 12px; font-weight: 500; color: #666; margin: 0 0 16px 8px; text-transform: uppercase; letter-spacing: 0.5px;">Main Menu</h3>
        <nav style="display: flex; flex-direction: column; gap: 4px;">
          
          <!-- Dashboard Link (Active) -->
          <a href="/dashboard" style="display: flex; align-items: center; padding: 12px 16px; color: white; background-color: #FF6B9D; border-radius: 8px; text-decoration: none; font-size: 14px; font-weight: 500;">
            <svg style="width: 18px; height: 18px; margin-right: 12px;" fill="currentColor" viewBox="0 0 20 20">
              <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
            </svg>
            Dashboard
          </a>

          <!-- Other Navigation Items -->
          <a href="#" style="display: flex; align-items: center; padding: 12px 16px; color: #999; border-radius: 8px; text-decoration: none; font-size: 14px; transition: all 0.2s;">
            <svg style="width: 18px; height: 18px; margin-right: 12px;" fill="currentColor" viewBox="0 0 20 20">
              <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"></path>
            </svg>
            Pillars
          </a>

          <a href="/videos" style="display: flex; align-items: center; padding: 12px 16px; color: #999; border-radius: 8px; text-decoration: none; font-size: 14px; transition: all 0.2s;">
            <svg style="width: 18px; height: 18px; margin-right: 12px;" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"></path>
            </svg>
            Videos
          </a>

          <a href="#" style="display: flex; align-items: center; padding: 12px 16px; color: #999; border-radius: 8px; text-decoration: none; font-size: 14px; transition: all 0.2s;">
            <svg style="width: 18px; height: 18px; margin-right: 12px;" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
            </svg>
            Content Studio
          </a>

          <a href="#" style="display: flex; align-items: center; padding: 12px 16px; color: #999; border-radius: 8px; text-decoration: none; font-size: 14px; transition: all 0.2s;">
            <svg style="width: 18px; height: 18px; margin-right: 12px;" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            AI Assistant
          </a>
        </nav>

        <!-- General Section -->
        <div style="margin-top: 32px;">
          <h3 style="font-size: 12px; font-weight: 500; color: #666; margin: 0 0 16px 8px; text-transform: uppercase; letter-spacing: 0.5px;">General</h3>
          <a href="#" style="display: flex; align-items: center; padding: 12px 16px; color: #999; border-radius: 8px; text-decoration: none; font-size: 14px;">
            <svg style="width: 18px; height: 18px; margin-right: 12px;" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"></path>
            </svg>
            Setting
          </a>
        </div>
      </div>

      <!-- User Profile at Bottom -->
      <div style="padding: 20px; border-top: 1px solid #444;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 40px; height: 40px; background: linear-gradient(45deg, #FF6B9D, #FF8E8E); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <span style="color: white; font-weight: bold; font-size: 16px;">M</span>
          </div>
          <div style="flex: 1;">
            <p style="color: #ccc; font-size: 12px; margin: 0;">Good Morning</p>
            <p style="color: white; font-weight: 600; font-size: 14px; margin: 2px 0 0 0;">MARCELINE ANDERSON!</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Area -->
    <div style="flex: 1; margin-left: 280px; padding: 24px; background-color: #f8f9fa;">
      
      <!-- Top Banner -->
      <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 16px; padding: 32px; margin-bottom: 24px; position: relative; overflow: hidden;">
        <!-- Status indicators -->
        <div style="position: absolute; top: 16px; right: 16px; display: flex; align-items: center; gap: 16px;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 32px; height: 32px; background: linear-gradient(45deg, #FF6B9D, #FF8E8E); border-radius: 50%;"></div>
            <span style="background-color: #10b981; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500;">● Online</span>
          </div>
        </div>
        
        <!-- Center content -->
        <div style="text-align: center;">
          <h2 style="color: white; font-size: 28px; font-weight: 700; margin: 0 0 8px 0;">📱iPhone 16 Pro</h2>
          <p style="color: #ccc; font-size: 16px; margin: 0;">Hello, Apple Intelligence</p>
        </div>
        
        <!-- Bottom right status -->
        <div style="position: absolute; bottom: 16px; right: 24px;">
          <span style="background-color: #10b981; color: white; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 500;">Youtube connected</span>
        </div>
      </div>

      <!-- Content Grid -->
      <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px;">
        
        <!-- Task Manager -->
        <div style="background: white; border-radius: 16px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
            <div>
              <h3 style="font-size: 20px; font-weight: 700; color: #1f2937; margin: 0 0 4px 0;">Task Manager</h3>
              <p style="font-size: 14px; color: #6b7280; margin: 0;">0 of 3 tasks completed</p>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
              <button style="background: #FF6B9D; color: white; border: none; padding: 8px 16px; border-radius: 8px; font-size: 12px; font-weight: 500;">All</button>
              <button style="background: transparent; color: #6b7280; border: none; padding: 8px 16px; border-radius: 8px; font-size: 12px;">Pending</button>
              <button style="background: transparent; color: #6b7280; border: none; padding: 8px 16px; border-radius: 8px; font-size: 12px;">Completed</button>
              <button style="background: #FF6B9D; color: white; border: none; padding: 8px 16px; border-radius: 8px; font-size: 12px; font-weight: 500;">+ Add New Goal</button>
            </div>
          </div>

          <!-- Task Items -->
          <div style="display: flex; flex-direction: column; gap: 16px;">
            <!-- Task 1 -->
            <div style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; display: flex; gap: 12px;">
              <input type="checkbox" style="width: 18px; height: 18px; margin-top: 2px;">
              <div style="flex: 1;">
                <h4 style="font-size: 14px; font-weight: 600; color: #1f2937; margin: 0 0 4px 0;">Create AI content creation assistant</h4>
                <p style="font-size: 12px; color: #6b7280; margin: 0 0 8px 0;">Hello! I'm your AI content creation assistant. How can I help you today?</p>
                <div style="display: flex; gap: 8px; align-items: center;">
                  <span style="background: #dbeafe; color: #1d4ed8; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 500;">Medium</span>
                  <span style="background: #f3f4f6; color: #4b5563; padding: 2px 8px; border-radius: 4px; font-size: 10px;">Content</span>
                  <span style="color: #6b7280; font-size: 10px;">Due: 18/7/2025</span>
                </div>
              </div>
            </div>

            <!-- Task 2 -->
            <div style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; display: flex; gap: 12px;">
              <input type="checkbox" style="width: 18px; height: 18px; margin-top: 2px;">
              <div style="flex: 1;">
                <h4 style="font-size: 14px; font-weight: 600; color: #1f2937; margin: 0 0 4px 0;">Schedule social media posts</h4>
                <p style="font-size: 12px; color: #6b7280; margin: 0 0 8px 0;">Plan and schedule posts for next week</p>
                <div style="display: flex; gap: 8px; align-items: center;">
                  <span style="background: #fee2e2; color: #dc2626; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 500;">High</span>
                  <span style="background: #f3f4f6; color: #4b5563; padding: 2px 8px; border-radius: 4px; font-size: 10px;">Content</span>
                  <span style="color: #6b7280; font-size: 10px;">Due: 18/7/2025</span>
                </div>
              </div>
            </div>

            <!-- Task 3 -->
            <div style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; display: flex; gap: 12px;">
              <input type="checkbox" style="width: 18px; height: 18px; margin-top: 2px;">
              <div style="flex: 1;">
                <h4 style="font-size: 14px; font-weight: 600; color: #1f2937; margin: 0 0 4px 0;">Update channel banner</h4>
                <p style="font-size: 12px; color: #6b7280; margin: 0 0 8px 0;">Design new banner with current subscriber count</p>
                <div style="display: flex; gap: 8px; align-items: center;">
                  <span style="background: #f3f4f6; color: #4b5563; padding: 2px 8px; border-radius: 4px; font-size: 10px;">Low</span>
                  <span style="background: #fce7f3; color: #be185d; padding: 2px 8px; border-radius: 4px; font-size: 10px;">Marketing</span>
                  <span style="color: #6b7280; font-size: 10px;">Due: 18/7/2025</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: Goals & Stats -->
        <div style="display: flex; flex-direction: column; gap: 20px;">
          
          <!-- Channel Goals -->
          <div style="background: white; border-radius: 16px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
              <h3 style="font-size: 16px; font-weight: 700; color: #1f2937; margin: 0;">Channel Goals</h3>
              <button style="background: #FF6B9D; color: white; border: none; padding: 6px 12px; border-radius: 6px; font-size: 11px; font-weight: 500;">+ Add Goal</button>
            </div>

            <!-- Views Goal -->
            <div style="background: linear-gradient(135deg, #FF6B9D 0%, #FF8E8E 100%); border-radius: 12px; padding: 16px; margin-bottom: 16px; color: white; text-align: center;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 12px; font-weight: 500;">👁️ Views</span>
              </div>
              <div style="font-size: 24px; font-weight: 700; margin-bottom: 8px;">75%</div>
              <div style="display: flex; justify-content: space-between; font-size: 11px; opacity: 0.9;">
                <div><div style="font-weight: 600;">7.5k</div><div>Completed</div></div>
                <div><div style="font-weight: 600;">2.5k</div><div>Remaining</div></div>
                <div><div style="font-weight: 600;">10k</div><div>Total</div></div>
              </div>
            </div>

            <!-- Subscribers Goal -->
            <div style="background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%); border-radius: 12px; padding: 16px; color: white; text-align: center;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 12px; font-weight: 500;">👥 Subscribers</span>
              </div>
              <div style="font-size: 24px; font-weight: 700; margin-bottom: 8px;">75%</div>
              <div style="display: flex; justify-content: space-between; font-size: 11px; opacity: 0.9;">
                <div><div style="font-weight: 600;">7.5k</div><div>Completed</div></div>
                <div><div style="font-weight: 600;">2.5k</div><div>Remaining</div></div>
                <div><div style="font-weight: 600;">10k</div><div>Total</div></div>
              </div>
            </div>
          </div>

          <!-- Quick Statistic -->
          <div style="background: white; border-radius: 16px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
              <h3 style="font-size: 16px; font-weight: 700; color: #1f2937; margin: 0;">Quick Statistic</h3>
              <button style="background: #FF6B9D; color: white; border: none; padding: 6px 12px; border-radius: 6px; font-size: 11px; font-weight: 500;">AI Assistant</button>
            </div>
            <div style="font-size: 32px; font-weight: 700; color: #1f2937; margin-bottom: 8px;">48%</div>
            <div style="color: #6b7280; font-size: 14px;">Audience Retention</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Vue composition API for any interactive functionality
// Add hover effects, click handlers, etc. here
</script>