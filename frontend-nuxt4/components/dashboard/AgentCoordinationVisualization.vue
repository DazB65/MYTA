<template>
  <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-lg bg-purple-500/20 flex items-center justify-center">
          <span class="text-purple-400">🔗</span>
        </div>
        <div>
          <h2 class="text-xl font-semibold text-white">Agent Coordination</h2>
          <p class="text-gray-400 text-sm">Real-time team collaboration network</p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <button
          @click="toggleLiveMode"
          :class="[
            'px-3 py-1 rounded-lg text-xs font-medium transition-colors',
            isLiveMode ? 'bg-green-500/20 text-green-300' : 'bg-gray-500/20 text-gray-300'
          ]"
        >
          {{ isLiveMode ? 'Live' : 'Paused' }}
        </button>
        <button
          @click="showCoordinationDetails"
          class="rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white hover:bg-purple-700 transition-colors"
        >
          View Details
        </button>
      </div>
    </div>

    <!-- Coordination Network Visualization -->
    <div class="relative mb-6">
      <div class="bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg rounded-lg p-6 min-h-[300px] relative overflow-hidden">
        <!-- Central Hub (Boss Agent) -->
        <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
          <div class="relative">
            <div 
              class="w-16 h-16 rounded-full border-4 border-orange-400 bg-gray-700 flex items-center justify-center"
              :class="{ 'animate-pulse': isLiveMode }"
            >
              <img 
                src="/BossAgent.png" 
                alt="Boss Agent"
                class="w-10 h-10 rounded-full object-cover"
              />
            </div>
            <div class="absolute -bottom-8 left-1/2 transform -translate-x-1/2 text-center">
              <div class="text-white text-sm font-medium">Boss Agent</div>
              <div class="text-gray-400 text-xs">Team Leader</div>
            </div>
          </div>
        </div>

        <!-- Surrounding Agents -->
        <div
          v-for="(agent, index) in coordinatingAgents"
          :key="agent.id"
          class="absolute"
          :style="getAgentPosition(index)"
        >
          <div class="relative">
            <!-- Connection Line to Center -->
            <svg 
              class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 pointer-events-none"
              :width="getConnectionDistance(index)"
              :height="getConnectionDistance(index)"
              style="z-index: 1;"
            >
              <line
                :x1="getConnectionDistance(index) / 2"
                :y1="getConnectionDistance(index) / 2"
                :x2="getCenterX(index)"
                :y2="getCenterY(index)"
                :stroke="agent.color"
                stroke-width="2"
                :class="{ 'animate-pulse': agent.isActive }"
                opacity="0.6"
              />
              <!-- Data flow animation -->
              <circle
                v-if="agent.isActive && isLiveMode"
                :cx="getCenterX(index)"
                :cy="getCenterY(index)"
                r="3"
                :fill="agent.color"
                class="animate-ping"
              />
            </svg>

            <!-- Agent Node -->
            <div 
              class="relative z-10 cursor-pointer transform transition-transform hover:scale-110"
              @click="selectAgent(agent)"
            >
              <div 
                class="w-12 h-12 rounded-full border-3 bg-forest-700 flex items-center justify-center"
                :style="{ borderColor: agent.color }"
                :class="{ 'animate-pulse': agent.isActive }"
              >
                <img 
                  :src="agent.avatar" 
                  :alt="agent.name"
                  class="w-8 h-8 rounded-full object-cover"
                />
              </div>
              
              <!-- Activity Indicator -->
              <div 
                v-if="agent.isActive"
                class="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-green-400 border-2 border-forest-800 animate-pulse"
              ></div>
              
              <!-- Agent Info -->
              <div class="absolute -bottom-12 left-1/2 transform -translate-x-1/2 text-center min-w-max">
                <div class="text-white text-xs font-medium">{{ agent.name }}</div>
                <div class="text-gray-400 text-xs">{{ agent.currentTask }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Collaboration Connections -->
        <svg 
          class="absolute inset-0 pointer-events-none"
          width="100%"
          height="100%"
          style="z-index: 2;"
        >
          <defs>
            <marker
              id="arrowhead"
              markerWidth="10"
              markerHeight="7"
              refX="9"
              refY="3.5"
              orient="auto"
            >
              <polygon
                points="0 0, 10 3.5, 0 7"
                fill="#60a5fa"
                opacity="0.7"
              />
            </marker>
          </defs>
          
          <!-- Inter-agent collaboration lines -->
          <line
            v-for="connection in activeConnections"
            :key="`${connection.from}-${connection.to}`"
            :x1="getAgentCoordinate(connection.from, 'x')"
            :y1="getAgentCoordinate(connection.from, 'y')"
            :x2="getAgentCoordinate(connection.to, 'x')"
            :y2="getAgentCoordinate(connection.to, 'y')"
            stroke="#60a5fa"
            stroke-width="2"
            stroke-dasharray="5,5"
            opacity="0.5"
            marker-end="url(#arrowhead)"
            class="animate-pulse"
          />
        </svg>
      </div>
    </div>

    <!-- Current Coordination Activities -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Active Collaborations -->
      <div>
        <h3 class="text-lg font-medium text-white mb-3">Active Collaborations</h3>
        <div class="space-y-3">
          <div
            v-for="collaboration in activeCollaborations"
            :key="collaboration.id"
            class="p-3 rounded-lg bg-forest-700 border-l-4"
            :style="{ borderLeftColor: collaboration.color }"
          >
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-white">{{ collaboration.task }}</span>
              <span class="text-xs px-2 py-1 rounded-full bg-blue-500/20 text-blue-300">
                Active
              </span>
            </div>
            <div class="flex items-center space-x-2 mb-2">
              <div class="flex -space-x-1">
                <img
                  v-for="agent in collaboration.agents"
                  :key="agent.id"
                  :src="agent.avatar"
                  :alt="agent.name"
                  class="w-5 h-5 rounded-full border border-forest-600"
                  :title="agent.name"
                />
              </div>
              <span class="text-xs text-gray-400">
                {{ collaboration.agents.length }} agents collaborating
              </span>
            </div>
            <div class="w-full bg-forest-600 rounded-full h-2">
              <div 
                class="bg-blue-500 h-2 rounded-full transition-all duration-300"
                :style="{ width: `${collaboration.progress}%` }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Coordination Insights -->
      <div>
        <h3 class="text-lg font-medium text-white mb-3">Coordination Insights</h3>
        <div class="space-y-3">
          <div
            v-for="insight in coordinationInsights"
            :key="insight.id"
            class="p-3 rounded-lg bg-forest-700"
          >
            <div class="flex items-start space-x-3">
              <div 
                class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                :style="{ backgroundColor: insight.color + '20' }"
              >
                <span class="text-sm">{{ insight.icon }}</span>
              </div>
              <div class="flex-1">
                <h4 class="font-medium text-white text-sm">{{ insight.title }}</h4>
                <p class="text-xs text-gray-300 mt-1">{{ insight.description }}</p>
                <span class="text-xs text-gray-400">{{ insight.time }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAgentsStore } from '../../stores/agents'

const agentsStore = useAgentsStore()
const isLiveMode = ref(true)

// Coordinating agents (excluding Boss Agent)
const coordinatingAgents = computed(() => 
  agentsStore.allAgents.filter(agent => agent.id !== 'boss_agent').map((agent, index) => ({
    ...agent,
    isActive: index < 3, // First 3 agents are active
    currentTask: ['Analyzing content', 'Creating thumbnails', 'Optimizing engagement', 'Planning strategy', 'Technical review'][index] || 'Standby'
  }))
)

// Active connections between agents
const activeConnections = ref([
  { from: 0, to: 1 }, // Alex to Levi
  { from: 1, to: 2 }, // Levi to Maya
  { from: 2, to: 3 }  // Maya to Zara
])

// Active collaborations
const activeCollaborations = ref([
  {
    id: 1,
    task: 'Content Strategy Optimization',
    color: '#3b82f6',
    progress: 75,
    agents: [
      { id: 'agent_1', name: 'Alex', avatar: '/optimized/Agent1.jpg' },
      { id: 'agent_2', name: 'Levi', avatar: '/optimized/Agent2.jpg' }
    ]
  },
  {
    id: 2,
    task: 'Audience Engagement Analysis',
    color: '#a855f7',
    progress: 60,
    agents: [
      { id: 'agent_3', name: 'Maya', avatar: '/optimized/Agent3.jpg' },
      { id: 'agent_4', name: 'Zara', avatar: '/optimized/Agent4.jpg' }
    ]
  }
])

// Coordination insights
const coordinationInsights = ref([
  {
    id: 1,
    title: 'Efficient Collaboration',
    description: 'Alex and Levi completed content analysis 23% faster through coordination',
    color: '#10b981',
    icon: '⚡',
    time: '5 min ago'
  },
  {
    id: 2,
    title: 'Cross-Agent Learning',
    description: 'Maya adopted optimization techniques from Zara for better engagement',
    color: '#f59e0b',
    icon: '🧠',
    time: '12 min ago'
  }
])

// Position calculation for agents in circle
const getAgentPosition = (index) => {
  const angle = (index * 2 * Math.PI) / coordinatingAgents.value.length
  const radius = 120
  const centerX = 50 // percentage
  const centerY = 50 // percentage
  
  const x = centerX + (radius * Math.cos(angle)) / 3 // Adjust for container size
  const y = centerY + (radius * Math.sin(angle)) / 3
  
  return {
    left: `${x}%`,
    top: `${y}%`,
    transform: 'translate(-50%, -50%)'
  }
}

// Connection distance calculation
const getConnectionDistance = (index) => {
  return 240 // Fixed distance for SVG
}

// Center coordinates for connections
const getCenterX = (index) => {
  return 120 // Half of connection distance
}

const getCenterY = (index) => {
  return 120 // Half of connection distance
}

// Get agent coordinates for inter-agent connections
const getAgentCoordinate = (agentIndex, coordinate) => {
  const angle = (agentIndex * 2 * Math.PI) / coordinatingAgents.value.length
  const radius = 120
  const centerX = 300 // Approximate center of container
  const centerY = 150
  
  if (coordinate === 'x') {
    return centerX + radius * Math.cos(angle)
  } else {
    return centerY + radius * Math.sin(angle)
  }
}

// Methods
const toggleLiveMode = () => {
  isLiveMode.value = !isLiveMode.value
}

const showCoordinationDetails = () => {
  console.log('Showing coordination details')
  // TODO: Implement coordination details modal
}

const selectAgent = (agent) => {
  console.log('Selected agent:', agent.name)
  // TODO: Implement agent selection/details
}
</script>

<style scoped>
@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

.animate-ping {
  animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
}
</style>
