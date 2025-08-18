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
      text: 'How is my channel performing this month?',
      category: 'analytics',
      agentSpecific: ['2'], // Levi - Content Analysis
      icon: '📊'
    },
    {
      id: 'analytics-2', 
      text: 'Which videos are driving the most engagement?',
      category: 'analytics',
      agentSpecific: ['2'],
      icon: '🔥'
    },
    {
      id: 'analytics-3',
      text: 'What are my peak viewing hours?',
      category: 'analytics',
      agentSpecific: ['3'], // Agent 3 - Audience Insights
      icon: '⏰'
    },

    // Content Strategy
    {
      id: 'content-1',
      text: 'What content should I create next?',
      category: 'content',
      agentSpecific: ['2'],
      icon: '💡'
    },
    {
      id: 'content-2',
      text: 'How can I improve my video thumbnails?',
      category: 'content',
      agentSpecific: ['2'],
      icon: '🎨'
    },
    {
      id: 'content-3',
      text: 'What trending topics match my niche?',
      category: 'content',
      agentSpecific: ['2', '4'], // Content Analysis + SEO
      icon: '📈'
    },

    // Growth & Audience
    {
      id: 'growth-1',
      text: 'How can I grow my subscriber base?',
      category: 'growth',
      agentSpecific: ['3'],
      icon: '🚀'
    },
    {
      id: 'growth-2',
      text: 'What demographics watch my content?',
      category: 'growth',
      agentSpecific: ['3'],
      icon: '👥'
    },
    {
      id: 'growth-3',
      text: 'How do I increase my video retention?',
      category: 'growth',
      agentSpecific: ['2', '3'],
      icon: '⏱️'
    },

    // SEO & Discoverability
    {
      id: 'seo-1',
      text: 'How can I optimize my video titles?',
      category: 'seo',
      agentSpecific: ['4'], // Agent 4 - SEO Discoverability
      icon: '🔍'
    },
    {
      id: 'seo-2',
      text: 'What keywords should I target?',
      category: 'seo',
      agentSpecific: ['4'],
      icon: '🎯'
    },
    {
      id: 'seo-3',
      text: 'How do I rank higher in search?',
      category: 'seo',
      agentSpecific: ['4'],
      icon: '📍'
    },

    // Monetization
    {
      id: 'monetization-1',
      text: 'How can I increase my ad revenue?',
      category: 'monetization',
      agentSpecific: ['5'], // Agent 5 - Monetization Strategy
      icon: '💰'
    },
    {
      id: 'monetization-2',
      text: 'What sponsorship opportunities exist?',
      category: 'monetization',
      agentSpecific: ['5'],
      icon: '🤝'
    },
    {
      id: 'monetization-3',
      text: 'Should I create a membership program?',
      category: 'monetization',
      agentSpecific: ['5'],
      icon: '⭐'
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
