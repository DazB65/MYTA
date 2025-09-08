<template>
  <div class="min-h-screen bg-slate-900 flex items-center justify-center p-4">
    <div class="max-w-md w-full">
      <!-- Loading State -->
      <div v-if="loading" class="bg-gray-800 rounded-xl p-8 text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
        <h2 class="text-xl font-semibold text-white mb-2">Processing Invitation...</h2>
        <p class="text-gray-400">Please wait while we verify your invitation.</p>
      </div>

      <!-- Success State -->
      <div v-else-if="success" class="bg-forest-800 rounded-xl p-8 text-center">
        <div class="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
        </div>

        <h1 class="text-2xl font-bold text-white mb-4">Welcome to the Team! 🎉</h1>

        <div v-if="teamInfo" class="bg-forest-700 rounded-lg p-4 mb-6">
          <p class="text-sm text-gray-400 mb-2">You've successfully joined:</p>
          <h3 class="font-semibold text-white">{{ teamInfo.name }}</h3>
          <p class="text-sm text-blue-400 mt-1">Role: {{ teamInfo.role }}</p>
        </div>

        <p class="text-gray-400 mb-6">
          You now have access to your team's workspace and can start collaborating on content creation.
        </p>

        <div class="space-y-3">
          <button
            @click="goToDashboard"
            class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Go to Dashboard
          </button>

          <button
            @click="goToTeamSettings"
            class="w-full bg-forest-700 text-gray-300 py-3 px-4 rounded-lg font-medium hover:bg-forest-600 transition-colors"
          >
            View Team Settings
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

        <h1 class="text-2xl font-bold text-white mb-4">Invitation Error</h1>

        <div class="bg-red-900/30 border border-red-500/30 rounded-lg p-4 mb-6">
          <p class="text-red-300 text-sm">{{ errorMessage }}</p>
        </div>

        <div class="space-y-3">
          <button
            @click="retryAcceptance"
            class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>

          <button
            @click="goToLogin"
            class="w-full bg-forest-700 text-gray-300 py-3 px-4 rounded-lg font-medium hover:bg-forest-600 transition-colors"
          >
            Go to Login
          </button>
        </div>
      </div>

      <!-- Need to Login State -->
      <div v-else-if="needsLogin" class="bg-forest-800 rounded-xl p-8 text-center">
        <div class="w-16 h-16 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
          </svg>
        </div>

        <h1 class="text-2xl font-bold text-white mb-4">Login Required</h1>

        <p class="text-gray-400 mb-6">
          Please log in to your MYTA account to accept this team invitation.
        </p>

        <div class="space-y-3">
          <button
            @click="goToLogin"
            class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Login to MYTA
          </button>

          <button
            @click="goToSignup"
            class="w-full bg-gray-700 text-gray-300 py-3 px-4 rounded-lg font-medium hover:bg-gray-600 transition-colors"
          >
            Create Account
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
  title: 'Accept Team Invitation'
})

const route = useRoute()
const router = useRouter()

// State
const loading = ref(true)
const success = ref(false)
const error = ref(false)
const needsLogin = ref(false)
const errorMessage = ref('')
const teamInfo = ref(null)

// Get invitation token from URL
const token = route.query.token

onMounted(async () => {
  if (!token) {
    error.value = true
    errorMessage.value = 'Invalid invitation link. No token provided.'
    loading.value = false
    return
  }

  await acceptInvitation()
})

async function acceptInvitation() {
  try {
    loading.value = true
    error.value = false

    // Demo mode - simulate different states based on token
    if (token === 'demo_token_123') {
      // Simulate processing delay
      await new Promise(resolve => setTimeout(resolve, 2000))

      // Simulate successful acceptance
      success.value = true
      teamInfo.value = {
        name: 'My Content Team',
        role: 'Editor'
      }
      loading.value = false
      return
    }

    if (token === 'demo_error_token') {
      // Simulate processing delay
      await new Promise(resolve => setTimeout(resolve, 1500))

      // Simulate error
      throw new Error('This invitation has expired.')
    }

    // Check if user is logged in
    const authToken = localStorage.getItem('auth_token')
    if (!authToken) {
      needsLogin.value = true
      loading.value = false
      return
    }

    // Accept the invitation
    const response = await $fetch('/api/teams/invitations/accept', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      },
      body: {
        action: 'accept',
        token: token
      }
    })

    if (response.success) {
      success.value = true
      teamInfo.value = {
        name: response.data?.team_name || 'Your Team',
        role: response.data?.role || 'Member'
      }
    } else {
      throw new Error(response.message || 'Failed to accept invitation')
    }

  } catch (err) {
    console.error('Error accepting invitation:', err)
    error.value = true
    
    if (err.status === 401) {
      needsLogin.value = true
      errorMessage.value = 'Please log in to accept this invitation.'
    } else if (err.status === 404) {
      errorMessage.value = 'This invitation is invalid or has expired.'
    } else if (err.status === 403) {
      errorMessage.value = 'This invitation is not for your email address.'
    } else {
      errorMessage.value = err.data?.detail || err.message || 'Failed to accept invitation. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

async function retryAcceptance() {
  await acceptInvitation()
}

function goToDashboard() {
  router.push('/dashboard')
}

function goToTeamSettings() {
  router.push('/settings?tab=team')
}

function goToLogin() {
  // Store the invitation token to retry after login
  localStorage.setItem('pending_invitation_token', token)
  router.push('/login')
}

function goToSignup() {
  // Store the invitation token to retry after signup
  localStorage.setItem('pending_invitation_token', token)
  router.push('/create-profile')
}
</script>
