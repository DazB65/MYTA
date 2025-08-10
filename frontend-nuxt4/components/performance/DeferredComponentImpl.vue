<template>
  <div class="lazy-component" ref="containerRef">
    <!-- Loading Skeleton -->
    <div v-if="!isLoaded" class="loading-skeleton">
      <div class="skeleton-header">
        <div class="skeleton-avatar"></div>
        <div class="skeleton-text">
          <div class="skeleton-line short"></div>
          <div class="skeleton-line medium"></div>
        </div>
      </div>
      <div class="skeleton-content">
        <div class="skeleton-line long"></div>
        <div class="skeleton-line medium"></div>
        <div class="skeleton-line short"></div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <svg class="error-icon" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
      </svg>
      <h3>Failed to Load Component</h3>
      <p>{{ error.message || 'An error occurred while loading this component.' }}</p>
      <button class="retry-button" @click="loadComponent">
        Try Again
      </button>
    </div>

    <!-- Loaded Component -->
    <Suspense v-else>
      <component 
        :is="loadedComponent" 
        v-bind="componentProps"
        @error="handleComponentError"
      />
      <template #fallback>
        <div class="suspense-loading">
          <div class="loading-spinner"></div>
          <p>Loading component...</p>
        </div>
      </template>
    </Suspense>
  </div>
</template>

<script setup>
import { usePerformance } from '@root/composables/usePerformance'
import { onMounted, onUnmounted, ref, shallowRef, watch } from 'vue'

const props = defineProps({
  componentLoader: { type: Function, required: true },
  componentProps: { type: Object, default: () => ({}) },
  threshold: { type: Number, default: 0.1 },
  rootMargin: { type: String, default: '50px' },
  immediate: { type: Boolean, default: false },
  preload: { type: Boolean, default: false },
  priority: { type: String, default: 'normal', validator: v => ['high', 'normal', 'low'].includes(v) },
  cacheComponent: { type: Boolean, default: true },
})

const emit = defineEmits(['load', 'error', 'visible'])
const { measureComponentLoad } = usePerformance()

const containerRef = ref(null)
const isLoaded = ref(false)
const isVisible = ref(false)
const loadedComponent = shallowRef(null)
const error = ref(null)
const loadStartTime = ref(0)

let observer = null
const componentCache = new Map()

const loadComponent = async () => {
  if (isLoaded.value && !error.value) return
  try {
    error.value = null
    loadStartTime.value = performance.now()

    const cacheKey = props.componentLoader.toString()
    if (props.cacheComponent && componentCache.has(cacheKey)) {
      loadedComponent.value = componentCache.get(cacheKey)
      isLoaded.value = true
      const loadTime = performance.now() - loadStartTime.value
      emit('load', { cached: true, loadTime })
      return
    }

    const component = await props.componentLoader()
    const componentDefinition = component.default || component
    if (!componentDefinition) throw new Error('Component loader must return a valid component definition')

    if (props.cacheComponent) componentCache.set(cacheKey, componentDefinition)

    loadedComponent.value = componentDefinition
    isLoaded.value = true

    const loadTime = performance.now() - loadStartTime.value
    const measureEnd = measureComponentLoad('DeferredComponent', loadStartTime.value)
    measureEnd()
    emit('load', { cached: false, loadTime })
  } catch (err) {
    error.value = err
    emit('error', err)
  }
}

const handleComponentError = (err) => {
  error.value = err
  emit('error', err)
}

const setupObserver = () => {
  if (!containerRef.value || typeof window === 'undefined' || !('IntersectionObserver' in window)) {
    if (!props.immediate) setTimeout(loadComponent, 100)
    return
  }
  const options = { threshold: props.threshold, rootMargin: props.rootMargin }
  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        isVisible.value = true
        emit('visible')
        const loadDelay = getLoadDelay(props.priority)
        setTimeout(loadComponent, loadDelay)
        observer.disconnect()
      }
    })
  }, options)
  observer.observe(containerRef.value)
}

const getLoadDelay = (priority) => ({ high: 0, normal: 50, low: 200 }[priority] ?? 50)

const preloadComponent = () => {
  if (props.preload && !isLoaded.value) setTimeout(loadComponent, 1000)
}

onMounted(() => {
  if (props.immediate) loadComponent()
  else setupObserver()
  preloadComponent()
})

onUnmounted(() => {
  if (observer) observer.disconnect()
})

watch(() => props.componentLoader, () => {
  if (isVisible.value || props.immediate) {
    isLoaded.value = false
    loadedComponent.value = null
    error.value = null
    loadComponent()
  }
})
</script>

<style scoped>
.lazy-component { min-height: 100px; width: 100%; }
.loading-skeleton { padding: 20px; background: #f8f9fa; border-radius: 12px; animation: pulse 1.5s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.7} }
.skeleton-header { display:flex; align-items:center; gap:12px; margin-bottom:16px; }
.skeleton-avatar { width:48px; height:48px; background:#e5e7eb; border-radius:50%; }
.skeleton-text .skeleton-line { height:12px; background:#e5e7eb; border-radius:6px; margin:6px 0; }
.skeleton-text .short { width:40%; }
.skeleton-text .medium { width:70%; }
.skeleton-content .long { width:100%; height:14px; background:#e5e7eb; border-radius:6px; margin:8px 0; }
.skeleton-content .medium { width:80%; height:14px; background:#e5e7eb; border-radius:6px; margin:8px 0; }
.skeleton-content .short { width:60%; height:14px; background:#e5e7eb; border-radius:6px; margin:8px 0; }
.suspense-loading { text-align:center; padding:20px; }
.loading-spinner { width:32px; height:32px; border:3px solid #e5e7eb; border-top-color:#3b82f6; border-radius:50%; animation: spin 1s linear infinite; margin:0 auto 10px; }
@keyframes spin { from{transform:rotate(0)} to{transform:rotate(360deg)} }
.error-state { padding:20px; border:1px solid #fee2e2; background:#fef2f2; color:#991b1b; border-radius:12px; }
.error-icon { width:24px; height:24px; margin-bottom:8px; }
.retry-button { margin-top:10px; padding:8px 16px; background:#ef4444; color:white; border:none; border-radius:8px; cursor:pointer; }
</style>

