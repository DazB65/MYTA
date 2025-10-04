<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <!-- Main Content Area -->
    <div class="p-6 pt-24">
      <!-- Header -->
      <div class="mb-4 flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <h1 class="text-2xl font-bold text-white">Content Pillars - New Design</h1>
          <span class="text-gray-400">•</span>
          <p class="text-gray-400">Expandable pillar cards with content focus</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="text-sm text-gray-400">{{ totalVideos }} total videos</div>
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
      </div>

      <!-- Pillar Cards Grid -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <!-- Dynamic Pillar Cards -->
        <PillarCard
          v-for="pillar in pillars"
          :key="pillar.id"
          :pillar="pillar"
        />
      </div>

      <!-- Summary Stats -->
      <div class="mt-8 grid grid-cols-1 gap-4 md:grid-cols-4">
        <div class="rounded-lg bg-forest-800 p-4">
          <div class="text-2xl font-bold text-white">{{ totalVideos }}</div>
          <div class="text-sm text-gray-400">Total Videos</div>
        </div>
        <div class="rounded-lg bg-forest-800 p-4">
          <div class="text-2xl font-bold text-white">{{ activePillars.length }}</div>
          <div class="text-sm text-gray-400">Active Pillars</div>
        </div>
        <div class="rounded-lg bg-forest-800 p-4">
          <div class="text-2xl font-bold text-white">{{ formatViews(totalViews) }}</div>
          <div class="text-sm text-gray-400">Total Views</div>
        </div>
        <div class="rounded-lg bg-forest-800 p-4">
          <div class="text-2xl font-bold text-white">{{ totalIdeas }}</div>
          <div class="text-sm text-gray-400">Content Ideas</div>
        </div>
      </div>
    </div>

    <!-- Add Pillar Modal (placeholder) -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="rounded-lg bg-forest-800 p-6 w-96">
        <h3 class="text-lg font-semibold text-white mb-4">Add New Pillar</h3>
        <p class="text-gray-400 mb-4">This would be a form to create a new content pillar.</p>
        <div class="flex space-x-2">
          <button 
            @click="showAddModal = false"
            class="flex-1 rounded bg-gray-600 py-2 text-white hover:bg-gray-700"
          >
            Cancel
          </button>
          <button 
            @click="showAddModal = false"
            class="flex-1 rounded bg-orange-500 py-2 text-white hover:bg-orange-600"
          >
            Create
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import PillarCard from '~/components/pillars/PillarCard.vue'
import { usePillars } from '~/composables/usePillars'

// Demo page - no auth required for testing

// Use pillars composable
const { pillars, totalVideos, totalViews, activePillars } = usePillars()

// Local state
const showAddModal = ref(false)

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

<style scoped>
/* Custom styles for the demo page */
</style>
