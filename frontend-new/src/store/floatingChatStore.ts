import { create } from 'zustand'

interface FloatingChatState {
  isOpen: boolean
  isMinimized: boolean
  
  // Actions
  openChat: () => void
  closeChat: () => void
  toggleMinimize: () => void
  setMinimized: (minimized: boolean) => void
}

export const useFloatingChatStore = create<FloatingChatState>((set) => ({
  isOpen: false,
  isMinimized: false,

  openChat: () => set({ isOpen: true, isMinimized: false }),
  
  closeChat: () => set({ isOpen: false, isMinimized: false }),
  
  toggleMinimize: () => set((state) => ({ isMinimized: !state.isMinimized })),
  
  setMinimized: (minimized) => set({ isMinimized: minimized }),
}))