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
    { id: 'calendar', label: 'Add to Content Calendar', action: 'add_to_calendar', icon: '📅' },
    { id: 'draft', label: 'Create Draft', action: 'create_draft', icon: '✏️' },
    { id: 'research', label: 'Save for Research', action: 'save_research', icon: '🔍' }
  ],
  title_optimization: [
    { id: 'apply_video', label: 'Apply to Video', action: 'apply_to_video', icon: '🎬' },
    { id: 'save_template', label: 'Save as Template', action: 'save_template', icon: '📋' },
    { id: 'test_variations', label: 'Test Variations', action: 'test_variations', icon: '🧪' }
  ],
  script_suggestion: [
    { id: 'save_scripts', label: 'Save to Scripts', action: 'save_to_scripts', icon: '📝' },
    { id: 'export_doc', label: 'Export as Document', action: 'export_document', icon: '📄' },
    { id: 'schedule_review', label: 'Schedule Review', action: 'schedule_review', icon: '⏰' }
  ],
  hook_improvement: [
    { id: 'copy_clipboard', label: 'Copy to Clipboard', action: 'copy_to_clipboard', icon: '📋' },
    { id: 'save_hooks', label: 'Save to Hook Library', action: 'save_to_hooks', icon: '🎣' },
    { id: 'apply_current', label: 'Apply to Current Video', action: 'apply_current', icon: '🎯' }
  ],
  general: [
    { id: 'save_note', label: 'Save as Note', action: 'save_as_note', icon: '📝' },
    { id: 'share', label: 'Share', action: 'share', icon: '🔗' },
    { id: 'bookmark', label: 'Bookmark', action: 'bookmark', icon: '🔖' }
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