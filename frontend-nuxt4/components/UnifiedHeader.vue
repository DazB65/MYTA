<template>
  <header class="fixed top-0 left-0 right-0 z-50">
    <div class="p-6">
      <!-- Header Container -->
      <div class="rounded-xl bg-gray-800 p-4">
      <!-- Top Navigation Bar -->
      <div class="flex items-center justify-between mb-3 h-12">
        <!-- Left: Logo -->
        <div class="flex items-center overflow-visible -ml-8">
          <NuxtLink to="/dashboard" class="flex items-center">
            <img
              src="/MY YT AGENT.png"
              alt="MY YT AGENT"
              class="h-72 w-72 rounded mt-8"
            />
          </NuxtLink>
        </div>

        <!-- Right: User Profile and Actions -->
        <div class="flex items-center space-x-4">
          <!-- Settings -->
          <NuxtLink
            to="/settings"
            class="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-700 transition-colors"
            title="Settings"
          >
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                clip-rule="evenodd"
              />
            </svg>
          </NuxtLink>

          <!-- User Profile -->
          <div class="flex items-center space-x-3">
            <div class="text-right">
              <p class="text-sm text-white font-medium">{{ userName }}</p>
              <p class="text-xs text-gray-400">{{ timeOfDay }}</p>
            </div>
            <div class="flex h-8 w-8 items-center justify-center rounded-full bg-pink-500">
              <span class="text-sm font-bold text-white">{{ userInitials }}</span>
            </div>
          </div>

          <!-- Mobile Menu Button -->
          <button
            @click="toggleMobileMenu"
            class="md:hidden p-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-700 transition-colors"
          >
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Navigation Menu -->
      <div v-if="showMobileMenu" class="md:hidden mb-4 pt-4 border-t border-gray-700">
        <nav class="space-y-2">
          <NuxtLink
            v-for="item in mainMenuItems"
            :key="item.path"
            :to="item.path"
            @click="closeMobileMenu"
            class="block px-3 py-2 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition-colors"
            active-class="bg-pink-500 text-white hover:bg-pink-600"
          >
            {{ item.name }}
          </NuxtLink>
        </nav>
      </div>

      <!-- iPhone Compartment Section -->
        <!-- Action Buttons with Navigation -->
        <div class="mb-4 flex items-center justify-between">
          <!-- Left spacer -->
          <div class="flex-1"></div>

          <!-- Center: Main Navigation -->
          <nav class="flex items-center space-x-1">
            <NuxtLink
              v-for="item in mainMenuItems"
              :key="item.path"
              :to="item.path"
              class="px-3 py-2 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition-colors"
              active-class="bg-pink-500 text-white hover:bg-pink-600"
            >
              {{ item.name }}
            </NuxtLink>
          </nav>

          <!-- Right: Action Buttons -->
          <div class="flex-1 flex justify-end">
            <div class="flex items-center space-x-3">
              <!-- Connect YouTube Button -->
              <button
                class="flex items-center space-x-2 rounded-lg bg-red-600 px-4 py-2 text-white transition-colors hover:bg-red-700"
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
              </button>

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
          </div>
        </div>

        <!-- YouTube Banner Preview -->
        <div
          class="relative flex h-24 items-center justify-between overflow-hidden rounded-xl bg-gradient-to-r from-orange-400 via-pink-500 to-purple-600 px-6"
        >
          <!-- Left side content -->
          <div class="flex items-center space-x-4">
            <div class="text-white">
              <div class="text-xl font-bold">iPhone 15 Pro</div>
              <div class="text-sm opacity-90">Hello, Apple Intelligence</div>
            </div>
          </div>

          <!-- Right side - PRO text with glow effect -->
          <div class="text-right">
            <div
              class="text-4xl font-bold tracking-wider text-white"
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
      </div>
    </div>

    <!-- YouTube Connect Modal -->
    <YouTubeConnectModal
      v-if="showConnectModal"
      @close="showConnectModal = false"
      @connect="handleYouTubeConnect"
    />

    <!-- Agent Modal -->
    <AgentModal :is-open="showAgentModal" @close="showAgentModal = false" />
  </header>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import AgentModal from './dashboard/AgentModal.vue'
import YouTubeConnectModal from './modals/YouTubeConnectModal.vue'

// Mobile menu state
const showMobileMenu = ref(false)

// iPhone compartment state
const showConnectModal = ref(false)
const showAgentModal = ref(false)

// Navigation items
const mainMenuItems = [
  { name: 'Dashboard', path: '/dashboard' },
  { name: 'Tasks', path: '/tasks' },
  { name: 'Pillars', path: '/pillars' },
  { name: 'Videos', path: '/videos' },
  { name: 'Content Studio', path: '/content-studio' }
]

// User data
const userName = computed(() => 'MARCELINE ANDERSON')
const userInitials = computed(() => 'MA')

// Time-based greeting
const timeOfDay = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good Morning'
  if (hour < 17) return 'Good Afternoon'
  return 'Good Evening'
})

// Mobile menu functions
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
}

// iPhone compartment functions
const handleYouTubeConnect = () => {
  console.log('YouTube connected successfully!')
  showConnectModal.value = false
}

// Close mobile menu when clicking outside
const handleClickOutside = (event) => {
  if (showMobileMenu.value && !event.target.closest('header')) {
    showMobileMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
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
