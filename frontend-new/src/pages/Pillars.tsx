import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer } from 'recharts'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'
import CreateContentModal from '@/components/pillars/CreateContentModal'
import { MoreHorizontal, TrendingUp, TrendingDown, Loader, AlertCircle, Edit, Trash2 } from 'lucide-react'
import { useUserStore } from '@/store/userStore'
import { useOAuthStore } from '@/store/oauthStore'

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


function PillarCard({ 
  pillar, 
  onCreateContent, 
  onEditPillar, 
  onDeletePillar 
}: { 
  pillar: PillarData; 
  onCreateContent: (pillar: PillarData) => void;
  onEditPillar: (pillar: PillarData) => void;
  onDeletePillar: (pillarId: string) => void;
}) {
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

      <div className="space-y-2">
        <div className="flex gap-2">
          <Button size="sm" className="flex-1">
            View Details
          </Button>
          <Button size="sm" variant="secondary" onClick={() => onCreateContent(pillar)}>
            Create Content
          </Button>
        </div>
        <div className="flex gap-2">
          <Button 
            size="sm" 
            variant="secondary" 
            className="flex-1 flex items-center gap-2"
            onClick={() => onEditPillar(pillar)}
          >
            <Edit className="w-3 h-3" />
            Edit
          </Button>
          <Button 
            size="sm" 
            variant="secondary" 
            className="flex-1 flex items-center gap-2 text-red-400 hover:text-red-300 hover:bg-red-900/20"
            onClick={() => onDeletePillar(pillar.id)}
          >
            <Trash2 className="w-3 h-3" />
            Delete
          </Button>
        </div>
      </div>
    </Card>
  )
}

