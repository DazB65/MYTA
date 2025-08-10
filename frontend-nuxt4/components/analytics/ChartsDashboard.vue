<template>
  <div class="charts-dashboard">
    <!-- Dashboard Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <h2>Analytics Charts</h2>
        <p>Interactive visualization of your channel performance</p>
      </div>
      <div class="header-controls">
        <div class="time-range-selector">
          <button
            v-for="range in timeRanges"
            :key="range.value"
            :class="['range-button', { active: selectedTimeRange === range.value }]"
            @click="handleTimeRangeChange(range.value)"
          >
            {{ range.label }}
          </button>
        </div>
        <button class="refresh-button" @click="refreshData" :disabled="loading">
          <svg class="refresh-icon" viewBox="0 0 20 20" fill="currentColor">
            <path d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" />
          </svg>
          Refresh
        </button>
      </div>
    </div>

    <!-- Charts Grid -->
    <div class="charts-grid">
      <!-- Views Over Time Chart -->
      <div class="chart-section large">
        <AnalyticsChart
          title="Views Over Time"
          subtitle="Daily views for the selected period"
          :data="viewsChartData"
          type="line"
          height="350px"
          :loading="loading"
          :error="error"
          :allow-type-change="true"
          :allow-period-change="false"
          @type-change="handleChartTypeChange('views', $event)"
          @retry="refreshData"
        />
      </div>

      <!-- Subscriber Growth Chart -->
      <div class="chart-section medium">
        <AnalyticsChart
          title="Subscriber Growth"
          subtitle="Net subscriber changes over time"
          :data="subscribersChartData"
          type="area"
          height="280px"
          :loading="loading"
          :error="error"
          :allow-type-change="true"
          @type-change="handleChartTypeChange('subscribers', $event)"
          @retry="refreshData"
        />
      </div>

      <!-- Watch Time Distribution -->
      <div class="chart-section medium">
        <AnalyticsChart
          title="Watch Time Distribution"
          subtitle="Average watch time by video"
          :data="watchTimeChartData"
          type="bar"
          height="280px"
          :loading="loading"
          :error="error"
          :allow-type-change="true"
          @type-change="handleChartTypeChange('watchTime', $event)"
          @retry="refreshData"
        />
      </div>

      <!-- Revenue Breakdown -->
      <div class="chart-section small" v-if="revenueChartData.datasets.length > 0">
        <AnalyticsChart
          title="Revenue Sources"
          subtitle="Revenue breakdown by source"
          :data="revenueChartData"
          type="doughnut"
          height="280px"
          :loading="loading"
          :error="error"
          :show-summary="false"
          @retry="refreshData"
        />
      </div>

      <!-- Top Videos Performance -->
      <div class="chart-section small">
        <AnalyticsChart
          title="Top Videos"
          subtitle="Performance of top 10 videos"
          :data="topVideosChartData"
          type="bar"
          height="280px"
          :loading="loading"
          :error="error"
          @retry="refreshData"
        />
      </div>

      <!-- Engagement Metrics -->
      <div class="chart-section large">
        <AnalyticsChart
          title="Engagement Metrics"
          subtitle="Likes, comments, and shares over time"
          :data="engagementChartData"
          type="line"
          height="300px"
          :loading="loading"
          :error="error"
          :allow-type-change="true"
          @type-change="handleChartTypeChange('engagement', $event)"
          @retry="refreshData"
        />
      </div>
    </div>

    <!-- Charts Summary -->
    <div class="charts-summary" v-if="!loading && !error">
      <h3>Key Insights</h3>
      <div class="insights-grid">
        <div class="insight-card">
          <div class="insight-icon views">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
              <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="insight-content">
            <h4>{{ viewsTrend }}</h4>
            <p>Views are {{ viewsTrendDirection }} compared to last period</p>
          </div>
        </div>
        
        <div class="insight-card">
          <div class="insight-icon subscribers">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
            </svg>
          </div>
          <div class="insight-content">
            <h4>{{ subscribersTrend }}</h4>
            <p>Subscriber growth is {{ subscribersTrendDirection }}</p>
          </div>
        </div>
        
        <div class="insight-card">
          <div class="insight-icon engagement">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
            </svg>
          </div>
          <div class="insight-content">
            <h4>{{ engagementTrend }}</h4>
            <p>Audience engagement is {{ engagementTrendDirection }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import AnalyticsChart from './AnalyticsChart.vue'

const props = defineProps({
  analyticsData: {
    type: Object,
    required: true
  },
  loading: Boolean,
  error: String
})

const emit = defineEmits(['time-range-change', 'refresh'])

// State
const selectedTimeRange = ref(30)
const chartTypes = ref({
  views: 'line',
  subscribers: 'area',
  watchTime: 'bar',
  engagement: 'line'
})

// Time range options
const timeRanges = [
  { label: '7D', value: 7 },
  { label: '30D', value: 30 },
  { label: '90D', value: 90 },
  { label: '1Y', value: 365 }
]

// Sample data generation (in real app, this would come from props.analyticsData)
const generateSampleData = (days, baseValue = 1000, variance = 0.3) => {
  const data = []
  const labels = []
  
  for (let i = days; i >= 0; i--) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    labels.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }))
    
    const randomFactor = 1 + (Math.random() - 0.5) * variance
    const trendFactor = 1 + (days - i) / (days * 10) // Slight upward trend
    data.push(Math.round(baseValue * randomFactor * trendFactor))
  }
  
  return { labels, data }
}

