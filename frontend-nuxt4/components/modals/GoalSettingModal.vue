<template>
  <div 
    v-if="isOpen" 
    class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-[60]"
    @click="closeModal"
  >
    <div 
      class="bg-forest-800 rounded-xl p-6 w-full max-w-md mx-4 border border-forest-600"
      @click.stop
    >
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
            <span class="text-xl">🎯</span>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-white">Set Goal</h3>
            <p class="text-sm text-gray-400">{{ goalData?.label || 'Metric Goal' }}</p>
          </div>
        </div>
        <button 
          @click="closeModal"
          class="text-gray-400 hover:text-white transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Current Stats -->
      <div class="mb-6 p-4 bg-forest-700 rounded-lg">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm text-gray-400">Current Value</span>
          <span class="text-lg font-semibold text-white">{{ goalData?.currentValue || '0' }}</span>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-400">Current Goal</span>
          <span class="text-lg font-semibold text-blue-400">{{ goalData?.currentGoal || '0' }}</span>
        </div>
      </div>

      <!-- Goal Input -->
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-300 mb-2">
          New Goal {{ goalData?.unit ? `(${goalData.unit})` : '' }}
        </label>
        <input
          v-model="newGoal"
          type="number"
          :min="goalData?.min || 0"
          :step="goalData?.step || 1"
          class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :placeholder="`Enter ${goalData?.label?.toLowerCase() || 'goal'}`"
        />
      </div>

      <!-- Suggested Goals -->
      <div v-if="suggestedGoals.length > 0" class="mb-6">
        <label class="block text-sm font-medium text-gray-300 mb-3">Quick Select</label>
        <div class="grid grid-cols-3 gap-2">
          <button
            v-for="suggestion in suggestedGoals"
            :key="suggestion.value"
            @click="newGoal = suggestion.value"
            class="px-3 py-2 bg-forest-700 hover:bg-forest-600 border border-forest-600 rounded-lg text-sm text-white transition-colors"
          >
            <div class="font-medium">{{ suggestion.value }}</div>
            <div class="text-xs text-gray-400">{{ suggestion.label }}</div>
          </button>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex space-x-3">
        <button
          @click="closeModal"
          class="flex-1 px-4 py-2 bg-forest-700 hover:bg-forest-600 text-white rounded-lg transition-colors"
        >
          Cancel
        </button>
        <button
          @click="saveGoal"
          :disabled="!newGoal || newGoal <= 0"
          class="flex-1 px-4 py-2 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
        >
          Save Goal
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  goalData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'save'])

const newGoal = ref('')

// Watch for modal opening to reset form
watch(() => props.isOpen, (isOpen) => {
  if (isOpen && props.goalData) {
    newGoal.value = props.goalData.currentGoal || ''
  }
})

// Generate suggested goals based on current performance
const suggestedGoals = computed(() => {
  if (!props.goalData) return []
  
  const current = parseFloat(props.goalData.currentValue) || 0
  const suggestions = []
  
  // Conservative goal (10% increase)
  const conservative = Math.round(current * 1.1)
  if (conservative > current) {
    suggestions.push({
      value: conservative,
      label: 'Conservative'
    })
  }
  
  // Moderate goal (25% increase)
  const moderate = Math.round(current * 1.25)
  if (moderate > conservative) {
    suggestions.push({
      value: moderate,
      label: 'Moderate'
    })
  }
  
  // Ambitious goal (50% increase)
  const ambitious = Math.round(current * 1.5)
  if (ambitious > moderate) {
    suggestions.push({
      value: ambitious,
      label: 'Ambitious'
    })
  }
  
  return suggestions.slice(0, 3) // Max 3 suggestions
})

const closeModal = () => {
  emit('close')
}

const saveGoal = () => {
  if (newGoal.value && newGoal.value > 0) {
    emit('save', {
      id: props.goalData?.id,
      goal: parseFloat(newGoal.value)
    })
    closeModal()
  }
}
</script>

<style scoped>
/* Custom number input styling */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
}
</style>
