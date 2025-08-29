/**
 * Tasks Plugin for Client-Side Initialization
 * Automatically initializes tasks store from localStorage on app load
 */

export default defineNuxtPlugin(async () => {
  const tasksStore = useTasksStore()

  // Initialize tasks store from storage
  try {
    console.log('🔥 Tasks plugin: Initializing tasks store')
    tasksStore.initializeTasks()
    console.log('✅ Tasks plugin: Tasks store initialized successfully')
  } catch (error) {
    console.warn('⚠️ Tasks plugin: Failed to initialize tasks store:', error)
  }
})
