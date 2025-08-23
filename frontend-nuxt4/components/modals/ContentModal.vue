<template>
  <div class="fixed inset-0 z-50">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black bg-opacity-50" @click="$emit('close')" />

    <!-- Centered Modal -->
    <div class="fixed top-48 left-4 right-4 bottom-4 bg-forest-800 rounded-xl shadow-xl overflow-hidden flex flex-col transform transition-transform duration-300 ease-out">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-forest-700 flex-shrink-0">
        <div class="flex items-center space-x-4">
          <h3 class="text-xl font-semibold text-white">
            {{ content ? 'Edit Content' : 'Create New Content' }}
          </h3>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-white transition-colors"
        >
          <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <!-- Main Content Area -->
      <div class="flex-1 flex overflow-hidden">
        <!-- Left Column: Content Form -->
        <div class="flex-1 overflow-y-auto">
          <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
            <!-- Title -->
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                Title *
              </label>
              <input
                v-model="form.title"
                type="text"
                class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="Enter content title"
                required
              />
            </div>

            <!-- Description -->
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                Description
              </label>
              <textarea
                v-model="form.description"
                rows="3"
                class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none"
                placeholder="Enter content description"
              />
            </div>

            <!-- Pillar Selection -->
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Content Pillar *</label>
              <select
                v-model="form.pillarId"
                required
                class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              >
                <option value="">Select a pillar...</option>
                <option v-for="pillar in availablePillars" :key="pillar.id" :value="pillar.id">
                  {{ pillar.icon }} {{ pillar.name }}
                </option>
              </select>
            </div>

            <!-- Priority -->
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Priority</label>
              <select
                v-model="form.priority"
                class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>

            <!-- Status -->
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Status</label>
              <select
                v-model="form.status"
                class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              >
                <option value="ideas">Ideas</option>
                <option value="planning">Planning</option>
                <option value="in-progress">In Progress</option>
                <option value="published">Published</option>
              </select>
            </div>

            <!-- Stage Workflow -->
            <div class="space-y-4">
              <h4 class="text-sm font-medium text-gray-300 uppercase tracking-wide">Content Workflow</h4>

              <!-- First Row: Ideas and Planning -->
              <div class="grid grid-cols-2 gap-4">
                <!-- Ideas Stage -->
                <div class="flex items-center space-x-3 p-3 bg-forest-700/30 rounded-lg">
                  <input
                    v-model="form.stageCompletions.ideas"
                    type="checkbox"
                    class="h-4 w-4 text-orange-500 bg-forest-700 border-forest-600 rounded focus:ring-orange-500"
                  />
                  <div class="flex-1">
                    <label class="text-sm font-medium text-white">Ideas</label>
                    <input
                      v-model="form.stageDueDates.ideas"
                      type="date"
                      class="mt-1 block w-full px-2 py-1 bg-forest-700 border border-forest-600 rounded text-white text-xs focus:outline-none focus:ring-1 focus:ring-orange-500"
                    />
                  </div>
                </div>

                <!-- Planning Stage -->
                <div class="flex items-center space-x-3 p-3 bg-forest-700/30 rounded-lg">
                  <input
                    v-model="form.stageCompletions.planning"
                    type="checkbox"
                    class="h-4 w-4 text-orange-500 bg-forest-700 border-forest-600 rounded focus:ring-orange-500"
                  />
                  <div class="flex-1">
                    <label class="text-sm font-medium text-white">Planning</label>
                    <input
                      v-model="form.stageDueDates.planning"
                      type="date"
                      class="mt-1 block w-full px-2 py-1 bg-forest-700 border border-forest-600 rounded text-white text-xs focus:outline-none focus:ring-1 focus:ring-orange-500"
                    />
                  </div>
                </div>
              </div>

              <!-- Second Row: In Progress and Published -->
              <div class="grid grid-cols-2 gap-4">
                <!-- In Progress Stage -->
                <div class="flex items-center space-x-3 p-3 bg-forest-700/30 rounded-lg">
                  <input
                    v-model="form.stageCompletions['in-progress']"
                    type="checkbox"
                    class="h-4 w-4 text-orange-500 bg-forest-700 border-forest-600 rounded focus:ring-orange-500"
                  />
                  <div class="flex-1">
                    <label class="text-sm font-medium text-white">In Progress</label>
                    <input
                      v-model="form.stageDueDates['in-progress']"
                      type="date"
                      class="mt-1 block w-full px-2 py-1 bg-forest-700 border border-forest-600 rounded text-white text-xs focus:outline-none focus:ring-1 focus:ring-orange-500"
                    />
                  </div>
                </div>

                <!-- Published Stage -->
                <div class="flex items-center space-x-3 p-3 bg-forest-700/30 rounded-lg">
                  <input
                    v-model="form.stageCompletions.published"
                    type="checkbox"
                    class="h-4 w-4 text-orange-500 bg-forest-700 border-forest-600 rounded focus:ring-orange-500"
                  />
                  <div class="flex-1">
                    <label class="text-sm font-medium text-white">Published</label>
                    <input
                      v-model="form.stageDueDates.published"
                      type="date"
                      class="mt-1 block w-full px-2 py-1 bg-forest-700 border border-forest-600 rounded text-white text-xs focus:outline-none focus:ring-1 focus:ring-orange-500"
                    />
                  </div>
                </div>
              </div>
            </div>



            <!-- Form Actions -->
            <div class="flex items-center justify-end space-x-3 pt-6 border-t border-forest-700">
              <button
                type="button"
                @click="$emit('close')"
                class="px-6 py-3 text-gray-400 hover:text-white transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-6 py-3 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors font-medium"
              >
                {{ content ? 'Update Content' : 'Create Content' }}
              </button>
            </div>
          </form>
        </div>

        <!-- Right Column: AI Assistant -->
        <div class="w-96 border-l border-forest-700 bg-forest-900/50 overflow-y-auto">
          <div class="p-6 space-y-6">
            <!-- Agent Header -->
            <div class="flex items-center space-x-3 pb-4 border-b border-forest-700">
              <div class="flex h-12 w-12 items-center justify-center rounded-lg overflow-hidden" :style="{ backgroundColor: selectedAgent.color + '20' }">
                <img
                  :src="selectedAgent.image"
                  :alt="selectedAgent.name"
                  class="h-full w-full object-cover rounded-lg"
                />
              </div>
              <div>
                <h4 class="text-lg font-semibold text-white">{{ agentName || selectedAgent.name }}</h4>
                <p class="text-sm text-gray-400">{{ selectedAgent.description }}</p>
              </div>
            </div>

            <!-- Content Generation Tools -->
            <div class="space-y-4">
              <h5 class="text-sm font-medium text-gray-300 uppercase tracking-wide">Content Generation</h5>

              <div class="space-y-3">
                <button
                  @click="generateTitle"
                  :disabled="isGenerating"
                  class="w-full flex items-center justify-between p-3 bg-forest-700 hover:bg-forest-600 rounded-lg transition-colors text-left disabled:opacity-50"
                >
                  <div class="flex items-center space-x-3">
                    <span class="text-lg">✨</span>
                    <div>
                      <div class="text-sm font-medium text-white">Generate Title</div>
                      <div class="text-xs text-gray-400">AI-powered title suggestions</div>
                    </div>
                  </div>
                  <span class="text-gray-400">→</span>
                </button>

                <button
                  @click="generateDescription"
                  :disabled="isGenerating"
                  class="w-full flex items-center justify-between p-3 bg-forest-700 hover:bg-forest-600 rounded-lg transition-colors text-left disabled:opacity-50"
                >
                  <div class="flex items-center space-x-3">
                    <span class="text-lg">📝</span>
                    <div>
                      <div class="text-sm font-medium text-white">Generate Description</div>
                      <div class="text-xs text-gray-400">Detailed content descriptions</div>
                    </div>
                  </div>
                  <span class="text-gray-400">→</span>
                </button>

                <button
                  @click="suggestTopics"
                  :disabled="isGenerating"
                  class="w-full flex items-center justify-between p-3 bg-forest-700 hover:bg-forest-600 rounded-lg transition-colors text-left disabled:opacity-50"
                >
                  <div class="flex items-center space-x-3">
                    <span class="text-lg">💡</span>
                    <div>
                      <div class="text-sm font-medium text-white">Suggest Topics</div>
                      <div class="text-xs text-gray-400">Related content ideas</div>
                    </div>
                  </div>
                  <span class="text-gray-400">→</span>
                </button>
              </div>
            </div>

            <!-- AI Suggestions -->
            <div class="space-y-4">
              <h5 class="text-sm font-medium text-gray-300 uppercase tracking-wide">Smart Suggestions</h5>

              <div class="space-y-3">
                <div
                  v-for="suggestion in aiSuggestions"
                  :key="suggestion.id"
                  class="p-3 bg-forest-700/50 rounded-lg border border-forest-600/30"
                >
                  <div class="flex items-start space-x-3">
                    <span class="text-lg">{{ suggestion.icon }}</span>
                    <div class="flex-1">
                      <div class="text-sm font-medium text-white mb-1">{{ suggestion.title }}</div>
                      <div class="text-xs text-gray-400">{{ suggestion.description }}</div>
                      <button
                        v-if="suggestion.action"
                        @click="applySuggestion(suggestion)"
                        class="mt-2 text-xs text-orange-400 hover:text-orange-300 transition-colors"
                      >
                        Apply suggestion →
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Content Templates -->
            <div class="space-y-4">
              <h5 class="text-sm font-medium text-gray-300 uppercase tracking-wide">Content Templates</h5>

              <div class="space-y-2">
                <button
                  v-for="template in contentTemplates"
                  :key="template.id"
                  @click="applyTemplate(template)"
                  class="w-full p-3 bg-forest-700/30 hover:bg-forest-700 rounded-lg transition-colors text-left border border-forest-600/20"
                >
                  <div class="flex items-center space-x-3">
                    <span class="text-lg">{{ template.icon }}</span>
                    <div>
                      <div class="text-sm font-medium text-white">{{ template.name }}</div>
                      <div class="text-xs text-gray-400">{{ template.description }}</div>
                    </div>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAgentSettings } from '../../composables/useAgentSettings.js'

