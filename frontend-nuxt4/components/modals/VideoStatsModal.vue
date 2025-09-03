<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-start justify-center bg-black bg-opacity-50 pt-80 pb-8 px-8 overflow-y-auto" @click="$emit('close')">
    <div class="w-full max-w-4xl bg-forest-800 rounded-xl p-6" @click.stop>
      <!-- Modal Header -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center space-x-4">
          <img :src="video?.thumbnail" :alt="video?.title" class="w-16 h-10 object-cover rounded-lg">
          <div>
            <h3 class="text-xl font-bold text-white">{{ video?.title }}</h3>
            <p class="text-sm text-gray-400">Published {{ formatDate(video?.publishedAt || video?.date) }}</p>
          </div>
        </div>
        <button @click="$emit('close')" class="text-gray-400 hover:text-white">
          <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
          </svg>
        </button>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-forest-700 rounded-lg p-4 text-center">
          <div class="text-2xl font-bold text-blue-400">{{ formatNumber(getVideoStat('views')) }}</div>
          <div class="text-sm text-gray-400">Total Views</div>
          <div class="text-xs text-green-400 mt-1">+{{ getVideoStat('viewsGrowth') || getVideoStat('viewsTrend') || 0 }}%</div>
        </div>
        <div class="bg-forest-700 rounded-lg p-4 text-center">
          <div class="text-2xl font-bold text-green-400">{{ getVideoStat('likes') || Math.round(getVideoStat('views') * 0.05) }}</div>
          <div class="text-sm text-gray-400">Likes</div>
          <div class="text-xs text-green-400 mt-1">{{ getVideoStat('likeRatio') || getVideoStat('ctr') || 0 }}% ratio</div>
        </div>
        <div class="bg-forest-700 rounded-lg p-4 text-center">
          <div class="text-2xl font-bold text-yellow-400">{{ getVideoStat('comments') || Math.round(getVideoStat('views') * 0.02) }}</div>
          <div class="text-sm text-gray-400">Comments</div>
          <div class="text-xs text-blue-400 mt-1">{{ getVideoStat('engagement') || 0 }}% engagement</div>
        </div>
        <div class="bg-forest-700 rounded-lg p-4 text-center">
          <div class="text-2xl font-bold text-purple-400">{{ getVideoStat('watchTime') || video?.duration || '0:00' }}</div>
          <div class="text-sm text-gray-400">Avg Watch Time</div>
          <div class="text-xs text-purple-400 mt-1">{{ getVideoStat('retention') || Math.round((getVideoStat('engagement') || 0) * 10) }}% retention</div>
        </div>
      </div>

      <!-- Performance Metrics -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <!-- Content Details -->
        <div class="bg-forest-700 rounded-lg p-4">
          <h4 class="text-lg font-semibold text-white mb-4">Content Details</h4>
          <div class="space-y-3">
            <div v-if="video?.pillar" class="flex items-center justify-between">
              <span class="text-gray-300">Pillar</span>
              <span class="text-sm px-2 py-1 rounded" :class="getPillarClass(video.pillar)">
                📌 {{ video.pillar }}
              </span>
            </div>
            <div v-if="video?.category" class="flex items-center justify-between">
              <span class="text-gray-300">Category</span>
              <span class="text-sm text-gray-400 bg-forest-600 px-2 py-1 rounded">{{ video.category }}</span>
            </div>
            <div v-if="video?.performance" class="flex items-center justify-between">
              <span class="text-gray-300">Performance</span>
              <span class="text-sm px-2 py-1 rounded" :class="getPerformanceClass(video.performance)">
                {{ video.performance }}
              </span>
            </div>
          </div>
        </div>

        <!-- Traffic Sources or Performance Trends -->
        <div class="bg-forest-700 rounded-lg p-4">
          <h4 class="text-lg font-semibold text-white mb-4">
            {{ hasTrafficSources ? 'Traffic Sources' : 'Performance Trends' }}
          </h4>
          <div class="space-y-3">
            <template v-if="hasTrafficSources">
              <div v-for="source in getVideoStat('trafficSources')" :key="source.name" class="flex items-center justify-between">
                <span class="text-gray-300">{{ source.name }}</span>
                <div class="flex items-center space-x-2">
                  <div class="w-20 bg-forest-600 rounded-full h-2">
                    <div class="bg-orange-500 h-2 rounded-full" :style="{ width: source.percentage + '%' }"></div>
                  </div>
                  <span class="text-sm text-gray-400">{{ source.percentage }}%</span>
                </div>
              </div>
            </template>
            <template v-else>
              <div class="flex items-center justify-between">
                <span class="text-gray-300">Views Trend</span>
                <span class="text-sm flex items-center" :class="getTrendClass('viewsTrend')">
                  <svg v-if="getTrendValue('viewsTrend') > 0" class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L10 4.414 6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <svg v-else class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L10 15.586l3.293-3.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  {{ Math.abs(getTrendValue('viewsTrend')) }}%
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-300">CTR Trend</span>
                <span class="text-sm flex items-center" :class="getTrendClass('ctrTrend')">
                  <svg v-if="getTrendValue('ctrTrend') > 0" class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L10 4.414 6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <svg v-else class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L10 15.586l3.293-3.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  {{ Math.abs(getTrendValue('ctrTrend')) }}%
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-300">Engagement Trend</span>
                <span class="text-sm flex items-center" :class="getTrendClass('engagementTrend')">
                  <svg v-if="getTrendValue('engagementTrend') > 0" class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L10 4.414 6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <svg v-else class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L10 15.586l3.293-3.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  {{ Math.abs(getTrendValue('engagementTrend')) }}%
                </span>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Agent Suggestions -->
      <div class="mt-6 bg-gradient-to-r from-orange-500/10 to-red-500/10 rounded-lg p-4 border border-orange-500/20">
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
          </div>
          <div>
            <h4 class="text-lg font-semibold text-white">{{ agentName || 'Boss Agent' }} Recommendations</h4>
            <p class="text-sm text-gray-400">AI-powered suggestions to optimize this video</p>
          </div>
        </div>

        <div v-if="convertedRecommendations.size < 3" class="space-y-3">
          <!-- Performance Optimization -->
          <div v-if="!convertedRecommendations.has('thumbnail')" class="bg-forest-700/50 rounded-lg p-3 border-l-4 border-blue-500">
            <div class="flex items-start space-x-3 justify-between">
              <div class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div class="flex-1">
                <h5 class="font-medium text-white">Improve Thumbnail</h5>
                <p class="text-sm text-gray-300 mt-1">Your click-through rate is {{ getVideoStat('ctr') || '3.2' }}%. Consider A/B testing a brighter thumbnail with larger text to increase CTR by 15-25%.</p>
              </div>
              <button
                @click="saveRecommendationAsTask('thumbnail')"
                class="px-3 py-1 text-xs font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors flex-shrink-0"
              >
                Save as Task
              </button>
            </div>
          </div>

          <!-- SEO Optimization -->
          <div v-if="!convertedRecommendations.has('seo')" class="bg-forest-700/50 rounded-lg p-3 border-l-4 border-green-500">
            <div class="flex items-start space-x-3 justify-between">
              <div class="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div class="flex-1">
                <h5 class="font-medium text-white">Optimize Tags & Description</h5>
                <p class="text-sm text-gray-300 mt-1">Add trending keywords and update description with timestamps to improve discoverability.</p>
              </div>
              <button
                @click="saveRecommendationAsTask('seo')"
                class="px-3 py-1 text-xs font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 transition-colors flex-shrink-0"
              >
                Save as Task
              </button>
            </div>
          </div>

          <!-- Content Strategy -->
          <div v-if="!convertedRecommendations.has('content')" class="bg-forest-700/50 rounded-lg p-3 border-l-4 border-purple-500">
            <div class="flex items-start space-x-3 justify-between">
              <div class="w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="flex-1">
                <h5 class="font-medium text-white">Create Follow-up Content</h5>
                <p class="text-sm text-gray-300 mt-1">This video has {{ getVideoStat('engagement') || '4.2' }}% engagement. Create a "Part 2" or "Advanced Tips" video to capitalize on viewer interest.</p>
              </div>
              <button
                @click="saveRecommendationAsTask('content')"
                class="px-3 py-1 text-xs font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors flex-shrink-0"
              >
                Save as Task
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State - All recommendations converted to tasks -->
        <div v-else class="text-center py-8">
          <div class="w-16 h-16 mx-auto mb-4 bg-green-500/10 rounded-full flex items-center justify-center">
            <svg class="h-8 w-8 text-green-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
          </div>
          <h4 class="text-white font-medium mb-2">All recommendations converted!</h4>
          <p class="text-sm text-gray-400">Great job! All {{ agentName || 'Boss Agent' }} recommendations have been saved as tasks.</p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center justify-end space-x-3 mt-6">
        <button
          @click="$emit('close')"
          class="px-4 py-2 text-sm font-medium text-gray-300 bg-forest-700 rounded-lg hover:bg-forest-600 transition-colors"
        >
          Close
        </button>
        <button
          @click="openYouTubeStudio"
          class="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors"
        >
          Open in YouTube Studio
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAgentSettings } from '../../composables/useAgentSettings'
import { useRecommendations } from '../../composables/useRecommendations'
import { useToast } from '../../composables/useToast'
import { useTasksStore } from '../../stores/tasks'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  video: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close'])

