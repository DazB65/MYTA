import { defineStore } from 'pinia'
import { computed, readonly, ref } from 'vue'
import type { AnalyticsData } from '../types/analytics'

export interface ChannelGoal {
  id: string
  type: 'views' | 'subscribers' | 'revenue' | 'engagement'
  title: string
  target: number
  current: number
  deadline: Date
  color: string
  icon: string
}

export interface GoalProgress {
  percentage: number
  remaining: number
  onTrack: boolean
  daysLeft: number
}

export const useAnalyticsStore = defineStore('analytics', () => {
  // State
  const data = ref<AnalyticsData>({
    overview: null,
    channelHealth: null,
    revenue: null,
    subscribers: null,
    contentPerformance: null,
    status: {
      youtube_connected: false,
      analytics_available: false,
      channel_id: null,
    },
  })

  const loading = ref(false)
  const error = ref<string | null>(null)

  // Channel Goals State
  const goals = ref<ChannelGoal[]>([
    {
      id: '1',
      type: 'views',
      title: 'Reach 10K Views',
      target: 10000,
      current: 7500,
      deadline: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days from now
      color: 'from-orange-400 to-pink-500',
      icon: '👁️',
    },
    {
      id: '2',
      type: 'subscribers',
      title: 'Get 1K Subscribers',
      target: 1000,
      current: 750,
      deadline: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000), // 14 days from now
      color: 'from-blue-400 to-cyan-500',
      icon: '👥',
    },
    {
      id: '3',
      type: 'revenue',
      title: 'Earn $500 Revenue',
      target: 500,
      current: 320,
      deadline: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000), // 3 days from now
      color: 'from-green-400 to-emerald-500',
      icon: '💰',
    },
  ])

  // Getters
  const isConnected = computed(() => data.value.status.youtube_connected)
  const hasData = computed(() => data.value.overview !== null)
  const isLoading = computed(() => loading.value)
  const healthScore = computed(() => 75) // Mock value
  const totalViews = computed(() => 1250000) // Mock value
  const subscriberGrowth = computed(() => ({ net: 150, rate: 2.5 })) // Mock value
  const revenueMetrics = computed(() => ({ total: 1250, rpm: 3.2, cpm: 1.8 })) // Mock value
  const topVideos = computed(() => []) // Mock empty array

  // Goal-related getters
  const getGoalProgress = (goal: ChannelGoal): GoalProgress => {
    const percentage = Math.min(Math.round((goal.current / goal.target) * 100), 100)
    const remaining = Math.max(goal.target - goal.current, 0)
    const now = new Date()
    const daysLeft = Math.ceil((goal.deadline.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
    const onTrack = percentage >= 100 - (daysLeft / 365) * 100

    return {
      percentage,
      remaining,
      onTrack,
      daysLeft: Math.max(daysLeft, 0),
    }
  }

  const goalsWithProgress = computed(() => {
    return goals.value.map(goal => ({
      ...goal,
      progress: getGoalProgress(goal),
    }))
  })

  // Actions
  const initialize = async (userId: string) => {
    console.log('Analytics initialized for user:', userId)
  }

  const refresh = async () => {
    console.log('Analytics refreshed')
  }

  const formatNumber = (num: number | null | undefined): string => {
    if (num === null || num === undefined) return '0'
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`
    } else if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`
    }
    return num.toString()
  }

  const formatCurrency = (amount: number | null | undefined): string => {
    if (amount === null || amount === undefined) return '$0.00'
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount)
  }

  const formatPercentage = (value: number | null | undefined, decimals: number = 1): string => {
    if (value === null || value === undefined) return '0%'
    return `${value.toFixed(decimals)}%`
  }

  const getHealthColor = (score: number): string => {
    if (score >= 80) return '#10b981'
    if (score >= 60) return '#f59e0b'
    return '#ef4444'
  }

  // Goal management actions
  const updateGoalProgress = (goalId: string, current: number) => {
    try {
      if (typeof current !== 'number' || current < 0) {
        throw new Error('Invalid current value')
      }

      const goal = goals.value.find(g => g.id === goalId)
      if (!goal) {
        throw new Error(`Goal with id ${goalId} not found`)
      }

      goal.current = current
    } catch (err) {
      error.value = `Failed to update goal progress: ${err instanceof Error ? err.message : 'Unknown error'}`
      if (process.env.NODE_ENV === 'development') {
        console.error('Error updating goal progress:', err)
      }
      throw err
    }
  }

  const addGoal = (goalData: Omit<ChannelGoal, 'id'>) => {
    try {
      if (!goalData.title || !goalData.target || !goalData.type) {
        throw new Error('Missing required goal data')
      }

      const newGoal: ChannelGoal = {
        ...goalData,
        id: Date.now().toString(),
      }
      goals.value.push(newGoal)
    } catch (err) {
      error.value = `Failed to add goal: ${err instanceof Error ? err.message : 'Unknown error'}`
      if (process.env.NODE_ENV === 'development') {
        console.error('Error adding goal:', err)
      }
      throw err
    }
  }

  const updateGoal = (goalId: string, updates: Partial<ChannelGoal>) => {
    try {
      const goal = goals.value.find(g => g.id === goalId)
      if (!goal) {
        throw new Error(`Goal with id ${goalId} not found`)
      }

      // Update the goal with the provided updates
      Object.assign(goal, updates)
    } catch (err) {
      error.value = `Failed to update goal: ${err instanceof Error ? err.message : 'Unknown error'}`
      if (process.env.NODE_ENV === 'development') {
        console.error('Error updating goal:', err)
      }
      throw err
    }
  }

  const removeGoal = (goalId: string) => {
    const index = goals.value.findIndex(g => g.id === goalId)
    if (index !== -1) {
      goals.value.splice(index, 1)
    }
  }

  return {
    // State
    data: readonly(data),
    loading: readonly(loading),
    error: readonly(error),

    // Getters
    isConnected,
    hasData,
    isLoading,
    healthScore,
    totalViews,
    subscriberGrowth,
    revenueMetrics,
    topVideos,
    goals: readonly(goals),
    goalsWithProgress,
    getGoalProgress,

    // Actions
    initialize,
    refresh,
    formatNumber,
    formatCurrency,
    formatPercentage,
    getHealthColor,
    updateGoalProgress,
    updateGoal,
    addGoal,
    removeGoal,
  }
})
