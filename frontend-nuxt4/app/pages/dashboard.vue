<template>
  <div class="min-h-screen bg-forest-900 text-white">
    <!-- Dashboard Content -->
    <div class="p-6 pt-24">
      <!-- Page Header -->
      <div class="mb-4 flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <h1 class="text-2xl font-bold text-white">Dashboard</h1>
          <span class="text-gray-400">•</span>
          <p class="text-gray-400">Overview of your channel performance and tasks</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="text-sm text-gray-400">Last 30 days</div>
        </div>
      </div>

      <!-- Channel Statistics -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div class="rounded-xl bg-forest-800 p-4 text-center">
          <div class="text-2xl font-bold text-blue-400">{{ formatNumber(channelStats.totalSubscribers) }}</div>
          <div class="text-sm text-gray-400">Current Subscribers</div>
        </div>
        <div class="rounded-xl bg-forest-800 p-4 text-center">
          <div class="text-2xl font-bold text-green-400">{{ formatSubscriberChange(channelStats.subscriberChange) }}</div>
          <div class="text-sm text-gray-400">Sub Change (7 days)</div>
        </div>
        <div class="rounded-xl bg-forest-800 p-4 text-center">
          <div class="text-2xl font-bold text-yellow-400">{{ formatNumber(channelStats.totalViews) }}</div>
          <div class="text-sm text-gray-400">Total Views</div>
        </div>
        <div class="rounded-xl bg-forest-800 p-4 text-center">
          <div class="text-2xl font-bold text-orange-400">{{ channelStats.avgViewDuration }}</div>
          <div class="text-sm text-gray-400">Avg View Duration</div>
        </div>
      </div>

      <!-- Dashboard Content Grid -->
      <div class="mb-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <!-- Left Column: Task Manager + Channel Goals -->
        <div class="space-y-6">
          <!-- Dynamic Task Manager Compartment -->
          <div class="rounded-xl bg-forest-800 p-6">
          <div class="mb-6 flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-500">
                <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">Today's Tasks</h3>
                <p class="text-sm text-gray-400">{{ taskStats.completed }} of {{ taskStats.total }} completed</p>
              </div>
            </div>
            <NuxtLink to="/tasks" class="text-gray-400 hover:text-white transition-colors">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 111.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
              </svg>
            </NuxtLink>
          </div>

          <!-- Quick Actions -->
          <div class="mb-6 flex items-center justify-between">
            <div class="flex space-x-2">
              <button
                :class="dashboardFilter === 'all' ? 'rounded-full bg-orange-500 px-4 py-2 text-sm text-white' : 'rounded-full bg-forest-700 px-4 py-2 text-sm text-gray-300 hover:bg-forest-600'"
                @click="dashboardFilter = 'all'"
              >
                All
              </button>
              <button
                :class="dashboardFilter === 'due_today' ? 'rounded-full bg-orange-500 px-4 py-2 text-sm text-white' : 'rounded-full bg-forest-700 px-4 py-2 text-sm text-gray-300 hover:bg-forest-600'"
                @click="dashboardFilter = 'due_today'"
              >
                Due Today
              </button>
              <button
                :class="dashboardFilter === 'high_priority' ? 'rounded-full bg-orange-500 px-4 py-2 text-sm text-white' : 'rounded-full bg-forest-700 px-4 py-2 text-sm text-gray-300 hover:bg-forest-600'"
                @click="dashboardFilter = 'high_priority'"
              >
                High Priority
              </button>
            </div>
            <button class="rounded-lg bg-orange-500 px-4 py-2 text-sm text-white hover:bg-orange-600" @click="showCreateModal = true">
              ➕ Add Task
            </button>
          </div>

          <!-- Dynamic Task List -->
          <div class="space-y-3">
            <div
              v-for="task in dashboardTasks"
              :key="task.id"
              class="flex items-center justify-between rounded-lg bg-forest-700 p-4 hover:bg-forest-600 transition-colors cursor-pointer"
              :class="{
                'border-l-4 border-red-500': isOverdue(task),
                'border-l-4 border-yellow-500': isDueToday(task),
              }"
              @click="editTask(task)"
            >
              <div class="flex items-center space-x-3">
                <input
                  :checked="task.completed"
                  type="checkbox"
                  class="rounded border-forest-600 bg-forest-700 text-orange-500 focus:ring-orange-500"
                  @click.stop
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
                    {{ truncateText(task.description, 60) }}
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
              <button
                class="text-gray-400 hover:text-white transition-colors"
                @click.stop="editTask(task)"
              >
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
                </svg>
              </button>
            </div>

            <!-- Empty State -->
            <div v-if="dashboardTasks.length === 0" class="text-center py-8">
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

            <!-- View All Tasks Link -->
            <div v-if="dashboardTasks.length > 0" class="text-center pt-4">
              <NuxtLink
                to="/tasks"
                class="text-sm text-orange-500 hover:text-orange-400 transition-colors"
              >
                View All Tasks ({{ taskStats.total }}) →
              </NuxtLink>
            </div>
          </div>
        </div>
        </div>

        <!-- Channel Goals & AI Insights -->
        <div class="space-y-6">
          <!-- Channel Goals -->
          <div class="rounded-xl bg-forest-800 p-6">
            <div class="mb-6 flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-500">
                  <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-white">Channel Goals</h3>
                  <p class="text-sm text-gray-400">Track your progress</p>
                </div>
              </div>
              <button class="text-gray-400 hover:text-white transition-colors">
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                </svg>
              </button>
            </div>

            <!-- Goals Grid -->
            <div class="space-y-6">
              <!-- Views Goal -->
              <div class="rounded-lg bg-gradient-to-r from-orange-500 to-orange-600 p-4 text-white">
              <div class="mb-4 flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
                    <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/>
                  </svg>
                  <span class="font-semibold">Views</span>
                </div>
                <button class="text-white/80 hover:text-white">
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                  </svg>
                </button>
              </div>
              <div class="mb-4 flex items-center justify-center">
                <div class="relative h-24 w-24">
                  <svg class="h-24 w-24 transform -rotate-90" viewBox="0 0 100 100">
                    <circle
                      cx="50"
                      cy="50"
                      r="40"
                      stroke="currentColor"
                      stroke-width="8"
                      fill="transparent"
                      class="text-white/20"
                    />
                    <circle
                      cx="50"
                      cy="50"
                      r="40"
                      stroke="currentColor"
                      stroke-width="8"
                      fill="transparent"
                      stroke-dasharray="251.2"
                      stroke-dashoffset="62.8"
                      class="text-white"
                      stroke-linecap="round"
                    />
                  </svg>
                  <div class="absolute inset-0 flex items-center justify-center">
                    <span class="text-2xl font-bold">75%</span>
                  </div>
                </div>
              </div>
              <div class="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div class="text-lg font-bold">7.5k</div>
                  <div class="text-xs opacity-80">Current</div>
                </div>
                <div>
                  <div class="text-lg font-bold">2.5k</div>
                  <div class="text-xs opacity-80">Remaining</div>
                </div>
                <div>
                  <div class="text-lg font-bold">10k</div>
                  <div class="text-xs opacity-80">Goal</div>
                </div>
              </div>
            </div>

              <!-- Subscribers Goal -->
              <div class="rounded-lg bg-gradient-to-r from-orange-600 to-orange-700 p-4 text-white">
              <div class="mb-4 flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
                  </svg>
                  <span class="font-semibold">Subscribers</span>
                </div>
                <button class="text-white/80 hover:text-white">
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                  </svg>
                </button>
              </div>
              <div class="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div class="text-lg font-bold">1.2k</div>
                  <div class="text-xs opacity-80">Current</div>
                </div>
                <div>
                  <div class="text-lg font-bold">800</div>
                  <div class="text-xs opacity-80">Remaining</div>
                </div>
                <div>
                  <div class="text-lg font-bold">2k</div>
                  <div class="text-xs opacity-80">Goal</div>
                </div>
              </div>
            </div>
          </div>

            <!-- Quick Actions -->
            <div class="mt-6 grid grid-cols-2 gap-4">
              <button
                class="flex items-center justify-center space-x-2 rounded-lg bg-forest-700 p-3 text-sm text-white hover:bg-forest-600"
                @click="openAgentModal"
              >
                <span>🤖</span>
                <span>AI Assistant</span>
              </button>
              <button
                class="flex items-center justify-center space-x-2 rounded-lg bg-orange-500 p-3 text-sm text-white hover:bg-orange-600"
                @click="showCreateModal = true"
              >
                <span>➕</span>
                <span>Add New Task</span>
              </button>
            </div>
          </div>

          </div>
        </div>

        <!-- Right Column: Agent Suggestions -->
        <div class="space-y-6">
          <!-- Agent Task Suggestions -->
          <div v-if="aiSuggestions.length > 0" class="rounded-xl bg-forest-800 p-6">
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
                v-for="suggestion in aiSuggestions.slice(0, 2)"
                :key="suggestion.id"
                class="flex items-center justify-between p-3 rounded-lg bg-forest-700 hover:bg-forest-600 transition-colors"
              >
                <div class="flex items-center space-x-3">
                  <div
                    class="w-8 h-8 rounded-lg flex items-center justify-center bg-forest-600"
                  >
                    <span class="text-sm">{{ suggestion.icon }}</span>
                  </div>
                  <div>
                    <h4 class="font-medium text-white">{{ suggestion.title }}</h4>
                    <p class="text-sm text-gray-400">{{ suggestion.description }}</p>
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
                    Create
                  </button>
                </div>
              </div>
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
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useAnalyticsStore } from '../../stores/analytics'
import { useTasksStore } from '../../stores/tasks'

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

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
    name: 'Levi',
    image: '/Agent2.png',
    color: '#FFEAA7', // Yellow
    description: 'Professional & Analytical',
    personality: 'Innovative & Artistic',
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

