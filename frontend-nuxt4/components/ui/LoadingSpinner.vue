<template>
  <div class="flex items-center justify-center" :class="containerClass">
    <div class="relative">
      <!-- Spinner -->
      <div 
        class="animate-spin rounded-full border-2 border-gray-300"
        :class="[
          sizeClass,
          `border-t-${color}-500`
        ]"
      ></div>
      
      <!-- Optional text -->
      <div v-if="text" class="mt-3 text-center">
        <p :class="textClass">{{ text }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

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
  }
})

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
  return `${textSizes[props.size]} text-gray-400`
})

const containerClass = computed(() => {
  if (props.overlay) {
    return 'fixed inset-0 bg-black bg-opacity-50 z-50'
  }
  return 'p-4'
})
</script>
