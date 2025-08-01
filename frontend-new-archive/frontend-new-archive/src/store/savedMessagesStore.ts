import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface SavedMessage {
  id: string
  content: string
  timestamp: number
  agentName: string
  avatar: string
  category?: string
  tags?: string[]
  notes?: string
}

interface SavedMessagesState {
  savedMessages: SavedMessage[]
  categories: string[]
  
  // Actions
  saveMessage: (message: Omit<SavedMessage, 'id' | 'timestamp'>) => void
  unsaveMessage: (messageId: string) => void
  updateMessage: (messageId: string, updates: Partial<SavedMessage>) => void
  addCategory: (category: string) => void
  removeCategory: (category: string) => void
  getMessagesByCategory: (category: string) => SavedMessage[]
  searchMessages: (query: string) => SavedMessage[]
  clearAll: () => void
  isMessageSaved: (messageContent: string) => boolean
}

export const useSavedMessagesStore = create<SavedMessagesState>()(
  persist(
    (set, get) => ({
      savedMessages: [],
      categories: ['General', 'Ideas', 'Scripts', 'Analytics', 'Strategy'],
      
      saveMessage: (message) => {
        const newMessage: SavedMessage = {
          ...message,
          id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
          timestamp: Date.now(),
          category: message.category || 'General'
        }
        
        set((state) => ({
          savedMessages: [newMessage, ...state.savedMessages]
        }))
      },
      
      unsaveMessage: (messageId) => {
        set((state) => ({
          savedMessages: state.savedMessages.filter(msg => msg.id !== messageId)
        }))
      },
      
      updateMessage: (messageId, updates) => {
        set((state) => ({
          savedMessages: state.savedMessages.map(msg => 
            msg.id === messageId ? { ...msg, ...updates } : msg
          )
        }))
      },
      
      addCategory: (category) => {
        set((state) => ({
          categories: [...state.categories, category]
        }))
      },
      
      removeCategory: (category) => {
        set((state) => ({
          categories: state.categories.filter(cat => cat !== category),
          savedMessages: state.savedMessages.map(msg => 
            msg.category === category ? { ...msg, category: 'General' } : msg
          )
        }))
      },
      
      getMessagesByCategory: (category) => {
        return get().savedMessages.filter(msg => msg.category === category)
      },
      
      searchMessages: (query) => {
        const messages = get().savedMessages
        const lowercaseQuery = query.toLowerCase()
        
        return messages.filter(msg => 
          msg.content.toLowerCase().includes(lowercaseQuery) ||
          msg.agentName.toLowerCase().includes(lowercaseQuery) ||
          msg.category?.toLowerCase().includes(lowercaseQuery) ||
          msg.tags?.some(tag => tag.toLowerCase().includes(lowercaseQuery)) ||
          msg.notes?.toLowerCase().includes(lowercaseQuery)
        )
      },
      
      clearAll: () => {
        set({ savedMessages: [] })
      },
      
      isMessageSaved: (messageContent) => {
        return get().savedMessages.some(msg => msg.content === messageContent)
      }
    }),
    {
      name: 'Vidalytics-saved-messages',
      version: 1
    }
  )
)