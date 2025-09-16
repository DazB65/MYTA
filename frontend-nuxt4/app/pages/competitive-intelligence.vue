<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
    <!-- Header -->
    <AppHeader />
    
    <!-- Main Content -->
    <main class="pt-20 pb-8">
      <div class="max-w-7xl mx-auto px-6">
        <CompetitiveIntelligenceDashboard />
      </div>
    </main>
  </div>
</template>

<script setup>
import AppHeader from '../../components/AppHeader.vue'
import CompetitiveIntelligenceDashboard from '../../components/competitive/CompetitiveIntelligenceDashboard.vue'

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
