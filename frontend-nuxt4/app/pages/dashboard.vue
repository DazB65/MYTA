<template>
  <div class="dashboard">
    <!-- Left Sidebar Navigation -->
    <div class="sidebar">
      <!-- Logo Section -->
      <div class="logo-section">
        <div class="logo">
          <div class="logo-icon">
            <span>✨</span>
          </div>
          <h1>Vidalytics</h1>
        </div>
        <p class="logo-subtitle">Your AI Agent for Content and Growth</p>
      </div>

      <!-- Main Menu -->
      <div class="menu-section">
        <h3 class="menu-header">Main Menu</h3>
        <nav class="main-nav">
          <!-- Dashboard Link (Active) -->
          <NuxtLink to="/dashboard" class="nav-link active">
            <svg class="nav-icon" fill="currentColor" viewBox="0 0 20 20">
              <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
            </svg>
            Dashboard
          </NuxtLink>

          <NuxtLink to="/pillars" class="nav-link">
            <svg class="nav-icon" fill="currentColor" viewBox="0 0 20 20">
              <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"></path>
            </svg>
            Pillars
          </NuxtLink>

          <NuxtLink to="/videos" class="nav-link">
            <svg class="nav-icon" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"></path>
            </svg>
            Videos
          </NuxtLink>

          <NuxtLink to="/content-studio" class="nav-link">
            <svg class="nav-icon" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
            </svg>
            Content Studio
          </NuxtLink>

          <NuxtLink to="/ai-assistant" class="nav-link">
            <svg class="nav-icon" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            AI Assistant
          </NuxtLink>
        </nav>

        <!-- General Section -->
        <div class="general-section">
          <h3 class="menu-header">General</h3>
          <NuxtLink to="/settings" class="nav-link">
            <svg class="nav-icon" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"></path>
            </svg>
            Settings
          </NuxtLink>
        </div>
      </div>

      <!-- User Profile at Bottom -->
      <div class="user-profile">
        <div class="profile-avatar">
          <span>{{ userInitials }}</span>
        </div>
        <div class="profile-info">
          <p class="greeting">{{ greeting }}</p>
          <p class="username">{{ userName }}!</p>
        </div>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="main-content">
      <!-- Dashboard Modal/Card Overlay -->
      <div class="dashboard-modal">
        <div class="modal-header">
          <div class="header-left">
            <h2>Task Manager</h2>
            <div class="task-stats">
              <span class="completed-tasks">3</span>
              <span class="total-tasks">/ 8 tasks completed</span>
            </div>
          </div>
          <div class="header-right">
            <h2>Channel Goals</h2>
            <button class="add-goal-btn">+ Add Goal</button>
          </div>
        </div>

        <div class="modal-content">
          <!-- Left Side - Task Manager -->
          <div class="task-manager-section">
            <div class="task-categories">
              <div class="category-tab active">All Tasks</div>
              <div class="category-tab">Content</div>
              <div class="category-tab">Analytics</div>
            </div>

            <div class="task-list">
              <div class="task-item completed">
                <input type="checkbox" checked class="task-checkbox">
                <span class="task-text">Create 5 content creative concepts</span>
              </div>
              <div class="task-item">
                <input type="checkbox" class="task-checkbox">
                <span class="task-text">Upload channel banner</span>
              </div>
              <div class="task-item">
                <input type="checkbox" class="task-checkbox">
                <span class="task-text">Post 10 community comments</span>
              </div>
            </div>
          </div>

          <!-- Right Side - Channel Goals -->
          <div class="channel-goals-section">
            <div class="goals-grid">
              <!-- Views Goal -->
              <div class="goal-card views-goal">
                <div class="goal-progress-circle">
                  <svg class="progress-ring" width="80" height="80">
                    <circle cx="40" cy="40" r="35" stroke="#f3f4f6" stroke-width="6" fill="none"/>
                    <circle cx="40" cy="40" r="35" stroke="#ec4899" stroke-width="6" fill="none" 
                            :stroke-dasharray="220" :stroke-dashoffset="66"/>
                  </svg>
                  <div class="progress-text">
                    <span class="percentage">75%</span>
                  </div>
                </div>
                <div class="goal-details">
                  <h4>Views</h4>
                  <p>7.5k / 10k</p>
                </div>
              </div>

              <!-- Subscribers Goal -->
              <div class="goal-card subscribers-goal">
                <div class="goal-progress-circle">
                  <svg class="progress-ring" width="80" height="80">
                    <circle cx="40" cy="40" r="35" stroke="#f3f4f6" stroke-width="6" fill="none"/>
                    <circle cx="40" cy="40" r="35" stroke="#3b82f6" stroke-width="6" fill="none" 
                            :stroke-dasharray="220" :stroke-dashoffset="154"/>
                  </svg>
                  <div class="progress-text">
                    <span class="percentage">30%</span>
                  </div>
                </div>
                <div class="goal-details">
                  <h4>Subscribers</h4>
                  <p>2.8k / 10k</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Bottom Statistics -->
        <div class="quick-statistics">
          <h3>Quick Statistics</h3>
          <div class="stats-grid">
            <div class="stat-card pink">
              <span class="stat-value">75%</span>
              <span class="stat-label">Completion Rate</span>
            </div>
            <div class="stat-card blue">
              <span class="stat-value">2.8k</span>
              <span class="stat-label">Subscribers</span>
            </div>
            <div class="stat-card green">
              <span class="stat-value">10k</span>
              <span class="stat-label">Views</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Performance Monitor (Development/Debug) -->
    <PerformanceMonitor v-if="showPerformanceMonitor" />
  </div>
