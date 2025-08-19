<template>
  <div class="flex items-start space-x-3" :class="message.isFromUser ? 'flex-row-reverse space-x-reverse' : ''">
    <!-- Avatar -->
    <div class="flex-shrink-0">
      <div
        v-if="!message.isFromUser"
        class="w-8 h-8 rounded-lg overflow-hidden"
        :style="{ backgroundColor: agentColor + '20' }"
      >
        <img
          :src="agentImage"
          :alt="agentName"
          class="w-full h-full object-cover"
        />
      </div>
      <div
        v-else
        class="w-8 h-8 rounded-lg bg-orange-600 flex items-center justify-center text-white text-sm font-bold"
      >
        U
      </div>
    </div>

    <!-- Message Content -->
    <div class="flex-1" :class="message.isFromUser ? 'max-w-[320px]' : 'max-w-[400px]'">
      <!-- Text Message -->
      <div
        v-if="message.type === 'text'"
        class="rounded-lg p-3 text-sm"
        :class="message.isFromUser 
          ? 'bg-orange-600 text-white ml-auto' 
          : 'bg-forest-700 text-white'"
      >
        <p>{{ message.content }}</p>
      </div>

      <!-- Insight Message -->
      <div
        v-else-if="message.type === 'insight'"
        class="rounded-lg border-l-4 bg-forest-700 text-white"
        :style="{ borderLeftColor: agentColor }"
      >
        <div class="p-3">
          <div class="flex items-center space-x-2 mb-2">
            <div class="w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold text-white"
                 :style="{ backgroundColor: agentColor }">
              💡
            </div>
            <span class="text-xs font-semibold text-gray-300 uppercase tracking-wide">Insight</span>
            <div v-if="message.metadata?.confidence" class="text-xs text-gray-400">
              {{ Math.round(message.metadata.confidence * 100) }}% confidence
            </div>
          </div>
          <p class="text-sm">{{ message.content }}</p>
          <div v-if="message.metadata?.actionItems?.length" class="mt-3 space-y-1">
            <p class="text-xs font-medium text-gray-300">Suggested Actions:</p>
            <div class="space-y-1">
              <button
                v-for="(action, index) in message.metadata.actionItems"
                :key="index"
                class="block w-full text-left text-xs px-2 py-1 rounded bg-forest-600 hover:bg-forest-500 transition-colors"
                @click="$emit('action-click', action)"
              >
                {{ action }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Recommendation Message -->
      <div
        v-else-if="message.type === 'recommendation'"
        class="rounded-lg bg-gradient-to-r from-forest-700 to-forest-600 text-white"
      >
        <div class="p-3">
          <div class="flex items-center space-x-2 mb-2">
            <div class="w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold text-white"
                 :style="{ backgroundColor: agentColor }">
              🎯
            </div>
            <span class="text-xs font-semibold text-yellow-300 uppercase tracking-wide">Recommendation</span>
          </div>
          <p class="text-sm font-medium">{{ message.content }}</p>
          <div v-if="message.metadata?.actionItems?.length" class="mt-3 flex flex-wrap gap-2">
            <button
              v-for="(action, index) in message.metadata.actionItems"
              :key="index"
              class="text-xs px-3 py-1 rounded-full border border-yellow-400 text-yellow-300 hover:bg-yellow-400 hover:text-forest-800 transition-colors"
              @click="$emit('action-click', action)"
            >
              {{ action }}
            </button>
          </div>
        </div>
      </div>

      <!-- Analysis Message -->
      <div
        v-else-if="message.type === 'analysis'"
        class="rounded-lg bg-forest-700 text-white border border-forest-600"
      >
        <div class="p-3">
          <div class="flex items-center space-x-2 mb-2">
            <div class="w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold text-white"
                 :style="{ backgroundColor: agentColor }">
              📊
            </div>
            <span class="text-xs font-semibold text-blue-300 uppercase tracking-wide">Analysis</span>
          </div>
          <p class="text-sm">{{ message.content }}</p>
          <div v-if="message.metadata?.sources?.length" class="mt-2 pt-2 border-t border-forest-600">
            <p class="text-xs text-gray-400 mb-1">Sources:</p>
            <div class="space-y-1">
              <div
                v-for="(source, index) in message.metadata.sources"
                :key="index"
                class="text-xs text-gray-300"
              >
                • {{ source }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Chart Data Message -->
      <div
        v-else-if="message.type === 'chart_data'"
        class="rounded-lg bg-forest-700 text-white border border-forest-600"
      >
        <div class="p-3">
          <div class="flex items-center space-x-2 mb-3">
            <div class="w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold text-white"
                 :style="{ backgroundColor: agentColor }">
              📈
            </div>
            <span class="text-xs font-semibold text-green-300 uppercase tracking-wide">Data Visualization</span>
          </div>
          <p v-if="message.content" class="text-sm mb-3">{{ message.content }}</p>
          
          <!-- Simple Chart Placeholder - Replace with actual chart component -->
          <div v-if="message.metadata?.chartData" class="bg-forest-800 rounded p-4">
            <div class="text-center text-gray-400 text-sm">
              📊 Chart: {{ message.metadata.chartData.type || 'Data Visualization' }}
            </div>
            <!-- TODO: Integrate with Chart.js or similar -->
          </div>
        </div>
      </div>

      <!-- System Message -->
      <div
        v-else-if="message.type === 'system'"
        class="text-center"
      >
        <div class="inline-block px-3 py-1 rounded-full bg-forest-600 text-gray-300 text-xs">
          {{ message.content }}
        </div>
      </div>

      <!-- Error Message -->
      <div
        v-else-if="message.type === 'error'"
        class="rounded-lg bg-red-900 border border-red-700 text-white"
      >
        <div class="p-3">
          <div class="flex items-center space-x-2 mb-2">
            <div class="w-5 h-5 rounded-full bg-red-600 flex items-center justify-center text-xs font-bold text-white">
              ⚠️
            </div>
            <span class="text-xs font-semibold text-red-300 uppercase tracking-wide">Error</span>
          </div>
          <p class="text-sm">{{ message.content }}</p>
        </div>
      </div>

      <!-- Action Buttons for Agent Messages -->
      <div v-if="!message.isFromUser && showActionButtons" class="mt-3 flex items-center space-x-2">
        <button
          @click="$emit('save-as-task', message)"
          class="text-xs px-3 py-1.5 rounded-full bg-blue-600 hover:bg-blue-500 text-white transition-colors flex items-center space-x-1.5 shadow-sm"
          title="Save this response as a task"
        >
          <span>📋</span>
          <span>Save as Task</span>
        </button>
        <button
          @click="$emit('save-as-goal', message)"
          class="text-xs px-3 py-1.5 rounded-full bg-purple-600 hover:bg-purple-500 text-white transition-colors flex items-center space-x-1.5 shadow-sm"
          title="Save this response as a goal"
        >
          <span>🎯</span>
          <span>Save as Goal</span>
        </button>
      </div>

      <!-- Timestamp -->
      <div class="text-xs text-gray-500 mt-1" :class="message.isFromUser ? 'text-right' : ''">
        {{ formatTime(message.timestamp) }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ChatMessage } from '~/types/agents'

interface Props {
  message: ChatMessage
  agentColor: string
  agentImage: string
  agentName: string
  showActionButtons?: boolean
}

defineProps<Props>()
defineEmits<{
  'action-click': [action: string]
  'save-as-task': [message: ChatMessage]
  'save-as-goal': [message: ChatMessage]
}>()

const formatTime = (timestamp: Date) => {
  return new Intl.DateTimeFormat('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  }).format(timestamp)
}
</script>

<style scoped>
/* Add any additional styling here */
</style>
