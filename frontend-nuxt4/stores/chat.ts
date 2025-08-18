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

    if (!content.trim()) {
      throw new Error('Message content cannot be empty')
    }

    try {
      loading.value = true
      error.value = null

      const message: ChatMessage = {
        id: uuidv4(),
        agentId: activeSession.value.agentId,
        userId: 'demo-user',
        content: content.trim(),
        type,
        timestamp: new Date(),
        isFromUser: true,
      }

      activeSession.value.messages.push(message)
      activeSession.value.updatedAt = new Date()
      lastActivity.value = new Date()

      // Save to localStorage
      saveChatData()

      return message
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to send message'
      throw err
    } finally {
      loading.value = false
    }
  }

  const receiveMessage = (message: ChatMessage) => {
    const session = sessions.value.get(message.agentId)
    if (session) {
      session.messages.push(message)
      session.updatedAt = new Date()
      lastActivity.value = new Date()
      saveChatData()
    }
  }

  const deleteMessage = (messageId: string) => {
    if (!activeSession.value) return false

    const messageIndex = activeSession.value.messages.findIndex(msg => msg.id === messageId)
    if (messageIndex > -1) {
      activeSession.value.messages.splice(messageIndex, 1)
      activeSession.value.updatedAt = new Date()
      saveChatData()
      return true
    }
    return false
  }

  const clearSession = (sessionId: string) => {
    const session = sessions.value.get(sessionId)
    if (session) {
      session.messages = []
      session.updatedAt = new Date()
      saveChatData()
    }
  }

  const deleteSession = (sessionId: string) => {
    sessions.value.delete(sessionId)
    if (activeSessionId.value === sessionId) {
      activeSessionId.value = null
    }
    saveChatData()
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
    saveChatData()
  }

  // Persistence functions
  const saveChatData = () => {
    if (typeof window === 'undefined') return

    try {
      const chatData = {
        sessions: Array.from(sessions.value.entries()).map(([id, session]) => [
          id,
          {
            ...session,
            createdAt: session.createdAt.toISOString(),
            updatedAt: session.updatedAt.toISOString(),
            messages: session.messages.map(msg => ({
              ...msg,
              timestamp: msg.timestamp.toISOString()
            }))
          }
        ]),
        activeSessionId: activeSessionId.value,
        lastActivity: lastActivity.value?.toISOString()
      }

      localStorage.setItem('chatData', JSON.stringify(chatData))
    } catch (error) {
      console.error('Failed to save chat data:', error)
    }
  }

  const loadChatData = () => {
    if (typeof window === 'undefined') return

    try {
      const savedData = localStorage.getItem('chatData')
      if (!savedData) return

      const chatData = JSON.parse(savedData)

      // Restore sessions
      const restoredSessions = new Map()
      chatData.sessions.forEach(([id, session]: [string, any]) => {
        restoredSessions.set(id, {
          ...session,
          createdAt: new Date(session.createdAt),
          updatedAt: new Date(session.updatedAt),
          messages: session.messages.map((msg: any) => ({
            ...msg,
            timestamp: new Date(msg.timestamp)
          }))
        })
      })

      sessions.value = restoredSessions
      activeSessionId.value = chatData.activeSessionId
      lastActivity.value = chatData.lastActivity ? new Date(chatData.lastActivity) : null
    } catch (error) {
      console.error('Failed to load chat data:', error)
      // Clear corrupted data
      localStorage.removeItem('chatData')
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
    deleteMessage,
    clearSession,
    updateConnectionStatus,
    addMessageToQueue,
    processMessageQueue,
    clearAllSessions,
    getSessionById,
    updateSessionTitle,
    saveChatData,
    loadChatData,
  }
})
