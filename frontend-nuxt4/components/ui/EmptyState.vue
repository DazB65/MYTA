<template>
  <div class="flex flex-col items-center justify-center py-12 px-4 text-center">
    <!-- Icon -->
    <div 
      class="mb-6 flex h-20 w-20 items-center justify-center rounded-full"
      :class="iconBackgroundClass"
    >
      <div class="text-4xl">{{ icon }}</div>
    </div>

    <!-- Title -->
    <h3 class="mb-2 text-xl font-semibold text-white">
      {{ title }}
    </h3>

    <!-- Description -->
    <p class="mb-6 max-w-md text-sm text-gray-400">
      {{ description }}
    </p>

    <!-- Action Button -->
    <button
      v-if="actionText"
      @click="$emit('action')"
      class="flex items-center space-x-2 rounded-lg bg-orange-500 px-6 py-3 text-white transition-colors hover:bg-orange-600"
    >
      <svg v-if="showPlusIcon" class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
        <path
          fill-rule="evenodd"
          d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
          clip-rule="evenodd"
        />
      </svg>
      <span>{{ actionText }}</span>
    </button>

    <!-- Secondary Action -->
    <button
      v-if="secondaryActionText"
      @click="$emit('secondary-action')"
      class="mt-3 text-sm text-gray-400 hover:text-white transition-colors"
    >
      {{ secondaryActionText }}
    </button>

    <!-- Additional Help Text -->
    <div v-if="helpText" class="mt-6 rounded-lg bg-gray-800/50 p-4 max-w-md">
      <p class="text-xs text-gray-400">
        💡 {{ helpText }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  icon?: string
  title: string
  description: string
  actionText?: string
  secondaryActionText?: string
  helpText?: string
  variant?: 'default' | 'primary' | 'success' | 'warning'
  showPlusIcon?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  icon: '📭',
  variant: 'default',
  showPlusIcon: true
})

defineEmits<{
  action: []
  'secondary-action': []
}>()

const iconBackgroundClass = computed(() => {
  const variants = {
    default: 'bg-gray-700/50',
    primary: 'bg-orange-500/20',
    success: 'bg-green-500/20',
    warning: 'bg-yellow-500/20'
  }
  return variants[props.variant]
})
</script>

