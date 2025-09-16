<template>
  <div class="space-y-6">
    <h2 class="text-xl font-bold text-white">Strategic Recommendations</h2>
    <p class="text-gray-400">AI-powered strategic guidance based on competitive analysis</p>
    
    <!-- Immediate Actions -->
    <div v-if="recommendations.immediate_actions" class="space-y-4">
      <h3 class="text-lg font-semibold text-white">Immediate Actions (Next 2 Weeks)</h3>
      <div class="space-y-3">
        <div
          v-for="action in recommendations.immediate_actions"
          :key="action.action"
          class="rounded-xl bg-red-900/20 border border-red-600/30 p-4"
        >
          <div class="flex items-start justify-between">
            <div>
              <h4 class="font-semibold text-red-300">{{ action.action }}</h4>
              <p class="text-red-200 text-sm mt-1">Expected Impact: {{ action.expected_impact }}</p>
            </div>
            <span class="px-2 py-1 bg-red-900/30 text-red-300 rounded text-xs">
              {{ action.priority }} Priority
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Short-term Strategy -->
    <div v-if="recommendations.short_term_strategy" class="space-y-4">
      <h3 class="text-lg font-semibold text-white">Short-term Strategy (1-3 Months)</h3>
      <div class="space-y-3">
        <div
          v-for="strategy in recommendations.short_term_strategy"
          :key="strategy.strategy"
          class="rounded-xl bg-yellow-900/20 border border-yellow-600/30 p-4"
        >
          <h4 class="font-semibold text-yellow-300">{{ strategy.strategy }}</h4>
          <p class="text-yellow-200 text-sm mt-1">{{ strategy.description }}</p>
          <div class="text-xs text-yellow-400 mt-2">Timeline: {{ strategy.timeline }}</div>
        </div>
      </div>
    </div>

    <!-- Long-term Vision -->
    <div v-if="recommendations.long_term_vision" class="space-y-4">
      <h3 class="text-lg font-semibold text-white">Long-term Vision (6-12 Months)</h3>
      <div class="space-y-3">
        <div
          v-for="vision in recommendations.long_term_vision"
          :key="vision.vision"
          class="rounded-xl bg-blue-900/20 border border-blue-600/30 p-4"
        >
          <h4 class="font-semibold text-blue-300">{{ vision.vision }}</h4>
          <p class="text-blue-200 text-sm mt-1">{{ vision.description }}</p>
          <div class="text-xs text-blue-400 mt-2">
            Success Probability: {{ vision.success_probability }}
          </div>
        </div>
      </div>
    </div>

    <!-- Competitive Score -->
    <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
      <h3 class="text-lg font-semibold text-white mb-4">Overall Competitive Health</h3>
      <div class="flex items-center space-x-4">
        <div class="text-3xl font-bold text-blue-400">{{ competitiveScore.toFixed(1) }}/100</div>
        <div class="flex-1">
          <div class="w-full bg-gray-600 rounded-full h-3">
            <div 
              class="bg-blue-400 h-3 rounded-full transition-all duration-1000 ease-out"
              :style="{ width: `${competitiveScore}%` }"
            ></div>
          </div>
          <p class="text-gray-400 text-sm mt-1">{{ getScoreDescription(competitiveScore) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  recommendations: Object,
  competitiveScore: Number
})

const getScoreDescription = (score) => {
  if (score >= 80) return "Excellent competitive position"
  if (score >= 60) return "Strong competitive position"
  if (score >= 40) return "Moderate competitive position"
  if (score >= 20) return "Weak competitive position"
  return "Critical competitive position"
}
</script>
