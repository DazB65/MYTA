import { defineStore } from 'pinia'
import { ref, computed, readonly } from 'vue'

export type Theme = 'light' | 'dark' | 'auto'

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  timestamp: Date
}

export const useUIStore = defineStore('ui', () => {
  // State
  const theme = ref<Theme>('auto')
  const notifications = ref<Notification[]>([])
  const isMobile = ref(false)

  // Getters
  const isDarkMode = computed(() => {
    if (theme.value === 'auto') {
      if (typeof window !== 'undefined') {
        return window.matchMedia('(prefers-color-scheme: dark)').matches
      }
      return false
    }
    return theme.value === 'dark'
  })

  const activeNotifications = computed(() => notifications.value)

  // Actions
  const setTheme = (newTheme: Theme) => {
    theme.value = newTheme
  }

  const toggleTheme = () => {
    const newTheme = isDarkMode.value ? 'light' : 'dark'
    setTheme(newTheme)
  }

  const addNotification = (notification: Omit<Notification, 'id' | 'timestamp'>) => {
    const id = `notification_${Date.now()}`
    const newNotification: Notification = {
      ...notification,
      id,
      timestamp: new Date()
    }

    notifications.value.push(newNotification)
    return id
  }

  const showSuccess = (title: string, message: string) => {
    return addNotification({ type: 'success', title, message })
  }

  const showError = (title: string, message: string) => {
    return addNotification({ type: 'error', title, message })
  }

  const showInfo = (title: string, message: string) => {
    return addNotification({ type: 'info', title, message })
  }

  const setLoading = (key: string, isLoading: boolean) => {
    // Mock loading state management
    console.log(`Loading ${key}: ${isLoading}`)
  }

  const initializeUI = () => {
    console.log('UI store initialized')
  }

  return {
    // State
    theme: readonly(theme),
    notifications: readonly(notifications),
    isMobile: readonly(isMobile),

    // Getters
    isDarkMode,
    activeNotifications,

    // Actions
    setTheme,
    toggleTheme,
    addNotification,
    showSuccess,
    showError,
    showInfo,
    setLoading,
    initializeUI,
  }
})