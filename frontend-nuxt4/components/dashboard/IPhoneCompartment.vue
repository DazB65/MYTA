<template>
  <div class="bg-gray-800 rounded-xl p-6">
    <!-- Action Buttons -->
    <div class="flex items-center justify-between mb-6">
      <!-- Connect YouTube Button -->
      <button
        @click="showConnectModal = true"
        class="flex items-center space-x-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
      >
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v1a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 4a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path>
        </svg>
        <span>Connect YouTube</span>
      </button>

      <!-- Agent Button -->
      <button
        @click="showAgentModal = true"
        class="flex items-center space-x-2 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors"
      >
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
        </svg>
        <span>Agent</span>
      </button>
    </div>

    <!-- YouTube Banner Preview - Exact format like your image -->
    <div class="bg-gradient-to-r from-orange-400 via-pink-500 to-purple-600 rounded-xl h-32 relative overflow-hidden flex items-center justify-between px-8">
      <!-- Left side content -->
      <div class="flex items-center space-x-4">
        <div class="text-white">
          <div class="text-2xl font-bold">iPhone 15 Pro</div>
          <div class="text-lg opacity-90">Hello, Apple Intelligence</div>
        </div>
      </div>

      <!-- Right side - PRO text with glow effect -->
      <div class="text-right">
        <div class="text-6xl font-bold text-white tracking-wider" style="text-shadow: 0 0 20px rgba(255,255,255,0.5);">
          PRO
        </div>
      </div>

      <!-- Decorative glow effects -->
      <div class="absolute top-0 right-0 w-32 h-32 bg-white bg-opacity-10 rounded-full blur-xl -mr-16 -mt-16"></div>
      <div class="absolute bottom-0 left-0 w-24 h-24 bg-white bg-opacity-10 rounded-full blur-lg -ml-12 -mb-12"></div>
    </div>



    <!-- YouTube Connect Modal -->
    <YouTubeConnectModal
      v-if="showConnectModal"
      @close="showConnectModal = false"
      @connect="handleYouTubeConnect"
    />

    <!-- Agent Modal -->
    <AgentModal
      :isOpen="showAgentModal"
      @close="showAgentModal = false"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import YouTubeConnectModal from '../modals/YouTubeConnectModal.vue'
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
