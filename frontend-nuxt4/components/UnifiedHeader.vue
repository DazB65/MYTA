<template>
  <header class="fixed top-0 left-0 right-0 z-50">
    <div class="p-4">
      <!-- Header Container -->
      <div class="rounded-xl bg-forest-800 p-3">
      <!-- Top Navigation Bar -->
      <div class="flex items-center justify-between mb-2 h-8">
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

          <!-- Logout Button -->
          <button
            @click="handleLogout"
            class="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-forest-700 transition-colors"
            title="Logout"
            :disabled="authStore.loading"
          >
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
                clip-rule="evenodd"
              />
            </svg>
          </button>

          <!-- User Profile -->
          <div class="flex items-center space-x-3">
            <div class="text-right">
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
      <div v-if="showMobileMenu" class="md:hidden mb-4 pt-4 border-t border-forest-700">
        <nav class="space-y-2">
          <NuxtLink
            v-for="item in mainMenuItems"
            :key="item.path"
            :to="item.path"
            @click="closeMobileMenu"
            class="block px-3 py-2 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:bg-forest-700 transition-colors"
            active-class="bg-orange-500 text-white hover:bg-orange-600"
          >
            <span class="flex items-center justify-between">
              {{ item.name }}
              <span v-if="item.premium" class="text-xs bg-orange-500 text-white px-2 py-1 rounded-full">PRO</span>
            </span>
          </NuxtLink>

          <!-- Mobile Logout Button -->
          <button
            @click="handleLogout"
            class="w-full text-left block px-3 py-2 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:bg-forest-700 transition-colors"
            :disabled="authStore.loading"
          >
            Logout
          </button>
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
              class="px-3 py-2 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:bg-forest-700 transition-colors relative"
              active-class="bg-orange-500 text-white hover:bg-orange-600"
            >
              {{ item.name }}
              <span v-if="item.premium" class="absolute -top-1 -right-1 text-xs bg-orange-500 text-white px-1.5 py-0.5 rounded-full">PRO</span>
            </NuxtLink>
          </nav>

          <!-- Right: Action Buttons -->
          <div class="flex-1 flex justify-end">
            <div class="flex items-center space-x-3">
              <!-- Connect YouTube Button -->
              <button
                class="btn btn-connect"
                @click="showConnectModal = true"
              >
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
                <span>Connect YouTube</span>
              </button>

              <!-- Selected Agent Button -->
              <button
                v-if="selectedAgent"
                class="btn btn-agent"
                @click="showChatPanel = true"
                :title="`Chat with ${selectedAgent.name}`"
              >
                <div class="w-6 h-6 rounded-lg overflow-hidden bg-white/30 flex items-center justify-center border border-white/20">
                  <img
                    :src="selectedAgent.image"
                    :alt="selectedAgent.name"
                    class="w-full h-full object-cover"
                  />
                </div>
                <span class="font-medium">{{ agentName || selectedAgent.name }}</span>
                <div class="w-2 h-2 rounded-full bg-green-400 shadow-sm" :title="`${selectedAgent.name} is online`"></div>
              </button>

              <!-- Fallback Agent Button -->
              <button
                v-else
                class="flex items-center space-x-2 rounded-lg bg-forest-700 px-3 py-2 text-sm text-white hover:bg-forest-600 transition-colors"
                @click="showChatPanel = true"
                title="Chat with Agent"
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

        <!-- YouTube Banner Compartment -->
        <YouTubeBannerCompartment
          :fallback-banner-url="userBanner.url"
          :fallback-channel-name="userBanner.channelName"
          :fallback-description="userBanner.description"
        />
      </div>
    </div>

    <!-- YouTube Connect Modal -->
    <YouTubeConnectModal
      v-if="showConnectModal"
      @close="showConnectModal = false"
      @connect="handleYouTubeConnect"
    />

    <!-- Agent Chat Panel -->
    <AgentChatPanel :is-open="showChatPanel" @close="showChatPanel = false" />
  </header>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useAgentSettings } from '../composables/useAgentSettings'
