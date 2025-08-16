<template>
  <div class="min-h-screen bg-gray-900 text-white">
    <!-- Analytics Dashboard -->
    <div class="pt-32 px-6">
      <div class="max-w-7xl mx-auto">
        <!-- Page Header -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-white mb-2">Analytics Dashboard</h1>
          <p class="text-gray-400">Track your YouTube channel performance and growth</p>
        </div>

        <!-- Analytics Overview Component -->
        <AnalyticsOverview
          :is-connected="isConnected"
          :has-data="hasData"
          :is-loading="isLoading"
          :error="error"
          :last-updated="lastUpdated"
          :health-score="healthScore"
          :total-views="totalViews"
          :subscriber-growth="subscriberGrowth"
          :revenue-metrics="revenueMetrics"
          :watch-time-minutes="watchTimeMinutes"
          :average-view-duration="averageViewDuration"
          :click-through-rate="clickThroughRate"
          :impressions="impressions"
          :top-videos="topVideos"
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
        <div v-if="hasData" class="mt-12 space-y-8">
          <!-- Charts Dashboard -->
          <div class="bg-gray-800 rounded-xl p-6">
            <h2 class="text-xl font-semibold mb-6">Performance Charts</h2>
            <ChartsDashboard
              :analytics-data="analyticsData"
              :loading="isLoading"
              :error="error"
            />
          </div>

          <!-- Channel Goals -->
          <div class="bg-gray-800 rounded-xl p-6">
            <ChannelGoals
              :subscriber-count="subscriberGrowth.current || 0"
              :view-count="totalViews"
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

// Computed properties for additional metrics
const watchTimeMinutes = computed(() => {
  if (!analyticsData.overview?.data) return 0
  return analyticsData.overview.data.watch_time_minutes || 0
})

const averageViewDuration = computed(() => {
  if (!analyticsData.overview?.data) return 0
  return analyticsData.overview.data.avg_view_duration || 0
})

const clickThroughRate = computed(() => {
  if (!analyticsData.overview?.data) return 0
  return analyticsData.overview.data.ctr || 0
})

const impressions = computed(() => {
  if (!analyticsData.overview?.data) return 0
  return analyticsData.overview.data.impressions || 0
})

// Channel goals (mock data for now)
const channelGoals = computed(() => [
  {
    id: 'subscribers',
    title: 'Subscribers',
    current: subscriberGrowth.value.current || 1200,
    target: 2000,
    percentage: Math.round(((subscriberGrowth.value.current || 1200) / 2000) * 100)
  },
  {
    id: 'views',
    title: 'Views',
    current: totalViews.value || 7500,
    target: 10000,
    percentage: Math.round(((totalViews.value || 7500) / 10000) * 100)
  }
])

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
