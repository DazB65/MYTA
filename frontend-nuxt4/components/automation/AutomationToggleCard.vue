<template>
  <div class="flex items-center justify-between p-4 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors">
    <!-- Feature Info -->
    <div class="flex items-center space-x-4 flex-1">
      <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-gray-600">
        <span class="text-xl">{{ icon }}</span>
      </div>
      <div class="flex-1">
        <h5 class="font-medium text-white">{{ title }}</h5>
        <p class="text-sm text-gray-400">{{ description }}</p>
        <div v-if="enabled" class="mt-1 flex items-center space-x-2">
          <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-900/30 text-green-300 border border-green-600/30">
            ✓ Active
          </span>
          <span v-if="stats" class="text-xs text-gray-400">{{ stats }}</span>
        </div>
      </div>
    </div>

    <!-- Toggle Switch -->
    <div class="flex items-center space-x-3">
      <!-- Settings Button (when enabled) -->
      <button
        v-if="enabled && hasSettings"
        @click="$emit('settings')"
        class="p-2 text-gray-400 hover:text-white transition-colors"
        title="Configure settings"
      >
        <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
        </svg>
      </button>

      <!-- Toggle Switch -->
      <button
        @click="handleToggle"
        :disabled="loading"
        class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 focus:ring-offset-gray-800 disabled:opacity-50"
        :class="enabled ? 'bg-orange-500' : 'bg-gray-600'"
      >
        <span
          class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
          :class="enabled ? 'translate-x-6' : 'translate-x-1'"
        />
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineEmits, defineProps } from 'vue'

const props = defineProps({
  enabled: {
    type: Boolean,
    required: true
  },
  icon: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  hasSettings: {
    type: Boolean,
    default: false
  },
  stats: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['toggle', 'settings'])

const handleToggle = () => {
  if (!props.loading) {
    emit('toggle')
  }
}
</script>
