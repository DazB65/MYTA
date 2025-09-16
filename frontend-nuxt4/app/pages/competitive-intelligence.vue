<template>
  <div class="p-6 pt-24">
    <!-- Page Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-white">Competitive Intelligence 2.0</h1>
      <p class="text-gray-400">Advanced market positioning and strategic analysis</p>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto">
      <CompetitiveIntelligenceDashboard />
    </div>
  </div>
</template>

<script setup>
import CompetitiveIntelligenceDashboard from '../../components/competitive/CompetitiveIntelligenceDashboard.vue';

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
