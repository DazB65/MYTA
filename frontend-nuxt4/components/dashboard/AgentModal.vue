<template>
  <div v-if="isOpen" class="fixed inset-0 z-50">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black bg-opacity-50" @click="closeModal"></div>

    <!-- Modal positioned below iPhone compartment -->
    <div class="absolute bg-gray-800 rounded-2xl shadow-2xl overflow-hidden"
         style="top: 280px; left: 312px; right: 24px; height: calc(100vh - 300px);">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 bg-gradient-to-r from-orange-400 via-pink-500 to-purple-600">
        <div class="flex items-center space-x-4">
          <div class="w-20 h-20 rounded-xl overflow-hidden">
            <img
              :src="agentData.image"
              :alt="agentData.name"
              class="w-full h-full object-cover bg-white rounded-xl"
            />
          </div>
          <div>
            <h2 class="text-3xl font-bold text-white">{{ agentData.name }}</h2>
            <p class="text-base font-medium text-white">MY YT Agent</p>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <button class="w-10 h-10 bg-pink-500 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
            </svg>
          </button>
          <button @click="openSettings" class="w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center hover:bg-gray-600">
            <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"></path>
            </svg>
          </button>
          <button @click="closeModal" class="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center hover:bg-gray-600">
            <svg class="w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>
      </div>

      <!-- Content -->
      <div class="flex h-full">
        <!-- Tabs -->
        <div class="w-64 bg-gray-900 p-4 border-r border-gray-700">
          <div class="space-y-2">
            <button
              @click="activeTab = 'chats'"
              :class="[
                'w-full text-left px-4 py-3 rounded-lg font-medium transition-colors',
                activeTab === 'chats' ? 'bg-pink-500 text-white' : 'text-gray-400 hover:bg-gray-800'
              ]"
            >
              Chats
            </button>
            <button
              @click="activeTab = 'visualizer'"
              :class="[
                'w-full text-left px-4 py-3 rounded-lg font-medium transition-colors',
                activeTab === 'visualizer' ? 'bg-pink-500 text-white' : 'text-gray-400 hover:bg-gray-800'
              ]"
            >
              Visualizer View
            </button>
          </div>

          <!-- Topic Tags -->
          <div class="mt-6">
            <div class="flex flex-wrap gap-2">
              <span class="px-3 py-1 bg-pink-600 text-pink-100 rounded-full text-sm">Trending Topics</span>
              <span class="px-3 py-1 bg-blue-600 text-blue-100 rounded-full text-sm">Competitor Analysis</span>
              <span class="px-3 py-1 bg-green-600 text-green-100 rounded-full text-sm">Channel Insights</span>
            </div>
          </div>
        </div>

        <!-- Chat Area -->
        <div class="flex-1 flex flex-col bg-gray-800">
          <!-- Chat Messages -->
          <div class="flex-1 p-6 overflow-y-auto">
            <div class="space-y-4">
              <!-- AI Message -->
              <div class="flex items-start space-x-3">
                <div class="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-white text-sm font-bold">AI</span>
                </div>
                <div class="flex-1">
                  <div class="bg-gray-700 rounded-lg p-3">
                    <p class="text-gray-300 text-sm">
                      <span class="font-medium text-white">AI Assistant</span>
                      <span class="text-gray-500 text-xs ml-2">10:30 AM</span>
                    </p>
                    <p class="text-gray-300 mt-1">Hello! I'm your AI content creation assistant. How can I help you today?</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Input Area -->
          <div class="p-6 border-t border-gray-700">
            <div class="flex items-center space-x-3">
              <input
                v-model="messageInput"
                type="text"
                placeholder="Type Something..."
                class="flex-1 px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                @keyup.enter="sendMessage"
              />
              <button
                @click="sendMessage"
                class="px-6 py-3 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors font-medium"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Settings Panel -->
      <div v-if="showSettings" class="absolute inset-y-0 right-0 w-96 bg-gray-800 border-l border-gray-700 transform transition-transform duration-300 ease-in-out">
        <!-- Settings Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-700">
          <h3 class="text-lg font-semibold text-white">Agent Settings</h3>
          <button @click="closeSettings" class="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center hover:bg-gray-600">
            <svg class="w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>

        <!-- Settings Content -->
        <div class="p-6 space-y-6 overflow-y-auto" style="height: calc(100% - 80px);">
          <!-- Agent Name -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Agent Name</label>
            <input
              v-model="tempSettings.name"
              type="text"
              placeholder="Enter your agent's name"
              class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>

          <!-- Agent Selection -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-3">Choose Your Agent</label>
            <div class="grid grid-cols-2 gap-3">
              <div
                v-for="agent in agents"
                :key="agent.id"
                @click="tempSettings.selectedAgent = agent.id"
                :class="[
                  'relative p-3 border-2 rounded-lg cursor-pointer transition-all hover:shadow-md',
                  tempSettings.selectedAgent === agent.id
                    ? 'border-purple-500 bg-purple-900/30'
                    : 'border-gray-600 hover:border-gray-500'
                ]"
              >
                <div class="text-center">
                  <div class="w-12 h-12 rounded-lg overflow-hidden mx-auto mb-2 bg-gray-100">
                    <img
                      :src="agent.image"
                      :alt="agent.name"
                      class="w-full h-full object-cover"
                    />
                  </div>
                  <div class="text-xs font-medium text-gray-300">{{ agent.name }}</div>
                </div>

                <!-- Selected indicator -->
                <div v-if="tempSettings.selectedAgent === agent.id"
                     class="absolute -top-2 -right-2 w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center">
                  <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                  </svg>
                </div>
              </div>
            </div>
          </div>

          <!-- Preview -->
          <div class="p-4 bg-gray-700 rounded-lg">
            <h4 class="text-sm font-medium text-gray-300 mb-3">Preview</h4>
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 rounded-lg overflow-hidden bg-gray-100">
                <img
                  :src="selectedTempAgentData.image"
                  :alt="selectedTempAgentData.name"
                  class="w-full h-full object-cover"
                />
              </div>
              <div>
                <div class="text-sm font-bold text-white">{{ tempSettings.name || 'Professional Assistant' }}</div>
                <div class="text-xs font-medium text-white">MY YT Agent</div>
              </div>
            </div>
          </div>

          <!-- Save Button -->
          <div class="flex justify-end space-x-3">
            <button
              @click="closeSettings"
              class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-500 transition-colors"
            >
              Cancel
            </button>
            <button
              @click="saveAgentSettings"
              class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
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

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const activeTab = ref('chats')
const messageInput = ref('')
const showSettings = ref(false)
const agentSettings = ref({
  name: 'Professional Assistant',
  selectedAgent: 1
})
const tempSettings = ref({
  name: 'Professional Assistant',
  selectedAgent: 1
})

