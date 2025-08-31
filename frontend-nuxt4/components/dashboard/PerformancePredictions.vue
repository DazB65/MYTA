<template>
  <div class="performance-predictions bg-white rounded-xl p-6 shadow-sm border border-gray-100">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="p-2 bg-purple-100 rounded-lg">
          <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-gray-900">Performance Predictions</h3>
          <p class="text-sm text-gray-500">AI-powered forecasts</p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <div class="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded">
          {{ confidenceLevel }}% Confidence
        </div>
      </div>
    </div>

    <!-- Prediction Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
      <!-- Next Video Prediction -->
      <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 border border-blue-200">
        <div class="flex items-center justify-between mb-3">
          <h4 class="font-medium text-blue-900">Next Video Forecast</h4>
          <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
          </svg>
        </div>
        <div class="space-y-2">
          <div class="flex justify-between">
            <span class="text-sm text-blue-700">Expected Views:</span>
            <span class="font-semibold text-blue-900">{{ formatNumber(nextVideoViews.min) }} - {{ formatNumber(nextVideoViews.max) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-sm text-blue-700">Engagement Rate:</span>
            <span class="font-semibold text-blue-900">{{ nextVideoEngagement }}%</span>
          </div>
          <div class="flex justify-between">
            <span class="text-sm text-blue-700">Best Upload Time:</span>
            <span class="font-semibold text-blue-900">{{ bestUploadTime }}</span>
          </div>
        </div>
      </div>

      <!-- Growth Milestone -->
      <div class="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4 border border-green-200">
        <div class="flex items-center justify-between mb-3">
          <h4 class="font-medium text-green-900">Growth Milestone</h4>
          <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
          </svg>
        </div>
        <div class="space-y-2">
          <div class="flex justify-between">
            <span class="text-sm text-green-700">Next Milestone:</span>
            <span class="font-semibold text-green-900">{{ formatNumber(nextMilestone.target) }} subs</span>
          </div>
          <div class="flex justify-between">
            <span class="text-sm text-green-700">Estimated Date:</span>
            <span class="font-semibold text-green-900">{{ nextMilestone.date }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-sm text-green-700">Progress:</span>
            <span class="font-semibold text-green-900">{{ nextMilestone.progress }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Trend Analysis -->
    <div class="bg-gray-50 rounded-lg p-4 mb-4">
      <h4 class="font-medium text-gray-900 mb-3">30-Day Trend Analysis</h4>
      <div class="grid grid-cols-3 gap-4">
        <div class="text-center">
          <div class="text-2xl font-bold text-blue-600">{{ trendAnalysis.views.change }}%</div>
          <div class="text-sm text-gray-600">Views Change</div>
          <div class="flex items-center justify-center mt-1">
            <svg v-if="trendAnalysis.views.change > 0" class="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
            </svg>
            <svg v-else class="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
          </div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-green-600">{{ trendAnalysis.engagement.change }}%</div>
          <div class="text-sm text-gray-600">Engagement</div>
          <div class="flex items-center justify-center mt-1">
            <svg v-if="trendAnalysis.engagement.change > 0" class="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
            </svg>
            <svg v-else class="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
          </div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-purple-600">{{ trendAnalysis.subscribers.change }}%</div>
          <div class="text-sm text-gray-600">Subscribers</div>
          <div class="flex items-center justify-center mt-1">
            <svg v-if="trendAnalysis.subscribers.change > 0" class="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
            </svg>
            <svg v-else class="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- AI Recommendations -->
    <div class="border-t border-gray-100 pt-4">
      <h4 class="font-medium text-gray-900 mb-3">🤖 AI Recommendations</h4>
      <div class="space-y-2">
        <div 
          v-for="recommendation in aiRecommendations" 
          :key="recommendation.id"
          class="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg border border-blue-100"
        >
          <div class="text-lg">{{ recommendation.icon }}</div>
          <div class="flex-1">
            <div class="font-medium text-blue-900">{{ recommendation.title }}</div>
            <div class="text-sm text-blue-700">{{ recommendation.description }}</div>
          </div>
          <button 
            @click="applyRecommendation(recommendation)"
            class="px-3 py-1 bg-blue-500 text-white text-xs rounded hover:bg-blue-600 transition-colors"
          >
            Apply
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const confidenceLevel = ref(87)

const nextVideoViews = ref({
  min: 15000,
  max: 25000
})

const nextVideoEngagement = ref(4.2)
const bestUploadTime = ref('2:00 PM PST')

const nextMilestone = ref({
  target: 100000,
  date: 'March 15, 2024',
  progress: 73
})

const trendAnalysis = ref({
  views: { change: 12.5 },
  engagement: { change: 8.3 },
  subscribers: { change: 15.7 }
})

const aiRecommendations = ref([
  {
    id: 1,
    icon: '🎯',
    title: 'Optimize Upload Schedule',
    description: 'Upload on Tuesdays at 2 PM for 23% higher engagement'
  },
  {
    id: 2,
    icon: '📱',
    title: 'Create YouTube Shorts',
    description: 'Shorts content could increase discovery by 45%'
  },
  {
    id: 3,
    icon: '🔥',
    title: 'Trending Topic Alert',
    description: 'Cover "AI productivity tools" - trending in your niche'
  }
])

const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const applyRecommendation = (recommendation) => {
  console.log('🔥 Applying recommendation:', recommendation.title)
  // Integrate with task creation or content planning
}
</script>

<style scoped>
.performance-predictions {
  min-height: 500px;
}
</style>
