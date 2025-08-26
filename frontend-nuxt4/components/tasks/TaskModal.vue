<template>
  <div class="fixed inset-0 z-[60] flex items-center justify-center">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black bg-opacity-50" @click="$emit('close')" />

    <!-- Modal -->
    <div class="relative bg-background-card rounded-xl shadow-xl w-full max-w-2xl mx-4 my-8 max-h-[calc(100vh-8rem)] overflow-y-auto">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-border">
        <h3 class="text-lg font-semibold text-text-primary">
          {{ task ? 'Edit Task' : 'Create New Task' }}
        </h3>
        <button
          class="text-text-muted hover:text-text-primary transition-colors"
          @click="$emit('close')"
        >
          ✕
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
        <!-- Title -->
        <div>
          <label class="block text-sm font-medium text-text-secondary mb-2">
            Title *
          </label>
          <VInput
            v-model="form.title"
            placeholder="Enter task title..."
            required
            :error="errors.title"
          />
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-text-secondary mb-2">
            Description
          </label>
          <textarea
            v-model="form.description"
            placeholder="Enter task description..."
            rows="3"
            class="input w-full resize-none"
          />
        </div>

        <!-- Notes -->
        <div>
          <label class="block text-sm font-medium text-text-secondary mb-2">
            Notes
          </label>
          <textarea
            v-model="form.notes"
            placeholder="Add personal notes for this task..."
            rows="4"
            class="input w-full resize-none"
          />
        </div>

        <!-- Priority and Category -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-2">
              Priority *
            </label>
            <select v-model="form.priority" class="input w-full" required>
              <option value="">Select priority</option>
              <option value="urgent">🔴 Urgent</option>
              <option value="high">🟠 High</option>
              <option value="medium">🟡 Medium</option>
              <option value="low">🟢 Low</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-text-secondary mb-2">
              Category *
            </label>
            <select v-model="form.category" class="input w-full" required>
              <option value="">Select category</option>
              <option value="content">📝 Content</option>
              <option value="marketing">📢 Marketing</option>
              <option value="analytics">📊 Analytics</option>
              <option value="seo">🔍 SEO</option>
              <option value="monetization">💰 Monetization</option>
              <option value="community">👥 Community</option>
              <option value="planning">📋 Planning</option>
              <option value="research">🔬 Research</option>
              <option value="general">⚡ General</option>
            </select>
          </div>
        </div>

        <!-- Due Date and Estimated Time -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-2">
              Due Date *
            </label>
            <input
              v-model="form.dueDate"
              type="date"
              class="input w-full"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-text-secondary mb-2">
              Estimated Time (minutes)
            </label>
            <VInput
              v-model="form.estimatedTime"
              type="number"
              placeholder="60"
              min="1"
            />
          </div>
        </div>



        <!-- Tags -->
        <div>
          <label class="block text-sm font-medium text-text-secondary mb-2">
            Tags
          </label>
          <div class="space-y-2">
            <VInput
              v-model="newTag"
              placeholder="Add a tag..."
              @keyup.enter="addTag"
            >
              <template #icon-right>
                <button
                  type="button"
                  class="text-brand-primary hover:text-brand-600 transition-colors"
                  @click="addTag"
                >
                  ➕
                </button>
              </template>
            </VInput>
            
            <div v-if="form.tags.length > 0" class="flex flex-wrap gap-2">
              <VBadge
                v-for="(tag, index) in form.tags"
                :key="index"
                variant="secondary"
                class="cursor-pointer"
                @click="removeTag(index)"
              >
                {{ tag }} ✕
              </VBadge>
            </div>
          </div>
        </div>

        <!-- Status (only for editing) -->
        <div v-if="task">
          <label class="block text-sm font-medium text-text-secondary mb-2">
            Status
          </label>
          <select v-model="form.status" class="input w-full">
            <option value="pending">📋 Pending</option>
            <option value="in_progress">⏳ In Progress</option>
            <option value="completed">✅ Completed</option>
            <option value="cancelled">❌ Cancelled</option>
            <option value="on_hold">⏸️ On Hold</option>
          </select>
        </div>

        <!-- Quick Templates -->
        <div v-if="!task">
          <label class="block text-sm font-medium text-text-secondary mb-2">
            Quick Templates
          </label>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
            <button
              v-for="template in taskTemplates"
              :key="template.name"
              type="button"
              class="p-3 text-left rounded-lg border border-border hover:border-border-light transition-colors"
              @click="applyTemplate(template)"
            >
              <div class="font-medium text-text-primary">{{ template.name }}</div>
              <div class="text-sm text-text-muted">{{ template.description }}</div>
            </button>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-end space-x-3 pt-4 border-t border-border">
          <VButton variant="ghost" @click="$emit('close')">
            Cancel
          </VButton>
          <VButton variant="primary" type="submit" :disabled="!isFormValid">
            {{ task ? 'Update Task' : 'Create Task' }}
          </VButton>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { CreateTaskRequest, Task, TaskCategory, TaskPriority, TaskStatus } from '../../types/tasks'
