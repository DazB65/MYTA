<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-slate-900 rounded-lg shadow-xl w-full max-w-5xl max-h-[90vh] overflow-hidden border-2 border-gray-600/70 shadow-lg">
      <!-- Modal Header -->
      <div class="bg-gradient-to-r from-gray-700 to-gray-800 text-white p-6 flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="h-10 w-10 rounded-lg bg-white/20 flex items-center justify-center">
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z"/>
            </svg>
          </div>
          <div>
            <h2 class="text-2xl font-bold">Research Templates</h2>
            <p class="text-gray-300">Pre-built research frameworks for different goals</p>
          </div>
        </div>
        <button @click="$emit('close')" class="text-white/80 hover:text-white transition-colors">
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Modal Content -->
      <div class="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
        <!-- Template Categories -->
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          
          <!-- Competitor Analysis Template -->
          <div class="bg-gray-800 border-2 border-gray-600/70 shadow-lg rounded-lg p-6 hover:border-gray-500 transition-colors">
            <div class="flex items-center mb-4">
              <div class="h-12 w-12 rounded-lg bg-red-500/20 flex items-center justify-center mr-4">
                <svg class="h-6 w-6 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">Competitor Analysis</h3>
                <p class="text-sm text-gray-400">Analyze top competitors in your niche</p>
              </div>
            </div>
            <div class="space-y-3 mb-4">
              <div class="text-sm text-gray-300">
                <p class="font-medium text-white mb-2">Research Steps:</p>
                <ul class="space-y-1">
                  <li>• Find top 5 competitors</li>
                  <li>• Analyze their best performing videos</li>
                  <li>• Document content patterns</li>
                  <li>• Identify content gaps</li>
                </ul>
              </div>
            </div>
            <button 
              @click="useTemplate('competitor-analysis')"
              class="w-full bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-lg transition-colors"
            >
              Use Template
            </button>
          </div>

          <!-- Trend Research Template -->
          <div class="bg-gray-800 border-2 border-gray-600/70 shadow-lg rounded-lg p-6 hover:border-gray-500 transition-colors">
            <div class="flex items-center mb-4">
              <div class="h-12 w-12 rounded-lg bg-blue-500/20 flex items-center justify-center mr-4">
                <svg class="h-6 w-6 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">Trend Research</h3>
                <p class="text-sm text-gray-400">Discover and analyze trending topics</p>
              </div>
            </div>
            <div class="space-y-3 mb-4">
              <div class="text-sm text-gray-300">
                <p class="font-medium text-white mb-2">Research Steps:</p>
                <ul class="space-y-1">
                  <li>• Identify trending topics</li>
                  <li>• Analyze trend performance</li>
                  <li>• Find related keywords</li>
                  <li>• Plan content calendar</li>
                </ul>
              </div>
            </div>
            <button 
              @click="useTemplate('trend-research')"
              class="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg transition-colors"
            >
              Use Template
            </button>
          </div>

          <!-- Content Pillar Research -->
          <div class="bg-forest-800 border border-forest-600 rounded-lg p-6 hover:border-forest-500 transition-colors">
            <div class="flex items-center mb-4">
              <div class="h-12 w-12 rounded-lg bg-green-500/20 flex items-center justify-center mr-4">
                <svg class="h-6 w-6 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">Content Pillar Research</h3>
                <p class="text-sm text-gray-400">Research for specific content pillars</p>
              </div>
            </div>
            <div class="space-y-3 mb-4">
              <div class="text-sm text-gray-300">
                <p class="font-medium text-white mb-2">Research Steps:</p>
                <ul class="space-y-1">
                  <li>• Define pillar focus</li>
                  <li>• Research successful videos</li>
                  <li>• Analyze audience engagement</li>
                  <li>• Create content strategy</li>
                </ul>
              </div>
            </div>
            <button 
              @click="useTemplate('content-pillar')"
              class="w-full bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-lg transition-colors"
            >
              Use Template
            </button>
          </div>

          <!-- Viral Video Analysis -->
          <div class="bg-forest-800 border border-forest-600 rounded-lg p-6 hover:border-forest-500 transition-colors">
            <div class="flex items-center mb-4">
              <div class="h-12 w-12 rounded-lg bg-purple-500/20 flex items-center justify-center mr-4">
                <svg class="h-6 w-6 text-purple-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">Viral Video Analysis</h3>
                <p class="text-sm text-gray-400">Reverse-engineer viral content</p>
              </div>
            </div>
            <div class="space-y-3 mb-4">
              <div class="text-sm text-gray-300">
                <p class="font-medium text-white mb-2">Research Steps:</p>
                <ul class="space-y-1">
                  <li>• Find viral videos (1M+ views)</li>
                  <li>• Analyze viral elements</li>
                  <li>• Study engagement patterns</li>
                  <li>• Extract replicable strategies</li>
                </ul>
              </div>
            </div>
            <button 
              @click="useTemplate('viral-analysis')"
              class="w-full bg-purple-500 hover:bg-purple-600 text-white py-2 px-4 rounded-lg transition-colors"
            >
              Use Template
            </button>
          </div>

          <!-- Niche Exploration -->
          <div class="bg-forest-800 border border-forest-600 rounded-lg p-6 hover:border-forest-500 transition-colors">
            <div class="flex items-center mb-4">
              <div class="h-12 w-12 rounded-lg bg-yellow-500/20 flex items-center justify-center mr-4">
                <svg class="h-6 w-6 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">Niche Exploration</h3>
                <p class="text-sm text-gray-400">Explore new content niches</p>
              </div>
            </div>
            <div class="space-y-3 mb-4">
              <div class="text-sm text-gray-300">
                <p class="font-medium text-white mb-2">Research Steps:</p>
                <ul class="space-y-1">
                  <li>• Identify potential niches</li>
                  <li>• Analyze niche competition</li>
                  <li>• Study audience demand</li>
                  <li>• Evaluate entry opportunities</li>
                </ul>
              </div>
            </div>
            <button 
              @click="useTemplate('niche-exploration')"
              class="w-full bg-yellow-500 hover:bg-yellow-600 text-white py-2 px-4 rounded-lg transition-colors"
            >
              Use Template
            </button>
          </div>

          <!-- SEO Optimization Research -->
          <div class="bg-forest-800 border border-forest-600 rounded-lg p-6 hover:border-forest-500 transition-colors">
            <div class="flex items-center mb-4">
              <div class="h-12 w-12 rounded-lg bg-indigo-500/20 flex items-center justify-center mr-4">
                <svg class="h-6 w-6 text-indigo-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">SEO Optimization</h3>
                <p class="text-sm text-gray-400">Research for better discoverability</p>
              </div>
            </div>
            <div class="space-y-3 mb-4">
              <div class="text-sm text-gray-300">
                <p class="font-medium text-white mb-2">Research Steps:</p>
                <ul class="space-y-1">
                  <li>• Research high-ranking videos</li>
                  <li>• Analyze titles and descriptions</li>
                  <li>• Study keyword strategies</li>
                  <li>• Optimize content approach</li>
                </ul>
              </div>
            </div>
            <button 
              @click="useTemplate('seo-optimization')"
              class="w-full bg-indigo-500 hover:bg-indigo-600 text-white py-2 px-4 rounded-lg transition-colors"
            >
              Use Template
            </button>
          </div>

        </div>

        <!-- Custom Template Section -->
        <div class="mt-8 pt-6 border-t border-forest-700">
          <h3 class="text-xl font-bold text-white mb-4">Create Custom Template</h3>
          <div class="bg-forest-800 border border-forest-600 rounded-lg p-6">
            <div class="grid md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Template Name</label>
                <input
                  v-model="customTemplate.name"
                  type="text"
                  placeholder="My Research Template"
                  class="w-full rounded-lg bg-forest-700 border border-forest-600 px-3 py-2 text-white placeholder-gray-400 focus:border-orange-500 focus:outline-none focus:ring-1 focus:ring-orange-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Research Goal</label>
                <input
                  v-model="customTemplate.goal"
                  type="text"
                  placeholder="What do you want to research?"
                  class="w-full rounded-lg bg-forest-700 border border-forest-600 px-3 py-2 text-white placeholder-gray-400 focus:border-orange-500 focus:outline-none focus:ring-1 focus:ring-orange-500"
                />
              </div>
            </div>
            <div class="mt-4">
              <label class="block text-sm font-medium text-gray-300 mb-2">Research Steps</label>
              <textarea
                v-model="customTemplate.steps"
                rows="4"
                placeholder="1. First step&#10;2. Second step&#10;3. Third step..."
                class="w-full rounded-lg bg-forest-700 border border-forest-600 px-3 py-2 text-white placeholder-gray-400 focus:border-orange-500 focus:outline-none focus:ring-1 focus:ring-orange-500"
              ></textarea>
            </div>
            <div class="mt-4 flex justify-end">
              <button
                @click="createCustomTemplate"
                :disabled="!customTemplate.name || !customTemplate.goal"
                class="bg-orange-500 hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-white py-2 px-6 rounded-lg transition-colors"
              >
                Create Template
              </button>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-between items-center pt-6 border-t border-forest-700 mt-6">
          <div class="text-sm text-gray-400">
            💡 Templates help you follow proven research methodologies
          </div>
          <button
            @click="$emit('close')"
            class="px-6 py-2 border border-forest-600 rounded-lg text-gray-300 hover:bg-forest-800 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Props {
  show: boolean
}

