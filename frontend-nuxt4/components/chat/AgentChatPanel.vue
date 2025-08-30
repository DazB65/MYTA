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
                :disabled="isSending"
                class="flex-1 text-left text-sm text-gray-300 hover:text-white bg-forest-600 hover:bg-forest-500 rounded-lg px-3 py-2 transition-colors truncate disabled:opacity-50 disabled:cursor-not-allowed"
                :class="{ 'animate-pulse': isSending }"
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
              :disabled="isSending"
              class="w-full text-left text-sm text-gray-300 hover:text-white bg-forest-600 hover:bg-forest-500 rounded-lg px-3 py-2 transition-colors flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              :class="{ 'animate-pulse': isSending }"
            >
              <span class="text-base">{{ suggestion.emoji }}</span>
              <span class="truncate">{{ suggestion.text }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Main Chat Area -->
      <div class="flex-1 flex flex-col">
      <!-- Enhanced Boss Agent Header -->
      <div
        class="border-b border-orange-500/30 p-6 relative overflow-hidden"
        :style="{ background: enhancedHeaderGradient }"
      >
        <!-- Animated Background Elements -->
        <div class="absolute inset-0 opacity-10">
          <div class="absolute top-0 right-0 w-32 h-32 bg-orange-400 rounded-full blur-3xl animate-pulse"></div>
          <div class="absolute bottom-0 left-0 w-24 h-24 bg-yellow-400 rounded-full blur-2xl animate-pulse" style="animation-delay: 1s;"></div>
        </div>

        <div class="flex items-center justify-between relative z-10">
          <div class="flex items-center space-x-4">
            <div class="relative">
              <!-- Enhanced Avatar with Orange Ring -->
              <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-orange-400 to-orange-600 p-0.5">
                <img
                  :src="selectedAgentData.image"
                  :alt="selectedAgentData.name"
                  class="w-full h-full rounded-xl object-cover"
                />
              </div>
              <!-- Executive Status Indicator -->
              <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full border-2 border-orange-600 flex items-center justify-center">
                <div class="w-2 h-2 bg-white rounded-full animate-pulse"></div>
              </div>
              <!-- Coordination Indicator -->
              <div class="absolute -top-1 -left-1 w-4 h-4 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full border border-orange-300 animate-bounce" style="animation-duration: 2s;" title="Coordinating with specialists"></div>
            </div>
            <div>
              <div class="flex items-center space-x-2">
                <h2 class="text-xl font-bold text-white drop-shadow-lg">{{ selectedAgentData.name }}</h2>
                <div class="px-2 py-1 bg-orange-500/20 rounded-full border border-orange-400/30">
                  <span class="text-xs font-medium text-orange-200">Executive Agent</span>
                </div>
              </div>
              <p class="text-sm text-orange-100/90 font-medium">{{ selectedAgentData.personality }}</p>
              <div class="flex items-center space-x-3 mt-1">
                <div class="flex items-center space-x-1 text-xs text-orange-200/80">
                  <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <span>Online & Coordinating</span>
                </div>
                <div class="text-xs text-orange-200/60">•</div>
                <div class="text-xs text-orange-200/80">Managing Alex, Levi, Maya, Zara & Kai</div>
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <!-- New Chat Button -->
            <button
              @click="startNewChat"
              class="p-2 rounded-lg bg-green-500/20 hover:bg-green-500/30 transition-all duration-200 text-green-200 hover:text-white border border-green-400/30 hover:border-green-400/50"
              title="Start New Chat"
            >
              ➕
            </button>

            <!-- Delete Chat Button -->
            <button
              @click="deleteCurrentChat"
              class="p-2 rounded-lg bg-red-500/20 hover:bg-red-500/30 transition-all duration-200 text-red-200 hover:text-white border border-red-400/30 hover:border-red-400/50"
              title="Delete Current Chat"
            >
              🗑️
            </button>
            <!-- Settings Button -->
            <button
              @click="showSettings = true"
              class="p-2 rounded-lg bg-orange-500/20 hover:bg-orange-500/30 transition-all duration-200 text-orange-200 hover:text-white border border-orange-400/30 hover:border-orange-400/50"
              title="Agent Settings"
            >
              ⚙️
            </button>
            <!-- Close Button -->
            <button
              @click="closeChat"
              class="p-2 rounded-lg bg-gray-500/20 hover:bg-gray-500/30 transition-all duration-200 text-gray-200 hover:text-white border border-gray-400/30 hover:border-gray-400/50"
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
        <!-- Enhanced Executive Welcome Message -->
        <div v-if="messages.length === 0" class="text-center py-8 px-4">
          <!-- Executive Avatar with Orange Styling -->
          <div class="w-24 h-24 mx-auto mb-6 relative">
            <div class="w-full h-full rounded-xl overflow-hidden ring-4 ring-orange-400/50 bg-gradient-to-br from-orange-400 to-orange-600 p-1">
              <img
                :src="selectedAgentData.image"
                :alt="selectedAgentData.name"
                class="w-full h-full object-cover rounded-lg"
              />
            </div>
            <!-- Executive Badge -->
            <div class="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-orange-500 to-orange-600 text-white text-xs font-bold px-3 py-1 rounded-full border-2 border-orange-300">
              EXECUTIVE
            </div>
          </div>

          <!-- Personalized Greeting -->
          <div class="mb-6">
            <h3 class="text-2xl font-bold text-white mb-2 bg-gradient-to-r from-orange-300 to-yellow-300 bg-clip-text text-transparent">
              Welcome back to {{ selectedAgentData.name }}
            </h3>
            <p class="text-orange-200 text-sm mb-2 font-medium">{{ selectedAgentData.description }}</p>
            <p class="text-orange-300/80 text-xs mb-4">{{ selectedAgentData.personality }}</p>

            <!-- Executive Status -->
            <div class="flex items-center justify-center space-x-4 text-xs">
              <div class="flex items-center space-x-1 bg-green-500/20 px-3 py-1 rounded-full border border-green-400/30">
                <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span class="text-green-300">All Systems Online</span>
              </div>
              <div class="flex items-center space-x-1 bg-blue-500/20 px-3 py-1 rounded-full border border-blue-400/30">
                <span class="text-blue-300">Alex, Levi, Maya, Zara & Kai Ready</span>
              </div>
            </div>
          </div>



          <p class="text-orange-300/80 text-sm font-medium">Ready to strategize your channel's growth? I'm coordinating with my specialist team to provide you with comprehensive insights.</p>
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
        />

        <!-- Enhanced Executive Typing Indicator -->
        <div v-if="isTyping" class="flex items-start space-x-3">
          <div class="w-10 h-10 rounded-lg overflow-hidden ring-2 ring-orange-400/50 bg-gradient-to-br from-orange-400 to-orange-600 p-0.5">
            <img
              :src="selectedAgentData.image"
              :alt="selectedAgentData.name"
              class="w-full h-full object-cover rounded-lg"
            />
          </div>
          <div class="bg-gradient-to-r from-orange-900/60 to-orange-800/60 rounded-xl p-4 border border-orange-500/30 backdrop-blur-sm max-w-md">
            <div class="flex items-center space-x-3 mb-2">
              <div class="w-6 h-6 rounded-full bg-gradient-to-r from-orange-400 to-orange-500 flex items-center justify-center text-sm animate-pulse">
                🧠
              </div>
              <span class="text-orange-200 text-sm font-medium">{{ selectedAgentData.name }} is strategizing...</span>
            </div>

            <!-- Executive Thinking Process -->
            <div class="space-y-1 text-xs text-orange-300/80">
              <div class="flex items-center space-x-2" v-if="typingStage >= 1">
                <div class="w-1 h-1 bg-blue-400 rounded-full animate-pulse"></div>
                <span>Consulting with {{ currentTypingAgents[0] || 'Alex' }}...</span>
              </div>
              <div class="flex items-center space-x-2" v-if="typingStage >= 2">
                <div class="w-1 h-1 bg-green-400 rounded-full animate-pulse"></div>
                <span>Coordinating with {{ currentTypingAgents[1] || 'Levi' }} and {{ currentTypingAgents[2] || 'Maya' }}...</span>
              </div>
              <div class="flex items-center space-x-2" v-if="typingStage >= 3">
                <div class="w-1 h-1 bg-purple-400 rounded-full animate-pulse"></div>
                <span>Finalizing team recommendations...</span>
              </div>
            </div>

            <!-- Animated Dots -->
            <div class="flex items-center space-x-1 mt-3">
              <span class="text-orange-300 text-sm">Preparing executive summary</span>
              <div class="flex space-x-1">
                <div class="w-1.5 h-1.5 rounded-full bg-orange-400 animate-pulse"></div>
                <div class="w-1.5 h-1.5 rounded-full bg-orange-400 animate-pulse" style="animation-delay: 0.2s;"></div>
                <div class="w-1.5 h-1.5 rounded-full bg-orange-400 animate-pulse" style="animation-delay: 0.4s;"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Enhanced Executive Input Area -->
      <div class="border-t border-orange-500/30 p-4 bg-gradient-to-r from-orange-900/20 to-orange-800/20">
        <!-- Executive Quick Actions Bar -->
        <div class="flex items-center space-x-2 mb-3 overflow-x-auto pb-2">
          <button
            v-for="action in executiveQuickActions"
            :key="action.id"
            @click="loadQuickAction(action.text)"
            :disabled="isSending"
            class="flex-shrink-0 px-3 py-1 bg-orange-600/20 hover:bg-orange-600/30 text-orange-200 text-xs rounded-full border border-orange-500/30 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            :class="{ 'animate-pulse': isSending }"
          >
            <span class="mr-1">{{ action.emoji }}</span>
            {{ action.label }}
          </button>
        </div>

        <div class="flex items-center space-x-3">
          <input
            v-model="messageInput"
            type="text"
            :placeholder="executivePlaceholder"
            class="flex-1 bg-gradient-to-r from-orange-900/40 to-orange-800/40 border border-orange-500/30 rounded-xl px-4 py-3 text-white placeholder-orange-300/60 focus:outline-none focus:ring-2 focus:ring-orange-400/50 focus:border-orange-400/50 backdrop-blur-sm"
            @keyup.enter="sendMessage"
            @input="handleTyping"
          />
          <!-- Executive Bookmark Button -->
          <button
            v-if="messageInput.trim() && !savedQuestions.some(q => q.text === messageInput.trim())"
            @click="saveCurrentQuestion"
            class="p-3 rounded-xl bg-yellow-600/20 hover:bg-yellow-600/30 text-yellow-200 hover:text-yellow-100 transition-all duration-200 border border-yellow-500/30 hover:border-yellow-500/50"
            title="Save this executive query"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
          </button>

          <!-- Saved Indicator -->
          <div
            v-else-if="messageInput.trim() && savedQuestions.some(q => q.text === messageInput.trim())"
            class="p-3 rounded-xl bg-green-600/30 text-green-200 border border-green-500/30"
            title="Executive query saved"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
          </div>

          <!-- Voice Input Button -->
          <button
            @click="toggleVoiceInput"
            class="p-3 rounded-xl bg-purple-600/20 hover:bg-purple-600/30 text-purple-200 hover:text-purple-100 transition-all duration-200 border border-purple-500/30 hover:border-purple-500/50"
            title="Voice input (coming soon)"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          </button>

          <!-- Enhanced Executive Send Button -->
          <button
            @click="sendMessage"
            :disabled="!messageInput.trim() || isSending"
            class="px-6 py-3 rounded-xl font-semibold text-white transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
            :class="messageInput.trim()
              ? 'bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 border border-orange-400/50 hover:border-orange-400/70 shadow-orange-500/25'
              : 'bg-gray-600 border border-gray-500/30'"
            title="Send executive message"
          >
            <div v-if="!isSending" class="flex items-center space-x-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
              <span class="text-sm">Send</span>
            </div>
            <div v-else class="flex items-center space-x-2">
              <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span class="text-sm">Processing...</span>
            </div>
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
          class="bg-forest-700 rounded-xl p-8 w-full max-w-2xl border border-forest-600"
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
            <label class="block text-sm font-medium text-gray-300 mb-2">Name Your Boss Agent</label>
            <input
              v-model="tempAgentName"
              type="text"
              placeholder="Enter agent name..."
              class="w-full bg-forest-600 border border-forest-500 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:border-transparent"
              :style="{ '--tw-ring-color': selectedAgentData.color }"
            />
          </div>

          <!-- Boss Agent Display -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-300 mb-3">Your Personal Boss Agent</label>
            <p class="text-sm text-gray-300 mb-4">Your Boss Agent coordinates with specialized agents behind the scenes</p>
            <div class="text-center">
              <div class="mx-auto mb-4 h-24 w-24 overflow-hidden rounded-xl bg-gray-100 ring-4 ring-orange-500 ring-opacity-50">
                <img :src="bossAgent.image" :alt="bossAgent.name" class="h-full w-full object-cover" />
              </div>
              <div class="text-lg font-semibold text-white">{{ tempAgentName || bossAgent.name }}</div>
              <div class="text-sm text-gray-400">{{ bossAgent.description }}</div>
            </div>
          </div>

          <!-- Specialist Agents Display -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-300 mb-3">Your Specialist Team</label>
            <p class="text-sm text-gray-300 mb-4">Your Boss Agent coordinates with these specialists behind the scenes</p>
            <div class="grid grid-cols-5 gap-2">
              <div
                v-for="agent in specialistAgents"
                :key="agent.id"
                class="text-center"
              >
                <div class="mx-auto mb-1 h-10 w-10 overflow-hidden rounded-lg bg-gray-100">
                  <img :src="agent.image" :alt="agent.name" class="h-full w-full object-cover" />
                </div>
                <div class="text-xs font-medium text-gray-400">{{ agent.name }}</div>
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

  <!-- Delete Confirmation Modal -->
  <Teleport to="body">
    <Transition name="backdrop">
      <div
        v-if="showDeleteConfirmation"
        class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        @click="showDeleteConfirmation = false"
      >
        <div
          class="bg-gradient-to-br from-red-900/90 to-red-800/90 rounded-xl p-6 max-w-md w-full border border-red-500/30 backdrop-blur-sm"
          @click.stop
        >
          <div class="flex items-center space-x-3 mb-4">
            <div class="w-10 h-10 rounded-full bg-red-500/20 flex items-center justify-center">
              <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-white">Delete Chat Conversation</h3>
              <p class="text-red-200/80 text-sm">This action cannot be undone</p>
            </div>
          </div>

          <p class="text-red-100 text-sm mb-6 leading-relaxed">
            Are you sure you want to delete this entire conversation with {{ selectedAgentData.name }}?
            All messages and insights will be permanently removed.
          </p>

          <div class="flex items-center space-x-3">
            <button
              @click="showDeleteConfirmation = false"
              class="flex-1 px-4 py-2 rounded-lg bg-gray-600/30 hover:bg-gray-600/50 text-gray-200 hover:text-white transition-all duration-200 border border-gray-500/30"
            >
              Cancel
            </button>
            <button
              @click="deleteCurrentChat"
              class="flex-1 px-4 py-2 rounded-lg bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-medium transition-all duration-200 shadow-lg"
            >
              Delete Chat
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue';
import { useAgentSettings } from '../../composables/useAgentSettings';
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

const { success, error } = useToast()
const { openTask } = useModals()

// Refs
const messagesContainer = ref<HTMLElement>()
const messageInput = ref('')
const isSending = ref(false)
const isTyping = ref(false)
const typingTimeout = ref<NodeJS.Timeout>()
const showSettings = ref(false)
const tempAgentName = ref('')
const tempSelectedAgent = ref(0) // Boss Agent is always ID 0
const savedQuestions = ref<Array<{ id: string; text: string; createdAt: Date }>>([])

const typingStage = ref(0)
const voiceInputActive = ref(false)
const currentTypingAgents = ref<string[]>(['Alex', 'Levi', 'Maya'])
const showDeleteConfirmation = ref(false)

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
    name: agentName.value || selectedAgent.value?.name || 'Agent'
  }
})

