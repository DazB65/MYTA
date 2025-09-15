<template>
  <div class="space-y-6">
    <!-- Automation Overview -->
    <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
      <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-500">
            <span class="text-white text-xl">🤖</span>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-white">Intelligent Automation</h3>
            <p class="text-sm text-gray-400">Save 2-3 hours per video with AI automation</p>
          </div>
        </div>
        <div class="text-right">
          <div class="text-2xl font-bold text-orange-500">{{ enabledAutomationsCount }}/6</div>
          <div class="text-sm text-gray-400">Active</div>
        </div>
      </div>

      <!-- Automation Status -->
      <div class="mb-6 rounded-lg p-4" :class="getStatusColor(automationStatus.status)">
        <div class="flex items-center space-x-2">
          <span class="text-lg">{{ getStatusIcon(automationStatus.status) }}</span>
          <span class="font-medium">{{ automationStatus.message }}</span>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-cols-3 gap-4">
        <div class="text-center p-3 rounded-lg bg-gray-700">
          <div class="text-xl font-bold text-green-400">2.5h</div>
          <div class="text-xs text-gray-400">Time Saved/Video</div>
        </div>
        <div class="text-center p-3 rounded-lg bg-gray-700">
          <div class="text-xl font-bold text-blue-400">+25%</div>
          <div class="text-xs text-gray-400">Performance Boost</div>
        </div>
        <div class="text-center p-3 rounded-lg bg-gray-700">
          <div class="text-xl font-bold text-purple-400">{{ urgentNotifications.length }}</div>
          <div class="text-xs text-gray-400">Urgent Alerts</div>
        </div>
      </div>
    </div>

    <!-- Core Automation Features -->
    <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
      <h4 class="text-lg font-semibold text-white mb-4">Core Automation Features</h4>
      
      <div class="space-y-4">
        <!-- Auto-Scheduling -->
        <AutomationToggleCard
          :enabled="settings.auto_scheduling_enabled"
          @toggle="toggleAutomation('auto_scheduling_enabled')"
          icon="📅"
          title="Smart Auto-Scheduling"
          description="AI determines optimal posting times based on your audience activity"
          :loading="isLoading"
        />

        <!-- Auto-Responses -->
        <AutomationToggleCard
          :enabled="settings.auto_responses_enabled"
          @toggle="toggleAutomation('auto_responses_enabled')"
          icon="💬"
          title="Smart Auto-Responses"
          description="AI responds to comments in your voice with escalation for complex issues"
          :loading="isLoading"
        />

        <!-- SEO Optimization -->
        <AutomationToggleCard
          :enabled="settings.seo_optimization_enabled"
          @toggle="toggleAutomation('seo_optimization_enabled')"
          icon="🔍"
          title="SEO Auto-Optimization"
          description="Real-time keyword optimization and description enhancement"
          :loading="isLoading"
        />

        <!-- Smart Notifications -->
        <AutomationToggleCard
          :enabled="settings.smart_notifications_enabled"
          @toggle="toggleAutomation('smart_notifications_enabled')"
          icon="🔔"
          title="Smart Notifications"
          description="Intelligent alerts for trending opportunities and performance issues"
          :loading="isLoading"
        />
      </div>
    </div>

    <!-- Advanced Features -->
    <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
      <h4 class="text-lg font-semibold text-white mb-4">Advanced Features</h4>
      
      <div class="space-y-4">
        <!-- Auto-Descriptions -->
        <AutomationToggleCard
          :enabled="settings.auto_descriptions_enabled"
          @toggle="toggleAutomation('auto_descriptions_enabled')"
          icon="📝"
          title="Auto-Generated Descriptions"
          description="AI creates optimized descriptions with SEO keywords and CTAs"
          :loading="isLoading"
        />

        <!-- Content Ideas -->
        <AutomationToggleCard
          :enabled="settings.content_ideas_enabled"
          @toggle="toggleAutomation('content_ideas_enabled')"
          icon="💡"
          title="Content Idea Generation"
          description="Automatic trending topic suggestions and content calendar population"
          :loading="isLoading"
        />
      </div>
    </div>

    <!-- Scheduling Preferences -->
    <div v-if="settings.auto_scheduling_enabled" class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
      <h4 class="text-lg font-semibold text-white mb-4">📅 Scheduling Preferences</h4>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Preferred Days -->
        <div>
          <label class="block text-sm font-medium text-white mb-3">Preferred Posting Days</label>
          <div class="grid grid-cols-2 gap-2">
            <label v-for="day in daysOfWeek" :key="day.value" class="flex items-center space-x-2 p-2 rounded-lg bg-gray-700 hover:bg-gray-600 cursor-pointer">
              <input
                type="checkbox"
                :value="day.value"
                v-model="settings.preferred_posting_days"
                class="rounded border-gray-600 text-orange-500 focus:ring-orange-500"
              />
              <span class="text-sm text-gray-300">{{ day.label }}</span>
            </label>
          </div>
        </div>

        <!-- Max Posts Per Week -->
        <div>
          <label class="block text-sm font-medium text-white mb-3">Max Posts Per Week</label>
          <div class="flex items-center space-x-4">
            <input
              type="range"
              min="1"
              max="14"
              v-model="settings.max_posts_per_week"
              class="flex-1 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
            />
            <div class="text-lg font-bold text-orange-500 min-w-[3rem]">
              {{ settings.max_posts_per_week }}
            </div>
          </div>
          <p class="text-xs text-gray-400 mt-1">AI will respect this limit when scheduling content</p>
        </div>
      </div>
    </div>

    <!-- Response Preferences -->
    <div v-if="settings.auto_responses_enabled" class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
      <h4 class="text-lg font-semibold text-white mb-4">💬 Response Preferences</h4>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Response Types -->
        <div>
          <label class="block text-sm font-medium text-white mb-3">Auto-Response Types</label>
          <div class="space-y-2">
            <label v-for="type in responseTypes" :key="type.value" class="flex items-center space-x-2 p-2 rounded-lg bg-gray-700 hover:bg-gray-600 cursor-pointer">
              <input
                type="checkbox"
                :value="type.value"
                v-model="settings.auto_response_types"
                class="rounded border-gray-600 text-orange-500 focus:ring-orange-500"
              />
              <span class="text-sm text-gray-300">{{ type.label }}</span>
            </label>
          </div>
        </div>

        <!-- Response Tone -->
        <div>
          <label class="block text-sm font-medium text-white mb-3">Response Tone</label>
          <select
            v-model="settings.response_tone"
            class="w-full rounded-lg border-2 border-gray-600/70 bg-gray-700 px-4 py-3 text-white focus:border-orange-500 focus:outline-none"
          >
            <option value="friendly">Friendly & Casual</option>
            <option value="professional">Professional</option>
            <option value="enthusiastic">Enthusiastic</option>
            <option value="helpful">Helpful & Supportive</option>
          </select>
          <p class="text-xs text-gray-400 mt-1">AI will match this tone in responses</p>
        </div>
      </div>
    </div>

    <!-- Notification Preferences -->
    <div v-if="settings.smart_notifications_enabled" class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
      <h4 class="text-lg font-semibold text-white mb-4">🔔 Notification Preferences</h4>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Notification Frequency -->
        <div>
          <label class="block text-sm font-medium text-white mb-3">Notification Frequency</label>
          <select
            v-model="settings.notification_frequency"
            class="w-full rounded-lg border-2 border-gray-600/70 bg-gray-700 px-4 py-3 text-white focus:border-orange-500 focus:outline-none"
          >
            <option value="real_time">Real-time</option>
            <option value="hourly">Hourly Digest</option>
            <option value="daily">Daily Summary</option>
            <option value="weekly">Weekly Report</option>
          </select>
        </div>

        <!-- Minimum Priority -->
        <div>
          <label class="block text-sm font-medium text-white mb-3">Minimum Priority</label>
          <select
            v-model="settings.min_notification_priority"
            class="w-full rounded-lg border-2 border-gray-600/70 bg-gray-700 px-4 py-3 text-white focus:border-orange-500 focus:outline-none"
          >
            <option value="low">All Notifications</option>
            <option value="medium">Medium & Above</option>
            <option value="high">High Priority Only</option>
            <option value="urgent">Urgent Only</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Save Button -->
    <div class="flex justify-end">
      <button
        @click="saveSettings"
        :disabled="isLoading"
        class="px-6 py-3 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
      >
        <span v-if="isLoading" class="animate-spin">⏳</span>
        <span>{{ isLoading ? 'Saving...' : 'Save Automation Settings' }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAutomation } from '../../composables/useAutomation'
