<template>
  <!-- Backdrop Overlay -->
  <Transition name="backdrop">
    <div 
      v-if="isOpen" 
      class="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm" 
      @click="closeChat" 
    />
  </Transition>

  <!-- Slide-out Panel -->
  <Transition name="slide-right">
    <div
      v-if="isOpen"
      class="fixed right-0 top-0 z-50 h-full bg-forest-800 shadow-2xl border-l border-forest-700 flex"
      style="width: calc(100vw - 280px); left: 280px;"
    >
      <!-- Left Sidebar for Questions & Suggestions -->
      <div class="w-80 bg-forest-700 border-r border-forest-600 flex flex-col">
        <!-- Sidebar Header -->
        <div class="p-4 border-b border-forest-700">
          <h3 class="text-sm font-medium text-white">Quick Access</h3>
        </div>

        <!-- Saved Questions Section -->
        <div v-if="savedQuestions.length > 0" class="p-4 border-b border-forest-700">
          <div class="flex items-center justify-between mb-3">
            <h4 class="text-xs font-medium text-gray-300 uppercase tracking-wide flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
              </svg>
              Your Saved Questions
            </h4>
          </div>
          <div class="space-y-2">
            <div v-for="question in savedQuestions" :key="question.id" class="flex items-center space-x-2">
              <button
                @click="loadSavedQuestion(question.text)"
                class="flex-1 text-left text-sm text-gray-300 hover:text-white bg-forest-600 hover:bg-forest-500 rounded-lg px-3 py-2 transition-colors truncate"
                :title="question.text"
              >
                {{ question.text }}
              </button>
              <button
                @click="removeSavedQuestion(question.id)"
                class="p-1 text-gray-500 hover:text-red-400 transition-colors"
                title="Remove saved question"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Smart Suggestions Section -->
        <div v-if="smartSuggestions.length > 0" class="p-4 flex-1 overflow-y-auto">
          <div class="flex items-center justify-between mb-3">
            <h4 class="text-xs font-medium text-gray-300 uppercase tracking-wide flex items-center">
              <span class="text-yellow-400 mr-2">✨</span>
              Smart Suggestions for {{ selectedAgentData.name }}
            </h4>
          </div>
          <div class="space-y-2">
            <button
              v-for="suggestion in smartSuggestions"
              :key="suggestion.id"
              @click="loadSmartSuggestion(suggestion.text)"
              class="w-full text-left text-sm text-gray-300 hover:text-white bg-forest-600 hover:bg-forest-500 rounded-lg px-3 py-2 transition-colors flex items-center space-x-2"
            >
              <span class="text-base">{{ suggestion.emoji }}</span>
              <span class="truncate">{{ suggestion.text }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Main Chat Area -->
      <div class="flex-1 flex flex-col">
      <!-- Agent Header -->
      <div 
        class="border-b border-forest-700 p-6"
        :style="{ background: headerGradient }"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <div class="relative">
              <img
                :src="selectedAgentData.image"
                :alt="selectedAgentData.name"
                class="w-12 h-12 rounded-xl object-cover"
              />
              <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-forest-800"></div>
            </div>
            <div>
              <h2 class="text-xl font-bold text-white">{{ selectedAgentData.name }}</h2>
              <p class="text-sm text-white/80">{{ selectedAgentData.personality }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <button
              @click="showSettings = true"
              class="p-2 rounded-lg hover:bg-white/10 transition-colors text-white/80 hover:text-white"
              title="Agent Settings"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
            <button
              @click="closeChat"
              class="p-2 rounded-lg hover:bg-white/10 transition-colors text-white/80 hover:text-white"
              title="Close Chat"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Chat Messages Area -->
      <div
        ref="messagesContainer"
        class="flex-1 overflow-y-auto p-4 space-y-4 overscroll-contain"
        :style="{ height: `calc(100vh - 200px)` }"
        @wheel.stop
      >
        <!-- Enhanced Welcome Message -->
        <div v-if="messages.length === 0" class="text-center py-8 px-4">
          <div class="w-20 h-20 mx-auto mb-4 rounded-xl overflow-hidden ring-4 ring-opacity-20"
               :style="{ ringColor: selectedAgentData.color }">
            <img
              :src="selectedAgentData.image"
              :alt="selectedAgentData.name"
              class="w-full h-full object-cover"
            />
          </div>
          <h3 class="text-xl font-bold text-white mb-2">Welcome to {{ selectedAgentData.name }}</h3>
          <p class="text-gray-300 text-sm mb-1">{{ selectedAgentData.description }}</p>
          <p class="text-gray-400 text-xs mb-6">{{ selectedAgentData.personality }}</p>

          <!-- Channel Overview Card -->
          <div class="bg-forest-700 rounded-lg p-4 mb-6 border border-forest-600">
            <h4 class="text-sm font-semibold text-white mb-3 flex items-center justify-center">
              <span class="mr-2">📊</span>
              Your Channel at a Glance
            </h4>
            <div class="grid grid-cols-2 gap-4 text-xs">
              <div class="text-center">
                <div class="text-lg font-bold text-white">1.2K</div>
                <div class="text-gray-400">Subscribers</div>
              </div>
              <div class="text-center">
                <div class="text-lg font-bold text-white">45.6K</div>
                <div class="text-gray-400">Total Views</div>
              </div>
              <div class="text-center">
                <div class="text-lg font-bold text-white">12</div>
                <div class="text-gray-400">Videos</div>
              </div>
              <div class="text-center">
                <div class="text-lg font-bold text-white">4.2%</div>
                <div class="text-gray-400">Avg CTR</div>
              </div>
            </div>
          </div>

          <p class="text-gray-400 text-sm">Ask me anything about your channel, content strategy, or growth opportunities!</p>
        </div>

        <!-- Messages -->
        <MessageBubble
          v-for="message in messages"
          :key="message.id"
          :message="message"
          :agent-color="selectedAgentData.color"
          :agent-image="selectedAgentData.image"
          :agent-name="selectedAgentData.name"
          :show-action-buttons="true"
          @action-click="handleActionClick"
          @save-as-task="handleSaveAsTask"
          @save-as-goal="handleSaveAsGoal"
        />

        <!-- Enhanced Typing Indicator -->
        <div v-if="isTyping" class="flex items-start space-x-3">
          <div
            class="w-8 h-8 rounded-lg overflow-hidden ring-2 ring-opacity-50"
            :style="{ backgroundColor: selectedAgentData.color + '20', ringColor: selectedAgentData.color }"
          >
            <img
              :src="selectedAgentData.image"
              :alt="selectedAgentData.name"
              class="w-full h-full object-cover"
            />
          </div>
          <div class="bg-gradient-to-r from-forest-700 to-forest-600 rounded-lg p-3 border border-forest-600">
            <div class="flex items-center space-x-2">
              <div class="w-5 h-5 rounded-full flex items-center justify-center text-xs"
                   :style="{ backgroundColor: selectedAgentData.color }">
                🤔
              </div>
              <span class="text-gray-200 text-sm">{{ selectedAgentData.name }} is analyzing...</span>
              <div class="flex space-x-1">
                <div class="w-1.5 h-1.5 rounded-full animate-pulse"
                     :style="{ backgroundColor: selectedAgentData.color }"></div>
                <div class="w-1.5 h-1.5 rounded-full animate-pulse"
                     :style="{ backgroundColor: selectedAgentData.color, animationDelay: '0.2s' }"></div>
                <div class="w-1.5 h-1.5 rounded-full animate-pulse"
                     :style="{ backgroundColor: selectedAgentData.color, animationDelay: '0.4s' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area - Always visible -->
      <div class="border-t border-forest-700 p-4">
        <div class="flex items-center space-x-3">
          <input
            v-model="messageInput"
            type="text"
            placeholder="Ask me anything..."
            class="flex-1 bg-forest-700 border border-forest-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:border-transparent"
            :style="{ '--tw-ring-color': selectedAgentData.color }"
            @keyup.enter="sendMessage"
            @input="handleTyping"
          />
          <!-- Bookmark button - shows when there's text and it's not already saved -->
          <button
            v-if="messageInput.trim() && !savedQuestions.some(q => q.text === messageInput.trim())"
            @click="saveCurrentQuestion"
            class="p-3 rounded-lg bg-forest-600 hover:bg-forest-500 text-white transition-colors"
            title="Save this question for quick access"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
          </button>
          <!-- Saved indicator - shows when question is already saved -->
          <div
            v-else-if="messageInput.trim() && savedQuestions.some(q => q.text === messageInput.trim())"
            class="p-3 rounded-lg bg-green-600 text-white"
            title="This question is already saved"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
          </div>
          <!-- Send button - always available when there's text -->
          <button
            @click="sendMessage"
            :disabled="!messageInput.trim() || isSending"
            class="px-4 py-3 rounded-lg font-medium text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            :style="{
              backgroundColor: messageInput.trim() ? selectedAgentData.color : '#374151',
              ':hover': { backgroundColor: messageInput.trim() ? selectedAgentData.color + 'dd' : '#374151' }
            }"
            title="Send message"
          >
            <svg v-if="!isSending" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
            <div v-else class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          </button>
        </div>
      </div>
      </div> <!-- Close Main Chat Area -->

      <!-- Settings Overlay -->
      <div
        v-if="showSettings"
        class="absolute inset-0 bg-black/50 backdrop-blur-sm z-10 flex items-center justify-center p-6"
        @click="showSettings = false"
      >
        <div
          class="bg-forest-700 rounded-xl p-6 w-full max-w-md border border-forest-600"
          @click.stop
        >
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-white">Agent Settings</h3>
            <button
              @click="showSettings = false"
              class="p-1 rounded-lg hover:bg-forest-600 transition-colors text-white/80 hover:text-white"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Agent Name Input -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-300 mb-2">Agent Name</label>
            <input
              v-model="tempAgentName"
              type="text"
              placeholder="Enter agent name..."
              class="w-full bg-forest-600 border border-forest-500 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:border-transparent"
              :style="{ '--tw-ring-color': selectedAgentData.color }"
            />
          </div>

          <!-- Agent Selection -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-300 mb-3">Choose Your Personal Avatar</label>
            <p class="text-xs text-gray-400 mb-4">Select your preferred visual representation</p>
            <div class="grid grid-cols-2 gap-4">
              <div
                v-for="agent in availableAgents"
                :key="agent.id"
                class="group relative cursor-pointer rounded-xl border-2 p-4 transition-all duration-300 hover:scale-105 hover:shadow-lg"
                :class="tempSelectedAgent === agent.id
                  ? 'border-opacity-100 shadow-lg transform scale-105'
                  : 'border-forest-500 hover:border-forest-400 border-opacity-50'"
                :style="tempSelectedAgent === agent.id ? {
                  borderColor: agent.color,
                  backgroundColor: agent.color + '15',
                  boxShadow: `0 8px 25px ${agent.color}30`
                } : {}"
                @click="tempSelectedAgent = agent.id"
              >
                <div class="text-center">
                  <!-- Agent Avatar with Glow Effect -->
                  <div
                    class="mx-auto mb-3 h-14 w-14 overflow-hidden rounded-full bg-forest-700 ring-2 ring-opacity-0 transition-all duration-300 group-hover:ring-opacity-50"
                    :class="tempSelectedAgent === agent.id ? 'ring-opacity-100' : ''"
                    :style="tempSelectedAgent === agent.id ? {
                      ringColor: agent.color,
                      boxShadow: `0 0 15px ${agent.color}40`
                    } : {}"
                  >
                    <img
                      :src="agent.image"
                      :alt="agent.name"
                      class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-110"
                    />
                  </div>

                  <!-- Agent Name -->
                  <div class="text-sm font-semibold text-gray-200 mb-1">{{ agent.name }}</div>

                  <!-- Agent Description -->
                  <div class="text-xs text-gray-400 leading-relaxed mb-2">{{ agent.description }}</div>

                  <!-- Personality Badge -->
                  <div
                    class="inline-block px-2 py-1 rounded-full text-xs font-medium transition-all duration-300"
                    :style="tempSelectedAgent === agent.id ? {
                      backgroundColor: agent.color + '25',
                      color: agent.color
                    } : {
                      backgroundColor: '#374151',
                      color: '#9ca3af'
                    }"
                  >
                    {{ agent.personality }}
                  </div>
                </div>

                <!-- Enhanced Selected Indicator -->
                <div
                  v-if="tempSelectedAgent === agent.id"
                  class="absolute -right-2 -top-2 flex h-6 w-6 items-center justify-center rounded-full shadow-lg animate-pulse"
                  :style="{
                    backgroundColor: agent.color,
                    boxShadow: `0 0 12px ${agent.color}60`
                  }"
                >
                  <svg class="h-3 w-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </div>

                <!-- Hover Glow Effect -->
                <div
                  class="absolute inset-0 rounded-xl opacity-0 transition-opacity duration-300 group-hover:opacity-100 pointer-events-none"
                  :style="{
                    background: `linear-gradient(135deg, ${agent.color}10 0%, transparent 50%, ${agent.color}10 100%)`
                  }"
                ></div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center justify-end space-x-3">
            <button
              @click="showSettings = false"
              class="px-4 py-2 rounded-lg bg-forest-600 text-white hover:bg-forest-500 transition-colors"
            >
              Cancel
            </button>
            <button
              @click="saveSettings"
              class="px-4 py-2 rounded-lg font-medium text-white transition-colors"
              :style="{ backgroundColor: selectedAgentData.color }"
            >
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div> <!-- Close Overall Container -->
  </Transition>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue';
