<template>
  <div class="min-h-screen bg-forest-900 text-white">
    <!-- Analytics Dashboard -->
    <div class="pt-24 px-6">
      <div class="max-w-7xl mx-auto">
        <!-- Page Header -->
        <div class="mb-4 flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <h1 class="text-2xl font-bold text-white">Analytics Dashboard</h1>
            <span class="text-gray-400">•</span>
            <p class="text-gray-400">Track your YouTube channel performance and growth</p>
          </div>

          <!-- Demo Mode Toggle -->
          <div class="flex items-center space-x-3">
            <span class="text-sm text-gray-400">Demo Mode</span>
            <button
              @click="toggleDemoMode"
              :class="[
                'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                isDemoMode ? 'bg-orange-500' : 'bg-gray-600'
              ]"
            >
              <span
                :class="[
                  'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                  isDemoMode ? 'translate-x-6' : 'translate-x-1'
                ]"
              />
            </button>
          </div>
        </div>

        <!-- Analytics Overview Component -->
        <AnalyticsOverview
          :is-connected="isConnected"
          :has-data="enhancedHasData"
          :is-loading="isLoading"
          :error="error"
          :last-updated="lastUpdated"
          :health-score="enhancedHealthScore"
          :total-views="enhancedTotalViews"
          :subscriber-growth="enhancedSubscriberGrowth"
          :revenue-metrics="enhancedRevenueMetrics"
          :watch-time-minutes="watchTimeMinutes"
          :average-view-duration="averageViewDuration"
          :click-through-rate="clickThroughRate"
          :impressions="impressions"
          :top-videos="enhancedTopVideos"
          :selected-time-range="selectedTimeRange"
          @connect="handleConnect"
          @view-health="handleViewHealth"
          @view-views="handleViewViews"
          @view-subscribers="handleViewSubscribers"
          @view-revenue="handleViewRevenue"
          @view-content="handleViewContent"
          @retry="handleRetry"
        />

        <!-- Additional Analytics Sections -->
        <div v-if="enhancedHasData" class="mt-12 space-y-8">
          <!-- Charts Dashboard -->
          <div class="bg-forest-800 rounded-xl p-6">
            <h2 class="text-xl font-semibold mb-6">Performance Charts</h2>
            <ChartsDashboard
              :analytics-data="analyticsData"
              :loading="isLoading"
              :error="error"
            />
          </div>

          <!-- Channel Goals -->
          <div class="bg-forest-800 rounded-xl p-6">
            <ChannelGoals
              :subscriber-count="enhancedSubscriberGrowth?.current || 0"
              :view-count="enhancedTotalViews"
              :goals="channelGoals"
            />
          </div>
        </div>

        <!-- YouTube Connect Modal -->
        <YouTubeConnectModal
          v-if="showConnectModal"
          @close="showConnectModal = false"
          @connect="handleYouTubeConnect"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import AnalyticsOverview from '../../components/analytics/AnalyticsOverview.vue'
import ChannelGoals from '../../components/analytics/ChannelGoals.vue'
import ChartsDashboard from '../../components/analytics/ChartsDashboard.vue'
import YouTubeConnectModal from '../../components/modals/YouTubeConnectModal.vue'
import { useAnalytics } from '../../composables/useAnalytics'

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// SEO optimization
const { setAnalyticsSEO, setSoftwareApplicationStructuredData } = useSEO()
setAnalyticsSEO()
setSoftwareApplicationStructuredData()

// State
const showConnectModal = ref(false)
const selectedTimeRange = ref(30)
const isDemoMode = ref(false)

// Mock data for demo mode
const mockData = {
  hasData: true,
  healthScore: 85,
  totalViews: 125000,
  subscriberGrowth: {
    current: 2450,
    previous: 2200,
    change: 250,
    percentage: 11.4
  },
  revenueMetrics: {
    total: 1250.50,
    rpm: 2.85,
    cpm: 4.20
  },
  watchTimeMinutes: 45000,
  averageViewDuration: 4.2,
  clickThroughRate: 8.5,
  impressions: 85000,
  topVideos: [
    {
      id: '1',
      title: 'How to Grow Your YouTube Channel in 2024',
      views: 25000,
      thumbnail: '/api/placeholder/120/68',
      duration: '12:45',
      published: '2024-01-15'
    },
    {
      id: '2',
      title: 'YouTube Algorithm Secrets Revealed',
      views: 18500,
      thumbnail: '/api/placeholder/120/68',
      duration: '8:30',
      published: '2024-01-10'
    },
    {
      id: '3',
      title: 'Best Video Editing Tips for Beginners',
      views: 15200,
      thumbnail: '/api/placeholder/120/68',
      duration: '15:20',
      published: '2024-01-05'
    }
  ]
}