const props = defineProps({
  content: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'save'])

// Agent settings
const { selectedAgent, agentName, allAgents } = useAgentSettings()

// Available pillars (mock data)
const availablePillars = ref([
  { id: 'marketing', name: 'Marketing', icon: '📈' },
  { id: 'technology', name: 'Technology', icon: '💻' },
  { id: 'lifestyle', name: 'Lifestyle', icon: '🌟' },
  { id: 'education', name: 'Education', icon: '📚' }
])

// Generation state
const isGenerating = ref(false)

// AI Suggestions based on selected agent and content context
const aiSuggestions = computed(() => {
  const agent = selectedAgent.value
  const pillar = availablePillars.value.find(p => p.id === form.value.pillarId)

  // Agent-specific suggestions
  const suggestions = []

  if (agent.name === 'Levi' || agentName.value === 'Levi' || agent.id === 2) {
    suggestions.push(
      {
        id: 'trending-topic',
        icon: '🔥',
        title: 'Trending Topic Detected',
        description: 'AI Gaming Tools is trending in your niche',
        action: 'apply-trending'
      },
      {
        id: 'optimal-timing',
        icon: '⏰',
        title: 'Optimal Publishing Time',
        description: 'Best time to publish: Tuesday 2-4 PM',
        action: 'set-timing'
      }
    )
  }

  if (pillar?.name === 'Marketing') {
    suggestions.push({
      id: 'marketing-hook',
      icon: '🎯',
      title: 'Marketing Hook Suggestion',
      description: 'Start with a problem your audience faces',
      action: 'apply-hook'
    })
  }

  if (form.value.status === 'ideas') {
    suggestions.push({
      id: 'research-tip',
      icon: '🔍',
      title: 'Research Tip',
      description: 'Check competitor content for gaps',
      action: null
    })
  }

  return suggestions
})