import { useAgentSettings } from '../../composables/useAgentSettings';
import { useSaveToGoal } from '../../composables/useSaveToGoal';
import { useSaveToTask } from '../../composables/useSaveToTask';
import { useSmartQuestions } from '../../composables/useSmartQuestions';
import { useToast } from '../../composables/useToast';
import { useChatStore } from '../../stores/chat';
import MessageBubble from './MessageBubble.vue';

// Props
interface Props {
  isOpen: boolean
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  close: []
}>()

// Composables
const { selectedAgent, agentName, allAgents, setSelectedAgent, setAgentName } = useAgentSettings()
const chatStore = useChatStore()
const { getContextualQuestions } = useSmartQuestions()
const { saveMessageAsTask, prepareTaskData } = useSaveToTask()
const { saveMessageAsGoal, prepareGoalData } = useSaveToGoal()
const { success, error } = useToast()

// Refs
const messagesContainer = ref<HTMLElement>()
const messageInput = ref('')
const isSending = ref(false)
const isTyping = ref(false)
const typingTimeout = ref<NodeJS.Timeout>()
const showSettings = ref(false)
const tempAgentName = ref('')
const tempSelectedAgent = ref(1)
const savedQuestions = ref<Array<{ id: string; text: string; createdAt: Date }>>([])

