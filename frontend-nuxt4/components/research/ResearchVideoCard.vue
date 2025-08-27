<template>
  <div 
    class="research-video-card"
    :style="{ 
      transform: `translate(${position.x}px, ${position.y}px)`,
      zIndex: isDragging ? 1000 : 1
    }"
    @mousedown="startDrag"
    :class="{ dragging: isDragging, analyzing: isAnalyzing }"
  >
    <!-- Card Header -->
    <div class="card-header">
      <div class="video-thumbnail">
        <img :src="video.thumbnail" :alt="video.title" />
        <div class="video-duration">{{ formatDuration(video.duration) }}</div>
        <div class="analysis-status" v-if="video.analysisStatus">
          <Icon :name="getStatusIcon(video.analysisStatus)" />
        </div>
      </div>
      <div class="card-actions">
        <button class="action-btn" @click="toggleAnalysis" :disabled="isAnalyzing">
          <Icon :name="isAnalyzing ? 'loader' : 'brain'" :class="{ 'animate-spin': isAnalyzing }" />
        </button>
        <button class="action-btn" @click="openVideoModal">
          <Icon name="external-link" />
        </button>
        <button class="action-btn danger" @click="$emit('remove', video.id)">
          <Icon name="trash" />
        </button>
      </div>
    </div>

    <!-- Video Info -->
    <div class="video-info">
      <h4 class="video-title">{{ truncateTitle(video.title) }}</h4>
      <div class="video-meta">
        <span class="channel-name">{{ video.channelName }}</span>
        <span class="video-stats">
          {{ formatViews(video.views) }} views • {{ formatDate(video.publishedAt) }}
        </span>
      </div>
    </div>

    <!-- Performance Metrics -->
    <div class="performance-metrics" v-if="video.metrics">
      <div class="metric">
        <Icon name="eye" class="metric-icon" />
        <span class="metric-value">{{ formatNumber(video.metrics.views) }}</span>
      </div>
      <div class="metric">
        <Icon name="thumbs-up" class="metric-icon" />
        <span class="metric-value">{{ formatNumber(video.metrics.likes) }}</span>
      </div>
      <div class="metric">
        <Icon name="message-circle" class="metric-icon" />
        <span class="metric-value">{{ formatNumber(video.metrics.comments) }}</span>
      </div>
      <div class="metric">
        <Icon name="share" class="metric-icon" />
        <span class="metric-value">{{ video.metrics.engagementRate }}%</span>
      </div>
    </div>

    <!-- AI Analysis Results -->
    <div class="analysis-results" v-if="video.analysis && !isAnalyzing">
      <div class="analysis-header">
        <Icon name="brain" class="analysis-icon" />
        <span class="analysis-title">AI Analysis</span>
        <div class="analysis-score" :class="getScoreClass(video.analysis.overallScore)">
          {{ video.analysis.overallScore }}/100
        </div>
      </div>
      
      <div class="analysis-insights">
        <div class="insight-item" v-for="insight in video.analysis.keyInsights" :key="insight.id">
          <Icon :name="insight.type" class="insight-icon" />
          <span class="insight-text">{{ insight.text }}</span>
        </div>
      </div>

      <div class="analysis-tags">
        <span 
          v-for="tag in video.analysis.tags" 
          :key="tag"
          class="analysis-tag"
        >
          {{ tag }}
        </span>
      </div>
    </div>

    <!-- Loading State -->
    <div class="analysis-loading" v-if="isAnalyzing">
      <div class="loading-spinner">
        <Icon name="loader" class="animate-spin" />
      </div>
      <p class="loading-text">Analyzing video content...</p>
      <div class="loading-progress">
        <div class="progress-bar" :style="{ width: `${analysisProgress}%` }"></div>
      </div>
    </div>

    <!-- Connection Points -->
    <div class="connection-points">
      <div class="connection-point top" @mousedown.stop="startConnection('top')"></div>
      <div class="connection-point right" @mousedown.stop="startConnection('right')"></div>
      <div class="connection-point bottom" @mousedown.stop="startConnection('bottom')"></div>
      <div class="connection-point left" @mousedown.stop="startConnection('left')"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { ResearchVideo } from '../../types/research'

interface Props {
  video: ResearchVideo
  position: { x: number, y: number }
}

