<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-sm border-b border-gray-600">
    <div class="px-6 py-3">
      <div class="flex items-center justify-between">
        <!-- Left: Logo and Navigation -->
        <div class="flex items-center space-x-8">
          <!-- Logo -->
          <NuxtLink to="/dashboard" class="flex items-center space-x-2">
            <div class="flex h-8 w-8 items-center justify-center rounded bg-orange-500">
              <span class="text-sm text-white">✨</span>
            </div>
            <div>
              <h1 class="text-lg font-bold text-white">MYTA</h1>
            </div>
          </NuxtLink>

          <!-- Main Navigation -->
          <nav class="hidden md:flex items-center space-x-1">
            <NuxtLink
              v-for="item in mainMenuItems"
              :key="item.path"
              :to="item.path"
              class="px-3 py-2 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:bg-forest-700 transition-colors"
              active-class="bg-orange-500 text-white hover:bg-orange-600"
            >
              {{ item.name }}
            </NuxtLink>
          </nav>
        </div>

        <!-- Right: User Profile and Actions -->
        <div class="flex items-center space-x-4">
          <!-- Smart Notifications -->
          <div class="relative">
            <button
              @click="toggleNotifications"
              class="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-forest-700 transition-colors relative"
              title="Smart Notifications"
            >
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/>
              </svg>
              <!-- Notification Badge -->
              <span
                v-if="urgentNotificationsCount > 0"
                class="absolute -top-1 -right-1 inline-flex items-center justify-center px-1.5 py-0.5 text-xs font-bold leading-none text-white bg-red-500 rounded-full"
              >
                {{ urgentNotificationsCount > 9 ? '9+' : urgentNotificationsCount }}
              </span>
            </button>

            <!-- Notifications Dropdown -->
            <div
              v-if="showNotifications"
              class="absolute right-0 mt-2 w-96 bg-gray-800 rounded-xl shadow-lg border border-gray-600 z-50"
              @click.stop
            >
              <div class="p-4 border-b border-gray-700">
                <div class="flex items-center justify-between">
                  <h3 class="text-lg font-semibold text-white">Smart Notifications</h3>
                  <button
                    @click="showNotifications = false"
                    class="text-gray-400 hover:text-white"
                  >
                    <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                    </svg>
                  </button>
                </div>
              </div>
              <div class="max-h-96 overflow-y-auto">
                <SmartNotifications @openSettings="openNotificationSettings" />
              </div>
            </div>
          </div>

          <!-- Settings -->
          <NuxtLink
            to="/settings"
            class="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-forest-700 transition-colors"
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
            <div class="flex h-8 w-8 items-center justify-center rounded-full bg-orange-500">
              <span class="text-sm font-bold text-white">{{ userInitials }}</span>
            </div>
          </div>

          <!-- Mobile Menu Button -->
          <button
            @click="toggleMobileMenu"
            class="md:hidden p-2 rounded-lg text-gray-400 hover:text-white hover:bg-forest-700 transition-colors"
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
      <div v-if="showMobileMenu" class="md:hidden mt-4 pt-4 border-t border-forest-700">
        <nav class="space-y-2">
          <NuxtLink
            v-for="item in mainMenuItems"
            :key="item.path"
            :to="item.path"
            @click="closeMobileMenu"
            class="block px-3 py-2 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:bg-forest-700 transition-colors"
            active-class="bg-orange-500 text-white hover:bg-orange-600"
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
import { useRouter } from 'vue-router'
import { useAutomation } from '../composables/useAutomation'
import SmartNotifications from './automation/SmartNotifications.vue'

// Mobile menu state
const showMobileMenu = ref(false)

// Notifications state
const showNotifications = ref(false)
const router = useRouter()

// Automation composable
const { urgentNotifications, getNotifications } = useAutomation()

// Computed
const urgentNotificationsCount = computed(() => urgentNotifications.value.length)

// Navigation items
const mainMenuItems = [
  { name: 'Dashboard', path: '/dashboard' },
  { name: 'Pillars', path: '/pillars' },
  { name: 'Videos', path: '/videos' },
  { name: 'Content Studio', path: '/content-studio' }
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

// Notifications methods
const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
  if (showNotifications.value) {
    getNotifications()
  }
}

const openNotificationSettings = () => {
  showNotifications.value = false
  router.push('/settings?tab=automation')
}

// Handle clicks outside components
const handleClickOutside = (event) => {
  // Close notifications dropdown
  if (showNotifications.value && !event.target.closest('.relative')) {
    showNotifications.value = false
  }

  // Close mobile menu
  if (showMobileMenu.value && !event.target.closest('header')) {
    closeMobileMenu()
  }
}

// Lifecycle hooks
onMounted(() => {
  // Load notifications on mount
  getNotifications()

  // Add click outside listener
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  // Remove click outside listener
  document.removeEventListener('click', handleClickOutside)
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
