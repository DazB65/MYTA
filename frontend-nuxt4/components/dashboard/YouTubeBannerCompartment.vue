<template>
  <div class="relative flex h-24 items-center justify-between overflow-hidden rounded-xl bg-gradient-to-r from-gray-600 via-gray-700 to-gray-800 px-6">
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

      <!-- Right side: Hidden for now -->
      <div class="text-right">
        <!-- Temporarily hidden until OAuth is working -->
        <!-- Will show Connect/Refresh buttons when OAuth flow is fixed -->
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
