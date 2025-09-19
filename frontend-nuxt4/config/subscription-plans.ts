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
    per_seat_monthly?: number
    per_seat_yearly?: number
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
    per_seat_monthly: plan.price_per_seat_monthly,
    per_seat_yearly: plan.price_per_seat_yearly
  },
  popular: plan.popular || false,
  agentAccess: plan.agent_access,
  features: plan.features,
  limits: plan.limits,
  trial_days: plan.trial_days
})

// Stripe Price IDs for MYTA billing plans
export const STRIPE_PRICE_IDS = {
  basic: {
    monthly: 'price_1S8pq3A4NbLKuuGeAXxxeENx',
    yearly: 'price_1S8pr7A4NbLKuuGeFTQs4lG5'
  },
  solo_pro: {
    monthly: 'price_1S8pucA4NbLKuuGeU13Jvpfa',
    yearly: 'price_1S8pv4A4NbLKuuGe5Cs1xl8O'
  },
  teams: {
    monthly: 'price_1S8pw0A4NbLKuuGeVAJjroZG',
    yearly: 'price_1S8pwNA4NbLKuuGeTBVbDjLP',
    monthly_per_seat: 'price_1S8pzaA4NbLKuuGeHnVRJfTc',
    yearly_per_seat: 'price_1S8q01A4NbLKuuGeeYQ1Dav1'
  }
}

// Use shared configuration data
export const SUBSCRIPTION_PLANS: SubscriptionPlan[] = [
  {
    id: 'basic',
    name: 'MYTA Basic',
    description: 'Perfect for new YouTubers getting started - Boss Agent + 3 specialist agents with 50 AI conversations per month',
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
    name: 'MYTA Solo Pro',
    description: 'For serious content creators - Boss Agent + 5 specialist agents with 200 AI conversations per month plus priority support',
    price: { monthly: 14.99, yearly: 149.99 },
    popular: true,
    agentAccess: {
      total: 6,
      agents: ['Boss Agent', 'Alex', 'Levi', 'Maya', 'Zara', 'Kai'],
      locked: []
    },
    features: [
      'Boss Agent + 5 specialist agents',
      '200 AI conversations/month',
      'Content pillars (up to 10)',
      'Advanced task management (unlimited)',
      'Unlimited goal tracking',
      '50 video analyses/month',
      'Unlimited research projects',
      'Advanced analytics and insights',
      'Priority support (24h response)',
      'Custom agent personalities'
    ],
    limits: {
      ai_conversations: 200,
      agents_count: 6,
      content_pillars: 10,
      goals: -1, // unlimited
      competitors: 5,
      team_members: 1,
      research_projects: -1, // unlimited
      video_analysis: 50,
      team_collaboration: false
    },
    trial_days: 14
  },
  {
    id: 'teams',
    name: 'MYTA Teams',
    description: 'For agencies and teams - Boss Agent + 5 specialist agents with unlimited AI conversations, team collaboration, and dedicated support',
    price: { monthly: 49.99, yearly: 499.99, per_seat_monthly: 9.99, per_seat_yearly: 99.99 },
    popular: false,
    agentAccess: {
      total: 6,
      agents: ['Boss Agent', 'Alex', 'Levi', 'Maya', 'Zara', 'Kai'],
      locked: []
    },
    features: [
      'Boss Agent + 5 specialist agents',
      'Unlimited AI conversations',
      'Team collaboration features',
      'Content pillars (unlimited)',
      'Advanced task management (unlimited)',
      'Unlimited goal tracking',
      'Unlimited video analyses',
      'Unlimited research projects',
      'Team notes and shared workspaces',
      'Role-based permissions',
      'Advanced team analytics',
      'Dedicated support (12h response)',
      'Custom integrations',
      'Flexible per-seat pricing available'
    ],
    limits: {
      ai_conversations: -1, // unlimited
      agents_count: 6,
      content_pillars: -1, // unlimited
      goals: -1, // unlimited
      competitors: -1, // unlimited
      team_members: 1, // base plan includes 1 seat
      max_team_members: 50,
      research_projects: -1, // unlimited
      video_analysis: -1, // unlimited
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
