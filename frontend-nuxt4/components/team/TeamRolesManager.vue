<template>
  <div class="rounded-xl bg-forest-800 p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center">
          <span class="text-green-400">👥</span>
        </div>
        <div>
          <h2 class="text-xl font-semibold text-white">Team Roles & Permissions</h2>
          <p class="text-gray-400 text-sm">Manage team member access and responsibilities</p>
        </div>
      </div>
      <button
        @click="openInviteModal"
        class="rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700 transition-colors"
      >
        Invite Member
      </button>
    </div>

    <!-- Team Overview Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div class="text-center p-3 rounded-lg bg-forest-700">
        <div class="text-2xl font-bold text-blue-400">{{ teamStats.totalMembers }}</div>
        <div class="text-xs text-gray-400">Total Members</div>
      </div>
      <div class="text-center p-3 rounded-lg bg-forest-700">
        <div class="text-2xl font-bold text-green-400">{{ teamStats.activeMembers }}</div>
        <div class="text-xs text-gray-400">Active Members</div>
      </div>
      <div class="text-center p-3 rounded-lg bg-forest-700">
        <div class="text-2xl font-bold text-yellow-400">{{ teamStats.pendingInvites }}</div>
        <div class="text-xs text-gray-400">Pending Invites</div>
      </div>
    </div>

    <!-- Team Members List -->
    <div class="space-y-4">
      <!-- Human Team Members -->
      <div>
        <h3 class="text-lg font-medium text-white mb-3">Human Team Members</h3>
        <div class="space-y-3">
          <div
            v-for="member in humanMembers"
            :key="member.id"
            class="p-4 rounded-lg bg-forest-700 hover:bg-forest-600 transition-colors"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <img 
                  :src="member.avatar" 
                  :alt="member.name"
                  class="w-10 h-10 rounded-lg object-cover"
                />
                <div>
                  <div class="text-white font-medium">{{ member.name }}</div>
                  <div class="text-gray-400 text-sm">{{ member.email }}</div>
                </div>
              </div>
              
              <div class="flex items-center space-x-3">
                <!-- Role Badge -->
                <span 
                  class="px-3 py-1 rounded-full text-xs font-medium"
                  :class="getRoleBadgeClass(member.role)"
                >
                  {{ member.role }}
                </span>
                
                <!-- Status -->
                <div class="flex items-center space-x-1">
                  <div 
                    :class="[
                      'w-2 h-2 rounded-full',
                      member.status === 'active' ? 'bg-green-400' : 
                      member.status === 'pending' ? 'bg-yellow-400' : 'bg-gray-400'
                    ]"
                  ></div>
                  <span class="text-xs text-gray-400">{{ member.status }}</span>
                </div>
                
                <!-- Actions -->
                <div class="flex items-center space-x-2">
                  <button
                    @click="editMemberRole(member)"
                    class="p-1 rounded text-gray-400 hover:text-white hover:bg-forest-600 transition-colors"
                  >
                    ⚙️
                  </button>
                  <button
                    v-if="member.role !== 'Owner'"
                    @click="removeMember(member)"
                    class="p-1 rounded text-gray-400 hover:text-red-400 hover:bg-red-500/20 transition-colors"
                  >
                    🗑️
                  </button>
                </div>
              </div>
            </div>

            <!-- Permissions Summary -->
            <div class="mt-3 pt-3 border-t border-forest-600">
              <div class="flex items-center justify-between">
                <div class="text-sm text-gray-300">
                  Permissions: {{ getPermissionsSummary(member.permissions) }}
                </div>
                <button
                  @click="viewPermissions(member)"
                  class="text-xs text-blue-400 hover:text-blue-300 transition-colors"
                >
                  View Details
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>


    </div>

    <!-- Role Definitions -->
    <div class="mt-8 pt-6 border-t border-forest-600">
      <h3 class="text-lg font-medium text-white mb-4">Role Definitions</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="role in roleDefinitions"
          :key="role.name"
          class="p-4 rounded-lg bg-forest-700"
        >
          <div class="flex items-center space-x-2 mb-2">
            <span 
              class="px-2 py-1 rounded text-xs font-medium"
              :class="getRoleBadgeClass(role.name)"
            >
              {{ role.name }}
            </span>
            <span class="text-xs text-gray-400">{{ role.level }}</span>
          </div>
          <p class="text-sm text-gray-300 mb-3">{{ role.description }}</p>
          <div class="space-y-1">
            <div class="text-xs text-gray-400">Key Permissions:</div>
            <ul class="text-xs text-gray-300 space-y-1">
              <li v-for="permission in role.keyPermissions" :key="permission">
                • {{ permission }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useModals } from '../../composables/useModals'
