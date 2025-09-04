/**
 * Authentication Middleware for Nuxt 4
 * Protects routes that require user authentication
 */

export default defineNuxtRouteMiddleware(async (to, from) => {
  // Skip middleware on server-side during initial render
  if (process.server) {
    return
  }

  // Auth middleware is now working properly

  // In development, be more permissive with authentication
  const isDevelopment = process.dev || process.env.NODE_ENV === 'development' || import.meta.dev

  // In development mode, skip all authentication checks
  if (isDevelopment) {
    console.log('Development mode: Skipping all authentication checks for route:', to.path)
    return
  }

  try {
    const authStore = useAuthStore()

    // Initialize auth if not already done (important for page refreshes)
    if (!authStore.isAuthenticated && process.client) {
      await authStore.initializeAuth()
    }

    // Debug auth state
    console.log('Auth Debug:', {
      isAuthenticated: authStore.isAuthenticated,
      user: authStore.user,
      isLoggedIn: authStore.isLoggedIn,
      route: to.path
    })

    // Check if user is authenticated
    if (!authStore.isLoggedIn) {
      console.log('User not logged in, redirecting to login')
      return navigateTo({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    }

    // Validate session with backend in production
    try {
      const isValid = await authStore.validateSession()
      if (!isValid) {
        console.log('Session validation failed, redirecting to login')
        return navigateTo({
          path: '/login',
          query: { redirect: to.fullPath }
        })
      }
    } catch (validationError) {
      console.warn('Session validation error:', validationError)
      return navigateTo({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    }
  } catch (error) {
    console.warn('Auth middleware error:', error)
    return navigateTo('/login')
  }
})
