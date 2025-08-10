/**
 * Performance optimization composable
 * Provides caching, lazy loading, and performance monitoring utilities
 */
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'

export const usePerformance = () => {
  // Performance metrics
  const metrics = reactive({
    pageLoadTime: 0,
    componentLoadTime: 0,
    apiResponseTimes: {},
    memoryUsage: 0,
    cacheHitRate: 0,
    renderTime: 0
  })

  // Cache management
  const cache = reactive(new Map())
  const cacheStats = reactive({
    hits: 0,
    misses: 0,
    sets: 0,
    evictions: 0
  })

  // Performance monitoring
  const performanceObserver = ref(null)
  const isPerformanceSupported = ref(typeof window !== 'undefined' && 'performance' in window)

  // Cache configuration
  const CACHE_CONFIG = {
    maxSize: 100,
    defaultTTL: 5 * 60 * 1000, // 5 minutes
    analytics: {
      overview: 5 * 60 * 1000,     // 5 minutes
      channelHealth: 10 * 60 * 1000, // 10 minutes
      revenue: 15 * 60 * 1000,     // 15 minutes
      charts: 10 * 60 * 1000       // 10 minutes
    }
  }

  /**
   * Advanced caching with TTL and LRU eviction
   */
  const cacheSet = (key, value, ttl = CACHE_CONFIG.defaultTTL) => {
    // LRU eviction if cache is full
    if (cache.size >= CACHE_CONFIG.maxSize) {
      const firstKey = cache.keys().next().value
      cache.delete(firstKey)
      cacheStats.evictions++
    }

    const expiresAt = Date.now() + ttl
    cache.set(key, {
      value,
      expiresAt,
      accessedAt: Date.now(),
      hitCount: 0
    })
    
    cacheStats.sets++
  }

  const cacheGet = (key) => {
    const item = cache.get(key)
    
    if (!item) {
      cacheStats.misses++
      return null
    }

    // Check expiration
    if (Date.now() > item.expiresAt) {
      cache.delete(key)
      cacheStats.misses++
      return null
    }

    // Update access tracking
    item.accessedAt = Date.now()
    item.hitCount++
    cacheStats.hits++

    // Move to end for LRU
    cache.delete(key)
    cache.set(key, item)

    return item.value
  }

  const cacheDelete = (key) => {
    return cache.delete(key)
  }

  const cacheClear = () => {
    cache.clear()
    cacheStats.hits = 0
    cacheStats.misses = 0
    cacheStats.sets = 0
    cacheStats.evictions = 0
  }

  // Cache hit rate calculation
  const cacheHitRate = computed(() => {
    const total = cacheStats.hits + cacheStats.misses
    return total > 0 ? (cacheStats.hits / total) * 100 : 0
  })

  /**
   * API call caching wrapper
   */
  const cachedApiCall = async (key, apiFunction, options = {}) => {
    const {
      ttl = CACHE_CONFIG.defaultTTL,
      forceRefresh = false,
      cacheType = 'default'
    } = options

    // Use specific TTL for analytics data
    const finalTTL = CACHE_CONFIG.analytics[cacheType] || ttl

    const startTime = performance.now()
    
    // Check cache first
    if (!forceRefresh) {
      const cached = cacheGet(key)
      if (cached) {
        return cached
      }
    }

    try {
      // Make API call
      const result = await apiFunction()
      const endTime = performance.now()
      
      // Track API response time
      metrics.apiResponseTimes[key] = Math.round(endTime - startTime)
      
      // Cache successful results
      if (result && result.status !== 'error') {
        cacheSet(key, result, finalTTL)
      }
      
      return result
    } catch (error) {
      const endTime = performance.now()
      metrics.apiResponseTimes[key] = Math.round(endTime - startTime)
      throw error
    }
  }

  /**
   * Debounced function wrapper
   */
  const debounce = (func, delay = 300) => {
    let timeoutId
    return (...args) => {
      clearTimeout(timeoutId)
      timeoutId = setTimeout(() => func.apply(null, args), delay)
    }
  }

  /**
   * Throttled function wrapper
   */
  const throttle = (func, limit = 100) => {
    let inThrottle
    return (...args) => {
      if (!inThrottle) {
        func.apply(null, args)
        inThrottle = true
        setTimeout(() => inThrottle = false, limit)
      }
    }
  }

  /**
   * Lazy loading utility
   */
  const createLazyLoader = (loadFunction, threshold = 0.1) => {
    return new Promise((resolve) => {
      if (typeof window === 'undefined' || !('IntersectionObserver' in window)) {
        // Fallback for SSR or unsupported browsers
        resolve(loadFunction())
        return
      }

      let observer
      const element = document.createElement('div')
      element.style.height = '1px'
      
      observer = new IntersectionObserver(
        (entries) => {
          if (entries[0].isIntersecting) {
            observer.disconnect()
            resolve(loadFunction())
          }
        },
        { threshold }
      )
      
      observer.observe(element)
    })
  }

  /**
   * Memory usage monitoring
   */
  const updateMemoryUsage = () => {
    if (performance.memory) {
      metrics.memoryUsage = Math.round(
        (performance.memory.usedJSHeapSize / performance.memory.jsHeapSizeLimit) * 100
      )
    }
  }

  /**
   * Performance metrics collection
   */
  const collectPerformanceMetrics = () => {
    if (!isPerformanceSupported.value) return

    // Page load time
    const navigation = performance.getEntriesByType('navigation')[0]
    if (navigation) {
      metrics.pageLoadTime = Math.round(navigation.loadEventEnd - navigation.loadEventStart)
    }

    // Update cache hit rate
    metrics.cacheHitRate = cacheHitRate.value

    // Memory usage
    updateMemoryUsage()

    // Render performance
    const paintEntries = performance.getEntriesByType('paint')
    const firstPaint = paintEntries.find(entry => entry.name === 'first-paint')
    if (firstPaint) {
      metrics.renderTime = Math.round(firstPaint.startTime)
    }
  }

  /**
   * Performance observer setup
   */
  const setupPerformanceObserver = () => {
    if (typeof window === 'undefined' || !('PerformanceObserver' in window)) return

    performanceObserver.value = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.entryType === 'navigation') {
          metrics.pageLoadTime = Math.round(entry.loadEventEnd - entry.loadEventStart)
        } else if (entry.entryType === 'paint' && entry.name === 'first-paint') {
          metrics.renderTime = Math.round(entry.startTime)
        }
      }
    })

    performanceObserver.value.observe({ 
      entryTypes: ['navigation', 'paint', 'resource'] 
    })
  }

  /**
   * Image lazy loading utility
   */
  const lazyLoadImage = (src, options = {}) => {
    const {
      placeholder = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIwIiBoZWlnaHQ9IjE4MCIgdmlld0JveD0iMCAwIDMyMCAxODAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+',
      errorImage = '/default-thumbnail.jpg',
      rootMargin = '50px',
      threshold = 0.1
    } = options

    return new Promise((resolve, reject) => {
      const img = new Image()
      
      img.onload = () => resolve(src)
      img.onerror = () => resolve(errorImage)
      
      // Use intersection observer for lazy loading
      if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(
          (entries) => {
            entries.forEach(entry => {
              if (entry.isIntersecting) {
                img.src = src
                observer.disconnect()
              }
            })
          },
          { rootMargin, threshold }
        )
        
        // Observe placeholder element
        const placeholder_element = document.createElement('div')
        observer.observe(placeholder_element)
      } else {
        // Fallback for unsupported browsers
        img.src = src
      }
    })
  }

  /**
   * Bundle size optimization utilities
   */
  const preloadResource = (href, type = 'script') => {
    if (typeof window === 'undefined') return

    const link = document.createElement('link')
    link.rel = 'preload'
    link.href = href
    link.as = type
    document.head.appendChild(link)
  }

  const prefetchResource = (href) => {
    if (typeof window === 'undefined') return

    const link = document.createElement('link')
    link.rel = 'prefetch'
    link.href = href
    document.head.appendChild(link)
  }

  /**
   * Component performance monitoring
   */
  const measureComponentLoad = (componentName, startTime = performance.now()) => {
    return () => {
      const endTime = performance.now()
      const loadTime = Math.round(endTime - startTime)
      metrics.componentLoadTime = loadTime
      
      console.log(`${componentName} loaded in ${loadTime}ms`)
    }
  }

  /**
   * Cleanup expired cache entries
   */
  const cleanupCache = () => {
    const now = Date.now()
    const keysToDelete = []
    
    cache.forEach((item, key) => {
      if (now > item.expiresAt) {
        keysToDelete.push(key)
      }
    })
    
    keysToDelete.forEach(key => cache.delete(key))
    return keysToDelete.length
  }

  // Lifecycle management
  onMounted(() => {
    setupPerformanceObserver()
    collectPerformanceMetrics()
    
    // Regular cache cleanup
    const cleanupInterval = setInterval(cleanupCache, 60000) // Every minute
    
    // Regular metrics update
    const metricsInterval = setInterval(collectPerformanceMetrics, 10000) // Every 10 seconds

    onUnmounted(() => {
      if (performanceObserver.value) {
        performanceObserver.value.disconnect()
      }
      clearInterval(cleanupInterval)
      clearInterval(metricsInterval)
    })
  })

  return {
    // Metrics
    metrics: readonly(metrics),
    cacheStats: readonly(cacheStats),
    cacheHitRate,
    
    // Cache management
    cacheSet,
    cacheGet,
    cacheDelete,
    cacheClear,
    cleanupCache,
    
    // API optimization
    cachedApiCall,
    
    // Function optimization
    debounce,
    throttle,
    
    // Lazy loading
    createLazyLoader,
    lazyLoadImage,
    
    // Resource optimization
    preloadResource,
    prefetchResource,
    
    // Performance monitoring
    measureComponentLoad,
    collectPerformanceMetrics,
    updateMemoryUsage
  }
}