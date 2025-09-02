<template>
  <div class="rounded-xl bg-forest-800 p-4">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-2">
        <div class="w-6 h-6 rounded-lg bg-green-500/20 flex items-center justify-center">
          <span class="text-green-400">👥</span>
        </div>
        <h3 class="text-sm font-semibold text-white">Team Members</h3>
      </div>
      <span class="text-xs text-gray-400">{{ onlineCount }} online</span>
    </div>

    <!-- Members List -->
    <div class="space-y-2">
      <div
        v-for="member in sortedMembers"
        :key="member.id"
        class="flex items-center justify-between p-2 rounded-lg hover:bg-forest-700 transition-colors cursor-pointer"
        @click="startDirectMessage(member)"
      >
        <div class="flex items-center space-x-3">
          <!-- Avatar with Status -->
          <div class="relative">
            <div class="w-8 h-8 rounded-full bg-gray-500 flex items-center justify-center text-sm text-white font-medium">
              {{ member.name.charAt(0) }}
            </div>
            <!-- Status Indicator -->
            <div
              class="absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full border-2 border-forest-800"
              :class="getStatusColor(member.status)"
            ></div>
          </div>
          
          <!-- Member Info -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center space-x-2">
              <p class="text-sm font-medium text-white truncate">{{ member.name }}</p>
              <span
                class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium"
                :class="getRoleBadgeClass(member.role)"
              >
                {{ member.role }}
              </span>
            </div>
            <p class="text-xs text-gray-400">{{ getStatusText(member) }}</p>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center space-x-1">
          <!-- Direct Message Button -->
          <button
            @click.stop="startDirectMessage(member)"
            class="p-1 rounded text-gray-400 hover:text-white hover:bg-forest-600 transition-colors"
            :title="`Message ${member.name}`"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
              <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
            </svg>
          </button>
          
          <!-- More Options -->
          <div class="relative" v-if="member.id !== currentUserId">
            <button
              @click.stop="toggleMemberMenu(member.id)"
              class="p-1 rounded text-gray-400 hover:text-white hover:bg-forest-600 transition-colors"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
              </svg>
            </button>
            
            <!-- Member Menu -->
            <div
              v-if="openMenuId === member.id"
              class="absolute right-0 top-8 w-48 bg-forest-700 rounded-lg shadow-lg border border-forest-600 py-1 z-10"
            >
              <button
                @click="viewMemberProfile(member)"
                class="w-full text-left px-3 py-2 text-sm text-gray-300 hover:bg-forest-600 hover:text-white"
              >
                View Profile
              </button>
              <button
                @click="startDirectMessage(member)"
                class="w-full text-left px-3 py-2 text-sm text-gray-300 hover:bg-forest-600 hover:text-white"
              >
                Send Message
              </button>
              <button
                v-if="canManageMembers"
                @click="editMemberRole(member)"
                class="w-full text-left px-3 py-2 text-sm text-gray-300 hover:bg-forest-600 hover:text-white"
              >
                Edit Role
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="mt-4 pt-4 border-t border-forest-600">
      <div class="flex space-x-2">
        <button
          @click="inviteNewMember"
          class="flex-1 bg-blue-600 text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
        >
          Invite Member
        </button>
        <button
          @click="createGroupChat"
          class="flex-1 bg-forest-700 text-gray-300 px-3 py-2 rounded-lg text-sm font-medium hover:bg-forest-600 transition-colors"
        >
          Group Chat
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { computed, ref } from 'vue'
import { useModals } from '../../composables/useModals'
import { useToast } from '../../composables/useToast'
import { useTeamChatStore } from '../../stores/teamChat'

// Define emits
const emit = defineEmits(['start-direct-message'])

// Composables
const teamChatStore = useTeamChatStore()
const { openTeamInvite, openTeamMemberEdit } = useModals()
const { success } = useToast()

// Local state
const openMenuId = ref(null)
const currentUserId = ref('current_user') // Would come from auth store

// Computed - Use storeToRefs to maintain reactivity
const { members } = storeToRefs(teamChatStore)

const sortedMembers = computed(() => {
  return [...members.value].sort((a, b) => {
    // Sort by status: online first, then away, then offline
    const statusOrder = { online: 0, away: 1, offline: 2 }
    const statusDiff = statusOrder[a.status] - statusOrder[b.status]
    if (statusDiff !== 0) return statusDiff
    
    // Then sort by name
    return a.name.localeCompare(b.name)
  })
})

const onlineCount = computed(() => {
  return members.value.filter(m => m.status === 'online').length
})

const canManageMembers = computed(() => {
  // In a real app, this would check user permissions
  return true
})

// Methods
const getStatusColor = (status) => {
  switch (status) {
    case 'online': return 'bg-green-500'
    case 'away': return 'bg-yellow-500'
    case 'offline': return 'bg-gray-500'
    default: return 'bg-gray-500'
  }
}

const getStatusText = (member) => {
  switch (member.status) {
    case 'online': return 'Online'
    case 'away': return 'Away'
    case 'offline': 
      if (member.lastSeen) {
        const now = new Date()
        const lastSeen = new Date(member.lastSeen)
        const diffInMinutes = Math.floor((now - lastSeen) / (1000 * 60))
        
        if (diffInMinutes < 60) return `Last seen ${diffInMinutes}m ago`
        if (diffInMinutes < 1440) return `Last seen ${Math.floor(diffInMinutes / 60)}h ago`
        return `Last seen ${Math.floor(diffInMinutes / 1440)}d ago`
      }
      return 'Offline'
    default: return 'Unknown'
  }
}

const getRoleBadgeClass = (role) => {
  switch (role.toLowerCase()) {
    case 'owner': return 'bg-red-500/20 text-red-300'
    case 'admin': return 'bg-orange-500/20 text-orange-300'
    case 'editor': return 'bg-blue-500/20 text-blue-300'
    case 'viewer': return 'bg-gray-500/20 text-gray-300'
    default: return 'bg-gray-500/20 text-gray-300'
  }
}

const toggleMemberMenu = (memberId) => {
  openMenuId.value = openMenuId.value === memberId ? null : memberId
}

const startDirectMessage = (member) => {
  // Emit event to parent component to start direct message
  emit('start-direct-message', member)
  openMenuId.value = null
}

const viewMemberProfile = (member) => {
  // In a real app, this would open a member profile modal
  success('Member Profile', `Viewing profile for ${member.name}`)
  openMenuId.value = null
}

const editMemberRole = (member) => {
  openTeamMemberEdit(member)
  openMenuId.value = null
}

const inviteNewMember = () => {
  openTeamInvite()
}

const createGroupChat = () => {
  // In a real app, this would open a group chat creation modal
  success('Group Chat', 'Creating new group chat...')
}

// Close menu when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    openMenuId.value = null
  }
}

// Add click outside listener
if (process.client) {
  document.addEventListener('click', handleClickOutside)
}
</script>
