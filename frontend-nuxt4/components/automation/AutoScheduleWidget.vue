<template>
  <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
    <!-- Header -->
    <div class="mb-4 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-orange-500">
          <span class="text-white text-sm">📅</span>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-white">Smart Scheduling</h3>
          <p class="text-sm text-gray-400">AI-optimized posting time</p>
        </div>
      </div>
      <button
        v-if="!autoScheduleEnabled"
        @click="enableAutoSchedule"
        class="text-xs text-orange-400 hover:text-orange-300 transition-colors"
      >
        Enable Auto-Schedule
      </button>
    </div>

    <!-- Auto-Schedule Recommendation -->
    <div v-if="recommendation && autoScheduleEnabled" class="space-y-4">
      <!-- Recommended Time -->
      <div class="rounded-lg bg-green-900/30 border border-green-600/30 p-4">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center space-x-2">
            <span class="text-green-400 text-lg">🎯</span>
            <span class="font-medium text-green-300">Optimal Time</span>
          </div>
          <div class="text-right">
            <div class="text-lg font-bold text-green-300">{{ formatDateTime(recommendation.recommended_time) }}</div>
            <div class="text-xs text-green-400">{{ recommendation.confidence_score }}% confidence</div>
          </div>
        </div>
        
        <div class="flex items-center justify-between">
          <p class="text-sm text-green-200">{{ recommendation.reasoning }}</p>
          <div class="text-sm text-green-400">
            +{{ (recommendation.expected_performance_boost * 100).toFixed(1) }}% boost
          </div>
        </div>
      </div>

      <!-- Alternative Times -->
      <div v-if="recommendation.alternative_times && recommendation.alternative_times.length > 0">
        <h4 class="text-sm font-medium text-white mb-2">Alternative Times</h4>
        <div class="space-y-2">
          <div
            v-for="(alt, index) in recommendation.alternative_times"
            :key="index"
            class="flex items-center justify-between p-3 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors cursor-pointer"
            @click="selectAlternativeTime(alt)"
          >
            <div>
              <div class="font-medium text-white">{{ formatDateTime(alt.time) }}</div>
              <div class="text-xs text-gray-400">{{ alt.reasoning }}</div>
            </div>
            <div class="text-sm text-gray-300">{{ alt.confidence }}% confidence</div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center space-x-3">
        <button
          @click="acceptRecommendation"
          :disabled="isScheduling"
          class="flex-1 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          <span v-if="isScheduling" class="animate-spin">⏳</span>
          <span>{{ isScheduling ? 'Scheduling...' : 'Accept & Schedule' }}</span>
        </button>
        <button
          @click="showManualSchedule = true"
          class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-500 transition-colors"
        >
          Manual
        </button>
        <button
          @click="refreshRecommendation"
          :disabled="isLoading"
          class="p-2 bg-gray-600 text-white rounded-lg hover:bg-gray-500 transition-colors disabled:opacity-50"
          title="Refresh recommendation"
        >
          <svg class="h-4 w-4" :class="{ 'animate-spin': isLoading }" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Manual Schedule Mode -->
    <div v-else-if="showManualSchedule || !autoScheduleEnabled" class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Date Picker -->
        <div>
          <label class="block text-sm font-medium text-white mb-2">Date</label>
          <input
            type="date"
            v-model="manualDate"
            :min="today"
            class="w-full rounded-lg border-2 border-gray-600/70 bg-gray-700 px-4 py-3 text-white focus:border-orange-500 focus:outline-none"
          />
        </div>

        <!-- Time Picker -->
        <div>
          <label class="block text-sm font-medium text-white mb-2">Time</label>
          <input
            type="time"
            v-model="manualTime"
            class="w-full rounded-lg border-2 border-gray-600/70 bg-gray-700 px-4 py-3 text-white focus:border-orange-500 focus:outline-none"
          />
        </div>
      </div>

      <!-- Manual Schedule Actions -->
      <div class="flex items-center space-x-3">
        <button
          @click="scheduleManually"
          :disabled="!manualDate || !manualTime || isScheduling"
          class="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          <span v-if="isScheduling" class="animate-spin">⏳</span>
          <span>{{ isScheduling ? 'Scheduling...' : 'Schedule Manually' }}</span>
        </button>
        <button
          v-if="autoScheduleEnabled"
          @click="showManualSchedule = false"
          class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-500 transition-colors"
        >
          Back to AI
        </button>
      </div>

      <!-- Performance Prediction for Manual Time -->
      <div v-if="manualDate && manualTime" class="rounded-lg bg-blue-900/30 border border-blue-600/30 p-3">
        <div class="flex items-center space-x-2 mb-1">
          <span class="text-blue-400 text-sm">📊</span>
          <span class="text-sm font-medium text-blue-300">Performance Prediction</span>
        </div>
        <p class="text-xs text-blue-200">
          {{ getManualTimePrediction() }}
        </p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else-if="isLoading" class="text-center py-8">
      <div class="animate-spin text-2xl mb-2">⏳</div>
      <p class="text-sm text-gray-400">Analyzing optimal posting time...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-8">
      <div class="text-red-400 text-2xl mb-2">⚠️</div>
      <p class="text-sm text-red-400 mb-3">{{ error }}</p>
      <button
        @click="refreshRecommendation"
        class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
      >
        Try Again
      </button>
    </div>

    <!-- Disabled State -->
    <div v-else class="text-center py-8">
      <div class="text-gray-400 text-2xl mb-2">📅</div>
      <p class="text-sm text-gray-400 mb-3">Auto-scheduling is disabled</p>
      <button
        @click="enableAutoSchedule"
        class="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
      >
        Enable Smart Scheduling
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAutomation } from '../../composables/useAutomation'
import { useToast } from '../../composables/useToast'

