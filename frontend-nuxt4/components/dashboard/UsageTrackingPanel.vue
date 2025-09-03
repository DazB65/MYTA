<template>
  <div class="rounded-xl bg-forest-800 p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-lg bg-orange-500/20 flex items-center justify-center">
          <span class="text-orange-400">📊</span>
        </div>
        <div>
          <h2 class="text-xl font-semibold text-white">Usage Tracking</h2>
          <p class="text-gray-400 text-sm">Monitor your subscription usage</p>
        </div>
      </div>
      <div class="text-right">
        <div class="text-sm text-gray-400">Current Plan</div>
        <div class="text-lg font-semibold text-orange-400">{{ currentPlan?.name || 'Loading...' }}</div>
      </div>
    </div>

    <!-- Usage Overview -->
    <div v-if="usage" class="space-y-4">
      <!-- Billing Period -->
      <div class="text-sm text-gray-400 mb-4">
        Billing Period: {{ formatDate(usage.period_start) }} - {{ formatDate(usage.period_end) }}
      </div>

      <!-- Usage Items -->
      <div class="space-y-3">
        <div 
          v-for="(usageData, usageType) in usage.usage" 
          :key="usageType"
          class="bg-forest-700/50 rounded-lg p-4"
        >
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center space-x-2">
              <span class="text-sm font-medium text-white">{{ formatUsageType(usageType) }}</span>
              <span 
                v-if="usageData.limit === -1"
                class="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full"
              >
                Unlimited
              </span>
            </div>
            <div class="text-right">
              <div class="text-sm font-medium text-white">
                {{ usageData.current_usage }}{{ usageData.limit > 0 ? ` / ${usageData.limit}` : '' }}
              </div>
              <div v-if="usageData.cost > 0" class="text-xs text-gray-400">
                ${{ usageData.cost.toFixed(4) }}
              </div>
            </div>
          </div>

          <!-- Progress Bar (only for limited usage) -->
          <div v-if="usageData.limit > 0" class="w-full bg-forest-600 rounded-full h-2">
            <div 
              class="h-2 rounded-full transition-all duration-300"
              :class="getProgressBarColor(usageData.percentage_used)"
              :style="{ width: `${Math.min(usageData.percentage_used, 100)}%` }"
            />
          </div>

          <!-- Usage Status -->
          <div class="flex items-center justify-between mt-2">
            <div class="text-xs text-gray-400">
              <span v-if="usageData.limit > 0">
                {{ usageData.remaining }} remaining
              </span>
              <span v-else>
                No limits
              </span>
            </div>
            <div 
              v-if="usageData.limit > 0"
              class="text-xs font-medium"
              :class="getUsageStatusColor(usageData.percentage_used)"
            >
              {{ usageData.percentage_used.toFixed(1) }}% used
            </div>
          </div>
        </div>
      </div>

      <!-- Total Cost -->
      <div v-if="usage.total_cost > 0" class="border-t border-forest-700 pt-4 mt-4">
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-400">Estimated Usage Cost</span>
          <span class="text-lg font-semibold text-orange-400">${{ usage.total_cost.toFixed(4) }}</span>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else class="flex items-center justify-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"></div>
    </div>

    <!-- Usage Alerts -->
    <div v-if="unreadAlerts.length > 0" class="mt-6 border-t border-forest-700 pt-4">
      <h3 class="text-sm font-medium text-white mb-3">Usage Alerts</h3>
      <div class="space-y-2">
        <div 
          v-for="alert in unreadAlerts.slice(0, 3)" 
          :key="alert.id"
          class="bg-red-500/10 border border-red-500/20 rounded-lg p-3"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="text-sm font-medium text-red-400">
                {{ formatUsageType(alert.usage_type) }} {{ alert.alert_type.replace('_', ' ') }}
              </div>
              <div class="text-xs text-gray-300 mt-1">
                {{ alert.message }}
              </div>
            </div>
            <button
              @click="markAlertAsRead(alert.id)"
              class="text-gray-400 hover:text-white text-xs ml-2"
            >
              ✕
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

// Use the usage tracking composable with fallback data
const {
  usage,
  currentPlan,
  usageAlerts,
  loading,
  error,
  unreadAlerts,
  fetchUsageSummary,
  markAlertAsRead: markAlertReadAPI,
  formatUsageType,
  formatDate,
  getProgressBarColor,
  getUsageStatusColor,
  getUsagePercentage
} = useUsageTracking()

// Initialize with mock data as fallback
if (!usage.value || Object.keys(usage.value).length === 0) {
  usage.value = {
    ai_conversations: { current: 45, limit: 100 },
    video_analysis: { current: 12, limit: 25 },
    research_projects: { current: 8, limit: -1 }, // unlimited
    content_pillars: { current: 15, limit: -1 } // unlimited
  }
}

if (!currentPlan.value) {
  currentPlan.value = {
    name: 'Solo Pro',
    price: 14.99,
    billing_cycle: 'monthly'
  }
}

if (!usageAlerts.value || usageAlerts.value.length === 0) {
  usageAlerts.value = [
    {
      id: 1,
      usage_type: 'ai_requests',
      threshold: 80,
      message: 'You\'ve used 80% of your AI requests this month',
      is_read: false,
      created_at: new Date().toISOString()
    }
  ]
}

// Local methods
const markAlertAsRead = async (alertId: number) => {
  try {
    await markAlertReadAPI(alertId)
    console.log('Alert marked as read:', alertId)
  } catch (error) {
    console.error('Error marking alert as read:', error)
  }
}

// Initialize data
onMounted(async () => {
  try {
    // Try to fetch real usage data from backend API
    await fetchUsageSummary()
    console.log('Usage tracking panel loaded successfully')
  } catch (error) {
    console.error('Error loading usage data, using fallback:', error)
  }
})
</script>
