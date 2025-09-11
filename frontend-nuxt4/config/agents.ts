/**
 * Centralized Agent Configuration
 * Single source of truth for all agent data across the application
 */

export interface Agent {
  id: string
  name: string
  type: string
  status: 'online' | 'offline' | 'busy' | 'thinking'
  capabilities: string[]
  description: string
  avatar: string
  color: string
  personality: string
  specialization: string
  lastActive?: Date
}

// Centralized agent colors - matches user's memory preferences
export const AGENT_COLORS = {
  boss_agent: '#f97316', // Orange
  agent_1: '#f97316',    // Alex - Orange  
  agent_2: '#3b82f6',    // Levi - Blue
  agent_3: '#a855f7',    // Maya - Purple
  agent_4: '#eab308',    // Zara - Yellow
  agent_5: '#16a34a'     // Kai - Green
} as const

export const AGENTS: Agent[] = [
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
    description: 'Your Team Leader - Coordinates with specialized team members to provide comprehensive support',
    avatar: '/BossAgent.png',
    color: AGENT_COLORS.boss_agent,
    personality: 'Leads your AI team and coordinates with specialized team members',
    specialization: 'Team Leader',
  },
  {
    id: 'agent_1',
    name: 'Alex',
    type: 'analytics_agent',
    status: 'online',
    capabilities: [
      'youtube_analytics',
      'performance_metrics',
      'growth_analysis',
      'competitive_research',
      'roi_optimization',
    ],
    description: 'Analytics Team Member - Collaborates with team on data-driven insights for YouTube growth',
    avatar: '/Alex.png',
    color: AGENT_COLORS.agent_1,
    personality: 'Data-driven and analytical, focuses on metrics and strategic insights',
    specialization: 'Analytics Specialist',
  },
  {
    id: 'agent_2',
    name: 'Levi',
    type: 'content_agent',
    status: 'online',
    capabilities: [
      'content_strategy',
      'creative_ideation',
      'video_optimization',
      'trend_analysis',
      'storytelling',
    ],
    description: 'Content Team Member - Works with team on creative and innovative content strategy',
    avatar: '/Levi.png',
    color: AGENT_COLORS.agent_2,
    personality: 'Creative and energetic, passionate about content creation and storytelling',
    specialization: 'Content Strategist',
  },
  {
    id: 'agent_3',
    name: 'Maya',
    type: 'engagement_agent',
    status: 'online',
    capabilities: [
      'audience_engagement',
      'community_building',
      'social_strategy',
      'interaction_optimization',
      'retention_analysis',
    ],
    description: 'Engagement Team Member - Collaborates with team on community-focused audience growth strategies',
    avatar: '/Maya.png',
    color: AGENT_COLORS.agent_3,
    personality: 'Warm and community-focused, excels at building audience relationships',
    specialization: 'Engagement Specialist',
  },
  {
    id: 'agent_4',
    name: 'Zara',
    type: 'growth_agent',
    status: 'online',
    capabilities: [
      'growth_strategy',
      'optimization',
      'scaling_tactics',
      'conversion_optimization',
      'performance_enhancement',
    ],
    description: 'Growth Team Member - Works with team on results-driven strategies for channel growth',
    avatar: '/Zara.png',
    color: AGENT_COLORS.agent_4,
    personality: 'Results-driven and ambitious, focused on scaling and optimization',
    specialization: 'Growth Strategist',
  },
  {
    id: 'agent_5',
    name: 'Kai',
    type: 'technical_agent',
    status: 'online',
    capabilities: [
      'technical_optimization',
      'seo_strategy',
      'algorithm_analysis',
      'platform_mechanics',
      'technical_troubleshooting',
    ],
    description: 'Technical Team Member - Coordinates with team on technical and detail-oriented optimization',
    avatar: '/Kai.png',
    color: AGENT_COLORS.agent_5,
    personality: 'Detail-oriented and systematic, excels at technical optimization',
    specialization: 'Technical Specialist',
  },
]

export const getAgentById = (id: string): Agent | undefined => {
  return AGENTS.find(agent => agent.id === id)
}

export const getAgentByName = (name: string): Agent | undefined => {
  return AGENTS.find(agent => agent.name.toLowerCase() === name.toLowerCase())
}

export const getAgentsByType = (type: string): Agent[] => {
  return AGENTS.filter(agent => agent.type === type)
}

export const getOnlineAgents = (): Agent[] => {
  return AGENTS.filter(agent => agent.status === 'online')
}

export const getAgentColor = (agentId: string): string => {
  const agent = getAgentById(agentId)
  return agent?.color || AGENT_COLORS.boss_agent
}
