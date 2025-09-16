<template>
  <div class="fixed inset-0 z-[60]">
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
            <!-- Step 1: Pillar Selection -->
            <div class="bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-xl p-4">
              <label class="block text-sm font-medium text-gray-300 mb-3">
                <span class="inline-flex items-center">
                  <span class="bg-gradient-to-r from-blue-500 to-purple-500 text-white text-sm font-bold px-3 py-2 rounded-full mr-3 shadow-lg">1</span>
                  <span class="text-lg font-semibold text-blue-300">Content Pillar *</span>
                </span>
              </label>
              <select
                v-model="form.pillarId"
                required
                class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select a pillar...</option>
                <option v-for="pillar in availablePillars" :key="pillar.id" :value="pillar.id">
                  {{ pillar.icon }} {{ pillar.name }}
                </option>
              </select>
              <p class="text-sm text-blue-200 mt-2 font-medium">🎯 Choose your content pillar to guide the content strategy</p>
            </div>

            <!-- Step 2: Description -->
            <div class="bg-gradient-to-r from-green-500/10 to-blue-500/10 border border-green-500/20 rounded-xl p-4">
              <label class="block text-sm font-medium text-gray-300 mb-3">
                <span class="inline-flex items-center">
                  <span class="bg-gradient-to-r from-green-500 to-blue-500 text-white text-sm font-bold px-3 py-2 rounded-full mr-3 shadow-lg">2</span>
                  <span class="text-lg font-semibold text-green-300">Description</span>
                </span>
              </label>
              <textarea
                v-model="form.description"
                rows="3"
                class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent resize-none"
                placeholder="Enter content description"
              />
              <p class="text-sm text-green-200 mt-2 font-medium">📝 Provide context and details about your content</p>
            </div>

            <!-- Step 2.5: Pre-Production Analysis (Optional) -->
            <div v-if="form.description && form.pillarId" class="bg-gradient-to-r from-orange-500/10 to-purple-500/10 border border-orange-500/20 rounded-xl p-4">
              <div class="flex items-center justify-between mb-3">
                <span class="inline-flex items-center">
                  <span class="bg-gradient-to-r from-orange-500 to-purple-500 text-white text-sm font-bold px-3 py-2 rounded-full mr-3 shadow-lg">🤖</span>
                  <span class="text-lg font-semibold text-orange-300">AI Pre-Production Analysis</span>
                </span>
                <span class="text-xs text-orange-200 bg-orange-500/20 px-2 py-1 rounded-full">Optional</span>
              </div>

              <p class="text-sm text-orange-200 mb-4">Get coordinated insights from your AI team before creating your video. You can use, modify, or ignore any suggestions.</p>

              <button
                @click="runPreProductionAnalysis"
                :disabled="isAnalyzing"
                class="w-full bg-gradient-to-r from-orange-500 to-purple-500 hover:from-orange-600 hover:to-purple-600 disabled:from-gray-600 disabled:to-gray-700 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2"
              >
                <span v-if="isAnalyzing" class="animate-spin">⚙️</span>
                <span v-else>🚀</span>
                <span>{{ isAnalyzing ? 'Analyzing with AI Team...' : 'Analyze & Get AI Suggestions' }}</span>
              </button>
            </div>

            <!-- Pre-Production Analysis Results -->
            <div v-if="analysisResults" class="bg-gray-900/80 backdrop-blur-sm border-2 border-gray-600/70 rounded-xl p-4 space-y-4">
              <div class="flex items-center justify-between">
                <h4 class="text-lg font-semibold text-white flex items-center space-x-2">
                  <span>🎯</span>
                  <span>Pre-Production Analysis Results</span>
                </h4>
                <button @click="clearAnalysis" class="text-xs text-gray-400 hover:text-white">Clear</button>
              </div>

              <!-- Analysis Results Grid -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <!-- SEO Recommendations -->
                <div class="bg-orange-500/10 border border-orange-500/20 rounded-lg p-3">
                  <h5 class="text-orange-400 font-medium flex items-center space-x-2 mb-2">
                    <span>📈</span>
                    <span>SEO Optimization (Maya)</span>
                  </h5>
                  <p class="text-sm text-gray-300 mb-3">{{ analysisResults.seo?.recommendations || 'Analyzing SEO potential...' }}</p>
                  <div class="flex space-x-2">
                    <button @click="applySEOSuggestions" class="text-xs bg-orange-500/20 hover:bg-orange-500/30 text-orange-300 px-2 py-1 rounded">Apply Suggestions</button>
                    <button @click="viewSEODetails" class="text-xs bg-gray-600/20 hover:bg-gray-600/30 text-gray-300 px-2 py-1 rounded">View Details</button>
                  </div>
                </div>

                <!-- Competitive Insights -->
                <div class="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                  <h5 class="text-blue-400 font-medium flex items-center space-x-2 mb-2">
                    <span>🔍</span>
                    <span>Competitive Analysis (Zara)</span>
                  </h5>
                  <p class="text-sm text-gray-300 mb-3">{{ analysisResults.competitive?.insights || 'Analyzing competition...' }}</p>
                  <div class="flex space-x-2">
                    <button @click="applyCompetitiveInsights" class="text-xs bg-blue-500/20 hover:bg-blue-500/30 text-blue-300 px-2 py-1 rounded">Apply Insights</button>
                    <button @click="viewCompetitiveDetails" class="text-xs bg-gray-600/20 hover:bg-gray-600/30 text-gray-300 px-2 py-1 rounded">View Details</button>
                  </div>
                </div>

                <!-- Audience Insights -->
                <div class="bg-purple-500/10 border border-purple-500/20 rounded-lg p-3">
                  <h5 class="text-purple-400 font-medium flex items-center space-x-2 mb-2">
                    <span>👥</span>
                    <span>Audience Insights (Levi)</span>
                  </h5>
                  <p class="text-sm text-gray-300 mb-3">{{ analysisResults.audience?.recommendations || 'Analyzing audience potential...' }}</p>
                  <div class="flex space-x-2">
                    <button @click="applyAudienceInsights" class="text-xs bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 px-2 py-1 rounded">Apply Insights</button>
                    <button @click="viewAudienceDetails" class="text-xs bg-gray-600/20 hover:bg-gray-600/30 text-gray-300 px-2 py-1 rounded">View Details</button>
                  </div>
                </div>

                <!-- Monetization Strategy -->
                <div class="bg-green-500/10 border border-green-500/20 rounded-lg p-3">
                  <h5 class="text-green-400 font-medium flex items-center space-x-2 mb-2">
                    <span>💰</span>
                    <span>Monetization Strategy (Kai)</span>
                  </h5>
                  <p class="text-sm text-gray-300 mb-3">{{ analysisResults.monetization?.tips || 'Analyzing monetization potential...' }}</p>
                  <div class="flex space-x-2">
                    <button @click="applyMonetizationTips" class="text-xs bg-green-500/20 hover:bg-green-500/30 text-green-300 px-2 py-1 rounded">Apply Tips</button>
                    <button @click="viewMonetizationDetails" class="text-xs bg-gray-600/20 hover:bg-gray-600/30 text-gray-300 px-2 py-1 rounded">View Details</button>
                  </div>
                </div>
              </div>

              <!-- Quick Actions -->
              <div class="flex flex-wrap gap-2 pt-3 border-t border-gray-600/30">
                <button @click="applyAllSuggestions" class="bg-gradient-to-r from-orange-500 to-purple-500 hover:from-orange-600 hover:to-purple-600 text-white text-sm font-medium px-4 py-2 rounded-lg">
                  Apply All Suggestions
                </button>
                <button @click="selectiveSuggestions" class="bg-gray-600/20 hover:bg-gray-600/30 text-gray-300 text-sm font-medium px-4 py-2 rounded-lg">
                  Choose Specific Suggestions
                </button>
                <button @click="ignoreAllSuggestions" class="bg-red-600/20 hover:bg-red-600/30 text-red-300 text-sm font-medium px-4 py-2 rounded-lg">
                  Continue Without AI Suggestions
                </button>
              </div>
            </div>

            <!-- Step 3: Title -->
            <div class="bg-gradient-to-r from-yellow-500/10 to-green-500/10 border border-yellow-500/20 rounded-xl p-4">
              <label class="block text-sm font-medium text-gray-300 mb-3">
                <span class="inline-flex items-center">
                  <span class="bg-gradient-to-r from-yellow-500 to-green-500 text-white text-sm font-bold px-3 py-2 rounded-full mr-3 shadow-lg">3</span>
                  <span class="text-lg font-semibold text-yellow-300">Title *</span>
                  <span v-if="titleSource === 'ai'" class="ml-2 text-xs bg-orange-500/20 text-orange-300 px-2 py-1 rounded-full">AI Suggested</span>
                  <span v-if="titleSource === 'user'" class="ml-2 text-xs bg-blue-500/20 text-blue-300 px-2 py-1 rounded-full">User Created</span>
                </span>
              </label>
              <div class="relative">
                <input
                  v-model="form.title"
                  type="text"
                  @input="onTitleChange"
                  class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
                placeholder="Enter content title"
                required
              />
              </div>
              <p class="text-sm text-yellow-200 mt-2 font-medium">✨ Create a compelling title that captures attention</p>
            </div>

            <!-- Step 4: Script Generator Section -->
            <div class="bg-gradient-to-r from-orange-500/10 to-yellow-500/10 border border-orange-500/20 rounded-xl p-4 space-y-3">
              <div class="flex items-center justify-between">
                <label class="block text-sm font-medium text-gray-300">
                  <span class="inline-flex items-center">
                    <span class="bg-gradient-to-r from-orange-500 to-yellow-500 text-white text-sm font-bold px-3 py-2 rounded-full mr-3 shadow-lg">4</span>
                    <span class="text-lg font-semibold text-orange-300">Video Script</span>
                  </span>
                </label>
                <button
                  type="button"
                  @click.stop="generateScript"
                  class="text-xs text-purple-400 hover:text-purple-300 transition-colors flex items-center space-x-1"
                  title="Generate AI script"
                >
                  <span>✨</span>
                  <span>Generate Script</span>
                </button>
              </div>
              <div class="relative">
                <textarea
                  v-model="form.script"
                  placeholder="Your video script will appear here... Click 'Generate Script' to create an AI-powered script based on your title and description."
                  class="w-full px-3 py-2 bg-forest-800 border border-forest-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                  rows="8"
                ></textarea>
              </div>

              <!-- Script Generation Options -->
              <div v-if="showScriptOptions" class="space-y-3 p-3 bg-purple-500/10 border border-purple-500/20 rounded-md">
                <div class="text-xs text-purple-300 font-medium">🎬 Script Options:</div>

                <!-- Script Type Selection -->
                <div class="space-y-2">
                  <label class="text-xs text-gray-300">Script Type:</label>
                  <div class="flex flex-wrap gap-2">
                    <button
                      v-for="type in scriptTypes"
                      :key="type.value"
                      type="button"
                      @click.stop="selectedScriptType = type.value"
                      :class="[
                        'px-2 py-1 text-xs rounded transition-colors border',
                        selectedScriptType === type.value
                          ? 'bg-purple-500/30 text-purple-300 border-purple-500/50'
                          : 'bg-purple-500/10 text-purple-400 border-purple-500/20 hover:bg-purple-500/20'
                      ]"
                    >
                      {{ type.label }}
                    </button>
                  </div>
                </div>

                <!-- Script Length Selection -->
                <div class="space-y-2">
                  <label class="text-xs text-gray-300">Video Length:</label>
                  <div class="flex flex-wrap gap-2">
                    <button
                      v-for="length in scriptLengths"
                      :key="length.value"
                      type="button"
                      @click.stop="selectedScriptLength = length.value"
                      :class="[
                        'px-2 py-1 text-xs rounded transition-colors border',
                        selectedScriptLength === length.value
                          ? 'bg-purple-500/30 text-purple-300 border-purple-500/50'
                          : 'bg-purple-500/10 text-purple-400 border-purple-500/20 hover:bg-purple-500/20'
                      ]"
                    >
                      {{ length.label }}
                    </button>
                  </div>
                </div>

                <!-- Tone Selection -->
                <div class="space-y-2">
                  <label class="text-xs text-gray-300">Tone & Style:</label>
                  <div class="flex flex-wrap gap-2">
                    <button
                      v-for="tone in scriptTones"
                      :key="tone.value"
                      type="button"
                      @click.stop="selectedScriptTone = tone.value"
                      :class="[
                        'px-2 py-1 text-xs rounded transition-colors border',
                        selectedScriptTone === tone.value
                          ? 'bg-purple-500/30 text-purple-300 border-purple-500/50'
                          : 'bg-purple-500/10 text-purple-400 border-purple-500/20 hover:bg-purple-500/20'
                      ]"
                    >
                      {{ tone.label }}
                    </button>
                  </div>
                </div>

                <div class="flex justify-between items-center pt-2">
                  <button
                    type="button"
                    @click.stop="showScriptOptions = false"
                    class="text-xs text-gray-400 hover:text-gray-300"
                  >
                    Hide options
                  </button>
                  <button
                    type="button"
                    @click.stop="generateCustomScript"
                    class="px-3 py-1 bg-purple-500 text-white text-xs rounded hover:bg-purple-600 transition-colors"
                  >
                    Generate Custom Script
                  </button>
                </div>
              </div>

              <!-- Script Templates -->
              <div v-if="showScriptTemplates" class="space-y-2">
                <div class="text-xs text-purple-300 font-medium">📝 Quick Script Templates:</div>
                <div class="grid grid-cols-2 gap-2">
                  <button
                    v-for="template in scriptTemplates"
                    :key="template.name"
                    type="button"
                    @click.stop="applyScriptTemplate(template)"
                    class="p-2 bg-purple-500/10 border border-purple-500/20 rounded text-xs text-purple-300 hover:bg-purple-500/20 transition-colors text-left"
                  >
                    <div class="font-medium">{{ template.name }}</div>
                    <div class="text-gray-400 text-xs">{{ template.description }}</div>
                  </button>
                </div>
                <button
                  type="button"
                  @click.stop="showScriptTemplates = false"
                  class="text-xs text-gray-400 hover:text-gray-300"
                >
                  Hide templates
                </button>
              </div>

              <div class="flex justify-between items-center">
                <div class="flex space-x-2 text-xs">
                  <button
                    type="button"
                    @click.stop="showScriptOptions = !showScriptOptions"
                    class="text-purple-400 hover:text-purple-300 transition-colors"
                  >
                    ⚙️ Options
                  </button>
                  <button
                    type="button"
                    @click.stop="showScriptTemplates = !showScriptTemplates"
                    class="text-purple-400 hover:text-purple-300 transition-colors"
                  >
                    📋 Templates
                  </button>
                </div>
                <div class="text-xs text-gray-400">
                  {{ form.script ? form.script.split(' ').length : 0 }} words
                </div>
              </div>

              <p class="text-sm text-orange-200 mt-2 font-medium">🎬 AI-generated scripts help structure your content and improve engagement</p>
            </div>

            <!-- Step 5: Tags with Keyword Suggestions -->
            <div class="bg-gradient-to-r from-red-500/10 to-orange-500/10 border border-red-500/20 rounded-xl p-4 space-y-3">
              <div class="flex items-center justify-between">
                <label class="block text-sm font-medium text-gray-300">
                  <span class="inline-flex items-center">
                    <span class="bg-gradient-to-r from-red-500 to-orange-500 text-white text-sm font-bold px-3 py-2 rounded-full mr-3 shadow-lg">5</span>
                    <span class="text-lg font-semibold text-red-300">Tags & Keywords</span>
                  </span>
                </label>
                <button
                  type="button"
                  @click.stop="generateKeywordSuggestions"
                  class="text-xs text-blue-400 hover:text-blue-300 transition-colors flex items-center space-x-1"
                  title="Get keyword suggestions"
                >
                  <span>💡</span>
                  <span>Get keywords</span>
                </button>
              </div>
              <div class="relative">
                <input
                  v-model="form.tags"
                  type="text"
                  placeholder="Enter tags separated by commas"
                  class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  @focus="showKeywordSuggestions = true"
                />
              </div>

              <!-- Keyword Suggestions -->
              <div v-if="showKeywordSuggestions && keywordSuggestions.length > 0" class="mt-2 p-3 bg-orange-500/10 rounded-lg border border-orange-500/20">
                <div class="text-sm font-medium text-orange-300 mb-2">💡 Suggested Keywords:</div>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="keyword in keywordSuggestions"
                    :key="keyword"
                    type="button"
                    @click.stop="addKeywordToTags(keyword)"
                    class="px-2 py-1 bg-orange-500/20 text-orange-300 rounded text-xs hover:bg-orange-500/30 transition-colors border border-orange-500/30"
                  >
                    + {{ keyword }}
                  </button>
                </div>
                <button
                  type="button"
                  @click.stop="showKeywordSuggestions = false"
                  class="mt-2 text-xs text-gray-400 hover:text-gray-300"
                >
                  Hide suggestions
                </button>
              </div>

              <p class="text-sm text-red-200 mt-2 font-medium">🏷️ Separate tags with commas for better SEO</p>
            </div>

            <!-- Step 6: Hashtags Section -->
            <div class="bg-gradient-to-r from-pink-500/10 to-red-500/10 border border-pink-500/20 rounded-xl p-4 space-y-3">
              <div class="flex items-center justify-between">
                <label class="block text-sm font-medium text-gray-300">
                  <span class="inline-flex items-center">
                    <span class="bg-gradient-to-r from-pink-500 to-red-500 text-white text-sm font-bold px-3 py-2 rounded-full mr-3 shadow-lg">6</span>
                    <span class="text-lg font-semibold text-pink-300">Hashtags</span>
                  </span>
                </label>
                <button
                  type="button"
                  @click.stop="generateHashtagSuggestions"
                  class="text-xs text-blue-400 hover:text-blue-300 transition-colors flex items-center space-x-1"
                  title="Get hashtag suggestions"
                >
                  <span>💡</span>
                  <span>Get hashtags</span>
                </button>
              </div>
              <div class="relative">
                <textarea
                  v-model="form.hashtags"
                  placeholder="Enter hashtags separated by spaces (e.g., #contentcreator #youtube #socialmedia)"
                  class="w-full px-3 py-2 bg-forest-800 border border-forest-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  rows="2"
                ></textarea>
              </div>

              <!-- Hashtag Suggestions -->
              <div v-if="showHashtagSuggestions" class="space-y-2">
                <div class="text-xs text-blue-300 font-medium">💡 Suggested Hashtags:</div>
                <div class="flex flex-wrap gap-1">
                  <button
                    v-for="hashtag in hashtagSuggestions"
                    :key="hashtag"
                    type="button"
                    @click.stop="addHashtagToContent(hashtag)"
                    class="px-2 py-1 bg-blue-500/20 text-blue-300 rounded text-xs hover:bg-blue-500/30 transition-colors border border-blue-500/30"
                  >
                    {{ hashtag }}
                  </button>
                </div>
                <button
                  type="button"
                  @click.stop="showHashtagSuggestions = false"
                  class="mt-2 text-xs text-gray-400 hover:text-gray-300"
                >
                  Hide hashtag suggestions
                </button>
              </div>
              <p class="text-sm text-pink-200 mt-2 font-medium">#️⃣ Use hashtags to increase discoverability on social platforms</p>
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

            <!-- Team Notes Section -->
            <div class="bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-xl p-4">
              <label class="block text-sm font-medium text-gray-300 mb-3">
                <span class="inline-flex items-center">
                  <span class="bg-gradient-to-r from-blue-500 to-purple-500 text-white text-sm font-bold px-3 py-2 rounded-full mr-3 shadow-lg">👥</span>
                  <span class="text-lg font-semibold text-blue-300">Team Notes</span>
                </span>
              </label>
              <textarea
                v-model="form.teamNotes"
                placeholder="Add notes for your team members about this content piece..."
                rows="4"
                class="w-full px-4 py-3 bg-forest-700 border border-forest-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              />
              <div class="mt-2 text-xs text-gray-400">
                Share important details, deadlines, or collaboration notes with your team
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

        <!-- Right Column: Agent -->
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

            <!-- Step-by-Step Content Workflow (for new content only) -->
            <div v-if="!props.content" class="space-y-6">
              <h5 class="text-sm font-medium text-gray-300 uppercase tracking-wide">Content Workflow Assistant</h5>

              <!-- Step 1: Pillar Selection -->
              <div class="bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-xl p-3 space-y-3">
                <div class="flex items-center space-x-3">
                  <span class="bg-gradient-to-r from-blue-500 to-purple-500 text-white text-sm font-bold px-3 py-2 rounded-full shadow-lg">1</span>
                  <span class="text-base font-semibold text-blue-300">Choose Content Pillar</span>
                </div>
                <div class="text-sm text-blue-200 font-medium">
                  {{ form.pillarId ? '✅ Pillar selected' : '⏳ Select your content pillar first' }}
                </div>
              </div>

              <!-- Step 2: Description -->
              <div class="bg-gradient-to-r from-green-500/10 to-blue-500/10 border border-green-500/20 rounded-xl p-3 space-y-2">
                <div class="flex items-center space-x-3">
                  <span class="bg-gradient-to-r from-green-500 to-blue-500 text-white text-sm font-bold px-3 py-2 rounded-full shadow-lg">2</span>
                  <span class="text-base font-semibold text-green-300">Add Description</span>
                </div>
                <div class="text-sm text-green-200 ml-10 font-medium">
                  {{ form.description ? '✅ Description added' : '⏳ Input by the user in the form' }}
                </div>
              </div>

              <!-- Step 3: Title Generation -->
              <div class="bg-gradient-to-r from-yellow-500/10 to-green-500/10 border border-yellow-500/20 rounded-xl p-3 space-y-3">
                <div class="flex items-center space-x-3">
                  <span class="bg-gradient-to-r from-yellow-500 to-green-500 text-white text-sm font-bold px-3 py-2 rounded-full shadow-lg">3</span>
                  <span class="text-base font-semibold text-yellow-300">Create Title</span>
                </div>
                <button
                  @click="generateTitle"
                  :disabled="isGenerating || !form.pillarId"
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

                <!-- Title Suggestions Panel -->
                <div v-if="showTitleSuggestions" class="mt-3 space-y-2">
                  <div class="text-sm font-medium text-yellow-300 mb-2">💡 Title Suggestions</div>
                  <div class="space-y-1">
                    <button
                      v-for="(suggestion, index) in titleSuggestions"
                      :key="`title-${index}`"
                      @click="selectTitleSuggestion(suggestion)"
                      class="w-full text-left p-2 bg-forest-800/50 hover:bg-forest-700 rounded text-xs text-gray-300 hover:text-white transition-colors border border-forest-600/30 hover:border-yellow-500/50"
                    >
                      {{ suggestion }}
                    </button>
                  </div>
                  <button
                    @click="showTitleSuggestions = false"
                    class="text-xs text-gray-400 hover:text-gray-300 mt-2"
                  >
                    ✕ Close suggestions
                  </button>
                </div>
              </div>

              <!-- Step 4: Script Generation -->
              <div class="bg-gradient-to-r from-orange-500/10 to-yellow-500/10 border border-orange-500/20 rounded-xl p-3 space-y-2">
                <div class="flex items-center space-x-3">
                  <span class="bg-gradient-to-r from-orange-500 to-yellow-500 text-white text-sm font-bold px-3 py-2 rounded-full shadow-lg">4</span>
                  <span class="text-base font-semibold text-orange-300">Generate Script</span>
                </div>
                <div class="text-sm text-orange-200 ml-10 font-medium">
                  {{ form.script ? '✅ Script generated' : '⏳ Use the Generate Script button in the form' }}
                </div>
              </div>

              <!-- Step 5: Keywords -->
              <div class="bg-gradient-to-r from-red-500/10 to-orange-500/10 border border-red-500/20 rounded-xl p-3 space-y-2">
                <div class="flex items-center space-x-3">
                  <span class="bg-gradient-to-r from-red-500 to-orange-500 text-white text-sm font-bold px-3 py-2 rounded-full shadow-lg">5</span>
                  <span class="text-base font-semibold text-red-300">Add Keywords</span>
                </div>
                <div class="text-sm text-red-200 ml-10 font-medium">
                  {{ form.tags ? '✅ Keywords added' : '⏳ Use keyword suggestions in the form' }}
                </div>
              </div>

              <!-- Step 6: Hashtags -->
              <div class="bg-gradient-to-r from-pink-500/10 to-red-500/10 border border-pink-500/20 rounded-xl p-3 space-y-2">
                <div class="flex items-center space-x-3">
                  <span class="bg-gradient-to-r from-pink-500 to-red-500 text-white text-sm font-bold px-3 py-2 rounded-full shadow-lg">6</span>
                  <span class="text-base font-semibold text-pink-300">Add Hashtags</span>
                </div>
                <div class="text-sm text-pink-200 ml-10 font-medium">
                  {{ form.hashtags ? '✅ Hashtags added' : '⏳ Use hashtag suggestions in the form' }}
                </div>
              </div>
            </div>

            <!-- Performance Predictions (for existing content) -->
            <div v-if="props.content" class="space-y-6">
              <h5 class="text-sm font-medium text-gray-300 uppercase tracking-wide">Performance Predictions</h5>

              <!-- Confidence Score -->
              <div class="p-4 bg-gradient-to-r from-green-900/30 to-emerald-900/30 rounded-lg border border-green-500/30">
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                    <h6 class="text-sm font-medium text-green-300">Confidence Score</h6>
                  </div>
                  <span class="text-lg font-bold text-green-400">{{ getContentConfidence() }}%</span>
                </div>
                <div class="mt-2 w-full bg-gray-700 rounded-full h-2">
                  <div class="bg-gradient-to-r from-green-400 to-emerald-400 h-2 rounded-full transition-all duration-500" :style="{ width: getContentConfidence() + '%' }"></div>
                </div>
              </div>

              <!-- Expected Views -->
              <div class="p-4 bg-gradient-to-r from-blue-900/30 to-cyan-900/30 rounded-lg border border-blue-500/30">
                <div class="flex items-center space-x-2 mb-3">
                  <span class="text-lg">👁️</span>
                  <h6 class="text-sm font-medium text-blue-300">Expected Views</h6>
                </div>
                <div class="text-2xl font-bold text-blue-400 mb-1">{{ getContentPredictedViews() }}</div>
                <div class="text-xs text-blue-200">Based on content priority and pillar performance</div>
              </div>

              <!-- Engagement Rate -->
              <div class="p-4 bg-gradient-to-r from-purple-900/30 to-pink-900/30 rounded-lg border border-purple-500/30">
                <div class="flex items-center space-x-2 mb-3">
                  <span class="text-lg">💬</span>
                  <h6 class="text-sm font-medium text-purple-300">Engagement Rate</h6>
                </div>
                <div class="text-2xl font-bold text-purple-400 mb-1">{{ getContentPredictedEngagement() }}%</div>
                <div class="text-xs text-purple-200">Likes, comments, and shares prediction</div>
              </div>

              <!-- Best Time to Post -->
              <div class="p-4 bg-gradient-to-r from-orange-900/30 to-yellow-900/30 rounded-lg border border-orange-500/30">
                <div class="flex items-center space-x-2 mb-3">
                  <span class="text-lg">⏰</span>
                  <h6 class="text-sm font-medium text-orange-300">Optimal Posting Time</h6>
                </div>
                <div class="text-xl font-bold text-orange-400 mb-1">{{ getContentBestTime() }}</div>
                <div class="text-xs text-orange-200">When your audience is most active</div>
              </div>

              <!-- Completion Date -->
              <div class="p-4 bg-gradient-to-r from-indigo-900/30 to-blue-900/30 rounded-lg border border-indigo-500/30">
                <div class="flex items-center space-x-2 mb-3">
                  <span class="text-lg">📅</span>
                  <h6 class="text-sm font-medium text-indigo-300">Estimated Completion</h6>
                </div>
                <div class="text-xl font-bold text-indigo-400 mb-1">{{ getContentCompletionDate() }}</div>
                <div class="text-xs text-indigo-200">Based on current priority and workflow</div>
              </div>

              <div class="space-y-4">
                <h6 class="text-sm font-medium text-gray-300 uppercase tracking-wide">Optimization Tips</h6>
                <div
                  v-for="(tip, index) in getContentOptimizationTips()"
                  :key="tip.id"
                  class="p-4 rounded-lg border transition-all duration-200 hover:scale-[1.02]"
                  :class="{
                    'bg-gradient-to-r from-red-900/30 to-pink-900/30 border-red-500/30': index === 0,
                    'bg-gradient-to-r from-teal-900/30 to-cyan-900/30 border-teal-500/30': index === 1,
                    'bg-gradient-to-r from-amber-900/30 to-orange-900/30 border-amber-500/30': index === 2
                  }"
                >
                  <div class="flex items-start space-x-3">
                    <span class="text-lg">{{ tip.icon }}</span>
                    <div class="flex-1">
                      <div class="text-sm font-medium text-white mb-1">{{ tip.title }}</div>
                      <div class="text-xs text-gray-300">{{ tip.description }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Contextual Tips & Suggestions (for new content) -->
            <div v-else class="space-y-4">
              <h5 class="text-sm font-medium text-gray-300 uppercase tracking-wide">Contextual Tips</h5>

              <!-- Current Step Guidance -->
              <div class="p-3 bg-purple-500/10 border border-purple-500/20 rounded-lg">
                <div class="flex items-center space-x-2 mb-2">
                  <span class="text-purple-400">💡</span>
                  <span class="text-sm font-medium text-purple-300">Current Step</span>
                </div>
                <div class="text-xs text-gray-300">
                  <div v-if="!form.pillarId">
                    <strong>Step 1:</strong> Choose a content pillar to define your content strategy and unlock AI suggestions.
                  </div>
                  <div v-else-if="!form.description">
                    <strong>Step 2:</strong> Add a description to provide context for your content.
                  </div>
                  <div v-else-if="!form.title">
                    <strong>Step 3:</strong> Create a compelling title. Use the Generate Title button for AI suggestions.
                  </div>
                  <div v-else-if="!form.script">
                    <strong>Step 4:</strong> Generate a video script to structure your content and improve engagement.
                  </div>
                  <div v-else-if="!form.tags">
                    <strong>Step 5:</strong> Add keywords and tags for better SEO and discoverability.
                  </div>
                  <div v-else-if="!form.hashtags">
                    <strong>Step 6:</strong> Add hashtags to increase social media reach and engagement.
                  </div>
                  <div v-else>
                    <strong>✅ Complete!</strong> Your content is ready. Review and create when satisfied.
                  </div>
                </div>
              </div>

              <!-- Dynamic Suggestions Based on Current Step -->
              <div class="space-y-3">
                <div
                  v-for="(suggestion, index) in getContextualSuggestions()"
                  :key="`suggestion-${index}`"
                  class="p-3 bg-forest-700/50 rounded-lg border border-forest-600/30 hover:bg-forest-700/70 transition-colors cursor-pointer"
                  @click="selectSuggestion(suggestion)"
                >
                  <div class="flex items-start space-x-3">
                    <span class="text-lg">{{ suggestion.icon }}</span>
                    <div class="flex-1">
                      <div class="text-sm font-medium text-white mb-1">{{ suggestion.title }}</div>
                      <div class="text-xs text-gray-400 mb-2">{{ suggestion.description }}</div>

                      <!-- Action Buttons -->
                      <div class="flex items-center space-x-2">
                        <button
                          v-if="suggestion.action"
                          @click.stop="applySuggestion(suggestion)"
                          class="text-xs px-2 py-1 bg-orange-500/20 text-orange-400 hover:text-orange-300 hover:bg-orange-500/30 rounded transition-colors"
                        >
                          Apply to Form
                        </button>
                        <button
                          @click.stop="saveAsContent(suggestion)"
                          class="text-xs px-2 py-1 bg-blue-500/20 text-blue-400 hover:text-blue-300 hover:bg-blue-500/30 rounded transition-colors"
                        >
                          Save as Content
                        </button>
                        <button
                          @click.stop="saveAsTask(suggestion)"
                          class="text-xs px-2 py-1 bg-green-500/20 text-green-400 hover:text-green-300 hover:bg-green-500/30 rounded transition-colors"
                        >
                          Save as Task
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Trending Keywords -->
              <div class="space-y-4 mb-6">
                <TrendingKeywords
                  @keyword-selected="handleKeywordSelected"
                  @content-idea-selected="handleContentIdeaSelected"
                  @generate-ideas="handleGenerateIdeas"
                  @analyze-competitors="handleAnalyzeCompetitors"
                />
              </div>

              <!-- Content Templates (for new content only) -->
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
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useAgentSettings } from '../../composables/useAgentSettings.js'
import { useModals } from '../../composables/useModals.js'
import { usePillars } from '../../composables/usePillars.js'
import TrendingKeywords from '../dashboard/TrendingKeywords.vue'

