import { loadStripe, type Stripe } from '@stripe/stripe-js'
import { ref } from 'vue'

// Stripe instance
let stripeInstance: Stripe | null = null

export const useStripe = () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Initialize Stripe
  const initStripe = async () => {
    if (stripeInstance) return stripeInstance

    try {
      // Use your Stripe publishable key from environment
      const runtimeConfig = useRuntimeConfig()
      const publishableKey = runtimeConfig.public.stripePublishableKey
      stripeInstance = await loadStripe(publishableKey)
      return stripeInstance
    } catch (err) {
      error.value = 'Failed to initialize Stripe'
      console.error('Stripe initialization error:', err)
      return null
    }
  }

  // Create checkout session
  const createCheckoutSession = async (priceId: string, customerId?: string) => {
    loading.value = true
    error.value = null

    try {
      // In a real app, this would call your backend API
      // For now, we'll simulate the checkout process
      
      const response = await $fetch('/api/stripe/create-checkout-session', {
        method: 'POST',
        body: {
          priceId,
          customerId,
          successUrl: `${window.location.origin}/settings?success=true`,
          cancelUrl: `${window.location.origin}/settings?canceled=true`
        }
      })

      const stripe = await initStripe()
      if (!stripe) throw new Error('Stripe not initialized')

      // Redirect to Stripe Checkout
      const { error: stripeError } = await stripe.redirectToCheckout({
        sessionId: response.sessionId
      })

      if (stripeError) {
        throw new Error(stripeError.message)
      }

    } catch (err: any) {
      error.value = err.message || 'Failed to create checkout session'
      console.error('Checkout error:', err)
    } finally {
      loading.value = false
    }
  }

  // Create customer portal session
  const createPortalSession = async (customerId: string) => {
    loading.value = true
    error.value = null

    try {
      const response = await $fetch('/api/stripe/create-portal-session', {
        method: 'POST',
        body: {
          customerId,
          returnUrl: `${window.location.origin}/settings`
        }
      })

      // Redirect to customer portal
      window.location.href = response.url

    } catch (err: any) {
      error.value = err.message || 'Failed to access billing portal'
      console.error('Portal error:', err)
    } finally {
      loading.value = false
    }
  }

  // Mock functions for demo (remove when backend is ready)
  const mockCheckoutSession = async (planId: string, billingCycle: 'monthly' | 'yearly') => {
    loading.value = true
    error.value = null

    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Simulate successful checkout
      console.log(`Mock checkout for plan: ${planId}, billing: ${billingCycle}`)
      
      // In demo mode, just show success message
      return {
        success: true,
        message: `Successfully initiated checkout for ${planId} plan (${billingCycle})`
      }

    } catch (err: any) {
      error.value = err.message || 'Checkout failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const mockPortalSession = async () => {
    loading.value = true
    error.value = null

    try {
      await new Promise(resolve => setTimeout(resolve, 500))
      
      return {
        success: true,
        message: 'Billing portal would open here'
      }

    } catch (err: any) {
      error.value = err.message || 'Portal access failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Stripe price IDs (replace with your actual price IDs)
  const priceIds = {
    starter: {
      monthly: 'price_starter_monthly',
      yearly: 'price_starter_yearly'
    },
    growth: {
      monthly: 'price_growth_monthly', 
      yearly: 'price_growth_yearly'
    },
    pro: {
      monthly: 'price_pro_monthly',
      yearly: 'price_pro_yearly'
    }
  }

  return {
    loading: readonly(loading),
    error: readonly(error),
    initStripe,
    createCheckoutSession,
    createPortalSession,
    mockCheckoutSession,
    mockPortalSession,
    priceIds
  }
}