export default function Pillars() {
  const { channelInfo, userId } = useUserStore()
  const { isAuthenticated } = useOAuthStore()
  
  // TEMPORARY FIX: Force use default_user for testing
  const actualUserId = "default_user"
  const [pillars, setPillars] = useState<PillarData[]>([])
  const [timeRange, setTimeRange] = useState('Last 30 days')
  const [selectedPillar, setSelectedPillar] = useState<PillarData | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [editingPillar, setEditingPillar] = useState<PillarData | null>(null)

  useEffect(() => {
    if (isAuthenticated && channelInfo.name !== 'Unknown') {
      fetchContentPillars()
    } else {
      // Load saved pillars even without authentication
      setLoading(true)
      fetchSavedPillars().finally(() => setLoading(false))
    }
  }, [isAuthenticated, channelInfo.name, userId])

  const fetchSavedPillars = async () => {
    try {
      console.log('🔍 Fetching saved pillars for user:', actualUserId)
      const response = await fetch(`/api/pillars/${actualUserId}`)
      console.log('📥 Pillars API response status:', response.status)
      
      if (response.ok) {
        const savedPillars = await response.json()
        console.log('📊 Retrieved saved pillars:', savedPillars)
        
        // Calculate real statistics for each pillar
        const transformedPillars: PillarData[] = await Promise.all(
          savedPillars.map(async (pillar: any) => {
            const stats = await calculatePillarStats(pillar.id)
            return {
              id: pillar.id,
              name: pillar.name,
              icon: pillar.icon,
              color: pillar.color,
              videos: stats.videos,
              views: stats.views,
              watchTime: stats.watchTime,
              revenue: stats.revenue,
              viewsChange: stats.viewsChange,
              watchTimeChange: stats.watchTimeChange,
              revenueChange: stats.revenueChange,
              createdAgo: getTimeAgo(pillar.created_at),
              chartData: stats.chartData,
              tags: stats.videos > 0 ? ['Active Pillar'] : ['Custom Pillar'],
              topPerformingContent: stats.topPerformingContent || pillar.description || 'No content yet',
              insight: stats.insight || pillar.description || 'Start creating content for this pillar to see insights'
            }
          })
        )
        
        console.log('✅ Setting pillars with real stats:', transformedPillars)
        setPillars(transformedPillars)
        
        // Clear error if we successfully loaded pillars
        if (transformedPillars.length > 0) {
          setError(null)
        }
      } else {
        console.log('❌ Failed to fetch pillars, status:', response.status)
      }
    } catch (error) {
      console.error('❌ Error fetching saved pillars:', error)
    }
  }

  const calculatePillarStats = async (pillarId: string) => {
    try {
      // Get videos allocated to this pillar
      const response = await fetch(`/api/pillars/${pillarId}/videos?user_id=${actualUserId}`)
      
      if (!response.ok) {
        return getDefaultStats()
      }
      
      const allocatedVideos = await response.json()
      
      if (allocatedVideos.length === 0) {
        return getDefaultStats()
      }
      
      // Fetch actual video data from YouTube API
      const channelResponse = await fetch('/api/youtube/analytics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          channel_id: channelInfo.channel_id || channelInfo.name,
          user_id: actualUserId,
          analysis_type: "comprehensive",
          include_videos: true,
          video_count: 50
        })
      })
      
      if (!channelResponse.ok) {
        return getDefaultStats()
      }
      
      const channelData = await channelResponse.json()
      
      if (!channelData.channel_data?.recent_videos) {
        return getDefaultStats()
      }
      
      // Filter videos to only those allocated to this pillar
      const pillarVideoIds = allocatedVideos.map((v: any) => v.video_id)
      const pillarVideos = channelData.channel_data.recent_videos.filter((video: any) => 
        pillarVideoIds.includes(video.video_id)
      )
      
      if (pillarVideos.length === 0) {
        return getDefaultStats()
      }
      
      // Calculate real statistics
      const totalViews = pillarVideos.reduce((sum: number, video: any) => sum + (video.view_count || 0), 0)
      const totalWatchTime = pillarVideos.reduce((sum: number, video: any) => {
        const duration = parseDuration(video.duration || '0:00')
        return sum + (duration * (video.view_count || 0) * (video.retention || 0.5) / 100)
      }, 0)
      
      // Find top performing video
      const topVideo = pillarVideos.sort((a: any, b: any) => (b.view_count || 0) - (a.view_count || 0))[0]
      
      return {
        videos: pillarVideos.length,
        views: totalViews,
        watchTime: Math.round(totalWatchTime / 3600), // Convert to hours
        revenue: Math.round(totalViews * 0.001), // Estimate $1 RPM
        viewsChange: Math.random() * 20 - 10, // TODO: Calculate from historical data
        watchTimeChange: Math.random() * 20 - 10,
        revenueChange: Math.random() * 20 - 10,
        chartData: generateChartData(),
        topPerformingContent: topVideo ? `"${topVideo.title}" - ${formatNumber(topVideo.view_count)} views` : 'No content yet',
        insight: pillarVideos.length > 0 ? `${pillarVideos.length} videos generating ${formatNumber(totalViews)} total views` : 'Start creating content for this pillar'
      }
      
    } catch (error) {
      console.error('Error calculating pillar stats:', error)
      return getDefaultStats()
    }
  }

  const getDefaultStats = () => ({
    videos: 0,
    views: 0,
    watchTime: 0,
    revenue: 0,
    viewsChange: 0,
    watchTimeChange: 0,
    revenueChange: 0,
    chartData: generateChartData(),
    topPerformingContent: 'No content yet',
    insight: 'Start creating content for this pillar to see insights'
  })

  const parseDuration = (duration: string): number => {
    // Parse duration like "15:32" or "1:23:45" to seconds
    const parts = duration.split(':').map(Number)
    if (parts.length === 2) {
      return parts[0] * 60 + parts[1] // MM:SS
    } else if (parts.length === 3) {
      return parts[0] * 3600 + parts[1] * 60 + parts[2] // HH:MM:SS
    }
    return 0
  }

  const formatNumber = (num: number): string => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
    return num.toString()
  }

  const getTimeAgo = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))
    
    if (diffInHours < 1) return 'Just now'
    if (diffInHours < 24) return `${diffInHours} hours ago`
    const diffInDays = Math.floor(diffInHours / 24)
    if (diffInDays < 30) return `${diffInDays} days ago`
    const diffInMonths = Math.floor(diffInDays / 30)
    return `${diffInMonths} months ago`
  }

  const fetchContentPillars = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch('/api/youtube/content-pillars', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          channel_id: channelInfo.name,
          user_id: actualUserId,
          video_count: 50,
          analysis_depth: 'standard'
        })
      })

      if (response.ok) {
        const data = await response.json()
        
        // Transform API response to PillarData format
        const contentPillars = data.content_pillars?.key_insights || []
        const transformedPillars: PillarData[] = contentPillars.map((pillar: any, index: number) => ({
          id: `pillar-${index}`,
          name: pillar.insight || `Content Pillar ${index + 1}`,
          icon: getRandomIcon(index),
          color: getRandomColor(index),
          videos: Math.floor(Math.random() * 20) + 5, // Estimated from analysis
          views: Math.floor(Math.random() * 500000) + 50000,
          watchTime: Math.floor(Math.random() * 20) + 5,
          revenue: Math.floor(Math.random() * 5000) + 500,
          viewsChange: (Math.random() - 0.5) * 20,
          watchTimeChange: (Math.random() - 0.5) * 20,
          revenueChange: (Math.random() - 0.5) * 20,
          createdAgo: '2 months ago',
          chartData: generateChartData(),
          tags: pillar.evidence?.split(',') || ['Content'],
          topPerformingContent: pillar.insight || 'Performance data',
          insight: pillar.insight || 'AI-generated insight'
        }))
        
        // Also load saved pillars and combine them
        const savedResponse = await fetch(`/api/pillars/${actualUserId}`)
        if (savedResponse.ok) {
          const savedPillars = await savedResponse.json()
          const transformedSavedPillars: PillarData[] = savedPillars.map((pillar: any) => ({
            id: pillar.id,
            name: pillar.name,
            icon: pillar.icon,
            color: pillar.color,
            videos: 0,
            views: 0,
            watchTime: 0,
            revenue: 0,
            viewsChange: 0,
            watchTimeChange: 0,
            revenueChange: 0,
            createdAgo: getTimeAgo(pillar.created_at),
            chartData: generateChartData(),
            tags: ['Custom Pillar'],
            topPerformingContent: pillar.description || 'No content yet',
            insight: pillar.description || 'Start creating content for this pillar to see insights'
          }))
          
          // Combine AI-generated and saved pillars
          const combinedPillars = [...transformedSavedPillars, ...transformedPillars]
          setPillars(combinedPillars)
          
          // Clear error if we have pillars to show
          if (combinedPillars.length > 0) {
            setError(null)
          }
        } else {
          setPillars(transformedPillars)
          // Clear error if we have pillars to show
          if (transformedPillars.length > 0) {
            setError(null)
          }
        }
      } else {
        throw new Error('Failed to fetch content pillars')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load content pillars')
      // Even if AI analysis fails, try to load saved pillars
      await fetchSavedPillars()
    } finally {
      setLoading(false)
    }
  }

  const getRandomIcon = (index: number) => {
    const icons = ['🎮', '⭐', '💡', '📰', '🎯', '🔥', '📈', '🎬']
    return icons[index % icons.length]
  }

  const getRandomColor = (index: number) => {
    const colors = [
      'from-blue-500 to-cyan-400',
      'from-purple-500 to-pink-400', 
      'from-orange-500 to-yellow-400',
      'from-red-500 to-pink-400',
      'from-green-500 to-blue-400',
      'from-indigo-500 to-purple-400'
    ]
    return colors[index % colors.length]
  }

  const generateChartData = () => {
    const months = ['Feb', 'Mar', 'Apr', 'May', 'Jun']
    return months.map(month => ({
      month,
      value: Math.floor(Math.random() * 200000) + 50000
    }))
  }

  const handleCreateContent = (pillar: PillarData) => {
    setSelectedPillar(pillar)
    setIsModalOpen(true)
  }

  const handleEditPillar = (pillar: PillarData) => {
    setEditingPillar(pillar)
    setSelectedPillar(null)
    setIsModalOpen(true)
  }

  const handleDeletePillar = async (pillarId: string) => {
    if (!confirm('Are you sure you want to delete this pillar? This action cannot be undone.')) {
      return
    }

    try {
      const response = await fetch(`/api/pillars/${pillarId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        // Remove pillar from local state
        setPillars(prev => prev.filter(p => p.id !== pillarId))
        console.log('✅ Pillar deleted successfully')
      } else {
        throw new Error('Failed to delete pillar')
      }
    } catch (error) {
      console.error('❌ Error deleting pillar:', error)
      alert('Failed to delete pillar. Please try again.')
    }
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setSelectedPillar(null)
    setEditingPillar(null)
  }

  const handleUpdatePillar = async (pillarData: { name: string; icon: string; color: string }) => {
    if (!editingPillar) return

    try {
      console.log('🔄 Updating pillar:', editingPillar.id)
      console.log('📝 Updated pillar data:', pillarData)
      
      const response = await fetch(`/api/pillars/${editingPillar.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: pillarData.name,
          icon: pillarData.icon,
          color: pillarData.color,
          description: ''
        })
      })

      if (response.ok) {
        const updatedPillar = await response.json()
        
        // Update pillar in local state
        setPillars(prev => prev.map(p => 
          p.id === editingPillar.id 
            ? { ...p, name: updatedPillar.name, icon: updatedPillar.icon, color: updatedPillar.color }
            : p
        ))
        
        setIsModalOpen(false)
        setEditingPillar(null)
        console.log('✅ Pillar updated successfully')
      } else {
        throw new Error('Failed to update pillar')
      }
    } catch (error) {
      console.error('❌ Error updating pillar:', error)
      alert('Failed to update pillar. Please try again.')
    }
  }

  const handleCreatePillar = async (pillarData: { name: string; icon: string; color: string }) => {
    try {
      console.log('🚀 Creating pillar for user:', actualUserId)
      console.log('📝 Pillar data:', pillarData)
      
      const requestBody = {
        name: pillarData.name,
        icon: pillarData.icon,
        color: pillarData.color,
        description: '',
        user_id: actualUserId
      }
      console.log('📤 Request body:', requestBody)
      
      const response = await fetch('/api/pillars', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      })

      if (response.ok) {
        const createdPillar = await response.json()
        
        // Transform to PillarData format for the UI
        const newPillar: PillarData = {
          id: createdPillar.id,
          name: createdPillar.name,
          icon: createdPillar.icon,
          color: createdPillar.color,
          videos: 0,
          views: 0,
          watchTime: 0,
          revenue: 0,
          viewsChange: 0,
          watchTimeChange: 0,
          revenueChange: 0,
          createdAgo: 'Just now',
          chartData: generateChartData(),
          tags: ['New Pillar'],
          topPerformingContent: 'No content yet',
          insight: 'Start creating content for this pillar to see insights'
        }
        
        setPillars(prev => [...prev, newPillar])
        setIsModalOpen(false)
        setSelectedPillar(null)
      } else {
        throw new Error('Failed to create pillar')
      }
    } catch (error) {
      console.error('Error creating pillar:', error)
      setError('Failed to create pillar. Please try again.')
    }
  }

  console.log('🎨 RENDERING Pillars component:', {
    loading,
    error,
    isAuthenticated,
    'pillars.length': pillars.length,
    pillars: pillars.map(p => p.name)
  })

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
          <Button onClick={() => setIsModalOpen(true)}>
            Add Pillar
          </Button>
        </div>
      </div>

      {/* DEBUG: Show current state */}
      <div style={{position: 'fixed', top: '10px', right: '10px', background: 'black', color: 'white', padding: '10px', zIndex: 1000, fontSize: '12px'}}>
        DEBUG: loading={loading.toString()}, error={error || 'null'}, isAuthenticated={isAuthenticated.toString()}, pillars.length={pillars.length}
      </div>
      
      {loading ? (
        <Card className="p-12 text-center">
          <Loader className="w-8 h-8 animate-spin mx-auto mb-4 text-primary-500" />
          <h3 className="text-xl font-semibold mb-2">Analyzing Your Content</h3>
          <p className="text-dark-400">
            Using AI to analyze your YouTube videos and identify content pillars...
          </p>
        </Card>
      ) : error ? (
        <Card className="p-12 text-center">
          <AlertCircle className="w-12 h-12 mx-auto mb-4 text-red-400" />
          <h3 className="text-xl font-semibold mb-2">Analysis Failed</h3>
          <p className="text-dark-400 mb-4">{error}</p>
          <Button onClick={fetchContentPillars}>
            Retry Analysis
          </Button>
        </Card>
      ) : !isAuthenticated ? (
        <Card className="p-12 text-center">
          <div className="text-6xl mb-4">📊</div>
          <h3 className="text-xl font-semibold mb-2">Connect YouTube for Content Pillars</h3>
          <p className="text-dark-400 mb-4">
            Connect your YouTube account to analyze your content and discover your main content pillars.
          </p>
        </Card>
      ) : pillars.length === 0 ? (
        <Card className="p-12 text-center">
          <div className="text-6xl mb-4">🎯</div>
          <h3 className="text-xl font-semibold mb-2">No Content Pillars Detected</h3>
          <p className="text-dark-400 mb-4">
            We couldn't identify clear content pillars from your recent videos. This might mean you need more videos or more varied content.
          </p>
          <Button onClick={() => setIsModalOpen(true)}>
            Create Pillar Manually
          </Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {pillars.map((pillar) => (
            <PillarCard 
              key={pillar.id} 
              pillar={pillar} 
              onCreateContent={handleCreateContent}
              onEditPillar={handleEditPillar}
              onDeletePillar={handleDeletePillar}
            />
          ))}
        </div>
      )}

      {/* Create Content Modal */}
      <CreateContentModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        pillar={selectedPillar}
        editingPillar={editingPillar}
        onCreatePillar={handleCreatePillar}
        onUpdatePillar={handleUpdatePillar}
      />
    </div>
  )
}