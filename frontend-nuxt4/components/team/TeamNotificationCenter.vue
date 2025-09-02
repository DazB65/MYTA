<template>
  <div :class="compact ? '' : 'rounded-xl bg-forest-800 p-6 h-full flex flex-col'">
    <!-- Header (only show in full mode) -->
    <div v-if="!compact" class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-lg bg-yellow-500/20 flex items-center justify-center">
          <span class="text-yellow-400">🔔</span>
        </div>
        <div>
          <h2 class="text-xl font-semibold text-white">Team Notifications</h2>
          <p class="text-gray-400 text-sm">Collaborative workflow updates and alerts</p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <button
          @click="markAllAsRead"
          class="text-sm text-gray-400 hover:text-white transition-colors"
        >
          Mark all read
        </button>
        <button
          @click="openNotificationSettings"
          class="rounded-lg bg-gray-600 px-3 py-1 text-sm font-medium text-white hover:bg-gray-700 transition-colors"
        >
          Settings
        </button>
      </div>
    </div>

    <!-- Compact header actions -->
    <div v-if="compact" class="flex items-center justify-between mb-3">
      <span class="text-xs text-gray-400">{{ unreadCount }} unread</span>
      <button
        @click="markAllAsRead"
        class="text-xs text-gray-400 hover:text-white transition-colors"
      >
        Mark all read
      </button>
    </div>

    <!-- Notification Filters (only show in full mode) -->
    <div v-if="!compact" class="flex items-center space-x-2 mb-6">
      <button
        v-for="filter in notificationFilters"
        :key="filter.id"
        @click="activeFilter = filter.id"
        :class="[
          'px-3 py-1 rounded-lg text-sm font-medium transition-colors',
          activeFilter === filter.id
            ? 'bg-blue-600 text-white'
            : 'bg-forest-700 text-gray-300 hover:bg-forest-600'
        ]"
      >
        {{ filter.label }}
        <span
          v-if="filter.count > 0"
          class="ml-1 px-1.5 py-0.5 rounded-full bg-red-500 text-xs text-white"
        >
          {{ filter.count }}
        </span>
      </button>
    </div>

    <!-- Notifications List -->
    <div class="space-y-3 flex-1 overflow-y-auto">
      <div
        v-for="notification in filteredNotifications"
        :key="notification.id"
        class="p-4 rounded-lg transition-colors cursor-pointer"
        :class="[
          notification.read ? 'bg-forest-700' : 'bg-forest-600 border-l-4 border-blue-500',
          'hover:bg-forest-600'
        ]"
        @click="markAsRead(notification)"
      >
        <div class="flex items-start space-x-3">
          <!-- Notification Icon -->
          <div 
            class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
            :style="{ backgroundColor: notification.color + '20' }"
          >
            <span class="text-sm">{{ notification.icon }}</span>
          </div>

          <!-- Notification Content -->
          <div class="flex-1">
            <div class="flex items-start justify-between mb-1">
              <h4 class="font-medium text-white">{{ notification.title }}</h4>
              <div class="flex items-center space-x-2">
                <span 
                  class="px-2 py-1 rounded-full text-xs font-medium"
                  :class="getNotificationTypeClass(notification.type)"
                >
                  {{ notification.type }}
                </span>
                <span class="text-xs text-gray-400">{{ notification.timestamp }}</span>
              </div>
            </div>
            
            <p class="text-sm text-gray-300 mb-2">{{ notification.message }}</p>
            
            <!-- Involved Team Members -->
            <div v-if="notification.teamMembers" class="flex items-center space-x-2 mb-2">
              <div class="flex -space-x-1">
                <img
                  v-for="member in notification.teamMembers"
                  :key="member.id"
                  :src="member.avatar"
                  :alt="member.name"
                  class="w-5 h-5 rounded-full border border-forest-600"
                  :title="member.name"
                />
              </div>
              <span class="text-xs text-gray-400">
                {{ notification.teamMembers.length }} team member{{ notification.teamMembers.length > 1 ? 's' : '' }} involved
              </span>
            </div>

            <!-- Action Buttons -->
            <div v-if="notification.actions" class="flex space-x-2">
              <button
                v-for="action in notification.actions"
                :key="action.id"
                @click.stop="executeAction(action, notification)"
                class="text-xs px-3 py-1 rounded-lg bg-blue-500/20 text-blue-300 hover:bg-blue-500/30 transition-colors"
              >
                {{ action.label }}
              </button>
            </div>
          </div>

          <!-- Unread Indicator -->
          <div 
            v-if="!notification.read"
            class="w-2 h-2 rounded-full bg-blue-500 flex-shrink-0 mt-2"
          ></div>
        </div>
      </div>

      <!-- Empty State -->
      <div 
        v-if="filteredNotifications.length === 0"
        class="text-center py-8 text-gray-400"
      >
        <div class="text-4xl mb-2">📭</div>
        <p>No notifications for {{ activeFilterLabel }}</p>
      </div>
    </div>

    <!-- Notification Settings Panel -->
    <div v-if="showSettings" class="mt-6 pt-6 border-t border-forest-600">
      <h3 class="text-lg font-medium text-white mb-4">Notification Preferences</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="setting in notificationSettings"
          :key="setting.id"
          class="p-3 rounded-lg bg-forest-700"
        >
          <div class="flex items-center justify-between">
            <div>
              <div class="text-white font-medium">{{ setting.label }}</div>
              <div class="text-sm text-gray-400">{{ setting.description }}</div>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input
                v-model="setting.enabled"
                type="checkbox"
                class="sr-only peer"
              />
              <div class="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useToast } from '../../composables/useToast'
import { useTeamNotificationStore } from '../../stores/teamNotifications'

