import { Play, Eye, ThumbsUp, MessageCircle, TrendingUp, Clock } from 'lucide-react'
import BaseWidget from './BaseWidget'

interface VideoPerformance {
  id: string
  title: string
  views: number
  likes: number
  comments: number
  retention: number
  published_days_ago: number
  thumbnail: string
  performance_score: number // 0-100
}

interface ContentAnalysis {
  upload_consistency: number
  avg_performance: number
  trending_topics: string[]
  best_performing_format: string
  optimal_upload_time: string
}

interface ContentPerformanceData {
  top_videos: VideoPerformance[]
  content_analysis: ContentAnalysis
  last_updated: string
}

interface ContentPerformanceWidgetProps {
  data?: ContentPerformanceData
  loading?: boolean
}

import { formatNumber } from '@/utils/format'
import { getScoreColor } from '@/utils/colors'

export default function ContentPerformanceWidget({ data, loading }: ContentPerformanceWidgetProps) {
  const contentData = data

  return (
    <BaseWidget
      title="Content Performance"
      loading={loading}
      error={!data && !loading ? "Upload videos to view performance metrics" : undefined}
      height="h-[720px]"
      className="p-6"
    >
      <div className="flex items-center gap-3 mb-6">
        <Play className="w-6 h-6 text-red-400" />
        <h3 className="text-xl font-semibold text-white">Content Performance</h3>
      </div>

      {/* Top Performing Videos */}
      <div className="mb-6">
        <h4 className="font-medium text-white mb-4">Top Videos (Last 30 Days)</h4>
        <div className="space-y-3">
          {contentData?.top_videos?.map((video, index) => (
            <div key={video.id} className="flex items-center gap-3 p-3 bg-gray-800/50 rounded-lg">
              {/* Rank */}
              <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                index === 0 ? 'bg-yellow-500 text-black' :
                index === 1 ? 'bg-gray-400 text-black' :
                'bg-orange-600 text-white'
              }`}>
                {index + 1}
              </div>

              {/* Thumbnail placeholder */}
              <div className="w-20 h-12 bg-gray-700 rounded flex items-center justify-center flex-shrink-0">
                <Play className="w-4 h-4 text-gray-400" />
              </div>

              {/* Video info */}
              <div className="flex-1 min-w-0">
                <div className="font-medium text-white text-sm truncate mb-1">
                  {video.title}
                </div>
                <div className="flex items-center gap-4 text-xs text-gray-400">
                  <div className="flex items-center gap-1">
                    <Eye className="w-3 h-3" />
                    {formatNumber(video.views)}
                  </div>
                  <div className="flex items-center gap-1">
                    <ThumbsUp className="w-3 h-3" />
                    {formatNumber(video.likes)}
                  </div>
                  <div className="flex items-center gap-1">
                    <MessageCircle className="w-3 h-3" />
                    {video.comments}
                  </div>
                </div>
              </div>

              {/* Performance score */}
              <div className="text-right">
                <div className={`text-lg font-bold ${getScoreColor(video.performance_score)}`}>
                  {video.performance_score}
                </div>
                <div className="text-xs text-gray-400">{video.retention}% retention</div>
              </div>
            </div>
          )) || (
            <div className="text-center text-gray-400 py-4">No video data available</div>
          )}
        </div>
      </div>

      {/* Content Analysis */}
      <div className="space-y-4">
        <h4 className="font-medium text-white">Content Insights</h4>
        
        {/* Metrics Grid */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-800/50 rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <Clock className="w-4 h-4 text-blue-400" />
              <span className="text-sm text-gray-400">Consistency</span>
            </div>
            <div className="text-lg font-bold text-blue-400">
              {contentData?.content_analysis?.upload_consistency || 0}%
            </div>
          </div>
          
          <div className="bg-gray-800/50 rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <TrendingUp className="w-4 h-4 text-green-400" />
              <span className="text-sm text-gray-400">Avg Performance</span>
            </div>
            <div className="text-lg font-bold text-green-400">
              {(contentData?.content_analysis?.avg_performance || 0).toFixed(1)}
            </div>
          </div>
        </div>

        {/* Trending Topics */}
        <div>
          <div className="text-sm text-gray-400 mb-2">Trending Topics</div>
          <div className="flex flex-wrap gap-2">
            {contentData?.content_analysis?.trending_topics?.map((topic, index) => (
              <span 
                key={index}
                className="px-2 py-1 bg-purple-900/30 text-purple-300 rounded-full text-xs"
              >
                {topic}
              </span>
            )) || (
              <span className="text-sm text-gray-400 italic">No trending topics available</span>
            )}
          </div>
        </div>

        {/* Quick Insights */}
        <div className="bg-gradient-to-r from-blue-900/20 to-purple-900/20 rounded-lg p-3">
          <div className="text-sm text-gray-300 space-y-1">
            <div>🎯 Best format: <span className="text-blue-400">{contentData?.content_analysis?.best_performing_format || 'Not available'}</span></div>
            <div>⏰ Optimal time: <span className="text-green-400">{contentData?.content_analysis?.optimal_upload_time || 'Not available'}</span></div>
          </div>
        </div>
      </div>

      {/* Last Updated */}
      <div className="mt-4 pt-4 border-t border-gray-700">
        <span className="text-xs text-gray-500">
          Updated {contentData?.last_updated ? new Date(contentData.last_updated).toLocaleDateString() : 'Never'}
        </span>
      </div>
    </BaseWidget>
  )
}