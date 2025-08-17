/**
 * Auth Plugin for Client-Side Initialization
 * Automatically initializes authentication state from localStorage on app load
 */

export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore()

  // Initialize auth state from storage
  try {
    await authStore.initializeAuth()
    console.log('Auth plugin: Authentication initialized')
  } catch (error) {
    console.warn('Auth plugin: Failed to initialize auth:', error)
  }
  
  // Set up automatic token refresh
  if (process.client) {
    // Check token expiry every 5 minutes
    setInterval(async () => {
      if (authStore.isLoggedIn) {
        try {
          await authStore.checkAndRefreshToken()
        } catch (error) {
          console.warn('Background token refresh failed:', error)
        }
      }
    }, 5 * 60 * 1000) // 5 minutes
    
    // Check token on page visibility change
    document.addEventListener('visibilitychange', async () => {
      if (!document.hidden && authStore.isLoggedIn) {
        try {
          await authStore.checkAndRefreshToken()
        } catch (error) {
          console.warn('Token refresh on visibility change failed:', error)
        }
      }
    })
  }
})
