<template>
  <div class="min-h-screen bg-gradient-to-b from-slate-800 via-gray-850 to-gray-900 text-white">



    <!-- Main Content Area -->
    <div class="p-6 pt-24">
      <!-- Header -->
      <div class="mb-4 flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <h1 class="text-2xl font-bold text-white">Video Analytics</h1>
          <span class="text-gray-400">•</span>
          <p class="text-gray-400">Track performance and manage your content</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search videos..."
              class="w-64 rounded-lg bg-gray-800 px-4 py-2 pl-10 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
            />
            <svg
              class="absolute left-3 top-2.5 h-5 w-5 text-gray-400"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <button
            @click="syncWithYouTube"
            :disabled="syncing"
            class="flex items-center space-x-2 rounded-lg bg-orange-500 px-4 py-2 text-white transition-colors hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg v-if="!syncing" class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                clip-rule="evenodd"
              />
            </svg>
            <svg v-else class="h-5 w-5 animate-spin" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                clip-rule="evenodd"
              />
            </svg>
            <span>{{ syncing ? 'Syncing...' : 'Sync with YouTube' }}</span>
          </button>
        </div>

        <!-- Last sync indicator -->
        <div v-if="lastSyncTime" class="text-sm text-gray-400 mt-2">
          Last synced: {{ lastSyncTime }}
        </div>
      </div>

      <!-- Recent Videos Section -->
      <div class="mb-8 rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
        <div class="mb-6 flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <h3 class="text-xl font-bold text-white">Recent Videos</h3>

            <!-- Compact Pagination Controls -->
            <div v-if="totalPages > 1" class="flex items-center space-x-2 text-sm">
              <span class="text-gray-400">Page</span>
              <button
                @click="prevPage"
                :disabled="!hasPrev"
                class="flex items-center px-2 py-1 text-gray-300 bg-gray-700 rounded hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
              <span class="text-white font-medium">{{ currentPage }}</span>
              <span class="text-gray-400">of</span>
              <span class="text-white font-medium">{{ totalPages }}</span>
              <button
                @click="nextPage"
                :disabled="!hasNext"
                class="flex items-center px-2 py-1 text-gray-300 bg-gray-700 rounded hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>

          <div class="flex items-center space-x-4">
            <!-- Sort by Pillar -->
            <select v-model="selectedPillar" class="rounded-lg bg-gray-700 px-3 py-2 text-sm text-white">
              <option value="all">All Pillars</option>
              <option value="Game Development">Game Development</option>
              <option value="Game Reviews">Game Reviews</option>
              <option value="Tech Tutorials">Tech Tutorials</option>
              <option value="Productivity Tips">Productivity Tips</option>
            </select>

            <!-- Sort by Performance -->
            <select v-model="sortBy" class="rounded-lg bg-gray-700 px-3 py-2 text-sm text-white">
              <option value="recent">Most Recent</option>
              <option value="views">Most Views</option>
              <option value="engagement">Best Engagement</option>
              <option value="duration">Longest Videos</option>
            </select>

            <button class="text-gray-400 hover:text-white">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          </div>
        </div>

        <!-- Pillar Legend -->
        <div class="mb-4 flex items-center justify-center">
          <div class="flex items-center space-x-6 rounded-lg bg-gray-800/60 px-4 py-2 border-2 border-gray-600/70 shadow-lg">
            <span class="text-sm font-medium text-gray-300">Pillar Colors:</span>
            <div class="flex items-center space-x-4">
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 rounded border-2 border-orange-500"></div>
                <span class="text-xs text-gray-400">Game Development</span>
              </div>
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 rounded border-2 border-blue-500"></div>
                <span class="text-xs text-gray-400">Game Reviews</span>
              </div>
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 rounded border-2 border-purple-500"></div>
                <span class="text-xs text-gray-400">Tech Tutorials</span>
              </div>
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 rounded border-2 border-green-500"></div>
                <span class="text-xs text-gray-400">Productivity Tips</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Video Grid -->
        <div class="grid grid-cols-4 gap-6">
          <div v-for="video in filteredAndSortedVideos" :key="video.id" :class="getVideoCardClasses(video)" @click="openVideoStats(video)">
            <div class="relative mb-3 aspect-video overflow-hidden rounded-lg bg-gray-700">
              <img :src="video.thumbnail" :alt="video.title" class="h-full w-full object-cover" />
              <div
                class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-0 transition-all duration-200 group-hover:bg-opacity-30"
              >
                <svg
                  class="h-8 w-8 text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
              <div
                class="absolute bottom-2 right-2 rounded bg-black bg-opacity-75 px-2 py-1 text-xs text-white"
              >
                {{ video.duration }}
              </div>
            </div>
            <div class="flex items-start space-x-2 mb-1">
              <span class="text-white text-sm mt-0.5">🎬</span>
              <h4 class="line-clamp-2 text-sm font-medium text-white">{{ video.title }}</h4>
            </div>
            <p class="text-xs text-gray-400">{{ formatNumber(video.detailedStats?.views || 0) }} views • {{ formatDate(video.date) }}</p>
          </div>
        </div>

        <!-- Video count info -->
        <div v-if="totalPages > 1" class="mt-6 text-center">
          <div class="text-sm text-gray-400">
            Showing {{ ((currentPage - 1) * perPage) + 1 }} to {{ Math.min(currentPage * perPage, totalCount) }} of {{ totalCount }} videos
          </div>
        </div>
      </div>


    </div>

    <!-- Video Stats Modal -->
    <VideoStatsModal
      :show="showStatsModal"
      :video="selectedVideo"
      @close="closeStatsModal"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// State for sync functionality