// Interface for saved questions
interface SavedQuestion {
  id: string
  text: string
  createdAt: Date
}

// Computed
const selectedAgentData = computed(() => {
  return {
    ...selectedAgent.value,
    name: agentName.value || selectedAgent.value?.name || 'AI Assistant'
  }
})

const headerGradient = computed(() => {
  const color = selectedAgentData.value.color || '#ea580c'
  return `linear-gradient(135deg, ${color}20 0%, ${color}10 100%)`
})

const messages = computed(() => {
  return chatStore.activeSessionMessages || []
})

const smartSuggestions = computed(() => {
  const agentId = selectedAgentData.value.id?.toString() || '1'
  return getContextualQuestions(agentId)
})

// Use agents from the main composable for consistency
const availableAgents = computed(() => allAgents.value)

// Create or get existing chat session for the selected agent
const ensureChatSession = () => {
  if (!chatStore.activeSession || chatStore.activeSession.agentId !== selectedAgentData.value.id?.toString()) {
    const agentId = selectedAgentData.value.id?.toString() || '1'
    const title = `Chat with ${selectedAgentData.value.name}`
    chatStore.createSession(agentId, title)
  }
}

// Methods
const closeChat = () => {
  emit('close')
}

const formatTime = (timestamp: Date | string) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!messageInput.value.trim() || isSending.value) return

  const content = messageInput.value.trim()
  messageInput.value = ''
  isSending.value = true

  try {
    // Ensure we have a chat session
    ensureChatSession()

    // Add user message
    await chatStore.sendMessage(content)

    // Show typing indicator
    isTyping.value = true

    // Simulate Agent response (replace with actual API call)
    setTimeout(async () => {
      isTyping.value = false

      // Generate sophisticated Agent responses based on content
      const responses = generateAIResponses(content, selectedAgentData.value)

      // Add Agent responses to the active session
      if (chatStore.activeSession) {
        for (const response of responses) {
          chatStore.activeSession.messages.push(response)
          await new Promise(resolve => setTimeout(resolve, 800)) // Stagger responses
          await scrollToBottom()
        }
        chatStore.activeSession.updatedAt = new Date()
      }

      await scrollToBottom()
    }, 1500)

    await scrollToBottom()
  } catch (error) {
    console.error('Failed to send message:', error)

    // Restore the message input if sending failed
    messageInput.value = content

    // Show error toast
    const { error: showError } = useToast()
    showError(
      'Message Failed',
      error instanceof Error ? error.message : 'Failed to send your message. Please try again.'
    )
  } finally {
    isSending.value = false
  }
}

