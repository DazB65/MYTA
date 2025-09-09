<template>
  <div
    :class="getPillarCardClasses(pillar.icon)"
    @click="openPillarModal"
  >
    <!-- Header -->
    <div class="mb-4 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="flex h-10 w-10 items-center justify-center rounded-lg" :class="getPillarIconColor(pillar.icon)">
          <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path v-if="pillar.icon === 'GameIcon'" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            <path v-else-if="pillar.icon === 'ReviewIcon'" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            <path v-else-if="pillar.icon === 'TechIcon'" fill-rule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
            <path v-else-if="pillar.icon === 'ProductivityIcon'" fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
            <path v-else d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-semibold" :class="getPillarTextColor(pillar.icon)">{{ pillar.name }}</h3>
          <p class="text-sm text-gray-400">{{ pillar.videoCount }} Videos • {{ pillar.lastUpload }}</p>
        </div>
      </div>
      <div class="text-gray-400">
        <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
        </svg>
      </div>
    </div>

    <!-- Compact Content (Always Visible) -->
    <div class="space-y-4">
      <!-- Pillar Stats (Compact) -->
      <div class="grid grid-cols-3 gap-3">
        <div class="text-center p-2 rounded-lg bg-forest-700">
          <div class="text-lg font-bold text-white">{{ formatViews(pillarStats.totalViews) }}</div>
          <div class="flex items-center justify-center text-xs mt-1" :class="pillarStats.viewsGrowth >= 0 ? 'text-green-400' : 'text-red-400'">
            <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
              <path v-if="pillarStats.viewsGrowth >= 0" fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              <path v-else fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 112 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            {{ Math.abs(pillarStats.viewsGrowth) }}%
          </div>
          <div class="text-xs text-gray-400">Total Views</div>
        </div>
        <div class="text-center p-2 rounded-lg bg-forest-700">
          <div class="text-lg font-bold text-white">{{ pillarStats.watchTime }}</div>
          <div class="flex items-center justify-center text-xs mt-1" :class="pillarStats.watchTimeGrowth >= 0 ? 'text-green-400' : 'text-red-400'">
            <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
              <path v-if="pillarStats.watchTimeGrowth >= 0" fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              <path v-else fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 112 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            {{ Math.abs(pillarStats.watchTimeGrowth) }}%
          </div>
          <div class="text-xs text-gray-400">Watch Time</div>
        </div>
        <div class="text-center p-2 rounded-lg bg-forest-700">
          <div class="text-lg font-bold text-white">{{ pillar.videoCount }}</div>
          <div class="flex items-center justify-center text-xs mt-1" :class="pillarStats.videoGrowth >= 0 ? 'text-green-400' : 'text-red-400'">
            <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
              <path v-if="pillarStats.videoGrowth >= 0" fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              <path v-else fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 112 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            {{ Math.abs(pillarStats.videoGrowth) }}%
          </div>
          <div class="text-xs text-gray-400">Total Videos</div>
        </div>
      </div>

      <!-- Best Performing Video -->
      <div class="flex items-center space-x-3 p-3 rounded-lg bg-forest-700">
        <div class="w-16 h-12 bg-gray-600 rounded overflow-hidden flex-shrink-0">
          <img
            :src="pillar.bestVideo.thumbnail"
            :alt="pillar.bestVideo.title"
            class="w-full h-full object-cover"
            @error="handleImageError"
            loading="lazy"
          />
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-white truncate">{{ pillar.bestVideo.title }}</p>
          <div class="flex items-center space-x-4 text-xs text-gray-400">
            <span>{{ formatViews(pillar.bestVideo.views) }} views</span>
            <span>{{ pillar.bestVideo.uploadDate }}</span>
          </div>
        </div>
        <div class="text-xs font-medium" :class="getPillarAccentColor(pillar.icon)">
          Top Performer
        </div>
      </div>

      <!-- Recent Videos Preview -->
      <div class="flex items-center justify-between">
        <h4 class="text-sm font-medium text-gray-300">Recent Videos</h4>
        <span class="text-xs text-gray-500">{{ pillar.recentVideos.length }} total</span>
      </div>
      
      <div class="grid grid-cols-3 gap-3">
        <div 
          v-for="video in pillar.recentVideos.slice(0, 3)" 
          :key="video.id"
          class="group cursor-pointer"
        >
          <div class="w-full h-16 bg-gray-600 rounded overflow-hidden mb-2">
            <img
              :src="video.thumbnail"
              :alt="video.title"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform"
              @error="handleImageError"
              loading="lazy"
            />
          </div>
          <p class="text-xs text-gray-400 truncate group-hover:text-white transition-colors">{{ video.title }}</p>
        </div>
      </div>
    </div>



  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useModals } from '../../composables/useModals'

// Props
const props = defineProps({
  pillar: {
    type: Object,
    required: true
  }
})

// Composables
const { openPillar } = useModals()



// Computed properties
const pillarStats = computed(() => {
  const videos = props.pillar.recentVideos || []
  const totalViews = videos.reduce((sum, video) => sum + video.views, 0)
  const avgViews = videos.length > 0 ? Math.round(totalViews / videos.length) : 0

  return {
    totalViews,
    avgViews,
    revenue: '2,450', // Mock data - would come from analytics
    watchTime: '45.2K hrs', // Mock data
    subscribers: 1200, // Mock data
    viewsGrowth: 12.5, // Mock data - percentage change
    revenueGrowth: 8.3, // Mock data
    watchTimeGrowth: 15.2, // Mock data
    subscriberGrowth: 9.8, // Mock data
    videoGrowth: 6.7 // Mock data - video upload growth percentage
  }
})

