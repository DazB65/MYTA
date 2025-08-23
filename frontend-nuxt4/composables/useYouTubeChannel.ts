import { ref, computed } from 'vue'

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

      // Check if user has connected YouTube account
      const response = await fetch('/api/youtube/connection-status', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const data = await response.json()
        state.value.isConnected = data.connected
        
        if (data.connected && data.channelData) {
          state.value.channelData = data.channelData
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

      const response = await fetch('/api/youtube/channel-data', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const data = await response.json()
        state.value.channelData = data.channelData
        state.value.isConnected = true
        
        // Cache the data locally
        if (typeof window !== 'undefined') {
          localStorage.setItem('youtubeChannelData', JSON.stringify({
            channelData: data.channelData,
            cachedAt: new Date().toISOString()
          }))
        }
        
        return data.channelData
      } else {
        const errorData = await response.json()
        state.value.error = errorData.message || 'Failed to fetch channel data'
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
      state.value.isLoading = true
      state.value.error = null

      // Get OAuth authorization URL
      const response = await fetch('/api/youtube/auth-url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userId: 'default_user' // In production, get from auth context
        })
      })

      if (response.ok) {
        const data = await response.json()
        // Redirect to YouTube OAuth
        window.location.href = data.authUrl
      } else {
        const errorData = await response.json()
        state.value.error = errorData.message || 'Failed to initiate YouTube connection'
      }
    } catch (error) {
      console.error('Error connecting to YouTube:', error)
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

      const response = await fetch('/api/youtube/disconnect', {
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
        state.value.error = errorData.message || 'Failed to disconnect YouTube'
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
