<template>
  <div class="space-y-6">
    <!-- Agent Status Overview -->
    <VCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold">Agent System Status</h3>
          <div class="flex items-center space-x-2">
            <div 
              :class="[
                'w-3 h-3 rounded-full',
                isConnected ? 'bg-agent-3' : 'bg-error-500'
              ]"
            ></div>
            <span class="text-sm text-text-secondary">
              {{ isConnected ? 'Connected' : 'Disconnected' }}
            </span>
          </div>
        </div>
      </template>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="text-center">
          <div class="text-2xl font-bold text-text-primary">{{ agentStats.total }}</div>
          <div class="text-sm text-text-muted">Total Agents</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-agent-3">{{ agentStats.online }}</div>
          <div class="text-sm text-text-muted">Online</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-agent-4">{{ agentStats.busy }}</div>
          <div class="text-sm text-text-muted">Busy</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-agent-1">{{ agentStats.thinking }}</div>
          <div class="text-sm text-text-muted">Thinking</div>
        </div>
      </div>
    </VCard>

    <!-- Agent Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="agent in allAgents"
        :key="agent.id"
        class="card card-hover cursor-pointer"
        :style="{ borderColor: agent.color + '40' }"
        @click="selectAgent(agent)"
      >
        <!-- Agent Header -->
        <div class="flex items-center space-x-3 mb-4">
          <div 
            class="w-12 h-12 rounded-lg flex items-center justify-center"
            :style="{ backgroundColor: agent.color + '20' }"
          >
            <img 
              v-if="agent.avatar" 
              :src="agent.avatar" 
              :alt="agent.name"
              class="w-8 h-8 rounded-lg object-cover"
            />
            <span v-else class="text-lg">🤖</span>
          </div>
          <div class="flex-1">
            <h4 class="font-semibold text-text-primary">{{ agent.name }}</h4>
            <p class="text-sm text-text-muted">{{ agent.personality }}</p>
          </div>
          <div 
            :class="[
              'w-3 h-3 rounded-full',
              getStatusColor(agent.status)
            ]"
          ></div>
        </div>

        <!-- Agent Info -->
        <div class="space-y-3">
          <div>
            <div class="text-sm font-medium text-text-secondary mb-1">Specialization</div>
            <div class="text-sm text-text-primary">{{ agent.specialization }}</div>
          </div>
          
          <div>
            <div class="text-sm font-medium text-text-secondary mb-1">Capabilities</div>
            <div class="flex flex-wrap gap-1">
              <VBadge 
                v-for="capability in agent.capabilities.slice(0, 3)" 
                :key="capability"
                variant="secondary"
                size="sm"
              >
                {{ capability.replace('_', ' ') }}
              </VBadge>
              <VBadge 
                v-if="agent.capabilities.length > 3"
                variant="secondary"
                size="sm"
              >
                +{{ agent.capabilities.length - 3 }}
              </VBadge>
            </div>
          </div>

          <div class="pt-2 border-t border-border">
            <div class="flex items-center justify-between text-sm">
              <span class="text-text-muted">Last Active</span>
              <span class="text-text-secondary">
                {{ formatLastActive(agent.lastActive) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="mt-4 flex space-x-2">
          <VButton 
            variant="ghost" 
            size="sm"
            @click.stop="startChat(agent)"
          >
            💬 Chat
          </VButton>
          <VButton 
            variant="ghost" 
            size="sm"
            @click.stop="viewInsights(agent)"
          >
            💡 Insights
          </VButton>
        </div>
      </div>
    </div>

    <!-- Recent Insights -->
    <VCard v-if="recentInsights.length > 0">
      <template #header>
        <h3 class="text-lg font-semibold">Recent Insights</h3>
      </template>

      <div class="space-y-4">
        <div
          v-for="insight in recentInsights.slice(0, 5)"
          :key="insight.id"
          class="flex items-start space-x-3 p-3 rounded-lg bg-background-elevated"
        >
          <div 
            class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
            :style="{ backgroundColor: getAgentById(insight.agentId)?.color + '20' }"
          >
            <span class="text-xs">💡</span>
          </div>
          <div class="flex-1">
            <div class="flex items-center justify-between mb-1">
              <h5 class="font-medium text-text-primary">{{ insight.title }}</h5>
              <VBadge 
                :variant="getPriorityVariant(insight.priority)"
                size="sm"
              >
                {{ insight.priority }}
              </VBadge>
            </div>
            <p class="text-sm text-text-secondary mb-2">{{ insight.description }}</p>
            <div class="flex items-center justify-between text-xs text-text-muted">
              <span>{{ getAgentById(insight.agentId)?.name }}</span>
              <span>{{ formatTimestamp(insight.timestamp) }}</span>
            </div>
          </div>
        </div>
      </div>
    </VCard>

    <!-- Active Chat Sessions -->
    <VCard v-if="activeChats.length > 0">
      <template #header>
        <h3 class="text-lg font-semibold">Active Conversations</h3>
      </template>

      <div class="space-y-3">
        <div
          v-for="session in activeChats.slice(0, 3)"
          :key="session.id"
          class="flex items-center justify-between p-3 rounded-lg bg-background-elevated cursor-pointer hover:bg-background-card transition-colors"
          @click="openChat(session)"
        >
          <div class="flex items-center space-x-3">
            <div 
              class="w-8 h-8 rounded-lg flex items-center justify-center"
              :style="{ backgroundColor: getAgentById(session.agentId)?.color + '20' }"
            >
              <span class="text-xs">💬</span>
            </div>
            <div>
              <div class="font-medium text-text-primary">{{ session.title }}</div>
              <div class="text-sm text-text-muted">
                {{ session.messages.length }} messages
              </div>
            </div>
          </div>
          <div class="text-xs text-text-muted">
            {{ formatTimestamp(session.updatedAt) }}
          </div>
        </div>
      </div>
    </VCard>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAgentsStore } from '../../stores/agents'
import { useChatStore } from '../../stores/chat'
import { useWebSocketAgent } from '../../composables/useWebSocketAgent'
import type { Agent, AgentInsight, ChatSession } from '../../types/agents'

const agentsStore = useAgentsStore()
const chatStore = useChatStore()
const { isConnected } = useWebSocketAgent()

// Computed properties
const allAgents = computed(() => agentsStore.allAgents)
const agentStats = computed(() => agentsStore.agentStats)
const recentInsights = computed(() => agentsStore.recentInsights)
const activeChats = computed(() => chatStore.recentSessions)

// Methods
const getStatusColor = (status: string) => {
  switch (status) {
    case 'online': return 'bg-agent-3'
    case 'busy': return 'bg-agent-4'
    case 'thinking': return 'bg-agent-1'
    case 'offline': return 'bg-text-muted'
    default: return 'bg-text-muted'
  }
}

const getPriorityVariant = (priority: string) => {
  switch (priority) {
    case 'critical': return 'error'
    case 'high': return 'warning'
    case 'medium': return 'primary'
    case 'low': return 'secondary'
    default: return 'secondary'
  }
}

const formatLastActive = (date?: Date) => {
  if (!date) return 'Never'
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  
  if (minutes < 1) return 'Just now'
  if (minutes < 60) return `${minutes}m ago`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}h ago`
  const days = Math.floor(hours / 24)
  return `${days}d ago`
}

const formatTimestamp = (date: Date) => {
  return new Intl.DateTimeFormat('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

const selectAgent = (agent: Agent) => {
  console.log('Selected agent:', agent)
  // Emit event or navigate to agent detail
}

const startChat = (agent: Agent) => {
  const sessionId = chatStore.createSession(agent.id, `Chat with ${agent.name}`)
  chatStore.setActiveSession(sessionId)
  // Navigate to chat or open chat modal
}

const viewInsights = (agent: Agent) => {
  console.log('View insights for:', agent)
  // Navigate to insights page or open insights modal
}

const openChat = (session: ChatSession) => {
  chatStore.setActiveSession(session.id)
  // Navigate to chat or open chat modal
}

const getAgentById = (id: string) => agentsStore.getAgentById(id)
</script>
