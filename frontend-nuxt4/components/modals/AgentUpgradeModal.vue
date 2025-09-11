<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black bg-opacity-50" @click="$emit('close')" />
    
    <!-- Modal -->
    <div class="relative bg-gray-800 rounded-xl shadow-xl max-w-md w-full mx-4 p-6">
      <!-- Header -->
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-xl font-semibold text-white">Unlock Premium Agents</h3>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-white transition-colors"
        >
          <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <!-- Agent Preview -->
      <div v-if="lockedAgent" class="mb-6">
        <div class="flex items-center space-x-3 p-4 bg-gray-700 rounded-lg">
          <img 
            :src="lockedAgent.avatar" 
            :alt="lockedAgent.name"
            class="w-12 h-12 rounded-lg object-cover"
          />
          <div class="flex-1">
            <h4 class="font-semibold text-white">{{ lockedAgent.name }}</h4>
            <p class="text-sm text-gray-300">{{ lockedAgent.specialization }}</p>
          </div>
          <div class="text-2xl">🔒</div>
        </div>
      </div>

      <!-- Upgrade Benefits -->
      <div class="mb-6">
        <h4 class="font-medium text-white mb-3">Upgrade to Pro to unlock:</h4>
        <ul class="space-y-2 text-sm text-gray-300">
          <li class="flex items-center space-x-2">
            <span class="text-green-400">✓</span>
            <span>Access to all 5 specialist agents</span>
          </li>
          <li class="flex items-center space-x-2">
            <span class="text-green-400">✓</span>
            <span>Advanced AI capabilities</span>
          </li>
          <li class="flex items-center space-x-2">
            <span class="text-green-400">✓</span>
            <span>Priority support</span>
          </li>
          <li class="flex items-center space-x-2">
            <span class="text-green-400">✓</span>
            <span>Enhanced team coordination</span>
          </li>
        </ul>
      </div>

      <!-- Current Plan Info -->
      <div class="mb-6 p-3 bg-blue-900/30 border border-blue-600/30 rounded-lg">
        <div class="text-sm text-blue-300">
          <strong>Current Plan:</strong> Basic (Boss Agent + 3 specialists)
        </div>
        <div class="text-xs text-blue-400 mt-1">
          Upgrade to unlock Zara and Kai for the complete team experience
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex space-x-3">
        <button
          @click="$emit('close')"
          class="flex-1 px-4 py-2 text-gray-300 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
        >
          Maybe Later
        </button>
        <button
          @click="upgradeNow"
          class="flex-1 px-4 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors font-medium"
        >
          Upgrade Now
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Agent } from '../../types/agents'

interface Props {
  isOpen: boolean
  lockedAgent?: Agent | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  close: []
}>()

const router = useRouter()

const upgradeNow = () => {
  // Navigate to subscription page
  router.push('/settings?tab=subscription&upgrade=pro')
  emit('close')
}
</script>
