import { useUserStore } from '@/store/userStore'
import Card from '@/components/common/Card'
import TaskManager from '@/components/dashboard/TaskManager'
import ChannelGoals from '@/components/dashboard/ChannelGoals'
import { Calendar, TrendingUp, Users, Video, Clock } from 'lucide-react'

export default function Dashboard() {
  const { channelInfo } = useUserStore()

  // Quick stats data - in real app this would come from API
  const quickStats = [
    {
      title: 'Total Views',
      value: '2.4M',
      change: '+12%',
      trend: 'up',
      icon: TrendingUp,
      color: 'text-blue-400'
    },
    {
      title: 'Subscribers',
      value: '45.2K',
      change: '+8%',
      trend: 'up',
      icon: Users,
      color: 'text-green-400'
    },
    {
      title: 'Videos',
      value: '127',
      change: '+3',
      trend: 'up',
      icon: Video,
      color: 'text-purple-400'
    },
    {
      title: 'Avg. Watch Time',
      value: '4:32',
      change: '+5%',
      trend: 'up',
      icon: Clock,
      color: 'text-orange-400'
    }
  ]

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

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {quickStats.map((stat, index) => (
          <Card key={index} className="p-4">
            <div className="flex items-center justify-between mb-2">
              <stat.icon className={`w-5 h-5 ${stat.color}`} />
              <span className="text-xs text-green-400 font-medium">
                {stat.change}
              </span>
            </div>
            <div className="space-y-1">
              <p className="text-2xl font-bold">{stat.value}</p>
              <p className="text-sm text-dark-400">{stat.title}</p>
            </div>
          </Card>
        ))}
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