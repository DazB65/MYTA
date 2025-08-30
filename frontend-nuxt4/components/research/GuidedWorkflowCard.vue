<template>
  <div class="bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg p-6 text-white shadow-lg border border-blue-500">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-3">
        <div class="h-10 w-10 rounded-lg bg-white/20 flex items-center justify-center">
          <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <h3 class="text-xl font-bold">{{ workflowData.template.name }}</h3>
          <p class="text-blue-100 text-sm">{{ workflowData.topic }}</p>
        </div>
      </div>
      <div class="text-right">
        <div class="text-sm text-blue-100">Progress</div>
        <div class="text-2xl font-bold">{{ completedSteps }}/{{ totalSteps }}</div>
      </div>
    </div>

    <!-- Progress Bar -->
    <div class="mb-6">
      <div class="w-full bg-white/20 rounded-full h-2">
        <div 
          class="bg-white rounded-full h-2 transition-all duration-500"
          :style="{ width: `${(completedSteps / totalSteps) * 100}%` }"
        ></div>
      </div>
    </div>

    <!-- Current Step -->
    <div v-if="currentStep" class="mb-6 p-4 bg-white/10 rounded-lg border border-white/20">
      <div class="flex items-center space-x-3 mb-3">
        <div class="w-8 h-8 bg-white rounded-full flex items-center justify-center text-blue-600 font-bold text-sm">
          {{ currentStepIndex + 1 }}
        </div>
        <h4 class="text-lg font-semibold">{{ currentStep.title }}</h4>
      </div>
      <p class="text-blue-100 mb-4">{{ currentStep.description }}</p>
      
      <!-- Step Actions -->
      <div class="space-y-3">
        <button
          v-for="action in currentStep.actions"
          :key="action.id"
          @click="executeAction(action)"
          :disabled="action.completed"
          class="w-full flex items-center justify-between p-4 bg-white/10 hover:bg-white/20 disabled:bg-green-500/20 rounded-lg transition-colors border border-white/20 hover:border-white/40"
        >
          <div class="flex items-center space-x-3">
            <div class="flex-shrink-0">
              <svg v-if="action.completed" class="h-6 w-6 text-green-300" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              <div v-else class="w-6 h-6 rounded-full bg-white/20 flex items-center justify-center">
                <svg class="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                </svg>
              </div>
            </div>
            <div class="text-left">
              <div class="font-medium text-white">{{ action.label }}</div>
              <div class="text-sm text-blue-100">{{ getActionDescription(action.id) }}</div>
            </div>
          </div>
          <div class="flex-shrink-0">
            <span v-if="action.completed" class="px-3 py-1 bg-green-500/20 text-green-300 text-sm rounded-full">✓ Done</span>
            <span v-else class="px-3 py-1 bg-white/10 text-white text-sm rounded-full">Click to start</span>
          </div>
        </button>
      </div>
    </div>

    <!-- Completed Steps Summary -->
    <div v-if="completedSteps > 0" class="mb-4">
      <h4 class="text-sm font-semibold text-blue-100 mb-2">Completed Steps:</h4>
      <div class="space-y-1">
        <div 
          v-for="(step, index) in steps.slice(0, currentStepIndex)"
          :key="index"
          class="flex items-center space-x-2 text-sm text-blue-100"
        >
          <svg class="h-4 w-4 text-green-300" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
          </svg>
          <span>{{ step.title }}</span>
        </div>
      </div>
    </div>

    <!-- Next Step Preview -->
    <div v-if="nextStep" class="p-3 bg-white/5 rounded-lg border border-white/10">
      <div class="flex items-center space-x-2 mb-1">
        <div class="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-xs font-bold">
          {{ currentStepIndex + 2 }}
        </div>
        <span class="text-sm font-medium text-blue-100">Next: {{ nextStep.title }}</span>
      </div>
      <p class="text-xs text-blue-200 ml-8">{{ nextStep.description }}</p>
    </div>

    <!-- Completion -->
    <div v-if="isCompleted" class="text-center p-4 bg-green-500/20 rounded-lg border border-green-400/30">
      <svg class="h-12 w-12 text-green-300 mx-auto mb-2" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
      </svg>
      <h4 class="text-lg font-bold text-green-300 mb-1">Research Complete!</h4>
      <p class="text-green-200 text-sm mb-3">You've completed all research steps</p>
      <button
        @click="$emit('exportResults')"
        class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium transition-colors"
      >
        Export to Content Studio
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

