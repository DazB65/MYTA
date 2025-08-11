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
            class="flex items-center px-4 py-3 text-white bg-pink-500 rounded-lg"
          >
            <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
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
            <p class="text-xs text-gray-400">Manage your video content</p>
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
          <h2 class="text-2xl font-bold text-white">Video Analytics</h2>
          <p class="text-gray-400">Track performance and manage your content</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="relative">
            <input
              type="text"
              placeholder="Search videos..."
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
            <span>Upload</span>
          </button>
        </div>
      </div>

      <!-- Analytics Overview -->
      <div class="grid grid-cols-4 gap-6 mb-8">
        <div class="bg-gray-800 p-6 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Total Views</p>
              <p class="text-2xl font-bold text-white">2.04M</p>
              <p class="text-green-400 text-sm">+12.5% vs last month</p>
            </div>
            <div class="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"></path>
                <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 p-6 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Avg Duration</p>
              <p class="text-2xl font-bold text-white">5.3m</p>
              <p class="text-green-400 text-sm">+8.2% vs last month</p>
            </div>
            <div class="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 p-6 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Engagement</p>
              <p class="text-2xl font-bold text-white">34.6%</p>
              <p class="text-red-400 text-sm">-2.1% vs last month</p>
            </div>
            <div class="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z"></path>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 p-6 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Revenue</p>
              <p class="text-2xl font-bold text-white">$70.2K</p>
              <p class="text-green-400 text-sm">+15.3% vs last month</p>
            </div>
            <div class="w-12 h-12 bg-yellow-500 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z"></path>
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clip-rule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Videos Section -->
      <div class="bg-gray-800 rounded-lg p-6 mb-8">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-white">Recent Videos</h3>
          <div class="flex items-center space-x-4">
            <select class="bg-gray-700 text-white px-3 py-2 rounded-lg text-sm">
              <option>Last 30 days</option>
              <option>Last 7 days</option>
              <option>Last 90 days</option>
            </select>
            <button class="text-gray-400 hover:text-white">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z" clip-rule="evenodd"></path>
              </svg>
            </button>
          </div>
        </div>

        <!-- Video Grid -->
        <div class="grid grid-cols-6 gap-4">
          <div v-for="video in recentVideos" :key="video.id" class="group cursor-pointer">
            <div class="relative bg-gray-700 rounded-lg overflow-hidden aspect-video mb-3">
              <img :src="video.thumbnail" :alt="video.title" class="w-full h-full object-cover">
              <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-200 flex items-center justify-center">
                <svg class="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-200" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"></path>
                </svg>
              </div>
              <div class="absolute bottom-2 right-2 bg-black bg-opacity-75 text-white text-xs px-2 py-1 rounded">
                {{ video.duration }}
              </div>
            </div>
            <h4 class="text-white text-sm font-medium mb-1 line-clamp-2">{{ video.title }}</h4>
            <p class="text-gray-400 text-xs">{{ video.views }} views • {{ video.date }}</p>
          </div>
        </div>
      </div>

      <!-- Performance Table -->
      <div class="bg-gray-800 rounded-lg p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-white">Video Performance</h3>
          <div class="flex items-center space-x-2">
            <button class="px-3 py-1 bg-pink-500 text-white rounded text-sm">All</button>
            <button class="px-3 py-1 text-gray-400 hover:text-white rounded text-sm">Published</button>
            <button class="px-3 py-1 text-gray-400 hover:text-white rounded text-sm">Draft</button>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-700">
                <th class="text-left text-gray-400 text-sm font-medium py-3 px-4">Video</th>
                <th class="text-left text-gray-400 text-sm font-medium py-3 px-4">Status</th>
                <th class="text-left text-gray-400 text-sm font-medium py-3 px-4">Views</th>
                <th class="text-left text-gray-400 text-sm font-medium py-3 px-4">Engagement</th>
                <th class="text-left text-gray-400 text-sm font-medium py-3 px-4">Revenue</th>
                <th class="text-left text-gray-400 text-sm font-medium py-3 px-4">Date</th>
                <th class="text-left text-gray-400 text-sm font-medium py-3 px-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="video in performanceVideos" :key="video.id" class="border-b border-gray-700 hover:bg-gray-700">
                <td class="py-4 px-4">
                  <div class="flex items-center space-x-3">
                    <img :src="video.thumbnail" :alt="video.title" class="w-16 h-10 object-cover rounded">
                    <div>
                      <p class="text-white font-medium text-sm">{{ video.title }}</p>
                      <p class="text-gray-400 text-xs">{{ video.duration }}</p>
                    </div>
                  </div>
                </td>
                <td class="py-4 px-4">
                  <span :class="video.status === 'Published' ? 'bg-green-500' : 'bg-yellow-500'" class="px-2 py-1 rounded-full text-xs text-white">
                    {{ video.status }}
                  </span>
                </td>
                <td class="py-4 px-4 text-white text-sm">{{ video.views }}</td>
                <td class="py-4 px-4 text-white text-sm">{{ video.engagement }}</td>
                <td class="py-4 px-4 text-white text-sm">{{ video.revenue }}</td>
                <td class="py-4 px-4 text-gray-400 text-sm">{{ video.date }}</td>
                <td class="py-4 px-4">
                  <div class="flex items-center space-x-2">
                    <button class="text-gray-400 hover:text-white">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
                      </svg>
                    </button>
                    <button class="text-gray-400 hover:text-white">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" clip-rule="evenodd"></path>
                        <path fill-rule="evenodd" d="M4 5a2 2 0 012-2h8a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 3a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"></path>
                      </svg>
                    </button>
                    <button class="text-gray-400 hover:text-red-400">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" clip-rule="evenodd"></path>
                        <path fill-rule="evenodd" d="M4 5a2 2 0 012-2h8a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm5 3a1 1 0 000 2h.01a1 1 0 100-2H9z" clip-rule="evenodd"></path>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Sample data for videos
