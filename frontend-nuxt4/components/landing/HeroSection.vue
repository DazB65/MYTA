<template>
  <section class="relative min-h-screen flex items-center justify-center overflow-hidden">
    <!-- Background Effects -->
    <div class="absolute inset-0 bg-gradient-to-br from-forest-900 via-forest-900 to-forest-800/20"></div>
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(249,115,22,0.1),transparent_70%)]"></div>

    <!-- Animated Background Elements -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-orange-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-forest-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
    </div>

    <!-- Main Content -->
    <div class="relative z-10 max-w-6xl mx-auto px-6 text-center">
      <!-- Main Headline -->
      <h1 class="text-5xl md:text-7xl font-bold mb-6 leading-tight">
        Your
        <span class="bg-gradient-to-r from-orange-500 via-forest-400 to-orange-500 bg-clip-text text-transparent animate-gradient">
          Agent Team
        </span>
        <br />
        for YouTube Growth
      </h1>

      <!-- Subheadline -->
      <p class="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
        Join the waitlist for the agent-powered platform that helps creators
        <span class="text-orange-400 font-semibold">optimize content</span>,
        <span class="text-forest-400 font-semibold">analyze performance</span>, and
        <span class="text-orange-400 font-semibold">scale their channels</span>
        with a team of specialized agents.
      </p>

      <!-- Key Benefits -->
      <div class="flex flex-wrap justify-center gap-4 mb-12">
        <div class="flex items-center space-x-2 bg-gray-800/50 px-4 py-2 rounded-full">
          <div class="w-2 h-2 bg-green-400 rounded-full"></div>
          <span class="text-sm text-gray-300">5 Agent Specialists</span>
        </div>
        <div class="flex items-center space-x-2 bg-forest-800/50 px-4 py-2 rounded-full">
          <div class="w-2 h-2 bg-forest-400 rounded-full"></div>
          <span class="text-sm text-gray-300">Real-time Analytics</span>
        </div>
        <div class="flex items-center space-x-2 bg-forest-800/50 px-4 py-2 rounded-full">
          <div class="w-2 h-2 bg-orange-400 rounded-full"></div>
          <span class="text-sm text-gray-300">Content Optimization</span>
        </div>
        <div class="flex items-center space-x-2 bg-forest-800/50 px-4 py-2 rounded-full">
          <div class="w-2 h-2 bg-forest-400 rounded-full"></div>
          <span class="text-sm text-gray-300">Strategy Planning</span>
        </div>
      </div>

      <!-- Waitlist Form -->
      <div id="waitlist" class="max-w-md mx-auto">
        <WaitlistForm />
      </div>

      <!-- Social Proof -->
      <div class="mt-12 text-center">
        <p class="text-gray-400 text-sm mb-4">Join {{ waitlistCount.toLocaleString() }}+ creators already on the waitlist</p>
        <div class="flex justify-center items-center space-x-8 opacity-60">
          <!-- Creator Avatars -->
          <div class="flex -space-x-2">
            <div class="w-8 h-8 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full border-2 border-background"></div>
            <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full border-2 border-background"></div>
            <div class="w-8 h-8 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full border-2 border-background"></div>
            <div class="w-8 h-8 bg-gradient-to-r from-orange-500 to-red-500 rounded-full border-2 border-background"></div>
            <div class="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full border-2 border-background flex items-center justify-center text-xs font-bold">
              +
            </div>
          </div>
        </div>
      </div>

      <!-- Scroll Indicator -->
      <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
        </svg>
      </div>
    </div>
  </section>
</template>

<script setup>
// Reactive waitlist count (you can connect this to your backend later)
const waitlistCount = ref(1247)

// Animate the gradient text
onMounted(() => {
  // Add any additional animations or effects here
})
</script>

<style scoped>
@keyframes gradient {
  0%, 100% {
    background-size: 200% 200%;
    background-position: left center;
  }
  50% {
    background-size: 200% 200%;
    background-position: right center;
  }
}

.animate-gradient {
  animation: gradient 3s ease infinite;
}
</style>
