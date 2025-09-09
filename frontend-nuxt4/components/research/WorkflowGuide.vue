<template>
  <div class="bg-forest-800 rounded-lg border border-forest-600 p-4">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
          <svg class="h-5 w-5 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <h3 class="font-semibold text-white">{{ currentTemplate?.name || 'Research Workflow' }}</h3>
          <p class="text-xs text-gray-400">Step {{ currentStep + 1 }} of {{ totalSteps }}</p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <div class="w-16 h-2 bg-forest-700 rounded-full overflow-hidden">
          <div
            class="h-full bg-blue-500 transition-all duration-300"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
        <span class="text-xs text-gray-400">{{ Math.round(progress) }}%</span>
        <div class="text-xs text-gray-500">{{ researchItemsCount }} items</div>
      </div>
    </div>

    <!-- Current Step -->
    <div v-if="currentTemplate && currentStepData" class="mb-4">
      <div class="flex items-start space-x-3 p-3 bg-forest-700 rounded-lg border-l-4 border-blue-500">
        <div class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-white text-xs font-bold mt-0.5">
          {{ currentStep + 1 }}
        </div>
        <div class="flex-1">
          <h4 class="font-medium text-white mb-1">{{ currentStepData.title }}</h4>
          <p class="text-sm text-gray-300 mb-2">{{ currentStepData.description }}</p>
          
          <!-- Step Actions -->
          <div v-if="currentStepData.actions?.length" class="space-y-2">
            <p class="text-xs font-medium text-gray-400">Actions:</p>
            <div class="space-y-1">
              <button
                v-for="action in currentStepData.actions"
                :key="action.id"
                @click="executeAction(action)"
                :disabled="action.completed"
                class="flex items-center space-x-2 text-sm px-3 py-1 rounded bg-forest-600 hover:bg-forest-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <span v-if="action.completed" class="text-green-400">✓</span>
                <span v-else class="text-gray-400">○</span>
                <span class="text-white">{{ action.label }}</span>
              </button>
            </div>
          </div>

          <!-- Step Tips -->
          <div v-if="currentStepData.tips?.length" class="mt-3 p-2 bg-forest-600 rounded text-xs">
            <p class="font-medium text-yellow-400 mb-1">💡 Tips:</p>
            <ul class="text-gray-300 space-y-1">
              <li v-for="tip in currentStepData.tips" :key="tip">• {{ tip }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <div class="flex items-center justify-between">
      <button
        @click="previousStep"
        :disabled="currentStep === 0"
        class="flex items-center space-x-1 px-3 py-1 text-sm bg-forest-700 text-white rounded hover:bg-forest-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
        <span>Previous</span>
      </button>

      <div class="flex items-center space-x-2">
        <button
          v-if="currentStep < totalSteps - 1"
          @click="nextStep"
          :disabled="!canProceed"
          class="flex items-center space-x-1 px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <span>Next Step</span>
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </button>
        <button
          v-else
          @click="completeWorkflow"
          :disabled="!canProceed"
          class="flex items-center space-x-1 px-3 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <span>Complete</span>
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Template Selection -->
    <div v-if="!currentTemplate" class="space-y-3">
      <h4 class="font-medium text-white">Choose a Research Template</h4>
      <div class="grid grid-cols-1 gap-2">
        <button
          v-for="template in availableTemplates"
          :key="template.id"
          @click="startTemplate(template)"
          class="flex items-center space-x-3 p-3 bg-gray-900/80 backdrop-blur-sm border border-gray-700/50 rounded-lg hover:bg-gray-600 transition-colors text-left"
        >
          <div class="w-8 h-8 rounded-lg flex items-center justify-center" :style="{ backgroundColor: template.color }">
            {{ template.icon }}
          </div>
          <div class="flex-1">
            <div class="font-medium text-white">{{ template.name }}</div>
            <div class="text-sm text-gray-400">{{ template.description }}</div>
          </div>
          <div class="text-xs text-gray-500">{{ template.steps.length }} steps</div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

interface Props {
  researchItems: any[]
}

interface Emits {
  (e: 'executeAction', action: any): void
  (e: 'templateComplete', template: any): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const currentTemplate = ref(null)
const currentStep = ref(0)
const completedActions = ref(new Set())

const availableTemplates = [
  {
    id: 'competitor-analysis',
    name: 'Competitor Analysis',
    description: 'Systematic analysis of competitors in your niche',
    icon: '⚔️',
    color: '#ef4444',
    steps: [
      {
        title: 'Identify Competitors',
        description: 'Find and list your main competitors',
        actions: [
          { id: 'search-competitors', label: 'Search for competitor channels', type: 'search' },
          { id: 'add-competitors', label: 'Add top 5 competitors to canvas', type: 'manual' }
        ],
        tips: ['Focus on channels with similar audience size', 'Look for channels in your exact niche']
      },
      {
        title: 'Analyze Top Content',
        description: 'Study their best performing videos',
        actions: [
          { id: 'analyze-videos', label: 'Analyze top 10 videos from each competitor', type: 'analysis' },
          { id: 'document-patterns', label: 'Document common patterns', type: 'manual' }
        ],
        tips: ['Look for common themes and formats', 'Note thumbnail and title patterns']
      },
      {
        title: 'Identify Opportunities',
        description: 'Find gaps and opportunities',
        actions: [
          { id: 'find-gaps', label: 'Identify content gaps', type: 'analysis' },
          { id: 'create-strategy', label: 'Create competitive strategy', type: 'manual' }
        ],
        tips: ['Look for topics they haven\'t covered', 'Find ways to improve on their content']
      }
    ]
  },
  {
    id: 'viral-analysis',
    name: 'Viral Video Analysis',
    description: 'Analyze viral content patterns and trends',
    icon: '📈',
    color: '#eab308',
    steps: [
      {
        title: 'Find Viral Content',
        description: 'Collect viral videos in your niche',
        actions: [
          { id: 'search-viral', label: 'Search for viral videos (1M+ views)', type: 'search' },
          { id: 'add-viral', label: 'Add 10-15 viral videos to canvas', type: 'manual' }
        ],
        tips: ['Focus on recent viral content', 'Include videos from different creators']
      },
      {
        title: 'Analyze Patterns',
        description: 'Study what made them go viral',
        actions: [
          { id: 'analyze-elements', label: 'Analyze titles, thumbnails, and hooks', type: 'analysis' },
          { id: 'timing-analysis', label: 'Study posting timing and trends', type: 'analysis' }
        ],
        tips: ['Look for emotional triggers', 'Note timing and current events']
      }
    ]
  }
]

const totalSteps = computed(() => currentTemplate.value?.steps.length || 0)
const progress = computed(() => totalSteps.value > 0 ? ((currentStep.value + 1) / totalSteps.value) * 100 : 0)
const currentStepData = computed(() => currentTemplate.value?.steps[currentStep.value])
const researchItemsCount = computed(() => props.researchItems.length)
const canProceed = computed(() => {
  if (!currentStepData.value?.actions) return true
  return currentStepData.value.actions.every(action =>
    action.completed || completedActions.value.has(action.id)
  )
})

const startTemplate = (template) => {
  currentTemplate.value = template
  currentStep.value = 0
  completedActions.value.clear()
}

const nextStep = () => {
  if (currentStep.value < totalSteps.value - 1) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const executeAction = (action) => {
  completedActions.value.add(action.id)
  action.completed = true

  // Provide immediate feedback
  const feedback = getActionFeedback(action.id)
  if (feedback) {
    setTimeout(() => {
      alert(feedback)
    }, 100)
  }

  emit('executeAction', { action, template: currentTemplate.value, step: currentStep.value })
}

const getActionFeedback = (actionId) => {
  const feedback = {
    'search-competitors': 'Great! Competitor channels will be added to your canvas for analysis.',
    'search-viral': 'Excellent! Viral videos will be analyzed for patterns and trends.',
    'analyze-videos': 'Perfect! Video analysis will identify key success patterns.',
    'analyze-elements': 'Awesome! Element analysis will reveal what makes content successful.',
    'find-gaps': 'Outstanding! Gap analysis will uncover new content opportunities.',
    'add-competitors': 'Remember to focus on channels with similar audience size and content style.',
    'document-patterns': 'Look for common themes in titles, thumbnails, and content structure.',
    'create-strategy': 'Use your findings to create a unique competitive advantage.'
  }
  return feedback[actionId]
}

const completeWorkflow = () => {
  emit('templateComplete', currentTemplate.value)
  currentTemplate.value = null
  currentStep.value = 0
  completedActions.value.clear()
}
</script>
