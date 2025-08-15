export default defineNuxtPlugin(() => {
  const { apiCall } = useApi()
  const config = useRuntimeConfig()

  // Initialize API configuration
  const initializeApi = () => {
    // Log API configuration in development
    if (config.public.enableDebugMode) {
      console.log('[API] Initialized with base URL:', config.public.apiBaseUrl)
    }
  }

  // Initialize on plugin load
  initializeApi()

  // Provide API globally
  return {
    provide: {
      api: apiCall
    }
  }
})