const handleTyping = () => {
  // Clear existing timeout
  if (typingTimeout.value) {
    clearTimeout(typingTimeout.value)
  }

  // Set new timeout
  typingTimeout.value = setTimeout(() => {
    // Stop typing indicator after 1 second of no input
  }, 1000)
}

const handleActionClick = (action: string) => {
  // Handle action button clicks from messages
  console.log('Action clicked:', action)

  // You can implement specific actions here:
  // - Create tasks
  // - Navigate to analytics
  // - Generate content
  // - etc.

  // For now, just add it as a new message
  messageInput.value = action
}

const generateAIResponses = (userMessage: string, agent: any) => {
  const responses = []
  const baseId = Date.now()

  // Analyze the user message to determine response type
  const lowerMessage = userMessage.toLowerCase()

  if (lowerMessage.includes('analytics') || lowerMessage.includes('performance') || lowerMessage.includes('views')) {
    // Analytics-focused response
    responses.push({
      id: `ai-${baseId}`,
      agentId: agent.id?.toString() || '1',
      userId: 'demo-user',
      content: `I'll analyze your channel performance for you. Here's what I found:`,
      type: 'text' as const,
      timestamp: new Date(),
      isFromUser: false,
    })

    responses.push({
      id: `ai-${baseId + 1}`,
      agentId: agent.id?.toString() || '1',
      userId: 'demo-user',
      content: `Your channel has shown strong growth in the past 30 days with a 15% increase in views and 8% growth in subscribers.`,
      type: 'analysis' as const,
      timestamp: new Date(Date.now() + 1000),
      isFromUser: false,
      metadata: {
        analysisType: 'performance',
        confidence: 0.92,
        sources: ['YouTube Analytics API', 'Channel Dashboard', 'Historical Data']
      }
    })

    responses.push({
      id: `ai-${baseId + 2}`,
      agentId: agent.id?.toString() || '1',
      userId: 'demo-user',
      content: `Based on this data, I recommend focusing on your top-performing content themes to maximize growth.`,
      type: 'recommendation' as const,
      timestamp: new Date(Date.now() + 2000),
      isFromUser: false,
      metadata: {
        actionItems: ['Create more tech tutorials', 'Post during peak hours (7-9 PM)', 'Optimize thumbnails']
      }
    })
  } else if (lowerMessage.includes('content') || lowerMessage.includes('video') || lowerMessage.includes('ideas')) {
    // Content creation response
    responses.push({
      id: `ai-${baseId}`,
      agentId: agent.id?.toString() || '1',
      userId: 'demo-user',
      content: `I have some great content ideas for your channel! Let me share what's trending in your niche.`,
      type: 'text' as const,
      timestamp: new Date(),
      isFromUser: false,
    })

    responses.push({
      id: `ai-${baseId + 1}`,
      agentId: agent.id?.toString() || '1',
      userId: 'demo-user',
      content: `Based on trending topics and your audience interests, here are my top recommendations:`,
      type: 'insight' as const,
      timestamp: new Date(Date.now() + 1000),
      isFromUser: false,
      metadata: {
        confidence: 0.88,
        actionItems: ['Create "2024 Tech Predictions" video', 'Start a weekly Q&A series', 'Collaborate with similar channels']
      }
    })
  } else {
    // General response
    responses.push({
      id: `ai-${baseId}`,
      agentId: agent.id?.toString() || '1',
      userId: 'demo-user',
      content: `I understand your question about "${userMessage}". Let me help you with that...`,
      type: 'text' as const,
      timestamp: new Date(),
      isFromUser: false,
    })

    responses.push({
      id: `ai-${baseId + 1}`,
      agentId: agent.id?.toString() || '1',
      userId: 'demo-user',
      content: `Here's my analysis and recommendations for your situation:`,
      type: 'recommendation' as const,
      timestamp: new Date(Date.now() + 1000),
      isFromUser: false,
      metadata: {
        actionItems: ['Review your channel strategy', 'Check latest analytics', 'Plan next content batch']
      }
    })
  }

  return responses
}

