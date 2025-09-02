<template>
  <div v-if="isOpen" class="fixed inset-0 z-50">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black bg-opacity-50" @click="closeModal"/>

    <!-- Modal positioned on right side -->
    <div
      class="absolute right-6 top-6 bottom-6 w-[600px] overflow-hidden rounded-2xl shadow-2xl"
      :style="{ backgroundColor: agentData.color + '20' }"
    >
      <!-- Header -->
      <div
        class="flex items-center justify-between p-6"
        :style="{ background: `linear-gradient(135deg, ${agentData.color}dd 0%, ${agentData.color} 100%)` }"
      >
        <div class="flex items-center space-x-4">
          <div class="h-20 w-20 overflow-hidden rounded-xl">
            <img
              :src="agentData.image"
              :alt="agentData.name"
              class="h-full w-full rounded-xl bg-white object-cover"
            />
          </div>
          <div>
            <h2 class="text-3xl font-bold text-white">{{ agentData.name }}</h2>
            <p class="text-base font-medium text-white">MY YT Agent</p>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <button
            class="flex h-10 w-10 items-center justify-center rounded-full text-white hover:opacity-80 transition-opacity"
            :style="{ backgroundColor: agentData.color }"
          >
            <svg class="h-5 w-5 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
          <button
            class="flex h-10 w-10 items-center justify-center rounded-full text-white hover:opacity-80 transition-opacity"
            :style="{ backgroundColor: agentData.color + 'aa' }"
            @click="openSettings"
          >
            <svg class="h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
          <button
            class="flex h-8 w-8 items-center justify-center rounded-full text-white hover:opacity-80 transition-opacity"
            :style="{ backgroundColor: agentData.color + '66' }"
            @click="closeModal"
          >
            <svg class="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Content -->
      <div class="flex" style="height: calc(100% - 120px)">
        <!-- Tabs -->
        <div class="w-64 border-r p-4" :style="{ borderColor: agentData.color + '44', backgroundColor: agentData.color + '11' }">
          <div class="space-y-2">
            <button
              :class="[
                'w-full rounded-lg px-4 py-3 text-left font-medium transition-colors',
                activeTab === 'chats'
                  ? 'bg-orange-500 text-white'
                  : 'text-gray-400',
              ]"
              @click="activeTab = 'chats'"
            >
              Chats
            </button>
            <button
              :class="[
                'w-full rounded-lg px-4 py-3 text-left font-medium transition-colors',
                activeTab === 'visualizer'
                  ? 'bg-orange-500 text-white'
                  : 'text-gray-400',
              ]"
              @click="activeTab = 'visualizer'"
            >
              Visualizer View
            </button>
          </div>

          <!-- Topic Tags -->
          <div class="mt-6">
            <div class="flex flex-wrap gap-2">
              <span class="rounded-full bg-pink-600 px-3 py-1 text-sm text-pink-100"
                >Trending Topics</span
              >
              <span class="rounded-full bg-blue-600 px-3 py-1 text-sm text-blue-100"
                >Competitor Analysis</span
              >
              <span class="rounded-full bg-green-600 px-3 py-1 text-sm text-green-100"
                >Channel Insights</span
              >
            </div>
          </div>

          <!-- Saved Questions -->
          <div v-if="savedQuestions.length > 0" class="mt-6">
            <h4 class="mb-3 text-sm font-medium text-gray-400">Saved Questions</h4>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="question in savedQuestions"
                :key="question.id"
                class="group relative cursor-pointer rounded-full bg-purple-600 px-3 py-1 text-sm text-purple-100 transition-colors hover:bg-purple-700"
                @click="loadSavedQuestion(question)"
              >
                {{
                  question.text.length > 30 ? question.text.substring(0, 30) + '...' : question.text
                }}
                <button
                  class="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 opacity-0 transition-opacity group-hover:opacity-100"
                  @click.stop="deleteSavedQuestion(question.id)"
                >
                  <svg
                    class="h-2 w-2 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </span>
            </div>
          </div>
        </div>

        <!-- Chat Area -->
        <div class="flex flex-1 flex-col" :style="{ backgroundColor: agentData.color + '08' }">
          <!-- Chat Messages -->
          <div class="flex-1 overflow-y-auto p-6">
            <div class="space-y-4">
              <div
                v-for="message in chatMessages"
                :key="message.id"
                class="flex items-start space-x-3"
                :class="message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''"
              >
                <div
                  class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full text-sm font-bold text-white"
                  :style="{ backgroundColor: message.type === 'ai' ? agentData.color : '#ea580c' }"
                >
                  {{ message.type === 'ai' ? 'AI' : 'U' }}
                </div>
                <div class="flex-1">
                  <div
                    class="rounded-lg p-3"
                    :class="message.type === 'ai' ? 'bg-gray-700' : 'ml-auto max-w-md bg-orange-600'"
                  >
                    <p class="text-sm">
                      <span class="font-medium text-white">
                        {{ message.type === 'ai' ? 'Agent' : 'You' }}
                      </span>
                      <span
                        class="ml-2 text-xs"
                        :class="message.type === 'ai' ? 'text-gray-500' : 'text-blue-200'"
                      >
                        {{ message.timestamp }}
                      </span>
                    </p>
                    <p class="mt-1" :class="message.type === 'ai' ? 'text-gray-300' : 'text-white'">
                      {{ message.message }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Input Area -->
          <div class="border-t px-6 py-4" :style="{ borderColor: agentData.color + '44' }">
            <div class="flex items-center space-x-3">
              <input
                v-model="messageInput"
                type="text"
                placeholder="Type your question..."
                class="flex-1 rounded-lg border px-4 py-3 text-white placeholder-gray-400 focus:border-transparent focus:outline-none focus:ring-2"
                :style="{
                  borderColor: agentData.color + '66',
                  backgroundColor: agentData.color + '22',
                  '--tw-ring-color': agentData.color
                }"
                @keyup.enter="sendMessage"
              />
              <button
                class="flex items-center space-x-2 rounded-lg bg-green-600 px-4 py-3 font-medium text-white transition-colors hover:bg-green-700"
                title="Save Question"
                @click="saveQuestion"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
                <span class="hidden sm:inline">Save</span>
              </button>
              <button
                class="rounded-lg bg-orange-500 px-6 py-3 font-medium text-white transition-colors hover:bg-orange-600"
                @click="sendMessage"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Settings Panel -->
      <div
        v-if="showSettings"
        class="absolute inset-y-0 right-0 w-96 transform border-l border-green-700 bg-green-800 transition-transform duration-300 ease-in-out"
      >
        <!-- Settings Header -->
        <div class="flex items-center justify-between border-b border-green-700 p-6">
          <h3 class="text-lg font-semibold text-white">Agent Settings</h3>
          <button
            class="flex h-8 w-8 items-center justify-center rounded-full bg-green-700 hover:bg-green-600"
            @click="closeSettings"
          >
            <svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>

        <!-- Settings Content -->
        <div class="space-y-6 overflow-y-auto p-6" style="height: calc(100% - 80px)">
          <!-- Agent Name -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-300">Boss Agent Name</label>
            <input
              v-model="tempSettings.name"
              type="text"
              placeholder="Enter your Boss Agent's name"
              class="w-full rounded-lg border border-green-600 bg-green-700 px-4 py-3 text-white placeholder-gray-400 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-orange-500"
            />
            <p class="mt-1 text-xs text-gray-400">
              Your Boss Agent coordinates with specialized agents behind the scenes
            </p>
          </div>

          <!-- Boss Agent Display -->
          <div>
            <label class="mb-3 block text-sm font-medium text-gray-300">Your Personal Boss Agent</label>
            <div class="mb-6 text-center">
              <div class="mx-auto mb-4 h-24 w-24 overflow-hidden rounded-xl bg-gray-100 ring-4 ring-orange-500 ring-opacity-50">
                <img :src="bossAgent.image" :alt="bossAgent.name" class="h-full w-full object-cover" />
              </div>
              <div class="text-lg font-semibold text-white">{{ tempSettings.name || bossAgent.name }}</div>
              <div class="text-sm text-gray-400">{{ bossAgent.description }}</div>
            </div>
          </div>

          <!-- Specialist Agents Display -->
          <div>
            <label class="mb-3 block text-sm font-medium text-gray-300">Your Specialist Team</label>
            <p class="mb-4 text-xs text-gray-400">
              Your Boss Agent coordinates with these specialists behind the scenes
            </p>
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

          <!-- Preview -->
          <div class="rounded-lg bg-green-800 p-4">
            <h4 class="mb-3 text-sm font-medium text-gray-300">Preview</h4>
            <div class="flex items-center space-x-3">
              <div class="h-10 w-10 overflow-hidden rounded-lg bg-gray-100">
                <img
                  :src="selectedTempAgentData.image"
                  :alt="selectedTempAgentData.name"
                  class="h-full w-full object-cover"
                />
              </div>
              <div>
                <div class="text-sm font-bold text-white">
                  {{ tempSettings.name || 'Professional Assistant' }}
                </div>
                <div class="text-xs font-medium text-white">MY YT Agent</div>
              </div>
            </div>
          </div>

          <!-- Save Button -->
          <div class="flex justify-end space-x-3">
            <button
              class="rounded-lg bg-gray-600 px-4 py-2 text-white transition-colors hover:bg-gray-500"
              @click="closeSettings"
            >
              Cancel
            </button>
            <button
              class="rounded-lg bg-orange-600 px-4 py-2 text-white transition-colors hover:bg-orange-700"
              @click="saveAgentSettings"
            >
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAgentSettings } from '../../composables/useAgentSettings'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close'])

