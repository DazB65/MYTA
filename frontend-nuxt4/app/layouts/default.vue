<template>
  <div class="min-h-screen bg-gradient-to-b from-slate-800 via-gray-850 to-gray-900 text-white">
    <!-- Unified Header -->
    <UnifiedHeader />

    <!-- Main Content -->
    <main class="pt-40">
      <slot />
    </main>
  </div>
</template>

<script setup>
// Layout-specific logic can go here
</script>

<style scoped>
/* Layout-specific styles */
</style>