const props = defineProps({
  content: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'save'])

// Agent settings
const { selectedAgent, agentName, allAgents } = useAgentSettings()

// Modal functions for creating new content/tasks
const { openContent, openTask } = useModals()

// Get pillars from the main pillars composable
const { pillars } = usePillars()

// Transform pillars for the dropdown (use actual pillars from pillars page)
const availablePillars = computed(() => {
  return pillars.value.map(pillar => ({
    id: pillar.id,
    name: pillar.name,
    icon: getIconEmoji(pillar.icon) // Convert icon name to emoji
  }))
})

// Helper function to convert icon names to emojis
const getIconEmoji = (iconName) => {
  const iconMap = {
    'GameIcon': '🎮',
    'ReviewIcon': '⭐',
    'TechIcon': '💻',
    'ProductivityIcon': '⏰'
  }
  return iconMap[iconName] || '📝'
}

// Generation state
const isGenerating = ref(false)

// Keyword suggestions state
const showKeywordSuggestions = ref(false)
const keywordSuggestions = ref([
  'YouTube growth', 'content strategy', 'video optimization', 'creator tips',
  'analytics insights', 'engagement boost', 'viral content', 'SEO tactics'
])

// Generate keyword suggestions based on title, pillar, and script content
const generateKeywordSuggestions = async () => {
  try {
    // In real implementation, this would call an API
    const pillar = availablePillars.value.find(p => p.id === form.value.pillarId)
    const suggestions = []

    if (pillar) {
      suggestions.push(`${pillar.name.toLowerCase()} tips`)
      suggestions.push(`${pillar.name.toLowerCase()} strategy`)
    }

    if (form.value.title) {
      const titleWords = form.value.title.toLowerCase().split(' ')
      titleWords.forEach(word => {
        if (word.length > 4) {
          suggestions.push(`${word} guide`)
          suggestions.push(`${word} tutorial`)
        }
      })
    }

    // Analyze script content for additional keywords
    if (form.value.script) {
      const scriptText = form.value.script.toLowerCase()

      // Extract key phrases from script
      const keyPhrases = [
        'step by step', 'how to', 'tutorial', 'guide', 'tips', 'tricks',
        'strategy', 'beginner', 'advanced', 'complete', 'ultimate', 'best',
        'review', 'comparison', 'vs', 'analysis', 'breakdown', 'explained'
      ]

      keyPhrases.forEach(phrase => {
        if (scriptText.includes(phrase)) {
          suggestions.push(phrase)
        }
      })

      // Extract important words from script (longer than 5 characters)
      const scriptWords = scriptText.match(/\b\w{6,}\b/g) || []
      const commonWords = scriptWords
        .filter(word => !['introduction', 'conclusion', 'everyone', 'welcome', 'channel', 'subscribe'].includes(word))
        .slice(0, 5)

      commonWords.forEach(word => {
        suggestions.push(word)
        suggestions.push(`${word} tips`)
      })
    }

    // Add trending keywords
    suggestions.push('YouTube 2024', 'content creator', 'viral strategy', 'growth hacks')

    keywordSuggestions.value = [...new Set(suggestions)].slice(0, 12)
    showKeywordSuggestions.value = true
  } catch (error) {
    console.error('Error generating keyword suggestions:', error)
  }
}

