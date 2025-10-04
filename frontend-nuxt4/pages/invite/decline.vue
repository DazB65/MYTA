<template>
  <div class="min-h-screen bg-forest-900 flex items-center justify-center p-4">
    <div class="max-w-md w-full">
      <!-- Loading State -->
      <div v-if="loading" class="bg-forest-800 rounded-xl p-8 text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto mb-4"></div>
        <h2 class="text-xl font-semibold text-white mb-2">Processing...</h2>
        <p class="text-gray-400">Please wait while we process your response.</p>
      </div>

      <!-- Confirmation State -->
      <div v-else-if="!confirmed && !error" class="bg-forest-800 rounded-xl p-8 text-center">
        <div class="w-16 h-16 bg-orange-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-8 h-8 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
          </svg>
        </div>

        <h1 class="text-2xl font-bold text-white mb-4">Decline Team Invitation?</h1>

        <p class="text-gray-400 mb-6">
          Are you sure you want to decline this team invitation? This action cannot be undone, and you'll need a new invitation to join the team later.
        </p>

        <div class="space-y-3">
          <button
            @click="confirmDecline"
            class="w-full bg-red-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-red-700 transition-colors"
          >
            Yes, Decline Invitation
          </button>

          <button
            @click="goToAccept"
            class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Actually, Accept Instead
          </button>

          <button
            @click="goHome"
            class="w-full bg-forest-700 text-gray-300 py-3 px-4 rounded-lg font-medium hover:bg-forest-600 transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>

      <!-- Success State -->
      <div v-else-if="success" class="bg-forest-800 rounded-xl p-8 text-center">
        <div class="w-16 h-16 bg-gray-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </div>

        <h1 class="text-2xl font-bold text-white mb-4">Invitation Declined</h1>

        <p class="text-gray-400 mb-6">
          You have successfully declined the team invitation. The team owner has been notified of your decision.
        </p>

        <div class="bg-blue-900/30 border border-blue-500/30 rounded-lg p-4 mb-6">
          <p class="text-blue-300 text-sm">
            <strong>Changed your mind?</strong> You can still create your own MYTA account to start your content creation journey.
          </p>
        </div>

        <div class="space-y-3">
          <button
            @click="goToSignup"
            class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Create Your Own Account
          </button>

          <button
            @click="goHome"
            class="w-full bg-forest-700 text-gray-300 py-3 px-4 rounded-lg font-medium hover:bg-forest-600 transition-colors"
          >
            Go to MYTA Home
          </button>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-forest-800 rounded-xl p-8 text-center">
        <div class="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </div>

        <h1 class="text-2xl font-bold text-white mb-4">Error</h1>

        <div class="bg-red-900/30 border border-red-500/30 rounded-lg p-4 mb-6">
          <p class="text-red-300 text-sm">{{ errorMessage }}</p>
        </div>

        <div class="space-y-3">
          <button
            @click="retryDecline"
            class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>

          <button
            @click="goHome"
            class="w-full bg-forest-700 text-gray-300 py-3 px-4 rounded-lg font-medium hover:bg-forest-600 transition-colors"
          >
            Go to MYTA Home
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// Set page title
useHead({
  title: 'Decline Team Invitation'
})

const route = useRoute()
const router = useRouter()

// State
const loading = ref(false)
const confirmed = ref(false)
const success = ref(false)
const error = ref(false)
const errorMessage = ref('')

// Get invitation token from URL
const token = route.query.token

onMounted(() => {
  if (!token) {
    error.value = true
    errorMessage.value = 'Invalid invitation link. No token provided.'
  }
})

async function confirmDecline() {
  try {
    loading.value = true
    error.value = false
    confirmed.value = true

    // Demo mode - simulate decline process
    if (token === 'demo_token_123') {
      // Simulate processing delay
      await new Promise(resolve => setTimeout(resolve, 1500))

      // Simulate successful decline
      success.value = true
      loading.value = false
      return
    }

    // Decline the invitation (no auth required for declining)
    const response = await $fetch('/api/teams/invitations/decline', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: {
        action: 'decline',
        token: token
      }
    })

    if (response.success) {
      success.value = true
    } else {
      throw new Error(response.message || 'Failed to decline invitation')
    }

  } catch (err) {
    console.error('Error declining invitation:', err)
    error.value = true
    confirmed.value = false
    
    if (err.status === 404) {
      errorMessage.value = 'This invitation is invalid or has already been processed.'
    } else {
      errorMessage.value = err.data?.detail || err.message || 'Failed to decline invitation. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

async function retryDecline() {
  await confirmDecline()
}

function goToAccept() {
  router.push(`/invite/accept?token=${token}`)
}

function goToSignup() {
  router.push('/create-profile')
}

function goHome() {
  // Navigate to home page or login
  router.push('/')
}
</script>