const syncing = ref(false)
const lastSyncTime = ref(null)

// State for video stats modal
const showStatsModal = ref(false)
const selectedVideo = ref(null)

// State for filtering and sorting
const selectedPillar = ref('all')
const sortBy = ref('recent')

// Reactive state for videos and pagination
const videos = ref([])
const loading = ref(false)
const error = ref(null)

// Pagination state
const currentPage = ref(1)
const perPage = ref(12)
const totalCount = ref(0)
const totalPages = ref(0)
const hasNext = ref(false)
const hasPrev = ref(false)

// Filter state
const searchQuery = ref('')
const selectedTier = ref('')
const dateFrom = ref('')
const dateTo = ref('')

// Sample video data with detailed stats (fallback for development)
const mockVideos = ref([
  {
    id: 1,
    title: "10 YouTube Growth Hacks That Actually Work in 2024",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "12:34",
    date: "2024-01-15",
    pillar: {
      name: "Productivity Tips",
      icon: "ProductivityIcon"
    },
    performance: "Excellent",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 45200,
      viewsGrowth: 12.5,
      likes: 2260,
      likeRatio: 8.2,
      comments: 904,
      engagement: 6.8,
      watchTime: "8:45",
      retention: 68,
      ctr: 8.2,
      trafficSources: [
        { name: "YouTube Search", percentage: 35 },
        { name: "Suggested Videos", percentage: 28 },
        { name: "Browse Features", percentage: 15 },
        { name: "External", percentage: 12 },
        { name: "Direct", percentage: 10 }
      ],
      topCountries: [
        { name: "United States", percentage: 45 },
        { name: "United Kingdom", percentage: 18 },
        { name: "Canada", percentage: 12 },
        { name: "Australia", percentage: 8 },
        { name: "Germany", percentage: 7 }
      ]
    },
    suggestedKeywords: ["youtube growth", "content strategy", "creator tips"]
  },
  {
    id: 2,
    title: "My Biggest YouTube Mistakes (And How to Avoid Them)",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "15:22",
    date: "2024-01-12",
    pillar: {
      name: "Game Development",
      icon: "GameIcon"
    },
    performance: "Good",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 28900,
      viewsGrowth: 8.3,
      likes: 1445,
      likeRatio: 6.5,
      comments: 578,
      engagement: 5.2,
      watchTime: "9:12",
      retention: 52,
      ctr: 6.5,
      trafficSources: [
        { name: "Suggested Videos", percentage: 42 },
        { name: "YouTube Search", percentage: 25 },
        { name: "Browse Features", percentage: 18 },
        { name: "External", percentage: 8 },
        { name: "Direct", percentage: 7 }
      ],
      topCountries: [
        { name: "United States", percentage: 38 },
        { name: "United Kingdom", percentage: 22 },
        { name: "Canada", percentage: 15 },
        { name: "Australia", percentage: 10 },
        { name: "Germany", percentage: 8 }
      ]
    },
    suggestedKeywords: ["youtube mistakes", "creator advice", "learning"]
  },
  {
    id: 3,
    title: "Creating Viral Content: The Complete Guide",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "18:45",
    date: "2024-01-10",
    pillar: {
      name: "Tech Tutorials",
      icon: "TechIcon"
    },
    performance: "Average",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 15600,
      viewsGrowth: -5.2,
      likes: 780,
      likeRatio: 4.8,
      comments: 312,
      engagement: 4.1,
      watchTime: "7:23",
      retention: 41,
      ctr: 4.8,
      trafficSources: [
        { name: "YouTube Search", percentage: 48 },
        { name: "Suggested Videos", percentage: 22 },
        { name: "Browse Features", percentage: 15 },
        { name: "External", percentage: 10 },
        { name: "Direct", percentage: 5 }
      ],
      topCountries: [
        { name: "United States", percentage: 42 },
        { name: "India", percentage: 18 },
        { name: "United Kingdom", percentage: 12 },
        { name: "Canada", percentage: 10 },
        { name: "Brazil", percentage: 8 }
      ]
    },
    suggestedKeywords: ["viral content", "content strategy", "social media"]
  },
  {
    id: 4,
    title: "Behind the Scenes: My Content Creation Process",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "22:10",
    date: "2024-01-08",
    pillar: {
      name: "Game Reviews",
      icon: "ReviewIcon"
    },
    performance: "Poor",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 8200,
      viewsGrowth: -12.8,
      likes: 410,
      likeRatio: 3.2,
      comments: 164,
      engagement: 2.9,
      watchTime: "6:45",
      retention: 29,
      ctr: 3.2,
      trafficSources: [
        { name: "Suggested Videos", percentage: 35 },
        { name: "YouTube Search", percentage: 30 },
        { name: "Browse Features", percentage: 20 },
        { name: "External", percentage: 8 },
        { name: "Direct", percentage: 7 }
      ],
      topCountries: [
        { name: "United States", percentage: 40 },
        { name: "United Kingdom", percentage: 20 },
        { name: "Canada", percentage: 15 },
        { name: "Australia", percentage: 12 },
        { name: "Germany", percentage: 8 }
      ]
    },
    suggestedKeywords: ["behind the scenes", "content creation", "workflow"]
  },
  {
    id: 5,
    title: "Gaming Setup Tour 2024: Everything You Need to Know",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "16:28",
    date: "2024-01-05",
    pillar: {
      name: "Game Development",
      icon: "GameIcon"
    },
    performance: "Good",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 32100,
      viewsGrowth: 15.7,
      likes: 1605,
      likeRatio: 7.1,
      comments: 642,
      engagement: 6.2,
      watchTime: "10:15",
      retention: 58,
      ctr: 7.1,
      trafficSources: [
        { name: "YouTube Search", percentage: 38 },
        { name: "Suggested Videos", percentage: 32 },
        { name: "Browse Features", percentage: 15 },
        { name: "External", percentage: 10 },
        { name: "Direct", percentage: 5 }
      ],
      topCountries: [
        { name: "United States", percentage: 35 },
        { name: "Germany", percentage: 18 },
        { name: "United Kingdom", percentage: 15 },
        { name: "Canada", percentage: 12 },
        { name: "France", percentage: 10 }
      ]
    },
    suggestedKeywords: ["gaming setup", "pc build", "gaming gear"]
  },
  {
    id: 6,
    title: "Tech Review: The Best Cameras for Content Creators",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "14:52",
    date: "2024-01-03",
    pillar: {
      name: "Tech Tutorials",
      icon: "TechIcon"
    },
    performance: "Excellent",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 67800,
      viewsGrowth: 22.4,
      likes: 3390,
      likeRatio: 9.1,
      comments: 1356,
      engagement: 8.4,
      watchTime: "11:30",
      retention: 72,
      ctr: 9.1,
      trafficSources: [
        { name: "YouTube Search", percentage: 45 },
        { name: "Suggested Videos", percentage: 25 },
        { name: "Browse Features", percentage: 12 },
        { name: "External", percentage: 10 },
        { name: "Direct", percentage: 8 }
      ],
      topCountries: [
        { name: "United States", percentage: 40 },
        { name: "United Kingdom", percentage: 16 },
        { name: "Canada", percentage: 14 },
        { name: "Australia", percentage: 12 },
        { name: "Germany", percentage: 10 }
      ]
    },
    suggestedKeywords: ["camera review", "content creation", "tech gear"]
  },
  {
    id: 7,
    title: "How I Edit My YouTube Videos: Complete Workflow",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "19:33",
    date: "2024-01-01",
    pillar: {
      name: "Productivity Tips",
      icon: "ProductivityIcon"
    },
    performance: "Excellent",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 52300,
      viewsGrowth: 18.9,
      likes: 2615,
      likeRatio: 8.7,
      comments: 1047,
      engagement: 7.3,
      watchTime: "12:45",
      retention: 65,
      ctr: 8.7,
      trafficSources: [
        { name: "YouTube Search", percentage: 41 },
        { name: "Suggested Videos", percentage: 29 },
        { name: "Browse Features", percentage: 16 },
        { name: "External", percentage: 9 },
        { name: "Direct", percentage: 5 }
      ],
      topCountries: [
        { name: "United States", percentage: 38 },
        { name: "United Kingdom", percentage: 18 },
        { name: "Canada", percentage: 15 },
        { name: "Australia", percentage: 11 },
        { name: "Germany", percentage: 9 }
      ]
    },
    suggestedKeywords: ["video editing", "workflow", "tutorial"]
  },
  {
    id: 8,
    title: "React vs Vue: Which Framework Should You Choose in 2024?",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "21:15",
    date: "2023-12-28",
    pillar: "Tech Tutorials",
    category: "Comparison",
    performance: "Good",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 34700,
      viewsGrowth: 11.2,
      likes: 1735,
      likeRatio: 7.4,
      comments: 693,
      engagement: 6.1,
      watchTime: "13:20",
      retention: 58,
      ctr: 7.4,
      trafficSources: [
        { name: "YouTube Search", percentage: 44 },
        { name: "Suggested Videos", percentage: 26 },
        { name: "Browse Features", percentage: 14 },
        { name: "External", percentage: 11 },
        { name: "Direct", percentage: 5 }
      ],
      topCountries: [
        { name: "United States", percentage: 42 },
        { name: "India", percentage: 16 },
        { name: "United Kingdom", percentage: 14 },
        { name: "Canada", percentage: 12 },
        { name: "Germany", percentage: 8 }
      ]
    },
    suggestedKeywords: ["react", "vue", "javascript", "framework comparison"]
  },
  {
    id: 9,
    title: "Building My Dream Gaming Setup on a Budget",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "17:42",
    date: "2023-12-25",
    pillar: "Game Reviews",
    category: "Setup",
    performance: "Average",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 19800,
      viewsGrowth: -2.1,
      likes: 990,
      likeRatio: 5.9,
      comments: 396,
      engagement: 4.8,
      watchTime: "9:30",
      retention: 47,
      ctr: 5.9,
      trafficSources: [
        { name: "Suggested Videos", percentage: 38 },
        { name: "YouTube Search", percentage: 32 },
        { name: "Browse Features", percentage: 18 },
        { name: "External", percentage: 7 },
        { name: "Direct", percentage: 5 }
      ],
      topCountries: [
        { name: "United States", percentage: 35 },
        { name: "United Kingdom", percentage: 19 },
        { name: "Canada", percentage: 16 },
        { name: "Australia", percentage: 13 },
        { name: "Germany", percentage: 10 }
      ]
    },
    suggestedKeywords: ["gaming setup", "budget build", "pc gaming"]
  },
  {
    id: 10,
    title: "Why I Quit My 9-5 Job to Become a Content Creator",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "13:28",
    date: "2023-12-22",
    pillar: "Productivity Tips",
    category: "Vlog",
    performance: "Excellent",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 78900,
      viewsGrowth: 25.6,
      likes: 3945,
      likeRatio: 9.3,
      comments: 1578,
      engagement: 8.9,
      watchTime: "10:15",
      retention: 71,
      ctr: 9.3,
      trafficSources: [
        { name: "Suggested Videos", percentage: 45 },
        { name: "YouTube Search", percentage: 28 },
        { name: "Browse Features", percentage: 12 },
        { name: "External", percentage: 10 },
        { name: "Direct", percentage: 5 }
      ],
      topCountries: [
        { name: "United States", percentage: 44 },
        { name: "United Kingdom", percentage: 17 },
        { name: "Canada", percentage: 15 },
        { name: "Australia", percentage: 11 },
        { name: "Germany", percentage: 8 }
      ]
    },
    suggestedKeywords: ["career change", "content creator", "entrepreneurship"]
  },
  {
    id: 11,
    title: "Top 5 AI Tools Every Creator Needs in 2024",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "16:07",
    date: "2023-12-20",
    pillar: "Tech Tutorials",
    category: "Review",
    performance: "Good",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 41200,
      viewsGrowth: 14.3,
      likes: 2060,
      likeRatio: 8.1,
      comments: 824,
      engagement: 6.7,
      watchTime: "11:45",
      retention: 62,
      ctr: 8.1,
      trafficSources: [
        { name: "YouTube Search", percentage: 39 },
        { name: "Suggested Videos", percentage: 31 },
        { name: "Browse Features", percentage: 15 },
        { name: "External", percentage: 10 },
        { name: "Direct", percentage: 5 }
      ],
      topCountries: [
        { name: "United States", percentage: 41 },
        { name: "India", percentage: 18 },
        { name: "United Kingdom", percentage: 15 },
        { name: "Canada", percentage: 12 },
        { name: "Germany", percentage: 9 }
      ]
    },
    suggestedKeywords: ["AI tools", "content creation", "productivity"]
  },
  {
    id: 12,
    title: "My First Year on YouTube: Lessons Learned",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "20:45",
    date: "2023-12-18",
    pillar: "Productivity Tips",
    category: "Reflection",
    performance: "Average",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 23400,
      viewsGrowth: 3.7,
      likes: 1170,
      likeRatio: 6.2,
      comments: 468,
      engagement: 5.1,
      watchTime: "12:30",
      retention: 53,
      ctr: 6.2,
      trafficSources: [
        { name: "Suggested Videos", percentage: 42 },
        { name: "YouTube Search", percentage: 29 },
        { name: "Browse Features", percentage: 16 },
        { name: "External", percentage: 8 },
        { name: "Direct", percentage: 5 }
      ],
      topCountries: [
        { name: "United States", percentage: 39 },
        { name: "United Kingdom", percentage: 18 },
        { name: "Canada", percentage: 16 },
        { name: "Australia", percentage: 12 },
        { name: "Germany", percentage: 10 }
      ]
    },
    suggestedKeywords: ["youtube journey", "creator tips", "lessons learned"]
  },
  {
    id: 13,
    title: "Coding a Full-Stack App in 24 Hours Challenge",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "25:12",
    date: "2023-12-15",
    pillar: "Tech Tutorials",
    category: "Challenge",
    performance: "Excellent",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 89300,
      viewsGrowth: 31.4,
      likes: 4465,
      likeRatio: 9.8,
      comments: 1786,
      engagement: 9.2,
      watchTime: "18:30",
      retention: 74,
      ctr: 9.8,
      trafficSources: [
        { name: "YouTube Search", percentage: 43 },
        { name: "Suggested Videos", percentage: 32 },
        { name: "Browse Features", percentage: 13 },
        { name: "External", percentage: 8 },
        { name: "Direct", percentage: 4 }
      ],
      topCountries: [
        { name: "United States", percentage: 45 },
        { name: "India", percentage: 19 },
        { name: "United Kingdom", percentage: 13 },
        { name: "Canada", percentage: 11 },
        { name: "Germany", percentage: 7 }
      ]
    },
    suggestedKeywords: ["coding challenge", "full stack", "programming"]
  },
  {
    id: 14,
    title: "The Truth About YouTube Shorts vs Long Form Content",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "14:33",
    date: "2023-12-12",
    pillar: "Productivity Tips",
    category: "Analysis",
    performance: "Good",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 36800,
      viewsGrowth: 9.7,
      likes: 1840,
      likeRatio: 7.6,
      comments: 736,
      engagement: 6.4,
      watchTime: "9:45",
      retention: 59,
      ctr: 7.6,
      trafficSources: [
        { name: "Suggested Videos", percentage: 41 },
        { name: "YouTube Search", percentage: 33 },
        { name: "Browse Features", percentage: 14 },
        { name: "External", percentage: 8 },
        { name: "Direct", percentage: 4 }
      ],
      topCountries: [
        { name: "United States", percentage: 42 },
        { name: "United Kingdom", percentage: 17 },
        { name: "Canada", percentage: 16 },
        { name: "Australia", percentage: 13 },
        { name: "Germany", percentage: 8 }
      ]
    },
    suggestedKeywords: ["youtube shorts", "content strategy", "algorithm"]
  },
  {
    id: 15,
    title: "Unboxing the Latest MacBook Pro M3: First Impressions",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "12:18",
    date: "2023-12-10",
    pillar: "Tech Tutorials",
    category: "Unboxing",
    performance: "Average",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 27600,
      viewsGrowth: 5.2,
      likes: 1380,
      likeRatio: 6.8,
      comments: 552,
      engagement: 5.3,
      watchTime: "8:15",
      retention: 51,
      ctr: 6.8,
      trafficSources: [
        { name: "YouTube Search", percentage: 46 },
        { name: "Suggested Videos", percentage: 28 },
        { name: "Browse Features", percentage: 15 },
        { name: "External", percentage: 7 },
        { name: "Direct", percentage: 4 }
      ],
      topCountries: [
        { name: "United States", percentage: 40 },
        { name: "United Kingdom", percentage: 18 },
        { name: "Canada", percentage: 15 },
        { name: "Australia", percentage: 12 },
        { name: "Germany", percentage: 10 }
      ]
    },
    suggestedKeywords: ["macbook pro", "unboxing", "apple", "tech review"]
  },
  {
    id: 16,
    title: "Day in the Life of a Content Creator: Behind the Scenes",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "18:55",
    date: "2023-12-08",
    pillar: "Productivity Tips",
    category: "Vlog",
    performance: "Good",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 44100,
      viewsGrowth: 12.8,
      likes: 2205,
      likeRatio: 8.3,
      comments: 882,
      engagement: 7.1,
      watchTime: "13:20",
      retention: 64,
      ctr: 8.3,
      trafficSources: [
        { name: "Suggested Videos", percentage: 39 },
        { name: "YouTube Search", percentage: 31 },
        { name: "Browse Features", percentage: 17 },
        { name: "External", percentage: 9 },
        { name: "Direct", percentage: 4 }
      ],
      topCountries: [
        { name: "United States", percentage: 41 },
        { name: "United Kingdom", percentage: 19 },
        { name: "Canada", percentage: 16 },
        { name: "Australia", percentage: 12 },
        { name: "Germany", percentage: 8 }
      ]
    },
    suggestedKeywords: ["day in the life", "content creator", "behind the scenes"]
  },
  {
    id: 17,
    title: "How to Optimize Your YouTube Thumbnails for More Clicks",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "11:42",
    date: "2023-12-05",
    pillar: "Productivity Tips",
    category: "Tutorial",
    performance: "Excellent",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 63700,
      viewsGrowth: 21.9,
      likes: 3185,
      likeRatio: 9.1,
      comments: 1274,
      engagement: 8.6,
      watchTime: "8:45",
      retention: 69,
      ctr: 9.1,
      trafficSources: [
        { name: "YouTube Search", percentage: 44 },
        { name: "Suggested Videos", percentage: 29 },
        { name: "Browse Features", percentage: 14 },
        { name: "External", percentage: 9 },
        { name: "Direct", percentage: 4 }
      ],
      topCountries: [
        { name: "United States", percentage: 43 },
        { name: "United Kingdom", percentage: 16 },
        { name: "Canada", percentage: 15 },
        { name: "Australia", percentage: 12 },
        { name: "Germany", percentage: 9 }
      ]
    },
    suggestedKeywords: ["youtube thumbnails", "click through rate", "youtube tips"]
  },
  {
    id: 18,
    title: "Building a Mechanical Keyboard from Scratch",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "23:17",
    date: "2023-12-03",
    pillar: "Tech Tutorials",
    category: "DIY",
    performance: "Average",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 18900,
      viewsGrowth: -1.4,
      likes: 945,
      likeRatio: 5.7,
      comments: 378,
      engagement: 4.6,
      watchTime: "11:30",
      retention: 46,
      ctr: 5.7,
      trafficSources: [
        { name: "YouTube Search", percentage: 38 },
        { name: "Suggested Videos", percentage: 34 },
        { name: "Browse Features", percentage: 16 },
        { name: "External", percentage: 8 },
        { name: "Direct", percentage: 4 }
      ],
      topCountries: [
        { name: "United States", percentage: 37 },
        { name: "United Kingdom", percentage: 20 },
        { name: "Canada", percentage: 17 },
        { name: "Australia", percentage: 13 },
        { name: "Germany", percentage: 9 }
      ]
    },
    suggestedKeywords: ["mechanical keyboard", "diy", "custom keyboard"]
  },
  {
    id: 19,
    title: "My Biggest Content Creation Mistakes and How to Avoid Them",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "16:44",
    date: "2023-12-01",
    pillar: "Productivity Tips",
    category: "Education",
    performance: "Good",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 38200,
      viewsGrowth: 13.1,
      likes: 1910,
      likeRatio: 7.8,
      comments: 764,
      engagement: 6.5,
      watchTime: "11:20",
      retention: 61,
      ctr: 7.8,
      trafficSources: [
        { name: "Suggested Videos", percentage: 40 },
        { name: "YouTube Search", percentage: 32 },
        { name: "Browse Features", percentage: 15 },
        { name: "External", percentage: 9 },
        { name: "Direct", percentage: 4 }
      ],
      topCountries: [
        { name: "United States", percentage: 41 },
        { name: "United Kingdom", percentage: 18 },
        { name: "Canada", percentage: 16 },
        { name: "Australia", percentage: 12 },
        { name: "Germany", percentage: 9 }
      ]
    },
    suggestedKeywords: ["content creation", "mistakes", "creator tips"]
  },
  {
    id: 20,
    title: "Testing Viral TikTok Life Hacks: Do They Actually Work?",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "13:29",
    date: "2023-11-28",
    pillar: "Tech Tutorials",
    category: "Entertainment",
    performance: "Excellent",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 95600,
      viewsGrowth: 28.7,
      likes: 4780,
      likeRatio: 9.5,
      comments: 1912,
      engagement: 9.1,
      watchTime: "10:15",
      retention: 73,
      ctr: 9.5,
      trafficSources: [
        { name: "Suggested Videos", percentage: 48 },
        { name: "YouTube Search", percentage: 26 },
        { name: "Browse Features", percentage: 12 },
        { name: "External", percentage: 10 },
        { name: "Direct", percentage: 4 }
      ],
      topCountries: [
        { name: "United States", percentage: 46 },
        { name: "United Kingdom", percentage: 16 },
        { name: "Canada", percentage: 14 },
        { name: "Australia", percentage: 11 },
        { name: "Germany", percentage: 8 }
      ]
    },
    suggestedKeywords: ["life hacks", "tiktok", "viral", "testing"]
  },
  {
    id: 21,
    title: "Setting Up the Perfect Home Office for Productivity",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "15:36",
    date: "2023-11-25",
    pillar: "Productivity Tips",
    category: "Lifestyle",
    performance: "Average",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 22400,
      viewsGrowth: 1.8,
      likes: 1120,
      likeRatio: 6.1,
      comments: 448,
      engagement: 4.9,
      watchTime: "9:45",
      retention: 49,
      ctr: 6.1,
      trafficSources: [
        { name: "YouTube Search", percentage: 41 },
        { name: "Suggested Videos", percentage: 33 },
        { name: "Browse Features", percentage: 14 },
        { name: "External", percentage: 8 },
        { name: "Direct", percentage: 4 }
      ],
      topCountries: [
        { name: "United States", percentage: 38 },
        { name: "United Kingdom", percentage: 19 },
        { name: "Canada", percentage: 17 },
        { name: "Australia", percentage: 13 },
        { name: "Germany", percentage: 9 }
      ]
    },
    suggestedKeywords: ["home office", "productivity", "workspace setup"]
  },
  {
    id: 22,
    title: "Learning Python in 30 Days: My Coding Journey",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "22:18",
    date: "2023-11-22",
    pillar: "Tech Tutorials",
    category: "Education",
    performance: "Good",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 47300,
      viewsGrowth: 16.4,
      likes: 2365,
      likeRatio: 8.4,
      comments: 946,
      engagement: 7.2,
      watchTime: "15:30",
      retention: 66,
      ctr: 8.4,
      trafficSources: [
        { name: "YouTube Search", percentage: 45 },
        { name: "Suggested Videos", percentage: 28 },
        { name: "Browse Features", percentage: 13 },
        { name: "External", percentage: 10 },
        { name: "Direct", percentage: 4 }
      ],
      topCountries: [
        { name: "United States", percentage: 43 },
        { name: "India", percentage: 20 },
        { name: "United Kingdom", percentage: 14 },
        { name: "Canada", percentage: 11 },
        { name: "Germany", percentage: 8 }
      ]
    },
    suggestedKeywords: ["python", "coding", "programming", "learning"]
  },
  {
    id: 23,
    title: "The Rise and Fall of My First Startup: Lessons Learned",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "24:51",
    date: "2023-11-20",
    pillar: "Productivity Tips",
    category: "Business",
    performance: "Excellent",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 72800,
      viewsGrowth: 24.3,
      likes: 3640,
      likeRatio: 9.2,
      comments: 1456,
      engagement: 8.7,
      watchTime: "17:45",
      retention: 70,
      ctr: 9.2,
      trafficSources: [
        { name: "Suggested Videos", percentage: 42 },
        { name: "YouTube Search", percentage: 30 },
        { name: "Browse Features", percentage: 14 },
        { name: "External", percentage: 10 },
        { name: "Direct", percentage: 4 }
      ],
      topCountries: [
        { name: "United States", percentage: 44 },
        { name: "United Kingdom", percentage: 17 },
        { name: "Canada", percentage: 15 },
        { name: "Australia", percentage: 12 },
        { name: "Germany", percentage: 8 }
      ]
    },
    suggestedKeywords: ["startup", "entrepreneurship", "business", "failure"]
  },
  {
    id: 24,
    title: "Ultimate Guide to Streaming Setup: Hardware and Software",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "19:27",
    date: "2023-11-18",
    pillar: "Game Reviews",
    category: "Tutorial",
    performance: "Average",
    youtubeUrl: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    detailedStats: {
      views: 31500,
      viewsGrowth: 7.9,
      likes: 1575,
      likeRatio: 7.2,
      comments: 630,
      engagement: 5.8,
      watchTime: "12:15",
      retention: 55,
      ctr: 7.2,
      trafficSources: [
        { name: "YouTube Search", percentage: 42 },
        { name: "Suggested Videos", percentage: 30 },
        { name: "Browse Features", percentage: 15 },
        { name: "External", percentage: 9 },
        { name: "Direct", percentage: 4 }
      ],
      topCountries: [
        { name: "United States", percentage: 40 },
        { name: "United Kingdom", percentage: 18 },
        { name: "Canada", percentage: 16 },
        { name: "Australia", percentage: 13 },
        { name: "Germany", percentage: 10 }
      ]
    },
    suggestedKeywords: ["streaming setup", "obs", "twitch", "gaming"]
  }
])

