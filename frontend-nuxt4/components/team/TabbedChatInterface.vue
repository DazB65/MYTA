<template>
  <div class="h-full flex flex-col">
    <!-- Chat Tabs Header -->
    <div class="flex items-center justify-between p-4 border-b border-forest-600">
      <div class="flex items-center space-x-2 flex-1 min-w-0">
        <!-- Active Chat Tabs -->
        <div class="flex items-center space-x-1 overflow-x-auto scrollbar-hide">
          <button
            v-for="chat in activeChats"
            :key="chat.id"
            @click="setActiveChat(chat.id)"
            class="flex items-center space-x-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors whitespace-nowrap"
            :class="chat.id === activeChatId 
              ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30' 
              : 'bg-forest-700 text-gray-300 hover:bg-forest-600'"
          >
            <!-- Chat Icon -->
            <span class="text-xs">{{ getChatIcon(chat) }}</span>
            
            <!-- Chat Name -->
            <span class="truncate max-w-24">{{ getChatName(chat) }}</span>
            
            <!-- Unread Count -->
            <span
              v-if="chat.unreadCount > 0"
              class="inline-flex items-center justify-center w-4 h-4 text-xs font-bold text-white bg-red-500 rounded-full"
            >
              {{ chat.unreadCount > 9 ? '9+' : chat.unreadCount }}
            </span>
            
            <!-- Close Tab -->
            <button
              v-if="activeChats.length > 1"
              @click.stop="closeChat(chat.id)"
              class="ml-1 text-gray-400 hover:text-white transition-colors"
            >
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
            </button>
          </button>
        </div>
        
        <!-- New Chat Button -->
        <button
          @click="showNewChatModal = true"
          class="flex items-center space-x-1 px-3 py-1.5 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
          </svg>
          <span>New Chat</span>
        </button>
      </div>
    </div>

    <!-- Active Chat Content -->
    <div v-if="activeChat" class="flex-1 flex flex-col min-h-0">
      <!-- Chat Header -->
      <div class="p-4 border-b border-forest-600">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center">
            <span class="text-blue-400">{{ getChatIcon(activeChat) }}</span>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-white">{{ getChatName(activeChat) }}</h3>
            <p class="text-xs text-gray-400">{{ getChatDescription(activeChat) }}</p>
          </div>
        </div>
      </div>

      <!-- Messages Area -->
      <div class="flex-1 overflow-y-auto p-4 space-y-4">
        <div
          v-for="message in activeChat.messages"
          :key="message.id"
          class="flex items-start space-x-3"
        >
          <!-- Avatar -->
          <div class="w-8 h-8 rounded-full bg-gray-500 flex items-center justify-center text-sm text-white font-medium flex-shrink-0">
            {{ message.sender.charAt(0) }}
          </div>
          
          <!-- Message Content -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center space-x-2 mb-1">
              <span class="text-sm font-medium text-white">{{ message.sender }}</span>
              <span class="text-xs text-gray-400">{{ formatTime(message.timestamp) }}</span>
            </div>
            <p class="text-sm text-gray-300">{{ message.content }}</p>
          </div>
        </div>
      </div>

      <!-- Message Input -->
      <div class="p-4 border-t border-forest-600">
        <div class="flex items-center space-x-2">
          <input
            v-model="newMessage"
            @keyup.enter="sendMessage"
            type="text"
            placeholder="Type a message..."
            class="flex-1 bg-forest-700 text-white placeholder-gray-400 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            @click="sendMessage"
            :disabled="!newMessage.trim()"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
          >
            Send
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="flex-1 flex items-center justify-center">
      <div class="text-center">
        <div class="w-16 h-16 rounded-full bg-gray-500/20 flex items-center justify-center mx-auto mb-4">
          <span class="text-2xl">💬</span>
        </div>
        <h3 class="text-lg font-medium text-white mb-2">No Active Chats</h3>
        <p class="text-gray-400 mb-4">Start a new conversation with your team members</p>
        <button
          @click="showNewChatModal = true"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
        >
          Start New Chat
        </button>
      </div>
    </div>

    <!-- New Chat Modal -->
    <div
      v-if="showNewChatModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click="showNewChatModal = false"
    >
      <div
        @click.stop
        class="bg-forest-800 rounded-xl p-6 w-full max-w-md mx-4"
      >
        <h3 class="text-lg font-semibold text-white mb-4">Start New Chat</h3>
        
        <!-- Chat Type Selection -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-300 mb-2">Chat Type</label>
          <div class="grid grid-cols-2 gap-2">
            <button
              @click="newChatType = 'direct'"
              class="p-3 rounded-lg border transition-colors"
              :class="newChatType === 'direct' 
                ? 'border-blue-500 bg-blue-500/20 text-blue-400' 
                : 'border-forest-600 bg-forest-700 text-gray-300 hover:bg-forest-600'"
            >
              <div class="text-center">
                <span class="block text-lg mb-1">👤</span>
                <span class="text-sm">Direct Message</span>
              </div>
            </button>
            <button
              @click="newChatType = 'channel'"
              class="p-3 rounded-lg border transition-colors"
              :class="newChatType === 'channel' 
                ? 'border-blue-500 bg-blue-500/20 text-blue-400' 
                : 'border-forest-600 bg-forest-700 text-gray-300 hover:bg-forest-600'"
            >
              <div class="text-center">
                <span class="block text-lg mb-1">#</span>
                <span class="text-sm">Channel</span>
              </div>
            </button>
          </div>
        </div>

        <!-- Team Member Selection (for Direct Messages) -->
        <div v-if="newChatType === 'direct'" class="mb-4">
          <label class="block text-sm font-medium text-gray-300 mb-2">Select Team Member</label>
          <div class="space-y-2 max-h-48 overflow-y-auto">
            <button
              v-for="member in availableMembers"
              :key="member.id"
              @click="startDirectMessage(member)"
              class="w-full flex items-center space-x-3 p-2 rounded-lg hover:bg-forest-700 transition-colors text-left"
            >
              <div class="w-8 h-8 rounded-full bg-gray-500 flex items-center justify-center text-sm text-white font-medium">
                {{ member.name.charAt(0) }}
              </div>
              <div class="flex-1">
                <p class="text-sm font-medium text-white">{{ member.name }}</p>
                <p class="text-xs text-gray-400">{{ member.role }} • {{ member.status }}</p>
              </div>
            </button>
          </div>
        </div>

        <!-- Channel Selection -->
        <div v-if="newChatType === 'channel'" class="mb-4">
          <label class="block text-sm font-medium text-gray-300 mb-2">Select Channel</label>
          <div class="space-y-2">
            <button
              v-for="channel in availableChannels"
              :key="channel.id"
              @click="openChannel(channel)"
              class="w-full flex items-center space-x-3 p-2 rounded-lg hover:bg-forest-700 transition-colors text-left"
            >
              <span class="text-lg">#</span>
              <div class="flex-1">
                <p class="text-sm font-medium text-white">{{ channel.name }}</p>
                <p class="text-xs text-gray-400">{{ channel.description }}</p>
              </div>
            </button>
          </div>
        </div>

        <!-- Modal Actions -->
        <div class="flex justify-end space-x-2">
          <button
            @click="showNewChatModal = false"
            class="px-4 py-2 text-gray-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';

