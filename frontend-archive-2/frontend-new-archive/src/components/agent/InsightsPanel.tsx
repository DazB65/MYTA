import { useEffect, useState } from 'react'
import { useUserStore } from '@/store/userStore'
import { api } from '@/services/api'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'
import LoadingSpinner from '@/components/common/LoadingSpinner'

interface Insight {
  type: string
  content: string
  priority: 'high' | 'medium' | 'low'
}

export default function InsightsPanel() {
  const { userId } = useUserStore()
  const [insights, setInsights] = useState<Insight[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)

  const loadInsights = async () => {
    if (!userId) return
    
    setIsLoading(true)
    try {
      const data = await api.agent.getInsights(userId)
      if (data.insights) {
        setInsights(data.insights)
      }
    } catch (error) {
      console.error('Failed to load insights:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const generateInsights = async () => {
    if (!userId) return
    
    setIsGenerating(true)
    try {
      await api.agent.generateInsights(userId)
      await loadInsights()
    } catch (error) {
      console.error('Failed to generate insights:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  useEffect(() => {
    loadInsights()
  }, [userId])

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'text-red-400 bg-red-900/20'
      case 'medium':
        return 'text-yellow-400 bg-yellow-900/20'
      case 'low':
        return 'text-green-400 bg-green-900/20'
      default:
        return 'text-dark-400 bg-dark-800'
    }
  }

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'performance':
        return '📊'
      case 'trending':
        return '🔥'
      case 'optimization':
        return '⚡'
      case 'content':
        return '💡'
      case 'engagement':
        return '❤️'
      default:
        return '💭'
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-32">
        <LoadingSpinner size="sm" />
      </div>
    )
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-xs text-dark-400">
          {insights.length} insights available
        </span>
        <Button
          onClick={generateInsights}
          isLoading={isGenerating}
          variant="secondary"
          size="xs"
        >
          🔄 Refresh
        </Button>
      </div>

      {insights.length === 0 ? (
        <Card className="p-4 text-center">
          <div className="text-dark-400 text-sm mb-3">
            No insights available yet
          </div>
          <Button
            onClick={generateInsights}
            isLoading={isGenerating}
            size="sm"
            variant="secondary"
          >
            Generate Insights
          </Button>
        </Card>
      ) : (
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {insights.map((insight, index) => (
            <Card key={index} className="p-3">
              <div className="flex items-start gap-2">
                <span className="text-lg">{getInsightIcon(insight.type)}</span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-medium capitalize">
                      {insight.type}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${getPriorityColor(insight.priority)}`}>
                      {insight.priority}
                    </span>
                  </div>
                  <p className="text-sm text-dark-300 leading-relaxed">
                    {insight.content}
                  </p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}