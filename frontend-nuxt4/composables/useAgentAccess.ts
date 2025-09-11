import { computed } from 'vue'
import {
    SUBSCRIPTION_TIER_MAP,
    TIER_AGENT_LIMITS,
    getAgentAccessForSubscription
} from '../config/agent-access'
import { useAgentsStore } from '../stores/agents'
import { useSubscriptionStore } from '../stores/subscription'

export interface AgentAccessInfo {
  agent: any
  isAccessible: boolean
  isLocked: boolean
  lockReason?: string
  upgradeRequired?: string
}

export const useAgentAccess = () => {
  const agentsStore = useAgentsStore()
  const subscriptionStore = useSubscriptionStore()

  // Get current subscription tier (with fallback to basic)
  const currentTier = computed(() => {
    const subscription = subscriptionStore.currentSubscription
    if (!subscription) return 'basic'
    return SUBSCRIPTION_TIER_MAP[subscription.id] || 'basic'
  })

  // Get allowed agent IDs for current tier
  const allowedAgentIds = computed(() => {
    const subscription = subscriptionStore.currentSubscription
    if (!subscription) return TIER_AGENT_LIMITS.basic
    return getAgentAccessForSubscription(subscription.id)
  })

  // Get all agents with access information
  const agentsWithAccess = computed((): AgentAccessInfo[] => {
    return agentsStore.allAgents.map(agent => {
      const isAccessible = allowedAgentIds.value.includes(agent.id)
      const isLocked = !isAccessible
      
      let lockReason = ''
      let upgradeRequired = ''
      
      if (isLocked) {
        lockReason = currentTier.value === 'basic' ? 'Upgrade to Solo Pro to unlock this agent' : 'Upgrade to access this agent'
        upgradeRequired = currentTier.value === 'basic' ? 'pro' : ''
      }

      return {
        agent,
        isAccessible,
        isLocked,
        lockReason,
        upgradeRequired
      }
    })
  })

  // Get only accessible agents
  const accessibleAgents = computed(() => {
    return agentsWithAccess.value
      .filter(info => info.isAccessible)
      .map(info => info.agent)
  })

  // Get only locked agents
  const lockedAgents = computed(() => {
    return agentsWithAccess.value
      .filter(info => info.isLocked)
      .map(info => info.agent)
  })

  // Check if a specific agent is accessible
  const isAgentAccessible = (agentId: string): boolean => {
    const subscription = subscriptionStore.currentSubscription
    if (!subscription) return TIER_AGENT_LIMITS.basic.includes(agentId)
    const tier = SUBSCRIPTION_TIER_MAP[subscription.id] || 'basic'
    return TIER_AGENT_LIMITS[tier].includes(agentId)
  }

  // Get access info for a specific agent
  const getAgentAccessInfo = (agentId: string): AgentAccessInfo | null => {
    return agentsWithAccess.value.find(info => info.agent.id === agentId) || null
  }

  // Get upgrade message for locked features
  const getUpgradeMessage = (agentId: string): string => {
    const accessInfo = getAgentAccessInfo(agentId)
    if (!accessInfo || accessInfo.isAccessible) return ''
    
    return accessInfo.lockReason || 'Upgrade your plan to access this agent'
  }

  // Check if user can access agent chat
  const canAccessAgentChat = (agentId: string): boolean => {
    return isAgentAccessible(agentId)
  }

  // Get locked agents count
  const lockedAgentsCount = computed(() => {
    return lockedAgents.value.length
  })

  // Get accessible agents count  
  const accessibleAgentsCount = computed(() => {
    return accessibleAgents.value.length
  })

  return {
    // Computed properties
    currentTier,
    allowedAgentIds,
    agentsWithAccess,
    accessibleAgents,
    lockedAgents,
    lockedAgentsCount,
    accessibleAgentsCount,

    // Methods
    isAgentAccessible,
    getAgentAccessInfo,
    getUpgradeMessage,
    canAccessAgentChat
  }
}
