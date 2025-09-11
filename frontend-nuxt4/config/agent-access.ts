/**
 * Centralized Agent Access Control Configuration
 * Defines which agents are accessible for each subscription tier
 */

export type SubscriptionTier = 'basic' | 'pro' | 'enterprise' | 'teams'

export interface TierAgentAccess {
  [tier: string]: string[]
}

// Define which agents are available for each tier
export const TIER_AGENT_LIMITS: TierAgentAccess = {
  basic: ['boss_agent', 'agent_1', 'agent_2', 'agent_3'], // Boss Agent + Alex, Levi, Maya (4 agents)
  pro: ['boss_agent', 'agent_1', 'agent_2', 'agent_3', 'agent_4', 'agent_5'], // All 6 agents
  enterprise: ['boss_agent', 'agent_1', 'agent_2', 'agent_3', 'agent_4', 'agent_5'], // All 6 agents
  teams: ['boss_agent', 'agent_1', 'agent_2', 'agent_3', 'agent_4', 'agent_5'] // All 6 agents
}

// Map subscription IDs to tier names
export const SUBSCRIPTION_TIER_MAP: Record<string, SubscriptionTier> = {
  'basic': 'basic',
  'solo_pro': 'pro',
  'Solo Pro': 'pro',
  'pro': 'pro',
  'enterprise': 'enterprise',
  'teams': 'teams'
}

export const getAgentAccessForTier = (tier: SubscriptionTier): string[] => {
  return TIER_AGENT_LIMITS[tier] || TIER_AGENT_LIMITS.basic
}

export const getAgentAccessForSubscription = (subscriptionId: string): string[] => {
  const tier = SUBSCRIPTION_TIER_MAP[subscriptionId] || 'basic'
  return getAgentAccessForTier(tier)
}

export const isAgentAccessible = (agentId: string, subscriptionId: string): boolean => {
  const allowedAgents = getAgentAccessForSubscription(subscriptionId)
  return allowedAgents.includes(agentId)
}

export const getLockedAgents = (subscriptionId: string): string[] => {
  const allowedAgents = getAgentAccessForSubscription(subscriptionId)
  const allAgents = ['boss_agent', 'agent_1', 'agent_2', 'agent_3', 'agent_4', 'agent_5']
  return allAgents.filter(agentId => !allowedAgents.includes(agentId))
}

export const getAccessibleAgentCount = (subscriptionId: string): number => {
  return getAgentAccessForSubscription(subscriptionId).length
}

export const getLockedAgentCount = (subscriptionId: string): number => {
  return getLockedAgents(subscriptionId).length
}

export const getUpgradeMessage = (currentTier: SubscriptionTier): string => {
  switch (currentTier) {
    case 'basic':
      return 'Upgrade to Pro to unlock all specialist agents'
    default:
      return 'All agents are available on your current plan'
  }
}
