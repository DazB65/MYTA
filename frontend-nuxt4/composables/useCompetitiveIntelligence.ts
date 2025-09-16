/**
 * Competitive Intelligence 2.0 Composable
 * Advanced market positioning and competitive strategy
 */

import { ref, computed, reactive } from 'vue'

// Types
interface CompetitorProfile {
  competitor_id: string
  name: string
  channel_url: string
  tier: string
  subscriber_count: number
  avg_views: number
  growth_rate: number
  strengths: string[]
  weaknesses: string[]
  content_strategy: Record<string, any>
}

interface ContentGap {
  gap_id: string
  topic: string
  search_volume: number
  competition_level: string
  opportunity_score: number
  potential_views: number
  difficulty_rating: number
  suggested_approach: string
  keywords: string[]
  estimated_effort: string
}

interface MarketOpportunity {
  opportunity_id: string
  type: string
  title: string
  description: string
  opportunity_score: number
  effort_required: string
  time_sensitivity: string
  potential_impact: string
  action_steps: string[]
  competitors_missing: string[]
}

interface CompetitiveThreat {
  threat_id: string
  competitor_name: string
  threat_level: string
  threat_type: string
  description: string
  impact_assessment: string
  timeline: string
  mitigation_strategies: string[]
}

interface BlueOceanOpportunity {
  ocean_id: string
  market_name: string
  market_size: number
  competition_density: number
  entry_difficulty: string
  potential_roi: number
  unique_value_proposition: string
  success_probability: number
  investment_required: string
}

interface CompetitiveLandscape {
  analysis_timestamp: string
  analysis_depth: string
  competitive_landscape: {
    total_competitors: number
    direct_competitors: number
    aspirational_targets: number
    market_position: Record<string, any>
  }
  competitor_profiles: CompetitorProfile[]
  content_gaps: ContentGap[]
  market_opportunities: MarketOpportunity[]
  competitive_threats: CompetitiveThreat[]
  blue_ocean_opportunities: BlueOceanOpportunity[]
  strategic_recommendations: Record<string, any>
  next_analysis_date: string
}

interface QuickInsights {
  market_position: Record<string, any>
  top_opportunity: MarketOpportunity | null
  urgent_threat: CompetitiveThreat | null
  recommended_action: string
  competitive_score: number
}