// Chart data computed properties
const viewsChartData = computed(() => {
  const sampleData = generateSampleData(selectedTimeRange.value, 2500, 0.4)
  return {
    labels: sampleData.labels,
    datasets: [{
      label: 'Views',
      data: sampleData.data,
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      fill: chartTypes.value.views === 'area'
    }]
  }
})

const subscribersChartData = computed(() => {
  const sampleData = generateSampleData(selectedTimeRange.value, 50, 0.6)
  return {
    labels: sampleData.labels,
    datasets: [{
      label: 'New Subscribers',
      data: sampleData.data,
      borderColor: '#10b981',
      backgroundColor: 'rgba(16, 185, 129, 0.1)',
      fill: true
    }]
  }
})

const watchTimeChartData = computed(() => {
  const videos = ['Video 1', 'Video 2', 'Video 3', 'Video 4', 'Video 5', 'Video 6', 'Video 7', 'Video 8']
  const data = videos.map(() => Math.round(Math.random() * 300 + 100))
  
  return {
    labels: videos,
    datasets: [{
      label: 'Avg Watch Time (mins)',
      data: data,
      backgroundColor: '#f59e0b',
      borderColor: '#f59e0b',
      borderWidth: 2
    }]
  }
})

const revenueChartData = computed(() => {
  // Only show if revenue data is available
  if (!props.analyticsData?.revenue?.data?.total || props.analyticsData.revenue.data.total <= 0) {
    return { labels: [], datasets: [] }
  }
  
  return {
    labels: ['Ad Revenue', 'Memberships', 'Super Chat', 'Other'],
    datasets: [{
      data: [65, 20, 10, 5],
      backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'],
      borderWidth: 2,
      borderColor: '#ffffff'
    }]
  }
})

const topVideosChartData = computed(() => {
  const videos = ['Video A', 'Video B', 'Video C', 'Video D', 'Video E']
  const data = videos.map(() => Math.round(Math.random() * 50000 + 10000))
  
  return {
    labels: videos,
    datasets: [{
      label: 'Views',
      data: data,
      backgroundColor: '#8b5cf6',
      borderColor: '#8b5cf6',
      borderWidth: 2
    }]
  }
})

const engagementChartData = computed(() => {
  const sampleData = generateSampleData(selectedTimeRange.value, 100, 0.3)
  const likesData = sampleData.data.map(val => Math.round(val * 0.05))
  const commentsData = sampleData.data.map(val => Math.round(val * 0.02))
  
  return {
    labels: sampleData.labels,
    datasets: [
      {
        label: 'Likes',
        data: likesData,
        borderColor: '#ec4899',
        backgroundColor: 'rgba(236, 72, 153, 0.1)',
        fill: false
      },
      {
        label: 'Comments',
        data: commentsData,
        borderColor: '#06b6d4',
        backgroundColor: 'rgba(6, 182, 212, 0.1)',
        fill: false
      }
    ]
  }
})

