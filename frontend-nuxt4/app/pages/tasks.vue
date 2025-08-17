<template>
  <div class="min-h-screen bg-forest-900 text-white p-6 pt-32">
    <div class="max-w-7xl mx-auto space-y-8">
      <!-- Page Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold mb-2">Task Management</h1>
          <p class="text-gray-400">
            Organize and track your content creation tasks with AI-powered insights
          </p>
        </div>

        <div class="flex items-center space-x-3">
          <button
            :class="currentView === 'dashboard' ? 'rounded-lg bg-orange-500 px-4 py-2 text-sm text-white' : 'rounded-lg bg-forest-700 px-4 py-2 text-sm text-gray-300 hover:bg-forest-600'"
            @click="currentView = 'dashboard'"
          >
            📊 Dashboard
          </button>
          <button
            :class="currentView === 'manager' ? 'rounded-lg bg-orange-500 px-4 py-2 text-sm text-white' : 'rounded-lg bg-forest-700 px-4 py-2 text-sm text-gray-300 hover:bg-forest-600'"
            @click="currentView = 'manager'"
          >
            📋 Task Manager
          </button>
          <button
            class="rounded-lg bg-orange-500 px-4 py-2 text-sm text-white hover:bg-orange-600"
            @click="showCreateModal = true"
          >
            ➕ New Task
          </button>
        </div>
      </div>

      <!-- Dashboard View -->
      <div v-if="currentView === 'dashboard'" class="space-y-6">
      </div>

      <!-- Task Manager View -->
      <div v-if="currentView === 'manager'" class="space-y-6">
        <!-- Filters and Search -->
        <div class="rounded-xl bg-forest-800 p-6">
          <div class="flex flex-col md:flex-row gap-4 items-center justify-between">
            <div class="flex flex-wrap gap-2">
              <button
                v-for="filter in filters"
                :key="filter.value"
                :class="activeFilter === filter.value ? 'rounded-full bg-orange-500 px-4 py-2 text-sm text-white' : 'rounded-full bg-forest-700 px-4 py-2 text-sm text-gray-300 hover:bg-forest-600'"
                @click="activeFilter = filter.value"
              >
                {{ filter.label }}
              </button>
            </div>
            <div class="flex gap-2">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search tasks..."
                class="rounded-lg bg-forest-700 border border-forest-600 px-3 py-2 text-sm text-white placeholder-gray-400 focus:border-orange-500 focus:outline-none"
              />
              <button
                class="rounded-lg bg-orange-500 px-4 py-2 text-sm text-white hover:bg-orange-600"
                @click="showCreateModal = true"
              >
                ➕ Add Task
              </button>
            </div>
          </div>
        </div>

        <!-- Task List -->
        <div class="rounded-xl bg-forest-800 p-6">
          <div class="space-y-3">
            <div
              v-for="task in filteredTasks"
              :key="task.id"
              class="flex items-center justify-between rounded-lg bg-forest-700 p-4 hover:bg-forest-600 transition-colors"
              :class="{
                'border-l-4 border-red-500': isOverdue(task),
                'border-l-4 border-yellow-500': isDueToday(task),
              }"
            >
              <div class="flex items-center space-x-3">
                <input
                  :checked="task.completed"
                  type="checkbox"
                  class="rounded border-forest-600 bg-forest-700 text-orange-500 focus:ring-orange-500"
                  @change="toggleTaskCompletion(task.id)"
                />
                <div class="flex-1">
                  <h4
                    class="font-medium"
                    :class="task.completed ? 'line-through text-gray-500' : 'text-white'"
                  >
                    {{ task.title }}
                  </h4>
                  <p
                    v-if="task.description"
                    class="text-sm mt-1"
                    :class="task.completed ? 'text-gray-500' : 'text-gray-400'"
                  >
                    {{ task.description }}
                  </p>
                  <div class="mt-2 flex items-center space-x-2">
                    <span class="rounded bg-forest-600 px-2 py-1 text-xs text-gray-300">
                      {{ formatCategory(task.category) }}
                    </span>
                    <span
                      class="rounded px-2 py-1 text-xs"
                      :class="getPriorityClass(task.priority)"
                    >
                      {{ formatPriority(task.priority) }}
                    </span>
                    <span class="text-xs text-gray-400">
                      {{ formatDueDate(task.dueDate) }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <button
                  class="text-gray-400 hover:text-white transition-colors p-2"
                  @click="editTask(task)"
                >
                  ✏️
                </button>
                <button
                  class="text-gray-400 hover:text-red-400 transition-colors p-2"
                  @click="deleteTask(task.id)"
                >
                  🗑️
                </button>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="filteredTasks.length === 0" class="text-center py-8">
              <div class="text-gray-400 mb-4">
                <span class="text-4xl">📝</span>
              </div>
              <h5 class="text-lg font-medium text-white mb-2">No tasks found</h5>
              <p class="text-gray-400 mb-4">Create your first task to get started</p>
              <button
                class="rounded-lg bg-orange-500 px-4 py-2 text-sm text-white hover:bg-orange-600"
                @click="showCreateModal = true"
              >
                Create Task
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Create Task Modal -->
      <TaskModal
        v-if="showCreateModal || editingTask"
        :task="editingTask"
        @close="closeModal"
        @save="saveTask"
      />

      <!-- AI Task Suggestions -->
      <div v-if="currentView === 'dashboard' && aiSuggestions.length > 0" class="rounded-xl bg-forest-800 p-6">
        <div class="mb-4 flex items-center space-x-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-lg overflow-hidden" :style="{ backgroundColor: selectedAgentData.color + '20' }">
            <img
              v-if="selectedAgentData.image"
              :src="selectedAgentData.image"
              :alt="selectedAgentData.name"
              class="h-full w-full object-cover"
            />
            <span v-else class="text-lg">🤖</span>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-white">{{ selectedAgentData.name }} Suggestions</h3>
            <p class="text-sm text-gray-400">Smart recommendations for your workflow</p>
          </div>
        </div>

        <div class="space-y-3">
          <div
            v-for="suggestion in aiSuggestions"
            :key="suggestion.id"
            class="flex items-center justify-between p-4 rounded-lg bg-forest-700 hover:bg-forest-600 transition-colors"
          >
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 rounded-lg flex items-center justify-center bg-forest-600">
                <span class="text-lg">{{ suggestion.icon }}</span>
              </div>
              <div>
                <h4 class="font-medium text-white">{{ suggestion.title }}</h4>
                <p class="text-sm text-gray-400">{{ suggestion.description }}</p>
                <div class="flex items-center space-x-2 mt-1">
                  <span
                    class="rounded px-2 py-1 text-xs"
                    :class="getPriorityClass(suggestion.priority)"
                  >
                    {{ formatPriority(suggestion.priority) }}
                  </span>
                  <span class="rounded bg-forest-600 px-2 py-1 text-xs text-gray-300">
                    {{ formatCategory(suggestion.category) }}
                  </span>
                </div>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <button
                class="text-gray-400 hover:text-white px-2 py-1 text-sm"
                @click="dismissSuggestion(suggestion.id)"
              >
                ✕
              </button>
              <button
                class="rounded bg-orange-500 px-3 py-1 text-sm text-white hover:bg-orange-600"
                @click="createFromSuggestion(suggestion)"
              >
                Create Task
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Task Analytics -->
      <div v-if="currentView === 'dashboard'" class="rounded-xl bg-forest-800 p-6">
        <h3 class="text-lg font-semibold text-white mb-6">Task Analytics</h3>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- Completion Rate -->
          <div class="text-center">
            <div class="relative w-20 h-20 mx-auto mb-3">
              <svg class="w-20 h-20 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  class="text-gray-600"
                  stroke="currentColor"
                  stroke-width="3"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  class="text-green-400"
                  stroke="currentColor"
                  stroke-width="3"
                  fill="none"
                  stroke-linecap="round"
                  :stroke-dasharray="`${taskStats.completionRate}, 100`"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-lg font-bold text-white">{{ taskStats.completionRate }}%</span>
              </div>
            </div>
            <div class="text-sm text-gray-400">Completion Rate</div>
          </div>

          <!-- Average Time -->
          <div class="text-center">
            <div class="text-2xl font-bold text-blue-400 mb-2">
              {{ averageTaskTime }}
            </div>
            <div class="text-sm text-gray-400">Avg. Task Time</div>
          </div>

          <!-- Tasks This Week -->
          <div class="text-center">
            <div class="text-2xl font-bold text-yellow-400 mb-2">
              {{ tasksThisWeek }}
            </div>
            <div class="text-sm text-gray-400">Tasks This Week</div>
          </div>

          <!-- Productivity Score -->
          <div class="text-center">
            <div class="text-2xl font-bold text-pink-400 mb-2">
              {{ productivityScore }}
            </div>
            <div class="text-sm text-gray-400">Productivity Score</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useTasksStore } from '../../stores/tasks'

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// Type definitions
type Task = {
  id: string
  title: string
  description: string
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled' | 'on_hold'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  category: 'content' | 'marketing' | 'analytics' | 'seo' | 'monetization' | 'community' | 'planning' | 'research' | 'general'
  dueDate: Date
  createdAt: Date
  updatedAt: Date
  completed: boolean
  userId?: string
  agentId?: string
  tags: string[]
  estimatedTime?: number
  actualTime?: number
}