// Add keyword to tags
const addKeywordToTags = (keyword) => {
  const currentTags = form.value.tags ? form.value.tags.split(',').map(t => t.trim()) : []
  if (!currentTags.includes(keyword)) {
    currentTags.push(keyword)
    form.value.tags = currentTags.join(', ')
  }
}

// Hashtag suggestions state
const showHashtagSuggestions = ref(false)
const hashtagSuggestions = ref([])

// Generate hashtag suggestions based on title, pillar, script, and content
const generateHashtagSuggestions = async () => {
  try {
    const pillar = availablePillars.value.find(p => p.id === form.value.pillarId)
    const title = form.value.title.toLowerCase()
    const description = form.value.description.toLowerCase()
    const script = form.value.script.toLowerCase()

    let suggestions = []

    // Base hashtags for all content
    suggestions.push('#contentcreator', '#youtube', '#socialmedia', '#content')

    // Pillar-specific hashtags
    if (pillar?.name === 'Game Development') {
      suggestions.push('#gamedev', '#indiegame', '#gaming', '#unity', '#unreal', '#gamedesign')
    } else if (pillar?.name === 'Marketing') {
      suggestions.push('#marketing', '#digitalmarketing', '#socialmediamarketing', '#contentmarketing', '#growth')
    } else if (pillar?.name === 'Tech Tutorials') {
      suggestions.push('#tech', '#tutorial', '#coding', '#programming', '#webdev', '#javascript')
    } else if (pillar?.name === 'Game Reviews') {
      suggestions.push('#gamereview', '#gaming', '#gamer', '#videogames', '#gameanalysis')
    }

    // Content-specific hashtags based on title/description/script
    const allContent = `${title} ${description} ${script}`

    if (allContent.includes('ai')) {
      suggestions.push('#ai', '#artificialintelligence', '#machinelearning')
    }
    if (allContent.includes('trend')) {
      suggestions.push('#trends', '#trending', '#2024trends')
    }
    if (allContent.includes('guide') || allContent.includes('tutorial')) {
      suggestions.push('#guide', '#howto', '#tips', '#tutorial')
    }
    if (allContent.includes('strategy')) {
      suggestions.push('#strategy', '#tactics', '#growth')
    }
    if (allContent.includes('review')) {
      suggestions.push('#review', '#honest', '#analysis', '#breakdown')
    }
    if (allContent.includes('beginner')) {
      suggestions.push('#beginner', '#basics', '#101', '#starter')
    }
    if (allContent.includes('advanced')) {
      suggestions.push('#advanced', '#pro', '#expert', '#masterclass')
    }
    if (allContent.includes('step') || allContent.includes('steps')) {
      suggestions.push('#stepbystep', '#process', '#method')
    }
    if (allContent.includes('secret') || allContent.includes('hack')) {
      suggestions.push('#secrets', '#hacks', '#insider', '#protips')
    }
    if (allContent.includes('2024')) {
      suggestions.push('#2024', '#latest', '#new', '#updated')
    }

    // Script-specific hashtags based on content type
    if (script) {
      if (script.includes('subscribe') || script.includes('like')) {
        suggestions.push('#subscribe', '#like', '#engagement')
      }
      if (script.includes('comment')) {
        suggestions.push('#comment', '#community', '#discussion')
      }
      if (script.includes('share')) {
        suggestions.push('#share', '#viral', '#spread')
      }
    }

    // Popular general hashtags
    suggestions.push('#viral', '#fyp', '#explore', '#creator', '#influence')

    // Remove duplicates and limit to 15 suggestions
    hashtagSuggestions.value = [...new Set(suggestions)].slice(0, 15)
    showHashtagSuggestions.value = true
  } catch (error) {
    console.error('Error generating hashtag suggestions:', error)
  }
}

