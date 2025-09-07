<script setup lang="ts">
// Use default layout
definePageMeta({
  layout: 'default'
})

// SEO for landing page
useHead({
  title: 'MYTA - Your Agent Team for YouTube Growth',
  meta: [
    { name: 'description', content: 'Join the waitlist for the agent-powered YouTube growth platform that helps creators optimize content, analyze performance, and scale their channels with a team of specialized agents.' },
    { name: 'keywords', content: 'YouTube growth, agent analytics, content optimization, YouTube strategy, creator tools, video analytics, thumbnail optimization, YouTube SEO' },
    { property: 'og:title', content: 'MYTA - Your Agent Team for YouTube Growth' },
    { property: 'og:description', content: 'Join the waitlist for the agent-powered YouTube growth platform that helps creators optimize content, analyze performance, and scale their channels.' },
    { property: 'og:image', content: '/MY YT AGENT.png' },
    { property: 'og:url', content: 'https://myta.ai' },
    { name: 'twitter:title', content: 'MYTA - Your Agent Team for YouTube Growth' },
    { name: 'twitter:description', content: 'Join the waitlist for the agent-powered YouTube growth platform that helps creators optimize content, analyze performance, and scale their channels.' },
    { name: 'twitter:image', content: '/MY YT AGENT.png' }
  ]
})
</script>

<template>
  <div class="relative min-h-screen overflow-hidden">
    <!-- Background Effects -->
    <div class="absolute inset-0 bg-gradient-to-br from-forest-900 via-forest-900 to-forest-800/20"></div>
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(249,115,22,0.1),transparent_70%)]"></div>

    <!-- Animated Background Elements -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-orange-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-forest-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
    </div>

    <!-- Content -->
    <div class="relative z-10">
      <!-- Hero Section -->
      <HeroSection />

      <!-- Spacer -->
      <div class="h-32"></div>

      <!-- Footer -->
      <FooterSection />
    </div>
  </div>
</template>
