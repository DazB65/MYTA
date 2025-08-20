<template>
  <div class="notification-bell-container">
    <!-- Notification Bell Button -->
    <button 
      @click="toggleNotifications" 
      class="notification-bell-button"
      :class="{ 'has-unread': unreadCount > 0 }"
    >
      <svg class="bell-icon" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/>
      </svg>
      
      <!-- Unread Count Badge -->
      <div v-if="unreadCount > 0" class="unread-badge">
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </div>
    </button>

    <!-- Notifications Dropdown -->
    <div v-if="showNotifications" class="notifications-dropdown" @click.stop>
      <!-- Header -->
      <div class="notifications-header">
        <h3>Notifications</h3>
        <div class="header-actions">
          <button 
            v-if="unreadCount > 0" 
            @click="markAllAsRead" 
            class="mark-all-read-btn"
          >
            Mark all read
          </button>
          <button @click="refreshNotifications" class="refresh-btn" :disabled="loading">
            <svg class="refresh-icon" :class="{ 'spinning': loading }" viewBox="0 0 20 20" fill="currentColor">
              <path d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="notifications-loading">
        <div class="loading-spinner"></div>
        <p>Loading notifications...</p>
      </div>

      <!-- Notifications List -->
      <div v-else-if="notifications.length > 0" class="notifications-list">
        <div 
          v-for="notification in notifications" 
          :key="notification.id"
          class="notification-item"
          :class="{ 
            'unread': !notification.is_read,
            'critical': notification.priority === 'critical',
            'high': notification.priority === 'high'
          }"
          @click="markAsRead(notification.id)"
        >
          <!-- Notification Icon -->
          <div class="notification-icon" :class="getNotificationIconClass(notification.type)">
            <svg v-if="notification.type === 'performance_alert'" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            <svg v-else-if="notification.type === 'optimization_opportunity'" viewBox="0 0 20 20" fill="currentColor">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
            <svg v-else-if="notification.type === 'milestone_achievement'" viewBox="0 0 20 20" fill="currentColor">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
            <svg v-else-if="notification.type === 'trending_opportunity'" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clip-rule="evenodd"/>
            </svg>
            <svg v-else viewBox="0 0 20 20" fill="currentColor">
              <path d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z"/>
            </svg>
          </div>

          <!-- Notification Content -->
          <div class="notification-content">
            <div class="notification-title">{{ notification.title }}</div>
            <div class="notification-message">{{ notification.message }}</div>
            <div class="notification-meta">
              <span class="notification-time">{{ formatTime(notification.created_at) }}</span>
              <span class="notification-priority" :class="notification.priority">
                {{ notification.priority }}
              </span>
            </div>
          </div>

          <!-- Unread Indicator -->
          <div v-if="!notification.is_read" class="unread-indicator"></div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="notifications-empty">
        <svg class="empty-icon" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/>
        </svg>
        <p>No notifications yet</p>
        <span>You're all caught up!</span>
      </div>

      <!-- Footer -->
      <div class="notifications-footer">
        <button @click="viewAllNotifications" class="view-all-btn">
          View All Notifications
        </button>
      </div>
    </div>

    <!-- Backdrop -->
    <div v-if="showNotifications" class="notification-backdrop" @click="closeNotifications"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// State
const showNotifications = ref(false)
const notifications = ref([])
const loading = ref(false)

// Computed
const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.is_read).length
})

// Methods
const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
  if (showNotifications.value && notifications.value.length === 0) {
    fetchNotifications()
  }
}

const closeNotifications = () => {
  showNotifications.value = false
}

const fetchNotifications = async () => {
  loading.value = true
  try {
    // Call our new notification API
    const response = await $fetch('/api/notifications/', {
      query: { limit: 10 },
      headers: {
        'Authorization': `Bearer ${useAuthStore().token}`
      }
    })
    
    if (response.success) {
      notifications.value = response.data.notifications
    }
  } catch (error) {
    console.error('Error fetching notifications:', error)
    // Fallback to mock data for demo
    notifications.value = [
      {
        id: 1,
        type: 'performance_alert',
        priority: 'high',
        title: 'Low Click-Through Rate',
        message: 'Your CTR has dropped to 2.8%, below the 4% benchmark.',
        created_at: new Date().toISOString(),
        is_read: false
      },
      {
        id: 2,
        type: 'optimization_opportunity',
        priority: 'medium',
        title: 'Thumbnail Optimization',
        message: 'AI suggests improving thumbnail contrast for better CTR.',
        created_at: new Date(Date.now() - 3600000).toISOString(),
        is_read: false
      },
      {
        id: 3,
        type: 'milestone_achievement',
        priority: 'low',
        title: 'Congratulations! 1K Subscribers',
        message: 'You\'ve reached 1,000 subscribers! Great milestone.',
        created_at: new Date(Date.now() - 7200000).toISOString(),
        is_read: true
      }
    ]
  } finally {
    loading.value = false
  }
}

const refreshNotifications = () => {
  fetchNotifications()
}