// Analytics composable
const {
  loading: isLoading,
  error,
  analyticsData,
  isConnected,
  hasData,
  healthScore,
  totalViews,
  subscriberGrowth,
  revenueMetrics,
  topVideos,
  lastUpdated,
  initialize,
  refresh,
  setTimeRange,
  connectYouTube,
  cleanup
} = useAnalytics()

// Enhanced computed properties that use mock data when demo mode is enabled
const enhancedHasData = computed(() => isDemoMode.value ? mockData.hasData : hasData.value)
const enhancedHealthScore = computed(() => isDemoMode.value ? mockData.healthScore : healthScore.value)
const enhancedTotalViews = computed(() => isDemoMode.value ? mockData.totalViews : totalViews.value)
const enhancedSubscriberGrowth = computed(() => isDemoMode.value ? mockData.subscriberGrowth : subscriberGrowth.value)
const enhancedRevenueMetrics = computed(() => isDemoMode.value ? mockData.revenueMetrics : revenueMetrics.value)
const enhancedTopVideos = computed(() => isDemoMode.value ? mockData.topVideos : topVideos.value)

// Computed properties for additional metrics
const watchTimeMinutes = computed(() => {
  if (isDemoMode.value) return mockData.watchTimeMinutes
  if (!analyticsData.overview?.data) return 0
  return analyticsData.overview.data.watch_time_minutes || 0
})

const averageViewDuration = computed(() => {
  if (isDemoMode.value) return mockData.averageViewDuration
  if (!analyticsData.overview?.data) return 0
  return analyticsData.overview.data.avg_view_duration || 0
})

const clickThroughRate = computed(() => {
  if (isDemoMode.value) return mockData.clickThroughRate
  if (!analyticsData.overview?.data) return 0
  return analyticsData.overview.data.ctr || 0
})

const impressions = computed(() => {
  if (isDemoMode.value) return mockData.impressions
  if (!analyticsData.overview?.data) return 0
  return analyticsData.overview.data.impressions || 0
})

// Channel goals
const channelGoals = computed(() => [
  {
    id: 'subscribers',
    title: 'Subscribers',
    current: enhancedSubscriberGrowth.value?.current || 1200,
    target: isDemoMode.value ? 3000 : 2000,
    percentage: Math.round(((enhancedSubscriberGrowth.value?.current || 1200) / (isDemoMode.value ? 3000 : 2000)) * 100)
  },
  {
    id: 'views',
    title: 'Views',
    current: enhancedTotalViews.value || 7500,
    target: isDemoMode.value ? 150000 : 10000,
    percentage: Math.round(((enhancedTotalViews.value || 7500) / (isDemoMode.value ? 150000 : 10000)) * 100)
  }
])

// Demo mode toggle
const toggleDemoMode = () => {
  isDemoMode.value = !isDemoMode.value
}

// Event handlers
const handleConnect = () => {
  showConnectModal.value = true
}

const handleYouTubeConnect = async () => {
  try {
    await connectYouTube('default_user')
    showConnectModal.value = false
  } catch (error) {
    console.error('YouTube connection failed:', error)
  }
}

const handleViewHealth = () => {
  // Navigate to detailed health view
  console.log('View health details')
}

const handleViewViews = () => {
  // Navigate to views analytics
  console.log('View views details')
}

const handleViewSubscribers = () => {
  // Navigate to subscriber analytics
  console.log('View subscriber details')
}

const handleViewRevenue = () => {
  // Navigate to revenue analytics
  console.log('View revenue details')
}

const handleViewContent = () => {
  // Navigate to content performance
  navigateTo('/videos')
}

const handleRetry = async () => {
  try {
    await refresh(true) // Force refresh
  } catch (error) {
    console.error('Retry failed:', error)
  }
}

// Lifecycle
onMounted(async () => {
  try {
    await initialize('default_user', {
      timeRange: selectedTimeRange.value,
      autoRefresh: true
    })
  } catch (error) {
    console.error('Analytics initialization failed:', error)
  }
})

onUnmounted(() => {
  cleanup()
})

// Watch for time range changes
watch(selectedTimeRange, async (newRange) => {
  try {
    await setTimeRange(newRange)
  } catch (error) {
    console.error('Time range change failed:', error)
  }
})
</script>

<style scoped>
/* Additional styles for the analytics page */
.analytics-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
}

.page-header {
  border-bottom: 1px solid #374151;
  padding-bottom: 2rem;
  margin-bottom: 2rem;
}

.analytics-section {
  background: rgba(31, 41, 55, 0.5);
  backdrop-filter: blur(10px);
  border: 1px solid #374151;
  transition: all 0.3s ease;
}

.analytics-section:hover {
  border-color: #6366f1;
  box-shadow: 0 10px 40px rgba(99, 102, 241, 0.1);
}

/* Responsive design */
@media (max-width: 768px) {
  .analytics-dashboard {
    padding: 1rem;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
}
</style>
