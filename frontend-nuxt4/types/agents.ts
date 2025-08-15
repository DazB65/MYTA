export interface Agent {
  id: string
  name: string
  type: AgentType
  status: AgentStatus
  capabilities: string[]
  description: string
  avatar?: string
  lastActive?: Date
}

export type AgentType =
  | 'boss_agent'
  | 'content_analysis'
  | 'audience_insights'
  | 'seo_discoverability'
  | 'monetization_strategy'
  | 'competitive_analysis'

export type AgentStatus = 'online' | 'offline' | 'busy' | 'thinking'

export interface ChatMessage {
  id: string
  agentId: string
  userId?: string
  content: string
  type: MessageType
  timestamp: Date
  metadata?: MessageMetadata
  isFromUser?: boolean
}

export type MessageType =
  | 'text'
  | 'insight'
  | 'recommendation'
  | 'analysis'
  | 'chart_data'
  | 'system'
  | 'error'

export interface MessageMetadata {
  analysisType?: string
  confidence?: number
  sources?: string[]
  chartData?: any
  actionItems?: string[]
}

export interface ChatSession {
  id: string
  userId: string
  agentId: string
  title: string
  messages: ChatMessage[]
  createdAt: Date
  updatedAt: Date
  isActive: boolean
}

export interface AgentInsight {
  id: string
  agentId: string
  type: InsightType
  title: string
  description: string
  data: any
  confidence: number
  timestamp: Date
  priority: 'low' | 'medium' | 'high' | 'critical'
}

export type InsightType =
  | 'content_performance'
  | 'audience_behavior'
  | 'seo_opportunity'
  | 'monetization_tip'
  | 'competitive_gap'
  | 'trend_alert'

export interface WebSocketMessage {
  type: WSMessageType
  payload: any
  timestamp: Date
  sessionId?: string
}

export type WSMessageType =
  | 'agent_message'
  | 'agent_status_change'
  | 'insight_generated'
  | 'analysis_complete'
  | 'user_joined'
  | 'user_left'
  | 'error'
  | 'heartbeat'