// Props
interface Props {
  teamId?: string
}

const props = withDefaults(defineProps<Props>(), {
  teamId: 'demo_team_123'
})

// Reactive data
const activeChats = ref([])
const activeChatId = ref(null)
const newMessage = ref('')
const showNewChatModal = ref(false)
const newChatType = ref('direct')

// Sample data
const teamMembers = ref([
  { id: '1', name: 'John Doe', role: 'Owner', status: 'online' },
  { id: '2', name: 'Sarah Wilson', role: 'Editor', status: 'online' },
  { id: '3', name: 'Mike Chen', role: 'Viewer', status: 'away' },
])

const channels = ref([
  { id: 'general', name: 'General', description: 'Team-wide discussions' },
  { id: 'content', name: 'Content Planning', description: 'Content strategy and planning' },
  { id: 'analytics', name: 'Analytics', description: 'Performance metrics and insights' },
])

// Computed properties
const activeChat = computed(() => {
  return activeChats.value.find(chat => chat.id === activeChatId.value)
})

const availableMembers = computed(() => {
  return teamMembers.value.filter(member => 
    !activeChats.value.some(chat => 
      chat.type === 'direct' && chat.participantId === member.id
    )
  )
})

const availableChannels = computed(() => {
  return channels.value.filter(channel => 
    !activeChats.value.some(chat => 
      chat.type === 'channel' && chat.channelId === channel.id
    )
  )
})

