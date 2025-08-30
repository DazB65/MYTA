<template>
  <div class="min-h-screen bg-forest-950">
    <!-- Professional Research Platform Header -->
    <div class="bg-gradient-to-r from-forest-900 via-forest-800 to-forest-900 border-b border-forest-700 shadow-xl">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center space-x-6">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                <svg class="h-5 w-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div>
                <h1 class="text-xl font-bold text-white">Research Analytics</h1>
                <p class="text-xs text-gray-400">Professional Market Intelligence</p>
              </div>
            </div>

            <!-- Research Module Tabs -->
            <nav class="flex space-x-1">
              <button
                v-for="module in researchModules"
                :key="module.id"
                @click="activeModule = module.id"
                :class="[
                  'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                  activeModule === module.id
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'text-gray-300 hover:text-white hover:bg-forest-700'
                ]"
              >
                {{ module.name }}
              </button>
            </nav>
          </div>

          <div class="flex items-center space-x-3">
            <button class="flex items-center space-x-2 bg-forest-700 hover:bg-forest-600 text-gray-300 px-3 py-2 rounded-lg text-sm transition-colors">
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
              <span>Export</span>
            </button>
            <button class="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg text-sm transition-colors">
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
              </svg>
              <span>New Analysis</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Research Analytics Dashboard -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">

      <!-- Competitor Analysis Module -->
      <div v-if="activeModule === 'competitors'" class="space-y-6">

        <!-- Search and Filters -->
        <div class="bg-forest-900 rounded-xl border border-forest-700 p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-bold text-white">Competitor Analysis</h2>
            <div class="flex items-center space-x-3">
              <select class="bg-forest-800 border border-forest-600 text-white rounded-lg px-3 py-2 text-sm">
                <option>All Categories</option>
                <option>Gaming</option>
                <option>Tech</option>
                <option>Fitness</option>
                <option>Education</option>
              </select>
              <select class="bg-forest-800 border border-forest-600 text-white rounded-lg px-3 py-2 text-sm">
                <option>Last 30 days</option>
                <option>Last 90 days</option>
                <option>Last 6 months</option>
                <option>Last year</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search channels, keywords, or topics..."
                class="w-full bg-forest-800 border border-forest-600 text-white rounded-lg px-4 py-3 pl-10 focus:border-blue-500 focus:outline-none"
              />
              <svg class="absolute left-3 top-3.5 h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
              </svg>
            </div>

            <div class="flex space-x-2">
              <input
                type="number"
                placeholder="Min subscribers"
                class="flex-1 bg-forest-800 border border-forest-600 text-white rounded-lg px-3 py-3 text-sm focus:border-blue-500 focus:outline-none"
              />
              <input
                type="number"
                placeholder="Max subscribers"
                class="flex-1 bg-forest-800 border border-forest-600 text-white rounded-lg px-3 py-3 text-sm focus:border-blue-500 focus:outline-none"
              />
            </div>

            <button
              @click="runAnalysis"
              class="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-6 py-3 font-medium transition-colors"
            >
              Analyze Competitors
            </button>
          </div>
        </div>

        <!-- Analytics Overview Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-forest-900 rounded-xl border border-forest-700 p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-gray-400 text-sm">Total Channels</span>
              <svg class="h-4 w-4 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 6a3 3 0 11-6 0 3 3 0 616 0zM17 6a3 3 0 11-6 0 3 3 0 616 0z"/>
              </svg>
            </div>
            <div class="text-2xl font-bold text-white mb-1">{{ competitorData.totalChannels }}</div>
            <div class="text-xs text-green-400">+12% vs last month</div>
          </div>

          <div class="bg-forest-900 rounded-xl border border-forest-700 p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-gray-400 text-sm">Avg Subscribers</span>
              <svg class="h-4 w-4 text-purple-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/>
              </svg>
            </div>
            <div class="text-2xl font-bold text-white mb-1">{{ competitorData.avgSubscribers }}</div>
            <div class="text-xs text-blue-400">Market median</div>
          </div>

          <div class="bg-forest-900 rounded-xl border border-forest-700 p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-gray-400 text-sm">Avg Views</span>
              <svg class="h-4 w-4 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
                <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/>
              </svg>
            </div>
            <div class="text-2xl font-bold text-white mb-1">{{ competitorData.avgViews }}</div>
            <div class="text-xs text-green-400">+8% growth</div>
          </div>

          <div class="bg-forest-900 rounded-xl border border-forest-700 p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-gray-400 text-sm">Upload Frequency</span>
              <svg class="h-4 w-4 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/>
              </svg>
            </div>
            <div class="text-2xl font-bold text-white mb-1">{{ competitorData.avgFrequency }}</div>
            <div class="text-xs text-gray-400">per week</div>
          </div>
        </div>
        <!-- Competitor Data Table -->
        <div class="bg-forest-900 rounded-xl border border-forest-700 overflow-hidden">
          <div class="px-6 py-4 border-b border-forest-700">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-bold text-white">Competitor Rankings</h3>
              <div class="flex items-center space-x-2">
                <button class="text-gray-400 hover:text-white text-sm">
                  <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/>
                  </svg>
                </button>
                <span class="text-gray-400 text-sm">Export CSV</span>
              </div>
            </div>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-forest-800">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Rank</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Channel</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Subscribers</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Avg Views</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Engagement</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Upload Freq</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Growth</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-forest-700">
                <tr v-for="(competitor, index) in competitorData.competitors" :key="competitor.id" class="hover:bg-forest-800/50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <span class="text-sm font-medium text-white">#{{ index + 1 }}</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-sm mr-3">
                        {{ competitor.name.charAt(0) }}
                      </div>
                      <div>
                        <div class="text-sm font-medium text-white">{{ competitor.name }}</div>
                        <div class="text-sm text-gray-400">{{ competitor.category }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-white">{{ competitor.subscribers }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-white">{{ competitor.avgViews }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="text-sm text-white">{{ competitor.engagement }}%</div>
                      <div class="ml-2 w-16 bg-forest-700 rounded-full h-2">
                        <div class="bg-green-500 h-2 rounded-full" :style="{ width: `${competitor.engagement * 10}%` }"></div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-white">{{ competitor.uploadFreq }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div :class="competitor.growth > 0 ? 'text-green-400' : 'text-red-400'" class="text-sm font-medium">
                      {{ competitor.growth > 0 ? '+' : '' }}{{ competitor.growth }}%
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button class="text-blue-400 hover:text-blue-300 mr-3">View</button>
                    <button class="text-gray-400 hover:text-gray-300">Compare</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Market Trends Module -->
      <div v-if="activeModule === 'trends'" class="space-y-6">
        <div class="bg-forest-900 rounded-xl border border-forest-700 p-6">
          <h2 class="text-xl font-bold text-white mb-4">Market Trends Analysis</h2>

          <!-- Trend Charts Placeholder -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-forest-800 rounded-lg p-4 h-64 flex items-center justify-center">
              <div class="text-center">
                <svg class="h-12 w-12 text-gray-400 mx-auto mb-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clip-rule="evenodd"/>
                </svg>
                <p class="text-gray-400">Growth Trends Chart</p>
                <p class="text-xs text-gray-500">Interactive chart coming soon</p>
              </div>
            </div>

            <div class="bg-forest-800 rounded-lg p-4 h-64 flex items-center justify-center">
              <div class="text-center">
                <svg class="h-12 w-12 text-gray-400 mx-auto mb-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"/>
                  <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"/>
                </svg>
                <p class="text-gray-400">Market Share Analysis</p>
                <p class="text-xs text-gray-500">Pie chart visualization</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Keyword Research Module -->
      <div v-if="activeModule === 'keywords'" class="space-y-6">
        <div class="bg-forest-900 rounded-xl border border-forest-700 p-6">
          <h2 class="text-xl font-bold text-white mb-4">Keyword Research</h2>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <input
              type="text"
              placeholder="Enter seed keyword..."
              class="bg-forest-800 border border-forest-600 text-white rounded-lg px-4 py-3 focus:border-blue-500 focus:outline-none"
            />
            <select class="bg-forest-800 border border-forest-600 text-white rounded-lg px-3 py-3">
              <option>All Languages</option>
              <option>English</option>
              <option>Spanish</option>
              <option>French</option>
            </select>
            <button class="bg-purple-600 hover:bg-purple-700 text-white rounded-lg px-6 py-3 font-medium transition-colors">
              Research Keywords
            </button>
          </div>

          <!-- Keyword Results Table -->
          <div class="bg-forest-800 rounded-lg overflow-hidden">
            <table class="w-full">
              <thead class="bg-forest-700">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">Keyword</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">Search Volume</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">Competition</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">Trend</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-forest-600">
                <tr v-for="keyword in keywordData" :key="keyword.id">
                  <td class="px-4 py-3 text-sm text-white">{{ keyword.term }}</td>
                  <td class="px-4 py-3 text-sm text-white">{{ keyword.volume }}</td>
                  <td class="px-4 py-3 text-sm">
                    <span :class="keyword.competition === 'Low' ? 'text-green-400' : keyword.competition === 'Medium' ? 'text-yellow-400' : 'text-red-400'">
                      {{ keyword.competition }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-sm text-green-400">{{ keyword.trend }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Research platform state
const activeModule = ref('competitors')
const searchQuery = ref('')

// Research modules configuration
const researchModules = ref([
  { id: 'competitors', name: 'Competitors' },
  { id: 'trends', name: 'Market Trends' },
  { id: 'keywords', name: 'Keywords' },
  { id: 'content', name: 'Content Analysis' }
])

// Competitor analysis data
const competitorData = ref({
  totalChannels: 247,
  avgSubscribers: '1.2M',
  avgViews: '450K',
  avgFrequency: '3.2',
  competitors: [
    {
      id: 1,
      name: 'TechReview Pro',
      category: 'Technology',
      subscribers: '2.1M',
      avgViews: '850K',
      engagement: 4.8,
      uploadFreq: '2x/week',
      growth: 12.5
    },
    {
      id: 2,
      name: 'Digital Trends',
      category: 'Technology',
      subscribers: '1.8M',
      avgViews: '620K',
      engagement: 3.9,
      uploadFreq: '4x/week',
      growth: 8.2
    },
    {
      id: 3,
      name: 'Future Tech',
      category: 'Technology',
      subscribers: '950K',
      avgViews: '380K',
      engagement: 5.2,
      uploadFreq: '1x/week',
      growth: -2.1
    },
    {
      id: 4,
      name: 'Innovation Hub',
      category: 'Technology',
      subscribers: '1.5M',
      avgViews: '720K',
      engagement: 4.1,
      uploadFreq: '3x/week',
      growth: 15.8
    },
    {
      id: 5,
      name: 'Tech Insider',
      category: 'Technology',
      subscribers: '3.2M',
      avgViews: '1.2M',
      engagement: 3.7,
      uploadFreq: '5x/week',
      growth: 6.9
    }
  ]
})

// Keyword research data
const keywordData = ref([
  { id: 1, term: 'tech review 2024', volume: '45K', competition: 'Medium', trend: '+12%' },
  { id: 2, term: 'best smartphones', volume: '89K', competition: 'High', trend: '+8%' },
  { id: 3, term: 'AI technology', volume: '156K', competition: 'High', trend: '+34%' },
  { id: 4, term: 'gadget unboxing', volume: '23K', competition: 'Low', trend: '+5%' },
  { id: 5, term: 'tech news today', volume: '67K', competition: 'Medium', trend: '+15%' }
])

// Methods
const runAnalysis = () => {
  console.log('Running competitor analysis...')
  // In a real app, this would trigger API calls
}
</script>
