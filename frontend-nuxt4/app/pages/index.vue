<script setup lang="ts">
// Check authentication before redirecting
const authStore = useAuthStore()

// Initialize auth if needed (client-side only)
if (process.client && !authStore.isAuthenticated) {
  await authStore.initializeAuth()
}

// Redirect based on authentication status
if (authStore.isLoggedIn) {
  await navigateTo('/dashboard', { replace: true })
} else {
  await navigateTo('/login', { replace: true })
}
</script>

<template>
  <!-- Loading state while checking authentication -->
  <div class="min-h-screen bg-gradient-to-b from-slate-800 via-gray-850 to-gray-900 flex items-center justify-center">
    <div class="text-center">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mb-4"></div>
      <p class="text-gray-400">Loading...</p>
    </div>
  </div>
</template>
