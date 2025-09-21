<template>
  <div
    class="flex items-center justify-center"
    :class="containerClass"
    role="status"
    :aria-label="ariaLabel"
    aria-live="polite"
  >
    <div class="relative">
      <!-- Spinner -->
      <div
        class="animate-spin rounded-full border-2 border-gray-300"
        :class="[
          sizeClass,
          `border-t-${color}-500`
        ]"
        :aria-hidden="true"
      >
        <span class="sr-only">{{ loadingMessage }}</span>
      </div>

      <!-- Optional text -->
      <div v-if="text" class="mt-3 text-center">
        <p :class="textClass" :id="textId">{{ text }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  color: {
    type: String,
    default: 'blue'
  },
  text: {
    type: String,
    default: ''
  },
  overlay: {
    type: Boolean,
    default: false
  },
  loadingMessage: {
    type: String,
    default: 'Loading content, please wait...'
  }
})

// Generate unique ID for accessibility
const textId = ref(`loading-text-${Math.random().toString(36).substr(2, 9)}`)

const sizeClass = computed(() => {
  const sizes = {
    xs: 'h-4 w-4',
    sm: 'h-6 w-6', 
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
    xl: 'h-16 w-16'
  }
  return sizes[props.size]
})

const textClass = computed(() => {
  const textSizes = {
    xs: 'text-xs',
    sm: 'text-sm',
    md: 'text-sm', 
    lg: 'text-base',
    xl: 'text-lg'
  }
  return `${textSizes[props.size]} text-text-secondary`
})

const containerClass = computed(() => {
  if (props.overlay) {
    return 'fixed inset-0 bg-black bg-opacity-50 z-50 backdrop-blur-sm'
  }
  return 'p-4'
})

const ariaLabel = computed(() => {
  return props.text ? undefined : props.loadingMessage
})
</script>
