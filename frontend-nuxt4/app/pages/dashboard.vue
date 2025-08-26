<template>
  <div class="min-h-screen bg-forest-900 text-white">
    <!-- Header -->
    <div class="p-6 pt-24">
      <!-- Page Header -->
      <div class="mb-4">
        <h1 class="text-2xl font-bold text-white">Dashboard</h1>
        <p class="text-gray-400">Welcome back! Here's your channel overview.</p>
      </div>

      <!-- Channel Statistics -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <!-- Subscribers -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-red-500 to-red-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('subscribers')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-red-100 font-medium">Subscribers</p>
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
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-blue-500 to-blue-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('views')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-blue-100 font-medium">Views</p>
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
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-purple-500 to-purple-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('watchTime')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-purple-100 font-medium">Watch Time</p>
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
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-green-500 to-green-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('revenue')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-green-100 font-medium">Revenue</p>
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
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-yellow-500 to-yellow-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('engagement')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-yellow-100 font-medium">Engagement</p>
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
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-orange-500 to-orange-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('ctr')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-orange-100 font-medium">CTR</p>
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
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('avgDuration')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-indigo-100 font-medium">Avg Duration</p>
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
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-pink-500 to-pink-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('retention')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-pink-100 font-medium">Retention</p>
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
      <div class="mb-6">
        <!-- Channel Tasks - Full Width -->
        <div class="rounded-xl bg-forest-800 p-6 mb-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-semibold text-white">Channel Tasks</h2>
            <div class="flex items-center space-x-3">
              <NuxtLink
                to="/tasks"
                class="rounded-lg bg-forest-600 px-4 py-2 text-sm font-medium text-white hover:bg-forest-500 transition-colors"
              >
                View All Tasks
              </NuxtLink>
              <button
                @click="handleAddTask"
                class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 transition-colors"
              >
                Add Task
              </button>
            </div>
          </div>
          
          <div class="space-y-4">
            <!-- Task Items - exact same structure as Tasks page -->
            <div
              v-for="task in tasks"
              :key="task.id"
              class="flex items-center justify-between rounded-lg bg-forest-700 p-4 hover:bg-forest-600 transition-colors"
              :class="{
                'border-l-4 border-red-500': isOverdue(task),
                'border-l-4 border-yellow-500': isDueToday(task),
              }"
            >
              <div class="flex items-center space-x-3">
                <input
                  :checked="task.completed"
                  type="checkbox"
                  class="rounded border-forest-600 bg-forest-700 text-orange-500 focus:ring-orange-500"
                  @change="toggleTaskCompletion(task.id)"
                />
                <div class="flex-1">
                  <h4
                    class="font-medium"
                    :class="task.completed ? 'line-through text-gray-500' : 'text-white'"
                  >
                    {{ task.title }}
                  </h4>
                  <p
                    v-if="task.description"
                    class="text-sm mt-1"
                    :class="task.completed ? 'text-gray-500' : 'text-gray-400'"
                  >
                    {{ task.description }}
                  </p>
                  <div class="mt-2 flex items-center space-x-2">
                    <span class="rounded bg-forest-600 px-2 py-1 text-xs text-gray-300">
                      {{ formatCategory(task.category) }}
                    </span>
                    <span
                      class="rounded px-2 py-1 text-xs"
                      :class="getPriorityClass(task.priority)"
                    >
                      {{ formatPriority(task.priority) }}
                    </span>
                    <span class="text-xs text-gray-400">
                      {{ formatDueDate(task.dueDate) }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <button
                  class="text-gray-400 hover:text-white transition-colors p-2"
                  @click="editTask(task)"
                >
                  ✏️
                </button>
                <button
                  class="text-gray-400 hover:text-red-400 transition-colors p-2"
                  @click="deleteTask(task.id)"
                >
                  🗑️
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Page metadata
definePageMeta({
  title: 'Dashboard - MYTA',
  description: 'Your YouTube channel dashboard'
})

// Use the modal composable
const { openGoalSetting, openTask } = useModals()

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

// Task management - using proper Task interface structure
const tasks = ref([
  {
    id: '1',
    title: 'Create thumbnail for latest video',
    description: 'Design and create an eye-catching thumbnail for the latest video upload',
    status: 'pending',
    priority: 'high',
    category: 'content',
    dueDate: new Date(Date.now() + 24 * 60 * 60 * 1000), // Tomorrow
    createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 days ago
    updatedAt: new Date(Date.now() - 1 * 60 * 60 * 1000), // 1 hour ago
    completed: false,
    tags: ['design', 'thumbnail', 'video'],
    estimatedTime: 60, // 1 hour
    notes: 'Use bright colors and clear text'
  },
  {
    id: '2',
    title: 'Write script for next video',
    description: 'Research and write a comprehensive script for the upcoming video',
    status: 'in_progress',
    priority: 'medium',
    category: 'content',
    dueDate: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000), // Day after tomorrow
    createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // 3 days ago
    updatedAt: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
    completed: false,
    tags: ['script', 'writing', 'content'],
    estimatedTime: 120, // 2 hours
    notes: 'Include call-to-action at the end'
  },
  {
    id: '3',
    title: 'Upload video to YouTube',
    description: 'Upload the finished video with proper tags and description',
    status: 'completed',
    priority: 'high',
    category: 'content',
    dueDate: new Date(Date.now() - 24 * 60 * 60 * 1000), // Yesterday (completed)
    createdAt: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000), // 4 days ago
    updatedAt: new Date(Date.now() - 24 * 60 * 60 * 1000), // Yesterday
    completed: true,
    tags: ['upload', 'youtube', 'publishing'],
    estimatedTime: 30, // 30 minutes
    actualTime: 25, // Completed in 25 minutes
    notes: 'Remember to add end screen'
  },
  {
    id: '4',
    title: 'Research trending topics',
    description: 'Analyze current trends and identify potential video topics',
    status: 'pending',
    priority: 'low',
    category: 'research',
    dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // Next week
    createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), // Yesterday
    updatedAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), // Yesterday
    completed: false,
    tags: ['research', 'trends', 'planning'],
    estimatedTime: 90, // 1.5 hours
    notes: 'Check YouTube trending page and Google Trends'
  }
])