// Add hashtag to content
const addHashtagToContent = (hashtag) => {
  const currentHashtags = form.value.hashtags ? form.value.hashtags.split(' ').filter(h => h.trim()) : []
  if (!currentHashtags.includes(hashtag)) {
    currentHashtags.push(hashtag)
    form.value.hashtags = currentHashtags.join(' ')
  }
}

// Script generation state
const showScriptOptions = ref(false)
const showScriptTemplates = ref(false)
const selectedScriptType = ref('tutorial')
const selectedScriptLength = ref('medium')
const selectedScriptTone = ref('engaging')

// Script generation options
const scriptTypes = ref([
  { value: 'tutorial', label: 'Tutorial' },
  { value: 'review', label: 'Review' },
  { value: 'vlog', label: 'Vlog' },
  { value: 'educational', label: 'Educational' },
  { value: 'entertainment', label: 'Entertainment' },
  { value: 'unboxing', label: 'Unboxing' },
  { value: 'comparison', label: 'Comparison' },
  { value: 'listicle', label: 'Top 10 List' }
])

const scriptLengths = ref([
  { value: 'short', label: '1-3 min' },
  { value: 'medium', label: '5-8 min' },
  { value: 'long', label: '10-15 min' },
  { value: 'extended', label: '20+ min' }
])

