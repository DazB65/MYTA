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
        class="rounded-xl p-4 text-sm shadow-lg"
        :class="message.isFromUser
          ? 'bg-gradient-to-r from-orange-500 to-orange-600 text-white ml-auto border border-orange-400/30'
          : 'bg-gradient-to-r from-orange-900/60 to-orange-800/60 text-white border border-orange-500/30 backdrop-blur-sm'"
      >
        <p class="leading-relaxed">{{ message.content }}</p>
      </div>

      <!-- Executive Coordination Message -->
      <div
        v-else-if="message.type === 'coordination'"
        class="rounded-xl bg-gradient-to-r from-blue-900/40 to-purple-900/40 text-white border border-blue-500/30 backdrop-blur-sm"
      >
        <div class="p-4">
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-8 h-8 rounded-full bg-gradient-to-r from-blue-400 to-purple-500 flex items-center justify-center text-sm animate-pulse">
              🤝
            </div>
            <div>
              <span class="text-sm font-semibold text-blue-200 uppercase tracking-wide">Team Coordination</span>
              <div class="text-xs text-blue-300/80">{{ message.metadata?.coordinationTime || '2.1s' }} coordination time</div>
            </div>
          </div>
          <p class="text-sm font-medium mb-3">{{ message.content }}</p>

          <!-- Coordinated Agents Display -->
          <div v-if="message.metadata?.coordinatedAgents?.length" class="space-y-2">
            <p class="text-xs font-medium text-blue-300">Specialists Coordinated:</p>
            <div class="flex flex-wrap gap-2">
              <div
                v-for="(specialist, index) in message.metadata.coordinatedAgents"
                :key="index"
                class="flex items-center space-x-1 bg-blue-600/20 px-2 py-1 rounded-full border border-blue-500/30"
              >
                <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span class="text-xs text-blue-200">{{ specialist }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Executive Insight Message -->
      <div
        v-else-if="message.type === 'executive_insight'"
        class="rounded-xl bg-gradient-to-r from-orange-900/60 to-amber-900/60 text-white border border-orange-500/40 backdrop-blur-sm"
      >
        <div class="p-4">
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-8 h-8 rounded-full bg-gradient-to-r from-orange-400 to-amber-500 flex items-center justify-center text-sm font-bold">
              🎯
            </div>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <span class="text-sm font-semibold text-orange-200 uppercase tracking-wide">Executive Insight</span>
                <div class="flex items-center space-x-2">
                  <div v-if="message.metadata?.confidence" class="text-xs text-orange-300/80 bg-orange-600/20 px-2 py-1 rounded-full">
                    {{ Math.round(message.metadata.confidence * 100) }}% confidence
                  </div>
                  <div v-if="message.metadata?.priority" class="text-xs font-bold px-2 py-1 rounded-full"
                       :class="{
                         'bg-red-600/30 text-red-200': message.metadata.priority === 'critical',
                         'bg-orange-600/30 text-orange-200': message.metadata.priority === 'high',
                         'bg-yellow-600/30 text-yellow-200': message.metadata.priority === 'medium',
                         'bg-blue-600/30 text-blue-200': message.metadata.priority === 'low'
                       }">
                    {{ message.metadata.priority.toUpperCase() }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <p class="text-sm font-medium leading-relaxed">{{ message.content }}</p>

          <!-- KPIs Display -->
          <div v-if="message.metadata?.kpis" class="mt-4 grid grid-cols-3 gap-3">
            <div v-for="(value, key) in message.metadata.kpis" :key="key" class="bg-orange-800/30 rounded-lg p-2 text-center border border-orange-600/30">
              <div class="text-lg font-bold text-orange-200">{{ value }}</div>
              <div class="text-xs text-orange-300/80 capitalize">{{ key }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Strategic Recommendation Message -->
      <div
        v-else-if="message.type === 'strategic_recommendation'"
        class="rounded-xl bg-gradient-to-r from-emerald-900/40 to-teal-900/40 text-white border border-emerald-500/30 backdrop-blur-sm"
      >
        <div class="p-4">
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-8 h-8 rounded-full bg-gradient-to-r from-emerald-400 to-teal-500 flex items-center justify-center text-sm font-bold">
              📋
            </div>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <span class="text-sm font-semibold text-emerald-200 uppercase tracking-wide">Strategic Recommendation</span>
                <div class="flex items-center space-x-2 text-xs text-emerald-300/80">
                  <span>{{ message.metadata?.timeline || 'Immediate' }}</span>
                  <span>•</span>
                  <span class="text-green-400 font-medium">{{ message.metadata?.expectedROI || 'High Impact' }}</span>
                </div>
              </div>
            </div>
          </div>
          <p class="text-sm font-medium mb-4 leading-relaxed">{{ message.content }}</p>

          <!-- Action Items -->
          <div v-if="message.metadata?.actionItems?.length" class="space-y-3">
            <p class="text-xs font-semibold text-emerald-300 uppercase tracking-wide">Strategic Action Items:</p>
            <div class="space-y-2">
              <button
                v-for="(action, index) in message.metadata.actionItems"
                :key="index"
                class="w-full text-left text-sm px-4 py-3 rounded-lg bg-emerald-800/30 hover:bg-emerald-700/40 transition-all duration-200 border border-emerald-600/30 hover:border-emerald-500/50 group"
                @click="$emit('action-click', action)"
              >
                <div class="flex items-center space-x-3">
                  <div class="w-6 h-6 rounded-full bg-emerald-600/30 flex items-center justify-center text-xs font-bold text-emerald-200 group-hover:bg-emerald-500/40">
                    {{ index + 1 }}
                  </div>
                  <span class="text-emerald-200 group-hover:text-emerald-100">{{ action }}</span>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Enhanced Insight Message -->
      <div
        v-else-if="message.type === 'insight'"
        class="rounded-xl bg-gradient-to-r from-purple-900/40 to-indigo-900/40 text-white border border-purple-500/30 backdrop-blur-sm"
      >
        <div class="p-4">
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-7 h-7 rounded-full bg-gradient-to-r from-purple-400 to-indigo-500 flex items-center justify-center text-sm font-bold animate-pulse">
              💡
            </div>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <span class="text-sm font-semibold text-purple-200 uppercase tracking-wide">Strategic Insight</span>
                <div v-if="message.metadata?.confidence" class="text-xs text-purple-300/80 bg-purple-600/20 px-2 py-1 rounded-full">
                  {{ Math.round(message.metadata.confidence * 100) }}% confidence
                </div>
              </div>
            </div>
          </div>
          <p class="text-sm font-medium leading-relaxed">{{ message.content }}</p>
          <div v-if="message.metadata?.actionItems?.length" class="mt-4 space-y-2">
            <p class="text-xs font-semibold text-purple-300 uppercase tracking-wide">Recommended Actions:</p>
            <div class="space-y-2">
              <button
                v-for="(action, index) in message.metadata.actionItems"
                :key="index"
                class="block w-full text-left text-sm px-3 py-2 rounded-lg bg-purple-800/30 hover:bg-purple-700/40 transition-all duration-200 border border-purple-600/30 hover:border-purple-500/50 text-purple-200 hover:text-purple-100"
                @click="$emit('action-click', action)"
              >
                {{ action }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Enhanced Recommendation Message -->
      <div
        v-else-if="message.type === 'recommendation'"
        class="rounded-xl bg-gradient-to-r from-amber-900/40 to-yellow-900/40 text-white border border-amber-500/30 backdrop-blur-sm"
      >
        <div class="p-4">
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-7 h-7 rounded-full bg-gradient-to-r from-amber-400 to-yellow-500 flex items-center justify-center text-sm font-bold">
              🎯
            </div>
            <span class="text-sm font-semibold text-amber-200 uppercase tracking-wide">Executive Recommendation</span>
          </div>
          <p class="text-sm font-medium leading-relaxed">{{ message.content }}</p>
          <div v-if="message.metadata?.actionItems?.length" class="mt-4 space-y-2">
            <p class="text-xs font-semibold text-amber-300 uppercase tracking-wide">Priority Actions:</p>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="(action, index) in message.metadata.actionItems"
                :key="index"
                class="text-sm px-4 py-2 rounded-full border-2 border-amber-400/50 text-amber-200 hover:bg-amber-400/20 hover:border-amber-400/70 hover:text-amber-100 transition-all duration-200 font-medium"
                @click="$emit('action-click', action)"
              >
                {{ action }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Enhanced Analysis Message -->
      <div
        v-else-if="message.type === 'analysis'"
        class="rounded-xl bg-gradient-to-r from-cyan-900/40 to-blue-900/40 text-white border border-cyan-500/30 backdrop-blur-sm"
      >
        <div class="p-4">
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-7 h-7 rounded-full bg-gradient-to-r from-cyan-400 to-blue-500 flex items-center justify-center text-sm font-bold">
              📊
            </div>
            <span class="text-sm font-semibold text-cyan-200 uppercase tracking-wide">Data Analysis</span>
          </div>
          <p class="text-sm font-medium leading-relaxed">{{ message.content }}</p>
          <div v-if="message.metadata?.sources?.length" class="mt-4 pt-3 border-t border-cyan-600/30">
            <p class="text-xs font-semibold text-cyan-300 mb-2 uppercase tracking-wide">Data Sources:</p>
            <div class="grid grid-cols-1 gap-1">
              <div
                v-for="(source, index) in message.metadata.sources"
                :key="index"
                class="flex items-center space-x-2 text-xs text-cyan-200/80 bg-cyan-800/20 px-2 py-1 rounded border border-cyan-600/20"
              >
                <div class="w-1.5 h-1.5 bg-cyan-400 rounded-full"></div>
                <span>{{ source }}</span>
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

      <!-- Enhanced Executive Action Buttons -->
      <div v-if="!message.isFromUser && showActionButtons" class="mt-4 flex items-center space-x-3">
        <button
          @click="$emit('save-as-task', message)"
          class="text-sm px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600/80 to-blue-700/80 hover:from-blue-600 hover:to-blue-700 text-white transition-all duration-200 flex items-center space-x-2 shadow-lg border border-blue-500/30 hover:border-blue-400/50 backdrop-blur-sm"
          title="Add to executive task list"
        >
          <span class="text-base">📋</span>
          <span class="font-medium">Add to Tasks</span>
        </button>
        <button
          @click="$emit('save-as-goal', message)"
          class="text-sm px-4 py-2 rounded-xl bg-gradient-to-r from-purple-600/80 to-purple-700/80 hover:from-purple-600 hover:to-purple-700 text-white transition-all duration-200 flex items-center space-x-2 shadow-lg border border-purple-500/30 hover:border-purple-400/50 backdrop-blur-sm"
          title="Set as strategic goal"
        >
          <span class="text-base">🎯</span>
          <span class="font-medium">Set as Goal</span>
        </button>
        <button
          class="text-sm px-4 py-2 rounded-xl bg-gradient-to-r from-emerald-600/80 to-emerald-700/80 hover:from-emerald-600 hover:to-emerald-700 text-white transition-all duration-200 flex items-center space-x-2 shadow-lg border border-emerald-500/30 hover:border-emerald-400/50 backdrop-blur-sm"
          title="Share with team"
        >
          <span class="text-base">📤</span>
          <span class="font-medium">Share</span>
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
