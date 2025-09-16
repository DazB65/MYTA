<template>
  <div class="space-y-6">
    <!-- Market Position Summary -->
    <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
      <h2 class="text-xl font-bold text-white mb-4">Market Position Analysis</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Overall Score -->
        <div class="text-center">
          <div class="relative w-24 h-24 mx-auto mb-3">
            <svg class="w-24 h-24 transform -rotate-90" viewBox="0 0 100 100">
              <!-- Background circle -->
              <circle
                cx="50"
                cy="50"
                r="40"
                stroke="currentColor"
                stroke-width="8"
                fill="none"
                class="text-gray-600"
              />
              <!-- Progress circle -->
              <circle
                cx="50"
                cy="50"
                r="40"
                stroke="currentColor"
                stroke-width="8"
                fill="none"
                :stroke-dasharray="circumference"
                :stroke-dashoffset="circumference - (marketPosition.overall_score / 100) * circumference"
                class="text-blue-400 transition-all duration-1000 ease-out"
                stroke-linecap="round"
              />
            </svg>
            <div class="absolute inset-0 flex items-center justify-center">
              <span class="text-xl font-bold text-white">{{ marketPosition.overall_score }}</span>
            </div>
          </div>
          <h3 class="font-semibold text-white">Overall Score</h3>
          <p class="text-sm text-gray-400">{{ marketPosition.position_category }}</p>
        </div>

        <!-- Percentile Rankings -->
        <div class="space-y-4">
          <div>
            <div class="flex justify-between items-center mb-1">
              <span class="text-sm text-gray-300">Subscribers</span>
              <span class="text-sm text-blue-400">{{ marketPosition.subscriber_percentile }}%</span>
            </div>
            <div class="w-full bg-gray-600 rounded-full h-2">
              <div 
                class="bg-blue-400 h-2 rounded-full transition-all duration-1000 ease-out"
                :style="{ width: `${marketPosition.subscriber_percentile}%` }"
              ></div>
            </div>
          </div>

          <div>
            <div class="flex justify-between items-center mb-1">
              <span class="text-sm text-gray-300">Views</span>
              <span class="text-sm text-green-400">{{ marketPosition.view_percentile }}%</span>
            </div>
            <div class="w-full bg-gray-600 rounded-full h-2">
              <div 
                class="bg-green-400 h-2 rounded-full transition-all duration-1000 ease-out"
                :style="{ width: `${marketPosition.view_percentile}%` }"
              ></div>
            </div>
          </div>

          <div>
            <div class="flex justify-between items-center mb-1">
              <span class="text-sm text-gray-300">Growth</span>
              <span class="text-sm text-purple-400">{{ marketPosition.growth_percentile }}%</span>
            </div>
            <div class="w-full bg-gray-600 rounded-full h-2">
              <div 
                class="bg-purple-400 h-2 rounded-full transition-all duration-1000 ease-out"
                :style="{ width: `${marketPosition.growth_percentile}%` }"
              ></div>
            </div>
          </div>
        </div>

        <!-- Advantages & Improvements -->
        <div class="space-y-4">
          <div>
            <h4 class="font-medium text-green-400 mb-2">Competitive Advantages</h4>
            <ul class="space-y-1">
              <li 
                v-for="advantage in marketPosition.competitive_advantages"
                :key="advantage"
                class="text-sm text-gray-300 flex items-center space-x-2"
              >
                <span class="text-green-400">✓</span>
                <span>{{ advantage }}</span>
              </li>
            </ul>
          </div>

          <div>
            <h4 class="font-medium text-orange-400 mb-2">Improvement Areas</h4>
            <ul class="space-y-1">
              <li 
                v-for="improvement in marketPosition.improvement_areas"
                :key="improvement"
                class="text-sm text-gray-300 flex items-center space-x-2"
              >
                <span class="text-orange-400">→</span>
                <span>{{ improvement }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Competitive Landscape Overview -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Competitor Distribution -->
      <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
        <h3 class="text-lg font-semibold text-white mb-4">Competitor Landscape</h3>
        
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-gray-300">Total Competitors</span>
            <span class="text-xl font-bold text-white">{{ competitiveLandscape.total_competitors }}</span>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 rounded-full bg-blue-400"></div>
                <span class="text-sm text-gray-300">Direct Competitors</span>
              </div>
              <span class="text-blue-400 font-medium">{{ competitiveLandscape.direct_competitors }}</span>
            </div>

            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 rounded-full bg-purple-400"></div>
                <span class="text-sm text-gray-300">Aspirational Targets</span>
              </div>
              <span class="text-purple-400 font-medium">{{ competitiveLandscape.aspirational_targets }}</span>
            </div>

            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 rounded-full bg-green-400"></div>
                <span class="text-sm text-gray-300">Adjacent Players</span>
              </div>
              <span class="text-green-400 font-medium">{{ adjacentCompetitors }}</span>
            </div>

            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 rounded-full bg-orange-400"></div>
                <span class="text-sm text-gray-300">Emerging Threats</span>
              </div>
              <span class="text-orange-400 font-medium">{{ emergingCompetitors }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Key Insights -->
      <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
        <h3 class="text-lg font-semibold text-white mb-4">Key Insights</h3>
        
        <div class="space-y-4">
          <!-- Top Insight -->
          <div class="p-4 rounded-lg bg-blue-900/30 border border-blue-600/30">
            <div class="flex items-center space-x-2 mb-2">
              <span class="text-blue-400 text-lg">💡</span>
              <span class="font-medium text-blue-300">Strategic Opportunity</span>
            </div>
            <p class="text-sm text-blue-200">
              {{ getTopInsight() }}
            </p>
          </div>

          <!-- Market Trend -->
          <div class="p-4 rounded-lg bg-green-900/30 border border-green-600/30">
            <div class="flex items-center space-x-2 mb-2">
              <span class="text-green-400 text-lg">📈</span>
              <span class="font-medium text-green-300">Market Trend</span>
            </div>
            <p class="text-sm text-green-200">
              {{ getMarketTrend() }}
            </p>
          </div>

          <!-- Competitive Advantage -->
          <div class="p-4 rounded-lg bg-purple-900/30 border border-purple-600/30">
            <div class="flex items-center space-x-2 mb-2">
              <span class="text-purple-400 text-lg">⚡</span>
              <span class="font-medium text-purple-300">Your Edge</span>
            </div>
            <p class="text-sm text-purple-200">
              {{ getCompetitiveEdge() }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
      <h3 class="text-lg font-semibold text-white mb-4">Recommended Actions</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          v-for="action in quickActions"
          :key="action.id"
          @click="$emit('navigate-to', action.tab)"
          class="p-4 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors text-left group"
        >
          <div class="flex items-center space-x-3 mb-2">
            <span class="text-2xl">{{ action.icon }}</span>
            <span class="font-medium text-white group-hover:text-blue-400 transition-colors">{{ action.title }}</span>
          </div>
          <p class="text-sm text-gray-400">{{ action.description }}</p>
          <div class="mt-2 text-xs text-blue-400">{{ action.priority }} Priority</div>
        </button>
      </div>
    </div>

    <!-- Analysis Metadata -->
    <div class="text-center text-sm text-gray-400">
      <p>Analysis completed: {{ formatDate(analysis.analysis_timestamp) }}</p>
      <p>Next analysis: {{ formatDate(analysis.next_analysis_date) }}</p>
      <p>Analysis depth: {{ analysis.analysis_depth }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  analysis: {
    type: Object,
    required: true
  },
  quickInsights: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['navigate-to'])

// Computed properties
const competitiveLandscape = computed(() => props.analysis.competitive_landscape)
const marketPosition = computed(() => competitiveLandscape.value.market_position)

const circumference = computed(() => 2 * Math.PI * 40) // radius = 40

const adjacentCompetitors = computed(() => {
  return props.analysis.competitor_profiles.filter(comp => comp.tier === 'adjacent').length
})

const emergingCompetitors = computed(() => {
  return props.analysis.competitor_profiles.filter(comp => comp.tier === 'emerging').length
})

const quickActions = computed(() => {
  const actions = []
  
  // Add action based on top opportunity
  if (props.analysis.content_gaps.length > 0) {
    actions.push({
      id: 'content-gaps',
      tab: 'content-gaps',
      icon: '🎯',
      title: 'Exploit Content Gaps',
      description: `${props.analysis.content_gaps.length} high-opportunity gaps identified`,
      priority: 'High'
    })
  }
  
  // Add action based on threats
  const urgentThreats = props.analysis.competitive_threats.filter(t => ['high', 'critical'].includes(t.threat_level))
  if (urgentThreats.length > 0) {
    actions.push({
      id: 'threats',
      tab: 'threats',
      icon: '⚠️',
      title: 'Address Threats',
      description: `${urgentThreats.length} urgent threats require attention`,
      priority: 'High'
    })
  }
  
  // Add opportunity action
  if (props.analysis.market_opportunities.length > 0) {
    actions.push({
      id: 'opportunities',
      tab: 'opportunities',
      icon: '🚀',
      title: 'Seize Opportunities',
      description: `${props.analysis.market_opportunities.length} strategic opportunities available`,
      priority: 'Medium'
    })
  }
  
  return actions.slice(0, 3) // Limit to 3 actions
})

// Methods
const getTopInsight = () => {
  if (props.analysis.content_gaps.length > 0) {
    const topGap = props.analysis.content_gaps[0]
    return `High-opportunity content gap identified: "${topGap.topic}" with ${topGap.potential_views.toLocaleString()} potential views.`
  }
  
  if (props.analysis.market_opportunities.length > 0) {
    const topOpp = props.analysis.market_opportunities[0]
    return `Strategic opportunity: ${topOpp.title} with ${topOpp.potential_impact} potential impact.`
  }
  
  return "Continue monitoring competitive landscape for emerging opportunities."
}

const getMarketTrend = () => {
  const avgGrowth = props.analysis.competitor_profiles.reduce((sum, comp) => sum + comp.growth_rate, 0) / props.analysis.competitor_profiles.length
  
  if (avgGrowth > 0.15) {
    return "Market is experiencing rapid growth. High competition but significant opportunity for expansion."
  } else if (avgGrowth > 0.05) {
    return "Market showing steady growth. Focus on differentiation and quality content."
  } else {
    return "Market growth is slowing. Innovation and unique positioning are critical for success."
  }
}

const getCompetitiveEdge = () => {
  const advantages = marketPosition.value.competitive_advantages
  if (advantages && advantages.length > 0) {
    return `Your strongest advantage: ${advantages[0]}. Leverage this to differentiate from competitors.`
  }
  return "Focus on developing unique competitive advantages through content quality and audience engagement."
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
