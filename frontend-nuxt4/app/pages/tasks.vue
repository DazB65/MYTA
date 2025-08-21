<template>
  <div class="min-h-screen bg-forest-900 text-white">
    <div class="p-4 pt-32">
      <div class="space-y-8">
      <!-- Page Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-white mb-2">Task Management</h1>
          <p class="text-gray-400">
            Organize and track your content creation tasks with AI-powered insights
          </p>
        </div>

        <div class="flex items-center space-x-3">
          <button
            :class="currentView === 'dashboard' ? 'rounded-lg bg-orange-500 px-4 py-2 text-sm text-white' : 'rounded-lg bg-forest-700 px-4 py-2 text-sm text-gray-300 hover:bg-forest-600'"
            @click="currentView = 'dashboard'"
          >
            📅 Calendar
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
        <!-- Two Column Layout: Calendar + Levi Suggestions -->
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <!-- Left Column: Calendar (2/3 width) -->
          <div class="lg:col-span-2">
            <!-- Calendar Container -->
            <div class="rounded-xl bg-forest-800 p-6">
              <!-- Calendar Header -->
              <div class="mb-6 flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <button @click="previousMonth" class="p-2 rounded-lg bg-forest-700 hover:bg-forest-600 text-white">
                    <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                  </button>
                  <h2 class="text-xl font-bold text-white">{{ currentMonthYear }}</h2>
                  <button @click="nextMonth" class="p-2 rounded-lg bg-forest-700 hover:bg-forest-600 text-white">
                    <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                    </svg>
                  </button>
                </div>
                <div class="flex items-center space-x-2">
                  <button @click="goToToday" class="px-4 py-2 rounded-lg bg-orange-500 hover:bg-orange-600 text-white text-sm">
                    Today
                  </button>
                </div>
              </div>

              <!-- Calendar Grid -->
              <div class="grid grid-cols-7 gap-1">
                <!-- Day Headers -->
                <div v-for="day in dayHeaders" :key="day" class="p-3 text-center text-sm font-medium text-gray-400">
                  {{ day }}
                </div>

                <!-- Calendar Days -->
                <div
                  v-for="day in calendarDays"
                  :key="`${day.date.getFullYear()}-${day.date.getMonth()}-${day.date.getDate()}`"
                  :class="[
                    'min-h-[120px] p-2 border border-forest-700 rounded-lg cursor-pointer transition-colors',
                    day.isCurrentMonth ? 'bg-forest-800 hover:bg-forest-700' : 'bg-forest-900 opacity-50',
                    day.isToday ? 'ring-2 ring-orange-500' : '',
                    selectedDate && day.date.toDateString() === selectedDate.toDateString() ? 'bg-forest-600' : ''
                  ]"
                  @click="selectDate(day.date)"
                >
                  <!-- Day Number -->
                  <div class="flex items-center justify-between mb-2">
                    <span :class="[
                      'text-sm font-medium',
                      day.isToday ? 'text-orange-400' : day.isCurrentMonth ? 'text-white' : 'text-gray-500'
                    ]">
                      {{ day.date.getDate() }}
                    </span>
                    <button
                      v-if="day.isCurrentMonth"
                      @click.stop="addTaskToDate(day.date)"
                      class="text-gray-400 hover:text-white text-xs opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      +
                    </button>
                  </div>

                  <!-- Tasks, Content, and Goals for this day -->
                  <div class="space-y-1">
                    <div
                      v-for="item in getTasksForDate(day.date)"
                      :key="`${item.type || 'task'}-${item.id}`"
                      :class="[
                        'text-xs p-1 rounded truncate cursor-pointer transition-colors',
                        item.type === 'content' ? getContentColor() :
                        item.type === 'goal' ? getGoalColor() :
                        getTaskColor(),
                        item.completed ? 'opacity-50 line-through' : ''
                      ]"
                      @click.stop.prevent="item.type === 'content' ? openContentModal(item) : item.type === 'goal' ? openGoalModal(item) : editTask(item)"
                      :title="item.type === 'content' ? `${item.title} (${getStageLabel(item.status)})` :
                               item.type === 'goal' ? `Goal: ${item.title} (${Math.round((item.current / item.target) * 100)}%)` :
                               item.title"
                    >
                      <div class="flex items-center space-x-1">
                        <span v-if="item.type === 'content'" class="text-xs opacity-75">
                          {{ item.pillar?.icon || '📄' }}
                        </span>
                        <span v-else-if="item.type === 'goal'" class="text-xs opacity-75">
                          {{ item.icon || '🎯' }}
                        </span>
                        <span v-else class="text-xs opacity-75">📋</span>
                        <span class="truncate">{{ item.title }}</span>
                      </div>
                      <div v-if="item.type === 'content'" class="text-xs opacity-60 mt-0.5">
                        {{ getStageLabel(item.status) }}
                      </div>
                      <div v-else-if="item.type === 'goal'" class="text-xs opacity-60 mt-0.5">
                        {{ Math.round((item.current / item.target) * 100) }}% Complete
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Calendar Legend -->
              <div class="mt-4 pt-4 border-t border-forest-700">
                <div class="flex items-center justify-between text-xs">
                  <div class="flex items-center space-x-6">
                    <div class="flex items-center space-x-2">
                      <div class="w-3 h-3 rounded bg-blue-500/20 border border-blue-500/40"></div>
                      <span class="text-gray-400">📄 Content</span>
                    </div>
                    <div class="flex items-center space-x-2">
                      <div class="w-3 h-3 rounded bg-orange-500/20 border border-orange-500/40"></div>
                      <span class="text-gray-400">📋 Tasks</span>
                    </div>
                    <div class="flex items-center space-x-2">
                      <div class="w-3 h-3 rounded bg-green-500/20 border border-green-500/40"></div>
                      <span class="text-gray-400">🎯 Goals</span>
                    </div>
                  </div>
                  <div class="text-gray-500">
                    Unified Calendar View
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column: Levi Suggestions (1/3 width) -->
          <div class="space-y-6">
            <!-- AI Task Suggestions -->
            <div class="rounded-xl bg-forest-800 p-6">
              <div class="mb-6 flex items-center space-x-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-lg overflow-hidden" style="background-color: #FFEAA720;">
                  <img
                    src="/optimized/Agent2.jpg"
                    alt="Levi"
                    class="h-full w-full object-cover rounded-lg"
                  />
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-white">Levi Suggestions</h3>
                  <p class="text-sm text-gray-400">Smart task recommendations</p>
                </div>
              </div>

              <div class="space-y-3">
                <div
                  v-for="suggestion in aiSuggestions"
                  :key="suggestion.id"
                  class="flex items-center justify-between p-3 rounded-lg bg-forest-700 hover:bg-forest-600 transition-colors"
                >
                  <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-forest-600">
                      <span class="text-sm">{{ suggestion.icon }}</span>
                    </div>
                    <div>
                      <h4 class="font-medium text-white">{{ suggestion.title }}</h4>
                      <p class="text-sm text-gray-400">{{ suggestion.description }}</p>
                    </div>
                  </div>
                  <button class="rounded bg-orange-500 px-3 py-1 text-sm text-white hover:bg-orange-600" @click="addSuggestionAsTask(suggestion)">
                    Add
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Task Details Sidebar (when date selected) -->
        <div v-if="selectedDate" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Selected Date Tasks -->
          <div class="lg:col-span-2 rounded-xl bg-forest-800 p-6">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-lg font-semibold text-white">
                Tasks for {{ formatDate(selectedDate) }}
              </h3>
              <button
                @click="addTaskToSelectedDate"
                class="rounded-lg bg-orange-500 px-4 py-2 text-sm text-white hover:bg-orange-600"
              >
                + Add Task
              </button>
            </div>

            <div class="space-y-3">
              <div
                v-for="item in getTasksForDate(selectedDate)"
                :key="`${item.type || 'task'}-${item.id}`"
                :class="[
                  'flex items-center justify-between rounded-lg p-4',
                  item.type === 'content' ? 'bg-forest-700/50 border border-forest-600/30' :
                  item.type === 'goal' ? 'bg-forest-700/30 border border-forest-600/20' :
                  'bg-forest-700'
                ]"
              >
                <div class="flex items-center space-x-3">
                  <!-- Different indicators for each type -->
                  <div v-if="item.type === 'content'" :class="['w-4 h-4 rounded border-2 flex items-center justify-center', getContentColor()]">
                    <span v-if="item.stageCompletions && item.stageCompletions[item.status]" class="text-xs">✓</span>
                  </div>
                  <div v-else-if="item.type === 'goal'" :class="['w-4 h-4 rounded-full border-2 flex items-center justify-center', getGoalColor()]">
                    <span class="text-xs">🎯</span>
                  </div>
                  <input
                    v-else
                    :checked="item.completed"
                    @change="toggleTaskCompletion(item.id)"
                    type="checkbox"
                    class="h-4 w-4 rounded border-gray-300 text-orange-500 focus:ring-orange-500"
                  />

                  <div class="flex-1">
                    <div class="flex items-center space-x-2">
                      <span v-if="item.type === 'content'" class="text-sm">{{ item.pillar?.icon || '📄' }}</span>
                      <span v-else-if="item.type === 'goal'" class="text-sm">{{ item.icon || '🎯' }}</span>
                      <span v-else class="text-sm">📋</span>
                      <h4 :class="['font-medium', item.completed ? 'line-through text-gray-500' : 'text-white']">
                        {{ item.title }}
                      </h4>
                    </div>
                    <p class="text-sm text-gray-400">{{ item.description || (item.type === 'goal' ? `Target: ${item.target}` : '') }}</p>
                    <div class="flex items-center space-x-2 mt-1">
                      <span v-if="item.type === 'content'" :class="['text-xs px-2 py-1 rounded', getContentColor()]">
                        {{ getStageLabel(item.status) }}
                      </span>
                      <span v-else-if="item.type === 'goal'" :class="['text-xs px-2 py-1 rounded', getGoalColor()]">
                        {{ Math.round((item.current / item.target) * 100) }}% Complete
                      </span>
                      <span v-else :class="['text-xs px-2 py-1 rounded', getTaskColor()]">
                        {{ formatPriority(item.priority) }}
                      </span>
                      <span v-if="item.type === 'task'" class="text-xs text-gray-400">{{ formatCategory(item.category) }}</span>
                      <span v-if="item.type === 'content'" class="text-xs text-gray-400">
                        Due: {{ getCurrentStageDueDate(item) }}
                      </span>
                      <span v-if="item.type === 'goal'" class="text-xs text-gray-400">
                        Deadline: {{ new Date(item.deadline).toLocaleDateString() }}
                      </span>
                    </div>
                  </div>
                </div>
                <button
                  @click="item.type === 'content' ? openContentModal(item) : item.type === 'goal' ? openGoalModal(item) : editTask(item)"
                  class="text-gray-400 hover:text-white transition-colors p-2"
                >
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
                  </svg>
                </button>
              </div>

              <!-- Empty state -->
              <div v-if="getTasksForDate(selectedDate).length === 0" class="text-center py-8">
                <div class="text-gray-400 mb-4">
                  <svg class="h-12 w-12 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <p class="text-gray-400 mb-4">No tasks scheduled for this date</p>
                <button
                  @click="addTaskToSelectedDate"
                  class="rounded-lg bg-orange-500 px-4 py-2 text-sm text-white hover:bg-orange-600"
                >
                  + Add First Task
                </button>
              </div>
            </div>
          </div>

          <!-- Quick Stats -->
          <div class="rounded-xl bg-forest-800 p-6">
            <h3 class="text-lg font-semibold text-white mb-4">Quick Stats</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Total Tasks</span>
                <span class="text-white font-medium">{{ taskStats.total }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Completed</span>
                <span class="text-green-400 font-medium">{{ taskStats.completed }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">In Progress</span>
                <span class="text-yellow-400 font-medium">{{ taskStats.inProgress }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Overdue</span>
                <span class="text-red-400 font-medium">{{ taskStats.overdue }}</span>
              </div>
            </div>
          </div>
        </div>
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




      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useModals } from '../../composables/useModals.js'
import { useAnalyticsStore } from '../../stores/analytics'
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
const analyticsStore = useAnalyticsStore()

// Use modal composable
const { openTask, openGoal, openContent } = useModals()
console.log('🔥 Tasks page - using modal composable')

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
    image: '/optimized/Agent1.jpg',
    color: '#ea580c', // Orange
    description: 'AI Content Creator',
    personality: 'Professional & Analytical',
  },
  {
    id: 2,
    name: 'Agent 2',
    image: '/optimized/Agent2.jpg',
    color: '#eab308', // Yellow
    description: 'Marketing Specialist',
    personality: 'Strategic & Data-Driven',
  },
  {
    id: 3,
    name: 'Agent 3',
    image: '/optimized/Agent3.jpg',
    color: '#16a34a', // Green
    description: 'Analytics Expert',
    personality: 'Detail-Oriented & Insightful',
  },
  {
    id: 4,
    name: 'Agent 4',
    image: '/optimized/Agent4.jpg',
    color: '#ea580c', // Orange
    description: 'Creative Assistant',
    personality: 'Innovative & Artistic',
  },
  {
    id: 5,
    name: 'Agent 5',
    image: '/optimized/Agent5.jpg',
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
  openTask(task)
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

// Calendar functionality
const currentDate = ref(new Date())
const selectedDate = ref<Date | null>(null)

const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const currentMonthYear = computed(() => {
  return currentDate.value.toLocaleDateString('en-US', {
    month: 'long',
    year: 'numeric'
  })
})

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()

  // First day of the month
  const firstDay = new Date(year, month, 1)
  // Last day of the month
  const lastDay = new Date(year, month + 1, 0)

  // Start from the first Sunday of the calendar view
  const startDate = new Date(firstDay)
  startDate.setDate(startDate.getDate() - startDate.getDay())

  // End at the last Saturday of the calendar view
  const endDate = new Date(lastDay)
  endDate.setDate(endDate.getDate() + (6 - endDate.getDay()))

  const days = []
  const currentDateObj = new Date(startDate)

  while (currentDateObj <= endDate) {
    const today = new Date()
    days.push({
      date: new Date(currentDateObj),
      isCurrentMonth: currentDateObj.getMonth() === month,
      isToday: currentDateObj.toDateString() === today.toDateString(),
    })
    currentDateObj.setDate(currentDateObj.getDate() + 1)
  }

  return days
})

const previousMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1)
}

const nextMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1)
}

const goToToday = () => {
  currentDate.value = new Date()
  selectedDate.value = new Date()
}

const selectDate = (date: Date) => {
  selectedDate.value = date
}

const addTaskToDate = (date: Date) => {
  selectedDate.value = date
  showCreateModal.value = true
}

const addTaskToSelectedDate = () => {
  if (selectedDate.value) {
    showCreateModal.value = true
  }
}

// Content items data (imported from Content Studio)
const contentItems = ref([
  // Ideas
  {
    id: 1,
    title: 'YouTube Shorts Strategy Guide',
    description: 'Create a comprehensive guide on YouTube Shorts best practices',
    status: 'ideas',
    priority: 'high',
    assignee: 'M',
    createdAt: '2023-12-15',
    dueDate: '2024-01-15',
    stageDueDates: {
      ideas: '2025-08-25',
      planning: '2025-08-28',
      'in-progress': '2025-09-02',
      published: '2025-09-05'
    },
    stageCompletions: {
      ideas: false,
      planning: false,
      'in-progress': false,
      published: false
    },
    pillar: { id: 1, name: 'Marketing', icon: '📈' },
    type: 'content'
  },
  {
    id: 2,
    title: 'AI Content Creation Tools Review',
    description: 'Review and compare top AI tools for content creators',
    status: 'ideas',
    priority: 'medium',
    assignee: 'M',
    createdAt: '2023-12-14',
    dueDate: '2024-01-20',
    stageDueDates: {
      ideas: '2025-08-26',
      planning: '2025-08-29',
      'in-progress': '2025-09-03',
      published: '2025-09-06'
    },
    stageCompletions: {
      ideas: false,
      planning: false,
      'in-progress': false,
      published: false
    },
    pillar: { id: 2, name: 'Technology', icon: '💻' },
    type: 'content'
  },
  // Planning
  {
    id: 4,
    title: 'Content Calendar Template',
    description: 'Design a comprehensive content calendar template',
    status: 'planning',
    priority: 'high',
    assignee: 'M',
    createdAt: '2023-12-12',
    dueDate: '2024-01-10',
    stageDueDates: {
      ideas: '2025-08-20',
      planning: '2025-08-23',
      'in-progress': '2025-08-27',
      published: '2025-08-30'
    },
    stageCompletions: {
      ideas: true,
      planning: false,
      'in-progress': false,
      published: false
    },
    pillar: { id: 3, name: 'Content Strategy', icon: '📝' },
    type: 'content'
  },
  // In Progress
  {
    id: 6,
    title: 'Video Editing Masterclass',
    description: 'Complete tutorial series on advanced video editing',
    status: 'in-progress',
    priority: 'high',
    assignee: 'M',
    progress: 75,
    createdAt: '2023-12-10',
    dueDate: '2024-01-05',
    stageDueDates: {
      ideas: '2025-08-15',
      planning: '2025-08-20',
      'in-progress': '2025-08-24',
      published: '2025-08-28'
    },
    stageCompletions: {
      ideas: true,
      planning: true,
      'in-progress': false,
      published: false
    },
    pillar: { id: 2, name: 'Technology', icon: '💻' },
    type: 'content'
  },
  // Published
  {
    id: 8,
    title: 'TikTok Algorithm Secrets',
    description: 'Deep dive into how TikTok algorithm works in 2024',
    status: 'published',
    priority: 'high',
    assignee: 'M',
    publishDate: 'Dec 8, 2023',
    createdAt: '2023-12-08',
    dueDate: '2023-12-08',
    stageDueDates: {
      ideas: '2025-08-10',
      planning: '2025-08-15',
      'in-progress': '2025-08-20',
      published: '2025-08-22'
    },
    stageCompletions: {
      ideas: true,
      planning: true,
      'in-progress': true,
      published: true
    },
    pillar: { id: 1, name: 'Marketing', icon: '📈' },
    type: 'content'
  }
])