import { useAuthStore } from '../stores/auth'
import AgentChatPanel from './chat/AgentChatPanel.vue'
import YouTubeBannerCompartment from './dashboard/YouTubeBannerCompartment.vue'
import YouTubeConnectModal from './modals/YouTubeConnectModal.vue'

// Auth store
const authStore = useAuthStore()

// Agent settings
const { selectedAgent, agentName } = useAgentSettings()

// Mobile menu state
const showMobileMenu = ref(false)

// Modal states
const showConnectModal = ref(false)
const showChatPanel = ref(false)

// Navigation items
const mainMenuItems = [
  { name: 'Dashboard', path: '/dashboard' },
  { name: 'Tasks', path: '/tasks' },
  { name: 'Pillars', path: '/pillars' },
  { name: 'Videos', path: '/videos' },
  { name: 'Content Studio', path: '/content-studio' }
]

// User data
const userName = computed(() => {
  if (authStore.user?.name) {
    return authStore.user.name.toUpperCase()
  }
  return 'MARCELINE ANDERSON'
})

const userInitials = computed(() => {
  if (authStore.user?.name) {
    const names = authStore.user.name.split(' ')
    return names.map(name => name.charAt(0)).join('').toUpperCase()
  }
  return 'MA'
})

// YouTube Banner data
const userBanner = ref({
  url: '', // User's banner image URL
  channelName: userName.value || 'Your Channel',
  description: 'Customize your YouTube banner',
  avatar: '' // Channel avatar URL
})

// Load banner from localStorage on mount
onMounted(() => {
  if (typeof window !== 'undefined') {
    const savedBanner = localStorage.getItem('userYouTubeBanner')
    if (savedBanner) {
      try {
        const bannerData = JSON.parse(savedBanner)
        userBanner.value = { ...userBanner.value, ...bannerData }
      } catch (error) {
        console.error('Failed to load banner data:', error)
      }
    }
  }
})

// Handle banner upload
const handleBannerUpload = (uploadData) => {
  // Update the banner URL with the preview
  userBanner.value.url = uploadData.previewUrl

  // Save to localStorage (in a real app, you'd upload to a server)
  if (typeof window !== 'undefined') {
    const bannerData = {
      url: uploadData.previewUrl,
      channelName: userBanner.value.channelName,
      description: userBanner.value.description,
      avatar: userBanner.value.avatar,
      uploadedAt: new Date().toISOString()
    }
    localStorage.setItem('userYouTubeBanner', JSON.stringify(bannerData))
  }

  // You could also emit an event or call an API here
  console.log('Banner uploaded:', uploadData)
}

// Time-based greeting
const timeOfDay = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good Morning'
  if (hour < 17) return 'Good Afternoon'
  return 'Good Evening'
})

// Computed property for agent button classes
const agentButtonClasses = computed(() => {
  if (!selectedAgent.value) return []

  const colorMap = {
    'bg-purple-600': 'hover:bg-purple-700',
    'bg-blue-600': 'hover:bg-blue-700',
    'bg-green-600': 'hover:bg-green-700',
    'bg-orange-600': 'hover:bg-orange-700',
    'bg-pink-600': 'hover:bg-pink-700',
    'bg-red-600': 'hover:bg-red-700',
    'bg-yellow-600': 'hover:bg-yellow-700',
  }

  const hoverColor = colorMap[selectedAgent.value.color] || 'hover:bg-forest-600'

  return [
    'flex items-center space-x-2 rounded-lg px-3 py-2 text-sm text-white transition-colors',
    selectedAgent.value.color,
    hoverColor
  ]
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

// Logout function
const handleLogout = async () => {
  try {
    await authStore.logout()
    await navigateTo('/login')
  } catch (error) {
    console.error('Logout failed:', error)
  }
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