// Methods
const setActiveChat = (chatId) => {
  activeChatId.value = chatId
}

const closeChat = (chatId) => {
  const index = activeChats.value.findIndex(chat => chat.id === chatId)
  if (index !== -1) {
    activeChats.value.splice(index, 1)
    
    // If we closed the active chat, switch to another one
    if (activeChatId.value === chatId) {
      if (activeChats.value.length > 0) {
        activeChatId.value = activeChats.value[0].id
      } else {
        activeChatId.value = null
      }
    }
  }
}

const startDirectMessage = (member) => {
  const chatId = `dm_${member.id}`
  
  // Check if chat already exists
  const existingChat = activeChats.value.find(chat => chat.id === chatId)
  if (existingChat) {
    activeChatId.value = chatId
    showNewChatModal.value = false
    return
  }

  // Create new direct message chat
  const newChat = {
    id: chatId,
    type: 'direct',
    participantId: member.id,
    participantName: member.name,
    unreadCount: 0,
    messages: [
      {
        id: '1',
        sender: 'System',
        content: `Started conversation with ${member.name}`,
        timestamp: new Date().toISOString()
      }
    ]
  }

  activeChats.value.push(newChat)
  activeChatId.value = chatId
  showNewChatModal.value = false
}

const openChannel = (channel) => {
  const chatId = `channel_${channel.id}`
  
  // Check if chat already exists
  const existingChat = activeChats.value.find(chat => chat.id === chatId)
  if (existingChat) {
    activeChatId.value = chatId
    showNewChatModal.value = false
    return
  }

  // Create new channel chat
  const newChat = {
    id: chatId,
    type: 'channel',
    channelId: channel.id,
    channelName: channel.name,
    unreadCount: 0,
    messages: [
      {
        id: '1',
        sender: 'Sarah Wilson',
        content: 'Hey team! I just finished the Q1 content calendar. Would love to get your feedback.',
        timestamp: new Date(Date.now() - 3600000).toISOString()
      },
      {
        id: '2',
        sender: 'John Doe',
        content: 'Great work Sarah! I\'ll review it this afternoon and share my thoughts.',
        timestamp: new Date(Date.now() - 3000000).toISOString()
      }
    ]
  }

  activeChats.value.push(newChat)
  activeChatId.value = chatId
  showNewChatModal.value = false
}

const sendMessage = () => {
  if (!newMessage.value.trim() || !activeChat.value) return

  const message = {
    id: Date.now().toString(),
    sender: 'You',
    content: newMessage.value.trim(),
    timestamp: new Date().toISOString()
  }

  activeChat.value.messages.push(message)
  newMessage.value = ''
}

const getChatIcon = (chat) => {
  return chat.type === 'direct' ? '👤' : '#'
}

const getChatName = (chat) => {
  return chat.type === 'direct' ? chat.participantName : chat.channelName
}

const getChatDescription = (chat) => {
  if (chat.type === 'direct') {
    const member = teamMembers.value.find(m => m.id === chat.participantId)
    return member ? `${member.role} • ${member.status}` : 'Direct Message'
  } else {
    const channel = channels.value.find(c => c.id === chat.channelId)
    return channel ? channel.description : 'Channel'
  }
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Initialize with General channel
onMounted(() => {
  openChannel(channels.value[0])
})

// Expose methods to parent component
defineExpose({
  startDirectMessage
})
</script>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>