import VBadge from '../ui/VBadge.vue'
import VButton from '../ui/VButton.vue'
import VInput from '../ui/VInput.vue'

interface Props {
  task?: Task | null
}

const props = defineProps<Props>()
const emit = defineEmits<{
  close: []
  save: [taskData: CreateTaskRequest]
}>()

// Form state
const form = ref({
  title: '',
  description: '',
  priority: '' as TaskPriority | '',
  category: '' as TaskCategory | '',
  dueDate: '',
  estimatedTime: '',
  tags: [] as string[],
  status: 'pending' as TaskStatus,
  notes: '',
})

const newTag = ref('')
const errors = ref({
  title: '',
  dueDate: '',
})

// Task templates
const taskTemplates = [
  {
    name: 'Content Creation',
    description: 'Create new video content',
    template: {
      title: 'Create new video content',
      description: 'Plan, script, and produce new video content',
      priority: 'medium' as TaskPriority,
      category: 'content' as TaskCategory,
      tags: ['video', 'content'],
      estimatedTime: 120,
    }
  },
  {
    name: 'SEO Optimization',
    description: 'Optimize content for search',
    template: {
      title: 'Optimize content for SEO',
      description: 'Research keywords and optimize content for better discoverability',
      priority: 'high' as TaskPriority,
      category: 'seo' as TaskCategory,
      tags: ['seo', 'keywords'],
      estimatedTime: 60,
    }
  },
  {
    name: 'Analytics Review',
    description: 'Review performance metrics',
    template: {
      title: 'Review analytics and metrics',
      description: 'Analyze channel performance and identify improvement opportunities',
      priority: 'medium' as TaskPriority,
      category: 'analytics' as TaskCategory,
      tags: ['analytics', 'metrics'],
      estimatedTime: 45,
    }
  },
  {
    name: 'Community Engagement',
    description: 'Engage with audience',
    template: {
      title: 'Engage with community',
      description: 'Respond to comments and engage with audience',
      priority: 'low' as TaskPriority,
      category: 'community' as TaskCategory,
      tags: ['community', 'engagement'],
      estimatedTime: 30,
    }
  },
]

// Form validation
const isFormValid = computed(() => {
  const valid = form.value.title.trim() &&
                form.value.priority &&
                form.value.category &&
                form.value.dueDate

  console.log('🔍 TaskModal: isFormValid check:', {
    title: !!form.value.title.trim(),
    priority: !!form.value.priority,
    category: !!form.value.category,
    dueDate: !!form.value.dueDate,
    overall: valid
  })

  return valid
})

// Helper to format date for input
const formatDateForInput = (date: Date | string) => {
  const d = new Date(date)
  return d.toISOString().split('T')[0]
}

