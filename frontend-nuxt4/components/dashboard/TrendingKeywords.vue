<template>
  <div class="trending-keywords-widget bg-forest-700/50 rounded-xl p-6 border border-forest-600/20">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-3">
        <div class="p-2 bg-red-500/20 rounded-lg">
          <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-white">Trending Keywords</h3>
          <p class="text-sm text-gray-300">Hot topics in your niche</p>
        </div>
      </div>
      <button
        @click="refreshKeywords"
        :disabled="isLoading"
        class="p-2 text-gray-400 hover:text-gray-200 transition-colors"
      >
        <svg class="w-5 h-5" :class="{ 'animate-spin': isLoading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>
      </button>
    </div>

    <!-- Keywords List -->
    <div class="space-y-4">
      <div
        v-for="(keyword, index) in trendingKeywords"
        :key="index"
        class="bg-forest-600/50 rounded-lg hover:bg-forest-600 transition-colors group"
      >
        <!-- Keyword Header -->
        <div
          class="flex items-center justify-between p-3 cursor-pointer"
          @click="toggleKeywordExpansion(index)"
        >
          <div class="flex items-center space-x-3">
            <div class="flex items-center justify-center w-6 h-6 bg-red-500 text-white text-xs font-bold rounded">
              {{ index + 1 }}
            </div>
            <div>
              <div class="font-medium text-white">{{ keyword.term }}</div>
              <div class="text-sm text-gray-300">{{ keyword.searchVolume }} searches • {{ keyword.contentIdeas?.length || 0 }} ideas</div>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <div class="flex items-center space-x-1">
              <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span class="text-sm font-medium text-green-400">+{{ keyword.growth }}%</span>
            </div>
            <svg
              class="w-4 h-4 text-gray-400 group-hover:text-gray-200 transition-all duration-200"
              :class="{ 'rotate-90': expandedKeywords.includes(index) }"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </div>
        </div>

        <!-- Expanded Content Ideas -->
        <div
          v-if="expandedKeywords.includes(index) && keyword.contentIdeas"
          class="px-3 pb-3 space-y-4"
        >
          <!-- Strategic Overview -->
          <div class="bg-forest-700/30 rounded-lg p-3 border border-forest-600/20">
            <div class="text-xs font-medium text-blue-300 mb-2">🎯 Strategic Insights</div>
            <div class="grid grid-cols-2 gap-2 text-xs">
              <div><span class="text-gray-400">Competition:</span> <span class="text-white">{{ keyword.competitionLevel }}</span></div>
              <div><span class="text-gray-400">Best Time:</span> <span class="text-white">{{ keyword.bestUploadTime }}</span></div>
              <div><span class="text-gray-400">Expected Views:</span> <span class="text-white">{{ keyword.expectedViews }}</span></div>
              <div><span class="text-gray-400">Audience:</span> <span class="text-white">{{ keyword.strategicInsights?.audienceIntent?.slice(0, 30) }}...</span></div>
            </div>
          </div>

          <!-- Content Ideas -->
          <div class="space-y-3">
            <div class="text-xs font-medium text-green-300">💡 AI-Generated Content Ideas</div>
            <div
              v-for="(idea, ideaIndex) in keyword.contentIdeas"
              :key="ideaIndex"
              @click="useContentIdea(keyword, idea)"
              class="bg-forest-700/50 rounded-lg p-3 hover:bg-forest-700 cursor-pointer transition-colors group border border-forest-600/20"
            >
              <div class="font-medium text-white text-sm mb-2 group-hover:text-blue-200">
                {{ typeof idea === 'string' ? idea : idea.title }}
              </div>

              <div v-if="typeof idea === 'object'" class="space-y-2">
                <div class="text-xs text-gray-300">{{ idea.reasoning }}</div>

                <div class="flex items-center space-x-4 text-xs">
                  <span class="text-green-400">📈 {{ idea.estimatedPerformance }}</span>
                </div>

                <div v-if="idea.hooks?.length" class="text-xs">
                  <span class="text-orange-300">🎣 Hook:</span>
                  <span class="text-gray-300 italic">"{{ idea.hooks[0] }}"</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Strategic Opportunities -->
          <div v-if="keyword.strategicInsights" class="bg-forest-700/30 rounded-lg p-3 border border-forest-600/20">
            <div class="text-xs font-medium text-purple-300 mb-2">🚀 Opportunities</div>
            <div class="space-y-1 text-xs text-gray-300">
              <div><span class="text-gray-400">Gap:</span> {{ keyword.strategicInsights.competitorGaps }}</div>
              <div><span class="text-gray-400">Monetization:</span> {{ keyword.strategicInsights.monetizationPotential }}</div>
              <div v-if="keyword.strategicInsights.contentSeries">
                <span class="text-gray-400">Series Potential:</span> {{ keyword.strategicInsights.contentSeries }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="mt-4 pt-4 border-t border-gray-600/30">
      <div class="flex space-x-2">
        <button
          @click="generateContentIdeas"
          class="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-sm font-medium"
        >
          Generate Ideas
        </button>
        <button
          @click="analyzeCompetitors"
          class="flex-1 px-4 py-2 bg-forest-600 text-gray-200 rounded-lg hover:bg-forest-500 transition-colors text-sm font-medium"
        >
          Analyze Competition
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

// Define emits for parent component communication
const emit = defineEmits(['keyword-selected', 'content-idea-selected', 'generate-ideas', 'analyze-competitors'])

const isLoading = ref(false)
const expandedKeywords = ref([])
const trendingKeywords = ref([
  {
    term: "AI YouTube automation",
    searchVolume: "45K",
    growth: 127,
    competitionLevel: "Medium",
    bestUploadTime: "2-4 PM PST",
    expectedViews: "15K-50K",
    contentIdeas: [
      {
        title: "How I Automated My Entire YouTube Channel with AI (Step-by-Step)",
        reasoning: "Personal case study format performs 3x better than generic tutorials. 'Step-by-Step' increases CTR by 23%.",
        hooks: ["What if I told you I haven't touched my YouTube channel in 30 days, but it's still growing?"],
        keyPoints: ["Show actual AI tools in action", "Include real results/screenshots", "Provide downloadable templates"],
        estimatedPerformance: "25K-40K views, 8.5% CTR"
      },
      {
        title: "5 AI Tools That Will Replace Manual YouTube Work in 2024",
        reasoning: "List format + year specificity drives urgency. Tool roundups have high shareability and bookmark rates.",
        hooks: ["These AI tools are putting YouTube editors out of business"],
        keyPoints: ["Demo each tool live", "Show before/after comparisons", "Include pricing breakdown"],
        estimatedPerformance: "20K-35K views, 7.2% CTR"
      },
      {
        title: "I Let AI Run My Channel for 30 Days - Here's What Happened",
        reasoning: "Experiment format creates curiosity gap. '30 days' timeframe feels achievable for viewers to replicate.",
        hooks: ["Day 1: AI wrote my script. Day 30: I couldn't believe the results."],
        keyPoints: ["Document the full journey", "Show real analytics", "Reveal unexpected challenges"],
        estimatedPerformance: "30K-55K views, 9.1% CTR"
      }
    ],
    strategicInsights: {
      audienceIntent: "Creators seeking efficiency and scale without losing quality",
      competitorGaps: "Most content is theoretical - practical implementation guides are underserved",
      trendingSubtopics: ["AI script writing", "Automated thumbnails", "Voice cloning ethics"],
      monetizationPotential: "High - tool affiliate opportunities, course upsells",
      contentSeries: "Could expand into 'AI Creator Toolkit' series with 8-12 episodes"
    }
  },
  {
    term: "YouTube Shorts strategy",
    searchVolume: "38K",
    growth: 89,
    competitionLevel: "High",
    bestUploadTime: "6-8 PM PST",
    expectedViews: "12K-30K",
    contentIdeas: [
      {
        title: "The YouTube Shorts Algorithm Changed - Here's How to Win Now",
        reasoning: "Algorithm update content creates urgency. 'How to Win' implies competitive advantage.",
        hooks: ["If your Shorts stopped getting views last month, this is why"],
        keyPoints: ["Explain recent algorithm changes", "Show new optimization tactics", "Include case studies"],
        estimatedPerformance: "18K-28K views, 6.8% CTR"
      },
      {
        title: "Why Your Shorts Aren't Getting Views (5 Common Mistakes)",
        reasoning: "Problem-solution format addresses pain points. Numbered mistakes create clear structure.",
        hooks: ["Mistake #3 killed my Shorts views for 2 weeks straight"],
        keyPoints: ["Analyze failed Shorts examples", "Show optimization fixes", "Provide checklist"],
        estimatedPerformance: "15K-25K views, 7.5% CTR"
      },
      {
        title: "I Tested 100 Shorts - This Strategy Got 10M+ Views",
        reasoning: "Large-scale test implies authority. Specific view count creates credibility.",
        hooks: ["After testing 100 different Shorts, only 1 strategy consistently worked"],
        keyPoints: ["Show testing methodology", "Reveal winning patterns", "Provide templates"],
        estimatedPerformance: "22K-35K views, 8.3% CTR"
      }
    ],
    strategicInsights: {
      audienceIntent: "Creators struggling with Shorts performance wanting proven strategies",
      competitorGaps: "Too much generic advice - need specific, tested tactics",
      trendingSubtopics: ["Shorts SEO", "Hook formulas", "Retention tactics"],
      monetizationPotential: "Medium - course sales, consulting services",
      contentSeries: "Shorts Mastery series - could include format-specific guides"
    }
  }
])

const refreshKeywords = async () => {
  isLoading.value = true
  try {
    // Simulate API call - replace with actual trending keywords API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // In real implementation, fetch from YouTube API or Google Trends
    console.log('🔥 Refreshing trending keywords...')
  } catch (error) {
    console.error('Error refreshing keywords:', error)
  } finally {
    isLoading.value = false
  }
}

const toggleKeywordExpansion = (index) => {
  if (expandedKeywords.value.includes(index)) {
    expandedKeywords.value = expandedKeywords.value.filter(i => i !== index)
  } else {
    expandedKeywords.value.push(index)
  }
}

const useKeyword = (keyword) => {
  // Emit event to parent component for content creation
  console.log('🔥 Using keyword:', keyword.term)
  emit('keyword-selected', keyword)
}

const useContentIdea = (keyword, idea) => {
  // Emit event with specific content idea
  console.log('🔥 Using content idea:', idea)
  emit('content-idea-selected', { keyword, idea })
}

const generateContentIdeas = () => {
  console.log('🔥 Generating content ideas from trending keywords...')
  emit('generate-ideas', trendingKeywords.value)
}

const analyzeCompetitors = () => {
  console.log('🔥 Analyzing competitors for trending keywords...')
  emit('analyze-competitors', trendingKeywords.value)
}

onMounted(() => {
  // Load initial trending keywords
  refreshKeywords()
})
</script>

<style scoped>
.trending-keywords-widget {
  min-height: 400px;
}
</style>
