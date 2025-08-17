<template>
  <div>
    <!-- Global Modal Container -->
    <Teleport to="body">
      <!-- YouTube Connect Modal -->
      <YouTubeConnectModal
        v-if="modals.youtubeConnect"
        @close="closeModal('youtubeConnect')"
      />
      

      
      <!-- Settings Modal -->
      <SettingsModal
        v-if="modals.settings"
        @close="closeModal('settings')"
      />
      
      <!-- Confirmation Modal -->
      <ConfirmationModal
        v-if="modals.confirmation"
        :title="confirmationData.title"
        :message="confirmationData.message"
        :confirm-text="confirmationData.confirmText"
        :cancel-text="confirmationData.cancelText"
        :type="confirmationData.type"
        @confirm="handleConfirmation(true)"
        @cancel="handleConfirmation(false)"
      />
    </Teleport>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, provide, reactive } from 'vue'

// Modal state
const modals = reactive({
  youtubeConnect: false,
  settings: false,
  confirmation: false
})

// Confirmation modal data
const confirmationData = reactive({
  title: '',
  message: '',
  confirmText: 'Confirm',
  cancelText: 'Cancel',
  type: 'info',
  resolve: null
})

// Modal management functions
const openModal = (modalName: string) => {
  modals[modalName] = true
}

const closeModal = (modalName: string) => {
  modals[modalName] = false
}

const closeAllModals = () => {
  Object.keys(modals).forEach(key => {
    modals[key] = false
  })
}

// Confirmation modal helper
const showConfirmation = (options: {
  title: string
  message: string
  confirmText?: string
  cancelText?: string
  type?: 'info' | 'warning' | 'error' | 'success'
}): Promise<boolean> => {
  return new Promise((resolve) => {
    Object.assign(confirmationData, {
      title: options.title,
      message: options.message,
      confirmText: options.confirmText || 'Confirm',
      cancelText: options.cancelText || 'Cancel',
      type: options.type || 'info',
      resolve
    })
    modals.confirmation = true
  })
}

const handleConfirmation = (confirmed: boolean) => {
  if (confirmationData.resolve) {
    confirmationData.resolve(confirmed)
  }
  closeModal('confirmation')
}

// Keyboard shortcuts
onMounted(() => {
  const handleKeydown = (event: KeyboardEvent) => {
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

// Provide modal functions globally
provide('modals', {
  open: openModal,
  close: closeModal,
  closeAll: closeAllModals,
  confirm: showConfirmation
})
</script>
