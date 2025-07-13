import { useState, useEffect } from 'react'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'
import { formatNumber } from '@/utils'
import { useUserStore } from '@/store/userStore'
import { useOAuthStore } from '@/store/oauthStore'
import { Loader, AlertCircle } from 'lucide-react'

interface VideoData {
  id: string
  title: string
  description: string
  views: number
  likes: number
  comments: number
  publishedAt: string
  thumbnail: string
  duration: string
  category_id: string
  pillarAllocation?: {
    pillar_id: string
    pillar_name: string
    pillar_icon: string
    pillar_color: string
  }
  analytics?: {
    retention: number
    ctr: number
    revenue: number
    watch_time_hours: number
    impressions: number
    traffic_sources?: {
      search: number
      suggested: number
      external: number
      browse: number
    }
    demographics?: {
      age_groups: Record<string, number>
      gender: Record<string, number>
    }
    grade: string
  }
  insights?: string[]
  recommendations?: Array<{
    type: string
    action: string
    reason: string
  }>
}

interface PillarOption {
  id: string
  name: string
  icon: string
  color: string
}

// YouTube category mapping
const getCategoryName = (categoryId: string): string => {
  const categories: { [key: string]: string } = {
    '1': 'Film & Animation',
    '2': 'Autos & Vehicles', 
    '10': 'Music',
    '15': 'Pets & Animals',
    '17': 'Sports',
    '19': 'Travel & Events',
    '20': 'Gaming',
    '22': 'People & Blogs',
    '23': 'Comedy',
    '24': 'Entertainment',
    '25': 'News & Politics',
    '26': 'Howto & Style',
    '27': 'Education',
    '28': 'Science & Technology',
    '29': 'Nonprofits & Activism'
  }
  return categories[categoryId] || `Category ${categoryId}`
}

// Performance grading functions
const getGradeColor = (grade: string): string => {
  switch (grade) {
    case 'A+':
    case 'A':
      return 'bg-green-600 text-white'
    case 'B+':
    case 'B':
      return 'bg-blue-600 text-white'
    case 'C+':
    case 'C':
      return 'bg-yellow-600 text-white'
    case 'D+':
    case 'D':
      return 'bg-orange-600 text-white'
    case 'F':
      return 'bg-red-600 text-white'
    default:
      return 'bg-gray-600 text-white'
  }
}

const formatPercentage = (value: number | undefined): string => {
  if (value === undefined) return '--'
  return value.toFixed(1)
}

const formatCurrency = (value: number | undefined): string => {
  if (value === undefined) return '$0.00'
  return `$${value.toFixed(2)}`
}

