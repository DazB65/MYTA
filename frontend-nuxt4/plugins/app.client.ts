import { useAgentsStore } from '~/stores/agents'
import { useAnalyticsStore } from '~/stores/analytics'
import { useAuthStore } from '~/stores/auth'
import { useChatStore } from '~/stores/chat'
import { useTasksStore } from '~/stores/tasks'

export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore()
  const analyticsStore = useAnalyticsStore()
  const agentsStore = useAgentsStore()
  const chatStore = useChatStore()
  const tasksStore = useTasksStore()

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

          // Initialize tasks store
          tasksStore.initializeTasks()
        } catch (error) {
          console.warn('Failed to initialize app data:', error)
        }
      }
    },
    { immediate: true }
  )
})
