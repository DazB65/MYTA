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
      class="fixed right-0 top-0 z-50 h-full w-[600px] bg-forest-800 shadow-2xl border-l border-forest-700"
    >
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
        class="flex-1 overflow-y-auto p-4 space-y-4"
        :style="{ height: `calc(100vh - ${savedQuestions.length > 0 ? '280px' : '200px'})` }"
      >
        <!-- Welcome Message -->
        <div v-if="messages.length === 0" class="text-center py-8">
          <div class="w-16 h-16 mx-auto mb-4 rounded-xl overflow-hidden">
            <img
              :src="selectedAgentData.image"
              :alt="selectedAgentData.name"
              class="w-full h-full object-cover"
            />
          </div>
          <h3 class="text-lg font-semibold text-white mb-2">Chat with {{ selectedAgentData.name }}</h3>
          <p class="text-gray-400 text-sm">{{ selectedAgentData.description }}</p>
          <p class="text-gray-500 text-xs mt-2">Start a conversation to get AI-powered insights!</p>
        </div>

        <!-- Messages -->
        <div
          v-for="message in messages"
          :key="message.id"
          class="flex items-start space-x-3"
          :class="message.isFromUser ? 'flex-row-reverse space-x-reverse' : ''"
        >
          <!-- Avatar -->
          <div class="flex-shrink-0">
            <div
              v-if="!message.isFromUser"
              class="w-8 h-8 rounded-lg overflow-hidden"
              :style="{ backgroundColor: selectedAgentData.color + '20' }"
            >
              <img
                :src="selectedAgentData.image"
                :alt="selectedAgentData.name"
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

          <!-- Message Bubble -->
          <div class="flex-1 max-w-[280px]">
            <div
              class="rounded-lg p-3 text-sm"
              :class="message.isFromUser 
                ? 'bg-orange-600 text-white ml-auto' 
                : 'bg-forest-700 text-white'"
            >
              <p>{{ message.content }}</p>
            </div>
            <div class="text-xs text-gray-500 mt-1" :class="message.isFromUser ? 'text-right' : ''">
              {{ formatTime(message.timestamp) }}
            </div>
          </div>
        </div>

        <!-- Typing Indicator -->
        <div v-if="isTyping" class="flex items-start space-x-3">
          <div
            class="w-8 h-8 rounded-lg overflow-hidden"
            :style="{ backgroundColor: selectedAgentData.color + '20' }"
          >
            <img
              :src="selectedAgentData.image"
              :alt="selectedAgentData.name"
              class="w-full h-full object-cover"
            />
          </div>
          <div class="bg-forest-700 rounded-lg p-3">
            <div class="flex space-x-1">
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Questions -->
      <div v-if="savedQuestions.length > 0" class="p-4">
        <div class="mb-3">
          <h4 class="text-sm font-medium text-gray-300 mb-2">Quick Questions</h4>
          <div class="flex flex-wrap gap-2">
            <div
              v-for="question in savedQuestions"
              :key="question.id"
              class="group relative bg-forest-700 hover:bg-forest-600 text-white text-xs px-3 py-2 rounded-lg transition-colors border border-forest-600 hover:border-forest-500"
            >
              <button
                @click="useQuickQuestion(question.text)"
                class="w-full text-left pr-4"
              >
                {{ question.text.length > 30 ? question.text.substring(0, 30) + '...' : question.text }}
              </button>
              <button
                @click.stop="removeSavedQuestion(question.id)"
                class="absolute right-1 top-1/2 transform -translate-y-1/2 opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-400 transition-all"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
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
            <label class="block text-sm font-medium text-gray-300 mb-3">Choose Your Agent</label>
            <div class="grid grid-cols-2 gap-3">
              <div
                v-for="agent in availableAgents"
                :key="agent.id"
                :class="[
                  'relative cursor-pointer rounded-lg border-2 p-3 transition-all hover:shadow-md',
                  tempSelectedAgent === agent.id
                    ? 'border-orange-500 bg-orange-900/30'
                    : 'border-forest-500 hover:border-forest-400',
                ]"
                @click="tempSelectedAgent = agent.id"
              >
                <div class="text-center">
                  <div class="mx-auto mb-2 h-12 w-12 overflow-hidden rounded-lg">
                    <img :src="agent.image" :alt="agent.name" class="h-full w-full object-cover" />
                  </div>
                  <div class="text-xs font-medium text-gray-300">{{ agent.name }}</div>
                  <div class="text-xs text-gray-400 mt-1">{{ agent.personality }}</div>
                </div>
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
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue';
import { useAgentSettings } from '../../composables/useAgentSettings';
import { useChatStore } from '../../stores/chat';

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
const { selectedAgent, agentName } = useAgentSettings()
const chatStore = useChatStore()

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

