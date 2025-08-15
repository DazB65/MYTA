<template>
  <div class="analytics-overview">
    <!-- Connection Status Banner -->
    <div v-if="!isConnected" class="connection-banner">
      <div class="banner-content">
        <div class="banner-icon">
          <svg viewBox="0 0 20 20" fill="currentColor">
            <path
              d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
            />
          </svg>
        </div>
        <div class="banner-text">
          <h3>YouTube Analytics Not Connected</h3>
          <p>Connect your YouTube account to view analytics data and insights.</p>
        </div>
        <button class="connect-button" @click="$emit('connect')">Connect YouTube</button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else-if="isLoading" class="loading-state">
      <div class="loading-spinner"/>
      <p>Loading your analytics data...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">
        <svg viewBox="0 0 20 20" fill="currentColor">
          <path
            fill-rule="evenodd"
            d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
      <h3>Failed to Load Analytics</h3>
      <p>{{ error }}</p>
      <button class="retry-button" @click="handleRetry">Try Again</button>
    </div>

    <!-- Analytics Data -->
    <div v-else-if="hasData" class="analytics-grid">
      <!-- Time Range Selector -->
      <div class="time-range-header">
        <h2>Analytics Overview</h2>
        <div class="time-selector">
          <button
            v-for="range in timeRanges"
            :key="range.value"
            :class="['time-button', { active: selectedTimeRange === range.value }]"
            @click="handleTimeRangeChange(range.value)"
          >
            {{ range.label }}
          </button>
        </div>
      </div>

      <!-- Primary Metrics Grid -->
      <div class="primary-metrics">
        <!-- Channel Health Score -->
        <MetricCard
          title="Channel Health"
          subtitle="Overall performance score"
          :value="healthScore"
          unit="%"
          :change="healthChange"
          icon="health"
          :color="getHealthColor(healthScore)"
          variant="gradient"
          :last-updated="lastUpdated"
          clickable
          @click="$emit('view-health')"
        >
          <div class="health-breakdown">
            <div class="health-item">
              <span class="label">Growth Rate</span>
              <span class="value">{{ formatPercentage(subscriberGrowth.rate) }}</span>
            </div>
            <div class="health-item">
              <span class="label">Engagement</span>
              <span class="value">{{ formatPercentage(engagementRate) }}</span>
            </div>
          </div>
        </MetricCard>

        <!-- Total Views -->
        <MetricCard
          title="Total Views"
          subtitle="Views in selected period"
          :value="totalViews"
          :change="viewsChange"
          icon="views"
          color="primary"
          :last-updated="lastUpdated"
          clickable
          @click="$emit('view-views')"
        />

        <!-- Subscribers -->
        <MetricCard
          title="Subscribers"
          subtitle="Net subscriber growth"
          :value="subscriberGrowth.net"
          :change="subscriberGrowth.rate"
          change-period="growth rate"
          icon="subscribers"
          color="success"
          :last-updated="lastUpdated"
          clickable
          @click="$emit('view-subscribers')"
        >
          <div class="subscriber-breakdown">
            <div class="sub-item">
              <span class="gained">+{{ formatNumber(subscriberGrowth.gained || 0) }} gained</span>
              <span class="lost">-{{ formatNumber(subscriberGrowth.lost || 0) }} lost</span>
            </div>
          </div>
        </MetricCard>

        <!-- Revenue (if available) -->
        <MetricCard
          v-if="revenueMetrics.total > 0"
          title="Revenue"
          subtitle="Estimated earnings"
          :value="revenueMetrics.total"
          :formatter="formatCurrency"
          :change="revenueChange"
          icon="revenue"
          color="warning"
          :last-updated="lastUpdated"
          clickable
          @click="$emit('view-revenue')"
        >
          <div class="revenue-breakdown">
            <div class="revenue-item">
              <span class="label">RPM</span>
              <span class="value">{{ formatCurrency(revenueMetrics.rpm) }}</span>
            </div>
            <div class="revenue-item">
              <span class="label">CPM</span>
              <span class="value">{{ formatCurrency(revenueMetrics.cpm) }}</span>
            </div>
          </div>
        </MetricCard>
      </div>

      <!-- Secondary Metrics -->
      <div class="secondary-metrics">
        <!-- Watch Time -->
        <MetricCard
          title="Watch Time"
          subtitle="Total minutes watched"
          :value="watchTimeMinutes"
          :formatter="formatDuration"
          :change="watchTimeChange"
          icon="retention"
          size="small"
          :last-updated="lastUpdated"
        />

        <!-- Average View Duration -->
        <MetricCard
          title="Avg. View Duration"
          subtitle="Average time per view"
          :value="averageViewDuration"
          :formatter="formatDuration"
          :change="avgDurationChange"
          icon="clock"
          size="small"
          :last-updated="lastUpdated"
        />

        <!-- Click-Through Rate -->
        <MetricCard
          title="Click-Through Rate"
          subtitle="Thumbnail performance"
          :value="clickThroughRate * 100"
          unit="%"
          :change="ctrChange"
          icon="engagement"
          size="small"
          :last-updated="lastUpdated"
        />

        <!-- Impressions -->
        <MetricCard
          title="Impressions"
          subtitle="Thumbnail views"
          :value="impressions"
          :change="impressionsChange"
          icon="views"
          size="small"
          :last-updated="lastUpdated"
        />
      </div>

      <!-- Top Videos Section -->
      <div v-if="topVideos.length > 0" class="top-videos-section">
        <h3>Top Performing Videos</h3>
        <div class="videos-grid">
          <div
            v-for="video in topVideos"
            :key="video.video_id"
            class="video-card"
            @click="$emit('view-video', video)"
          >
            <div class="video-thumbnail">
              <img
                :src="video.thumbnail_url || '/default-thumbnail.jpg'"
                :alt="video.title"
                loading="lazy"
              />
              <div class="video-stats">
                <span class="views">{{ formatNumber(video.views) }} views</span>
              </div>
            </div>
            <div class="video-info">
              <h4 class="video-title">{{ video.title }}</h4>
              <div class="video-metrics">
                <span class="metric">
                  <svg class="metric-icon" viewBox="0 0 20 20" fill="currentColor">
                    <path
                      d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z"
                    />
                  </svg>
                  {{ formatNumber(video.likes || 0) }}
                </span>
                <span class="metric">
                  <svg class="metric-icon" viewBox="0 0 20 20" fill="currentColor">
                    <path
                      d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
                    />
                  </svg>
                  {{ formatNumber(video.comments || 0) }}
                </span>
              </div>
              <div class="video-published">
                {{ formatDate(video.published_at) }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Refresh Info -->
      <div class="refresh-info">
        <div class="last-updated-info">
          <svg class="icon" viewBox="0 0 20 20" fill="currentColor">
            <path
              d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
            />
          </svg>
          <span>Last updated {{ formatUpdateTime(lastUpdated) }}</span>
        </div>
        <button class="refresh-button" :disabled="isLoading" @click="handleRefresh">
          <svg class="icon" viewBox="0 0 20 20" fill="currentColor">
            <path
              d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
            />
          </svg>
          Refresh
        </button>
      </div>
    </div>

    <!-- No Data State -->
    <div v-else class="no-data-state">
      <div class="no-data-icon">
        <svg viewBox="0 0 20 20" fill="currentColor">
          <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
          <path
            fill-rule="evenodd"
            d="M4 5a2 2 0 012-2v1a1 1 0 012 0V3h6v1a1 1 0 012 0V3a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
      <h3>No Analytics Data Available</h3>
      <p>Your analytics data will appear here once you start creating content.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import MetricCard from './MetricCard.vue'

const props = defineProps({
  // Analytics data
  isConnected: Boolean,
  hasData: Boolean,
  isLoading: Boolean,
  error: String,
  lastUpdated: Date,

  // Metrics
  healthScore: { type: Number, default: 0 },
  totalViews: { type: Number, default: 0 },
  subscriberGrowth: { type: Object, default: () => ({ net: 0, rate: 0, gained: 0, lost: 0 }) },
  revenueMetrics: { type: Object, default: () => ({ total: 0, rpm: 0, cpm: 0 }) },
  watchTimeMinutes: { type: Number, default: 0 },
  averageViewDuration: { type: Number, default: 0 },
  clickThroughRate: { type: Number, default: 0 },
  impressions: { type: Number, default: 0 },
  topVideos: { type: Array, default: () => [] },

  // Change percentages (vs previous period)
  healthChange: { type: Number, default: null },
  viewsChange: { type: Number, default: null },
  revenueChange: { type: Number, default: null },
  watchTimeChange: { type: Number, default: null },
  avgDurationChange: { type: Number, default: null },
  ctrChange: { type: Number, default: null },
  impressionsChange: { type: Number, default: null },

  // Configuration
  selectedTimeRange: { type: Number, default: 30 },
})

const emit = defineEmits([
  'connect',
  'refresh',
  'retry',
  'time-range-change',
  'view-health',
  'view-views',
  'view-subscribers',
  'view-revenue',
  'view-video',
])

// Time range options
const timeRanges = [
  { label: '7D', value: 7 },
  { label: '30D', value: 30 },
  { label: '90D', value: 90 },
  { label: '1Y', value: 365 },
]

// Computed properties
const engagementRate = computed(() => {
  // Calculate based on available metrics
  if (props.totalViews === 0) return 0
  const likes = props.topVideos.reduce((sum, video) => sum + (video.likes || 0), 0)
  const comments = props.topVideos.reduce((sum, video) => sum + (video.comments || 0), 0)
  return ((likes + comments) / props.totalViews) * 100
})

// Event handlers
const handleTimeRangeChange = range => {
  emit('time-range-change', range)
}

const handleRefresh = () => {
  emit('refresh')
}

const handleRetry = () => {
  emit('retry')
}

// Utility functions
const formatNumber = num => {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toLocaleString()
}

const formatCurrency = amount => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount)
}