// Content Templates
const contentTemplates = ref([
  {
    id: 'how-to',
    name: 'How-To Guide',
    icon: '📚',
    description: 'Step-by-step tutorial format',
    template: {
      title: 'How to [Action] in [Timeframe]',
      description: 'A comprehensive guide that walks viewers through the process of [specific action], perfect for beginners and intermediate users.'
    }
  },
  {
    id: 'listicle',
    name: 'Top 10 List',
    icon: '📝',
    description: 'Numbered list format',
    template: {
      title: 'Top 10 [Items] for [Audience]',
      description: 'A curated list of the best [items] that [audience] needs to know about, with detailed explanations and examples.'
    }
  },
  {
    id: 'case-study',
    name: 'Case Study',
    icon: '📊',
    description: 'Real-world example analysis',
    template: {
      title: 'How [Company/Person] Achieved [Result]',
      description: 'An in-depth analysis of a real success story, breaking down the strategies and tactics used to achieve remarkable results.'
    }
  },
  {
    id: 'comparison',
    name: 'Comparison',
    icon: '⚖️',
    description: 'Compare different options',
    template: {
      title: '[Option A] vs [Option B]: Which is Better?',
      description: 'A detailed comparison helping viewers choose between different options, with pros, cons, and recommendations.'
    }
  }
])