// Computed property for filtered and sorted videos with pagination
const filteredAndSortedVideos = computed(() => {
  let filtered = videos.value

  // Filter by pillar - handle both string and object pillar formats
  if (selectedPillar.value !== 'all') {
    filtered = filtered.filter(video => {
      const pillarName = typeof video.pillar === 'string'
        ? video.pillar
        : video.pillar?.name || ''
      return pillarName === selectedPillar.value
    })
  }

  // Sort videos
  const sorted = filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'views':
        return (b.detailedStats?.views || 0) - (a.detailedStats?.views || 0)
      case 'engagement':
        return (b.detailedStats?.engagement || 0) - (a.detailedStats?.engagement || 0)
      case 'duration':
        // Convert duration to seconds for comparison
        const aDuration = a.duration.split(':').reduce((acc, time) => (60 * acc) + +time, 0)
        const bDuration = b.duration.split(':').reduce((acc, time) => (60 * acc) + +time, 0)
        return bDuration - aDuration
      case 'recent':
      default:
        return new Date(b.date) - new Date(a.date)
    }
  })

  // Apply pagination - show only current page videos (12 videos = 3 rows × 4 columns)
  const startIndex = (currentPage.value - 1) * perPage.value
  const endIndex = startIndex + perPage.value

  // Update total count for pagination controls
  totalCount.value = sorted.length
  totalPages.value = Math.ceil(sorted.length / perPage.value)
  hasNext.value = currentPage.value < totalPages.value
  hasPrev.value = currentPage.value > 1

  return sorted.slice(startIndex, endIndex)
})

