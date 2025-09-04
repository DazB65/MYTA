<template>
  <div class="flex items-start space-x-3 mb-4">
    <!-- Agent Avatar -->
    <div class="w-10 h-10 rounded-lg overflow-hidden ring-2 ring-opacity-50 bg-gradient-to-br p-0.5 flex-shrink-0"
         :class="getAgentRingColor(notification.agentName)"
         :style="{ background: getAgentGradient(notification.agentName) }">
      <img
        :src="getAgentImage(notification.agentName)"
        :alt="notification.agentName"
        class="w-full h-full object-cover rounded-lg"
      />
    </div>

    <!-- Notification Content -->
    <div class="flex-1 max-w-2xl">
      <!-- Notification Header -->
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center space-x-2">
          <span class="text-sm font-medium text-white">{{ notification.agentName }}</span>
          <div class="w-1 h-1 bg-gray-400 rounded-full"></div>
          <span class="text-xs text-gray-400">{{ formatTimestamp(notification.timestamp) }}</span>

          <!-- Priority Badge -->
          <div v-if="notification.priority === 'high'"
               class="px-2 py-0.5 bg-red-500/20 text-red-300 text-xs font-medium rounded-full border border-red-500/30">
            High Priority
          </div>

          <!-- Unread Indicator -->
          <div v-if="!notification.isRead"
               class="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
        </div>

        <!-- Delete Button -->
        <button
          @click="deleteNotification(notification)"
          class="text-xs p-1.5 rounded-full bg-red-600/20 hover:bg-red-600/40 text-red-300 hover:text-red-200 transition-all duration-200 border border-red-500/30 hover:border-red-400/50"
          title="Delete this insight"
        >
          🗑️
        </button>
      </div>

      <!-- Notification Bubble -->
      <div class="rounded-xl p-4 border backdrop-blur-sm"
           :class="getNotificationStyle(notification.agentName, notification.priority)">
        
        <!-- Notification Title -->
        <div class="flex items-center space-x-2 mb-2">
          <span class="text-lg">{{ getNotificationIcon(notification.type) }}</span>
          <h4 class="text-sm font-semibold text-white">{{ notification.title }}</h4>
        </div>

        <!-- Notification Message -->
        <p class="text-sm text-gray-200 mb-4 leading-relaxed">{{ notification.message }}</p>

        <!-- Action Buttons -->
        <div v-if="notification.actionButtons && notification.actionButtons.length > 0" 
             class="flex flex-wrap gap-2">
          <button
            v-for="button in notification.actionButtons"
            :key="button.action"
            @click="handleActionClick(button.action, notification)"
            class="px-3 py-1.5 text-xs font-medium rounded-lg transition-all duration-200 border"
            :class="getButtonStyle(notification.agentName)"
          >
            {{ button.text }}
          </button>
        </div>

        <!-- Mark as Read Button -->
        <div v-if="!notification.isRead" class="mt-3 pt-3 border-t border-gray-600/30">
          <button
            @click="markAsRead(notification)"
            class="text-xs text-gray-400 hover:text-white transition-colors"
          >
            Mark as read
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

// Props
interface Props {
  notification: {
    id: string
    agentId: string
    agentName: string
    type: string
    title: string
    content: string
    timestamp: Date
    actionButtons?: Array<{ text: string; action: string }>
    priority: string
    isRead: boolean
  }
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits(['action-click', 'mark-read', 'delete-notification'])

// Agent data mapping
const agentData = {
  'Alex': {
    image: '/optimized/Agent1.jpg',
    color: '#3b82f6', // blue
    gradient: 'from-blue-400 to-blue-600'
  },
  'Levi': {
    image: '/optimized/Agent2.jpg',
    color: '#eab308', // yellow
    gradient: 'from-yellow-400 to-yellow-600'
  },
  'Maya': {
    image: '/optimized/Agent3.jpg',
    color: '#ec4899', // pink
    gradient: 'from-pink-400 to-pink-600'
  },
  'Zara': {
    image: '/optimized/Agent4.jpg',
    color: '#8b5cf6', // purple
    gradient: 'from-purple-400 to-purple-600'
  },
  'Kai': {
    image: '/optimized/Agent5.jpg',
    color: '#10b981', // green
    gradient: 'from-green-400 to-green-600'
  }
}

// Methods
const getAgentImage = (agentName: string) => {
  return agentData[agentName]?.image || '/BossAgent.png'
}

const getAgentGradient = (agentName: string) => {
  const gradient = agentData[agentName]?.gradient || 'from-orange-400 to-orange-600'
  return `linear-gradient(135deg, var(--tw-gradient-stops)) ${gradient}`
}

const getAgentRingColor = (agentName: string) => {
  const color = agentData[agentName]?.color || '#f97316'
  return `ring-[${color}]`
}

const getNotificationStyle = (agentName: string, priority: string) => {
  const color = agentData[agentName]?.color || '#f97316'
  const baseClasses = 'bg-gradient-to-r backdrop-blur-sm'
  
  if (priority === 'high') {
    return `${baseClasses} from-red-900/40 to-red-800/40 border-red-500/30`
  } else {
    return `${baseClasses} from-gray-900/60 to-gray-800/60 border-gray-500/30`
  }
}

const getButtonStyle = (agentName: string) => {
  const color = agentData[agentName]?.color || '#f97316'
  return `bg-${color}/20 hover:bg-${color}/30 text-${color.replace('#', '')}-200 hover:text-white border-${color.replace('#', '')}-400/30 hover:border-${color.replace('#', '')}-400/50`
}

const getNotificationIcon = (type: string) => {
  const icons = {
    'ai_coordination': '🔗',
    'performance_alert': '📈',
    'strategy_update': '🤝',
    'content_suggestion': '💡',
    'optimization': '⚡',
    'analytics': '📊'
  }
  return icons[type] || '🤖'
}

const formatTimestamp = (timestamp: Date) => {
  const now = new Date()
  const diff = now.getTime() - timestamp.getTime()
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  
  if (minutes < 1) return 'Just now'
  if (minutes < 60) return `${minutes}m ago`
  if (hours < 24) return `${hours}h ago`
  return timestamp.toLocaleDateString()
}

const handleActionClick = (action: string, notification: any) => {
  emit('action-click', { action, notification })
}

const markAsRead = (notification: any) => {
  emit('mark-read', notification.id)
}

const deleteNotification = (notification: any) => {
  emit('delete-notification', notification.id)
}
</script>

<style scoped>
/* Custom gradient backgrounds for different agents */
.bg-alex {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.4) 0%, rgba(59, 130, 246, 0.2) 100%);
}

.bg-levi {
  background: linear-gradient(135deg, rgba(234, 179, 8, 0.4) 0%, rgba(234, 179, 8, 0.2) 100%);
}

.bg-maya {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.4) 0%, rgba(236, 72, 153, 0.2) 100%);
}

.bg-zara {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.4) 0%, rgba(139, 92, 246, 0.2) 100%);
}

.bg-kai {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.4) 0%, rgba(16, 185, 129, 0.2) 100%);
}
</style>
