import { useUserStore } from '@/store/userStore'
import { useAnalytics } from '@/hooks/useAnalytics'
import Card from '@/components/common/Card'
import TaskManager from '@/components/dashboard/TaskManager'
import ChannelGoals from '@/components/dashboard/ChannelGoals'
import { ChannelHealthWidget, RevenueDashboardWidget, SubscriberGrowthWidget, ContentPerformanceWidget, AlgorithmPerformanceWidget, CommunityHealthWidget } from '@/components/dashboard/widgets'
import { AlertCircle } from 'lucide-react'

export default function Dashboard() {
  const { channelInfo } = useUserStore()
  
  // TEMPORARY FIX: Force use default_user for consistency
  const actualUserId = "default_user"
  const { data: analyticsData, loading: analyticsLoading, error: analyticsError, refetch } = useAnalytics(actualUserId)

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">
            Welcome back, {channelInfo.name || 'Creator'}! 👋
          </h1>
          <p className="text-dark-400">
            Here's what's happening with your channel today
          </p>
        </div>
      </div>


      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Task Manager - Takes up 2 columns on large screens */}
        <div className="lg:col-span-2">
          <TaskManager />
        </div>

        {/* Right Sidebar - Quick Actions & Info */}
        <div className="space-y-6">
          {/* Channel Goals */}
          <ChannelGoals />
        </div>
      </div>

      {/* Analytics Error Display */}
      {analyticsError && (
        <Card className="p-4 border-red-500/30 bg-red-900/20">
          <div className="flex items-center gap-3 text-red-400">
            <AlertCircle className="w-5 h-5" />
            <div>
              <div className="font-medium">Analytics Unavailable</div>
              <div className="text-sm text-red-300">{analyticsError}</div>
            </div>
            <button 
              onClick={refetch}
              className="ml-auto px-3 py-1 bg-red-600 hover:bg-red-700 rounded text-sm"
            >
              Retry
            </button>
          </div>
        </Card>
      )}

      {/* Performance Overview Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Algorithm Performance - Channel Overview */}
        <div className="p-4 bg-white rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Algorithm Performance</h3>
          <AlgorithmPerformanceWidget userId={actualUserId} />
        </div>
        
        {/* Community Health - Channel Overview */}
        <div className="p-4 bg-white rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Community Health</h3>
          <CommunityHealthWidget userId={actualUserId} />
        </div>
      </div>

    </div>
  )
}