// Methods

const openPillarModal = () => {
  console.log('🔥 Opening pillar modal for:', props.pillar.name)
  openPillar(props.pillar)
}

const formatViews = (views) => {
  if (views >= 1000000) {
    return `${(views / 1000000).toFixed(1)}M`
  } else if (views >= 1000) {
    return `${(views / 1000).toFixed(1)}K`
  }
  return views.toString()
}

const getPillarIconColor = (icon) => {
  // Map pillar icons to agent colors for visual distinction
  const colorMap = {
    'GameIcon': 'bg-blue-600', // Agent 2 - Blue for Gaming content
    'ReviewIcon': 'bg-yellow-500', // Agent 2 (Levi) - Yellow for Reviews
    'TechIcon': 'bg-purple-600', // Agent 1 - Purple for Tech content
    'ProductivityIcon': 'bg-green-600', // Agent 3 - Green for Productivity
    'default': 'bg-orange-500' // Default orange
  }
  return colorMap[icon] || colorMap.default
}

const getPillarTextColor = (icon) => {
  // Map pillar icons to matching text colors
  const colorMap = {
    'GameIcon': 'text-blue-400', // Blue accent for Gaming
    'ReviewIcon': 'text-yellow-400', // Yellow accent for Reviews
    'TechIcon': 'text-purple-400', // Purple accent for Tech
    'ProductivityIcon': 'text-green-400', // Green accent for Productivity
    'default': 'text-white' // Default white
  }
  return colorMap[icon] || colorMap.default
}

const getPillarAccentColor = (icon) => {
  // Map pillar icons to accent colors for badges and highlights
  const colorMap = {
    'GameIcon': 'text-blue-400', // Blue accent for Gaming
    'ReviewIcon': 'text-yellow-400', // Yellow accent for Reviews
    'TechIcon': 'text-purple-400', // Purple accent for Tech
    'ProductivityIcon': 'text-green-400', // Green accent for Productivity
    'default': 'text-green-400' // Default green
  }
  return colorMap[icon] || colorMap.default
}

const getPillarButtonColor = (icon) => {
  // Map pillar icons to button colors
  const colorMap = {
    'GameIcon': 'bg-blue-600 hover:bg-blue-700', // Blue for Gaming
    'ReviewIcon': 'bg-yellow-500 hover:bg-yellow-600', // Yellow for Reviews
    'TechIcon': 'bg-purple-600 hover:bg-purple-700', // Purple for Tech
    'ProductivityIcon': 'bg-green-600 hover:bg-green-700', // Green for Productivity
    'default': 'bg-orange-500 hover:bg-orange-600' // Default orange
  }
  return colorMap[icon] || colorMap.default
}

// Get pillar card classes with enhanced colored borders
const getPillarCardClasses = (icon) => {
  const baseClasses = "rounded-xl p-6 cursor-pointer transition-all duration-300 hover:scale-[1.02] hover:shadow-lg"

  const colorMap = {
    'GameIcon': `${baseClasses} bg-blue-900/70 backdrop-blur-sm border-2 border-blue-600/60 shadow-blue-600/20 shadow-sm`,
    'ReviewIcon': `${baseClasses} bg-yellow-900/70 backdrop-blur-sm border-2 border-yellow-600/60 shadow-yellow-600/20 shadow-sm`,
    'TechIcon': `${baseClasses} bg-purple-900/70 backdrop-blur-sm border-2 border-purple-600/60 shadow-purple-600/20 shadow-sm`,
    'ProductivityIcon': `${baseClasses} bg-green-900/70 backdrop-blur-sm border-2 border-green-600/60 shadow-green-600/20 shadow-sm`,
    'default': `${baseClasses} bg-orange-900/70 backdrop-blur-sm border-2 border-orange-600/60 shadow-orange-600/20 shadow-sm`
  }
  return colorMap[icon] || colorMap.default
}

const handleImageError = (event) => {
  // Fallback to a solid color background when image fails to load
  event.target.style.display = 'none'
  event.target.parentElement.style.background = 'linear-gradient(135deg, #374151, #4B5563)'
  event.target.parentElement.style.display = 'flex'
  event.target.parentElement.style.alignItems = 'center'
  event.target.parentElement.style.justifyContent = 'center'

  // Add a play icon as fallback
  if (!event.target.parentElement.querySelector('.fallback-icon')) {
    const icon = document.createElement('div')
    icon.className = 'fallback-icon text-gray-400'
    icon.innerHTML = `
      <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
      </svg>
    `
    event.target.parentElement.appendChild(icon)
  }
}
</script>

<style scoped>
/* Smooth transitions for expand/collapse */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Image loading states */
img {
  background: linear-gradient(135deg, #374151, #4B5563);
  min-height: 100%;
  min-width: 100%;
}

/* Fallback for failed images */
.bg-gray-600 {
  background: linear-gradient(135deg, #374151, #4B5563) !important;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
