import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export interface SubscriptionPlan {
  id: string
  name: string
  price_monthly: number
  price_yearly: number
  features: string[]
  limits: {
    ai_requests: number
    video_analysis: number
  }
}

export interface UserSubscription {
  id: string
  name: string
  status: 'active' | 'cancelled' | 'expired' | 'past_due'
  current_period_start: string
  current_period_end: string
  cancel_at_period_end: boolean
}

export interface UsageStats {
  ai_requests: number
  video_analysis: number
  period_start: string
  period_end: string
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
  // State
  const currentSubscription = ref<UserSubscription | null>(null)
  const availablePlans = ref<SubscriptionPlan[]>([])
  const usage = ref<UsageStats | null>(null)
  const billingHistory = ref<BillingHistoryItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isSubscribed = computed(() => 
    currentSubscription.value?.status === 'active'
  )
  
  const currentPlan = computed(() => {
    if (!currentSubscription.value) return null
    return availablePlans.value.find(plan => plan.id === currentSubscription.value?.id)
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

  const createCheckoutSession = async (planId: string, billingCycle: 'monthly' | 'yearly' = 'monthly') => {
    try {
      loading.value = true
      error.value = null
      
      const { $api } = useNuxtApp()
      const response = await $api('/api/subscription/checkout', {
        method: 'POST',
        body: {
          plan_id: planId,
          billing_cycle: billingCycle
        }
      })
      
      if (response.status === 'success') {
        // Redirect to LemonSqueezy checkout
        window.location.href = response.data.checkout_url
      } else {
        throw new Error(response.error || 'Failed to create checkout session')
      }
    } catch (err: any) {
      error.value = err.message
      console.error('Error creating checkout session:', err)
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

  const trackUsage = async (usageType: 'ai_request' | 'video_analysis', amount: number = 1) => {
    try {
      const { $api } = useNuxtApp()
      await $api('/api/subscription/track-usage', {
        method: 'POST',
        body: {
          usage_type: usageType,
          amount
        }
      })
      
      // Refresh usage data
      await fetchUsage()
    } catch (err: any) {
      console.error('Error tracking usage:', err)
    }
  }

  const initializeSubscription = async () => {
    await Promise.all([
      fetchPlans(),
      fetchCurrentSubscription(),
      fetchUsage(),
      fetchBillingHistory()
    ])
  }

  return {
    // State
    currentSubscription,
    availablePlans,
    usage,
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
    fetchBillingHistory,
    createCheckoutSession,
    cancelSubscription,
    trackUsage,
    initializeSubscription
  }
})
