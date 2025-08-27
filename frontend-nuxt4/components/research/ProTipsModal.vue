<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-forest-900 rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-hidden border border-forest-700">
      <!-- Modal Header -->
      <div class="bg-gradient-to-r from-orange-500 to-orange-600 text-white p-6 flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="h-10 w-10 rounded-lg bg-white/20 flex items-center justify-center">
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
            </svg>
          </div>
          <div>
            <h2 class="text-2xl font-bold">Research Workspace Pro Tips</h2>
            <p class="text-orange-100">Master your YouTube research workflow</p>
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
        <!-- Quick Start Guide -->
        <div class="mb-8">
          <h3 class="text-xl font-bold text-white mb-4 flex items-center">
            <span class="h-8 w-8 rounded-full bg-green-500 text-white flex items-center justify-center text-sm font-bold mr-3">1</span>
            Quick Start Guide
          </h3>
          <div class="grid md:grid-cols-2 gap-4">
            <div class="bg-forest-800 border border-forest-600 rounded-lg p-4">
              <h4 class="font-semibold text-green-400 mb-2">🎯 Start with Trending Topics</h4>
              <p class="text-gray-300 text-sm">Click "Research" on any trending topic to automatically find 2-3 related videos. This gives you instant market insights.</p>
            </div>
            <div class="bg-forest-800 border border-forest-600 rounded-lg p-4">
              <h4 class="font-semibold text-blue-400 mb-2">🔍 Analyze Specific Videos</h4>
              <p class="text-gray-300 text-sm">Paste YouTube URLs of successful videos in your niche to get AI-powered analysis and insights.</p>
            </div>
          </div>
        </div>

        <!-- Research Workflow -->
        <div class="mb-8">
          <h3 class="text-xl font-bold text-white mb-4 flex items-center">
            <span class="h-8 w-8 rounded-full bg-blue-500 text-white flex items-center justify-center text-sm font-bold mr-3">2</span>
            Optimal Research Workflow
          </h3>
          <div class="space-y-4">
            <div class="flex items-start space-x-4 p-4 bg-forest-800 border border-forest-600 rounded-lg">
              <div class="h-8 w-8 rounded-full bg-orange-500 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">A</div>
              <div>
                <h4 class="font-semibold text-white">Discover Trends</h4>
                <p class="text-gray-300 text-sm">Start with "Find Trending Content" or research specific trending topics to understand what's working now.</p>
              </div>
            </div>
            <div class="flex items-start space-x-4 p-4 bg-forest-800 border border-forest-600 rounded-lg">
              <div class="h-8 w-8 rounded-full bg-orange-500 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">B</div>
              <div>
                <h4 class="font-semibold text-white">Analyze & Compare</h4>
                <p class="text-gray-300 text-sm">Add your own video URLs to compare against trending content. Look for patterns in high-scoring videos.</p>
              </div>
            </div>
            <div class="flex items-start space-x-4 p-4 bg-forest-800 border border-forest-600 rounded-lg">
              <div class="h-8 w-8 rounded-full bg-orange-500 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">C</div>
              <div>
                <h4 class="font-semibold text-white">Document Insights</h4>
                <p class="text-gray-300 text-sm">Use the floating "+" button to add research notes. Document what you want to replicate or avoid.</p>
              </div>
            </div>
            <div class="flex items-start space-x-4 p-4 bg-forest-800 border border-forest-600 rounded-lg">
              <div class="h-8 w-8 rounded-full bg-orange-500 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">D</div>
              <div>
                <h4 class="font-semibold text-white">Organize & Export</h4>
                <p class="text-gray-300 text-sm">Drag items around the canvas to organize your research, then export to Content Studio for content creation.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Understanding AI Analysis -->
        <div class="mb-8">
          <h3 class="text-xl font-bold text-white mb-4 flex items-center">
            <span class="h-8 w-8 rounded-full bg-purple-500 text-white flex items-center justify-center text-sm font-bold mr-3">3</span>
            Understanding AI Analysis
          </h3>
          <div class="grid md:grid-cols-3 gap-4">
            <div class="bg-forest-800 border border-forest-600 rounded-lg p-4">
              <h4 class="font-semibold text-purple-400 mb-2">📊 Analysis Scores</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between text-gray-300"><span>80-100:</span><span class="text-green-400 font-medium">Excellent</span></div>
                <div class="flex justify-between text-gray-300"><span>60-79:</span><span class="text-yellow-400 font-medium">Good</span></div>
                <div class="flex justify-between text-gray-300"><span>40-59:</span><span class="text-orange-400 font-medium">Average</span></div>
                <div class="flex justify-between text-gray-300"><span>0-39:</span><span class="text-red-400 font-medium">Poor</span></div>
              </div>
            </div>
            <div class="bg-forest-800 border border-forest-600 rounded-lg p-4">
              <h4 class="font-semibold text-purple-400 mb-2">🔍 Key Insights</h4>
              <ul class="text-sm text-gray-300 space-y-1">
                <li>• Engagement patterns</li>
                <li>• Content structure</li>
                <li>• SEO optimization</li>
                <li>• Thumbnail effectiveness</li>
                <li>• Title psychology</li>
              </ul>
            </div>
            <div class="bg-forest-800 border border-forest-600 rounded-lg p-4">
              <h4 class="font-semibold text-purple-400 mb-2">🏷️ Content Tags</h4>
              <div class="flex flex-wrap gap-1">
                <span class="px-2 py-1 bg-purple-600 text-purple-200 text-xs rounded-full">educational</span>
                <span class="px-2 py-1 bg-purple-600 text-purple-200 text-xs rounded-full">trending</span>
                <span class="px-2 py-1 bg-purple-600 text-purple-200 text-xs rounded-full">viral</span>
                <span class="px-2 py-1 bg-purple-600 text-purple-200 text-xs rounded-full">engaging</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Pro Tips -->
        <div class="mb-8">
          <h3 class="text-xl font-bold text-white mb-4 flex items-center">
            <span class="h-8 w-8 rounded-full bg-yellow-500 text-white flex items-center justify-center text-sm font-bold mr-3">4</span>
            Pro Tips & Best Practices
          </h3>
          <div class="grid md:grid-cols-2 gap-6">
            <div>
              <h4 class="font-semibold text-white mb-3">🎯 Research Strategy</h4>
              <ul class="space-y-2 text-sm text-gray-300">
                <li class="flex items-start"><span class="text-green-400 mr-2">✓</span>Research 5-10 videos per content pillar</li>
                <li class="flex items-start"><span class="text-green-400 mr-2">✓</span>Focus on videos with 80+ analysis scores</li>
                <li class="flex items-start"><span class="text-green-400 mr-2">✓</span>Look for patterns across successful videos</li>
                <li class="flex items-start"><span class="text-green-400 mr-2">✓</span>Save different projects for different niches</li>
              </ul>
            </div>
            <div>
              <h4 class="font-semibold text-white mb-3">📝 Note-Taking Tips</h4>
              <ul class="space-y-2 text-sm text-gray-300">
                <li class="flex items-start"><span class="text-blue-400 mr-2">💡</span>Document specific hooks and openings</li>
                <li class="flex items-start"><span class="text-blue-400 mr-2">💡</span>Note thumbnail and title patterns</li>
                <li class="flex items-start"><span class="text-blue-400 mr-2">💡</span>Track content structure and pacing</li>
                <li class="flex items-start"><span class="text-blue-400 mr-2">💡</span>Identify content gaps and opportunities</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- AI Research Agents -->
        <div class="mb-6">
          <h3 class="text-xl font-bold text-white mb-4 flex items-center">
            <span class="h-8 w-8 rounded-full bg-indigo-500 text-white flex items-center justify-center text-sm font-bold mr-3">5</span>
            AI Research Agents
          </h3>
          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div class="bg-forest-800 border border-forest-600 rounded-lg p-3">
              <h4 class="font-semibold text-indigo-400 text-sm">🧠 Algorithm Whisperer</h4>
              <p class="text-gray-300 text-xs mt-1">YouTube algorithm optimization and ranking strategies</p>
            </div>
            <div class="bg-forest-800 border border-forest-600 rounded-lg p-3">
              <h4 class="font-semibold text-indigo-400 text-sm">🎨 Thumbnail Genius</h4>
              <p class="text-gray-300 text-xs mt-1">Visual design and click-through rate optimization</p>
            </div>
            <div class="bg-forest-800 border border-forest-600 rounded-lg p-3">
              <h4 class="font-semibold text-indigo-400 text-sm">📝 Title Master</h4>
              <p class="text-gray-300 text-xs mt-1">Title psychology and optimization techniques</p>
            </div>
            <div class="bg-forest-800 border border-forest-600 rounded-lg p-3">
              <h4 class="font-semibold text-indigo-400 text-sm">📈 Trend Scout</h4>
              <p class="text-gray-300 text-xs mt-1">Competitor analysis and trend identification</p>
            </div>
            <div class="bg-forest-800 border border-forest-600 rounded-lg p-3">
              <h4 class="font-semibold text-indigo-400 text-sm">🚀 Growth Strategist</h4>
              <p class="text-gray-300 text-xs mt-1">Channel growth and audience development</p>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-between items-center pt-6 border-t border-forest-700">
          <div class="text-sm text-gray-400">
            💡 Tip: Bookmark this page and return to these tips anytime!
          </div>
          <div class="flex space-x-3">
            <button
              @click="$emit('close')"
              class="px-4 py-2 border border-forest-600 rounded-lg text-gray-300 hover:bg-forest-800 transition-colors"
            >
              Close
            </button>
            <button
              @click="startTour"
              class="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
            >
              Start Interactive Tour
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  show: boolean
}

interface Emits {
  (e: 'close'): void
  (e: 'startTour'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const startTour = () => {
  emit('startTour')
  emit('close')
}
</script>

<style scoped>
/* Custom scrollbar for the modal content */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
