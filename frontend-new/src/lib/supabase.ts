/**
 * Supabase Client Configuration
 * Handles Supabase authentication and client setup
 */

import { createClient } from '@supabase/supabase-js'

// Supabase configuration
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || ''
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || ''

if (!supabaseUrl || !supabaseAnonKey) {
  console.warn('Supabase URL or Anon Key not configured. OAuth features will be disabled.')
}

// Create Supabase client with fallback for missing credentials
export const supabase = createClient(
  supabaseUrl || 'https://placeholder.supabase.co', 
  supabaseAnonKey || 'placeholder-key', 
  {
    auth: {
      // Auto-refresh tokens
      autoRefreshToken: true,
    // Persist session in localStorage
    persistSession: true,
    // Detect session from URL on initialization
    detectSessionInUrl: true
  }
})

// YouTube OAuth scopes for accessing YouTube Data API and Analytics
export const YOUTUBE_OAUTH_SCOPES = [
  'https://www.googleapis.com/auth/youtube.readonly',
  'https://www.googleapis.com/auth/yt-analytics.readonly', 
  'https://www.googleapis.com/auth/yt-analytics-monetary.readonly'
].join(' ')

// Helper function to check if Supabase is configured
export const isSupabaseConfigured = () => {
  return !!(supabaseUrl && supabaseAnonKey)
}

export default supabase