// Composables
const { agentName } = useAgentSettings()
const tasksStore = useTasksStore()
const { success, error } = useToast()
const { addRecommendation, markAsConverted, getRecommendationsBySource } = useRecommendations()

// Track which recommendations have been converted to tasks for this video
const convertedRecommendations = ref(new Set())

// Get existing recommendations for this video
const videoRecommendations = computed(() => {
  if (!props.video) return []
  return getRecommendationsBySource('video-modal', props.video.id)
})

// Helper methods
const formatNumber = (num) => {
  if (!num) return '0'
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const formatDate = (dateString) => {
  if (!dateString) return 'Unknown'
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) return '1 day ago'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  return `${Math.floor(diffDays / 30)} months ago`
}

const getVideoStat = (statName) => {
  if (!props.video) return 0
  
  // Check detailedStats first (from videos page)
  if (props.video.detailedStats && props.video.detailedStats[statName] !== undefined) {
    return props.video.detailedStats[statName]
  }
  
  // Check direct properties (from dashboard)
  if (props.video[statName] !== undefined) {
    return props.video[statName]
  }
  
  return 0
}

const getPillarClass = (pillar) => {
  const pillarColors = {
    'Growth Strategies': 'bg-orange-600 text-white',
    'Personal Stories': 'bg-purple-600 text-white',
    'Content Creation': 'bg-blue-600 text-white',
    'Behind the Scenes': 'bg-pink-600 text-white',
    'Tutorials': 'bg-green-600 text-white',
    'Reviews': 'bg-indigo-600 text-white',
    'Entertainment': 'bg-red-600 text-white',
    'Educational': 'bg-teal-600 text-white'
  }
  
  return pillarColors[pillar] || 'bg-gray-600 text-white'
}

