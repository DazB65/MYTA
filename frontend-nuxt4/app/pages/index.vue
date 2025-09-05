<script setup>
// Use landing layout instead of default
definePageMeta({
  layout: 'landing'
})

// SEO for landing page
useHead({
  title: 'MYTA - Your AI Team for YouTube Growth',
  meta: [
    { name: 'description', content: 'Get early access to the AI-powered YouTube growth platform that helps creators optimize content, analyze performance, and scale their channels with a team of specialized AI agents.' },
    { name: 'keywords', content: 'YouTube growth, AI analytics, content optimization, YouTube strategy, creator tools, video analytics, thumbnail optimization, YouTube SEO' },
    { property: 'og:title', content: 'MYTA - Your AI Team for YouTube Growth' },
    { property: 'og:description', content: 'Get early access to the AI-powered YouTube growth platform that helps creators optimize content, analyze performance, and scale their channels.' },
    { property: 'og:image', content: '/MY YT AGENT.png' },
    { property: 'og:url', content: 'https://myta.ai' },
    { name: 'twitter:title', content: 'MYTA - Your AI Team for YouTube Growth' },
    { name: 'twitter:description', content: 'Get early access to the AI-powered YouTube growth platform that helps creators optimize content, analyze performance, and scale their channels.' },
    { name: 'twitter:image', content: '/MY YT AGENT.png' }
  ]
})
</script>

<template>
  <div>
    <!-- Hero Section -->
    <HeroSection />

    <!-- Features Grid -->
    <FeatureGrid />

    <!-- Agent Showcase -->
    <AgentShowcase />

    <!-- Footer -->
    <FooterSection />

    <!-- Additional sections can be added here -->
    <!-- <PricingSection /> -->
    <!-- <TestimonialsSection /> -->
    <!-- <FAQSection /> -->
  </div>
</template>
