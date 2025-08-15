export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  
  // Create WebSocket instance
  const ws = useWebSocket({
    debug: config.public.enableDebugMode,
    reconnectInterval: 5000,
    maxReconnectAttempts: 5,
    heartbeatInterval: 30000
  })

  // Auto-connect in production or when explicitly enabled
  if (config.public.environment === 'production' || config.public.enableWebSocket) {
    // Connect after a short delay to ensure the app is ready
    setTimeout(() => {
      ws.connect()
    }, 1000)
  }

  // Provide WebSocket globally
  return {
    provide: {
      websocket: ws
    }
  }
})
