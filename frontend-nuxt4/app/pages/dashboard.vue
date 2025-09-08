<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <!-- Header -->
    <div class="pt-24">
      <!-- Page Header -->
      <div class="mb-4 px-4">
        <h1 class="text-2xl font-bold text-white">Dashboard</h1>
        <p class="text-gray-400">Welcome back! Here's your channel overview.</p>
      </div>

      <!-- Channel Statistics -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 px-4">
        <!-- Subscribers -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-red-700 to-red-800 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('subscribers')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-base text-red-100 font-medium">Subscribers</p>
              <!-- Change Indicator -->
              <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-100">
                <span>↗</span>
                <span>12%</span>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">1.2K</div>
              <div class="text-sm text-white/70">Total subscribers</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">{{ getGoalText('subscribers') }}</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" :style="{ width: getProgressWidth('subscribers') }"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        <!-- Views -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-blue-700 to-blue-800 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('views')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-base text-blue-100 font-medium">Views</p>
              <!-- Change Indicator -->
              <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-100">
                <span>↗</span>
                <span>8%</span>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">45.6K</div>
              <div class="text-sm text-white/70">Total views</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">{{ getGoalText('views') }}</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" :style="{ width: getProgressWidth('views') }"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        <!-- Watch Time -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-purple-700 to-purple-800 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('watchTime')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-base text-purple-100 font-medium">Watch Time</p>
              <!-- Change Indicator -->
              <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-100">
                <span>↗</span>
                <span>15%</span>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">2.1K hrs</div>
              <div class="text-sm text-white/70">Total watch time</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">{{ getGoalText('watchTime') }}</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" :style="{ width: getProgressWidth('watchTime') }"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        <!-- Revenue -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-green-700 to-green-800 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('revenue')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-base text-green-100 font-medium">Revenue</p>
              <!-- Change Indicator -->
              <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-100">
                <span>↗</span>
                <span>22%</span>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">$1,234</div>
              <div class="text-sm text-white/70">Total revenue</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">{{ getGoalText('revenue') }}</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" :style="{ width: getProgressWidth('revenue') }"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        <!-- Engagement Rate -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-yellow-700 to-yellow-800 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('engagement')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-base text-yellow-100 font-medium">Engagement</p>
              <!-- Change Indicator -->
              <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-100">
                <span>↗</span>
                <span>0.3%</span>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">4.2%</div>
              <div class="text-sm text-white/70">Engagement rate</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">{{ getGoalText('engagement') }}</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" :style="{ width: getProgressWidth('engagement') }"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        <!-- Click-Through Rate -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-orange-700 to-orange-800 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('ctr')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-base text-orange-100 font-medium">CTR</p>
              <!-- Change Indicator -->
              <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-red-500/20 text-red-100">
                <span>↘</span>
                <span>0.2%</span>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">3.8%</div>
              <div class="text-sm text-white/70">Click-through rate</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">{{ getGoalText('ctr') }}</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" :style="{ width: getProgressWidth('ctr') }"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        <!-- Average View Duration -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-indigo-700 to-indigo-800 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('avgDuration')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-base text-indigo-100 font-medium">Avg Duration</p>
              <!-- Change Indicator -->
              <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-100">
                <span>↗</span>
                <span>15s</span>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">2:45</div>
              <div class="text-sm text-white/70">Average view duration</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">{{ getGoalText('avgDuration') }}</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" :style="{ width: getProgressWidth('avgDuration') }"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        <!-- Retention Rate -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-pink-700 to-pink-800 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('retention')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-base text-pink-100 font-medium">Retention</p>
              <!-- Change Indicator -->
              <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-100">
                <span>↗</span>
                <span>5%</span>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">68%</div>
              <div class="text-sm text-white/70">Retention rate</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">{{ getGoalText('retention') }}</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" :style="{ width: getProgressWidth('retention') }"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
      </div>



      <!-- Main Dashboard Content -->
      <div class="mb-6 px-4">
        <!-- Recent Video Performance - Full Width -->
        <RecentVideoPerformance />

        <!-- Usage Tracking Panel -->
        <div class="mt-6">
          <UsageTrackingPanel />
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
// Import team collaboration components

// Import VidIQ-inspired components

// Import usage tracking component
// UsageTrackingPanel will be auto-imported by Nuxt

// Page metadata
definePageMeta({
  title: 'Dashboard - MYTA',
  description: 'Your YouTube channel dashboard'
})

// Use the modal composable
const { openGoalSetting } = useModals()