import AutomationToggleCard from './AutomationToggleCard.vue'

const {
  settings,
  isLoading,
  enabledAutomationsCount,
  urgentNotifications,
  automationStatus,
  getSettings,
  updateSettings,
  toggleAutomation
} = useAutomation()

// Data
const daysOfWeek = [
  { value: 'monday', label: 'Monday' },
  { value: 'tuesday', label: 'Tuesday' },
  { value: 'wednesday', label: 'Wednesday' },
  { value: 'thursday', label: 'Thursday' },
  { value: 'friday', label: 'Friday' },
  { value: 'saturday', label: 'Saturday' },
  { value: 'sunday', label: 'Sunday' }
]

const responseTypes = [
  { value: 'questions', label: 'Questions' },
  { value: 'compliments', label: 'Compliments' },
  { value: 'simple', label: 'Simple Comments' },
  { value: 'feedback', label: 'Feedback' }
]

// Methods
const saveSettings = async () => {
  await updateSettings(settings.value)
}

const getStatusColor = (status) => {
  switch (status) {
    case 'optimal': return 'bg-green-900/30 border border-green-600/30 text-green-300'
    case 'good': return 'bg-blue-900/30 border border-blue-600/30 text-blue-300'
    case 'partial': return 'bg-yellow-900/30 border border-yellow-600/30 text-yellow-300'
    case 'minimal': return 'bg-red-900/30 border border-red-600/30 text-red-300'
    default: return 'bg-gray-900/30 border border-gray-600/30 text-gray-300'
  }
}

const getStatusIcon = (status) => {
  switch (status) {
    case 'optimal': return '🚀'
    case 'good': return '✅'
    case 'partial': return '⚠️'
    case 'minimal': return '🔴'
    default: return '⚙️'
  }
}

// Initialize
onMounted(async () => {
  await getSettings()
})
</script>
