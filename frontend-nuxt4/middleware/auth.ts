export default defineNuxtRouteMiddleware(async (to, from) => {
  // Skip middleware on server side
  if (process.server) return

  const { useAuthStore } = await import('~/stores/auth')
  const authStore = useAuthStore()

  // Check if user is authenticated
  if (!authStore.user) {
    // Redirect to login page
    return navigateTo('/login')
  }
})
