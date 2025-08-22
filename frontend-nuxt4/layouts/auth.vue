<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
    <!-- Background Pattern -->
    <div class="absolute inset-0 bg-[url('/grid-pattern.svg')] opacity-10" />
    
    <!-- Content Container -->
    <div class="relative flex min-h-screen items-center justify-center p-6">
      <!-- Auth Card -->
      <div class="w-full max-w-md">
        <!-- Logo Section -->
        <div class="mb-8 text-center">
          <div class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-pink-500">
            <span class="text-2xl">✨</span>
          </div>
          <h1 class="text-3xl font-bold text-white">MYTA</h1>
          <p class="text-gray-400">Your AI Agent for Content and Growth</p>
        </div>
        
        <!-- Auth Content -->
        <div class="rounded-2xl bg-gray-800/50 p-8 backdrop-blur-sm border border-gray-700/50">
          <slot />
        </div>
        
        <!-- Footer -->
        <div class="mt-8 text-center text-sm text-gray-400">
          <p>&copy; 2025 MYTA. All rights reserved.</p>
        </div>
      </div>
    </div>
    
    <!-- Floating Elements -->
    <div class="absolute top-10 left-10 h-20 w-20 rounded-full bg-pink-500/20 blur-xl" />
    <div class="absolute bottom-10 right-10 h-32 w-32 rounded-full bg-purple-500/20 blur-xl" />
    <div class="absolute top-1/2 right-20 h-16 w-16 rounded-full bg-blue-500/20 blur-xl" />
  </div>
</template>

<script setup>
// Auth layout specific configuration
useHead({
  titleTemplate: '%s - MYTA Auth',
  meta: [
    { name: 'robots', content: 'noindex, nofollow' }
  ]
})
</script>

<style scoped>
/* Auth layout animations */
.auth-enter-active,
.auth-leave-active {
  transition: all 0.4s ease;
}

.auth-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.auth-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
