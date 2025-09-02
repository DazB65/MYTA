<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
    @click="closeModal"
  >
    <div
      class="bg-forest-800 rounded-xl max-w-md w-full p-6"
      @click.stop
    >
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-lg bg-green-500/20 flex items-center justify-center">
            <span class="text-green-400">👥</span>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-white">Create Team</h2>
            <p class="text-gray-400 text-sm">Start collaborating with your team</p>
          </div>
        </div>
        <button
          @click="closeModal"
          class="w-8 h-8 rounded-lg bg-forest-700 hover:bg-forest-600 flex items-center justify-center text-gray-400 hover:text-white transition-colors"
        >
          ✕
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit">
        <!-- Team Name -->
        <div class="mb-4">
          <label for="teamName" class="block text-sm font-medium text-gray-300 mb-2">
            Team Name
          </label>
          <input
            id="teamName"
            v-model="formData.name"
            type="text"
            placeholder="Enter your team name"
            class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-green-500 transition-colors"
            :class="{ 'border-red-500': errors.name }"
            required
          />
          <p v-if="errors.name" class="mt-1 text-sm text-red-400">{{ errors.name }}</p>
        </div>

        <!-- Team Size -->
        <div class="mb-4">
          <label for="teamSize" class="block text-sm font-medium text-gray-300 mb-2">
            Maximum Team Size
          </label>
          <select
            id="teamSize"
            v-model="formData.maxSeats"
            class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white focus:outline-none focus:border-green-500 transition-colors"
          >
            <option value="3">3 members (Small team)</option>
            <option value="5">5 members (Medium team)</option>
            <option value="10">10 members (Large team)</option>
            <option value="25">25 members (Enterprise)</option>
          </select>
        </div>

        <!-- Team Description -->
        <div class="mb-6">
          <label for="teamDescription" class="block text-sm font-medium text-gray-300 mb-2">
            Description (Optional)
          </label>
          <textarea
            id="teamDescription"
            v-model="formData.description"
            placeholder="Describe your team's purpose and goals"
            rows="3"
            class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-green-500 transition-colors resize-none"
          ></textarea>
        </div>

        <!-- Features Info -->
        <div class="mb-6 p-4 rounded-lg bg-forest-700 border border-green-500/20">
          <h4 class="text-white font-medium mb-2">Team Features Include:</h4>
          <ul class="text-sm text-gray-300 space-y-1">
            <li class="flex items-center space-x-2">
              <span class="text-green-400">✓</span>
              <span>Collaborative content planning</span>
            </li>
            <li class="flex items-center space-x-2">
              <span class="text-green-400">✓</span>
              <span>Shared AI team insights</span>
            </li>
            <li class="flex items-center space-x-2">
              <span class="text-green-400">✓</span>
              <span>Team notifications and updates</span>
            </li>
            <li class="flex items-center space-x-2">
              <span class="text-green-400">✓</span>
              <span>Role-based permissions</span>
            </li>
            <li class="flex items-center space-x-2">
              <span class="text-green-400">✓</span>
              <span>Team performance analytics</span>
            </li>
          </ul>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mb-4 p-3 rounded-lg bg-red-500/20 border border-red-500/30">
          <p class="text-red-300 text-sm">{{ error }}</p>
        </div>

        <!-- Success Message -->
        <div v-if="success" class="mb-4 p-3 rounded-lg bg-green-500/20 border border-green-500/30">
          <p class="text-green-300 text-sm">{{ success }}</p>
        </div>

        <!-- Actions -->
        <div class="flex space-x-3">
          <button
            type="button"
            @click="closeModal"
            class="flex-1 px-4 py-3 bg-forest-700 text-gray-300 rounded-lg hover:bg-forest-600 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="loading || !formData.name.trim()"
            class="flex-1 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
          >
            <span v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            <span>{{ loading ? 'Creating...' : 'Create Team' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useTeamManagement } from '../../composables/useTeamManagement'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'created'])

const { createTeam } = useTeamManagement()

// Form state
const formData = reactive({
  name: '',
  maxSeats: 5,
  description: ''
})

const errors = ref({})
const loading = ref(false)
const error = ref('')
const success = ref('')

// Methods
const closeModal = () => {
  // Reset form
  formData.name = ''
  formData.maxSeats = 5
  formData.description = ''
  errors.value = {}
  error.value = ''
  success.value = ''
  loading.value = false
  
  emit('close')
}

const validateForm = () => {
  errors.value = {}
  
  if (!formData.name.trim()) {
    errors.value.name = 'Team name is required'
    return false
  }
  
  if (formData.name.trim().length < 2) {
    errors.value.name = 'Team name must be at least 2 characters'
    return false
  }
  
  if (formData.name.trim().length > 50) {
    errors.value.name = 'Team name must be less than 50 characters'
    return false
  }
  
  return true
}

const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }
  
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    // Create team
    const team = await createTeam(formData.name.trim(), formData.maxSeats)
    
    success.value = 'Team created successfully! 🎉'
    
    // Wait a moment to show success message
    setTimeout(() => {
      emit('created', team)
      closeModal()
    }, 1500)
    
  } catch (err) {
    console.error('Team creation error:', err)
    
    // Handle different error types
    if (err.message?.includes('backend connection')) {
      error.value = 'Creating team in demo mode. Full features require backend connection.'
      // Still show success for demo
      setTimeout(() => {
        success.value = 'Demo team created! 🎉'
        setTimeout(() => {
          emit('created', { 
            id: 'demo-team', 
            name: formData.name.trim(),
            max_seats: formData.maxSeats,
            description: formData.description
          })
          closeModal()
        }, 1000)
      }, 1000)
    } else if (err.message?.includes('subscription')) {
      error.value = 'Team features require a Team subscription. Please upgrade your plan.'
    } else if (err.message?.includes('Authentication')) {
      error.value = 'Please log in to create a team.'
    } else {
      error.value = err.message || 'Failed to create team. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>
