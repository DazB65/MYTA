/**
 * Team WebSocket Composable for MYTA
 * Extends the existing WebSocket system for team communication
 */

import { ref, computed, onUnmounted } from 'vue'
import { useTeamChatStore } from '../stores/teamChat'
import { useToast } from './useToast'

interface TeamWebSocketMessage {
  type: 'team_message' | 'member_status' | 'typing_start' | 'typing_stop' | 'member_joined' | 'member_left'
  teamId: string
  userId: string
  channelId?: string
  data: any
  timestamp: string
}

export const useTeamWebSocket = () => {
  // State
  const socket = ref<WebSocket | null>(null)
  const isConnected = ref(false)
  const isConnecting = ref(false)
  const error = ref<string | null>(null)
  const reconnectAttempts = ref(0)
  const maxReconnectAttempts = 5

  // Composables
  const teamChatStore = useTeamChatStore()
  const { success, error: showError } = useToast()

  // Computed
  const connectionStatus = computed(() => {
    if (isConnecting.value) return 'connecting'
    if (isConnected.value) return 'connected'
    return 'disconnected'
  })

  // WebSocket connection
  const connect = async (userId: string, teamId: string) => {
    if (isConnecting.value || isConnected.value) return

    try {
      isConnecting.value = true
      error.value = null

      // In a real app, this would connect to the actual WebSocket endpoint
      // For now, we'll simulate the connection
      await simulateConnection(userId, teamId)
      
      isConnected.value = true
      reconnectAttempts.value = 0
      
      success('Team Chat Connected', 'Real-time messaging is now active')
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to connect to team chat'
      showError('Connection Failed', error.value)
      
      // Attempt reconnection
      if (reconnectAttempts.value < maxReconnectAttempts) {
        setTimeout(() => {
          reconnectAttempts.value++
          connect(userId, teamId)
        }, Math.pow(2, reconnectAttempts.value) * 1000) // Exponential backoff
      }
    } finally {
      isConnecting.value = false
    }
  }

  const simulateConnection = async (userId: string, teamId: string) => {
    return new Promise((resolve, reject) => {
      try {
        // Simulate WebSocket connection
        const wsUrl = `ws://localhost:8000/api/chat/ws/${userId}/team_${teamId}`
        
        // Create mock WebSocket for demo purposes
        socket.value = {
          send: (data: string) => {
            console.log('📤 Sending team message:', data)
            // Simulate message delivery
            setTimeout(() => {
              handleIncomingMessage({
                type: 'message_delivered',
                teamId,
                userId,
                data: JSON.parse(data),
                timestamp: new Date().toISOString()
              })
            }, 100)
          },
          close: () => {
            isConnected.value = false
            console.log('🔌 Team WebSocket disconnected')
          },
          readyState: 1 // OPEN
        } as any

        // Simulate connection success
        setTimeout(() => {
          console.log('🔌 Team WebSocket connected to:', wsUrl)
          
          // Simulate receiving some initial presence updates
          simulateInitialPresence(teamId)
          
          resolve(true)
        }, 500)
        
      } catch (err) {
        reject(err)
      }
    })
  }

  const simulateInitialPresence = (teamId: string) => {
    // Simulate other team members coming online
    setTimeout(() => {
      handleIncomingMessage({
        type: 'member_status',
        teamId,
        userId: 'user_2',
        data: { status: 'online' },
        timestamp: new Date().toISOString()
      })
    }, 1000)

    setTimeout(() => {
      handleIncomingMessage({
        type: 'member_status',
        teamId,
        userId: 'user_3',
        data: { status: 'away' },
        timestamp: new Date().toISOString()
      })
    }, 2000)
  }

  // Message handling
  const handleIncomingMessage = (message: TeamWebSocketMessage) => {
    console.log('📥 Received team message:', message)

    switch (message.type) {
      case 'team_message':
        handleTeamMessage(message)
        break
      case 'member_status':
        handleMemberStatusUpdate(message)
        break
      case 'typing_start':
        handleTypingStart(message)
        break
      case 'typing_stop':
        handleTypingStop(message)
        break
      case 'member_joined':
        handleMemberJoined(message)
        break
      case 'member_left':
        handleMemberLeft(message)
        break
      default:
        console.warn('Unknown team message type:', message.type)
    }
  }

  const handleTeamMessage = (message: TeamWebSocketMessage) => {
    const { data } = message
    
    // Add message to store
    teamChatStore.messages.push({
      id: data.id,
      teamId: message.teamId,
      senderId: message.userId,
      senderName: data.senderName,
      senderAvatar: data.senderAvatar,
      content: data.content,
      type: data.type || 'text',
      timestamp: new Date(message.timestamp),
      status: 'delivered'
    })

    // Update channel unread count if not active
    if (data.channelId && teamChatStore.activeChannelId !== data.channelId) {
      const channel = teamChatStore.channels.find(c => c.id === data.channelId)
      if (channel) {
        channel.unreadCount++
      }
    }
  }

  const handleMemberStatusUpdate = (message: TeamWebSocketMessage) => {
    teamChatStore.updateMemberStatus(message.userId, message.data.status)
  }

  const handleTypingStart = (message: TeamWebSocketMessage) => {
    if (message.data.channelId) {
      teamChatStore.addTypingUser(message.data.channelId, message.userId)
    }
  }

  const handleTypingStop = (message: TeamWebSocketMessage) => {
    if (message.data.channelId) {
      teamChatStore.removeTypingUser(message.data.channelId, message.userId)
    }
  }

  const handleMemberJoined = (message: TeamWebSocketMessage) => {
    success('Team Update', `${message.data.memberName} joined the team`)
  }

  const handleMemberLeft = (message: TeamWebSocketMessage) => {
    success('Team Update', `${message.data.memberName} left the team`)
  }

  // Send messages
  const sendTeamMessage = (teamId: string, channelId: string, content: string) => {
    if (!socket.value || !isConnected.value) {
      throw new Error('Not connected to team chat')
    }

    const message = {
      type: 'team_message',
      teamId,
      channelId,
      content,
      timestamp: new Date().toISOString()
    }

    socket.value.send(JSON.stringify(message))
  }

  const sendTypingIndicator = (teamId: string, channelId: string, isTyping: boolean) => {
    if (!socket.value || !isConnected.value) return

    const message = {
      type: isTyping ? 'typing_start' : 'typing_stop',
      teamId,
      channelId,
      timestamp: new Date().toISOString()
    }

    socket.value.send(JSON.stringify(message))
  }

  const sendStatusUpdate = (teamId: string, status: 'online' | 'away' | 'offline') => {
    if (!socket.value || !isConnected.value) return

    const message = {
      type: 'member_status',
      teamId,
      status,
      timestamp: new Date().toISOString()
    }

    socket.value.send(JSON.stringify(message))
  }

  // Disconnect
  const disconnect = () => {
    if (socket.value) {
      socket.value.close()
      socket.value = null
    }
    isConnected.value = false
    isConnecting.value = false
    reconnectAttempts.value = 0
  }

  // Cleanup on unmount
  onUnmounted(() => {
    disconnect()
  })

  return {
    // State
    isConnected,
    isConnecting,
    connectionStatus,
    error,

    // Methods
    connect,
    disconnect,
    sendTeamMessage,
    sendTypingIndicator,
    sendStatusUpdate
  }
}
