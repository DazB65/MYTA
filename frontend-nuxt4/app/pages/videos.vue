<template>
  <div class="min-h-screen bg-forest-900 text-white">



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
              type="text"
              placeholder="Search videos..."
              class="w-64 rounded-lg bg-forest-800 px-4 py-2 pl-10 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
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
      <div class="mb-8 rounded-xl bg-forest-800 p-6">
        <div class="mb-6 flex items-center justify-between">
          <h3 class="text-xl font-bold text-white">Recent Videos</h3>
          <div class="flex items-center space-x-4">
            <!-- Sort by Pillar -->
            <select v-model="selectedPillar" class="rounded-lg bg-forest-700 px-3 py-2 text-sm text-white">
              <option value="all">All Pillars</option>
              <option value="Gaming Reviews">Gaming Reviews</option>
              <option value="Tech Tutorials">Tech Tutorials</option>
              <option value="Product Reviews">Product Reviews</option>
              <option value="Industry News">Industry News</option>
            </select>

            <!-- Sort by Performance -->
            <select v-model="sortBy" class="rounded-lg bg-forest-700 px-3 py-2 text-sm text-white">
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

        <!-- Video Grid -->
        <div class="grid grid-cols-6 gap-4">
          <div v-for="video in filteredAndSortedVideos" :key="video.id" class="group cursor-pointer" @click="openVideoStats(video)">
            <div class="relative mb-3 aspect-video overflow-hidden rounded-lg bg-forest-700">
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
            <h4 class="mb-1 line-clamp-2 text-sm font-medium text-white">{{ video.title }}</h4>
            <p class="text-xs text-gray-400">{{ formatNumber(video.detailedStats?.views || 0) }} views • {{ formatDate(video.date) }}</p>
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
import { computed, ref } from 'vue'

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

// Sample video data with detailed stats
const videos = ref([
  {
    id: 1,
    title: "10 YouTube Growth Hacks That Actually Work in 2024",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "12:34",
    date: "2024-01-15",
    pillar: "Growth Strategies",
    category: "Tutorial",
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
    pillar: "Personal Stories",
    category: "Vlog",
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
    pillar: "Content Creation",
    category: "Education",
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
    pillar: "Behind the Scenes",
    category: "Behind the Scenes",
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
    pillar: "Gaming Reviews",
    category: "Review",
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
    pillar: "Tech Tutorials",
    category: "Review",
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
  }
])

// Computed property for filtered and sorted videos
const filteredAndSortedVideos = computed(() => {
  let filtered = videos.value

  // Filter by pillar
  if (selectedPillar.value !== 'all') {
    filtered = filtered.filter(video => video.pillar === selectedPillar.value)
  }

  // Sort videos
  return filtered.sort((a, b) => {
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
</script>