// Type imports
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
type TaskFilter = 'all' | 'pending' | 'completed' | 'in_progress' | 'high_priority' | 'due_today' | 'overdue'
type TaskPriority = 'low' | 'medium' | 'high' | 'urgent'

// SEO optimization
const { setDashboardSEO, setWebsiteStructuredData } = useSEO()
setDashboardSEO()
setWebsiteStructuredData()

const tasksStore = useTasksStore()
const analyticsStore = useAnalyticsStore()

// Local state
const showCreateModal = ref(false)
const editingTask = ref<Task | null>(null)
const dashboardFilter = ref<TaskFilter>('all')

// Computed properties
const taskStats = computed(() => tasksStore.taskStats)

// Channel statistics computed properties
const channelStats = computed(() => {
  return {
    totalSubscribers: analyticsStore.data?.overview?.data?.total_subscribers || 125000,
    subscriberChange: analyticsStore.subscriberGrowth?.net || 150,
    totalViews: analyticsStore.data?.overview?.data?.total_views || analyticsStore.totalViews || 1250000,
    avgViewDuration: formatDuration(analyticsStore.data?.overview?.data?.avg_view_duration || 272) // 272 seconds = 4:32
  }
})

// Formatting functions for channel stats
const formatNumber = (num: number) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const formatSubscriberChange = (change: number) => {
  const prefix = change >= 0 ? '+' : ''
  return prefix + formatNumber(Math.abs(change))
}