import { useToast } from '../../composables/useToast'
const { success, error } = useToast()
const {
  openTeamInvite,
  openTeamMemberEdit,
  openTeamMemberRemove
} = useModals()

// Team statistics
const teamStats = ref({
  totalMembers: 3,
  activeMembers: 2,
  pendingInvites: 1
})

// Human team members
const humanMembers = ref([
  {
    id: 'user_1',
    name: 'John Doe',
    email: 'john@example.com',
    avatar: '/user-avatars/user1.jpg',
    role: 'Owner',
    status: 'active',
    permissions: ['all']
  },
  {
    id: 'user_2',
    name: 'Sarah Wilson',
    email: 'sarah@example.com',
    avatar: '/user-avatars/user2.jpg',
    role: 'Editor',
    status: 'active',
    permissions: ['content_create', 'content_edit', 'analytics_view']
  },
  {
    id: 'user_3',
    name: 'Mike Chen',
    email: 'mike@example.com',
    avatar: '/user-avatars/user3.jpg',
    role: 'Viewer',
    status: 'pending',
    permissions: ['analytics_view']
  }
])



// Role definitions
const roleDefinitions = ref([
  {
    name: 'Owner',
    level: 'Full Access',
    description: 'Complete control over team, content, and settings',
    keyPermissions: ['Team management', 'Billing', 'All content access', 'AI configuration']
  },
  {
    name: 'Admin',
    level: 'High Access',
    description: 'Manage team members and most content operations',
    keyPermissions: ['Team management', 'Content management', 'Analytics access']
  },
  {
    name: 'Editor',
    level: 'Content Access',
    description: 'Create and edit content, view analytics',
    keyPermissions: ['Content creation', 'Content editing', 'Analytics viewing']
  },
  {
    name: 'Viewer',
    level: 'Read Only',
    description: 'View analytics and reports only',
    keyPermissions: ['Analytics viewing', 'Report access']
  }
])

// Methods
const getRoleBadgeClass = (role) => {
  const classes = {
    'Owner': 'bg-red-500/20 text-red-300',
    'Admin': 'bg-orange-500/20 text-orange-300',
    'Editor': 'bg-blue-500/20 text-blue-300',
    'Viewer': 'bg-gray-500/20 text-gray-300'
  }
  return classes[role] || 'bg-gray-500/20 text-gray-300'
}

const getPermissionsSummary = (permissions) => {
  if (permissions.includes('all')) return 'Full Access'
  return `${permissions.length} permissions`
}

const openInviteModal = () => {
  openTeamInvite()
  success('Team Invitation', 'Opening team member invitation form')
}

const editMemberRole = (member) => {
  openTeamMemberEdit(member)
  success('Edit Member', `Opening role editor for ${member.name}`)
}

const removeMember = (member) => {
  openTeamMemberRemove(member)
  success('Remove Member', `Opening removal confirmation for ${member.name}`)
}

const viewPermissions = (member) => {
  // For now, show detailed permissions in a toast
  // In a real app, this could open a detailed permissions modal
  const permissions = member.permissions.includes('all')
    ? 'Full Access to all features'
    : member.permissions.join(', ')
  success('Member Permissions', `${member.name}: ${permissions}`)
}


</script>
