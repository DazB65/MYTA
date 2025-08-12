<template>
  <div class="bg-gray-900 text-white min-h-screen flex">
    <!-- Left Sidebar Navigation (Same as Pillars page) -->
    <div class="w-72 bg-gray-800 h-screen flex flex-col fixed">
      <!-- Logo Section -->
      <div class="p-6">
        <div class="flex items-center space-x-2">
          <div class="w-8 h-8 bg-pink-500 rounded flex items-center justify-center">
            <span class="text-white text-sm">✨</span>
          </div>
          <h1 class="text-xl font-bold text-white">Vidalytics</h1>
        </div>
        <p class="text-xs text-gray-400 mt-1">
          Your AI Agent for Content and Growth
        </p>
      </div>

      <!-- Main Menu -->
      <div class="px-4">
        <h3 class="text-sm font-medium text-gray-400 mb-4">Main Menu</h3>
        <nav class="space-y-2">
          <NuxtLink
            to="/dashboard"
            class="flex items-center px-4 py-3 text-white bg-pink-500 rounded-lg"
          >
            <svg
              class="w-5 h-5 mr-3"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
            </svg>
            Dashboard
          </NuxtLink>
          <NuxtLink
            to="/pillars"
            class="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg
              class="w-5 h-5 mr-3"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"></path>
            </svg>
            Pillars
          </NuxtLink>
          <NuxtLink
            to="/videos"
            class="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg
              class="w-5 h-5 mr-3"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"></path>
            </svg>
            Videos
          </NuxtLink>
          <NuxtLink
            to="/content-studio"
            class="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg
              class="w-5 h-5 mr-3"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
            </svg>
            Content Studio
          </NuxtLink>
          <NuxtLink
            to="/ai-assistant"
            class="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg
              class="w-5 h-5 mr-3"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            AI Assistant
          </NuxtLink>
        </nav>
      </div>

      <!-- General Section -->
      <div class="px-4 mt-8">
        <h3 class="text-sm font-medium text-gray-400 mb-4">General</h3>
        <nav class="space-y-2">
          <NuxtLink
            to="/settings"
            class="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg
              class="w-5 h-5 mr-3"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                clip-rule="evenodd"
              ></path>
            </svg>
            Settings
          </NuxtLink>
        </nav>
      </div>

      <!-- User Profile Section -->
      <div class="mt-auto p-6 border-t border-gray-700">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-pink-500 rounded-full flex items-center justify-center">
            <span class="text-white font-bold">M</span>
          </div>
          <div class="flex-1">
            <p class="text-sm text-white">Good Morning</p>
            <p class="text-sm font-bold text-white">
              MARCELINE ANDERSON!
            </p>
            <p class="text-xs text-gray-400">
              Let's see your current task work today
            </p>
          </div>
        </div>
        <div class="mt-4 flex items-center justify-between">
          <div class="text-xs text-gray-400">📅 23 July, 2026</div>
          <button class="text-gray-400 hover:text-white">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </button>
        </div>
        <button class="mt-2 text-gray-400 hover:text-white text-sm flex items-center">
          <svg
            class="w-4 h-4 mr-1"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
              clip-rule="evenodd"
            ></path>
          </svg>
          Log Out
        </button>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="flex-1 bg-gray-900 p-6 overflow-y-auto ml-72">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-2xl font-bold text-white">Dashboard</h2>
          <p class="text-gray-400">Monitor your YouTube channel performance</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <div class="w-3 h-3 bg-pink-500 rounded-full"></div>
            <span class="text-white text-sm">● Online</span>
          </div>
          <div class="bg-green-500 text-white px-3 py-1 rounded-full text-sm">
            ✓ YouTube connected
          </div>
        </div>
      </div>

      <!-- Banner Compartment Section -->
      <div class="mb-6">
        <IPhoneCompartment />
      </div>

      <!-- Dashboard Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Task Manager Compartment -->
        <div class="bg-gray-800 rounded-xl p-6">
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-pink-500 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div>
                <h3 class="text-white font-semibold text-lg">Task Manager</h3>
                <p class="text-gray-400 text-sm">Out of 5 tasks completed</p>
              </div>
            </div>
            <button class="text-gray-400 hover:text-white">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
              </svg>
            </button>
          </div>

          <!-- Filter Buttons -->
          <div class="flex items-center space-x-2 mb-6">
            <button class="px-3 py-1 bg-pink-500 text-white rounded-full text-sm">All</button>
            <button class="px-3 py-1 bg-gray-700 text-gray-300 rounded-full text-sm hover:bg-gray-600">Pending</button>
            <button class="px-3 py-1 bg-gray-700 text-gray-300 rounded-full text-sm hover:bg-gray-600">Completed</button>
            <button class="p-2 bg-pink-500 text-white rounded-full ml-auto">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"></path>
              </svg>
            </button>
            <span class="text-pink-500 text-sm font-medium">Add New Goal</span>
          </div>

          <!-- Task List -->
          <div class="space-y-4">
            <!-- Task 1 -->
            <div class="bg-gray-700 rounded-lg p-4 border border-gray-600">
              <div class="flex items-start space-x-3">
                <input type="checkbox" class="mt-1 w-5 h-5 text-pink-500 rounded bg-gray-600 border-gray-500" />
                <div class="flex-1">
                  <h3 class="font-semibold text-white">Create AI content creation assistant</h3>
                  <p class="text-gray-300 text-sm mt-1">Hello! I'm your AI content creation assistant. How can I help you today?</p>
                  <div class="flex items-center space-x-2 mt-3">
                    <span class="px-2 py-1 bg-blue-500 text-white text-xs rounded">General</span>
                    <span class="px-2 py-1 bg-gray-600 text-gray-300 text-xs rounded">Content</span>
                    <span class="text-gray-400 text-xs">📅 Due: 18/7/2025</span>
                  </div>
                </div>
                <button class="text-gray-400 hover:text-white">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Task 2 -->
            <div class="bg-gray-700 rounded-lg p-4 border border-gray-600">
              <div class="flex items-start space-x-3">
                <input type="checkbox" class="mt-1 w-5 h-5 text-pink-500 rounded bg-gray-600 border-gray-500" />
                <div class="flex-1">
                  <h3 class="font-semibold text-white">Schedule social media posts</h3>
                  <p class="text-gray-300 text-sm mt-1">Plan and schedule posts for next week</p>
                  <div class="flex items-center space-x-2 mt-3">
                    <span class="px-2 py-1 bg-red-500 text-white text-xs rounded">High</span>
                    <span class="px-2 py-1 bg-gray-600 text-gray-300 text-xs rounded">Content</span>
                    <span class="text-gray-400 text-xs">📅 Due: 18/7/2025</span>
                  </div>
                </div>
                <button class="text-gray-400 hover:text-white">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Task 3 -->
            <div class="bg-gray-700 rounded-lg p-4 border border-gray-600">
              <div class="flex items-start space-x-3">
                <input type="checkbox" class="mt-1 w-5 h-5 text-pink-500 rounded bg-gray-600 border-gray-500" />
                <div class="flex-1">
                  <h3 class="font-semibold text-white">Update channel banners</h3>
                  <p class="text-gray-300 text-sm mt-1">Design new banner with current subscriber count</p>
                  <div class="flex items-center space-x-2 mt-3">
                    <span class="px-2 py-1 bg-purple-500 text-white text-xs rounded">Low</span>
                    <span class="px-2 py-1 bg-orange-500 text-white text-xs rounded">Marketing</span>
                    <span class="px-2 py-1 bg-gray-600 text-gray-300 text-xs rounded">Content</span>
                    <span class="text-gray-400 text-xs">📅 Due: 18/7/2025</span>
                  </div>
                </div>
                <button class="text-gray-400 hover:text-white">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Task 4 -->
            <div class="bg-gray-700 rounded-lg p-4 border border-gray-600">
              <div class="flex items-start space-x-3">
                <input type="checkbox" class="mt-1 w-5 h-5 text-pink-500 rounded bg-gray-600 border-gray-500" />
                <div class="flex-1">
                  <h3 class="font-semibold text-white">Reply to community comments</h3>
                  <p class="text-gray-300 text-sm mt-1">Engage with your audience by responding to comments on your latest video posts</p>
                </div>
                <button class="text-gray-400 hover:text-white">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Channel Goals Compartment -->
        <div class="bg-gray-800 rounded-xl p-6">
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div>
                <h3 class="text-white font-semibold text-lg">Channel Goals</h3>
                <p class="text-gray-400 text-sm">Track your progress</p>
              </div>
            </div>
            <button class="text-gray-400 hover:text-white">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
              </svg>
            </button>
          </div>

          <!-- Views Goal -->
          <div class="bg-gradient-to-br from-orange-400 to-pink-500 rounded-xl p-6 text-white mb-4">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-2">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"></path>
                  <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"></path>
                </svg>
                <span class="font-semibold">Views</span>
              </div>
              <button class="text-white/80 hover:text-white">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                </svg>
              </button>
            </div>
            <div class="flex items-center justify-center mb-4">
              <div class="relative w-24 h-24">
                <svg class="w-24 h-24 transform -rotate-90" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="40" stroke="rgba(255,255,255,0.2)" stroke-width="8" fill="none"/>
                  <circle cx="50" cy="50" r="40" stroke="white" stroke-width="8" fill="none" stroke-dasharray="251.2" stroke-dashoffset="62.8"/>
                </svg>
                <div class="absolute inset-0 flex items-center justify-center">
                  <span class="text-2xl font-bold">75%</span>
                </div>
              </div>
            </div>
            <div class="grid grid-cols-3 gap-4 text-center">
              <div>
                <div class="text-lg font-bold">7.5k</div>
                <div class="text-xs opacity-80">Completed</div>
              </div>
              <div>
                <div class="text-lg font-bold">2.5k</div>
                <div class="text-xs opacity-80">Remaining</div>
              </div>
              <div>
                <div class="text-lg font-bold">10k</div>
                <div class="text-xs opacity-80">Total</div>
              </div>
            </div>
          </div>

          <!-- Subscribers Goal -->
          <div class="bg-gradient-to-br from-blue-400 to-cyan-500 rounded-xl p-6 text-white mb-6">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-2">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"></path>
                </svg>
                <span class="font-semibold">Subscribers</span>
              </div>
              <button class="text-white/80 hover:text-white">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                </svg>
              </button>
            </div>
            <div class="flex items-center justify-center mb-4">
              <div class="relative w-24 h-24">
                <svg class="w-24 h-24 transform -rotate-90" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="40" stroke="rgba(255,255,255,0.2)" stroke-width="8" fill="none"/>
                  <circle cx="50" cy="50" r="40" stroke="white" stroke-width="8" fill="none" stroke-dasharray="251.2" stroke-dashoffset="62.8"/>
                </svg>
                <div class="absolute inset-0 flex items-center justify-center">
                  <span class="text-2xl font-bold">75%</span>
                </div>
              </div>
            </div>
            <div class="grid grid-cols-3 gap-4 text-center">
              <div>
                <div class="text-lg font-bold">7.5k</div>
                <div class="text-xs opacity-80">Completed</div>
              </div>
              <div>
                <div class="text-lg font-bold">2.5k</div>
                <div class="text-xs opacity-80">Remaining</div>
              </div>
              <div>
                <div class="text-lg font-bold">10k</div>
                <div class="text-xs opacity-80">Total</div>
              </div>
            </div>
          </div>

          <!-- Quick Statistics -->
          <div class="bg-gray-700 rounded-xl p-4">
            <div class="flex items-center justify-between mb-4">
              <h3 class="font-semibold text-white">Quick Statistic</h3>
              <button class="bg-pink-500 text-white px-3 py-1 rounded-full text-sm flex items-center space-x-1">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>AI Assistant</span>
              </button>
            </div>
          </div>

          <!-- Add New Task Button -->
          <div class="mt-6 flex justify-center">
            <button class="flex items-center space-x-2 text-pink-500 font-medium hover:text-pink-400">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"></path>
              </svg>
              <span>Add New Task</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
// Simple script for the new dashboard design
useHead({
  title: 'Dashboard - Vidalytics',
  meta: [
    {
      name: 'description',
      content: 'Monitor your YouTube channel performance with comprehensive analytics and AI-powered insights.'
    }
  ]
})
</script>



