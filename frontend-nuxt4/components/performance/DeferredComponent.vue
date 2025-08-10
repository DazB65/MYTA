<template>
  <DeferredComponentImpl v-bind="$attrs" />
</template>

<script setup>
// Thin wrapper to avoid using the reserved "Lazy" prefix directly in templates
import DeferredComponentImpl from './DeferredComponentImpl.vue';
</script>