const props = defineProps({
  contentData: {
    type: Object,
    required: true
  },
  autoScheduleEnabled: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['scheduled', 'enableAutoSchedule'])

const { scheduleContent } = useAutomation()
const { success, error: showError } = useToast()

// State
const recommendation = ref(null)
const isLoading = ref(false)
const isScheduling = ref(false)
const error = ref(null)
const showManualSchedule = ref(false)

// Manual scheduling
const manualDate = ref('')
const manualTime = ref('')

// Computed
const today = computed(() => {
  return new Date().toISOString().split('T')[0]
})

// Methods
const getRecommendation = async () => {
  if (!props.contentData || !props.autoScheduleEnabled) return

  try {
    isLoading.value = true
    error.value = null
    
    const result = await scheduleContent({
      content_id: props.contentData.id || 'new-content',
      title: props.contentData.title || 'Untitled',
      content_type: props.contentData.type || 'video',
      description: props.contentData.description || '',
      tags: props.contentData.tags || []
    })
    
    recommendation.value = result
  } catch (err) {
    error.value = 'Failed to get scheduling recommendation'
    console.error('Scheduling error:', err)
  } finally {
    isLoading.value = false
  }
}

const refreshRecommendation = () => {
  getRecommendation()
}

const acceptRecommendation = async () => {
  if (!recommendation.value) return

  try {
    isScheduling.value = true
    
    // In production, would call API to actually schedule the content
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API call
    
    emit('scheduled', {
      time: recommendation.value.recommended_time,
      type: 'auto',
      confidence: recommendation.value.confidence_score
    })
    
    success('Content Scheduled', `Content scheduled for ${formatDateTime(recommendation.value.recommended_time)}`)
  } catch (err) {
    showError('Scheduling Failed', 'Failed to schedule content')
  } finally {
    isScheduling.value = false
  }
}

const selectAlternativeTime = (alternative) => {
  // Update recommendation with selected alternative
  recommendation.value = {
    ...recommendation.value,
    recommended_time: alternative.time,
    confidence_score: alternative.confidence,
    reasoning: alternative.reasoning
  }
}

const scheduleManually = async () => {
  if (!manualDate.value || !manualTime.value) return

  try {
    isScheduling.value = true
    
    const scheduledTime = `${manualDate.value}T${manualTime.value}:00`
    
    // In production, would call API to schedule the content
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API call
    
    emit('scheduled', {
      time: scheduledTime,
      type: 'manual',
      confidence: null
    })
    
    success('Content Scheduled', `Content scheduled for ${formatDateTime(scheduledTime)}`)
  } catch (err) {
    showError('Scheduling Failed', 'Failed to schedule content manually')
  } finally {
    isScheduling.value = false
  }
}

const enableAutoSchedule = () => {
  emit('enableAutoSchedule')
  getRecommendation()
}

const formatDateTime = (dateTimeString) => {
  const date = new Date(dateTimeString)
  return date.toLocaleString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}

const getManualTimePrediction = () => {
  if (!manualDate.value || !manualTime.value) return ''

  const selectedDate = new Date(`${manualDate.value}T${manualTime.value}`)
  const dayOfWeek = selectedDate.getDay()
  const hour = selectedDate.getHours()

  // Simple prediction logic
  let prediction = 'Average performance expected'
  
  if ([1, 2, 4].includes(dayOfWeek) && hour >= 18 && hour <= 21) {
    prediction = 'Good performance expected (+15-25% above average)'
  } else if ([0, 6].includes(dayOfWeek) && hour >= 14 && hour <= 18) {
    prediction = 'Moderate performance expected (+5-15% above average)'
  } else if (hour < 8 || hour > 23) {
    prediction = 'Lower performance expected (-10-20% below average)'
  }

  return prediction
}

// Watchers
watch(() => props.contentData, () => {
  if (props.autoScheduleEnabled) {
    getRecommendation()
  }
}, { deep: true })

watch(() => props.autoScheduleEnabled, (enabled) => {
  if (enabled) {
    getRecommendation()
  } else {
    recommendation.value = null
    showManualSchedule.value = false
  }
})

// Initialize
onMounted(() => {
  if (props.autoScheduleEnabled && props.contentData) {
    getRecommendation()
  }
})
</script>