// Use the agent settings composable
const { agentName, selectedAgentId, selectedAgent, setSelectedAgent, setAgentName } = useAgentSettings()

const activeTab = ref('chats')
const messageInput = ref('')
const showSettings = ref(false)
const showSaveDialog = ref(false)
const questionToSave = ref('')
const savedQuestions = ref([])
const chatMessages = ref([
  {
    id: 1,
    type: 'ai',
    message: "Hello! I'm your AI content creation assistant. How can I help you today?",
    timestamp: '10:30 AM',
  },
])

// Temporary settings for the modal (before saving)
const tempSettings = ref({
  name: '',
})

// Available AI team members - Boss Agent leads the team coordination
const agents = [
  {
    id: 0,
    name: 'Boss Agent',
    image: '/BossAgent.png',
    color: '#f97316', // Orange - primary brand color
    description: 'Your Team Leader',
    personality: 'Leads your AI team and coordinates with specialized team members',
  },
  {
    id: 1,
    name: 'Alex',
    image: '/optimized/Agent1.jpg',
    color: '#f97316', // Orange
    description: 'Analytics Team Member',
    personality: 'Data-driven team member who collaborates on strategic insights',
  },
  {
    id: 2,
    name: 'Levi',
    image: '/optimized/Agent2.jpg',
    color: '#3b82f6', // Blue
    description: 'Content Team Member',
    personality: 'Creative team member who works with others on content strategy',
  },
  {
    id: 3,
    name: 'Maya',
    image: '/optimized/Agent3.jpg',
    color: '#a855f7', // Purple
    description: 'Engagement Team Member',
    personality: 'Community-focused team member who collaborates on audience strategy',
  },
  {
    id: 4,
    name: 'Zara',
    image: '/optimized/Agent4.jpg',
    color: '#eab308', // Yellow
    description: 'Growth Team Member',
    personality: 'Results-driven team member who works with others on optimization',
  },
  {
    id: 5,
    name: 'Kai',
    image: '/optimized/Agent5.jpg',
    color: '#16a34a', // Green
    description: 'Technical Team Member',
    personality: 'Technical team member who coordinates on SEO and optimization',
  },
]

