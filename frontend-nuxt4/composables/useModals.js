import { reactive, ref } from 'vue'

// Global modal state - shared across all components
const modals = reactive({
  youtubeConnect: false,
  task: false,
  goal: false,
  content: false
})

// Modal data objects
const taskData = ref(null)
const goalData = ref(null)
const contentData = ref(null)

// Modal management functions
const openModal = (modalName) => {
  console.log('🔥 Opening modal:', modalName)
  modals[modalName] = true
}

const closeModal = (modalName) => {
  console.log('🔥 Closing modal:', modalName)
  modals[modalName] = false
}

const closeAllModals = () => {
  console.log('🔥 Closing all modals')
  Object.keys(modals).forEach(key => {
    modals[key] = false
  })
}

// Modal opening functions with data
const openTaskModal = (task = null) => {
  console.log('🔥 Opening task modal with data:', task)
  taskData.value = task
  modals.task = true
}

const openGoalModal = (goal = null) => {
  console.log('🔥 Opening goal modal with data:', goal)
  goalData.value = goal
  modals.goal = true
}

const openContentModal = (content = null) => {
  console.log('🔥 Opening content modal with data:', content)
  contentData.value = content
  modals.content = true
}

// Modal save handlers
const handleTaskSave = (data) => {
  console.log('🔥 Task saved:', data)
  closeModal('task')
}

const handleGoalSave = (data) => {
  console.log('🔥 Goal saved:', data)
  closeModal('goal')
}

const handleContentSave = (data) => {
  console.log('🔥 Content saved:', data)
  closeModal('content')
}

// Composable function
export const useModals = () => {
  return {
    // State
    modals,
    taskData,
    goalData,
    contentData,
    
    // Functions
    open: openModal,
    close: closeModal,
    closeAll: closeAllModals,
    openTask: openTaskModal,
    openGoal: openGoalModal,
    openContent: openContentModal,
    
    // Save handlers
    handleTaskSave,
    handleGoalSave,
    handleContentSave
  }
}