// Available agents (same as in settings)
const agents = [
  {
    id: 1,
    name: 'Agent 1',
    image: '/Agent1.png',
    color: 'bg-purple-600',
    description: 'AI Content Creator',
    personality: 'Professional & Analytical'
  },
  {
    id: 2,
    name: 'Agent 2',
    image: '/Agent2.png',
    color: 'bg-blue-600',
    description: 'Marketing Specialist',
    personality: 'Strategic & Data-Driven'
  },
  {
    id: 3,
    name: 'Agent 3',
    image: '/Agent3.png',
    color: 'bg-green-600',
    description: 'Analytics Expert',
    personality: 'Detail-Oriented & Insightful'
  },
  {
    id: 4,
    name: 'Agent 4',
    image: '/Agent4.png',
    color: 'bg-orange-600',
    description: 'Creative Assistant',
    personality: 'Innovative & Artistic'
  },
  {
    id: 5,
    name: 'Agent 5',
    image: '/Agent5.png',
    color: 'bg-pink-600',
    description: 'Strategy Advisor',
    personality: 'Visionary & Strategic'
  }
]

// Computed property for current agent data
const agentData = computed(() => {
  const selectedAgentData = agents.find(agent => agent.id === agentSettings.value.selectedAgent) || agents[0]
  return {
    ...selectedAgentData,
    name: agentSettings.value.name || selectedAgentData.name
  }
})

// Computed property for temp settings preview
const selectedTempAgentData = computed(() => {
  return agents.find(agent => agent.id === tempSettings.value.selectedAgent) || agents[0]
})

// Load agent settings
const loadAgentSettings = () => {
  const savedSettings = localStorage.getItem('agentSettings')
  if (savedSettings) {
    agentSettings.value = JSON.parse(savedSettings)
  }
}

const openSettings = () => {
  // Copy current settings to temp settings
  tempSettings.value = { ...agentSettings.value }
  showSettings.value = true
}

const closeSettings = () => {
  showSettings.value = false
}

const saveAgentSettings = () => {
  // Update main settings
  agentSettings.value = { ...tempSettings.value }

  // Save to localStorage
  localStorage.setItem('agentSettings', JSON.stringify(agentSettings.value))

  // Close settings panel
  showSettings.value = false

  // Optional: Show success message
  console.log('Agent settings saved!')
}

const closeModal = () => {
  showSettings.value = false
  emit('close')
}

const sendMessage = () => {
  if (messageInput.value.trim()) {
    // Handle message sending logic here
    console.log('Sending message:', messageInput.value)
    messageInput.value = ''
  }
}

// Load settings when component mounts
onMounted(() => {
  loadAgentSettings()
})

// Watch for settings changes (in case user updates settings in another tab)
if (typeof window !== 'undefined') {
  window.addEventListener('storage', loadAgentSettings)
}
</script>