const saveSettings = () => {
  // Update agent name if changed
  if (tempAgentName.value.trim()) {
    setAgentName(tempAgentName.value.trim())
  }

  // Update selected agent if changed
  if (tempSelectedAgent.value !== selectedAgent.value?.id) {
    setSelectedAgent(tempSelectedAgent.value)
  }

  showSettings.value = false
}

// Saved questions management
const saveCurrentQuestion = () => {
  const questionText = messageInput.value.trim()
  if (!questionText || savedQuestions.value.some(q => q.text === questionText)) return

  const newQuestion: SavedQuestion = {
    id: Date.now().toString(),
    text: questionText,
    createdAt: new Date()
  }

  savedQuestions.value.unshift(newQuestion)

  // Limit to 10 saved questions
  if (savedQuestions.value.length > 10) {
    savedQuestions.value = savedQuestions.value.slice(0, 10)
  }

  // Save to localStorage
  saveSavedQuestions()
}

const useQuickQuestion = (questionText: string) => {
  messageInput.value = questionText
  // Auto-focus the input after setting the text
  nextTick(() => {
    const inputElement = document.querySelector('input[placeholder="Ask me anything..."]') as HTMLInputElement
    if (inputElement) {
      inputElement.focus()
    }
  })
}

// Sidebar methods
const loadSavedQuestion = (questionText: string) => {
  messageInput.value = questionText
  // Auto-focus the input after setting the text
  nextTick(() => {
    const inputElement = document.querySelector('input[placeholder="Ask me anything..."]') as HTMLInputElement
    if (inputElement) {
      inputElement.focus()
    }
  })
}

