<template>
  <div class="space-y-6">
    <!-- Task Manager Header -->
    <VCard>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold">Task Manager</h3>
            <p class="text-sm text-text-muted">
              {{ taskStats.total }} tasks • {{ taskStats.completed }} completed • {{ taskStats.completionRate }}% completion rate
            </p>
          </div>
          <VButton variant="primary" @click="showCreateModal = true">
            ➕ Add Task
          </VButton>
        </div>
      </template>

      <!-- Task Stats -->
      <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div class="text-center">
          <div class="text-2xl font-bold text-text-primary">{{ taskStats.total }}</div>
          <div class="text-sm text-text-muted">Total</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-agent-3">{{ taskStats.completed }}</div>
          <div class="text-sm text-text-muted">Completed</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-agent-1">{{ taskStats.inProgress }}</div>
          <div class="text-sm text-text-muted">In Progress</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-agent-4">{{ taskStats.pending }}</div>
          <div class="text-sm text-text-muted">Pending</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-error">{{ taskStats.overdue }}</div>
          <div class="text-sm text-text-muted">Overdue</div>
        </div>
      </div>
    </VCard>

    <!-- Filters and Search -->
    <VCard>
      <div class="space-y-4">
        <!-- Search Bar -->
        <div class="flex items-center space-x-4">
          <VInput
            v-model="searchQuery"
            placeholder="Search tasks..."
            class="flex-1"
          >
            <template #icon-left>
              <span class="text-text-muted">🔍</span>
            </template>
          </VInput>
          <VButton variant="ghost" @click="clearFilters">
            Clear Filters
          </VButton>
        </div>

        <!-- Filter Buttons -->
        <div class="flex flex-wrap gap-2">
          <VButton
            v-for="filter in filterOptions"
            :key="filter.value"
            :variant="activeFilter === filter.value ? 'primary' : 'secondary'"
            size="sm"
            @click="setActiveFilter(filter.value)"
          >
            {{ filter.label }}
          </VButton>
        </div>

        <!-- Advanced Filters -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Category Filter -->
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-2">Category</label>
            <select
              v-model="selectedCategory"
              class="input w-full"
            >
              <option value="all">All Categories</option>
              <option v-for="category in categoryOptions" :key="category" :value="category">
                {{ formatCategory(category) }}
              </option>
            </select>
          </div>

          <!-- Priority Filter -->
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-2">Priority</label>
            <select
              v-model="selectedPriority"
              class="input w-full"
            >
              <option value="all">All Priorities</option>
              <option v-for="priority in priorityOptions" :key="priority" :value="priority">
                {{ formatPriority(priority) }}
              </option>
            </select>
          </div>

          <!-- Sort Options -->
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-2">Sort By</label>
            <select
              v-model="sortBy"
              class="input w-full"
              @change="setSortBy(sortBy)"
            >
              <option value="dueDate">Due Date</option>
              <option value="priority">Priority</option>
              <option value="createdAt">Created Date</option>
              <option value="title">Title</option>
            </select>
          </div>
        </div>

        <!-- Show/Hide Completed -->
        <div class="flex items-center space-x-2">
          <input
            id="showCompleted"
            v-model="showCompleted"
            type="checkbox"
            class="rounded border-border bg-background-elevated text-brand-primary focus:ring-brand-primary"
          />
          <label for="showCompleted" class="text-sm text-text-secondary">
            Show completed tasks
          </label>
        </div>
      </div>
    </VCard>

    <!-- Task List -->
    <VCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h4 class="font-semibold">
            Tasks ({{ filteredTasks.length }})
          </h4>
          <div class="flex items-center space-x-2">
            <VButton
              v-if="selectedTasks.length > 0"
              variant="secondary"
              size="sm"
              @click="bulkComplete"
            >
              ✅ Complete Selected ({{ selectedTasks.length }})
            </VButton>
            <VButton
              v-if="selectedTasks.length > 0"
              variant="ghost"
              size="sm"
              @click="bulkDelete"
            >
              🗑️ Delete Selected
            </VButton>
          </div>
        </div>
      </template>

      <div v-if="filteredTasks.length === 0" class="text-center py-8">
        <div class="text-text-muted mb-4">
          <span class="text-4xl">📝</span>
        </div>
        <h5 class="text-lg font-medium text-text-primary mb-2">No tasks found</h5>
        <p class="text-text-muted mb-4">
          {{ searchQuery ? 'Try adjusting your search or filters' : 'Create your first task to get started' }}
        </p>
        <VButton variant="primary" @click="showCreateModal = true">
          Create Task
        </VButton>
      </div>

      <div v-else class="space-y-3">
        <div
          v-for="task in filteredTasks"
          :key="task.id"
          class="task-item p-4 rounded-lg border border-border hover:border-border-light transition-colors"
          :class="{
            'bg-background-elevated': !task.completed,
            'bg-background-card opacity-75': task.completed,
            'border-error': isOverdue(task),
            'border-warning': isDueToday(task),
          }"
        >
          <div class="flex items-start space-x-3">
            <!-- Checkbox -->
            <input
              v-model="selectedTasks"
              :value="task.id"
              type="checkbox"
              class="mt-1 rounded border-border bg-background-elevated text-brand-primary focus:ring-brand-primary"
            />

            <!-- Task Checkbox -->
            <input
              :checked="task.completed"
              type="checkbox"
              class="mt-1 rounded border-border bg-background-elevated text-agent-3 focus:ring-agent-3"
              @change="toggleTaskCompletion(task.id)"
            />

            <!-- Task Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <h5 
                    class="font-medium"
                    :class="task.completed ? 'line-through text-text-muted' : 'text-text-primary'"
                  >
                    {{ task.title }}
                  </h5>
                  <p 
                    v-if="task.description"
                    class="text-sm mt-1"
                    :class="task.completed ? 'text-text-muted' : 'text-text-secondary'"
                  >
                    {{ task.description }}
                  </p>
                </div>

                <!-- Task Actions -->
                <div class="flex items-center space-x-2 ml-4">
                  <VButton variant="ghost" size="sm" @click="editTask(task)">
                    ✏️
                  </VButton>
                  <VButton variant="ghost" size="sm" @click="duplicateTask(task.id)">
                    📋
                  </VButton>
                  <VButton variant="ghost" size="sm" @click="deleteTask(task.id)">
                    🗑️
                  </VButton>
                </div>
              </div>

              <!-- Task Meta -->
              <div class="flex items-center justify-between mt-3">
                <div class="flex items-center space-x-4">
                  <!-- Priority Badge -->
                  <VBadge :variant="getPriorityVariant(task.priority)" size="sm">
                    {{ formatPriority(task.priority) }}
                  </VBadge>

                  <!-- Category Badge -->
                  <VBadge variant="secondary" size="sm">
                    {{ formatCategory(task.category) }}
                  </VBadge>

                  <!-- Tags -->
                  <div v-if="task.tags.length > 0" class="flex items-center space-x-1">
                    <VBadge
                      v-for="tag in task.tags.slice(0, 2)"
                      :key="tag"
                      variant="secondary"
                      size="sm"
                    >
                      {{ tag }}
                    </VBadge>
                    <span v-if="task.tags.length > 2" class="text-xs text-text-muted">
                      +{{ task.tags.length - 2 }}
                    </span>
                  </div>
                </div>

                <!-- Due Date -->
                <div class="text-sm">
                  <span 
                    :class="{
                      'text-error': isOverdue(task),
                      'text-warning': isDueToday(task),
                      'text-text-muted': !isOverdue(task) && !isDueToday(task),
                    }"
                  >
                    {{ formatDueDate(task.dueDate) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </VCard>

    <!-- Create/Edit Task Modal -->
    <TaskModal
      v-if="showCreateModal || editingTask"
      :task="editingTask"
      @close="closeModal"
      @save="saveTask"
      @delete="handleDeleteTask"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useTasksStore } from '../../stores/tasks'
import type { Task, TaskCategory, TaskFilter, TaskPriority } from '../../types/tasks'

const tasksStore = useTasksStore()

// Local state
const showCreateModal = ref(false)
const editingTask = ref<Task | null>(null)
const selectedTasks = ref<string[]>([])

// Computed properties from store
const filteredTasks = computed(() => tasksStore.filteredTasks)
const taskStats = computed(() => tasksStore.taskStats)
const activeFilter = computed(() => tasksStore.activeFilter)
const searchQuery = computed({
  get: () => tasksStore.searchQuery,
  set: (value) => tasksStore.setSearchQuery(value)
})
const selectedCategory = computed({
  get: () => tasksStore.selectedCategory,
  set: (value) => tasksStore.setSelectedCategory(value)
})
const selectedPriority = computed({
  get: () => tasksStore.selectedPriority,
  set: (value) => tasksStore.setSelectedPriority(value)
})
const showCompleted = computed({
  get: () => tasksStore.showCompleted,
  set: () => tasksStore.toggleShowCompleted()
})
const sortBy = computed({
  get: () => tasksStore.sortBy,
  set: (value) => tasksStore.setSortBy(value)
})

// Filter options
const filterOptions = [
  { label: 'All', value: 'all' as TaskFilter },
  { label: 'Pending', value: 'pending' as TaskFilter },
  { label: 'In Progress', value: 'in_progress' as TaskFilter },
  { label: 'Completed', value: 'completed' as TaskFilter },
  { label: 'High Priority', value: 'high_priority' as TaskFilter },
  { label: 'Due Today', value: 'due_today' as TaskFilter },
  { label: 'Overdue', value: 'overdue' as TaskFilter },
]

const categoryOptions: TaskCategory[] = [
  'content', 'marketing', 'analytics', 'seo', 'monetization', 
  'community', 'planning', 'research', 'general'
]

const priorityOptions: TaskPriority[] = ['urgent', 'high', 'medium', 'low']

// Methods
const setActiveFilter = (filter: TaskFilter) => {
  tasksStore.setActiveFilter(filter)
}

const setSortBy = (field: any) => {
  tasksStore.setSortBy(field)
}

const clearFilters = () => {
  tasksStore.clearFilters()
  selectedTasks.value = []
}

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

const handleDeleteTask = (taskId: string) => {
  console.log('🗑️ TaskManager: handleDeleteTask called with ID:', taskId)
  tasksStore.deleteTask(taskId)
  closeModal() // Close the modal after deletion
}

const bulkComplete = () => {
  tasksStore.markTasksAsCompleted(selectedTasks.value)
  selectedTasks.value = []
}

const bulkDelete = () => {
  if (confirm(`Delete ${selectedTasks.value.length} selected tasks?`)) {
    tasksStore.bulkDeleteTasks(selectedTasks.value)
    selectedTasks.value = []
  }
}

// Utility functions
const formatCategory = (category: string) => {
  return category.charAt(0).toUpperCase() + category.slice(1).replace('_', ' ')
}

const formatPriority = (priority: string) => {
  return priority.charAt(0).toUpperCase() + priority.slice(1)
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
  if (diffDays < 0) return `${Math.abs(diffDays)} days overdue`
  if (diffDays <= 7) return `Due in ${diffDays} days`
  
  return dueDate.toLocaleDateString()
}
</script>

<style scoped>
.task-item {
  transition: all 0.2s ease-in-out;
}

.task-item:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}
</style>
