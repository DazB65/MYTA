/**
 * Team Management Composable for MYTA
 * Handles team operations, invitations, and member management
 */

import { computed, ref } from 'vue'

// Types
interface TeamMember {
  id: string
  team_id: string
  user_id: string
  user_name: string
  user_email: string
  role: 'owner' | 'editor' | 'viewer'
  joined_at: string
  invited_by?: string
  invited_by_name?: string
  status: 'active' | 'invited' | 'inactive'
}

interface TeamInvitation {
  id: string
  team_id: string
  email: string
  role: 'editor' | 'viewer'
  token: string
  invited_by: string
  invited_by_name: string
  invited_by_email: string
  expires_at: string
  created_at: string
  status: 'pending' | 'accepted' | 'declined' | 'expired'
}

interface Team {
  id: string
  name: string
  owner_id: string
  subscription_id?: string
  max_seats: number
  created_at: string
  updated_at: string
  members: TeamMember[]
  pending_invitations: TeamInvitation[]
  member_count: number
  available_seats: number
  is_full: boolean
}

interface TeamPermissions {
  can_invite_members: boolean
  can_remove_members: boolean
  can_change_roles: boolean
  can_edit_team: boolean
  can_manage_billing: boolean
  can_delete_team: boolean
  can_create_content: boolean
  can_edit_content: boolean
  can_view_analytics: boolean
}

// State
const currentTeam = ref<Team | null>(null)
const userPermissions = ref<TeamPermissions | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

export const useTeamManagement = () => {
  // Computed properties
  const isTeamOwner = computed(() => {
    if (!currentTeam.value) return false
    const currentUser = getCurrentUser()
    return currentTeam.value.owner_id === currentUser?.id
  })

  const userRole = computed(() => {
    if (!currentTeam.value) return null
    const currentUser = getCurrentUser()
    const member = currentTeam.value.members.find(m => m.user_id === currentUser?.id)
    return member?.role || null
  })

  const canInviteMembers = computed(() => {
    return userPermissions.value?.can_invite_members || false
  })

  const canManageTeam = computed(() => {
    return userPermissions.value?.can_edit_team || false
  })

  const hasAvailableSeats = computed(() => {
    return currentTeam.value ? !currentTeam.value.is_full : false
  })

  // Helper function to get current user from auth store
  function getCurrentUser() {
    const authStore = useAuthStore()
    return authStore.user
  }

  // API helper
  async function apiCall(endpoint: string, options: any = {}) {
    const authStore = useAuthStore()
    const authToken = authStore.token

    if (!authToken) {
      throw new Error('Authentication required')
    }

    const response = await $fetch(endpoint, {
      ...options,
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json',
        ...options.headers
      }
    })

    if (!response.success) {
      throw new Error(response.message || 'API call failed')
    }

    return response
  }

  // Team operations
  async function fetchMyTeam() {
    try {
      loading.value = true
      error.value = null

      const response = await apiCall('/api/teams/my-team')
      currentTeam.value = response.data

      // Fetch permissions if we have a team
      if (currentTeam.value) {
        await fetchUserPermissions(currentTeam.value.id)
      }

    } catch (err: any) {
      error.value = err.message || 'Failed to fetch team'
      console.error('Error fetching team:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchUserPermissions(teamId: string) {
    try {
      const response = await apiCall(`/api/teams/${teamId}/permissions`)
      userPermissions.value = response.data
    } catch (err: any) {
      console.error('Error fetching permissions:', err)
    }
  }

  async function createTeam(name: string, maxSeats: number = 3) {
    try {
      loading.value = true
      error.value = null

      const response = await apiCall('/api/teams', {
        method: 'POST',
        body: { name, max_seats: maxSeats }
      })

      currentTeam.value = response.data
      await fetchUserPermissions(response.data.id)

      return response.data
    } catch (err: any) {
      // Handle backend not available gracefully
      if (err.message?.includes('404') || err.message?.includes('Failed to fetch')) {
        error.value = 'Team features require backend connection. Please start the backend server.'
        // Create mock team for frontend development
        const mockTeam = {
          id: 'mock-team-id',
          name,
          max_seats: maxSeats,
          owner_id: 'mock-user-id',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
        currentTeam.value = mockTeam
        return mockTeam
      }
      error.value = err.message || 'Failed to create team'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateTeam(teamId: string, updates: { name?: string; max_seats?: number }) {
    try {
      loading.value = true
      error.value = null

      const response = await apiCall(`/api/teams/${teamId}`, {
        method: 'PUT',
        body: updates
      })

      currentTeam.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message || 'Failed to update team'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Member management
  async function inviteMember(teamId: string, email: string, role: 'editor' | 'viewer', message?: string) {
    try {
      loading.value = true
      error.value = null

      const response = await apiCall(`/api/teams/${teamId}/invite`, {
        method: 'POST',
        body: { email, role, message }
      })

      // Refresh team data to show new invitation
      await fetchMyTeam()

      return response.data
    } catch (err: any) {
      error.value = err.message || 'Failed to send invitation'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function removeMember(teamId: string, memberId: string) {
    try {
      loading.value = true
      error.value = null

      await apiCall(`/api/teams/${teamId}/members/${memberId}`, {
        method: 'DELETE'
      })

      // Refresh team data
      await fetchMyTeam()

    } catch (err: any) {
      error.value = err.message || 'Failed to remove member'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function acceptInvitation(token: string) {
    try {
      loading.value = true
      error.value = null

      const response = await apiCall('/api/teams/invitations/accept', {
        method: 'POST',
        body: { action: 'accept', token }
      })

      // Refresh team data
      await fetchMyTeam()

      return response.data
    } catch (err: any) {
      error.value = err.message || 'Failed to accept invitation'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function declineInvitation(token: string) {
    try {
      loading.value = true
      error.value = null

      await apiCall('/api/teams/invitations/decline', {
        method: 'POST',
        body: { action: 'decline', token }
      })

    } catch (err: any) {
      error.value = err.message || 'Failed to decline invitation'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Utility functions
  function getRoleDisplayName(role: string): string {
    const roleNames = {
      owner: 'Owner',
      editor: 'Editor',
      viewer: 'Viewer'
    }
    return roleNames[role as keyof typeof roleNames] || role
  }

  function getRoleDescription(role: string): string {
    const descriptions = {
      owner: 'Full access to team management, billing, and all features',
      editor: 'Can create and edit content, tasks, and pillars',
      viewer: 'Read-only access to analytics and content'
    }
    return descriptions[role as keyof typeof descriptions] || ''
  }

  function formatMemberSince(joinedAt: string): string {
    const date = new Date(joinedAt)
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
  }

  // Clear state (for logout)
  function clearTeamData() {
    currentTeam.value = null
    userPermissions.value = null
    error.value = null
  }

  return {
    // State
    currentTeam: readonly(currentTeam),
    userPermissions: readonly(userPermissions),
    loading: readonly(loading),
    error: readonly(error),

    // Computed
    isTeamOwner,
    userRole,
    canInviteMembers,
    canManageTeam,
    hasAvailableSeats,

    // Methods
    fetchMyTeam,
    createTeam,
    updateTeam,
    inviteMember,
    removeMember,
    acceptInvitation,
    declineInvitation,
    clearTeamData,

    // Utilities
    getRoleDisplayName,
    getRoleDescription,
    formatMemberSince
  }
}
