/**
 * Supabase OAuth Store for React State Management
 * Manages OAuth authentication state using Zustand and Supabase Auth
 */

import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { useEffect } from 'react'
import supabaseOAuthService, { YouTubeOAuthStatus, YouTubeTokens } from '../services/supabaseOAuth'

interface SupabaseOAuthState {
  // Authentication state
  isAuthenticated: boolean
  status: YouTubeOAuthStatus | null
  isLoading: boolean
  error: string | null
  
  // User info
  userId: string
  email: string | null
  
  // OAuth flow state
  isAuthenticating: boolean
  
  // YouTube tokens for API calls
  youtubeTokens: YouTubeTokens | null
  
  // Actions
  setUserId: (userId: string) => void
  checkStatus: () => Promise<void>
  initiateOAuth: (returnUrl?: string) => Promise<void>
  handleCallback: () => { success: boolean; error?: string; userId?: string }
  refreshSession: () => Promise<boolean>
  signOut: () => Promise<boolean>
  getYouTubeTokens: () => Promise<YouTubeTokens | null>
  clearError: () => void
  resetAuthentication: () => void
}

export const useSupabaseOAuthStore = create<SupabaseOAuthState>()(
  persist(
    (set, get) => ({
      // Initial state
      isAuthenticated: false,
      status: null,
      isLoading: false,
      error: null,
      userId: '',
      email: null,
      isAuthenticating: false,
      youtubeTokens: null,

      // Set user ID (for compatibility with existing code)
      setUserId: (userId: string) => {
        set({ userId })
      },

      // Check OAuth status
      checkStatus: async () => {
        set({ isLoading: true, error: null })

        try {
          console.log('🔐 Checking Supabase OAuth status...')
          const status = await supabaseOAuthService.checkOAuthStatus()
          console.log('🔐 Supabase OAuth status received:', status)
          
          // Get YouTube tokens if authenticated
          let youtubeTokens = null
          if (status.authenticated) {
            youtubeTokens = await supabaseOAuthService.getYouTubeTokens()
          }
          
          set({
            status,
            isAuthenticated: status.authenticated,
            userId: status.user_id,
            email: status.email || null,
            youtubeTokens,
            isLoading: false,
            error: null
          })
          
          if (status.authenticated) {
            console.log('✅ User is authenticated via Supabase')
          } else {
            console.log('❌ User is not authenticated via Supabase:', status.message)
          }
        } catch (error) {
          console.error('🔐 Supabase OAuth status check failed:', error)
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to check OAuth status'
          })
        }
      },

      // Initiate OAuth flow
      initiateOAuth: async (returnUrl?: string) => {
        set({ isAuthenticating: true, error: null })

        try {
          console.log('🔑 Initiating Supabase OAuth...')
          await supabaseOAuthService.initiateOAuth(returnUrl)
          
          // Note: The actual redirect happens in the service
          // The user will be redirected to Google OAuth
        } catch (error) {
          console.error('🔑 Failed to initiate Supabase OAuth:', error)
          set({
            isAuthenticating: false,
            error: error instanceof Error ? error.message : 'Failed to initiate OAuth'
          })
        }
      },

      // Handle OAuth callback
      handleCallback: () => {
        const result = supabaseOAuthService.handleOAuthCallback()
        
        if (result.success) {
          console.log('✅ Supabase OAuth callback handled successfully')
          set({ 
            isAuthenticating: false, 
            error: null,
            userId: result.userId || ''
          })
          
          // Check status after successful callback
          get().checkStatus()
          
          return { success: true, userId: result.userId }
        } else if (result.error) {
          console.error('❌ Supabase OAuth callback failed:', result.error)
          set({ 
            isAuthenticating: false, 
            error: result.error 
          })
          
          return { success: false, error: result.error }
        }
        
        return { success: false }
      },

      // Refresh session
      refreshSession: async () => {
        set({ isLoading: true, error: null })

        try {
          const success = await supabaseOAuthService.refreshSession()
          
          if (success) {
            // Refresh status after session refresh
            await get().checkStatus()
            return true
          } else {
            set({ 
              isLoading: false,
              error: 'Failed to refresh session'
            })
            return false
          }
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to refresh session'
          })
          return false
        }
      },

      // Sign out
      signOut: async () => {
        set({ isLoading: true, error: null })

        try {
          const success = await supabaseOAuthService.signOut()
          
          if (success) {
            set({
              isAuthenticated: false,
              status: null,
              userId: '',
              email: null,
              youtubeTokens: null,
              isLoading: false,
              error: null
            })
            return true
          } else {
            set({ 
              isLoading: false,
              error: 'Failed to sign out'
            })
            return false
          }
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to sign out'
          })
          return false
        }
      },

      // Get YouTube tokens for API calls
      getYouTubeTokens: async () => {
        try {
          const tokens = await supabaseOAuthService.getYouTubeTokens()
          set({ youtubeTokens: tokens })
          return tokens
        } catch (error) {
          console.error('Failed to get YouTube tokens:', error)
          set({ 
            error: error instanceof Error ? error.message : 'Failed to get YouTube tokens'
          })
          return null
        }
      },

      // Clear error
      clearError: () => {
        set({ error: null })
      },

      // Reset authentication state
      resetAuthentication: () => {
        set({
          isAuthenticated: false,
          status: null,
          userId: '',
          email: null,
          isAuthenticating: false,
          youtubeTokens: null,
          error: null
        })
      }
    }),
    {
      name: 'supabase-oauth-store',
      partialize: (state) => ({
        userId: state.userId,
        email: state.email,
        // Don't persist sensitive auth data - it will be refreshed on app load
      })
    }
  )
)

// Custom hook for Supabase OAuth status checking
export const useSupabaseOAuthStatus = () => {
  const store = useSupabaseOAuthStore()
  
  // Auto-check status on mount and when service is ready
  useEffect(() => {
    const checkWhenReady = async () => {
      // Wait for service to be ready
      if (supabaseOAuthService.isReady()) {
        await store.checkStatus()
      } else {
        // Check again in a bit if not ready
        setTimeout(checkWhenReady, 100)
      }
    }
    
    checkWhenReady()
    
    // Set up periodic status checking (every 5 minutes)
    const interval = setInterval(() => {
      if (store.isAuthenticated && supabaseOAuthService.isReady()) {
        store.checkStatus()
      }
    }, 5 * 60 * 1000)
    
    return () => clearInterval(interval)
  }, [store.checkStatus, store.isAuthenticated])
  
  return store
}

export default useSupabaseOAuthStore