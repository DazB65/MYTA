<template>
  <div class="space-y-6">
    <h2 class="text-xl font-bold text-white">Competitor Profiles</h2>
    <p class="text-gray-400">Detailed analysis of your competitive landscape</p>
    
    <!-- Placeholder content -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div
        v-for="competitor in competitors"
        :key="competitor.competitor_id"
        class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6"
      >
        <h3 class="text-lg font-semibold text-white mb-2">{{ competitor.name }}</h3>
        <p class="text-gray-400 mb-4">{{ competitor.tier }} competitor</p>
        
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-gray-300">Subscribers:</span>
            <span class="text-white">{{ formatNumber(competitor.subscriber_count) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-300">Avg Views:</span>
            <span class="text-white">{{ formatNumber(competitor.avg_views) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-300">Growth Rate:</span>
            <span class="text-green-400">{{ (competitor.growth_rate * 100).toFixed(1) }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  competitors: Array,
  marketPosition: Object
})

const formatNumber = (num) => {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toString()
}
</script>
