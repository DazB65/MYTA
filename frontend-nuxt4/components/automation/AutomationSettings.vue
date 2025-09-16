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
          <div class="text-2xl font-bold text-green-400">6/6</div>
          <div class="text-sm text-gray-400">Always On</div>
        </div>
      </div>

      <!-- Automation Status -->
      <div class="mb-6 rounded-lg p-4 bg-green-900/30 border border-green-600/30 text-green-300">
        <div class="flex items-center space-x-2">
          <span class="text-lg">🚀</span>
          <span class="font-medium">All automations running optimally</span>
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
      <p class="text-sm text-gray-400 mb-6">These automations run automatically based on your subscription tier</p>

      <div class="space-y-4">
        <!-- Auto-Scheduling -->
        <AutomationStatusCard
          icon="📅"
          title="Smart Auto-Scheduling"
          description="AI determines optimal posting times based on your audience activity"
          status="active"
          tier="basic"
        />

        <!-- Auto-Responses -->
        <AutomationStatusCard
          icon="💬"
          title="Smart Auto-Responses"
          description="AI responds to comments in your voice with escalation for complex issues"
          status="active"
          tier="pro"
        />

        <!-- SEO Optimization -->
        <AutomationStatusCard
          icon="🔍"
          title="SEO Auto-Optimization"
          description="Real-time keyword optimization and description enhancement"
          status="active"
          tier="basic"
        />

        <!-- Smart Notifications -->
        <AutomationStatusCard
          icon="🔔"
          title="Smart Notifications"
          description="Intelligent alerts for trending opportunities and performance issues"
          status="active"
          tier="basic"
        />
      </div>
    </div>

    <!-- Advanced Features -->
    <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
      <h4 class="text-lg font-semibold text-white mb-4">Advanced Features</h4>
      <p class="text-sm text-gray-400 mb-6">Premium automations for enhanced productivity</p>

      <div class="space-y-4">
        <!-- Auto-Descriptions -->
        <AutomationStatusCard
          icon="📝"
          title="Auto-Generated Descriptions"
          description="AI creates optimized descriptions with SEO keywords and CTAs"
          status="active"
          tier="pro"
        />

        <!-- Content Ideas -->
        <AutomationStatusCard
          icon="💡"
          title="Content Idea Generation"
          description="Automatic trending topic suggestions and content calendar population"
          status="active"
          tier="pro"
        />
      </div>
    </div>

    <!-- Scheduling Preferences -->
    <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
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
    <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
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
    <div class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6">
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

    <!-- Save Preferences Button -->
    <div class="flex justify-end">
      <button
        @click="saveSettings"
        :disabled="isLoading"
        class="px-6 py-3 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
      >
        <span v-if="isLoading" class="animate-spin">⏳</span>
        <span>{{ isLoading ? 'Saving...' : 'Save Preferences' }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAutomation } from '../../composables/useAutomation'
import AutomationStatusCard from './AutomationStatusCard.vue'

const {
  settings,
  isLoading,
  enabledAutomationsCount,
  urgentNotifications,
  automationStatus,
  getSettings,
  updateSettings
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
  // Only save user preferences (posting days, response tone, etc.)
  const preferencesToSave = {
    preferred_posting_days: settings.value.preferred_posting_days,
    max_posts_per_week: settings.value.max_posts_per_week,
    auto_response_types: settings.value.auto_response_types,
    response_tone: settings.value.response_tone,
    notification_frequency: settings.value.notification_frequency,
    min_notification_priority: settings.value.min_notification_priority
  }
  await updateSettings(preferencesToSave)
}

// Initialize
onMounted(async () => {
  await getSettings()
})
</script>
