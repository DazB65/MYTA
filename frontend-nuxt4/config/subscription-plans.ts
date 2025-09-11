/**
 * Centralized Subscription Plans Configuration
 * Single source of truth for all plan data across the application
 */

// Import shared configuration

export interface SubscriptionPlan {
  id: string
  name: string
  description: string
  price: {
    monthly: number
    yearly: number
    per_seat?: number
  }
  popular?: boolean
  agentAccess: {
    total: number
    agents: string[]
    locked: string[]
  }
  features: string[]
  limits: {
    ai_conversations: number
    agents_count: number
    content_pillars: number
    goals: number
    competitors: number
    team_members: number
    max_team_members?: number
    research_projects: number
    video_analysis: number
    team_collaboration: boolean
  }
  trial_days?: number
}

// Transform shared data to frontend format
const transformPlanData = (plan: any): SubscriptionPlan => ({
  id: plan.id,
  name: plan.name,
  description: plan.description,
  price: {
    monthly: plan.price_monthly,
    yearly: plan.price_yearly,
    per_seat: plan.price_per_seat
  },
  popular: plan.popular || false,
  agentAccess: plan.agent_access,
  features: plan.features,
  limits: plan.limits,
  trial_days: plan.trial_days
})

// Use shared configuration data
export const SUBSCRIPTION_PLANS: SubscriptionPlan[] = [
  {
    id: 'basic',
    name: 'Basic',
    description: 'Perfect for new YouTubers getting started',
    price: { monthly: 4.99, yearly: 49.99 },
    popular: false,
    agentAccess: {
      total: 4,
      agents: ['Boss Agent', 'Alex', 'Levi', 'Maya'],
      locked: ['Zara', 'Kai']
    },
    features: [
      'Boss Agent + 3 specialist agents',
      '50 AI conversations/month',
      'Basic content pillars (up to 3)',
      'Task management (up to 25 tasks)',
      'Goal tracking (5 goals)',
      '10 video analyses/month',
      '5 research projects/month',
      'Email support (48h response)'
    ],
    limits: {
      ai_conversations: 50,
      agents_count: 4,
      content_pillars: 3,
      goals: 5,
      competitors: 2,
      team_members: 1,
      research_projects: 5,
      video_analysis: 10,
      team_collaboration: false
    }
  },
  {
    id: 'solo_pro',
    name: 'Solo Pro',
    description: 'For serious creators ready to scale',
    price: { monthly: 14.99, yearly: 149.99 },
    popular: true,
    agentAccess: {
      total: 6,
      agents: ['Boss Agent', 'Alex', 'Levi', 'Maya', 'Zara', 'Kai'],
      locked: []
    },
    features: [
      'All 6 AI agents with full access',
      '100 AI conversations/month',
      'Content pillars (up to 10)',
      'Advanced task management (unlimited)',
      'Unlimited goal tracking',
      '25 video analyses/month',
      'Unlimited research projects',
      'Advanced analytics and insights',
      'Priority support (24h response)',
      'Custom agent personalities'
    ],
    limits: {
      ai_conversations: 100,
      agents_count: 6,
      content_pillars: 10,
      goals: -1, // unlimited
      competitors: 5,
      team_members: 1,
      research_projects: -1, // unlimited
      video_analysis: 25,
      team_collaboration: false
    },
    trial_days: 14
  },
  {
    id: 'teams',
    name: 'Teams',
    description: 'For agencies and multi-channel operations',
    price: { monthly: 29.99, yearly: 299.99, per_seat: 9.99 },
    popular: false,
    agentAccess: {
      total: 6,
      agents: ['Boss Agent', 'Alex', 'Levi', 'Maya', 'Zara', 'Kai'],
      locked: []
    },
    features: [
      'All 6 AI agents with team collaboration',
      '250 AI conversations/month (shared across team)',
      'Content pillars (up to 10)',
      'Advanced task management (unlimited)',
      'Unlimited goal tracking',
      '50 video analyses/month (shared across team)',
      'Unlimited research projects',
      'Team collaboration features',
      'Team notes and shared workspaces',
      'Role-based permissions',
      'Advanced team analytics',
      'Priority support (12h response)',
      'Custom integrations'
    ],
    limits: {
      ai_conversations: 250,
      agents_count: 6,
      content_pillars: 10,
      goals: -1, // unlimited
      competitors: 10,
      team_members: 1, // base plan includes 1 seat
      max_team_members: 20,
      research_projects: -1, // unlimited
      video_analysis: 50,
      team_collaboration: true
    },
    trial_days: 14
  }
]

export const getPlanById = (planId: string): SubscriptionPlan | undefined => {
  return SUBSCRIPTION_PLANS.find(plan => plan.id === planId)
}

export const getAgentAccessForPlan = (planId: string) => {
  const plan = getPlanById(planId)
  return plan?.agentAccess || { total: 4, agents: [], locked: [] }
}
