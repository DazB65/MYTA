<template>
  <span :class="badgeClasses">
    <slot name="icon" />
    <slot />
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'error'
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
})

const badgeClasses = computed(() => [
  'badge',
  `badge-${props.variant}`,
  {
    'text-xs px-2 py-1': props.size === 'sm',
    'text-sm px-3 py-1': props.size === 'md',
    'text-base px-4 py-2': props.size === 'lg',
  },
])
</script>

<style scoped>
.badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  border-radius: var(--radius-md);
  font-weight: var(--font-weight-medium);
  line-height: 1;
  white-space: nowrap;
}
</style>
