export interface ChannelInfo {
  name: string
  channel_id?: string
  niche: string
  content_type: string
  subscriber_count: number
  avg_view_count: number
  total_view_count?: number
  video_count?: number
  ctr: number
  retention: number
  upload_frequency: string
  video_length: string
  monetization_status: string
  primary_goal: string
  notes: string
  created_date?: string
}

export interface ChatMessage {
  id: string
  role: 'user' | 'agent'
  content: string
  timestamp: Date
  isError?: boolean
}

export interface ThinkingMessage {
  id: string
  message: string
}

export interface QuickAction {
  id: string
  title: string
  description: string
  action: string
  icon: string
}

export interface Insight {
  id?: string
  title?: string
  content: string
  type: 'performance' | 'trending' | 'growth' | 'strategy' | 'timing' | 'revenue' | 'monetization'
  priority: 'high' | 'medium' | 'low'
  created_at?: string
}

export interface AgentSettings {
  avatar: string
  name: string
  personality: 'professional' | 'friendly' | 'energetic' | 'analytical'
  responseLength: 'short' | 'medium' | 'long'
}

export interface UserContext {
  userId: string
  channelInfo: ChannelInfo
  conversationHistory: ChatMessage[]
  agentSettings: AgentSettings
}

export interface APIResponse<T = unknown> {
  status: 'success' | 'error'
  data?: T
  message?: string
  error?: string
}

export interface AnalyticsData {
  total_views: number
  subscriber_growth: number
  engagement_rate: number
  top_performing_videos: Array<{
    title: string
    views: number
    ctr: number
    retention: number
  }>
  performance_trends: {
    views_trend: 'up' | 'down' | 'stable'
    ctr_trend: 'up' | 'down' | 'stable'
    retention_trend: 'up' | 'down' | 'stable'
  }
}