import { computed } from 'vue'

export interface SmartQuestion {
  id: string
  text: string
  category: 'analytics' | 'content' | 'growth' | 'monetization' | 'seo'
  agentSpecific?: string[] // Agent IDs that this question is most relevant for
  icon: string
}

export const useSmartQuestions = () => {
  // Channel-specific smart questions that provide real value
  const smartQuestions = computed<SmartQuestion[]>(() => [
    // Analytics & Performance
    {
      id: 'analytics-1',
      text: 'Analyze my channel performance and give me 3 key insights',
      category: 'analytics',
      agentSpecific: ['2'], // Levi - Content Analysis
      icon: '📊'
    },
    {
      id: 'analytics-2',
      text: 'Which of my videos should I promote more and why?',
      category: 'analytics',
      agentSpecific: ['2'],
      icon: '🔥'
    },
    {
      id: 'analytics-3',
      text: 'What time should I post to maximize views?',
      category: 'analytics',
      agentSpecific: ['3'], // Agent 3 - Audience Insights
      icon: '⏰'
    },
    {
      id: 'analytics-4',
      text: 'Why did my latest video underperform?',
      category: 'analytics',
      agentSpecific: ['2'],
      icon: '📉'
    },

    // Content Strategy
    {
      id: 'content-1',
      text: 'Generate 5 viral video ideas for my niche',
      category: 'content',
      agentSpecific: ['2'],
      icon: '💡'
    },
    {
      id: 'content-2',
      text: 'What trending topics should I cover this week?',
      category: 'content',
      agentSpecific: ['2'],
      icon: '🔥'
    },
    {
      id: 'content-3',
      text: 'Help me plan a content series that will go viral',
      category: 'content',
      agentSpecific: ['2'],
      icon: '🎬'
    },
    {
      id: 'content-4',
      text: 'Design me 3 thumbnail concepts that will get clicks',
      category: 'content',
      agentSpecific: ['2'],
      icon: '🎨'
    },
    {
      id: 'content-5',
      text: 'What trending topics should I jump on this week?',
      category: 'content',
      agentSpecific: ['2', '4'], // Content Analysis + SEO
      icon: '📈'
    },

    // Growth & Audience
    {
      id: 'growth-1',
      text: 'Give me 5 proven strategies to gain 1000 subscribers',
      category: 'growth',
      agentSpecific: ['3'],
      icon: '🚀'
    },
    {
      id: 'growth-2',
      text: 'Who is my target audience and how do I reach them?',
      category: 'growth',
      agentSpecific: ['3'],
      icon: '👥'
    },
    {
      id: 'growth-3',
      text: 'Why do people click away from my videos?',
      category: 'growth',
      agentSpecific: ['2', '3'],
      icon: '⏱️'
    },
    {
      id: 'growth-4',
      text: 'What should I do to get featured on YouTube homepage?',
      category: 'growth',
      agentSpecific: ['4'],
      icon: '⭐'
    },

    // SEO & Discoverability
    {
      id: 'seo-1',
      text: 'Write me 5 high-converting titles for my next video',
      category: 'seo',
      agentSpecific: ['4'], // Agent 4 - SEO Discoverability
      icon: '🔍'
    },
    {
      id: 'seo-2',
      text: 'Find me low-competition keywords I can rank for',
      category: 'seo',
      agentSpecific: ['4'],
      icon: '🎯'
    },
    {
      id: 'seo-3',
      text: 'Optimize my video description for maximum discoverability',
      category: 'seo',
      agentSpecific: ['4'],
      icon: '📍'
    },

    // Monetization
    {
      id: 'monetization-1',
      text: 'Show me 3 ways to double my YouTube revenue',
      category: 'monetization',
      agentSpecific: ['5'], // Agent 5 - Monetization Strategy
      icon: '💰'
    },
    {
      id: 'monetization-2',
      text: 'Find brands that would sponsor my content',
      category: 'monetization',
      agentSpecific: ['5'],
      icon: '🤝'
    },
    {
      id: 'monetization-3',
      text: 'Should I launch a Patreon or membership program?',
      category: 'monetization',
      agentSpecific: ['5'],
      icon: '⭐'
    },
    {
      id: 'monetization-4',
      text: 'What products could I create and sell to my audience?',
      category: 'monetization',
      agentSpecific: ['5'],
      icon: '🛍️'
    }
  ])

  // Get questions relevant to a specific agent
  const getQuestionsForAgent = (agentId: string) => {
    return smartQuestions.value.filter(q => 
      !q.agentSpecific || q.agentSpecific.includes(agentId)
    )
  }

  // Get questions by category
  const getQuestionsByCategory = (category: SmartQuestion['category']) => {
    return smartQuestions.value.filter(q => q.category === category)
  }

  // Get random questions for variety
  const getRandomQuestions = (count: number = 3) => {
    const shuffled = [...smartQuestions.value].sort(() => 0.5 - Math.random())
    return shuffled.slice(0, count)
  }

  // Get contextual questions based on time of day, recent activity, etc.
  const getContextualQuestions = (agentId: string) => {
    const agentQuestions = getQuestionsForAgent(agentId)
    const hour = new Date().getHours()
    
    // Morning: Focus on analytics and planning
    if (hour >= 6 && hour < 12) {
      return agentQuestions.filter(q => 
        q.category === 'analytics' || q.category === 'content'
      ).slice(0, 3)
    }
    
    // Afternoon: Focus on content creation and optimization
    if (hour >= 12 && hour < 18) {
      return agentQuestions.filter(q => 
        q.category === 'content' || q.category === 'seo'
      ).slice(0, 3)
    }
    
    // Evening: Focus on growth and monetization
    return agentQuestions.filter(q => 
      q.category === 'growth' || q.category === 'monetization'
    ).slice(0, 3)
  }

  return {
    smartQuestions,
    getQuestionsForAgent,
    getQuestionsByCategory,
    getRandomQuestions,
    getContextualQuestions
  }
}
