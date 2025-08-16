<template>
  <div :class="cardClasses">
    <div v-if="$slots.header" class="card-header">
      <slot name="header" />
    </div>
    
    <div class="card-content">
      <slot />
    </div>
    
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'default' | 'glass' | 'elevated'
  hoverable?: boolean
  padding?: 'none' | 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  hoverable: false,
  padding: 'md',
})

const cardClasses = computed(() => [
  {
    'card': props.variant === 'default',
    'card-glass': props.variant === 'glass',
    'card card-elevated': props.variant === 'elevated',
    'card-hover': props.hoverable,
  },
  // Custom padding classes
  {
    'p-0': props.padding === 'none',
    'p-3': props.padding === 'sm',
    'p-6': props.padding === 'md',
    'p-8': props.padding === 'lg',
  }
])
</script>

<style scoped>
.card-header {
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--color-border);
}

.card-content {
  flex: 1;
}

.card-footer {
  margin-top: var(--space-4);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border);
}

/* Override padding when using custom padding */
.p-0 .card-header,
.p-0 .card-footer {
  margin: 0;
  padding: var(--space-4);
}

.p-0 .card-header {
  border-bottom: 1px solid var(--color-border);
}

.p-0 .card-footer {
  border-top: 1px solid var(--color-border);
}

.p-0 .card-content {
  padding: var(--space-4);
}
</style>
