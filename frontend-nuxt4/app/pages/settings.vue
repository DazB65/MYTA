<template>
  <div class="flex min-h-screen bg-gray-900 text-white">
    <!-- Left Sidebar Navigation -->
    <div class="fixed flex h-screen w-72 flex-col bg-gray-800">
      <!-- Logo Section -->
      <div class="p-6">
        <div class="flex items-center space-x-2">
          <div class="flex h-8 w-8 items-center justify-center rounded bg-pink-500">
            <span class="text-sm text-white">✨</span>
          </div>
          <h1 class="text-xl font-bold text-white">Vidalytics</h1>
        </div>
        <p class="mt-1 text-xs text-gray-400">Your AI Agent for Content and Growth</p>
      </div>

      <!-- Main Menu -->
      <div class="px-4">
        <h3 class="mb-4 text-sm font-medium text-gray-400">Main Menu</h3>
        <nav class="space-y-2">
          <NuxtLink
            to="/dashboard"
            class="flex items-center rounded-lg px-4 py-3 text-gray-300 transition-colors hover:bg-gray-700 hover:text-white"
          >
            <svg class="mr-3 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"
              />
            </svg>
            Dashboard
          </NuxtLink>
          <NuxtLink
            to="/pillars"
            class="flex items-center rounded-lg px-4 py-3 text-gray-300 transition-colors hover:bg-gray-700 hover:text-white"
          >
            <svg class="mr-3 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"
              />
            </svg>
            Pillars
          </NuxtLink>
          <NuxtLink
            to="/videos"
            class="flex items-center rounded-lg px-4 py-3 text-gray-300 transition-colors hover:bg-gray-700 hover:text-white"
          >
            <svg class="mr-3 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"
              />
            </svg>
            Videos
          </NuxtLink>
          <NuxtLink
            to="/content-studio"
            class="flex items-center rounded-lg px-4 py-3 text-gray-300 transition-colors hover:bg-gray-700 hover:text-white"
          >
            <svg class="mr-3 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"
              />
            </svg>
            Content Studio
          </NuxtLink>
          <NuxtLink
            to="/ai-assistant"
            class="flex items-center rounded-lg px-4 py-3 text-gray-300 transition-colors hover:bg-gray-700 hover:text-white"
          >
            <svg class="mr-3 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            AI Assistant
          </NuxtLink>
        </nav>
      </div>

      <!-- General Section -->
      <div class="mt-8 px-4">
        <h3 class="mb-4 text-sm font-medium text-gray-400">General</h3>
        <nav class="space-y-2">
          <NuxtLink
            to="/settings"
            class="flex items-center rounded-lg bg-pink-500 px-4 py-3 text-white"
          >
            <svg class="mr-3 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                clip-rule="evenodd"
              />
            </svg>
            Settings
          </NuxtLink>
        </nav>
      </div>

      <!-- User Profile Section -->
      <div class="mt-auto border-t border-gray-700 p-6">
        <div class="flex items-center space-x-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-full bg-pink-500">
            <span class="font-bold text-white">M</span>
          </div>
          <div class="flex-1">
            <p class="text-sm text-white">Good Morning</p>
            <p class="text-sm font-bold text-white">MARCELINE ANDERSON!</p>
            <p class="text-xs text-gray-400">Manage your preferences</p>
          </div>
        </div>
        <div class="mt-4 flex items-center justify-between">
          <div class="text-xs text-gray-400">📅 23 July, 2026</div>
          <button class="text-gray-400 hover:text-white">
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
        <button class="mt-2 flex items-center text-sm text-gray-400 hover:text-white">
          <svg class="mr-1 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
              clip-rule="evenodd"
            />
          </svg>
          Log Out
        </button>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="ml-72 flex-1 overflow-y-auto bg-gray-100 p-8">
      <!-- Header -->
      <div class="mb-8 flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">Settings</h2>
          <p class="text-gray-500">Manage your account and application preferences</p>
        </div>
      </div>

      <!-- Settings Content -->
      <div class="space-y-8">
        <!-- Agent Customization Section -->
        <div class="rounded-xl bg-white p-6 shadow-sm">
          <div class="mb-6 flex items-center space-x-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-100">
              <svg class="h-6 w-6 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"
                />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">AI Agent Customization</h3>
              <p class="text-sm text-gray-500">Personalize your AI assistant experience</p>
            </div>
          </div>

          <div class="grid grid-cols-1 gap-8 lg:grid-cols-2">
            <!-- Agent Name -->
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700">Agent Name</label>
              <input
                v-model="agentName"
                type="text"
                placeholder="Enter your agent's name"
                class="w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
              <p class="mt-1 text-xs text-gray-500">
                This name will appear in the agent modal header
              </p>
            </div>

            <!-- Agent Selection -->
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700">Choose Your Agent</label>
              <div class="grid grid-cols-5 gap-3">
                <div
                  v-for="agent in agents"
                  :key="agent.id"
                  :class="[
                    'relative cursor-pointer rounded-lg border-2 p-4 transition-all hover:shadow-md',
                    selectedAgent === agent.id
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-gray-300',
                  ]"
                  @click="selectedAgent = agent.id"
                >
                  <div class="text-center">
                    <div class="mx-auto mb-2 h-16 w-16 overflow-hidden rounded-full bg-gray-100">
                      <img
                        :src="agent.image"
                        :alt="agent.name"
                        class="h-full w-full object-cover"
                      />
                    </div>
                    <div class="text-xs font-medium text-gray-700">{{ agent.name }}</div>
                    <div class="mt-1 text-xs text-gray-500">{{ agent.personality }}</div>
                  </div>

                  <!-- Selected indicator -->
                  <div
                    v-if="selectedAgent === agent.id"
                    class="absolute -right-2 -top-2 flex h-6 w-6 items-center justify-center rounded-full bg-purple-500"
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
              <p class="mt-2 text-xs text-gray-500">
                Select from 5 different AI agent personalities
              </p>
            </div>
          </div>

          <!-- Preview Section -->
          <div class="mt-8 rounded-lg bg-gray-50 p-4">
            <h4 class="mb-3 text-sm font-medium text-gray-700">Preview</h4>
            <div class="flex items-center space-x-3">
              <div class="h-12 w-12 overflow-hidden rounded-lg bg-gray-100">
                <img
                  :src="selectedAgentData.image"
                  :alt="selectedAgentData.name"
                  class="h-full w-full object-cover"
                />
              </div>
              <div>
                <div class="text-xl font-bold text-gray-900">
                  {{ agentName || 'Professional Assistant' }}
                </div>
                <div class="text-sm font-medium text-gray-900">MY YT Agent</div>
              </div>
            </div>
          </div>

          <!-- Save Button -->
          <div class="mt-6 flex justify-end">
            <button
              class="rounded-lg bg-purple-600 px-6 py-3 font-medium text-white transition-colors hover:bg-purple-700"
              @click="saveSettings"
            >
              Save Changes
            </button>
          </div>
        </div>

        <!-- Other Settings Sections -->
        <div class="rounded-xl bg-white p-6 shadow-sm">
          <div class="mb-6 flex items-center space-x-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-gray-100">
              <svg class="h-6 w-6 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">General Settings</h3>
              <p class="text-sm text-gray-500">Additional settings coming soon</p>
            </div>
          </div>

          <div class="py-8 text-center">
            <p class="mb-4 text-gray-500">More settings will be available in future updates</p>
            <button
              class="rounded-lg bg-gray-100 px-4 py-2 text-gray-600 transition-colors hover:bg-gray-200"
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
