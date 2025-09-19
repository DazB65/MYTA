<template>
  <div class="bg-forest-800 rounded-lg border border-forest-600 p-4">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-3">
        <img 
          :src="selectedAgent.avatar" 
          :alt="selectedAgent.name"
          class="w-8 h-8 rounded-lg border-2"
          :style="{ borderColor: selectedAgent.color }"
        />
        <div>
          <h3 class="font-semibold text-white">{{ selectedAgent.name }} Insights</h3>
          <p class="text-xs text-gray-400">{{ selectedAgent.specialization }}</p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <select 
          v-model="selectedAgentId" 
          @change="switchAgent"
          class="bg-forest-700 border border-forest-600 rounded px-2 py-1 text-sm text-white"
        >
          <option v-for="agent in agents" :key="agent.id" :value="agent.id">
            {{ agent.name }}
          </option>
        </select>
        <button
          @click="generateInsights"
          :disabled="isGenerating"
          class="px-3 py-1 bg-orange-500 text-white rounded text-sm hover:bg-orange-600 disabled:opacity-50 transition-colors"
        >
          {{ isGenerating ? 'Analyzing...' : 'Analyze' }}
        </button>
      </div>
    </div>

    <!-- Agent-Specific Insights -->
    <div class="space-y-3">
      <!-- Loading State -->
      <div v-if="isGenerating" class="flex items-center justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2" :style="{ borderColor: selectedAgent.color }"></div>
      </div>

      <!-- Insights Content -->
      <div v-else-if="insights.length > 0" class="space-y-3">
        <div
          v-for="insight in insights"
          :key="insight.id"
          class="p-3 rounded-lg border-l-4 bg-forest-700"
          :style="{ borderLeftColor: selectedAgent.color }"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-2 mb-1">
                <span class="text-sm font-medium" :style="{ color: selectedAgent.color }">
                  {{ insight.type }}
                </span>
                <span class="text-xs px-2 py-1 rounded-full bg-forest-600 text-gray-300">
                  {{ insight.confidence }}% confidence
                </span>
              </div>
              <p class="text-sm text-gray-200 mb-2">{{ insight.description }}</p>
              <div v-if="insight.actionItems?.length" class="space-y-1">
                <p class="text-xs font-medium text-gray-300">Recommended Actions:</p>
                <ul class="text-xs text-gray-400 space-y-1">
                  <li v-for="action in insight.actionItems" :key="action" class="flex items-start space-x-1">
                    <span class="text-orange-400">•</span>
                    <span>{{ action }}</span>
                  </li>
                </ul>
              </div>
            </div>
            <button
              @click="addInsightToCanvas(insight)"
              class="ml-2 p-1 text-gray-400 hover:text-white transition-colors"
              title="Add to canvas"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-8">
        <div class="w-12 h-12 mx-auto mb-3 rounded-full flex items-center justify-center" :style="{ backgroundColor: selectedAgent.color + '20' }">
          <span class="text-lg">🔍</span>
        </div>
        <p class="text-sm text-gray-400 mb-3">No insights generated yet</p>
        <p class="text-xs text-gray-500">Add research items to the canvas and click "Analyze" to get {{ selectedAgent.name }}'s insights</p>
      </div>
    </div>

    <!-- Agent Recommendations -->
    <div v-if="recommendations.length > 0" class="mt-4 pt-4 border-t border-forest-600">
      <h4 class="text-sm font-medium text-gray-300 mb-2">{{ selectedAgent.name }}'s Recommendations</h4>
      <div class="space-y-2">
        <div
          v-for="rec in recommendations"
          :key="rec.id"
          class="flex items-center justify-between p-2 bg-forest-700 rounded text-sm"
        >
          <span class="text-gray-200">{{ rec.text }}</span>
          <button
            @click="applyRecommendation(rec)"
            class="px-2 py-1 text-xs rounded"
            :style="{ backgroundColor: selectedAgent.color, color: 'white' }"
          >
            Apply
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';

interface Props {
  researchItems: any[]
}

