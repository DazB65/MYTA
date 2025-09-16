<template>
  <div class="space-y-6">
    <h2 class="text-xl font-bold text-white">Competitive Threats</h2>
    <p class="text-gray-400">Identified threats and mitigation strategies</p>
    
    <div class="space-y-4">
      <div
        v-for="threat in threats"
        :key="threat.threat_id"
        class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6"
      >
        <div class="flex items-start justify-between mb-4">
          <div>
            <h4 class="text-lg font-semibold text-white">{{ threat.threat_type }}</h4>
            <p class="text-gray-400 mt-1">{{ threat.description }}</p>
          </div>
          <span 
            :class="getThreatLevelColor(threat.threat_level)"
            class="px-3 py-1 rounded-full text-sm font-medium"
          >
            {{ threat.threat_level }} threat
          </span>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <span class="text-gray-400">Competitor:</span>
            <span class="text-white ml-1">{{ threat.competitor_name }}</span>
          </div>
          <div>
            <span class="text-gray-400">Timeline:</span>
            <span class="text-orange-400 ml-1">{{ threat.timeline }}</span>
          </div>
          <div>
            <span class="text-gray-400">Impact:</span>
            <span class="text-red-400 ml-1">{{ threat.impact_assessment }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  threats: Array,
  allThreats: Array
})

const getThreatLevelColor = (level) => {
  const colors = {
    low: 'bg-green-900/30 text-green-300',
    medium: 'bg-yellow-900/30 text-yellow-300',
    high: 'bg-orange-900/30 text-orange-300',
    critical: 'bg-red-900/30 text-red-300'
  }
  return colors[level] || 'bg-gray-900/30 text-gray-300'
}
</script>
