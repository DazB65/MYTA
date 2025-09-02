import { defineStore } from 'pinia'
import { computed, readonly, ref } from 'vue'
import type { Agent, AgentInsight, AgentStatus, ChatSession } from '../types/agents'

export const useAgentsStore = defineStore('agents', () => {
  // State
  const agents = ref<Map<string, Agent>>(new Map())
  const insights = ref<AgentInsight[]>([])
  const activeChatSessions = ref<Map<string, ChatSession>>(new Map())
  const currentChatSession = ref<ChatSession | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const isConnected = ref(false)
  const lastHeartbeat = ref<Date | null>(null)

  // Initialize default AI team members with color-coded personalities - matching backend
  const defaultAgents: Agent[] = [
    {
      id: 'boss_agent',
      name: 'Boss Agent',
      type: 'boss_agent',
      status: 'online',
      capabilities: [
        'team_coordination',
        'task_management',
        'agent_delegation',
        'comprehensive_analysis',
        'user_interaction',
      ],
      description:
        'Your Team Leader - Coordinates with specialized team members to provide comprehensive support',
      avatar: '/BossAgent.png',
      color: '#f97316', // Orange - primary brand color
      personality: 'Leads your AI team and coordinates with specialized team members',
      specialization: 'Team Leader',
    },
    {
      id: 'agent_1',
      name: 'Alex',
      type: 'content_analysis',
      status: 'online',
      capabilities: [
        'team_video_analysis',
        'collaborative_metrics',
        'team_optimization',
        'viral_potential',
      ],
      description:
        'Analytics Team Member - Collaborates with team on data-driven insights for YouTube growth',
      avatar: '/optimized/Agent1.jpg',
      color: '#3b82f6', // Blue
      personality: 'Data-driven team member who collaborates on strategic insights',
      specialization: 'Analytics Team Member',
    },
    {
      id: 'agent_2',
      name: 'Levi',
      type: 'audience_insights',
      status: 'online',
      capabilities: [
        'team_content_creation',
        'collaborative_strategy',
        'video_production',
        'storytelling',
      ],
      description: 'Content Team Member - Works with team on creative and innovative content strategy',
      avatar: '/optimized/Agent2.jpg',
      color: '#eab308', // Yellow
      personality: 'Creative team member who works with others on content strategy',
      specialization: 'Content Team Member',
    },
    {
      id: 'agent_3',
      name: 'Maya',
      type: 'seo_discoverability',
      status: 'online',
      capabilities: [
        'team_audience_engagement',
        'collaborative_community_building',
        'social_interaction',
        'relationship_management',
      ],
      description:
        'Engagement Team Member - Collaborates with team on community-focused audience growth strategies',
      avatar: '/optimized/Agent3.jpg',
      color: '#16a34a', // Green
      personality: 'Community-focused team member who collaborates on audience strategy',
      specialization: 'Engagement Team Member',
    },
    {
      id: 'agent_4',
      name: 'Zara',
      type: 'competitive_analysis',
      status: 'online',
      capabilities: ['team_growth_strategy', 'collaborative_optimization', 'performance_analysis', 'scaling'],
      description: 'Growth Team Member - Works with team on results-driven strategies for channel growth',
      avatar: '/optimized/Agent4.jpg',
      color: '#a855f7', // Purple
      personality: 'Results-driven team member who works with others on optimization',
      specialization: 'Growth Team Member',
    },
    {
      id: 'agent_5',
      name: 'Kai',
      type: 'monetization_strategy',
      status: 'online',
      capabilities: [
        'team_technical_optimization',
        'collaborative_seo_analysis',
        'algorithm_insights',
        'technical_strategy',
      ],
      description: 'Technical Team Member - Coordinates with team on technical and detail-oriented optimization',
      avatar: '/optimized/Agent5.jpg',
      color: '#dc2626', // Red
      personality: 'Technical team member who coordinates on SEO and optimization',
      specialization: 'Technical Team Member',
    },
  ]

  // Getters
  const allAgents = computed(() => Array.from(agents.value.values()))
  const onlineAgents = computed(() => allAgents.value.filter(agent => agent.status === 'online'))
  const bossAgent = computed(() => agents.value.get('boss_agent'))
  const agentsByType = computed(() => {
    const byType: Record<string, Agent[]> = {}
    allAgents.value.forEach(agent => {
      if (!byType[agent.type]) byType[agent.type] = []
      byType[agent.type].push(agent)
    })
    return byType
  })

  const activeChats = computed(() => Array.from(activeChatSessions.value.values()))
  const recentInsights = computed(() =>
    insights.value.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime()).slice(0, 10)
  )

  const agentStats = computed(() => ({
    total: allAgents.value.length,
    online: onlineAgents.value.length,
    busy: allAgents.value.filter(a => a.status === 'busy').length,
    thinking: allAgents.value.filter(a => a.status === 'thinking').length,
  }))

  const getAgentById = (id: string) => agents.value.get(id)
  const getAgentByColor = (color: string) => allAgents.value.find(agent => agent.color === color)
  const getChatSession = (sessionId: string) => activeChatSessions.value.get(sessionId)

  // Actions
  const addInsight = (insight: AgentInsight) => {
    insights.value.unshift(insight)
    // Keep only last 100 insights
    if (insights.value.length > 100) {
      insights.value = insights.value.slice(0, 100)
    }
  }

  const initializeAgents = () => {
    defaultAgents.forEach(agent => {
      agents.value.set(agent.id, {
        ...agent,
        lastActive: new Date(),
      })
    })
  }

  const updateAgentStatus = (agentId: string, status: AgentStatus) => {
    const agent = agents.value.get(agentId)
    if (agent) {
      agent.status = status
      agent.lastActive = new Date()
    }
  }

  const createChatSession = (agentId: string, userId: string): ChatSession => {
    const sessionId = `chat_${agentId}_${Date.now()}`
    const session: ChatSession = {
      id: sessionId,
      userId,
      agentId,
      title: `Chat with ${getAgentById(agentId)?.name || 'Agent'}`,
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
      isActive: true,
    }
    activeChatSessions.value.set(sessionId, session)
    return session
  }

  const setCurrentChatSession = (sessionId: string | null) => {
    if (sessionId) {
      currentChatSession.value = activeChatSessions.value.get(sessionId) || null
    } else {
      currentChatSession.value = null
    }
  }

  const addMessageToSession = (
    sessionId: string,
    message: Omit<ChatMessage, 'id' | 'timestamp'>
  ) => {
    const session = activeChatSessions.value.get(sessionId)
    if (session) {
      const fullMessage: ChatMessage = {
        ...message,
        id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        timestamp: new Date(),
      }
      session.messages.push(fullMessage)
      session.updatedAt = new Date()
    }
  }

  const updateConnectionStatus = (connected: boolean) => {
    isConnected.value = connected
    lastHeartbeat.value = connected ? new Date() : null
  }

  const setLoading = (loading: boolean) => {
    loading.value = loading
  }

  const setError = (errorMessage: string | null) => {
    error.value = errorMessage
  }

  // Initialize agents on store creation
  initializeAgents()

  return {
    // State
    agents: readonly(agents),
    insights: readonly(insights),
    activeChatSessions: readonly(activeChatSessions),
    currentChatSession: readonly(currentChatSession),
    loading: readonly(loading),
    error: readonly(error),
    isConnected: readonly(isConnected),
    lastHeartbeat: readonly(lastHeartbeat),

    // Getters
    allAgents,
    onlineAgents,
    bossAgent,
    agentsByType,
    activeChats,
    recentInsights,
    agentStats,

    // Actions
    initializeAgents,
    updateAgentStatus,
    addInsight,
    getAgentById,
    getAgentByColor,
    getChatSession,
    createChatSession,
    setCurrentChatSession,
    addMessageToSession,
    updateConnectionStatus,
    setLoading,
    setError,
  }
})