const formatPercentage = value => {
  return `${value.toFixed(1)}%`
}

const formatDuration = minutes => {
  if (minutes < 60) return `${Math.round(minutes)}m`
  const hours = Math.floor(minutes / 60)
  const mins = Math.round(minutes % 60)
  return `${hours}h ${mins}m`
}

const formatDate = dateString => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  })
}

const formatUpdateTime = date => {
  if (!date) return ''
  const now = new Date()
  const diff = now - date

  if (diff < 60000) return 'just now'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`
  return date.toLocaleDateString()
}

const getHealthColor = score => {
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  return 'danger'
}
</script>

<style scoped>
.analytics-overview {
  max-width: 1200px;
  margin: 0 auto;
}

/* Connection Banner */
.connection-banner {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 2px solid #f59e0b;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.banner-icon {
  width: 48px;
  height: 48px;
  color: #d97706;
}

.banner-text h3 {
  font-size: 18px;
  font-weight: 700;
  color: #92400e;
  margin: 0 0 4px 0;
}

.banner-text p {
  color: #a16207;
  margin: 0;
}

.connect-button {
  background: #f59e0b;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.connect-button:hover {
  background: #d97706;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px;
  text-align: center;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Error State */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px;
  text-align: center;
}

.error-icon {
  width: 64px;
  height: 64px;
  color: #ef4444;
  margin-bottom: 16px;
}

.error-state h3 {
  color: #1f2937;
  margin: 0 0 8px 0;
}

.error-state p {
  color: #6b7280;
  margin: 0 0 24px 0;
}

.retry-button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

/* No Data State */
.no-data-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px;
  text-align: center;
}

.no-data-icon {
  width: 64px;
  height: 64px;
  color: #9ca3af;
  margin-bottom: 16px;
}

/* Analytics Grid */
.analytics-grid {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.time-range-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.time-range-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.time-selector {
  display: flex;
  gap: 4px;
  background: #f3f4f6;
  padding: 4px;
  border-radius: 8px;
}

.time-button {
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

.time-button.active {
  background: #ff6b9d;
  color: white;
}

.time-button:hover:not(.active) {
  background: #e5e7eb;
}

.primary-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.secondary-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

/* Metric Card Content */
.health-breakdown {
  display: flex;
  justify-content: space-between;
  gap: 16px;
}

.health-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.health-item .label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.8);
}

.health-item .value {
  font-size: 14px;
  font-weight: 600;
  color: white;
}

.subscriber-breakdown .sub-item {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.gained {
  color: #10b981;
  font-weight: 600;
}

.lost {
  color: #ef4444;
  font-weight: 600;
}

.revenue-breakdown {
  display: flex;
  justify-content: space-between;
  gap: 16px;
}

.revenue-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.revenue-item .label {
  font-size: 11px;
  color: #6b7280;
}

.revenue-item .value {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

/* Top Videos Section */
.top-videos-section {
  margin-top: 8px;
}

.top-videos-section h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 16px 0;
}

.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.video-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: all 0.2s;
}

.video-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.video-thumbnail {
  position: relative;
  width: 100%;
  height: 140px;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 12px;
}

.video-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-stats {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}

.video-title {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-metrics {
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
}

.metric {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #6b7280;
}

.metric-icon {
  width: 14px;
  height: 14px;
}

.video-published {
  font-size: 11px;
  color: #9ca3af;
}

/* Refresh Info */
.refresh-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-top: 1px solid #e5e7eb;
}

.last-updated-info {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #6b7280;
}

.refresh-button {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-button:hover:not(:disabled) {
  background: #e5e7eb;
}

.refresh-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.icon {
  width: 16px;
  height: 16px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .time-range-header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .primary-metrics {
    grid-template-columns: 1fr;
  }

  .secondary-metrics {
    grid-template-columns: repeat(2, 1fr);
  }

  .videos-grid {
    grid-template-columns: 1fr;
  }
}
</style>
