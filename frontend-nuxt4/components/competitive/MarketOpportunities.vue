<template>
  <div class="space-y-6">
    <h2 class="text-xl font-bold text-white">Market Opportunities</h2>
    <p class="text-gray-400">Strategic opportunities and blue ocean markets</p>
    
    <!-- Market Opportunities -->
    <div class="space-y-4">
      <h3 class="text-lg font-semibold text-white">Strategic Opportunities</h3>
      <div
        v-for="opportunity in opportunities"
        :key="opportunity.opportunity_id"
        class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6"
      >
        <div class="flex items-start justify-between mb-4">
          <div>
            <h4 class="text-lg font-semibold text-white">{{ opportunity.title }}</h4>
            <p class="text-gray-400 mt-1">{{ opportunity.description }}</p>
          </div>
          <span class="px-3 py-1 bg-blue-900/30 text-blue-300 rounded-full text-sm">
            {{ opportunity.opportunity_score }}/100
          </span>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span class="text-gray-400">Effort:</span>
            <span class="text-white ml-1">{{ opportunity.effort_required }}</span>
          </div>
          <div>
            <span class="text-gray-400">Time Sensitivity:</span>
            <span class="text-orange-400 ml-1">{{ opportunity.time_sensitivity }}</span>
          </div>
          <div>
            <span class="text-gray-400">Impact:</span>
            <span class="text-green-400 ml-1">{{ opportunity.potential_impact }}</span>
          </div>
          <div>
            <span class="text-gray-400">Type:</span>
            <span class="text-purple-400 ml-1">{{ opportunity.type }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Blue Ocean Opportunities -->
    <div class="space-y-4">
      <h3 class="text-lg font-semibold text-white">Blue Ocean Markets</h3>
      <div
        v-for="ocean in blueOceans"
        :key="ocean.ocean_id"
        class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-blue-600/70 shadow-lg p-6"
      >
        <h4 class="text-lg font-semibold text-white mb-2">{{ ocean.market_name }}</h4>
        <p class="text-gray-400 mb-4">{{ ocean.unique_value_proposition }}</p>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span class="text-gray-400">Market Size:</span>
            <span class="text-white ml-1">{{ ocean.market_size.toLocaleString() }}</span>
          </div>
          <div>
            <span class="text-gray-400">Competition:</span>
            <span class="text-green-400 ml-1">{{ (ocean.competition_density * 100).toFixed(1) }}%</span>
          </div>
          <div>
            <span class="text-gray-400">ROI Potential:</span>
            <span class="text-blue-400 ml-1">{{ ocean.potential_roi.toFixed(1) }}x</span>
          </div>
          <div>
            <span class="text-gray-400">Success Rate:</span>
            <span class="text-purple-400 ml-1">{{ (ocean.success_probability * 100).toFixed(0) }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  opportunities: Array,
  blueOceans: Array
})
</script>
