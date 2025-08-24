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
            <p class="text-xs text-gray-400">{{ video.views }} views • {{ video.date }}</p>
          </div>
        </div>
      </div>


    </div>

    <!-- Video Stats Modal -->
    <div v-if="showStatsModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50" @click="closeStatsModal">
      <div class="w-full max-w-4xl mx-4 bg-forest-800 rounded-xl p-6" @click.stop>
        <!-- Modal Header -->
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center space-x-4">
            <img :src="selectedVideo?.thumbnail" :alt="selectedVideo?.title" class="w-16 h-10 object-cover rounded-lg">
            <div>
              <h3 class="text-xl font-bold text-white">{{ selectedVideo?.title }}</h3>
              <p class="text-sm text-gray-400">Published {{ selectedVideo?.date }}</p>
            </div>
          </div>
          <button @click="closeStatsModal" class="text-gray-400 hover:text-white">
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div class="bg-forest-700 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-blue-400">{{ formatNumber(selectedVideo?.detailedStats?.views || 0) }}</div>
            <div class="text-sm text-gray-400">Total Views</div>
            <div class="text-xs text-green-400 mt-1">+{{ selectedVideo?.detailedStats?.viewsGrowth || 0 }}%</div>
          </div>
          <div class="bg-forest-700 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-green-400">{{ selectedVideo?.detailedStats?.likes || 0 }}</div>
            <div class="text-sm text-gray-400">Likes</div>
            <div class="text-xs text-green-400 mt-1">{{ selectedVideo?.detailedStats?.likeRatio || 0 }}% ratio</div>
          </div>
          <div class="bg-forest-700 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-yellow-400">{{ selectedVideo?.detailedStats?.comments || 0 }}</div>
            <div class="text-sm text-gray-400">Comments</div>
            <div class="text-xs text-blue-400 mt-1">{{ selectedVideo?.detailedStats?.engagement || 0 }}% engagement</div>
          </div>
          <div class="bg-forest-700 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-purple-400">{{ selectedVideo?.detailedStats?.watchTime || '0:00' }}</div>
            <div class="text-sm text-gray-400">Avg Watch Time</div>
            <div class="text-xs text-purple-400 mt-1">{{ selectedVideo?.detailedStats?.retention || 0 }}% retention</div>
          </div>
        </div>

        <!-- Performance Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Traffic Sources -->
          <div class="bg-forest-700 rounded-lg p-4">
            <h4 class="text-lg font-semibold text-white mb-4">Traffic Sources</h4>
            <div class="space-y-3">
              <div v-for="source in selectedVideo?.detailedStats?.trafficSources || []" :key="source.name" class="flex items-center justify-between">
                <span class="text-gray-300">{{ source.name }}</span>
                <div class="flex items-center space-x-2">
                  <div class="w-20 bg-forest-600 rounded-full h-2">
                    <div class="bg-orange-500 h-2 rounded-full" :style="{ width: source.percentage + '%' }"></div>
                  </div>
                  <span class="text-sm text-gray-400">{{ source.percentage }}%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Audience Demographics -->
          <div class="bg-forest-700 rounded-lg p-4">
            <h4 class="text-lg font-semibold text-white mb-4">Top Countries</h4>
            <div class="space-y-3">
              <div v-for="country in selectedVideo?.detailedStats?.topCountries || []" :key="country.name" class="flex items-center justify-between">
                <span class="text-gray-300">{{ country.name }}</span>
                <div class="flex items-center space-x-2">
                  <div class="w-20 bg-forest-600 rounded-full h-2">
                    <div class="bg-blue-500 h-2 rounded-full" :style="{ width: country.percentage + '%' }"></div>
                  </div>
                  <span class="text-sm text-gray-400">{{ country.percentage }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center justify-end space-x-3 mt-6 pt-4 border-t border-forest-600">
          <a
            :href="selectedVideo?.youtubeUrl || '#'"
            target="_blank"
            rel="noopener noreferrer"
            class="px-4 py-2 bg-forest-700 text-gray-300 rounded-lg hover:bg-forest-600 transition-colors inline-flex items-center space-x-2"
          >
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
            </svg>
            <span>View on YouTube</span>
          </a>
          <button class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
            Update SEO & Tags
          </button>
          <button class="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors">
            Create Follow-up Content
          </button>
        </div>
      </div>
    </div>
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

// Sample data for videos
const recentVideos = ref([
  {
    id: 1,
    title: 'How to Create Engaging Content That Converts',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '12:34',
    views: '45.2K',
    viewsNumeric: 45200,
    engagementRate: 4.8,
    date: '2 days ago',
    pillar: 'Tech Tutorials',
    youtubeUrl: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    detailedStats: {
      views: 45234,
      viewsGrowth: 12,
      likes: 1847,
      likeRatio: 96.2,
      comments: 234,
      engagement: 4.8,
      watchTime: '8:42',
      retention: 69.3,
      trafficSources: [
        { name: 'YouTube Search', percentage: 42 },
        { name: 'Suggested Videos', percentage: 28 },
        { name: 'Browse Features', percentage: 18 },
        { name: 'External', percentage: 12 }
      ],
      topCountries: [
        { name: 'United States', percentage: 35 },
        { name: 'United Kingdom', percentage: 18 },
        { name: 'Canada', percentage: 12 },
        { name: 'Australia', percentage: 8 }
      ]
    }
  },
  {
    id: 2,
    title: 'Advanced YouTube Analytics Strategies',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '8:45',
    views: '32.1K',
    viewsNumeric: 32100,
    engagementRate: 5.2,
    date: '5 days ago',
    pillar: 'Tech Tutorials',
    youtubeUrl: 'https://www.youtube.com/watch?v=jNQXAC9IVRw',
  },
  {
    id: 3,
    title: 'Building Your Personal Brand Online',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '15:22',
    views: '28.7K',
    viewsNumeric: 28700,
    engagementRate: 3.9,
    date: '1 week ago',
    pillar: 'Industry News',
  },
  {
    id: 4,
    title: 'Content Creation Tools & Tips',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '10:18',
    views: '19.3K',
    viewsNumeric: 19300,
    engagementRate: 6.1,
    date: '1 week ago',
    pillar: 'Product Reviews',
  },
  {
    id: 5,
    title: 'Social Media Marketing Masterclass',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '22:15',
    views: '67.8K',
    viewsNumeric: 67800,
    engagementRate: 4.1,
    date: '2 weeks ago',
    pillar: 'Tech Tutorials',
  },
  {
    id: 6,
    title: 'Video SEO Best Practices',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '9:33',
    views: '15.4K',
    date: '2 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=oHg5SJYRHA0',
  },
  {
    id: 7,
    title: 'Monetization Strategies That Actually Work',
    thumbnail: 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=300&h=200&fit=crop',
    duration: '18:42',
    views: '52.3K',
    date: '3 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=kJQP7kiw5Fk',
  },
  {
    id: 8,
    title: 'Thumbnail Design Psychology',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '11:27',
    views: '38.9K',
    date: '3 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=lXMskKTw3Bc',
  },
  {
    id: 9,
    title: 'Live Streaming Setup Guide',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '14:55',
    views: '29.7K',
    date: '1 month ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=fJ9rUzIMcZQ',
  },
  {
    id: 10,
    title: 'YouTube Shorts Strategy 2024',
    thumbnail: 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=300&h=200&fit=crop',
    duration: '7:18',
    views: '73.1K',
    viewsNumeric: 73100,
    engagementRate: 7.8,
    date: '1 month ago',
    pillar: 'Gaming Reviews',
    youtubeUrl: 'https://www.youtube.com/watch?v=QH2-TGUlwu4',
  },
  {
    id: 11,
    title: 'Community Building on YouTube',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '16:33',
    views: '41.8K',
    date: '1 month ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=nfWlot6h_JM',
  },
  {
    id: 12,
    title: 'Analytics Deep Dive: What Really Matters',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '20:14',
    views: '35.6K',
    date: '5 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=4fAGfKKoDg8',
  },
  {
    id: 13,
    title: 'Collaboration Strategies for Growth',
    thumbnail: 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=300&h=200&fit=crop',
    duration: '13:09',
    views: '27.4K',
    date: '5 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=ZXsQAXx_ao0',
  },
  {
    id: 14,
    title: 'Equipment Setup on a Budget',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '12:51',
    views: '44.2K',
    date: '6 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=Sagg08DrO5U',
  },
  {
    id: 15,
    title: 'Content Calendar Planning',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '9:47',
    views: '31.5K',
    date: '6 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=5qap5aO4i9A',
  },
  {
    id: 16,
    title: 'Audience Retention Secrets',
    thumbnail: 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=300&h=200&fit=crop',
    duration: '15:23',
    views: '48.7K',
    date: '7 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=BaW_jenozKc',
  },
  {
    id: 17,
    title: 'Brand Partnerships & Sponsorships',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '17:41',
    views: '39.2K',
    date: '7 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=y8Kyi0WNg40',
  },
  {
    id: 18,
    title: 'YouTube Studio Hidden Features',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '11:58',
    views: '33.8K',
    date: '8 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=ktvTqknDobU',
  },
])

// Add default pillar and engagement data to videos without it
recentVideos.value.forEach(video => {
  if (!video.pillar) {
    // Assign pillars based on video content
    if (video.title.includes('Gaming') || video.title.includes('Shorts')) {
      video.pillar = 'Gaming Reviews'
    } else if (video.title.includes('Analytics') || video.title.includes('SEO') || video.title.includes('Tutorial') || video.title.includes('YouTube')) {
      video.pillar = 'Tech Tutorials'
    } else if (video.title.includes('Equipment') || video.title.includes('Tools') || video.title.includes('Review')) {
      video.pillar = 'Product Reviews'
    } else {
      video.pillar = 'Industry News'
    }
  }

  if (!video.viewsNumeric) {
    // Convert views string to numeric
    const viewsStr = video.views.replace('K', '').replace('M', '')
    video.viewsNumeric = video.views.includes('K') ? parseFloat(viewsStr) * 1000 : parseFloat(viewsStr) * 1000000
  }

  if (!video.engagementRate) {
    // Generate realistic engagement rates
    video.engagementRate = Math.random() * 4 + 3 // 3-7% range
  }
})

// Computed property for filtered and sorted videos
const filteredAndSortedVideos = computed(() => {
  let filtered = recentVideos.value

  // Filter by pillar
  if (selectedPillar.value !== 'all') {
    filtered = filtered.filter(video => video.pillar === selectedPillar.value)
  }

  // Sort by selected criteria
  switch (sortBy.value) {
    case 'views':
      return filtered.sort((a, b) => b.viewsNumeric - a.viewsNumeric)
    case 'engagement':
      return filtered.sort((a, b) => b.engagementRate - a.engagementRate)
    case 'duration':
      return filtered.sort((a, b) => {
        const aDuration = a.duration.split(':').reduce((acc, time) => (60 * acc) + +time, 0)
        const bDuration = b.duration.split(':').reduce((acc, time) => (60 * acc) + +time, 0)
        return bDuration - aDuration
      })
    case 'recent':
    default:
      return filtered.sort((a, b) => a.id - b.id) // Keep original order for recent
  }
})

// Sync with YouTube functionality
const syncWithYouTube = async () => {
  if (syncing.value) return

  syncing.value = true

  try {
    // Simulate API call to sync with YouTube
    console.log('🔄 Syncing with YouTube...')

    // In a real app, this would:
    // 1. Call YouTube API to get latest videos
    // 2. Update video analytics data
    // 3. Refresh the videos list
    // 4. Update performance metrics

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 2000))

    // Update last sync time
    lastSyncTime.value = new Date().toLocaleString()

    // Show success message
    console.log('✅ Successfully synced with YouTube!')

    // In a real app, you might want to show a toast notification
    alert('Successfully synced with YouTube! Video data has been updated.')

  } catch (error) {
    console.error('❌ Failed to sync with YouTube:', error)
    alert('Failed to sync with YouTube. Please try again.')
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
</script>