const enhancedHeaderGradient = computed(() => {
  const color = selectedAgentData.value.color || '#f97316'
  return `linear-gradient(135deg, ${color}40 0%, ${color}20 50%, ${color}10 100%)`
})

const executivePlaceholder = computed(() => {
  const name = selectedAgentData.value.name || 'Boss Agent'
  const placeholders = [
    `Ask ${name} for strategic insights...`,
    `What's your executive recommendation, ${name}?`,
    `${name}, analyze my channel performance...`,
    `Help me strategize, ${name}...`,
    `${name}, coordinate with your team on...`
  ]
  return placeholders[Math.floor(Math.random() * placeholders.length)]
})

const messages = computed(() => {
  return chatStore.activeSessionMessages || []
})

const smartSuggestions = computed(() => {
  const agentId = selectedAgentData.value.id?.toString() || '1'
  return getContextualQuestions(agentId)
})

const executiveQuickActions = computed(() => [
  { id: 1, emoji: '📊', label: 'Analytics Review', text: 'Provide me with a comprehensive analytics review of my channel performance' },
  { id: 2, emoji: '🎯', label: 'Growth Strategy', text: 'What\'s our strategic plan for channel growth this quarter?' },
  { id: 3, emoji: '💡', label: 'Content Ideas', text: 'Generate 5 viral content ideas for my niche based on current trends' },
  { id: 4, emoji: '🔍', label: 'Competitor Analysis', text: 'Analyze my top 3 competitors and identify content gaps I can exploit' },
  { id: 5, emoji: '📈', label: 'Revenue Optimization', text: 'How can we optimize revenue streams and monetization?' },
  { id: 6, emoji: '🎬', label: 'Video Optimization', text: 'Review my latest video and suggest improvements for better performance' },
  { id: 7, emoji: '🔥', label: 'Trending Topics', text: 'What are the hottest trending topics in my niche right now?' },
  { id: 8, emoji: '📝', label: 'Script Ideas', text: 'Generate 3 detailed video script outlines for my next uploads' },
  { id: 9, emoji: '🎨', label: 'Thumbnail Tips', text: 'Analyze successful thumbnails in my niche and give me design tips' },
  { id: 10, emoji: '⚡', label: 'Quick Wins', text: 'Give me 5 quick actions I can take today to boost my channel' }
])

