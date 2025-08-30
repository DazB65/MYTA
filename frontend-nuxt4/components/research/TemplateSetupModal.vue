<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-forest-900 rounded-lg shadow-xl w-full max-w-2xl border border-forest-700">
      <!-- Modal Header -->
      <div class="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 rounded-t-lg">
        <div class="flex items-center space-x-3">
          <div class="h-10 w-10 rounded-lg bg-white/20 flex items-center justify-center">
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div>
            <h2 class="text-2xl font-bold">{{ template?.name || 'Setup Research' }}</h2>
            <p class="text-blue-100">Let's customize this template for your research</p>
          </div>
        </div>
      </div>

      <!-- Modal Content -->
      <div class="p-6">
        <!-- Template Goal -->
        <div class="mb-6 p-4 bg-forest-800 rounded-lg border-l-4 border-blue-500">
          <h3 class="text-lg font-semibold text-white mb-2">Research Goal</h3>
          <p class="text-gray-300">{{ template?.goal }}</p>
        </div>

        <!-- User Input Section -->
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              What's your research topic or content pillar?
            </label>
            <input
              v-model="researchTopic"
              type="text"
              placeholder="e.g., Productivity tips for entrepreneurs, Morning routines, Fitness for beginners..."
              class="w-full rounded-lg bg-forest-700 border border-forest-600 px-4 py-3 text-white placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              @keyup.enter="startResearch"
            />
          </div>

          <div v-if="template?.name === 'Competitor Analysis'">
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Any specific competitors you want to analyze? (optional)
            </label>
            <input
              v-model="specificCompetitors"
              type="text"
              placeholder="e.g., @channel1, @channel2, or leave blank to find them automatically"
              class="w-full rounded-lg bg-forest-700 border border-forest-600 px-4 py-3 text-white placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          <div v-if="template?.name === 'Content Pillar Research'">
            <label class="block text-sm font-medium text-gray-300 mb-2">
              What type of content are you planning?
            </label>
            <select
              v-model="contentType"
              class="w-full rounded-lg bg-forest-700 border border-forest-600 px-4 py-3 text-white focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="">Select content type...</option>
              <option value="tutorials">Tutorials & How-to</option>
              <option value="reviews">Reviews & Comparisons</option>
              <option value="entertainment">Entertainment & Lifestyle</option>
              <option value="educational">Educational & Informative</option>
              <option value="vlogs">Vlogs & Personal</option>
            </select>
          </div>
        </div>

        <!-- Preview Steps -->
        <div class="mt-6 p-4 bg-forest-800 rounded-lg">
          <h3 class="text-lg font-semibold text-white mb-3">Research Steps Preview</h3>
          <div class="space-y-2">
            <div v-for="(step, index) in template?.steps" :key="index" class="flex items-center space-x-3">
              <div class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
                {{ index + 1 }}
              </div>
              <span class="text-gray-300 text-sm">{{ step }}</span>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-between mt-6">
          <button
            @click="$emit('close')"
            class="px-6 py-2 text-gray-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
          <button
            @click="startResearch"
            :disabled="!researchTopic.trim()"
            class="px-6 py-3 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
          >
            Start Research
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  show: boolean
  template: any
}

interface Emits {
  (e: 'close'): void
  (e: 'startResearch', data: any): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const researchTopic = ref('')
const specificCompetitors = ref('')
const contentType = ref('')

const startResearch = () => {
  if (!researchTopic.value.trim()) return

  const researchData = {
    template: props.template,
    topic: researchTopic.value.trim(),
    competitors: specificCompetitors.value.trim(),
    contentType: contentType.value,
    timestamp: new Date()
  }

  emit('startResearch', researchData)
  emit('close')
  
  // Reset form
  researchTopic.value = ''
  specificCompetitors.value = ''
  contentType.value = ''
}
</script>
