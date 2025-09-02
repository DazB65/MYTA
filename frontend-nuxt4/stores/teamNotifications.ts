import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface TeamNotification {
  id: number
  title: string
  message: string
  type: string
  category: string
  icon: string
  color: string
  timestamp: string
  read: boolean
  teamMembers?: Array<{
    id: string
    name: string
    avatar: string
  }>
  actions?: Array<{
    id: string
    label: string
  }>
}

export const useTeamNotificationStore = defineStore('teamNotifications', () => {
  // State
  const notifications = ref<TeamNotification[]>([])
  const nextId = ref(1)

  // Computed
  const unreadCount = computed(() => 
    notifications.value.filter(n => !n.read).length
  )

  const unreadNotifications = computed(() =>
    notifications.value.filter(n => !n.read)
  )

  const readNotifications = computed(() =>
    notifications.value.filter(n => n.read)
  )

  // Actions
  const addNotification = (notification: Omit<TeamNotification, 'id'>) => {
    const newNotification: TeamNotification = {
      ...notification,
      id: nextId.value++
    }
    
    // Add to the beginning of the array (newest first)
    notifications.value.unshift(newNotification)
    
    // Limit to 50 notifications to prevent memory issues
    if (notifications.value.length > 50) {
      notifications.value = notifications.value.slice(0, 50)
    }
  }

  const markAsRead = (notificationId: number) => {
    const notification = notifications.value.find(n => n.id === notificationId)
    if (notification) {
      notification.read = true
    }
  }

  const markAllAsRead = () => {
    notifications.value.forEach(notification => {
      notification.read = true
    })
  }

  const removeNotification = (notificationId: number) => {
    const index = notifications.value.findIndex(n => n.id === notificationId)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const clearAllNotifications = () => {
    notifications.value = []
  }

  const getNotificationsByCategory = (category: string) => {
    return notifications.value.filter(n => n.category === category)
  }

  return {
    // State
    notifications,
    
    // Computed
    unreadCount,
    unreadNotifications,
    readNotifications,
    
    // Actions
    addNotification,
    markAsRead,
    markAllAsRead,
    removeNotification,
    clearAllNotifications,
    getNotificationsByCategory
  }
})