type TaskCategory = 'content' | 'marketing' | 'analytics' | 'seo' | 'monetization' | 'community' | 'planning' | 'research' | 'general'
type TaskPriority = 'low' | 'medium' | 'high' | 'urgent'
type TaskFilter = 'all' | 'pending' | 'completed' | 'in_progress' | 'high_priority' | 'due_today' | 'overdue'

// Set page title
useHead({
  title: 'Task Management - Vidalytics'
})

const tasksStore = useTasksStore()

// Local state
const currentView = ref<'dashboard' | 'manager'>('dashboard')
const showCreateModal = ref(false)
const editingTask = ref<Task | null>(null)
const activeFilter = ref<TaskFilter>('all')
const searchQuery = ref('')

// Agent settings state
const selectedAgent = ref(1)
const agentName = ref('Professional Assistant')

// Available agents (same as in settings and modal)
const agents = [
  {
    id: 1,
    name: 'Agent 1',
    image: '/Agent1.png',
    color: '#ea580c', // Orange
    description: 'AI Content Creator',
    personality: 'Professional & Analytical',
  },
  {
    id: 2,
    name: 'Agent 2',
    image: '/Agent2.png',
    color: '#eab308', // Yellow
    description: 'Marketing Specialist',
    personality: 'Strategic & Data-Driven',
  },
  {
    id: 3,
    name: 'Agent 3',
    image: '/Agent3.png',
    color: '#16a34a', // Green
    description: 'Analytics Expert',
    personality: 'Detail-Oriented & Insightful',
  },
  {
    id: 4,
    name: 'Agent 4',
    image: '/Agent4.png',
    color: '#ea580c', // Orange
    description: 'Creative Assistant',
    personality: 'Innovative & Artistic',
  },
  {
    id: 5,
    name: 'Agent 5',
    image: '/Agent5.png',
    color: '#dc2626', // Red/Pink
    description: 'Strategy Advisor',
    personality: 'Visionary & Strategic',
  },
]

