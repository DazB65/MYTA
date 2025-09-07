<template>
  <div>
    <!-- Global Modal Container -->
    <Teleport to="body">
      <!-- YouTube Connect Modal -->
      <YouTubeConnectModal
        v-if="modals.youtubeConnect"
        @close="closeModal('youtubeConnect')"
      />
      

      
      <!-- Task Modal -->
      <TaskModal
        v-if="modals.task"
        :task="taskData"
        @close="() => { console.log('🔥 AppModals: Closing task modal'); modals.task = false }"
        @save="handleGlobalTaskSave"
      />

      <!-- Goal Modal -->
      <GoalModal
        v-if="modals.goal"
        :goal="goalData"
        @close="() => modals.goal = false"
        @save="handleGoalSave"
      />

      <!-- Goal Setting Modal -->
      <GoalSettingModal
        v-if="modals.goalSetting"
        :is-open="modals.goalSetting"
        :goal-data="goalSettingData"
        @close="() => modals.goalSetting = false"
        @save="handleGoalSettingSave"
      />

      <!-- Content Modal -->
      <ContentModal
        v-if="modals.content"
        :content="contentData"
        @close="() => modals.content = false"
        @save="handleContentSave"
      />

      <!-- Pillar Modal -->
      <PillarModal
        v-if="modals.pillar"
        :pillar="pillarData"
        @close="() => modals.pillar = false"
        @edit="handlePillarEdit"
        @delete="handlePillarDelete"
      />

      <!-- Team Invite Modal -->
      <TeamInviteModal
        v-if="modals.teamInvite"
        :teamData="teamInviteData"
        @close="() => modals.teamInvite = false"
        @save="handleTeamInviteSave"
      />

      <!-- Team Edit Modal -->
      <TeamEditModal
        v-if="modals.teamEdit"
        :teamData="teamEditData"
        @close="() => modals.teamEdit = false"
        @save="handleTeamEditSave"
      />

      <!-- Team Member Remove Modal -->
      <TeamMemberRemoveModal
        v-if="modals.teamMemberRemove"
        :memberData="teamMemberData"
        @close="() => modals.teamMemberRemove = false"
        @remove="handleTeamMemberRemove"
      />
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, watch } from 'vue'
import { useModals } from '../composables/useModals.js'
import { useToast } from '../composables/useToast'
import { useTasksStore } from '../stores/tasks'
import GoalModal from './goals/GoalModal.vue'
import ContentModal from './modals/ContentModal.vue'
import GoalSettingModal from './modals/GoalSettingModal.vue'
import PillarModal from './pillars/PillarModal.vue'
import TaskModal from './tasks/TaskModal.vue'
import TeamEditModal from './team/TeamEditModal.vue'
import TeamInviteModal from './team/TeamInviteModal.vue'
import TeamMemberRemoveModal from './team/TeamMemberRemoveModal.vue'

// Debug logging
console.log('🔥 AppModals component is loading...')

// Use the modal composable
const {
  modals,
  taskData,
  goalData,
  goalSettingData,
  contentData,
  pillarData,
  teamInviteData,
  teamEditData,
  teamMemberData,
  handleTaskSave,
  handleGoalSave,
  handleGoalSettingSave,
  handleContentSave,
  handleTeamInviteSave,
  handleTeamEditSave,
  handleTeamMemberRemove,
  closeAll: closeAllModals
} = useModals()

// Watch for modal state changes
watch(() => modals.task, (newValue, oldValue) => {
  console.log('🔥 AppModals: Task modal state changed from', oldValue, 'to', newValue)
  console.log('🔥 AppModals: Task data is:', taskData.value)
}, { immediate: true })

// Pillar modal handlers
const handlePillarEdit = (pillar) => {
  console.log('🔥 Pillar edit requested:', pillar)
  // TODO: Implement edit functionality
  alert('Edit functionality coming soon!')
}

const handlePillarDelete = (pillar) => {
  console.log('🔥 Pillar delete completed:', pillar)
  modals.pillar = false
}

// Custom task save handler that actually saves to the store
const handleGlobalTaskSave = (data) => {
  console.log('🔥 Global task save:', data)

  // Get stores and composables
  const tasksStore = useTasksStore()
  const { success } = useToast()

  try {
    // Add the task to the store
    console.log('🔥 Tasks before adding:', tasksStore.tasks.length)
    const newTask = tasksStore.addTask(data)
    console.log('🔥 New task created:', newTask)
    console.log('🔥 Tasks after adding:', tasksStore.tasks.length)
    console.log('🔥 All tasks:', tasksStore.tasks.map(t => ({ id: t.id, title: t.title })))

    // Show success message
    success('Task Created', 'Task has been successfully created and added to your calendar.')

    // Close the modal
    modals.task = false
  } catch (error) {
    console.error('Failed to save task:', error)
    const { error: showError } = useToast()
    showError('Failed to Save Task', 'There was an error saving the task. Please try again.')
  }
}



// Keyboard shortcuts
onMounted(() => {
  const handleKeydown = (event) => {
    // Close modals on Escape
    if (event.key === 'Escape') {
      closeAllModals()
    }
  }
  
  document.addEventListener('keydown', handleKeydown)
  
  onUnmounted(() => {
    document.removeEventListener('keydown', handleKeydown)
  })
})

console.log('🔥 AppModals using composable - modals state:', modals)

// Debug contentData changes
watch(() => contentData.value, (newData) => {
  console.log('🔥 AppModals - contentData changed:', newData)
}, { immediate: true })

watch(() => modals.content, (isOpen) => {
  console.log('🔥 AppModals - content modal state:', isOpen, 'contentData:', contentData.value)
})
</script>
