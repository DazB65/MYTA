<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <h2>Connect Your YouTube Channel</h2>
        <button class="close-button" @click="$emit('close')">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path
              d="M18 6L6 18M6 6L18 18"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            />
          </svg>
        </button>
      </div>

      <div class="modal-content">
        <div class="connection-info">
          <div class="youtube-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="#FF0000">
              <path
                d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"
              />
            </svg>
          </div>

          <h3>Unlock Powerful Analytics</h3>
          <p>Connect your YouTube channel to access:</p>

          <ul class="features-list">
            <li>📊 Real-time analytics and insights</li>
            <li>🎯 AI-powered content recommendations</li>
            <li>📈 Growth tracking and optimization</li>
            <li>🔍 Audience insights and demographics</li>
            <li>💰 Revenue and monetization tracking</li>
          </ul>
        </div>

        <div class="connection-actions">
          <!-- Error message -->
          <div v-if="error" class="error-message">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="#ef4444" stroke-width="2"/>
              <path d="M15 9l-6 6M9 9l6 6" stroke="#ef4444" stroke-width="2" stroke-linecap="round"/>
            </svg>
            {{ error }}
          </div>

          <button class="connect-button" :disabled="connecting" @click="handleConnect">
            <svg v-if="connecting" class="spinner" width="20" height="20" viewBox="0 0 24 24">
              <circle
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
                fill="none"
                opacity="0.25"
              />
              <path
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                fill="currentColor"
              />
            </svg>
            {{ connecting ? 'Connecting...' : 'Connect with YouTube' }}
          </button>

          <p class="privacy-note">
            🔒 Your data is secure. We only access analytics data and never post content without
            your permission.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAnalytics } from '~/composables/useAnalytics'

// Define emits
const emit = defineEmits(['close', 'connect'])

// Component state
const connecting = ref(false)
const error = ref(null)

// Analytics composable
const { connectYouTube } = useAnalytics()

// Event handlers
const handleOverlayClick = () => {
  emit('close')
}

const handleConnect = async () => {
  connecting.value = true
  error.value = null

  try {
    // Use a default user ID for now - in production this would come from auth
    const userId = 'default_user'

    // Connect to YouTube using real OAuth
    await connectYouTube(userId)

    // Emit connect event
    emit('connect')

    // Note: Modal will close when OAuth redirects back
  } catch (err) {
    console.error('Failed to connect YouTube:', err)
    error.value = err.message
    connecting.value = false
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-container {
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0 24px;
  border-bottom: 1px solid #f3f4f6;
  margin-bottom: 24px;
}

.modal-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s;
}

.close-button:hover {
  background: #f3f4f6;
  color: #374151;
}

.modal-content {
  padding: 0 24px 24px 24px;
}

.connection-info {
  text-align: center;
  margin-bottom: 32px;
}

.youtube-icon {
  margin-bottom: 16px;
}

.connection-info h3 {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.connection-info p {
  color: #6b7280;
  margin: 0 0 24px 0;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left;
}

.features-list li {
  padding: 8px 0;
  color: #374151;
  font-size: 14px;
}

.connection-actions {
  text-align: center;
}

.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.connect-button {
  background: linear-gradient(135deg, #ff0000 0%, #cc0000 100%);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  margin-bottom: 16px;
}

.connect-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 0, 0, 0.3);
}

.connect-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.privacy-note {
  font-size: 12px;
  color: #6b7280;
  margin: 0;
  line-height: 1.4;
}

/* Responsive */
@media (max-width: 640px) {
  .modal-container {
    width: 95%;
    margin: 20px;
  }

  .modal-header {
    padding: 20px 20px 0 20px;
  }

  .modal-content {
    padding: 0 20px 20px 20px;
  }
}
</style>
