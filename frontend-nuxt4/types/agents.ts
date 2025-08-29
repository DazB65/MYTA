export interface Agent {
  id: string
  name: string
  type: AgentType
  status: AgentStatus
  capabilities: string[]
  description: string
  avatar?: string
  lastActive?: Date
  color?: string
  personality?: string
  specialization?: string
  metrics?: AgentMetrics
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
  | 'coordination'
  | 'executive_insight'
  | 'strategic_recommendation'

export interface MessageMetadata {
  analysisType?: string
  confidence?: number
  sources?: string[]
  chartData?: any
  actionItems?: string[]
  // Executive message metadata
  coordinatedAgents?: string[]
  coordinationTime?: string
  priority?: 'low' | 'medium' | 'high' | 'critical'
  kpis?: Record<string, string>
  strategicPillars?: string[]
  timeline?: string
  expectedROI?: string
  analysisDepth?: string
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

export interface AgentMetrics {
  totalInteractions: number
  averageResponseTime: number
  successRate: number
  lastInteraction?: Date
  insightsGenerated: number
  userSatisfactionScore?: number
}

export interface AgentPerformance {
  agentId: string
  period: 'hour' | 'day' | 'week' | 'month'
  metrics: AgentMetrics
  trends: {
    interactions: number[]
    responseTime: number[]
    successRate: number[]
  }
}

export interface MultiAgentCoordination {
  sessionId: string
  involvedAgents: string[]
  coordinationType: 'sequential' | 'parallel' | 'hierarchical'
  status: 'pending' | 'active' | 'completed' | 'failed'
  startTime: Date
  endTime?: Date
  results?: any
}
