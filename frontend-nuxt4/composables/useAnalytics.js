/**
 * Analytics composable for managing YouTube Analytics data
 * Provides reactive state management and API integration with performance optimization
 */
import { computed, reactive, readonly, ref, watch } from 'vue'
import { usePerformance } from './usePerformance'

export const useAnalytics = () => {
  // Performance optimization
  const { cachedApiCall, debounce, metrics } = usePerformance()

  // Reactive state
  const loading = ref(false)
  const error = ref(null)
  const lastUpdated = ref(null)

  // Analytics data state
  const analyticsData = reactive({
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

  // Configuration
  const config = reactive({
    userId: null,
    timeRange: 30, // days
    autoRefresh: true,
    refreshInterval: 5 * 60 * 1000, // 5 minutes
  })

  let refreshTimer = null

  // API base URL - configured for MYTA backend
  const API_BASE =
    process.env.NODE_ENV === 'production' ? 'https://your-api-domain.com' : 'http://localhost:8000'

  // Computed properties for derived data
  const isConnected = computed(() => analyticsData.status.youtube_connected)
  const hasData = computed(() => analyticsData.overview !== null)
  const isLoading = computed(() => loading.value)

  const healthScore = computed(() => {
    if (!analyticsData.channelHealth?.data) return 0
    return Math.round(analyticsData.channelHealth.data.health_score || 0)
  })

  const totalViews = computed(() => {
    if (!analyticsData.channelHealth?.data) return 0
    return analyticsData.channelHealth.data.view_velocity || 0
  })

  const subscriberGrowth = computed(() => {
    if (!analyticsData.subscribers?.data?.summary) return { net: 0, rate: 0 }
    const summary = analyticsData.subscribers.data.summary
    return {
      net: summary.net_change || 0,
      rate: summary.growth_rate || 0,
    }
  })

  const revenueMetrics = computed(() => {
    if (!analyticsData.revenue?.data) return { total: 0, rpm: 0, cpm: 0 }
    return {
      total: analyticsData.revenue.data.total_revenue || 0,
      rpm: analyticsData.revenue.data.rpm || 0,
      cpm: analyticsData.revenue.data.cpm || 0,
    }
  })

  const topVideos = computed(() => {
    if (!analyticsData.contentPerformance?.data?.videos) return []
    return analyticsData.contentPerformance.data.videos
      .sort((a, b) => b.views - a.views)
      .slice(0, 5)
  })

  // Mock data for frontend development
  const getMockData = endpoint => {
    const mockResponses = {
      '/api/analytics/status/': {
        status: 'success',
        data: {
          youtube_connected: true,
          analytics_available: true,
          channel_id: 'UC_mock_channel_id',
        },
      },
      '/api/analytics/overview/': {
        status: 'success',
        data: {
          total_views: 125000,
          total_subscribers: 8500,
          total_videos: 45,
          avg_view_duration: 4.2,
        },
      },
    }

    // Find matching mock response
    for (const [pattern, response] of Object.entries(mockResponses)) {
      if (endpoint.includes(pattern.replace('/', ''))) {
        return Promise.resolve(response)
      }
    }

    return Promise.resolve({ status: 'success', data: {} })
  }

  // API helper function - real backend integration
  const apiCall = async (endpoint, options = {}) => {
    try {
      const url = `${API_BASE}${endpoint}`
      console.log(`API call: ${url}`)

      const response = await fetch(url, {
        method: options.method || 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        body: options.body ? JSON.stringify(options.body) : undefined,
        ...options,
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      return data
    } catch (err) {
      console.error(`API call failed for ${endpoint}:`, err)
      // Fallback to mock data during development if backend is unavailable
      if (process.env.NODE_ENV === 'development') {
        console.warn('Falling back to mock data due to API error')
        return getMockData(endpoint)
      }
      throw err
    }
  }

  // Fetch analytics status
  const fetchStatus = async userId => {
    if (!userId) {
      throw new Error('User ID is required')
    }

    try {
      // Use the YouTube channel status endpoint
      const result = await apiCall(`/api/youtube/channel-status/${userId}`)

      if (result.status === 'success') {
        // Map the response to our expected format
        const statusData = {
          youtube_connected: result.data.has_channel || false,
          analytics_available: result.data.can_fetch_videos || false,
          channel_id: result.data.channel_id || null,
        }
        analyticsData.status = statusData
        return statusData
      } else {
        throw new Error(result.error || 'Failed to fetch status')
      }
    } catch (err) {
      error.value = `Status check failed: ${err.message}`
      throw err
    }
  }

  // Fetch overview data (combines all metrics) - with caching
  const fetchOverview = async (userId, days = 30) => {
    if (!userId) {
      throw new Error('User ID is required')
    }

    try {
      loading.value = true
      error.value = null

      const cacheKey = `overview:${userId}:${days}`
      const result = await cachedApiCall(
        cacheKey,
        () =>
          apiCall(`/api/youtube/analytics`, {
            method: 'POST',
            body: {
              channel_id: '', // Will be auto-resolved by backend
              user_id: userId,
              include_videos: true,
              video_count: 10,
            },
          }),
        { cacheType: 'analytics' }
      )

      if (result.status === 'success') {
        // Update individual data stores
        analyticsData.overview = result

        if (result.data.channel_health?.status === 'success') {
          analyticsData.channelHealth = result.data.channel_health
        }

        if (result.data.revenue?.status === 'success') {
          analyticsData.revenue = result.data.revenue
        }

        if (result.data.subscribers?.status === 'success') {
          analyticsData.subscribers = result.data.subscribers
        }

        if (result.data.content_performance?.status === 'success') {
          analyticsData.contentPerformance = result.data.content_performance
        }

        lastUpdated.value = new Date()
        return result
      } else {
        throw new Error(result.error || 'Failed to fetch overview')
      }
    } catch (err) {
      error.value = `Failed to load analytics: ${err.message}`
      throw err
    } finally {
      loading.value = false
    }
  }

  // Fetch individual metrics - with caching
  const fetchChannelHealth = async (userId, days = 30) => {
    try {
      const cacheKey = `channelHealth:${userId}:${days}`
      const result = await cachedApiCall(
        cacheKey,
        () => apiCall(`/api/analytics/channel-health/${userId}?days=${days}`),
        { cacheType: 'channelHealth' }
      )

      if (result.status === 'success') {
        analyticsData.channelHealth = result
        return result
      } else {
        throw new Error(result.error)
      }
    } catch (err) {
      error.value = `Channel health fetch failed: ${err.message}`
      throw err
    }
  }

  const fetchRevenue = async (userId, days = 30) => {
    try {
      const cacheKey = `revenue:${userId}:${days}`
      const result = await cachedApiCall(
        cacheKey,
        () => apiCall(`/api/analytics/revenue/${userId}?days=${days}`),
        { cacheType: 'revenue' }
      )

      if (result.status === 'success') {
        analyticsData.revenue = result
        return result
      } else {
        throw new Error(result.error)
      }
    } catch (err) {
      error.value = `Revenue fetch failed: ${err.message}`
      throw err
    }
  }

  const fetchSubscribers = async (userId, days = 30) => {
    try {
      const cacheKey = `subscribers:${userId}:${days}`
      const result = await cachedApiCall(
        cacheKey,
        () => apiCall(`/api/analytics/subscribers/${userId}?days=${days}`),
        { cacheType: 'subscribers' }
      )

      if (result.status === 'success') {
        analyticsData.subscribers = result
        return result
      } else {
        throw new Error(result.error)
      }
    } catch (err) {
      error.value = `Subscribers fetch failed: ${err.message}`
      throw err
    }
  }

  const fetchContentPerformance = async (userId, days = 30) => {
    try {
      const cacheKey = `contentPerformance:${userId}:${days}`
      const result = await cachedApiCall(
        cacheKey,
        () => apiCall(`/api/analytics/content-performance/${userId}?days=${days}`),
        { cacheType: 'content' }
      )

      if (result.status === 'success') {
        analyticsData.contentPerformance = result
        return result
      } else {
        throw new Error(result.error)
      }
    } catch (err) {
      error.value = `Content performance fetch failed: ${err.message}`
      throw err
    }
  }

  // Initialize and load data
  const initialize = async (userId, options = {}) => {
    if (!userId) {
      throw new Error('User ID is required for initialization')
    }

    config.userId = userId
    config.timeRange = options.timeRange || 30
    config.autoRefresh = options.autoRefresh !== false

    try {
      // First check status
      await fetchStatus(userId)

      if (analyticsData.status.analytics_available) {
        // Load overview data
        await fetchOverview(userId, config.timeRange)

        // Set up auto-refresh if enabled
        if (config.autoRefresh) {
          startAutoRefresh()
        }
      } else {
        error.value = 'YouTube Analytics not available. Please connect your YouTube account.'
      }
    } catch (err) {
      error.value = `Initialization failed: ${err.message}`
      throw err
    }
  }

  // Refresh all data - debounced for performance
  const refresh = debounce(async (forceRefresh = false) => {
    if (!config.userId) {
      throw new Error('Analytics not initialized')
    }

    try {
      if (forceRefresh) {
        // Clear cache and force fresh data
        const { cacheClear } = usePerformance()
        cacheClear()
      }

      await fetchOverview(config.userId, config.timeRange)
    } catch (err) {
      error.value = `Refresh failed: ${err.message}`
      throw err
    }
  }, 500)

  // Auto-refresh management
  const startAutoRefresh = () => {
    if (refreshTimer) clearInterval(refreshTimer)

    refreshTimer = setInterval(async () => {
      try {
        await refresh()
      } catch (err) {
        console.warn('Auto-refresh failed:', err)
      }
    }, config.refreshInterval)
  }

  const stopAutoRefresh = () => {
    if (refreshTimer) {
      clearInterval(refreshTimer)
      refreshTimer = null
    }
  }

  // Change time range
  const setTimeRange = async days => {
    config.timeRange = days
    if (config.userId) {
      await fetchOverview(config.userId, days)
    }
  }

  // YouTube OAuth connection
  const connectYouTube = async userId => {
    if (!userId) {
      throw new Error('User ID is required')
    }

    try {
      // Initiate OAuth flow
      const result = await apiCall('/api/oauth/initiate', {
        method: 'POST',
        body: {
          user_id: userId,
          return_url: window.location.href,
        },
      })

      if (result.authorization_url) {
        // Redirect to Google OAuth
        window.location.href = result.authorization_url
      } else {
        throw new Error('Failed to get authorization URL')
      }
    } catch (err) {
      error.value = `YouTube connection failed: ${err.message}`
      throw err
    }
  }

  // Check OAuth status
  const checkOAuthStatus = async userId => {
    try {
      const result = await apiCall(`/api/oauth/status/${userId}`)
      return result
    } catch (err) {
      console.warn('OAuth status check failed:', err)
      return { authenticated: false }
    }
  }

  // Utility functions
  const formatNumber = num => {
    if (num === null || num === undefined) return '0'
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`
    } else if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`
    }
    return num.toString()
  }

  const formatCurrency = amount => {
    if (amount === null || amount === undefined) return '$0.00'
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount)
  }

  const formatPercentage = (value, decimals = 1) => {
    if (value === null || value === undefined) return '0%'
    return `${value.toFixed(decimals)}%`
  }

  const getHealthColor = score => {
    if (score >= 80) return '#10b981' // green
    if (score >= 60) return '#f59e0b' // yellow
    return '#ef4444' // red
  }

  // Cleanup on unmount
  const cleanup = () => {
    stopAutoRefresh()
  }

  // Watch for configuration changes
  watch(
    () => config.timeRange,
    newRange => {
      if (config.userId) {
        fetchOverview(config.userId, newRange)
      }
    }
  )

  return {
    // State
    loading: readonly(loading),
    error: readonly(error),
    lastUpdated: readonly(lastUpdated),
    analyticsData: readonly(analyticsData),
    config: readonly(config),

    // Performance metrics
    performanceMetrics: readonly(metrics),

    // Computed
    isConnected,
    hasData,
    isLoading,
    healthScore,
    totalViews,
    subscriberGrowth,
    revenueMetrics,
    topVideos,

    // Methods
    initialize,
    refresh,
    fetchStatus,
    fetchOverview,
    fetchChannelHealth,
    fetchRevenue,
    fetchSubscribers,
    fetchContentPerformance,
    setTimeRange,
    startAutoRefresh,
    stopAutoRefresh,
    cleanup,

    // OAuth methods
    connectYouTube,
    checkOAuthStatus,

    // Utilities
    formatNumber,
    formatCurrency,
    formatPercentage,
    getHealthColor,
  }
}