const scriptTones = ref([
  { value: 'engaging', label: 'Engaging' },
  { value: 'professional', label: 'Professional' },
  { value: 'casual', label: 'Casual' },
  { value: 'energetic', label: 'Energetic' },
  { value: 'educational', label: 'Educational' },
  { value: 'humorous', label: 'Humorous' }
])

const scriptTemplates = ref([
  {
    name: 'Hook + Tutorial',
    description: 'Strong opening with step-by-step guide',
    template: `[HOOK - 0:00-0:15]
"Have you ever wondered how to [TOPIC]? In the next [TIME], I'll show you exactly how to do it, step by step."

[INTRODUCTION - 0:15-0:30]
"Hey everyone, welcome back to my channel! I'm [NAME], and today we're diving into [TOPIC]. If this helps you out, don't forget to hit that like button and subscribe for more content like this."

[MAIN CONTENT - 0:30-[TIME]]
"Let's jump right in. Here's what we'll cover:
1. [STEP 1]
2. [STEP 2]
3. [STEP 3]

First, let's start with [STEP 1]..."

[CALL TO ACTION - [TIME]]
"And that's how you [TOPIC]! Which step did you find most helpful? Let me know in the comments below. If you want to see more tutorials like this, make sure to subscribe and hit the notification bell. I'll see you in the next video!"`
  },
  {
    name: 'Problem + Solution',
    description: 'Address a problem and provide solution',
    template: `[PROBLEM IDENTIFICATION - 0:00-0:20]
"Are you struggling with [PROBLEM]? You're not alone. This is one of the most common issues that [AUDIENCE] face, and today I'm going to show you exactly how to solve it."

[CREDIBILITY - 0:20-0:35]
"I'm [NAME], and I've been [EXPERIENCE/CREDENTIALS]. I've helped [NUMBER] people overcome this exact challenge."

[SOLUTION PREVIEW - 0:35-0:50]
"In this video, I'll share [NUMBER] proven strategies that will help you [DESIRED OUTCOME]. Stay until the end because tip number [NUMBER] is a game-changer."

[MAIN CONTENT - 0:50-[TIME]]
"Let's dive into solution number one..."

[CONCLUSION - [TIME]]
"These [NUMBER] strategies have worked for thousands of people, and they'll work for you too. Try them out and let me know your results in the comments!"`
  },
  {
    name: 'Story + Lesson',
    description: 'Personal story with valuable takeaway',
    template: `[STORY HOOK - 0:00-0:20]
"[TIME PERIOD] ago, I [SITUATION/CHALLENGE]. What happened next completely changed my perspective on [TOPIC]."

[STORY DEVELOPMENT - 0:20-[TIME]]
"Let me tell you the full story. It all started when [BEGINNING OF STORY]...

[TURNING POINT]
But then something happened that changed everything...

[RESOLUTION]
And that's when I realized [KEY INSIGHT]."

[LESSON APPLICATION - [TIME]]
"Here's what this taught me, and how you can apply it to your own [SITUATION]:
1. [LESSON 1]
2. [LESSON 2]
3. [LESSON 3]"

[CALL TO ACTION]
"What's your biggest takeaway from this story? Share it in the comments below!"`
  },
  {
    name: 'Review Format',
    description: 'Comprehensive product/service review',
    template: `[INTRODUCTION - 0:00-0:30]
"Today I'm reviewing [PRODUCT/SERVICE]. I've been using it for [TIME PERIOD], and I'm going to give you my honest thoughts - the good, the bad, and everything in between."

[OVERVIEW - 0:30-1:00]
"First, let me show you what [PRODUCT] is and who it's for..."

[DETAILED REVIEW - 1:00-[TIME]]
"Let's break this down into categories:

PROS:
- [PRO 1]
- [PRO 2]
- [PRO 3]

CONS:
- [CON 1]
- [CON 2]

PRICING:
[PRICING DETAILS]"

[FINAL VERDICT - [TIME]]
"So, is [PRODUCT] worth it? Here's my final verdict: [RECOMMENDATION]. If you're [TARGET AUDIENCE], then yes. If you're [NOT TARGET AUDIENCE], then probably not."

[CALL TO ACTION]
"Have you tried [PRODUCT]? Let me know your experience in the comments!"`
  }
])

// Generate basic script based on title and description
const generateScript = async () => {
  try {
    if (!form.value.title.trim()) {
      alert('Please enter a title first to generate a script')
      return
    }

    isGenerating.value = true
    const { $api } = useNuxtApp()

    const pillar = availablePillars.value.find(p => p.id === form.value.pillarId)
    const title = form.value.title
    const description = form.value.description || 'No description provided'
    const pillarName = pillar?.name || 'General'

    // Call backend AI service for script generation
    const response = await $api('/api/content/generate-script', {
      method: 'POST',
      body: {
        title,
        description,
        contentIdea: form.value.contentIdea,
        pillar: pillarName,
        type: 'tutorial',
        length: 'medium',
        tone: 'engaging',
        agent_id: selectedAgent.value.id
      }
    })

    if (response.status === 'success') {
      form.value.script = response.data.script
    } else {
      // Fallback to template-based generation
      let script = generateScriptContent(title, description, pillarName, 'tutorial', 'medium', 'engaging')
      form.value.script = script
    }
  } catch (error) {
    console.error('Error generating script:', error)
    // Fallback to template-based generation
    const pillar = availablePillars.value.find(p => p.id === form.value.pillarId)
    const title = form.value.title
    const description = form.value.description || 'No description provided'
    const pillarName = pillar?.name || 'General'
    let script = generateScriptContent(title, description, pillarName, 'tutorial', 'medium', 'engaging')
    form.value.script = script
  } finally {
    isGenerating.value = false
  }
}

// Generate custom script with selected options
const generateCustomScript = async () => {
  try {
    if (!form.value.title.trim()) {
      alert('Please enter a title first to generate a script')
      return
    }

    isGenerating.value = true
    const { $api } = useNuxtApp()

    const pillar = availablePillars.value.find(p => p.id === form.value.pillarId)
    const title = form.value.title
    const description = form.value.description || 'No description provided'
    const pillarName = pillar?.name || 'General'

    // Call backend AI service for custom script generation
    const response = await $api('/api/content/generate-script', {
      method: 'POST',
      body: {
        title,
        description,
        contentIdea: form.value.contentIdea,
        pillar: pillarName,
        type: selectedScriptType.value,
        length: selectedScriptLength.value,
        tone: selectedScriptTone.value,
        agent_id: selectedAgent.value.id
      }
    })

    if (response.status === 'success') {
      form.value.script = response.data.script
    } else {
      // Fallback to template-based generation
      let script = generateScriptContent(
        title,
        description,
        pillarName,
        selectedScriptType.value,
        selectedScriptLength.value,
        selectedScriptTone.value
      )
      form.value.script = script
    }

    showScriptOptions.value = false
  } catch (error) {
    console.error('Error generating custom script:', error)
    // Fallback to template-based generation
    const pillar = availablePillars.value.find(p => p.id === form.value.pillarId)
    const title = form.value.title
    const description = form.value.description || 'No description provided'
    const pillarName = pillar?.name || 'General'
    let script = generateScriptContent(
      title,
      description,
      pillarName,
      selectedScriptType.value,
      selectedScriptLength.value,
      selectedScriptTone.value
    )
    form.value.script = script
    showScriptOptions.value = false
  } finally {
    isGenerating.value = false
  }
}

// Apply script template
const applyScriptTemplate = (template) => {
  form.value.script = template.template
  showScriptTemplates.value = false
}

