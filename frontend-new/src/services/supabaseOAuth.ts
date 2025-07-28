/**
 * Supabase OAuth Service for YouTube Authentication
 * Handles OAuth 2.0 flow using Supabase Auth with Google provider
 */

import { supabase, YOUTUBE_OAUTH_SCOPES, isSupabaseConfigured } from '../lib/supabase'
import type { Session } from '@supabase/supabase-js'

export interface YouTubeOAuthStatus {
  authenticated: boolean
  user_id: string
  email?: string
  expires_at?: string
  expires_in_seconds?: number
  scopes?: string[]
  access_token?: string
  refresh_token?: string
  provider_token?: string
  provider_refresh_token?: string
  needs_refresh?: boolean
  message?: string
}

export interface YouTubeTokens {
  access_token: string
  refresh_token?: string
  expires_at?: string
  scopes: string[]
}

class SupabaseOAuthService {
  private session: Session | null = null
  private isInitialized = false

  constructor() {
    this.initializeAuth()
  }

  /**
   * Initialize Supabase Auth and set up session listener
   */
  private async initializeAuth() {
    if (!isSupabaseConfigured()) {
      console.warn('Supabase not configured - OAuth features disabled')
      return
    }

    try {
      // Get initial session
      const { data: { session } } = await supabase.auth.getSession()
      this.session = session
      
      // Listen for auth state changes
      supabase.auth.onAuthStateChange(async (event, session) => {
        console.log('🔐 Supabase auth state changed:', event, session?.user?.email)
        this.session = session
        
        if (event === 'SIGNED_IN' && session) {
          console.log('✅ User signed in via Supabase')
        } else if (event === 'SIGNED_OUT') {
          console.log('👋 User signed out via Supabase')
        }
      })

      this.isInitialized = true
      console.log('🔐 Supabase OAuth service initialized')
    } catch (error) {
      console.error('❌ Failed to initialize Supabase OAuth:', error)
    }
  }

  /**
   * Check current OAuth authentication status
   */
  async checkOAuthStatus(userId?: string): Promise<YouTubeOAuthStatus> {
    if (!isSupabaseConfigured()) {
      return {
        authenticated: false,
        user_id: userId || 'unknown',
        message: 'Supabase not configured'
      }
    }

    try {
      const { data: { session } } = await supabase.auth.getSession()
      
      if (!session || !session.user) {
        return {
          authenticated: false,
          user_id: userId || 'unknown',
          message: 'No active session'
        }
      }

      // Check if we have Google provider tokens for YouTube access
      const hasYouTubeAccess = this.hasYouTubeTokens(session)
      
      return {
        authenticated: hasYouTubeAccess,
        user_id: session.user.id,
        email: session.user.email || undefined,
        expires_at: new Date(session.expires_at! * 1000).toISOString(),
        expires_in_seconds: session.expires_at! - Math.floor(Date.now() / 1000),
        scopes: hasYouTubeAccess ? YOUTUBE_OAUTH_SCOPES.split(' ') : [],
        access_token: session.access_token,
        refresh_token: session.refresh_token,
        provider_token: session.provider_token || undefined,
        provider_refresh_token: session.provider_refresh_token || undefined,
        message: hasYouTubeAccess ? 'Authenticated with YouTube access' : 'Authenticated but no YouTube access'
      }
    } catch (error) {
      console.error('Error checking OAuth status:', error)
      return {
        authenticated: false,
        user_id: userId || 'unknown',
        message: 'Failed to check authentication status'
      }
    }
  }

  /**
   * Initiate OAuth flow with Google for YouTube access
   */
  async initiateOAuth(returnUrl?: string): Promise<void> {
    if (!isSupabaseConfigured()) {
      throw new Error('Supabase not configured')
    }

    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          scopes: YOUTUBE_OAUTH_SCOPES,
          redirectTo: returnUrl || `${window.location.origin}/auth/callback`,
          queryParams: {
            access_type: 'offline',
            prompt: 'consent', // Force consent to get refresh token
          }
        }
      })

      if (error) {
        throw error
      }

      console.log('🔑 OAuth initiated with Supabase')
    } catch (error) {
      console.error('❌ Failed to initiate OAuth:', error)
      throw error
    }
  }

  /**
   * Handle OAuth callback - this is automatically handled by Supabase
   * This method is mainly for compatibility with existing code
   */
  handleOAuthCallback(): { success: boolean; error?: string; userId?: string } {
    // Supabase handles the callback automatically
    // Check if we have a session
    if (this.session?.user) {
      return {
        success: true,
        userId: this.session.user.id
      }
    }

    // Check URL parameters for error states
    const urlParams = new URLSearchParams(window.location.search)
    const error = urlParams.get('error')
    const errorDescription = urlParams.get('error_description')
    
    if (error) {
      return {
        success: false,
        error: errorDescription || error
      }
    }

    return { success: false }
  }

  /**
   * Get YouTube OAuth tokens for backend API calls
   */
  async getYouTubeTokens(): Promise<YouTubeTokens | null> {
    const status = await this.checkOAuthStatus()
    
    if (!status.authenticated || !status.provider_token) {
      return null
    }

    return {
      access_token: status.provider_token,
      refresh_token: status.provider_refresh_token,
      expires_at: status.expires_at,
      scopes: status.scopes || []
    }
  }

  /**
   * Sign out user
   */
  async signOut(): Promise<boolean> {
    if (!isSupabaseConfigured()) {
      return false
    }

    try {
      const { error } = await supabase.auth.signOut()
      if (error) {
        throw error
      }
      
      this.session = null
      console.log('👋 User signed out successfully')
      return true
    } catch (error) {
      console.error('❌ Failed to sign out:', error)
      return false
    }
  }

  /**
   * Refresh the current session
   */
  async refreshSession(): Promise<boolean> {
    if (!isSupabaseConfigured()) {
      return false
    }

    try {
      const { data, error } = await supabase.auth.refreshSession()
      if (error) {
        throw error
      }
      
      this.session = data.session
      console.log('🔄 Session refreshed successfully')
      return true
    } catch (error) {
      console.error('❌ Failed to refresh session:', error)
      return false
    }
  }

  /**
   * Check if session has YouTube-specific tokens
   */
  private hasYouTubeTokens(session: Session): boolean {
    // Check if we have provider tokens (Google OAuth tokens)
    return !!(session.provider_token && session.user?.app_metadata?.provider === 'google')
  }

  /**
   * Get current session
   */
  getCurrentSession(): Session | null {
    return this.session
  }

  /**
   * Check if service is initialized
   */
  isReady(): boolean {
    return this.isInitialized
  }
}

// Export singleton instance
export const supabaseOAuthService = new SupabaseOAuthService()
export default supabaseOAuthService