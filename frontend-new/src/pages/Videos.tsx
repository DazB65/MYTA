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

export default function Videos() {
  const { channelInfo } = useUserStore()
  const { isAuthenticated } = useOAuthStore()
  
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

  useEffect(() => {
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
      // Fetch real video data from YouTube API
      const response = await fetch('/api/youtube/analytics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          channel_id: channelInfo.channel_id || channelInfo.name,
          user_id: actualUserId,
          analysis_type: "comprehensive", 
          include_videos: true,
          video_count: 50
        })
      })

      if (response.ok) {
        const data = await response.json()
        
        if (data.status === 'success' && data.channel_data?.recent_videos && data.channel_data.recent_videos.length > 0) {
          // Transform API data to VideoData format - only real data
          const transformedVideos: VideoData[] = data.channel_data.recent_videos.map((video: any) => ({
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

      {/* Real Video Stats */}
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

                {/* Real Video Metrics */}
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <div className="text-sm font-semibold">{formatNumber(video.views)}</div>
                    <div className="text-xs text-dark-400">Views</div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold">{formatNumber(video.likes)}</div>
                    <div className="text-xs text-dark-400">Likes</div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold">{formatNumber(video.comments)}</div>
                    <div className="text-xs text-dark-400">Comments</div>
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