// Core script generation logic
const generateScriptContent = (title, description, pillar, type, length, tone) => {
  const hooks = {
    tutorial: [
      `Have you ever wondered how to ${title.toLowerCase()}? In this video, I'll show you exactly how to do it step by step.`,
      `Want to master ${title.toLowerCase()}? You're in the right place! Let's dive in.`,
      `${title} - sounds complicated? It's actually easier than you think. Let me show you how.`
    ],
    review: [
      `I've been testing ${title.toLowerCase()} for the past few weeks, and here's my honest review.`,
      `Is ${title.toLowerCase()} worth your money? Let's find out together.`,
      `${title} - the good, the bad, and everything you need to know before buying.`
    ],
    educational: [
      `Today we're exploring ${title.toLowerCase()} - and trust me, this will change how you think about ${pillar.toLowerCase()}.`,
      `What if I told you that ${title.toLowerCase()} could revolutionize your approach to ${pillar.toLowerCase()}?`,
      `Let's break down ${title.toLowerCase()} in a way that actually makes sense.`
    ]
  }

  const introductions = {
    engaging: `Hey everyone! Welcome back to my channel. I'm [YOUR NAME], and if you're new here, I create content about ${pillar.toLowerCase()} to help you [ACHIEVE GOAL].`,
    professional: `Hello and welcome. I'm [YOUR NAME], and today we'll be discussing ${title.toLowerCase()} in detail.`,
    casual: `What's up everyone! Back with another video, and today we're talking about ${title.toLowerCase()}.`,
    energetic: `Hey hey hey! Welcome back to the channel! I am SO excited to share this with you today!`,
    educational: `Welcome to today's lesson. I'm [YOUR NAME], and we'll be exploring ${title.toLowerCase()} from a comprehensive perspective.`,
    humorous: `Well, well, well... look who's back for more ${pillar.toLowerCase()} content! Today's topic: ${title.toLowerCase()}. Buckle up!`
  }

  const mainContentStructures = {
    tutorial: `
[MAIN CONTENT]
Let's break this down into simple steps:

Step 1: [FIRST STEP]
${description.includes('step') ? 'As mentioned in the description, ' : ''}[Detailed explanation of first step]

Step 2: [SECOND STEP]
Now that we've covered the basics, let's move on to [next concept]

Step 3: [THIRD STEP]
This is where it gets interesting. [Advanced technique or tip]

Pro Tip: [BONUS TIP]
Here's something most people don't know about ${title.toLowerCase()}...`,

    review: `
[DETAILED REVIEW]
Let me break down my experience with ${title.toLowerCase()}:

What I Loved:
✓ [POSITIVE ASPECT 1]
✓ [POSITIVE ASPECT 2]
✓ [POSITIVE ASPECT 3]

What Could Be Better:
✗ [NEGATIVE ASPECT 1]
✗ [NEGATIVE ASPECT 2]

Overall Performance:
${description ? `Based on ${description.toLowerCase()}, ` : ''}I'd rate this [RATING]/10.`,

    educational: `
[CORE CONCEPTS]
To understand ${title.toLowerCase()}, we need to cover three key areas:

1. The Foundation
${description ? `As we discussed, ${description.toLowerCase()}` : 'The basic principles are...'}

2. Practical Applications
Here's how this applies in real-world scenarios...

3. Advanced Strategies
Once you master the basics, you can implement these advanced techniques...`
  }

  const conclusions = {
    short: `And that's a wrap! Hope this helped you understand ${title.toLowerCase()} better.`,
    medium: `So there you have it - everything you need to know about ${title.toLowerCase()}. The key takeaways are [SUMMARY OF MAIN POINTS].`,
    long: `We've covered a lot of ground today. From [TOPIC 1] to [TOPIC 2], you now have a comprehensive understanding of ${title.toLowerCase()}. Remember, the most important thing is to [KEY ACTION].`,
    extended: `This has been an in-depth exploration of ${title.toLowerCase()}. We've discussed [COMPREHENSIVE SUMMARY]. As you implement these strategies, remember that [FINAL WISDOM].`
  }

  const callToActions = [
    `If this video helped you out, smash that like button and subscribe for more ${pillar.toLowerCase()} content!`,
    `What's your experience with ${title.toLowerCase()}? Drop a comment below and let me know!`,
    `Don't forget to hit the notification bell so you never miss my latest videos!`,
    `Share this video with someone who needs to see it, and I'll see you in the next one!`
  ]

  // Select random elements for variety
  const selectedHook = hooks[type] ? hooks[type][Math.floor(Math.random() * hooks[type].length)] : hooks.tutorial[0]
  const selectedIntro = introductions[tone] || introductions.engaging
  const selectedMainContent = mainContentStructures[type] || mainContentStructures.tutorial
  const selectedConclusion = conclusions[length] || conclusions.medium
  const selectedCTA = callToActions[Math.floor(Math.random() * callToActions.length)]

  return `[HOOK - 0:00-0:15]
${selectedHook}

[INTRODUCTION - 0:15-0:45]
${selectedIntro}

${selectedMainContent}

[CONCLUSION - ${length === 'short' ? '2:30' : length === 'medium' ? '7:00' : length === 'long' ? '14:00' : '18:00'}]
${selectedConclusion}

[CALL TO ACTION]
${selectedCTA}

---
📝 SCRIPT NOTES:
- Replace [PLACEHOLDERS] with your specific content
- Adjust timing based on your speaking pace
- Add personal anecdotes to make it more engaging
- Include relevant visuals or graphics during key points
- Remember to maintain eye contact with the camera
- Speak clearly and at a moderate pace

💡 ENGAGEMENT TIPS:
- Ask questions to encourage comments
- Use hand gestures to emphasize points
- Vary your tone to maintain interest
- Include a clear call-to-action
- End with a teaser for your next video`
}

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
        title: 'AI Gaming Tools: Complete Guide',
        description: 'Create a comprehensive guide on trending AI gaming tools and their applications',
        action: 'apply-trending',
        contentData: {
          title: 'AI Gaming Tools: The Complete 2024 Guide',
          description: 'A comprehensive guide covering the latest AI gaming tools, their features, and how to use them effectively for content creation.',
          status: 'ideas',
          priority: 'high'
        }
      },
      {
        id: 'gaming-tutorial',
        icon: '🎮',
        title: 'Gaming Tutorial Series',
        description: 'Step-by-step tutorials for popular gaming tools',
        action: null,
        contentData: {
          title: 'Gaming Tool Tutorials: From Beginner to Pro',
          description: 'Create a series of tutorials showing how to master popular gaming tools and techniques.',
          status: 'ideas',
          priority: 'medium'
        }
      },
      {
        id: 'optimal-timing',
        icon: '⏰',
        title: 'Schedule Content Publishing',
        description: 'Set up optimal publishing schedule for gaming content',
        action: 'set-timing',
        taskData: {
          title: 'Research optimal publishing times for gaming content',
          description: 'Analyze audience engagement patterns to determine best posting schedule',
          priority: 'medium',
          dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] // 1 week from now
        }
      }
    )
  }

  if (pillar?.name === 'Marketing') {
    suggestions.push({
      id: 'marketing-hook',
      icon: '🎯',
      title: 'Marketing Hook Strategy',
      description: 'Create content that addresses audience pain points',
      action: 'apply-hook',
      contentData: {
        title: 'Solving Your Biggest Marketing Challenge',
        description: 'Are you struggling with low engagement? This comprehensive guide will help you create content that resonates with your audience.',
        status: 'ideas',
        priority: 'high'
      }
    })
  }

  if (form.value.status === 'ideas') {
    suggestions.push(
      {
        id: 'research-tip',
        icon: '🔍',
        title: 'Competitor Research Guide',
        description: 'Analyze competitor content to find content gaps and opportunities',
        action: null,
        contentData: {
          title: 'Complete Competitor Analysis Framework',
          description: 'A step-by-step guide to researching competitors and identifying content opportunities in your niche.',
          status: 'ideas',
          priority: 'medium'
        }
      },
      {
        id: 'content-calendar',
        icon: '📅',
        title: 'Content Calendar Planning',
        description: 'Plan your content strategy for the next month',
        action: null,
        taskData: {
          title: 'Create content calendar for next month',
          description: 'Plan and schedule content topics, publishing dates, and promotional strategy',
          priority: 'high',
          dueDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] // 3 days from now
        }
      }
    )
  }

  // Add some general suggestions that always appear
  suggestions.push(
    {
      id: 'seo-optimization',
      icon: '🔍',
      title: 'SEO Content Optimization',
      description: 'Create SEO-friendly content that ranks well in search results',
      action: null,
      contentData: {
        title: 'SEO Content Strategy Guide',
        description: 'Learn how to create content that ranks well in search engines and drives organic traffic.',
        status: 'ideas',
        priority: 'high'
      }
    },
    {
      id: 'engagement-boost',
      icon: '💬',
      title: 'Audience Engagement Strategy',
      description: 'Increase audience interaction and community building',
      action: null,
      taskData: {
        title: 'Develop audience engagement strategy',
        description: 'Create a plan to increase comments, shares, and community interaction',
        priority: 'medium',
        dueDate: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] // 5 days from now
      }
    },
    {
      id: 'content-repurpose',
      icon: '♻️',
      title: 'Content Repurposing Ideas',
      description: 'Turn one piece of content into multiple formats',
      action: null,
      contentData: {
        title: 'Content Repurposing Masterclass',
        description: 'Learn how to maximize your content by repurposing it across different platforms and formats.',
        status: 'ideas',
        priority: 'medium'
      }
    }
  )

  return suggestions
})

// Contextual suggestions based on current workflow step
const getContextualSuggestions = () => {
  const suggestions = []
  const pillar = availablePillars.value.find(p => p.id === form.value.pillarId)

  // Step 1: Pillar Selection
  if (!form.value.pillarId) {
    suggestions.push(
      {
        id: 'pillar-guide',
        icon: '🎯',
        title: 'Choose the Right Content Pillar',
        description: 'Learn how to select the best pillar for your content strategy',
        action: null
      },
      {
        id: 'pillar-examples',
        icon: '💡',
        title: 'Content Pillar Examples',
        description: 'See examples of successful content for each pillar type',
        action: null
      }
    )
  }
  // Step 2: Title Creation
  else if (!form.value.title) {
    suggestions.push(
      {
        id: 'title-formulas',
        icon: '✨',
        title: 'Proven Title Formulas',
        description: 'Use tested title structures that drive clicks and engagement',
        action: null
      },
      {
        id: 'title-keywords',
        icon: '🔍',
        title: 'SEO Title Optimization',
        description: 'Include target keywords for better search visibility',
        action: null
      }
    )
  }
  // Step 3: Description
  else if (!form.value.description) {
    suggestions.push(
      {
        id: 'description-hook',
        icon: '🎣',
        title: 'Write Compelling Descriptions',
        description: 'Create descriptions that hook viewers and encourage engagement',
        action: null
      }
    )
  }
  // Step 4: Script
  else if (!form.value.script) {
    suggestions.push(
      {
        id: 'script-structure',
        icon: '📝',
        title: 'Video Script Structure',
        description: 'Learn the proven structure for engaging video scripts',
        action: null
      },
      {
        id: 'script-hooks',
        icon: '🎬',
        title: 'Powerful Opening Hooks',
        description: 'Start your videos with hooks that grab attention immediately',
        action: null
      }
    )
  }
  // Step 5: Keywords
  else if (!form.value.tags) {
    suggestions.push(
      {
        id: 'keyword-research',
        icon: '🔍',
        title: 'Keyword Research Tips',
        description: 'Find the right keywords to boost your content discoverability',
        action: null
      }
    )
  }
  // Step 6: Hashtags
  else if (!form.value.hashtags) {
    suggestions.push(
      {
        id: 'hashtag-strategy',
        icon: '#️⃣',
        title: 'Hashtag Strategy Guide',
        description: 'Use hashtags effectively to reach your target audience',
        action: null
      }
    )
  }
  // All steps complete
  else {
    suggestions.push(
      {
        id: 'content-optimization',
        icon: '🚀',
        title: 'Final Content Review',
        description: 'Review and optimize your content before publishing',
        action: null
      },
      {
        id: 'promotion-strategy',
        icon: '📢',
        title: 'Content Promotion Plan',
        description: 'Plan how to promote your content across platforms',
        action: null
      }
    )
  }

  return suggestions
}

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
  contentIdea: '',
  tags: '',
  hashtags: '',
  script: '',
  teamNotes: '',
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

// Pre-production analysis state
const isAnalyzing = ref(false)
const analysisResults = ref(null)
const titleSource = ref('user') // 'user', 'ai', or 'mixed'
const descriptionSource = ref('user')
const tagsSource = ref('user')

// Initialize form with content data when editing
const initializeForm = () => {
  if (props.content) {
    console.log('🔥 Initializing form with content:', props.content)
    form.value = {
      title: props.content.title || '',
      description: props.content.description || '',
      status: props.content.status || 'ideas',
      priority: props.content.priority || 'medium',
      pillarId: props.content.pillar?.id || '',
      contentIdea: props.content.contentIdea || '',
      tags: props.content.tags || '',
      hashtags: props.content.hashtags || '',
      script: props.content.script || '',
      teamNotes: props.content.teamNotes || '',
      stageDueDates: props.content.stageDueDates || {
        ideas: '',
        planning: '',
        'in-progress': '',
        published: ''
      },
      stageCompletions: props.content.stageCompletions || {
        ideas: false,
        planning: false,
        'in-progress': false,
        published: false
      }
    }
  } else {
    console.log('🔥 Creating new content - using default form values')
  }
}

