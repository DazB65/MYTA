/**
 * Simplified Analytics composable that works with Pinia store
 * Provides backward compatibility and additional utility functions
 */
import { computed } from 'vue'
import { useAnalyticsStore } from '../stores/analytics'
import { usePerformance } from './usePerformance'

export const useAnalytics = () => {
  const analyticsStore = useAnalyticsStore()
  const { formatNumber, formatCurrency, formatPercentage, getHealthColor } = analyticsStore

  // Re-export store state and actions for backward compatibility
  const {
    data: analyticsData,
    loading,
    error,
    isConnected,
    hasData,
    isLoading,
    healthScore,
    totalViews,
    subscriberGrowth,
    revenueMetrics,
    topVideos,
    initialize,
    refresh,
  } = analyticsStore

  // Additional computed properties for enhanced functionality
  const performanceMetrics = computed(() => {
    const { metrics } = usePerformance()
    return metrics
  })

  const dashboardSummary = computed(() => {
    if (!hasData) return null

    return {
      health: {
        score: healthScore,
        color: getHealthColor(healthScore),
        status: healthScore >= 80 ? 'excellent' : healthScore >= 60 ? 'good' : 'needs_improvement',
      },
      growth: {
        subscribers: subscriberGrowth,
        views: totalViews,
        revenue: revenueMetrics.total,
      },
      content: {
        topVideos,
        totalVideos: analyticsData.overview?.data.total_videos || 0,
        avgDuration: analyticsData.overview?.data.avg_view_duration || 0,
      },
    }
  })

  const trendsData = computed(() => {
    if (!analyticsData.subscribers?.data?.daily_changes) return []

    return analyticsData.subscribers.data.daily_changes.map(change => ({
      date: change.date,
      subscribers: change.net_change,
      views: 0, // Would need to be added to API response
      revenue: 0, // Would need to be added to API response
    }))
  })

  // Enhanced utility functions
  const getMetricTrend = (current: number, previous: number) => {
    if (previous === 0) return { trend: 'neutral', percentage: 0 }

    const change = ((current - previous) / previous) * 100
    return {
      trend: change > 0 ? 'up' : change < 0 ? 'down' : 'neutral',
      percentage: Math.abs(change),
    }
  }

  const getRevenueBreakdown = () => {
    if (!analyticsData.revenue?.data?.revenue_sources) return []

    return analyticsData.revenue.data.revenue_sources.map(source => ({
      ...source,
      formattedAmount: formatCurrency(source.amount),
      formattedPercentage: formatPercentage(source.percentage),
    }))
  }

  const getTopPerformingContent = (limit: number = 5) => {
    if (!analyticsData.contentPerformance?.data?.videos) return []

    return [...analyticsData.contentPerformance.data.videos]
      .sort((a, b) => b.engagement_rate - a.engagement_rate)
      .slice(0, limit)
      .map(video => ({
        ...video,
        formattedViews: formatNumber(video.views),
        formattedLikes: formatNumber(video.likes),
        formattedComments: formatNumber(video.comments),
        engagementRate: formatPercentage(video.engagement_rate),
      }))
  }

  const exportData = (format: 'json' | 'csv' = 'json') => {
    const data = {
      overview: analyticsData.overview,
      channelHealth: analyticsData.channelHealth,
      revenue: analyticsData.revenue,
      subscribers: analyticsData.subscribers,
      contentPerformance: analyticsData.contentPerformance,
      exportedAt: new Date().toISOString(),
    }

    if (format === 'json') {
      return JSON.stringify(data, null, 2)
    }

    // CSV export would require additional implementation
    return data
  }

  return {
    // Store state (backward compatibility)
    loading,
    error,
    analyticsData,
    performanceMetrics,

    // Computed properties
    isConnected,
    hasData,
    isLoading,
    healthScore,
    totalViews,
    subscriberGrowth,
    revenueMetrics,
    topVideos,
    dashboardSummary,
    trendsData,

    // Store actions (backward compatibility)
    initialize,
    refresh,

    // Utility functions
    formatNumber,
    formatCurrency,
    formatPercentage,
    getHealthColor,
    getMetricTrend,
    getRevenueBreakdown,
    getTopPerformingContent,
    exportData,
  }
}
