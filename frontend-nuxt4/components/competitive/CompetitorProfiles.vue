<template>
  <div class="space-y-6">
    <!-- Header with Add Competitor Button -->
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-xl font-bold text-white">Competitor Profiles</h2>
        <p class="text-gray-400">Detailed analysis of your competitive landscape</p>
      </div>
      <button
        @click="showAddForm = true"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors flex items-center space-x-2"
      >
        <span>➕</span>
        <span>Add Competitor</span>
      </button>
    </div>

    <!-- Add Competitor Form -->
    <div v-if="showAddForm" class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-blue-600/70 shadow-lg p-6">
      <h3 class="text-lg font-semibold text-white mb-4">Add New Competitor</h3>
      <form @submit.prevent="addCompetitor" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Channel Name *</label>
            <input
              v-model="newCompetitor.name"
              type="text"
              required
              placeholder="e.g., TechReviewer Pro"
              class="w-full rounded-lg border-2 border-gray-600/70 bg-gray-700 px-3 py-2 text-white placeholder-gray-400 focus:border-blue-500 focus:outline-none"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">YouTube URL *</label>
            <input
              v-model="newCompetitor.channel_url"
              type="url"
              required
              placeholder="https://youtube.com/@channelname"
              class="w-full rounded-lg border-2 border-gray-600/70 bg-gray-700 px-3 py-2 text-white placeholder-gray-400 focus:border-blue-500 focus:outline-none"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Competitor Type</label>
            <select
              v-model="newCompetitor.tier"
              class="w-full rounded-lg border-2 border-gray-600/70 bg-gray-700 px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
            >
              <option value="direct">Direct Competitor</option>
              <option value="aspirational">Aspirational Target</option>
              <option value="adjacent">Adjacent Player</option>
              <option value="emerging">Emerging Threat</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Notes (Optional)</label>
            <input
              v-model="newCompetitor.notes"
              type="text"
              placeholder="Why are they a competitor?"
              class="w-full rounded-lg border-2 border-gray-600/70 bg-gray-700 px-3 py-2 text-white placeholder-gray-400 focus:border-blue-500 focus:outline-none"
            />
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <button
            type="submit"
            :disabled="isAnalyzing"
            class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <span v-if="isAnalyzing" class="animate-spin">🔍</span>
            <span v-else>✅</span>
            <span>{{ isAnalyzing ? 'Analyzing...' : 'Add & Analyze' }}</span>
          </button>
          <button
            type="button"
            @click="cancelAdd"
            class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>

    <!-- Competitors Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- User Added Competitors -->
      <div
        v-for="competitor in userCompetitors"
        :key="competitor.id"
        class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-blue-600/70 shadow-lg p-6 relative"
      >
        <div class="absolute top-3 right-3 flex items-center space-x-2">
          <span class="px-2 py-1 bg-blue-500/20 text-blue-300 text-xs font-medium rounded-full">Custom</span>
          <button
            @click="removeCompetitor(competitor.id)"
            class="text-red-400 hover:text-red-300 transition-colors"
            title="Remove competitor"
          >
            ❌
          </button>
        </div>

        <h3 class="text-lg font-semibold text-white mb-2 pr-20">{{ competitor.name }}</h3>
        <p class="text-gray-400 mb-4">{{ formatTier(competitor.tier) }}</p>

        <div v-if="competitor.analyzed" class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-gray-300">Subscribers:</span>
            <span class="text-white">{{ formatNumber(competitor.subscriber_count) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-300">Avg Views:</span>
            <span class="text-white">{{ formatNumber(competitor.avg_views) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-300">Growth Rate:</span>
            <span class="text-green-400">{{ (competitor.growth_rate * 100).toFixed(1) }}%</span>
          </div>
          <div v-if="competitor.notes" class="pt-2 border-t border-gray-600">
            <span class="text-gray-300 text-xs">Notes: </span>
            <span class="text-gray-400 text-xs">{{ competitor.notes }}</span>
          </div>
        </div>
        <div v-else class="text-center py-4">
          <div class="animate-spin text-2xl mb-2">🔍</div>
          <p class="text-gray-400 text-sm">Analyzing channel...</p>
        </div>

        <div class="mt-4 pt-4 border-t border-gray-600">
          <a
            :href="competitor.channel_url"
            target="_blank"
            class="text-blue-400 hover:text-blue-300 text-sm flex items-center space-x-1"
          >
            <span>🔗</span>
            <span>View Channel</span>
          </a>
        </div>
      </div>

      <!-- Auto-Detected Competitors -->
      <div
        v-for="competitor in competitors"
        :key="competitor.competitor_id"
        class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 shadow-lg p-6 relative"
      >
        <div class="absolute top-3 right-3">
          <span class="px-2 py-1 bg-orange-500/20 text-orange-300 text-xs font-medium rounded-full">Auto-detected</span>
        </div>

        <h3 class="text-lg font-semibold text-white mb-2 pr-20">{{ competitor.name }}</h3>
        <p class="text-gray-400 mb-4">{{ formatTier(competitor.tier) }}</p>

        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-gray-300">Subscribers:</span>
            <span class="text-white">{{ formatNumber(competitor.subscriber_count) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-300">Avg Views:</span>
            <span class="text-white">{{ formatNumber(competitor.avg_views) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-300">Growth Rate:</span>
            <span class="text-green-400">{{ (competitor.growth_rate * 100).toFixed(1) }}%</span>
          </div>
        </div>

        <div class="mt-4 pt-4 border-t border-gray-600">
          <a
            :href="competitor.channel_url"
            target="_blank"
            class="text-blue-400 hover:text-blue-300 text-sm flex items-center space-x-1"
          >
            <span>🔗</span>
            <span>View Channel</span>
          </a>
        </div>
      </div>

      <!-- Add Competitor Card -->
      <div
        v-if="!showAddForm"
        @click="showAddForm = true"
        class="rounded-xl bg-gray-900/80 backdrop-blur-sm border-2 border-dashed border-gray-600/70 shadow-lg p-6 cursor-pointer hover:border-blue-500/50 transition-colors group"
      >
        <div class="text-center">
          <div class="text-4xl mb-4 group-hover:scale-110 transition-transform">➕</div>
          <h3 class="text-lg font-semibold text-white mb-2">Add Competitor</h3>
          <p class="text-gray-400 text-sm">Track a specific channel you compete with</p>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!competitors?.length && !userCompetitors.length" class="text-center py-12">
      <div class="text-6xl mb-4">🏢</div>
      <h3 class="text-xl font-semibold text-white mb-2">No Competitors Found</h3>
      <p class="text-gray-400 mb-6">Add competitors manually to start tracking your competitive landscape</p>
      <button
        @click="showAddForm = true"
        class="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
      >
        Add Your First Competitor
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'

const props = defineProps({
  competitors: Array,
  marketPosition: Object
})

// Reactive state
const showAddForm = ref(false)
const isAnalyzing = ref(false)
const userCompetitors = ref([])

// New competitor form data
const newCompetitor = reactive({
  name: '',
  channel_url: '',
  tier: 'direct',
  notes: ''
})

// Load saved competitors from localStorage
onMounted(() => {
  const saved = localStorage.getItem('userCompetitors')
  if (saved) {
    userCompetitors.value = JSON.parse(saved)
  }
})

// Save competitors to localStorage
const saveCompetitors = () => {
  localStorage.setItem('userCompetitors', JSON.stringify(userCompetitors.value))
}

// Add new competitor
const addCompetitor = async () => {
  if (!newCompetitor.name || !newCompetitor.channel_url) return

  isAnalyzing.value = true

  try {
    // Create competitor object
    const competitor = {
      id: Date.now().toString(),
      name: newCompetitor.name,
      channel_url: newCompetitor.channel_url,
      tier: newCompetitor.tier,
      notes: newCompetitor.notes,
      analyzed: false,
      subscriber_count: 0,
      avg_views: 0,
      growth_rate: 0,
      added_date: new Date().toISOString()
    }

    // Add to list
    userCompetitors.value.push(competitor)
    saveCompetitors()

    // Simulate analysis (in real app, this would call YouTube API)
    setTimeout(() => {
      const competitorIndex = userCompetitors.value.findIndex(c => c.id === competitor.id)
      if (competitorIndex !== -1) {
        // Mock analysis results
        userCompetitors.value[competitorIndex] = {
          ...userCompetitors.value[competitorIndex],
          analyzed: true,
          subscriber_count: Math.floor(Math.random() * 1000000) + 10000,
          avg_views: Math.floor(Math.random() * 100000) + 5000,
          growth_rate: (Math.random() * 0.2) + 0.01 // 1-21% growth
        }
        saveCompetitors()
      }
      isAnalyzing.value = false
    }, 3000)

    // Reset form
    resetForm()

  } catch (error) {
    console.error('Error adding competitor:', error)
    isAnalyzing.value = false
  }
}

// Remove competitor
const removeCompetitor = (id) => {
  if (confirm('Are you sure you want to remove this competitor?')) {
    userCompetitors.value = userCompetitors.value.filter(c => c.id !== id)
    saveCompetitors()
  }
}

// Cancel adding competitor
const cancelAdd = () => {
  resetForm()
}

// Reset form
const resetForm = () => {
  showAddForm.value = false
  newCompetitor.name = ''
  newCompetitor.channel_url = ''
  newCompetitor.tier = 'direct'
  newCompetitor.notes = ''
}

// Format numbers
const formatNumber = (num) => {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toString()
}

// Format tier names
const formatTier = (tier) => {
  const tierMap = {
    'direct': 'Direct Competitor',
    'aspirational': 'Aspirational Target',
    'adjacent': 'Adjacent Player',
    'emerging': 'Emerging Threat'
  }
  return tierMap[tier] || tier
}
</script>
