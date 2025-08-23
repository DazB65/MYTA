<template>
  <div class="relative flex h-24 items-center justify-between overflow-hidden rounded-xl bg-gradient-to-r from-forest-600 via-forest-700 to-forest-800 px-6">
    <!-- Banner Background Image -->
    <div 
      v-if="bannerUrl"
      class="absolute inset-0 bg-cover bg-center bg-no-repeat"
      :style="{ backgroundImage: `url(${bannerUrl})` }"
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
        <!-- Channel Avatar (optional) -->
        <div 
          v-if="channelAvatar"
          class="h-12 w-12 overflow-hidden rounded-full bg-white bg-opacity-20 ring-2 ring-white ring-opacity-30"
        >
          <img
            :src="channelAvatar"
            :alt="channelName"
            class="h-full w-full object-cover"
          />
        </div>

        <!-- Channel Name and Info -->
        <div class="text-white">
          <div class="text-xl font-bold drop-shadow-lg">
            {{ channelName || 'Your YouTube Channel' }}
          </div>
          <div class="text-sm opacity-90 drop-shadow">
            {{ channelDescription || 'Upload your banner to personalize this space' }}
          </div>
        </div>
      </div>

      <!-- Right side: Upload/Edit Button -->
      <div class="text-right">
        <button
          @click="openBannerUpload"
          class="flex items-center space-x-2 rounded-lg bg-white bg-opacity-20 px-4 py-2 text-white backdrop-blur-sm transition-all hover:bg-opacity-30 hover:scale-105"
          title="Upload YouTube Banner"
        >
          <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd"/>
          </svg>
          <span class="text-sm font-medium">{{ bannerUrl ? 'Change' : 'Upload' }}</span>
        </button>
      </div>
    </div>

    <!-- Decorative glow effects -->
    <div class="absolute right-0 top-0 -mr-16 -mt-16 h-32 w-32 rounded-full bg-white bg-opacity-10 blur-xl"></div>
    <div class="absolute bottom-0 left-0 -mb-12 -ml-12 h-24 w-24 rounded-full bg-white bg-opacity-10 blur-lg"></div>

    <!-- Hidden file input -->
    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      class="hidden"
      @change="handleFileUpload"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Props
const props = defineProps({
  bannerUrl: {
    type: String,
    default: ''
  },
  channelName: {
    type: String,
    default: ''
  },
  channelDescription: {
    type: String,
    default: ''
  },
  channelAvatar: {
    type: String,
    default: ''
  }
})

// Emits
const emit = defineEmits(['upload', 'update'])

// Refs
const fileInput = ref(null)

// Methods
const openBannerUpload = () => {
  fileInput.value?.click()
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Create a preview URL
    const previewUrl = URL.createObjectURL(file)
    
    // Emit the upload event with file and preview
    emit('upload', {
      file,
      previewUrl,
      name: file.name,
      size: file.size
    })
  }
}
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