// Boss Agent and specialist agents for the new interface
const bossAgent = computed(() => allAgents.value[0]) // Boss Agent is always first
const specialistAgents = computed(() => allAgents.value.slice(1)) // All other agents are specialists

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

    // Show enhanced typing indicator with stages
    isTyping.value = true
    typingStage.value = 0

    // Determine which agents to show based on message content
    const lowerContent = content.toLowerCase()
    if (lowerContent.includes('analytics') || lowerContent.includes('performance')) {
      currentTypingAgents.value = ['Alex', 'Zara', 'Kai']
    } else if (lowerContent.includes('content') || lowerContent.includes('video')) {
      currentTypingAgents.value = ['Levi', 'Maya', 'Alex']
    } else if (lowerContent.includes('strategy') || lowerContent.includes('growth')) {
      currentTypingAgents.value = ['Alex', 'Zara', 'Levi']
    } else {
      currentTypingAgents.value = ['Alex', 'Levi', 'Maya']
    }

    // Simulate executive thinking process
    const thinkingStages = [
      { delay: 500, stage: 1 },
      { delay: 1000, stage: 2 },
      { delay: 1500, stage: 3 }
    ]

    thinkingStages.forEach(({ delay, stage }) => {
      setTimeout(() => {
        if (isTyping.value) typingStage.value = stage
      }, delay)
    })

    // Simulate Agent response (replace with actual API call)
    setTimeout(async () => {
      isTyping.value = false
      typingStage.value = 0

      // Generate sophisticated Agent responses based on content
      const responses = generateExecutiveResponses(content, selectedAgentData.value)

      // Add Agent responses to the active session
      if (chatStore.activeSession) {
        for (const response of responses) {
          chatStore.activeSession.messages.push(response)
          await new Promise(resolve => setTimeout(resolve, 1000)) // Stagger responses
          await scrollToBottom()
        }
        chatStore.activeSession.updatedAt = new Date()
      }

      await scrollToBottom()
    }, 2500)

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