interface Emits {
  (e: 'move', videoId: string, position: { x: number, y: number }): void
  (e: 'analyze', videoId: string): void
  (e: 'remove', videoId: string): void
  (e: 'connect', videoId: string, point: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Reactive state
const isDragging = ref(false)
const isAnalyzing = ref(false)
const analysisProgress = ref(0)
const dragOffset = ref({ x: 0, y: 0 })

// Computed properties
const truncateTitle = (title: string) => {
  return title.length > 50 ? title.substring(0, 50) + '...' : title
}

// Drag functionality
const startDrag = (event: MouseEvent) => {
  isDragging.value = true
  dragOffset.value = {
    x: event.clientX - props.position.x,
    y: event.clientY - props.position.y
  }

  const handleMouseMove = (e: MouseEvent) => {
    if (isDragging.value) {
      const newPosition = {
        x: e.clientX - dragOffset.value.x,
        y: e.clientY - dragOffset.value.y
      }
      emit('move', props.video.id, newPosition)
    }
  }

  const handleMouseUp = () => {
    isDragging.value = false
    document.removeEventListener('mousemove', handleMouseMove)
    document.removeEventListener('mouseup', handleMouseUp)
  }

  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
}

// Analysis functionality
const toggleAnalysis = async () => {
  if (isAnalyzing.value) return

  isAnalyzing.value = true
  analysisProgress.value = 0

  try {
    // Simulate analysis progress
    const progressInterval = setInterval(() => {
      analysisProgress.value += 10
      if (analysisProgress.value >= 100) {
        clearInterval(progressInterval)
      }
    }, 200)

    // Trigger actual analysis
    emit('analyze', props.video.id)

    // Wait for analysis to complete
    await new Promise(resolve => setTimeout(resolve, 2000))

  } catch (error) {
    console.error('Analysis failed:', error)
  } finally {
    isAnalyzing.value = false
    analysisProgress.value = 0
  }
}

// Connection functionality
const startConnection = (point: string) => {
  emit('connect', props.video.id, point)
}

// Utility functions
const formatDuration = (seconds: number) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

const formatViews = (views: number) => {
  if (views >= 1000000) return `${(views / 1000000).toFixed(1)}M`
  if (views >= 1000) return `${(views / 1000).toFixed(1)}K`
  return views.toString()
}

const formatNumber = (num: number) => {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toString()
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString()
}

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'completed': return 'check-circle'
    case 'analyzing': return 'loader'
    case 'failed': return 'x-circle'
    default: return 'clock'
  }
}

const getScoreClass = (score: number) => {
  if (score >= 80) return 'score-excellent'
  if (score >= 60) return 'score-good'
  if (score >= 40) return 'score-average'
  return 'score-poor'
}

const openVideoModal = () => {
  // Open video in modal or new tab
  window.open(props.video.url, '_blank')
}
</script>

<style scoped>
.research-video-card {
  @apply absolute bg-white rounded-lg shadow-lg border border-gray-200 w-80 cursor-move select-none;
  transition: transform 0.1s ease-out, box-shadow 0.2s ease;
}

.research-video-card:hover {
  @apply shadow-xl;
}

.research-video-card.dragging {
  @apply shadow-2xl scale-105;
}

.research-video-card.analyzing {
  @apply border-blue-500;
}

.card-header {
  @apply relative;
}

.video-thumbnail {
  @apply relative rounded-t-lg overflow-hidden;
}

.video-thumbnail img {
  @apply w-full h-48 object-cover;
}

.video-duration {
  @apply absolute bottom-2 right-2 bg-black bg-opacity-75 text-white text-xs px-2 py-1 rounded;
}

.analysis-status {
  @apply absolute top-2 left-2 w-6 h-6 bg-white rounded-full flex items-center justify-center;
}

.card-actions {
  @apply absolute top-2 right-2 flex space-x-1;
}

.action-btn {
  @apply w-8 h-8 bg-white bg-opacity-90 rounded-full flex items-center justify-center hover:bg-opacity-100 transition-all;
}

.action-btn.danger {
  @apply text-red-500 hover:bg-red-50;
}

.video-info {
  @apply p-4 pb-2;
}

.video-title {
  @apply font-semibold text-gray-900 mb-2;
}

.video-meta {
  @apply text-sm text-gray-600 space-y-1;
}

.channel-name {
  @apply font-medium;
}

.performance-metrics {
  @apply flex justify-between px-4 py-2 bg-gray-50 border-t border-gray-100;
}

.metric {
  @apply flex items-center space-x-1 text-sm text-gray-600;
}

.metric-icon {
  @apply w-4 h-4;
}

.analysis-results {
  @apply p-4 border-t border-gray-100;
}

.analysis-header {
  @apply flex items-center justify-between mb-3;
}

.analysis-title {
  @apply font-medium text-gray-900;
}

.analysis-score {
  @apply px-2 py-1 rounded text-sm font-medium;
}

.score-excellent {
  @apply bg-green-100 text-green-800;
}

.score-good {
  @apply bg-blue-100 text-blue-800;
}

.score-average {
  @apply bg-yellow-100 text-yellow-800;
}

.score-poor {
  @apply bg-red-100 text-red-800;
}

.analysis-insights {
  @apply space-y-2 mb-3;
}

.insight-item {
  @apply flex items-start space-x-2 text-sm;
}

.insight-icon {
  @apply w-4 h-4 mt-0.5 text-blue-500;
}

.analysis-tags {
  @apply flex flex-wrap gap-1;
}

.analysis-tag {
  @apply px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded;
}

.analysis-loading {
  @apply p-4 text-center border-t border-gray-100;
}

.loading-spinner {
  @apply mb-2;
}

.loading-text {
  @apply text-sm text-gray-600 mb-2;
}

.loading-progress {
  @apply w-full bg-gray-200 rounded-full h-2;
}

.progress-bar {
  @apply bg-blue-500 h-2 rounded-full transition-all duration-300;
}

.connection-points {
  @apply absolute inset-0 pointer-events-none;
}

.connection-point {
  @apply absolute w-3 h-3 bg-blue-500 rounded-full border-2 border-white pointer-events-auto cursor-crosshair opacity-0 hover:opacity-100 transition-opacity;
}

.connection-point.top {
  @apply top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2;
}

.connection-point.right {
  @apply top-1/2 right-0 transform translate-x-1/2 -translate-y-1/2;
}

.connection-point.bottom {
  @apply bottom-0 left-1/2 transform -translate-x-1/2 translate-y-1/2;
}

.connection-point.left {
  @apply top-1/2 left-0 transform -translate-x-1/2 -translate-y-1/2;
}

.research-video-card:hover .connection-point {
  @apply opacity-50;
}
</style>
