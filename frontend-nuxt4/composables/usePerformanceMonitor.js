/**
 * Performance monitoring composable for Core Web Vitals and user experience metrics
 * Tracks LCP, FID, CLS, and other performance indicators
 */
import { onMounted, onUnmounted, readonly, ref } from 'vue'

export const usePerformanceMonitor = () => {
  // Performance metrics state
  const metrics = ref({
    lcp: null,        // Largest Contentful Paint
    fid: null,        // First Input Delay
    cls: null,        // Cumulative Layout Shift
    fcp: null,        // First Contentful Paint
    ttfb: null,       // Time to First Byte
    navigationTiming: null,
    resourceTiming: [],
    memoryUsage: null,
    connectionType: null
  })

  const isSupported = ref(false)
  const isMonitoring = ref(false)

  // Performance observer for Core Web Vitals
  let performanceObserver = null
  let memoryMonitorInterval = null

  // Initialize performance monitoring
  const initializeMonitoring = () => {
    if (typeof window === 'undefined') return

    isSupported.value = 'PerformanceObserver' in window
    if (!isSupported.value) return

    isMonitoring.value = true

    // Monitor Core Web Vitals
    try {
      performanceObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          switch (entry.entryType) {
            case 'largest-contentful-paint':
              metrics.value.lcp = Math.round(entry.startTime)
              break
            case 'first-input':
              metrics.value.fid = Math.round(entry.processingStart - entry.startTime)
              break
            case 'layout-shift':
              if (!entry.hadRecentInput) {
                metrics.value.cls = (metrics.value.cls || 0) + entry.value
              }
              break
            case 'paint':
              if (entry.name === 'first-contentful-paint') {
                metrics.value.fcp = Math.round(entry.startTime)
              }
              break
            case 'navigation':
              metrics.value.ttfb = Math.round(entry.responseStart - entry.requestStart)
              metrics.value.navigationTiming = {
                domContentLoaded: Math.round(entry.domContentLoadedEventEnd - entry.domContentLoadedEventStart),
                loadComplete: Math.round(entry.loadEventEnd - entry.loadEventStart),
                domInteractive: Math.round(entry.domInteractive - entry.fetchStart),
                redirectTime: Math.round(entry.redirectEnd - entry.redirectStart),
                dnsTime: Math.round(entry.domainLookupEnd - entry.domainLookupStart),
                connectTime: Math.round(entry.connectEnd - entry.connectStart),
                requestTime: Math.round(entry.responseEnd - entry.requestStart)
              }
              break
            case 'resource':
              // Track critical resources only
              if (entry.name.includes('.js') || entry.name.includes('.css') || entry.name.includes('.woff')) {
                metrics.value.resourceTiming.push({
                  name: entry.name.split('/').pop(),
                  duration: Math.round(entry.duration),
                  size: entry.transferSize || 0,
                  type: entry.initiatorType
                })
              }
              break
          }
        }
      })

      // Observe different performance entry types
      const entryTypes = ['largest-contentful-paint', 'first-input', 'layout-shift', 'paint', 'navigation', 'resource']
      
      entryTypes.forEach(type => {
        try {
          performanceObserver.observe({ entryTypes: [type] })
        } catch (e) {
          // Some entry types might not be supported
          console.warn(`Performance entry type '${type}' not supported`)
        }
      })

    } catch (error) {
      console.warn('Performance monitoring initialization failed:', error)
    }

    // Monitor memory usage (if available)
    if ('memory' in performance) {
      memoryMonitorInterval = setInterval(() => {
        metrics.value.memoryUsage = {
          used: Math.round(performance.memory.usedJSHeapSize / 1024 / 1024), // MB
          total: Math.round(performance.memory.totalJSHeapSize / 1024 / 1024), // MB
          limit: Math.round(performance.memory.jsHeapSizeLimit / 1024 / 1024) // MB
        }
      }, 5000)
    }

    // Monitor connection type
    if ('connection' in navigator) {
      metrics.value.connectionType = {
        effectiveType: navigator.connection.effectiveType,
        downlink: navigator.connection.downlink,
        rtt: navigator.connection.rtt,
        saveData: navigator.connection.saveData
      }
    }
  }

  // Get performance score based on Core Web Vitals
  const getPerformanceScore = () => {
    const { lcp, fid, cls } = metrics.value
    
    if (!lcp && !fid && !cls) return null

    let score = 100
    
    // LCP scoring (Good: <2.5s, Needs Improvement: 2.5-4s, Poor: >4s)
    if (lcp) {
      if (lcp > 4000) score -= 30
      else if (lcp > 2500) score -= 15
    }
    
    // FID scoring (Good: <100ms, Needs Improvement: 100-300ms, Poor: >300ms)
    if (fid) {
      if (fid > 300) score -= 25
      else if (fid > 100) score -= 10
    }
    
    // CLS scoring (Good: <0.1, Needs Improvement: 0.1-0.25, Poor: >0.25)
    if (cls) {
      if (cls > 0.25) score -= 25
      else if (cls > 0.1) score -= 10
    }
    
    return Math.max(0, score)
  }

  // Get performance recommendations
  const getRecommendations = () => {
    const recommendations = []
    const { lcp, fid, cls, ttfb, resourceTiming } = metrics.value

    if (lcp > 2500) {
      recommendations.push({
        type: 'lcp',
        severity: lcp > 4000 ? 'high' : 'medium',
        message: 'Largest Contentful Paint is slow. Consider optimizing images and critical resources.',
        value: `${lcp}ms`
      })
    }

    if (fid > 100) {
      recommendations.push({
        type: 'fid',
        severity: fid > 300 ? 'high' : 'medium',
        message: 'First Input Delay is high. Consider reducing JavaScript execution time.',
        value: `${fid}ms`
      })
    }

    if (cls > 0.1) {
      recommendations.push({
        type: 'cls',
        severity: cls > 0.25 ? 'high' : 'medium',
        message: 'Cumulative Layout Shift is high. Ensure images and ads have dimensions.',
        value: cls.toFixed(3)
      })
    }

    if (ttfb > 600) {
      recommendations.push({
        type: 'ttfb',
        severity: ttfb > 1000 ? 'high' : 'medium',
        message: 'Time to First Byte is slow. Consider server optimization.',
        value: `${ttfb}ms`
      })
    }

    // Check for large resources
    const largeResources = resourceTiming.filter(resource => resource.duration > 1000)
    if (largeResources.length > 0) {
      recommendations.push({
        type: 'resources',
        severity: 'medium',
        message: `${largeResources.length} resources are loading slowly. Consider optimization.`,
        value: largeResources.map(r => r.name).join(', ')
      })
    }

    return recommendations
  }

  // Format metrics for display
  const formatMetrics = () => {
    const { lcp, fid, cls, fcp, ttfb } = metrics.value
    
    return {
      lcp: lcp ? `${lcp}ms` : 'N/A',
      fid: fid ? `${fid}ms` : 'N/A',
      cls: cls ? cls.toFixed(3) : 'N/A',
      fcp: fcp ? `${fcp}ms` : 'N/A',
      ttfb: ttfb ? `${ttfb}ms` : 'N/A'
    }
  }

  // Send metrics to analytics (placeholder)
  const sendMetrics = () => {
    if (process.env.NODE_ENV === 'production') {
      // Send to your analytics service
      console.log('Performance metrics:', metrics.value)
    }
  }

  // Cleanup
  const cleanup = () => {
    if (performanceObserver) {
      performanceObserver.disconnect()
      performanceObserver = null
    }
    
    if (memoryMonitorInterval) {
      clearInterval(memoryMonitorInterval)
      memoryMonitorInterval = null
    }
    
    isMonitoring.value = false
  }

  // Lifecycle
  onMounted(() => {
    // Delay initialization to avoid affecting initial page load
    setTimeout(initializeMonitoring, 1000)
  })

  onUnmounted(() => {
    cleanup()
  })

  return {
    metrics: readonly(metrics),
    isSupported: readonly(isSupported),
    isMonitoring: readonly(isMonitoring),
    getPerformanceScore,
    getRecommendations,
    formatMetrics,
    sendMetrics,
    cleanup
  }
}
