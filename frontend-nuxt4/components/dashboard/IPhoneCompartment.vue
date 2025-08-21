<template>
  <div class="rounded-xl bg-gray-800 p-6">
    <!-- Action Buttons -->
    <div class="mb-6 flex items-center justify-between">
      <!-- Connect YouTube Button -->
      <LoadingButton
        button-class="flex items-center space-x-2 rounded-lg bg-red-600 px-4 py-2 text-white transition-colors hover:bg-red-700"
        @click="showConnectModal = true"
      >
        <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
          <path
            fill-rule="evenodd"
            d="M3 4a1 1 0 011-1h12a1 1 0 011 1v1a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 4a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1z"
            clip-rule="evenodd"
          />
        </svg>
        <span>Connect YouTube</span>
      </LoadingButton>

      <!-- Agent Button -->
      <button
        class="flex items-center space-x-2 rounded-lg bg-purple-600 px-4 py-2 text-white transition-colors hover:bg-purple-700"
        @click="showAgentModal = true"
      >
        <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
          <path
            d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"
          />
        </svg>
        <span>Agent</span>
      </button>
    </div>

    <!-- YouTube Banner Preview - Exact format like your image -->
    <div
      class="relative flex h-32 items-center justify-between overflow-hidden rounded-xl bg-gradient-to-r from-orange-400 via-pink-500 to-purple-600 px-8"
    >
      <!-- Left side content -->
      <div class="flex items-center space-x-4">
        <div class="text-white">
          <div class="text-2xl font-bold">iPhone 15 Pro</div>
          <div class="text-lg opacity-90">Hello, Apple Intelligence</div>
        </div>
      </div>

      <!-- Right side - PRO text with glow effect -->
      <div class="text-right">
        <div
          class="text-6xl font-bold tracking-wider text-white"
          style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.5)"
        >
          PRO
        </div>
      </div>

      <!-- Decorative glow effects -->
      <div
        class="absolute right-0 top-0 -mr-16 -mt-16 h-32 w-32 rounded-full bg-white bg-opacity-10 blur-xl"
      />
      <div
        class="absolute bottom-0 left-0 -mb-12 -ml-12 h-24 w-24 rounded-full bg-white bg-opacity-10 blur-lg"
      />
    </div>

    <!-- YouTube Connect Modal -->
    <YouTubeConnectModal
      v-if="showConnectModal"
      @close="showConnectModal = false"
      @connect="handleYouTubeConnect"
    />

    <!-- Agent Modal -->
    <AgentModal :is-open="showAgentModal" @close="showAgentModal = false" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import YouTubeConnectModal from '../modals/YouTubeConnectModal.vue'
import LoadingButton from '../ui/LoadingButton.vue'
import AgentModal from './AgentModal.vue'

// Component state
const showConnectModal = ref(false)
const showAgentModal = ref(false)

// Event handlers
const handleYouTubeConnect = () => {
  console.log('YouTube connected successfully!')
  // Handle YouTube connection logic here
}
</script>

<style scoped>
/* Additional custom styles if needed */
.gradient-border {
  background: linear-gradient(45deg, #3b82f6, #8b5cf6, #ef4444);
  padding: 2px;
  border-radius: 1rem;
}

.gradient-border > div {
  background: #1f2937;
  border-radius: calc(1rem - 2px);
}
</style>
