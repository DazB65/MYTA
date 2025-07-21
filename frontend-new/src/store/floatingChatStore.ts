import { create } from 'zustand'

interface FloatingChatState {
  isOpen: boolean
  position: { x: number; y: number }
  isDragging: boolean
  setOpen: (open: boolean) => void
  setPosition: (position: { x: number; y: number }) => void
  setDragging: (dragging: boolean) => void
  openChat: () => void
}

export const useFloatingChatStore = create<FloatingChatState>((set) => ({
  isOpen: false,
  position: { x: 20, y: 20 },
  isDragging: false,
  setOpen: (open) => set({ isOpen: open }),
  setPosition: (position) => set({ position }),
  setDragging: (dragging) => set({ isDragging: dragging }),
  openChat: () => set({ isOpen: true }),
}))