export const useCompetitiveIntelligence = () => {
  // State
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const lastAnalysis = ref<CompetitiveLandscape | null>(null)
  const quickInsights = ref<QuickInsights | null>(null)
  
  // Reactive filters
  const filters = reactive({
    analysisDepth: 'comprehensive',
    includeBlueOceans: true,
    competitorLimit: 10,
    minOpportunityScore: 0,
    threatLevel: null as string | null,
    timeframe: 'all'
  })

  // Computed
  const hasAnalysis = computed(() => lastAnalysis.value !== null)
  const competitiveScore = computed(() => quickInsights.value?.competitive_score || 0)
  const marketPosition = computed(() => quickInsights.value?.market_position?.position_category || 'Unknown')
  
  const topOpportunities = computed(() => {
    if (!lastAnalysis.value) return []
    return lastAnalysis.value.market_opportunities
      .filter(opp => opp.opportunity_score >= filters.minOpportunityScore)
      .sort((a, b) => b.opportunity_score - a.opportunity_score)
      .slice(0, 5)
  })
  
  const urgentThreats = computed(() => {
    if (!lastAnalysis.value) return []
    return lastAnalysis.value.competitive_threats
      .filter(threat => ['high', 'critical'].includes(threat.threat_level))
      .sort((a, b) => {
        const priority = { critical: 4, high: 3, medium: 2, low: 1 }
        return priority[b.threat_level as keyof typeof priority] - priority[a.threat_level as keyof typeof priority]
      })
  })
  
  const contentGapsByScore = computed(() => {
    if (!lastAnalysis.value) return []
    return lastAnalysis.value.content_gaps
      .filter(gap => gap.opportunity_score >= filters.minOpportunityScore)
      .sort((a, b) => b.opportunity_score - a.opportunity_score)
  })

  // API Functions
  const analyzeCompetitiveLandscape = async (userId: string) => {
    try {
      isLoading.value = true
      error.value = null

      const response = await $fetch('/api/competitive-intelligence/analyze', {
        method: 'POST',
        body: {
          user_id: userId,
          analysis_depth: filters.analysisDepth,
          include_blue_oceans: filters.includeBlueOceans,
          competitor_limit: filters.competitorLimit
        }
      })

      lastAnalysis.value = response as CompetitiveLandscape
      return response
    } catch (err: any) {
      error.value = err.message || 'Failed to analyze competitive landscape'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const getQuickInsights = async (userId: string) => {
    try {
      isLoading.value = true
      error.value = null

      const response = await $fetch(`/api/competitive-intelligence/quick-insights/${userId}`)
      quickInsights.value = response as QuickInsights
      return response
    } catch (err: any) {
      error.value = err.message || 'Failed to get quick insights'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const getContentGaps = async (userId: string, limit = 10, minScore = 0) => {
    try {
      isLoading.value = true
      error.value = null

      const response = await $fetch(`/api/competitive-intelligence/content-gaps/${userId}`, {
        query: {
          limit,
          min_opportunity_score: minScore
        }
      })

      return response
    } catch (err: any) {
      error.value = err.message || 'Failed to get content gaps'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const getMarketOpportunities = async (userId: string, opportunityType?: string, minScore = 0) => {
    try {
      isLoading.value = true
      error.value = null

      const query: Record<string, any> = { min_score: minScore }
      if (opportunityType) query.opportunity_type = opportunityType

      const response = await $fetch(`/api/competitive-intelligence/market-opportunities/${userId}`, {
        query
      })

      return response
    } catch (err: any) {
      error.value = err.message || 'Failed to get market opportunities'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const getCompetitiveThreats = async (userId: string, threatLevel?: string) => {
    try {
      isLoading.value = true
      error.value = null

      const query: Record<string, any> = {}
      if (threatLevel) query.threat_level = threatLevel

      const response = await $fetch(`/api/competitive-intelligence/competitive-threats/${userId}`, {
        query
      })

      return response
    } catch (err: any) {
      error.value = err.message || 'Failed to get competitive threats'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const getStrategicRecommendations = async (userId: string, timeframe = 'all') => {
    try {
      isLoading.value = true
      error.value = null

      const response = await $fetch(`/api/competitive-intelligence/strategic-recommendations/${userId}`, {
        query: { timeframe }
      })

      return response
    } catch (err: any) {
      error.value = err.message || 'Failed to get strategic recommendations'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Utility Functions
  const getOpportunityTypeIcon = (type: string): string => {
    const icons = {
      content_gap: '🎯',
      timing_advantage: '⚡',
      format_innovation: '🚀',
      audience_overlap: '👥',
      trending_topic: '📈',
      blue_ocean: '🌊'
    }
    return icons[type as keyof typeof icons] || '💡'
  }

  const getThreatLevelColor = (level: string): string => {
    const colors = {
      low: 'text-green-400',
      medium: 'text-yellow-400',
      high: 'text-orange-400',
      critical: 'text-red-400'
    }
    return colors[level as keyof typeof colors] || 'text-gray-400'
  }

  const getCompetitorTierColor = (tier: string): string => {
    const colors = {
      direct: 'text-blue-400',
      aspirational: 'text-purple-400',
      adjacent: 'text-green-400',
      emerging: 'text-orange-400'
    }
    return colors[tier as keyof typeof colors] || 'text-gray-400'
  }

  const formatOpportunityScore = (score: number): string => {
    if (score >= 80) return 'Excellent'
    if (score >= 60) return 'Good'
    if (score >= 40) return 'Moderate'
    if (score >= 20) return 'Low'
    return 'Very Low'
  }

  const formatGrowthRate = (rate: number): string => {
    return `${(rate * 100).toFixed(1)}%`
  }

  const formatSubscriberCount = (count: number): string => {
    if (count >= 1000000) return `${(count / 1000000).toFixed(1)}M`
    if (count >= 1000) return `${(count / 1000).toFixed(1)}K`
    return count.toString()
  }

  const getEffortColor = (effort: string): string => {
    const colors = {
      'Low': 'text-green-400',
      'Medium': 'text-yellow-400',
      'High': 'text-orange-400',
      'Very High': 'text-red-400'
    }
    return colors[effort as keyof typeof colors] || 'text-gray-400'
  }

  const getTimeSensitivityColor = (sensitivity: string): string => {
    if (sensitivity.toLowerCase().includes('high')) return 'text-red-400'
    if (sensitivity.toLowerCase().includes('medium')) return 'text-yellow-400'
    return 'text-green-400'
  }

  // Reset function
  const reset = () => {
    isLoading.value = false
    error.value = null
    lastAnalysis.value = null
    quickInsights.value = null
    Object.assign(filters, {
      analysisDepth: 'comprehensive',
      includeBlueOceans: true,
      competitorLimit: 10,
      minOpportunityScore: 0,
      threatLevel: null,
      timeframe: 'all'
    })
  }

  return {
    // State
    isLoading,
    error,
    lastAnalysis,
    quickInsights,
    filters,

    // Computed
    hasAnalysis,
    competitiveScore,
    marketPosition,
    topOpportunities,
    urgentThreats,
    contentGapsByScore,

    // API Functions
    analyzeCompetitiveLandscape,
    getQuickInsights,
    getContentGaps,
    getMarketOpportunities,
    getCompetitiveThreats,
    getStrategicRecommendations,

    // Utility Functions
    getOpportunityTypeIcon,
    getThreatLevelColor,
    getCompetitorTierColor,
    formatOpportunityScore,
    formatGrowthRate,
    formatSubscriberCount,
    getEffortColor,
    getTimeSensitivityColor,

    // Actions
    reset
  }
}