// Computed property for selected agent data
const selectedAgentData = computed(() => {
  const agent = agents.find(agent => agent.id === selectedAgent.value) || agents[0]
  return {
    ...agent,
    name: agentName.value || agent.name
  }
})

// Load agent settings from localStorage
const loadAgentSettings = () => {
  if (typeof window !== 'undefined') {
    const savedSettings = localStorage.getItem('agentSettings')
    if (savedSettings) {
      const settings = JSON.parse(savedSettings)
      selectedAgent.value = settings.selectedAgent || 1
      agentName.value = settings.name || 'Professional Assistant'
    }
  }
}

// Initialize agent settings on mount
onMounted(() => {
  loadAgentSettings()
})

// Filter options
const filters = [
  { label: 'All Tasks', value: 'all' as TaskFilter },
  { label: 'Pending', value: 'pending' as TaskFilter },
  { label: 'In Progress', value: 'in_progress' as TaskFilter },
  { label: 'Completed', value: 'completed' as TaskFilter },
  { label: 'High Priority', value: 'high_priority' as TaskFilter },
  { label: 'Due Today', value: 'due_today' as TaskFilter },
  { label: 'Overdue', value: 'overdue' as TaskFilter },
]

// Computed properties
const taskStats = computed(() => tasksStore.taskStats)
const productivityStats = computed(() => tasksStore.getProductivityStats())

// Filtered tasks based on active filter and search
const filteredTasks = computed(() => {
  let tasks = tasksStore.tasks

  // Apply filter
  switch (activeFilter.value) {
    case 'pending':
      tasks = tasks.filter(t => t.status === 'pending')
      break
    case 'in_progress':
      tasks = tasks.filter(t => t.status === 'in_progress')
      break
    case 'completed':
      tasks = tasks.filter(t => t.completed)
      break
    case 'high_priority':
      tasks = tasks.filter(t => t.priority === 'high' || t.priority === 'urgent')
      break
    case 'due_today':
      tasks = tasks.filter(t => isDueToday(t))
      break
    case 'overdue':
      tasks = tasks.filter(t => isOverdue(t))
      break
    default:
      // 'all' - no filter
      break
  }

  // Apply search
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    tasks = tasks.filter(t =>
      t.title.toLowerCase().includes(query) ||
      t.description.toLowerCase().includes(query) ||
      t.category.toLowerCase().includes(query) ||
      t.tags.some(tag => tag.toLowerCase().includes(query))
    )
  }

  return tasks
})

// AI Suggestions (mock data - would come from AI service)
const aiSuggestions = ref([
  {
    id: '1',
    title: 'Optimize video thumbnails',
    description: 'Your click-through rate could improve with better thumbnails',
    priority: 'high' as TaskPriority,
    category: 'content' as TaskCategory,
    icon: '🎨',
    color: '#9333ea',
    estimatedTime: 60,
  },
  {
    id: '2',
    title: 'Research trending keywords',
    description: 'New keywords are trending in your niche',
    priority: 'medium' as TaskPriority,
    category: 'seo' as TaskCategory,
    icon: '🔍',
    color: '#059669',
    estimatedTime: 45,
  },
  {
    id: '3',
    title: 'Engage with community comments',
    description: 'You have 23 unresponded comments from this week',
    priority: 'low' as TaskPriority,
    category: 'community' as TaskCategory,
    icon: '💬',
    color: '#7c3aed',
    estimatedTime: 30,
  },
])

