import { useUserStore } from '@/store/userStore'
import Card from '@/components/common/Card'
import TaskManager from '@/components/dashboard/TaskManager'
import ChannelGoals from '@/components/dashboard/ChannelGoals'
import { Calendar, Video } from 'lucide-react'

export default function Dashboard() {
  const { channelInfo } = useUserStore()

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

      {/* Bottom Section - Placeholder for future widgets */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Performance Overview</h3>
          <div className="text-center py-8 text-dark-400">
            <Calendar className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>Chart widget will go here</p>
            <p className="text-sm">Integration with analytics coming soon</p>
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Content Calendar</h3>
          <div className="text-center py-8 text-dark-400">
            <Video className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>Content schedule will go here</p>
            <p className="text-sm">Upload planning widget coming soon</p>
          </div>
        </Card>
      </div>
    </div>
  )
}