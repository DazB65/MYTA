import { useState } from 'react'
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer } from 'recharts'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'
import { MoreHorizontal, TrendingUp, TrendingDown } from 'lucide-react'

interface PillarData {
  id: string
  name: string
  icon: string
  color: string
  videos: number
  views: number
  watchTime: number
  revenue: number
  viewsChange: number
  watchTimeChange: number
  revenueChange: number
  createdAgo: string
  chartData: Array<{ month: string; value: number }>
  tags: string[]
  topPerformingContent: string
  insight: string
}

const mockPillarsData: PillarData[] = [
  {
    id: 'game-development',
    name: 'Game Development',
    icon: '🎮',
    color: 'from-blue-500 to-cyan-400',
    videos: 12,
    views: 248300,
    watchTime: 14.2,
    revenue: 3842,
    viewsChange: -3.5,
    watchTimeChange: -2.1,
    revenueChange: -6.8,
    createdAgo: '4 months ago',
    chartData: [
      { month: 'Feb', value: 180000 },
      { month: 'Mar', value: 220000 },
      { month: 'Apr', value: 235000 },
      { month: 'May', value: 248000 },
      { month: 'Jun', value: 248300 }
    ],
    tags: ['Unity', 'C#', 'Indie Games', 'Tutorials'],
    topPerformingContent: 'Top performing content pillar',
    insight: 'Strong technical content with consistent growth'
  },
  {
    id: 'game-reviews',
    name: 'Game Reviews',
    icon: '⭐',
    color: 'from-purple-500 to-pink-400',
    videos: 8,
    views: 166700,
    watchTime: 8.6,
    revenue: 2156,
    viewsChange: -6.4,
    watchTimeChange: -3.2,
    revenueChange: -1.1,
    createdAgo: '3 months ago',
    chartData: [
      { month: 'Feb', value: 120000 },
      { month: 'Mar', value: 140000 },
      { month: 'Apr', value: 155000 },
      { month: 'May', value: 162000 },
      { month: 'Jun', value: 166700 }
    ],
    tags: ['Reviews', 'AAA Games', 'Indie', 'First Impressions'],
    topPerformingContent: 'Consistent growth in audience retention',
    insight: 'High engagement from loyal audience base'
  },
  {
    id: 'gaming-tips',
    name: 'Gaming Tips',
    icon: '💡',
    color: 'from-orange-500 to-yellow-400',
    videos: 15,
    views: 203500,
    watchTime: 10.1,
    revenue: 2937,
    viewsChange: -1.7,
    watchTimeChange: -8.5,
    revenueChange: -6.5,
    createdAgo: '5 months ago',
    chartData: [
      { month: 'Feb', value: 150000 },
      { month: 'Mar', value: 175000 },
      { month: 'Apr', value: 190000 },
      { month: 'May', value: 200000 },
      { month: 'Jun', value: 203500 }
    ],
    tags: ['Tips & Tricks', 'Strategy', 'Guides', 'Competitive'],
    topPerformingContent: 'High engagement from returning viewers',
    insight: 'Educational content with strong retention'
  },
  {
    id: 'gaming-news',
    name: 'Gaming News',
    icon: '📰',
    color: 'from-red-500 to-pink-400',
    videos: 6,
    views: 97200,
    watchTime: 4.3,
    revenue: 843,
    viewsChange: -3.6,
    watchTimeChange: -5.2,
    revenueChange: -3.5,
    createdAgo: '2 months ago',
    chartData: [
      { month: 'Feb', value: 85000 },
      { month: 'Mar', value: 110000 },
      { month: 'Apr', value: 102000 },
      { month: 'May', value: 95000 },
      { month: 'Jun', value: 97200 }
    ],
    tags: ['Industry News', 'Updates', 'Releases', 'Events'],
    topPerformingContent: 'Needs improvement in content strategy',
    insight: 'Trending content requires timely coverage'
  }
]

