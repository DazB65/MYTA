<template>
  <div class="trending-keywords-widget bg-white rounded-xl p-6 shadow-sm border border-gray-100">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-3">
        <div class="p-2 bg-red-100 rounded-lg">
          <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-gray-900">Trending Keywords</h3>
          <p class="text-sm text-gray-500">Hot topics in your niche</p>
        </div>
      </div>
      <button 
        @click="refreshKeywords"
        :disabled="isLoading"
        class="p-2 text-gray-400 hover:text-gray-600 transition-colors"
      >
        <svg class="w-5 h-5" :class="{ 'animate-spin': isLoading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>
      </button>
    </div>

    <!-- Keywords List -->
    <div class="space-y-3">
      <div 
        v-for="(keyword, index) in trendingKeywords" 
        :key="index"
        class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer group"
        @click="useKeyword(keyword)"
      >
        <div class="flex items-center space-x-3">
          <div class="flex items-center justify-center w-6 h-6 bg-red-500 text-white text-xs font-bold rounded">
            {{ index + 1 }}
          </div>
          <div>
            <div class="font-medium text-gray-900">{{ keyword.term }}</div>
            <div class="text-sm text-gray-500">{{ keyword.searchVolume }} searches</div>
          </div>
        </div>
        <div class="flex items-center space-x-2">
          <div class="flex items-center space-x-1">
            <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span class="text-sm font-medium text-green-600">+{{ keyword.growth }}%</span>
          </div>
          <svg class="w-4 h-4 text-gray-400 group-hover:text-gray-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="mt-4 pt-4 border-t border-gray-100">
      <div class="flex space-x-2">
        <button 
          @click="generateContentIdeas"
          class="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-sm font-medium"
        >
          Generate Ideas
        </button>
        <button 
          @click="analyzeCompetitors"
          class="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium"
        >
          Analyze Competition
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isLoading = ref(false)
const trendingKeywords = ref([
  { term: "AI YouTube automation", searchVolume: "45K", growth: 127 },
  { term: "YouTube Shorts strategy", searchVolume: "38K", growth: 89 },
  { term: "Content creator tools", searchVolume: "32K", growth: 76 },
  { term: "YouTube analytics 2024", searchVolume: "28K", growth: 65 },
  { term: "Video SEO optimization", searchVolume: "25K", growth: 54 },
  { term: "Creator economy trends", searchVolume: "22K", growth: 43 },
  { term: "YouTube monetization", searchVolume: "19K", growth: 38 },
  { term: "Viral video formula", searchVolume: "17K", growth: 32 }
])

const refreshKeywords = async () => {
  isLoading.value = true
  try {
    // Simulate API call - replace with actual trending keywords API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // In real implementation, fetch from YouTube API or Google Trends
    console.log('🔥 Refreshing trending keywords...')
  } catch (error) {
    console.error('Error refreshing keywords:', error)
  } finally {
    isLoading.value = false
  }
}

const useKeyword = (keyword) => {
  // Emit event to parent or use composable to add keyword to content creation
  console.log('🔥 Using keyword:', keyword.term)
  
  // Could integrate with content modal or task creation
  // emit('keyword-selected', keyword)
}

const generateContentIdeas = () => {
  console.log('🔥 Generating content ideas from trending keywords...')
  // Integrate with AI agent to generate ideas based on trending keywords
}

const analyzeCompetitors = () => {
  console.log('🔥 Analyzing competitors for trending keywords...')
  // Open competitor analysis modal or navigate to competitor page
}

onMounted(() => {
  // Load initial trending keywords
  refreshKeywords()
})
</script>

<style scoped>
.trending-keywords-widget {
  min-height: 400px;
}
</style>
