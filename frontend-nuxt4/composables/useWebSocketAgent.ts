import { ref, onMounted, onUnmounted, watch } from 'vue'
import type { WebSocketMessage, WSMessageType, ChatMessage, AgentStatus } from '../types/agents'
import { useAgentsStore } from '../stores/agents'
import { useChatStore } from '../stores/chat'

export const useWebSocketAgent = () => {
  const agentsStore = useAgentsStore()
  const chatStore = useChatStore()
  
  const ws = ref<WebSocket | null>(null)
  const isConnected = ref(false)
  const reconnectAttempts = ref(0)
  const maxReconnectAttempts = 5
  const reconnectDelay = ref(1000)
  const heartbeatInterval = ref<NodeJS.Timeout | null>(null)

  const connect = () => {
    try {
      // Use environment variable or fallback to localhost
      const wsUrl = process.env.NUXT_WS_URL || 'ws://localhost:8000/ws'
      ws.value = new WebSocket(wsUrl)

      ws.value.onopen = () => {
        console.log('WebSocket connected to agent system')
        isConnected.value = true
        reconnectAttempts.value = 0
        reconnectDelay.value = 1000
        
        // Update store connection status
        agentsStore.updateConnectionStatus(true)
        chatStore.updateConnectionStatus(true)
        
        // Start heartbeat
        startHeartbeat()
        
        // Process any queued messages
        chatStore.processMessageQueue()
      }

      ws.value.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          handleMessage(message)
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }

      ws.value.onclose = () => {
        console.log('WebSocket disconnected from agent system')
        isConnected.value = false
        agentsStore.updateConnectionStatus(false)
        chatStore.updateConnectionStatus(false)
        stopHeartbeat()
        
        // Attempt to reconnect
        if (reconnectAttempts.value < maxReconnectAttempts) {
          setTimeout(() => {
            reconnectAttempts.value++
            reconnectDelay.value *= 2
            connect()
          }, reconnectDelay.value)
        }
      }

      ws.value.onerror = (error) => {
        console.error('WebSocket error:', error)
        agentsStore.setError('WebSocket connection error')
      }

    } catch (error) {
      console.error('Failed to create WebSocket connection:', error)
      agentsStore.setError('Failed to connect to agent system')
    }
  }

  const disconnect = () => {
    if (ws.value) {
      ws.value.close()
      ws.value = null
    }
    stopHeartbeat()
  }

  const sendMessage = (type: WSMessageType, payload: any, sessionId?: string) => {
    if (ws.value && isConnected.value) {
      const message: WebSocketMessage = {
        type,
        payload,
        timestamp: new Date(),
        sessionId,
      }
      ws.value.send(JSON.stringify(message))
    } else {
      console.warn('WebSocket not connected, message not sent:', { type, payload })
    }
  }

  const handleMessage = (message: WebSocketMessage) => {
    switch (message.type) {
      case 'agent_message':
        handleAgentMessage(message.payload)
        break
      
      case 'agent_status_change':
        handleAgentStatusChange(message.payload)
        break
      
      case 'insight_generated':
        handleInsightGenerated(message.payload)
        break
      
      case 'analysis_complete':
        handleAnalysisComplete(message.payload)
        break
      
      case 'heartbeat':
        // Update last heartbeat time
        agentsStore.updateConnectionStatus(true)
        break
      
      case 'error':
        handleError(message.payload)
        break
      
      default:
        console.log('Unknown message type:', message.type)
    }
  }

  const handleAgentMessage = (payload: ChatMessage) => {
    chatStore.receiveMessage(payload)
    
    // Stop typing indicator for this agent
    chatStore.setAgentTyping(payload.agentId, false)
  }

  const handleAgentStatusChange = (payload: { agentId: string; status: AgentStatus }) => {
    agentsStore.updateAgentStatus(payload.agentId, payload.status)
    
    // Handle typing status
    if (payload.status === 'thinking') {
      chatStore.setAgentTyping(payload.agentId, true)
    } else {
      chatStore.setAgentTyping(payload.agentId, false)
    }
  }

  const handleInsightGenerated = (payload: any) => {
    agentsStore.addInsight(payload)
  }

  const handleAnalysisComplete = (payload: any) => {
    console.log('Analysis complete:', payload)
    // Handle analysis completion
  }

  const handleError = (payload: { message: string; code?: string }) => {
    console.error('Agent system error:', payload)
    agentsStore.setError(payload.message)
  }

  const startHeartbeat = () => {
    heartbeatInterval.value = setInterval(() => {
      sendMessage('heartbeat', { timestamp: new Date() })
    }, 30000) // Send heartbeat every 30 seconds
  }

  const stopHeartbeat = () => {
    if (heartbeatInterval.value) {
      clearInterval(heartbeatInterval.value)
      heartbeatInterval.value = null
    }
  }

  // Public API for sending specific message types
  const sendChatMessage = (content: string, agentId: string, sessionId?: string) => {
    sendMessage('agent_message', {
      content,
      agentId,
      type: 'text',
      isFromUser: true,
    }, sessionId)
  }

  const requestAnalysis = (type: string, data: any, agentId: string) => {
    sendMessage('analysis_complete', {
      type,
      data,
      agentId,
    })
  }

  const joinSession = (sessionId: string) => {
    sendMessage('user_joined', { sessionId })
  }

  const leaveSession = (sessionId: string) => {
    sendMessage('user_left', { sessionId })
  }

  // Lifecycle management
  onMounted(() => {
    connect()
  })

  onUnmounted(() => {
    disconnect()
  })

  // Watch for active session changes
  watch(() => chatStore.activeSessionId, (newSessionId, oldSessionId) => {
    if (oldSessionId) {
      leaveSession(oldSessionId)
    }
    if (newSessionId) {
      joinSession(newSessionId)
    }
  })

  return {
    // State
    isConnected: readonly(isConnected),
    reconnectAttempts: readonly(reconnectAttempts),
    
    // Actions
    connect,
    disconnect,
    sendMessage,
    sendChatMessage,
    requestAnalysis,
    joinSession,
    leaveSession,
  }
}
