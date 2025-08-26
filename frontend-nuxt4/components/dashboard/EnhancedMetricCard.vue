<template>
  <div
    class="enhanced-metric-card group"
    :class="[
      'relative overflow-hidden rounded-xl bg-gradient-to-br p-4 transition-all duration-300',
      'hover:scale-105 hover:shadow-xl cursor-pointer',
      gradientClass
    ]"
    @click="$emit('click')"
  >
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
      <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
    </div>

    <!-- Content -->
    <div class="relative z-10">
      <!-- Header with Icon and Change -->
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center space-x-2">
          <div class="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center">
            <span class="text-lg">{{ icon }}</span>
          </div>
          <span class="text-base font-semibold text-white/90">{{ label }}</span>
        </div>

        <div class="flex items-center space-x-2">
          <!-- Goal Setting Icon -->
          <button
            v-if="progress !== null"
            @click.stop="$emit('edit-goal')"
            class="w-6 h-6 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors group/goal"
            title="Edit goal"
          >
            <svg class="w-3 h-3 text-white/60 group-hover/goal:text-white/80" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
            </svg>
          </button>

          <!-- Change Indicator -->
          <div
            v-if="change !== null"
            class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold"
            :class="changeClass"
          >
            <span>{{ changeIcon }}</span>
            <span>{{ Math.abs(change) }}%</span>
          </div>
        </div>
      </div>

      <!-- Main Value with Animation -->
      <div class="mb-3">
        <div class="text-2xl font-bold text-white leading-tight">
          {{ displayValue }}
        </div>
        <div class="text-sm text-white/70">{{ subtitle }}</div>
      </div>

      <!-- Progress Display (if currentValue and goalValue are provided) -->
      <div v-if="currentValue !== null && goalValue !== null" class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
            <span class="text-sm font-semibold text-white">
              {{ formatProgressValue(currentValue) }} of {{ formatProgressValue(goalValue) }}
            </span>
          </div>
          <span class="text-sm text-white/70 font-medium">{{ progressLabel }}</span>
        </div>

        <!-- Trend Indicator -->
        <div v-if="trend" class="flex items-center space-x-1">
          <div class="w-12 h-6 relative">
            <!-- Mini Sparkline -->
            <svg class="w-full h-full" viewBox="0 0 48 24">
              <polyline
                :points="sparklinePoints"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                class="text-white/70"
              />
            </svg>
          </div>
        </div>
      </div>

      <!-- Fallback Progress Ring (if only progress percentage is provided) -->
      <div v-else-if="progress !== null" class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <div class="relative w-8 h-8">
            <!-- Background Circle -->
            <svg class="w-8 h-8 transform -rotate-90" viewBox="0 0 32 32">
              <circle
                cx="16"
                cy="16"
                r="14"
                stroke="currentColor"
                stroke-width="2.5"
                fill="none"
                class="text-white/20"
              />
              <!-- Progress Circle -->
              <circle
                cx="16"
                cy="16"
                r="14"
                stroke="currentColor"
                stroke-width="2.5"
                fill="none"
                stroke-linecap="round"
                class="text-white transition-all duration-1000 ease-out"
                :stroke-dasharray="circumference"
                :stroke-dashoffset="progressOffset"
              />
            </svg>
            <!-- Progress Text -->
            <div class="absolute inset-0 flex items-center justify-center">
              <span class="text-xs font-bold text-white">{{ Math.round(progress) }}%</span>
            </div>
          </div>
          <span class="text-sm text-white/70 font-medium">{{ progressLabel }}</span>
        </div>

        <!-- Trend Indicator -->
        <div v-if="trend" class="flex items-center space-x-1">
          <div class="w-12 h-6 relative">
            <!-- Mini Sparkline -->
            <svg class="w-full h-full" viewBox="0 0 48 24">
              <polyline
                :points="sparklinePoints"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                class="text-white/70"
              />
            </svg>
          </div>
        </div>
      </div>

      <!-- Achievement Badge (if provided) -->
      <div v-if="achievement" class="mt-3 flex items-center space-x-2">
        <div class="w-5 h-5 rounded-full bg-yellow-400 flex items-center justify-center">
          <span class="text-xs">🏆</span>
        </div>
        <span class="text-sm text-white/85 font-semibold">{{ achievement }}</span>
      </div>
    </div>

    <!-- Hover Glow Effect -->
    <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'

