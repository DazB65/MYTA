import { ref, computed } from 'vue'

export interface Recommendation {
  id: string
  type: string
  title: string
  description: string
  category: string
  priority: string
  source: string // 'video-modal', 'dashboard', 'agent-chat', etc.
  sourceId?: string // video ID, agent ID, etc.
  agentId?: string
  createdAt: Date
  convertedToTask?: boolean
  taskId?: string
}

// Global state for recommendations
const recommendations = ref<Recommendation[]>([])
const convertedRecommendations = ref<Set<string>>(new Set())

export const useRecommendations = () => {
  
  /**
   * Add a new recommendation
   */
  const addRecommendation = (recommendation: Omit<Recommendation, 'id' | 'createdAt'>) => {
    const newRecommendation: Recommendation = {
      ...recommendation,
      id: `rec_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      createdAt: new Date()
    }
    
    recommendations.value.push(newRecommendation)
    return newRecommendation.id
  }

  /**
   * Mark a recommendation as converted to task
   */
  const markAsConverted = (recommendationId: string, taskId?: string) => {
    const recommendation = recommendations.value.find(r => r.id === recommendationId)
    if (recommendation) {
      recommendation.convertedToTask = true
      recommendation.taskId = taskId
      convertedRecommendations.value.add(recommendationId)
    }
  }

  /**
   * Remove a recommendation
   */
  const removeRecommendation = (recommendationId: string) => {
    const index = recommendations.value.findIndex(r => r.id === recommendationId)
    if (index !== -1) {
      recommendations.value.splice(index, 1)
      convertedRecommendations.value.delete(recommendationId)
    }
  }

  /**
   * Get recommendations by source
   */
  const getRecommendationsBySource = (source: string, sourceId?: string) => {
    return recommendations.value.filter(r => {
      if (sourceId) {
        return r.source === source && r.sourceId === sourceId && !r.convertedToTask
      }
      return r.source === source && !r.convertedToTask
    })
  }

  /**
   * Get recommendations by agent
   */
  const getRecommendationsByAgent = (agentId: string) => {
    return recommendations.value.filter(r => r.agentId === agentId && !r.convertedToTask)
  }

  /**
   * Check if a recommendation is converted
   */
  const isConverted = (recommendationId: string) => {
    return convertedRecommendations.value.has(recommendationId)
  }

  /**
   * Get all active (non-converted) recommendations
   */
  const activeRecommendations = computed(() => {
    return recommendations.value.filter(r => !r.convertedToTask)
  })

  /**
   * Get converted recommendations
   */
  const convertedRecommendationsList = computed(() => {
    return recommendations.value.filter(r => r.convertedToTask)
  })

  /**
   * Clear all recommendations for a specific source
   */
  const clearRecommendationsForSource = (source: string, sourceId?: string) => {
    recommendations.value = recommendations.value.filter(r => {
      if (sourceId) {
        return !(r.source === source && r.sourceId === sourceId)
      }
      return r.source !== source
    })
  }

  /**
   * Get recommendation statistics
   */
  const getStats = () => {
    const total = recommendations.value.length
    const converted = recommendations.value.filter(r => r.convertedToTask).length
    const active = total - converted
    
    return {
      total,
      active,
      converted,
      conversionRate: total > 0 ? Math.round((converted / total) * 100) : 0
    }
  }

  return {
    // State
    recommendations: computed(() => recommendations.value),
    convertedRecommendations: computed(() => convertedRecommendations.value),
    activeRecommendations,
    convertedRecommendationsList,

    // Actions
    addRecommendation,
    markAsConverted,
    removeRecommendation,
    getRecommendationsBySource,
    getRecommendationsByAgent,
    isConverted,
    clearRecommendationsForSource,
    getStats
  }
}
