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
    switch (activeFilter.value) {
      case 'completed':
        return tasks.value.filter(task => task.completed)
      case 'pending':
        return tasks.value.filter(task => task.status === 'pending')
      case 'in_progress':
        return tasks.value.filter(task => task.status === 'in_progress')
      case 'high_priority':
        return tasks.value.filter(task => task.priority === 'high' || task.priority === 'urgent')
      case 'due_today':
        const today = new Date()
        today.setHours(0, 0, 0, 0)
        const tomorrow = new Date(today)
        tomorrow.setDate(tomorrow.getDate() + 1)
        return tasks.value.filter(task => {
          const dueDate = new Date(task.dueDate)
          dueDate.setHours(0, 0, 0, 0)
          return dueDate >= today && dueDate < tomorrow
        })
      case 'overdue':
        const now = new Date()
        return tasks.value.filter(task => new Date(task.dueDate) < now && !task.completed)
      default:
        return tasks.value
    }
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

  // Actions
  const setActiveFilter = (filter: TaskFilter) => {
    activeFilter.value = filter
  }

  const toggleTaskCompletion = (taskId: string) => {
    const task = tasks.value.find(t => t.id === taskId)
    if (task) {
      task.completed = !task.completed
      task.status = task.completed ? 'completed' : 'pending'
      task.updatedAt = new Date()
    }
  }

  const addTask = (taskData: CreateTaskRequest) => {
    const newTask: Task = {
      id: Date.now().toString(),
      ...taskData,
      status: 'pending',
      createdAt: new Date(),
      updatedAt: new Date(),
      completed: false,
      tags: taskData.tags || [],
    }
    tasks.value.push(newTask)
  }

  const updateTask = (taskData: UpdateTaskRequest) => {
    const taskIndex = tasks.value.findIndex(t => t.id === taskData.id)
    if (taskIndex !== -1) {
      const currentTask = tasks.value[taskIndex]
      if (!currentTask) return

      // Update only the fields that are provided
      if (taskData.title !== undefined) currentTask.title = taskData.title
      if (taskData.description !== undefined) currentTask.description = taskData.description
      if (taskData.status !== undefined) currentTask.status = taskData.status
      if (taskData.priority !== undefined) currentTask.priority = taskData.priority
      if (taskData.category !== undefined) currentTask.category = taskData.category
      if (taskData.dueDate !== undefined) currentTask.dueDate = taskData.dueDate
      if (taskData.tags !== undefined) currentTask.tags = taskData.tags
      if (taskData.estimatedTime !== undefined) currentTask.estimatedTime = taskData.estimatedTime
      if (taskData.actualTime !== undefined) currentTask.actualTime = taskData.actualTime

      currentTask.updatedAt = new Date()
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

  // Initialize tasks on store creation
  initializeTasks()

  return {
    // State
    tasks: readonly(tasks),
    loading: readonly(loading),
    error: readonly(error),
    activeFilter: readonly(activeFilter),

    // Getters
    filteredTasks,
    taskStats,
    completedTasksCount,

    // Actions
    setActiveFilter,
    toggleTaskCompletion,
    addTask,
    updateTask,
    deleteTask,
    getTaskById,
    getTasksByCategory,
    getTasksByPriority,
    initializeTasks,
  }
})