// Sync with YouTube function
const syncWithYouTube = async () => {
  syncing.value = true
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    lastSyncTime.value = new Date()
    console.log('Synced with YouTube successfully')
  } catch (error) {
    console.error('Failed to sync with YouTube:', error)
  } finally {
    syncing.value = false
  }
}

// Video stats modal functions
const openVideoStats = (video) => {
  selectedVideo.value = video
  showStatsModal.value = true
}

const closeStatsModal = () => {
  showStatsModal.value = false
  selectedVideo.value = null
}

// Helper function to format numbers
const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

// Helper function to format dates
const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 1) return '1 day ago'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  return `${Math.floor(diffDays / 30)} months ago`
}

// API Functions
const fetchVideos = async () => {
  loading.value = true
  error.value = null

  try {
    const params = new URLSearchParams({
      page: currentPage.value.toString(),
      per_page: perPage.value.toString(),
      sort_by: sortBy.value === 'recent' ? 'published_at' : 'performance_score',
      sort_order: sortBy.value === 'recent' ? 'DESC' : 'DESC'
    })

    // Add filters if they exist
    if (searchQuery.value) params.append('search', searchQuery.value)
    if (selectedPillar.value && selectedPillar.value !== 'all') params.append('pillar_id', selectedPillar.value)
    if (selectedTier.value) params.append('performance_tier', selectedTier.value)
    if (dateFrom.value) params.append('date_from', dateFrom.value)
    if (dateTo.value) params.append('date_to', dateTo.value)

    const response = await fetch(`/api/videos?${params}`)

    if (!response.ok) {
      throw new Error('Failed to fetch videos')
    }

    const data = await response.json()

    if (data.success) {
      videos.value = data.data.videos
      totalCount.value = data.data.pagination.total_count
      totalPages.value = data.data.pagination.total_pages
      hasNext.value = data.data.pagination.has_next
      hasPrev.value = data.data.pagination.has_prev
    } else {
      throw new Error('API returned error')
    }

  } catch (err) {
    console.error('Error fetching videos:', err)
    error.value = 'Failed to load videos'
    // Fallback to mock data for development - only if no videos loaded yet
    if (videos.value.length === 0) {
      videos.value = mockVideos.value
      totalCount.value = mockVideos.value.length
      totalPages.value = Math.ceil(mockVideos.value.length / perPage.value)
      hasNext.value = totalPages.value > 1
      hasPrev.value = false
      error.value = null // Clear error when using mock data
    }
  } finally {
    loading.value = false
  }
}

