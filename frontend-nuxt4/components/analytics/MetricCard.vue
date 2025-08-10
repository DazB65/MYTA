<template>
  <div :class="cardClasses">
    <!-- Header -->
    <div class="card-header">
      <div class="metric-info">
        <div class="metric-icon" v-if="icon">
          <component :is="iconComponent" />
        </div>
        <div>
          <h3 class="metric-title">{{ title }}</h3>
          <p class="metric-subtitle" v-if="subtitle">{{ subtitle }}</p>
        </div>
      </div>
      <div class="metric-actions" v-if="$slots.actions">
        <slot name="actions" />
      </div>
    </div>

    <!-- Main Content -->
    <div class="card-content">
      <div class="metric-value-section">
        <div class="metric-main">
          <span class="metric-value" :style="{ color: valueColor }">{{ formattedValue }}</span>
          <span class="metric-unit" v-if="unit">{{ unit }}</span>
        </div>
        
        <!-- Change indicator -->
        <div class="metric-change" v-if="change !== null">
          <div :class="changeClasses">
            <svg class="change-icon" viewBox="0 0 20 20" fill="currentColor">
              <path v-if="change >= 0" d="M3 10l9-7 9 7-9 6-9-6z" transform="rotate(180 10 10)" />
              <path v-else d="M3 10l9-7 9 7-9 6-9-6z" />
            </svg>
            <span>{{ Math.abs(change).toFixed(1) }}%</span>
          </div>
          <span class="change-period">{{ changePeriod }}</span>
        </div>
      </div>

      <!-- Additional content -->
      <div class="card-extra" v-if="$slots.default">
        <slot />
      </div>
    </div>

    <!-- Footer -->
    <div class="card-footer" v-if="$slots.footer || lastUpdated">
      <slot name="footer">
        <div class="last-updated" v-if="lastUpdated">
          <svg class="update-icon" viewBox="0 0 20 20" fill="currentColor">
            <path d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" />
          </svg>
          <span>{{ formatUpdateTime(lastUpdated) }}</span>
        </div>
      </slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: String,
  value: {
    type: [Number, String],
    required: true
  },
  unit: String,
  change: {
    type: Number,
    default: null
  },
  changePeriod: {
    type: String,
    default: 'vs last period'
  },
  icon: String,
  color: {
    type: String,
    default: 'default'
  },
  variant: {
    type: String,
    default: 'default', // default, gradient, outline
    validator: value => ['default', 'gradient', 'outline'].includes(value)
  },
  size: {
    type: String,
    default: 'medium',
    validator: value => ['small', 'medium', 'large'].includes(value)
  },
  loading: Boolean,
  error: String,
  lastUpdated: Date,
  clickable: Boolean,
  formatter: Function
})

const emit = defineEmits(['click'])

// Format the main value
const formattedValue = computed(() => {
  if (props.loading) return '...'
  if (props.error) return '--'
  if (props.formatter && typeof props.formatter === 'function') {
    return props.formatter(props.value)
  }
  
  if (typeof props.value === 'number') {
    if (props.value >= 1000000) {
      return `${(props.value / 1000000).toFixed(1)}M`
    } else if (props.value >= 1000) {
      return `${(props.value / 1000).toFixed(1)}K`
    }
    return props.value.toLocaleString()
  }
  
  return props.value
})

// Dynamic icon component
const iconComponent = computed(() => {
  if (!props.icon) return null
  
  const icons = {
    views: 'IconEye',
    subscribers: 'IconUsers',
    revenue: 'IconCurrency',
    health: 'IconHeart',
    engagement: 'IconThumbsUp',
    retention: 'IconClock',
    growth: 'IconTrendingUp'
  }
  
  return icons[props.icon] || 'IconChart'
})

// Color mapping
const valueColor = computed(() => {
  const colors = {
    default: '#1f2937',
    primary: '#3b82f6',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    info: '#06b6d4'
  }
  
  return colors[props.color] || colors.default
})

// Card classes
const cardClasses = computed(() => [
  'metric-card',
  `metric-card--${props.variant}`,
  `metric-card--${props.size}`,
  {
    'metric-card--loading': props.loading,
    'metric-card--error': props.error,
    'metric-card--clickable': props.clickable
  }
])

// Change indicator classes
const changeClasses = computed(() => [
  'change-indicator',
  {
    'change-indicator--positive': props.change > 0,
    'change-indicator--negative': props.change < 0,
    'change-indicator--neutral': props.change === 0
  }
])

// Format update time
const formatUpdateTime = (date) => {
  if (!date) return ''
  
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) { // < 1 minute
    return 'Just now'
  } else if (diff < 3600000) { // < 1 hour
    const minutes = Math.floor(diff / 60000)
    return `${minutes}m ago`
  } else if (diff < 86400000) { // < 1 day
    const hours = Math.floor(diff / 3600000)
    return `${hours}h ago`
  } else {
    return date.toLocaleDateString()
  }
}

const handleClick = () => {
  if (props.clickable) {
    emit('click')
  }
}
</script>

<style scoped>
.metric-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
  position: relative;
}

.metric-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.metric-card--clickable {
  cursor: pointer;
}

.metric-card--clickable:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.metric-card--gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.metric-card--outline {
  background: transparent;
  border: 2px solid #e5e7eb;
}

.metric-card--small {
  padding: 16px;
  border-radius: 12px;
}

.metric-card--large {
  padding: 32px;
  border-radius: 20px;
}

.metric-card--loading {
  opacity: 0.7;
  pointer-events: none;
}

.metric-card--loading::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  animation: shimmer 1.5s infinite;
}

.metric-card--error {
  border-color: #ef4444;
  background: #fef2f2;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.metric-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.metric-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(45deg, #FF6B9D, #FF8E8E);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
}

.metric-title {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.metric-card--gradient .metric-title {
  color: white;
}

.metric-subtitle {
  font-size: 12px;
  color: #6b7280;
  margin: 2px 0 0 0;
}

.metric-card--gradient .metric-subtitle {
  color: rgba(255, 255, 255, 0.8);
}

.card-content {
  margin-bottom: 16px;
}

.metric-value-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 16px;
}

.metric-main {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.metric-value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
}

.metric-card--small .metric-value {
  font-size: 24px;
}

.metric-card--large .metric-value {
  font-size: 40px;
}

.metric-unit {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.metric-change {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.change-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.change-indicator--positive {
  background: #dcfce7;
  color: #166534;
}

.change-indicator--negative {
  background: #fef2f2;
  color: #dc2626;
}

.change-indicator--neutral {
  background: #f3f4f6;
  color: #4b5563;
}

.change-icon {
  width: 12px;
  height: 12px;
}

.change-period {
  font-size: 10px;
  color: #9ca3af;
}

.card-extra {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.metric-card--gradient .card-extra {
  border-top-color: rgba(255, 255, 255, 0.2);
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
}

.metric-card--gradient .card-footer {
  border-top-color: rgba(255, 255, 255, 0.2);
}

.last-updated {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #9ca3af;
}

.metric-card--gradient .last-updated {
  color: rgba(255, 255, 255, 0.7);
}

.update-icon {
  width: 12px;
  height: 12px;
}
</style>