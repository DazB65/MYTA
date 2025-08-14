import { defineStore } from 'pinia'
import { ref, computed, watch, readonly } from 'vue'
import type { AnalyticsData, AnalyticsConfig } from '../types/analytics'

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

  // Getters
  const isConnected = computed(() => data.value.status.youtube_connected)
  const hasData = computed(() => data.value.overview !== null)
  const isLoading = computed(() => loading.value)
  const healthScore = computed(() => 75) // Mock value
  const totalViews = computed(() => 125000) // Mock value
  const subscriberGrowth = computed(() => ({ net: 150, rate: 2.5 })) // Mock value
  const revenueMetrics = computed(() => ({ total: 1250, rpm: 3.2, cpm: 1.8 })) // Mock value
  const topVideos = computed(() => []) // Mock empty array

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

    // Actions
    initialize,
    refresh,
    formatNumber,
    formatCurrency,
    formatPercentage,
    getHealthColor,
  }
})