// Initialize form when component mounts
onMounted(() => {
  initializeForm()
})

// Watch for changes to content prop (in case it changes after mount)
watch(() => props.content, () => {
  initializeForm()
}, { immediate: true })



// Title suggestions state
const titleSuggestions = ref([])
const showTitleSuggestions = ref(false)

// AI Generation Functions
const generateTitle = async () => {
  if (isGenerating.value) return

  isGenerating.value = true
  try {
    const { $api } = useNuxtApp()
    const pillar = availablePillars.value.find(p => p.id === form.value.pillarId)
    const pillarName = pillar?.name || 'General'

    // Get topic from content idea, existing title, or use pillar name
    const topic = form.value.contentIdea || form.value.title || pillarName

    // Call backend AI service for title generation
    const response = await $api('/api/content/generate-title', {
      method: 'POST',
      body: {
        topic,
        contentIdea: form.value.contentIdea,
        pillar: pillarName,
        agent_id: selectedAgent.value.id,
        count: 5
      }
    })

    if (response.status === 'success' && response.data.titles) {
      titleSuggestions.value = response.data.titles
      showTitleSuggestions.value = true
    } else {
      // Fallback to template-based generation
      let suggestions = []

      if (pillar?.name === 'Game Development') {
        suggestions = [
          '5 Game Development Tips That Actually Work in 2024',
          'Complete Beginner\'s Guide to Game Development',
          'How to Build Your First Game in 30 Days',
          'Game Development Mistakes Every Beginner Makes',
          'From Idea to Launch: Game Development Roadmap'
        ]
      } else if (pillar?.name === 'Game Reviews') {
        suggestions = [
          'Honest Review: Is This Game Worth Your Time?',
          'Top 10 Hidden Gems You Need to Play',
          'Game Review: What They Don\'t Tell You',
          'Complete Analysis: Graphics vs Gameplay',
          'Why This Game Failed (And What We Can Learn)'
        ]
      } else if (pillar?.name === 'Tech Tutorials') {
        suggestions = [
          'Complete Guide to Technology for Beginners',
          'Step-by-Step Tutorial: Master Skills in 2024',
          'Tech Tutorial: From Zero to Pro',
          'How to Learn Technology Fast (Proven Method)',
          'Advanced Techniques Explained'
        ]
      } else if (pillar?.name === 'Productivity Tips') {
        suggestions = [
          'Productivity Hacks That Will Transform Your Workflow',
          '10 Productivity Tips That Actually Work',
          'How to 10x Your Productivity in 2024',
          'Productivity System That Changed My Life',
          'Time Management Secrets of Successful People'
        ]
      } else {
        suggestions = [
          'How to Create Engaging Content That Converts',
          'Content Creation Strategy That Works',
          'From Zero to Viral: Content Creation Guide',
          'Content Creator\'s Complete Playbook',
          'How to Build an Audience Through Content'
        ]
      }

      titleSuggestions.value = suggestions
      showTitleSuggestions.value = true
    }
  } catch (error) {
    console.error('Failed to generate title:', error)
    // Fallback to template-based generation on error
    const pillar = availablePillars.value.find(p => p.id === form.value.pillarId)

    const suggestions = [
      'How to Master Your Topic in 30 Days',
      'The Ultimate Guide to Your Topic',
      'Top 10 Tips for Beginners',
      'Why Everyone is Wrong About This',
      'The Secret to Success'
    ]

    titleSuggestions.value = suggestions
    showTitleSuggestions.value = true
  } finally {
    isGenerating.value = false
  }
}

// Select a title suggestion
const selectTitleSuggestion = (title) => {
  form.value.title = title
  showTitleSuggestions.value = false
}

