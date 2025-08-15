import { useAuthStore } from '~/stores/auth'
import { useAnalyticsStore } from '~/stores/analytics'
import { useAgentsStore } from '~/stores/agents'
import { useChatStore } from '~/stores/chat'

export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore()
  const analyticsStore = useAnalyticsStore()
  const agentsStore = useAgentsStore()
  const chatStore = useChatStore()

  // Auto-initialize analytics when user is authenticated
  watch(
    () => authStore.isLoggedIn,
    async isLoggedIn => {
      if (isLoggedIn && authStore.userId) {
        try {
          // Initialize analytics if YouTube is connected
          if (authStore.hasYouTubeAccess) {
            await analyticsStore.initialize(authStore.userId)
          }

          // Load chat sessions
          await chatStore.loadAllSessions()
        } catch (error) {
          console.warn('Failed to initialize app data:', error)
        }
      }
    },
    { immediate: true }
  )
})
