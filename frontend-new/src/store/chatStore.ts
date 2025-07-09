import { create } from 'zustand'
import type { ChatMessage, ThinkingMessage } from '@/types'

interface ChatState {
  messages: ChatMessage[]
  thinkingMessage: ThinkingMessage | null
  isLoading: boolean
  
  // Actions
  addMessage: (message: Omit<ChatMessage, 'id' | 'timestamp'>) => void
  addThinkingMessage: (message: string) => string
  removeThinkingMessage: () => void
  setLoading: (loading: boolean) => void
  clearMessages: () => void
}

const thinkingMessages = [
  "🤔 Let me think about your channel specifically...",
  "💭 Analyzing your niche and performance metrics...",
  "🎯 Considering your subscriber tier and goals...",
  "📊 Looking at your CTR and retention data...",
  "🧠 Crafting personalized advice for your channel...",
  "⚡ Processing your channel context...",
  "🎬 Thinking about your content strategy...",
  "🔍 Analyzing what works in your niche..."
]

export const useChatStore = create<ChatState>((set) => ({
  messages: [
    {
      id: 'welcome',
      role: 'agent',
      content: "Hello! I'm your AI content creation assistant. How can I help you today?",
      timestamp: new Date(),
    }
  ],
  thinkingMessage: null,
  isLoading: false,

  addMessage: (message) => {
    const newMessage: ChatMessage = {
      ...message,
      id: Date.now().toString(),
      timestamp: new Date(),
    }
    
    set((state) => ({
      messages: [...state.messages, newMessage],
    }))
  },

  addThinkingMessage: (customMessage) => {
    const message = customMessage || thinkingMessages[Math.floor(Math.random() * thinkingMessages.length)]
    const id = Date.now().toString()
    
    set({
      thinkingMessage: { id, message },
      isLoading: true,
    })
    
    return id
  },

  removeThinkingMessage: () => {
    set({
      thinkingMessage: null,
      isLoading: false,
    })
  },

  setLoading: (loading) => set({ isLoading: loading }),

  clearMessages: () => set({ 
    messages: [{
      id: 'welcome',
      role: 'agent',
      content: "Hello! I'm your AI content creation assistant. How can I help you today?",
      timestamp: new Date(),
    }] 
  }),
}))