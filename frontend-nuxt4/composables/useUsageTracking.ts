/**
 * Usage Tracking Composable for MYTA
 * Provides easy-to-use functions for tracking usage and checking limits
 */

import { computed, ref } from 'vue'

interface UsageData {
  [key: string]: {
    current: number
    limit: number
  }
}

interface UsageAlert {
  id: number
  usage_type: string
  threshold: number
  message: string
  is_read: boolean
  created_at: string
}

interface PlanData {
  name: string
  price: number
  billing_cycle: string
}

export const useUsageTracking = () => {
  // State
  const usage = ref<UsageData>({})
  const currentPlan = ref<PlanData | null>(null)
  const usageAlerts = ref<UsageAlert[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const unreadAlerts = computed(() => 
    usageAlerts.value.filter(alert => !alert.is_read)
  )

  // API Base URL
  const apiBase = 'http://localhost:8000/api/usage'

  // Methods
  const fetchUsageSummary = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await $fetch(`${apiBase}/summary`)
      if (response.success) {
        const data = response.data
        usage.value = data.usage || {}
        currentPlan.value = data.plan || null
        usageAlerts.value = data.alerts || []
      } else {
        throw new Error(response.message || 'Failed to fetch usage summary')
      }
    } catch (err: any) {
      console.error('Error fetching usage summary:', err)
      error.value = err.message || 'Failed to fetch usage summary'
    } finally {
      loading.value = false
    }
  }

  const markAlertAsRead = async (alertId: number) => {
    try {
      const response = await $fetch(`${apiBase}/alerts/${alertId}/read`, {
        method: 'POST'
      })
      
      if (response.success) {
        // Update local state
        const alert = usageAlerts.value.find(a => a.id === alertId)
        if (alert) {
          alert.is_read = true
        }
      } else {
        throw new Error(response.message || 'Failed to mark alert as read')
      }
    } catch (err: any) {
      console.error('Error marking alert as read:', err)
      
      // Fallback: mark as read locally
      const alert = usageAlerts.value.find(a => a.id === alertId)
      if (alert) {
        alert.is_read = true
      }
    }
  }

  // Utility functions
  const formatUsageType = (usageType: string) => {
    return usageType
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const getProgressBarColor = (percentage: number) => {
    if (percentage >= 90) return 'bg-red-500'
    if (percentage >= 75) return 'bg-yellow-500'
    return 'bg-green-500'
  }

  const getUsageStatusColor = (percentage: number) => {
    if (percentage >= 90) return 'text-red-400'
    if (percentage >= 75) return 'text-yellow-400'
    return 'text-green-400'
  }

  const getUsagePercentage = (current: number, limit: number) => {
    return limit > 0 ? Math.round((current / limit) * 100) : 0
  }

  return {
    // State
    usage,
    currentPlan,
    usageAlerts,
    loading,
    error,
    
    // Computed
    unreadAlerts,
    
    // Methods
    fetchUsageSummary,
    markAlertAsRead,
    
    // Utilities
    formatUsageType,
    formatDate,
    getProgressBarColor,
    getUsageStatusColor,
    getUsagePercentage
  }
}
