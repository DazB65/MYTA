<template>
  <div class="rounded-xl bg-forest-800 p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-lg bg-indigo-500/20 flex items-center justify-center">
          <span class="text-indigo-400">🎯</span>
        </div>
        <div>
          <h2 class="text-xl font-semibold text-white">Strategic Planning Dashboard</h2>
          <p class="text-gray-400 text-sm">Long-term channel strategy with AI team collaboration</p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <button
          @click="generateStrategy"
          class="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition-colors"
        >
          Generate Strategy
        </button>
        <button
          @click="openTeamStrategy"
          class="rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white hover:bg-purple-700 transition-colors"
        >
          Team Strategy Session
        </button>
      </div>
    </div>

    <!-- Strategy Overview Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="text-center p-4 rounded-lg bg-forest-700">
        <div class="text-2xl font-bold text-indigo-400">{{ strategyMetrics.quarterlyGoals }}</div>
        <div class="text-xs text-gray-400">Quarterly Goals</div>
      </div>
      <div class="text-center p-4 rounded-lg bg-forest-700">
        <div class="text-2xl font-bold text-green-400">{{ strategyMetrics.activePillars }}</div>
        <div class="text-xs text-gray-400">Active Pillars</div>
      </div>
      <div class="text-center p-4 rounded-lg bg-forest-700">
        <div class="text-2xl font-bold text-yellow-400">{{ strategyMetrics.teamInsights }}</div>
        <div class="text-xs text-gray-400">Team Insights</div>
      </div>
      <div class="text-center p-4 rounded-lg bg-forest-700">
        <div class="text-2xl font-bold text-purple-400">{{ strategyMetrics.strategyScore }}%</div>
        <div class="text-xs text-gray-400">Strategy Alignment</div>
      </div>
    </div>

    <!-- Main Strategy Content -->
    <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
      <!-- Enhanced Content Pillars -->
      <div>
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-white">Enhanced Content Pillars</h3>
          <button
            @click="addPillar"
            class="text-sm text-indigo-400 hover:text-indigo-300 transition-colors"
          >
            + Add Pillar
          </button>
        </div>
        
        <div class="space-y-4">
          <div
            v-for="pillar in enhancedPillars"
            :key="pillar.id"
            class="p-4 rounded-lg bg-forest-700 hover:bg-forest-600 transition-colors cursor-pointer"
            @click="openPillarDetails(pillar)"
          >
            <div class="flex items-start justify-between mb-3">
              <div class="flex-1">
                <h4 class="font-medium text-white">{{ pillar.name }}</h4>
                <p class="text-sm text-gray-300 mt-1">{{ pillar.description }}</p>
              </div>
              <span 
                class="px-2 py-1 rounded-full text-xs font-medium"
                :class="getPillarStatusClass(pillar.status)"
              >
                {{ pillar.status }}
              </span>
            </div>

            <!-- AI Team Insights for this Pillar -->
            <div class="mb-3">
              <div class="text-xs text-gray-400 mb-2">AI Team Insights:</div>
              <div class="flex flex-wrap gap-2">
                <div
                  v-for="insight in pillar.aiInsights"
                  :key="insight.id"
                  class="flex items-center space-x-1 px-2 py-1 rounded-lg bg-forest-600 text-xs"
                >
                  <img 
                    :src="insight.agent.avatar" 
                    :alt="insight.agent.name"
                    class="w-4 h-4 rounded-full"
                  />
                  <span class="text-gray-300">{{ insight.suggestion }}</span>
                </div>
              </div>
            </div>

            <!-- Pillar Metrics -->
            <div class="grid grid-cols-3 gap-3 text-center">
              <div>
                <div class="text-sm font-medium text-white">{{ pillar.metrics.videos }}</div>
                <div class="text-xs text-gray-400">Videos</div>
              </div>
              <div>
                <div class="text-sm font-medium text-green-400">{{ pillar.metrics.performance }}%</div>
                <div class="text-xs text-gray-400">Performance</div>
              </div>
              <div>
                <div class="text-sm font-medium text-blue-400">{{ pillar.metrics.potential }}</div>
                <div class="text-xs text-gray-400">Potential</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Long-term Strategy Timeline -->
      <div>
        <h3 class="text-lg font-medium text-white mb-4">Long-term Strategy Timeline</h3>
        
        <div class="space-y-4">
          <div
            v-for="milestone in strategyTimeline"
            :key="milestone.id"
            class="relative"
          >
            <!-- Timeline Line -->
            <div 
              v-if="milestone.id !== strategyTimeline[strategyTimeline.length - 1].id"
              class="absolute left-4 top-8 w-0.5 h-16 bg-forest-600"
            ></div>
            
            <div class="flex items-start space-x-4">
              <!-- Timeline Dot -->
              <div 
                class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 border-2"
                :class="getMilestoneStatusClass(milestone.status)"
              >
                <span class="text-xs">{{ milestone.icon }}</span>
              </div>
              
              <!-- Milestone Content -->
              <div class="flex-1 pb-6">
                <div class="flex items-start justify-between mb-2">
                  <div>
                    <h4 class="font-medium text-white">{{ milestone.title }}</h4>
                    <p class="text-sm text-gray-300">{{ milestone.description }}</p>
                  </div>
                  <span class="text-xs text-gray-400">{{ milestone.timeframe }}</span>
                </div>
                
                <!-- AI Team Recommendations -->
                <div v-if="milestone.teamRecommendations" class="mt-2">
                  <div class="text-xs text-gray-400 mb-1">Team Recommendations:</div>
                  <div class="space-y-1">
                    <div
                      v-for="rec in milestone.teamRecommendations"
                      :key="rec.id"
                      class="flex items-center space-x-2 text-xs"
                    >
                      <div class="flex -space-x-1">
                        <img
                          v-for="agent in rec.agents"
                          :key="agent.id"
                          :src="agent.avatar"
                          :alt="agent.name"
                          class="w-4 h-4 rounded-full border border-forest-600"
                        />
                      </div>
                      <span class="text-gray-300">{{ rec.recommendation }}</span>
                    </div>
                  </div>
                </div>

                <!-- Progress Bar -->
                <div class="mt-3">
                  <div class="flex items-center justify-between text-xs text-gray-400 mb-1">
                    <span>Progress</span>
                    <span>{{ milestone.progress }}%</span>
                  </div>
                  <div class="w-full bg-forest-600 rounded-full h-2">
                    <div 
                      class="h-2 rounded-full transition-all duration-300"
                      :class="getProgressBarClass(milestone.status)"
                      :style="{ width: `${milestone.progress}%` }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Strategy Insights from AI Team -->
    <div class="mt-8 pt-6 border-t border-forest-600">
      <h3 class="text-lg font-medium text-white mb-4">AI Team Strategy Insights</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="insight in strategyInsights"
          :key="insight.id"
          class="p-4 rounded-lg bg-forest-700"
        >
          <div class="flex items-start space-x-3">
            <div class="flex -space-x-1 flex-shrink-0">
              <img
                v-for="agent in insight.collaboratingAgents"
                :key="agent.id"
                :src="agent.avatar"
                :alt="agent.name"
                class="w-6 h-6 rounded-full border border-forest-600"
              />
            </div>
            <div class="flex-1">
              <h4 class="font-medium text-white mb-1">{{ insight.title }}</h4>
              <p class="text-sm text-gray-300 mb-2">{{ insight.description }}</p>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-400">
                  {{ insight.collaboratingAgents.length }} agents collaborated
                </span>
                <button
                  @click="implementInsight(insight)"
                  class="text-xs px-3 py-1 rounded-lg bg-indigo-500/20 text-indigo-300 hover:bg-indigo-500/30 transition-colors"
                >
                  Implement
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Strategy metrics
const strategyMetrics = ref({
  quarterlyGoals: 8,
  activePillars: 5,
  teamInsights: 12,
  strategyScore: 92
})