// Props
const props = defineProps({
  compact: {
    type: Boolean,
    default: false
  }
})

// Store
const teamNotificationStore = useTeamNotificationStore()
const { success } = useToast()

const activeFilter = ref('all')
const showSettings = ref(false)

// Notification filters
const notificationFilters = ref([
  { id: 'all', label: 'All', count: 8 },
  { id: 'team', label: 'Team', count: 3 },
  { id: 'ai', label: 'AI Agents', count: 2 },
  { id: 'content', label: 'Content', count: 2 },
  { id: 'system', label: 'System', count: 1 }
])

// Use store notifications
const notifications = computed(() => teamNotificationStore.notifications)

// Sample notifications for initial demo (add to store on mount)
const sampleNotifications = [
  {
    id: 1,
    title: 'Team Collaboration Update',
    message: 'Alex and Levi completed the content strategy analysis for your Q1 planning.',
    type: 'Team',
    category: 'ai',
    icon: '🤝',
    color: '#3b82f6',
    timestamp: '5 min ago',
    read: false,
    teamMembers: [
      { id: 'agent_1', name: 'Alex', avatar: '/optimized/Agent1.jpg' },
      { id: 'agent_2', name: 'Levi', avatar: '/optimized/Agent2.jpg' }
    ],
    actions: [
      { id: 'view', label: 'View Analysis' },
      { id: 'implement', label: 'Implement Suggestions' }
    ]
  },
  {
    id: 2,
    title: 'New Team Member Joined',
    message: 'Sarah Wilson has joined your team as an Editor and can now access content creation tools.',
    type: 'Team',
    category: 'team',
    icon: '👋',
    color: '#10b981',
    timestamp: '1 hour ago',
    read: false,
    teamMembers: [
      { id: 'user_2', name: 'Sarah Wilson', avatar: '/user-avatars/user2.jpg' }
    ],
    actions: [
      { id: 'welcome', label: 'Send Welcome Message' }
    ]
  },
  {
    id: 3,
    title: 'Content Performance Alert',
    message: 'Your latest video is performing 45% above average. Maya suggests capitalizing on this trend.',
    type: 'Content',
    category: 'content',
    icon: '📈',
    color: '#f59e0b',
    timestamp: '2 hours ago',
    read: true,
    teamMembers: [
      { id: 'agent_3', name: 'Maya', avatar: '/optimized/Agent3.jpg' }
    ],
    actions: [
      { id: 'create_similar', label: 'Create Similar Content' }
    ]
  },
  {
    id: 4,
    title: 'AI Team Coordination',
    message: 'Your AI team has identified optimization opportunities across 3 recent videos.',
    type: 'AI Agents',
    category: 'ai',
    icon: '🔗',
    color: '#a855f7',
    timestamp: '3 hours ago',
    read: true,
    teamMembers: [
      { id: 'agent_1', name: 'Alex', avatar: '/optimized/Agent1.jpg' },
      { id: 'agent_4', name: 'Zara', avatar: '/optimized/Agent4.jpg' },
      { id: 'agent_5', name: 'Kai', avatar: '/optimized/Agent5.jpg' }
    ],
    actions: [
      { id: 'review', label: 'Review Opportunities' }
    ]
  }
]

// Notification settings
const notificationSettings = ref([
  {
    id: 'team_updates',
    label: 'Team Updates',
    description: 'When team members join, leave, or change roles',
    enabled: true
  },
  {
    id: 'ai_insights',
    label: 'AI Insights',
    description: 'When AI agents discover new opportunities or complete analysis',
    enabled: true
  },
  {
    id: 'content_alerts',
    label: 'Content Performance',
    description: 'When content performs significantly above or below average',
    enabled: true
  },
  {
    id: 'collaboration',
    label: 'Collaboration Updates',
    description: 'When team members collaborate on projects or share insights',
    enabled: false
  }
])

// Computed properties
const filteredNotifications = computed(() => {
  if (activeFilter.value === 'all') return notifications.value
  return notifications.value.filter(n => n.category === activeFilter.value)
})

const activeFilterLabel = computed(() => {
  const filter = notificationFilters.value.find(f => f.id === activeFilter.value)
  return filter ? filter.label.toLowerCase() : 'this filter'
})

const unreadCount = computed(() => teamNotificationStore.unreadCount)

// Methods
const getNotificationTypeClass = (type) => {
  const classes = {
    'Team': 'bg-green-500/20 text-green-300',
    'AI Agents': 'bg-purple-500/20 text-purple-300',
    'Content': 'bg-yellow-500/20 text-yellow-300',
    'System': 'bg-gray-500/20 text-gray-300'
  }
  return classes[type] || 'bg-gray-500/20 text-gray-300'
}

const markAsRead = (notification) => {
  teamNotificationStore.markAsRead(notification.id)
  updateFilterCounts()
}

const markAllAsRead = () => {
  teamNotificationStore.markAllAsRead()
  updateFilterCounts()
}

const updateFilterCounts = () => {
  notificationFilters.value.forEach(filter => {
    if (filter.id === 'all') {
      filter.count = notifications.value.filter(n => !n.read).length
    } else {
      filter.count = notifications.value.filter(n => !n.read && n.category === filter.id).length
    }
  })
}

const executeAction = (action, notification) => {
  console.log('Executing action:', action.label, 'for notification:', notification.title)
  // TODO: Implement action execution
}

const openNotificationSettings = () => {
  showSettings.value = !showSettings.value
}

// Initialize sample notifications and filter counts
onMounted(() => {
  // Add sample notifications to store if empty
  if (teamNotificationStore.notifications.length === 0) {
    sampleNotifications.forEach(notification => {
      teamNotificationStore.addNotification(notification)
    })
  }
  updateFilterCounts()
})
</script>