// Available agents for selection
const availableAgents = [
  {
    id: 1,
    name: 'Agent 1',
    image: '/Agent1.png',
    color: '#ea580c',
    description: 'AI Content Creator',
    personality: 'Professional & Analytical',
  },
  {
    id: 2,
    name: 'Agent 2',
    image: '/Agent2.png',
    color: '#eab308',
    description: 'Marketing Specialist',
    personality: 'Strategic & Data-Driven',
  },
  {
    id: 3,
    name: 'Agent 3',
    image: '/Agent3.png',
    color: '#16a34a',
    description: 'Analytics Expert',
    personality: 'Detail-Oriented & Insightful',
  },
  {
    id: 4,
    name: 'Agent 4',
    image: '/Agent4.png',
    color: '#ea580c',
    description: 'Creative Assistant',
    personality: 'Innovative & Artistic',
  },
  {
    id: 5,
    name: 'Agent 5',
    image: '/Agent5.png',
    color: '#dc2626',
    description: 'Strategy Advisor',
    personality: 'Visionary & Strategic',
  },
]

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

    // Simulate AI response (replace with actual API call)
    setTimeout(async () => {
      isTyping.value = false

      // Mock AI response - in real implementation this would come from WebSocket
      const aiResponse = {
        id: `ai-${Date.now()}`,
        agentId: selectedAgentData.value.id?.toString() || '1',
        userId: 'demo-user',
        content: `I understand your question about "${content}". Let me help you with that...`,
        type: 'text' as const,
        timestamp: new Date(),
        isFromUser: false,
      }

      // Add AI response to the active session
      if (chatStore.activeSession) {
        chatStore.activeSession.messages.push(aiResponse)
        chatStore.activeSession.updatedAt = new Date()
      }

      await scrollToBottom()
    }, 1500)

    await scrollToBottom()
  } catch (error) {
    console.error('Failed to send message:', error)
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

const saveSettings = () => {
  // Update global agent settings
  if (tempAgentName.value.trim()) {
    agentName.value = tempAgentName.value.trim()
  }

  if (tempSelectedAgent.value !== selectedAgent.value?.id) {
    const newAgent = availableAgents.find(a => a.id === tempSelectedAgent.value)
    if (newAgent) {
      // Save to localStorage (this should ideally use the useAgentSettings composable)
      const settings = {
        name: tempAgentName.value.trim() || newAgent.name,
        selectedAgent: tempSelectedAgent.value
      }
      localStorage.setItem('agentSettings', JSON.stringify(settings))

      // Trigger a page reload to update all components with new agent
      window.location.reload()
    }
  } else if (tempAgentName.value.trim()) {
    // Just update the name
    const settings = {
      name: tempAgentName.value.trim(),
      selectedAgent: selectedAgent.value?.id || 1
    }
    localStorage.setItem('agentSettings', JSON.stringify(settings))

    // Update the reactive value
    agentName.value = tempAgentName.value.trim()
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

// Initialize saved questions on mount
onMounted(() => {
  loadSavedQuestions()
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
