<template>
  <svg
    class="connection-line"
    :style="{
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      pointerEvents: 'none',
      zIndex: 0
    }"
  >
    <defs>
      <!-- Different arrow types for different connection types -->
      <marker
        :id="`arrowhead-${connection.type}`"
        markerWidth="10"
        markerHeight="7"
        refX="9"
        refY="3.5"
        orient="auto"
      >
        <polygon
          points="0 0, 10 3.5, 0 7"
          :fill="getConnectionColor(connection.type)"
        />
      </marker>

      <!-- Gradient for special connections -->
      <linearGradient
        v-if="connection.type === 'trend'"
        :id="`gradient-${connection.id}`"
        x1="0%" y1="0%" x2="100%" y2="0%"
      >
        <stop offset="0%" :stop-color="getConnectionColor(connection.type)" stop-opacity="0.3"/>
        <stop offset="100%" :stop-color="getConnectionColor(connection.type)" stop-opacity="1"/>
      </linearGradient>
    </defs>

    <path
      :d="pathData"
      :stroke="getConnectionStroke()"
      :stroke-width="getConnectionWidth()"
      :stroke-dasharray="getConnectionDashArray()"
      fill="none"
      :marker-end="`url(#arrowhead-${connection.type})`"
      class="connection-path"
      :class="getConnectionClass()"
    />

    <!-- Connection type icon -->
    <circle
      :cx="midPoint.x - 20"
      :cy="midPoint.y - 20"
      r="12"
      :fill="getConnectionColor(connection.type)"
      class="connection-icon-bg"
      opacity="0.9"
    />
    <text
      :x="midPoint.x - 20"
      :y="midPoint.y - 16"
      text-anchor="middle"
      fill="white"
      font-size="10"
      font-weight="bold"
      class="connection-icon"
    >
      {{ getConnectionIcon(connection.type) }}
    </text>

    <!-- Connection label with background -->
    <rect
      v-if="connection.label || getConnectionLabel(connection.type)"
      :x="midPoint.x - 40"
      :y="midPoint.y + 5"
      width="80"
      height="20"
      :fill="getConnectionColor(connection.type)"
      opacity="0.9"
      rx="10"
      class="connection-label-bg"
    />
    <text
      v-if="connection.label || getConnectionLabel(connection.type)"
      :x="midPoint.x"
      :y="midPoint.y + 18"
      text-anchor="middle"
      class="connection-label"
      fill="white"
      font-size="11"
      font-weight="600"
    >
      {{ connection.label || getConnectionLabel(connection.type) }}
    </text>

    <!-- Remove button -->
    <circle
      :cx="midPoint.x + 20"
      :cy="midPoint.y - 20"
      r="8"
      fill="#EF4444"
      class="remove-btn"
      style="pointer-events: all; cursor: pointer;"
      @click="removeConnection"
    />
    <text
      :x="midPoint.x + 20"
      :y="midPoint.y - 16"
      text-anchor="middle"
      fill="white"
      font-size="10"
      font-weight="bold"
      style="pointer-events: none;"
    >
      ×
    </text>
  </svg>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { ResearchConnection } from '../../types/research';

interface Props {
  connection: ResearchConnection
}

interface Emits {
  (e: 'remove', connectionId: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Calculate path data for the connection line
const pathData = computed(() => {
  const { fromPosition, toPosition } = props.connection
  
  // Create a curved path between the two points
  const dx = toPosition.x - fromPosition.x
  const dy = toPosition.y - fromPosition.y
  
  // Control points for the curve
  const cp1x = fromPosition.x + dx * 0.5
  const cp1y = fromPosition.y
  const cp2x = fromPosition.x + dx * 0.5
  const cp2y = toPosition.y
  
  return `M ${fromPosition.x} ${fromPosition.y} C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${toPosition.x} ${toPosition.y}`
})

// Calculate midpoint for label and remove button
const midPoint = computed(() => {
  const { fromPosition, toPosition } = props.connection
  return {
    x: (fromPosition.x + toPosition.x) / 2,
    y: (fromPosition.y + toPosition.y) / 2
  }
})

const removeConnection = () => {
  emit('remove', props.connection.id)
}

// Connection type styling functions
const getConnectionColor = (type: string) => {
  const colors = {
    'related': '#3b82f6',      // Blue
    'competitor': '#ef4444',    // Red
    'trend': '#eab308',        // Yellow
    'inspired-by': '#16a34a',  // Green
    'custom': '#a855f7'        // Purple
  }
  return colors[type] || '#6B7280'
}

const getConnectionIcon = (type: string) => {
  const icons = {
    'related': '🔗',
    'competitor': '⚔️',
    'trend': '📈',
    'inspired-by': '💡',
    'custom': '⭐'
  }
  return icons[type] || '🔗'
}

const getConnectionLabel = (type: string) => {
  const labels = {
    'related': 'Related',
    'competitor': 'Competitor',
    'trend': 'Trending',
    'inspired-by': 'Inspired By',
    'custom': 'Custom'
  }
  return labels[type] || 'Related'
}

const getConnectionStroke = () => {
  if (props.connection.type === 'trend') {
    return `url(#gradient-${props.connection.id})`
  }
  return getConnectionColor(props.connection.type)
}

const getConnectionWidth = () => {
  const widths = {
    'related': '2',
    'competitor': '3',
    'trend': '4',
    'inspired-by': '2',
    'custom': '2'
  }
  return widths[props.connection.type] || '2'
}

const getConnectionDashArray = () => {
  const patterns = {
    'related': 'none',
    'competitor': '5,5',
    'trend': 'none',
    'inspired-by': '3,3',
    'custom': '8,4'
  }
  return patterns[props.connection.type] || 'none'
}

const getConnectionClass = () => {
  return `connection-${props.connection.type}`
}
</script>

<style scoped>
.connection-line {
  pointer-events: none;
}

.connection-path {
  transition: stroke-width 0.2s ease, opacity 0.2s ease;
}

.connection-line:hover .connection-path {
  stroke-width: 4;
}

.connection-label {
  font-family: system-ui, -apple-system, sans-serif;
}

.connection-label-bg {
  transition: opacity 0.2s ease;
}

.connection-icon-bg {
  transition: transform 0.2s ease;
}

.connection-line:hover .connection-icon-bg {
  transform: scale(1.1);
}

.remove-btn {
  opacity: 0;
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.connection-line:hover .remove-btn {
  opacity: 1;
  transform: scale(1.1);
}

/* Connection type specific styles */
.connection-related {
  filter: drop-shadow(0 0 3px rgba(59, 130, 246, 0.3));
}

.connection-competitor {
  filter: drop-shadow(0 0 3px rgba(239, 68, 68, 0.4));
}

.connection-trend {
  filter: drop-shadow(0 0 4px rgba(234, 179, 8, 0.5));
  animation: pulse-trend 2s infinite;
}

.connection-inspired-by {
  filter: drop-shadow(0 0 3px rgba(22, 163, 74, 0.3));
}

.connection-custom {
  filter: drop-shadow(0 0 3px rgba(168, 85, 247, 0.3));
}

@keyframes pulse-trend {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
</style>
