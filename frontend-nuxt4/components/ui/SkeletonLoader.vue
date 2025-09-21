<template>
  <div 
    :class="containerClasses"
    role="status"
    aria-label="Loading content"
    aria-live="polite"
  >
    <!-- Card skeleton -->
    <div v-if="variant === 'card'" class="space-y-4">
      <div class="skeleton-shimmer h-48 w-full rounded-lg"></div>
      <div class="space-y-2">
        <div class="skeleton-shimmer h-4 w-3/4 rounded"></div>
        <div class="skeleton-shimmer h-4 w-1/2 rounded"></div>
      </div>
    </div>

    <!-- List item skeleton -->
    <div v-else-if="variant === 'list'" class="space-y-3">
      <div v-for="i in count" :key="i" class="flex items-center space-x-4">
        <div class="skeleton-shimmer h-12 w-12 rounded-full flex-shrink-0"></div>
        <div class="flex-1 space-y-2">
          <div class="skeleton-shimmer h-4 w-3/4 rounded"></div>
          <div class="skeleton-shimmer h-3 w-1/2 rounded"></div>
        </div>
      </div>
    </div>

    <!-- Text skeleton -->
    <div v-else-if="variant === 'text'" class="space-y-2">
      <div v-for="i in lines" :key="i" class="skeleton-shimmer h-4 rounded" :class="getTextWidth(i)"></div>
    </div>

    <!-- Video card skeleton -->
    <div v-else-if="variant === 'video'" class="space-y-3">
      <div class="skeleton-shimmer aspect-video w-full rounded-lg"></div>
      <div class="flex space-x-3">
        <div class="skeleton-shimmer h-10 w-10 rounded-full flex-shrink-0"></div>
        <div class="flex-1 space-y-2">
          <div class="skeleton-shimmer h-4 w-full rounded"></div>
          <div class="skeleton-shimmer h-3 w-2/3 rounded"></div>
          <div class="skeleton-shimmer h-3 w-1/3 rounded"></div>
        </div>
      </div>
    </div>

    <!-- Analytics dashboard skeleton -->
    <div v-else-if="variant === 'dashboard'" class="space-y-6">
      <!-- Stats cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div v-for="i in 4" :key="i" class="p-4 border rounded-lg space-y-2">
          <div class="skeleton-shimmer h-4 w-1/2 rounded"></div>
          <div class="skeleton-shimmer h-8 w-3/4 rounded"></div>
        </div>
      </div>
      
      <!-- Chart area -->
      <div class="skeleton-shimmer h-64 w-full rounded-lg"></div>
      
      <!-- Table header -->
      <div class="space-y-3">
        <div class="skeleton-shimmer h-6 w-1/4 rounded"></div>
        <div class="space-y-2">
          <div v-for="i in 5" :key="i" class="flex space-x-4">
            <div class="skeleton-shimmer h-4 w-1/4 rounded"></div>
            <div class="skeleton-shimmer h-4 w-1/4 rounded"></div>
            <div class="skeleton-shimmer h-4 w-1/4 rounded"></div>
            <div class="skeleton-shimmer h-4 w-1/4 rounded"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Custom skeleton -->
    <div v-else-if="variant === 'custom'" class="space-y-4">
      <slot name="skeleton">
        <div class="skeleton-shimmer h-20 w-full rounded"></div>
      </slot>
    </div>

    <!-- Default rectangle skeleton -->
    <div v-else class="skeleton-shimmer rounded" :style="{ height: height, width: width }"></div>

    <span class="sr-only">Loading content, please wait...</span>
  </div>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'card' | 'list' | 'text' | 'video' | 'dashboard' | 'custom' | 'rectangle'
  count?: number
  lines?: number
  height?: string
  width?: string
  animated?: boolean
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'rectangle',
  count: 3,
  lines: 3,
  height: '20px',
  width: '100%',
  animated: true,
  className: ''
})

const containerClasses = computed(() => {
  const base = 'animate-pulse'
  const animation = props.animated ? 'animate-pulse' : ''
  return [base, animation, props.className].filter(Boolean).join(' ')
})

const getTextWidth = (lineIndex: number) => {
  // Vary the width of text lines for more realistic skeleton
  const widths = ['w-full', 'w-5/6', 'w-4/5', 'w-3/4', 'w-2/3', 'w-1/2']
  return widths[lineIndex % widths.length]
}
</script>

<style scoped>
.skeleton-shimmer {
  @apply bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200;
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}

.dark .skeleton-shimmer {
  @apply from-gray-700 via-gray-600 to-gray-700;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Reduce motion for users who prefer it */
@media (prefers-reduced-motion: reduce) {
  .skeleton-shimmer {
    animation: none;
  }
  
  .animate-pulse {
    animation: none;
  }
}
</style>
