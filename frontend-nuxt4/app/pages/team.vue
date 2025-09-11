<template>
  <div class="min-h-screen bg-gradient-to-b from-slate-800 via-gray-850 to-gray-900 text-white">
    <!-- Header -->
    <div class="p-6 pt-24">
      <!-- Page Header -->
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-white">Team Management</h1>
        <p class="text-gray-400">Manage your team members, roles, and collaborative workflows</p>
      </div>



      <!-- Tabbed Interface -->
      <div class="bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg rounded-xl overflow-hidden">
        <!-- Tab Navigation -->
        <div class="flex border-b border-gray-700">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            class="flex items-center space-x-2 px-6 py-4 text-sm font-medium transition-colors duration-200"
            :class="activeTab === tab.id
              ? 'bg-gray-700 text-white border-b-2 border-blue-500'
              : 'text-gray-400 hover:text-white hover:bg-gray-700/50'"
          >
            <span class="text-lg">{{ tab.icon }}</span>
            <span>{{ tab.name }}</span>
            <span v-if="tab.badge" class="bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
              {{ tab.badge }}
            </span>
          </button>
        </div>

        <!-- Tab Content -->
        <div class="p-6 h-[calc(100vh-280px)] overflow-y-auto">
          <!-- Team Management Tab -->
          <div v-if="activeTab === 'management'" class="space-y-6">
            <TeamRolesManager />
          </div>

          <!-- Chat & Communication Tab -->
          <div v-if="activeTab === 'chat'" class="h-full">
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
              <!-- Tabbed Chat Interface - Takes up 2 columns -->
              <div class="lg:col-span-2 h-full">
                <div class="rounded-xl bg-gray-700 h-full flex flex-col">
                  <TabbedChatInterface ref="tabbedChatRef" :team-id="'demo_team_123'" />
                </div>
              </div>

              <!-- Member Presence - Takes up 1 column -->
              <div class="lg:col-span-1">
                <TeamMemberPresence @start-direct-message="handleStartDirectMessage" />
              </div>
            </div>
          </div>



          <!-- Analytics Tab -->
          <div v-if="activeTab === 'analytics'" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <!-- Team Performance Metrics -->
              <div class="bg-gray-700 rounded-xl p-6">
                <div class="flex items-center space-x-3 mb-4">
                  <div class="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                    <span class="text-blue-400 text-lg">📊</span>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-white">Team Performance</h3>
                    <p class="text-sm text-gray-400">Collaboration metrics</p>
                  </div>
                </div>
                <div class="space-y-4">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Active Projects</span>
                    <span class="text-white font-semibold">12</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Completed Tasks</span>
                    <span class="text-white font-semibold">89</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Team Efficiency</span>
                    <span class="text-green-400 font-semibold">94%</span>
                  </div>
                </div>
              </div>

              <!-- Communication Stats -->
              <div class="bg-gray-700 rounded-xl p-6">
                <div class="flex items-center space-x-3 mb-4">
                  <div class="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center">
                    <span class="text-green-400 text-lg">💬</span>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-white">Communication</h3>
                    <p class="text-sm text-gray-400">Team interaction stats</p>
                  </div>
                </div>
                <div class="space-y-4">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Messages Today</span>
                    <span class="text-white font-semibold">47</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Response Time</span>
                    <span class="text-white font-semibold">12m</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Active Discussions</span>
                    <span class="text-blue-400 font-semibold">8</span>
                  </div>
                </div>
              </div>

              <!-- AI Agent Activity -->
              <div class="bg-gray-700 rounded-xl p-6">
                <div class="flex items-center space-x-3 mb-4">
                  <div class="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center">
                    <span class="text-purple-400 text-lg">🤖</span>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-white">AI Agent Activity</h3>
                    <p class="text-sm text-gray-400">Automation insights</p>
                  </div>
                </div>
                <div class="space-y-4">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Tasks Automated</span>
                    <span class="text-white font-semibold">156</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Time Saved</span>
                    <span class="text-white font-semibold">23h</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Efficiency Gain</span>
                    <span class="text-green-400 font-semibold">+34%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <button
          @click="createTeamProject"
          class="p-4 rounded-xl bg-gray-800 hover:bg-gray-700 transition-colors text-left"
        >
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center">
              <span class="text-green-400">📋</span>
            </div>
            <div>
              <div class="text-white font-medium">New Project</div>
              <div class="text-gray-400 text-sm">Create team project</div>
            </div>
          </div>
        </button>

        <button
          @click="viewTeamAnalytics"
          class="p-4 rounded-xl bg-gray-800 hover:bg-gray-700 transition-colors text-left"
        >
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center">
              <span class="text-blue-400">📊</span>
            </div>
            <div>
              <div class="text-white font-medium">Team Analytics</div>
              <div class="text-gray-400 text-sm">View collaboration metrics</div>
            </div>
          </div>
        </button>

        <button
          @click="managePermissions"
          class="p-4 rounded-xl bg-gray-800 hover:bg-gray-700 transition-colors text-left"
        >
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-lg bg-orange-500/20 flex items-center justify-center">
              <span class="text-orange-400">🔐</span>
            </div>
            <div>
              <div class="text-white font-medium">Permissions</div>
              <div class="text-gray-400 text-sm">Manage access control</div>
            </div>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, ref } from 'vue'
