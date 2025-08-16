<template>
  <div class="space-y-6">
    <!-- Productivity Overview -->
    <VCard>
      <template #header>
        <h3 class="text-lg font-semibold">Productivity Overview</h3>
      </template>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Today -->
        <div class="text-center">
          <div class="text-3xl font-bold text-agent-3 mb-2">
            {{ productivityStats.today.completed }}
          </div>
          <div class="text-sm text-text-muted mb-1">Tasks Completed Today</div>
          <div class="text-xs text-text-secondary">
            {{ productivityStats.today.created }} created
          </div>
        </div>

        <!-- This Week -->
        <div class="text-center">
          <div class="text-3xl font-bold text-agent-2 mb-2">
            {{ productivityStats.thisWeek.completed }}
          </div>
          <div class="text-sm text-text-muted mb-1">This Week</div>
          <div class="text-xs text-text-secondary">
            {{ productivityStats.thisWeek.created }} created
          </div>
        </div>

        <!-- This Month -->
        <div class="text-center">
          <div class="text-3xl font-bold text-agent-1 mb-2">
            {{ productivityStats.thisMonth.completed }}
          </div>
          <div class="text-sm text-text-muted mb-1">This Month</div>
          <div class="text-xs text-text-secondary">
            {{ productivityStats.thisMonth.created }} created
          </div>
        </div>
      </div>
    </VCard>

    <!-- Quick Actions -->
    <VCard>
      <template #header>
        <h3 class="text-lg font-semibold">Quick Actions</h3>
      </template>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <button
          v-for="action in quickActions"
          :key="action.name"
          class="p-4 rounded-lg border border-border hover:border-border-light transition-all hover:scale-105"
          :style="{ backgroundColor: action.color + '20' }"
          @click="action.handler"
        >
          <div class="text-2xl mb-2">{{ action.icon }}</div>
          <div class="font-medium text-text-primary">{{ action.name }}</div>
          <div class="text-sm text-text-muted">{{ action.description }}</div>
        </button>
      </div>
    </VCard>

    <!-- Upcoming Tasks -->
    <VCard v-if="upcomingTasks.length > 0">
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold">Upcoming Tasks</h3>
          <VButton variant="ghost" size="sm" @click="$emit('view-all')">
            View All
          </VButton>
        </div>
      </template>

      <div class="space-y-3">
        <div
          v-for="task in upcomingTasks.slice(0, 5)"
          :key="task.id"
          class="flex items-center justify-between p-3 rounded-lg bg-background-elevated hover:bg-background-card transition-colors cursor-pointer"
          @click="$emit('edit-task', task)"
        >
          <div class="flex items-center space-x-3">
            <input
              :checked="task.completed"
              type="checkbox"
              class="rounded border-border bg-background-elevated text-agent-3 focus:ring-agent-3"
              @click.stop
              @change="toggleTaskCompletion(task.id)"
            />
            <div>
              <div class="font-medium text-text-primary">{{ task.title }}</div>
              <div class="text-sm text-text-muted">
                {{ formatCategory(task.category) }} • {{ formatPriority(task.priority) }}
              </div>
            </div>
          </div>
          <div class="text-right">
            <VBadge :variant="getPriorityVariant(task.priority)" size="sm">
              {{ formatDueDate(task.dueDate) }}
            </VBadge>
          </div>
        </div>
      </div>
    </VCard>

    <!-- Task Categories -->
    <VCard>
      <template #header>
        <h3 class="text-lg font-semibold">Tasks by Category</h3>
      </template>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div
          v-for="(tasks, category) in tasksByCategory"
          :key="category"
          class="p-4 rounded-lg bg-background-elevated"
        >
          <div class="flex items-center justify-between mb-3">
            <h4 class="font-medium text-text-primary">
              {{ formatCategory(category) }}
            </h4>
            <VBadge variant="secondary" size="sm">
              {{ tasks.length }}
            </VBadge>
          </div>
          
          <div class="space-y-2">
            <div class="flex justify-between text-sm">
              <span class="text-text-muted">Completed</span>
              <span class="text-agent-3">
                {{ tasks.filter(t => t.completed).length }}
              </span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-text-muted">Pending</span>
              <span class="text-agent-4">
                {{ tasks.filter(t => !t.completed).length }}
              </span>
            </div>
            
            <!-- Progress Bar -->
            <div class="w-full bg-background-card rounded-full h-2 mt-3">
              <div
                class="bg-agent-3 h-2 rounded-full transition-all duration-300"
                :style="{ width: `${getCategoryProgress(tasks)}%` }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </VCard>

    <!-- Recent Activity -->
    <VCard v-if="recentTasks.length > 0">
      <template #header>
        <h3 class="text-lg font-semibold">Recent Activity</h3>
      </template>

      <div class="space-y-3">
        <div
          v-for="task in recentTasks.slice(0, 5)"
          :key="task.id"
          class="flex items-center space-x-3 p-3 rounded-lg bg-background-elevated"
        >
          <div 
            class="w-8 h-8 rounded-lg flex items-center justify-center text-xs"
            :style="{ backgroundColor: getCategoryColor(task.category) + '40' }"
          >
            {{ getCategoryIcon(task.category) }}
          </div>
          <div class="flex-1">
            <div class="font-medium text-text-primary">{{ task.title }}</div>
            <div class="text-sm text-text-muted">
              Created {{ formatRelativeTime(task.createdAt) }}
            </div>
          </div>
          <VBadge :variant="getStatusVariant(task.status)" size="sm">
            {{ formatStatus(task.status) }}
          </VBadge>
        </div>
      </div>
    </VCard>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useTasksStore } from '../../stores/tasks'