// Initialize form with task data if editing
watch(() => props.task, (task) => {
  console.log('🔄 TaskModal: Initializing form with task:', task)

  if (task) {
    const formattedDate = formatDateForInput(task.dueDate)
    console.log('📅 TaskModal: Formatting existing date:', task.dueDate, '→', formattedDate)
    console.log('🔍 TaskModal: Task data received:', {
      id: task.id,
      title: task.title,
      estimatedTime: task.estimatedTime,
      estimatedTimeType: typeof task.estimatedTime,
      tags: task.tags,
      isInsightTask: task.tags?.includes('levi-insight')
    })

    form.value = {
      title: task.title,
      description: task.description,
      priority: task.priority,
      category: task.category,
      dueDate: formattedDate,
      estimatedTime: typeof task.estimatedTime === 'number' ? task.estimatedTime.toString() : (task.estimatedTime || ''),
      tags: [...task.tags],
      status: task.status,
      notes: task.notes || '',
    }
  } else {
    // Reset form for new task
    const tomorrow = new Date()
    tomorrow.setDate(tomorrow.getDate() + 1)
    const tomorrowFormatted = formatDateForInput(tomorrow)
    console.log('📅 TaskModal: Setting default date to tomorrow:', tomorrowFormatted)

    form.value = {
      title: '',
      description: '',
      priority: '' as TaskPriority | '',
      category: '' as TaskCategory | '',
      dueDate: tomorrowFormatted,
      estimatedTime: '',
      tags: [] as string[],
      status: 'pending' as TaskStatus,
      notes: '',
    }
  }

  console.log('✅ TaskModal: Form initialized with dueDate:', form.value.dueDate)
}, { immediate: true })

// Methods
const addTag = () => {
  const tag = newTag.value.trim()
  if (tag && !form.value.tags.includes(tag)) {
    form.value.tags.push(tag)
    newTag.value = ''
  }
}

const removeTag = (index: number) => {
  form.value.tags.splice(index, 1)
}

const applyTemplate = (template: any) => {
  Object.assign(form.value, template.template)
  
  // Set due date to tomorrow
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  form.value.dueDate = tomorrow.toISOString().split('T')[0]
}

const validateForm = () => {
  console.log('🔍 TaskModal: Validating form with data:', form.value)

  errors.value = { title: '', dueDate: '' }

  if (!form.value.title.trim()) {
    errors.value.title = 'Title is required'
    console.log('❌ TaskModal: Title validation failed')
  }

  if (!form.value.dueDate) {
    errors.value.dueDate = 'Due date is required'
    console.log('❌ TaskModal: Due date validation failed')
  }

  const isValid = !errors.value.title && !errors.value.dueDate
  console.log('✅ TaskModal: Form validation result:', isValid, 'Errors:', errors.value)

  return isValid
}

const handleSubmit = () => {
  console.log('🚀 TaskModal: handleSubmit called!')

  if (!validateForm()) {
    console.log('❌ TaskModal: Form validation failed, not submitting')
    return
  }

  console.log('💾 TaskModal: Form validation passed, submitting form with dueDate:', form.value.dueDate)

  const taskData: any = {
    title: form.value.title.trim(),
    description: form.value.description.trim(),
    priority: form.value.priority as TaskPriority,
    category: form.value.category as TaskCategory,
    dueDate: new Date(form.value.dueDate),
    tags: form.value.tags,
    estimatedTime: form.value.estimatedTime ? parseInt(form.value.estimatedTime) : undefined,
    notes: form.value.notes.trim(),
  }

  // Include status when editing
  if (props.task) {
    taskData.status = form.value.status
    console.log('✏️ TaskModal: Updating task with status:', taskData.status)
  }

  console.log('📤 TaskModal: Final taskData:', taskData)
  emit('save', taskData)
}
</script>

<style scoped>
.input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background-color: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  color: var(--color-text-primary);
  font-size: 0.875rem;
  transition: var(--transition-normal);
}

.input:focus {
  outline: none;
  border-color: var(--color-brand-primary);
  box-shadow: 0 0 0 3px rgba(228, 117, 163, 0.1);
}

.input::placeholder {
  color: var(--color-text-muted);
}

select.input {
  cursor: pointer;
}

textarea.input {
  resize: none;
}
</style>
