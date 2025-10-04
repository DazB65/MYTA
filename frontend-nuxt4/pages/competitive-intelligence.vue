<template>
  <div class="min-h-screen bg-gradient-to-b from-slate-800 via-gray-850 to-gray-900 text-white">
    <div class="p-6 pt-24">
      <!-- Page Header -->
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-white">Competitive Intelligence 2.0</h1>
        <p class="text-gray-400">Advanced market positioning and strategic analysis</p>
        <div class="mt-2 flex items-center gap-2">
          <span class="px-2 py-1 bg-orange-900/30 text-orange-300 rounded text-xs font-medium">PRO FEATURE</span>
          <span class="text-gray-500 text-sm">Available for Pro and Teams subscribers</span>
        </div>
      </div>

      <!-- Main Content -->
      <div class="max-w-7xl mx-auto">
        <CompetitiveIntelligenceDashboard />
      </div>
    </div>
  </div>
</template>

<script setup>
import CompetitiveIntelligenceDashboard from '~/components/competitive/CompetitiveIntelligenceDashboard.vue';

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// Set page title
useHead({
  title: 'Competitive Intelligence 2.0 - MYTA',
  meta: [
    { name: 'description', content: 'Advanced competitive analysis and market positioning for content creators' }
  ]
})
</script>
