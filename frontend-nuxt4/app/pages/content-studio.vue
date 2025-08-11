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
            <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
            </svg>
            Dashboard
          </NuxtLink>
          <NuxtLink
            to="/pillars"
            class="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"></path>
            </svg>
            Pillars
          </NuxtLink>
          <NuxtLink
            to="/videos"
            class="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"></path>
            </svg>
            Videos
          </NuxtLink>
          <NuxtLink
            to="/content-studio"
            class="flex items-center px-4 py-3 text-white bg-pink-500 rounded-lg"
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
              <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"></path>
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
            <p class="text-sm font-bold text-white">MARCELINE ANDERSON!</p>
            <p class="text-xs text-gray-400">Create amazing content</p>
          </div>
        </div>
        <div class="mt-4 flex items-center justify-between">
          <div class="text-xs text-gray-400">📅 23 July, 2026</div>
          <button class="text-gray-400 hover:text-white">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>
        <button class="mt-2 text-gray-400 hover:text-white text-sm flex items-center">
          <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd"></path>
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
          <h2 class="text-2xl font-bold text-white">Content Studio</h2>
          <p class="text-gray-400">Manage your content workflow from idea to publication</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="relative">
            <input
              type="text"
              placeholder="Search content..."
              class="bg-gray-800 text-white px-4 py-2 rounded-lg pl-10 w-64 focus:outline-none focus:ring-2 focus:ring-pink-500"
            >
            <svg class="w-5 h-5 text-gray-400 absolute left-3 top-2.5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"></path>
            </svg>
          </div>
          <button class="px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors flex items-center space-x-2">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"></path>
            </svg>
            <span>New Content</span>
          </button>
        </div>
      </div>

      <!-- Workflow Stats -->
      <div class="grid grid-cols-5 gap-4 mb-6">
        <div class="bg-gray-800 p-4 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Ideas</p>
              <p class="text-xl font-bold text-white">{{ getColumnCount('ideas') }}</p>
            </div>
            <div class="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>
        <div class="bg-gray-800 p-4 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Planning</p>
              <p class="text-xl font-bold text-white">{{ getColumnCount('planning') }}</p>
            </div>
            <div class="w-8 h-8 bg-yellow-500 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>
        <div class="bg-gray-800 p-4 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">In Progress</p>
              <p class="text-xl font-bold text-white">{{ getColumnCount('in-progress') }}</p>
            </div>
            <div class="w-8 h-8 bg-orange-500 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>
        <div class="bg-gray-800 p-4 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Ready to Publish</p>
              <p class="text-xl font-bold text-white">{{ getColumnCount('ready') }}</p>
            </div>
            <div class="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>
        <div class="bg-gray-800 p-4 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Analytics</p>
              <p class="text-xl font-bold text-white">{{ getColumnCount('analytics') }}</p>
            </div>
            <div class="w-8 h-8 bg-purple-500 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Kanban Board -->
      <div class="bg-gray-800 rounded-lg p-6">
        <div class="flex space-x-6 overflow-x-auto">
          <!-- Ideas Column -->
          <div class="flex-shrink-0 w-80">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 bg-blue-500 rounded-full"></div>
                <h3 class="text-white font-semibold">Ideas</h3>
                <span class="bg-gray-700 text-gray-300 text-xs px-2 py-1 rounded-full">{{ getColumnCount('ideas') }}</span>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"></path>
                </svg>
              </button>
            </div>
            <div class="space-y-3 min-h-96">
              <div v-for="item in getColumnItems('ideas')" :key="item.id" class="bg-gray-700 p-4 rounded-lg cursor-pointer hover:bg-gray-600 transition-colors">
                <div class="flex items-start justify-between mb-2">
                  <h4 class="text-white font-medium text-sm">{{ item.title }}</h4>
                  <button class="text-gray-400 hover:text-white">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                    </svg>
                  </button>
                </div>
                <p class="text-gray-300 text-xs mb-3">{{ item.description }}</p>
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span :class="item.priority === 'high' ? 'bg-red-500' : item.priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'" class="w-2 h-2 rounded-full"></span>
                    <span class="text-gray-400 text-xs">{{ item.priority }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="w-6 h-6 bg-pink-500 rounded-full flex items-center justify-center">
                      <span class="text-white text-xs">{{ item.assignee }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Planning Column -->
          <div class="flex-shrink-0 w-80">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <h3 class="text-white font-semibold">Planning</h3>
                <span class="bg-gray-700 text-gray-300 text-xs px-2 py-1 rounded-full">{{ getColumnCount('planning') }}</span>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"></path>
                </svg>
              </button>
            </div>
            <div class="space-y-3 min-h-96">
              <div v-for="item in getColumnItems('planning')" :key="item.id" class="bg-gray-700 p-4 rounded-lg cursor-pointer hover:bg-gray-600 transition-colors">
                <div class="flex items-start justify-between mb-2">
                  <h4 class="text-white font-medium text-sm">{{ item.title }}</h4>
                  <button class="text-gray-400 hover:text-white">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                    </svg>
                  </button>
                </div>
                <p class="text-gray-300 text-xs mb-3">{{ item.description }}</p>
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span :class="item.priority === 'high' ? 'bg-red-500' : item.priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'" class="w-2 h-2 rounded-full"></span>
                    <span class="text-gray-400 text-xs">{{ item.priority }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="w-6 h-6 bg-pink-500 rounded-full flex items-center justify-center">
                      <span class="text-white text-xs">{{ item.assignee }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- In Progress Column -->
          <div class="flex-shrink-0 w-80">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 bg-orange-500 rounded-full"></div>
                <h3 class="text-white font-semibold">In Progress</h3>
                <span class="bg-gray-700 text-gray-300 text-xs px-2 py-1 rounded-full">{{ getColumnCount('in-progress') }}</span>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"></path>
                </svg>
              </button>
            </div>
            <div class="space-y-3 min-h-96">
              <div v-for="item in getColumnItems('in-progress')" :key="item.id" class="bg-gray-700 p-4 rounded-lg cursor-pointer hover:bg-gray-600 transition-colors">
                <div class="flex items-start justify-between mb-2">
                  <h4 class="text-white font-medium text-sm">{{ item.title }}</h4>
                  <button class="text-gray-400 hover:text-white">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                    </svg>
                  </button>
                </div>
                <p class="text-gray-300 text-xs mb-3">{{ item.description }}</p>
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center space-x-2">
                    <span :class="item.priority === 'high' ? 'bg-red-500' : item.priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'" class="w-2 h-2 rounded-full"></span>
                    <span class="text-gray-400 text-xs">{{ item.priority }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="w-6 h-6 bg-pink-500 rounded-full flex items-center justify-center">
                      <span class="text-white text-xs">{{ item.assignee }}</span>
                    </div>
                  </div>
                </div>
                <div v-if="item.progress" class="w-full bg-gray-600 rounded-full h-2">
                  <div class="bg-orange-500 h-2 rounded-full" :style="`width: ${item.progress}%`"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Ready to Publish Column -->
          <div class="flex-shrink-0 w-80">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                <h3 class="text-white font-semibold">Ready to Publish</h3>
                <span class="bg-gray-700 text-gray-300 text-xs px-2 py-1 rounded-full">{{ getColumnCount('ready') }}</span>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"></path>
                </svg>
              </button>
            </div>
            <div class="space-y-3 min-h-96">
              <div v-for="item in getColumnItems('ready')" :key="item.id" class="bg-gray-700 p-4 rounded-lg cursor-pointer hover:bg-gray-600 transition-colors">
                <div class="flex items-start justify-between mb-2">
                  <h4 class="text-white font-medium text-sm">{{ item.title }}</h4>
                  <button class="text-gray-400 hover:text-white">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                    </svg>
                  </button>
                </div>
                <p class="text-gray-300 text-xs mb-3">{{ item.description }}</p>
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span :class="item.priority === 'high' ? 'bg-red-500' : item.priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'" class="w-2 h-2 rounded-full"></span>
                    <span class="text-gray-400 text-xs">{{ item.priority }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="w-6 h-6 bg-pink-500 rounded-full flex items-center justify-center">
                      <span class="text-white text-xs">{{ item.assignee }}</span>
                    </div>
                    <button class="bg-green-500 text-white px-2 py-1 rounded text-xs hover:bg-green-600">
                      Publish
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Analytics Column -->
          <div class="flex-shrink-0 w-80">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 bg-purple-500 rounded-full"></div>
                <h3 class="text-white font-semibold">Analytics</h3>
                <span class="bg-gray-700 text-gray-300 text-xs px-2 py-1 rounded-full">{{ getColumnCount('analytics') }}</span>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"></path>
                </svg>
              </button>
            </div>
            <div class="space-y-3 min-h-96">
              <div v-for="item in getColumnItems('analytics')" :key="item.id" class="bg-gray-700 p-4 rounded-lg cursor-pointer hover:bg-gray-600 transition-colors">
                <div class="flex items-start justify-between mb-2">
                  <h4 class="text-white font-medium text-sm">{{ item.title }}</h4>
                  <button class="text-gray-400 hover:text-white">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                    </svg>
                  </button>
                </div>
                <p class="text-gray-300 text-xs mb-3">{{ item.description }}</p>
                <div v-if="item.metrics" class="mb-3">
                  <div class="flex justify-between text-xs text-gray-400 mb-1">
                    <span>Views: {{ item.metrics.views }}</span>
                    <span>Engagement: {{ item.metrics.engagement }}%</span>
                  </div>
                  <div class="flex justify-between text-xs text-gray-400">
                    <span>Likes: {{ item.metrics.likes }}</span>
                    <span>Shares: {{ item.metrics.shares }}</span>
                  </div>
                </div>
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span :class="item.priority === 'high' ? 'bg-red-500' : item.priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'" class="w-2 h-2 rounded-full"></span>
                    <span class="text-gray-400 text-xs">{{ item.priority }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="w-6 h-6 bg-pink-500 rounded-full flex items-center justify-center">
                      <span class="text-white text-xs">{{ item.assignee }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Content items data
const contentItems = ref([
  // Ideas
  {
    id: 1,
    title: "YouTube Shorts Strategy Guide",
    description: "Create a comprehensive guide on YouTube Shorts best practices",
    status: "ideas",
    priority: "high",
    assignee: "M",
    createdAt: "2023-12-15"
  },
  {
    id: 2,
    title: "AI Content Creation Tools Review",
    description: "Review and compare top AI tools for content creators",
    status: "ideas",
    priority: "medium",
    assignee: "M",
    createdAt: "2023-12-14"
  },
  {
    id: 3,
    title: "Social Media Trends 2024",
    description: "Analyze upcoming social media trends for next year",
    status: "ideas",
    priority: "low",
    assignee: "M",
    createdAt: "2023-12-13"
  },

  // Planning
  {
    id: 4,
    title: "Content Calendar Template",
    description: "Design a comprehensive content calendar template",
    status: "planning",
    priority: "high",
    assignee: "M",
    createdAt: "2023-12-12"
  },
  {
    id: 5,
    title: "Brand Voice Guidelines",
    description: "Establish consistent brand voice across all platforms",
    status: "planning",
    priority: "medium",
    assignee: "M",
    createdAt: "2023-12-11"
  },

  // In Progress
  {
    id: 6,
    title: "Video Editing Masterclass",
    description: "Complete tutorial series on advanced video editing",
    status: "in-progress",
    priority: "high",
    assignee: "M",
    progress: 75,
    createdAt: "2023-12-10"
  },
  {
    id: 7,
    title: "Instagram Growth Hacks",
    description: "Proven strategies to grow Instagram following organically",
    status: "in-progress",
    priority: "medium",
    assignee: "M",
    progress: 45,
    createdAt: "2023-12-09"
  },

  // Ready to Publish
  {
    id: 8,
    title: "TikTok Algorithm Secrets",
    description: "Deep dive into how TikTok algorithm works in 2024",
    status: "ready",
    priority: "high",
    assignee: "M",
    createdAt: "2023-12-08"
  },
  {
    id: 9,
    title: "Content Monetization Guide",
    description: "Complete guide to monetizing your content across platforms",
    status: "ready",
    priority: "medium",
    assignee: "M",
    createdAt: "2023-12-07"
  },

  // Analytics
  {
    id: 10,
    title: "Q4 Performance Report",
    description: "Comprehensive analysis of Q4 content performance",
    status: "analytics",
    priority: "high",
    assignee: "M",
    metrics: {
      views: "2.4M",
      engagement: "8.7",
      likes: "156K",
      shares: "23K"
    },
    createdAt: "2023-12-06"
  },
  {
    id: 11,
    title: "Viral Video Analysis",
    description: "Breakdown of what made our top videos go viral",
    status: "analytics",
    priority: "medium",
    assignee: "M",
    metrics: {
      views: "1.8M",
      engagement: "12.3",
      likes: "89K",
      shares: "45K"
    },
    createdAt: "2023-12-05"
  }
])

// Helper functions
const getColumnItems = (status) => {
  return contentItems.value.filter(item => item.status === status)
}

const getColumnCount = (status) => {
  return getColumnItems(status).length
}
</script>