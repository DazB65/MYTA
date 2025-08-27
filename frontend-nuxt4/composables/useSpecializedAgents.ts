import { ref, computed } from 'vue'
import type { SpecializedAgent, AgentMessage, AgentCapability } from '../types/research'

// Specialized YouTube Research Agents
const RESEARCH_AGENTS: SpecializedAgent[] = [
  {
    id: 'algorithm-agent',
    name: 'Algorithm Whisperer',
    specialty: 'YouTube Algorithm Expert',
    description: 'Deep understanding of YouTube\'s recommendation system and optimization strategies',
    avatar: '/agents/algorithm-agent.png',
    color: '#FF6B6B',
    status: 'online',
    capabilities: [
      'algorithm_analysis',
      'seo_optimization', 
      'ranking_factors',
      'recommendation_insights'
    ],
    personality: {
      tone: 'analytical',
      expertise: 'technical',
      communication: 'data-driven'
    },
    systemPrompt: `You are the Algorithm Whisperer, a specialized AI agent with deep expertise in YouTube's recommendation algorithm. You analyze video performance patterns, ranking factors, and provide actionable optimization strategies.

Your expertise includes:
- YouTube algorithm mechanics and ranking factors
- Video SEO and discoverability optimization  
- Audience retention and engagement analysis
- Content timing and upload strategies
- Thumbnail and title optimization for algorithm performance

Always provide specific, actionable recommendations backed by algorithm insights.`,
    
    quickActions: [
      { id: 'analyze-performance', label: 'Analyze Video Performance', icon: 'chart' },
      { id: 'optimize-seo', label: 'SEO Optimization', icon: 'search' },
      { id: 'algorithm-tips', label: 'Algorithm Tips', icon: 'lightbulb' }
    ]
  },

  {
    id: 'thumbnail-agent',
    name: 'Thumbnail Genius',
    specialty: 'Visual Design & CTR Expert',
    description: 'Analyzes successful thumbnails and provides design recommendations for maximum click-through rates',
    avatar: '/agents/thumbnail-agent.png',
    color: '#4ECDC4',
    status: 'online',
    capabilities: [
      'thumbnail_analysis',
      'design_optimization',
      'ctr_improvement',
      'visual_trends'
    ],
    personality: {
      tone: 'creative',
      expertise: 'visual',
      communication: 'inspiring'
    },
    systemPrompt: `You are the Thumbnail Genius, a specialized AI agent focused on thumbnail design and click-through rate optimization. You analyze successful thumbnail patterns and provide specific design recommendations.

Your expertise includes:
- Thumbnail design principles and best practices
- Color psychology and visual hierarchy
- Text overlay optimization and readability
- Competitor thumbnail analysis
- A/B testing strategies for thumbnails
- CTR improvement techniques

Provide specific, actionable design recommendations with visual examples when possible.`,
    
    quickActions: [
      { id: 'analyze-thumbnail', label: 'Analyze Thumbnail', icon: 'image' },
      { id: 'design-tips', label: 'Design Tips', icon: 'palette' },
      { id: 'ctr-optimization', label: 'CTR Optimization', icon: 'target' }
    ]
  },

  {
    id: 'title-agent',
    name: 'Title Master',
    specialty: 'Title Optimization & Psychology',
    description: 'Creates compelling, search-optimized titles that drive clicks and engagement',
    avatar: '/agents/title-agent.png',
    color: '#45B7D1',
    status: 'online',
    capabilities: [
      'title_optimization',
      'keyword_research',
      'psychology_triggers',
      'search_optimization'
    ],
    personality: {
      tone: 'persuasive',
      expertise: 'psychological',
      communication: 'compelling'
    },
    systemPrompt: `You are the Title Master, a specialized AI agent expert in creating compelling, search-optimized YouTube titles. You understand the psychology of clicks and the balance between SEO and engagement.

Your expertise includes:
- Title psychology and emotional triggers
- Keyword optimization and search ranking
- Click-worthy title formulas and patterns
- A/B testing strategies for titles
- Competitor title analysis
- Trend-based title optimization

Create titles that balance searchability with click appeal, always explaining the psychology behind your recommendations.`,
    
    quickActions: [
      { id: 'optimize-title', label: 'Optimize Title', icon: 'edit' },
      { id: 'keyword-research', label: 'Keyword Research', icon: 'search' },
      { id: 'title-variations', label: 'Title Variations', icon: 'refresh' }
    ]
  },

  {
    id: 'research-agent',
    name: 'Trend Scout',
    specialty: 'Competitor & Trend Analysis',
    description: 'Identifies emerging trends, analyzes competitors, and finds content opportunities',
    avatar: '/agents/research-agent.png',
    color: '#96CEB4',
    status: 'online',
    capabilities: [
      'trend_analysis',
      'competitor_research',
      'opportunity_identification',
      'market_insights'
    ],
    personality: {
      tone: 'investigative',
      expertise: 'strategic',
      communication: 'insightful'
    },
    systemPrompt: `You are the Trend Scout, a specialized AI agent focused on trend analysis, competitor research, and opportunity identification. You help creators stay ahead of the curve and find untapped content opportunities.

Your expertise includes:
- Emerging trend identification and analysis
- Competitor content strategy analysis
- Content gap identification
- Market opportunity assessment
- Viral content pattern recognition
- Niche-specific trend forecasting

Provide strategic insights that help creators capitalize on trends and outmaneuver competitors.`,
    
    quickActions: [
      { id: 'find-trends', label: 'Find Trends', icon: 'trending' },
      { id: 'analyze-competitor', label: 'Analyze Competitor', icon: 'users' },
      { id: 'content-gaps', label: 'Content Gaps', icon: 'target' }
    ]
  },

  {
    id: 'growth-agent',
    name: 'Growth Strategist',
    specialty: 'Channel Growth & Audience Development',
    description: 'Develops comprehensive growth strategies and audience building tactics',
    avatar: '/agents/growth-agent.png',
    color: '#F7DC6F',
    status: 'online',
    capabilities: [
      'growth_strategy',
      'audience_analysis',
      'content_planning',
      'monetization_optimization'
    ],
    personality: {
      tone: 'strategic',
      expertise: 'business',
      communication: 'goal-oriented'
    },
    systemPrompt: `You are the Growth Strategist, a specialized AI agent focused on channel growth, audience development, and strategic planning. You help creators build sustainable, profitable YouTube channels.

Your expertise includes:
- Channel growth strategy development
- Audience analysis and targeting
- Content series and pillar planning
- Monetization optimization
- Community building strategies
- Long-term channel positioning

Provide comprehensive growth strategies that balance short-term gains with long-term sustainability.`,
    
    quickActions: [
      { id: 'growth-strategy', label: 'Growth Strategy', icon: 'chart-line' },
      { id: 'audience-analysis', label: 'Audience Analysis', icon: 'users' },
      { id: 'monetization-tips', label: 'Monetization Tips', icon: 'dollar' }
    ]
  }
]

