<template>
  <div class="min-h-screen bg-gradient-to-b from-slate-800 via-gray-850 to-gray-900 text-white">
    <!-- Main Content Area -->
    <div class="p-6 pt-24">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-white">Content Pillars</h1>
        <p class="text-gray-400">Organize and manage your content themes</p>
      </div>

      <!-- Content -->
      <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
        <div class="space-y-6">
          <!-- Header with Add Button -->
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <div class="text-sm text-gray-400">{{ totalVideos }} total videos</div>
            </div>
            <button
              class="flex items-center space-x-2 rounded-lg bg-orange-500 px-4 py-2 text-white transition-colors hover:bg-orange-600"
              @click="handleAddPillar"
            >
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                  clip-rule="evenodd"
                />
              </svg>
              <span>Add Pillar</span>
            </button>
          </div>

          <!-- Pillar Cards Grid -->
          <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <!-- Empty State -->
            <div v-if="pillars.length === 0" class="col-span-full">
              <EmptyState
                icon="🎯"
                title="No Content Pillars Yet"
                description="Content pillars help you organize your content strategy into themes. Create your first pillar to get started!"
                action-text="Create First Pillar"
                help-text="Pillars are strategic content themes that help you stay focused and consistent with your content creation"
                variant="primary"
                @action="handleAddPillar"
              />
            </div>

            <!-- Dynamic Pillar Cards -->
            <PillarCard
              v-for="pillar in pillars"
              :key="pillar.id"
              :pillar="pillar"
            />
          </div>

          <!-- Summary Stats -->
          <div class="mt-8 grid grid-cols-1 gap-4 md:grid-cols-4">
            <div class="rounded-lg bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-4">
              <div class="text-2xl font-bold text-white">{{ totalVideos }}</div>
              <div class="text-sm text-gray-400">Total Videos</div>
            </div>
            <div class="rounded-lg bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-4">
              <div class="text-2xl font-bold text-white">{{ activePillars.length }}</div>
              <div class="text-sm text-gray-400">Active Pillars</div>
            </div>
            <div class="rounded-lg bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-4">
              <div class="text-2xl font-bold text-white">{{ formatViews(totalViews) }}</div>
              <div class="text-sm text-gray-400">Total Views</div>
            </div>
            <div class="rounded-lg bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-4">
              <div class="text-2xl font-bold text-white">{{ totalIdeas }}</div>
              <div class="text-sm text-gray-400">Content Ideas</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Pillar Modal -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6 w-full max-w-md mx-4">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-white">Add New Pillar</h3>
          <button @click="showAddModal = false" class="text-gray-400 hover:text-white">
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="createPillar">
          <div class="space-y-4">
            <!-- Pillar Name -->
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Pillar Name</label>
              <input
                v-model="newPillar.name"
                type="text"
                required
                class="w-full rounded-lg bg-gray-700 border-2 border-gray-600/70 shadow-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
                placeholder="e.g., Gaming Tutorials, Tech Reviews..."
              />
            </div>

            <!-- Description -->
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Description</label>
              <textarea
                v-model="newPillar.description"
                rows="3"
                class="w-full rounded-lg bg-gray-700 border-2 border-gray-600/70 shadow-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
                placeholder="Describe what type of content this pillar will focus on..."
              ></textarea>
            </div>

            <!-- Icon Selection -->
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Icon</label>
              <div class="grid grid-cols-4 gap-2">
                <button
                  v-for="icon in availableIcons"
                  :key="icon.value"
                  type="button"
                  @click="newPillar.icon = icon.value"
                  :class="[
                    'p-3 rounded-lg border-2 transition-colors',
                    newPillar.icon === icon.value
                      ? 'border-orange-500 bg-orange-500/20'
                      : 'border-gray-600 bg-gray-700 hover:border-orange-400'
                  ]"
                >
                  <svg class="h-5 w-5 text-white mx-auto" fill="currentColor" viewBox="0 0 20 20">
                    <path v-html="icon.path"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <div class="flex items-center justify-end space-x-3 mt-6">
            <button
              type="button"
              @click="showAddModal = false"
              class="px-4 py-2 text-gray-400 hover:text-white transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
            >
              Create Pillar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import PillarCard from '../../components/pillars/PillarCard.vue'
import { usePillars } from '../../composables/usePillars'

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// Use pillars composable
const { pillars, totalVideos, totalViews, activePillars, addPillar } = usePillars()

// Auth store for premium access
const authStore = useAuthStore()

// Premium access check
const hasPremiumAccess = computed(() => {
  // For demo purposes, you can set this to true/false
  // In production, this would check the user's subscription tier
  return authStore.user?.subscription_tier === 'pro' || authStore.user?.subscription_tier === 'teams'
})

// Local state
const showAddModal = ref(false)

// New pillar form data
const newPillar = ref({
  name: '',
  description: '',
  icon: 'GameIcon'
})

// Available icons for pillar selection
const availableIcons = ref([
  {
    value: 'GameIcon',
    path: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
  },
  {
    value: 'ReviewIcon',
    path: 'M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z'
  },
  {
    value: 'TechIcon',
    path: 'M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z'
  },
  {
    value: 'ProductivityIcon',
    path: 'M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z'
  }
])

// Computed properties
const totalIdeas = computed(() => {
  return pillars.value.reduce((total, pillar) => total + pillar.contentIdeas.length, 0)
})

// Methods
const handleAddPillar = () => {
  console.log('🎯 Add Pillar button clicked!')
  showAddModal.value = true
  console.log('🎯 Modal should be visible:', showAddModal.value)
}

const createPillar = () => {
  try {
    // Validate required fields
    if (!newPillar.value.name.trim()) {
      alert('Please enter a pillar name')
      return
    }

    // Create new pillar using the composable
    const pillarData = {
      name: newPillar.value.name.trim(),
      icon: newPillar.value.icon,
      videoCount: 0,
      lastUpload: 'No uploads yet',
      status: 'New content pillar - ready to start creating!',
      bestVideo: {
        id: 'placeholder',
        title: 'No videos yet - start creating content!',
        thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=320&h=180&fit=crop&crop=center',
        views: 0,
        uploadDate: 'N/A',
        duration: '0:00'
      },
      recentVideos: [],
      contentIdeas: [
        {
          id: Date.now(),
          title: 'Welcome to your new pillar!',
          description: newPillar.value.description.trim() || 'Start brainstorming content ideas for this pillar.',
          priority: 'medium',
          status: 'idea'
        }
      ]
    }

    addPillar(pillarData)

    // Reset form
    newPillar.value = {
      name: '',
      description: '',
      icon: 'GameIcon'
    }

    // Close modal
    showAddModal.value = false

    // Show success message
    alert(`Successfully created "${pillarData.name}" pillar!`)
  } catch (error) {
    console.error('Error creating pillar:', error)
    alert('Error creating pillar. Please try again.')
  }
}

// Helper function
const formatViews = (views) => {
  if (views >= 1000000) {
    return `${(views / 1000000).toFixed(1)}M`
  } else if (views >= 1000) {
    return `${(views / 1000).toFixed(1)}K`
  }
  return views.toString()
}
</script>