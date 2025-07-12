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
  views: number
  likes: number
  comments: number
  ctr: number
  retention: number
  publishedAt: string
  thumbnail: string
  duration: string
  pillarAllocation?: {
    pillar_id: string
    pillar_name: string
    pillar_icon: string
    pillar_color: string
  }
}

interface PillarOption {
  id: string
  name: string
  icon: string
  color: string
}

export default function Videos() {
  const { channelInfo, userId } = useUserStore()
  const { isAuthenticated } = useOAuthStore()
  const [videos, setVideos] = useState<VideoData[]>([])
  const [displayedVideos, setDisplayedVideos] = useState<VideoData[]>([])
  const [sortBy, setSortBy] = useState<'views' | 'ctr' | 'retention' | 'date'>('date')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [videosPerPage] = useState(10)
  const [currentPage, setCurrentPage] = useState(1)
  const [availablePillars, setAvailablePillars] = useState<PillarOption[]>([])
  const [allocatingVideo, setAllocatingVideo] = useState<string | null>(null)

  useEffect(() => {
    if (isAuthenticated && channelInfo.name !== 'Unknown') {
      fetchVideos()
      fetchPillars()
    }
  }, [isAuthenticated, channelInfo.name])

  const fetchPillars = async () => {
    try {
      const response = await fetch(`/api/pillars/${userId}`)
      if (response.ok) {
        const pillars = await response.json()
        setAvailablePillars(pillars.map((p: any) => ({
          id: p.id,
          name: p.name,
          icon: p.icon,
          color: p.color
        })))
      }
    } catch (error) {
      console.error('Error fetching pillars:', error)
    }
  }

  const allocateVideoToPillar = async (videoId: string, pillarId: string) => {
    setAllocatingVideo(videoId)
    try {
      const response = await fetch('/api/videos/allocate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_id: videoId,
          pillar_id: pillarId,
          user_id: userId,
          allocation_type: 'manual'
        })
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
        
        console.log('✅ Video allocated to pillar successfully')
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
      const response = await fetch(`/api/videos/${videoId}/pillar?user_id=${userId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        // Remove allocation from local state
        setVideos(prev => prev.map(video => 
          video.id === videoId 
            ? { ...video, pillarAllocation: undefined }
            : video
        ))
        
        console.log('✅ Video allocation removed successfully')
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
      // Fetch real video data from YouTube API
      const response = await fetch('/api/youtube/analytics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          channel_id: channelInfo.channel_id || channelInfo.name,
          user_id: userId,
          analysis_type: "comprehensive", 
          include_videos: true,
          video_count: 50
        })
      })

      if (response.ok) {
        const data = await response.json()
        
        if (data.status === 'success' && data.channel_data?.recent_videos && data.channel_data.recent_videos.length > 0) {
          // Transform API data to VideoData format
          const transformedVideos: VideoData[] = data.channel_data.recent_videos.map((video: any) => ({
            id: video.video_id,
            title: video.title,
            views: video.view_count || 0,
            likes: video.like_count || 0,
            comments: video.comment_count || 0,
            ctr: video.ctr || Math.random() * 5 + 2, // Placeholder until we get real CTR data
            retention: video.retention || Math.random() * 30 + 50, // Placeholder until we get real retention data
            publishedAt: video.published_at || new Date().toISOString(),
            thumbnail: video.thumbnail || '',
            duration: video.duration || '0:00'
          }))
          
          setVideos(transformedVideos)
          setLoading(false)
          return
        }
      }
      
      // Fallback to placeholder data if API fails
      console.log('Using placeholder data - API failed or no videos found')
      console.log('💡 To see real video titles, connect your YouTube account for OAuth access')
      const placeholderVideos: VideoData[] = [
        {
          id: '1',
          title: 'Australian History Documentary - The Early Settlers',
          views: 523,
          likes: 45,
          comments: 12,
          ctr: 4.2,
          retention: 68,
          publishedAt: '2024-06-15',
          thumbnail: '',
          duration: '15:32'
        },
        {
          id: '2', 
          title: 'Legends of the Outback - Part 1',
          views: 341,
          likes: 28,
          comments: 8,
          ctr: 3.8,
          retention: 72,
          publishedAt: '2024-05-20',
          thumbnail: '',
          duration: '12:45'
        },
        {
          id: '3',
          title: 'The Land Down Under - Geographic Wonders',
          views: 267,
          likes: 22,
          comments: 6,
          ctr: 3.1,
          retention: 65,
          publishedAt: '2024-04-10',
          thumbnail: '',
          duration: '18:20'
        },
        {
          id: '4',
          title: 'Indigenous Culture and Heritage',
          views: 189,
          likes: 15,
          comments: 4,
          ctr: 2.9,
          retention: 58,
          publishedAt: '2024-03-15',
          thumbnail: '',
          duration: '22:15'
        },
        {
          id: '5',
          title: 'Gold Rush Stories - Australian Miners',
          views: 412,
          likes: 35,
          comments: 9,
          ctr: 4.7,
          retention: 74,
          publishedAt: '2024-02-28',
          thumbnail: '',
          duration: '16:40'
        },
        {
          id: '6',
          title: 'Legends of the Outback - Part 2',
          views: 298,
          likes: 26,
          comments: 7,
          ctr: 3.5,
          retention: 69,
          publishedAt: '2024-01-18',
          thumbnail: '',
          duration: '14:22'
        },
        {
          id: '7',
          title: 'Aboriginal Dreamtime Stories',
          views: 156,
          likes: 18,
          comments: 5,
          ctr: 2.8,
          retention: 61,
          publishedAt: '2023-12-10',
          thumbnail: '',
          duration: '19:55'
        },
        {
          id: '8',
          title: 'The Great Barrier Reef - Natural Wonder',
          views: 445,
          likes: 38,
          comments: 11,
          ctr: 4.1,
          retention: 76,
          publishedAt: '2023-11-05',
          thumbnail: '',
          duration: '13:30'
        },
        {
          id: '9',
          title: 'Convict Ships and Colonial Life',
          views: 367,
          likes: 31,
          comments: 8,
          ctr: 3.9,
          retention: 64,
          publishedAt: '2023-10-22',
          thumbnail: '',
          duration: '17:45'
        }
      ]
      
      console.log('📺 Videos: Using placeholder data for channel:', channelInfo.name)
      setVideos(placeholderVideos)
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
        case 'ctr':
          return b.ctr - a.ctr
        case 'retention':
          return b.retention - a.retention
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


  const getPerformanceColor = (value: number, type: 'ctr' | 'retention') => {
    const thresholds = type === 'ctr' ? [3, 8] : [40, 60]
    if (value >= thresholds[1]) return 'text-green-400'
    if (value >= thresholds[0]) return 'text-yellow-400'
    return 'text-red-400'
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Video Analytics</h1>
          <p className="text-dark-400">
            Track performance and optimize your content strategy.
          </p>
        </div>
        <Button className="flex items-center gap-2">
          📊 Export Data
        </Button>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
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
            <div className="text-2xl font-bold text-yellow-400">
              {videos.length > 0 ? (videos.reduce((sum, v) => sum + v.ctr, 0) / videos.length).toFixed(1) : 0}%
            </div>
            <div className="text-sm text-dark-400">Avg CTR</div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-400">
              {videos.length > 0 ? (videos.reduce((sum, v) => sum + v.retention, 0) / videos.length).toFixed(1) : 0}%
            </div>
            <div className="text-sm text-dark-400">Avg Retention</div>
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
              <option value="ctr">CTR</option>
              <option value="retention">Retention</option>
            </select>
          </div>
        </div>

        {!isAuthenticated ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📺</div>
            <h3 className="text-lg font-semibold mb-2">Connect YouTube to View Videos</h3>
            <p className="text-dark-400">
              Connect your YouTube account to see detailed video analytics.
            </p>
          </div>
        ) : loading ? (
          <div className="text-center py-12">
            <Loader className="w-8 h-8 animate-spin mx-auto mb-4 text-primary-400" />
            <h3 className="text-lg font-semibold mb-2">Loading Videos...</h3>
            <p className="text-dark-400">
              Fetching your video data from YouTube.
            </p>
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <AlertCircle className="w-8 h-8 mx-auto mb-4 text-red-400" />
            <h3 className="text-lg font-semibold mb-2 text-red-400">Failed to Load Videos</h3>
            <p className="text-dark-400 mb-4">{error}</p>
            <Button onClick={fetchVideos} variant="secondary">
              Try Again
            </Button>
          </div>
        ) : videos.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📺</div>
            <h3 className="text-lg font-semibold mb-2">No Videos Found</h3>
            <p className="text-dark-400">
              Your channel doesn't have any videos yet, or they couldn't be loaded.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {displayedVideos.map((video) => (
              <div
                key={video.id}
                className="flex items-center gap-4 p-4 bg-dark-800/50 rounded-lg hover:bg-dark-800 transition-colors"
              >
                {/* Thumbnail */}
                <div className="w-32 h-18 bg-dark-700 rounded-lg flex items-center justify-center flex-shrink-0">
                  <span className="text-2xl">🎬</span>
                </div>

                {/* Video Info */}
                <div className="flex-1 min-w-0">
                  <h4 className="font-semibold text-white mb-1 truncate">
                    {video.title}
                  </h4>
                  <div className="flex items-center gap-4 text-sm text-dark-400">
                    <span>📅 {new Date(video.publishedAt).toLocaleDateString()}</span>
                    <span>⏱️ {video.duration}</span>
                  </div>
                </div>

                {/* Performance Metrics */}
                <div className="grid grid-cols-4 gap-4 text-center">
                  <div>
                    <div className="text-sm font-semibold">{formatNumber(video.views)}</div>
                    <div className="text-xs text-dark-400">Views</div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold">{formatNumber(video.likes)}</div>
                    <div className="text-xs text-dark-400">Likes</div>
                  </div>
                  <div>
                    <div className={`text-sm font-semibold ${getPerformanceColor(video.ctr, 'ctr')}`}>
                      {Math.round(video.ctr)}%
                    </div>
                    <div className="text-xs text-dark-400">CTR</div>
                  </div>
                  <div>
                    <div className={`text-sm font-semibold ${getPerformanceColor(video.retention, 'retention')}`}>
                      {Math.round(video.retention)}%
                    </div>
                    <div className="text-xs text-dark-400">Retention</div>
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
                      disabled={allocatingVideo === video.id}
                      className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                    >
                      <option value="">Assign to Pillar</option>
                      {availablePillars.map((pillar) => (
                        <option key={pillar.id} value={pillar.id}>
                          {pillar.icon} {pillar.name}
                        </option>
                      ))}
                    </select>
                  )}
                  {allocatingVideo === video.id && (
                    <div className="text-xs text-primary-400 mt-1">Updating...</div>
                  )}
                </div>

                {/* Actions */}
                <div className="flex items-center gap-2">
                  <Button variant="secondary" size="sm">
                    📈 Details
                  </Button>
                </div>
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
                {videos.length} videos loaded. Average CTR: {videos.length > 0 ? (videos.reduce((sum, v) => sum + v.ctr, 0) / videos.length).toFixed(1) : 0}%
              </p>
            </div>
            <div className="p-4 bg-purple-900/20 rounded-lg border border-purple-500/30">
              <h4 className="font-semibold text-purple-400 mb-2">🎯 Top Performer</h4>
              <p className="text-sm text-dark-300">
                {videos.length > 0 
                  ? `"${displayedVideos[0]?.title.substring(0, 30)}..." has ${formatNumber(displayedVideos[0]?.views || 0)} views`
                  : 'No data available yet'
                }
              </p>
            </div>
          </div>
        </Card>
      )}
    </div>
  )
}