import { defineStore } from 'pinia'
import { ref, computed, readonly } from 'vue'

export interface User {
  id: string
  email: string
  name: string
  avatar?: string
  subscription_tier: 'free' | 'pro' | 'enterprise'
  youtube_connected: boolean
  channel_id?: string
  created_at: Date
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const isAuthenticated = ref(false)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const token = ref<string | null>(null)

  // Getters
  const isLoggedIn = computed(() => isAuthenticated.value && user.value !== null)
  const userRole = computed(() => user.value?.subscription_tier || 'free')
  const hasYouTubeAccess = computed(() => user.value?.youtube_connected || false)
  const userId = computed(() => user.value?.id || null)

  // Actions
  const login = async (credentials: { email: string; password: string }) => {
    loading.value = true
    error.value = null

    try {
      // Mock login for demo
      await new Promise(resolve => setTimeout(resolve, 1000))

      user.value = {
        id: '1',
        email: credentials.email,
        name: 'Demo User',
        subscription_tier: 'pro',
        youtube_connected: true,
        created_at: new Date(),
      }
      token.value = 'demo-token'
      isAuthenticated.value = true

      return { user: user.value, token: token.value }
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    user.value = null
    token.value = null
    isAuthenticated.value = false
    error.value = null
  }

  const initializeAuth = () => {
    // Mock initialization
    console.log('Auth store initialized')
  }

  return {
    // State
    user: readonly(user),
    isAuthenticated: readonly(isAuthenticated),
    loading: readonly(loading),
    error: readonly(error),
    token: readonly(token),

    // Getters
    isLoggedIn,
    userRole,
    hasYouTubeAccess,
    userId,

    // Actions
    login,
    logout,
    initializeAuth,
  }
})