// Pagination functions
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    fetchVideos()
  }
}

const nextPage = () => {
  if (hasNext.value) {
    goToPage(currentPage.value + 1)
  }
}

const prevPage = () => {
  if (hasPrev.value) {
    goToPage(currentPage.value - 1)
  }
}

// Filter functions
const applyFilters = () => {
  currentPage.value = 1 // Reset to first page when filtering
  fetchVideos()
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedPillar.value = 'all'
  selectedTier.value = ''
  dateFrom.value = ''
  dateTo.value = ''
  currentPage.value = 1
  fetchVideos()
}

// Debounced search function
let searchTimeout = null

// Watch for filter changes with proper debouncing
watch([searchQuery, selectedPillar, selectedTier, dateFrom, dateTo, sortBy], () => {
  // Clear existing timeout
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }

  // Debounce search queries, apply others immediately
  if (searchQuery.value) {
    searchTimeout = setTimeout(() => {
      applyFilters()
    }, 500)
  } else {
    applyFilters()
  }
})

// Pagination helper functions
const getPageNumbers = () => {
  const pages = []
  const maxVisible = 5

  if (totalPages.value <= maxVisible) {
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i)
    }
  } else {
    // Always show first page
    pages.push(1)

    // Calculate range around current page
    let start = Math.max(2, currentPage.value - 1)
    let end = Math.min(totalPages.value - 1, currentPage.value + 1)

    // Add ellipsis if needed
    if (start > 2) {
      pages.push('...')
    }

    // Add pages around current
    for (let i = start; i <= end; i++) {
      if (i !== 1 && i !== totalPages.value) {
        pages.push(i)
      }
    }

    // Add ellipsis if needed
    if (end < totalPages.value - 1) {
      pages.push('...')
    }

    // Always show last page
    if (totalPages.value > 1) {
      pages.push(totalPages.value)
    }
  }

  return pages
}

