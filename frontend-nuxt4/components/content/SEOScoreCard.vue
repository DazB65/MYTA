<template>
  <div class="seo-score-card bg-white rounded-xl p-6 shadow-sm border border-gray-100">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-3">
        <div class="p-2 bg-green-100 rounded-lg">
          <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-gray-900">SEO Score</h3>
          <p class="text-sm text-gray-500">Optimization analysis</p>
        </div>
      </div>
      <div class="text-right">
        <div class="text-2xl font-bold" :class="scoreColor">{{ seoScore }}/100</div>
        <div class="text-sm text-gray-500">{{ scoreLabel }}</div>
      </div>
    </div>

    <!-- Score Circle -->
    <div class="flex justify-center mb-6">
      <div class="relative w-32 h-32">
        <svg class="w-32 h-32 transform -rotate-90" viewBox="0 0 120 120">
          <!-- Background circle -->
          <circle
            cx="60"
            cy="60"
            r="50"
            stroke="#f3f4f6"
            stroke-width="8"
            fill="none"
          />
          <!-- Progress circle -->
          <circle
            cx="60"
            cy="60"
            r="50"
            :stroke="scoreColorHex"
            stroke-width="8"
            fill="none"
            stroke-linecap="round"
            :stroke-dasharray="circumference"
            :stroke-dashoffset="circumference - (seoScore / 100) * circumference"
            class="transition-all duration-1000 ease-out"
          />
        </svg>
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="text-center">
            <div class="text-2xl font-bold text-gray-900">{{ seoScore }}</div>
            <div class="text-sm text-gray-500">Score</div>
          </div>
        </div>
      </div>
    </div>

    <!-- SEO Factors -->
    <div class="space-y-3">
      <div 
        v-for="factor in seoFactors" 
        :key="factor.name"
        class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
      >
        <div class="flex items-center space-x-3">
          <div 
            class="w-3 h-3 rounded-full"
            :class="{
              'bg-green-500': factor.status === 'good',
              'bg-yellow-500': factor.status === 'warning',
              'bg-red-500': factor.status === 'error'
            }"
          ></div>
          <span class="font-medium text-gray-900">{{ factor.name }}</span>
        </div>
        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-600">{{ factor.score }}/{{ factor.maxScore }}</span>
          <svg 
            v-if="factor.status === 'good'" 
            class="w-4 h-4 text-green-500" 
            fill="currentColor" 
            viewBox="0 0 20 20"
          >
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
          </svg>
          <svg 
            v-else-if="factor.status === 'warning'" 
            class="w-4 h-4 text-yellow-500" 
            fill="currentColor" 
            viewBox="0 0 20 20"
          >
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
          </svg>
          <svg 
            v-else 
            class="w-4 h-4 text-red-500" 
            fill="currentColor" 
            viewBox="0 0 20 20"
          >
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- Recommendations -->
    <div class="mt-6 pt-4 border-t border-gray-100">
      <h4 class="font-medium text-gray-900 mb-3">Quick Improvements</h4>
      <div class="space-y-2">
        <div 
          v-for="recommendation in recommendations" 
          :key="recommendation"
          class="flex items-start space-x-2 text-sm"
        >
          <div class="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
          <span class="text-gray-600">{{ recommendation }}</span>
        </div>
      </div>
    </div>

    <!-- Action Button -->
    <div class="mt-4">
      <button 
        @click="optimizeContent"
        class="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors font-medium"
      >
        AI Optimize Content
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  tags: {
    type: Array,
    default: () => []
  },
  targetKeyword: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['optimize'])

const circumference = 2 * Math.PI * 50

// Calculate SEO score based on content
const seoFactors = computed(() => {
  const factors = [
    {
      name: 'Title Length',
      score: props.title.length >= 30 && props.title.length <= 60 ? 20 : props.title.length > 0 ? 10 : 0,
      maxScore: 20,
      status: props.title.length >= 30 && props.title.length <= 60 ? 'good' : props.title.length > 0 ? 'warning' : 'error'
    },
    {
      name: 'Description Length',
      score: props.description.length >= 100 && props.description.length <= 160 ? 20 : props.description.length > 0 ? 10 : 0,
      maxScore: 20,
      status: props.description.length >= 100 && props.description.length <= 160 ? 'good' : props.description.length > 0 ? 'warning' : 'error'
    },
    {
      name: 'Target Keyword',
      score: props.targetKeyword && props.title.toLowerCase().includes(props.targetKeyword.toLowerCase()) ? 20 : props.targetKeyword ? 10 : 0,
      maxScore: 20,
      status: props.targetKeyword && props.title.toLowerCase().includes(props.targetKeyword.toLowerCase()) ? 'good' : props.targetKeyword ? 'warning' : 'error'
    },
    {
      name: 'Tags Count',
      score: props.tags.length >= 5 && props.tags.length <= 10 ? 20 : props.tags.length > 0 ? 10 : 0,
      maxScore: 20,
      status: props.tags.length >= 5 && props.tags.length <= 10 ? 'good' : props.tags.length > 0 ? 'warning' : 'error'
    },
    {
      name: 'Keyword Density',
      score: props.targetKeyword && props.description.toLowerCase().includes(props.targetKeyword.toLowerCase()) ? 20 : 0,
      maxScore: 20,
      status: props.targetKeyword && props.description.toLowerCase().includes(props.targetKeyword.toLowerCase()) ? 'good' : 'error'
    }
  ]
  
  return factors
})

const seoScore = computed(() => {
  const totalScore = seoFactors.value.reduce((sum, factor) => sum + factor.score, 0)
  return Math.round(totalScore)
})

const scoreColor = computed(() => {
  if (seoScore.value >= 80) return 'text-green-600'
  if (seoScore.value >= 60) return 'text-yellow-600'
  return 'text-red-600'
})

const scoreColorHex = computed(() => {
  if (seoScore.value >= 80) return '#059669'
  if (seoScore.value >= 60) return '#d97706'
  return '#dc2626'
})

const scoreLabel = computed(() => {
  if (seoScore.value >= 80) return 'Excellent'
  if (seoScore.value >= 60) return 'Good'
  if (seoScore.value >= 40) return 'Fair'
  return 'Needs Work'
})

const recommendations = computed(() => {
  const recs = []
  
  if (props.title.length < 30) {
    recs.push('Make your title longer (30-60 characters)')
  } else if (props.title.length > 60) {
    recs.push('Shorten your title (30-60 characters)')
  }
  
  if (props.description.length < 100) {
    recs.push('Add more detail to your description (100-160 characters)')
  }
  
  if (!props.targetKeyword) {
    recs.push('Add a target keyword for better SEO')
  } else if (!props.title.toLowerCase().includes(props.targetKeyword.toLowerCase())) {
    recs.push('Include your target keyword in the title')
  }
  
  if (props.tags.length < 5) {
    recs.push('Add more relevant tags (5-10 recommended)')
  }
  
  return recs.slice(0, 3) // Show top 3 recommendations
})

const optimizeContent = () => {
  emit('optimize', {
    currentScore: seoScore.value,
    factors: seoFactors.value,
    recommendations: recommendations.value
  })
}
</script>

<style scoped>
.seo-score-card {
  min-height: 500px;
}
</style>
