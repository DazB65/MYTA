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
      <marker
        id="arrowhead"
        markerWidth="10"
        markerHeight="7"
        refX="9"
        refY="3.5"
        orient="auto"
      >
        <polygon
          points="0 0, 10 3.5, 0 7"
          fill="#6B7280"
        />
      </marker>
    </defs>
    
    <path
      :d="pathData"
      stroke="#6B7280"
      stroke-width="2"
      fill="none"
      marker-end="url(#arrowhead)"
      class="connection-path"
    />
    
    <!-- Connection label -->
    <text
      v-if="connection.label"
      :x="midPoint.x"
      :y="midPoint.y"
      text-anchor="middle"
      class="connection-label"
      fill="#374151"
      font-size="12"
      font-weight="500"
    >
      {{ connection.label }}
    </text>
    
    <!-- Remove button -->
    <circle
      :cx="midPoint.x"
      :cy="midPoint.y - 15"
      r="8"
      fill="#EF4444"
      class="remove-btn"
      style="pointer-events: all; cursor: pointer;"
      @click="removeConnection"
    />
    <text
      :x="midPoint.x"
      :y="midPoint.y - 11"
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
import { computed } from 'vue'
import type { ResearchConnection } from '../../types/research'

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
</script>

<style scoped>
.connection-line {
  pointer-events: none;
}

.connection-path {
  transition: stroke-width 0.2s ease;
}

.connection-line:hover .connection-path {
  stroke-width: 3;
}

.connection-label {
  font-family: system-ui, -apple-system, sans-serif;
}

.remove-btn {
  opacity: 0;
  transition: opacity 0.2s ease;
}

.connection-line:hover .remove-btn {
  opacity: 1;
}
</style>
