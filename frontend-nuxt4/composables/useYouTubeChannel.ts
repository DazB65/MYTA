import { computed, ref } from 'vue'

interface ChannelData {
  id: string
  title: string
  description: string
  thumbnails: {
    default: { url: string }
    medium: { url: string }
    high: { url: string }
  }
  bannerExternalUrl?: string
  subscriberCount: string
  videoCount: string
  viewCount: string
  customUrl?: string
}

interface YouTubeChannelState {
  channelData: ChannelData | null
  isConnected: boolean
  isLoading: boolean
  error: string | null
}

// Global state for YouTube channel
const state = ref<YouTubeChannelState>({
  channelData: null,
  isConnected: false,
  isLoading: false,
  error: null
})

export const useYouTubeChannel = () => {
  // Computed properties
  const channelName = computed(() => state.value.channelData?.title || '')
  const channelAvatar = computed(() => state.value.channelData?.thumbnails?.high?.url || '')
  const channelBanner = computed(() => state.value.channelData?.bannerExternalUrl || '')
  const channelDescription = computed(() => state.value.channelData?.description || '')
  const subscriberCount = computed(() => state.value.channelData?.subscriberCount || '0')

  // Check if user has connected YouTube account
  const checkConnection = async () => {
    try {
      state.value.isLoading = true
      state.value.error = null

      // Check OAuth status using existing YouTube endpoint
      const response = await fetch('/api/youtube/oauth-status/default_user', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const data = await response.json()
        state.value.isConnected = data.status === 'success' && data.data?.authenticated

        // If connected, try to fetch channel data
        if (state.value.isConnected) {
          await fetchChannelData()
        }
      } else {
        state.value.isConnected = false
      }
    } catch (error) {
      console.error('Error checking YouTube connection:', error)
      state.value.error = 'Failed to check YouTube connection'
      state.value.isConnected = false
    } finally {
      state.value.isLoading = false
    }
  }

  // Fetch channel data from YouTube API
  const fetchChannelData = async (forceRefresh = false) => {
    if (!state.value.isConnected && !forceRefresh) {
      console.warn('YouTube not connected, cannot fetch channel data')
      return null
    }

    try {
      state.value.isLoading = true
      state.value.error = null

      // Use the existing analytics endpoint to get channel data
      const response = await fetch('/api/youtube/analytics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          channel_id: '', // Empty to auto-detect
          user_id: 'default_user',
          include_videos: false,
          video_count: 1
        })
      })

      if (response.ok) {
        const data = await response.json()
        if (data.status === 'success' && data.data?.channel_data?.basic_info) {
          const basicInfo = data.data.channel_data.basic_info

          // Transform to our expected format
          const channelData = {
            id: basicInfo.channel_id,
            title: basicInfo.title,
            description: '', // Not available in basic_info
            thumbnails: {
              high: { url: '' } // Not available in basic_info
            },
            bannerExternalUrl: '', // Not available in basic_info
            subscriberCount: basicInfo.subscriber_count,
            videoCount: basicInfo.video_count,
            viewCount: basicInfo.view_count
          }

          state.value.channelData = channelData
          state.value.isConnected = true

          // Cache the data locally
          if (typeof window !== 'undefined') {
            localStorage.setItem('youtubeChannelData', JSON.stringify({
              channelData: channelData,
              cachedAt: new Date().toISOString()
            }))
          }

          return channelData
        } else {
          throw new Error('Invalid response format')
        }
      } else {
        const errorData = await response.json()
        state.value.error = errorData.detail || 'Failed to fetch channel data'
        state.value.isConnected = false
        return null
      }
    } catch (error) {
      console.error('Error fetching channel data:', error)
      state.value.error = 'Failed to fetch channel data'
      return null
    } finally {
      state.value.isLoading = false
    }
  }

  // Connect to YouTube (redirect to OAuth)
  const connectYouTube = async () => {
    try {
      console.log('🔗 connectYouTube: Starting OAuth flow...')
      state.value.isLoading = true
      state.value.error = null

      const requestBody = {
        userId: 'default_user' // In production, get from auth context
      }
      console.log('🔗 connectYouTube: Request body:', requestBody)

      // Use the correct YouTube OAuth endpoint
      const response = await fetch('/api/youtube/auth-url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest', // Add CSRF header
        },
        body: JSON.stringify(requestBody)
      })

      console.log('🔗 connectYouTube: Response status:', response.status)
      console.log('🔗 connectYouTube: Response headers:', Object.fromEntries(response.headers.entries()))

      if (response.ok) {
        const data = await response.json()
        console.log('🔗 connectYouTube: Response data:', data)
        // Redirect to YouTube OAuth
        console.log('🔗 connectYouTube: Redirecting to:', data.authUrl)
        window.location.href = data.authUrl
      } else {
        const errorData = await response.json()
        console.error('🔗 connectYouTube: Error response:', errorData)
        state.value.error = errorData.detail || 'Failed to initiate YouTube connection'
      }
    } catch (error) {
      console.error('❌ connectYouTube: Exception:', error)
      state.value.error = 'Failed to connect to YouTube'
    } finally {
      state.value.isLoading = false
    }
  }

  // Disconnect YouTube account
  const disconnectYouTube = async () => {
    try {
      state.value.isLoading = true
      state.value.error = null

      const response = await fetch('/auth/revoke/default_user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        state.value.channelData = null
        state.value.isConnected = false

        // Clear cached data
        if (typeof window !== 'undefined') {
          localStorage.removeItem('youtubeChannelData')
        }
      } else {
        const errorData = await response.json()
        state.value.error = errorData.detail || 'Failed to disconnect YouTube'
      }
    } catch (error) {
      console.error('Error disconnecting YouTube:', error)
      state.value.error = 'Failed to disconnect YouTube'
    } finally {
      state.value.isLoading = false
    }
  }

  // Load cached data on initialization
  const loadCachedData = () => {
    if (typeof window !== 'undefined') {
      const cached = localStorage.getItem('youtubeChannelData')
      if (cached) {
        try {
          const { channelData, cachedAt } = JSON.parse(cached)
          const cacheAge = Date.now() - new Date(cachedAt).getTime()
          
          // Use cached data if less than 1 hour old
          if (cacheAge < 3600000) {
            state.value.channelData = channelData
            state.value.isConnected = true
          }
        } catch (error) {
          console.error('Error loading cached channel data:', error)
        }
      }
    }
  }

  // Initialize on first use
  const initialize = async () => {
    loadCachedData()
    await checkConnection()
    
    // If connected but no cached data, fetch fresh data
    if (state.value.isConnected && !state.value.channelData) {
      await fetchChannelData()
    }
  }

  return {
    // State
    channelData: computed(() => state.value.channelData),
    isConnected: computed(() => state.value.isConnected),
    isLoading: computed(() => state.value.isLoading),
    error: computed(() => state.value.error),
    
    // Computed channel properties
    channelName,
    channelAvatar,
    channelBanner,
    channelDescription,
    subscriberCount,
    
    // Methods
    checkConnection,
    fetchChannelData,
    connectYouTube,
    disconnectYouTube,
    initialize
  }
}
