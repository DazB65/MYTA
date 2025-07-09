import { useState, useEffect } from 'react'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'
import { formatNumber } from '@/utils'

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
}

export default function Videos() {
  const [videos, setVideos] = useState<VideoData[]>([])
  const [sortBy, setSortBy] = useState<'views' | 'ctr' | 'retention' | 'date'>('date')

  // Sample video data for demo
  const sampleVideos: VideoData[] = [
    {
      id: '1',
      title: 'How to Start Your First Project - Complete Guide',
      views: 15420,
      likes: 892,
      comments: 156,
      ctr: 8.2,
      retention: 68.5,
      publishedAt: '2024-01-15',
      thumbnail: '/assets/images/video-thumb-1.jpg',
      duration: '12:34'
    },
    {
      id: '2',
      title: 'Top 10 Mistakes Beginners Make',
      views: 23890,
      likes: 1205,
      comments: 234,
      ctr: 12.1,
      retention: 71.2,
      publishedAt: '2024-01-12',
      thumbnail: '/assets/images/video-thumb-2.jpg',
      duration: '15:22'
    },
    {
      id: '3',
      title: 'Advanced Techniques You Need to Know',
      views: 8760,
      likes: 445,
      comments: 89,
      ctr: 6.8,
      retention: 62.3,
      publishedAt: '2024-01-08',
      thumbnail: '/assets/images/video-thumb-3.jpg',
      duration: '18:45'
    }
  ]

  useEffect(() => {
    setVideos(sampleVideos)
  }, [])

  const sortedVideos = [...videos].sort((a, b) => {
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
          <h3 className="text-xl font-semibold">Recent Videos</h3>
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

        {videos.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📺</div>
            <h3 className="text-lg font-semibold mb-2">No videos yet</h3>
            <p className="text-dark-400">
              Connect your YouTube channel to see video analytics.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {sortedVideos.map((video) => (
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
                      {video.ctr}%
                    </div>
                    <div className="text-xs text-dark-400">CTR</div>
                  </div>
                  <div>
                    <div className={`text-sm font-semibold ${getPerformanceColor(video.retention, 'retention')}`}>
                      {video.retention}%
                    </div>
                    <div className="text-xs text-dark-400">Retention</div>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center gap-2">
                  <Button variant="secondary" size="sm">
                    📈 Details
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Performance Tips */}
      <Card>
        <h3 className="text-lg font-semibold mb-4">Performance Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-green-900/20 rounded-lg border border-green-500/30">
            <h4 className="font-semibold text-green-400 mb-2">🎯 Best Performing</h4>
            <p className="text-sm text-dark-300">
              Your "Top 10 Mistakes" video has the highest CTR at 12.1% - consider creating more list-style content.
            </p>
          </div>
          <div className="p-4 bg-yellow-900/20 rounded-lg border border-yellow-500/30">
            <h4 className="font-semibold text-yellow-400 mb-2">⚡ Optimization Tip</h4>
            <p className="text-sm text-dark-300">
              Retention drops around the 8-minute mark - try adding hooks or changing pace at that point.
            </p>
          </div>
        </div>
      </Card>
    </div>
  )
}