// Enhanced content pillars with AI insights
const enhancedPillars = ref([
  {
    id: 1,
    name: 'Educational Content',
    description: 'In-depth tutorials and how-to guides',
    status: 'Active',
    metrics: {
      videos: 24,
      performance: 87,
      potential: 'High'
    },
    aiInsights: [
      {
        id: 1,
        agent: { name: 'Alex', avatar: '/optimized/Agent1.jpg' },
        suggestion: 'Increase tutorial length by 2-3 minutes'
      },
      {
        id: 2,
        agent: { name: 'Levi', avatar: '/optimized/Agent2.jpg' },
        suggestion: 'Add visual diagrams for better engagement'
      }
    ]
  },
  {
    id: 2,
    name: 'Industry Insights',
    description: 'Analysis and commentary on industry trends',
    status: 'Growing',
    metrics: {
      videos: 16,
      performance: 94,
      potential: 'Very High'
    },
    aiInsights: [
      {
        id: 3,
        agent: { name: 'Maya', avatar: '/optimized/Agent3.jpg' },
        suggestion: 'Focus on controversial topics for engagement'
      },
      {
        id: 4,
        agent: { name: 'Zara', avatar: '/optimized/Agent4.jpg' },
        suggestion: 'Optimize posting schedule for maximum reach'
      }
    ]
  }
])