import { useRouter } from 'vue-router'
import TabbedChatInterface from '../../components/team/TabbedChatInterface.vue'
import TeamMemberPresence from '../../components/team/TeamMemberPresence.vue'
import TeamRolesManager from '../../components/team/TeamRolesManager.vue'
import { useModals } from '../../composables/useModals'
import { useTeamManagement } from '../../composables/useTeamManagement'
import { useToast } from '../../composables/useToast'

// Page metadata
definePageMeta({
  title: 'Team Management - MYTA',
  description: 'Manage your team members, roles, and collaborative workflows'
})

// Composables
const router = useRouter()
const { success, error } = useToast()
const {
  openTask,
  openTeamInvite,
  openTeamEdit,
  openTeamMemberEdit,
  openTeamMemberRemove
} = useModals()
const {
  currentTeam,
  loading,
  fetchMyTeam,
  createTeam,
  inviteMember,
  isTeamOwner,
  canInviteMembers
} = useTeamManagement()

// Tab state
const activeTab = ref('management')

// Chat interface ref
const tabbedChatRef = ref(null)

// Tab definitions
const tabs = computed(() => [
  {
    id: 'management',
    name: 'Team Management',
    icon: '👥',
    badge: null
  },
  {
    id: 'chat',
    name: 'Chat & Communication',
    icon: '💬',
    badge: 2 // Unread messages count
  },

  {
    id: 'analytics',
    name: 'Team Analytics',
    icon: '📊',
    badge: null
  }
])

// Methods

const createTeamProject = () => {
  // Open the task modal to create a new team project
  // This reuses the existing task creation functionality but for team projects
  openTask({
    title: '',
    description: '',
    priority: 'medium',
    assignedTo: 'team',
    isTeamProject: true
  })
  success('Project Creation', 'Opening project creation form')
}

const viewTeamAnalytics = () => {
  // Navigate to analytics page with team filter
  router.push('/analytics/charts?filter=team')
  success('Team Analytics', 'Navigating to team performance metrics')
}

const managePermissions = () => {
  // Open team edit modal to manage permissions and roles
  if (currentTeam.value) {
    openTeamEdit(currentTeam.value)
    success('Permissions Manager', 'Opening team permissions and roles management')
  } else {
    error('No Team Found', 'Please create or join a team first')
  }
}

// Additional team management functions
const inviteTeamMember = () => {
  if (canInviteMembers.value) {
    openTeamInvite()
    success('Team Invitation', 'Opening team member invitation form')
  } else {
    error('Permission Denied', 'You do not have permission to invite team members')
  }
}

const editTeamSettings = () => {
  if (currentTeam.value && isTeamOwner.value) {
    openTeamEdit(currentTeam.value)
    success('Team Settings', 'Opening team configuration')
  } else {
    error('Permission Denied', 'Only team owners can edit team settings')
  }
}

// Handle starting direct message from team member presence
const handleStartDirectMessage = (member) => {
  // Switch to chat tab if not already active
  if (activeTab.value !== 'chat') {
    activeTab.value = 'chat'
  }

  // Wait for next tick to ensure the chat component is rendered
  nextTick(() => {
    if (tabbedChatRef.value && tabbedChatRef.value.startDirectMessage) {
      tabbedChatRef.value.startDirectMessage(member)
    }
  })
}
</script>
