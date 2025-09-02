<template>
  <div class="h-full flex flex-col">
    <!-- Header -->
    <div class="flex items-center justify-between p-4 border-b border-forest-600">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center relative">
          <span class="text-blue-400">💬</span>
          <!-- Unread Messages Indicator -->
          <div
            v-if="totalUnreadMessages > 0"
            class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full flex items-center justify-center"
          >
            <span class="text-xs text-white font-bold">{{ totalUnreadMessages > 9 ? '9+' : totalUnreadMessages }}</span>
          </div>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-white flex items-center space-x-2">
            <span>Team Chat</span>
            <span v-if="totalUnreadMessages > 0" class="text-red-400 text-sm">({{ totalUnreadMessages }} new)</span>
          </h3>
          <p class="text-xs text-gray-400">
            {{ onlineMembers.length }} online • {{ activeChannel?.name || 'Select a channel' }}
          </p>
        </div>
      </div>
      
      <!-- Channel Selector -->
      <div class="flex items-center space-x-2">
        <select 
          v-model="activeChannelId" 
          @change="handleChannelChange"
          class="bg-forest-700 text-white text-sm rounded-lg px-3 py-1 border border-forest-600 focus:border-blue-500 focus:outline-none"
        >
          <option v-for="channel in channels" :key="channel.id" :value="channel.id">
            {{ channel.name }}
            <span v-if="channel.unreadCount > 0">({{ channel.unreadCount }})</span>
          </option>
        </select>
        
        <!-- Online Members Indicator -->
        <div class="flex -space-x-1">
          <div
            v-for="member in onlineMembers.slice(0, 3)"
            :key="member.id"
            class="w-6 h-6 rounded-full border-2 border-forest-800 bg-gray-500 flex items-center justify-center text-xs text-white font-medium"
            :title="member.name"
          >
            {{ member.name.charAt(0) }}
          </div>
          <div
            v-if="onlineMembers.length > 3"
            class="w-6 h-6 rounded-full border-2 border-forest-800 bg-gray-600 flex items-center justify-center text-xs text-white"
            :title="`+${onlineMembers.length - 3} more`"
          >
            +{{ onlineMembers.length - 3 }}
          </div>
        </div>
      </div>
    </div>

    <!-- Messages Area -->
    <div class="flex-1 overflow-y-auto p-4 space-y-3" ref="messagesContainer">
      <div v-if="loading" class="flex justify-center py-8">
        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
      </div>
      
      <div v-else-if="activeChannelMessages.length === 0" class="text-center py-8 text-gray-400">
        <p>No messages yet. Start the conversation!</p>
      </div>
      
      <div v-else>
        <div
          v-for="message in activeChannelMessages"
          :key="message.id"
          class="flex space-x-3"
          :class="{ 'opacity-60': message.status === 'sending' }"
        >
          <!-- Avatar -->
          <div class="w-8 h-8 rounded-full bg-gray-500 flex items-center justify-center text-sm text-white font-medium flex-shrink-0">
            {{ message.senderName.charAt(0) }}
          </div>
          
          <!-- Message Content -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center space-x-2 mb-1">
              <span class="text-sm font-medium text-white">{{ message.senderName }}</span>
              <span class="text-xs text-gray-400">{{ formatTime(message.timestamp) }}</span>
              <span
                v-if="message.status === 'sending'"
                class="text-xs text-gray-500"
              >
                Sending...
              </span>
              <span
                v-else-if="message.status === 'failed'"
                class="text-xs text-red-400"
              >
                Failed
              </span>
            </div>
            <p class="text-gray-300 text-sm break-words">{{ message.content }}</p>
          </div>
        </div>
      </div>
      
      <!-- Typing Indicators -->
      <div v-if="currentTypingUsers.length > 0" class="flex items-center space-x-2 text-gray-400 text-sm">
        <div class="flex space-x-1">
          <div class="w-1 h-1 bg-gray-400 rounded-full animate-bounce"></div>
          <div class="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
          <div class="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
        </div>
        <span>{{ formatTypingUsers(currentTypingUsers) }}</span>
      </div>
    </div>

    <!-- Message Input -->
    <div class="p-4 border-t border-forest-600">
      <div class="flex space-x-2">
        <input
          v-model="newMessage"
          @keydown.enter="handleSendMessage"
          @input="handleTyping"
          @blur="handleStopTyping"
          placeholder="Type a message..."
          class="flex-1 bg-forest-700 text-white placeholder-gray-400 rounded-lg px-3 py-2 text-sm border border-forest-600 focus:border-blue-500 focus:outline-none"
          :disabled="!activeChannel"
        />
        <button
          @click="handleSendMessage"
          :disabled="!newMessage.trim() || !activeChannel"
          class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Send
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useToast } from '../../composables/useToast'
import { useTeamChatStore } from '../../stores/teamChat'
import { useTeamNotificationStore } from '../../stores/teamNotifications'

