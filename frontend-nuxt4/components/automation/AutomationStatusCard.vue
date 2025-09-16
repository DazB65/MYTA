<template>
  <div class="flex items-center justify-between p-4 rounded-lg bg-gray-700 transition-colors">
    <!-- Feature Info -->
    <div class="flex items-center space-x-4 flex-1">
      <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-gray-600">
        <span class="text-xl">{{ icon }}</span>
      </div>
      <div class="flex-1">
        <h5 class="font-medium text-white">{{ title }}</h5>
        <p class="text-sm text-gray-400">{{ description }}</p>
        <div class="mt-1 flex items-center space-x-2">
          <!-- Status Badge -->
          <span 
            class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
            :class="getStatusBadgeClass()"
          >
            {{ getStatusText() }}
          </span>
          <!-- Tier Badge -->
          <span 
            class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
            :class="getTierBadgeClass()"
          >
            {{ getTierText() }}
          </span>
          <span v-if="stats" class="text-xs text-gray-400">{{ stats }}</span>
        </div>
      </div>
    </div>

    <!-- Status Icon -->
    <div class="flex items-center space-x-3">
      <div class="text-2xl">
        {{ getStatusIcon() }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAgentAccess } from '../../composables/useAgentAccess'

const props = defineProps({
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
  status: {
    type: String,
    required: true,
    validator: (value) => ['active', 'available', 'locked'].includes(value)
  },
  tier: {
    type: String,
    required: true,
    validator: (value) => ['basic', 'pro', 'teams'].includes(value)
  },
  stats: {
    type: String,
    default: null
  }
})

// Get current user's tier (simplified for demo)
const currentTier = 'basic' // In real app, get from subscription store

const isFeatureAvailable = computed(() => {
  const tierHierarchy = { basic: 1, pro: 2, teams: 3 }
  return tierHierarchy[currentTier] >= tierHierarchy[props.tier]
})

const getStatusBadgeClass = () => {
  if (!isFeatureAvailable.value) {
    return 'bg-gray-900/30 text-gray-400 border border-gray-600/30'
  }
  
  switch (props.status) {
    case 'active':
      return 'bg-green-900/30 text-green-300 border border-green-600/30'
    case 'available':
      return 'bg-blue-900/30 text-blue-300 border border-blue-600/30'
    default:
      return 'bg-gray-900/30 text-gray-400 border border-gray-600/30'
  }
}

const getTierBadgeClass = () => {
  switch (props.tier) {
    case 'basic':
      return 'bg-gray-900/30 text-gray-300 border border-gray-600/30'
    case 'pro':
      return 'bg-orange-900/30 text-orange-300 border border-orange-600/30'
    case 'teams':
      return 'bg-purple-900/30 text-purple-300 border border-purple-600/30'
    default:
      return 'bg-gray-900/30 text-gray-300 border border-gray-600/30'
  }
}

const getStatusText = () => {
  if (!isFeatureAvailable.value) {
    return '🔒 Upgrade Required'
  }
  
  switch (props.status) {
    case 'active':
      return '✓ Active'
    case 'available':
      return '⚡ Available'
    case 'locked':
      return '🔒 Locked'
    default:
      return '⚙️ Unknown'
  }
}

const getTierText = () => {
  switch (props.tier) {
    case 'basic':
      return 'Basic Plan'
    case 'pro':
      return 'Pro Plan'
    case 'teams':
      return 'Teams Plan'
    default:
      return 'Unknown Plan'
  }
}

const getStatusIcon = () => {
  if (!isFeatureAvailable.value) {
    return '🔒'
  }
  
  switch (props.status) {
    case 'active':
      return '🚀'
    case 'available':
      return '⚡'
    case 'locked':
      return '🔒'
    default:
      return '⚙️'
  }
}
</script>