// Trend analysis
const viewsTrend = computed(() => {
  const data = viewsChartData.value.datasets[0]?.data || []
  if (data.length < 2) return 'Stable'
  
  const recent = data.slice(-7).reduce((a, b) => a + b, 0) / 7
  const previous = data.slice(-14, -7).reduce((a, b) => a + b, 0) / 7
  const change = ((recent - previous) / previous) * 100
  
  if (change > 10) return 'Strong Growth'
  if (change > 0) return 'Growing'
  if (change > -10) return 'Stable'
  return 'Declining'
})

const viewsTrendDirection = computed(() => {
  const data = viewsChartData.value.datasets[0]?.data || []
  if (data.length < 2) return 'stable'
  
  const recent = data.slice(-3).reduce((a, b) => a + b, 0) / 3
  const previous = data.slice(-6, -3).reduce((a, b) => a + b, 0) / 3
  
  return recent > previous ? 'trending up' : 'trending down'
})

const subscribersTrend = computed(() => {
  const data = subscribersChartData.value.datasets[0]?.data || []
  const avg = data.reduce((a, b) => a + b, 0) / data.length
  
  if (avg > 80) return 'Excellent'
  if (avg > 50) return 'Good'
  if (avg > 20) return 'Moderate'
  return 'Needs Attention'
})

const subscribersTrendDirection = computed(() => {
  return subscribersTrend.value === 'Excellent' || subscribersTrend.value === 'Good' 
    ? 'healthy' : 'needs improvement'
})

const engagementTrend = computed(() => {
  const likesData = engagementChartData.value.datasets[0]?.data || []
  const commentsData = engagementChartData.value.datasets[1]?.data || []
  
  const totalEngagement = [...likesData, ...commentsData].reduce((a, b) => a + b, 0)
  
  if (totalEngagement > 1000) return 'High'
  if (totalEngagement > 500) return 'Good'
  return 'Growing'
})

const engagementTrendDirection = computed(() => {
  return engagementTrend.value === 'High' ? 'strong' : 'improving'
})

// Event handlers
const handleTimeRangeChange = (range) => {
  selectedTimeRange.value = range
  emit('time-range-change', range)
}

const handleChartTypeChange = (chart, type) => {
  chartTypes.value[chart] = type
}

const refreshData = () => {
  emit('refresh')
}

// Lifecycle
onMounted(() => {
  // Initialize with current data
})
</script>

<style scoped>
.charts-dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  padding: 24px 0;
  border-bottom: 1px solid #e5e7eb;
}

.header-content h2 {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.header-content p {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
}

.header-controls {
  display: flex;
  gap: 16px;
  align-items: center;
}

.time-range-selector {
  display: flex;
  gap: 4px;
  background: #f3f4f6;
  padding: 4px;
  border-radius: 8px;
}

.range-button {
  padding: 8px 16px;
  border: none;
  background: transparent;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.range-button.active {
  background: #FF6B9D;
  color: white;
}

.range-button:hover:not(.active) {
  background: #e5e7eb;
}

.refresh-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  color: #374151;
  border: 1px solid #d1d5db;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-button:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #9ca3af;
}

.refresh-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-icon {
  width: 16px;
  height: 16px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.chart-section.large {
  grid-column: span 8;
}

.chart-section.medium {
  grid-column: span 6;
}

.chart-section.small {
  grid-column: span 4;
}

.charts-summary {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.charts-summary h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 24px 0;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.insight-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  border-left: 4px solid transparent;
}

.insight-card:first-child {
  border-left-color: #3b82f6;
}

.insight-card:nth-child(2) {
  border-left-color: #10b981;
}

.insight-card:nth-child(3) {
  border-left-color: #ec4899;
}

.insight-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.insight-icon.views {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
}

.insight-icon.subscribers {
  background: linear-gradient(135deg, #10b981 0%, #047857 100%);
}

.insight-icon.engagement {
  background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
}

.insight-icon svg {
  width: 24px;
  height: 24px;
}

.insight-content h4 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
}

.insight-content p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .chart-section.large {
    grid-column: span 12;
  }
  
  .chart-section.medium {
    grid-column: span 6;
  }
  
  .chart-section.small {
    grid-column: span 6;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    gap: 20px;
  }
  
  .header-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-section.large,
  .chart-section.medium,
  .chart-section.small {
    grid-column: span 1;
  }
  
  .insights-grid {
    grid-template-columns: 1fr;
  }
}
</style>