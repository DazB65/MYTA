<template>
  <button
    :class="[
      'relative transition-all duration-150 ease-in-out',
      'disabled:opacity-50 disabled:cursor-not-allowed',
      buttonClass
    ]"
    :disabled="loading || disabled"
    @click="handleClick"
  >
    <!-- Loading Spinner -->
    <div
      v-if="loading"
      class="absolute inset-0 flex items-center justify-center"
    >
      <svg
        class="animate-spin h-4 w-4 text-current"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        ></circle>
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>
    </div>

    <!-- Button Content -->
    <span :class="{ 'opacity-0': loading }">
      <slot />
    </span>
  </button>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  buttonClass: {
    type: String,
    default: ''
  },
  loadingDuration: {
    type: Number,
    default: 800 // milliseconds
  }
})

const emit = defineEmits(['click'])

const isLoading = ref(false)

const handleClick = async (event) => {
  if (props.loading || isLoading.value) return
  
  // Show loading state
  isLoading.value = true
  
  // Emit click event
  emit('click', event)
  
  // Auto-hide loading after duration (for demo purposes)
  setTimeout(() => {
    isLoading.value = false
  }, props.loadingDuration)
}

// Computed loading state
const loading = computed(() => props.loading || isLoading.value)
</script>

<style scoped>
/* Smooth transitions for all button states */
button {
  transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Ensure spinner is perfectly centered */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
