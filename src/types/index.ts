export interface Agent {
  id: string;
  name: string;
  type: AgentType;
  status: AgentStatus;
  capabilities: string[];
  description: string;
  avatar?: string;
  lastActive?: Date;
}

export type AgentType = 
  | 'boss_agent'
  | 'content_analysis'
  | 'audience_insights'
  | 'seo_discoverability'
  | 'monetization_strategy'
  | 'competitive_analysis';

export type AgentStatus = 'online' | 'offline' | 'busy' | 'thinking';

export interface ChatMessage {
  id: string;
  agentId: string;
  userId?: string;
  content: string;
  type: MessageType;
  timestamp: Date;
  metadata?: MessageMetadata;
  isFromUser?: boolean;
}

export type MessageType = 
  | 'text'
  | 'insight'
  | 'recommendation'
  | 'analysis'
  | 'chart_data'
  | 'system'
  | 'error';

export interface MessageMetadata {
  analysisType?: string;
  confidence?: number;
  sources?: string[];
  chartData?: any;
  actionItems?: string[];
}

export interface ChatSession {
  id: string;
  userId: string;
  agentId: string;
  title: string;
  messages: ChatMessage[];
  createdAt: Date;
  updatedAt: Date;
  isActive: boolean;
}

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  subscription_tier: 'free' | 'pro' | 'enterprise';
  youtube_connected: boolean;
  channel_id?: string;
  created_at: Date;
}

export interface AnalyticsData {
  totalViews: number;
  totalSubscribers: number;
  totalVideos: number;
  healthScore: number;
  revenueMetrics: {
    total: number;
    rpm: number;
    cpm: number;
  };
  subscriberGrowth: {
    net: number;
    rate: number;
  };
}

export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  timestamp: Date;
}