const loadQuickAction = async (actionText: string) => {
  // Immediately send the action as a message instead of populating input
  if (isSending.value) return

  isSending.value = true

  try {
    // Ensure we have a chat session
    ensureChatSession()

    // Add user message directly
    await chatStore.sendMessage(actionText)

    // Show enhanced typing indicator with stages
    isTyping.value = true
    typingStage.value = 0

    // Determine which agents to show based on action content
    const lowerAction = actionText.toLowerCase()
    if (lowerAction.includes('analytics') || lowerAction.includes('performance')) {
      currentTypingAgents.value = ['Alex', 'Zara', 'Kai']
    } else if (lowerAction.includes('content') || lowerAction.includes('video')) {
      currentTypingAgents.value = ['Levi', 'Maya', 'Alex']
    } else if (lowerAction.includes('strategy') || lowerAction.includes('growth')) {
      currentTypingAgents.value = ['Alex', 'Zara', 'Levi']
    } else if (lowerAction.includes('competitor') || lowerAction.includes('seo')) {
      currentTypingAgents.value = ['Kai', 'Alex', 'Zara']
    } else if (lowerAction.includes('revenue') || lowerAction.includes('monetization')) {
      currentTypingAgents.value = ['Zara', 'Alex', 'Maya']
    } else {
      currentTypingAgents.value = ['Alex', 'Levi', 'Maya']
    }

    // Simulate executive thinking process
    const thinkingStages = [
      { delay: 500, stage: 1 },
      { delay: 1000, stage: 2 },
      { delay: 1500, stage: 3 }
    ]

    thinkingStages.forEach(({ delay, stage }) => {
      setTimeout(() => {
        if (isTyping.value) typingStage.value = stage
      }, delay)
    })

    // Generate executive response
    setTimeout(async () => {
      isTyping.value = false
      typingStage.value = 0

      // Generate sophisticated Agent responses based on content
      const responses = generateExecutiveResponses(actionText, selectedAgentData.value)

      // Add Agent responses to the active session
      if (chatStore.activeSession) {
        for (const response of responses) {
          chatStore.activeSession.messages.push(response)
          await new Promise(resolve => setTimeout(resolve, 1000)) // Stagger responses
          await scrollToBottom()
        }
        chatStore.activeSession.updatedAt = new Date()
      }

      await scrollToBottom()
    }, 2500)

    await scrollToBottom()
  } catch (error) {
    console.error('Failed to send quick action:', error)

    // Show error toast
    const { error: showError } = useToast()
    showError(
      'Quick Action Failed',
      error instanceof Error ? error.message : 'Failed to execute quick action. Please try again.'
    )
  } finally {
    isSending.value = false
  }
}

