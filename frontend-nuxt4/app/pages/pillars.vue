<template>
  <div class="bg-gray-900 text-white min-h-screen flex">
    <!-- Left Sidebar Navigation -->
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
            class="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
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
            class="flex items-center px-4 py-3 text-white bg-pink-500 rounded-lg"
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
              Let's organize your content pillars
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
          <h2 class="text-2xl font-bold text-white">Content Pillars</h2>
          <p class="text-gray-400">Analyze and optimize your content strategy</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="text-gray-400 text-sm">Last 30 days</div>
          <button class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors flex items-center space-x-2">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"></path>
            </svg>
            <span>Add Pillar</span>
          </button>
        </div>
      </div>

      <!-- Content Pillars Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Game Development Pillar -->
        <div class="bg-gray-800 rounded-xl p-6">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div>
                <h3 class="text-white font-semibold text-lg">Game Development</h3>
                <p class="text-gray-400 text-sm">3 Videos • Created 4 months ago</p>
              </div>
            </div>
            <button class="text-gray-400 hover:text-white">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
              </svg>
            </button>
          </div>

          <!-- Metrics -->
          <div class="grid grid-cols-3 gap-4 mb-6">
            <div>
              <div class="text-2xl font-bold text-white">248.3K</div>
              <div class="text-green-400 text-sm flex items-center">
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                </svg>
                +12.5%
              </div>
              <div class="text-gray-400 text-xs">Revenue</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">14.2K hrs</div>
              <div class="text-green-400 text-sm flex items-center">
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                </svg>
                +8.2%
              </div>
              <div class="text-gray-400 text-xs">Watch Time</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">93,842</div>
              <div class="text-green-400 text-sm flex items-center">
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                </svg>
                +15.3%
              </div>
              <div class="text-gray-400 text-xs">Subscribers</div>
            </div>
          </div>

          <!-- Chart Area -->
          <div class="h-32 mb-4 relative">
            <svg class="w-full h-full" viewBox="0 0 300 100">
              <defs>
                <linearGradient id="blueGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:0.3" />
                  <stop offset="100%" style="stop-color:#3B82F6;stop-opacity:0" />
                </linearGradient>
              </defs>
              <path d="M0,80 Q50,70 100,60 T200,45 T300,35" stroke="#3B82F6" stroke-width="2" fill="none"/>
              <path d="M0,80 Q50,70 100,60 T200,45 T300,35 L300,100 L0,100 Z" fill="url(#blueGradient)"/>
            </svg>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center justify-between">
            <div class="text-gray-400 text-sm">Top performing content pillar</div>
            <div class="flex space-x-2">
              <button class="px-3 py-1 text-gray-300 hover:text-white text-sm">View Details</button>
              <button class="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600">Create Content</button>
            </div>
          </div>
        </div>

        <!-- Game Reviews Pillar -->
        <div class="bg-gray-800 rounded-xl p-6">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-purple-500 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                </svg>
              </div>
              <div>
                <h3 class="text-white font-semibold text-lg">Game Reviews</h3>
                <p class="text-gray-400 text-sm">8 Videos • Created 3 months ago</p>
              </div>
            </div>
            <button class="text-gray-400 hover:text-white">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
              </svg>
            </button>
          </div>

          <!-- Metrics -->
          <div class="grid grid-cols-3 gap-4 mb-6">
            <div>
              <div class="text-2xl font-bold text-white">186.7K</div>
              <div class="text-green-400 text-sm flex items-center">
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                </svg>
                +9.8%
              </div>
              <div class="text-gray-400 text-xs">Revenue</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">6.9K hrs</div>
              <div class="text-green-400 text-sm flex items-center">
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                </svg>
                +6.1%
              </div>
              <div class="text-gray-400 text-xs">Watch Time</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">52,156</div>
              <div class="text-green-400 text-sm flex items-center">
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                </svg>
                +11.2%
              </div>
              <div class="text-gray-400 text-xs">Subscribers</div>
            </div>
          </div>

          <!-- Chart Area -->
          <div class="h-32 mb-4 relative">
            <svg class="w-full h-full" viewBox="0 0 300 100">
              <defs>
                <linearGradient id="purpleGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color:#8B5CF6;stop-opacity:0.3" />
                  <stop offset="100%" style="stop-color:#8B5CF6;stop-opacity:0" />
                </linearGradient>
              </defs>
              <path d="M0,85 Q50,75 100,65 T200,50 T300,40" stroke="#8B5CF6" stroke-width="2" fill="none"/>
              <path d="M0,85 Q50,75 100,65 T200,50 T300,40 L300,100 L0,100 Z" fill="url(#purpleGradient)"/>
            </svg>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center justify-between">
            <div class="text-gray-400 text-sm">Consistent growth in audience retention</div>
            <div class="flex space-x-2">
              <button class="px-3 py-1 text-gray-300 hover:text-white text-sm">View Details</button>
              <button class="px-3 py-1 bg-purple-500 text-white rounded text-sm hover:bg-purple-600">Create Content</button>
            </div>
          </div>
        </div>

        <!-- Gaming Tips Pillar -->
        <div class="bg-gray-800 rounded-xl p-6">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-orange-500 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"></path>
                </svg>
              </div>
              <div>
                <h3 class="text-white font-semibold text-lg">Gaming Tips</h3>
                <p class="text-gray-400 text-sm">12 Videos • Created 2 months ago</p>
              </div>
            </div>
            <button class="text-gray-400 hover:text-white">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
              </svg>
            </button>
          </div>

          <!-- Metrics -->
          <div class="grid grid-cols-3 gap-4 mb-6">
            <div>
              <div class="text-2xl font-bold text-white">203.5K</div>
              <div class="text-green-400 text-sm flex items-center">
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                </svg>
                +7.3%
              </div>
              <div class="text-gray-400 text-xs">Revenue</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">10.1K hrs</div>
              <div class="text-green-400 text-sm flex items-center">
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                </svg>
                +5.8%
              </div>
              <div class="text-gray-400 text-xs">Watch Time</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">92,037</div>
              <div class="text-green-400 text-sm flex items-center">
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                </svg>
                +13.7%
              </div>
              <div class="text-gray-400 text-xs">Subscribers</div>
            </div>
          </div>

          <!-- Chart Area -->
          <div class="h-32 mb-4 relative">
            <svg class="w-full h-full" viewBox="0 0 300 100">
              <defs>
                <linearGradient id="orangeGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color:#F97316;stop-opacity:0.3" />
                  <stop offset="100%" style="stop-color:#F97316;stop-opacity:0" />
                </linearGradient>
              </defs>
              <path d="M0,90 Q50,85 100,75 T200,60 T300,45" stroke="#F97316" stroke-width="2" fill="none"/>
              <path d="M0,90 Q50,85 100,75 T200,60 T300,45 L300,100 L0,100 Z" fill="url(#orangeGradient)"/>
            </svg>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center justify-between">
            <div class="text-gray-400 text-sm">High engagement from returning viewers</div>
            <div class="flex space-x-2">
              <button class="px-3 py-1 text-gray-300 hover:text-white text-sm">View Details</button>
              <button class="px-3 py-1 bg-orange-500 text-white rounded text-sm hover:bg-orange-600">Create Content</button>
            </div>
          </div>
        </div>
        <!-- Gaming News Pillar -->
        <div class="bg-gray-800 rounded-xl p-6">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-red-500 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"></path>
                </svg>
              </div>
              <div>
                <h3 class="text-white font-semibold text-lg">Gaming News</h3>
                <p class="text-gray-400 text-sm">6 Videos • Created 4 months ago</p>
              </div>
            </div>
            <button class="text-gray-400 hover:text-white">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
              </svg>
            </button>
          </div>

          <!-- Metrics -->
          <div class="grid grid-cols-3 gap-4 mb-6">
            <div>
              <div class="text-2xl font-bold text-white">97.2K</div>
              <div class="text-red-400 text-sm flex items-center">
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 112 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                -3.8%
              </div>
              <div class="text-gray-400 text-xs">Revenue</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">4.3K hrs</div>
              <div class="text-red-400 text-sm flex items-center">
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 112 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                -1.2%
              </div>
              <div class="text-gray-400 text-xs">Watch Time</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">8843</div>
              <div class="text-red-400 text-sm flex items-center">
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 112 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                -6.5%
              </div>
              <div class="text-gray-400 text-xs">Subscribers</div>
            </div>
          </div>

          <!-- Chart Area -->
          <div class="h-32 mb-4 relative">
            <svg class="w-full h-full" viewBox="0 0 300 100">
              <defs>
                <linearGradient id="redGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color:#EF4444;stop-opacity:0.3" />
                  <stop offset="100%" style="stop-color:#EF4444;stop-opacity:0" />
                </linearGradient>
              </defs>
              <path d="M0,60 Q50,65 100,70 T200,75 T300,80" stroke="#EF4444" stroke-width="2" fill="none"/>
              <path d="M0,60 Q50,65 100,70 T200,75 T300,80 L300,100 L0,100 Z" fill="url(#redGradient)"/>
            </svg>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center justify-between">
            <div class="text-gray-400 text-sm">Needs improvement in content strategy</div>
            <div class="flex space-x-2">
              <button class="px-3 py-1 text-gray-300 hover:text-white text-sm">View Details</button>
              <button class="px-3 py-1 bg-red-500 text-white rounded text-sm hover:bg-red-600">Create Content</button>
            </div>
          </div>
        </div>
      </div>

      <!-- AI Suggested Pillar -->
      <div class="mt-6 bg-gray-800 rounded-xl p-6 border border-blue-500/20">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-white font-semibold text-lg">AI Suggested: Metaverse Coverage</h3>
              <p class="text-blue-400 text-sm">NEW</p>
            </div>
          </div>
          <div class="flex space-x-2">
            <button class="px-3 py-1 text-gray-300 hover:text-white text-sm border border-gray-600 rounded">Dismiss</button>
            <button class="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600">Create Pillar</button>
          </div>
        </div>
        <p class="text-gray-300 text-sm">Based on trending topics and your audience interests, consider creating content about metaverse gaming and virtual worlds.</p>
      </div>
    </div>

  </div>
</template>

<script setup>
// Content Pillars Analytics Dashboard
// Static data display matching the design from the image
</script>