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
            <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
            </svg>
            Content Studio
          </NuxtLink>
          <NuxtLink
            to="/ai-assistant"
            class="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
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
            <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
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
            <span class="text-white font-bold">{{ userInitials }}</span>
          </div>
          <div class="flex-1">
            <p class="text-sm text-white">{{ greeting }}</p>
            <p class="text-sm font-bold text-white">{{ userName }}!</p>
            <p class="text-xs text-gray-400">Track your growth</p>
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
      <!-- Header Banner -->
      <div class="bg-gradient-to-r from-pink-500 to-purple-600 rounded-xl p-8 mb-6 relative overflow-hidden">
        <div class="relative z-10">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-bold text-white mb-2">{{ bannerTitle }}</h1>
              <p class="text-pink-100 text-lg">{{ bannerSubtitle }}</p>
            </div>
            <div class="flex items-center space-x-4">
              <div class="text-pink-100 text-sm">Last updated: 2 min ago</div>
              <button
                v-if="!youtubeConnected"
                @click="handleYouTubeConnect"
                class="px-6 py-3 bg-white text-pink-600 rounded-lg hover:bg-pink-50 transition-colors font-semibold"
              >
                Connect YouTube
              </button>
              <button
                v-else
                @click="refreshAnalytics"
                class="px-6 py-3 bg-white/20 text-white rounded-lg hover:bg-white/30 transition-colors"
              >
                Refresh Data
              </button>
            </div>
          </div>
        </div>
        <!-- Background decoration -->
        <div class="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-32 translate-x-32"></div>
        <div class="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full translate-y-24 -translate-x-24"></div>
      </div>

      <!-- Dashboard Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Task Manager Card -->
        <div
          @click="showTaskManager = true"
          class="bg-gray-800 rounded-xl p-6 cursor-pointer hover:bg-gray-750 transition-colors group"
        >
          <div class="flex items-center justify-between mb-4">
            <div class="w-12 h-12 bg-pink-500 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" clip-rule="evenodd"></path>
              </svg>
            </div>
            <svg class="w-5 h-5 text-gray-400 group-hover:text-white transition-colors" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">Task Manager</h3>
          <p class="text-gray-400 mb-4">Manage your content creation tasks</p>
          <div class="flex items-center space-x-2">
            <div class="text-2xl font-bold text-pink-500">3</div>
            <div class="text-gray-400">/ 8 tasks completed</div>
          </div>
        </div>

        <!-- Channel Goals Card -->
        <div
          @click="showChannelGoals = true"
          class="bg-gray-800 rounded-xl p-6 cursor-pointer hover:bg-gray-750 transition-colors group"
        >
          <div class="flex items-center justify-between mb-4">
            <div class="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <svg class="w-5 h-5 text-gray-400 group-hover:text-white transition-colors" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">Channel Goals</h3>
          <p class="text-gray-400 mb-4">Track your growth objectives</p>
          <div class="flex items-center space-x-4">
            <div class="text-center">
              <div class="text-lg font-bold text-blue-500">75%</div>
              <div class="text-xs text-gray-400">Views</div>
            </div>
            <div class="text-center">
              <div class="text-lg font-bold text-green-500">30%</div>
              <div class="text-xs text-gray-400">Subscribers</div>
            </div>
          </div>
        </div>

        <!-- Quick Statistics Card -->
        <div
          @click="showQuickStats = true"
          class="bg-gray-800 rounded-xl p-6 cursor-pointer hover:bg-gray-750 transition-colors group"
        >
          <div class="flex items-center justify-between mb-4">
            <div class="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"></path>
              </svg>
            </div>
            <svg class="w-5 h-5 text-gray-400 group-hover:text-white transition-colors" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">Quick Statistics</h3>
          <p class="text-gray-400 mb-4">Overview of key metrics</p>
          <div class="flex items-center space-x-4">
            <div class="text-center">
              <div class="text-lg font-bold text-pink-500">75%</div>
              <div class="text-xs text-gray-400">Completion</div>
            </div>
            <div class="text-center">
              <div class="text-lg font-bold text-blue-500">2.8k</div>
              <div class="text-xs text-gray-400">Subscribers</div>
            </div>
            <div class="text-center">
              <div class="text-lg font-bold text-green-500">10k</div>
              <div class="text-xs text-gray-400">Views</div>
            </div>
          </div>
        </div>
      </div>

    <!-- Task Manager Modal -->
    <div v-if="showTaskManager" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-gray-800 rounded-xl p-6 w-full max-w-2xl mx-4 max-h-[80vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-semibold text-white">Task Manager</h3>
          <button @click="showTaskManager = false" class="text-gray-400 hover:text-white">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>

        <div class="mb-6">
          <div class="text-gray-400 text-sm mb-4">
            <span class="text-pink-500 font-bold">3</span> / 8 tasks completed
          </div>

          <!-- Task Categories -->
          <div class="flex space-x-4 mb-6">
            <button class="px-4 py-2 bg-pink-500 text-white rounded-lg text-sm">All Tasks</button>
            <button class="px-4 py-2 bg-gray-700 text-gray-300 rounded-lg text-sm hover:bg-gray-600">Content</button>
            <button class="px-4 py-2 bg-gray-700 text-gray-300 rounded-lg text-sm hover:bg-gray-600">Analytics</button>
          </div>

          <!-- Task List -->
          <div class="space-y-3">
            <div class="flex items-center space-x-3 p-4 bg-gray-700 rounded-lg">
              <input type="checkbox" checked class="w-5 h-5 text-pink-500 bg-gray-600 border-gray-500 rounded focus:ring-pink-500">
              <span class="text-gray-300 line-through">Create 5 content creative concepts</span>
            </div>
            <div class="flex items-center space-x-3 p-4 bg-gray-700 rounded-lg">
              <input type="checkbox" checked class="w-5 h-5 text-pink-500 bg-gray-600 border-gray-500 rounded focus:ring-pink-500">
              <span class="text-gray-300 line-through">Upload channel banner</span>
            </div>
            <div class="flex items-center space-x-3 p-4 bg-gray-700 rounded-lg">
              <input type="checkbox" checked class="w-5 h-5 text-pink-500 bg-gray-600 border-gray-500 rounded focus:ring-pink-500">
              <span class="text-gray-300 line-through">Post 10 community comments</span>
            </div>
            <div class="flex items-center space-x-3 p-4 bg-gray-700 rounded-lg">
              <input type="checkbox" class="w-5 h-5 text-pink-500 bg-gray-600 border-gray-500 rounded focus:ring-pink-500">
              <span class="text-white">Analyze competitor content</span>
            </div>
            <div class="flex items-center space-x-3 p-4 bg-gray-700 rounded-lg">
              <input type="checkbox" class="w-5 h-5 text-pink-500 bg-gray-600 border-gray-500 rounded focus:ring-pink-500">
              <span class="text-white">Schedule next week's uploads</span>
            </div>
            <div class="flex items-center space-x-3 p-4 bg-gray-700 rounded-lg">
              <input type="checkbox" class="w-5 h-5 text-pink-500 bg-gray-600 border-gray-500 rounded focus:ring-pink-500">
              <span class="text-white">Create thumbnail templates</span>
            </div>
            <div class="flex items-center space-x-3 p-4 bg-gray-700 rounded-lg">
              <input type="checkbox" class="w-5 h-5 text-pink-500 bg-gray-600 border-gray-500 rounded focus:ring-pink-500">
              <span class="text-white">Research trending topics</span>
            </div>
            <div class="flex items-center space-x-3 p-4 bg-gray-700 rounded-lg">
              <input type="checkbox" class="w-5 h-5 text-pink-500 bg-gray-600 border-gray-500 rounded focus:ring-pink-500">
              <span class="text-white">Update video descriptions</span>
            </div>
          </div>
        </div>

        <div class="flex justify-end space-x-3">
          <button @click="showTaskManager = false" class="px-4 py-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600">
            Close
          </button>
          <button class="px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600">
            Add New Task
          </button>
        </div>
      </div>
    </div>

    <!-- Channel Goals Modal -->
    <div v-if="showChannelGoals" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-gray-800 rounded-xl p-6 w-full max-w-2xl mx-4">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-semibold text-white">Channel Goals</h3>
          <button @click="showChannelGoals = false" class="text-gray-400 hover:text-white">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>

        <!-- Goals Grid -->
        <div class="space-y-6 mb-6">
          <!-- Views Goal -->
          <div class="flex items-center space-x-6 p-6 bg-gray-700 rounded-lg">
            <div class="relative w-24 h-24">
              <svg class="w-24 h-24 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="#374151"
                  stroke-width="3"
                />
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="#ec4899"
                  stroke-width="3"
                  stroke-dasharray="75, 100"
                />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-white font-bold text-lg">75%</span>
              </div>
            </div>
            <div class="flex-1">
              <h4 class="text-white font-semibold text-xl mb-2">Views Goal</h4>
              <p class="text-gray-400 mb-2">7.5k / 10k views</p>
              <p class="text-green-400 text-sm">+12% this month</p>
              <div class="mt-3">
                <div class="w-full bg-gray-600 rounded-full h-2">
                  <div class="bg-pink-500 h-2 rounded-full" style="width: 75%"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Subscribers Goal -->
          <div class="flex items-center space-x-6 p-6 bg-gray-700 rounded-lg">
            <div class="relative w-24 h-24">
              <svg class="w-24 h-24 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="#374151"
                  stroke-width="3"
                />
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="#3b82f6"
                  stroke-width="3"
                  stroke-dasharray="30, 100"
                />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-white font-bold text-lg">30%</span>
              </div>
            </div>
            <div class="flex-1">
              <h4 class="text-white font-semibold text-xl mb-2">Subscribers Goal</h4>
              <p class="text-gray-400 mb-2">2.8k / 10k subscribers</p>
              <p class="text-green-400 text-sm">+8% this month</p>
              <div class="mt-3">
                <div class="w-full bg-gray-600 rounded-full h-2">
                  <div class="bg-blue-500 h-2 rounded-full" style="width: 30%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="flex justify-end space-x-3">
          <button @click="showChannelGoals = false" class="px-4 py-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600">
            Close
          </button>
          <button class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
            Add New Goal
          </button>
        </div>
      </div>
    </div>

    <!-- Quick Statistics Modal -->
    <div v-if="showQuickStats" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-gray-800 rounded-xl p-6 w-full max-w-4xl mx-4">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-semibold text-white">Quick Statistics</h3>
          <button @click="showQuickStats = false" class="text-gray-400 hover:text-white">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div class="bg-gradient-to-r from-pink-500 to-pink-600 p-6 rounded-lg text-white">
            <div class="flex items-center justify-between mb-4">
              <div class="text-3xl font-bold">75%</div>
              <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
              </svg>
            </div>
            <div class="text-pink-100 text-sm mb-2">Task Completion Rate</div>
            <div class="text-pink-100 text-xs">+5% from last week</div>
          </div>

          <div class="bg-gradient-to-r from-blue-500 to-blue-600 p-6 rounded-lg text-white">
            <div class="flex items-center justify-between mb-4">
              <div class="text-3xl font-bold">2.8k</div>
              <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"></path>
              </svg>
            </div>
            <div class="text-blue-100 text-sm mb-2">Total Subscribers</div>
            <div class="text-blue-100 text-xs">+8% from last month</div>
          </div>

          <div class="bg-gradient-to-r from-green-500 to-green-600 p-6 rounded-lg text-white">
            <div class="flex items-center justify-between mb-4">
              <div class="text-3xl font-bold">10k</div>
              <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"></path>
                <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"></path>
              </svg>
            </div>
            <div class="text-green-100 text-sm mb-2">Total Views</div>
            <div class="text-green-100 text-xs">+12% from last month</div>
          </div>
        </div>

        <!-- Additional Stats -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div class="bg-gray-700 p-4 rounded-lg text-center">
            <div class="text-2xl font-bold text-white mb-1">4.2k</div>
            <div class="text-gray-400 text-sm">Watch Time (hrs)</div>
          </div>
          <div class="bg-gray-700 p-4 rounded-lg text-center">
            <div class="text-2xl font-bold text-white mb-1">3.8%</div>
            <div class="text-gray-400 text-sm">CTR</div>
          </div>
          <div class="bg-gray-700 p-4 rounded-lg text-center">
            <div class="text-2xl font-bold text-white mb-1">2:45</div>
            <div class="text-gray-400 text-sm">Avg Duration</div>
          </div>
          <div class="bg-gray-700 p-4 rounded-lg text-center">
            <div class="text-2xl font-bold text-white mb-1">$247</div>
            <div class="text-gray-400 text-sm">Revenue</div>
          </div>
        </div>

        <div class="flex justify-end">
          <button @click="showQuickStats = false" class="px-4 py-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600">
            Close
          </button>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

// User data (this would come from authentication/user store)
const userData = ref({
  id: 'demo-user-123', // This would be from auth
  name: 'Marceline Anderson',
  initials: 'M',
  isOnline: true
})

// Modal states
const showTaskManager = ref(false)
const showChannelGoals = ref(false)
const showQuickStats = ref(false)

// Mock YouTube connection state
const youtubeConnected = ref(false)

// Computed properties for user interface
const userInitials = computed(() => userData.value.initials)
const userName = computed(() => userData.value.name)

const bannerTitle = computed(() => {
  if (!youtubeConnected.value) {
    return '🔗 Connect Your Channel'
  }
  return '📊 Your Analytics Dashboard'
})

const bannerSubtitle = computed(() => {
  if (!youtubeConnected.value) {
    return 'Link your YouTube account to get started'
  }
  return 'Track your growth and optimize performance'
})

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good Morning'
  if (hour < 17) return 'Good Afternoon'
  return 'Good Evening'
})

// Event handlers
const handleYouTubeConnect = () => {
  // Navigate to OAuth connection flow or show connection modal
  console.log('Connect YouTube clicked')
  youtubeConnected.value = true
}

const refreshAnalytics = () => {
  // Refresh analytics data
  console.log('Refresh analytics clicked')
}

// Meta for SEO
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
