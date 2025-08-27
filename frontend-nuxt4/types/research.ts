// Research Workspace Types

export interface ResearchProject {
  id: string
  name: string
  description: string
  createdAt: Date
  updatedAt: Date
  videos: ResearchVideo[]
  notes: ResearchNote[]
  connections: ResearchConnection[]
  insights: ResearchInsight[]
  tags?: string[]
  isPublic?: boolean
}

export interface ResearchVideo {
  id: string
  url: string
  videoId: string
  title: string
  channelName: string
  channelId: string
  thumbnail: string
  duration: number
  views: number
  publishedAt: string
  position: { x: number, y: number }
  addedAt: Date
  analysisStatus: 'pending' | 'analyzing' | 'completed' | 'failed'
  analysis?: VideoAnalysis
  metrics?: VideoMetrics
  tags?: string[]
  notes?: string
}

export interface VideoAnalysis {
  overallScore: number
  keyInsights: VideoInsight[]
  successFactors: string[]
  improvementAreas: string[]
  tags: string[]
  sentiment: 'positive' | 'neutral' | 'negative'
  contentType: string
  targetAudience: string
  estimatedPerformance: {
    viewsPrediction: number
    engagementPrediction: number
    viralPotential: number
  }
  competitorComparison?: {
    betterThan: number
    similarTo: string[]
    gapsIdentified: string[]
  }
}

export interface VideoInsight {
  id: string
  type: 'thumbnail' | 'title' | 'content' | 'timing' | 'engagement' | 'seo'
  text: string
  importance: 'high' | 'medium' | 'low'
  actionable: boolean
  recommendation?: string
}

export interface VideoMetrics {
  views: number
  likes: number
  dislikes: number
  comments: number
  shares: number
  engagementRate: number
  clickThroughRate?: number
  averageViewDuration?: number
  retentionRate?: number
  subscribersGained?: number
}

export interface ResearchNote {
  id: string
  content: string
  position: { x: number, y: number }
  createdAt: Date
  updatedAt?: Date
  color: string
  size?: { width: number, height: number }
  tags?: string[]
  linkedItems?: string[] // IDs of connected videos/notes
}

export interface ResearchConnection {
  id: string
  fromId: string
  toId: string
  fromPosition: { x: number, y: number }
  toPosition: { x: number, y: number }
  type: 'related' | 'inspired-by' | 'competitor' | 'trend' | 'custom'
  label?: string
  createdAt: Date
  strength?: number // 1-10 scale
  notes?: string
}

export interface ResearchInsight {
  id: string
  title: string
  description: string
  type: 'trend' | 'opportunity' | 'threat' | 'pattern' | 'recommendation'
  importance: 'high' | 'medium' | 'low'
  confidence: number // 0-100
  source: 'ai-analysis' | 'trend-data' | 'competitor-analysis' | 'user-input'
  relatedItems: string[] // IDs of related videos/notes
  actionItems?: string[]
  createdAt: Date
  tags?: string[]
}

export interface TrendingTopic {
  id: string
  title: string
  description: string
  growth: number // percentage growth
  volume: number // search volume or mentions
  category: string
  timeframe: '24h' | '7d' | '30d'
  relatedKeywords: string[]
  competitorVideos?: string[] // video IDs
  opportunity: 'high' | 'medium' | 'low'
  difficulty: 'easy' | 'medium' | 'hard'
  estimatedViews?: number
}

// Specialized AI Agents Types

export interface SpecializedAgent {
  id: string
  name: string
  specialty: string
  description: string
  avatar: string
  color: string
  status: 'online' | 'offline' | 'busy'
  capabilities: AgentCapability[]
  personality: AgentPersonality
  systemPrompt: string
  quickActions: QuickAction[]
  stats?: AgentStats
}

export type AgentCapability = 
  | 'algorithm_analysis'
  | 'seo_optimization'
  | 'ranking_factors'
  | 'recommendation_insights'
  | 'thumbnail_analysis'
  | 'design_optimization'
  | 'ctr_improvement'
  | 'visual_trends'
  | 'title_optimization'
  | 'keyword_research'
  | 'psychology_triggers'
  | 'search_optimization'
  | 'trend_analysis'
  | 'competitor_research'
  | 'opportunity_identification'
  | 'market_insights'
  | 'growth_strategy'
  | 'audience_analysis'
  | 'content_planning'
  | 'monetization_optimization'

export interface AgentPersonality {
  tone: 'analytical' | 'creative' | 'persuasive' | 'investigative' | 'strategic'
  expertise: 'technical' | 'visual' | 'psychological' | 'strategic' | 'business'
  communication: 'data-driven' | 'inspiring' | 'compelling' | 'insightful' | 'goal-oriented'
}

export interface QuickAction {
  id: string
  label: string
  icon: string
  description?: string
}

export interface AgentStats {
  totalInteractions: number
  successfulAnalyses: number
  averageResponseTime: number
  userSatisfaction: number
  lastActive: Date
}

export interface AgentMessage {
  id: string
  type: 'user' | 'agent'
  content: string
  timestamp: Date
  agentId: string
  insights?: ResearchInsight[]
  recommendations?: string[]
  actionResult?: any
  isError?: boolean
  metadata?: {
    analysisType?: string
    confidence?: number
    processingTime?: number
  }
}

// Research Analysis Types

export interface CompetitorAnalysis {
  channelId: string
  channelName: string
  subscriberCount: number
  averageViews: number
  uploadFrequency: string
  topPerformingVideos: ResearchVideo[]
  contentStrategy: {
    mainTopics: string[]
    videoFormats: string[]
    uploadSchedule: string
    thumbnailStyle: string
  }
  strengths: string[]
  weaknesses: string[]
  opportunities: string[]
  threats: string[]
}

export interface TrendAnalysis {
  trend: TrendingTopic
  relatedVideos: ResearchVideo[]
  keyInsights: string[]
  contentGaps: string[]
  recommendedActions: string[]
  competitorResponse: string[]
  estimatedOpportunity: {
    viewsPotential: number
    competitionLevel: 'low' | 'medium' | 'high'
    timeToCapitalize: string
  }
}

// Export/Import Types

export interface WorkspaceExport {
  projectId: string
  exportedAt: Date
  videos: ResearchVideo[]
  insights: ResearchInsight[]
  notes: ResearchNote[]
  summary: {
    totalItems: number
    keyFindings: string[]
    recommendedActions: string[]
  }
}

export interface ContentStudioImport {
  importId: string
  sourceProject: string
  contentIdeas: ContentIdea[]
  researchInsights: ResearchInsight[]
  competitorData: CompetitorAnalysis[]
  trendData: TrendAnalysis[]
}

export interface ContentIdea {
  id: string
  title: string
  description: string
  sourceVideo?: string
  sourceInsight?: string
  estimatedPerformance: number
  difficulty: 'easy' | 'medium' | 'hard'
  requiredResources: string[]
  suggestedPillar?: string
  tags: string[]
}
