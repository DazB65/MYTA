import type { ChannelInfo, AnalyticsData, Insight } from '@/types'

const API_BASE_URL = '/api'

class APIError extends Error {
  constructor(message: string, public status?: number) {
    super(message)
    this.name = 'APIError'
  }
}

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`
  
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => null)
      throw new APIError(
        errorData?.detail || errorData?.message || `HTTP ${response.status}`,
        response.status
      )
    }

    return await response.json()
  } catch (error) {
    if (error instanceof APIError) {
      throw error
    }
    throw new APIError(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`)
  }
}

export const api = {
  // Agent endpoints
  agent: {
    async chat(message: string, userId: string): Promise<{ response: string; status: string }> {
      return fetchAPI('/agent/chat', {
        method: 'POST',
        body: JSON.stringify({ message, user_id: userId }),
      })
    },

    async quickAction(action: string, userId: string, context = ''): Promise<{ response: string; status: string }> {
      return fetchAPI('/agent/quick-action', {
        method: 'POST',
        body: JSON.stringify({ action, user_id: userId, context }),
      })
    },

    async getStatus(): Promise<{ status: string; version: string; model: string; timestamp: string }> {
      return fetchAPI('/agent/status')
    },

    async getInsights(userId: string): Promise<{ insights: Insight[]; status: string }> {
      return fetchAPI(`/agent/insights/${userId}`)
    },

    async generateInsights(userId: string): Promise<{ status: string; message: string }> {
      return fetchAPI('/agent/generate-insights', {
        method: 'POST',
        body: JSON.stringify({ user_id: userId }),
      })
    },

    async getContext(userId: string): Promise<{ channel_info: ChannelInfo; status: string }> {
      return fetchAPI(`/agent/context/${userId}`)
    },

    async setChannelInfo(channelInfo: ChannelInfo & { user_id: string }): Promise<{ status: string; message: string }> {
      console.log('Making API call to set channel info:', channelInfo)
      
      try {
        const response = await fetchAPI('/agent/set-channel-info', {
          method: 'POST',
          body: JSON.stringify(channelInfo),
        })
        
        console.log('API response received:', response)
        return response as { status: string; message: string }
      } catch (error) {
        console.error('API call failed:', error)
        throw error
      }
    },
  },

  // Content endpoints
  content: {
    async generate(action: string, userId: string, context = ''): Promise<{ response: string; content_type: string; status: string }> {
      return fetchAPI('/content/generate', {
        method: 'POST',
        body: JSON.stringify({ action, user_id: userId, context }),
      })
    },
  },

  // Analytics endpoints
  analytics: {
    async getPerformance(userId: string): Promise<{ analytics: AnalyticsData; status: string }> {
      return fetchAPI(`/analytics/performance/${userId}`)
    },
  },

  // Tools endpoints
  tools: {
    async analyzeSEO(content: string, userId: string): Promise<{ analysis: string; status: string }> {
      return fetchAPI('/tools/seo-analyze', {
        method: 'POST',
        body: JSON.stringify({ message: content, user_id: userId }),
      })
    },
  },

  // Reports endpoints
  reports: {
    async generate(reportType: string, userId: string): Promise<{ report: string; report_type: string; generated_at: string; status: string }> {
      return fetchAPI('/reports/generate', {
        method: 'POST',
        body: JSON.stringify({ message: reportType, user_id: userId }),
      })
    },
  },

  // Export endpoints
  export: {
    async getData(userId: string, format = 'json'): Promise<Blob> {
      const response = await fetch(`${API_BASE_URL}/export/data/${userId}?format=${format}`)
      if (!response.ok) {
        throw new APIError(`Export failed: ${response.status}`, response.status)
      }
      return response.blob()
    },
  },

  // YouTube API endpoints
  youtube: {
    async getAnalytics(channelId: string, userId: string, includeVideos = true, videoCount = 10): Promise<any> {
      return fetchAPI('/youtube/analytics', {
        method: 'POST',
        body: JSON.stringify({
          channel_id: channelId,
          user_id: userId,
          include_videos: includeVideos,
          video_count: videoCount,
          analysis_type: 'comprehensive'
        }),
      })
    },

    async getAuthenticatedAnalytics(channelId: string, userId: string, includeVideos = true, videoCount = 10): Promise<any> {
      return fetchAPI('/youtube/analytics/authenticated', {
        method: 'POST',
        body: JSON.stringify({
          channel_id: channelId,
          user_id: userId,
          include_videos: includeVideos,
          video_count: videoCount,
          analysis_type: 'comprehensive'
        }),
      })
    },

    async getQuota(): Promise<{ quota_status: any; status: string }> {
      return fetchAPI('/youtube/quota')
    },
  },

  // OAuth endpoints
  oauth: {
    async getStatus(userId: string): Promise<any> {
      return fetchAPI(`/auth/status/${userId}`, { method: 'GET' })
    },

    async initiate(userId: string, returnUrl?: string): Promise<any> {
      return fetchAPI('/auth/initiate', {
        method: 'POST',
        body: JSON.stringify({ user_id: userId, return_url: returnUrl }),
      })
    },

    async refresh(userId: string): Promise<any> {
      return fetchAPI(`/auth/refresh/${userId}`, { method: 'POST' })
    },

    async revoke(userId: string): Promise<any> {
      return fetchAPI(`/auth/revoke/${userId}`, { method: 'DELETE' })
    },

    async health(): Promise<any> {
      return fetchAPI('/auth/health')
    },
  },

  // Health check
  async health(): Promise<{ status: string; timestamp: string; service: string; version: string }> {
    return fetchAPI('/health')
  },
}

export { APIError }