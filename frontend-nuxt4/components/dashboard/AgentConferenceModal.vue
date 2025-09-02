<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
    @click="closeModal"
  >
    <div
      class="bg-forest-800 rounded-xl max-w-4xl w-full max-h-[90vh] overflow-hidden"
      @click.stop
    >
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-forest-600">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center">
            <span class="text-purple-400 text-lg">🎯</span>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-white">Agent Conference</h2>
            <p class="text-gray-400 text-sm">Strategic discussion with your AI team</p>
          </div>
        </div>
        <button
          @click="closeModal"
          class="w-8 h-8 rounded-lg bg-forest-700 hover:bg-forest-600 flex items-center justify-center text-gray-400 hover:text-white transition-colors"
        >
          ✕
        </button>
      </div>

      <!-- Conference Content -->
      <div class="flex h-[600px]">
        <!-- Participants Panel -->
        <div class="w-80 bg-forest-900 p-4 border-r border-forest-600">
          <h3 class="text-lg font-medium text-white mb-4">Conference Participants</h3>
          
          <!-- Boss Agent (Moderator) -->
          <div class="mb-4 p-3 rounded-lg bg-orange-500/10 border border-orange-500/20">
            <div class="flex items-center space-x-3">
              <img 
                src="/BossAgent.png" 
                alt="Boss Agent"
                class="w-10 h-10 rounded-lg object-cover"
              />
              <div class="flex-1">
                <div class="text-white font-medium">Boss Agent</div>
                <div class="text-orange-400 text-xs">Conference Moderator</div>
              </div>
              <div class="w-2 h-2 rounded-full bg-green-400"></div>
            </div>
          </div>

          <!-- Team Members -->
          <div class="space-y-3">
            <div
              v-for="agent in conferenceAgents"
              :key="agent.id"
              class="p-3 rounded-lg bg-forest-700 hover:bg-forest-600 transition-colors cursor-pointer"
              :class="{ 'ring-2 ring-blue-500': agent.id === selectedAgent?.id }"
              @click="selectAgent(agent)"
            >
              <div class="flex items-center space-x-3">
                <img 
                  :src="agent.avatar" 
                  :alt="agent.name"
                  class="w-8 h-8 rounded-lg object-cover"
                />
                <div class="flex-1">
                  <div class="text-white text-sm font-medium">{{ agent.name }}</div>
                  <div class="text-gray-400 text-xs">{{ agent.specialization }}</div>
                </div>
                <div 
                  :class="[
                    'w-2 h-2 rounded-full',
                    agent.isActive ? 'bg-green-400' : 'bg-gray-400'
                  ]"
                ></div>
              </div>
              
              <!-- Agent's Current Focus -->
              <div class="mt-2 text-xs text-gray-300">
                Focus: {{ agent.currentFocus }}
              </div>
            </div>
          </div>

          <!-- Conference Controls -->
          <div class="mt-6 space-y-3">
            <button
              @click="startNewTopic"
              class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
            >
              Start New Topic
            </button>
            <button
              @click="generateSummary"
              class="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium"
            >
              Generate Summary
            </button>
          </div>
        </div>

        <!-- Discussion Area -->
        <div class="flex-1 flex flex-col">
          <!-- Current Topic -->
          <div class="p-4 bg-forest-700 border-b border-forest-600">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="text-white font-medium">{{ currentTopic.title }}</h4>
                <p class="text-gray-400 text-sm">{{ currentTopic.description }}</p>
              </div>
              <span class="text-xs px-2 py-1 rounded-full bg-blue-500/20 text-blue-300">
                {{ currentTopic.status }}
              </span>
            </div>
          </div>

          <!-- Discussion Messages -->
          <div class="flex-1 overflow-y-auto p-4 space-y-4">
            <div
              v-for="message in discussionMessages"
              :key="message.id"
              class="flex space-x-3"
            >
              <img 
                :src="message.agent.avatar" 
                :alt="message.agent.name"
                class="w-8 h-8 rounded-lg object-cover flex-shrink-0"
              />
              <div class="flex-1">
                <div class="flex items-center space-x-2 mb-1">
                  <span class="text-white text-sm font-medium">{{ message.agent.name }}</span>
                  <span class="text-xs text-gray-400">{{ message.timestamp }}</span>
                  <span 
                    v-if="message.type"
                    class="text-xs px-2 py-1 rounded-full"
                    :class="getMessageTypeClass(message.type)"
                  >
                    {{ message.type }}
                  </span>
                </div>
                <div class="text-gray-300 text-sm">{{ message.content }}</div>
                
                <!-- Message Actions -->
                <div v-if="message.actions" class="mt-2 flex space-x-2">
                  <button
                    v-for="action in message.actions"
                    :key="action.id"
                    @click="executeAction(action)"
                    class="text-xs px-3 py-1 rounded-lg bg-blue-500/20 text-blue-300 hover:bg-blue-500/30 transition-colors"
                  >
                    {{ action.label }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Typing Indicators -->
            <div
              v-for="agent in typingAgents"
              :key="`typing-${agent.id}`"
              class="flex space-x-3"
            >
              <img 
                :src="agent.avatar" 
                :alt="agent.name"
                class="w-8 h-8 rounded-lg object-cover flex-shrink-0"
              />
              <div class="flex-1">
                <div class="text-white text-sm font-medium">{{ agent.name }}</div>
                <div class="text-gray-400 text-sm flex items-center space-x-1">
                  <span>is thinking</span>
                  <div class="flex space-x-1">
                    <div class="w-1 h-1 bg-gray-400 rounded-full animate-bounce"></div>
                    <div class="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                    <div class="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Input Area -->
          <div class="p-4 border-t border-forest-600">
            <div class="flex space-x-3">
              <input
                v-model="userInput"
                @keyup.enter="sendMessage"
                type="text"
                placeholder="Ask your team a question or start a discussion..."
                class="flex-1 px-4 py-2 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
              />
              <button
                @click="sendMessage"
                :disabled="!userInput.trim()"
                class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAgentsStore } from '../../stores/agents'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const agentsStore = useAgentsStore()
