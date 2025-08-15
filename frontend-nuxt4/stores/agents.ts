import { defineStore } from 'pinia'
import { ref, computed, readonly } from 'vue'
import type { Agent, AgentType, AgentStatus, AgentInsight } from '../types/agents'

export const useAgentsStore = defineStore('agents', () => {
  // State
  const agents = ref<Map<string, Agent>>(new Map())
  const insights = ref<AgentInsight[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Initialize default agents
  const defaultAgents: Agent[] = [
    {
      id: 'boss_agent',
      name: 'Boss Agent',
      type: 'boss_agent',
      status: 'online',
      capabilities: ['coordination', 'strategy', 'overview'],
      description: 'Coordinates all specialist agents and provides strategic oversight',
    },
    {
      id: 'content_analysis',
      name: 'Content Analyst',
      type: 'content_analysis',
      status: 'online',
      capabilities: ['video_analysis', 'performance_metrics', 'content_optimization'],
      description: 'Analyzes video content performance and provides optimization recommendations',
    },
    {
      id: 'audience_insights',
      name: 'Audience Expert',
      type: 'audience_insights',
      status: 'online',
      capabilities: ['demographic_analysis', 'engagement_patterns', 'audience_growth'],
      description: 'Provides deep insights into audience behavior and growth opportunities',
    },
    {
      id: 'seo_discoverability',
      name: 'SEO Specialist',
      type: 'seo_discoverability',
      status: 'online',
      capabilities: ['keyword_optimization', 'search_ranking', 'discoverability'],
      description: 'Optimizes content for search and improves discoverability',
    },
    {
      id: 'monetization_strategy',
      name: 'Revenue Optimizer',
      type: 'monetization_strategy',
      status: 'online',
      capabilities: ['revenue_analysis', 'monetization_strategies', 'financial_optimization'],
      description: 'Analyzes revenue streams and suggests monetization improvements',
    },
    {
      id: 'competitive_analysis',
      name: 'Market Analyst',
      type: 'competitive_analysis',
      status: 'online',
      capabilities: ['competitor_tracking', 'market_trends', 'benchmarking'],
      description: 'Tracks competitors and identifies market opportunities',
    },
  ]

  // Getters
  const allAgents = computed(() => Array.from(agents.value.values()))
  const onlineAgents = computed(() => allAgents.value.filter(agent => agent.status === 'online'))
  const bossAgent = computed(() => agents.value.get('boss_agent'))

  const getAgentById = (id: string) => agents.value.get(id)

  // Actions
  const addInsight = (insight: AgentInsight) => {
    insights.value.unshift(insight)
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

  // Initialize agents on store creation
  initializeAgents()

  return {
    // State
    agents: readonly(agents),
    insights: readonly(insights),
    loading: readonly(loading),
    error: readonly(error),

    // Getters
    allAgents,
    onlineAgents,
    bossAgent,

    // Actions
    initializeAgents,
    updateAgentStatus,
    addInsight,
    getAgentById,
  }
})