const getPerformanceClass = (performance) => {
  switch (performance?.toLowerCase()) {
    case 'excellent':
      return 'bg-green-600 text-white'
    case 'good':
      return 'bg-blue-600 text-white'
    case 'average':
      return 'bg-yellow-600 text-white'
    case 'poor':
      return 'bg-red-600 text-white'
    default:
      return 'bg-gray-600 text-white'
  }
}

const getTrendValue = (trendName) => {
  return getVideoStat(trendName) || 0
}

const getTrendClass = (trendName) => {
  const value = getTrendValue(trendName)
  return value > 0 ? 'text-green-400' : value < 0 ? 'text-red-400' : 'text-gray-400'
}

const hasTrafficSources = computed(() => {
  return props.video?.detailedStats?.trafficSources && props.video.detailedStats.trafficSources.length > 0
})

const openYouTubeStudio = () => {
  if (!props.video) return

  const youtubeStudioUrl = `https://studio.youtube.com/video/${props.video.id}/edit`
  window.open(youtubeStudioUrl, '_blank')
}

const saveRecommendationAsTask = (type) => {
  if (!props.video) return

  const videoTitle = props.video.title || 'Video'
  const recommendations = {
    thumbnail: {
      title: `Improve Thumbnail for "${videoTitle}"`,
      description: `A/B test a brighter thumbnail with larger text to increase CTR. Current CTR: ${getVideoStat('ctr') || '3.2'}%. Target: 15-25% improvement.`,
      category: 'content',
      priority: 'medium'
    },
    seo: {
      title: `Optimize SEO for "${videoTitle}"`,
      description: `Add trending keywords and update description with timestamps to improve discoverability. Focus on tags and description optimization.`,
      category: 'seo',
      priority: 'medium'
    },
    content: {
      title: `Create Follow-up Content for "${videoTitle}"`,
      description: `Create a "Part 2" or "Advanced Tips" video to capitalize on viewer interest. Current engagement: ${getVideoStat('engagement') || '4.2'}%.`,
      category: 'content',
      priority: 'high'
    }
  }

  const recommendation = recommendations[type]
  if (!recommendation) return

  try {
    // Set due date to 1 week from now
    const dueDate = new Date()
    dueDate.setDate(dueDate.getDate() + 7)

    const taskData = {
      title: recommendation.title,
      description: recommendation.description,
      category: recommendation.category,
      priority: recommendation.priority,
      dueDate,
      tags: ['agent-generated', agentName.value?.toLowerCase().replace(/\s+/g, '-') || 'boss-agent', 'video-optimization'],
      estimatedTime: 60, // 1 hour default
      agentId: '0', // Boss Agent ID
      notes: `Generated from ${agentName.value || 'Boss Agent'} recommendation for video: ${videoTitle}`
    }

    const newTask = tasksStore.addTask(taskData)

    // Add recommendation to global store
    const recommendationId = addRecommendation({
      type,
      title: recommendation.title,
      description: recommendation.description,
      category: recommendation.category,
      priority: recommendation.priority,
      source: 'video-modal',
      sourceId: props.video.id,
      agentId: '0'
    })

    // Mark as converted immediately
    markAsConverted(recommendationId, newTask.id)

    // Mark this recommendation as converted in local state (hide it from the UI)
    convertedRecommendations.value.add(type)

    success(`Task created: ${recommendation.title}`)
  } catch (err) {
    console.error('Error creating task:', err)
    error('Failed to create task')
  }
}
</script>
