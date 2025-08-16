/**
 * Authentication Middleware for Nuxt 4
 * Protects routes that require user authentication
 */

export default defineNuxtRouteMiddleware(async (to, from) => {
  // Skip middleware on server-side during initial render
  if (process.server) {
    return
  }

  try {
    const authStore = useAuthStore()

    // Check if user is authenticated and token is valid
    if (!authStore.isLoggedIn) {
      // Redirect to login page with return URL
      return navigateTo({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    }

    // Check if token is expired and try to refresh
    if (authStore.isTokenExpired) {
      try {
        await authStore.checkAndRefreshToken()
        // If refresh failed, user will be logged out automatically
        if (!authStore.isLoggedIn) {
          return navigateTo({
            path: '/login',
            query: { redirect: to.fullPath }
          })
        }
      } catch (error) {
        console.warn('Token refresh failed in middleware:', error)
        return navigateTo('/login')
      }
    }
  } catch (error) {
    // If store is not available, redirect to login
    console.warn('Auth store not available, redirecting to login')
    return navigateTo('/login')
  }
})