// Strategy timeline with team recommendations
const strategyTimeline = ref([
  {
    id: 1,
    title: 'Q1 Content Foundation',
    description: 'Establish core content pillars and team workflows',
    timeframe: 'Jan - Mar 2024',
    status: 'completed',
    progress: 100,
    icon: '✅',
    teamRecommendations: [
      {
        id: 1,
        agents: [
          { id: 'agent_1', name: 'Alex', avatar: '/optimized/Agent1.jpg' },
          { id: 'agent_2', name: 'Levi', avatar: '/optimized/Agent2.jpg' }
        ],
        recommendation: 'Focus on educational content for foundation building'
      }
    ]
  },
  {
    id: 2,
    title: 'Q2 Growth Acceleration',
    description: 'Scale content production and optimize for viral potential',
    timeframe: 'Apr - Jun 2024',
    status: 'in-progress',
    progress: 65,
    icon: '🚀',
    teamRecommendations: [
      {
        id: 2,
        agents: [
          { id: 'agent_3', name: 'Maya', avatar: '/optimized/Agent3.jpg' },
          { id: 'agent_4', name: 'Zara', avatar: '/optimized/Agent4.jpg' }
        ],
        recommendation: 'Implement trending topic integration strategy'
      }
    ]
  },
  {
    id: 3,
    title: 'Q3 Monetization Focus',
    description: 'Optimize revenue streams and brand partnerships',
    timeframe: 'Jul - Sep 2024',
    status: 'planned',
    progress: 0,
    icon: '💰',
    teamRecommendations: [
      {
        id: 3,
        agents: [
          { id: 'agent_5', name: 'Kai', avatar: '/optimized/Agent5.jpg' },
          { id: 'agent_1', name: 'Alex', avatar: '/optimized/Agent1.jpg' }
        ],
        recommendation: 'Develop premium content tier and sponsorship strategy'
      }
    ]
  }
])

// AI team strategy insights
const strategyInsights = ref([
  {
    id: 1,
    title: 'Cross-Pillar Content Opportunities',
    description: 'Alex and Levi identified 3 content ideas that bridge multiple pillars for maximum impact.',
    collaboratingAgents: [
      { id: 'agent_1', name: 'Alex', avatar: '/optimized/Agent1.jpg' },
      { id: 'agent_2', name: 'Levi', avatar: '/optimized/Agent2.jpg' }
    ]
  },
  {
    id: 2,
    title: 'Audience Engagement Optimization',
    description: 'Maya and Zara developed a strategy to increase audience retention by 23% through interactive elements.',
    collaboratingAgents: [
      { id: 'agent_3', name: 'Maya', avatar: '/optimized/Agent3.jpg' },
      { id: 'agent_4', name: 'Zara', avatar: '/optimized/Agent4.jpg' }
    ]
  }
])

// Methods
const getPillarStatusClass = (status) => {
  const classes = {
    'Active': 'bg-green-500/20 text-green-300',
    'Growing': 'bg-blue-500/20 text-blue-300',
    'Planning': 'bg-yellow-500/20 text-yellow-300'
  }
  return classes[status] || 'bg-gray-500/20 text-gray-300'
}

const getMilestoneStatusClass = (status) => {
  const classes = {
    'completed': 'bg-green-500 border-green-500 text-white',
    'in-progress': 'bg-blue-500 border-blue-500 text-white',
    'planned': 'bg-forest-600 border-forest-400 text-gray-300'
  }
  return classes[status] || 'bg-gray-500 border-gray-500 text-white'
}

const getProgressBarClass = (status) => {
  const classes = {
    'completed': 'bg-green-500',
    'in-progress': 'bg-blue-500',
    'planned': 'bg-gray-500'
  }
  return classes[status] || 'bg-gray-500'
}

const generateStrategy = () => {
  console.log('Generating AI team strategy')
  // TODO: Implement AI strategy generation
}

const openTeamStrategy = () => {
  console.log('Opening team strategy session')
  // TODO: Open team strategy modal
}

const addPillar = () => {
  console.log('Adding new pillar')
  // TODO: Open pillar creation modal
}

const openPillarDetails = (pillar) => {
  console.log('Opening pillar details:', pillar.name)
  // TODO: Open pillar details modal
}

const implementInsight = (insight) => {
  console.log('Implementing insight:', insight.title)
  // TODO: Implement insight action
}
</script>