// Load more function (alternative to pagination)
const loadMore = async () => {
  if (!hasNext.value || loading.value) return

  const nextPage = currentPage.value + 1
  loading.value = true

  try {
    const params = new URLSearchParams({
      page: nextPage.toString(),
      per_page: perPage.value.toString(),
      sort_by: sortBy.value === 'recent' ? 'published_at' : 'performance_score',
      sort_order: 'DESC'
    })

    if (searchQuery.value) params.append('search', searchQuery.value)
    if (selectedPillar.value && selectedPillar.value !== 'all') params.append('pillar_id', selectedPillar.value)

    const response = await fetch(`/api/videos?${params}`)
    const data = await response.json()

    if (data.success) {
      videos.value = [...videos.value, ...data.data.videos]
      currentPage.value = nextPage
      hasNext.value = data.data.pagination.has_next
    }
  } catch (err) {
    console.error('Error loading more videos:', err)
  } finally {
    loading.value = false
  }
}

// Get video card classes based on pillar for enhanced borders
const getVideoCardClasses = (video) => {
  const baseClasses = "group cursor-pointer rounded-lg p-3 transition-all duration-300 hover:scale-[1.02] hover:shadow-lg bg-gray-800"

  // Get pillar name and icon - handle both string and object formats
  let pillarIcon = null
  if (typeof video.pillar === 'string') {
    // Map pillar names to icons
    const pillarIconMap = {
      'Game Development': 'GameIcon',
      'Game Reviews': 'ReviewIcon',
      'Tech Tutorials': 'TechIcon',
      'Productivity Tips': 'ProductivityIcon'
    }
    pillarIcon = pillarIconMap[video.pillar]
  } else if (video.pillar?.icon) {
    pillarIcon = video.pillar.icon
  }

  // Get pillar-based border colors
  const pillarColors = getPillarCardColors(pillarIcon)

  return `${baseClasses} border-2 ${pillarColors.border} ${pillarColors.shadow} shadow-sm`
}

