/**
 * Guest Middleware for Nuxt 4
 * Redirects authenticated users away from auth pages (login, signup)
 */

export default defineNuxtRouteMiddleware(async (to, from) => {
  // Skip middleware on server-side during initial render
  if (process.server) {
    return
  }

  try {
    const authStore = useAuthStore()

    // If user is already logged in, redirect to dashboard
    if (authStore.isLoggedIn) {
      return navigateTo('/dashboard')
    }
  } catch (error) {
    // If store is not available, allow access (guest behavior)
    console.warn('Auth store not available, allowing guest access')
  }
})
