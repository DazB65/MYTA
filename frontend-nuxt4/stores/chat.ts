import { defineStore } from 'pinia'
import { v4 as uuidv4 } from 'uuid'
import { computed, readonly, ref } from 'vue'
import type { ChatMessage, ChatSession, MessageType } from '../types/agents'

export const useChatStore = defineStore('chat', () => {
  // State
  const sessions = ref<Map<string, ChatSession>>(new Map())
  const activeSessionId = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const typingAgents = ref<Set<string>>(new Set())
  const isConnected = ref(false)
  const messageQueue = ref<ChatMessage[]>([])
  const lastActivity = ref<Date | null>(null)

  // Getters
  const allSessions = computed(() => Array.from(sessions.value.values()))
  const activeSession = computed(() =>
    activeSessionId.value ? sessions.value.get(activeSessionId.value) : null
  )

  const recentSessions = computed(() =>
    allSessions.value.sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime()).slice(0, 10)
  )

  const sessionsByAgent = computed(() => {
    const byAgent: Record<string, ChatSession[]> = {}
    allSessions.value.forEach(session => {
      if (!byAgent[session.agentId]) byAgent[session.agentId] = []
      byAgent[session.agentId].push(session)
    })
    return byAgent
  })

  const totalMessages = computed(() =>
    allSessions.value.reduce((total, session) => total + session.messages.length, 0)
  )

  const isAnyAgentTyping = computed(() => typingAgents.value.size > 0)

  const activeSessionMessages = computed(() => activeSession.value?.messages || [])

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
    if (typing) {
      typingAgents.value.add(agentId)
    } else {
      typingAgents.value.delete(agentId)
    }
  }

  const setActiveSession = (sessionId: string | null) => {
    activeSessionId.value = sessionId
    if (sessionId) {
      lastActivity.value = new Date()
    }
  }

  const closeSession = (sessionId: string) => {
    const session = sessions.value.get(sessionId)
    if (session) {
      session.isActive = false
      if (activeSessionId.value === sessionId) {
        activeSessionId.value = null
      }
    }
  }

  const deleteSession = (sessionId: string) => {
    sessions.value.delete(sessionId)
    if (activeSessionId.value === sessionId) {
      activeSessionId.value = null
    }
  }

  const updateConnectionStatus = (connected: boolean) => {
    isConnected.value = connected
    if (!connected) {
      typingAgents.value.clear()
    }
  }

  const addMessageToQueue = (message: ChatMessage) => {
    messageQueue.value.push(message)
  }

  const processMessageQueue = () => {
    while (messageQueue.value.length > 0) {
      const message = messageQueue.value.shift()
      if (message) {
        receiveMessage(message)
      }
    }
  }

  const clearAllSessions = () => {
    sessions.value.clear()
    activeSessionId.value = null
    typingAgents.value.clear()
    messageQueue.value = []
  }

  const getSessionById = (sessionId: string) => {
    return sessions.value.get(sessionId)
  }

  const updateSessionTitle = (sessionId: string, title: string) => {
    const session = sessions.value.get(sessionId)
    if (session) {
      session.title = title
      session.updatedAt = new Date()
    }
  }

  return {
    // State
    sessions: readonly(sessions),
    activeSessionId: readonly(activeSessionId),
    loading: readonly(loading),
    error: readonly(error),
    typingAgents: readonly(typingAgents),
    isConnected: readonly(isConnected),
    lastActivity: readonly(lastActivity),

    // Getters
    allSessions,
    activeSession,
    recentSessions,
    sessionsByAgent,
    totalMessages,
    isAnyAgentTyping,
    activeSessionMessages,

    // Actions
    createSession,
    sendMessage,
    receiveMessage,
    setAgentTyping,
    setActiveSession,
    closeSession,
    deleteSession,
    updateConnectionStatus,
    addMessageToQueue,
    processMessageQueue,
    clearAllSessions,
    getSessionById,
    updateSessionTitle,
  }
})
