import { useState, useEffect } from 'react'
import { useUserStore } from '@/store/userStore'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'

interface ContentPillar {
  id: string
  name: string
  description: string
  topics: string[]
  lastUpdated: string
}

export default function Pillars() {
  const { channelInfo } = useUserStore()
  const [pillars, setPillars] = useState<ContentPillar[]>([])
  const [isGenerating, setIsGenerating] = useState(false)

  // Sample pillars for demo - in real app this would come from API
  const samplePillars: ContentPillar[] = [
    {
      id: '1',
      name: 'Tutorial Content',
      description: 'Step-by-step educational content for your audience',
      topics: ['Beginner guides', 'Advanced techniques', 'Tool reviews', 'Setup tutorials'],
      lastUpdated: '2024-01-15'
    },
    {
      id: '2', 
      name: 'Industry Insights',
      description: 'Latest trends and developments in your niche',
      topics: ['Market analysis', 'Trend predictions', 'Industry news', 'Expert interviews'],
      lastUpdated: '2024-01-14'
    },
    {
      id: '3',
      name: 'Community Content',
      description: 'Content that builds engagement with your audience',
      topics: ['Q&A sessions', 'Behind the scenes', 'Viewer challenges', 'Community highlights'],
      lastUpdated: '2024-01-13'
    }
  ]

  useEffect(() => {
    // Load pillars based on channel niche
    setPillars(samplePillars)
  }, [channelInfo.niche])

  const generatePillars = async () => {
    setIsGenerating(true)
    try {
      // In real app, this would call API to generate pillars based on channel info
      await new Promise(resolve => setTimeout(resolve, 2000)) // Simulate API call
      setPillars(samplePillars)
    } catch (error) {
      console.error('Failed to generate pillars:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Content Pillars</h1>
          <p className="text-dark-400">
            Build your content strategy around these core themes and topics.
          </p>
        </div>
        <Button
          onClick={generatePillars}
          isLoading={isGenerating}
          className="flex items-center gap-2"
        >
          🏛️ Generate Pillars
        </Button>
      </div>

      {/* Pillars Overview */}
      <Card>
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-purple-500 rounded-2xl flex items-center justify-center">
            <span className="text-2xl">🏛️</span>
          </div>
          <div>
            <h3 className="text-xl font-semibold">Your Content Foundation</h3>
            <p className="text-dark-400">
              Content pillars optimized for {channelInfo.niche} channels
            </p>
          </div>
        </div>

        {pillars.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🏛️</div>
            <h3 className="text-lg font-semibold mb-2">No pillars yet</h3>
            <p className="text-dark-400 mb-6">
              Generate content pillars based on your channel's niche and goals.
            </p>
            <Button
              onClick={generatePillars}
              isLoading={isGenerating}
            >
              Generate Content Pillars
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {pillars.map((pillar) => (
              <Card key={pillar.id} className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <h4 className="text-lg font-semibold">{pillar.name}</h4>
                  <span className="text-xs text-dark-400">
                    Updated {new Date(pillar.lastUpdated).toLocaleDateString()}
                  </span>
                </div>
                
                <p className="text-dark-300 mb-4">
                  {pillar.description}
                </p>
                
                <div className="space-y-2">
                  <h5 className="text-sm font-medium text-dark-200">Content Ideas:</h5>
                  <div className="flex flex-wrap gap-2">
                    {pillar.topics.map((topic, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-primary-600/20 text-primary-300 text-xs rounded-full"
                      >
                        {topic}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-dark-700">
                  <Button
                    variant="secondary"
                    size="sm"
                    className="w-full"
                  >
                    Generate Video Ideas
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}
      </Card>

      {/* Strategy Tips */}
      <Card>
        <h3 className="text-lg font-semibold mb-4">Content Pillar Strategy</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center p-4">
            <div className="text-2xl mb-2">🎯</div>
            <h4 className="font-semibold mb-1">Stay Focused</h4>
            <p className="text-sm text-dark-400">
              Stick to 3-5 core pillars for consistent messaging
            </p>
          </div>
          <div className="text-center p-4">
            <div className="text-2xl mb-2">🔄</div>
            <h4 className="font-semibold mb-1">Rotate Content</h4>
            <p className="text-sm text-dark-400">
              Cycle through pillars to maintain variety
            </p>
          </div>
          <div className="text-center p-4">
            <div className="text-2xl mb-2">📊</div>
            <h4 className="font-semibold mb-1">Track Performance</h4>
            <p className="text-sm text-dark-400">
              Monitor which pillars resonate most with your audience
            </p>
          </div>
        </div>
      </Card>
    </div>
  )
}