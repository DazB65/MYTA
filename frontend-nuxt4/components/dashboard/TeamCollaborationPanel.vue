<template>
  <div class="rounded-xl bg-forest-800 p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center">
          <span class="text-blue-400">👥</span>
        </div>
        <div>
          <h2 class="text-xl font-semibold text-white">AI Team Collaboration</h2>
          <p class="text-gray-400 text-sm">Your AI team working together</p>
        </div>
      </div>
      <button
        @click="openTeamConference"
        class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 transition-colors"
      >
        Team Conference
      </button>
    </div>

    <!-- Active Team Members -->
    <div class="mb-6">
      <h3 class="text-lg font-medium text-white mb-3">Active Team Members</h3>
      <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
        <div
          v-for="agent in activeAgents"
          :key="agent.id"
          class="flex flex-col items-center p-3 rounded-lg bg-forest-700 hover:bg-forest-600 transition-colors cursor-pointer"
          :style="{ borderLeft: `3px solid ${agent.color}` }"
          @click="viewAgentActivity(agent)"
        >
          <img 
            :src="agent.avatar" 
            :alt="agent.name"
            class="w-10 h-10 rounded-lg object-cover mb-2"
          />
          <span class="text-white text-sm font-medium">{{ agent.name }}</span>
          <span class="text-gray-400 text-xs">{{ agent.specialization }}</span>
          <div class="flex items-center mt-1">
            <div 
              :class="[
                'w-2 h-2 rounded-full',
                agent.status === 'active' ? 'bg-green-400' : 'bg-gray-400'
              ]"
            ></div>
            <span class="text-xs text-gray-400 ml-1">{{ agent.status }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Team Collaboration Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent Team Insights -->
      <div>
        <h3 class="text-lg font-medium text-white mb-3">Team Insights</h3>
        <div class="space-y-3">
          <div
            v-for="insight in teamInsights"
            :key="insight.id"
            class="p-4 rounded-lg bg-forest-700 border-l-4"
            :style="{ borderLeftColor: insight.color }"
          >
            <div class="flex items-start justify-between mb-2">
              <div class="flex items-center space-x-2">
                <span class="text-sm font-medium text-white">{{ insight.title }}</span>
                <span class="text-xs px-2 py-1 rounded-full bg-blue-500/20 text-blue-300">
                  Team Collaboration
                </span>
              </div>
              <span class="text-xs text-gray-400">{{ insight.time }}</span>
            </div>
            <p class="text-sm text-gray-300 mb-2">{{ insight.description }}</p>
            <div class="flex items-center space-x-2">
              <div class="flex -space-x-1">
                <img
                  v-for="agent in insight.contributors"
                  :key="agent.id"
                  :src="agent.avatar"
                  :alt="agent.name"
                  class="w-5 h-5 rounded-full border border-forest-600"
                  :title="agent.name"
                />
              </div>
              <span class="text-xs text-gray-400">
                {{ insight.contributors.length }} team members collaborated
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Shared Content Planning -->
      <div>
        <h3 class="text-lg font-medium text-white mb-3">Shared Content Planning</h3>
        <div class="space-y-3">
          <div
            v-for="plan in sharedPlans"
            :key="plan.id"
            class="p-4 rounded-lg bg-forest-700 hover:bg-forest-600 transition-colors cursor-pointer"
            @click="openSharedPlan(plan)"
          >
            <div class="flex items-start justify-between mb-2">
              <h4 class="font-medium text-white">{{ plan.title }}</h4>
              <span class="text-xs px-2 py-1 rounded-full bg-green-500/20 text-green-300">
                {{ plan.status }}
              </span>
            </div>
            <p class="text-sm text-gray-300 mb-3">{{ plan.description }}</p>
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="flex -space-x-1">
                  <img
                    v-for="agent in plan.assignedAgents"
                    :key="agent.id"
                    :src="agent.avatar"
                    :alt="agent.name"
                    class="w-5 h-5 rounded-full border border-forest-600"
                    :title="agent.name"
                  />
                </div>
                <span class="text-xs text-gray-400">Team assigned</span>
              </div>
              <span class="text-xs text-gray-400">Due {{ plan.dueDate }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Team Performance Metrics -->
    <div class="mt-6 pt-6 border-t border-forest-600/30">
      <h3 class="text-lg font-medium text-white mb-3">Team Performance</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="text-center p-3 rounded-lg bg-forest-700">
          <div class="text-2xl font-bold text-blue-400">{{ teamMetrics.collaborations }}</div>
          <div class="text-xs text-gray-400">Team Collaborations</div>
        </div>
        <div class="text-center p-3 rounded-lg bg-forest-700">
          <div class="text-2xl font-bold text-green-400">{{ teamMetrics.insights }}</div>
          <div class="text-xs text-gray-400">Shared Insights</div>
        </div>
        <div class="text-center p-3 rounded-lg bg-forest-700">
          <div class="text-2xl font-bold text-yellow-400">{{ teamMetrics.plans }}</div>
          <div class="text-xs text-gray-400">Active Plans</div>
        </div>
        <div class="text-center p-3 rounded-lg bg-forest-700">
          <div class="text-2xl font-bold text-purple-400">{{ teamMetrics.efficiency }}%</div>
          <div class="text-xs text-gray-400">Team Efficiency</div>
        </div>
      </div>
    </div>

    <!-- Agent Conference Modal -->
    <AgentConferenceModal
      :is-open="showConferenceModal"
      @close="showConferenceModal = false"
    />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAgentsStore } from '../../stores/agents'
import AgentConferenceModal from './AgentConferenceModal.vue'

const agentsStore = useAgentsStore()

// Modal state
const showConferenceModal = ref(false)

// Active agents (team members)
const activeAgents = computed(() => 
  agentsStore.allAgents.filter(agent => agent.status === 'online').map(agent => ({
    ...agent,
    status: 'active',
    specialization: agent.specialization || 'Team Member'
  }))
)

// Sample team insights data
const teamInsights = ref([
  {
    id: 1,
    title: 'Content Strategy Alignment',
    description: 'Alex and Levi collaborated on optimizing your video titles for better CTR while maintaining creative appeal.',
    color: '#3b82f6',
    time: '2 hours ago',
    contributors: [
      { id: 'agent_1', name: 'Alex', avatar: '/optimized/Agent1.jpg' },
      { id: 'agent_2', name: 'Levi', avatar: '/optimized/Agent2.jpg' }
    ]
  },
  {
    id: 2,
    title: 'Audience Engagement Strategy',
    description: 'Maya and Zara worked together to identify optimal posting times and engagement tactics for your audience.',
    color: '#a855f7',
    time: '4 hours ago',
    contributors: [
      { id: 'agent_3', name: 'Maya', avatar: '/optimized/Agent3.jpg' },
      { id: 'agent_4', name: 'Zara', avatar: '/optimized/Agent4.jpg' }
    ]
  }
])

// Sample shared content plans
const sharedPlans = ref([
  {
    id: 1,
    title: 'Q1 Content Series',
    description: 'Collaborative planning for educational content series with team input on topics, timing, and optimization.',
    status: 'In Progress',
    dueDate: 'Mar 15',
    assignedAgents: [
      { id: 'agent_1', name: 'Alex', avatar: '/Alex.png' },
      { id: 'agent_2', name: 'Levi', avatar: '/Levi.png' },
      { id: 'agent_3', name: 'Maya', avatar: '/Maya.png' }
    ]
  },
  {
    id: 2,
    title: 'Thumbnail A/B Testing',
    description: 'Team collaboration on thumbnail design variations and performance testing strategy.',
    status: 'Planning',
    dueDate: 'Mar 10',
    assignedAgents: [
      { id: 'agent_2', name: 'Levi', avatar: '/optimized/Agent2.jpg' },
      { id: 'agent_4', name: 'Zara', avatar: '/optimized/Agent4.jpg' }
    ]
  }
])

// Team performance metrics
const teamMetrics = ref({
  collaborations: 24,
  insights: 18,
  plans: 6,
  efficiency: 94
})

// Methods
const openTeamConference = () => {
  showConferenceModal.value = true
}

const viewAgentActivity = (agent) => {
  console.log('Viewing activity for agent:', agent.name)
  // TODO: Implement agent activity view
}

const openSharedPlan = (plan) => {
  console.log('Opening shared plan:', plan.title)
  // TODO: Implement shared plan modal
}
</script>
