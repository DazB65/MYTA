<template>
  <div class="bg-gray-800 rounded-xl p-6">
    <!-- Header with Connect YouTube Button -->
    <div class="flex items-center justify-end mb-6">
      <button
        @click="showConnectModal = true"
        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center space-x-2"
      >
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"></path>
        </svg>
        <span>Connect YouTube</span>
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
  </div>
</template>

<script setup>
import { ref } from 'vue'
import YouTubeConnectModal from '../modals/YouTubeConnectModal.vue'

// Component state
const showConnectModal = ref(false)

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