const selectedAgent = ref(null)
const userInput = ref('')

// Conference participants (excluding Boss Agent)
const conferenceAgents = computed(() => 
  agentsStore.allAgents.filter(agent => agent.id !== 'boss_agent').map(agent => ({
    ...agent,
    isActive: true,
    currentFocus: ['Content Strategy', 'Audience Analysis', 'Performance Optimization', 'Technical Review', 'Growth Planning'][Math.floor(Math.random() * 5)]
  }))
)

// Current discussion topic
const currentTopic = ref({
  title: 'Q1 Content Strategy Planning',
  description: 'Collaborative planning for upcoming content series and optimization strategies',
  status: 'Active Discussion'
})

// Discussion messages
const discussionMessages = ref([
  {
    id: 1,
    agent: { name: 'Boss Agent', avatar: '/BossAgent.png' },
    content: 'Team, let\'s discuss our Q1 content strategy. I\'d like each of you to share your insights on how we can improve our approach.',
    timestamp: '2 min ago',
    type: 'Moderator'
  },
  {
    id: 2,
    agent: { name: 'Alex', avatar: '/optimized/Agent1.jpg' },
    content: 'Based on our analytics, videos with educational content perform 34% better. I recommend focusing on tutorial-style content for Q1.',
    timestamp: '1 min ago',
    type: 'Analysis',
    actions: [
      { id: 'view-data', label: 'View Data' },
      { id: 'create-plan', label: 'Create Plan' }
    ]
  },
  {
    id: 3,
    agent: { name: 'Levi', avatar: '/optimized/Agent2.jpg' },
    content: 'I agree with Alex. I can create engaging thumbnails and titles that emphasize the educational value while maintaining creative appeal.',
    timestamp: '30 sec ago',
    type: 'Creative'
  }
])

// Agents currently typing
const typingAgents = ref([
  { id: 'agent_3', name: 'Maya', avatar: '/optimized/Agent3.jpg' }
])

// Methods
const closeModal = () => {
  emit('close')
}

const selectAgent = (agent) => {
  selectedAgent.value = agent
}

const startNewTopic = () => {
  console.log('Starting new topic')
  // TODO: Implement new topic creation
}

const generateSummary = () => {
  console.log('Generating conference summary')
  // TODO: Implement summary generation
}

const sendMessage = () => {
  if (!userInput.value.trim()) return
  
  // Add user message
  discussionMessages.value.push({
    id: Date.now(),
    agent: { name: 'You', avatar: '/user-avatar.png' },
    content: userInput.value,
    timestamp: 'now',
    type: 'User'
  })
  
  userInput.value = ''
  
  // Simulate agent responses
  setTimeout(() => {
    // Remove typing indicator
    typingAgents.value = []
    
    // Add agent response
    discussionMessages.value.push({
      id: Date.now() + 1,
      agent: { name: 'Boss Agent', avatar: '/BossAgent.png' },
      content: 'Great question! Let me coordinate with the team to provide you with comprehensive insights.',
      timestamp: 'now',
      type: 'Coordination'
    })
  }, 2000)
}

const executeAction = (action) => {
  console.log('Executing action:', action.label)
  // TODO: Implement action execution
}

const getMessageTypeClass = (type) => {
  const classes = {
    'Moderator': 'bg-orange-500/20 text-orange-300',
    'Analysis': 'bg-blue-500/20 text-blue-300',
    'Creative': 'bg-purple-500/20 text-purple-300',
    'User': 'bg-green-500/20 text-green-300',
    'Coordination': 'bg-yellow-500/20 text-yellow-300'
  }
  return classes[type] || 'bg-gray-500/20 text-gray-300'
}
</script>
