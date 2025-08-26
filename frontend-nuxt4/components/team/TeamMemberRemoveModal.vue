<template>
  <div class="fixed inset-0 z-[60]">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black bg-opacity-50" @click="$emit('close')" />

    <!-- Modal centered -->
    <div class="fixed inset-0 flex items-center justify-center p-4">
      <div class="bg-forest-800 rounded-xl shadow-2xl max-w-md w-full">
        <!-- Header -->
        <div class="flex items-center justify-between p-6 border-b border-forest-700">
          <div class="flex items-center space-x-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-red-500">
              <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" clip-rule="evenodd"/>
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
              </svg>
            </div>
            <div>
              <h3 class="text-xl font-semibold text-white">Remove Team Member</h3>
              <p class="text-sm text-gray-400">This action cannot be undone</p>
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
        <div class="p-6">
          <div v-if="memberData" class="space-y-4">
            <!-- Member Info -->
            <div class="bg-forest-700 rounded-lg p-4">
              <div class="flex items-center space-x-3">
                <div 
                  class="w-12 h-12 rounded-full flex items-center justify-center text-white font-medium"
                  :style="{ backgroundColor: getMemberColor(memberData) }"
                >
                  {{ getMemberInitials(memberData) }}
                </div>
                <div>
                  <p class="font-medium text-white">{{ memberData.user_name }}</p>
                  <p class="text-sm text-gray-400">{{ memberData.user_email }}</p>
                  <span 
                    class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium mt-1"
                    :class="getRoleBadgeClasses(memberData.role)"
                  >
                    {{ getRoleDisplayName(memberData.role) }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Warning Message -->
            <div class="bg-red-900/30 border border-red-500/30 rounded-lg p-4">
              <div class="flex items-start space-x-3">
                <svg class="w-5 h-5 text-red-400 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                </svg>
                <div>
                  <h4 class="font-medium text-red-300 mb-1">Are you sure?</h4>
                  <p class="text-sm text-red-200">
                    Removing <strong>{{ memberData.user_name }}</strong> will:
                  </p>
                  <ul class="text-sm text-red-200 mt-2 space-y-1">
                    <li>• Immediately revoke their access to the team</li>
                    <li>• Remove them from all team content and discussions</li>
                    <li>• Free up one seat in your team plan</li>
                    <li>• Require a new invitation to rejoin</li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- Error Message -->
            <div v-if="error" class="bg-red-900/30 border border-red-500/30 rounded-lg p-3">
              <p class="text-red-300 text-sm">{{ error }}</p>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="flex items-center justify-between p-6 border-t border-forest-700">
          <button
            @click="$emit('close')"
            class="px-4 py-2 text-gray-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
          <button
            @click="handleRemove"
            :disabled="loading"
            class="px-6 py-2 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <svg v-if="loading" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ loading ? 'Removing...' : 'Remove Member' }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useTeamManagement } from '../../composables/useTeamManagement'
import { useToast } from '../../composables/useToast'

const props = defineProps({
  memberData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'remove'])

// Composables
const { currentTeam, removeMember, loading, error, getRoleDisplayName } = useTeamManagement()
const { success, error: showError } = useToast()

// Helper functions
const getMemberInitials = (member) => {
  if (!member?.user_name) return '??'
  return member.user_name
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const getMemberColor = (member) => {
  const colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
  const index = member?.user_name?.charCodeAt(0) % colors.length || 0
  return colors[index]
}

const getRoleBadgeClasses = (role) => {
  switch (role) {
    case 'owner':
      return 'bg-orange-100 text-orange-800'
    case 'editor':
      return 'bg-blue-100 text-blue-800'
    case 'viewer':
      return 'bg-gray-100 text-gray-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

// Handle member removal
const handleRemove = async () => {
  if (!props.memberData || !currentTeam.value) return

  try {
    await removeMember(currentTeam.value.id, props.memberData.id)
    
    success('Member Removed', `${props.memberData.user_name} has been removed from the team`)
    emit('remove', props.memberData)
    emit('close')
  } catch (err) {
    showError('Removal Failed', err.message || 'Failed to remove team member')
  }
}
</script>
