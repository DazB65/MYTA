<template>
  <div class="fixed inset-0 z-50">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black bg-opacity-50" @click="$emit('close')" />

    <!-- Modal positioned on left side -->
    <div class="absolute left-6 top-6 bottom-6 w-[500px] bg-forest-800 rounded-xl shadow-2xl overflow-hidden flex flex-col">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-forest-700 flex-shrink-0">
        <div class="flex items-center space-x-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-500">
            <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z"/>
            </svg>
          </div>
          <div>
            <h3 class="text-xl font-semibold text-white">Invite Team Member</h3>
            <p class="text-sm text-gray-400">Send an invitation to join your team</p>
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
          <!-- Email Input -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Email Address <span class="text-red-400">*</span>
            </label>
            <input
              v-model="formData.email"
              type="email"
              required
              placeholder="colleague@example.com"
              class="w-full px-3 py-2 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              :class="{ 'border-red-500': errors.email }"
            />
            <p v-if="errors.email" class="mt-1 text-sm text-red-400">{{ errors.email }}</p>
          </div>

          <!-- Role Selection -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Role <span class="text-red-400">*</span>
            </label>
            <select
              v-model="formData.role"
              required
              class="w-full px-3 py-2 bg-forest-700 border border-forest-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="editor">Editor - Can create and edit content</option>
              <option value="viewer">Viewer - Read-only access</option>
            </select>
            <p class="mt-1 text-sm text-gray-400">{{ getRoleDescription(formData.role) }}</p>
          </div>

          <!-- Optional Message -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Personal Message (Optional)
            </label>
            <textarea
              v-model="formData.message"
              rows="3"
              placeholder="Add a personal message to the invitation..."
              class="w-full px-3 py-2 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            ></textarea>
          </div>

          <!-- Team Info -->
          <div v-if="currentTeam" class="bg-forest-700 rounded-lg p-4">
            <h4 class="font-medium text-white mb-2">Team Information</h4>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-400">Team Name:</span>
                <span class="text-white">{{ currentTeam.name }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-400">Available Seats:</span>
                <span class="text-white">{{ currentTeam.available_seats }} of {{ currentTeam.max_seats }}</span>
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
          class="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
        >
          <svg v-if="loading" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ loading ? 'Sending...' : 'Send Invitation' }}</span>
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
const { currentTeam, inviteMember, loading, error, getRoleDescription } = useTeamManagement()
const { success, error: showError } = useToast()

// Form data
const formData = ref({
  email: '',
  role: 'editor',
  message: ''
})

// Form validation
const errors = ref({})

const isFormValid = computed(() => {
  return formData.value.email && 
         formData.value.role && 
         !errors.value.email &&
         !loading.value
})

// Validate email
const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// Handle form submission
const handleSubmit = async () => {
  // Clear previous errors
  errors.value = {}

  // Validate email
  if (!validateEmail(formData.value.email)) {
    errors.value.email = 'Please enter a valid email address'
    return
  }

  try {
    await inviteMember(
      currentTeam.value.id,
      formData.value.email,
      formData.value.role,
      formData.value.message || undefined
    )

    success('Invitation Sent! 📧', `Invitation sent to ${formData.value.email}`)
    emit('save', formData.value)
    emit('close')
  } catch (err) {
    showError('Invitation Failed', err.message || 'Failed to send invitation')
  }
}

// Reset form when modal opens
onMounted(() => {
  formData.value = {
    email: '',
    role: 'editor',
    message: ''
  }
  errors.value = {}
})
</script>
