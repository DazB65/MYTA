<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-75 backdrop-blur-sm">
    <div class="text-center">
      <!-- Animated Logo -->
      <div class="mb-6 flex justify-center">
        <div class="relative">
          <div class="h-16 w-16 animate-pulse rounded-2xl bg-pink-500 flex items-center justify-center">
            <span class="text-2xl">✨</span>
          </div>
          <!-- Spinning Ring -->
          <div class="absolute inset-0 h-16 w-16 animate-spin rounded-full border-2 border-transparent border-t-pink-400" />
        </div>
      </div>
      
      <!-- Loading Text -->
      <h2 class="mb-2 text-xl font-semibold text-white">
        {{ loadingText }}
      </h2>
      
      <!-- Loading Subtitle -->
      <p class="text-sm text-gray-400">
        {{ loadingSubtext }}
      </p>
      
      <!-- Progress Bar (optional) -->
      <div v-if="showProgress" class="mt-4 w-64 mx-auto">
        <div class="h-1 w-full bg-gray-700 rounded-full overflow-hidden">
          <div 
            class="h-full bg-gradient-to-r from-pink-500 to-purple-500 transition-all duration-300 ease-out"
            :style="{ width: `${progress}%` }"
          />
        </div>
        <p class="mt-2 text-xs text-gray-500">{{ progress }}%</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

interface Props {
  text?: string
  subtext?: string
  showProgress?: boolean
  progress?: number
}

const props = withDefaults(defineProps<Props>(), {
  text: 'Loading...',
  subtext: 'Please wait while we prepare your dashboard',
  showProgress: false,
  progress: 0
})

// Dynamic loading messages
const loadingMessages = [
  'Loading your dashboard...',
  'Preparing AI agents...',
  'Fetching analytics data...',
  'Optimizing performance...',
  'Almost ready...'
]

const loadingSubtexts = [
  'Please wait while we prepare your dashboard',
  'Your AI agents are getting ready',
  'Gathering your latest YouTube insights',
  'Ensuring the best experience',
  'Just a moment more...'
]

const loadingText = ref(props.text)
const loadingSubtext = ref(props.subtext)

let messageInterval: NodeJS.Timeout | null = null

onMounted(() => {
  // Cycle through loading messages if no custom text provided
  if (props.text === 'Loading...') {
    let messageIndex = 0
    
    messageInterval = setInterval(() => {
      messageIndex = (messageIndex + 1) % loadingMessages.length
      loadingText.value = loadingMessages[messageIndex]
      loadingSubtext.value = loadingSubtexts[messageIndex]
    }, 2000)
  }
})

onUnmounted(() => {
  if (messageInterval) {
    clearInterval(messageInterval)
  }
})
</script>

<style scoped>
/* Custom animations */
@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(236, 72, 153, 0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(236, 72, 153, 0.6);
  }
}

.animate-pulse {
  animation: pulse-glow 2s ease-in-out infinite;
}

/* Backdrop blur fallback */
@supports not (backdrop-filter: blur(8px)) {
  .backdrop-blur-sm {
    background-color: rgba(17, 24, 39, 0.9);
  }
}
</style>