const props = defineProps({
  label: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    required: true
  },
  change: {
    type: Number,
    default: null
  },
  progress: {
    type: Number,
    default: null // 0-100
  },
  currentValue: {
    type: [Number, String],
    default: null
  },
  goalValue: {
    type: [Number, String],
    default: null
  },
  progressLabel: {
    type: String,
    default: 'Progress'
  },
  trend: {
    type: Array,
    default: null // Array of numbers for sparkline
  },
  achievement: {
    type: String,
    default: null
  },
  color: {
    type: String,
    default: 'blue' // blue, green, yellow, orange, purple, pink
  },
  formatter: {
    type: Function,
    default: null
  }
})

const emit = defineEmits(['click', 'edit-goal'])

// Animated value
const animatedValue = ref(0)
const displayValue = computed(() => {
  if (props.formatter) {
    return props.formatter(animatedValue.value)
  }
  return typeof animatedValue.value === 'number' 
    ? animatedValue.value.toLocaleString() 
    : animatedValue.value
})

// Color schemes
const gradientClass = computed(() => {
  const gradients = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600', 
    yellow: 'from-yellow-500 to-yellow-600',
    orange: 'from-orange-500 to-orange-600',
    purple: 'from-purple-500 to-purple-600',
    pink: 'from-pink-500 to-pink-600'
  }
  return gradients[props.color] || gradients.blue
})

// Change indicator
const changeClass = computed(() => {
  if (props.change === null) return ''
  return props.change >= 0 
    ? 'bg-green-500/20 text-green-300' 
    : 'bg-red-500/20 text-red-300'
})

const changeIcon = computed(() => {
  if (props.change === null) return ''
  return props.change >= 0 ? '↗️' : '↘️'
})

// Progress ring calculations
const circumference = 2 * Math.PI * 14 // radius = 14
const progressOffset = computed(() => {
  if (props.progress === null) return circumference
  const progress = Math.max(0, Math.min(100, props.progress))
  return circumference - (progress / 100) * circumference
})

// Sparkline points
const sparklinePoints = computed(() => {
  if (!props.trend || props.trend.length === 0) return ''

  const width = 48
  const height = 24
  const padding = 2

  const min = Math.min(...props.trend)
  const max = Math.max(...props.trend)
  const range = max - min || 1

  return props.trend.map((value, index) => {
    const x = padding + (index / (props.trend.length - 1)) * (width - 2 * padding)
    const y = height - padding - ((value - min) / range) * (height - 2 * padding)
    return `${x},${y}`
  }).join(' ')
})

// Format progress values for display
const formatProgressValue = (value) => {
  if (typeof value === 'number') {
    if (value >= 1000000) {
      return (value / 1000000).toFixed(1) + 'M'
    } else if (value >= 1000) {
      return (value / 1000).toFixed(1) + 'K'
    } else {
      return value.toLocaleString()
    }
  }
  return value
}

// Animation
const animateValue = () => {
  const targetValue = typeof props.value === 'number' ? props.value : 0
  const startValue = 0
  const duration = 1500 // 1.5 seconds
  const startTime = Date.now()
  
  const animate = () => {
    const elapsed = Date.now() - startTime
    const progress = Math.min(elapsed / duration, 1)
    
    // Easing function (ease-out)
    const easeOut = 1 - Math.pow(1 - progress, 3)
    
    animatedValue.value = Math.round(startValue + (targetValue - startValue) * easeOut)
    
    if (progress < 1) {
      requestAnimationFrame(animate)
    }
  }
  
  requestAnimationFrame(animate)
}

// Watch for value changes
watch(() => props.value, () => {
  animateValue()
}, { immediate: false })

// Initialize animation on mount
onMounted(() => {
  // Small delay to make the animation more noticeable
  setTimeout(() => {
    animateValue()
  }, 100)
})
</script>

<style scoped>
.enhanced-metric-card {
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.enhanced-metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
</style>
