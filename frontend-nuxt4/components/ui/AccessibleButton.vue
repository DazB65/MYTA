<template>
  <component
    :is="tag"
    :type="tag === 'button' ? type : undefined"
    :href="tag === 'a' ? href : undefined"
    :to="tag === 'NuxtLink' ? to : undefined"
    :disabled="disabled || loading"
    :aria-label="ariaLabel"
    :aria-describedby="ariaDescribedby"
    :aria-expanded="ariaExpanded"
    :aria-pressed="ariaPressed"
    :aria-controls="ariaControls"
    :class="buttonClasses"
    @click="handleClick"
    @keydown="handleKeydown"
    v-bind="$attrs"
  >
    <!-- Loading spinner -->
    <LoadingSpinner
      v-if="loading"
      size="sm"
      :variant="loadingSpinnerVariant"
      class="mr-2"
      :aria-hidden="true"
    />
    
    <!-- Icon (left) -->
    <span
      v-if="iconLeft && !loading"
      class="icon-left"
      :class="iconLeftClasses"
      :aria-hidden="true"
    >
      <slot name="icon-left">
        <component :is="iconLeft" />
      </slot>
    </span>
    
    <!-- Button text/content -->
    <span :class="textClasses">
      <slot>{{ text }}</slot>
    </span>
    
    <!-- Icon (right) -->
    <span
      v-if="iconRight"
      class="icon-right"
      :class="iconRightClasses"
      :aria-hidden="true"
    >
      <slot name="icon-right">
        <component :is="iconRight" />
      </slot>
    </span>
    
    <!-- Screen reader text for loading state -->
    <span v-if="loading" class="sr-only">
      {{ loadingText }}
    </span>
  </component>
</template>

<script setup lang="ts">
interface Props {
  // Content
  text?: string
  
  // Behavior
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  loading?: boolean
  loadingText?: string
  
  // Navigation (for links)
  href?: string
  to?: string | object
  external?: boolean
  
  // Styling
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'success'
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  fullWidth?: boolean
  rounded?: boolean
  
  // Icons
  iconLeft?: string | object
  iconRight?: string | object
  
  // Accessibility
  ariaLabel?: string
  ariaDescribedby?: string
  ariaExpanded?: boolean
  ariaPressed?: boolean
  ariaControls?: string
  
  // Events
  onClick?: (event: Event) => void
}

const props = withDefaults(defineProps<Props>(), {
  type: 'button',
  variant: 'primary',
  size: 'md',
  loadingText: 'Loading...',
  disabled: false,
  loading: false,
  fullWidth: false,
  rounded: false,
  external: false
})

const emit = defineEmits<{
  click: [event: Event]
}>()

// Determine the component tag
const tag = computed(() => {
  if (props.href) {
    return props.external ? 'a' : 'NuxtLink'
  }
  return 'button'
})

// Base button classes
const baseClasses = 'inline-flex items-center justify-center font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'

// Size classes
const sizeClasses = computed(() => {
  const sizes = {
    xs: 'px-2.5 py-1.5 text-xs',
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-4 py-2 text-base',
    xl: 'px-6 py-3 text-base'
  }
  return sizes[props.size]
})

// Variant classes
const variantClasses = computed(() => {
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500 active:bg-blue-800',
    secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500 active:bg-gray-800',
    outline: 'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 focus:ring-blue-500 active:bg-gray-100',
    ghost: 'text-gray-700 hover:bg-gray-100 focus:ring-gray-500 active:bg-gray-200',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500 active:bg-red-800',
    success: 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500 active:bg-green-800'
  }
  return variants[props.variant]
})

// Shape classes
const shapeClasses = computed(() => {
  return props.rounded ? 'rounded-full' : 'rounded-md'
})

// Width classes
const widthClasses = computed(() => {
  return props.fullWidth ? 'w-full' : ''
})

// Combined button classes
const buttonClasses = computed(() => {
  return [
    baseClasses,
    sizeClasses.value,
    variantClasses.value,
    shapeClasses.value,
    widthClasses.value
  ].filter(Boolean).join(' ')
})

// Icon classes
const iconLeftClasses = computed(() => {
  const spacing = props.text || $slots.default ? 'mr-2' : ''
  return `w-4 h-4 ${spacing}`
})

const iconRightClasses = computed(() => {
  const spacing = props.text || $slots.default ? 'ml-2' : ''
  return `w-4 h-4 ${spacing}`
})

// Text classes for loading state
const textClasses = computed(() => {
  return props.loading ? 'opacity-75' : ''
})

// Loading spinner variant based on button variant
const loadingSpinnerVariant = computed(() => {
  const darkVariants = ['primary', 'secondary', 'danger', 'success']
  return darkVariants.includes(props.variant) ? 'white' : 'gray'
})

// Event handlers
const handleClick = (event: Event) => {
  if (props.disabled || props.loading) {
    event.preventDefault()
    return
  }
  
  if (props.onClick) {
    props.onClick(event)
  }
  
  emit('click', event)
}

const handleKeydown = (event: KeyboardEvent) => {
  // Handle Enter and Space keys for better accessibility
  if (event.key === 'Enter' || event.key === ' ') {
    if (tag.value === 'a' || tag.value === 'NuxtLink') {
      // Let the default behavior handle navigation
      return
    }
    
    event.preventDefault()
    handleClick(event)
  }
}

// Expose methods for parent components
defineExpose({
  focus: () => {
    const el = getCurrentInstance()?.proxy?.$el
    if (el && el.focus) {
      el.focus()
    }
  },
  blur: () => {
    const el = getCurrentInstance()?.proxy?.$el
    if (el && el.blur) {
      el.blur()
    }
  }
})
</script>

<style scoped>
/* High contrast mode support */
@media (prefers-contrast: high) {
  .inline-flex {
    border-width: 2px;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .inline-flex {
    transition: none;
  }
}

/* Focus visible for better keyboard navigation */
.inline-flex:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 2px;
}

/* Screen reader only class */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>
