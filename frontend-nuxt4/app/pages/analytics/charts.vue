<template>
  <div class="charts-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="breadcrumb">
          <NuxtLink to="/dashboard" class="breadcrumb-link">Dashboard</NuxtLink>
          <span class="breadcrumb-separator">/</span>
          <span class="breadcrumb-current">Analytics Charts</span>
        </div>
        <h1>Analytics Charts</h1>
        <p>Deep dive into your channel's performance with interactive visualizations</p>
      </div>
      <div class="header-actions">
        <button class="export-button" :disabled="loading" @click="exportCharts">
          <svg class="export-icon" viewBox="0 0 20 20" fill="currentColor">
            <path
              fill-rule="evenodd"
              d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
          Export Charts
        </button>
        <button class="settings-button" @click="showSettings = true">
          <svg class="settings-icon" viewBox="0 0 20 20" fill="currentColor">
            <path
              fill-rule="evenodd"
              d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
              clip-rule="evenodd"
            />
          </svg>
          Settings
        </button>
      </div>
    </div>

    <!-- Connection Status -->
    <div v-if="!isConnected" class="connection-warning">
      <div class="warning-content">
        <svg class="warning-icon" viewBox="0 0 20 20" fill="currentColor">
          <path
            fill-rule="evenodd"
            d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
            clip-rule="evenodd"
          />
        </svg>
        <div>
          <h3>Analytics Not Available</h3>
          <p>Connect your YouTube account to view detailed analytics charts.</p>
        </div>
        <NuxtLink to="/auth/youtube-connect" class="connect-button"> Connect YouTube </NuxtLink>
      </div>
    </div>

    <!-- Main Charts Dashboard -->
    <div v-else class="main-content">
      <ChartsDashboard
        :analytics-data="analyticsData"
        :loading="loading"
        :error="error"
        @time-range-change="handleTimeRangeChange"
        @refresh="refreshAnalytics"
      />
    </div>

    <!-- Chart Settings Modal -->
    <div v-if="showSettings" class="modal-overlay" @click="showSettings = false">
      <div class="settings-modal" @click.stop>
        <div class="modal-header">
          <h3>Chart Settings</h3>
          <button class="close-button" @click="showSettings = false">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path
                fill-rule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
        <div class="modal-content">
          <div class="setting-group">
            <label class="setting-label">Default Chart Type</label>
            <select v-model="settings.defaultChartType" class="setting-select">
              <option value="line">Line Chart</option>
              <option value="bar">Bar Chart</option>
              <option value="area">Area Chart</option>
            </select>
          </div>
          <div class="setting-group">
            <label class="setting-label">Animation Duration</label>
            <input
              v-model="settings.animationDuration"
              type="range"
              min="0"
              max="2000"
              step="100"
              class="setting-slider"
            />
            <span class="slider-value">{{ settings.animationDuration }}ms</span>
          </div>
          <div class="setting-group">
            <label class="setting-checkbox">
              <input v-model="settings.showLegends" type="checkbox" />
              <span class="checkbox-label">Show Chart Legends</span>
            </label>
          </div>
          <div class="setting-group">
            <label class="setting-checkbox">
              <input v-model="settings.showGridLines" type="checkbox" />
              <span class="checkbox-label">Show Grid Lines</span>
            </label>
          </div>
          <div class="setting-group">
            <label class="setting-checkbox">
              <input v-model="settings.enableTooltips" type="checkbox" />
              <span class="checkbox-label">Enable Tooltips</span>
            </label>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-button" @click="showSettings = false">Cancel</button>
          <button class="save-button" @click="saveSettings">Save Settings</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAnalytics } from '@root/composables/useAnalytics'
import { onMounted, onUnmounted, ref } from 'vue'

// Lazy load the heavy ChartsDashboard component
const ChartsDashboard = defineAsyncComponent(() =>
  import('@root/components/analytics/ChartsDashboard.vue')
)

// Meta for SEO
useHead({
  title: 'Analytics Charts - Vidalytics',
  meta: [
    {
      name: 'description',
      content:
        'Explore your YouTube channel performance with interactive charts and detailed analytics visualizations.',
    },
  ],
})

// Analytics composable
const {
  loading,
  error,
  analyticsData,
  isConnected,
  hasData,
  initialize,
  refresh,
  setTimeRange,
  cleanup,
} = useAnalytics()

// Component state
const showSettings = ref(false)
const userData = ref({
  id: 'demo-user-123',
})