export default function Videos() {
  const { channelInfo } = useUserStore()
  const { isAuthenticated, checkStatus } = useOAuthStore()
  
  // TEMPORARY FIX: Force use default_user for consistency with Pillars page
  const actualUserId = "default_user"
  const [videos, setVideos] = useState<VideoData[]>([])
  const [displayedVideos, setDisplayedVideos] = useState<VideoData[]>([])
  const [sortBy, setSortBy] = useState<'views' | 'likes' | 'comments' | 'date'>('date')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [videosPerPage] = useState(10)
  const [currentPage, setCurrentPage] = useState(1)
  const [availablePillars, setAvailablePillars] = useState<PillarOption[]>([])
  const [allocatingVideo, setAllocatingVideo] = useState<string | null>(null)
  const [expandedVideo, setExpandedVideo] = useState<string | null>(null)

  useEffect(() => {
    // Check OAuth status when component mounts
    checkStatus()
  }, [])

  useEffect(() => {
    // Fetch videos when authenticated and channel is configured
    if (isAuthenticated && channelInfo.name !== 'Unknown') {
      fetchVideos()
      fetchPillars()
    }
  }, [isAuthenticated, channelInfo.name])

  const fetchPillars = async () => {
    try {
      const response = await fetch(`/api/pillars/${actualUserId}`)
      if (response.ok) {
        const pillars = await response.json()
        setAvailablePillars(pillars.map((p: any) => ({
          id: p.id,
          name: p.name,
          icon: p.icon,
          color: p.color
        })))
      } else {
        console.error('Failed to fetch pillars, status:', response.status)
      }
    } catch (error) {
      console.error('Error fetching pillars:', error)
    }
  }

  const allocateVideoToPillar = async (videoId: string, pillarId: string) => {
    setAllocatingVideo(videoId)
    try {
      const payload = {
        video_id: videoId,
        pillar_id: pillarId,
        user_id: actualUserId,
        allocation_type: 'manual'
      }
      
      const response = await fetch('/api/videos/allocate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      })

      if (response.ok) {
        const allocation = await response.json()
        
        // Update video in local state
        setVideos(prev => prev.map(video => 
          video.id === videoId 
            ? { 
                ...video, 
                pillarAllocation: {
                  pillar_id: allocation.pillar_id,
                  pillar_name: allocation.pillar_name,
                  pillar_icon: allocation.pillar_icon,
                  pillar_color: allocation.pillar_color
                }
              }
            : video
        ))
        
      } else {
        throw new Error('Failed to allocate video to pillar')
      }
    } catch (error) {
      console.error('❌ Error allocating video:', error)
      alert('Failed to allocate video to pillar. Please try again.')
    } finally {
      setAllocatingVideo(null)
    }
  }

  const removeVideoAllocation = async (videoId: string) => {
    setAllocatingVideo(videoId)
    try {
      const response = await fetch(`/api/videos/${videoId}/pillar?user_id=${actualUserId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        // Remove allocation from local state
        setVideos(prev => prev.map(video => 
          video.id === videoId 
            ? { ...video, pillarAllocation: undefined }
            : video
        ))
        
      } else {
        throw new Error('Failed to remove video allocation')
      }
    } catch (error) {
      console.error('❌ Error removing allocation:', error)
      alert('Failed to remove video allocation. Please try again.')
    } finally {
      setAllocatingVideo(null)
    }
  }

  const fetchVideos = async () => {
    setLoading(true)
    setError(null)
    
    try {
      // First check if user has a valid channel configured
      const statusResponse = await fetch(`/api/youtube/channel-status/${actualUserId}`)
      if (statusResponse.ok) {
        const statusData = await statusResponse.json()
        if (!statusData.data?.has_channel) {
          setError(`No YouTube channel connected. ${statusData.data?.suggestions?.[0] || 'Please connect your YouTube channel first.'}`)
          setVideos([])
          setLoading(false)
          return
        }
      }

      // Use the simpler my-videos endpoint 
      const response = await fetch(`/api/youtube/my-videos/${actualUserId}?count=50`)

      if (response.ok) {
        const data = await response.json()
        
        if (data.status === 'success' && data.data?.videos && data.data.videos.length > 0) {
          // Transform API data to VideoData format - using simpler endpoint structure
          const transformedVideos: VideoData[] = data.data.videos.map((video: any) => ({
            id: video.video_id,
            title: video.title,
            description: video.description || '',
            views: video.view_count || 0,
            likes: video.like_count || 0,
            comments: video.comment_count || 0,
            publishedAt: video.published_at || new Date().toISOString(),
            thumbnail: video.thumbnail || '',
            duration: video.duration || '0:00',
            category_id: video.category_id || ''
          }))
          
          // Fetch existing pillar allocations for each video
          const videosWithAllocations = await Promise.all(
            transformedVideos.map(async (video) => {
              try {
                const allocationResponse = await fetch(`/api/videos/${video.id}/pillar?user_id=${actualUserId}`)
                if (allocationResponse.ok) {
                  const allocation = await allocationResponse.json()
                  if (allocation) {
                    return {
                      ...video,
                      pillarAllocation: {
                        pillar_id: allocation.pillar_id,
                        pillar_name: allocation.pillar_name,
                        pillar_icon: allocation.pillar_icon,
                        pillar_color: allocation.pillar_color
                      }
                    }
                  }
                }
              } catch (error) {
                console.error(`Error fetching allocation for video ${video.id}:`, error)
              }
              return video
            })
          )
          
          setVideos(videosWithAllocations)
          setLoading(false)
          return
        }
      } else {
        // Handle API error responses
        const errorData = await response.json().catch(() => null)
        if (errorData?.detail && typeof errorData.detail === 'object') {
          // Enhanced error response from backend
          setError(`${errorData.detail.error}: ${errorData.detail.details}`)
        } else if (errorData?.detail) {
          setError(errorData.detail)
        } else {
          setError('Failed to fetch videos from YouTube API')
        }
        setVideos([])
        setLoading(false)
        return
      }
      
      // No fallback data - only show real YouTube videos
      setVideos([])
      setCurrentPage(1) // Reset pagination when fetching new data
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load videos')
      setVideos([])
    } finally {
      setLoading(false)
    }
  }

  // Update displayed videos when videos or pagination changes
  useEffect(() => {
    const startIndex = (currentPage - 1) * videosPerPage
    const endIndex = startIndex + videosPerPage
    const sorted = [...videos].sort((a, b) => {
      switch (sortBy) {
        case 'views':
          return b.views - a.views
        case 'likes':
          return b.likes - a.likes
        case 'comments':
          return b.comments - a.comments
        case 'date':
          return new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime()
        default:
          return 0
      }
    })
    setDisplayedVideos(sorted.slice(startIndex, endIndex))
  }, [videos, currentPage, videosPerPage, sortBy])

  // Pagination helpers
  const totalPages = Math.ceil(videos.length / videosPerPage)
  const startVideo = (currentPage - 1) * videosPerPage + 1
  const endVideo = Math.min(currentPage * videosPerPage, videos.length)

  const goToPage = (page: number) => {
    setCurrentPage(page)
  }

  const goToPrevious = () => {
    setCurrentPage(prev => Math.max(1, prev - 1))
  }

  const goToNext = () => {
    setCurrentPage(prev => Math.min(totalPages, prev + 1))
  }

  // Generate page numbers for pagination
  const getPageNumbers = () => {
    const pages = []
    const maxVisible = 5
    
    if (totalPages <= maxVisible) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i)
      }
    } else {
      if (currentPage <= 3) {
        pages.push(1, 2, 3, 4, '...', totalPages)
      } else if (currentPage >= totalPages - 2) {
        pages.push(1, '...', totalPages - 3, totalPages - 2, totalPages - 1, totalPages)
      } else {
        pages.push(1, '...', currentPage - 1, currentPage, currentPage + 1, '...', totalPages)
      }
    }
    
    return pages
  }


  // Removed getPerformanceColor - no longer needed for real data only

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Video Analytics</h1>
          <p className="text-dark-400">
            Track performance and optimize your content strategy.
          </p>
          <p className="text-xs text-blue-400 mt-1">
            📊 Showing real data from YouTube Data API • No estimates or calculations
          </p>
        </div>
        <Button className="flex items-center gap-2">
          📊 Export Data
        </Button>
      </div>

      {/* Enhanced Video Stats */}
      <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
        <Card className="p-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-400">
              {videos.length}
            </div>
            <div className="text-sm text-dark-400">Total Videos</div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-400">
              {formatNumber(videos.reduce((sum, v) => sum + v.views, 0))}
            </div>
            <div className="text-sm text-dark-400">Total Views</div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-400">
              {formatNumber(videos.reduce((sum, v) => sum + v.likes, 0))}
            </div>
            <div className="text-sm text-dark-400">Total Likes</div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-400">
              {formatNumber(videos.reduce((sum, v) => sum + v.comments, 0))}
            </div>
            <div className="text-sm text-dark-400">Total Comments</div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-400">
              {formatNumber(videos.reduce((sum, v) => sum + (v.analytics?.watch_time_hours || 0), 0))}
            </div>
            <div className="text-sm text-dark-400">Watch Hours</div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-400">
              {formatCurrency(videos.reduce((sum, v) => sum + (v.analytics?.revenue || 0), 0))}
            </div>
            <div className="text-sm text-dark-400">Total Revenue</div>
          </div>
        </Card>
      </div>

      {/* Video List */}
      <Card>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-xl font-semibold">Recent Videos</h3>
            <p className="text-sm text-dark-400 mt-1">
              Showing {startVideo}-{endVideo} of {videos.length} videos
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm text-dark-400">Sort by:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="px-3 py-1 bg-dark-800 border border-dark-600 rounded text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="date">Date</option>
              <option value="views">Views</option>
              <option value="likes">Likes</option>
              <option value="comments">Comments</option>
            </select>
          </div>
        </div>

        {!isAuthenticated ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🔐</div>
            <h3 className="text-lg font-semibold mb-2 text-white">Connect YouTube to View Videos</h3>
            <p className="text-gray-300 mb-6">
              Connect your YouTube account to access detailed video analytics and data.
            </p>
            <Button 
              onClick={() => window.open(`/api/youtube/debug/oauth-redirect/${actualUserId}`, '_blank')}
              variant="primary"
            >
              Connect YouTube Account
            </Button>
          </div>
        ) : loading ? (
          <div className="text-center py-12">
            <Loader className="w-8 h-8 animate-spin mx-auto mb-4 text-primary-400" />
            <h3 className="text-lg font-semibold mb-2 text-white">Loading Videos...</h3>
            <p className="text-gray-300">
              Fetching your video data from YouTube.
            </p>
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <AlertCircle className="w-8 h-8 mx-auto mb-4 text-red-400" />
            <h3 className="text-lg font-semibold mb-2 text-red-400">Failed to Load Videos</h3>
            <p className="text-gray-300 mb-4 font-medium">{error}</p>
            <div className="flex justify-center gap-3">
              <Button onClick={fetchVideos} variant="secondary">
                Try Again
              </Button>
              {error.includes('No YouTube channel connected') && (
                <Button 
                  onClick={() => window.open(`/api/youtube/debug/oauth-redirect/${actualUserId}`, '_blank')}
                  variant="primary"
                >
                  Connect YouTube Channel
                </Button>
              )}
            </div>
          </div>
        ) : videos.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📺</div>
            <h3 className="text-lg font-semibold mb-2 text-white">No Videos Found</h3>
            <p className="text-gray-300">
              Your channel doesn't have any videos yet, or they couldn't be loaded.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {displayedVideos.map((video) => (
              <div key={video.id}>
                <div className="flex items-center gap-4 p-4 bg-dark-800/50 rounded-lg hover:bg-dark-800 transition-colors">
                {/* Thumbnail */}
                <div className="w-32 h-18 bg-dark-700 rounded-lg flex items-center justify-center flex-shrink-0 overflow-hidden">
                  {video.thumbnail ? (
                    <img 
                      src={video.thumbnail} 
                      alt={video.title}
                      className="w-full h-full object-cover rounded-lg"
                      onError={(e) => {
                        e.currentTarget.style.display = 'none';
                        e.currentTarget.parentElement!.innerHTML = '<span class="text-2xl">🎬</span>';
                      }}
                    />
                  ) : (
                    <span className="text-2xl">🎬</span>
                  )}
                </div>

                {/* Video Info */}
                <div className="flex-1 min-w-0">
                  <h4 className="font-semibold text-white mb-1 truncate">
                    {video.title}
                  </h4>
                  <div className="flex items-center gap-4 text-sm text-dark-400">
                    <span>📅 {new Date(video.publishedAt).toLocaleDateString()}</span>
                    <span>⏱️ {video.duration}</span>
                    {video.category_id && (
                      <span>🏷️ {getCategoryName(video.category_id)}</span>
                    )}
                  </div>
                </div>

                {/* Enhanced Analytics Metrics */}
                <div className="grid grid-cols-5 gap-3 text-center text-xs">
                  <div>
                    <div className="text-sm font-semibold">{formatNumber(video.views)}</div>
                    <div className="text-xs text-dark-400">Views</div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-green-400">{formatPercentage(video.analytics?.retention)}%</div>
                    <div className="text-xs text-dark-400">Retention</div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-blue-400">{formatPercentage(video.analytics?.ctr)}%</div>
                    <div className="text-xs text-dark-400">CTR</div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-purple-400">{formatCurrency(video.analytics?.revenue)}</div>
                    <div className="text-xs text-dark-400">Revenue</div>
                  </div>
                  <div>
                    <div className={`text-xs font-bold px-2 py-1 rounded ${getGradeColor(video.analytics?.grade || 'N/A')}`}>
                      {video.analytics?.grade || 'N/A'}
                    </div>
                    <div className="text-xs text-dark-400">Grade</div>
                  </div>
                </div>

                {/* Pillar Allocation */}
                <div className="w-48">
                  {video.pillarAllocation ? (
                    <div className="flex items-center gap-2 p-2 bg-dark-700 rounded-lg">
                      <span className="text-lg">{video.pillarAllocation.pillar_icon}</span>
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-medium text-white truncate">
                          {video.pillarAllocation.pillar_name}
                        </div>
                        <div className="text-xs text-dark-400">Assigned</div>
                      </div>
                      <button
                        onClick={() => removeVideoAllocation(video.id)}
                        disabled={allocatingVideo === video.id}
                        className="text-red-400 hover:text-red-300 text-xs"
                        title="Remove allocation"
                      >
                        ✕
                      </button>
                    </div>
                  ) : (
                    <select
                      value=""
                      onChange={(e) => {
                        if (e.target.value) {
                          allocateVideoToPillar(video.id, e.target.value)
                        }
                      }}
                      onClick={() => {
                      }}
                      disabled={allocatingVideo === video.id}
                      className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500 cursor-pointer relative z-10"
                      style={{ minHeight: '40px' }}
                    >
                      <option value="">Assign to Pillar</option>
                      {availablePillars.length > 0 ? (
                        availablePillars.map((pillar) => (
                          <option key={pillar.id} value={pillar.id}>
                            {pillar.icon} {pillar.name}
                          </option>
                        ))
                      ) : (
                        <option value="" disabled>No pillars available</option>
                      )}
                    </select>
                  )}
                  {allocatingVideo === video.id && (
                    <div className="text-xs text-primary-400 mt-1">Updating...</div>
                  )}
                </div>

                {/* Expand Button */}
                <button 
                  onClick={() => setExpandedVideo(expandedVideo === video.id ? null : video.id)}
                  className="w-8 h-8 text-gray-400 hover:text-white transition-colors flex items-center justify-center"
                  title={expandedVideo === video.id ? "Hide details" : "Show details"}
                >
                  {expandedVideo === video.id ? '−' : '+'}
                </button>

                </div>

              {/* Expandable Analytics Details */}
              {expandedVideo === video.id && (
                <div className="ml-36 mr-4 mb-4 p-4 bg-dark-700 rounded-lg">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {/* Traffic Sources */}
                    <div>
                      <h5 className="font-medium mb-2 text-white">Traffic Sources</h5>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-300">Search</span>
                          <span className="text-blue-400">{formatPercentage(video.analytics?.traffic_sources?.search)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-300">Suggested</span>
                          <span className="text-green-400">{formatPercentage(video.analytics?.traffic_sources?.suggested)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-300">External</span>
                          <span className="text-purple-400">{formatPercentage(video.analytics?.traffic_sources?.external)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-300">Browse</span>
                          <span className="text-orange-400">{formatPercentage(video.analytics?.traffic_sources?.browse)}%</span>
                        </div>
                      </div>
                    </div>
                    
                    {/* Quick Insights */}
                    <div>
                      <h5 className="font-medium mb-2 text-white">Quick Insights</h5>
                      <div className="space-y-1 text-sm">
                        {video.insights && video.insights.length > 0 ? (
                          video.insights.slice(0, 3).map((insight, i) => (
                            <div key={i} className="text-blue-300 flex items-start gap-1">
                              <span className="text-yellow-400 mt-0.5">•</span>
                              <span>{insight}</span>
                            </div>
                          ))
                        ) : (
                          <div className="text-gray-400 italic">No insights available</div>
                        )}
                      </div>
                    </div>
                    
                    {/* Recommendations */}
                    <div>
                      <h5 className="font-medium mb-2 text-white">Recommendations</h5>
                      <div className="space-y-2">
                        {video.recommendations && video.recommendations.length > 0 ? (
                          video.recommendations.slice(0, 2).map((rec, i) => (
                            <div key={i} className="p-2 bg-dark-600 rounded text-sm">
                              <div className="font-medium text-white text-xs mb-1">{rec.action}</div>
                              <div className="text-gray-400 text-xs">{rec.reason}</div>
                            </div>
                          ))
                        ) : (
                          <div className="text-gray-400 italic text-sm">No recommendations available</div>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Additional Metrics Row */}
                  <div className="mt-4 pt-4 border-t border-dark-600">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center text-sm">
                      <div>
                        <div className="text-gray-400">Impressions</div>
                        <div className="font-semibold text-white">{formatNumber(video.analytics?.impressions || 0)}</div>
                      </div>
                      <div>
                        <div className="text-gray-400">Watch Time</div>
                        <div className="font-semibold text-orange-400">{formatNumber(video.analytics?.watch_time_hours || 0)}h</div>
                      </div>
                      <div>
                        <div className="text-gray-400">Likes</div>
                        <div className="font-semibold text-blue-400">{formatNumber(video.likes)}</div>
                      </div>
                      <div>
                        <div className="text-gray-400">Comments</div>
                        <div className="font-semibold text-purple-400">{formatNumber(video.comments)}</div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              </div>
            ))}
            
            {/* Pagination Controls */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between pt-6 border-t border-dark-600">
                <div className="text-sm text-dark-400">
                  Page {currentPage} of {totalPages}
                </div>
                
                <div className="flex items-center gap-1">
                  {/* Previous Button */}
                  <Button
                    onClick={goToPrevious}
                    disabled={currentPage === 1}
                    variant="ghost"
                    size="sm"
                  >
                    ← Previous
                  </Button>
                  
                  {/* Page Numbers */}
                  {getPageNumbers().map((page, index) => (
                    <div key={index}>
                      {page === '...' ? (
                        <span className="px-2 py-1 text-dark-400">...</span>
                      ) : (
                        <Button
                          onClick={() => goToPage(page as number)}
                          variant={currentPage === page ? "primary" : "ghost"}
                          size="sm"
                          className="min-w-[2.5rem]"
                        >
                          {page}
                        </Button>
                      )}
                    </div>
                  ))}
                  
                  {/* Next Button */}
                  <Button
                    onClick={goToNext}
                    disabled={currentPage === totalPages}
                    variant="ghost"
                    size="sm"
                  >
                    Next →
                  </Button>
                </div>
                
                <div className="text-sm text-dark-400">
                  {videos.length} total videos
                </div>
              </div>
            )}
          </div>
        )}
      </Card>

      {/* Performance Tips */}
      {videos.length > 0 && (
        <Card>
          <h3 className="text-lg font-semibold mb-4">Performance Insights</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-blue-900/20 rounded-lg border border-blue-500/30">
              <h4 className="font-semibold text-blue-400 mb-2">📊 Analytics Summary</h4>
              <p className="text-sm text-dark-300">
                {videos.length} videos loaded from YouTube Data API with real view counts, likes, and comments
              </p>
            </div>
            <div className="p-4 bg-purple-900/20 rounded-lg border border-purple-500/30">
              <h4 className="font-semibold text-purple-400 mb-2">🎯 Top Performer</h4>
              <p className="text-sm text-dark-300">
                {videos.length > 0 
                  ? `"${videos.sort((a, b) => b.views - a.views)[0]?.title.substring(0, 30)}..." - ${formatNumber(videos.sort((a, b) => b.views - a.views)[0]?.views || 0)} views`
                  : 'No videos found'
                }
              </p>
            </div>
          </div>
        </Card>
      )}
    </div>
  )
}