// Analytics computed properties
const averageTaskTime = computed(() => {
  const tasks = tasksStore.tasks.filter(t => t.actualTime)
  if (tasks.length === 0) return '0m'
  const avg = tasks.reduce((sum, t) => sum + (t.actualTime || 0), 0) / tasks.length
  return `${Math.round(avg)}m`
})

const tasksThisWeek = computed(() => {
  const weekAgo = new Date()
  weekAgo.setDate(weekAgo.getDate() - 7)
  return tasksStore.tasks.filter(t => new Date(t.createdAt) >= weekAgo).length
})

const productivityScore = computed(() => {
  const stats = productivityStats.value
  const weeklyCompletion = stats.thisWeek.completed
  const weeklyCreated = stats.thisWeek.created
  
  if (weeklyCreated === 0) return 0
  
  const completionRate = (weeklyCompletion / weeklyCreated) * 100
  const activityBonus = Math.min(weeklyCompletion * 2, 20)
  
  return Math.min(Math.round(completionRate + activityBonus), 100)
})

// Methods
const editTask = (task: Task) => {
  editingTask.value = task
}

const createTaskWithCategory = (category?: TaskCategory) => {
  showCreateModal.value = true
  // Could pre-fill category if provided
}

const closeModal = () => {
  showCreateModal.value = false
  editingTask.value = null
}

const saveTask = (taskData: any) => {
  if (editingTask.value) {
    tasksStore.updateTask({ id: editingTask.value.id, ...taskData })
  } else {
    tasksStore.addTask(taskData)
  }
  closeModal()
}

const createFromSuggestion = (suggestion: any) => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  
  tasksStore.addTask({
    title: suggestion.title,
    description: suggestion.description,
    priority: suggestion.priority,
    category: suggestion.category,
    dueDate: tomorrow,
    estimatedTime: suggestion.estimatedTime,
    tags: ['ai-suggested'],
  })
  
  dismissSuggestion(suggestion.id)
}

const dismissSuggestion = (id: string) => {
  const index = aiSuggestions.value.findIndex(s => s.id === id)
  if (index !== -1) {
    aiSuggestions.value.splice(index, 1)
  }
}

// Utility functions
const formatCategory = (category: string) => {
  return category.charAt(0).toUpperCase() + category.slice(1).replace('_', ' ')
}

const formatPriority = (priority: string) => {
  return priority.charAt(0).toUpperCase() + priority.slice(1)
}

const getPriorityClass = (priority: TaskPriority) => {
  switch (priority) {
    case 'urgent': return 'bg-red-500 text-white'
    case 'high': return 'bg-orange-500 text-white'
    case 'medium': return 'bg-yellow-500 text-black'
    case 'low': return 'bg-green-500 text-white'
    default: return 'bg-forest-600 text-white'
  }
}

// Task utility functions
const isOverdue = (task: Task) => {
  return new Date(task.dueDate) < new Date() && !task.completed
}

const isDueToday = (task: Task) => {
  const today = new Date()
  const dueDate = new Date(task.dueDate)
  return (
    dueDate.getDate() === today.getDate() &&
    dueDate.getMonth() === today.getMonth() &&
    dueDate.getFullYear() === today.getFullYear() &&
    !task.completed
  )
}

const formatDueDate = (date: Date) => {
  const now = new Date()
  const dueDate = new Date(date)
  const diffTime = dueDate.getTime() - now.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays < 0) {
    return `${Math.abs(diffDays)}d overdue`
  } else if (diffDays === 0) {
    return 'Due today'
  } else if (diffDays === 1) {
    return 'Due tomorrow'
  } else if (diffDays <= 7) {
    return `Due in ${diffDays}d`
  } else {
    return dueDate.toLocaleDateString()
  }
}

const toggleTaskCompletion = (taskId: string) => {
  const task = tasksStore.tasks.find(t => t.id === taskId)
  if (task) {
    tasksStore.updateTask({
      id: taskId,
      completed: !task.completed,
      status: !task.completed ? 'completed' : 'pending'
    })
  }
}

const deleteTask = (taskId: string) => {
  if (confirm('Are you sure you want to delete this task?')) {
    tasksStore.deleteTask(taskId)
  }
}
</script>

<style scoped>
.transition-colors {
  transition: background-color 0.2s ease-in-out;
}
</style>