// Form state
const form = ref({
  title: '',
  description: '',
  status: 'ideas',
  priority: 'medium',
  pillarId: '',
  stageDueDates: {
    ideas: '',
    planning: '',
    'in-progress': '',
    published: ''
  },
  stageCompletions: {
    ideas: false,
    planning: false,
    'in-progress': false,
    published: false
  }
})

// AI Generation Functions
const generateTitle = async () => {
  if (isGenerating.value) return

  isGenerating.value = true
  try {
    // Simulate Agent generation (replace with actual Agent service call)
    await new Promise(resolve => setTimeout(resolve, 1500))

    const pillar = availablePillars.value.find(p => p.id === form.value.pillarId)
    const agent = selectedAgent.value

    let generatedTitle = ''

    if ((agent.name === 'Levi' || agentName.value === 'Levi' || agent.id === 2) && pillar?.name === 'Marketing') {
      generatedTitle = '5 Marketing Strategies That Actually Work in 2024'
    } else if (pillar?.name === 'Technology') {
      generatedTitle = 'The Ultimate Guide to Agent Tools for Content Creators'
    } else {
      generatedTitle = 'How to Create Engaging Content That Converts'
    }

    form.value.title = generatedTitle
  } catch (error) {
    console.error('Failed to generate title:', error)
  } finally {
    isGenerating.value = false
  }
}

const generateDescription = async () => {
  if (isGenerating.value) return

  isGenerating.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1500))

    const pillar = availablePillars.value.find(p => p.id === form.value.pillarId)
    const agent = selectedAgent.value

    let generatedDescription = ''

    if (agent.name === 'Levi') {
      generatedDescription = 'A comprehensive guide that breaks down proven strategies and actionable tactics. Perfect for creators looking to level up their content game with data-driven insights and creative approaches.'
    } else {
      generatedDescription = 'An in-depth analysis covering everything you need to know, with practical examples and step-by-step instructions to help you achieve your goals.'
    }

    form.value.description = generatedDescription
  } catch (error) {
    console.error('Failed to generate description:', error)
  } finally {
    isGenerating.value = false
  }
}

const suggestTopics = async () => {
  if (isGenerating.value) return

  isGenerating.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))

    // This would show a list of suggested topics in a future enhancement
    alert('Topic suggestions feature coming soon! This would show related content ideas based on your selected pillar and agent expertise.')
  } catch (error) {
    console.error('Failed to suggest topics:', error)
  } finally {
    isGenerating.value = false
  }
}

const applySuggestion = (suggestion) => {
  switch (suggestion.action) {
    case 'apply-trending':
      form.value.title = 'AI Gaming Tools: The Complete 2024 Guide'
      break
    case 'set-timing':
      // This would set optimal publishing time in a future enhancement
      alert('Optimal timing applied! This would set the best publishing schedule.')
      break
    case 'apply-hook':
      if (!form.value.description.includes('Are you struggling with')) {
        form.value.description = 'Are you struggling with ' + form.value.description
      }
      break
  }
}

const applyTemplate = (template) => {
  form.value.title = template.template.title
  form.value.description = template.template.description
}

const handleSubmit = () => {
  if (!form.value.title.trim()) {
    alert('Please enter a title')
    return
  }

  if (!form.value.pillarId) {
    alert('Please select a pillar')
    return
  }

  const selectedPillar = availablePillars.value.find(p => p.id === form.value.pillarId)

  const contentData = {
    id: props.content?.id || Date.now(),
    title: form.value.title.trim(),
    description: form.value.description.trim(),
    status: form.value.status,
    priority: form.value.priority,
    pillar: selectedPillar,
    stageDueDates: form.value.stageDueDates,
    stageCompletions: form.value.stageCompletions,
    createdAt: props.content?.createdAt || new Date().toISOString(),
    dueDate: form.value.stageDueDates.published || new Date().toISOString()
  }

  emit('save', contentData)
}
</script>
