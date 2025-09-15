/**
 * Automation Composable
 * Manages intelligent automation features and settings
 */

import { ref, computed } from 'vue'
import { useApi } from './useApi'
import { useToast } from './useToast'

// Types
interface AutomationSettings {
  auto_scheduling_enabled: boolean
  auto_responses_enabled: boolean
  seo_optimization_enabled: boolean
  content_ideas_enabled: boolean
  smart_notifications_enabled: boolean
  auto_descriptions_enabled: boolean
  preferred_posting_days: string[]
  max_posts_per_week: number
  auto_response_types: string[]
  response_tone: string
  notification_frequency: string
  min_notification_priority: string
}

interface SmartNotification {
  id: string
  priority: 'low' | 'medium' | 'high' | 'urgent'
  title: string
  message: string
  action_required: boolean
  suggested_actions: string[]
  related_content?: string
  created_at: string
  expires_at?: string
}

interface AutoScheduleRecommendation {
  recommended_time: string
  confidence_score: number
  expected_performance_boost: number
  reasoning: string
  alternative_times: Array<{
    time: string
    confidence: number
    reasoning: string
  }>
}

interface AutoResponse {
  text: string
  type: string
  tone: string
  confidence: number
  requires_review: boolean
}

interface SEOOptimization {
  optimized_content: {
    title?: string
    description?: string
    tags?: string[]
  }
  improvements: {
    predicted_improvement: number
    changes_made: string[]
  }
}