interface Props {
  workflowData: any
}

interface Emits {
  (e: 'executeAction', action: any): void
  (e: 'exportResults'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Generate workflow steps based on template
const steps = computed(() => {
  const template = props.workflowData.template
  const topic = props.workflowData.topic
  
  if (template.name === 'Content Pillar Research') {
    return [
      {
        title: 'Define Your Focus',
        description: `Research successful content in the "${topic}" pillar`,
        actions: [
          { id: 'niche-analysis', label: 'Run Niche Analysis', completed: false, tool: 'niche-analysis' },
          { id: 'find-content', label: 'Find Related Content', completed: false, tool: 'find-content' }
        ]
      },
      {
        title: 'Analyze Top Videos',
        description: 'Find and analyze the best performing videos in your pillar',
        actions: [
          { id: 'add-videos', label: 'Add Top Videos to Canvas', completed: false, tool: 'video-search' },
          { id: 'analyze-patterns', label: 'Analyze Content Patterns', completed: false, tool: 'pattern-analysis' }
        ]
      },
      {
        title: 'Study Engagement',
        description: 'Understand what makes content engaging in this pillar',
        actions: [
          { id: 'engagement-analysis', label: 'Analyze Engagement Patterns', completed: false, tool: 'engagement-analysis' },
          { id: 'audience-insights', label: 'Study Audience Behavior', completed: false, tool: 'audience-analysis' }
        ]
      },
      {
        title: 'Create Strategy',
        description: 'Develop your content strategy based on research findings',
        actions: [
          { id: 'strategy-notes', label: 'Document Key Insights', completed: false, tool: 'notes' },
          { id: 'content-plan', label: 'Create Content Plan', completed: false, tool: 'content-plan' }
        ]
      }
    ]
  }
  
  // Default steps for other templates
  return template.steps.map((step: string, index: number) => ({
    title: step,
    description: `Complete step ${index + 1} of your research workflow`,
    actions: [
      { id: `step-${index}`, label: 'Complete This Step', completed: false, tool: 'generic' }
    ]
  }))
})

const currentStepIndex = ref(0)
const currentStep = computed(() => steps.value[currentStepIndex.value])
const nextStep = computed(() => steps.value[currentStepIndex.value + 1])
const totalSteps = computed(() => steps.value.length)
const completedSteps = computed(() => currentStepIndex.value)
const isCompleted = computed(() => currentStepIndex.value >= totalSteps.value)

const executeAction = (action: any) => {
  if (action.completed) return

  // Mark action as completed
  action.completed = true

  // Check if all actions in current step are completed
  const allActionsCompleted = currentStep.value.actions.every((a: any) => a.completed)

  if (allActionsCompleted && currentStepIndex.value < totalSteps.value - 1) {
    // Move to next step after a short delay
    setTimeout(() => {
      currentStepIndex.value++
    }, 1000)
  }

  // Emit action to parent component
  emit('executeAction', {
    action,
    step: currentStep.value,
    workflowData: props.workflowData
  })
}

const getActionDescription = (actionId: string) => {
  const descriptions = {
    'niche-analysis': 'Analyze market opportunities and trends',
    'find-content': 'Find sample videos to analyze',
    'add-videos': 'Add top performing videos to your canvas',
    'analyze-patterns': 'Identify successful content patterns',
    'engagement-analysis': 'Study audience engagement metrics',
    'audience-analysis': 'Understand your target audience',
    'strategy-notes': 'Document key insights and findings',
    'content-plan': 'Create actionable content strategy'
  }
  return descriptions[actionId] || 'Complete this research step'
}
</script>
