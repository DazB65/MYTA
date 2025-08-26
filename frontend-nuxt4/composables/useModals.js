import { reactive, ref } from 'vue'

// Global modal state - shared across all components
const modals = reactive({
  youtubeConnect: false,
  task: false,
  goal: false,
  goalSetting: false,
  content: false,
  pillar: false,
  teamInvite: false,
  teamEdit: false,
  teamMemberEdit: false,
  teamMemberRemove: false
})

// Modal data objects
const taskData = ref(null)
const goalData = ref(null)
const goalSettingData = ref(null)
const contentData = ref(null)
const pillarData = ref(null)
const teamInviteData = ref(null)
const teamEditData = ref(null)
const teamMemberData = ref(null)

// Modal management functions
const openModal = (modalName) => {
  console.log('🔥 Opening modal:', modalName)
  modals[modalName] = true
}

const closeModal = (modalName) => {
  console.log('🔥 Closing modal:', modalName)
  modals[modalName] = false
}

const closeAllModals = () => {
  console.log('🔥 Closing all modals')
  Object.keys(modals).forEach(key => {
    modals[key] = false
  })
}

// Modal opening functions with data
const openTaskModal = (task = null) => {
  console.log('🔥 Opening task modal with data:', task)
  taskData.value = task
  modals.task = true
}

const openGoalModal = (goal = null) => {
  console.log('🔥 Opening goal modal with data:', goal)
  goalData.value = goal
  modals.goal = true
}

const openGoalSettingModal = (goalSetting = null) => {
  console.log('🔥 Opening goal setting modal with data:', goalSetting)
  goalSettingData.value = goalSetting
  modals.goalSetting = true
}

const openContentModal = (content = null) => {
  console.log('🔥 Opening content modal with data:', content)
  contentData.value = content
  modals.content = true
}

const openPillarModal = (pillar = null) => {
  console.log('🔥 Opening pillar modal with data:', pillar)
  pillarData.value = pillar
  modals.pillar = true
}

const openTeamInviteModal = (teamData = null) => {
  console.log('🔥 Opening team invite modal with data:', teamData)
  teamInviteData.value = teamData
  modals.teamInvite = true
}

const openTeamEditModal = (team = null) => {
  console.log('🔥 Opening team edit modal with data:', team)
  teamEditData.value = team
  modals.teamEdit = true
}

const openTeamMemberEditModal = (member = null) => {
  console.log('🔥 Opening team member edit modal with data:', member)
  teamMemberData.value = member
  modals.teamMemberEdit = true
}

const openTeamMemberRemoveModal = (member = null) => {
  console.log('🔥 Opening team member remove modal with data:', member)
  teamMemberData.value = member
  modals.teamMemberRemove = true
}

// Modal save handlers
const handleTaskSave = (data) => {
  console.log('🔥 Task saved:', data)
  closeModal('task')
}

const handleGoalSave = (data) => {
  console.log('🔥 Goal saved:', data)
  closeModal('goal')
}

const handleGoalSettingSave = (data) => {
  console.log('🔥 Goal setting saved:', data)

  // Emit a custom event that the dashboard can listen to
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent('goalUpdated', {
      detail: data
    }))
  }

  closeModal('goalSetting')
}

const handleContentSave = (data) => {
  console.log('🔥 Content saved:', data)
  closeModal('content')
}

const handleTeamInviteSave = (data) => {
  console.log('🔥 Team invitation sent:', data)
  closeModal('teamInvite')
}

const handleTeamEditSave = (data) => {
  console.log('🔥 Team updated:', data)
  closeModal('teamEdit')
}

const handleTeamMemberEditSave = (data) => {
  console.log('🔥 Team member updated:', data)
  closeModal('teamMemberEdit')
}

const handleTeamMemberRemove = (data) => {
  console.log('🔥 Team member removed:', data)
  closeModal('teamMemberRemove')
}

// Composable function
export const useModals = () => {
  return {
    // State
    modals,
    taskData,
    goalData,
    goalSettingData,
    contentData,
    pillarData,
    teamInviteData,
    teamEditData,
    teamMemberData,

    // Functions
    open: openModal,
    close: closeModal,
    closeAll: closeAllModals,
    openTask: openTaskModal,
    openGoal: openGoalModal,
    openGoalSetting: openGoalSettingModal,
    openContent: openContentModal,
    openPillar: openPillarModal,
    openTeamInvite: openTeamInviteModal,
    openTeamEdit: openTeamEditModal,
    openTeamMemberEdit: openTeamMemberEditModal,
    openTeamMemberRemove: openTeamMemberRemoveModal,

    // Save handlers
    handleTaskSave,
    handleGoalSave,
    handleGoalSettingSave,
    handleContentSave,
    handleTeamInviteSave,
    handleTeamEditSave,
    handleTeamMemberEditSave,
    handleTeamMemberRemove
  }
}
