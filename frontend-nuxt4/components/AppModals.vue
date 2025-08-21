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
    </Teleport>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useModals } from '../composables/useModals.js'
import GoalModal from './goals/GoalModal.vue'
import ContentModal from './modals/ContentModal.vue'
import TaskModal from './tasks/TaskModal.vue'

// Debug logging
console.log('🔥 AppModals component is loading...')

// Use the modal composable
const {
  modals,
  taskData,
  goalData,
  contentData,
  handleTaskSave,
  handleGoalSave,
  handleContentSave,
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
