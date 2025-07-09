import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface AvatarCustomization {
  name: string
  avatar: string
  color: string
  size: 'normal' | 'large' | 'xlarge'
}

interface AvatarState {
  customization: AvatarCustomization
  isCustomizing: boolean
  setName: (name: string) => void
  setAvatar: (avatar: string) => void
  setColor: (color: string) => void
  setSize: (size: AvatarCustomization['size']) => void
  openCustomization: () => void
  closeCustomization: () => void
  resetToDefaults: () => void
}

const defaultCustomization: AvatarCustomization = {
  name: 'AI Assistant',
  avatar: 'MateBlue.svg',
  color: '#6366f1', // Primary blue
  size: 'xlarge'
}

export const brandColors = [
  { name: 'Primary Blue', value: '#6366f1' },
  { name: 'Purple', value: '#8b5cf6' },
  { name: 'Teal', value: '#14b8a6' },
  { name: 'Green', value: '#22c55e' },
  { name: 'Orange', value: '#f97316' },
  { name: 'Pink', value: '#ec4899' },
  { name: 'Red', value: '#ef4444' },
  { name: 'Yellow', value: '#eab308' }
]

export const useAvatarStore = create<AvatarState>()(
  persist(
    (set) => ({
      customization: defaultCustomization,
      isCustomizing: false,
      
      setName: (name: string) => 
        set((state) => ({
          customization: { ...state.customization, name }
        })),
      
      setAvatar: (avatar: string) =>
        set((state) => ({
          customization: { ...state.customization, avatar }
        })),
      
      setColor: (color: string) =>
        set((state) => ({
          customization: { ...state.customization, color }
        })),
      
      setSize: (size: AvatarCustomization['size']) =>
        set((state) => ({
          customization: { ...state.customization, size }
        })),
      
      openCustomization: () => set({ isCustomizing: true }),
      closeCustomization: () => set({ isCustomizing: false }),
      
      resetToDefaults: () =>
        set({
          customization: defaultCustomization,
          isCustomizing: false
        })
    }),
    {
      name: 'avatar-customization',
      partialize: (state) => ({ customization: state.customization })
    }
  )
)