const loadSmartSuggestion = (suggestionText: string) => {
  messageInput.value = suggestionText
  // Auto-focus the input after setting the text
  nextTick(() => {
    const inputElement = document.querySelector('input[placeholder="Ask me anything..."]') as HTMLInputElement
    if (inputElement) {
      inputElement.focus()
    }
  })
}

// Save to task/goal handlers
const handleSaveAsTask = (message: ChatMessage) => {
  try {
    const taskId = saveMessageAsTask(message, selectedAgentData.value)
    success('Task Created', 'Agent response has been saved as a task and added to your calendar.')
  } catch (err) {
    console.error('Failed to save task:', err)
    error('Failed to Save Task', 'There was an error saving the task. Please try again.')
  }
}

const handleSaveAsGoal = (message: ChatMessage) => {
  try {
    saveMessageAsGoal(message, selectedAgentData.value)
    success('Goal Created', 'Agent response has been saved as a goal.')
  } catch (err) {
    console.error('Failed to save goal:', err)
    error('Failed to Save Goal', 'There was an error saving the goal. Please try again.')
  }
}

const removeSavedQuestion = (questionId: string) => {
  savedQuestions.value = savedQuestions.value.filter(q => q.id !== questionId)
  saveSavedQuestions()
}

const saveSavedQuestions = () => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('chatSavedQuestions', JSON.stringify(savedQuestions.value))
  }
}

const loadSavedQuestions = () => {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('chatSavedQuestions')
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        savedQuestions.value = parsed.map((q: any) => ({
          ...q,
          createdAt: new Date(q.createdAt)
        }))
      } catch (error) {
        console.error('Failed to load saved questions:', error)
        savedQuestions.value = []
      }
    }
  }
}

// Watch for new messages to auto-scroll
watch(messages, () => {
  scrollToBottom()
}, { deep: true })

// Auto-scroll when panel opens and ensure chat session
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    ensureChatSession()
    scrollToBottom()
  }
})

// Initialize temp values when settings modal opens
watch(showSettings, (isOpen) => {
  if (isOpen) {
    tempAgentName.value = agentName.value || selectedAgentData.value.name || ''
    tempSelectedAgent.value = selectedAgent.value?.id || 1
  }
})

// Initialize saved questions and chat data on mount
onMounted(() => {
  // Load saved chat data first
  chatStore.loadChatData()

  // Load saved questions
  loadSavedQuestions()

  // Ensure we have a chat session
  ensureChatSession()
})
</script>

<style scoped>
/* Slide-right transition */
.slide-right-enter-active,
.slide-right-leave-active {
  transition: transform 0.3s ease-in-out;
}

.slide-right-enter-from {
  transform: translateX(100%);
}

.slide-right-leave-to {
  transform: translateX(100%);
}

/* Backdrop transition */
.backdrop-enter-active,
.backdrop-leave-active {
  transition: opacity 0.3s ease-in-out;
}

.backdrop-enter-from,
.backdrop-leave-to {
  opacity: 0;
}

/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #374151;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #4b5563;
}
</style>