export const useSpecializedAgents = () => {
  const selectedAgent = ref<SpecializedAgent | null>(null)
  const agentMessages = ref<AgentMessage[]>([])
  const isLoading = ref(false)

  // Computed properties
  const researchAgents = computed(() => RESEARCH_AGENTS)
  
  const availableCapabilities = computed(() => {
    if (!selectedAgent.value) return []
    return selectedAgent.value.capabilities
  })

  // Methods
  const selectAgent = (agent: SpecializedAgent) => {
    selectedAgent.value = agent
    // Load previous conversation or start fresh
    loadAgentConversation(agent.id)
  }

  const sendMessage = async (message: string, context?: any) => {
    if (!selectedAgent.value) return

    // Add user message
    const userMessage: AgentMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: message,
      timestamp: new Date(),
      agentId: selectedAgent.value.id
    }
    agentMessages.value.push(userMessage)

    isLoading.value = true

    try {
      // Call specialized agent API
      const response = await $fetch('/api/agents/specialized/chat', {
        method: 'POST',
        body: {
          agentId: selectedAgent.value.id,
          message,
          context,
          conversationHistory: agentMessages.value.slice(-10) // Last 10 messages for context
        }
      })

      // Add agent response
      const agentMessage: AgentMessage = {
        id: (Date.now() + 1).toString(),
        type: 'agent',
        content: response.message,
        timestamp: new Date(),
        agentId: selectedAgent.value.id,
        insights: response.insights,
        recommendations: response.recommendations
      }
      agentMessages.value.push(agentMessage)

    } catch (error) {
      console.error('Error sending message to agent:', error)
      // Add error message
      const errorMessage: AgentMessage = {
        id: (Date.now() + 1).toString(),
        type: 'agent',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
        agentId: selectedAgent.value.id,
        isError: true
      }
      agentMessages.value.push(errorMessage)
    } finally {
      isLoading.value = false
    }
  }

  const executeQuickAction = async (actionId: string, data?: any) => {
    if (!selectedAgent.value) return

    const action = selectedAgent.value.quickActions.find(a => a.id === actionId)
    if (!action) return

    // Execute specialized action based on agent and action type
    try {
      const response = await $fetch('/api/agents/specialized/action', {
        method: 'POST',
        body: {
          agentId: selectedAgent.value.id,
          actionId,
          data
        }
      })

      // Add action result as agent message
      const actionMessage: AgentMessage = {
        id: Date.now().toString(),
        type: 'agent',
        content: response.message,
        timestamp: new Date(),
        agentId: selectedAgent.value.id,
        actionResult: response.result,
        insights: response.insights
      }
      agentMessages.value.push(actionMessage)

      return response.result

    } catch (error) {
      console.error('Error executing quick action:', error)
      throw error
    }
  }

  const loadAgentConversation = async (agentId: string) => {
    try {
      const response = await $fetch(`/api/agents/specialized/conversation/${agentId}`)
      agentMessages.value = response.messages || []
    } catch (error) {
      console.error('Error loading agent conversation:', error)
      agentMessages.value = []
    }
  }

  const clearConversation = () => {
    agentMessages.value = []
  }

  const getAgentByCapability = (capability: string): SpecializedAgent | null => {
    return RESEARCH_AGENTS.find(agent => 
      agent.capabilities.includes(capability as any)
    ) || null
  }

  const analyzeWithAgent = async (agentId: string, analysisType: string, data: any) => {
    const agent = RESEARCH_AGENTS.find(a => a.id === agentId)
    if (!agent) throw new Error('Agent not found')

    try {
      const response = await $fetch('/api/agents/specialized/analyze', {
        method: 'POST',
        body: {
          agentId,
          analysisType,
          data
        }
      })

      return response.analysis

    } catch (error) {
      console.error('Error analyzing with agent:', error)
      throw error
    }
  }

  return {
    // State
    selectedAgent: readonly(selectedAgent),
    agentMessages: readonly(agentMessages),
    isLoading: readonly(isLoading),
    
    // Computed
    researchAgents,
    availableCapabilities,
    
    // Methods
    selectAgent,
    sendMessage,
    executeQuickAction,
    loadAgentConversation,
    clearConversation,
    getAgentByCapability,
    analyzeWithAgent
  }
}
