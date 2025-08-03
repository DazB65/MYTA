import { Users, TrendingUp, Target, Calendar } from 'lucide-react'
import Card from '@/components/common/Card'

interface SubscriberData {
  current_subscribers: number
  daily_gain: number
  weekly_gain: number
  growth_rate: number // percentage
  next_milestone: {
    target: number
    progress: number // percentage to milestone
    estimated_days: number
  }
  growth_velocity: Array<{
    date: string
    subscribers: number
  }>
  last_updated: string
}

interface SubscriberGrowthWidgetProps {
  data?: SubscriberData
  loading?: boolean
}

const formatNumber = (num: number): string => {
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1)}M`
  } else if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K`
  }
  return num.toLocaleString()
}


export default function SubscriberGrowthWidget({ data, loading }: SubscriberGrowthWidgetProps) {
  if (!data && !loading) {
    return (
      <Card className="p-6">
        <div className="text-center py-8 text-gray-400">
          <Users className="w-12 h-12 mx-auto mb-3 opacity-50" />
          <h3 className="text-xl font-semibold text-white mb-2">Subscriber Growth</h3>
          <p>No subscriber data available</p>
          <p className="text-sm">Connect your YouTube account to view growth metrics</p>
        </div>
      </Card>
    )
  }

  const subscriberData = data

  if (loading) {
    return (
      <Card className="p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-700 rounded mb-4"></div>
          <div className="h-12 bg-gray-700 rounded mb-4"></div>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="h-16 bg-gray-700 rounded"></div>
            <div className="h-16 bg-gray-700 rounded"></div>
          </div>
          <div className="h-20 bg-gray-700 rounded"></div>
        </div>
      </Card>
    )
  }

  return (
    <Card className="p-6">
      <div className="flex items-center gap-3 mb-6">
        <Users className="w-6 h-6 text-blue-400" />
        <h3 className="text-xl font-semibold text-white">Subscriber Growth</h3>
      </div>

      {/* Current Subscribers */}
      <div className="mb-6">
        <div className="text-3xl font-bold text-blue-400 mb-2">
          {formatNumber(subscriberData?.current_subscribers || 0)}
        </div>
        <div className="text-gray-400">Total Subscribers</div>
      </div>

      {/* Growth Metrics */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-gray-800/50 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <Calendar className="w-4 h-4 text-green-400" />
            <span className="text-sm text-gray-400">Daily</span>
          </div>
          <div className="text-xl font-bold text-green-400">+{subscriberData?.daily_gain || 0}</div>
        </div>
        
        <div className="bg-gray-800/50 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <TrendingUp className="w-4 h-4 text-purple-400" />
            <span className="text-sm text-gray-400">Weekly</span>
          </div>
          <div className="text-xl font-bold text-purple-400">+{subscriberData?.weekly_gain || 0}</div>
        </div>
      </div>

      {/* Growth Rate */}
      <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-lg p-4 mb-6">
        <div className="text-sm text-gray-400 mb-1">Growth Rate</div>
        <div className="text-2xl font-bold text-blue-400">
          {(subscriberData?.growth_rate || 0).toFixed(1)}%
        </div>
        <div className="text-xs text-gray-500 mt-1">
          Monthly average
        </div>
      </div>

      {/* Milestone Progress */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-3">
          <Target className="w-5 h-5 text-yellow-400" />
          <h4 className="font-medium text-white">Next Milestone</h4>
        </div>
        
        <div className="mb-3">
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-400">Progress to {formatNumber(subscriberData?.next_milestone?.target || 0)}</span>
            <span className="text-yellow-400">{(subscriberData?.next_milestone?.progress || 0).toFixed(1)}%</span>
          </div>
          
          {/* Progress bar */}
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-yellow-400 to-orange-400 h-2 rounded-full transition-all duration-300"
              style={{ width: `${subscriberData?.next_milestone?.progress || 0}%` }}
            ></div>
          </div>
        </div>
        
        <div className="text-sm text-gray-400">
          Estimated: {subscriberData?.next_milestone?.estimated_days || 0} days
        </div>
      </div>

      {/* Mini Growth Chart */}
      <div className="mb-4">
        <h4 className="font-medium text-white mb-3">7-Day Trend</h4>
        <div className="flex items-end gap-1 h-16">
          {subscriberData?.growth_velocity?.map((point, index) => {
            const minSubs = Math.min(...(subscriberData.growth_velocity?.map(p => p.subscribers) || [0]))
            const maxSubs = Math.max(...(subscriberData.growth_velocity?.map(p => p.subscribers) || [0]))
            const height = maxSubs > minSubs ? 
              ((point.subscribers - minSubs) / (maxSubs - minSubs)) * 60 + 8 : 8
            
            return (
              <div
                key={index}
                className="flex-1 bg-gradient-to-t from-blue-600 to-blue-400 rounded-t"
                style={{ height: `${height}px` }}
                title={`${new Date(point.date).toLocaleDateString()}: ${formatNumber(point.subscribers)}`}
              ></div>
            )
          }) || (
            <div className="flex-1 text-center text-gray-400 text-sm">No chart data available</div>
          )}
        </div>
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>7 days ago</span>
          <span>Today</span>
        </div>
      </div>

      {/* Last Updated */}
      <div className="pt-4 border-t border-gray-700">
        <span className="text-xs text-gray-500">
          Updated {subscriberData?.last_updated ? new Date(subscriberData.last_updated).toLocaleDateString() : 'Never'}
        </span>
      </div>
    </Card>
  )
}