interface Emits {
  (e: 'addToCanvas', insight: any): void
  (e: 'applyRecommendation', recommendation: any): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const selectedAgentId = ref('agent_1')
const isGenerating = ref(false)
const insights = ref([])
const recommendations = ref([])

// Agent definitions matching the existing system
const agents = [
  {
    id: 'agent_1',
    name: 'Alex',
    avatar: '/Alex.png',
    color: '#3b82f6',
    specialization: 'Analytics & Strategy',
    expertise: ['performance_metrics', 'competitive_analysis', 'growth_strategy']
  },
  {
    id: 'agent_2',
    name: 'Levi',
    avatar: '/Levi.png',
    color: '#eab308',
    specialization: 'Content Creation',
    expertise: ['content_optimization', 'creative_strategy', 'storytelling']
  },
  {
    id: 'agent_3',
    name: 'Maya',
    avatar: '/Maya.png',
    color: '#16a34a',
    specialization: 'Audience Engagement',
    expertise: ['audience_insights', 'community_building', 'engagement_optimization']
  },
  {
    id: 'agent_4',
    name: 'Zara',
    avatar: '/Zara.png',
    color: '#a855f7',
    specialization: 'Growth Optimization',
    expertise: ['algorithm_optimization', 'viral_potential', 'growth_hacking']
  },
  {
    id: 'agent_5',
    name: 'Kai',
    avatar: '/Kai.png',
    color: '#dc2626',
    specialization: 'Technical SEO',
    expertise: ['seo_optimization', 'metadata_analysis', 'technical_optimization']
  }
]

const selectedAgent = computed(() => {
  return agents.find(a => a.id === selectedAgentId.value) || agents[0]
})

const switchAgent = () => {
  insights.value = []
  recommendations.value = []
}

const generateInsights = async () => {
  if (props.researchItems.length === 0) return
  
  isGenerating.value = true
  
  try {
    // Simulate AI analysis based on agent expertise
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    insights.value = generateAgentSpecificInsights()
    recommendations.value = generateAgentRecommendations()
  } finally {
    isGenerating.value = false
  }
}

const generateAgentSpecificInsights = () => {
  const agent = selectedAgent.value
  const baseInsights = []
  
  if (agent.id === 'agent_1') { // Alex - Analytics
    baseInsights.push({
      id: 1,
      type: 'Performance Analysis',
      description: 'Based on the research items, I notice strong engagement patterns in educational content with clear value propositions.',
      confidence: 87,
      actionItems: ['Focus on tutorial-style content', 'Include clear learning outcomes', 'Use data-driven thumbnails']
    })
  } else if (agent.id === 'agent_2') { // Levi - Content
    baseInsights.push({
      id: 1,
      type: 'Content Strategy',
      description: 'The research shows successful content follows a problem-solution narrative structure with personal storytelling elements.',
      confidence: 92,
      actionItems: ['Start with a relatable problem', 'Share personal experiences', 'End with actionable solutions']
    })
  }
  // Add more agent-specific insights...
  
  return baseInsights
}

const generateAgentRecommendations = () => {
  const agent = selectedAgent.value
  const recs = []
  
  if (agent.id === 'agent_1') {
    recs.push({
      id: 1,
      text: 'Analyze competitor performance metrics',
      action: 'competitor_analysis'
    })
  } else if (agent.id === 'agent_2') {
    recs.push({
      id: 1,
      text: 'Create content templates based on research',
      action: 'content_templates'
    })
  }
  
  return recs
}

const addInsightToCanvas = (insight) => {
  emit('addToCanvas', {
    type: 'agent-insight',
    agent: selectedAgent.value,
    content: insight,
    position: { x: Math.random() * 300 + 100, y: Math.random() * 200 + 100 }
  })
}

const applyRecommendation = (recommendation) => {
  emit('applyRecommendation', {
    agent: selectedAgent.value,
    recommendation
  })
}

// Watch for research items changes to auto-generate insights
watch(() => props.researchItems.length, (newLength) => {
  if (newLength > 0 && insights.value.length === 0) {
    generateInsights()
  }
})
</script>
