<template>
  <div class="bg-gray-800 rounded-xl p-6">


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
