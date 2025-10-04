<template>
  <div class="performance-monitor" :class="{ expanded: isExpanded }">
    <!-- Toggle Button -->
    <button class="performance-toggle" @click="isExpanded = !isExpanded">
      <svg class="icon" viewBox="0 0 20 20" fill="currentColor">
        <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>Performance</span>
      <div class="performance-indicator" :class="performanceStatus"/>
    </button>

    <!-- Performance Details Panel -->
    <div v-if="isExpanded" class="performance-panel">
      <div class="panel-header">
        <h3>Performance Monitor</h3>
        <button class="close-button" @click="isExpanded = false">
          <svg viewBox="0 0 20 20" fill="currentColor">
            <path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
        </button>
      </div>

      <!-- Performance Metrics -->
      <div class="metrics-grid">
        <!-- Page Performance -->
        <div class="metric-card">
          <div class="metric-header">
            <svg class="metric-icon" viewBox="0 0 20 20" fill="currentColor">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="metric-title">Page Load</span>
          </div>
          <div class="metric-value">{{ formatTime(metrics.pageLoadTime) }}</div>
          <div class="metric-status" :class="getLoadTimeStatus(metrics.pageLoadTime)">
            {{ getLoadTimeLabel(metrics.pageLoadTime) }}
          </div>
        </div>

        <!-- API Response Times -->
        <div class="metric-card">
          <div class="metric-header">
            <svg class="metric-icon" viewBox="0 0 20 20" fill="currentColor">
              <path
                d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"
              />
            </svg>
            <span class="metric-title">API Response</span>
          </div>
          <div class="metric-value">{{ formatTime(averageApiTime) }}</div>
          <div class="metric-status" :class="getApiTimeStatus(averageApiTime)">
            {{ getApiTimeLabel(averageApiTime) }}
          </div>
        </div>

        <!-- Cache Performance -->
        <div class="metric-card">
          <div class="metric-header">
            <svg class="metric-icon" viewBox="0 0 20 20" fill="currentColor">
              <path
                d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
              />
            </svg>
            <span class="metric-title">Cache Hit Rate</span>
          </div>
          <div class="metric-value">{{ formatPercentage(cacheHitRate) }}</div>
          <div class="metric-status" :class="getCacheStatus(cacheHitRate)">
            {{ getCacheLabel(cacheHitRate) }}
          </div>
        </div>

        <!-- Memory Usage -->
        <div v-if="metrics.memoryUsage > 0" class="metric-card">
          <div class="metric-header">
            <svg class="metric-icon" viewBox="0 0 20 20" fill="currentColor">
              <path
                d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"
              />
            </svg>
            <span class="metric-title">Memory Usage</span>
          </div>
          <div class="metric-value">{{ formatPercentage(metrics.memoryUsage) }}</div>
          <div class="metric-status" :class="getMemoryStatus(metrics.memoryUsage)">
            {{ getMemoryLabel(metrics.memoryUsage) }}
          </div>
        </div>
      </div>

      <!-- Cache Statistics -->
      <div class="cache-stats">
        <h4>Cache Statistics</h4>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-label">Total Requests</span>
            <span class="stat-value">{{ cacheStats.hits + cacheStats.misses }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Cache Hits</span>
            <span class="stat-value success">{{ cacheStats.hits }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Cache Misses</span>
            <span class="stat-value warning">{{ cacheStats.misses }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Cache Sets</span>
            <span class="stat-value">{{ cacheStats.sets }}</span>
          </div>
        </div>
      </div>

      <!-- API Response Times Breakdown -->
      <div v-if="Object.keys(metrics.apiResponseTimes).length > 0" class="api-breakdown">
        <h4>API Response Times</h4>
        <div class="api-list">
          <div
            v-for="(time, endpoint) in metrics.apiResponseTimes"
            :key="endpoint"
            class="api-item"
          >
            <span class="api-endpoint">{{ formatEndpoint(endpoint) }}</span>
            <span class="api-time" :class="getApiTimeStatus(time)">
              {{ formatTime(time) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Performance Actions -->
      <div class="performance-actions">
        <button class="action-button" @click="clearCache">
          <svg class="button-icon" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" clip-rule="evenodd" />
            <path
              fill-rule="evenodd"
              d="M10 5a2 2 0 00-2 2v6a2 2 0 002 2h6a2 2 0 002-2V7a2 2 0 00-2-2H4z"
              clip-rule="evenodd"
            />
          </svg>
          Clear Cache
        </button>
        <button class="action-button" @click="refreshMetrics">
          <svg class="button-icon" viewBox="0 0 20 20" fill="currentColor">
            <path
              d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
            />
          </svg>
          Refresh Metrics
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { usePerformance } from '~/composables/usePerformance'

const { metrics, cacheStats, cacheHitRate, cacheClear, collectPerformanceMetrics } =
  usePerformance()

// Component state
const isExpanded = ref(false)

// Computed properties
const averageApiTime = computed(() => {
  const times = Object.values(metrics.apiResponseTimes)
  if (times.length === 0) return 0
  return Math.round(times.reduce((sum, time) => sum + time, 0) / times.length)
})

const performanceStatus = computed(() => {
  const loadTime = metrics.pageLoadTime
  const apiTime = averageApiTime.value
  const memory = metrics.memoryUsage

  if (loadTime > 3000 || apiTime > 1000 || memory > 80) return 'poor'
  if (loadTime > 1500 || apiTime > 500 || memory > 60) return 'fair'
  return 'good'
})

// Utility functions
const formatTime = milliseconds => {
  if (milliseconds === 0) return '0ms'
  if (milliseconds < 1000) return `${milliseconds}ms`
  return `${(milliseconds / 1000).toFixed(1)}s`
}

const formatPercentage = value => {
  return `${Math.round(value)}%`
}

const formatEndpoint = endpoint => {
  return endpoint.replace(/^.*:/, '').replace(/:\d+$/, '')
}

// Status classification functions
const getLoadTimeStatus = time => {
  if (time === 0) return 'unknown'
  if (time > 3000) return 'poor'
  if (time > 1500) return 'fair'
  return 'good'
}

const getLoadTimeLabel = time => {
  if (time === 0) return 'Unknown'
  if (time > 3000) return 'Slow'
  if (time > 1500) return 'Fair'
  return 'Fast'
}

const getApiTimeStatus = time => {
  if (time === 0) return 'unknown'
  if (time > 1000) return 'poor'
  if (time > 500) return 'fair'
  return 'good'
}

const getApiTimeLabel = time => {
  if (time === 0) return 'Unknown'
  if (time > 1000) return 'Slow'
  if (time > 500) return 'Fair'
  return 'Fast'
}

const getCacheStatus = rate => {
  if (rate === 0) return 'unknown'
  if (rate < 50) return 'poor'
  if (rate < 80) return 'fair'
  return 'good'
}

const getCacheLabel = rate => {
  if (rate === 0) return 'No Data'
  if (rate < 50) return 'Low'
  if (rate < 80) return 'Good'
  return 'Excellent'
}

const getMemoryStatus = usage => {
  if (usage === 0) return 'unknown'
  if (usage > 80) return 'poor'
  if (usage > 60) return 'fair'
  return 'good'
}

const getMemoryLabel = usage => {
  if (usage === 0) return 'Unknown'
  if (usage > 80) return 'High'
  if (usage > 60) return 'Moderate'
  return 'Low'
}

// Action handlers
const clearCache = () => {
  cacheClear()
  // Show success feedback
  console.log('Cache cleared successfully')
}

const refreshMetrics = () => {
  collectPerformanceMetrics()
  // Show success feedback
  console.log('Performance metrics refreshed')
}

// Auto-refresh metrics
let metricsInterval
onMounted(() => {
  collectPerformanceMetrics()
  metricsInterval = setInterval(collectPerformanceMetrics, 5000) // Every 5 seconds
})

onUnmounted(() => {
  if (metricsInterval) {
    clearInterval(metricsInterval)
  }
})
</script>

<style scoped>
.performance-monitor {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.performance-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #1f2937;
  color: white;
  border: none;
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.2s;
  font-size: 14px;
  font-weight: 500;
}

.performance-toggle:hover {
  background: #374151;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.icon {
  width: 16px;
  height: 16px;
}

.performance-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.performance-indicator.good {
  background: #10b981;
}

.performance-indicator.fair {
  background: #f59e0b;
}

.performance-indicator.poor {
  background: #ef4444;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.performance-panel {
  position: absolute;
  bottom: 60px;
  right: 0;
  width: 400px;
  max-height: 600px;
  overflow-y: auto;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  border: 1px solid #e5e7eb;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.panel-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s;
}

.close-button:hover {
  background: #f3f4f6;
  color: #374151;
}

.close-button svg {
  width: 16px;
  height: 16px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  padding: 20px;
}

.metric-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
}

.metric-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-bottom: 12px;
}

.metric-icon {
  width: 16px;
  height: 16px;
  color: #6b7280;
}

.metric-title {
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
}

.metric-value {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.metric-status {
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 2px 6px;
  border-radius: 4px;
}

.metric-status.good {
  background: #dcfce7;
  color: #166534;
}

.metric-status.fair {
  background: #fef3c7;
  color: #92400e;
}

.metric-status.poor {
  background: #fef2f2;
  color: #dc2626;
}

.metric-status.unknown {
  background: #f3f4f6;
  color: #6b7280;
}

.cache-stats,
.api-breakdown {
  padding: 20px;
  border-top: 1px solid #e5e7eb;
}

.cache-stats h4,
.api-breakdown h4 {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 12px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
}

.stat-value {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.stat-value.success {
  color: #10b981;
}

.stat-value.warning {
  color: #f59e0b;
}

.api-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.api-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.api-endpoint {
  font-size: 12px;
  color: #6b7280;
  font-family: monospace;
}

.api-time {
  font-size: 12px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}

.api-time.good {
  background: #dcfce7;
  color: #166534;
}

.api-time.fair {
  background: #fef3c7;
  color: #92400e;
}

.api-time.poor {
  background: #fef2f2;
  color: #dc2626;
}

.performance-actions {
  padding: 16px 20px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.action-button:hover {
  background: #e5e7eb;
}

.button-icon {
  width: 14px;
  height: 14px;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .performance-monitor {
    bottom: 10px;
    right: 10px;
  }

  .performance-panel {
    width: 320px;
    max-height: 500px;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
