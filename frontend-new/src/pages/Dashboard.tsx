import { useUserStore } from '@/store/userStore'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'
import TaskManager from '@/components/dashboard/TaskManager'
import { Calendar, TrendingUp, Users, Video, Clock, Target } from 'lucide-react'

export default function Dashboard() {
  const { channelInfo, agentSettings } = useUserStore()

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
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-2 bg-dark-800 rounded-lg">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-purple-500 flex items-center justify-center">
              <img
                src={`/assets/images/Avatars/${agentSettings.avatar}`}
                alt={agentSettings.name}
                className="w-6 h-6 rounded-full"
              />
            </div>
            <span className="text-sm font-medium">{agentSettings.name}</span>
          </div>
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
          {/* Quick Actions */}
          <Card>
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-primary-400" />
              Quick Actions
            </h3>
            <div className="space-y-3">
              <Button size="sm" className="w-full justify-start">
                <Video className="w-4 h-4 mr-2" />
                Generate Script Idea
              </Button>
              <Button size="sm" variant="secondary" className="w-full justify-start">
                <TrendingUp className="w-4 h-4 mr-2" />
                Analyze Performance
              </Button>
              <Button size="sm" variant="secondary" className="w-full justify-start">
                <Users className="w-4 h-4 mr-2" />
                Check Audience Insights
              </Button>
            </div>
          </Card>

          {/* Recent Activity Placeholder */}
          <Card>
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Clock className="w-5 h-5 text-primary-400" />
              Recent Activity
            </h3>
            <div className="space-y-3 text-sm">
              <div className="flex items-start gap-3 p-2 bg-dark-800 rounded">
                <div className="w-2 h-2 bg-green-400 rounded-full mt-2 flex-shrink-0"></div>
                <div>
                  <p className="text-dark-200">Video "How to Code Better" published</p>
                  <p className="text-dark-400 text-xs">2 hours ago</p>
                </div>
              </div>
              <div className="flex items-start gap-3 p-2 bg-dark-800 rounded">
                <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
                <div>
                  <p className="text-dark-200">New insight generated</p>
                  <p className="text-dark-400 text-xs">5 hours ago</p>
                </div>
              </div>
              <div className="flex items-start gap-3 p-2 bg-dark-800 rounded">
                <div className="w-2 h-2 bg-purple-400 rounded-full mt-2 flex-shrink-0"></div>
                <div>
                  <p className="text-dark-200">Task "Edit intro" completed</p>
                  <p className="text-dark-400 text-xs">1 day ago</p>
                </div>
              </div>
            </div>
          </Card>

          {/* Channel Goals Placeholder */}
          <Card>
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-primary-400" />
              Channel Goals
            </h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Subscriber Goal</span>
                  <span>45.2K / 50K</span>
                </div>
                <div className="w-full bg-dark-700 rounded-full h-2">
                  <div className="bg-primary-500 h-2 rounded-full" style={{ width: '90.4%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Monthly Views</span>
                  <span>380K / 500K</span>
                </div>
                <div className="w-full bg-dark-700 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{ width: '76%' }}></div>
                </div>
              </div>
            </div>
          </Card>
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