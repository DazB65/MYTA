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
      class="fixed right-0 top-0 z-50 h-full w-[400px] bg-forest-800 shadow-2xl border-l border-forest-700"
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
          <button
            @click="closeChat"
            class="p-2 rounded-lg hover:bg-white/10 transition-colors text-white/80 hover:text-white"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Chat Messages Area -->
      <div 
        ref="messagesContainer"
        class="flex-1 overflow-y-auto p-4 space-y-4"
        style="height: calc(100vh - 200px);"
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

      <!-- Input Area -->
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
          <button
            @click="sendMessage"
            :disabled="!messageInput.trim() || isSending"
            class="px-4 py-3 rounded-lg font-medium text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            :style="{ 
              backgroundColor: messageInput.trim() ? selectedAgentData.color : '#374151',
              ':hover': { backgroundColor: messageInput.trim() ? selectedAgentData.color + 'dd' : '#374151' }
            }"
          >
            <svg v-if="!isSending" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
            <div v-else class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue';
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
