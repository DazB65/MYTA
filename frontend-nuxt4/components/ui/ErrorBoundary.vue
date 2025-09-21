<template>
  <div>
    <!-- Error state -->
    <div 
      v-if="hasError" 
      class="error-boundary"
      :class="errorContainerClasses"
      role="alert"
      aria-live="assertive"
    >
      <div class="error-content">
        <!-- Error icon -->
        <div class="error-icon" :class="iconClasses">
          <svg 
            class="w-8 h-8" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path 
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2" 
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
            />
          </svg>
        </div>

        <!-- Error message -->
        <div class="error-text">
          <h3 class="error-title" :class="titleClasses">
            {{ errorTitle }}
          </h3>
          <p class="error-description" :class="descriptionClasses">
            {{ errorMessage }}
          </p>
          
          <!-- Error details (development only) -->
          <details v-if="showDetails && errorDetails" class="error-details mt-4">
            <summary class="cursor-pointer text-sm font-medium text-gray-600 hover:text-gray-800">
              Technical Details
            </summary>
            <pre class="mt-2 text-xs bg-gray-100 p-3 rounded overflow-auto max-h-40">{{ errorDetails }}</pre>
          </details>
        </div>

        <!-- Action buttons -->
        <div class="error-actions" :class="actionsClasses">
          <button
            v-if="showRetry"
            @click="handleRetry"
            class="btn-retry"
            :class="retryButtonClasses"
            type="button"
            :aria-describedby="retryAriaId"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Try Again
          </button>
          
          <button
            v-if="showReload"
            @click="handleReload"
            class="btn-reload"
            :class="reloadButtonClasses"
            type="button"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Reload Page
          </button>

          <button
            v-if="showReport"
            @click="handleReport"
            class="btn-report"
            :class="reportButtonClasses"
            type="button"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
            Report Issue
          </button>
        </div>
      </div>
    </div>

    <!-- Normal content -->
    <div v-else>
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  fallbackTitle?: string
  fallbackMessage?: string
  showRetry?: boolean
  showReload?: boolean
  showReport?: boolean
  showDetails?: boolean
  variant?: 'default' | 'minimal' | 'card'
  onRetry?: () => void
  onReport?: (error: Error) => void
}

const props = withDefaults(defineProps<Props>(), {
  fallbackTitle: 'Something went wrong',
  fallbackMessage: 'An unexpected error occurred. Please try again or contact support if the problem persists.',
  showRetry: true,
  showReload: false,
  showReport: false,
  showDetails: false,
  variant: 'default'
})

const emit = defineEmits<{
  retry: []
  report: [error: Error]
}>()

// Error state
const hasError = ref(false)
const error = ref<Error | null>(null)
const errorInfo = ref<any>(null)

// Computed properties
const errorTitle = computed(() => {
  if (error.value?.name === 'ChunkLoadError') {
    return 'Update Required'
  }
  return props.fallbackTitle
})

const errorMessage = computed(() => {
  if (error.value?.name === 'ChunkLoadError') {
    return 'The application has been updated. Please refresh the page to get the latest version.'
  }
  return props.fallbackMessage
})

const errorDetails = computed(() => {
  if (!error.value) return null
  return `${error.value.name}: ${error.value.message}\n${error.value.stack || ''}`
})

const retryAriaId = computed(() => `retry-${Math.random().toString(36).substr(2, 9)}`)

// Styling classes
const errorContainerClasses = computed(() => {
  const base = 'flex items-center justify-center min-h-[200px] p-6'
  const variants = {
    default: 'bg-red-50 border border-red-200 rounded-lg',
    minimal: 'bg-gray-50 rounded',
    card: 'bg-white border border-gray-200 rounded-lg shadow-sm'
  }
  return [base, variants[props.variant]].join(' ')
})

const iconClasses = computed(() => {
  const variants = {
    default: 'text-red-500',
    minimal: 'text-gray-400',
    card: 'text-red-500'
  }
  return variants[props.variant]
})

const titleClasses = computed(() => {
  const base = 'text-lg font-semibold mb-2'
  const variants = {
    default: 'text-red-800',
    minimal: 'text-gray-800',
    card: 'text-gray-900'
  }
  return [base, variants[props.variant]].join(' ')
})

const descriptionClasses = computed(() => {
  const base = 'text-sm'
  const variants = {
    default: 'text-red-600',
    minimal: 'text-gray-600',
    card: 'text-gray-600'
  }
  return [base, variants[props.variant]].join(' ')
})

const actionsClasses = computed(() => {
  return 'flex flex-wrap gap-3 mt-4'
})

const retryButtonClasses = computed(() => {
  return 'inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors'
})

const reloadButtonClasses = computed(() => {
  return 'inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors'
})

const reportButtonClasses = computed(() => {
  return 'inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors'
})

// Error handling methods
const captureError = (err: Error, info?: any) => {
  hasError.value = true
  error.value = err
  errorInfo.value = info
  
  // Log error for debugging
  console.error('Error Boundary caught an error:', err)
  if (info) {
    console.error('Error Info:', info)
  }
  
  // Report to error tracking service
  if (process.client && window.gtag) {
    window.gtag('event', 'exception', {
      description: err.message,
      fatal: false
    })
  }
}

const handleRetry = () => {
  hasError.value = false
  error.value = null
  errorInfo.value = null
  
  if (props.onRetry) {
    props.onRetry()
  } else {
    emit('retry')
  }
}

const handleReload = () => {
  if (process.client) {
    window.location.reload()
  }
}

const handleReport = () => {
  if (error.value) {
    if (props.onReport) {
      props.onReport(error.value)
    } else {
      emit('report', error.value)
    }
  }
}

// Global error handler
onMounted(() => {
  if (process.client) {
    window.addEventListener('error', (event) => {
      captureError(new Error(event.message), {
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno
      })
    })
    
    window.addEventListener('unhandledrejection', (event) => {
      captureError(new Error(event.reason), {
        type: 'unhandledrejection'
      })
    })
  }
})

// Expose methods for parent components
defineExpose({
  captureError,
  reset: () => {
    hasError.value = false
    error.value = null
    errorInfo.value = null
  }
})
</script>

<style scoped>
.error-boundary {
  isolation: isolate;
}

.error-content {
  text-align: center;
  max-width: 500px;
}

.error-icon {
  margin: 0 auto 1rem;
  width: fit-content;
}

.error-details summary {
  outline: none;
}

.error-details summary:focus {
  @apply ring-2 ring-blue-500 ring-offset-2 rounded;
}

.btn-retry:focus,
.btn-reload:focus,
.btn-report:focus {
  outline: none;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .error-boundary {
    border-width: 2px;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .btn-retry,
  .btn-reload,
  .btn-report {
    transition: none;
  }
}
</style>
