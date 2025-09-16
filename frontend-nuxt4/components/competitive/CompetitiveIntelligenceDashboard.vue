<template>
  <div class="space-y-6">
    <!-- Controls -->
    <div class="flex items-center justify-end space-x-3">
      <button
        @click="refreshAnalysis"
        :disabled="isLoading"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
      >
        <svg class="h-4 w-4" :class="{ 'animate-spin': isLoading }" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/>
        </svg>
        <span>{{ isLoading ? 'Analyzing...' : 'Refresh Analysis' }}</span>
      </button>
      <select
        v-model="filters.analysisDepth"
        @change="refreshAnalysis"
        class="rounded-lg border-2 border-gray-600/70 bg-gray-700 px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
      >
        <option value="quick">Quick Analysis</option>
        <option value="standard">Standard Analysis</option>
        <option value="comprehensive">Comprehensive Analysis</option>
      </select>
    </div>

    <!-- Quick Insights Cards -->
    <div v-if="quickInsights" class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Market Position -->
      <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-4">
        <div class="flex items-center space-x-3 mb-2">
          <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-500">
            <span class="text-white text-sm">📊</span>
          </div>
          <div>
            <h3 class="font-semibold text-white">Market Position</h3>
            <p class="text-sm text-gray-400">{{ marketPosition }}</p>
          </div>
        </div>
        <div class="text-2xl font-bold text-blue-400">{{ competitiveScore.toFixed(1) }}/100</div>
        <div class="text-xs text-gray-400 mt-1">Competitive Score</div>
      </div>

      <!-- Top Opportunity -->
      <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-4">
        <div class="flex items-center space-x-3 mb-2">
          <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-green-500">
            <span class="text-white text-sm">🎯</span>
          </div>
          <div>
            <h3 class="font-semibold text-white">Top Opportunity</h3>
            <p class="text-sm text-gray-400">{{ quickInsights.top_opportunity?.type || 'None' }}</p>
          </div>
        </div>
        <div class="text-sm text-green-400 font-medium">
          {{ quickInsights.top_opportunity?.title || 'No opportunities found' }}
        </div>
        <div v-if="quickInsights.top_opportunity" class="text-xs text-gray-400 mt-1">
          Score: {{ quickInsights.top_opportunity.opportunity_score }}/100
        </div>
      </div>



      <!-- Recommended Action -->
      <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-4">
        <div class="flex items-center space-x-3 mb-2">
          <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-orange-500">
            <span class="text-white text-sm">💡</span>
          </div>
          <div>
            <h3 class="font-semibold text-white">Next Action</h3>
            <p class="text-sm text-gray-400">Recommended</p>
          </div>
        </div>
        <div class="text-sm text-orange-400 font-medium">
          {{ quickInsights.recommended_action }}
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && !hasAnalysis" class="text-center py-12">
      <div class="animate-spin text-4xl mb-4">🔍</div>
      <h3 class="text-lg font-semibold text-white mb-2">Analyzing Competitive Landscape</h3>
      <p class="text-gray-400">This may take a few moments...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-400 text-4xl mb-4">⚠️</div>
      <h3 class="text-lg font-semibold text-red-400 mb-2">Analysis Failed</h3>
      <p class="text-gray-400 mb-4">{{ error }}</p>
      <button
        @click="refreshAnalysis"
        class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
      >
        Try Again
      </button>
    </div>

    <!-- Main Analysis Content -->
    <div v-else-if="hasAnalysis" class="space-y-6">
      <!-- Tab Navigation -->
      <div class="border-b border-gray-600">
        <nav class="flex space-x-8">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'py-2 px-1 border-b-2 font-medium text-sm transition-colors',
              activeTab === tab.id
                ? 'border-blue-500 text-blue-400'
                : 'border-transparent text-gray-400 hover:text-white hover:border-gray-300'
            ]"
          >
            {{ tab.icon }} {{ tab.name }}
          </button>
        </nav>
      </div>

      <!-- Tab Content -->
      <div class="min-h-96">
        <!-- Overview Tab -->
        <div v-if="activeTab === 'overview'">
          <CompetitiveOverview 
            :analysis="lastAnalysis"
            :quick-insights="quickInsights"
          />
        </div>

        <!-- Competitors Tab -->
        <div v-else-if="activeTab === 'competitors'">
          <CompetitorProfiles 
            :competitors="lastAnalysis.competitor_profiles"
            :market-position="lastAnalysis.competitive_landscape.market_position"
          />
        </div>

        <!-- Content Gaps Tab -->
        <div v-else-if="activeTab === 'content-gaps'">
          <ContentGapsAnalysis 
            :content-gaps="contentGapsByScore"
            :filters="filters"
            @update-filters="updateFilters"
          />
        </div>

        <!-- Opportunities Tab -->
        <div v-else-if="activeTab === 'opportunities'">
          <MarketOpportunities 
            :opportunities="topOpportunities"
            :blue-oceans="lastAnalysis.blue_ocean_opportunities"
          />
        </div>



        <!-- Strategy Tab -->
        <div v-else-if="activeTab === 'strategy'">
          <StrategicRecommendations 
            :recommendations="lastAnalysis.strategic_recommendations"
            :competitive-score="competitiveScore"
          />
        </div>
      </div>
    </div>

    <!-- No Analysis State -->
    <div v-else class="text-center py-12">
      <div class="text-gray-400 text-4xl mb-4">🔍</div>
      <h3 class="text-lg font-semibold text-white mb-2">No Analysis Available</h3>
      <p class="text-gray-400 mb-4">Run your first competitive analysis to get started</p>
      <button
        @click="refreshAnalysis"
        class="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
      >
        Start Analysis
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useCompetitiveIntelligence } from '../../composables/useCompetitiveIntelligence'

// Import child components (will create these next)
import CompetitiveOverview from './CompetitiveOverview.vue'
import CompetitorProfiles from './CompetitorProfiles.vue'
import ContentGapsAnalysis from './ContentGapsAnalysis.vue'
import MarketOpportunities from './MarketOpportunities.vue'
import StrategicRecommendations from './StrategicRecommendations.vue'

// Competitive intelligence composable
const {
  isLoading,
  error,
  lastAnalysis,
  quickInsights,
  filters,
  hasAnalysis,
  competitiveScore,
  marketPosition,
  topOpportunities,
  contentGapsByScore,
  analyzeCompetitiveLandscape,
  getQuickInsights
} = useCompetitiveIntelligence()

// Tab management
const activeTab = ref('overview')
const tabs = [
  { id: 'overview', name: 'Overview', icon: '📊' },
  { id: 'competitors', name: 'Competitors', icon: '🏢' },
  { id: 'content-gaps', name: 'Content Gaps', icon: '🎯' },
  { id: 'opportunities', name: 'Opportunities', icon: '🚀' },
  { id: 'strategy', name: 'Strategy', icon: '💡' }
]

// Methods
const refreshAnalysis = async () => {
  try {
    const userId = 'current-user' // In production, get from auth store
    
    // Run both analyses in parallel
    await Promise.all([
      analyzeCompetitiveLandscape(userId),
      getQuickInsights(userId)
    ])
  } catch (err) {
    console.error('Analysis failed:', err)
  }
}

const updateFilters = (newFilters) => {
  Object.assign(filters, newFilters)
}

// Initialize
onMounted(() => {
  refreshAnalysis()
})
</script>
