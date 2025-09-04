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
  
  // Set up automatic session validation
  if (process.client) {
    // Validate session every 10 minutes
    setInterval(async () => {
      if (authStore.isLoggedIn) {
        try {
          const isValid = await authStore.validateSession()
          if (!isValid) {
            await authStore.logout()
            await navigateTo('/login')
          }
        } catch (error) {
          console.warn('Background session validation failed:', error)
        }
      }
    }, 10 * 60 * 1000) // 10 minutes

    // Validate session on page visibility change
    document.addEventListener('visibilitychange', async () => {
      if (!document.hidden && authStore.isLoggedIn) {
        try {
          const isValid = await authStore.validateSession()
          if (!isValid) {
            await authStore.logout()
            await navigateTo('/login')
          }
        } catch (error) {
          console.warn('Session validation on visibility change failed:', error)
        }
      }
    })
  }
})