</template>

<script setup>
import { useAnalytics } from '#imports'
import PerformanceMonitor from '@root/components/performance/PerformanceMonitor.vue'
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'

// Router for navigation
const router = useRouter()

// Analytics composable
const {
  loading,
  error,
  lastUpdated,
  analyticsData,
  isConnected,
  hasData,
  healthScore,
  totalViews,
  subscriberGrowth,
  revenueMetrics,
  topVideos,
  formatNumber,
  formatCurrency,
  initialize,
  refresh,
  setTimeRange,
  cleanup,
  performanceMetrics
} = useAnalytics()

// User data (this would come from authentication/user store)
const userData = ref({
  id: 'demo-user-123', // This would be from auth
  name: 'Marceline Anderson',
  initials: 'MA',
  isOnline: true
})

// Dashboard state
const selectedTimeRange = ref(30)
const showAddGoalModal = ref(false)
const showPerformanceMonitor = ref(process.env.NODE_ENV === 'development')

// Goals data (would be stored in database/user preferences)
const goals = ref({
  views: {
    target: 10000,
    current: 0
  },
  subscribers: {
    target: 1000,
    current: 0
  }
})

// Computed properties for user interface
const userInitials = computed(() => userData.value.initials)
const userName = computed(() => userData.value.name)
const isOnline = computed(() => userData.value.isOnline)
const youtubeConnected = computed(() => analyticsData.status.youtube_connected)

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good Morning'
  if (hour < 17) return 'Good Afternoon'
  return 'Good Evening'
})

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

// Analytics computed properties
const watchTimeMinutes = computed(() => {
  if (!analyticsData.channelHealth?.data) return 0
  return analyticsData.channelHealth.data.watch_time_minutes || 0
})

const averageViewDuration = computed(() => {
  if (!analyticsData.channelHealth?.data) return 0
  return analyticsData.channelHealth.data.average_view_duration || 0
})

const clickThroughRate = computed(() => {
  if (!analyticsData.channelHealth?.data) return 0
  return analyticsData.channelHealth.data.click_through_rate || 0
})

const impressions = computed(() => {
  if (!analyticsData.channelHealth?.data) return 0
  return analyticsData.channelHealth.data.impressions || 0
})

// Change percentages (would be calculated from previous period data)
const healthChange = computed(() => 5.2) // Mock data
const viewsChange = computed(() => 12.8)
const revenueChange = computed(() => -2.1)
const watchTimeChange = computed(() => 8.4)
const avgDurationChange = computed(() => 3.7)
const ctrChange = computed(() => -1.2)
const impressionsChange = computed(() => 15.6)

// Goals computed properties
const currentSubscribers = computed(() => {
  // This would come from analytics data or be tracked separately
  return goals.value.subscribers.current + (subscriberGrowth.value.net || 0)
})

const viewsGoalProgress = computed(() => {
  const progress = (totalViews.value / goals.value.views.target) * 100
  return Math.min(Math.round(progress), 100)
})

const subscribersGoalProgress = computed(() => {
  const progress = (currentSubscribers.value / goals.value.subscribers.target) * 100
  return Math.min(Math.round(progress), 100)
})

const viewsGoalTarget = computed(() => goals.value.views.target)
const subscribersGoalTarget = computed(() => goals.value.subscribers.target)

// Event handlers
const handleYouTubeConnect = () => {
  // Navigate to OAuth connection flow
  router.push('/auth/youtube-connect')
}

const refreshAnalytics = async () => {
  try {
    await refresh()
  } catch (err) {
    console.error('Failed to refresh analytics:', err)
  }
}

const initializeAnalytics = async () => {
  try {
    await initialize(userData.value.id, {
      timeRange: selectedTimeRange.value,
      autoRefresh: true
    })
  } catch (err) {
    console.error('Failed to initialize analytics:', err)
  }
}

const handleTimeRangeChange = async (range) => {
  selectedTimeRange.value = range
  try {
    await setTimeRange(range)
  } catch (err) {
    console.error('Failed to change time range:', err)
  }
}

// Navigation handlers
const navigateToHealth = () => {
  router.push('/analytics/health')
}

const navigateToViews = () => {
  router.push('/analytics/views')
}

const navigateToSubscribers = () => {
  router.push('/analytics/subscribers')
}

const navigateToRevenue = () => {
  router.push('/analytics/revenue')
}

const navigateToVideo = (video) => {
  router.push(`/videos/${video.video_id}`)
}

const navigateToAI = () => {
  router.push('/ai-assistant')
}

const navigateToContentStudio = () => {
  router.push('/content-studio')
}

const navigateToVideos = () => {
  router.push('/videos')
}

