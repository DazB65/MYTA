import { DollarSign, TrendingUp, TrendingDown, Eye, Target } from 'lucide-react'
import Card from '@/components/common/Card'

interface RevenueData {
  monthly_earnings: number
  monthly_change: number // percentage change
  rpm: number // Revenue per mille
  cpm: number // Cost per mille
  projected_annual: number
  revenue_sources: {
    ads: number
    memberships: number
    super_chat: number
    other: number
  }
  last_updated: string
}

interface RevenueDashboardWidgetProps {
  data?: RevenueData
  loading?: boolean
}

const formatCurrency = (amount: number): string => {
  if (amount >= 1000000) {
    return `$${(amount / 1000000).toFixed(1)}M`
  } else if (amount >= 1000) {
    return `$${(amount / 1000).toFixed(1)}K`
  }
  return `$${amount.toFixed(2)}`
}

export default function RevenueDashboardWidget({ data, loading }: RevenueDashboardWidgetProps) {
  if (!data && !loading) {
    return (
      <Card className="p-6">
        <div className="text-center py-8 text-gray-400">
          <DollarSign className="w-12 h-12 mx-auto mb-3 opacity-50" />
          <h3 className="text-xl font-semibold text-white mb-2">Revenue Dashboard</h3>
          <p>No revenue data available</p>
          <p className="text-sm">Connect monetized YouTube account to view earnings</p>
        </div>
      </Card>
    )
  }

  const revenueData = data

  const getChangeColor = (change: number): string => {
    return change >= 0 ? 'text-green-400' : 'text-red-400'
  }

  const getChangeIcon = (change: number) => {
    return change >= 0 ? 
      <TrendingUp className="w-4 h-4 text-green-400" /> : 
      <TrendingDown className="w-4 h-4 text-red-400" />
  }

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
        <DollarSign className="w-6 h-6 text-green-400" />
        <h3 className="text-xl font-semibold text-white">Revenue Dashboard</h3>
      </div>

      {/* Main Revenue Display */}
      <div className="mb-6">
        <div className="flex items-baseline gap-3 mb-2">
          <span className="text-3xl font-bold text-green-400">
            {formatCurrency(revenueData?.monthly_earnings || 0)}
          </span>
          <span className="text-gray-400">this month</span>
        </div>
        
        <div className="flex items-center gap-2">
          {getChangeIcon(revenueData?.monthly_change || 0)}
          <span className={`text-sm font-medium ${getChangeColor(revenueData?.monthly_change || 0)}`}>
            {(revenueData?.monthly_change || 0) >= 0 ? '+' : ''}{(revenueData?.monthly_change || 0).toFixed(1)}% vs last month
          </span>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-gray-800/50 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <Eye className="w-4 h-4 text-blue-400" />
            <span className="text-sm text-gray-400">RPM</span>
          </div>
          <div className="text-xl font-bold text-blue-400">${(revenueData?.rpm || 0).toFixed(2)}</div>
        </div>
        
        <div className="bg-gray-800/50 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <Target className="w-4 h-4 text-purple-400" />
            <span className="text-sm text-gray-400">CPM</span>
          </div>
          <div className="text-xl font-bold text-purple-400">${(revenueData?.cpm || 0).toFixed(2)}</div>
        </div>
      </div>

      {/* Projected Annual */}
      <div className="bg-gradient-to-r from-green-900/30 to-blue-900/30 rounded-lg p-4 mb-6">
        <div className="text-sm text-gray-400 mb-1">Projected Annual Revenue</div>
        <div className="text-2xl font-bold text-green-400">
          {formatCurrency(revenueData?.projected_annual || 0)}
        </div>
        <div className="text-xs text-gray-500 mt-1">
          Based on current 3-month trend
        </div>
      </div>

      {/* Revenue Sources */}
      <div>
        <h4 className="font-medium text-white mb-3">Revenue Sources</h4>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-green-400 rounded-full"></div>
              <span className="text-sm text-gray-300">Ad Revenue</span>
            </div>
            <span className="text-sm font-medium text-white">{(revenueData?.revenue_sources?.ads || 0).toFixed(1)}%</span>
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-blue-400 rounded-full"></div>
              <span className="text-sm text-gray-300">Memberships</span>
            </div>
            <span className="text-sm font-medium text-white">{(revenueData?.revenue_sources?.memberships || 0).toFixed(1)}%</span>
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-purple-400 rounded-full"></div>
              <span className="text-sm text-gray-300">Super Chat</span>
            </div>
            <span className="text-sm font-medium text-white">{(revenueData?.revenue_sources?.super_chat || 0).toFixed(1)}%</span>
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-orange-400 rounded-full"></div>
              <span className="text-sm text-gray-300">Other</span>
            </div>
            <span className="text-sm font-medium text-white">{(revenueData?.revenue_sources?.other || 0).toFixed(1)}%</span>
          </div>
        </div>
      </div>

      {/* Last Updated */}
      <div className="mt-4 pt-4 border-t border-gray-700">
        <span className="text-xs text-gray-500">
          Updated {revenueData?.last_updated ? new Date(revenueData.last_updated).toLocaleDateString() : 'Never'}
        </span>
      </div>
    </Card>
  )
}