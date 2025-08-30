<template>
  <div class="min-h-screen bg-forest-950">
    <!-- Header -->
    <div class="bg-forest-900 border-b border-forest-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center space-x-4">
            <h1 class="text-xl font-bold text-white">Research Workspace</h1>
            <span class="text-blue-400">•</span>
            <p class="text-gray-400">AI-powered research for YouTube success</p>
          </div>
          <div class="flex items-center space-x-3">
            <button class="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
              </svg>
              <span>Templates</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-12 gap-6">
        
        <!-- Left Sidebar - Step-by-Step Workflow -->
        <div class="col-span-4 space-y-4">
          
          <!-- Progress Overview -->
          <div class="bg-forest-800 rounded-lg p-4 border border-forest-700">
            <div class="flex items-center justify-between mb-3">
              <h3 class="text-lg font-bold text-white">Research Progress</h3>
              <span class="text-sm text-gray-400">{{ workflowProgress }}% Complete</span>
            </div>
            <div class="w-full bg-forest-700 rounded-full h-2 mb-3">
              <div
                class="bg-blue-500 rounded-full h-2 transition-all duration-500"
                :style="{ width: `${workflowProgress}%` }"
              ></div>
            </div>
            <button
              @click="resetWorkflow"
              class="text-xs text-gray-400 hover:text-white transition-colors"
            >
              Reset Workflow
            </button>
          </div>

          <!-- Workflow Steps -->
          <div class="space-y-3">
            <div
              v-for="step in workflowSteps"
              :key="step.id"
              @click="goToStep(step.id)"
              :class="[
                'rounded-lg p-4 border transition-all cursor-pointer',
                step.id === currentStep ? 'bg-blue-600 border-blue-500 shadow-lg' : 
                step.completed ? 'bg-green-600/20 border-green-500/50' :
                step.unlocked ? 'bg-forest-800 border-forest-600 hover:border-forest-500' :
                'bg-forest-900 border-forest-700 opacity-50 cursor-not-allowed'
              ]"
            >
              <div class="flex items-center space-x-3">
                <!-- Step Icon -->
                <div :class="[
                  'w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm',
                  step.completed ? 'bg-green-500 text-white' :
                  step.id === currentStep ? 'bg-white text-blue-600' :
                  step.unlocked ? 'bg-forest-700 text-white' :
                  'bg-forest-800 text-gray-500'
                ]">
                  <svg v-if="step.completed" class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <span v-else>{{ step.id }}</span>
                </div>
                
                <!-- Step Content -->
                <div class="flex-1">
                  <h4 :class="[
                    'font-semibold',
                    step.id === currentStep ? 'text-white' :
                    step.completed ? 'text-green-300' :
                    step.unlocked ? 'text-white' :
                    'text-gray-500'
                  ]">{{ step.title }}</h4>
                  <p :class="[
                    'text-sm',
                    step.id === currentStep ? 'text-blue-100' :
                    step.completed ? 'text-green-200' :
                    step.unlocked ? 'text-gray-400' :
                    'text-gray-600'
                  ]">{{ step.description }}</p>
                </div>
                
                <!-- Step Status -->
                <div v-if="step.id === currentStep" class="text-blue-200">
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
              </div>
            </div>
          </div>

          <!-- Current Step Actions -->
          <div v-if="currentStepData" class="bg-forest-800 rounded-lg p-4 border border-forest-700">
            <h4 class="text-white font-semibold mb-2">{{ currentStepData.title }}</h4>
            <p class="text-gray-400 text-sm mb-3">{{ currentStepData.requirements }}</p>
            
            <!-- Step 1: Template Selection -->
            <div v-if="currentStep === 1" class="space-y-2">
              <button
                @click="showTemplates = true"
                class="w-full flex items-center space-x-3 bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg transition-colors"
              >
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
                </svg>
                <span>Choose Research Template</span>
              </button>
              <div v-if="selectedTemplate" class="text-green-400 text-sm">
                ✓ Selected: {{ selectedTemplate.name }}
              </div>
            </div>

            <!-- Next Step Button -->
            <div v-if="canProceedToNextStep && currentStep < 5" class="mt-4 pt-3 border-t border-forest-700">
              <button
                @click="completeCurrentStep"
                class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors"
              >
                Complete Step & Continue
              </button>
            </div>
          </div>
        </div>

        <!-- Right Side - Results Dashboard -->
        <div class="col-span-8 space-y-4">
          <!-- Dashboard Header -->
          <div class="bg-forest-900 rounded-lg p-4 border border-forest-700">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-bold text-white">Research Results</h2>
                <p class="text-gray-400">AI-powered insights for your content strategy</p>
              </div>
              <div class="flex items-center space-x-4">
                <div class="text-sm text-gray-400">0 videos analyzed</div>
                <button class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors">
                  Export Results
                </button>
              </div>
            </div>
          </div>

          <!-- Dashboard Content -->
          <div class="grid grid-cols-2 gap-4">
            <!-- Top Competitors -->
            <div class="bg-forest-900 rounded-lg p-4 border border-forest-700">
              <div class="flex items-center mb-4">
                <svg class="h-5 w-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 6a3 3 0 11-6 0 3 3 0 616 0zM17 6a3 3 0 11-6 0 3 3 0 616 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 515 5v1H1v-1a5 5 0 515-5z"/>
                </svg>
                <h3 class="text-lg font-bold text-white">Top Competitors</h3>
              </div>
              <div class="text-center py-8">
                <p class="text-gray-400 mb-4">No competitor analysis yet</p>
                <p class="text-sm text-gray-500">Use the research tools to analyze competitors</p>
              </div>
            </div>

            <!-- Trending Topics -->
            <div class="bg-forest-900 rounded-lg p-4 border border-forest-700">
              <div class="flex items-center mb-4">
                <svg class="h-5 w-5 text-blue-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clip-rule="evenodd"/>
                </svg>
                <h3 class="text-lg font-bold text-white">Trending Topics</h3>
              </div>
              <div class="space-y-3">
                <div v-for="trend in trendingTopics" :key="trend.id" class="flex items-center justify-between">
                  <div>
                    <h4 class="font-medium text-white">{{ trend.title }}</h4>
                    <p class="text-sm text-gray-400">{{ trend.category }}</p>
                  </div>
                  <div class="text-green-400 font-bold">+{{ trend.growth }}%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Reactive state
