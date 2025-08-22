<template>
  <div class="fixed inset-0 z-50">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black bg-opacity-50" @click="$emit('close')" />

    <!-- Modal positioned on left side -->
    <div class="absolute left-6 top-6 bottom-6 w-[500px] bg-forest-800 rounded-xl shadow-2xl overflow-hidden flex flex-col">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-forest-700 flex-shrink-0">
        <div class="flex items-center space-x-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-500">
            <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
            </svg>
          </div>
          <div>
            <h3 class="text-xl font-semibold text-white">Edit Team Settings</h3>
            <p class="text-sm text-gray-400">Update your team information</p>
          </div>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-white transition-colors"
        >
          <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="flex-1 overflow-y-auto p-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Team Name -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Team Name <span class="text-red-400">*</span>
            </label>
            <input
              v-model="formData.name"
              type="text"
              required
              placeholder="My Content Team"
              class="w-full px-3 py-2 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              :class="{ 'border-red-500': errors.name }"
            />
            <p v-if="errors.name" class="mt-1 text-sm text-red-400">{{ errors.name }}</p>
          </div>

          <!-- Team Statistics -->
          <div class="bg-forest-700 rounded-lg p-4">
            <h4 class="font-medium text-white mb-4">Team Statistics</h4>
            <div class="grid grid-cols-2 gap-4">
              <div class="text-center">
                <div class="text-2xl font-bold text-blue-400">{{ currentTeam?.member_count || 0 }}</div>
                <div class="text-sm text-gray-400">Members</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-orange-400">{{ currentTeam?.max_seats || 3 }}</div>
                <div class="text-sm text-gray-400">Max Seats</div>
              </div>
            </div>
          </div>

          <!-- Seat Usage Visualization -->
          <div v-if="currentTeam" class="bg-forest-700 rounded-lg p-4">
            <h4 class="font-medium text-white mb-3">Seat Usage</h4>
            <div class="flex items-center space-x-3 mb-2">
              <div class="flex-1 bg-forest-600 rounded-full h-3">
                <div 
                  class="bg-blue-500 h-3 rounded-full transition-all duration-300"
                  :style="{ width: `${(currentTeam.member_count / currentTeam.max_seats) * 100}%` }"
                ></div>
              </div>
              <span class="text-sm text-gray-400">
                {{ currentTeam.member_count }}/{{ currentTeam.max_seats }}
              </span>
            </div>
            <p class="text-xs text-gray-400">
              {{ currentTeam.available_seats }} seats available
            </p>
          </div>

          <!-- Team Created -->
          <div v-if="currentTeam" class="bg-forest-700 rounded-lg p-4">
            <h4 class="font-medium text-white mb-2">Team Information</h4>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-400">Created:</span>
                <span class="text-white">{{ formatDate(currentTeam.created_at) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-400">Plan:</span>
                <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Team Plan
                </span>
              </div>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="bg-red-900/30 border border-red-500/30 rounded-lg p-3">
            <p class="text-red-300 text-sm">{{ error }}</p>
          </div>
        </form>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-between p-6 border-t border-forest-700 flex-shrink-0">
        <button
          @click="$emit('close')"
          class="px-4 py-2 text-gray-400 hover:text-white transition-colors"
        >
          Cancel
        </button>
        <button
          @click="handleSubmit"
          :disabled="loading || !isFormValid"
          class="px-6 py-2 bg-orange-600 text-white rounded-lg font-medium hover:bg-orange-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
        >
          <svg v-if="loading" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ loading ? 'Saving...' : 'Save Changes' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTeamManagement } from '../../composables/useTeamManagement'
import { useToast } from '../../composables/useToast'

const props = defineProps({
  teamData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'save'])

// Composables
const { currentTeam, updateTeam, loading, error } = useTeamManagement()
const { success, error: showError } = useToast()

// Form data
const formData = ref({
  name: ''
})

// Form validation
const errors = ref({})

const isFormValid = computed(() => {
  return formData.value.name && 
         formData.value.name.trim().length > 0 &&
         !errors.value.name &&
         !loading.value
})

// Handle form submission
const handleSubmit = async () => {
  // Clear previous errors
  errors.value = {}

  // Validate name
  if (!formData.value.name || formData.value.name.trim().length === 0) {
    errors.value.name = 'Team name is required'
    return
  }

  if (formData.value.name.trim().length > 255) {
    errors.value.name = 'Team name must be less than 255 characters'
    return
  }

  try {
    await updateTeam(currentTeam.value.id, {
      name: formData.value.name.trim()
    })

    success('Team Updated! ✅', 'Team settings have been saved successfully')
    emit('save', formData.value)
    emit('close')
  } catch (err) {
    showError('Update Failed', err.message || 'Failed to update team settings')
  }
}

// Format date helper
const formatDate = (dateString) => {
  if (!dateString) return 'Unknown'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Initialize form when modal opens
onMounted(() => {
  if (currentTeam.value) {
    formData.value.name = currentTeam.value.name || ''
  }
  errors.value = {}
})
</script>