const recentVideos = ref([
  {
    id: 1,
    title: "How to Create Engaging Content That Converts",
    thumbnail: "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop",
    duration: "12:34",
    views: "45.2K",
    date: "2 days ago"
  },
  {
    id: 2,
    title: "Advanced YouTube Analytics Strategies",
    thumbnail: "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop",
    duration: "8:45",
    views: "32.1K",
    date: "5 days ago"
  },
  {
    id: 3,
    title: "Building Your Personal Brand Online",
    thumbnail: "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop",
    duration: "15:22",
    views: "28.7K",
    date: "1 week ago"
  },
  {
    id: 4,
    title: "Content Creation Tools & Tips",
    thumbnail: "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop",
    duration: "10:18",
    views: "19.3K",
    date: "1 week ago"
  },
  {
    id: 5,
    title: "Social Media Marketing Masterclass",
    thumbnail: "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop",
    duration: "22:15",
    views: "67.8K",
    date: "2 weeks ago"
  },
  {
    id: 6,
    title: "Video SEO Best Practices",
    thumbnail: "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop",
    duration: "9:33",
    views: "15.4K",
    date: "2 weeks ago"
  }
])

const performanceVideos = ref([
  {
    id: 1,
    title: "How to Create Engaging Content That Converts",
    thumbnail: "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=100&h=60&fit=crop",
    duration: "12:34",
    status: "Published",
    views: "45.2K",
    engagement: "8.7%",
    revenue: "$1,234",
    date: "Dec 15, 2023"
  },
  {
    id: 2,
    title: "Advanced YouTube Analytics Strategies",
    thumbnail: "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=100&h=60&fit=crop",
    duration: "8:45",
    status: "Published",
    views: "32.1K",
    engagement: "6.2%",
    revenue: "$892",
    date: "Dec 12, 2023"
  },
  {
    id: 3,
    title: "Building Your Personal Brand Online",
    thumbnail: "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=100&h=60&fit=crop",
    duration: "15:22",
    status: "Published",
    views: "28.7K",
    engagement: "9.1%",
    revenue: "$1,567",
    date: "Dec 8, 2023"
  },
  {
    id: 4,
    title: "Content Creation Tools & Tips",
    thumbnail: "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=100&h=60&fit=crop",
    duration: "10:18",
    status: "Draft",
    views: "19.3K",
    engagement: "5.4%",
    revenue: "$623",
    date: "Dec 5, 2023"
  },
  {
    id: 5,
    title: "Social Media Marketing Masterclass",
    thumbnail: "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=100&h=60&fit=crop",
    duration: "22:15",
    status: "Published",
    views: "67.8K",
    engagement: "12.3%",
    revenue: "$2,891",
    date: "Dec 1, 2023"
  }
])
</script>