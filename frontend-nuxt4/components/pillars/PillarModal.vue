<template>
  <div class="fixed inset-0 z-50 flex items-start justify-center" style="padding-top: 280px;">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black bg-opacity-50" @click="$emit('close')" />

    <!-- Modal -->
    <div class="relative bg-forest-800 rounded-xl shadow-xl mx-4 max-h-[calc(100vh-10rem)] overflow-y-auto border border-forest-600" style="width: calc(100% - 2rem);">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-forest-600">
        <div class="flex items-center space-x-3">
          <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-orange-500">
            <svg class="h-8 w-8 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path v-if="pillar.icon === 'GameIcon'" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              <path v-else-if="pillar.icon === 'ReviewIcon'" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              <path v-else-if="pillar.icon === 'TechIcon'" fill-rule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
              <path v-else-if="pillar.icon === 'ProductivityIcon'" fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
              <path v-else d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div>
            <h3 class="text-xl font-semibold text-white">{{ pillar.name }} Pillar</h3>
            <p class="text-sm text-gray-400">{{ pillar.videoCount }} Videos • {{ pillar.lastUpload }}</p>
          </div>
        </div>
        <button
          class="text-gray-400 hover:text-white transition-colors"
          @click="$emit('close')"
        >
          <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="p-6 space-y-6">
        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-forest-700 rounded-lg p-4">
            <div class="text-2xl font-bold text-white">{{ formatViews(pillarStats.totalViews) }}</div>
            <div class="flex items-center text-sm mt-1" :class="pillarStats.viewsGrowth >= 0 ? 'text-green-400' : 'text-red-400'">
              <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                <path v-if="pillarStats.viewsGrowth >= 0" fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                <path v-else fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 112 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              {{ Math.abs(pillarStats.viewsGrowth) }}%
            </div>
            <div class="text-xs text-gray-400">Total Views</div>
          </div>
          
          <div class="bg-forest-700 rounded-lg p-4">
            <div class="text-2xl font-bold text-white">{{ pillarStats.watchTime }}</div>
            <div class="flex items-center text-sm mt-1" :class="pillarStats.watchTimeGrowth >= 0 ? 'text-green-400' : 'text-red-400'">
              <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                <path v-if="pillarStats.watchTimeGrowth >= 0" fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                <path v-else fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 112 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              {{ Math.abs(pillarStats.watchTimeGrowth) }}%
            </div>
            <div class="text-xs text-gray-400">Watch Time</div>
          </div>
          
          <div class="bg-forest-700 rounded-lg p-4">
            <div class="text-2xl font-bold text-white">{{ pillar.videoCount }}</div>
            <div class="flex items-center text-sm mt-1" :class="pillarStats.videoGrowth >= 0 ? 'text-green-400' : 'text-red-400'">
              <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                <path v-if="pillarStats.videoGrowth >= 0" fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                <path v-else fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 112 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              {{ Math.abs(pillarStats.videoGrowth) }}%
            </div>
            <div class="text-xs text-gray-400">Total Videos</div>
          </div>
          
          <div class="bg-forest-700 rounded-lg p-4">
            <div class="text-2xl font-bold text-white">{{ pillar.contentIdeas?.length || 0 }}</div>
            <div class="text-xs text-gray-400">Content Ideas</div>
          </div>
        </div>

        <!-- Best Performing Video -->
        <div v-if="pillar.bestVideo" class="bg-forest-700 rounded-lg p-4">
          <h4 class="text-lg font-semibold text-white mb-3">Best Performing Video</h4>
          <div class="flex items-center space-x-4">
            <img 
              :src="pillar.bestVideo.thumbnail" 
              :alt="pillar.bestVideo.title"
              class="w-24 h-16 rounded-lg object-cover"
            />
            <div class="flex-1">
              <h5 class="font-medium text-white">{{ pillar.bestVideo.title }}</h5>
              <div class="flex items-center space-x-4 text-sm text-gray-400 mt-1">
                <span>{{ formatViews(pillar.bestVideo.views) }} views</span>
                <span>{{ pillar.bestVideo.uploadDate }}</span>
                <span>{{ pillar.bestVideo.duration }}</span>
              </div>
            </div>
            <div class="text-sm text-orange-400 font-medium">Top Performer</div>
          </div>
        </div>

        <!-- Recent Videos -->
        <div v-if="pillar.recentVideos && pillar.recentVideos.length > 0" class="bg-forest-700 rounded-lg p-4">
          <div class="flex items-center justify-between mb-3">
            <h4 class="text-lg font-semibold text-white">Recent Videos</h4>
            <span class="text-sm text-gray-400">{{ pillar.recentVideos.length }} total</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            <div 
              v-for="video in pillar.recentVideos.slice(0, 6)" 
              :key="video.id"
              class="flex items-center space-x-3 p-2 rounded-lg hover:bg-forest-600 transition-colors cursor-pointer"
            >
              <img 
                :src="video.thumbnail" 
                :alt="video.title"
                class="w-16 h-10 rounded object-cover"
              />
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-white truncate">{{ video.title }}</p>
                <p class="text-xs text-gray-400">{{ formatViews(video.views) }} views</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Content Ideas -->
        <div v-if="pillar.contentIdeas && pillar.contentIdeas.length > 0" class="bg-forest-700 rounded-lg p-4">
          <div class="flex items-center justify-between mb-3">
            <h4 class="text-lg font-semibold text-white">Content Ideas</h4>
            <span class="text-sm text-gray-400">{{ pillar.contentIdeas.length }} ideas</span>
          </div>
          <div class="space-y-2">
            <div 
              v-for="idea in pillar.contentIdeas.slice(0, 5)" 
              :key="idea.id"
              class="p-3 rounded-lg bg-forest-600 hover:bg-forest-500 transition-colors cursor-pointer"
            >
              <div class="flex items-center justify-between">
                <h5 class="font-medium text-white">{{ idea.title }}</h5>
                <span 
                  class="text-xs px-2 py-1 rounded-full"
                  :class="{
                    'bg-red-500/20 text-red-400': idea.priority === 'high',
                    'bg-yellow-500/20 text-yellow-400': idea.priority === 'medium',
                    'bg-green-500/20 text-green-400': idea.priority === 'low'
                  }"
                >
                  {{ idea.priority }}
                </span>
              </div>
              <p class="text-sm text-gray-400 mt-1">{{ idea.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center justify-between p-6 border-t border-forest-600">
        <div class="text-sm text-gray-400">{{ pillar.status }}</div>
        <div class="flex space-x-3">
          <button 
            @click="handleEdit"
            class="px-4 py-2 bg-forest-600 text-white rounded-lg hover:bg-forest-500 transition-colors flex items-center space-x-2"
          >
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
            </svg>
            <span>Edit Pillar</span>
          </button>
          <button 
            @click="handleDelete"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center space-x-2"
          >
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <span>Delete Pillar</span>
          </button>
          <button 
            class="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors flex items-center space-x-2"
          >
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            <span>Create Content</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 z-60 flex items-center justify-center bg-black bg-opacity-50">
      <div class="rounded-xl bg-forest-800 p-6 w-full max-w-md mx-4 border border-forest-600">
        <div class="mb-4 flex items-center">
          <div class="flex h-10 w-10 items-center justify-center rounded-full bg-red-100">
            <svg class="h-6 w-6 text-red-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-semibold text-white">Delete Pillar</h3>
            <p class="text-sm text-gray-400">This action cannot be undone</p>
          </div>
        </div>

        <div class="mb-6">
          <p class="text-gray-300">
            Are you sure you want to delete the <strong class="text-white">"{{ pillar.name }}"</strong> pillar? 
            This will permanently remove all associated content ideas and cannot be undone.
          </p>
        </div>

        <div class="flex items-center justify-end space-x-3">
          <button
            @click="showDeleteConfirm = false"
            class="px-4 py-2 text-gray-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
          <button
            @click="confirmDelete"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Delete Pillar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { usePillars } from '../../composables/usePillars'

// Props
const props = defineProps({
  pillar: {
    type: Object,
    required: true
  }
})

// Emits
const emit = defineEmits(['close', 'edit', 'delete'])

// Composables
const { deletePillar } = usePillars()

// State
const showDeleteConfirm = ref(false)

// Computed properties
const pillarStats = computed(() => {
  const videos = props.pillar.recentVideos || []
  const totalViews = videos.reduce((sum, video) => sum + video.views, 0)

  return {
    totalViews,
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
const formatViews = (views) => {
  if (views >= 1000000) {
    return `${(views / 1000000).toFixed(1)}M`
  } else if (views >= 1000) {
    return `${(views / 1000).toFixed(1)}K`
  }
  return views.toString()
}

const handleEdit = () => {
  emit('edit', props.pillar)
}

const handleDelete = () => {
  showDeleteConfirm.value = true
}

const confirmDelete = () => {
  try {
    deletePillar(props.pillar.id)
    showDeleteConfirm.value = false
    emit('close')
    console.log('Deleted pillar:', props.pillar.name)
  } catch (error) {
    console.error('Error deleting pillar:', error)
    alert('Error deleting pillar. Please try again.')
  }
}
</script>
