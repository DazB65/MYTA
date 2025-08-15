import { ref, onUnmounted, readonly } from 'vue'

export interface WebSocketMessage {
  type: string
  data: any
  timestamp: number
}

export interface WebSocketOptions {
  reconnectInterval?: number
  maxReconnectAttempts?: number
  heartbeatInterval?: number
  debug?: boolean
}

export const useWebSocket = (options: WebSocketOptions = {}) => {
  const config = useRuntimeConfig()
  const {
    reconnectInterval = 5000,
    maxReconnectAttempts = 5,
    heartbeatInterval = 30000,
    debug = false
  } = options

  // State
  const isConnected = ref(false)
  const isConnecting = ref(false)
  const error = ref<string | null>(null)
  const lastMessage = ref<WebSocketMessage | null>(null)
  const connectionAttempts = ref(0)

  // WebSocket instance
  let ws: WebSocket | null = null
  let heartbeatTimer: NodeJS.Timeout | null = null
  let reconnectTimer: NodeJS.Timeout | null = null

  // Event listeners
  const messageListeners = new Map<string, Set<(data: any) => void>>()
  const connectionListeners = new Set<(connected: boolean) => void>()

  // Get WebSocket URL
  const getWebSocketUrl = () => {
    const wsUrl = config.public.wsUrl || 'ws://localhost:8000'
    return wsUrl.replace(/^http/, 'ws')
  }

  // Logging helper
  const log = (message: string, ...args: any[]) => {
    if (debug) {
      console.log(`[WebSocket] ${message}`, ...args)
    }
  }

  // Send heartbeat
  const sendHeartbeat = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      send('heartbeat', { timestamp: Date.now() })
    }
  }

  // Start heartbeat
  const startHeartbeat = () => {
    if (heartbeatTimer) {
      clearInterval(heartbeatTimer)
    }
    heartbeatTimer = setInterval(sendHeartbeat, heartbeatInterval)
  }

  // Stop heartbeat
  const stopHeartbeat = () => {
    if (heartbeatTimer) {
      clearInterval(heartbeatTimer)
      heartbeatTimer = null
    }
  }

  // Connect to WebSocket
  const connect = () => {
    if (isConnecting.value || isConnected.value) {
      return
    }

    isConnecting.value = true
    error.value = null

    try {
      const url = getWebSocketUrl()
      log('Connecting to:', url)
      
      ws = new WebSocket(url)

      ws.onopen = () => {
        log('Connected')
        isConnected.value = true
        isConnecting.value = false
        connectionAttempts.value = 0
        error.value = null
        
        // Start heartbeat
        startHeartbeat()
        
        // Notify connection listeners
        connectionListeners.forEach(listener => listener(true))
      }

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          log('Received message:', message)
          
          lastMessage.value = message
          
          // Call type-specific listeners
          const listeners = messageListeners.get(message.type)
          if (listeners) {
            listeners.forEach(listener => listener(message.data))
          }
          
          // Call general message listeners
          const generalListeners = messageListeners.get('*')
          if (generalListeners) {
            generalListeners.forEach(listener => listener(message))
          }
        } catch (err) {
          log('Error parsing message:', err)
        }
      }

      ws.onclose = (event) => {
        log('Disconnected:', event.code, event.reason)
        isConnected.value = false
        isConnecting.value = false
        
        // Stop heartbeat
        stopHeartbeat()
        
        // Notify connection listeners
        connectionListeners.forEach(listener => listener(false))
        
        // Attempt reconnection if not a clean close
        if (event.code !== 1000 && connectionAttempts.value < maxReconnectAttempts) {
          scheduleReconnect()
        }
      }

      ws.onerror = (event) => {
        log('Error:', event)
        error.value = 'WebSocket connection error'
        isConnecting.value = false
      }
    } catch (err) {
      log('Connection error:', err)
      error.value = 'Failed to create WebSocket connection'
      isConnecting.value = false
    }
  }

  // Schedule reconnection
  const scheduleReconnect = () => {
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
    }
    
    connectionAttempts.value++
    const delay = Math.min(reconnectInterval * Math.pow(2, connectionAttempts.value - 1), 30000)
    
    log(`Reconnecting in ${delay}ms (attempt ${connectionAttempts.value}/${maxReconnectAttempts})`)
    
    reconnectTimer = setTimeout(() => {
      connect()
    }, delay)
  }

  // Disconnect
  const disconnect = () => {
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }
    
    stopHeartbeat()
    
    if (ws) {
      ws.close(1000, 'Manual disconnect')
      ws = null
    }
    
    isConnected.value = false
    isConnecting.value = false
    connectionAttempts.value = 0
  }

  // Send message
  const send = (type: string, data: any = {}) => {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      log('Cannot send message: WebSocket not connected')
      return false
    }

    const message: WebSocketMessage = {
      type,
      data,
      timestamp: Date.now()
    }

    try {
      ws.send(JSON.stringify(message))
      log('Sent message:', message)
      return true
    } catch (err) {
      log('Error sending message:', err)
      return false
    }
  }

  // Add message listener
  const on = (type: string, listener: (data: any) => void) => {
    if (!messageListeners.has(type)) {
      messageListeners.set(type, new Set())
    }
    messageListeners.get(type)!.add(listener)
    
    // Return unsubscribe function
    return () => {
      const listeners = messageListeners.get(type)
      if (listeners) {
        listeners.delete(listener)
        if (listeners.size === 0) {
          messageListeners.delete(type)
        }
      }
    }
  }

  // Add connection listener
  const onConnection = (listener: (connected: boolean) => void) => {
    connectionListeners.add(listener)
    
    // Return unsubscribe function
    return () => {
      connectionListeners.delete(listener)
    }
  }

  // Remove message listener
  const off = (type: string, listener?: (data: any) => void) => {
    if (listener) {
      const listeners = messageListeners.get(type)
      if (listeners) {
        listeners.delete(listener)
        if (listeners.size === 0) {
          messageListeners.delete(type)
        }
      }
    } else {
      messageListeners.delete(type)
    }
  }

  // Cleanup on unmount
  onUnmounted(() => {
    disconnect()
  })

  return {
    // State
    isConnected: readonly(isConnected),
    isConnecting: readonly(isConnecting),
    error: readonly(error),
    lastMessage: readonly(lastMessage),
    connectionAttempts: readonly(connectionAttempts),
    
    // Methods
    connect,
    disconnect,
    send,
    on,
    off,
    onConnection
  }
}
