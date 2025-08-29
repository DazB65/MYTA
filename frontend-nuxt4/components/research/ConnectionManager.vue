<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-forest-900 border border-forest-600 rounded-lg w-full max-w-md p-6">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-xl font-bold text-white">Create Connection</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-white transition-colors">
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Connection Type Selection -->
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">Connection Type</label>
          <div class="grid grid-cols-1 gap-2">
            <button
              v-for="type in connectionTypes"
              :key="type.id"
              @click="selectedType = type.id"
              :class="[
                'flex items-center space-x-3 p-3 rounded-lg border-2 transition-all',
                selectedType === type.id
                  ? 'border-orange-500 bg-orange-500/10'
                  : 'border-forest-600 bg-forest-800 hover:border-forest-500'
              ]"
            >
              <div 
                class="w-8 h-8 rounded-full flex items-center justify-center text-white font-bold"
                :style="{ backgroundColor: type.color }"
              >
                {{ type.icon }}
              </div>
              <div class="flex-1 text-left">
                <div class="font-medium text-white">{{ type.name }}</div>
                <div class="text-sm text-gray-400">{{ type.description }}</div>
              </div>
            </button>
          </div>
        </div>

        <!-- Custom Label -->
        <div v-if="selectedType">
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Connection Label (Optional)
          </label>
          <input
            v-model="customLabel"
            type="text"
            :placeholder="getDefaultLabel(selectedType)"
            class="w-full px-3 py-2 bg-forest-800 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:border-orange-500 focus:outline-none"
          />
        </div>

        <!-- Connection Strength -->
        <div v-if="selectedType">
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Connection Strength
          </label>
          <div class="flex items-center space-x-3">
            <span class="text-sm text-gray-400">Weak</span>
            <input
              v-model="connectionStrength"
              type="range"
              min="1"
              max="10"
              class="flex-1 h-2 bg-forest-700 rounded-lg appearance-none cursor-pointer"
            />
            <span class="text-sm text-gray-400">Strong</span>
            <span class="text-sm font-medium text-white w-8">{{ connectionStrength }}</span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex space-x-3 pt-4">
          <button
            @click="$emit('close')"
            class="flex-1 px-4 py-2 bg-forest-700 text-white rounded-lg hover:bg-forest-600 transition-colors"
          >
            Cancel
          </button>
          <button
            @click="createConnection"
            :disabled="!selectedType"
            class="flex-1 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Create Connection
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  show: boolean
  sourceItem: any
  targetItem: any
}

interface Emits {
  (e: 'close'): void
  (e: 'create', connection: any): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const selectedType = ref('')
const customLabel = ref('')
const connectionStrength = ref(5)

const connectionTypes = [
  {
    id: 'related',
    name: 'Related Content',
    description: 'Similar topics or themes',
    icon: '🔗',
    color: '#3b82f6'
  },
  {
    id: 'competitor',
    name: 'Competitor Analysis',
    description: 'Competing content or channels',
    icon: '⚔️',
    color: '#ef4444'
  },
  {
    id: 'trend',
    name: 'Trending Connection',
    description: 'Part of current trends',
    icon: '📈',
    color: '#eab308'
  },
  {
    id: 'inspired-by',
    name: 'Inspired By',
    description: 'Content that inspired this',
    icon: '💡',
    color: '#16a34a'
  },
  {
    id: 'custom',
    name: 'Custom Connection',
    description: 'Define your own relationship',
    icon: '⭐',
    color: '#a855f7'
  }
]

const getDefaultLabel = (type: string) => {
  const labels = {
    'related': 'Related Content',
    'competitor': 'Competitor',
    'trend': 'Trending',
    'inspired-by': 'Inspired By',
    'custom': 'Custom'
  }
  return labels[type] || 'Connection'
}

const createConnection = () => {
  if (!selectedType.value) return

  const connection = {
    type: selectedType.value,
    label: customLabel.value || getDefaultLabel(selectedType.value),
    strength: connectionStrength.value,
    sourceId: props.sourceItem?.id,
    targetId: props.targetItem?.id,
    sourcePosition: props.sourceItem?.position,
    targetPosition: props.targetItem?.position
  }

  emit('create', connection)
  emit('close')
  
  // Reset form
  selectedType.value = ''
  customLabel.value = ''
  connectionStrength.value = 5
}
</script>
