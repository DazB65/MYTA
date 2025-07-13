import { useState, useEffect } from 'react'

interface AnalyticsData {
  channel_health?: any
  revenue?: any
  subscribers?: any
  content_performance?: any
}

interface UseAnalyticsReturn {
  data: AnalyticsData
  loading: boolean
  error: string | null
  refetch: () => void
}

export function useAnalytics(userId: string): UseAnalyticsReturn {
  const [data, setData] = useState<AnalyticsData>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchAnalytics = async () => {
    if (!userId) return

    setLoading(true)
    setError(null)

    try {
      // Check analytics status first
      const statusResponse = await fetch(`/api/analytics/status/${userId}`)
      const statusData = await statusResponse.json()

      if (!statusData.data?.youtube_connected) {
        setError('YouTube account not connected')
        setData({})
        setLoading(false)
        return
      }

      // Fetch all analytics data in parallel
      const [channelHealthRes, revenueRes, subscribersRes, contentPerformanceRes] = await Promise.all([
        fetch(`/api/analytics/channel-health/${userId}`),
        fetch(`/api/analytics/revenue/${userId}`),
        fetch(`/api/analytics/subscribers/${userId}`),
        fetch(`/api/analytics/content-performance/${userId}`)
      ])

      const channelHealth = await channelHealthRes.json()
      const revenue = await revenueRes.json()
      const subscribers = await subscribersRes.json()
      const contentPerformance = await contentPerformanceRes.json()

      setData({
        channel_health: channelHealth.data,
        revenue: revenue.data,
        subscribers: subscribers.data,
        content_performance: contentPerformance.data
      })

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch analytics data')
      setData({})
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchAnalytics()
  }, [userId])

  return {
    data,
    loading,
    error,
    refetch: fetchAnalytics
  }
}