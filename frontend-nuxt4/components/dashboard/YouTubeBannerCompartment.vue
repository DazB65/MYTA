<template>
  <div class="relative flex h-24 items-center justify-between overflow-hidden rounded-xl bg-gradient-to-r from-forest-600 via-forest-700 to-forest-800 px-6">
    <!-- Banner Background Image -->
    <div
      v-if="displayBanner"
      class="absolute inset-0 bg-cover bg-center bg-no-repeat"
      :style="{ backgroundImage: `url(${displayBanner})` }"
    >
      <!-- Dark overlay for text readability -->
      <div class="absolute inset-0 bg-black bg-opacity-40"></div>
    </div>

    <!-- Default gradient background when no banner -->
    <div
      v-else
      class="absolute inset-0 bg-gradient-to-r from-orange-500 via-orange-600 to-red-500"
    ></div>

    <!-- Content overlay -->
    <div class="relative z-10 flex w-full items-center justify-between">
      <!-- Left side: Channel Info -->
      <div class="flex items-center space-x-4">
        <!-- Channel Avatar -->
        <div
          v-if="displayAvatar"
          class="h-12 w-12 overflow-hidden rounded-full bg-white bg-opacity-20 ring-2 ring-white ring-opacity-30"
        >
          <img
            :src="displayAvatar"
            :alt="displayChannelName"
            class="h-full w-full object-cover"
          />
        </div>

        <!-- Channel Name and Info -->
        <div class="text-white">
          <div class="text-xl font-bold drop-shadow-lg">
            {{ displayChannelName }}
          </div>
          <div class="text-sm opacity-90 drop-shadow">
            {{ displayDescription }}
          </div>
          <!-- Subscriber count if available -->
          <div v-if="subscriberCount && subscriberCount !== '0'" class="text-xs opacity-75 drop-shadow">
            {{ formatSubscriberCount(subscriberCount) }} subscribers
          </div>
        </div>
      </div>

      <!-- Right side: Connect/Refresh Button -->
      <div class="text-right">
        <!-- Loading state -->
        <div v-if="isLoading" class="flex items-center space-x-2 text-white">
          <svg class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span class="text-sm">Loading...</span>
        </div>

        <!-- Connect button if not connected -->
        <button
          v-else-if="!isConnected"
          @click="handleConnect"
          class="flex items-center space-x-2 rounded-lg bg-red-600 bg-opacity-90 px-4 py-2 text-white backdrop-blur-sm transition-all hover:bg-opacity-100 hover:scale-105"
          title="Connect YouTube Account"
        >
          <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
          </svg>
          <span class="text-sm font-medium">Connect</span>
        </button>

        <!-- Refresh button if connected -->
        <button
          v-else
          @click="handleRefresh"
          class="flex items-center space-x-2 rounded-lg bg-white bg-opacity-20 px-4 py-2 text-white backdrop-blur-sm transition-all hover:bg-opacity-30 hover:scale-105"
          title="Refresh Channel Data"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          <span class="text-sm font-medium">Refresh</span>
        </button>
      </div>
    </div>

    <!-- Decorative glow effects -->
    <div class="absolute right-0 top-0 -mr-16 -mt-16 h-32 w-32 rounded-full bg-white bg-opacity-10 blur-xl"></div>
    <div class="absolute bottom-0 left-0 -mb-12 -ml-12 h-24 w-24 rounded-full bg-white bg-opacity-10 blur-lg"></div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useYouTubeChannel } from '../../composables/useYouTubeChannel'

// Props (fallback values if YouTube not connected)
const props = defineProps({
  fallbackBannerUrl: {
    type: String,
    default: ''
  },
  fallbackChannelName: {
    type: String,
    default: 'Your YouTube Channel'
  },
  fallbackDescription: {
    type: String,
    default: 'Connect your YouTube account to display your channel banner'
  }
})

// YouTube channel composable
const {
  channelName,
  channelAvatar,
  channelBanner,
  channelDescription,
  subscriberCount,
  isConnected,
  isLoading,
  error,
  connectYouTube,
  fetchChannelData,
  initialize
} = useYouTubeChannel()

// Computed display values (use YouTube data if available, otherwise fallbacks)
const displayChannelName = computed(() => {
  return channelName.value || 'Your YouTube Channel'
})

const displayDescription = computed(() => {
  if (isConnected.value) {
    return channelDescription.value || 'YouTube channel connected'
  }
  return 'Your YT Banner goes here'
})

const displayBanner = computed(() => {
  return channelBanner.value || props.fallbackBannerUrl
})

const displayAvatar = computed(() => {
  return channelAvatar.value
})

// Format subscriber count for display
const formatSubscriberCount = (count) => {
  const num = parseInt(count)
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1)}M`
  } else if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K`
  }
  return num.toString()
}

// Handle connect button click
const handleConnect = async () => {
  console.log('🔗 Connect button clicked!')
  try {
    console.log('🔗 Calling connectYouTube...')
    await connectYouTube()
    console.log('🔗 connectYouTube completed')
  } catch (error) {
    console.error('❌ Failed to connect YouTube:', error)
  }
}

// Handle refresh button click
const handleRefresh = async () => {
  try {
    await fetchChannelData(true) // Force refresh
  } catch (error) {
    console.error('Failed to refresh channel data:', error)
  }
}

// Initialize on mount
onMounted(async () => {
  await initialize()
})
</script>

<style scoped>
/* Additional styles for better text readability */
.drop-shadow-lg {
  filter: drop-shadow(0 10px 8px rgb(0 0 0 / 0.04)) drop-shadow(0 4px 3px rgb(0 0 0 / 0.1));
}

.drop-shadow {
  filter: drop-shadow(0 1px 2px rgb(0 0 0 / 0.1)) drop-shadow(0 1px 1px rgb(0 0 0 / 0.06));
}
</style>
