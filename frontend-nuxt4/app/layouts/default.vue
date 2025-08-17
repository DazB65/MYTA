<template>
  <div class="min-h-screen bg-background">
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