import type { Task, TaskCategory, TaskPriority, TaskStatus } from '../../types/tasks'

const emit = defineEmits<{
  'view-all': []
  'edit-task': [task: Task]
  'create-task': [category?: TaskCategory]
}>()

const tasksStore = useTasksStore()

// Computed properties
const upcomingTasks = computed(() => tasksStore.upcomingTasks)
const recentTasks = computed(() => tasksStore.recentTasks)
const tasksByCategory = computed(() => tasksStore.tasksByCategory)
const productivityStats = computed(() => tasksStore.getProductivityStats())

// Quick actions
const quickActions = [
  {
    name: 'Content Task',
    description: 'Create content',
    icon: '📝',
    color: '#9333ea',
    handler: () => emit('create-task', 'content')
  },
  {
    name: 'SEO Task',
    description: 'Optimize SEO',
    icon: '🔍',
    color: '#059669',
    handler: () => emit('create-task', 'seo')
  },
  {
    name: 'Analytics',
    description: 'Review metrics',
    icon: '📊',
    color: '#2563eb',
    handler: () => emit('create-task', 'analytics')
  },
  {
    name: 'Marketing',
    description: 'Promote content',
    icon: '📢',
    color: '#ea580c',
    handler: () => emit('create-task', 'marketing')
  },
]

// Methods
const toggleTaskCompletion = (taskId: string) => {
  tasksStore.toggleTaskCompletion(taskId)
}

const formatCategory = (category: string) => {
  return category.charAt(0).toUpperCase() + category.slice(1).replace('_', ' ')
}

const formatPriority = (priority: TaskPriority) => {
  return priority.charAt(0).toUpperCase() + priority.slice(1)
}

const formatStatus = (status: TaskStatus) => {
  return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const getPriorityVariant = (priority: TaskPriority) => {
  switch (priority) {
    case 'urgent': return 'error'
    case 'high': return 'warning'
    case 'medium': return 'primary'
    case 'low': return 'secondary'
    default: return 'secondary'
  }
}

const getStatusVariant = (status: TaskStatus) => {
  switch (status) {
    case 'completed': return 'success'
    case 'in_progress': return 'warning'
    case 'cancelled': return 'error'
    case 'on_hold': return 'secondary'
    default: return 'secondary'
  }
}

const getCategoryProgress = (tasks: Task[]) => {
  if (tasks.length === 0) return 0
  const completed = tasks.filter(t => t.completed).length
  return Math.round((completed / tasks.length) * 100)
}

const getCategoryColor = (category: TaskCategory) => {
  const colors = {
    content: '#9333ea',
    marketing: '#ea580c',
    analytics: '#2563eb',
    seo: '#059669',
    monetization: '#db2777',
    community: '#7c3aed',
    planning: '#0891b2',
    research: '#dc2626',
    general: '#6b7280',
  }
  return colors[category] || colors.general
}

const getCategoryIcon = (category: TaskCategory) => {
  const icons = {
    content: '📝',
    marketing: '📢',
    analytics: '📊',
    seo: '🔍',
    monetization: '💰',
    community: '👥',
    planning: '📋',
    research: '🔬',
    general: '⚡',
  }
  return icons[category] || icons.general
}

const formatDueDate = (date: Date) => {
  const now = new Date()
  const dueDate = new Date(date)
  const diffTime = dueDate.getTime() - now.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Tomorrow'
  if (diffDays === -1) return 'Yesterday'
  if (diffDays < 0) return `${Math.abs(diffDays)}d overdue`
  if (diffDays <= 7) return `${diffDays}d`
  
  return dueDate.toLocaleDateString()
}

const formatRelativeTime = (date: Date) => {
  const now = new Date()
  const diffTime = now.getTime() - new Date(date).getTime()
  const diffMinutes = Math.floor(diffTime / (1000 * 60))
  const diffHours = Math.floor(diffMinutes / 60)
  const diffDays = Math.floor(diffHours / 24)

  if (diffMinutes < 1) return 'just now'
  if (diffMinutes < 60) return `${diffMinutes}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  
  return new Date(date).toLocaleDateString()
}
</script>

<style scoped>
.transition-all {
  transition: all 0.2s ease-in-out;
}
</style>