// Task functions - same as Tasks page
const editTask = (task) => {
  console.log('✏️ Dashboard: editTask called with:', task)
  openTask(task)
}

const handleAddTask = () => {
  console.log('➕ Add task clicked')
  openTask(null) // Open modal for new task
}

const deleteTask = (taskId) => {
  if (confirm('Are you sure you want to delete this task?')) {
    const index = tasks.value.findIndex(t => t.id === taskId)
    if (index > -1) {
      tasks.value.splice(index, 1)
      console.log(`🗑️ Deleted task with ID: ${taskId}`)
    }
  }
}

const toggleTaskCompletion = (taskId) => {
  const task = tasks.value.find(t => t.id === taskId)
  if (task) {
    task.completed = !task.completed
    console.log(`✅ Task ${taskId} completion toggled:`, task.completed)
  }
}

// Utility functions - same as Tasks page
const formatCategory = (category) => {
  return category.charAt(0).toUpperCase() + category.slice(1).replace('_', ' ')
}

const formatPriority = (priority) => {
  return priority.charAt(0).toUpperCase() + priority.slice(1)
}

const getPriorityClass = (priority) => {
  switch (priority) {
    case 'urgent': return 'bg-red-500 text-white'
    case 'high': return 'bg-orange-500 text-white'
    case 'medium': return 'bg-yellow-500 text-black'
    case 'low': return 'bg-green-500 text-white'
    default: return 'bg-gray-500 text-white'
  }
}

const formatDueDate = (date) => {
  const now = new Date()
  const dueDate = new Date(date)
  const diffTime = dueDate.getTime() - now.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays < 0) return 'Overdue'
  if (diffDays === 0) return 'Due today'
  if (diffDays === 1) return 'Due tomorrow'
  if (diffDays <= 7) return `Due in ${diffDays} days`
  return dueDate.toLocaleDateString()
}

const isOverdue = (task) => {
  if (task.completed) return false
  const now = new Date()
  const dueDate = new Date(task.dueDate)
  return dueDate < now
}

const isDueToday = (task) => {
  if (task.completed) return false
  const now = new Date()
  const dueDate = new Date(task.dueDate)
  return dueDate.toDateString() === now.toDateString()
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
