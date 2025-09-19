import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { SUBSCRIPTION_PLANS, type SubscriptionPlan, getPlanById } from '../config/subscription-plans'

export interface UserSubscription {
  id: string
  name: string
  status: 'active' | 'cancelled' | 'expired' | 'past_due'
  current_period_start: string
  current_period_end: string
  cancel_at_period_end: boolean
}

export interface UsageStats {
  period_start: string
  period_end: string
  plan_id: string
  usage: {
    [key: string]: {
      current_usage: number
      limit: number
      cost: number
      percentage_used: number
      remaining: number
    }
  }
  total_cost: number
}

export interface UsageAlert {
  id: string
  usage_type: string
  alert_type: 'warning' | 'limit_reached' | 'overage'
  current_usage: number
  usage_limit: number
  percentage_used: number
  message: string
  is_read: boolean
  created_at: string
}

export interface BillingHistoryItem {
  id: string
  description: string
  amount: number
  currency: string
  status: 'paid' | 'pending' | 'failed' | 'refunded'
  created_at: string
  invoice_url?: string
}

export const useSubscriptionStore = defineStore('subscription', () => {
  // Initialize Stripe composable
  const stripe = useStripe()

  // State
  const currentSubscription = ref<UserSubscription | null>({
    id: 'basic',
    name: 'Basic',
    status: 'active',
    current_period_start: new Date().toISOString(),
    current_period_end: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
    cancel_at_period_end: false
  })
  const availablePlans = ref<SubscriptionPlan[]>(SUBSCRIPTION_PLANS)
  const usage = ref<UsageStats | null>(null)
  const usageAlerts = ref<UsageAlert[]>([])
  const billingHistory = ref<BillingHistoryItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const stripeCustomerId = ref<string | null>(null)

  // Getters
  const isSubscribed = computed(() => 
    currentSubscription.value?.status === 'active'
  )
  
  const currentPlan = computed(() => {
    if (!currentSubscription.value) return null
    return getPlanById(currentSubscription.value.id)
  })

  const usagePercentage = computed(() => {
    if (!usage.value || !currentPlan.value) return {}
    
    const plan = currentPlan.value
    return {
      ai_requests: plan.limits.ai_requests === -1 ? 0 : 
        (usage.value.ai_requests / plan.limits.ai_requests) * 100,
      video_analysis: plan.limits.video_analysis === -1 ? 0 :
        (usage.value.video_analysis / plan.limits.video_analysis) * 100
    }
  })

  const isUsageLimitReached = computed(() => {
    if (!usage.value || !currentPlan.value) return false
    
    const plan = currentPlan.value
    return (
      (plan.limits.ai_requests !== -1 && usage.value.ai_requests >= plan.limits.ai_requests) ||
      (plan.limits.video_analysis !== -1 && usage.value.video_analysis >= plan.limits.video_analysis)
    )
  })

  // Actions
  const fetchPlans = async () => {
    try {
      loading.value = true
      error.value = null
      
      const { $api } = useNuxtApp()
      const response = await $api('/api/subscription/plans')
      
      if (response.status === 'success') {
        availablePlans.value = response.data.plans
      } else {
        throw new Error(response.error || 'Failed to fetch plans')
      }
    } catch (err: any) {
      error.value = err.message
      console.error('Error fetching subscription plans:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchCurrentSubscription = async () => {
    try {
      loading.value = true
      error.value = null
      
      const { $api } = useNuxtApp()
      const response = await $api('/api/subscription/current')
      
      if (response.status === 'success') {
        currentSubscription.value = response.data.subscription
      } else {
        throw new Error(response.error || 'Failed to fetch subscription')
      }
    } catch (err: any) {
      error.value = err.message
      console.error('Error fetching current subscription:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchUsage = async () => {
    try {
      const { $api } = useNuxtApp()
      const response = await $api('/api/subscription/usage')
      
      if (response.status === 'success') {
        usage.value = response.data.usage
      } else {
        throw new Error(response.error || 'Failed to fetch usage')
      }
    } catch (err: any) {
      error.value = err.message
      console.error('Error fetching usage:', err)
    }
  }

  const fetchBillingHistory = async () => {
    try {
      const { $api } = useNuxtApp()
      const response = await $api('/api/subscription/billing-history')
      
      if (response.status === 'success') {
        billingHistory.value = response.data.history
      } else {
        throw new Error(response.error || 'Failed to fetch billing history')
      }
    } catch (err: any) {
      error.value = err.message
      console.error('Error fetching billing history:', err)
    }
  }

  const createCheckoutSession = async (
    planId: string,
    billingCycle: 'monthly' | 'yearly' = 'monthly',
    teamSeats: number = 1,
    pricingType: 'fixed' | 'per_seat' = 'fixed'
  ) => {
    try {
      loading.value = true
      error.value = null

      const config = useRuntimeConfig()

      // Use GET endpoint to avoid request body parsing timeout
      const result = await $fetch('/api/stripe/create-checkout-session', {
        method: 'GET',
        baseURL: config.public.apiBase,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        },
        query: {
          plan_id: planId,
          billing_cycle: billingCycle,
          pricing_type: pricingType,
          customer_email: 'demo@example.com'
        }
      })

      if (result.checkout_url) {
        // Redirect to Stripe Checkout
        window.location.href = result.checkout_url
        await fetchCurrentSubscription()
      }

      return result
    } catch (err: any) {
      error.value = err.message
      console.error('Error creating checkout session:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const calculateTeamPrice = async (teamSeats: number, billingCycle: 'monthly' | 'yearly' = 'monthly') => {
    try {
      const { $api } = useNuxtApp()
      const result = await $api('/api/subscription/calculate-team-price', {
        method: 'POST',
        body: {
          team_seats: teamSeats,
          billing_cycle: billingCycle
        }
      })

      return result.data
    } catch (err: any) {
      console.error('Error calculating team price:', err)
      throw err
    }
  }

  // Create Stripe customer portal session
  const createPortalSession = async (customerId?: string) => {
    try {
      loading.value = true
      error.value = null

      const config = useRuntimeConfig()

      // Use new Stripe API endpoint
      const result = await $fetch('/api/stripe/create-portal-session', {
        method: 'POST',
        baseURL: config.public.apiBase,
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'Content-Type': 'application/json'
        },
        body: {
          customer_id: customerId || stripeCustomerId.value,
          return_url: `${window.location.origin}/settings`
        }
      })

      if (result.success) {
        // Redirect to Stripe Customer Portal
        if (result.data.portal_url) {
          window.location.href = result.data.portal_url
        }
      }

      return result
    } catch (err: any) {
      error.value = err.message
      console.error('Error creating portal session:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const cancelSubscription = async () => {
    try {
      loading.value = true
      error.value = null
      
      const { $api } = useNuxtApp()
      const response = await $api('/api/subscription/cancel', {
        method: 'POST'
      })
      
      if (response.status === 'success') {
        // Refresh subscription data
        await fetchCurrentSubscription()
        return true
      } else {
        throw new Error(response.error || 'Failed to cancel subscription')
      }
    } catch (err: any) {
      error.value = err.message
      console.error('Error cancelling subscription:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  const trackUsage = async (
    usageType: string,
    amount: number = 1,
    costEstimate: number = 0,
    metadata: Record<string, any> = {}
  ) => {
    try {
      const { $api } = useNuxtApp()
      await $api('/api/subscription/track-usage', {
        method: 'POST',
        body: {
          usage_type: usageType,
          amount,
          cost_estimate: costEstimate,
          metadata
        }
      })

      // Refresh usage data
      await fetchUsage()
    } catch (err: any) {
      console.error('Error tracking usage:', err)
      throw err
    }
  }

  const checkUsageLimit = async (usageType: string) => {
    try {
      const { $api } = useNuxtApp()
      const result = await $api(`/api/subscription/check-limit/${usageType}`)
      return result.data
    } catch (err: any) {
      console.error('Error checking usage limit:', err)
      throw err
    }
  }

  const fetchUsageAlerts = async (unreadOnly: boolean = true) => {
    try {
      const { $api } = useNuxtApp()
      const result = await $api('/api/subscription/alerts', {
        method: 'GET',
        query: { unread_only: unreadOnly }
      })

      usageAlerts.value = result.data.alerts
      return result.data.alerts
    } catch (err: any) {
      console.error('Error fetching usage alerts:', err)
      throw err
    }
  }

  const markAlertRead = async (alertId: string) => {
    try {
      const { $api } = useNuxtApp()
      await $api(`/api/subscription/alerts/${alertId}/read`, {
        method: 'POST'
      })

      // Refresh alerts
      await fetchUsageAlerts()
    } catch (err: any) {
      console.error('Error marking alert as read:', err)
      throw err
    }
  }

  const initializeSubscription = async () => {
    await Promise.all([
      fetchPlans(),
      fetchCurrentSubscription(),
      fetchUsage(),
      fetchUsageAlerts(),
      fetchBillingHistory()
    ])
  }

  return {
    // State
    currentSubscription,
    availablePlans,
    usage,
    usageAlerts,
    billingHistory,
    loading,
    error,

    // Getters
    isSubscribed,
    currentPlan,
    usagePercentage,
    isUsageLimitReached,

    // Actions
    fetchPlans,
    fetchCurrentSubscription,
    fetchUsage,
    fetchUsageAlerts,
    fetchBillingHistory,
    createCheckoutSession,
    createPortalSession,
    cancelSubscription,
    trackUsage,
    checkUsageLimit,
    markAlertRead,
    calculateTeamPrice,
    initializeSubscription
  }
})