// Function to get the current stage due date for content items
const getCurrentStageDueDate = (item: any) => {
  if (!item.stageDueDates || !item.status) return item.dueDate

  // Find the current stage that should be worked on
  const stageOrder = ['ideas', 'planning', 'in-progress', 'published']
  const currentStageIndex = stageOrder.indexOf(item.status)

  // If current stage is completed, move to next stage
  if (item.stageCompletions && item.stageCompletions[item.status]) {
    const nextStageIndex = currentStageIndex + 1
    if (nextStageIndex < stageOrder.length) {
      const nextStage = stageOrder[nextStageIndex]
      return item.stageDueDates[nextStage] || item.dueDate
    }
  }

  // Return current stage due date
  return item.stageDueDates[item.status] || item.dueDate
}

const getTasksForDate = (date: Date) => {
  // Get regular tasks
  const tasks = tasksStore.tasks.filter(task => {
    const taskDate = new Date(task.dueDate)
    return (
      taskDate.getDate() === date.getDate() &&
      taskDate.getMonth() === date.getMonth() &&
      taskDate.getFullYear() === date.getFullYear()
    )
  }).map(task => ({ ...task, type: 'task' }))

  // Get content items for this date based on their current stage due date
  const contentForDate = contentItems.value.filter(item => {
    const itemDate = new Date(getCurrentStageDueDate(item))
    return (
      itemDate.getDate() === date.getDate() &&
      itemDate.getMonth() === date.getMonth() &&
      itemDate.getFullYear() === date.getFullYear()
    )
  })

  // Get goals for this date based on their deadline
  const goalsForDate = analyticsStore.goals.filter(goal => {
    const goalDate = new Date(goal.deadline)
    return (
      goalDate.getDate() === date.getDate() &&
      goalDate.getMonth() === date.getMonth() &&
      goalDate.getFullYear() === date.getFullYear()
    )
  }).map(goal => ({ ...goal, type: 'goal' }))

  // Combine tasks, content items, and goals
  return [...tasks, ...contentForDate, ...goalsForDate]
}

