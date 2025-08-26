<template>
  <div class="fixed inset-0 z-[60] flex items-center justify-center">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black bg-opacity-50" @click="$emit('close')" />
    
    <!-- Modal -->
    <div class="relative bg-background-card rounded-xl shadow-xl w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-border">
        <h3 class="text-lg font-semibold text-text-primary">
          {{ goal ? 'Edit Goal' : 'Create New Goal' }}
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
            Goal Title *
          </label>
          <VInput
            v-model="form.title"
            placeholder="Enter goal title..."
            required
            :error="errors.title"
          />
        </div>

        <!-- Goal Type and Target -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-2">
              Goal Type *
            </label>
            <select
              v-model="form.type"
              class="input w-full"
              required
            >
              <option value="">Select goal type</option>
              <option value="views">👁️ Views</option>
              <option value="subscribers">👥 Subscribers</option>
              <option value="revenue">💰 Revenue</option>
              <option value="engagement">❤️ Engagement</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-text-secondary mb-2">
              Target Value *
            </label>
            <VInput
              v-model="form.target"
              type="number"
              placeholder="10000"
              min="1"
              required
              :error="errors.target"
            />
          </div>
        </div>

        <!-- Current Value and Deadline -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-2">
              Current Value
            </label>
            <VInput
              v-model="form.current"
              type="number"
              placeholder="0"
              min="0"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-text-secondary mb-2">
              Deadline *
            </label>
            <VInput
              v-model="form.deadline"
              type="date"
              required
              :error="errors.deadline"
            />
          </div>
        </div>

        <!-- Color Selection -->
        <div>
          <label class="block text-sm font-medium text-text-secondary mb-2">
            Goal Color
          </label>
          <div class="flex space-x-3">
            <button
              v-for="color in colorOptions"
              :key="color.value"
              type="button"
              class="w-8 h-8 rounded-full border-2 transition-all"
              :class="[
                color.class,
                form.color === color.value 
                  ? 'border-white scale-110' 
                  : 'border-transparent hover:scale-105'
              ]"
              @click="form.color = color.value"
            />
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-end space-x-3 pt-4 border-t border-border">
          <VButton variant="ghost" @click="$emit('close')">
            Cancel
          </VButton>
          <VButton variant="primary" type="submit" :disabled="!isFormValid">
            {{ goal ? 'Update Goal' : 'Create Goal' }}
          </VButton>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { ChannelGoal } from '../../stores/analytics'
import { useAnalyticsStore } from '../../stores/analytics'
import VButton from '../ui/VButton.vue'
import VInput from '../ui/VInput.vue'

interface Props {
  goal?: ChannelGoal | null
}

const props = defineProps<Props>()
const emit = defineEmits<{
  close: []
  save: [goalData: Omit<ChannelGoal, 'id'>]
}>()

const analyticsStore = useAnalyticsStore()

// Form state
const form = ref({
  title: '',
  type: '' as 'views' | 'subscribers' | 'revenue' | 'engagement' | '',
  target: '',
  current: '',
  deadline: '',
  color: 'from-orange-400 to-pink-500',
})

const errors = ref({
  title: '',
  target: '',
  deadline: '',
})

// Color options
const colorOptions = [
  { value: 'from-orange-400 to-pink-500', class: 'bg-gradient-to-r from-orange-400 to-pink-500' },
  { value: 'from-blue-400 to-cyan-500', class: 'bg-gradient-to-r from-blue-400 to-cyan-500' },
  { value: 'from-purple-400 to-indigo-500', class: 'bg-gradient-to-r from-purple-400 to-indigo-500' },
  { value: 'from-green-400 to-emerald-500', class: 'bg-gradient-to-r from-green-400 to-emerald-500' },
  { value: 'from-red-400 to-rose-500', class: 'bg-gradient-to-r from-red-400 to-rose-500' },
  { value: 'from-yellow-400 to-amber-500', class: 'bg-gradient-to-r from-yellow-400 to-amber-500' },
]

// Icon mapping
const getIconForType = (type: string): string => {
  const icons = {
    views: '👁️',
    subscribers: '👥',
    revenue: '💰',
    engagement: '❤️',
  }
  return icons[type as keyof typeof icons] || '🎯'
}

// Form validation
const isFormValid = computed(() => {
  return form.value.title.trim() && 
         form.value.type && 
         form.value.target && 
         form.value.deadline
})

// Initialize form with goal data if editing
watch(() => props.goal, (goal) => {
  if (goal) {
    form.value = {
      title: goal.title,
      type: goal.type,
      target: goal.target.toString(),
      current: goal.current.toString(),
      deadline: new Date(goal.deadline).toISOString().split('T')[0],
      color: goal.color,
    }
  } else {
    // Set default deadline to end of year
    const endOfYear = new Date()
    endOfYear.setMonth(11, 31)
    form.value.deadline = endOfYear.toISOString().split('T')[0]
  }
}, { immediate: true })

// Methods
const validateForm = () => {
  errors.value = { title: '', target: '', deadline: '' }
  
  if (!form.value.title.trim()) {
    errors.value.title = 'Title is required'
  }
  
  if (!form.value.target || parseInt(form.value.target) <= 0) {
    errors.value.target = 'Target must be greater than 0'
  }
  
  if (!form.value.deadline) {
    errors.value.deadline = 'Deadline is required'
  }
  
  return !errors.value.title && !errors.value.target && !errors.value.deadline
}

const handleSubmit = () => {
  if (!validateForm()) return
  
  const goalData: Omit<ChannelGoal, 'id'> = {
    title: form.value.title.trim(),
    type: form.value.type as 'views' | 'subscribers' | 'revenue' | 'engagement',
    target: parseInt(form.value.target),
    current: parseInt(form.value.current) || 0,
    deadline: new Date(form.value.deadline),
    color: form.value.color,
    icon: getIconForType(form.value.type),
  }
  
  emit('save', goalData)
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

select.input {
  cursor: pointer;
}
</style>