const toggleVoiceInput = () => {
  voiceInputActive.value = !voiceInputActive.value
  // TODO: Implement voice input functionality
  console.log('Voice input toggled:', voiceInputActive.value)
}

const startNewChat = () => {
  // Clear current session and start fresh
  if (chatStore.activeSession) {
    chatStore.setActiveSession(null)
  }

  // Create a new session
  ensureChatSession()

  // Clear any typing states
  isTyping.value = false
  typingStage.value = 0
  messageInput.value = ''

  // Show success message
  success('New Chat Started', `Started a fresh conversation with ${selectedAgentData.value.name}!`)
}

const deleteCurrentChat = () => {
  if (!chatStore.activeSession) {
    showDeleteConfirmation.value = false
    return
  }

  const sessionId = chatStore.activeSession.id

  // Delete the session from the store
  chatStore.deleteSession(sessionId)

  // Clear any typing states
  isTyping.value = false
  typingStage.value = 0
  messageInput.value = ''

  // Close the confirmation modal
  showDeleteConfirmation.value = false

  // Create a new session immediately
  ensureChatSession()

  // Show success message
  success('Chat Deleted', `Conversation deleted and started fresh with ${selectedAgentData.value.name}!`)
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

const handleActionClick = async (action: string) => {
  // Handle action button clicks from messages - immediately send as message
  console.log('Action clicked:', action)

  // Immediately send the action as a message for instant interaction
  await loadQuickAction(action)
}

const getCoordinationScenario = (messageType: string) => {
  const scenarios = {
    analytics: {
      agents: ['Alex', 'Zara', 'Kai'],
      content: 'I\'ve consulted with Alex on analytics, Zara on growth metrics, and Kai on technical performance.',
      time: '2.1 seconds'
    },
    content: {
      agents: ['Levi', 'Maya', 'Alex'],
      content: 'I\'ve coordinated with Levi on content strategy, Maya on audience engagement, and Alex on performance data.',
      time: '2.4 seconds'
    },
    strategy: {
      agents: ['Alex', 'Zara', 'Levi', 'Maya'],
      content: 'I\'ve assembled the full team - Alex, Zara, Levi, and Maya - for comprehensive strategic planning.',
      time: '3.1 seconds'
    },
    general: {
      agents: ['Alex', 'Levi', 'Maya'],
      content: 'I\'ve coordinated with Alex, Levi, and Maya to provide you with well-rounded insights.',
      time: '2.3 seconds'
    }
  }
  return scenarios[messageType] || scenarios.general
}

const generateExecutiveResponses = (userMessage: string, agent: any) => {
  const responses = []
  const baseId = Date.now()
  const lowerMessage = userMessage.toLowerCase()

  // Determine coordination scenario based on message content
  let coordinationScenario
  if (lowerMessage.includes('analytics') || lowerMessage.includes('performance') || lowerMessage.includes('views')) {
    coordinationScenario = getCoordinationScenario('analytics')
  } else if (lowerMessage.includes('content') || lowerMessage.includes('video') || lowerMessage.includes('ideas')) {
    coordinationScenario = getCoordinationScenario('content')
  } else if (lowerMessage.includes('strategy') || lowerMessage.includes('growth') || lowerMessage.includes('plan')) {
    coordinationScenario = getCoordinationScenario('strategy')
  } else {
    coordinationScenario = getCoordinationScenario('general')
  }

  // Executive coordination message
  responses.push({
    id: `ai-${baseId}`,
    agentId: agent.id?.toString() || '0',
    userId: 'demo-user',
    content: coordinationScenario.content,
    type: 'coordination' as const,
    timestamp: new Date(),
    isFromUser: false,
    metadata: {
      coordinatedAgents: coordinationScenario.agents,
      coordinationTime: coordinationScenario.time
    }
  })

  if (lowerMessage.includes('analytics') || lowerMessage.includes('performance') || lowerMessage.includes('views')) {
    // Executive analytics response
    responses.push({
      id: `ai-${baseId + 1}`,
      agentId: agent.id?.toString() || '0',
      userId: 'demo-user',
      content: `Executive Summary: Your channel performance shows strong momentum with strategic opportunities for acceleration.`,
      type: 'executive_insight' as const,
      timestamp: new Date(Date.now() + 1000),
      isFromUser: false,
      metadata: {
        confidence: 0.94,
        priority: 'high',
        kpis: {
          growth: '+15%',
          engagement: '+8%',
          revenue: '+12%'
        }
      }
    })

    responses.push({
      id: `ai-${baseId + 2}`,
      agentId: agent.id?.toString() || '0',
      userId: 'demo-user',
      content: `Strategic Recommendations: Focus on high-performing content verticals and optimize posting schedule for maximum reach.`,
      type: 'strategic_recommendation' as const,
      timestamp: new Date(Date.now() + 2000),
      isFromUser: false,
      metadata: {
        actionItems: [
          'Scale successful content formats by 40%',
          'Implement data-driven posting schedule',
          'Launch premium content tier',
          'Expand into trending niches'
        ],
        timeline: '30-day implementation',
        expectedROI: '25-35% growth'
      }
    })
  } else if (lowerMessage.includes('strategy') || lowerMessage.includes('growth') || lowerMessage.includes('plan')) {
    // Strategic planning response
    responses.push({
      id: `ai-${baseId + 1}`,
      agentId: agent.id?.toString() || '0',
      userId: 'demo-user',
      content: `Executive Strategy Brief: I've developed a comprehensive growth strategy based on market analysis and competitive intelligence.`,
      type: 'executive_insight' as const,
      timestamp: new Date(Date.now() + 1000),
      isFromUser: false,
      metadata: {
        confidence: 0.91,
        priority: 'critical',
        strategicPillars: ['Content Excellence', 'Audience Expansion', 'Revenue Diversification']
      }
    })

    responses.push({
      id: `ai-${baseId + 2}`,
      agentId: agent.id?.toString() || '0',
      userId: 'demo-user',
      content: `Implementation Roadmap: Phase 1 focuses on content optimization, Phase 2 on audience expansion, and Phase 3 on monetization enhancement.`,
      type: 'strategic_recommendation' as const,
      timestamp: new Date(Date.now() + 2000),
      isFromUser: false,
      metadata: {
        actionItems: [
          'Q1: Content format optimization',
          'Q2: Audience acquisition campaigns',
          'Q3: Revenue stream diversification',
          'Q4: Market expansion strategy'
        ],
        timeline: '12-month strategic plan',
        expectedROI: '150-200% growth'
      }
    })
  } else {
    // General executive response
    responses.push({
      id: `ai-${baseId + 1}`,
      agentId: agent.id?.toString() || '0',
      userId: 'demo-user',
      content: `Executive Analysis: I've reviewed your query "${userMessage}" and coordinated with relevant specialists for a comprehensive response.`,
      type: 'executive_insight' as const,
      timestamp: new Date(Date.now() + 1000),
      isFromUser: false,
      metadata: {
        confidence: 0.87,
        priority: 'medium',
        analysisDepth: 'comprehensive'
      }
    })

    responses.push({
      id: `ai-${baseId + 2}`,
      agentId: agent.id?.toString() || '0',
      userId: 'demo-user',
      content: `Strategic Next Steps: Based on our analysis, here are the prioritized actions to address your needs effectively.`,
      type: 'strategic_recommendation' as const,
      timestamp: new Date(Date.now() + 2000),
      isFromUser: false,
      metadata: {
        actionItems: [
          'Conduct detailed situation analysis',
          'Develop targeted action plan',
          'Implement monitoring systems',
          'Schedule progress reviews'
        ],
        timeline: '2-week sprint',
        expectedROI: 'Measurable improvement'
      }
    })
  }

  return responses
}

const saveSettings = () => {
  // Update Boss Agent name if changed
  if (tempAgentName.value.trim()) {
    setAgentName(tempAgentName.value.trim())
  }

  // Always ensure Boss Agent is selected (ID 0)
  if (selectedAgent.value?.id !== 0) {
    setSelectedAgent(0)
  }

  showSettings.value = false
  success('Settings Saved', 'Your Boss Agent settings have been updated!')
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

// Enhanced sidebar methods - immediately send messages
const loadSavedQuestion = async (questionText: string) => {
  // Immediately send the saved question as a message
  await loadQuickAction(questionText)
}

const loadSmartSuggestion = async (suggestionText: string) => {
  // Immediately send the smart suggestion as a message
  await loadQuickAction(suggestionText)
}

// Save to task/goal handlers
const handleSaveAsTask = (message: ChatMessage) => {
  try {
    // Prepare task data for the modal
    const taskData = prepareTaskData(message, selectedAgentData.value)

    // Close the chat panel first
    emit('close')

    // Open task modal with prefilled data after a short delay
    setTimeout(() => {
      openTask(taskData)
    }, 100)

  } catch (err) {
    console.error('Failed to prepare task data:', err)
    error('Failed to Open Task Modal', 'There was an error preparing the task data. Please try again.')
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
    tempSelectedAgent.value = 0 // Always Boss Agent
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
/* Enhanced slide-right transition */
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.slide-right-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.slide-right-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* Enhanced backdrop transition */
.backdrop-enter-active,
.backdrop-leave-active {
  transition: all 0.3s ease-in-out;
}

.backdrop-enter-from,
.backdrop-leave-to {
  opacity: 0;
  backdrop-filter: blur(0px);
}

/* Custom executive scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(249, 115, 22, 0.1);
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #f97316, #ea580c);
  border-radius: 4px;
  border: 1px solid rgba(249, 115, 22, 0.3);
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #ea580c, #c2410c);
}

/* Executive glow effects */
@keyframes executive-glow {
  0%, 100% { box-shadow: 0 0 20px rgba(249, 115, 22, 0.3); }
  50% { box-shadow: 0 0 30px rgba(249, 115, 22, 0.5); }
}

.executive-glow {
  animation: executive-glow 3s ease-in-out infinite;
}

/* Floating animation for background elements */
@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  33% { transform: translateY(-10px) rotate(1deg); }
  66% { transform: translateY(5px) rotate(-1deg); }
}

.float-animation {
  animation: float 6s ease-in-out infinite;
}

/* Pulse animation for status indicators */
@keyframes status-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.1); }
}

.status-pulse {
  animation: status-pulse 2s ease-in-out infinite;
}

/* Gradient text animation */
@keyframes gradient-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.gradient-text {
  background: linear-gradient(45deg, #f97316, #fbbf24, #f97316);
  background-size: 200% 200%;
  animation: gradient-shift 3s ease infinite;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
