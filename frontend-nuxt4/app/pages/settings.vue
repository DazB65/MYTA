<template>
  <div>
    <!-- Settings Content -->
    <div class="space-y-6 pt-32 px-6">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-white mb-2">Settings</h1>
        <p class="text-gray-400">Manage your account and application preferences</p>
      </div>

      <!-- Settings Content -->
      <div class="space-y-8">
        <!-- Agent Customization Section -->
        <div class="rounded-xl bg-forest-800 p-6">
          <div class="mb-6 flex items-center space-x-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-500">
              <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"
                />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-white">AI Agent Customization</h3>
              <p class="text-sm text-gray-400">Personalize your AI assistant experience</p>
            </div>
          </div>

          <div class="grid grid-cols-1 gap-8 lg:grid-cols-2">
            <!-- Agent Name -->
            <div>
              <label class="mb-2 block text-sm font-medium text-white">Agent Name</label>
              <input
                v-model="agentName"
                type="text"
                placeholder="Enter your agent's name"
                class="w-full rounded-lg border border-forest-600 bg-forest-700 px-4 py-3 text-white placeholder-gray-400 focus:border-orange-500 focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
              <p class="mt-1 text-xs text-gray-400">
                This name will appear in the agent modal header
              </p>
            </div>

            <!-- Agent Selection -->
            <div>
              <label class="mb-2 block text-sm font-medium text-white">Choose Your Agent</label>
              <div class="grid grid-cols-5 gap-3">
                <div
                  v-for="agent in agents"
                  :key="agent.id"
                  :class="[
                    'relative cursor-pointer rounded-lg border-2 p-4 transition-all hover:shadow-md',
                    selectedAgent === agent.id
                      ? 'border-orange-500 bg-orange-500/10'
                      : 'border-forest-600 hover:border-forest-500',
                  ]"
                  @click="selectedAgent = agent.id"
                >
                  <div class="text-center">
                    <div class="mx-auto mb-2 h-16 w-16 overflow-hidden rounded-full bg-forest-700">
                      <img
                        :src="agent.image"
                        :alt="agent.name"
                        class="h-full w-full object-cover"
                      />
                    </div>
                    <div class="text-xs font-medium text-white">{{ agent.name }}</div>
                    <div class="mt-1 text-xs text-gray-400">{{ agent.personality }}</div>
                  </div>

                  <!-- Selected indicator -->
                  <div
                    v-if="selectedAgent === agent.id"
                    class="absolute -right-2 -top-2 flex h-6 w-6 items-center justify-center rounded-full bg-orange-500"
                  >
                    <svg class="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </div>
                </div>
              </div>
              <p class="mt-2 text-xs text-gray-400">
                Select from 5 different AI agent personalities
              </p>
            </div>
          </div>

          <!-- Preview Section -->
          <div class="mt-8 rounded-lg bg-forest-700 p-4">
            <h4 class="mb-3 text-sm font-medium text-white">Preview</h4>
            <div class="flex items-center space-x-3">
              <div class="h-12 w-12 overflow-hidden rounded-lg bg-forest-600">
                <img
                  :src="selectedAgentData.image"
                  :alt="selectedAgentData.name"
                  class="h-full w-full object-cover"
                />
              </div>
              <div>
                <div class="text-xl font-bold text-white">
                  {{ agentName || 'Professional Assistant' }}
                </div>
                <div class="text-sm font-medium text-orange-400">MYTA</div>
              </div>
            </div>
          </div>

          <!-- Save Button -->
          <div class="mt-6 flex justify-end">
            <button
              class="rounded-lg bg-orange-500 px-6 py-3 font-medium text-white transition-colors hover:bg-orange-600"
              @click="saveSettings"
            >
              Save Changes
            </button>
          </div>
        </div>

        <!-- Other Settings Sections -->
        <div class="rounded-xl bg-forest-800 p-6">
          <div class="mb-6 flex items-center space-x-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-forest-700">
              <svg class="h-6 w-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-white">General Settings</h3>
              <p class="text-sm text-gray-400">Additional settings coming soon</p>
            </div>
          </div>

          <div class="py-8 text-center">
            <p class="mb-4 text-gray-400">More settings will be available in future updates</p>
            <button
              class="rounded-lg bg-forest-700 px-4 py-2 text-gray-300 transition-colors hover:bg-forest-600"
            >
              Request Features
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// Agent customization state
const agentName = ref('Professional Assistant')
const selectedAgent = ref(1)

// Available agents
const agents = ref([
  {
    id: 1,
    name: 'Agent 1',
    image: '/Agent1.png',
    color: 'bg-purple-600',
    description: 'AI Content Creator',
    personality: 'Professional & Analytical',
  },
  {
    id: 2,
    name: 'Agent 2',
    image: '/Agent2.png',
    color: 'bg-blue-600',
    description: 'Marketing Specialist',
    personality: 'Strategic & Data-Driven',
  },
  {
    id: 3,
    name: 'Agent 3',
    image: '/Agent3.png',
    color: 'bg-green-600',
    description: 'Analytics Expert',
    personality: 'Detail-Oriented & Insightful',
  },
  {
    id: 4,
    name: 'Agent 4',
    image: '/Agent4.png',
    color: 'bg-orange-600',
    description: 'Creative Assistant',
    personality: 'Innovative & Artistic',
  },
  {
    id: 5,
    name: 'Agent 5',
    image: '/Agent5.png',
    color: 'bg-pink-600',
    description: 'Strategy Advisor',
    personality: 'Visionary & Strategic',
  },
])

// Computed property for selected agent data
const selectedAgentData = computed(() => {
  return agents.value.find(agent => agent.id === selectedAgent.value) || agents.value[0]
})

// Save settings function
const saveSettings = () => {
  // Store settings in localStorage for now
  localStorage.setItem(
    'agentSettings',
    JSON.stringify({
      name: agentName.value,
      selectedAgent: selectedAgent.value,
    })
  )

  // Show success message (you could add a toast notification here)
  alert('Agent settings saved successfully!')
}

// Load settings on component mount
onMounted(() => {
  const savedSettings = localStorage.getItem('agentSettings')
  if (savedSettings) {
    const settings = JSON.parse(savedSettings)
    agentName.value = settings.name || 'Professional Assistant'
    selectedAgent.value = settings.selectedAgent || 1
  }
})
</script>
