<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-gray-800/95 backdrop-blur-sm border-b border-gray-700">
    <div class="px-6 py-3">
      <div class="flex items-center justify-between">
        <!-- Left: Logo and Navigation -->
        <div class="flex items-center space-x-8">
          <!-- Logo -->
          <NuxtLink to="/dashboard" class="flex items-center space-x-2">
            <div class="flex h-8 w-8 items-center justify-center rounded bg-pink-500">
              <span class="text-sm text-white">✨</span>
            </div>
            <div>
              <h1 class="text-lg font-bold text-white">Vidalytics</h1>
            </div>
          </NuxtLink>

          <!-- Main Navigation -->
          <nav class="hidden md:flex items-center space-x-1">
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
            <div class="hidden sm:block text-right">
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
      <div v-if="showMobileMenu" class="md:hidden mt-4 pt-4 border-t border-gray-700">
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
    </div>
  </header>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

// Mobile menu state
const showMobileMenu = ref(false)

// Navigation items
const mainMenuItems = [
  { name: 'Dashboard', path: '/dashboard' },
  { name: 'Pillars', path: '/pillars' },
  { name: 'Videos', path: '/videos' },
  { name: 'Content Studio', path: '/content-studio' },
  { name: 'AI Assistant', path: '/ai-assistant' }
]

// User data (replace with actual user store)
const userName = computed(() => 'MARCELINE ANDERSON')
const userInitials = computed(() => 'MA')

// Time-based greeting
const timeOfDay = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good Morning'
  if (hour < 18) return 'Good Afternoon'
  return 'Good Evening'
})

// Mobile menu functions
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
}

// Close mobile menu when clicking outside
onMounted(() => {
  const handleClickOutside = (event) => {
    if (showMobileMenu.value && !event.target.closest('header')) {
      closeMobileMenu()
    }
  }
  
  document.addEventListener('click', handleClickOutside)
  
  onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
  })
})
</script>

<style scoped>
/* Backdrop blur fallback */
@supports not (backdrop-filter: blur(8px)) {
  header {
    background-color: rgba(31, 41, 55, 0.95);
  }
}
</style>