// Computed properties for Boss Agent and specialists
const bossAgent = computed(() => agents[0]) // Boss Agent is always first
const specialistAgents = computed(() => agents.slice(1)) // All other agents are specialists

// Computed property for current agent data (always Boss Agent)
const agentData = computed(() => {
  return {
    ...bossAgent.value,
    name: agentName.value || bossAgent.value.name,
  }
})

const openSettings = () => {
  // Copy current settings to temp settings
  tempSettings.value = {
    name: agentName.value
  }
  showSettings.value = true
}

const closeSettings = () => {
  showSettings.value = false
}

const saveAgentSettings = () => {
  // Update settings using the composable (only name, since Boss Agent is always selected)
  if (tempSettings.value.name !== agentName.value) {
    setAgentName(tempSettings.value.name)
  }

  // Close settings panel
  showSettings.value = false

  // Optional: Show success message
  console.log('Boss Agent settings saved!')
}

const closeModal = () => {
  showSettings.value = false
  emit('close')
}

const sendMessage = () => {
  if (messageInput.value.trim()) {
    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      type: 'user',
      message: messageInput.value,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    }
    chatMessages.value.push(userMessage)

    // Simulate AI response (replace with actual API call later)
    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        type: 'ai',
        message: 'I understand your question. Let me help you with that...',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }
      chatMessages.value.push(aiResponse)
    }, 1000)

    messageInput.value = ''
  }
}

const saveQuestion = () => {
  if (messageInput.value.trim()) {
    const newQuestion = {
      id: Date.now(),
      text: messageInput.value,
      timestamp: new Date().toLocaleDateString(),
    }
    savedQuestions.value.push(newQuestion)

    // Save to localStorage
    localStorage.setItem('savedQuestions', JSON.stringify(savedQuestions.value))

    // Optional: Clear input after saving
    // messageInput.value = ''
  }
}

const loadSavedQuestion = question => {
  messageInput.value = question.text
}

const deleteSavedQuestion = questionId => {
  savedQuestions.value = savedQuestions.value.filter(q => q.id !== questionId)
  localStorage.setItem('savedQuestions', JSON.stringify(savedQuestions.value))
}

// Load settings when component mounts
onMounted(() => {
  // Load saved questions from localStorage
  const saved = localStorage.getItem('savedQuestions')
  if (saved) {
    savedQuestions.value = JSON.parse(saved)
  }
})
</script>