const generateDescription = async () => {
  if (isGenerating.value) return

  isGenerating.value = true
  try {
    const { $api } = useNuxtApp()
    const pillar = availablePillars.value.find(p => p.id === form.value.pillarId)
    const pillarName = pillar?.name || 'General'
    const title = form.value.title || 'Your Content'

    // Call backend AI service for description generation
    const response = await $api('/api/content/generate-description', {
      method: 'POST',
      body: {
        title,
        pillar: pillarName,
        agent_id: selectedAgent.value.id,
        keywords: []
      }
    })

    if (response.status === 'success' && response.data.description) {
      form.value.description = response.data.description
    } else {
      // Fallback to template-based generation
      const agent = selectedAgent.value
      let generatedDescription = ''

      if (agent.name === 'Levi') {
        generatedDescription = 'A comprehensive guide that breaks down proven strategies and actionable tactics. Perfect for creators looking to level up their content game with data-driven insights and creative approaches.'
      } else {
        generatedDescription = 'An in-depth analysis covering everything you need to know, with practical examples and step-by-step instructions to help you achieve your goals.'
      }

      form.value.description = generatedDescription
    }
  } catch (error) {
    console.error('Failed to generate description:', error)
    // Fallback to template-based generation on error
    const agent = selectedAgent.value
    let generatedDescription = ''

    if (agent.name === 'Levi') {
      generatedDescription = 'A comprehensive guide that breaks down proven strategies and actionable tactics. Perfect for creators looking to level up their content game with data-driven insights and creative approaches.'
    } else {
      generatedDescription = 'An in-depth analysis covering everything you need to know, with practical examples and step-by-step instructions to help you achieve your goals.'
    }

    form.value.description = generatedDescription
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

// Performance Prediction Methods for Existing Content
const getContentConfidence = () => {
  if (!props.content) return 85

  const priority = form.value.priority || props.content.priority
  const pillar = availablePillars.value.find(p => p.id === form.value.pillarId) || props.content.pillar

  let confidence = 75
  if (priority === 'high') confidence += 15
  if (priority === 'urgent') confidence += 10
  if (pillar?.name === 'Marketing') confidence += 10
  if (pillar?.name === 'Game Development') confidence += 5

  return Math.min(confidence, 95)
}

const getContentPredictedViews = () => {
  if (!props.content) return '5.0K - 12.0K'

  const priority = form.value.priority || props.content.priority
  const pillar = availablePillars.value.find(p => p.id === form.value.pillarId) || props.content.pillar

  let baseMin = 3000, baseMax = 8000

  if (priority === 'high') { baseMin += 3000; baseMax += 7000 }
  if (priority === 'urgent') { baseMin += 2000; baseMax += 5000 }
  if (pillar?.name === 'Marketing') { baseMin += 2000; baseMax += 6000 }
  if (pillar?.name === 'Game Development') { baseMin += 1000; baseMax += 3000 }

  const formatNum = (num) => num >= 1000 ? (num/1000).toFixed(1) + 'K' : num.toString()
  return `${formatNum(baseMin)} - ${formatNum(baseMax)}`
}

const getContentPredictedEngagement = () => {
  if (!props.content) return '3.5'

  const priority = form.value.priority || props.content.priority
  const pillar = availablePillars.value.find(p => p.id === form.value.pillarId) || props.content.pillar

  let engagement = 3.2
  if (priority === 'high') engagement += 1.0
  if (priority === 'urgent') engagement += 0.8
  if (pillar?.name === 'Marketing') engagement += 0.6
  if (pillar?.name === 'Game Development') engagement += 0.4

  return Math.min(engagement, 6.5).toFixed(1)
}

const getContentBestTime = () => {
  const pillar = availablePillars.value.find(p => p.id === form.value.pillarId) || props.content?.pillar

  if (pillar?.name === 'Marketing') return '2:00 PM PST'
  if (pillar?.name === 'Game Development') return '6:00 PM PST'
  if (pillar?.name === 'Tech Tutorials') return '10:00 AM PST'
  return '3:00 PM PST'
}

const getContentCompletionDate = () => {
  const status = form.value.status || props.content?.status
  const priority = form.value.priority || props.content?.priority

  let daysToAdd = 7
  if (status === 'planning') daysToAdd = 5
  if (status === 'in-progress') daysToAdd = 3
  if (priority === 'high') daysToAdd -= 2
  if (priority === 'urgent') daysToAdd -= 3

  const date = new Date()
  date.setDate(date.getDate() + Math.max(daysToAdd, 1))
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const getContentOptimizationTips = () => {
  const pillar = availablePillars.value.find(p => p.id === form.value.pillarId) || props.content?.pillar
  const priority = form.value.priority || props.content?.priority

  const tips = []

  if (pillar?.name === 'Marketing') {
    tips.push({
      id: 'marketing-tip',
      icon: '📈',
      title: 'Add trending hashtags',
      description: 'Marketing content performs 40% better with trending hashtags'
    })
  }

  if (priority === 'high' || priority === 'urgent') {
    tips.push({
      id: 'priority-tip',
      icon: '⚡',
      title: 'Fast-track production',
      description: 'High priority content should be published within 3 days'
    })
  }

  tips.push({
    id: 'engagement-tip',
    icon: '💬',
    title: 'Add call-to-action',
    description: 'Content with clear CTAs get 25% more engagement'
  })

  return tips.slice(0, 3)
}

const applySuggestion = (suggestion) => {
  switch (suggestion.action) {
    case 'apply-trending':
      if (suggestion.contentData) {
        form.value.title = suggestion.contentData.title
        form.value.description = suggestion.contentData.description
        form.value.priority = suggestion.contentData.priority
      }
      break
    case 'set-timing':
      // This would set optimal publishing time in a future enhancement
      alert('Optimal timing applied! This would set the best publishing schedule.')
      break
    case 'apply-hook':
      if (suggestion.contentData) {
        form.value.title = suggestion.contentData.title
        form.value.description = suggestion.contentData.description
      }
      break
  }
}

// New functions for saving suggestions as content or tasks
const selectSuggestion = (suggestion) => {
  console.log('🔥 Selected suggestion:', suggestion)
  // This could show a preview or more details about the suggestion
}

const saveAsContent = (suggestion) => {
  console.log('🔥 Saving suggestion as content:', suggestion)

  try {
    if (suggestion.contentData) {
      // Close current modal first
      emit('close')

      // Open new content modal with suggestion data
      setTimeout(() => {
        openContent(suggestion.contentData)
      }, 100)
    } else {
      // Create basic content from suggestion
      const contentData = {
        title: suggestion.title,
        description: suggestion.description,
        status: 'ideas',
        priority: 'medium'
      }

      emit('close')
      setTimeout(() => {
        openContent(contentData)
      }, 100)
    }
  } catch (error) {
    console.error('🔥 Error in saveAsContent:', error)
  }
}

const saveAsTask = (suggestion) => {
  console.log('🔥 Saving suggestion as task:', suggestion)

  try {
    if (suggestion.taskData) {
      // Close current modal first
      emit('close')

      // Open task modal with suggestion data
      setTimeout(() => {
        openTask(suggestion.taskData)
      }, 100)
    } else {
      // Create basic task from suggestion
      const taskData = {
        title: suggestion.title,
        description: suggestion.description,
        priority: 'medium',
        dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] // 1 week from now
      }

      emit('close')
      setTimeout(() => {
        openTask(taskData)
      }, 100)
    }
  } catch (error) {
    console.error('🔥 Error in saveAsTask:', error)
  }
}

const applyTemplate = (template) => {
  form.value.title = template.template.title
  form.value.description = template.template.description
}

// Trending Keywords Event Handlers
const handleKeywordSelected = (keyword) => {
  console.log('🔥 Keyword selected:', keyword.term)

  // Auto-populate title with keyword if title is empty
  if (!form.value.title.trim()) {
    form.value.title = `How to ${keyword.term}`
  }

  // Add keyword to description if description is empty
  if (!form.value.description.trim()) {
    form.value.description = `Learn everything about ${keyword.term} in this comprehensive guide. This trending topic has ${keyword.searchVolume} searches and is growing by ${keyword.growth}%.`
  }

  // Add keyword to tags if tags field exists
  if (form.value.tags !== undefined) {
    const currentTags = form.value.tags ? form.value.tags.split(',').map(t => t.trim()).filter(t => t) : []
    if (!currentTags.includes(keyword.term)) {
      currentTags.push(keyword.term)
      form.value.tags = currentTags.join(', ')
    }
  }
}

const handleContentIdeaSelected = ({ keyword, idea }) => {
  console.log('🔥 Content idea selected:', idea)

  // Handle both string and object idea formats
  const title = typeof idea === 'string' ? idea : idea.title
  const reasoning = typeof idea === 'object' ? idea.reasoning : `Strategic content leveraging trending topic "${keyword.term}"`

  // Use the specific content idea as the title
  form.value.title = title

  // Create a comprehensive description with AI reasoning
  let description = `${reasoning}\n\n`
  description += `📊 STRATEGIC CONTEXT:\n`
  description += `• Trending topic: "${keyword.term}" (${keyword.searchVolume} searches, +${keyword.growth}% growth)\n`
  description += `• Competition level: ${keyword.competitionLevel}\n`
  description += `• Expected performance: ${keyword.expectedViews} views\n`
  description += `• Best upload time: ${keyword.bestUploadTime}\n\n`

  if (typeof idea === 'object') {
    description += `🎯 CONTENT STRATEGY:\n`
    if (idea.hooks?.length) {
      description += `• Hook: "${idea.hooks[0]}"\n`
    }
    if (idea.keyPoints?.length) {
      description += `• Key points to cover:\n`
      idea.keyPoints.forEach(point => {
        description += `  - ${point}\n`
      })
    }
    if (idea.estimatedPerformance) {
      description += `• Expected performance: ${idea.estimatedPerformance}\n`
    }
    description += `\n`
  }

  if (keyword.strategicInsights) {
    description += `💡 AUDIENCE INSIGHTS:\n`
    description += `• Target audience: ${keyword.strategicInsights.audienceIntent}\n`
    description += `• Market gap: ${keyword.strategicInsights.competitorGaps}\n`
    description += `• Monetization potential: ${keyword.strategicInsights.monetizationPotential}\n`

    if (keyword.strategicInsights.trendingSubtopics?.length) {
      description += `• Related trending topics: ${keyword.strategicInsights.trendingSubtopics.join(', ')}\n`
    }
  }

  form.value.description = description

  // Add keyword and related tags
  if (form.value.tags !== undefined) {
    const currentTags = form.value.tags ? form.value.tags.split(',').map(t => t.trim()).filter(t => t) : []

    // Add main keyword
    if (!currentTags.includes(keyword.term)) {
      currentTags.push(keyword.term)
    }

    // Add related trending subtopics as tags
    if (keyword.strategicInsights?.trendingSubtopics) {
      keyword.strategicInsights.trendingSubtopics.forEach(subtopic => {
        if (!currentTags.includes(subtopic)) {
          currentTags.push(subtopic)
        }
      })
    }

    form.value.tags = currentTags.slice(0, 10).join(', ') // Limit to 10 tags
  }
}

const handleGenerateIdeas = (keywords) => {
  console.log('🔥 Generating content ideas from keywords:', keywords)
  // This could trigger AI generation based on trending keywords
  // For now, we'll show a simple notification
  alert('Content ideas will be generated based on trending keywords!')
}

const handleAnalyzeCompetitors = (keywords) => {
  console.log('🔥 Analyzing competitors for keywords:', keywords)
  // This could open a competitor analysis modal or section
  alert('Competitor analysis feature coming soon!')
}

// Pre-production analysis functions
const runPreProductionAnalysis = async () => {
  if (isAnalyzing.value) return

  isAnalyzing.value = true
  try {
    const pillar = availablePillars.value.find(p => p.id === form.value.pillarId)
    const { post } = useApi()

    // Call the automation workflow we built using proper API composable
    const response = await post('/api/workflows/pre-production-analysis', {
      description: form.value.description,
      contentIdea: form.value.contentIdea || form.value.description,
      pillar: pillar?.name || 'General',
      pillarId: form.value.pillarId
    }, {
      showLoading: true,
      loadingKey: 'pre-production-analysis'
    })

    if (response.status === 'success') {
      analysisResults.value = response.data
      // Show success message
      console.log('🎯 Pre-production analysis complete:', analysisResults.value)
    } else {
      throw new Error(response.error || 'Analysis failed')
    }

  } catch (error) {
    console.error('Error running pre-production analysis:', error)
    alert('Error running analysis. Please try again.')
  } finally {
    isAnalyzing.value = false
  }
}

const clearAnalysis = () => {
  analysisResults.value = null
}

// Individual suggestion application functions
const applySEOSuggestions = () => {
  if (analysisResults.value?.seo?.optimizedTitle) {
    form.value.title = analysisResults.value.seo.optimizedTitle
    titleSource.value = 'ai'
  }
  if (analysisResults.value?.seo?.optimizedTags) {
    form.value.tags = analysisResults.value.seo.optimizedTags
    tagsSource.value = 'ai'
  }
  if (analysisResults.value?.seo?.optimizedDescription) {
    form.value.description = analysisResults.value.seo.optimizedDescription
    descriptionSource.value = 'ai'
  }
}

const applyCompetitiveInsights = () => {
  if (analysisResults.value?.competitive?.differentiationTips) {
    // Add competitive insights to description or team notes
    const insights = analysisResults.value.competitive.differentiationTips
    form.value.teamNotes = form.value.teamNotes ?
      `${form.value.teamNotes}\n\nCompetitive Insights:\n${insights}` :
      `Competitive Insights:\n${insights}`
  }
}

const applyAudienceInsights = () => {
  if (analysisResults.value?.audience?.contentStructure) {
    const structure = analysisResults.value.audience.contentStructure
    form.value.teamNotes = form.value.teamNotes ?
      `${form.value.teamNotes}\n\nAudience-Optimized Structure:\n${structure}` :
      `Audience-Optimized Structure:\n${structure}`
  }
}

const applyMonetizationTips = () => {
  if (analysisResults.value?.monetization?.integrationTips) {
    const tips = analysisResults.value.monetization.integrationTips
    form.value.teamNotes = form.value.teamNotes ?
      `${form.value.teamNotes}\n\nMonetization Strategy:\n${tips}` :
      `Monetization Strategy:\n${tips}`
  }
}

const applyAllSuggestions = () => {
  applySEOSuggestions()
  applyCompetitiveInsights()
  applyAudienceInsights()
  applyMonetizationTips()
  alert('All AI suggestions have been applied! You can still edit any field as needed.')
}

const selectiveSuggestions = () => {
  // This could open a detailed modal for selective application
  alert('Selective suggestions feature - choose which specific recommendations to apply.')
}

const ignoreAllSuggestions = () => {
  analysisResults.value = null
  alert('Continuing with manual content creation. You can run analysis again anytime.')
}

// Track when user manually edits fields
const onTitleChange = () => {
  if (titleSource.value === 'ai') {
    titleSource.value = 'mixed'
  } else if (!form.value.title) {
    titleSource.value = 'user'
  }
}

const onDescriptionChange = () => {
  if (descriptionSource.value === 'ai') {
    descriptionSource.value = 'mixed'
  } else if (!form.value.description) {
    descriptionSource.value = 'user'
  }
}

const onTagsChange = () => {
  if (tagsSource.value === 'ai') {
    tagsSource.value = 'mixed'
  } else if (!form.value.tags) {
    tagsSource.value = 'user'
  }
}

// Detail view functions (placeholder for future enhancement)
const viewSEODetails = () => alert('Detailed SEO analysis coming soon!')
const viewCompetitiveDetails = () => alert('Detailed competitive analysis coming soon!')
const viewAudienceDetails = () => alert('Detailed audience insights coming soon!')
const viewMonetizationDetails = () => alert('Detailed monetization strategy coming soon!')

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
    contentIdea: form.value.contentIdea.trim(),
    status: form.value.status,
    priority: form.value.priority,
    pillar: selectedPillar,
    tags: form.value.tags.trim(),
    hashtags: form.value.hashtags.trim(),
    script: form.value.script.trim(),
    teamNotes: form.value.teamNotes.trim(),
    stageDueDates: form.value.stageDueDates,
    stageCompletions: form.value.stageCompletions,
    createdAt: props.content?.createdAt || new Date().toISOString(),
    dueDate: form.value.stageDueDates.published || new Date().toISOString(),
    // Track AI assistance usage
    aiAssisted: analysisResults.value ? true : false,
    aiSuggestions: analysisResults.value || null
  }

  emit('save', contentData)
}
</script>
