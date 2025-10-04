export default defineNuxtRouteMiddleware(async (to, from) => {
  // Skip middleware on server side
  if (process.server) return

  const { useAuthStore } = await import('~/stores/auth')
  const authStore = useAuthStore()

  // If user is already authenticated, redirect to dashboard
  if (authStore.user) {
    return navigateTo('/dashboard')
  }
})