function PillarCard({ pillar }: { pillar: PillarData }) {
  const formatViews = (views: number) => {
    if (views >= 1000000) return `${(views / 1000000).toFixed(1)}M`
    if (views >= 1000) return `${(views / 1000).toFixed(1)}K`
    return views.toString()
  }

  const formatWatchTime = (hours: number) => {
    if (hours >= 1000) return `${(hours / 1000).toFixed(1)}K hrs`
    return `${hours}K hrs`
  }

  const formatRevenue = (revenue: number) => {
    return `$${revenue.toLocaleString()}`
  }

  const getChangeIcon = (change: number) => {
    if (change > 0) return <TrendingUp className="w-3 h-3 text-green-400" />
    return <TrendingDown className="w-3 h-3 text-red-400" />
  }

  const getChangeColor = (change: number) => {
    return change > 0 ? 'text-green-400' : 'text-red-400'
  }

  return (
    <Card className="p-6 bg-dark-900 border-dark-700">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${pillar.color} flex items-center justify-center text-lg`}>
            {pillar.icon}
          </div>
          <div>
            <h3 className="font-semibold text-white">{pillar.name}</h3>
            <p className="text-sm text-dark-400">{pillar.videos} videos • Created {pillar.createdAgo}</p>
          </div>
        </div>
        <button className="p-1 text-dark-400 hover:text-white">
          <MoreHorizontal className="w-4 h-4" />
        </button>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-6">
        <div>
          <div className="text-sm text-dark-400 mb-1">Views</div>
          <div className="text-xl font-bold text-white">{formatViews(pillar.views)}</div>
          <div className={`text-xs flex items-center gap-1 ${getChangeColor(pillar.viewsChange)}`}>
            {getChangeIcon(pillar.viewsChange)}
            {Math.abs(pillar.viewsChange).toFixed(1)}%
          </div>
        </div>
        <div>
          <div className="text-sm text-dark-400 mb-1">Watch Time</div>
          <div className="text-xl font-bold text-white">{formatWatchTime(pillar.watchTime)}</div>
          <div className={`text-xs flex items-center gap-1 ${getChangeColor(pillar.watchTimeChange)}`}>
            {getChangeIcon(pillar.watchTimeChange)}
            {Math.abs(pillar.watchTimeChange).toFixed(1)}%
          </div>
        </div>
        <div>
          <div className="text-sm text-dark-400 mb-1">Revenue</div>
          <div className="text-xl font-bold text-white">{formatRevenue(pillar.revenue)}</div>
          <div className={`text-xs flex items-center gap-1 ${getChangeColor(pillar.revenueChange)}`}>
            {getChangeIcon(pillar.revenueChange)}
            {Math.abs(pillar.revenueChange).toFixed(1)}%
          </div>
        </div>
      </div>

      <div className="mb-6">
        <ResponsiveContainer width="100%" height={120}>
          <LineChart data={pillar.chartData}>
            <XAxis 
              dataKey="month" 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6B7280' }}
            />
            <YAxis hide />
            <Line 
              type="monotone" 
              dataKey="value" 
              stroke={pillar.color.includes('blue') ? '#3B82F6' : 
                     pillar.color.includes('purple') ? '#8B5CF6' :
                     pillar.color.includes('orange') ? '#F59E0B' : '#EF4444'}
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="flex flex-wrap gap-1 mb-4">
        {pillar.tags.map((tag) => (
          <span 
            key={tag} 
            className="px-2 py-1 text-xs bg-dark-800 text-dark-300 rounded"
          >
            {tag}
          </span>
        ))}
      </div>

      <div className="text-sm text-dark-400 mb-4">{pillar.topPerformingContent}</div>

      <div className="flex gap-2">
        <Button size="sm" className="flex-1">
          View Details
        </Button>
        <Button size="sm" variant="secondary">
          Create Content
        </Button>
      </div>
    </Card>
  )
}

export default function Pillars() {
  const [pillars] = useState<PillarData[]>(mockPillarsData)
  const [timeRange, setTimeRange] = useState('Last 30 days')

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Content Pillars</h1>
          <p className="text-dark-400">
            Analyze and optimize your content strategy
          </p>
        </div>
        <div className="flex items-center gap-3">
          <select 
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option>Last 30 days</option>
            <option>Last 60 days</option>
            <option>Last 90 days</option>
          </select>
          <Button>
            Add Pillar
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {pillars.map((pillar) => (
          <PillarCard key={pillar.id} pillar={pillar} />
        ))}
      </div>

      <Card className="p-6 bg-gradient-to-r from-purple-600/20 to-blue-600/20 border-purple-500/30">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
            🤖
          </div>
          <div>
            <h3 className="font-semibold text-white">AI Suggested: Metaverse Coverage</h3>
            <span className="text-xs bg-blue-500 text-white px-2 py-0.5 rounded">NEW</span>
          </div>
        </div>
        <p className="text-sm text-dark-300 mb-4">
          Based on trending topics and your audience interests, consider creating content about metaverse gaming platforms.
        </p>
        <Button size="sm" variant="secondary">
          Explore Suggestion
        </Button>
      </Card>
    </div>
  )
}