const markAsRead = async (notificationId) => {
  try {
    await $fetch(`/api/notifications/${notificationId}/read`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${useAuthStore().token}`
      }
    })
    
    // Update local state
    const notification = notifications.value.find(n => n.id === notificationId)
    if (notification) {
      notification.is_read = true
    }
  } catch (error) {
    console.error('Error marking notification as read:', error)
    // Fallback: update local state anyway
    const notification = notifications.value.find(n => n.id === notificationId)
    if (notification) {
      notification.is_read = true
    }
  }
}

const markAllAsRead = async () => {
  try {
    await $fetch('/api/notifications/mark-all-read', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${useAuthStore().token}`
      }
    })
    
    // Update local state
    notifications.value.forEach(n => n.is_read = true)
  } catch (error) {
    console.error('Error marking all notifications as read:', error)
    // Fallback: update local state anyway
    notifications.value.forEach(n => n.is_read = true)
  }
}

const viewAllNotifications = () => {
  closeNotifications()
  // Navigate to notifications page (if you have one)
  // navigateTo('/notifications')
}

const getNotificationIconClass = (type) => {
  const classes = {
    'performance_alert': 'alert-icon',
    'optimization_opportunity': 'optimization-icon',
    'milestone_achievement': 'milestone-icon',
    'trending_opportunity': 'trending-icon',
    'agent_recommendation': 'agent-icon'
  }
  return classes[type] || 'default-icon'
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  
  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  return date.toLocaleDateString()
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.notification-bell-container')) {
    closeNotifications()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  // Fetch initial notifications
  fetchNotifications()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.notification-bell-container {
  position: relative;
}

.notification-bell-button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #D1D5DB;
  cursor: pointer;
  transition: all 0.2s;
}

.notification-bell-button:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}

.notification-bell-button.has-unread {
  color: #FCD34D;
}

.bell-icon {
  width: 20px;
  height: 20px;
}

.unread-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #EF4444;
  color: white;
  border-radius: 10px;
  padding: 2px 6px;
  font-size: 11px;
  font-weight: 600;
  min-width: 18px;
  text-align: center;
  line-height: 1.2;
}

.notifications-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 380px;
  max-height: 500px;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  z-index: 50;
  margin-top: 8px;
  overflow: hidden;
}

.notifications-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #F3F4F6;
  background: #F9FAFB;
}

.notifications-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1F2937;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mark-all-read-btn {
  background: none;
  border: none;
  color: #3B82F6;
  font-size: 14px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.2s;
}

.mark-all-read-btn:hover {
  background: #EBF8FF;
}

.refresh-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: none;
  border: 1px solid #D1D5DB;
  border-radius: 6px;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: #F3F4F6;
  color: #374151;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.refresh-icon {
  width: 14px;
  height: 14px;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.notifications-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  color: #6B7280;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid #E5E7EB;
  border-top: 2px solid #3B82F6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 12px;
}

.notifications-list {
  max-height: 320px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 1px solid #F3F4F6;
  cursor: pointer;
  transition: background 0.2s;
  position: relative;
}

.notification-item:hover {
  background: #F9FAFB;
}

.notification-item.unread {
  background: #F0F9FF;
}

.notification-item.critical {
  border-left: 3px solid #EF4444;
}

.notification-item.high {
  border-left: 3px solid #F59E0B;
}

.notification-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.alert-icon {
  background: #FEF3C7;
  color: #D97706;
}

.optimization-icon {
  background: #DBEAFE;
  color: #3B82F6;
}

.milestone-icon {
  background: #DCFCE7;
  color: #16A34A;
}

.trending-icon {
  background: #FEE2E2;
  color: #DC2626;
}

.agent-icon {
  background: #F3E8FF;
  color: #8B5CF6;
}

.default-icon {
  background: #F3F4F6;
  color: #6B7280;
}

.notification-icon svg {
  width: 16px;
  height: 16px;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  font-weight: 600;
  color: #1F2937;
  font-size: 14px;
  margin-bottom: 4px;
}

.notification-message {
  color: #6B7280;
  font-size: 13px;
  line-height: 1.4;
  margin-bottom: 8px;
}

.notification-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.notification-time {
  color: #9CA3AF;
}

.notification-priority {
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
  text-transform: uppercase;
}

.notification-priority.critical {
  background: #FEE2E2;
  color: #DC2626;
}

.notification-priority.high {
  background: #FEF3C7;
  color: #D97706;
}

.notification-priority.medium {
  background: #DBEAFE;
  color: #3B82F6;
}

.notification-priority.low {
  background: #F3F4F6;
  color: #6B7280;
}

.unread-indicator {
  width: 8px;
  height: 8px;
  background: #3B82F6;
  border-radius: 50%;
  position: absolute;
  top: 20px;
  right: 16px;
}

.notifications-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  text-align: center;
  color: #6B7280;
}

.empty-icon {
  width: 48px;
  height: 48px;
  color: #D1D5DB;
  margin-bottom: 16px;
}

.notifications-empty p {
  font-weight: 600;
  color: #374151;
  margin-bottom: 4px;
}

.notifications-empty span {
  font-size: 14px;
}

.notifications-footer {
  padding: 12px 20px;
  border-top: 1px solid #F3F4F6;
  background: #F9FAFB;
}

.view-all-btn {
  width: 100%;
  background: none;
  border: 1px solid #D1D5DB;
  border-radius: 6px;
  padding: 8px 16px;
  color: #374151;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.view-all-btn:hover {
  background: #F3F4F6;
}

.notification-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 40;
}

/* Responsive */
@media (max-width: 640px) {
  .notifications-dropdown {
    width: 320px;
    right: -140px;
  }
}
</style>
