<template>
  <div class="min-h-screen bg-gray-900 text-white">
    <!-- Navigation Bar -->
    <AppHeader />

    <!-- Main Content Area -->
    <main class="min-h-screen">
      <!-- Page Content -->
      <div class="p-6">
        <slot />
      </div>
    </main>
    
    <!-- Global Modals -->
    <AppModals />
    
    <!-- Notifications -->
    <AppNotifications />
    
    <!-- Loading Overlay -->
    <AppLoading v-if="$loading" />
  </div>
</template>

<script setup>
import AppHeader from '~/components/AppHeader.vue'

// Global layout composables
const { $loading } = useNuxtApp()

// SEO and meta configuration
useHead({
  titleTemplate: '%s - Vidalytics',
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { name: 'theme-color', content: '#EC4899' },
    { name: 'apple-mobile-web-app-capable', content: 'yes' },
    { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' }
  ],
  link: [
    { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
    { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' }
  ]
})

// Global error handling
onErrorCaptured((error) => {
  console.error('Layout error:', error)
  return false
})
</script>

<style scoped>
/* Layout-specific styles */
.layout-enter-active,
.layout-leave-active {
  transition: opacity 0.3s ease;
}

.layout-enter-from,
.layout-leave-to {
  opacity: 0;
}
</style>
