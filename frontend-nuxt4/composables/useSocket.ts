import type { Socket } from 'socket.io-client';
import { io } from 'socket.io-client';
import { onMounted, onUnmounted, readonly, ref, watch } from 'vue';
import { useAgentsStore } from '../stores/agents';
import { useAuthStore } from '../stores/auth';
import { useChatStore } from '../stores/chat';
import { useUIStore } from '../stores/ui';
import type { ChatMessage } from '../types/agents';

export const useSocket = () => {
  const config = useRuntimeConfig()
  const authStore = useAuthStore()
  const chatStore = useChatStore()
  const agentsStore = useAgentsStore()
  const uiStore = useUIStore()

  const socket = ref<Socket | null>(null)
  const isConnected = ref(false)
  const isConnecting = ref(false)
  const error = ref<string | null>(null)
  const reconnectAttempts = ref(0)
  const maxReconnectAttempts = 5

  const connect = () => {
    if (socket.value?.connected || isConnecting.value) return

    if (!authStore.isLoggedIn) {
      error.value = 'Authentication required for WebSocket connection'
      return
    }

    isConnecting.value = true
    error.value = null

    try {
      socket.value = io(config.public.wsUrl, {
        auth: {
          token: authStore.token,
        },
        transports: ['websocket', 'polling'],
        timeout: 20000,
        reconnection: true,
        reconnectionAttempts: maxReconnectAttempts,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
      })

      setupEventListeners()
    } catch (err: any) {
      error.value = `Failed to connect: ${err.message}`
      isConnecting.value = false
    }
  }

  const disconnect = () => {
    if (socket.value) {
      socket.value.disconnect()
      socket.value = null
    }
    isConnected.value = false
    isConnecting.value = false
    reconnectAttempts.value = 0
  }

  const setupEventListeners = () => {
    if (!socket.value) return

    // Connection events
    socket.value.on('connect', () => {
      isConnected.value = true
      isConnecting.value = false
      reconnectAttempts.value = 0
      error.value = null

      uiStore.showSuccess('Connected', 'Real-time connection established')

      // Join user room for personalized messages
      if (authStore.userId) {
        socket.value?.emit('join_user_room', { userId: authStore.userId })
      }
    })

    socket.value.on('disconnect', reason => {
      isConnected.value = false

      if (reason === 'io server disconnect') {
        // Server disconnected, manual reconnection needed
        error.value = 'Server disconnected'
      } else {
        // Client disconnected, automatic reconnection will happen
        console.log('WebSocket disconnected:', reason)
      }
    })

    socket.value.on('connect_error', err => {
      isConnecting.value = false
      reconnectAttempts.value++
      error.value = `Connection failed: ${err.message}`

      if (reconnectAttempts.value >= maxReconnectAttempts) {
        uiStore.showError('Connection Failed', 'Unable to establish real-time connection')
      }
    })

    socket.value.on('reconnect', attemptNumber => {
      uiStore.showInfo('Reconnected', 'Real-time connection restored')
    })

    socket.value.on('reconnect_failed', () => {
      error.value = 'Failed to reconnect after multiple attempts'
      uiStore.showError('Connection Lost', 'Unable to restore real-time connection')
    })

    // Chat events
    socket.value.on('agent_message', (data: { message: ChatMessage }) => {
      chatStore.receiveMessage(data.message)
    })

    socket.value.on('agent_typing', (data: { agentId: string; typing: boolean }) => {
      chatStore.setAgentTyping(data.agentId, data.typing)
    })

    // Agent events
    socket.value.on('agent_status_change', (data: { agentId: string; status: string }) => {
      agentsStore.updateAgentStatus(data.agentId, data.status as any)
    })

    socket.value.on('insight_generated', (data: { insight: any }) => {
      agentsStore.addInsight(data.insight)
      uiStore.showInfo('New Insight', `${data.insight.title} from ${data.insight.agentId}`)
    })

    socket.value.on('analysis_complete', (data: { agentId: string; result: any }) => {
      uiStore.showSuccess('Analysis Complete', `${data.agentId} has finished analysis`)
    })

    // Error events
    socket.value.on('error', (data: { message: string }) => {
      error.value = data.message
      uiStore.showError('WebSocket Error', data.message)
    })

    // Heartbeat
    socket.value.on('heartbeat', () => {
      // Keep connection alive
      socket.value?.emit('heartbeat_response')
    })
  }

  const emit = (event: string, data?: any) => {
    if (!socket.value?.connected) {
      error.value = 'WebSocket not connected'
      return false
    }

    try {
      socket.value.emit(event, data)
      return true
    } catch (err: any) {
      error.value = `Failed to emit event: ${err.message}`
      return false
    }
  }

  const sendMessage = (sessionId: string, message: ChatMessage) => {
    return emit('chat_message', { sessionId, message })
  }

  const joinChatSession = (sessionId: string) => {
    return emit('join_chat_session', { sessionId })
  }

  const leaveChatSession = (sessionId: string) => {
    return emit('leave_chat_session', { sessionId })
  }

  const requestAnalysis = (agentId: string, analysisType: string, data: any) => {
    return emit('request_analysis', { agentId, analysisType, data })
  }

  const setTyping = (sessionId: string, typing: boolean) => {
    return emit('typing', { sessionId, typing })
  }

  // Auto-connect when auth state changes
  watch(
    () => authStore.isLoggedIn,
    isLoggedIn => {
      if (isLoggedIn) {
        connect()
      } else {
        disconnect()
      }
    }
  )

  // Lifecycle
  onMounted(() => {
    if (authStore.isLoggedIn) {
      connect()
    }
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    socket: readonly(socket),
    isConnected: readonly(isConnected),
    isConnecting: readonly(isConnecting),
    error: readonly(error),
    reconnectAttempts: readonly(reconnectAttempts),

    connect,
    disconnect,
    emit,
    sendMessage,
    joinChatSession,
    leaveChatSession,
    requestAnalysis,
    setTyping,
  }
}

// Plugin to make $socket available globally
export const socketPlugin = () => {
  const socketComposable = useSocket()

  return {
    provide: {
      socket: socketComposable.socket.value,
    },
  }
}
