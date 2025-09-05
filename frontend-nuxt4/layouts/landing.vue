<template>
  <div class="min-h-screen bg-background text-white">
    <!-- Landing Page Header -->
    <LandingHeader />
    
    <!-- Main Content -->
    <main>
      <slot />
    </main>
    
    <!-- Keep modals for waitlist signup -->
    <AppModals />
    
    <!-- Notifications for success messages -->
    <AppNotifications />
  </div>
</template>

<script setup>
// SEO and meta configuration for landing page
useHead({
  titleTemplate: '%s',
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { name: 'theme-color', content: '#EC4899' },
    { name: 'apple-mobile-web-app-capable', content: 'yes' },
    { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' },
    { name: 'robots', content: 'index, follow' },
    { property: 'og:type', content: 'website' },
    { property: 'og:site_name', content: 'MYTA' },
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:site', content: '@MYTA' }
  ],
  link: [
    { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
    { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' },
    { rel: 'canonical', href: 'https://myta.ai' }
  ]
})

// Global error handling
onErrorCaptured((error) => {
  console.error('Landing page error:', error)
  return false
})
</script>

<style scoped>
/* Landing page specific styles */
main {
  /* Remove the default padding-top from the main app */
  padding-top: 0;
}
</style>
