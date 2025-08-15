export interface AnalyticsData {
  overview: AnalyticsOverview | null
  channelHealth: ChannelHealth | null
  revenue: RevenueData | null
  subscribers: SubscriberData | null
  contentPerformance: ContentPerformance | null
  status: AnalyticsStatus
}

export interface AnalyticsStatus {
  youtube_connected: boolean
  analytics_available: boolean
  channel_id: string | null
}

export interface AnalyticsOverview {
  status: string
  data: {
    total_views: number
    total_subscribers: number
    total_videos: number
    avg_view_duration: number
    channel_health?: ChannelHealth
    revenue?: RevenueData
    subscribers?: SubscriberData
    content_performance?: ContentPerformance
  }
}

export interface ChannelHealth {
  status: string
  data: {
    health_score: number
    view_velocity: number
    engagement_rate: number
    subscriber_retention: number
    content_consistency: number
  }
}

export interface RevenueData {
  status: string
  data: {
    total_revenue: number
    rpm: number
    cpm: number
    estimated_monthly: number
    revenue_sources: RevenueSource[]
  }
}

export interface RevenueSource {
  type: string
  amount: number
  percentage: number
}

export interface SubscriberData {
  status: string
  data: {
    summary: {
      net_change: number
      growth_rate: number
      total_subscribers: number
    }
    daily_changes: DailyChange[]
  }
}

export interface DailyChange {
  date: string
  subscribers_gained: number
  subscribers_lost: number
  net_change: number
}

export interface ContentPerformance {
  status: string
  data: {
    videos: VideoPerformance[]
    top_performing: VideoPerformance[]
    underperforming: VideoPerformance[]
  }
}

export interface VideoPerformance {
  id: string
  title: string
  views: number
  likes: number
  comments: number
  duration: number
  published_at: string
  thumbnail_url?: string
  engagement_rate: number
}

export interface AnalyticsConfig {
  userId: string | null
  timeRange: number
  autoRefresh: boolean
  refreshInterval: number
}
