import { useCallback } from 'react'
import { useChatStore } from '@/store/chatStore'
import { useUserStore } from '@/store/userStore'
import { api } from '@/services/api'

export function useChat() {
  const { messages, thinkingMessage, isLoading, addMessage, addThinkingMessage, removeThinkingMessage } = useChatStore()
  const { userId } = useUserStore()

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || isLoading) return

    // Add user message
    addMessage({ role: 'user', content })

    // Add thinking indicator
    addThinkingMessage('')

    try {
      const response = await api.agent.chat(content, userId)
      
      // Remove thinking indicator
      removeThinkingMessage()
      
      // Add agent response
      addMessage({ 
        role: 'agent', 
        content: response.response 
      })
    } catch (error) {
      // Remove thinking indicator
      removeThinkingMessage()
      
      // Add error message
      addMessage({ 
        role: 'agent', 
        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}. Please try again.`,
        isError: true
      })
    }
  }, [userId, isLoading, addMessage, addThinkingMessage, removeThinkingMessage])

  const sendQuickAction = useCallback(async (action: string, context = '') => {
    if (isLoading) return

    // Add user message for the action
    addMessage({ 
      role: 'user', 
      content: `${action.replace('_', ' ')} (Quick Action)` 
    })

    // Add thinking indicator
    addThinkingMessage('')

    try {
      const response = await api.agent.quickAction(action, userId, context)
      
      // Remove thinking indicator
      removeThinkingMessage()
      
      // Add agent response
      addMessage({ 
        role: 'agent', 
        content: response.response 
      })
    } catch (error) {
      // Remove thinking indicator
      removeThinkingMessage()
      
      // Add error message
      addMessage({ 
        role: 'agent', 
        content: `Sorry, I encountered an error with the action: ${error instanceof Error ? error.message : 'Unknown error'}. Please try again.`,
        isError: true
      })
    }
  }, [userId, isLoading, addMessage, addThinkingMessage, removeThinkingMessage])

  return {
    messages,
    thinkingMessage,
    isLoading,
    sendMessage,
    sendQuickAction,
  }
}