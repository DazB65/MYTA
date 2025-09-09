<template>
  <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border border-gray-700/50 p-6 mb-6">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-semibold text-white">Recent Video Performance</h2>
      <div class="flex items-center space-x-3">
        <NuxtLink
          to="/videos"
          class="rounded-lg bg-gray-600 px-4 py-2 text-sm font-medium text-white hover:bg-gray-500 transition-colors"
        >
          View All Videos
        </NuxtLink>
        <button
          @click="refreshData"
          class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 transition-colors"
          :disabled="loading"
        >
          {{ loading ? 'Refreshing...' : 'Refresh' }}
        </button>
      </div>
    </div>

    <!-- Video Performance Cards -->
    <div class="space-y-4">
      <div
        v-for="video in recentVideos"
        :key="video.id"
        :class="getVideoCardClasses(calculatePerformance(video))"
        @click="analyzeVideo(video)"
      >
        <!-- Video Info -->
        <div class="flex items-center space-x-4 flex-1">
          <!-- Thumbnail -->
          <div class="relative">
            <img
              :src="video.thumbnail"
              :alt="video.title"
              class="w-20 h-12 rounded object-cover"
            />
            <div class="absolute bottom-1 right-1 bg-black bg-opacity-75 text-white text-xs px-1 rounded">
              {{ video.duration }}
            </div>
          </div>

          <!-- Video Details -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center space-x-2">
              <span class="text-purple-300">🎬</span>
              <h4 class="font-medium text-white truncate">
                {{ video.title }}
              </h4>
            </div>
            <p class="text-sm text-gray-400 mt-1">
              Published {{ formatDate(video.publishedAt) }}
            </p>
            <div class="flex items-center space-x-2 mt-2">
              <span class="text-xs text-gray-300 bg-gray-600 px-2 py-1 rounded">
                {{ video.category }}
              </span>
              <span
                class="text-xs px-2 py-1 rounded"
                :class="getPillarClass(video.pillar)"
              >
                📌 {{ video.pillar }}
              </span>
              <span
                class="text-xs px-2 py-1 rounded"
                :class="getPerformanceClass(calculatePerformance(video))"
              >
                {{ calculatePerformance(video) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Metrics -->
        <div class="flex items-center space-x-6 text-sm">
          <!-- Views -->
          <div class="text-center">
            <div class="text-white font-semibold">{{ formatNumber(video.views) }}</div>
            <div class="text-gray-400 text-xs">Views</div>
            <div class="flex items-center justify-center mt-1">
              <span 
                class="text-xs flex items-center"
                :class="video.viewsTrend > 0 ? 'text-green-400' : video.viewsTrend < 0 ? 'text-red-400' : 'text-gray-400'"
              >
                <svg v-if="video.viewsTrend > 0" class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L10 4.414 6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                </svg>
                <svg v-else-if="video.viewsTrend < 0" class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L10 15.586l3.293-3.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                {{ Math.abs(video.viewsTrend) }}%
              </span>
            </div>
          </div>

          <!-- CTR -->
          <div class="text-center">
            <div class="text-white font-semibold">{{ video.ctr }}%</div>
            <div class="text-gray-400 text-xs">CTR</div>
            <div class="flex items-center justify-center mt-1">
              <span 
                class="text-xs flex items-center"
                :class="video.ctrTrend > 0 ? 'text-green-400' : video.ctrTrend < 0 ? 'text-red-400' : 'text-gray-400'"
              >
                <svg v-if="video.ctrTrend > 0" class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L10 4.414 6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                </svg>
                <svg v-else-if="video.ctrTrend < 0" class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L10 15.586l3.293-3.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                {{ Math.abs(video.ctrTrend) }}%
              </span>
            </div>
          </div>

          <!-- Engagement -->
          <div class="text-center">
            <div class="text-white font-semibold">{{ video.engagement }}%</div>
            <div class="text-gray-400 text-xs">Engagement</div>
            <div class="flex items-center justify-center mt-1">
              <span 
                class="text-xs flex items-center"
                :class="video.engagementTrend > 0 ? 'text-green-400' : video.engagementTrend < 0 ? 'text-red-400' : 'text-gray-400'"
              >
                <svg v-if="video.engagementTrend > 0" class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L10 4.414 6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                </svg>
                <svg v-else-if="video.engagementTrend < 0" class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L10 15.586l3.293-3.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                {{ Math.abs(video.engagementTrend) }}%
              </span>
            </div>
          </div>

          <!-- Action Button -->
          <button
            @click.stop="analyzeVideo(video)"
            class="rounded-lg bg-orange-600 px-3 py-2 text-sm font-medium text-white hover:bg-orange-700 transition-colors"
          >
            Analyze
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="recentVideos.length === 0" class="text-center py-12">
      <div class="text-gray-400 mb-4">
        <svg class="w-16 h-16 mx-auto" fill="currentColor" viewBox="0 0 20 20">
          <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"/>
        </svg>
      </div>
      <h3 class="text-lg font-medium text-white mb-2">No Recent Videos</h3>
      <p class="text-gray-400 mb-4">Upload your first video to see performance insights here.</p>
      <button
        @click="connectYouTube"
        class="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 transition-colors"
      >
        Connect YouTube Channel
      </button>
    </div>

    <!-- Video Stats Modal -->
    <Teleport to="body">
      <VideoStatsModal
        :show="showStatsModal"
        :video="selectedVideo"
        @close="closeStatsModal"
      />
    </Teleport>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

// Reactive data
const loading = ref(false)
const showStatsModal = ref(false)
const selectedVideo = ref(null)
const recentVideos = ref([
  {
    id: 1,
    title: "10 YouTube Growth Hacks That Actually Work in 2024",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "12:34",
    publishedAt: "2024-01-15T10:00:00Z",
    category: "Tutorial",
    pillar: "Growth Strategies",
    performance: "Excellent",
    views: 45200,
    viewsTrend: 12.5,
    ctr: 8.2,
    ctrTrend: 2.1,
    engagement: 6.8,
    engagementTrend: -1.2
  },
  {
    id: 2,
    title: "My Biggest YouTube Mistakes (And How to Avoid Them)",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "15:22",
    publishedAt: "2024-01-12T14:30:00Z",
    category: "Vlog",
    pillar: "Personal Stories",
    performance: "Good",
    views: 28900,
    viewsTrend: 8.3,
    ctr: 6.5,
    ctrTrend: 1.8,
    engagement: 5.2,
    engagementTrend: 3.4
  },
  {
    id: 3,
    title: "Creating Viral Content: The Complete Guide",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "18:45",
    publishedAt: "2024-01-10T09:15:00Z",
    category: "Education",
    pillar: "Content Creation",
    performance: "Average",
    views: 15600,
    viewsTrend: -5.2,
    ctr: 4.8,
    ctrTrend: -2.1,
    engagement: 4.1,
    engagementTrend: 0.8
  },
  {
    id: 4,
    title: "Behind the Scenes: My Content Creation Process",
    thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
    duration: "22:10",
    publishedAt: "2024-01-08T16:45:00Z",
    category: "Behind the Scenes",
    pillar: "Behind the Scenes",
    performance: "Poor",
    views: 8200,
    viewsTrend: -12.8,
    ctr: 3.2,
    ctrTrend: -4.5,
    engagement: 2.9,
    engagementTrend: -2.1
  }
])

// Calculate performance level based on video metrics
const calculatePerformance = (video) => {
  // Create detailedStats from available data if not present
  const stats = video.detailedStats || {
    views: video.views,
    ctr: video.ctr,
    engagement: video.engagement,
    retention: video.retention || (video.engagement * 10) // Estimate retention from engagement
  }

  if (!stats.views) return 'Unknown'

  let score = 0

  // CTR Score (30% weight)
  const ctr = stats.ctr || 0
  let ctrScore = 0
  if (ctr >= 10) ctrScore = 30
  else if (ctr >= 8) ctrScore = 27
  else if (ctr >= 6) ctrScore = 22
  else if (ctr >= 4) ctrScore = 16
  else if (ctr >= 2) ctrScore = 8
  else ctrScore = 2

  // Retention Score (40% weight)
  const retention = stats.retention || 0
  let retentionScore = 0
  if (retention >= 70) retentionScore = 40
  else if (retention >= 60) retentionScore = 35
  else if (retention >= 50) retentionScore = 28
  else if (retention >= 40) retentionScore = 20
  else if (retention >= 30) retentionScore = 10
  else retentionScore = 3

  // Engagement Score (20% weight)
  const engagement = stats.engagement || 0
  let engagementScore = 0
  if (engagement >= 8) engagementScore = 20
  else if (engagement >= 6) engagementScore = 17
  else if (engagement >= 4) engagementScore = 14
  else if (engagement >= 2) engagementScore = 10
  else if (engagement >= 1) engagementScore = 5
  else engagementScore = 1

  // Views Performance (10% weight)
  const views = stats.views || 0
  const channelAverage = 25000
  let viewsScore = 0
  const viewsRatio = views / channelAverage
  if (viewsRatio >= 2.0) viewsScore = 10
  else if (viewsRatio >= 1.5) viewsScore = 8
  else if (viewsRatio >= 1.0) viewsScore = 6
  else if (viewsRatio >= 0.7) viewsScore = 4
  else if (viewsRatio >= 0.5) viewsScore = 2
  else viewsScore = 1

  // Calculate total score
  score = ctrScore + retentionScore + engagementScore + viewsScore

  // Convert to performance level
  if (score >= 85) return 'Excellent'
  else if (score >= 70) return 'Good'
  else if (score >= 50) return 'Average'
  else return 'Poor'
}

// Get video card classes based on performance for enhanced borders
const getVideoCardClasses = (performance) => {
  const baseClasses = "flex items-center justify-between rounded-lg p-4 transition-all duration-300 hover:scale-[1.01] hover:shadow-lg cursor-pointer"

  switch (performance?.toLowerCase()) {
    case 'excellent':
      return `${baseClasses} bg-gray-900/70 backdrop-blur-sm border-2 border-green-600/60 shadow-green-600/20 shadow-sm`
    case 'good':
      return `${baseClasses} bg-gray-900/70 backdrop-blur-sm border-2 border-blue-600/60 shadow-blue-600/20 shadow-sm`
    case 'average':
      return `${baseClasses} bg-gray-900/70 backdrop-blur-sm border-2 border-yellow-600/60 shadow-yellow-600/20 shadow-sm`
    case 'poor':
      return `${baseClasses} bg-gray-900/70 backdrop-blur-sm border-2 border-red-600/60 shadow-red-600/20 shadow-sm`
    default:
      return `${baseClasses} bg-gray-700 border border-gray-600/50`
  }
}

// Methods
const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

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

const getPerformanceClass = (performance) => {
  switch (performance.toLowerCase()) {
    case 'excellent':
      return 'bg-green-600 text-white'
    case 'good':
      return 'bg-blue-600 text-white'
    case 'average':
      return 'bg-yellow-600 text-white'
    case 'poor':
      return 'bg-red-600 text-white'
    default:
      return 'bg-gray-600 text-white'
  }
}

const getPillarClass = (pillar) => {
  // Different colors for different pillars to make them visually distinct
  const pillarColors = {
    'Growth Strategies': 'bg-orange-600 text-white',
    'Personal Stories': 'bg-purple-600 text-white',
    'Content Creation': 'bg-blue-600 text-white',
    'Behind the Scenes': 'bg-pink-600 text-white',
    'Tutorials': 'bg-green-600 text-white',
    'Reviews': 'bg-indigo-600 text-white',
    'Entertainment': 'bg-red-600 text-white',
    'Educational': 'bg-teal-600 text-white'
  }

  return pillarColors[pillar] || 'bg-gray-600 text-white'
}

const refreshData = async () => {
  loading.value = true
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1000))
  loading.value = false
  // In real app, would fetch fresh data from YouTube API
}

const analyzeVideo = (video) => {
  // Open the video stats modal
  selectedVideo.value = video
  showStatsModal.value = true
}

const closeStatsModal = () => {
  showStatsModal.value = false
  selectedVideo.value = null
}

const connectYouTube = () => {
  // Open YouTube connection modal
  console.log('Opening YouTube connection modal')
}

// Lifecycle
onMounted(() => {
  // Load recent videos data
})
</script>
