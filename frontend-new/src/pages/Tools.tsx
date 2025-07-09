import { useState } from 'react'
import { useChat } from '@/hooks/useChat'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'

interface Tool {
  id: string
  title: string
  description: string
  icon: string
  category: 'content' | 'optimization' | 'analysis' | 'planning'
  action: string
}

const tools: Tool[] = [
  {
    id: 'script_generator',
    title: 'Script Generator',
    description: 'Generate engaging video scripts based on your topic and style',
    icon: '📝',
    category: 'content',
    action: 'generate_script'
  },
  {
    id: 'title_optimizer',
    title: 'Title Optimizer',
    description: 'Create SEO-friendly titles that increase click-through rates',
    icon: '🎯',
    category: 'optimization',
    action: 'optimize_title'
  },
  {
    id: 'thumbnail_analyzer',
    title: 'Thumbnail Analyzer',
    description: 'Analyze thumbnail effectiveness and get improvement suggestions',
    icon: '🖼️',
    category: 'analysis',
    action: 'analyze_thumbnail'
  },
  {
    id: 'hook_improver',
    title: 'Hook Improver',
    description: 'Craft compelling video openings that hook viewers immediately',
    icon: '🎣',
    category: 'content',
    action: 'improve_hooks'
  },
  {
    id: 'trending_topics',
    title: 'Trending Topics',
    description: 'Discover trending topics and keywords in your niche',
    icon: '🔥',
    category: 'planning',
    action: 'get_trending'
  },
  {
    id: 'competitor_analysis',
    title: 'Competitor Analysis',
    description: 'Analyze competitor strategies and find content gaps',
    icon: '🕵️',
    category: 'analysis',
    action: 'analyze_competitors'
  },
  {
    id: 'content_calendar',
    title: 'Content Calendar',
    description: 'Plan and schedule your content strategy for maximum impact',
    icon: '📅',
    category: 'planning',
    action: 'create_calendar'
  },
  {
    id: 'engagement_booster',
    title: 'Engagement Booster',
    description: 'Generate ideas to increase likes, comments, and subscriber engagement',
    icon: '❤️',
    category: 'optimization',
    action: 'boost_engagement'
  }
]

const categories = [
  { id: 'all', name: 'All Tools', icon: '🛠️' },
  { id: 'content', name: 'Content Creation', icon: '📝' },
  { id: 'optimization', name: 'Optimization', icon: '⚡' },
  { id: 'analysis', name: 'Analytics', icon: '📊' },
  { id: 'planning', name: 'Planning', icon: '📋' }
]

export default function Tools() {
  const { sendQuickAction, isLoading } = useChat()
  const [selectedCategory, setSelectedCategory] = useState<string>('all')

  const filteredTools = selectedCategory === 'all' 
    ? tools 
    : tools.filter(tool => tool.category === selectedCategory)

  const handleToolClick = (action: string) => {
    sendQuickAction(action)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Creator Tools</h1>
        <p className="text-dark-400">
          Powerful AI-driven tools to enhance your content creation workflow.
        </p>
      </div>

      {/* Category Filter */}
      <Card>
        <div className="flex flex-wrap gap-2">
          {categories.map((category) => (
            <Button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              variant={selectedCategory === category.id ? 'primary' : 'secondary'}
              size="sm"
              className="flex items-center gap-2"
            >
              <span>{category.icon}</span>
              {category.name}
            </Button>
          ))}
        </div>
      </Card>

      {/* Tools Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredTools.map((tool) => (
          <Card key={tool.id} className="p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-purple-500 rounded-xl flex items-center justify-center text-2xl">
                {tool.icon}
              </div>
              <span className="text-xs px-2 py-1 bg-dark-700 rounded-full text-dark-300 capitalize">
                {tool.category}
              </span>
            </div>
            
            <h3 className="text-lg font-semibold mb-2">{tool.title}</h3>
            <p className="text-dark-400 text-sm mb-6 leading-relaxed">
              {tool.description}
            </p>
            
            <Button
              onClick={() => handleToolClick(tool.action)}
              isLoading={isLoading}
              className="w-full"
              size="sm"
            >
              Use Tool
            </Button>
          </Card>
        ))}
      </div>

      {/* Quick Access */}
      <Card>
        <h3 className="text-lg font-semibold mb-4">Quick Access</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {tools.slice(0, 4).map((tool) => (
            <Button
              key={tool.id}
              onClick={() => handleToolClick(tool.action)}
              isLoading={isLoading}
              variant="secondary"
              className="flex flex-col items-center gap-2 h-auto py-4"
            >
              <span className="text-2xl">{tool.icon}</span>
              <span className="text-sm font-medium">{tool.title}</span>
            </Button>
          ))}
        </div>
      </Card>

      {/* Usage Tips */}
      <Card>
        <h3 className="text-lg font-semibold mb-4">💡 Pro Tips</h3>
        <div className="space-y-3">
          <div className="flex items-start gap-3">
            <span className="text-primary-400 mt-1">•</span>
            <p className="text-sm text-dark-300">
              Use the Script Generator with specific topics for best results - the more context you provide, the better the output.
            </p>
          </div>
          <div className="flex items-start gap-3">
            <span className="text-primary-400 mt-1">•</span>
            <p className="text-sm text-dark-300">
              Run Title Optimizer on multiple variations to find the highest-performing option for your niche.
            </p>
          </div>
          <div className="flex items-start gap-3">
            <span className="text-primary-400 mt-1">•</span>
            <p className="text-sm text-dark-300">
              Check Trending Topics weekly to stay ahead of viral content opportunities in your field.
            </p>
          </div>
        </div>
      </Card>
    </div>
  )
}