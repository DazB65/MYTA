<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-500">
          <span class="text-white text-xl">🔔</span>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-white">Smart Notifications</h3>
          <p class="text-sm text-gray-400">AI-powered alerts and opportunities</p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <span v-if="urgentNotifications.length > 0" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-900/30 text-red-300 border border-red-600/30">
          {{ urgentNotifications.length }} Urgent
        </span>
        <button
          @click="refreshNotifications"
          :disabled="isLoading"
          class="p-2 text-gray-400 hover:text-white transition-colors disabled:opacity-50"
          title="Refresh notifications"
        >
          <svg class="h-4 w-4" :class="{ 'animate-spin': isLoading }" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Notifications List -->
    <div v-if="notifications.length > 0" class="space-y-3 max-h-96 overflow-y-auto">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="rounded-lg p-4 border transition-colors hover:bg-gray-700/50"
        :class="getPriorityColor(notification.priority)"
      >
        <!-- Notification Header -->
        <div class="flex items-start justify-between mb-2">
          <div class="flex items-center space-x-2">
            <span class="text-lg">{{ getPriorityIcon(notification.priority) }}</span>
            <h4 class="font-medium text-white">{{ notification.title }}</h4>
          </div>
          <div class="flex items-center space-x-2">
            <span class="text-xs text-gray-400">{{ formatNotificationTime(notification.created_at) }}</span>
            <button
              @click="dismissNotification(notification.id)"
              class="p-1 text-gray-400 hover:text-white transition-colors"
              title="Dismiss"
            >
              <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Notification Message -->
        <p class="text-sm text-gray-300 mb-3">{{ notification.message }}</p>

        <!-- Suggested Actions -->
        <div v-if="notification.suggested_actions && notification.suggested_actions.length > 0" class="flex flex-wrap gap-2">
          <button
            v-for="action in notification.suggested_actions"
            :key="action"
            @click="executeAction(notification, action)"
            class="px-3 py-1 text-xs rounded-full bg-gray-600 text-gray-300 hover:bg-gray-500 transition-colors"
          >
            {{ action }}
          </button>
        </div>

        <!-- Related Content Link -->
        <div v-if="notification.related_content" class="mt-2">
          <button
            @click="navigateToContent(notification.related_content)"
            class="text-xs text-blue-400 hover:text-blue-300 transition-colors"
          >
            View Related Content →
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!isLoading" class="text-center py-8">
      <div class="text-gray-400 mb-4">
        <span class="text-4xl">🔔</span>
      </div>
      <p class="text-gray-400 mb-4">No notifications at the moment</p>
      <p class="text-sm text-gray-500">Smart notifications will appear here when there are opportunities or issues to address</p>
    </div>

    <!-- Loading State -->
    <div v-else class="text-center py-8">
      <div class="animate-spin text-4xl mb-4">⏳</div>
      <p class="text-gray-400">Loading notifications...</p>
    </div>

    <!-- Notification Settings Link -->
    <div class="pt-4 border-t border-gray-700">
      <button
        @click="$emit('openSettings')"
        class="w-full text-center text-sm text-gray-400 hover:text-white transition-colors"
      >
        Configure Notification Settings →
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useAutomation } from '../../composables/useAutomation'
import { useRouter } from 'vue-router'

const router = useRouter()

const {
  notifications,
  urgentNotifications,
  isLoading,
  getNotifications,
  formatNotificationTime,
  getPriorityColor
} = useAutomation()

const emit = defineEmits(['openSettings'])

// Auto-refresh interval
let refreshInterval = null

// Methods
const refreshNotifications = async () => {
  await getNotifications()
}

const dismissNotification = (notificationId) => {
  // Remove notification from local state
  const index = notifications.value.findIndex(n => n.id === notificationId)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
  
  // In production, would also call API to mark as dismissed
}

const executeAction = (notification, action) => {
  // Handle different action types
  switch (action.toLowerCase()) {
    case 'optimize thumbnail':
      router.push('/content-studio?action=optimize-thumbnail')
      break
    case 'update title':
      router.push('/content-studio?action=update-title')
      break
    case 'check analytics':
      router.push('/analytics')
      break
    case 'review comments':
      router.push('/videos?tab=comments')
      break
    case 'create content':
      router.push('/content-studio?action=create')
      break
    default:
      console.log('Executing action:', action, 'for notification:', notification.id)
  }
}

const navigateToContent = (contentId) => {
  // Navigate to related content
  router.push(`/videos/${contentId}`)
}

const getPriorityIcon = (priority) => {
  switch (priority) {
    case 'urgent': return '🚨'
    case 'high': return '⚠️'
    case 'medium': return 'ℹ️'
    case 'low': return '💡'
    default: return '🔔'
  }
}

// Lifecycle
onMounted(async () => {
  await refreshNotifications()
  
  // Set up auto-refresh every 30 seconds
  refreshInterval = setInterval(refreshNotifications, 30000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>
