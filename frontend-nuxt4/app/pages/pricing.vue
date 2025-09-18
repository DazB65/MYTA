<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="text-center">
          <h1 class="text-4xl font-bold text-gray-900 mb-4">
            Choose Your MYTA Plan
          </h1>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            Unlock the power of AI-driven YouTube growth with our flexible pricing plans.
            Start with Basic and scale as you grow.
          </p>
        </div>
        
        <!-- Billing Toggle -->
        <div class="flex justify-center mt-8">
          <div class="bg-gray-100 p-1 rounded-lg">
            <button
              @click="billingCycle = 'monthly'"
              :class="[
                'px-4 py-2 rounded-md text-sm font-medium transition-colors',
                billingCycle === 'monthly'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-500 hover:text-gray-900'
              ]"
            >
              Monthly
            </button>
            <button
              @click="billingCycle = 'yearly'"
              :class="[
                'px-4 py-2 rounded-md text-sm font-medium transition-colors',
                billingCycle === 'yearly'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-500 hover:text-gray-900'
              ]"
            >
              Yearly
              <span class="ml-1 text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                Save 17%
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Pricing Cards -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Basic Plan -->
        <div class="bg-white rounded-lg shadow-lg p-8 relative">
          <div class="text-center">
            <h3 class="text-2xl font-bold text-gray-900 mb-2">MYTA Basic</h3>
            <p class="text-gray-600 mb-6">Perfect for new YouTubers getting started</p>
            
            <div class="mb-6">
              <span class="text-4xl font-bold text-gray-900">
                ${{ billingCycle === 'monthly' ? '4.99' : '49.99' }}
              </span>
              <span class="text-gray-600">
                /{{ billingCycle === 'monthly' ? 'month' : 'year' }}
              </span>
            </div>

            <ul class="text-left space-y-3 mb-8">
              <li class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Boss Agent + 3 specialist agents
              </li>
              <li class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                50 AI conversations/month
              </li>
              <li class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Basic content pillars (up to 3)
              </li>
              <li class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Email support (48h response)
              </li>
            </ul>

            <button
              @click="selectPlan('basic')"
              class="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              Get Started
            </button>
          </div>
        </div>

        <!-- Solo Pro Plan -->
        <div class="bg-white rounded-lg shadow-lg p-8 relative border-2 border-blue-500">
          <!-- Popular Badge -->
          <div class="absolute -top-4 left-1/2 transform -translate-x-1/2">
            <span class="bg-blue-500 text-white px-4 py-1 rounded-full text-sm font-medium">
              Most Popular
            </span>
          </div>
          
          <div class="text-center">
            <h3 class="text-2xl font-bold text-gray-900 mb-2">MYTA Solo Pro</h3>
            <p class="text-gray-600 mb-6">For serious content creators</p>
            
            <div class="mb-6">
              <span class="text-4xl font-bold text-gray-900">
                ${{ billingCycle === 'monthly' ? '14.99' : '149.99' }}
              </span>
              <span class="text-gray-600">
                /{{ billingCycle === 'monthly' ? 'month' : 'year' }}
              </span>
            </div>

            <ul class="text-left space-y-3 mb-8">
              <li class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Boss Agent + 4 specialist agents
              </li>
              <li class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                200 AI conversations/month
              </li>
              <li class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Unlimited content pillars
              </li>
              <li class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Priority support (24h response)
              </li>
            </ul>

            <button
              @click="selectPlan('solo_pro')"
              class="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              Start Free Trial
            </button>
          </div>
        </div>

        <!-- Teams Plan -->
        <div class="bg-white rounded-lg shadow-lg p-8 relative">
          <div class="text-center">
            <h3 class="text-2xl font-bold text-gray-900 mb-2">MYTA Teams</h3>
            <p class="text-gray-600 mb-6">For agencies and teams</p>
            
            <div class="mb-6">
              <span class="text-4xl font-bold text-gray-900">
                ${{ billingCycle === 'monthly' ? '49.99' : '499.99' }}
              </span>
              <span class="text-gray-600">
                /{{ billingCycle === 'monthly' ? 'month' : 'year' }}
              </span>
              <div class="text-sm text-gray-500 mt-1">
                Or ${{ billingCycle === 'monthly' ? '9.99' : '99.99' }}/seat/{{ billingCycle === 'monthly' ? 'month' : 'year' }}
              </div>
            </div>

            <ul class="text-left space-y-3 mb-8">
              <li class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Boss Agent + 5 specialist agents
              </li>
              <li class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Unlimited AI conversations
              </li>
              <li class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Team collaboration features
              </li>
              <li class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Dedicated support (12h response)
              </li>
            </ul>

            <button
              @click="selectPlan('teams')"
              class="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              Contact Sales
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- FAQ Section -->
    <div class="bg-white py-16">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">
          Frequently Asked Questions
        </h2>
        
        <div class="space-y-8">
          <div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              Can I change plans anytime?
            </h3>
            <p class="text-gray-600">
              Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately, and we'll prorate any billing differences.
            </p>
          </div>
          
          <div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              What's included in the free trial?
            </h3>
            <p class="text-gray-600">
              Solo Pro and Teams plans include a 14-day free trial with full access to all features. No credit card required to start.
            </p>
          </div>
          
          <div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              How does Teams per-seat pricing work?
            </h3>
            <p class="text-gray-600">
              Teams offers flexible pricing: choose the fixed plan for unlimited team members, or pay per seat for smaller teams. Perfect for agencies of any size.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from '../../composables/useToast'
import { useAuthStore } from '../../stores/auth'
import { useSubscriptionStore } from '../../stores/subscription'

// Page meta
definePageMeta({
  layout: 'default'
})

// Reactive data
const billingCycle = ref('monthly')
const subscriptionStore = useSubscriptionStore()
const { success, error } = useToast()

// Methods
const selectPlan = async (planId) => {
  try {
    if (planId === 'teams') {
      // For teams, show contact sales or custom flow
      success('Contact Sales', 'Please contact our sales team for Teams pricing and setup.')
      return
    }

    // Check if user is authenticated
    const { $router } = useNuxtApp()
    const authStore = useAuthStore()

    if (!authStore.isAuthenticated) {
      // Redirect to login with return URL
      await $router.push(`/login?redirect=/pricing&plan=${planId}&billing=${billingCycle.value}`)
      return
    }

    // Create checkout session
    await subscriptionStore.createCheckoutSession(planId, billingCycle.value)

  } catch (err) {
    error('Plan Selection Failed', 'Failed to select plan. Please try again.')
  }
}
</script>
