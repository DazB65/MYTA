<template>
  <div class="fixed top-4 right-4 z-50 space-y-2">
    <TransitionGroup
      name="notification"
      tag="div"
      class="space-y-2"
    >
      <div
        v-for="notification in notifications"
        :key="notification.id"
        :class="[
          'max-w-sm rounded-lg p-4 shadow-lg backdrop-blur-sm',
          'border border-opacity-20',
          getNotificationClasses(notification.type)
        ]"
      >
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <component
              :is="getNotificationIcon(notification.type)"
              class="h-5 w-5"
            />
          </div>
          <div class="ml-3 flex-1">
            <p class="text-sm font-medium">
              {{ notification.title }}
            </p>
            <p v-if="notification.message" class="mt-1 text-sm opacity-90">
              {{ notification.message }}
            </p>
          </div>
          <div class="ml-4 flex-shrink-0">
            <button
              @click="removeNotification(notification.id)"
              class="inline-flex rounded-md p-1.5 hover:bg-black hover:bg-opacity-10 focus:outline-none focus:ring-2 focus:ring-offset-2"
            >
              <span class="sr-only">Dismiss</span>
              <IconClose class="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// Icons
const IconSuccess = 'div' // Replace with actual icon
const IconError = 'div'
const IconWarning = 'div'
const IconInfo = 'div'
const IconClose = 'div'

// Notification interface
interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
}

// Notifications state
const notifications = ref<Notification[]>([])

// Notification management
const addNotification = (notification: Omit<Notification, 'id'>) => {
  const id = Date.now().toString()
  const newNotification: Notification = {
    id,
    duration: 5000,
    ...notification
  }
  
  notifications.value.push(newNotification)
  
  // Auto-remove after duration
  if (newNotification.duration && newNotification.duration > 0) {
    setTimeout(() => {
      removeNotification(id)
    }, newNotification.duration)
  }
  
  return id
}

const removeNotification = (id: string) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
}

const clearAllNotifications = () => {
  notifications.value = []
}

// Helper functions
const getNotificationClasses = (type: string) => {
  const classes = {
    success: 'bg-green-500 bg-opacity-90 text-white border-green-400',
    error: 'bg-red-500 bg-opacity-90 text-white border-red-400',
    warning: 'bg-yellow-500 bg-opacity-90 text-white border-yellow-400',
    info: 'bg-blue-500 bg-opacity-90 text-white border-blue-400'
  }
  return classes[type] || classes.info
}

const getNotificationIcon = (type: string) => {
  const icons = {
    success: IconSuccess,
    error: IconError,
    warning: IconWarning,
    info: IconInfo
  }
  return icons[type] || IconInfo
}

// Convenience methods
const showSuccess = (title: string, message?: string) => {
  return addNotification({ type: 'success', title, message })
}

const showError = (title: string, message?: string) => {
  return addNotification({ type: 'error', title, message })
}

const showWarning = (title: string, message?: string) => {
  return addNotification({ type: 'warning', title, message })
}

const showInfo = (title: string, message?: string) => {
  return addNotification({ type: 'info', title, message })
}

// Provide notification functions globally
provide('notifications', {
  add: addNotification,
  remove: removeNotification,
  clear: clearAllNotifications,
  success: showSuccess,
  error: showError,
  warning: showWarning,
  info: showInfo
})
</script>

<style scoped>
/* Notification animations */
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform 0.3s ease;
}
</style>
