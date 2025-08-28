<template>
  <div class="min-h-screen bg-forest-900">
    <!-- Header -->
    <AppHeader />

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <!-- Page Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <h1 class="text-3xl font-bold text-white">AI Research Assistant</h1>
            <span class="text-orange-400">•</span>
            <p class="text-gray-400">Let AI do the research for you</p>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="showProTips = true"
              class="flex items-center space-x-2 rounded-lg bg-forest-700 px-4 py-2 text-white transition-colors hover:bg-forest-600"
            >
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
              </svg>
              <span>Pro Tips</span>
            </button>
            <button
              @click="showTemplates = true"
              class="flex items-center space-x-2 rounded-lg bg-forest-700 px-4 py-2 text-white transition-colors hover:bg-forest-600"
            >
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z"/>
              </svg>
              <span>Templates</span>
            </button>
            <button
              @click="showSavedProjects = true"
              class="flex items-center space-x-2 rounded-lg bg-forest-700 px-4 py-2 text-white transition-colors hover:bg-forest-600"
            >
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"/>
              </svg>
              <span>Saved Projects</span>
            </button>
            <button
              @click="saveCurrentProject"
              class="flex items-center space-x-2 rounded-lg bg-orange-500 px-4 py-2 text-white transition-colors hover:bg-orange-600"
            >
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M7.707 10.293a1 1 0 10-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 11.586V6h5a2 2 0 012 2v7a2 2 0 01-2 2H4a2 2 0 01-2-2V8a2 2 0 012-2h5v5.586l-1.293-1.293zM9 4a1 1 0 012 0v2H9V4z"/>
              </svg>
              <span>Save Project</span>
            </button>
          </div>
        </div>
      </div>

      <!-- AI Research Center -->
      <AIResearchCenter />
    </main>

    <!-- Modals -->
    <ProTipsModal 
      :show="showProTips" 
      @close="showProTips = false"
      @startTour="startInteractiveTour"
    />

    <TemplatesModal 
      :show="showTemplates" 
      @close="showTemplates = false"
      @useTemplate="applyTemplate"
    />

    <!-- Saved Projects Modal -->
    <div v-if="showSavedProjects" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-forest-900 rounded-lg shadow-xl w-full max-w-4xl max-h-[80vh] overflow-hidden border border-forest-700">
        <div class="bg-gradient-to-r from-forest-700 to-forest-800 text-white p-6 flex items-center justify-between">
          <h2 class="text-2xl font-bold">Saved Research Projects</h2>
          <button @click="showSavedProjects = false" class="text-white/80 hover:text-white transition-colors">
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="p-6">
          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="project in savedProjects" :key="project.id" class="bg-forest-800 border border-forest-600 rounded-lg p-4 hover:border-forest-500 transition-colors cursor-pointer">
              <h3 class="text-white font-semibold mb-2">{{ project.name }}</h3>
              <p class="text-gray-400 text-sm mb-3">{{ project.description }}</p>
              <div class="flex justify-between items-center">
                <span class="text-xs text-gray-500">{{ formatDate(project.createdAt) }}</span>
                <button @click="loadProject(project)" class="text-orange-400 hover:text-orange-300 text-sm">
                  Load Project
                </button>
              </div>
            </div>
          </div>
          <div v-if="savedProjects.length === 0" class="text-center py-12">
            <svg class="h-16 w-16 mx-auto mb-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"/>
            </svg>
            <h3 class="text-xl font-semibold text-white mb-2">No Saved Projects</h3>
            <p class="text-gray-400">Start researching and save your projects to see them here</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AIResearchCenter from '../../components/research/AIResearchCenter.vue'
import ProTipsModal from '../../components/research/ProTipsModal.vue'
import TemplatesModal from '../../components/research/TemplatesModal.vue'

// Page state
const showProTips = ref(false)
const showTemplates = ref(false)
const showSavedProjects = ref(false)

// Mock saved projects
const savedProjects = ref([
  {
    id: 1,
    name: 'Competitor Analysis - Productivity Niche',
    description: 'Deep dive into top 5 productivity YouTubers',
    createdAt: new Date('2024-01-15'),
    template: 'Competitor Analysis'
  },
  {
    id: 2,
    name: 'Viral Video Research - Morning Routines',
    description: 'Analysis of viral morning routine content',
    createdAt: new Date('2024-01-10'),
    template: 'Viral Video Analysis'
  }
])

// Methods
const startInteractiveTour = () => {
  alert('Interactive tour coming soon! The AI Research Assistant will guide you through the process.')
}

const applyTemplate = (template) => {
  // Template application will be handled by the AIResearchCenter component
  console.log('Applying template:', template)
}

const saveCurrentProject = () => {
  const projectName = prompt('Enter a name for this research project:')
  if (projectName) {
    const newProject = {
      id: Date.now(),
      name: projectName,
      description: 'AI-powered research project',
      createdAt: new Date(),
      template: 'Custom'
    }
    savedProjects.value.unshift(newProject)
    alert(`Project "${projectName}" saved successfully!`)
  }
}

const loadProject = (project) => {
  alert(`Loading project: ${project.name}`)
  showSavedProjects.value = false
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

// SEO
useHead({
  title: 'AI Research Assistant - MYTA',
  meta: [
    { name: 'description', content: 'AI-powered YouTube research assistant that does the heavy lifting for you' }
  ]
})
</script>

<style scoped>
/* Additional styles if needed */
</style>