// Get pillar-based border colors for videos
const getPillarCardColors = (pillarIcon) => {
  const colorMap = {
    'GameIcon': {
      border: 'border-orange-500/60',
      shadow: 'shadow-orange-500/20'
    },
    'ReviewIcon': {
      border: 'border-blue-500/60',
      shadow: 'shadow-blue-500/20'
    },
    'TechIcon': {
      border: 'border-purple-500/60',
      shadow: 'shadow-purple-500/20'
    },
    'ProductivityIcon': {
      border: 'border-green-500/60',
      shadow: 'shadow-green-500/20'
    },
    'default': {
      border: 'border-gray-600/60',
      shadow: 'shadow-gray-600/20'
    }
  }
  return colorMap[pillarIcon] || colorMap.default
}

// Calculate performance level based on video metrics
const calculatePerformance = (video) => {
  if (!video.detailedStats) return 'Unknown'

  const stats = video.detailedStats
  let score = 0
  let maxScore = 100

  // CTR Score (30% weight) - Based on YouTube industry standards
  const ctr = stats.ctr || 0
  let ctrScore = 0
  if (ctr >= 10) ctrScore = 30      // Exceptional (10%+)
  else if (ctr >= 8) ctrScore = 27  // Excellent (8-10%)
  else if (ctr >= 6) ctrScore = 22  // Very Good (6-8%)
  else if (ctr >= 4) ctrScore = 16  // Good (4-6%)
  else if (ctr >= 2) ctrScore = 8   // Below Average (2-4%)
  else ctrScore = 2                 // Poor (<2%)

  // Retention Score (40% weight) - Average View Percentage
  const retention = stats.retention || 0
  let retentionScore = 0
  if (retention >= 70) retentionScore = 40      // Exceptional (70%+)
  else if (retention >= 60) retentionScore = 35 // Excellent (60-70%)
  else if (retention >= 50) retentionScore = 28 // Very Good (50-60%)
  else if (retention >= 40) retentionScore = 20 // Good (40-50%)
  else if (retention >= 30) retentionScore = 10 // Below Average (30-40%)
  else retentionScore = 3                       // Poor (<30%)

  // Engagement Score (20% weight) - Likes + Comments relative to views
  const engagement = stats.engagement || 0
  let engagementScore = 0
  if (engagement >= 8) engagementScore = 20      // Exceptional (8%+)
  else if (engagement >= 6) engagementScore = 17 // Excellent (6-8%)
  else if (engagement >= 4) engagementScore = 14 // Very Good (4-6%)
  else if (engagement >= 2) engagementScore = 10 // Good (2-4%)
  else if (engagement >= 1) engagementScore = 5  // Below Average (1-2%)
  else engagementScore = 1                       // Poor (<1%)

  // Views Performance (10% weight) - Relative to channel average
  const views = stats.views || 0
  const channelAverage = 25000 // This could be calculated from all videos
  let viewsScore = 0
  const viewsRatio = views / channelAverage
  if (viewsRatio >= 2.0) viewsScore = 10      // 200%+ of average
  else if (viewsRatio >= 1.5) viewsScore = 8  // 150-200% of average
  else if (viewsRatio >= 1.0) viewsScore = 6  // 100-150% of average
  else if (viewsRatio >= 0.7) viewsScore = 4  // 70-100% of average
  else if (viewsRatio >= 0.5) viewsScore = 2  // 50-70% of average
  else viewsScore = 1                         // <50% of average

  // Calculate total score
  score = ctrScore + retentionScore + engagementScore + viewsScore

  // Convert to performance level
  if (score >= 85) return 'Excellent'      // 85-100
  else if (score >= 70) return 'Good'      // 70-84
  else if (score >= 50) return 'Average'   // 50-69
  else return 'Poor'                       // <50
}



// Load videos on component mount
onMounted(() => {
  // Start with empty array and loading state
  videos.value = []
  loading.value = true
  fetchVideos()
})

// Cleanup on unmount
onUnmounted(() => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
})
</script>
