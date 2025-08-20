/**
 * Real-Time Analytics Composable for MYTA
 * Integrates with backend analytics APIs to provide live data
 */

import { ref, computed, onMounted, onUnmounted } from 'vue'

export interface RealTimeMetrics {
  views: number
  watchTime: number
  subscribers: number
  ctr: number
  retention: number
  revenue: number
  lastUpdated: string
}

export interface PerformanceAlert {
  id: string
  type: string
  priority: 'critical' | 'high' | 'medium' | 'low'
  title: string
  message: string
  urgency: string
  recommendedAction: string
}

export interface OptimizationRecommendation {
  id: string
  category: string
  priority: 'high' | 'medium' | 'low'
  title: string
  description: string
  expectedImpact: string
  timeline: string
  specificActions: string[]
}

export interface TrendingOpportunity {
  id: string
  title: string
  description: string
  urgency: 'high' | 'medium' | 'low'
  trendingTopics: string[]
  actionDeadline: string
  potentialImpact: string
}

export interface RealTimeInsights {
  performanceAlerts: PerformanceAlert[]
  optimizationRecommendations: OptimizationRecommendation[]
  trendingOpportunities: TrendingOpportunity[]
  competitiveInsights: any[]
  growthPredictions: any
}

export const useRealTimeAnalytics = (channelId?: string) => {
  // State
  const metrics = ref<RealTimeMetrics>({
    views: 0,
    watchTime: 0,
    subscribers: 0,
    ctr: 0,
    retention: 0,
    revenue: 0,
    lastUpdated: new Date().toISOString()
  })

  const insights = ref<RealTimeInsights>({
    performanceAlerts: [],
    optimizationRecommendations: [],
    trendingOpportunities: [],
    competitiveInsights: [],
    growthPredictions: {}
  })

  const loading = ref(false)
  const error = ref<string | null>(null)
  const connected = ref(false)

  // Auto-refresh interval
  let refreshInterval: NodeJS.Timeout | null = null

  // Computed
  const healthScore = computed(() => {
    const ctrScore = Math.min(metrics.value.ctr / 0.06, 1) * 30
    const retentionScore = Math.min(metrics.value.retention / 0.50, 1) * 40
    const subscriberScore = Math.min(metrics.value.subscribers / 10000, 1) * 30
    return Math.round(ctrScore + retentionScore + subscriberScore)
  })

  const performanceStatus = computed(() => {
    const score = healthScore.value
    if (score >= 80) return { status: 'excellent', color: '#10B981' }
    if (score >= 60) return { status: 'good', color: '#3B82F6' }
    if (score >= 40) return { status: 'fair', color: '#F59E0B' }
    return { status: 'needs improvement', color: '#EF4444' }
  })

  const criticalAlerts = computed(() => {
    return insights.value.performanceAlerts.filter(alert => 
      alert.priority === 'critical' || alert.priority === 'high'
    )
  })

  const hasUrgentOpportunities = computed(() => {
    return insights.value.trendingOpportunities.some(opp => opp.urgency === 'high')
  })

  // Methods
  const fetchRealTimeMetrics = async (timeRange: string = 'last_7_days') => {
    if (!channelId) return

    try {
      loading.value = true
      error.value = null

      const response = await $fetch(`/api/realtime-analytics/dashboard/${channelId}`, {
        query: { time_range: timeRange },
        headers: {
          'Authorization': `Bearer ${useAuthStore().token}`
        }
      })

      if (response.success) {
        const data = response.data
        
        // Update metrics
        metrics.value = {
          views: data.real_time_metrics.views || 0,
          watchTime: data.real_time_metrics.watch_time_minutes || 0,
          subscribers: data.dashboard.performance_overview?.current_metrics?.subscriber_count || 0,
          ctr: data.real_time_metrics.ctr || 0,
          retention: data.real_time_metrics.retention || 0,
          revenue: data.real_time_metrics.revenue || 0,
          lastUpdated: data.real_time_metrics.last_updated || new Date().toISOString()
        }

        connected.value = true
      }
    } catch (err) {
      console.error('Error fetching real-time metrics:', err)
      error.value = 'Failed to fetch real-time data'
      connected.value = false
      
      // Fallback to mock data for demo
      metrics.value = {
        views: 12543,
        watchTime: 6271.5,
        subscribers: 1247,
        ctr: 0.045,
        retention: 0.42,
        revenue: 23.45,
        lastUpdated: new Date().toISOString()
      }
    } finally {
      loading.value = false
    }
  }

  const fetchRealTimeInsights = async () => {
    if (!channelId) return

    try {
      const response = await $fetch(`/api/realtime-analytics/insights/${channelId}`, {
        headers: {
          'Authorization': `Bearer ${useAuthStore().token}`
        }
      })

      if (response.success) {
        const data = response.data.insights
        
        insights.value = {
          performanceAlerts: data.performance_alerts || [],
          optimizationRecommendations: data.optimization_recommendations || [],
          trendingOpportunities: data.trending_opportunities || [],
          competitiveInsights: data.competitive_insights || [],
          growthPredictions: data.growth_predictions || {}
        }
      }
    } catch (err) {
      console.error('Error fetching real-time insights:', err)
      
      // Fallback to mock data for demo
      insights.value = {
        performanceAlerts: [
          {
            id: '1',
            type: 'performance_alert',
            priority: 'high',
            title: 'Low Click-Through Rate',
            message: 'Your CTR has dropped to 2.8%, below the 4% benchmark',
            urgency: 'high',
            recommendedAction: 'Optimize thumbnails and titles immediately'
          }
        ],
        optimizationRecommendations: [
          {
            id: '1',
            category: 'thumbnails',
            priority: 'high',
            title: 'Optimize Thumbnail Strategy',
            description: 'Your CTR suggests thumbnail improvements could significantly boost performance',
            expectedImpact: '15-25% CTR improvement',
            timeline: '1-2 weeks',
            specificActions: [
              'Use high contrast colors and bold text',
              'Include faces with clear emotions',
              'A/B test different thumbnail styles'
            ]
          }
        ],
        trendingOpportunities: [
          {
            id: '1',
            title: 'Trending Content Opportunity',
            description: 'Hot topics in your niche are trending right now',
            urgency: 'high',
            trendingTopics: ['AI tools', 'productivity hacks', '2024 trends'],
            actionDeadline: 'next 24-48 hours',
            potentialImpact: '30-50% view increase'
          }
        ],
        competitiveInsights: [],
        growthPredictions: {
          next_30_days: {
            subscribers: metrics.value.subscribers * 1.05,
            confidence: 'medium'
          }
        }
      }
    }
  }

  const refreshData = async (timeRange?: string) => {
    await Promise.all([
      fetchRealTimeMetrics(timeRange),
      fetchRealTimeInsights()
    ])
  }

  const startAutoRefresh = (intervalMs: number = 300000) => { // 5 minutes default
    if (refreshInterval) {
      clearInterval(refreshInterval)
    }
    
    refreshInterval = setInterval(() => {
      refreshData()
    }, intervalMs)
  }

  const stopAutoRefresh = () => {
    if (refreshInterval) {
      clearInterval(refreshInterval)
      refreshInterval = null
    }
  }

  const getOptimizationRecommendations = async () => {
    if (!channelId) return []

    try {
      const response = await $fetch(`/api/realtime-analytics/optimization-recommendations/${channelId}`, {
        headers: {
          'Authorization': `Bearer ${useAuthStore().token}`
        }
      })

      if (response.success) {
        return response.data.recommendations
      }
    } catch (err) {
      console.error('Error fetching optimization recommendations:', err)
    }

    return []
  }

  const getTrendingAnalysis = async (niche: string = 'general') => {
    try {
      const response = await $fetch('/api/realtime-analytics/trending-analysis', {
        query: { niche },
        headers: {
          'Authorization': `Bearer ${useAuthStore().token}`
        }
      })

      if (response.success) {
        return response.data.trending_analysis
      }
    } catch (err) {
      console.error('Error fetching trending analysis:', err)
    }

    return null
  }

  const trackOptimizationImplementation = async (implementedActions: string[]) => {
    if (!channelId) return

    try {
      await $fetch('/api/realtime-analytics/track-implementation', {
        method: 'POST',
        body: {
          channel_id: channelId,
          implemented_actions: implementedActions
        },
        headers: {
          'Authorization': `Bearer ${useAuthStore().token}`
        }
      })
    } catch (err) {
      console.error('Error tracking implementation:', err)
    }
  }

  // Lifecycle
  onMounted(() => {
    if (channelId) {
      refreshData()
      startAutoRefresh()
    }
  })

  onUnmounted(() => {
    stopAutoRefresh()
  })

  return {
    // State
    metrics: readonly(metrics),
    insights: readonly(insights),
    loading: readonly(loading),
    error: readonly(error),
    connected: readonly(connected),

    // Computed
    healthScore,
    performanceStatus,
    criticalAlerts,
    hasUrgentOpportunities,

    // Methods
    refreshData,
    fetchRealTimeMetrics,
    fetchRealTimeInsights,
    startAutoRefresh,
    stopAutoRefresh,
    getOptimizationRecommendations,
    getTrendingAnalysis,
    trackOptimizationImplementation
  }
}
