/**
 * Goals Store for Creator Goal Management
 * Manages user-created goals and their progress
 */

import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface Goal {
  id: string
  title: string
  description: string
  type: 'subscribers' | 'views' | 'engagement' | 'revenue' | 'custom'
  targetValue: number
  currentValue: number
  targetDate?: string
  isCompleted: boolean
  createdAt: string
  updatedAt: string
  priority: 'high' | 'medium' | 'low'
  category: string
}

interface GoalsState {
  goals: Goal[]
  isLoading: boolean
  error: string | null
  
  // Actions
  addGoal: (goal: Omit<Goal, 'id' | 'createdAt' | 'updatedAt'>) => void
  updateGoal: (id: string, updates: Partial<Goal>) => void
  deleteGoal: (id: string) => void
  updateProgress: (id: string, currentValue: number) => void
  toggleComplete: (id: string) => void
  getGoalsByCategory: (category: string) => Goal[]
  getActiveGoals: () => Goal[]
  getCompletedGoals: () => Goal[]
  clearError: () => void
}

export const useGoalsStore = create<GoalsState>()(
  persist(
    (set, get) => ({
      goals: [
        // Default example goal
        {
          id: 'default-1',
          title: '100K Subscribers',
          description: 'Reach 100,000 subscribers milestone',
          type: 'subscribers',
          targetValue: 100000,
          currentValue: 67000,
          targetDate: '2024-12-31',
          isCompleted: false,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          priority: 'high',
          category: 'growth'
        }
      ],
      isLoading: false,
      error: null,

      addGoal: (goalData) => {
        const newGoal: Goal = {
          ...goalData,
          id: crypto.randomUUID(),
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        }
        
        set(state => ({
          goals: [...state.goals, newGoal],
          error: null
        }))
      },

      updateGoal: (id, updates) => {
        set(state => ({
          goals: state.goals.map(goal => 
            goal.id === id 
              ? { ...goal, ...updates, updatedAt: new Date().toISOString() }
              : goal
          ),
          error: null
        }))
      },

      deleteGoal: (id) => {
        set(state => ({
          goals: state.goals.filter(goal => goal.id !== id),
          error: null
        }))
      },

      updateProgress: (id, currentValue) => {
        set(state => ({
          goals: state.goals.map(goal => 
            goal.id === id 
              ? { 
                  ...goal, 
                  currentValue,
                  isCompleted: currentValue >= goal.targetValue,
                  updatedAt: new Date().toISOString()
                }
              : goal
          ),
          error: null
        }))
      },

      toggleComplete: (id) => {
        set(state => ({
          goals: state.goals.map(goal => 
            goal.id === id 
              ? { 
                  ...goal, 
                  isCompleted: !goal.isCompleted,
                  updatedAt: new Date().toISOString()
                }
              : goal
          ),
          error: null
        }))
      },

      getGoalsByCategory: (category) => {
        return get().goals.filter(goal => goal.category === category)
      },

      getActiveGoals: () => {
        return get().goals.filter(goal => !goal.isCompleted)
      },

      getCompletedGoals: () => {
        return get().goals.filter(goal => goal.isCompleted)
      },

      clearError: () => {
        set({ error: null })
      }
    }),
    {
      name: 'goals-store',
      partialize: (state) => ({
        goals: state.goals
      })
    }
  )
)

export default useGoalsStore