import { defineStore } from 'pinia'
import { computed, readonly, ref } from 'vue'

// Note: Tokens are now stored in secure httpOnly cookies
// Only user data is stored in localStorage for UI purposes
const USER_KEY = 'myta_user_data'

export interface User {
  id: string
  email: string
  name: string
  avatar?: string
  subscription_tier: 'free' | 'pro' | 'team' | 'enterprise'
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
  // Note: tokens are now stored in secure httpOnly cookies, not in state

  // Getters
  const isLoggedIn = computed(() => isAuthenticated.value && user.value !== null)
  const userRole = computed(() => user.value?.subscription_tier || 'free')
  const hasYouTubeAccess = computed(() => user.value?.youtube_connected || false)
  const userId = computed(() => user.value?.id || null)

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
  const login = async (credentials: { email: string; password: string; remember_me?: boolean }) => {
    loading.value = true
    error.value = null

    try {
      const { $api } = useNuxtApp()

      // Call secure login endpoint
      const response = await $api('/api/auth/login', {
        method: 'POST',
        body: {
          email: credentials.email,
          password: credentials.password,
          remember_me: credentials.remember_me || false
        },
        credentials: 'include' // Include cookies in request
      })

      if (response.status === 'success') {
        // Update state with user data (token is in httpOnly cookie)
        user.value = response.user
        isAuthenticated.value = true

        // Only persist user data to localStorage (not tokens)
        saveToStorage(USER_KEY, response.user)

        console.log('Login successful for:', credentials.email)
        return response.user
      } else {
        throw new Error(response.error || 'Login failed')
      }
    } catch (err: any) {
      console.error('Login failed:', err)
      error.value = err.message || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      const { $api } = useNuxtApp()

      // Call secure logout endpoint
      await $api('/api/auth/logout', {
        method: 'POST',
        credentials: 'include' // Include cookies in request
      })
    } catch (error) {
      console.warn('Logout API call failed:', error)
      // Continue with local logout even if API call fails
    }

    // Clear state
    user.value = null
    isAuthenticated.value = false
    error.value = null

    // Clear storage (only user data, tokens are httpOnly cookies)
    removeFromStorage(USER_KEY)
  }

  const initializeAuth = async () => {
    // Only run on client side
    if (!process.client) return

    // Prevent multiple initializations
    if (loading.value) return

    loading.value = true

    try {
      // Try to restore user data from storage
      const storedUser = getFromStorage(USER_KEY)

      if (storedUser) {
        // Validate session with backend using httpOnly cookie
        try {
          const { $api } = useNuxtApp()
          const response = await $api('/api/auth/verify-token', {
            method: 'POST',
            credentials: 'include'
          })

          if (response.status === 'success') {
            // Session is valid, restore user state
            user.value = storedUser
            isAuthenticated.value = true
            console.log('Session restored for user:', storedUser.email)
          } else {
            // Session invalid, clear stored data
            await logout()
          }
        } catch (error) {
          console.warn('Session validation failed:', error)
          await logout()
        }
      } else {
        console.log('No stored user data found - user needs to login')
        // Ensure clean state
        user.value = null
        isAuthenticated.value = false
      }
    } catch (error) {
      console.warn('Failed to initialize auth:', error)
      // Clear potentially corrupted data
      await logout()
    } finally {
      loading.value = false
    }
  }

  const validateSession = async () => {
    try {
      const { $api } = useNuxtApp()
      const response = await $api('/api/auth/verify-token', {
        method: 'POST',
        credentials: 'include'
      })

      return response.status === 'success'
    } catch (error) {
      console.warn('Session validation failed:', error)
      return false
    }
  }

  return {
    // State
    user: readonly(user),
    isAuthenticated: readonly(isAuthenticated),
    loading: readonly(loading),
    error: readonly(error),

    // Getters
    isLoggedIn,
    userRole,
    hasYouTubeAccess,
    userId,

    // Actions
    login,
    logout,
    initializeAuth,
    validateSession,
  }
})