// Metric data mapping
const metricData = {
  subscribers: {
    id: 'subscribers',
    label: 'Subscribers',
    currentValue: 1200,
    currentGoal: 2000,
    unit: 'subscribers',
    min: 0,
    step: 100
  },
  views: {
    id: 'views',
    label: 'Views',
    currentValue: 45600,
    currentGoal: 100000,
    unit: 'views',
    min: 0,
    step: 1000
  },
  watchTime: {
    id: 'watchTime',
    label: 'Watch Time',
    currentValue: 2100,
    currentGoal: 5000,
    unit: 'hours',
    min: 0,
    step: 100
  },
  revenue: {
    id: 'revenue',
    label: 'Revenue',
    currentValue: 1234,
    currentGoal: 3000,
    unit: 'dollars',
    min: 0,
    step: 50
  },
  engagement: {
    id: 'engagement',
    label: 'Engagement',
    currentValue: 4.2,
    currentGoal: 6.0,
    unit: '%',
    min: 0,
    step: 0.1
  },
  ctr: {
    id: 'ctr',
    label: 'CTR',
    currentValue: 3.8,
    currentGoal: 5.0,
    unit: '%',
    min: 0,
    step: 0.1
  },
  avgDuration: {
    id: 'avgDuration',
    label: 'Avg Duration',
    currentValue: 165,
    currentGoal: 240,
    unit: 'seconds',
    min: 0,
    step: 15
  },
  retention: {
    id: 'retention',
    label: 'Retention',
    currentValue: 68,
    currentGoal: 80,
    unit: '%',
    min: 0,
    step: 1
  }
}

// Default metric goals
const defaultGoals = {
  subscribers: 2000,
  views: 100000,
  watchTime: 5000,
  revenue: 3000,
  engagement: 6.0,
  ctr: 5.0,
  avgDuration: 240,
  retention: 80
}

// Load goals from localStorage or use defaults
const loadGoalsFromStorage = () => {
  if (typeof window !== 'undefined') {
    try {
      const saved = localStorage.getItem('myta-metric-goals')
      if (saved) {
        const parsed = JSON.parse(saved)
        // Merge with defaults to ensure all keys exist
        return { ...defaultGoals, ...parsed }
      }
    } catch (error) {
      console.warn('Failed to load goals from localStorage:', error)
    }
  }
  return defaultGoals
}

// Save goals to localStorage
const saveGoalsToStorage = (goals) => {
  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem('myta-metric-goals', JSON.stringify(goals))
    } catch (error) {
      console.warn('Failed to save goals to localStorage:', error)
    }
  }
}

// Reactive metric data mapping
const metricGoals = ref(loadGoalsFromStorage())

// Handle metric card clicks - now opens goal setting modal
const handleMetricClick = (metric) => {
  console.log(`Opening goal setting for ${metric}`)
  const data = {
    ...metricData[metric],
    currentGoal: metricGoals.value[metric]
  }
  openGoalSetting(data)
}



// Handle goal saving
const handleGoalSave = (goalData) => {
  console.log('🎯 Goal save data received:', goalData)

  if (goalData && goalData.id && goalData.goal) {
    // Update the metric goals
    metricGoals.value[goalData.id] = goalData.goal

    // Save to localStorage for persistence
    saveGoalsToStorage(metricGoals.value)

    console.log(`✅ Updated ${goalData.id} goal to ${goalData.goal} and saved to localStorage`)
  }
}

// Computed properties for dynamic progress calculation
const getProgress = (metricId) => {
  const metric = metricData[metricId]
  const goal = metricGoals.value[metricId]
  if (!metric || !goal) return 0
  return Math.min(100, Math.round((metric.currentValue / goal) * 100))
}

const getProgressWidth = (metricId) => {
  return `${getProgress(metricId)}%`
}

const getGoalText = (metricId) => {
  const metric = metricData[metricId]
  const goal = metricGoals.value[metricId]
  if (!metric || !goal) return ''

  const current = metric.currentValue
  const unit = metric.unit

  if (unit === 'seconds') {
    const currentMin = Math.floor(current / 60)
    const currentSec = current % 60
    const goalMin = Math.floor(goal / 60)
    const goalSec = goal % 60
    return `${currentMin}:${currentSec.toString().padStart(2, '0')} of ${goalMin}:${goalSec.toString().padStart(2, '0')}`
  } else if (unit === 'dollars') {
    return `$${current.toLocaleString()} of $${goal.toLocaleString()}`
  } else if (unit === 'hours') {
    return `${(current / 1000).toFixed(1)}K of ${(goal / 1000).toFixed(1)}K hrs`
  } else if (unit === '%') {
    return `${current}% of ${goal}%`
  } else {
    return `${current.toLocaleString()} of ${goal.toLocaleString()}`
  }
}









// Listen for goal updates
onMounted(() => {
  // Reload goals from localStorage on mount (in case of page refresh)
  metricGoals.value = loadGoalsFromStorage()
  console.log('📊 Goals loaded from localStorage:', metricGoals.value)

  const handleGoalUpdate = (event) => {
    console.log('🎯 Goal update event received:', event.detail)
    handleGoalSave(event.detail)
  }

  window.addEventListener('goalUpdated', handleGoalUpdate)

  onUnmounted(() => {
    window.removeEventListener('goalUpdated', handleGoalUpdate)
  })
})
</script>