// Props
const props = defineProps({
  teamId: {
    type: String,
    required: true
  }
})

// Composables
const teamChatStore = useTeamChatStore()
const teamNotificationStore = useTeamNotificationStore()
const { success, error: showError } = useToast()

// Template refs
const messagesContainer = ref(null)

// Local state
const newMessage = ref('')
const typingTimeout = ref(null)

// Computed - Use storeToRefs to maintain reactivity
const {
  channels,
  activeChannel,
  activeChannelMessages,
  onlineMembers,
  loading,
  error,
  typingUsers,
  activeChannelId
} = storeToRefs(teamChatStore)

const totalUnreadMessages = computed(() =>
  channels.value.reduce((total, channel) => total + (channel.unreadCount || 0), 0)
)

// Watch for new messages and create notifications
watch(
  () => activeChannelMessages.value,
  (newMessages, oldMessages) => {
    if (!oldMessages || newMessages.length <= oldMessages.length) return

    // Get the newest message
    const newestMessage = newMessages[newMessages.length - 1]

    // Don't notify for our own messages
    if (newestMessage.sender === 'current_user') return

    // Create notification for new message
    teamNotificationStore.addNotification({
      title: 'New Team Message',
      message: `${newestMessage.sender}: ${newestMessage.content.length > 50 ? newestMessage.content.substring(0, 50) + '...' : newestMessage.content}`,
      type: 'Team',
      category: 'team',
      icon: '💬',
      color: '#3b82f6',
      timestamp: 'now',
      read: false,
      teamMembers: [
        { id: newestMessage.senderId, name: newestMessage.sender, avatar: newestMessage.avatar }
      ],
      actions: [
        { id: 'view_chat', label: 'View Chat' }
      ]
    })
  },
  { deep: true }
)



const currentTypingUsers = computed(() => {
  if (!activeChannelId.value || !typingUsers[activeChannelId.value]) {
    return []
  }
  return typingUsers[activeChannelId.value]
    .map(userId => teamChatStore.members.find(m => m.id === userId))
    .filter(Boolean)
    .map(member => member.name)
})

// Methods
const handleChannelChange = () => {
  if (activeChannelId.value) {
    teamChatStore.setActiveChannel(activeChannelId.value)
    scrollToBottom()
  }
}

const handleSendMessage = async () => {
  if (!newMessage.value.trim() || !activeChannel) return

  try {
    await teamChatStore.sendMessage(newMessage.value)
    newMessage.value = ''
    handleStopTyping()
    await nextTick()
    scrollToBottom()
    success('Message sent', '')
  } catch (err) {
    showError('Failed to send message', err.message)
  }
}

const handleTyping = () => {
  if (!activeChannelId.value) return

  // Add current user to typing users
  teamChatStore.addTypingUser(activeChannelId.value, 'current_user')

  // Clear existing timeout
  if (typingTimeout.value) {
    clearTimeout(typingTimeout.value)
  }

  // Set new timeout to stop typing
  typingTimeout.value = setTimeout(() => {
    handleStopTyping()
  }, 2000)
}

const handleStopTyping = () => {
  if (activeChannelId.value) {
    teamChatStore.removeTypingUser(activeChannelId.value, 'current_user')
  }
  if (typingTimeout.value) {
    clearTimeout(typingTimeout.value)
    typingTimeout.value = null
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatTime = (timestamp) => {
  const now = new Date()
  const messageTime = new Date(timestamp)
  const diffInMinutes = Math.floor((now - messageTime) / (1000 * 60))

  if (diffInMinutes < 1) return 'now'
  if (diffInMinutes < 60) return `${diffInMinutes}m ago`
  if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`
  return messageTime.toLocaleDateString()
}

const formatTypingUsers = (users) => {
  if (users.length === 1) return `${users[0]} is typing...`
  if (users.length === 2) return `${users[0]} and ${users[1]} are typing...`
  return `${users[0]} and ${users.length - 1} others are typing...`
}

// Lifecycle
onMounted(async () => {
  try {
    await teamChatStore.initializeTeamChat(props.teamId)
    await nextTick()
    scrollToBottom()
  } catch (err) {
    showError('Failed to load team chat', err.message)
  }
})

// Watch for new messages to auto-scroll
watch(activeChannelMessages, async () => {
  await nextTick()
  scrollToBottom()
}, { deep: true })
</script>
