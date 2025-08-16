import { defineStore } from 'pinia'
import { computed, readonly, ref } from 'vue'

// Storage keys for persistence
const TOKEN_KEY = 'myta_auth_token'
const USER_KEY = 'myta_user_data'
const REFRESH_TOKEN_KEY = 'myta_refresh_token'

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
  const refreshToken = ref<string | null>(null)
  const tokenExpiry = ref<Date | null>(null)

  // Getters
  const isLoggedIn = computed(() => isAuthenticated.value && user.value !== null && token.value !== null)
  const userRole = computed(() => user.value?.subscription_tier || 'free')
  const hasYouTubeAccess = computed(() => user.value?.youtube_connected || false)
  const userId = computed(() => user.value?.id || null)
  const isTokenExpired = computed(() => {
    if (!tokenExpiry.value) return false
    return new Date() >= tokenExpiry.value
  })

  // Storage utilities
  const saveToStorage = (key: string, value: any) => {
    if (process.client) {
      try {
        localStorage.setItem(key, JSON.stringify(value))
      } catch (error) {
        console.warn('Failed to save to localStorage:', error)
      }
    }
  }

  const getFromStorage = (key: string) => {
    if (process.client) {
      try {
        const item = localStorage.getItem(key)
        return item ? JSON.parse(item) : null
      } catch (error) {
        console.warn('Failed to read from localStorage:', error)
        return null
      }
    }
    return null
  }

  const removeFromStorage = (key: string) => {
    if (process.client) {
      try {
        localStorage.removeItem(key)
      } catch (error) {
        console.warn('Failed to remove from localStorage:', error)
      }
    }
  }

  // Actions
  const login = async (credentials: { email: string; password: string }) => {
    loading.value = true
    error.value = null

    try {
      // Mock login for demo
      await new Promise(resolve => setTimeout(resolve, 1000))

      const mockUser = {
        id: '1',
        email: credentials.email,
        name: 'Demo User',
        subscription_tier: 'pro' as const,
        youtube_connected: true,
        created_at: new Date(),
      }

      const mockToken = 'demo-token-' + Date.now()
      const mockRefreshToken = 'refresh-token-' + Date.now()
      const expiry = new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours

      // Set state
      user.value = mockUser
      token.value = mockToken
      refreshToken.value = mockRefreshToken
      tokenExpiry.value = expiry
      isAuthenticated.value = true

      // Persist to storage
      saveToStorage(USER_KEY, mockUser)
      saveToStorage(TOKEN_KEY, mockToken)
      saveToStorage(REFRESH_TOKEN_KEY, mockRefreshToken)

      return { user: mockUser, token: mockToken }
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    // Clear state
    user.value = null
    token.value = null
    refreshToken.value = null
    tokenExpiry.value = null
    isAuthenticated.value = false
    error.value = null

    // Clear storage
    removeFromStorage(USER_KEY)
    removeFromStorage(TOKEN_KEY)
    removeFromStorage(REFRESH_TOKEN_KEY)
  }

  const initializeAuth = async () => {
    // Only run on client side
    if (!process.client) return

    loading.value = true

    try {
      // Try to restore session from storage
      const storedUser = getFromStorage(USER_KEY)
      const storedToken = getFromStorage(TOKEN_KEY)
      const storedRefreshToken = getFromStorage(REFRESH_TOKEN_KEY)

      if (storedUser && storedToken) {
        // Restore user session
        user.value = storedUser
        token.value = storedToken
        refreshToken.value = storedRefreshToken
        isAuthenticated.value = true

        // Set token expiry (assume 24 hours if not stored)
        tokenExpiry.value = new Date(Date.now() + 24 * 60 * 60 * 1000)

        console.log('Session restored from storage')

        // Optionally validate token with backend here
        // await validateToken(storedToken)
      } else {
        console.log('No stored session found')
      }
    } catch (error) {
      console.warn('Failed to initialize auth:', error)
      // Clear potentially corrupted data
      await logout()
    } finally {
      loading.value = false
    }
  }

  const refreshSession = async () => {
    if (!refreshToken.value) {
      throw new Error('No refresh token available')
    }

    loading.value = true

    try {
      // Mock refresh for demo
      await new Promise(resolve => setTimeout(resolve, 500))

      const newToken = 'refreshed-token-' + Date.now()
      const newExpiry = new Date(Date.now() + 24 * 60 * 60 * 1000)

      token.value = newToken
      tokenExpiry.value = newExpiry

      // Update storage
      saveToStorage(TOKEN_KEY, newToken)

      console.log('Session refreshed successfully')
      return newToken
    } catch (error) {
      console.error('Failed to refresh session:', error)
      // If refresh fails, logout user
      await logout()
      throw error
    } finally {
      loading.value = false
    }
  }

  const checkAndRefreshToken = async () => {
    if (isTokenExpired.value && refreshToken.value) {
      try {
        await refreshSession()
      } catch (error) {
        console.error('Auto-refresh failed:', error)
        return false
      }
    }
    return true
  }

  return {
    // State
    user: readonly(user),
    isAuthenticated: readonly(isAuthenticated),
    loading: readonly(loading),
    error: readonly(error),
    token: readonly(token),
    refreshToken: readonly(refreshToken),
    tokenExpiry: readonly(tokenExpiry),

    // Getters
    isLoggedIn,
    userRole,
    hasYouTubeAccess,
    userId,
    isTokenExpired,

    // Actions
    login,
    logout,
    initializeAuth,
    refreshSession,
    checkAndRefreshToken,
  }
})