// Content-specific helper functions
const getContentColor = () => {
  return 'bg-blue-500/20 border border-blue-500/40 text-blue-300'
}

const getStageLabel = (status: string) => {
  switch (status) {
    case 'ideas':
      return 'Ideas'
    case 'planning':
      return 'Planning'
    case 'in-progress':
      return 'In Progress'
    case 'published':
      return 'Published'
    default:
      return status
  }
}

const openContentModal = (item: any) => {
  openContent(item)
}

// Goal-specific helper functions
const getGoalColor = () => {
  return 'bg-green-500/20 border border-green-500/40 text-green-300'
}

// Task-specific helper functions
const getTaskColor = () => {
  return 'bg-orange-500/20 border border-orange-500/40 text-orange-300'
}

const openGoalModal = (goal: any) => {
  openGoal(goal)
}

const formatDate = (date: Date) => {
  return date.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getPriorityColor = (priority: TaskPriority) => {
  switch (priority) {
    case 'urgent': return 'bg-red-500 text-white'
    case 'high': return 'bg-orange-500 text-white'
    case 'medium': return 'bg-yellow-500 text-black'
    case 'low': return 'bg-green-500 text-white'
    default: return 'bg-forest-600 text-white'
  }
}

const addSuggestionAsTask = (suggestion: any) => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)

  tasksStore.addTask({
    title: suggestion.title,
    description: suggestion.description,
    priority: suggestion.priority,
    category: suggestion.category,
    dueDate: selectedDate.value || tomorrow,
    estimatedTime: suggestion.estimatedTime,
    tags: ['ai-suggested'],
  })

  dismissSuggestion(suggestion.id)
}
</script>

<style scoped>
.transition-colors {
  transition: background-color 0.2s ease-in-out;
}
</style>
