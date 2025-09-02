/**
 * Team Chat Store for MYTA
 * Manages team member communication and real-time messaging
 */

import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export interface TeamMessage {
  id: string
  teamId: string
  senderId: string
  senderName: string
  senderAvatar?: string
  content: string
  type: 'text' | 'image' | 'file' | 'system'
  timestamp: Date
  edited?: boolean
  editedAt?: Date
  replyTo?: string
  mentions?: string[]
  reactions?: { [emoji: string]: string[] }
  status: 'sending' | 'sent' | 'delivered' | 'read' | 'failed'
}

export interface TeamMember {
  id: string
  name: string
  email: string
  avatar?: string
  role: string
  status: 'online' | 'away' | 'offline'
  lastSeen?: Date
}

export interface TeamChatChannel {
  id: string
  teamId: string
  name: string
  type: 'general' | 'private' | 'direct'
  description?: string
  members: string[]
  lastMessage?: TeamMessage
  unreadCount: number
  createdAt: Date
}

export const useTeamChatStore = defineStore('teamChat', () => {
  // State
  const messages = ref<TeamMessage[]>([])
  const channels = ref<TeamChatChannel[]>([])
  const members = ref<TeamMember[]>([])
  const activeChannelId = ref<string | null>(null)
  const typingUsers = ref<{ [channelId: string]: string[] }>({})
  const isConnected = ref(false)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const activeChannel = computed(() => 
    channels.value.find(c => c.id === activeChannelId.value)
  )

  const activeChannelMessages = computed(() => {
    // For demo purposes, show all messages in the active channel
    // In a real app, messages would be filtered by channelId
    if (!activeChannel.value) return []

    return messages.value
      .filter(m => m.teamId === activeChannel.value.teamId)
      .sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime())
  })

  const onlineMembers = computed(() => 
    members.value.filter(m => m.status === 'online')
  )

  const totalUnreadCount = computed(() => 
    channels.value.reduce((total, channel) => total + channel.unreadCount, 0)
  )

  // Actions
  const initializeTeamChat = async (teamId: string) => {
    try {
      loading.value = true
      error.value = null

      // Initialize with demo data for now
      // In a real app, this would fetch from the API
      await loadTeamMembers(teamId)
      await loadChannels(teamId)
      await loadRecentMessages(teamId)

      // Set default channel
      if (channels.value.length > 0) {
        activeChannelId.value = channels.value[0].id
      }

    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to initialize team chat'
      throw err
    } finally {
      loading.value = false
    }
  }

  const loadTeamMembers = async (teamId: string) => {
    // Demo team members
    members.value = [
      {
        id: 'user_1',
        name: 'John Doe',
        email: 'john@example.com',
        avatar: '/user-avatars/user1.jpg',
        role: 'Owner',
        status: 'online',
        lastSeen: new Date()
      },
      {
        id: 'user_2',
        name: 'Sarah Wilson',
        email: 'sarah@example.com',
        avatar: '/user-avatars/user2.jpg',
        role: 'Editor',
        status: 'online',
        lastSeen: new Date()
      },
      {
        id: 'user_3',
        name: 'Mike Chen',
        email: 'mike@example.com',
        avatar: '/user-avatars/user3.jpg',
        role: 'Viewer',
        status: 'away',
        lastSeen: new Date(Date.now() - 300000) // 5 minutes ago
      }
    ]
  }

  const loadChannels = async (teamId: string) => {
    // Demo channels
    channels.value = [
      {
        id: 'general',
        teamId,
        name: 'General',
        type: 'general',
        description: 'Team-wide discussions and announcements',
        members: ['user_1', 'user_2', 'user_3'],
        unreadCount: 2,
        createdAt: new Date()
      },
      {
        id: 'content-planning',
        teamId,
        name: 'Content Planning',
        type: 'private',
        description: 'Collaborate on content strategy and planning',
        members: ['user_1', 'user_2'],
        unreadCount: 0,
        createdAt: new Date()
      }
    ]
  }

  const loadRecentMessages = async (teamId: string) => {
    // Demo messages
    const now = new Date()
    messages.value = [
      {
        id: 'msg_1',
        teamId,
        senderId: 'user_2',
        senderName: 'Sarah Wilson',
        senderAvatar: '/user-avatars/user2.jpg',
        content: 'Hey team! I just finished the Q1 content calendar. Would love to get your feedback.',
        type: 'text',
        timestamp: new Date(now.getTime() - 3600000), // 1 hour ago
        status: 'read'
      },
      {
        id: 'msg_2',
        teamId,
        senderId: 'user_1',
        senderName: 'John Doe',
        senderAvatar: '/user-avatars/user1.jpg',
        content: 'Great work Sarah! I\'ll review it this afternoon and share my thoughts.',
        type: 'text',
        timestamp: new Date(now.getTime() - 3000000), // 50 minutes ago
        status: 'read'
      },
      {
        id: 'msg_3',
        teamId,
        senderId: 'user_3',
        senderName: 'Mike Chen',
        senderAvatar: '/user-avatars/user3.jpg',
        content: 'The analytics data looks promising for our video series. Should we discuss this in our next meeting?',
        type: 'text',
        timestamp: new Date(now.getTime() - 1800000), // 30 minutes ago
        status: 'delivered'
      }
    ]
  }

  const sendMessage = async (content: string, channelId?: string) => {
    if (!content.trim()) return

    const targetChannelId = channelId || activeChannelId.value
    if (!targetChannelId) throw new Error('No active channel')

    const message: TeamMessage = {
      id: `msg_${Date.now()}`,
      teamId: activeChannel.value?.teamId || '',
      senderId: 'current_user', // Would be from auth store
      senderName: 'You',
      content: content.trim(),
      type: 'text',
      timestamp: new Date(),
      status: 'sending'
    }

    // Add message optimistically
    messages.value.push(message)

    try {
      // In a real app, send via WebSocket or API
      // For now, simulate success
      setTimeout(() => {
        message.status = 'sent'
      }, 500)

      return message
    } catch (err) {
      message.status = 'failed'
      throw err
    }
  }

  const setActiveChannel = (channelId: string) => {
    activeChannelId.value = channelId
    
    // Mark channel as read
    const channel = channels.value.find(c => c.id === channelId)
    if (channel) {
      channel.unreadCount = 0
    }
  }

  const updateMemberStatus = (memberId: string, status: TeamMember['status']) => {
    const member = members.value.find(m => m.id === memberId)
    if (member) {
      member.status = status
      if (status !== 'offline') {
        member.lastSeen = new Date()
      }
    }
  }

  const addTypingUser = (channelId: string, userId: string) => {
    if (!typingUsers.value[channelId]) {
      typingUsers.value[channelId] = []
    }
    if (!typingUsers.value[channelId].includes(userId)) {
      typingUsers.value[channelId].push(userId)
    }
  }

  const removeTypingUser = (channelId: string, userId: string) => {
    if (typingUsers.value[channelId]) {
      typingUsers.value[channelId] = typingUsers.value[channelId].filter(id => id !== userId)
    }
  }

  const clearChat = () => {
    messages.value = []
    channels.value = []
    members.value = []
    activeChannelId.value = null
    typingUsers.value = {}
    error.value = null
  }

  return {
    // State
    messages,
    channels,
    members,
    activeChannelId,
    typingUsers,
    isConnected,
    loading,
    error,

    // Computed
    activeChannel,
    activeChannelMessages,
    onlineMembers,
    totalUnreadCount,

    // Actions
    initializeTeamChat,
    sendMessage,
    setActiveChannel,
    updateMemberStatus,
    addTypingUser,
    removeTypingUser,
    clearChat
  }
})
