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
        @close="() => modals.task = false"
        @save="handleTaskSave"
      />

      <!-- Goal Modal -->
      <GoalModal
        v-if="modals.goal"
        :goal="goalData"
        @close="() => modals.goal = false"
        @save="handleGoalSave"
      />

      <!-- Content Modal -->
      <ContentModal
        v-if="modals.content"
        :content="contentData"
        @close="() => modals.content = false"
        @save="handleContentSave"
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

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useModals } from '../composables/useModals.js'
import GoalModal from './goals/GoalModal.vue'
import ContentModal from './modals/ContentModal.vue'
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
  contentData,
  teamInviteData,
  teamEditData,
  teamMemberData,
  handleTaskSave,
  handleGoalSave,
  handleContentSave,
  handleTeamInviteSave,
  handleTeamEditSave,
  handleTeamMemberRemove,
  closeAll: closeAllModals
} = useModals()



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
</script>
