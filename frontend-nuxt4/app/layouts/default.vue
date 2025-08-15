<template>
  <div class="min-h-screen bg-gray-900">
    <!-- Header -->
    <AppHeader />
    
    <!-- Main Content -->
    <main class="pt-16">
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
