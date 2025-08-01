import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { ChannelInfo, AgentSettings } from '@/types'

interface UserState {
  userId: string
  isOnboarded: boolean
  channelInfo: ChannelInfo
  agentSettings: AgentSettings
  
  // Actions
  setUserId: (userId: string) => void
  setOnboarded: (status: boolean) => void
  updateChannelInfo: (info: Partial<ChannelInfo>) => void
  updateAgentSettings: (settings: Partial<AgentSettings>) => void
  checkOnboardingStatus: () => Promise<void>
  generateUserId: () => string
  fetchRealChannelData: () => Promise<void>
}

const defaultChannelInfo: ChannelInfo = {
  name: 'Unknown',
  channel_id: '',
  niche: 'Unknown',
  content_type: 'Unknown',
  subscriber_count: 0,
  avg_view_count: 0,
  total_view_count: 0,
  video_count: 0,
  ctr: 0,
  retention: 0,
  upload_frequency: 'Unknown',
  video_length: 'Unknown',
  monetization_status: 'Unknown',
  primary_goal: 'Unknown',
  notes: '',
  created_date: '',
}

const defaultAgentSettings: AgentSettings = {
  avatar: 'MateBlue.svg',
  name: 'Your Personal Agent',
  personality: 'professional',
  responseLength: 'medium',
}

export const useUserStore = create<UserState>()(
  persist(
    (set, get) => ({
      userId: '',
      isOnboarded: false,
      channelInfo: defaultChannelInfo,
      agentSettings: defaultAgentSettings,

      setUserId: (userId) => set({ userId }),

      setOnboarded: (status) => set({ isOnboarded: status }),

      updateChannelInfo: (info) =>
        set((state) => ({
          channelInfo: { ...state.channelInfo, ...info },
        })),

      updateAgentSettings: (settings) =>
        set((state) => ({
          agentSettings: { ...state.agentSettings, ...settings },
        })),

      checkOnboardingStatus: async () => {
        const state = get()
        
        // Check if userId exists in localStorage first
        const storedUserId = localStorage.getItem('Vidalytics_user_id')
        let currentUserId = state.userId || storedUserId
        
        if (!currentUserId) {
          currentUserId = state.generateUserId()
          set({ userId: currentUserId })
        } else if (currentUserId !== state.userId) {
          // Update store with localStorage value
          set({ userId: currentUserId })
        }
        
        console.log('User ID set to:', currentUserId)
        
        // Check if onboarding is complete
        const onboarded = localStorage.getItem('Vidalytics_onboarded') === 'true'
        set({ isOnboarded: onboarded })
        
        // If onboarded, immediately fetch real channel data to override any stale data
        if (onboarded && currentUserId) {
          try {
            const response = await fetch(`/api/agent/context/${currentUserId}`)
            if (response.ok) {
              const data = await response.json()
              if (data.status === 'success' && data.channel_info) {
                console.log('🔄 Overriding stored data with real YouTube channel data:', data.channel_info.name)
                set((state) => ({
                  ...state,
                  channelInfo: { 
                    ...data.channel_info
                  }
                }))
              }
            }
          } catch (error) {
            console.error('Failed to fetch real channel data during onboarding check:', error)
          }
        }
      },

      generateUserId: () => {
        const userId = 'user_' + Math.random().toString(36).substring(2, 15)
        localStorage.setItem('Vidalytics_user_id', userId)
        return userId
      },

      fetchRealChannelData: async () => {
        const state = get()
        if (!state.userId) return

        try {
          const response = await fetch(`/api/agent/context/${state.userId}`)
          if (response.ok) {
            const data = await response.json()
            if (data.status === 'success' && data.channel_info) {
              // Update with real YouTube channel data
              set((state) => ({
                channelInfo: { 
                  ...state.channelInfo, 
                  ...data.channel_info,
                  // Ensure we use the real YouTube channel name
                  name: data.channel_info.name
                }
              }))
            }
          }
        } catch (error) {
          console.error('Failed to fetch real channel data:', error)
        }
      },
    }),
    {
      name: 'Vidalytics-user',
      partialize: (state) => ({
        userId: state.userId,
        channelInfo: state.channelInfo,
        agentSettings: state.agentSettings,
      }),
    }
  )
)