const currentStep = ref(1)
const selectedTemplate = ref(null)
const showTemplates = ref(false)

const workflowSteps = ref([
  {
    id: 1,
    title: 'Define Research Goal',
    description: 'Choose your research focus and objectives',
    completed: false,
    unlocked: true,
    requirements: 'Select a research template and define your goal'
  },
  {
    id: 2,
    title: 'Gather Intelligence',
    description: 'Collect data using AI research tools',
    completed: false,
    unlocked: false,
    requirements: 'Use research tools to gather at least 3 data points'
  },
  {
    id: 3,
    title: 'Analyze Content',
    description: 'Deep-dive analysis of collected content',
    completed: false,
    unlocked: false,
    requirements: 'Analyze key videos and extract insights'
  },
  {
    id: 4,
    title: 'Generate Insights',
    description: 'AI-powered insights and recommendations',
    completed: false,
    unlocked: false,
    requirements: 'Review and confirm AI-generated insights'
  },
  {
    id: 5,
    title: 'Create Strategy',
    description: 'Export actionable content strategy',
    completed: false,
    unlocked: false,
    requirements: 'Generate and export your content strategy'
  }
])

const trendingTopics = ref([
  { id: 1, title: 'AI Content Creation', growth: 45, category: 'Technology' },
  { id: 2, title: 'YouTube Shorts Strategy', growth: 32, category: 'Marketing' },
  { id: 3, title: 'Creator Economy 2024', growth: 28, category: 'Business' },
  { id: 4, title: 'Video SEO Tips', growth: 25, category: 'SEO' },
  { id: 5, title: 'Monetization Strategies', growth: 22, category: 'Business' }
])

// Computed properties
const workflowProgress = computed(() => {
  const completedSteps = workflowSteps.value.filter(step => step.completed).length
  return Math.round((completedSteps / workflowSteps.value.length) * 100)
})

const currentStepData = computed(() => {
  return workflowSteps.value.find(step => step.id === currentStep.value)
})

const canProceedToNextStep = computed(() => {
  switch (currentStep.value) {
    case 1: return selectedTemplate.value !== null
    case 2: return false // Add logic for step 2
    case 3: return false // Add logic for step 3
    case 4: return false // Add logic for step 4
    case 5: return false // Final step
    default: return false
  }
})

// Functions
const goToStep = (stepId) => {
  const step = workflowSteps.value.find(s => s.id === stepId)
  if (step && step.unlocked) {
    currentStep.value = stepId
  }
}

const completeCurrentStep = () => {
  const current = currentStepData.value
  if (current && canProceedToNextStep.value) {
    current.completed = true
    
    // Unlock next step
    const nextStep = workflowSteps.value.find(s => s.id === current.id + 1)
    if (nextStep) {
      nextStep.unlocked = true
      currentStep.value = nextStep.id
    }
  }
}

const resetWorkflow = () => {
  workflowSteps.value.forEach((step, index) => {
    step.completed = false
    step.unlocked = index === 0
  })
  currentStep.value = 1
  selectedTemplate.value = null
}
</script>
