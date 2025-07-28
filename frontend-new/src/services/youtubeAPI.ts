/**
 * YouTube API Service with Supabase Authentication
 * Handles YouTube API calls by sending tokens to backend
 */

import supabaseOAuthService from './supabaseOAuth'

export interface YouTubeChannelInfo {
  channel_id: string
  title: string
  description: string
  published_at: string
  subscriber_count: number
  video_count: number
  view_count: number
  custom_url?: string
  thumbnail_url: string
}

export interface YouTubeVideo {
  video_id: string
  title: string
  description: string
  published_at: string
  thumbnail_url: string
  duration: string
  view_count: number
  like_count: number
  comment_count: number
  category_id?: string
  tags: string[]
}

export interface YouTubeAnalytics {
  daily_data: Array<{
    day: string
    views: number
    estimatedMinutesWatched: number
    subscribersGained: number
    subscribersLost: number
    [key: string]: any
  }>
  summary: {
    total_views: number
    total_watch_time: number
    total_subscribers_gained: number
    total_subscribers_lost: number
  }
}

class YouTubeAPIService {
  private baseUrl = '' // Use relative URLs

  /**
   * Validate and send tokens to backend
   */
  private async validateTokens(): Promise<boolean> {
    try {
      const tokens = await supabaseOAuthService.getYouTubeTokens()
      if (!tokens) {
        throw new Error('No YouTube tokens available')
      }

      const response = await fetch(`${this.baseUrl}/api/auth/validate-youtube-tokens`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          access_token: tokens.access_token,
          refresh_token: tokens.refresh_token,
          expires_at: tokens.expires_at,
          scopes: tokens.scopes,
          user_id: supabaseOAuthService.getCurrentSession()?.user?.id || 'unknown'
        })
      })

      if (!response.ok) {
        throw new Error(`Token validation failed: ${response.statusText}`)
      }

      const result = await response.json()
      console.log('🔑 YouTube tokens validated:', result.valid)
      return result.valid
    } catch (error) {
      console.error('❌ Failed to validate YouTube tokens:', error)
      throw error
    }
  }

  /**
   * Get authenticated user's channel information
   */
  async getMyChannelInfo(): Promise<YouTubeChannelInfo> {
    try {
      // Validate tokens first
      await this.validateTokens()

      const session = supabaseOAuthService.getCurrentSession()
      if (!session?.user?.id) {
        throw new Error('No authenticated user session')
      }

      const response = await fetch(`${this.baseUrl}/api/youtube/my-channel`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: session.user.id
        })
      })

      if (!response.ok) {
        throw new Error(`Failed to get channel info: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('❌ Failed to get channel info:', error)
      throw error
    }
  }

  /**
   * Get videos for a channel
   */
  async getChannelVideos(channelId: string, maxResults: number = 50): Promise<YouTubeVideo[]> {
    try {
      // Validate tokens first
      await this.validateTokens()

      const session = supabaseOAuthService.getCurrentSession()
      if (!session?.user?.id) {
        throw new Error('No authenticated user session')
      }

      const response = await fetch(`${this.baseUrl}/api/youtube/channel-videos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: session.user.id,
          channel_id: channelId,
          max_results: maxResults
        })
      })

      if (!response.ok) {
        throw new Error(`Failed to get channel videos: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('❌ Failed to get channel videos:', error)
      throw error
    }
  }

  /**
   * Get analytics for specific videos
   */
  async getVideoAnalytics(videoIds: string[], startDate: string, endDate: string): Promise<Record<string, any>> {
    try {
      // Validate tokens first
      await this.validateTokens()

      const session = supabaseOAuthService.getCurrentSession()
      if (!session?.user?.id) {
        throw new Error('No authenticated user session')
      }

      const response = await fetch(`${this.baseUrl}/api/youtube/video-analytics`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: session.user.id,
          video_ids: videoIds,
          start_date: startDate,
          end_date: endDate
        })
      })

      if (!response.ok) {
        throw new Error(`Failed to get video analytics: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('❌ Failed to get video analytics:', error)
      throw error
    }
  }

  /**
   * Get channel-level analytics
   */
  async getChannelAnalytics(startDate: string, endDate: string): Promise<YouTubeAnalytics> {
    try {
      // Validate tokens first
      await this.validateTokens()

      const session = supabaseOAuthService.getCurrentSession()
      if (!session?.user?.id) {
        throw new Error('No authenticated user session')
      }

      const response = await fetch(`${this.baseUrl}/api/youtube/channel-analytics`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: session.user.id,
          start_date: startDate,
          end_date: endDate
        })
      })

      if (!response.ok) {
        throw new Error(`Failed to get channel analytics: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('❌ Failed to get channel analytics:', error)
      throw error
    }
  }

  /**
   * Check if YouTube API service is available for the user
   */
  async checkServiceStatus(): Promise<{ available: boolean; message: string }> {
    try {
      const session = supabaseOAuthService.getCurrentSession()
      if (!session?.user?.id) {
        return { available: false, message: 'No authenticated user session' }
      }

      const response = await fetch(`${this.baseUrl}/api/auth/youtube-service-status/${session.user.id}`)
      
      if (!response.ok) {
        return { available: false, message: 'Failed to check service status' }
      }

      const result = await response.json()
      return { 
        available: result.has_youtube_service, 
        message: result.has_youtube_service ? 'YouTube service available' : 'No YouTube service found'
      }
    } catch (error) {
      console.error('❌ Failed to check service status:', error)
      return { available: false, message: 'Error checking service status' }
    }
  }

  /**
   * Clear the user's session from backend
   */
  async clearSession(): Promise<boolean> {
    try {
      const session = supabaseOAuthService.getCurrentSession()
      if (!session?.user?.id) {
        return true // Nothing to clear
      }

      const response = await fetch(`${this.baseUrl}/api/auth/clear-session/${session.user.id}`, {
        method: 'DELETE'
      })

      return response.ok
    } catch (error) {
      console.error('❌ Failed to clear session:', error)
      return false
    }
  }
}

// Export singleton instance
export const youtubeAPIService = new YouTubeAPIService()
export default youtubeAPIService