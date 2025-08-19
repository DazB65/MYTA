<template>
  <div>
    <!-- Main Application -->
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>

    <!-- Toast Notifications -->
    <UiToastContainer />
  </div>
</template>

<script setup>
// Global app configuration
useHead({
  title: 'Vidalytics - Your AI Agent for Content and Growth',
  meta: [
    { name: 'description', content: 'Vidalytics helps YouTube creators grow their channels with AI-powered insights, content planning, and analytics.' },
    { name: 'keywords', content: 'YouTube analytics, content creation, AI assistant, channel growth, video optimization' },
    { property: 'og:title', content: 'Vidalytics - Your AI Agent for Content and Growth' },
    { property: 'og:description', content: 'Grow your YouTube channel with AI-powered insights and content planning.' },
    { property: 'og:type', content: 'website' },
    { property: 'og:image', content: '/og-image.png' },
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:title', content: 'Vidalytics - Your AI Agent for Content and Growth' },
    { name: 'twitter:description', content: 'Grow your YouTube channel with AI-powered insights and content planning.' },
    { name: 'twitter:image', content: '/og-image.png' }
  ],
  htmlAttrs: {
    lang: 'en'
  }
})

// Global error handling
onErrorCaptured((error, instance, info) => {
  console.error('Global error:', error, info)
  // You can send this to an error reporting service
  return false
})
</script>

<style>
/* Import main CSS file */
@import '../assets/css/main.css';

/* Global styles */
html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #1f2937;
}

::-webkit-scrollbar-thumb {
  background: #4b5563;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}

/* Focus styles */
*:focus {
  outline: 2px solid #ec4899;
  outline-offset: 2px;
}

/* Selection styles */
::selection {
  background-color: #ec4899;
  color: white;
}

/* Transitions */
* {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>
