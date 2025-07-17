import { useState, useEffect } from 'react'
import { BarChart3, Users, Eye, DollarSign, Calendar, RefreshCw } from 'lucide-react'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'
import { useUserStore } from '@/store/userStore'
import { useOAuthStore } from '@/store/oauthStore'
import OAuthConnection from '@/components/oauth/OAuthConnection'
import { api } from '@/services/api'

interface AnalyticsData {
  overview: {
    views: number
    watchTime: number
    subscribers: number
    revenue: number
  }
  trends: {
    viewsTrend: number
    watchTimeTrend: number
    subscribersTrend: number
    revenueTrend: number
  }
  topVideos: Array<{
    id: string
    title: string
    views: number
    watchTime: number
    revenue: number
  }>
  audienceRetention: {
    average: number
    improvement: number
  }
}

export default function Analytics() {
  const { userId, channelInfo } = useUserStore()
  const { isAuthenticated } = useOAuthStore()
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [timeRange, setTimeRange] = useState('last_30_days')

  const fetchAnalytics = async () => {
    if (!isAuthenticated) return

    setIsLoading(true)
    setError(null)

    try {
      const response = await api.youtube.getAnalytics(
        channelInfo.channel_id || '',
        userId,
        true,
        10
      )

      // Transform the response data to match our interface
      const transformedData: AnalyticsData = {
        overview: {
          views: response.views || 0,
          watchTime: response.watchTime || 0,
          subscribers: response.subscribers || 0,
          revenue: response.revenue || 0
        },
        trends: {
          viewsTrend: response.viewsTrend || 0,
          watchTimeTrend: response.watchTimeTrend || 0,
          subscribersTrend: response.subscribersTrend || 0,
          revenueTrend: response.revenueTrend || 0
        },
        topVideos: response.topVideos || [],
        audienceRetention: {
          average: response.audienceRetention?.average || 0,
          improvement: response.audienceRetention?.improvement || 0
        }
      }

      setAnalyticsData(transformedData)
    } catch (err) {
      console.error('Failed to fetch analytics:', err)
      setError('Failed to load analytics data. Please ensure you are connected to YouTube.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    if (isAuthenticated) {
      fetchAnalytics()
    }
  }, [isAuthenticated, timeRange])

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
    return num.toString()
  }

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    if (hours > 0) return `${hours}h ${mins}m`
    return `${mins}m`
  }

  const formatTrend = (trend: number) => {
    const sign = trend > 0 ? '+' : ''
    const color = trend > 0 ? 'text-green-600' : trend < 0 ? 'text-red-600' : 'text-gray-600'
    return <span className={`font-medium ${color}`}>{sign}{trend}%</span>
  }

  if (!isAuthenticated) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
          <p className="mt-2 text-gray-600">Connect your YouTube account to view detailed analytics</p>
        </div>

        <Card>
          <div className="text-center py-12">
            <BarChart3 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">YouTube Analytics Not Connected</h2>
            <p className="text-gray-600 mb-6 max-w-md mx-auto">
              Connect your YouTube account to access detailed analytics including views, watch time, revenue, and audience insights.
            </p>
            <div className="max-w-md mx-auto">
              <OAuthConnection variant="full" showBenefits={false} />
            </div>
          </div>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
          <p className="mt-2 text-gray-600">Track your channel performance and growth</p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="last_7_days">Last 7 days</option>
            <option value="last_30_days">Last 30 days</option>
            <option value="last_90_days">Last 90 days</option>
            <option value="last_365_days">Last year</option>
          </select>
          <Button
            onClick={fetchAnalytics}
            disabled={isLoading}
            variant="secondary"
            size="sm"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
      </div>

      {error && (
        <Card className="bg-red-50 border-red-200">
          <p className="text-red-700">{error}</p>
        </Card>
      )}

      {isLoading && !analyticsData ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <div className="h-32 bg-gray-200 rounded"></div>
            </Card>
          ))}
        </div>
      ) : analyticsData ? (
        <>
          {/* Overview Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Eye className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Views</p>
                    <p className="text-2xl font-bold text-gray-900">{formatNumber(analyticsData.overview.views)}</p>
                  </div>
                </div>
                <div className="text-right">
                  {formatTrend(analyticsData.trends.viewsTrend)}
                </div>
              </div>
            </Card>

            <Card>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                    <Calendar className="w-6 h-6 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Watch Time</p>
                    <p className="text-2xl font-bold text-gray-900">{formatDuration(analyticsData.overview.watchTime)}</p>
                  </div>
                </div>
                <div className="text-right">
                  {formatTrend(analyticsData.trends.watchTimeTrend)}
                </div>
              </div>
            </Card>

            <Card>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                    <Users className="w-6 h-6 text-green-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Subscribers</p>
                    <p className="text-2xl font-bold text-gray-900">{formatNumber(analyticsData.overview.subscribers)}</p>
                  </div>
                </div>
                <div className="text-right">
                  {formatTrend(analyticsData.trends.subscribersTrend)}
                </div>
              </div>
            </Card>

            <Card>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                    <DollarSign className="w-6 h-6 text-yellow-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Revenue</p>
                    <p className="text-2xl font-bold text-gray-900">${formatNumber(analyticsData.overview.revenue)}</p>
                  </div>
                </div>
                <div className="text-right">
                  {formatTrend(analyticsData.trends.revenueTrend)}
                </div>
              </div>
            </Card>
          </div>

          {/* Top Videos */}
          <Card>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Top Performing Videos</h2>
            <div className="space-y-4">
              {analyticsData.topVideos.length > 0 ? (
                analyticsData.topVideos.map((video) => (
                  <div key={video.id} className="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900">{video.title}</h3>
                      <div className="flex items-center gap-4 mt-1 text-sm text-gray-600">
                        <span>{formatNumber(video.views)} views</span>
                        <span>{formatDuration(video.watchTime)} watch time</span>
                        <span>${formatNumber(video.revenue)} revenue</span>
                      </div>
                    </div>
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={() => window.open(`https://youtube.com/watch?v=${video.id}`, '_blank')}
                    >
                      View
                    </Button>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 text-center py-8">No video data available for this time period</p>
              )}
            </div>
          </Card>

          {/* Audience Retention */}
          <Card>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Audience Retention</h2>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-3xl font-bold text-gray-900">{analyticsData.audienceRetention.average}%</p>
                <p className="text-sm text-gray-600">Average retention rate</p>
              </div>
              <div className="text-right">
                <p className="text-lg font-medium">{formatTrend(analyticsData.audienceRetention.improvement)}</p>
                <p className="text-sm text-gray-600">vs. previous period</p>
              </div>
            </div>
          </Card>
        </>
      ) : null}
    </div>
  )
}