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
  checkOnboardingStatus: () => void
  generateUserId: () => string
}

const defaultChannelInfo: ChannelInfo = {
  name: 'Unknown',
  niche: 'Unknown',
  content_type: 'Unknown',
  subscriber_count: 0,
  avg_view_count: 0,
  ctr: 0,
  retention: 0,
  upload_frequency: 'Unknown',
  video_length: 'Unknown',
  monetization_status: 'Unknown',
  primary_goal: 'Unknown',
  notes: '',
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

      checkOnboardingStatus: () => {
        const state = get()
        
        // Check if userId exists in localStorage first
        const storedUserId = localStorage.getItem('creatormate_user_id')
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
        const onboarded = localStorage.getItem('creatormate_onboarded') === 'true'
        set({ isOnboarded: onboarded })
      },

      generateUserId: () => {
        const userId = 'user_' + Math.random().toString(36).substring(2, 15)
        localStorage.setItem('creatormate_user_id', userId)
        return userId
      },
    }),
    {
      name: 'creatormate-user',
      partialize: (state) => ({
        userId: state.userId,
        channelInfo: state.channelInfo,
        agentSettings: state.agentSettings,
      }),
    }
  )
)