// Settings
const settings = ref({
  defaultChartType: 'line',
  animationDuration: 750,
  showLegends: true,
  showGridLines: true,
  enableTooltips: true,
})

// Event handlers
const handleTimeRangeChange = async range => {
  try {
    await setTimeRange(range)
  } catch (err) {
    console.error('Failed to change time range:', err)
  }
}

const refreshAnalytics = async () => {
  try {
    await refresh()
  } catch (err) {
    console.error('Failed to refresh analytics:', err)
  }
}

const exportCharts = () => {
  // Implementation for exporting charts as images or PDF
  console.log('Exporting charts...')
  // This would typically use html2canvas or similar library
  // to capture chart visualizations and export them
}

const saveSettings = () => {
  // Save settings to localStorage or user preferences
  localStorage.setItem('chartSettings', JSON.stringify(settings.value))
  showSettings.value = false
}

const loadSettings = () => {
  // Load settings from localStorage
  const saved = localStorage.getItem('chartSettings')
  if (saved) {
    settings.value = { ...settings.value, ...JSON.parse(saved) }
  }
}

// Initialize analytics on mount
onMounted(async () => {
  loadSettings()

  try {
    await initialize(userData.value.id, {
      timeRange: 30,
      autoRefresh: true,
    })
  } catch (err) {
    console.error('Charts page initialization failed:', err)
  }
})

// Cleanup on unmount
onUnmounted(() => {
  cleanup()
})
</script>

<style scoped>
.charts-page {
  min-height: 100vh;
  background: #f8f9fa;
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.header-content {
  flex: 1;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  font-size: 14px;
}

.breadcrumb-link {
  color: #6b7280;
  text-decoration: none;
  transition: color 0.2s;
}

.breadcrumb-link:hover {
  color: #ff6b9d;
}

.breadcrumb-separator {
  color: #d1d5db;
}

.breadcrumb-current {
  color: #1f2937;
  font-weight: 500;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.page-header p {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.export-button,
.settings-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.export-button {
  background: #ff6b9d;
  color: white;
}

.export-button:hover:not(:disabled) {
  background: #e55a87;
}

.export-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.settings-button {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.settings-button:hover {
  background: #e5e7eb;
}

.export-icon,
.settings-icon {
  width: 16px;
  height: 16px;
}

.connection-warning {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 2px solid #f59e0b;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
}

.warning-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.warning-icon {
  width: 48px;
  height: 48px;
  color: #d97706;
  flex-shrink: 0;
}

.warning-content h3 {
  font-size: 18px;
  font-weight: 700;
  color: #92400e;
  margin: 0 0 4px 0;
}

.warning-content p {
  color: #a16207;
  margin: 0;
}

.connect-button {
  background: #f59e0b;
  color: white;
  text-decoration: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: background 0.2s;
  white-space: nowrap;
}

.connect-button:hover {
  background: #d97706;
}

.main-content {
  /* ChartsDashboard handles its own styling */
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.settings-modal {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0 24px;
}

.modal-header h3 {
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

.modal-content {
  padding: 24px;
  flex: 1;
  overflow-y: auto;
}

.setting-group {
  margin-bottom: 24px;
}

.setting-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.setting-select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  color: #374151;
  background: white;
  cursor: pointer;
}

.setting-select:focus {
  outline: none;
  border-color: #ff6b9d;
  box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.1);
}

.setting-slider {
  width: 100%;
  margin-bottom: 8px;
}

.slider-value {
  font-size: 12px;
  color: #6b7280;
}

.setting-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.setting-checkbox input[type='checkbox'] {
  width: 16px;
  height: 16px;
  accent-color: #ff6b9d;
}

.checkbox-label {
  font-size: 14px;
  color: #374151;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px 24px 24px;
  border-top: 1px solid #e5e7eb;
}

.cancel-button,
.save-button {
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-button {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.cancel-button:hover {
  background: #e5e7eb;
}

.save-button {
  background: #ff6b9d;
  color: white;
  border: none;
}

.save-button:hover {
  background: #e55a87;
}

/* Responsive Design */
@media (max-width: 768px) {
  .charts-page {
    padding: 16px;
  }

  .page-header {
    flex-direction: column;
    gap: 20px;
  }

  .header-actions {
    width: 100%;
    justify-content: stretch;
  }

  .export-button,
  .settings-button {
    flex: 1;
    justify-content: center;
  }

  .warning-content {
    flex-direction: column;
    text-align: center;
  }

  .modal-overlay {
    padding: 16px;
  }
}
</style>