export const useAutomation = () => {
  const { $api } = useApi()
  const { success, error } = useToast()

  // State
  const settings = ref<AutomationSettings>({
    auto_scheduling_enabled: true,
    auto_responses_enabled: true,
    seo_optimization_enabled: true,
    content_ideas_enabled: true,
    smart_notifications_enabled: true,
    auto_descriptions_enabled: true,
    preferred_posting_days: ['tuesday', 'thursday', 'sunday'],
    max_posts_per_week: 7,
    auto_response_types: ['questions', 'compliments'],
    response_tone: 'friendly',
    notification_frequency: 'real_time',
    min_notification_priority: 'medium'
  })

  const notifications = ref<SmartNotification[]>([])
  const dashboardData = ref<any>({})
  const isLoading = ref(false)

  // Computed
  const enabledAutomationsCount = computed(() => {
    return [
      settings.value.auto_scheduling_enabled,
      settings.value.auto_responses_enabled,
      settings.value.seo_optimization_enabled,
      settings.value.smart_notifications_enabled
    ].filter(Boolean).length
  })

  const urgentNotifications = computed(() => {
    return notifications.value.filter(n => n.priority === 'urgent' || n.priority === 'high')
  })

  const automationStatus = computed(() => {
    const total = 4 // Total automation features
    const enabled = enabledAutomationsCount.value
    
    if (enabled === total) return { status: 'optimal', message: 'All automations active' }
    if (enabled >= total * 0.75) return { status: 'good', message: 'Most automations active' }
    if (enabled >= total * 0.5) return { status: 'partial', message: 'Some automations active' }
    return { status: 'minimal', message: 'Limited automation' }
  })

  // API Methods
  const getSettings = async () => {
    try {
      isLoading.value = true
      const response = await $api('/api/automation/settings')
      
      if (response.success) {
        settings.value = { ...settings.value, ...response.settings }
      }
      
      return response
    } catch (err) {
      error('Settings Error', 'Failed to load automation settings')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const updateSettings = async (newSettings: Partial<AutomationSettings>) => {
    try {
      isLoading.value = true
      const response = await $api('/api/automation/settings', {
        method: 'POST',
        body: newSettings
      })
      
      if (response.success) {
        settings.value = { ...settings.value, ...response.settings }
        success('Settings Updated', 'Automation settings saved successfully')
      }
      
      return response
    } catch (err) {
      error('Update Failed', 'Failed to update automation settings')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const scheduleContent = async (contentData: {
    content_id: string
    title: string
    content_type?: string
    description?: string
    tags?: string[]
  }): Promise<AutoScheduleRecommendation | null> => {
    try {
      const response = await $api('/api/automation/schedule-content', {
        method: 'POST',
        body: contentData
      })
      
      if (response.success && response.recommendation) {
        success('Content Scheduled', response.message)
        return response.recommendation
      }
      
      return null
    } catch (err) {
      error('Scheduling Failed', 'Failed to schedule content automatically')
      throw err
    }
  }

  const generateAutoResponse = async (commentData: {
    comment_id: string
    comment_text: string
    video_id?: string
    commenter_name?: string
  }): Promise<AutoResponse | null> => {
    try {
      const response = await $api('/api/automation/auto-response', {
        method: 'POST',
        body: commentData
      })
      
      if (response.success && response.response) {
        return response.response
      } else if (response.requires_escalation) {
        // Comment needs manual review
        return null
      }
      
      return null
    } catch (err) {
      error('Response Generation Failed', 'Failed to generate automatic response')
      throw err
    }
  }

  const optimizeSEO = async (contentData: {
    content_id: string
    title: string
    description: string
    tags: string[]
    content_type?: string
  }): Promise<SEOOptimization | null> => {
    try {
      const response = await $api('/api/automation/optimize-seo', {
        method: 'POST',
        body: contentData
      })
      
      if (response.success) {
        success('SEO Optimized', response.message)
        return {
          optimized_content: response.optimized_content,
          improvements: response.improvements
        }
      }
      
      return null
    } catch (err) {
      error('SEO Optimization Failed', 'Failed to optimize content for SEO')
      throw err
    }
  }

  const getNotifications = async () => {
    try {
      const response = await $api('/api/automation/notifications')
      
      if (response.success) {
        notifications.value = response.notifications
      }
      
      return response
    } catch (err) {
      error('Notifications Error', 'Failed to load smart notifications')
      throw err
    }
  }

  const getDashboard = async () => {
    try {
      const response = await $api('/api/automation/dashboard')
      
      if (response.success) {
        dashboardData.value = response.dashboard_data
      }
      
      return response
    } catch (err) {
      error('Dashboard Error', 'Failed to load automation dashboard')
      throw err
    }
  }

  const getOptimizationTips = async (contentType: string = 'general') => {
    try {
      const response = await $api(`/api/automation/optimization-tips?content_type=${contentType}`)
      
      if (response.success) {
        return response.tips
      }
      
      return []
    } catch (err) {
      error('Tips Error', 'Failed to load optimization tips')
      return []
    }
  }

  // Utility Methods
  const toggleAutomation = async (automationType: keyof AutomationSettings) => {
    const newValue = !settings.value[automationType]
    await updateSettings({ [automationType]: newValue })
  }

  const formatNotificationTime = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMins / 60)
    const diffDays = Math.floor(diffHours / 24)

    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    if (diffDays < 7) return `${diffDays}d ago`
    return date.toLocaleDateString()
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'text-red-400 bg-red-900/20 border-red-500/30'
      case 'high': return 'text-orange-400 bg-orange-900/20 border-orange-500/30'
      case 'medium': return 'text-yellow-400 bg-yellow-900/20 border-yellow-500/30'
      case 'low': return 'text-blue-400 bg-blue-900/20 border-blue-500/30'
      default: return 'text-gray-400 bg-gray-900/20 border-gray-500/30'
    }
  }

  const getAutomationIcon = (automationType: string) => {
    switch (automationType) {
      case 'auto_scheduling_enabled': return '📅'
      case 'auto_responses_enabled': return '💬'
      case 'seo_optimization_enabled': return '🔍'
      case 'smart_notifications_enabled': return '🔔'
      case 'auto_descriptions_enabled': return '📝'
      case 'content_ideas_enabled': return '💡'
      default: return '🤖'
    }
  }

  return {
    // State
    settings,
    notifications,
    dashboardData,
    isLoading,

    // Computed
    enabledAutomationsCount,
    urgentNotifications,
    automationStatus,

    // Methods
    getSettings,
    updateSettings,
    scheduleContent,
    generateAutoResponse,
    optimizeSEO,
    getNotifications,
    getDashboard,
    getOptimizationTips,
    toggleAutomation,

    // Utilities
    formatNotificationTime,
    getPriorityColor,
    getAutomationIcon
  }
}
