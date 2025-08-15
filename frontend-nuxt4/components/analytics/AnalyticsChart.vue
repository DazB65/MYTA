<template>
  <div class="analytics-chart">
    <!-- Chart Header -->
    <div class="chart-header">
      <div class="chart-info">
        <h3 class="chart-title">{{ title }}</h3>
        <p v-if="subtitle" class="chart-subtitle">{{ subtitle }}</p>
      </div>
      <div class="chart-controls">
        <!-- Chart Type Selector -->
        <div v-if="allowTypeChange" class="chart-type-selector">
          <button
            v-for="type in chartTypes"
            :key="type.value"
            :class="['type-button', { active: chartType === type.value }]"
            @click="handleTypeChange(type.value)"
          >
            <component :is="type.icon" class="type-icon" />
            <span>{{ type.label }}</span>
          </button>
        </div>

        <!-- Period Selector -->
        <div v-if="allowPeriodChange" class="period-selector">
          <select v-model="selectedPeriod" class="period-select" @change="handlePeriodChange">
            <option v-for="period in periods" :key="period.value" :value="period.value">
              {{ period.label }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Chart Container -->
    <div class="chart-container" :style="{ height: chartHeight }">
      <!-- Loading State -->
      <div v-if="loading" class="chart-loading">
        <div class="loading-spinner"/>
        <p>Loading chart data...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="chart-error">
        <svg class="error-icon" viewBox="0 0 20 20" fill="currentColor">
          <path
            fill-rule="evenodd"
            d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
            clip-rule="evenodd"
          />
        </svg>
        <h4>Chart Error</h4>
        <p>{{ error }}</p>
        <button class="retry-button" @click="$emit('retry')">Retry</button>
      </div>

      <!-- Chart Canvas -->
      <canvas
        v-else
        ref="chartCanvas"
        class="chart-canvas"
        :width="canvasWidth"
        :height="canvasHeight"
      />

      <!-- Chart Legend -->
      <div v-if="showLegend && chartData.datasets" class="chart-legend">
        <div v-for="(dataset, index) in chartData.datasets" :key="index" class="legend-item">
          <div
            class="legend-color"
            :style="{ backgroundColor: dataset.borderColor || dataset.backgroundColor }"
          />
          <span class="legend-label">{{ dataset.label }}</span>
        </div>
      </div>
    </div>

    <!-- Chart Summary -->
    <div v-if="showSummary" class="chart-summary">
      <div class="summary-stats">
        <div class="stat-item">
          <span class="stat-label">Total</span>
          <span class="stat-value">{{ formatValue(totalValue) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Average</span>
          <span class="stat-value">{{ formatValue(averageValue) }}</span>
        </div>
        <div v-if="changeValue !== null" class="stat-item">
          <span class="stat-label">Change</span>
          <span :class="['stat-value', changeClass]">
            {{ changeValue >= 0 ? '+' : '' }}{{ changeValue.toFixed(1) }}%
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: String,
  data: {
    type: Object,
    required: true,
  },
  type: {
    type: String,
    default: 'line',
    validator: value => ['line', 'bar', 'area', 'doughnut', 'pie'].includes(value),
  },
  height: {
    type: String,
    default: '300px',
  },
  loading: Boolean,
  error: String,
  showLegend: {
    type: Boolean,
    default: true,
  },
  showSummary: {
    type: Boolean,
    default: true,
  },
  allowTypeChange: {
    type: Boolean,
    default: false,
  },
  allowPeriodChange: {
    type: Boolean,
    default: false,
  },
  animate: {
    type: Boolean,
    default: true,
  },
  responsive: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['type-change', 'period-change', 'retry'])

// Refs
const chartCanvas = ref(null)
const chartType = ref(props.type)
const selectedPeriod = ref(30)

// Chart instance
let chartInstance = null

// Chart configuration
const chartTypes = [
  { value: 'line', label: 'Line', icon: 'IconLine' },
  { value: 'bar', label: 'Bar', icon: 'IconBar' },
  { value: 'area', label: 'Area', icon: 'IconArea' },
  { value: 'doughnut', label: 'Donut', icon: 'IconDonut' },
]

const periods = [
  { value: 7, label: '7 days' },
  { value: 30, label: '30 days' },
  { value: 90, label: '90 days' },
  { value: 365, label: '1 year' },
]

// Computed properties
const chartHeight = computed(() => props.height)
const canvasWidth = computed(() => 800)
const canvasHeight = computed(() => parseInt(props.height) || 300)

const chartData = computed(() => {
  if (!props.data || !props.data.datasets) return { labels: [], datasets: [] }
  return props.data
})

const totalValue = computed(() => {
  if (!chartData.value.datasets.length) return 0
  return chartData.value.datasets[0].data.reduce((sum, val) => sum + (val || 0), 0)
})

const averageValue = computed(() => {
  if (!chartData.value.datasets.length) return 0
  const data = chartData.value.datasets[0].data
  return data.length > 0 ? totalValue.value / data.length : 0
})

const changeValue = computed(() => {
  if (!chartData.value.datasets.length) return null
  const data = chartData.value.datasets[0].data
  if (data.length < 2) return null

  const latest = data[data.length - 1] || 0
  const previous = data[data.length - 2] || 0

  if (previous === 0) return null
  return ((latest - previous) / previous) * 100
})

const changeClass = computed(() => {
  if (changeValue.value === null) return ''
  return changeValue.value >= 0 ? 'positive' : 'negative'
})

// Chart creation and management
const createChart = async () => {
  if (!chartCanvas.value || !chartData.value.datasets.length) return

  const ctx = chartCanvas.value.getContext('2d')

  // Destroy existing chart
  if (chartInstance) {
    chartInstance.destroy()
  }

  // Chart.js configuration
  const config = {
    type: chartType.value,
    data: chartData.value,
    options: {
      responsive: props.responsive,
      maintainAspectRatio: false,
      animation: {
        duration: props.animate ? 750 : 0,
        easing: 'easeInOutQuart',
      },
      plugins: {
        legend: {
          display: false, // We use custom legend
        },
        tooltip: {
          mode: 'index',
          intersect: false,
          backgroundColor: '#1f2937',
          titleColor: '#ffffff',
          bodyColor: '#ffffff',
          borderColor: '#374151',
          borderWidth: 1,
          cornerRadius: 8,
          padding: 12,
          callbacks: {
            label (context) {
              return `${context.dataset.label}: ${formatValue(context.parsed.y)}`
            },
          },
        },
      },
      scales: getScalesConfig(),
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false,
      },
      elements: {
        line: {
          tension: 0.4,
          borderWidth: 3,
          fill: chartType.value === 'area',
        },
        point: {
          radius: 4,
          hoverRadius: 6,
          borderWidth: 2,
          backgroundColor: '#ffffff',
        },
        bar: {
          borderRadius: 4,
          borderSkipped: false,
        },
      },
    },
  }

  // Apply Chart.js specific configurations
  if (chartType.value === 'doughnut' || chartType.value === 'pie') {
    config.options.cutout = chartType.value === 'doughnut' ? '60%' : '0%'
    config.options.scales = {}
  }

  // Create chart (mock implementation - would use Chart.js in real app)
  chartInstance = {
    destroy: () => {},
    update: () => {},
    data: config.data,
  }

  // Draw simple chart visualization
  drawChart(ctx)
}

const getScalesConfig = () => {
  if (chartType.value === 'doughnut' || chartType.value === 'pie') {
    return {}
  }

  return {
    x: {
      grid: {
        display: true,
        color: '#f3f4f6',
      },
      ticks: {
        color: '#6b7280',
        font: {
          size: 12,
        },
      },
    },
    y: {
      grid: {
        display: true,
        color: '#f3f4f6',
      },
      ticks: {
        color: '#6b7280',
        font: {
          size: 12,
        },
        callback (value) {
          return formatValue(value)
        },
      },
    },
  }
}

const drawChart = ctx => {
  const canvas = chartCanvas.value
  const width = canvas.width
  const height = canvas.height

  // Clear canvas
  ctx.clearRect(0, 0, width, height)

  if (!chartData.value.datasets.length) return

  const data = chartData.value.datasets[0].data
  const labels = chartData.value.labels

  if (chartType.value === 'line' || chartType.value === 'area') {
    drawLineChart(ctx, data, labels, width, height)
  } else if (chartType.value === 'bar') {
    drawBarChart(ctx, data, labels, width, height)
  } else if (chartType.value === 'doughnut' || chartType.value === 'pie') {
    drawDoughnutChart(ctx, data, labels, width, height)
  }
}

const drawLineChart = (ctx, data, labels, width, height) => {
  const padding = 60
  const chartWidth = width - 2 * padding
  const chartHeight = height - 2 * padding

  const maxValue = Math.max(...data, 0)
  const minValue = Math.min(...data, 0)
  const valueRange = maxValue - minValue || 1

  // Draw grid
  ctx.strokeStyle = '#f3f4f6'
  ctx.lineWidth = 1
  for (let i = 0; i <= 5; i++) {
    const y = padding + (chartHeight / 5) * i
    ctx.beginPath()
    ctx.moveTo(padding, y)
    ctx.lineTo(width - padding, y)
    ctx.stroke()
  }

  // Draw line
  ctx.strokeStyle = '#3b82f6'
  ctx.lineWidth = 3
  ctx.beginPath()

  data.forEach((value, index) => {
    const x = padding + (chartWidth / (data.length - 1)) * index
    const y = padding + chartHeight - ((value - minValue) / valueRange) * chartHeight

    if (index === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
  })

  ctx.stroke()

  // Draw area fill if area chart
  if (chartType.value === 'area') {
    ctx.fillStyle = 'rgba(59, 130, 246, 0.1)'
    ctx.lineTo(width - padding, height - padding)
    ctx.lineTo(padding, height - padding)
    ctx.fill()
  }

  // Draw points
  ctx.fillStyle = '#3b82f6'
  data.forEach((value, index) => {
    const x = padding + (chartWidth / (data.length - 1)) * index
    const y = padding + chartHeight - ((value - minValue) / valueRange) * chartHeight

    ctx.beginPath()
    ctx.arc(x, y, 4, 0, 2 * Math.PI)
    ctx.fill()
  })
}

const drawBarChart = (ctx, data, labels, width, height) => {
  const padding = 60
  const chartWidth = width - 2 * padding
  const chartHeight = height - 2 * padding

  const maxValue = Math.max(...data, 0)
  const barWidth = (chartWidth / data.length) * 0.8
  const barSpacing = (chartWidth / data.length) * 0.2

  ctx.fillStyle = '#3b82f6'

  data.forEach((value, index) => {
    const barHeight = (value / maxValue) * chartHeight
    const x = padding + index * (barWidth + barSpacing) + barSpacing / 2
    const y = height - padding - barHeight

    // Draw rounded rectangle
    ctx.beginPath()
    ctx.roundRect(x, y, barWidth, barHeight, 4)
    ctx.fill()
  })
}

const drawDoughnutChart = (ctx, data, labels, width, height) => {
  const centerX = width / 2
  const centerY = height / 2
  const radius = Math.min(width, height) / 3
  const innerRadius = chartType.value === 'doughnut' ? radius * 0.6 : 0

  const total = data.reduce((sum, val) => sum + val, 0)
  let currentAngle = -Math.PI / 2

  const colors = [
    '#3b82f6',
    '#ef4444',
    '#10b981',
    '#f59e0b',
    '#8b5cf6',
    '#ec4899',
    '#06b6d4',
    '#84cc16',
  ]

  data.forEach((value, index) => {
    const sliceAngle = (value / total) * 2 * Math.PI

    ctx.fillStyle = colors[index % colors.length]
    ctx.beginPath()
    ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle)
    ctx.arc(centerX, centerY, innerRadius, currentAngle + sliceAngle, currentAngle, true)
    ctx.closePath()
    ctx.fill()

    currentAngle += sliceAngle
  })
}

// Event handlers
const handleTypeChange = type => {
  chartType.value = type
  emit('type-change', type)
}

const handlePeriodChange = () => {
  emit('period-change', selectedPeriod.value)
}

// Utility functions
const formatValue = value => {
  if (value === null || value === undefined) return '0'
  if (typeof value === 'number') {
    if (value >= 1000000) {
      return `${(value / 1000000).toFixed(1)}M`
    } else if (value >= 1000) {
      return `${(value / 1000).toFixed(1)}K`
    }
    return value.toLocaleString()
  }
  return value.toString()
}

// Lifecycle
onMounted(async () => {
  await nextTick()
  createChart()
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})

// Watchers
watch(
  () => props.data,
  () => {
    if (chartInstance) {
      createChart()
    }
  },
  { deep: true }
)

watch(
  () => chartType.value,
  () => {
    createChart()
  }
)
</script>

<style scoped>
.analytics-chart {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5e7eb;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.chart-info {
  flex: 1;
}

.chart-title {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 4px 0;
}

.chart-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.chart-controls {
  display: flex;
  gap: 16px;
  align-items: center;
}

.chart-type-selector {
  display: flex;
  gap: 4px;
  background: #f3f4f6;
  padding: 4px;
  border-radius: 8px;
}

.type-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border: none;
  background: transparent;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.type-button.active {
  background: #ff6b9d;
  color: white;
}

.type-button:hover:not(.active) {
  background: #e5e7eb;
}

.type-icon {
  width: 16px;
  height: 16px;
}

.period-selector {
  position: relative;
}

.period-select {
  appearance: none;
  background: #f9fafb;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 8px 32px 8px 12px;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 8px center;
  background-repeat: no-repeat;
  background-size: 16px;
}

.period-select:focus {
  outline: none;
  border-color: #ff6b9d;
  box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.1);
}

.chart-container {
  position: relative;
  margin-bottom: 16px;
}

.chart-loading,
.chart-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 12px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-icon {
  width: 48px;
  height: 48px;
  color: #ef4444;
  margin-bottom: 12px;
}

.chart-error h4 {
  color: #1f2937;
  margin: 0 0 8px 0;
}

.chart-error p {
  color: #6b7280;
  margin: 0 0 16px 0;
}

.retry-button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
}

.chart-canvas {
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.legend-label {
  font-size: 12px;
  color: #6b7280;
}

.chart-summary {
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.summary-stats {
  display: flex;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 4px;
}

.stat-value {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.stat-value.positive {
  color: #10b981;
}

.stat-value.negative {
  color: #ef4444;
}

/* Responsive Design */
@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    gap: 16px;
  }

  .chart-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .chart-type-selector {
    justify-content: center;
  }

  .summary-stats {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
