<template>
  <div class="space-y-6">
    <!-- Header and Filters -->
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-xl font-bold text-white">Content Gap Analysis</h2>
        <p class="text-gray-400">Identify high-opportunity content your competitors are missing</p>
      </div>
      
      <div class="flex items-center space-x-3">
        <!-- Opportunity Score Filter -->
        <div class="flex items-center space-x-2">
          <label class="text-sm text-gray-300">Min Score:</label>
          <select
            :value="filters.minOpportunityScore"
            @change="updateFilter('minOpportunityScore', Number($event.target.value))"
            class="rounded-lg border-2 border-gray-600/70 bg-gray-700 px-3 py-1 text-white focus:border-blue-500 focus:outline-none"
          >
            <option value="0">All (0+)</option>
            <option value="20">Low (20+)</option>
            <option value="40">Moderate (40+)</option>
            <option value="60">Good (60+)</option>
            <option value="80">Excellent (80+)</option>
          </select>
        </div>

        <!-- Sort Options -->
        <select
          v-model="sortBy"
          class="rounded-lg border-2 border-gray-600/70 bg-gray-700 px-3 py-1 text-white focus:border-blue-500 focus:outline-none"
        >
          <option value="opportunity_score">Opportunity Score</option>
          <option value="search_volume">Search Volume</option>
          <option value="potential_views">Potential Views</option>
          <option value="difficulty_rating">Difficulty</option>
        </select>
      </div>
    </div>

    <!-- Summary Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-4">
        <div class="text-2xl font-bold text-blue-400">{{ filteredGaps.length }}</div>
        <div class="text-sm text-gray-400">Content Gaps</div>
      </div>
      
      <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-4">
        <div class="text-2xl font-bold text-green-400">{{ totalPotentialViews.toLocaleString() }}</div>
        <div class="text-sm text-gray-400">Potential Views</div>
      </div>
      
      <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-4">
        <div class="text-2xl font-bold text-purple-400">{{ averageOpportunityScore.toFixed(1) }}</div>
        <div class="text-sm text-gray-400">Avg Opportunity Score</div>
      </div>
      
      <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-4">
        <div class="text-2xl font-bold text-orange-400">{{ highOpportunityCount }}</div>
        <div class="text-sm text-gray-400">High Opportunity (60+)</div>
      </div>
    </div>

    <!-- Content Gaps List -->
    <div class="space-y-4">
      <div
        v-for="gap in sortedGaps"
        :key="gap.gap_id"
        class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6 hover:border-blue-500/50 transition-colors"
      >
        <div class="flex items-start justify-between mb-4">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <h3 class="text-lg font-semibold text-white">{{ gap.topic }}</h3>
              <div class="flex items-center space-x-2">
                <!-- Opportunity Score Badge -->
                <span 
                  :class="[
                    'px-2 py-1 rounded-full text-xs font-medium',
                    getOpportunityScoreColor(gap.opportunity_score)
                  ]"
                >
                  {{ gap.opportunity_score }}/100
                </span>
                
                <!-- Competition Level Badge -->
                <span 
                  :class="[
                    'px-2 py-1 rounded-full text-xs font-medium',
                    getCompetitionLevelColor(gap.competition_level)
                  ]"
                >
                  {{ gap.competition_level }} competition
                </span>
              </div>
            </div>
            
            <p class="text-gray-400 mb-3">{{ gap.suggested_approach }}</p>
            
            <!-- Metrics Row -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span class="text-gray-400">Search Volume:</span>
                <span class="text-white font-medium ml-1">{{ gap.search_volume.toLocaleString() }}</span>
              </div>
              <div>
                <span class="text-gray-400">Potential Views:</span>
                <span class="text-green-400 font-medium ml-1">{{ gap.potential_views.toLocaleString() }}</span>
              </div>
              <div>
                <span class="text-gray-400">Difficulty:</span>
                <span 
                  :class="getDifficultyColor(gap.difficulty_rating)"
                  class="font-medium ml-1"
                >
                  {{ gap.difficulty_rating }}/10
                </span>
              </div>
              <div>
                <span class="text-gray-400">Effort:</span>
                <span class="text-orange-400 font-medium ml-1">{{ gap.estimated_effort }}</span>
              </div>
            </div>
          </div>
          
          <!-- Action Button -->
          <button
            @click="createContent(gap)"
            class="ml-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors flex items-center space-x-2"
          >
            <span>Create Content</span>
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>

        <!-- Expandable Details -->
        <div v-if="expandedGap === gap.gap_id" class="mt-4 pt-4 border-t border-gray-600">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Keywords -->
            <div>
              <h4 class="font-medium text-white mb-2">Target Keywords</h4>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="keyword in gap.keywords"
                  :key="keyword"
                  class="px-2 py-1 bg-blue-900/30 text-blue-300 rounded text-sm"
                >
                  {{ keyword }}
                </span>
              </div>
            </div>

            <!-- Missing Competitors -->
            <div>
              <h4 class="font-medium text-white mb-2">Competitors Missing This</h4>
              <div class="space-y-1">
                <div
                  v-for="competitor in gap.missing_competitors"
                  :key="competitor"
                  class="text-sm text-gray-300 flex items-center space-x-2"
                >
                  <span class="text-red-400">•</span>
                  <span>{{ competitor }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Content Format -->
          <div class="mt-4">
            <h4 class="font-medium text-white mb-2">Recommended Format</h4>
            <p class="text-gray-300 text-sm">{{ gap.content_format }}</p>
          </div>
        </div>

        <!-- Expand/Collapse Button -->
        <button
          @click="toggleExpand(gap.gap_id)"
          class="mt-3 text-sm text-blue-400 hover:text-blue-300 transition-colors flex items-center space-x-1"
        >
          <span>{{ expandedGap === gap.gap_id ? 'Show Less' : 'Show Details' }}</span>
          <svg 
            class="h-4 w-4 transition-transform"
            :class="{ 'rotate-180': expandedGap === gap.gap_id }"
            fill="currentColor" 
            viewBox="0 0 20 20"
          >
            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredGaps.length === 0" class="text-center py-12">
      <div class="text-gray-400 text-4xl mb-4">🎯</div>
      <h3 class="text-lg font-semibold text-white mb-2">No Content Gaps Found</h3>
      <p class="text-gray-400 mb-4">Try adjusting your filters or run a new analysis</p>
      <button
        @click="updateFilter('minOpportunityScore', 0)"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
      >
        Clear Filters
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  contentGaps: {
    type: Array,
    required: true
  },
  filters: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update-filters'])

// State
const sortBy = ref('opportunity_score')
const expandedGap = ref(null)

// Computed
const filteredGaps = computed(() => {
  return props.contentGaps.filter(gap => 
    gap.opportunity_score >= props.filters.minOpportunityScore
  )
})

const sortedGaps = computed(() => {
  const gaps = [...filteredGaps.value]
  
  gaps.sort((a, b) => {
    switch (sortBy.value) {
      case 'opportunity_score':
        return b.opportunity_score - a.opportunity_score
      case 'search_volume':
        return b.search_volume - a.search_volume
      case 'potential_views':
        return b.potential_views - a.potential_views
      case 'difficulty_rating':
        return a.difficulty_rating - b.difficulty_rating
      default:
        return b.opportunity_score - a.opportunity_score
    }
  })
  
  return gaps
})

const totalPotentialViews = computed(() => {
  return filteredGaps.value.reduce((sum, gap) => sum + gap.potential_views, 0)
})

const averageOpportunityScore = computed(() => {
  if (filteredGaps.value.length === 0) return 0
  return filteredGaps.value.reduce((sum, gap) => sum + gap.opportunity_score, 0) / filteredGaps.value.length
})

const highOpportunityCount = computed(() => {
  return filteredGaps.value.filter(gap => gap.opportunity_score >= 60).length
})

// Methods
const updateFilter = (key, value) => {
  emit('update-filters', { [key]: value })
}

const toggleExpand = (gapId) => {
  expandedGap.value = expandedGap.value === gapId ? null : gapId
}

const createContent = (gap) => {
  // In production, would navigate to content creation with pre-filled data
  console.log('Creating content for gap:', gap.topic)
  // Could emit event to parent or use router to navigate
  // emit('create-content', gap)
}

const getOpportunityScoreColor = (score) => {
  if (score >= 80) return 'bg-green-900/30 text-green-300 border border-green-600/30'
  if (score >= 60) return 'bg-blue-900/30 text-blue-300 border border-blue-600/30'
  if (score >= 40) return 'bg-yellow-900/30 text-yellow-300 border border-yellow-600/30'
  return 'bg-gray-900/30 text-gray-300 border border-gray-600/30'
}

const getCompetitionLevelColor = (level) => {
  const colors = {
    low: 'bg-green-900/30 text-green-300 border border-green-600/30',
    medium: 'bg-yellow-900/30 text-yellow-300 border border-yellow-600/30',
    high: 'bg-red-900/30 text-red-300 border border-red-600/30'
  }
  return colors[level] || 'bg-gray-900/30 text-gray-300 border border-gray-600/30'
}

const getDifficultyColor = (rating) => {
  if (rating <= 3) return 'text-green-400'
  if (rating <= 6) return 'text-yellow-400'
  return 'text-red-400'
}
</script>
