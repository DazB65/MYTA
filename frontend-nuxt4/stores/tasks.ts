import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import type {
    CreateTaskRequest,
    Task,
    TaskCategory,
    TaskFilter,
    TaskPriority,
    TaskStats,
    UpdateTaskRequest,
} from '../types/tasks'

export const useTasksStore = defineStore('tasks', () => {
  // State
  const tasks = ref<Task[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const activeFilter = ref<TaskFilter>('all')
  const searchQuery = ref('')
  const sortBy = ref<'dueDate' | 'priority' | 'createdAt' | 'title'>('dueDate')
  const sortOrder = ref<'asc' | 'desc'>('asc')
  const selectedCategory = ref<TaskCategory | 'all'>('all')
  const selectedPriority = ref<TaskPriority | 'all'>('all')
  const showCompleted = ref(true)
  const isInitialized = ref(false)

  // Initialize with sample tasks
  const initializeTasks = () => {
    const sampleTasks: Task[] = [
      {
        id: '1',
        title: 'Create AI content creation assistant',
        description: "Hello! I'm your AI content creation assistant. How can I help you today?",
        status: 'pending',
        priority: 'medium',
        category: 'content',
        dueDate: new Date('2025-07-18'),
        createdAt: new Date('2025-07-15'),
        updatedAt: new Date('2025-07-15'),
        completed: false,
        tags: ['General', 'Content'],
        estimatedTime: 120,
      },
      {
        id: '2',
        title: 'Schedule social media posts',
        description: 'Plan and schedule posts for next week',
        status: 'pending',
        priority: 'high',
        category: 'marketing',
        dueDate: new Date('2025-07-18'),
        createdAt: new Date('2025-07-15'),
        updatedAt: new Date('2025-07-15'),
        completed: false,
        tags: ['Content'],
        estimatedTime: 60,
      },
      {
        id: '3',
        title: 'Update channel banners',
        description: 'Design new banner with current subscriber count',
        status: 'pending',
        priority: 'low',
        category: 'marketing',
        dueDate: new Date('2025-07-18'),
        createdAt: new Date('2025-07-15'),
        updatedAt: new Date('2025-07-15'),
        completed: false,
        tags: ['Marketing', 'Content'],
        estimatedTime: 90,
      },
      {
        id: '4',
        title: 'Reply to community comments',
        description:
          'Engage with your audience by responding to comments on your latest video posts',
        status: 'in_progress',
        priority: 'medium',
        category: 'community',
        dueDate: new Date('2025-07-19'),
        createdAt: new Date('2025-07-14'),
        updatedAt: new Date('2025-07-16'),
        completed: false,
        tags: ['Community'],
        estimatedTime: 45,
      },
    ]

    tasks.value = sampleTasks
  }

  // Getters
  const filteredTasks = computed(() => {
    let filtered = [...tasks.value]

    // Apply completion filter
    if (!showCompleted.value) {
      filtered = filtered.filter(task => !task.completed)
    }

    // Apply status filter
    switch (activeFilter.value) {
      case 'completed':
        filtered = filtered.filter(task => task.completed)
        break
      case 'pending':
        filtered = filtered.filter(task => task.status === 'pending')
        break
      case 'in_progress':
        filtered = filtered.filter(task => task.status === 'in_progress')
        break
      case 'high_priority':
        filtered = filtered.filter(task => task.priority === 'high' || task.priority === 'urgent')
        break
      case 'due_today':
        const today = new Date()
        today.setHours(0, 0, 0, 0)
        const tomorrow = new Date(today)
        tomorrow.setDate(tomorrow.getDate() + 1)
        filtered = filtered.filter(task => {
          const dueDate = new Date(task.dueDate)
          dueDate.setHours(0, 0, 0, 0)
          return dueDate >= today && dueDate < tomorrow
        })
        break
      case 'overdue':
        const now = new Date()
        filtered = filtered.filter(task => new Date(task.dueDate) < now && !task.completed)
        break
    }

    // Apply category filter
    if (selectedCategory.value !== 'all') {
      filtered = filtered.filter(task => task.category === selectedCategory.value)
    }

    // Apply priority filter
    if (selectedPriority.value !== 'all') {
      filtered = filtered.filter(task => task.priority === selectedPriority.value)
    }

    // Apply search filter
    if (searchQuery.value.trim()) {
      const query = searchQuery.value.toLowerCase()
      filtered = filtered.filter(
        task =>
          task.title.toLowerCase().includes(query) ||
          task.description.toLowerCase().includes(query) ||
          task.tags.some(tag => tag.toLowerCase().includes(query))
      )
    }

    // Apply sorting
    filtered.sort((a, b) => {
      let aValue: any, bValue: any

      switch (sortBy.value) {
        case 'priority':
          const priorityOrder = { urgent: 4, high: 3, medium: 2, low: 1 }
          aValue = priorityOrder[a.priority]
          bValue = priorityOrder[b.priority]
          break
        case 'dueDate':
          aValue = new Date(a.dueDate).getTime()
          bValue = new Date(b.dueDate).getTime()
          break
        case 'createdAt':
          aValue = new Date(a.createdAt).getTime()
          bValue = new Date(b.createdAt).getTime()
          break
        case 'title':
          aValue = a.title.toLowerCase()
          bValue = b.title.toLowerCase()
          break
        default:
          return 0
      }

      if (sortOrder.value === 'desc') {
        return bValue > aValue ? 1 : bValue < aValue ? -1 : 0
      } else {
        return aValue > bValue ? 1 : aValue < bValue ? -1 : 0
      }
    })

    return filtered
  })

  const taskStats = computed((): TaskStats => {
    const total = tasks.value.length
    const completed = tasks.value.filter(task => task.completed).length
    const pending = tasks.value.filter(task => task.status === 'pending').length
    const inProgress = tasks.value.filter(task => task.status === 'in_progress').length
    const now = new Date()
    const overdue = tasks.value.filter(
      task => new Date(task.dueDate) < now && !task.completed
    ).length

    return {
      total,
      completed,
      pending,
      inProgress,
      overdue,
      completionRate: total > 0 ? Math.round((completed / total) * 100) : 0,
    }
  })

  const completedTasksCount = computed(() => tasks.value.filter(task => task.completed).length)

  const tasksByCategory = computed(() => {
    const categories: Record<TaskCategory, Task[]> = {
      content: [],
      marketing: [],
      analytics: [],
      seo: [],
      monetization: [],
      community: [],
      planning: [],
      research: [],
      general: [],
    }

    tasks.value.forEach(task => {
      categories[task.category].push(task)
    })

    return categories
  })

  const tasksByPriority = computed(() => {
    const priorities: Record<TaskPriority, Task[]> = {
      urgent: [],
      high: [],
      medium: [],
      low: [],
    }

    tasks.value.forEach(task => {
      priorities[task.priority].push(task)
    })

    return priorities
  })

  const upcomingTasks = computed(() => {
    const now = new Date()
    const nextWeek = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000)

    return tasks.value
      .filter(task => !task.completed && new Date(task.dueDate) <= nextWeek)
      .sort((a, b) => new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime())
      .slice(0, 5)
  })

  const recentTasks = computed(() => {
    return tasks.value
      .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
      .slice(0, 10)
  })

  const availableCategories = computed(() => {
    const categories = new Set(tasks.value.map(task => task.category))
    return Array.from(categories).sort()
  })

  const availableTags = computed(() => {
    const tags = new Set(tasks.value.flatMap(task => task.tags))
    return Array.from(tags).sort()
  })

  // Actions
  const setActiveFilter = (filter: TaskFilter) => {
    activeFilter.value = filter
  }

  const setSearchQuery = (query: string) => {
    searchQuery.value = query
  }

  const setSortBy = (field: 'dueDate' | 'priority' | 'createdAt' | 'title') => {
    if (sortBy.value === field) {
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
    } else {
      sortBy.value = field
      sortOrder.value = 'asc'
    }
  }

  const setSelectedCategory = (category: TaskCategory | 'all') => {
    selectedCategory.value = category
  }

  const setSelectedPriority = (priority: TaskPriority | 'all') => {
    selectedPriority.value = priority
  }

  const toggleShowCompleted = () => {
    showCompleted.value = !showCompleted.value
  }

  const clearFilters = () => {
    activeFilter.value = 'all'
    searchQuery.value = ''
    selectedCategory.value = 'all'
    selectedPriority.value = 'all'
    showCompleted.value = true
    sortBy.value = 'dueDate'
    sortOrder.value = 'asc'
  }

  const toggleTaskCompletion = (taskId: string) => {
    const task = tasks.value.find(t => t.id === taskId)
    if (task) {
      task.completed = !task.completed
      task.status = task.completed ? 'completed' : 'pending'
      task.updatedAt = new Date()
    }
  }

  const addTask = (taskData: CreateTaskRequest): Task => {
    const newTask: Task = {
      id: `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      ...taskData,
      status: 'pending',
      createdAt: new Date(),
      updatedAt: new Date(),
      completed: false,
      tags: taskData.tags || [],
    }
    tasks.value.unshift(newTask) // Add to beginning for recent tasks
    return newTask
  }

  const addQuickTask = (title: string, category: TaskCategory = 'general'): Task => {
    const tomorrow = new Date()
    tomorrow.setDate(tomorrow.getDate() + 1)

    return addTask({
      title,
      description: '',
      priority: 'medium',
      category,
      dueDate: tomorrow,
    })
  }

  const duplicateTask = (taskId: string): Task | null => {
    const originalTask = getTaskById(taskId)
    if (!originalTask) return null

    const duplicatedTask = addTask({
      title: `${originalTask.title} (Copy)`,
      description: originalTask.description,
      priority: originalTask.priority,
      category: originalTask.category,
      dueDate: new Date(originalTask.dueDate),
      tags: [...originalTask.tags],
      estimatedTime: originalTask.estimatedTime,
      agentId: originalTask.agentId,
    })

    return duplicatedTask
  }

  const updateTask = (taskData: UpdateTaskRequest) => {
    console.log('🏪 Tasks Store: updateTask called with:', taskData)

    const taskIndex = tasks.value.findIndex(t => t.id === taskData.id)
    console.log('🔍 Tasks Store: Found task at index:', taskIndex)

    if (taskIndex !== -1) {
      const currentTask = tasks.value[taskIndex]
      if (!currentTask) return

      console.log('📋 Tasks Store: Current task before update:', { ...currentTask })

      // Update only the fields that are provided
      if (taskData.title !== undefined) currentTask.title = taskData.title
      if (taskData.description !== undefined) currentTask.description = taskData.description
      if (taskData.status !== undefined) currentTask.status = taskData.status
      if (taskData.priority !== undefined) currentTask.priority = taskData.priority
      if (taskData.category !== undefined) currentTask.category = taskData.category
      if (taskData.dueDate !== undefined) {
        console.log('📅 Tasks Store: Updating dueDate from', currentTask.dueDate, 'to', taskData.dueDate)
        currentTask.dueDate = taskData.dueDate
      }
      if (taskData.tags !== undefined) currentTask.tags = taskData.tags
      if (taskData.estimatedTime !== undefined) currentTask.estimatedTime = taskData.estimatedTime
      if (taskData.actualTime !== undefined) currentTask.actualTime = taskData.actualTime

      currentTask.updatedAt = new Date()

      console.log('✅ Tasks Store: Task updated to:', { ...currentTask })
    } else {
      console.error('❌ Tasks Store: Task not found with ID:', taskData.id)
    }
  }

  const deleteTask = (taskId: string) => {
    const taskIndex = tasks.value.findIndex(t => t.id === taskId)
    if (taskIndex !== -1) {
      tasks.value.splice(taskIndex, 1)
    }
  }

  const getTaskById = (taskId: string) => {
    return tasks.value.find(t => t.id === taskId)
  }

  const getTasksByCategory = (category: TaskCategory) => {
    return tasks.value.filter(task => task.category === category)
  }

  const getTasksByPriority = (priority: TaskPriority) => {
    return tasks.value.filter(task => task.priority === priority)
  }

  const bulkUpdateTasks = (taskIds: string[], updates: Partial<Task>) => {
    taskIds.forEach(id => {
      const task = tasks.value.find(t => t.id === id)
      if (task) {
        Object.assign(task, updates, { updatedAt: new Date() })
        if (updates.status === 'completed') {
          task.completed = true
        } else if (updates.status && updates.status !== 'completed') {
          task.completed = false
        }
      }
    })
  }

  const bulkDeleteTasks = (taskIds: string[]) => {
    tasks.value = tasks.value.filter(task => !taskIds.includes(task.id))
  }

  const markTasksAsCompleted = (taskIds: string[]) => {
    bulkUpdateTasks(taskIds, { status: 'completed', completed: true })
  }

  const archiveCompletedTasks = () => {
    const completedTasks = tasks.value.filter(task => task.completed)
    // In a real app, you might move these to an archive store or send to backend
    tasks.value = tasks.value.filter(task => !task.completed)
    return completedTasks.length
  }

  const getTasksForAgent = (agentId: string) => {
    return tasks.value.filter(task => task.agentId === agentId)
  }

  const assignTaskToAgent = (taskId: string, agentId: string) => {
    const task = getTaskById(taskId)
    if (task) {
      task.agentId = agentId
      task.updatedAt = new Date()
    }
  }

  const getTaskProgress = (taskId: string) => {
    const task = getTaskById(taskId)
    if (!task) return 0

    if (task.completed) return 100
    if (task.status === 'in_progress') return 50
    if (task.status === 'pending') return 0
    return 0
  }

  const getProductivityStats = () => {
    const now = new Date()
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const thisWeek = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000)
    const thisMonth = new Date(today.getFullYear(), today.getMonth(), 1)

    return {
      today: {
        completed: tasks.value.filter(t => t.completed && new Date(t.updatedAt) >= today).length,
        created: tasks.value.filter(t => new Date(t.createdAt) >= today).length,
      },
      thisWeek: {
        completed: tasks.value.filter(t => t.completed && new Date(t.updatedAt) >= thisWeek).length,
        created: tasks.value.filter(t => new Date(t.createdAt) >= thisWeek).length,
      },
      thisMonth: {
        completed: tasks.value.filter(t => t.completed && new Date(t.updatedAt) >= thisMonth)
          .length,
        created: tasks.value.filter(t => new Date(t.createdAt) >= thisMonth).length,
      },
    }
  }

  // Initialize tasks on store creation
  const initialize = () => {
    if (!isInitialized.value) {
      initializeTasks()
      isInitialized.value = true
    }
  }

  // Auto-initialize
  initialize()

  return {
    // State
    tasks: readonly(tasks),
    loading: readonly(loading),
    error: readonly(error),
    activeFilter: readonly(activeFilter),
    searchQuery: readonly(searchQuery),
    sortBy: readonly(sortBy),
    sortOrder: readonly(sortOrder),
    selectedCategory: readonly(selectedCategory),
    selectedPriority: readonly(selectedPriority),
    showCompleted: readonly(showCompleted),

    // Getters
    filteredTasks,
    taskStats,
    completedTasksCount,
    tasksByCategory,
    tasksByPriority,
    upcomingTasks,
    recentTasks,
    availableCategories,
    availableTags,

    // Actions
    setActiveFilter,
    setSearchQuery,
    setSortBy,
    setSelectedCategory,
    setSelectedPriority,
    toggleShowCompleted,
    clearFilters,
    toggleTaskCompletion,
    addTask,
    addQuickTask,
    duplicateTask,
    updateTask,
    deleteTask,
    bulkUpdateTasks,
    bulkDeleteTasks,
    markTasksAsCompleted,
    archiveCompletedTasks,
    getTaskById,
    getTasksByCategory,
    getTasksByPriority,
    getTasksForAgent,
    assignTaskToAgent,
    getTaskProgress,
    getProductivityStats,
    initializeTasks,
    initialize,
  }
})
