import { defineStore } from 'pinia'
import { ref, computed, readonly } from 'vue'
import { v4 as uuidv4 } from 'uuid'
import type { ChatMessage, ChatSession, MessageType } from '../types/agents'

export const useChatStore = defineStore('chat', () => {
  // State
  const sessions = ref<Map<string, ChatSession>>(new Map())
  const activeSessionId = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const allSessions = computed(() => Array.from(sessions.value.values()))
  const activeSession = computed(() =>
    activeSessionId.value ? sessions.value.get(activeSessionId.value) : null
  )

  // Actions
  const createSession = (agentId: string, title?: string): string => {
    const sessionId = uuidv4()
    const session: ChatSession = {
      id: sessionId,
      userId: 'demo-user',
      agentId,
      title: title || `Chat with Agent`,
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
      isActive: true,
    }

    sessions.value.set(sessionId, session)
    activeSessionId.value = sessionId
    return sessionId
  }

  const sendMessage = async (content: string, type: MessageType = 'text') => {
    if (!activeSession.value) {
      throw new Error('No active chat session')
    }

    const message: ChatMessage = {
      id: uuidv4(),
      agentId: activeSession.value.agentId,
      userId: 'demo-user',
      content,
      type,
      timestamp: new Date(),
      isFromUser: true,
    }

    activeSession.value.messages.push(message)
    activeSession.value.updatedAt = new Date()
    return message
  }

  const receiveMessage = (message: ChatMessage) => {
    const session = sessions.value.get(message.agentId)
    if (session) {
      session.messages.push(message)
      session.updatedAt = new Date()
    }
  }

  const setAgentTyping = (agentId: string, typing: boolean) => {
    console.log(`Agent ${agentId} typing: ${typing}`)
  }

  return {
    // State
    sessions: readonly(sessions),
    activeSessionId: readonly(activeSessionId),
    loading: readonly(loading),
    error: readonly(error),

    // Getters
    allSessions,
    activeSession,

    // Actions
    createSession,
    sendMessage,
    receiveMessage,
    setAgentTyping,
  }
})
