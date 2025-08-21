<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black bg-opacity-50" @click="$emit('close')" />
    
    <!-- Modal -->
    <div class="relative bg-forest-800 rounded-xl shadow-xl w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-forest-700">
        <h3 class="text-lg font-semibold text-white">
          {{ content ? 'Edit Content' : 'Create New Content' }}
        </h3>
        <button
          class="text-gray-400 hover:text-white transition-colors"
          @click="$emit('close')"
        >
          ✕
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
        <!-- Title -->
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Title *
          </label>
          <input
            v-model="form.title"
            type="text"
            class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            placeholder="Enter content title"
            required
          />
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Description
          </label>
          <textarea
            v-model="form.description"
            rows="3"
            class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none"
            placeholder="Enter content description"
          />
        </div>

        <!-- Status and Priority -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Stage *
            </label>
            <select
              v-model="form.status"
              class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              required
            >
              <option value="ideas">Ideas</option>
              <option value="planning">Planning</option>
              <option value="in-progress">In Progress</option>
              <option value="published">Published</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Priority *
            </label>
            <select
              v-model="form.priority"
              class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              required
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>
        </div>

        <!-- Pillar -->
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Pillar *
          </label>
          <select
            v-model="form.pillarId"
            class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            required
          >
            <option value="">Select a pillar</option>
            <option v-for="pillar in availablePillars" :key="pillar.id" :value="pillar.id">
              {{ pillar.icon }} {{ pillar.name }}
            </option>
          </select>
        </div>

        <!-- Stage Due Dates -->
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-3">
            Stage Due Dates
          </label>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs text-gray-400 mb-1">Ideas Due Date</label>
              <input
                v-model="form.stageDueDates.ideas"
                type="date"
                class="w-full px-3 py-2 bg-forest-700 border border-forest-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>
            <div>
              <label class="block text-xs text-gray-400 mb-1">Planning Due Date</label>
              <input
                v-model="form.stageDueDates.planning"
                type="date"
                class="w-full px-3 py-2 bg-forest-700 border border-forest-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>
            <div>
              <label class="block text-xs text-gray-400 mb-1">In Progress Due Date</label>
              <input
                v-model="form.stageDueDates['in-progress']"
                type="date"
                class="w-full px-3 py-2 bg-forest-700 border border-forest-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>
            <div>
              <label class="block text-xs text-gray-400 mb-1">Published Due Date</label>
              <input
                v-model="form.stageDueDates.published"
                type="date"
                class="w-full px-3 py-2 bg-forest-700 border border-forest-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>
          </div>
        </div>

        <!-- Stage Completions -->
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-3">
            Stage Completion
          </label>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="flex items-center space-x-2">
              <input
                v-model="form.stageCompletions.ideas"
                type="checkbox"
                class="w-4 h-4 text-orange-500 bg-forest-700 border-forest-600 rounded focus:ring-orange-500 focus:ring-2"
              />
              <label class="text-sm text-gray-300">Ideas Done</label>
            </div>
            <div class="flex items-center space-x-2">
              <input
                v-model="form.stageCompletions.planning"
                type="checkbox"
                class="w-4 h-4 text-orange-500 bg-forest-700 border-forest-600 rounded focus:ring-orange-500 focus:ring-2"
              />
              <label class="text-sm text-gray-300">Planning Done</label>
            </div>
            <div class="flex items-center space-x-2">
              <input
                v-model="form.stageCompletions['in-progress']"
                type="checkbox"
                class="w-4 h-4 text-orange-500 bg-forest-700 border-forest-600 rounded focus:ring-orange-500 focus:ring-2"
              />
              <label class="text-sm text-gray-300">In Progress Done</label>
            </div>
            <div class="flex items-center space-x-2">
              <input
                v-model="form.stageCompletions.published"
                type="checkbox"
                class="w-4 h-4 text-orange-500 bg-forest-700 border-forest-600 rounded focus:ring-orange-500 focus:ring-2"
              />
              <label class="text-sm text-gray-300">Published Done</label>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-end space-x-3 pt-4 border-t border-forest-700">
          <button
            type="button"
            @click="$emit('close')"
            class="px-6 py-2 text-gray-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-6 py-2 bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors"
          >
            {{ content ? 'Update Content' : 'Create Content' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  content: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'save'])

// Available pillars (this should come from a store in a real app)
const availablePillars = ref([
  { id: 1, name: 'Marketing', icon: '📈' },
  { id: 2, name: 'Technology', icon: '💻' },
  { id: 3, name: 'Content Strategy', icon: '📝' },
  { id: 4, name: 'Analytics', icon: '📊' }
])

// Form state
const form = ref({
  title: '',
  description: '',
  status: 'ideas',
  priority: 'medium',
  pillarId: '',
  stageDueDates: {
    ideas: '',
    planning: '',
    'in-progress': '',
    published: ''
  },
  stageCompletions: {
    ideas: false,
    planning: false,
    'in-progress': false,
    published: false
  }
})

// Watch for content prop changes to populate form
watch(() => props.content, (newContent) => {
  if (newContent) {
    form.value = {
      title: newContent.title || '',
      description: newContent.description || '',
      status: newContent.status || 'ideas',
      priority: newContent.priority || 'medium',
      pillarId: newContent.pillar?.id || '',
      stageDueDates: {
        ideas: newContent.stageDueDates?.ideas || '',
        planning: newContent.stageDueDates?.planning || '',
        'in-progress': newContent.stageDueDates?.['in-progress'] || '',
        published: newContent.stageDueDates?.published || ''
      },
      stageCompletions: {
        ideas: newContent.stageCompletions?.ideas || false,
        planning: newContent.stageCompletions?.planning || false,
        'in-progress': newContent.stageCompletions?.['in-progress'] || false,
        published: newContent.stageCompletions?.published || false
      }
    }
  } else {
    // Reset form for new content
    form.value = {
      title: '',
      description: '',
      status: 'ideas',
      priority: 'medium',
      pillarId: '',
      stageDueDates: {
        ideas: '',
        planning: '',
        'in-progress': '',
        published: ''
      },
      stageCompletions: {
        ideas: false,
        planning: false,
        'in-progress': false,
        published: false
      }
    }
  }
}, { immediate: true })

const handleSubmit = () => {
  if (!form.value.title.trim()) {
    alert('Please enter a title')
    return
  }

  if (!form.value.pillarId) {
    alert('Please select a pillar')
    return
  }

  const selectedPillar = availablePillars.value.find(p => p.id === form.value.pillarId)
  
  const contentData = {
    id: props.content?.id || Date.now(),
    title: form.value.title.trim(),
    description: form.value.description.trim(),
    status: form.value.status,
    priority: form.value.priority,
    pillar: selectedPillar,
    stageDueDates: form.value.stageDueDates,
    stageCompletions: form.value.stageCompletions,
    createdAt: props.content?.createdAt || new Date().toISOString(),
    dueDate: form.value.stageDueDates.published || new Date().toISOString()
  }

  emit('save', contentData)
}
</script>
