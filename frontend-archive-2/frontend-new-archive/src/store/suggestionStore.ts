import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export type SuggestionType = 'content_idea' | 'title_optimization' | 'script_suggestion' | 'hook_improvement' | 'general'

export interface SavedSuggestion {
  id: string
  type: SuggestionType
  content: string
  category: string
  timestamp: Date
  isImplemented: boolean
  implementedAt?: Date
  feedback?: 'helpful' | 'not_helpful'
  tags: string[]
}

export interface ImplementationOption {
  id: string
  label: string
  action: string
  icon: string
}

export interface SuggestionState {
  savedSuggestions: SavedSuggestion[]
  implementationHistory: string[]
  analytics: {
    totalSuggestions: number
    implementedCount: number
    helpfulCount: number
    notHelpfulCount: number
  }
  
  // Actions
  saveSuggestion: (suggestion: Omit<SavedSuggestion, 'id' | 'timestamp'>) => void
  implementSuggestion: (suggestionId: string, implementationDetails?: any) => void
  provideFeedback: (suggestionId: string, feedback: 'helpful' | 'not_helpful') => void
  deleteSuggestion: (suggestionId: string) => void
  getSuggestionsByType: (type: SuggestionType) => SavedSuggestion[]
  getImplementationOptions: (type: SuggestionType) => ImplementationOption[]
  clearHistory: () => void
  getAnalytics: () => any
}

const implementationOptionsMap: Record<SuggestionType, ImplementationOption[]> = {
  content_idea: [
    { id: 'add_to_tasks', label: 'Convert to Task', action: 'add_to_tasks', icon: '📋' },
    { id: 'save_chat', label: 'Save Chat', action: 'save_chat', icon: '💬' }
  ],
  title_optimization: [
    { id: 'add_to_tasks', label: 'Convert to Task', action: 'add_to_tasks', icon: '📋' },
    { id: 'save_chat', label: 'Save Chat', action: 'save_chat', icon: '💬' }
  ],
  script_suggestion: [
    { id: 'add_to_tasks', label: 'Convert to Task', action: 'add_to_tasks', icon: '📋' },
    { id: 'save_chat', label: 'Save Chat', action: 'save_chat', icon: '💬' }
  ],
  hook_improvement: [
    { id: 'add_to_tasks', label: 'Convert to Task', action: 'add_to_tasks', icon: '📋' },
    { id: 'save_chat', label: 'Save Chat', action: 'save_chat', icon: '💬' }
  ],
  general: [
    { id: 'add_to_tasks', label: 'Convert to Task', action: 'add_to_tasks', icon: '📋' },
    { id: 'save_chat', label: 'Save Chat', action: 'save_chat', icon: '💬' }
  ]
}

export const useSuggestionStore = create<SuggestionState>()(
  persist(
    (set, get) => ({
      savedSuggestions: [],
      implementationHistory: [],
      analytics: {
        totalSuggestions: 0,
        implementedCount: 0,
        helpfulCount: 0,
        notHelpfulCount: 0
      },

      saveSuggestion: (suggestion) => {
        const id = `suggestion_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
        const newSuggestion: SavedSuggestion = {
          ...suggestion,
          id,
          timestamp: new Date()
        }
        
        set((state) => ({
          savedSuggestions: [...state.savedSuggestions, newSuggestion],
          analytics: {
            ...state.analytics,
            totalSuggestions: state.analytics.totalSuggestions + 1
          }
        }))
      },

      implementSuggestion: (suggestionId, _implementationDetails) => {
        set((state) => ({
          savedSuggestions: state.savedSuggestions.map(suggestion =>
            suggestion.id === suggestionId
              ? { ...suggestion, isImplemented: true, implementedAt: new Date() }
              : suggestion
          ),
          implementationHistory: [...state.implementationHistory, suggestionId],
          analytics: {
            ...state.analytics,
            implementedCount: state.analytics.implementedCount + 1
          }
        }))
      },

      provideFeedback: (suggestionId, feedback) => {
        set((state) => ({
          savedSuggestions: state.savedSuggestions.map(suggestion =>
            suggestion.id === suggestionId
              ? { ...suggestion, feedback }
              : suggestion
          ),
          analytics: {
            ...state.analytics,
            helpfulCount: feedback === 'helpful' 
              ? state.analytics.helpfulCount + 1 
              : state.analytics.helpfulCount,
            notHelpfulCount: feedback === 'not_helpful' 
              ? state.analytics.notHelpfulCount + 1 
              : state.analytics.notHelpfulCount
          }
        }))
      },

      deleteSuggestion: (suggestionId) => {
        set((state) => ({
          savedSuggestions: state.savedSuggestions.filter(s => s.id !== suggestionId)
        }))
      },

      getSuggestionsByType: (type) => {
        return get().savedSuggestions.filter(s => s.type === type)
      },

      getImplementationOptions: (type) => {
        return implementationOptionsMap[type] || implementationOptionsMap.general
      },

      clearHistory: () => {
        set({
          savedSuggestions: [],
          implementationHistory: [],
          analytics: {
            totalSuggestions: 0,
            implementedCount: 0,
            helpfulCount: 0,
            notHelpfulCount: 0
          }
        })
      },

      getAnalytics: () => {
        const state = get()
        return {
          ...state.analytics,
          implementationRate: state.analytics.totalSuggestions > 0 
            ? (state.analytics.implementedCount / state.analytics.totalSuggestions * 100).toFixed(1)
            : 0,
          helpfulnessRate: (state.analytics.helpfulCount + state.analytics.notHelpfulCount) > 0
            ? (state.analytics.helpfulCount / (state.analytics.helpfulCount + state.analytics.notHelpfulCount) * 100).toFixed(1)
            : 0
        }
      }
    }),
    {
      name: 'suggestion-store',
      partialize: (state) => ({
        savedSuggestions: state.savedSuggestions,
        implementationHistory: state.implementationHistory,
        analytics: state.analytics
      })
    }
  )
)