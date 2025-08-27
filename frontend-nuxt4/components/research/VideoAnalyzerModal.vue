<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-hidden">
      <!-- Modal Header -->
      <div class="bg-forest-800 text-white p-4 flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="h-8 w-8 rounded-lg bg-orange-500 flex items-center justify-center">
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd"/>
            </svg>
          </div>
          <h2 class="text-xl font-semibold">Video Analyzer</h2>
        </div>
        <button @click="$emit('close')" class="text-gray-300 hover:text-white">
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Modal Content -->
      <div class="p-6 overflow-y-auto max-h-[calc(90vh-80px)]">
        <!-- URL Input Section -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">YouTube Video URL</label>
          <div class="flex space-x-3">
            <input
              v-model="videoUrl"
              type="text"
              placeholder="https://youtube.com/watch?v=..."
              class="flex-1 rounded-lg border border-gray-300 px-3 py-2 focus:border-orange-500 focus:outline-none focus:ring-1 focus:ring-orange-500"
            />
            <button
              @click="analyzeVideo"
              :disabled="isAnalyzing || !videoUrl.trim()"
              class="rounded-lg bg-orange-500 px-6 py-2 text-white transition-colors hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isAnalyzing ? 'Analyzing...' : 'Analyze' }}
            </button>
          </div>
        </div>

        <!-- Analysis Results -->
        <div v-if="analysisResults" class="space-y-6">
          <!-- Video Info -->
          <div class="bg-gray-50 rounded-lg p-4">
            <div class="flex items-start space-x-4">
              <img :src="analysisResults.thumbnail" :alt="analysisResults.title" class="w-32 h-24 object-cover rounded-lg" />
              <div class="flex-1">
                <h3 class="font-semibold text-lg text-gray-900">{{ analysisResults.title }}</h3>
                <p class="text-gray-600">{{ analysisResults.channelName }}</p>
                <div class="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                  <span>{{ formatViews(analysisResults.views) }} views</span>
                  <span>{{ formatDuration(analysisResults.duration) }}</span>
                  <span>{{ formatDate(analysisResults.publishedAt) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Analysis Score -->
          <div class="bg-gradient-to-r from-orange-50 to-orange-100 rounded-lg p-4">
            <div class="flex items-center justify-between">
              <h4 class="text-lg font-semibold text-gray-900">Overall Analysis Score</h4>
              <div class="text-3xl font-bold" :class="getScoreColor(analysisResults.analysis.overallScore)">
                {{ analysisResults.analysis.overallScore }}/100
              </div>
            </div>
            <div class="mt-2 bg-gray-200 rounded-full h-2">
              <div 
                class="h-2 rounded-full transition-all duration-500"
                :class="getScoreBarColor(analysisResults.analysis.overallScore)"
                :style="{ width: `${analysisResults.analysis.overallScore}%` }"
              ></div>
            </div>
          </div>

          <!-- Key Insights -->
          <div class="bg-white border border-gray-200 rounded-lg p-4">
            <h4 class="text-lg font-semibold text-gray-900 mb-4">Key Insights</h4>
            <div class="space-y-3">
              <div 
                v-for="insight in analysisResults.analysis.keyInsights" 
                :key="insight.id"
                class="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg"
              >
                <div class="h-6 w-6 rounded-full bg-orange-500 flex items-center justify-center flex-shrink-0">
                  <svg class="h-3 w-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div class="flex-1">
                  <p class="text-gray-900">{{ insight.text }}</p>
                  <span class="inline-block mt-1 px-2 py-1 text-xs font-medium rounded-full" 
                        :class="getInsightTypeColor(insight.type)">
                    {{ insight.type }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Tags -->
          <div class="bg-white border border-gray-200 rounded-lg p-4">
            <h4 class="text-lg font-semibold text-gray-900 mb-3">Content Tags</h4>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="tag in analysisResults.analysis.tags" 
                :key="tag"
                class="px-3 py-1 bg-orange-100 text-orange-800 text-sm font-medium rounded-full"
              >
                {{ tag }}
              </span>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex space-x-3">
            <button
              @click="addToCanvas"
              class="flex-1 rounded-lg bg-orange-500 px-4 py-2 text-white transition-colors hover:bg-orange-600"
            >
              Add to Research Canvas
            </button>
            <button
              @click="exportAnalysis"
              class="rounded-lg border border-gray-300 px-4 py-2 text-gray-700 transition-colors hover:bg-gray-50"
            >
              Export Analysis
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-else-if="isAnalyzing" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
          <p class="mt-4 text-gray-600">Analyzing video content...</p>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
          </svg>
          <h3 class="mt-4 text-lg font-medium text-gray-900">No video analyzed yet</h3>
          <p class="mt-2 text-gray-500">Enter a YouTube URL above to get started with AI-powered video analysis.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  show: boolean
}

interface Emits {
  (e: 'close'): void
  (e: 'addToCanvas', video: any): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const videoUrl = ref('')
const isAnalyzing = ref(false)
const analysisResults = ref(null)

const analyzeVideo = async () => {
  if (!videoUrl.value.trim()) return

  isAnalyzing.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 3000))
    
    // Mock analysis results
    analysisResults.value = {
      title: 'How to Create Viral YouTube Content in 2024',
      channelName: 'Creator Academy',
      thumbnail: 'https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',
      views: 125000,
      duration: 720,
      publishedAt: '2024-01-15',
      analysis: {
        overallScore: 85,
        keyInsights: [
          { id: 1, type: 'engagement', text: 'Strong hook in first 15 seconds increases retention' },
          { id: 2, type: 'content', text: 'Clear value proposition throughout the video' },
          { id: 3, type: 'seo', text: 'Well-optimized title and description for search' }
        ],
        tags: ['viral', 'content creation', 'youtube strategy', 'engagement']
      }
    }
  } catch (error) {
    console.error('Analysis failed:', error)
  } finally {
    isAnalyzing.value = false
  }
}

const addToCanvas = () => {
  if (analysisResults.value) {
    emit('addToCanvas', analysisResults.value)
    emit('close')
  }
}

const exportAnalysis = () => {
  if (analysisResults.value) {
    const dataStr = JSON.stringify(analysisResults.value, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'video-analysis.json'
    link.click()
    URL.revokeObjectURL(url)
  }
}

// Helper functions
const formatViews = (views: number) => {
  if (views >= 1000000) return `${(views / 1000000).toFixed(1)}M`
  if (views >= 1000) return `${(views / 1000).toFixed(1)}K`
  return views.toString()
}

const formatDuration = (seconds: number) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const getScoreColor = (score: number) => {
  if (score >= 80) return 'text-green-600'
  if (score >= 60) return 'text-yellow-600'
  return 'text-red-600'
}

const getScoreBarColor = (score: number) => {
  if (score >= 80) return 'bg-green-500'
  if (score >= 60) return 'bg-yellow-500'
  return 'bg-red-500'
}

const getInsightTypeColor = (type: string) => {
  const colors = {
    engagement: 'bg-blue-100 text-blue-800',
    content: 'bg-green-100 text-green-800',
    seo: 'bg-purple-100 text-purple-800',
    thumbnail: 'bg-pink-100 text-pink-800',
    title: 'bg-indigo-100 text-indigo-800',
    timing: 'bg-yellow-100 text-yellow-800'
  }
  return colors[type] || 'bg-gray-100 text-gray-800'
}
</script>
