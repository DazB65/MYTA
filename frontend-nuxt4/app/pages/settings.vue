<template>
  <div class="min-h-screen bg-forest-900 text-white">
    <!-- Settings Content -->
    <div class="p-6 pt-24">
      <!-- Page Header -->
      <div class="mb-4 flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <h1 class="text-2xl font-bold text-white">Settings</h1>
          <span class="text-gray-400">•</span>
          <p class="text-gray-400">Manage your account and application preferences</p>
        </div>
        <div class="flex items-center space-x-4">
          <!-- Future: Add settings actions here -->
        </div>
      </div>

      <!-- Settings Content -->
      <div>
        <!-- Agent Customization Section -->
        <div class="mb-6 rounded-xl bg-forest-800 p-6">
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
                  class="relative cursor-pointer rounded-lg border-2 p-4 transition-all hover:shadow-md"
                  :class="selectedAgentId === agent.id ? '' : 'border-forest-600 hover:border-forest-500'"
                  :style="selectedAgentId === agent.id ? {
                    borderColor: agent.color,
                    backgroundColor: agent.color + '20'
                  } : {}"
                  @click="setSelectedAgent(agent.id)"
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
                    v-if="selectedAgentId === agent.id"
                    class="absolute -right-2 -top-2 flex h-6 w-6 items-center justify-center rounded-full"
                    :style="{ backgroundColor: agent.color }"
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
                  :src="selectedAgent.image"
                  :alt="selectedAgent.name"
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
              class="rounded-lg px-6 py-3 font-medium text-white transition-colors hover:opacity-90"
              :style="{ backgroundColor: selectedAgent.color }"
              @click="handleSaveSettings"
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
import { useAgentSettings } from '../../composables/useAgentSettings'

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// Agent settings
const { agentName, selectedAgentId, selectedAgent, allAgents, setSelectedAgent, setAgentName, saveSettings } = useAgentSettings()

// Use agents from composable
const agents = allAgents

// Toast notifications
const { success, error } = useToast()

// Save settings function
const handleSaveSettings = () => {
  try {
    saveSettings()
    success('Settings Saved', 'Your agent settings have been saved successfully!')
  } catch (err) {
    error('Save Failed', 'Failed to save your settings. Please try again.')
  }
}
</script>