const formatDuration = (seconds: number) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

const dashboardTasks = computed(() => {
  let tasks = tasksStore.filteredTasks

  // Apply dashboard-specific filter
  switch (dashboardFilter.value) {
    case 'due_today':
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      const tomorrow = new Date(today)
      tomorrow.setDate(tomorrow.getDate() + 1)
      tasks = tasks.filter(task => {
        const dueDate = new Date(task.dueDate)
        dueDate.setHours(0, 0, 0, 0)
        return dueDate >= today && dueDate < tomorrow
      })
      break
    case 'high_priority':
      tasks = tasks.filter(task => task.priority === 'high' || task.priority === 'urgent')
      break
  }

  // Limit to 5 tasks for dashboard
  return tasks.slice(0, 5)
})

// AI Suggestions (mock data - would come from AI service)
const aiSuggestions = ref([
  {
    id: '1',
    title: 'Optimize video thumbnails',
    description: 'Your CTR could improve with better thumbnails',
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
])

// Methods
const toggleTaskCompletion = (taskId: string) => {
  tasksStore.toggleTaskCompletion(taskId)
}

const editTask = (task: Task) => {
  editingTask.value = task
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

const openAgentModal = () => {
  // This would open the agent modal - integrate with existing agent system
  console.log('Opening agent modal...')
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

const isOverdue = (task: Task) => {
  return new Date(task.dueDate) < new Date() && !task.completed
}

const isDueToday = (task: Task) => {
  const today = new Date()
  const dueDate = new Date(task.dueDate)
  return today.toDateString() === dueDate.toDateString() && !task.completed
}

const formatDueDate = (date: Date) => {
  const now = new Date()
  const dueDate = new Date(date)
  const diffTime = dueDate.getTime() - now.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Due today'
  if (diffDays === 1) return 'Due tomorrow'
  if (diffDays === -1) return 'Due yesterday'
  if (diffDays < 0) return `${Math.abs(diffDays)}d overdue`
  if (diffDays <= 7) return `Due in ${diffDays}d`

  return dueDate.toLocaleDateString()
}

const truncateText = (text: string, maxLength: number) => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

// Load settings on component mount
onMounted(() => {
  loadAgentSettings()
})
</script>