interface Emits {
  (e: 'close'): void
  (e: 'useTemplate', template: any): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const customTemplate = ref({
  name: '',
  goal: '',
  steps: ''
})

const templates = {
  'competitor-analysis': {
    name: 'Competitor Analysis',
    goal: 'Analyze top competitors in your niche',
    steps: [
      'Find top 5 competitors in your niche',
      'Analyze their 10 best performing videos',
      'Document common content patterns',
      'Identify content gaps and opportunities',
      'Create competitive strategy notes'
    ],
    initialVideos: [
      'Search for competitor channels',
      'Add their top videos to canvas',
      'Compare performance metrics'
    ]
  },
  'trend-research': {
    name: 'Trend Research',
    goal: 'Discover and analyze trending topics',
    steps: [
      'Research current trending topics',
      'Analyze trend performance metrics',
      'Find related keywords and topics',
      'Study audience engagement patterns',
      'Plan content calendar around trends'
    ],
    initialVideos: [
      'Use "Find Trending Content" feature',
      'Research trending topics from sidebar',
      'Add trending videos to canvas'
    ]
  },
  'content-pillar': {
    name: 'Content Pillar Research',
    goal: 'Research for specific content pillars',
    steps: [
      'Define your content pillar focus',
      'Research successful videos in this pillar',
      'Analyze audience engagement patterns',
      'Study content formats and styles',
      'Create pillar-specific strategy'
    ],
    initialVideos: [
      'Search for pillar-related content',
      'Add high-performing videos',
      'Analyze content patterns'
    ]
  },
  'viral-analysis': {
    name: 'Viral Video Analysis',
    goal: 'Reverse-engineer viral content',
    steps: [
      'Find viral videos (1M+ views) in your niche',
      'Analyze viral elements (hook, pacing, etc.)',
      'Study engagement patterns and comments',
      'Identify replicable strategies',
      'Document viral content formulas'
    ],
    initialVideos: [
      'Search for viral videos',
      'Focus on 1M+ view content',
      'Analyze viral elements'
    ]
  },
  'niche-exploration': {
    name: 'Niche Exploration',
    goal: 'Explore new content niches',
    steps: [
      'Identify potential new niches',
      'Analyze niche competition levels',
      'Study audience demand and engagement',
      'Evaluate entry opportunities',
      'Create niche expansion strategy'
    ],
    initialVideos: [
      'Research different niche content',
      'Compare competition levels',
      'Analyze audience engagement'
    ]
  },
  'seo-optimization': {
    name: 'SEO Optimization Research',
    goal: 'Research for better discoverability',
    steps: [
      'Research high-ranking videos for target keywords',
      'Analyze titles and descriptions',
      'Study keyword strategies and tags',
      'Research thumbnail optimization',
      'Create SEO-optimized content plan'
    ],
    initialVideos: [
      'Search for keyword-optimized videos',
      'Analyze top-ranking content',
      'Study SEO best practices'
    ]
  }
}

const useTemplate = (templateKey: string) => {
  const template = templates[templateKey]
  if (template) {
    emit('useTemplate', template)
    emit('close')
  }
}

const createCustomTemplate = () => {
  if (customTemplate.value.name && customTemplate.value.goal) {
    const template = {
      name: customTemplate.value.name,
      goal: customTemplate.value.goal,
      steps: customTemplate.value.steps.split('\n').filter(step => step.trim()),
      isCustom: true
    }
    
    emit('useTemplate', template)
    
    // Reset form
    customTemplate.value = { name: '', goal: '', steps: '' }
    
    emit('close')
  }
}
</script>
