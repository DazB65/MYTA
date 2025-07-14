import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import BaseWidget from './BaseWidget'

interface ChannelHealthData {
  overall_score: number // 0-100
  grade: string // A+ to F
  trend: 'up' | 'down' | 'stable'
  subscriber_growth: number
  engagement_rate: number
  upload_consistency: number
  insights: string[]
  last_updated: string
}

interface ChannelHealthWidgetProps {
  data?: ChannelHealthData
  loading?: boolean
}

import { getGradeColor, getScoreColor } from '@/utils/colors'

export default function ChannelHealthWidget({ data, loading }: ChannelHealthWidgetProps) {
  const healthData = data

  const getTrendIcon = () => {
    if (!healthData) return <Minus className="w-5 h-5 text-gray-400" />
    
    switch (healthData.trend) {
      case 'up':
        return <TrendingUp className="w-5 h-5 text-green-400" />
      case 'down':
        return <TrendingDown className="w-5 h-5 text-red-400" />
      default:
        return <Minus className="w-5 h-5 text-gray-400" />
    }
  }

  return (
    <BaseWidget
      title="Channel Health Score"
      loading={loading}
      error={!data && !loading ? "Connect your YouTube account to view analytics" : undefined}
      height="h-[520px]"
      className="p-6"
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold text-white">Channel Health Score</h3>
        {getTrendIcon()}
      </div>

      {/* Main Score Circle */}
      <div className="flex items-center justify-center mb-6">
        <div className="relative">
          {/* Background circle */}
          <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 36 36">
            <path
              className="stroke-gray-700"
              strokeWidth="3"
              fill="none"
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            {/* Progress circle */}
            <path
              className={`stroke-current ${getScoreColor(healthData?.overall_score || 0)}`}
              strokeWidth="3"
              strokeLinecap="round"
              fill="none"
              strokeDasharray={`${healthData?.overall_score || 0}, 100`}
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
            />
          </svg>
          
          {/* Score text in center */}
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className={`text-3xl font-bold ${getScoreColor(healthData?.overall_score || 0)}`}>
              {healthData?.overall_score || 0}
            </span>
            <span className={`text-2xl font-bold ${getGradeColor(healthData?.grade || 'N/A')}`}>
              {healthData?.grade || 'N/A'}
            </span>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="text-center">
          <div className="text-sm text-gray-400">Growth</div>
          <div className="text-lg font-semibold text-green-400">+{healthData?.subscriber_growth?.toFixed(1) || '0.0'}%</div>
        </div>
        <div className="text-center">
          <div className="text-sm text-gray-400">Engagement</div>
          <div className="text-lg font-semibold text-blue-400">{healthData?.engagement_rate?.toFixed(1) || '0.0'}%</div>
        </div>
        <div className="text-center">
          <div className="text-sm text-gray-400">Consistency</div>
          <div className="text-lg font-semibold text-purple-400">{healthData?.upload_consistency || 0}%</div>
        </div>
      </div>

      {/* Key Insights */}
      <div className="space-y-2">
        <h4 className="font-medium text-white mb-3">Key Insights</h4>
        {healthData?.insights?.slice(0, 2).map((insight, index) => (
          <div key={index} className="flex items-start gap-2 text-sm">
            <span className="text-yellow-400 mt-1">•</span>
            <span className="text-gray-300">{insight}</span>
          </div>
        )) || (
          <div className="text-sm text-gray-400 italic">No insights available</div>
        )}
      </div>

      {/* Last Updated */}
      <div className="mt-4 pt-4 border-t border-gray-700">
        <span className="text-xs text-gray-500">
          Updated {healthData?.last_updated ? new Date(healthData.last_updated).toLocaleDateString() : 'Never'}
        </span>
      </div>
    </BaseWidget>
  )
}