// Performance and lazy loading handlers
const onChartsLoaded = ({ cached, loadTime }) => {
  console.log(`Charts dashboard loaded in ${Math.round(loadTime)}ms ${cached ? '(cached)' : '(fresh)'}`)
}

// Modal handlers
const openAddGoalModal = () => {
  // This would open a modal to add custom goals
  console.log('Add goal modal would open here')
}

// Initialize on mount
onMounted(async () => {
  try {
    await initializeAnalytics()
    
    // Update goals current values from analytics
    goals.value.views.current = totalViews.value
    
    // If we have subscriber data, use it
    if (analyticsData.channelHealth?.data?.current_subscribers) {
      goals.value.subscribers.current = analyticsData.channelHealth.data.current_subscribers
    }
  } catch (err) {
    console.error('Dashboard initialization failed:', err)
  }
})

// Cleanup on unmount
onUnmounted(() => {
  cleanup()
})

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

<style scoped>
.dashboard {
  background-color: #f5f5f5;
  min-height: 100vh;
  display: flex;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Sidebar Styles */
.sidebar {
  width: 280px;
  background-color: #2D2D2D;
  height: 100vh;
  display: flex;
  flex-direction: column;
  position: fixed;
  z-index: 100;
}

.logo-section {
  padding: 24px 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.logo-icon {
  width: 28px;
  height: 28px;
  background: linear-gradient(45deg, #FF6B9D, #FF8E8E);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  font-weight: bold;
}

.logo h1 {
  font-size: 18px;
  font-weight: 700;
  color: white;
  margin: 0;
}

.logo-subtitle {
  font-size: 12px;
  color: #888;
  margin: 0;
}

.menu-section {
  padding: 0 16px;
  flex: 1;
}

.menu-header {
  font-size: 12px;
  font-weight: 500;
  color: #666;
  margin: 0 0 16px 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.main-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  color: #999;
  border-radius: 8px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: #ccc;
  background-color: rgba(255, 255, 255, 0.05);
}

.nav-link.active {
  color: white;
  background-color: #FF6B9D;
}

.nav-icon {
  width: 18px;
  height: 18px;
  margin-right: 12px;
}

.general-section {
  margin-top: 32px;
}

.user-profile {
  padding: 20px;
  border-top: 1px solid #444;
  display: flex;
  align-items: center;
  gap: 12px;
}

.profile-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(45deg, #FF6B9D, #FF8E8E);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 16px;
}

.profile-info {
  flex: 1;
}

.greeting {
  color: #ccc;
  font-size: 12px;
  margin: 0;
}

.username {
  color: white;
  font-weight: 600;
  font-size: 14px;
  margin: 2px 0 0 0;
}

/* Main Content Styles */
.main-content {
  flex: 1;
  margin-left: 280px;
  padding: 24px;
  background-color: #f8f9fa;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dashboard-modal {
  background: white;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 1200px;
  min-height: 600px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.header-left h2,
.header-right h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.task-stats {
  display: flex;
  align-items: center;
  gap: 4px;
}

.completed-tasks {
  font-size: 18px;
  font-weight: 700;
  color: #ec4899;
}

.total-tasks {
  font-size: 14px;
  color: #6b7280;
}

.modal-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  margin-bottom: 32px;
}

/* Task Manager Styles */
.task-categories {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.category-tab {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.category-tab.active {
  background: #ec4899;
  color: white;
}

.category-tab:not(.active) {
  background: #f3f4f6;
  color: #6b7280;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.task-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 12px;
  background: #f9fafb;
  transition: all 0.2s;
}

.task-item:hover {
  background: #f3f4f6;
}

.task-item.completed {
  opacity: 0.6;
}

.task-checkbox {
  width: 20px;
  height: 20px;
  accent-color: #ec4899;
}

.task-text {
  font-size: 14px;
  color: #374151;
}

/* Channel Goals Styles */
.goals-grid {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.goal-card {
  display: flex;
  align-items: center;
  gap: 20px;
}

.goal-progress-circle {
  position: relative;
  width: 80px;
  height: 80px;
}

.progress-ring {
  transform: rotate(-90deg);
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.percentage {
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
}

.goal-details h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
}

.goal-details p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

/* Quick Statistics */
.quick-statistics h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 16px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat-card {
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  color: white;
}

.stat-card.pink {
  background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
}

.stat-card.blue {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
}

.stat-card.green {
  background: linear-gradient(135deg, #10b981 0%, #047857 100%);
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  opacity: 0.9;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .secondary-content {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
  }
  
  .main-content {
    margin-left: 0;
    padding: 16px;
  }
  
  .status-indicators {
    position: relative;
    top: auto;
    right: auto;
    margin-bottom: 16px;
  }
  
  .connection-status {
    position: relative;
    bottom: auto;
    right: auto;
    text-align: center;
    margin-top: 16px;
  }
  
  .actions-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 480px) {
  .top-banner {
    padding: 20px;
  }
  
  .banner-content h2 {
    font-size: 20px;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .goals-grid {
    gap: 12px;
  }
  
  .goal-card {
    padding: 16px;
  }
}
</style>
