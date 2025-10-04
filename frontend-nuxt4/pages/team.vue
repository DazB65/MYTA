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
                <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm h-full flex flex-col border-2 border-gray-600/70 shadow-lg">
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
            <!-- Header with Time Range -->
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-xl font-semibold text-white">Team Performance Analytics</h3>
                <p class="text-sm text-gray-400">Monitor your team's productivity and collaboration effectiveness</p>
              </div>
              <div class="text-sm text-gray-400">
                Last updated: {{ new Date().toLocaleDateString() }}
              </div>
            </div>

            <!-- Key Performance Indicators -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div class="bg-gradient-to-r from-green-600/20 to-green-500/20 border border-green-500/30 rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <div>
                    <div class="text-2xl font-bold text-green-400">94%</div>
                    <div class="text-sm text-gray-300">Team Efficiency</div>
                  </div>
                  <div class="text-green-400">
                    <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                </div>
                <div class="text-xs text-green-300 mt-2">+8% from last month</div>
              </div>

              <div class="bg-gradient-to-r from-blue-600/20 to-blue-500/20 border border-blue-500/30 rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <div>
                    <div class="text-2xl font-bold text-blue-400">$12.4K</div>
                    <div class="text-sm text-gray-300">Revenue Impact</div>
                  </div>
                  <div class="text-blue-400">
                    <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z"/>
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                </div>
                <div class="text-xs text-blue-300 mt-2">+23% this quarter</div>
              </div>

              <div class="bg-gradient-to-r from-purple-600/20 to-purple-500/20 border border-purple-500/30 rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <div>
                    <div class="text-2xl font-bold text-purple-400">4.8</div>
                    <div class="text-sm text-gray-300">Content Quality</div>
                  </div>
                  <div class="text-purple-400">
                    <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                    </svg>
                  </div>
                </div>
                <div class="text-xs text-purple-300 mt-2">Average rating</div>
              </div>

              <div class="bg-gradient-to-r from-orange-600/20 to-orange-500/20 border border-orange-500/30 rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <div>
                    <div class="text-2xl font-bold text-orange-400">92%</div>
                    <div class="text-sm text-gray-300">Team Satisfaction</div>
                  </div>
                  <div class="text-orange-400">
                    <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                </div>
                <div class="text-xs text-orange-300 mt-2">Based on feedback</div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <!-- Team Performance Metrics -->
              <div class="bg-gray-900/80 backdrop-blur-sm rounded-xl p-6 border-2 border-gray-600/70 shadow-lg">
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
                    <div class="flex items-center space-x-2">
                      <span class="text-white font-semibold">12</span>
                      <span class="text-xs text-green-400">+3 this week</span>
                    </div>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Completed Tasks</span>
                    <div class="flex items-center space-x-2">
                      <span class="text-white font-semibold">89</span>
                      <span class="text-xs text-gray-400">/ 102 total</span>
                    </div>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Deadline Adherence</span>
                    <span class="text-green-400 font-semibold">96%</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Quality Score</span>
                    <span class="text-yellow-400 font-semibold">4.8/5.0</span>
                  </div>
                </div>
              </div>

              <!-- Communication & Productivity -->
              <div class="bg-gray-900/80 backdrop-blur-sm rounded-xl p-6 border-2 border-gray-600/70 shadow-lg">
                <div class="flex items-center space-x-3 mb-4">
                  <div class="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center">
                    <span class="text-green-400 text-lg">💬</span>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-white">Communication & Productivity</h3>
                    <p class="text-sm text-gray-400">Team interaction & output metrics</p>
                  </div>
                </div>
                <div class="space-y-4">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Messages Today</span>
                    <div class="flex items-center space-x-2">
                      <span class="text-white font-semibold">47</span>
                      <span class="text-xs text-green-400">+12 vs yesterday</span>
                    </div>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Avg Response Time</span>
                    <div class="flex items-center space-x-2">
                      <span class="text-white font-semibold">12m</span>
                      <span class="text-xs text-green-400">-3m improved</span>
                    </div>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Active Discussions</span>
                    <span class="text-blue-400 font-semibold">8</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Daily Output</span>
                    <span class="text-purple-400 font-semibold">2.3 videos</span>
                  </div>
                </div>
              </div>

              <!-- AI Agent ROI & Impact -->
              <div class="bg-gray-900/80 backdrop-blur-sm rounded-xl p-6 border-2 border-gray-600/70 shadow-lg">
                <div class="flex items-center space-x-3 mb-4">
                  <div class="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center">
                    <span class="text-purple-400 text-lg">🤖</span>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-white">AI Agent ROI & Impact</h3>
                    <p class="text-sm text-gray-400">Automation value & cost savings</p>
                  </div>
                </div>
                <div class="space-y-4">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Tasks Automated</span>
                    <div class="flex items-center space-x-2">
                      <span class="text-white font-semibold">156</span>
                      <span class="text-xs text-green-400">+24 this week</span>
                    </div>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Time Saved</span>
                    <div class="flex items-center space-x-2">
                      <span class="text-white font-semibold">23h</span>
                      <span class="text-xs text-gray-400">≈ $920 value</span>
                    </div>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Cost Efficiency</span>
                    <span class="text-green-400 font-semibold">340% ROI</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Agent Utilization</span>
                    <span class="text-blue-400 font-semibold">87%</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Additional Analytics Sections -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Content Performance Overview -->
              <div class="bg-gray-900/80 backdrop-blur-sm rounded-xl p-6 border-2 border-gray-600/70 shadow-lg">
                <div class="flex items-center space-x-3 mb-4">
                  <div class="w-10 h-10 bg-yellow-500/20 rounded-lg flex items-center justify-center">
                    <span class="text-yellow-400 text-lg">📈</span>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-white">Content Performance</h3>
                    <p class="text-sm text-gray-400">Team content creation impact</p>
                  </div>
                </div>
                <div class="space-y-4">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Videos Created</span>
                    <div class="flex items-center space-x-2">
                      <span class="text-white font-semibold">23</span>
                      <span class="text-xs text-green-400">+5 this month</span>
                    </div>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Total Views</span>
                    <div class="flex items-center space-x-2">
                      <span class="text-white font-semibold">1.2M</span>
                      <span class="text-xs text-green-400">+18% growth</span>
                    </div>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Avg Performance</span>
                    <span class="text-yellow-400 font-semibold">Excellent</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Revenue Generated</span>
                    <span class="text-green-400 font-semibold">$8,450</span>
                  </div>
                </div>
              </div>

              <!-- Team Health & Insights -->
              <div class="bg-gray-900/80 backdrop-blur-sm rounded-xl p-6 border-2 border-gray-600/70 shadow-lg">
                <div class="flex items-center space-x-3 mb-4">
                  <div class="w-10 h-10 bg-red-500/20 rounded-lg flex items-center justify-center">
                    <span class="text-red-400 text-lg">❤️</span>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-white">Team Health & Insights</h3>
                    <p class="text-sm text-gray-400">Wellbeing & optimization opportunities</p>
                  </div>
                </div>
                <div class="space-y-4">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Workload Balance</span>
                    <span class="text-green-400 font-semibold">Optimal</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Burnout Risk</span>
                    <span class="text-green-400 font-semibold">Low</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Skill Development</span>
                    <div class="flex items-center space-x-2">
                      <span class="text-white font-semibold">4 areas</span>
                      <span class="text-xs text-blue-400">improving</span>
                    </div>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-300">Collaboration Score</span>
                    <span class="text-purple-400 font-semibold">9.2/10</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Recommendations Section -->
            <div class="bg-gradient-to-r from-blue-600/10 to-purple-600/10 border border-blue-500/20 rounded-xl p-6">
              <div class="flex items-center space-x-3 mb-4">
                <div class="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                  <span class="text-blue-400 text-lg">💡</span>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-white">AI Recommendations for Team Optimization</h3>
                  <p class="text-sm text-gray-400">Data-driven insights to improve team performance</p>
                </div>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-gray-800/50 rounded-lg p-4">
                  <div class="flex items-start space-x-3">
                    <div class="w-6 h-6 bg-green-500/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <span class="text-green-400 text-xs">✓</span>
                    </div>
                    <div>
                      <h4 class="text-white font-medium">Optimize Content Schedule</h4>
                      <p class="text-sm text-gray-400 mt-1">Your team performs 23% better on Tuesday-Thursday. Consider scheduling important tasks during these days.</p>
                    </div>
                  </div>
                </div>
                <div class="bg-gray-800/50 rounded-lg p-4">
                  <div class="flex items-start space-x-3">
                    <div class="w-6 h-6 bg-yellow-500/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <span class="text-yellow-400 text-xs">!</span>
                    </div>
                    <div>
                      <h4 class="text-white font-medium">Increase Agent Collaboration</h4>
                      <p class="text-sm text-gray-400 mt-1">Cross-agent projects show 34% higher success rates. Consider more collaborative workflows.</p>
                    </div>
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
          class="p-4 rounded-xl bg-gray-900/80 backdrop-blur-sm hover:bg-gray-700 transition-colors text-left border-2 border-gray-600/70 shadow-lg"
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
          class="p-4 rounded-xl bg-gray-900/80 backdrop-blur-sm hover:bg-gray-700 transition-colors text-left border-2 border-gray-600/70 shadow-lg"
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
          class="p-4 rounded-xl bg-gray-900/80 backdrop-blur-sm hover:bg-gray-700 transition-colors text-left border-2 border-gray-600/70 shadow-lg"
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
import TabbedChatInterface from '~/components/team/TabbedChatInterface.vue'
import TeamMemberPresence from '~/components/team/TeamMemberPresence.vue'
import TeamRolesManager from '~/components/team/TeamRolesManager.vue'
import { useModals } from '~/composables/useModals'
import { useTeamManagement } from '~/composables/useTeamManagement'
import { useToast } from '~/composables/useToast'

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
