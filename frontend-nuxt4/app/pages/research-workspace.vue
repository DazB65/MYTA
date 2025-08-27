<template>
  <div class="min-h-screen bg-forest-900 text-white">
    <!-- Main Content Area -->
    <div class="p-6 pt-24">
      <!-- Header -->
      <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <h1 class="text-2xl font-bold text-white">Research Workspace</h1>
          <span class="text-gray-400">•</span>
          <p class="text-gray-400">Visual research and competitor analysis for YouTube success</p>
        </div>
        <div class="flex items-center space-x-3">
          <button
            class="flex items-center space-x-2 rounded-lg bg-blue-500 px-4 py-2 text-white transition-colors hover:bg-blue-600"
            @click="showProTips = true"
          >
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
            </svg>
            <span>Pro Tips</span>
          </button>
          <button
            class="flex items-center space-x-2 rounded-lg bg-forest-700 px-4 py-2 text-white transition-colors hover:bg-forest-600"
            @click="showTemplates = true"
          >
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z"/>
            </svg>
            <span>Templates</span>
          </button>
          <button
            class="flex items-center space-x-2 rounded-lg bg-forest-700 px-4 py-2 text-white transition-colors hover:bg-forest-600"
            @click="showSavedProjects = true"
          >
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/>
            </svg>
            <span>Saved Projects</span>
          </button>
          <button
            class="flex items-center space-x-2 rounded-lg bg-orange-500 px-4 py-2 text-white transition-colors hover:bg-orange-600"
            @click="saveProject"
          >
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M7.707 10.293a1 1 0 10-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 11.586V6h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V8a2 2 0 012-2h5v5.586l-1.293-1.293zM9 4a1 1 0 012 0v2H9V4z"/>
            </svg>
            <span>Save Project</span>
          </button>
        </div>
      </div>

      <!-- Main Workspace Layout -->
      <div class="grid grid-cols-12 gap-6 h-[calc(100vh-200px)]">
        <!-- Left Sidebar - Tools & Agents -->
        <div class="col-span-3 space-y-6">
          <!-- Research Tools -->
          <div class="rounded-lg bg-forest-800 p-4">
            <h3 class="mb-4 text-lg font-semibold text-white">Research Tools</h3>
            <div class="grid grid-cols-2 gap-3">
              <div
                class="flex flex-col items-center space-y-2 rounded-lg bg-forest-700 p-3 text-center transition-colors hover:bg-forest-600 cursor-pointer"
                @click="openVideoAnalyzer"
              >
                <svg class="h-6 w-6 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"/>
                </svg>
                <span class="text-sm font-medium text-white">Video Analyzer</span>
              </div>
              <div
                class="flex flex-col items-center space-y-2 rounded-lg bg-forest-700 p-3 text-center transition-colors hover:bg-forest-600 cursor-pointer"
                @click="openCompetitorTracker"
              >
                <svg class="h-6 w-6 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
                </svg>
                <span class="text-sm font-medium text-white">Competitor Tracker</span>
              </div>
              <div
                class="flex flex-col items-center space-y-2 rounded-lg bg-forest-700 p-3 text-center transition-colors hover:bg-forest-600 cursor-pointer"
                @click="openTrendScout"
              >
                <svg class="h-6 w-6 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clip-rule="evenodd"/>
                </svg>
                <span class="text-sm font-medium text-white">Trend Scout</span>
              </div>
              <div
                class="flex flex-col items-center space-y-2 rounded-lg bg-forest-700 p-3 text-center transition-colors hover:bg-forest-600 cursor-pointer"
                @click="openKeywordResearch"
              >
                <svg class="h-6 w-6 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
                </svg>
                <span class="text-sm font-medium text-white">Keyword Research</span>
              </div>
            </div>
          </div>

          <!-- Specialized AI Agents -->
          <div class="rounded-lg bg-forest-800 p-4">
            <h3 class="mb-4 text-lg font-semibold text-white">AI Research Agents</h3>
            <div class="space-y-3">
              <div
                v-for="agent in researchAgents"
                :key="agent.id"
                class="flex items-center space-x-3 rounded-lg bg-forest-700 p-3 transition-colors hover:bg-forest-600 cursor-pointer"
                :class="{ 'ring-2 ring-orange-500': selectedAgent?.id === agent.id }"
                @click="selectAgent(agent)"
              >
                <div class="h-10 w-10 rounded-lg bg-orange-500 flex items-center justify-center">
                  <img :src="agent.avatar" :alt="agent.name" class="h-8 w-8 rounded-lg object-cover" />
                </div>
                <div class="flex-1">
                  <h4 class="font-medium text-white">{{ agent.name }}</h4>
                  <p class="text-sm text-gray-400">{{ agent.specialty }}</p>
                </div>
                <div class="h-2 w-2 rounded-full" :class="agent.status === 'online' ? 'bg-green-400' : 'bg-gray-400'"></div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="rounded-lg bg-forest-800 p-4">
            <h3 class="mb-4 text-lg font-semibold text-white">Quick Actions</h3>
            <div class="space-y-3">
              <!-- Video URL Input -->
              <div class="space-y-2">
                <label class="text-sm font-medium text-gray-300">YouTube Video URL</label>
                <div class="flex space-x-2">
                  <input
                    v-model="videoUrl"
                    type="text"
                    placeholder="https://youtube.com/watch?v=..."
                    class="flex-1 rounded-lg bg-forest-700 border border-forest-600 px-3 py-2 text-white placeholder-gray-400 focus:border-orange-500 focus:outline-none focus:ring-1 focus:ring-orange-500"
                    @keyup.enter="analyzeVideoFromUrl"
                  />
                  <button
                    @click="analyzeVideoFromUrl"
                    :disabled="isAnalyzing || !videoUrl.trim()"
                    class="rounded-lg bg-orange-500 px-4 py-2 text-white transition-colors hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <svg v-if="isAnalyzing" class="h-4 w-4 animate-spin" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/>
                    </svg>
                    <svg v-else class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clip-rule="evenodd"/>
                    </svg>
                  </button>
                </div>
              </div>
              <button
                class="flex w-full items-center space-x-2 rounded-lg bg-forest-700 px-3 py-2 text-left transition-colors hover:bg-forest-600"
                @click="findTrendingContent"
              >
                <svg class="h-4 w-4 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clip-rule="evenodd"/>
                </svg>
                <span class="text-sm font-medium text-white">Find Trending Content</span>
              </button>
              <button
                class="flex w-full items-center space-x-2 rounded-lg bg-forest-700 px-3 py-2 text-left transition-colors hover:bg-forest-600"
                @click="exportToContentStudio"
              >
                <svg class="h-4 w-4 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
                <span class="text-sm font-medium text-white">Export to Content Studio</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Main Canvas Area -->
        <div class="col-span-6">
          <div class="rounded-lg bg-forest-800 p-4 h-full relative overflow-hidden">
            <!-- Canvas Background -->
            <div class="absolute inset-0 bg-forest-700 rounded-lg">
              <div class="w-full h-full opacity-10" style="background-image: radial-gradient(circle, #fff 1px, transparent 1px); background-size: 20px 20px;"></div>
            </div>

            <!-- Research Items -->
            <div class="relative z-10 h-full">
              <!-- Empty State -->
              <div class="flex items-center justify-center h-full text-center" v-if="!researchVideos.length && !researchNotes.length">
                <div>
                  <svg class="h-16 w-16 mx-auto mb-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h4a1 1 0 010 2H6.414l2.293 2.293a1 1 0 01-1.414 1.414L5 6.414V8a1 1 0 01-2 0V4zm9 1a1 1 0 010-2h4a1 1 0 011 1v4a1 1 0 01-2 0V6.414l-2.293 2.293a1 1 0 11-1.414-1.414L13.586 5H12zm-9 7a1 1 0 012 0v1.586l2.293-2.293a1 1 0 111.414 1.414L6.414 15H8a1 1 0 010 2H4a1 1 0 01-1-1v-4zm13-1a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 010-2h1.586l-2.293-2.293a1 1 0 111.414-1.414L15 13.586V12a1 1 0 011-1z" clip-rule="evenodd"/>
                  </svg>
                  <h3 class="text-xl font-semibold text-white mb-2">Start Your Research</h3>
                  <p class="text-gray-400 mb-6">Use the tools on the left to begin analyzing videos and trends</p>
                  <button
                    class="rounded-lg bg-orange-500 px-4 py-2 text-white transition-colors hover:bg-orange-600"
                    @click="openVideoAnalyzer"
                  >
                    Analyze Your First Video
                  </button>
                </div>
              </div>

              <!-- Research Content -->
              <div v-else class="h-full">
                <ResearchVideoCard
                  v-for="video in researchVideos"
                  :key="video.id"
                  :video="video"
                  :position="video.position"
                  @move="updateVideoPosition"
                  @analyze="analyzeVideo"
                  @remove="removeVideo"
                />

                <ResearchNoteCard
                  v-for="note in researchNotes"
                  :key="note.id"
                  :note="note"
                  :position="note.position"
                  @move="updateNotePosition"
                  @edit="editNote"
                  @remove="removeNote"
                />

                <ConnectionLine
                  v-for="connection in connections"
                  :key="connection.id"
                  :connection="connection"
                  @remove="removeConnection"
                />

                <!-- Floating Add Note Button -->
                <button
                  @click="addNewNote"
                  class="absolute bottom-4 right-4 h-12 w-12 rounded-full bg-orange-500 text-white shadow-lg hover:bg-orange-600 transition-colors flex items-center justify-center"
                  title="Add Note"
                >
                  <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Canvas Controls -->
            <div class="absolute top-4 right-4 flex flex-col space-y-2">
              <button
                class="flex h-10 w-10 items-center justify-center rounded-lg bg-forest-700 text-white transition-colors hover:bg-forest-600"
                @click="zoomIn"
              >
                <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
                  <path d="M8 6a1 1 0 011 1v1h1a1 1 0 110 2H9v1a1 1 0 11-2 0V10H6a1 1 0 110-2h1V7a1 1 0 011-1z"/>
                </svg>
              </button>
              <button
                class="flex h-10 w-10 items-center justify-center rounded-lg bg-forest-700 text-white transition-colors hover:bg-forest-600"
                @click="zoomOut"
              >
                <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
                  <path d="M6 8a1 1 0 011-1h2a1 1 0 110 2H7a1 1 0 01-1-1z"/>
                </svg>
              </button>
              <button
                class="flex h-10 w-10 items-center justify-center rounded-lg bg-forest-700 text-white transition-colors hover:bg-forest-600"
                @click="resetZoom"
              >
                <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/>
                </svg>
              </button>
              <button
                class="flex h-10 w-10 items-center justify-center rounded-lg bg-forest-700 text-white transition-colors hover:bg-forest-600"
                @click="fitToScreen"
              >
                <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h4a1 1 0 010 2H6.414l2.293 2.293a1 1 0 01-1.414 1.414L5 6.414V8a1 1 0 01-2 0V4zm9 1a1 1 0 010-2h4a1 1 0 011 1v4a1 1 0 01-2 0V6.414l-2.293 2.293a1 1 0 11-1.414-1.414L13.586 5H12zm-9 7a1 1 0 012 0v1.586l2.293-2.293a1 1 0 111.414 1.414L6.414 15H8a1 1 0 010 2H4a1 1 0 01-1-1v-4zm13-1a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 010-2h1.586l-2.293-2.293a1 1 0 111.414-1.414L15 13.586V12a1 1 0 011-1z" clip-rule="evenodd"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Right Panel - Analysis & Insights -->
        <div class="col-span-3 space-y-6">
          <!-- Agent Chat -->
          <div class="rounded-lg bg-forest-800 p-4" v-if="selectedAgent">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-lg font-semibold text-white">{{ selectedAgent.name }} Insights</h3>
              <button
                class="rounded-lg bg-forest-700 p-2 text-white transition-colors hover:bg-forest-600"
                @click="clearChat"
              >
                <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"/>
                </svg>
              </button>
            </div>
            <div class="flex flex-col h-80">
              <div class="flex-1 space-y-2 overflow-y-auto mb-4">
                <div
                  v-for="message in agentMessages"
                  :key="message.id"
                  class="rounded-lg p-3"
                  :class="message.type === 'user' ? 'bg-orange-500/20 ml-4' : 'bg-forest-700 mr-4'"
                >
                  <div class="text-sm text-white">{{ message.content }}</div>
                  <div class="text-xs text-gray-400 mt-1">{{ formatTime(message.timestamp) }}</div>
                </div>
              </div>
              <div class="flex space-x-2">
                <input
                  v-model="chatInput"
                  @keyup.enter="sendMessage"
                  placeholder="Ask your research agent..."
                  class="flex-1 rounded-lg bg-forest-700 px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
                <button
                  @click="sendMessage"
                  class="rounded-lg bg-orange-500 px-4 py-2 text-white transition-colors hover:bg-orange-600"
                >
                  <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Research Insights -->
          <div class="rounded-lg bg-forest-800 p-4">
            <h3 class="mb-4 text-lg font-semibold text-white">Research Insights</h3>
            <div class="space-y-3">
              <div
                v-for="insight in researchInsights"
                :key="insight.id"
                class="rounded-lg bg-forest-700 p-3"
              >
                <div class="mb-2 flex items-center space-x-2">
                  <svg class="h-4 w-4 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/>
                  </svg>
                  <span class="font-medium text-white">{{ insight.title }}</span>
                </div>
                <p class="text-sm text-gray-400 mb-3">{{ insight.description }}</p>
                <button
                  class="rounded-lg bg-forest-600 px-3 py-1 text-sm text-white transition-colors hover:bg-forest-500"
                  @click="addToCanvas(insight)"
                >
                  Add to Canvas
                </button>
              </div>
            </div>
          </div>

          <!-- Trending Topics -->
          <div class="rounded-lg bg-forest-800 p-4">
            <h3 class="mb-4 text-lg font-semibold text-white">Trending in Your Niche</h3>
            <div class="space-y-3">
              <div
                v-for="trend in trendingTopics"
                :key="trend.id"
                class="flex items-center justify-between rounded-lg bg-forest-700 p-3"
              >
                <div>
                  <span class="font-medium text-white">{{ trend.title }}</span>
                  <span class="ml-2 rounded-full bg-green-500/20 px-2 py-1 text-xs font-semibold text-green-400">+{{ trend.growth }}%</span>
                </div>
                <button
                  class="rounded-lg bg-orange-500 px-3 py-1 text-sm text-white transition-colors hover:bg-orange-600"
                  @click="researchTrend(trend)"
                >
                  Research
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <VideoAnalyzerModal
      :show="showVideoAnalyzer"
      @close="showVideoAnalyzer = false"
      @addToCanvas="addVideoToCanvas"
    />

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
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ProTipsModal from '../../components/research/ProTipsModal.vue'
import TemplatesModal from '../../components/research/TemplatesModal.vue'
import VideoAnalyzerModal from '../../components/research/VideoAnalyzerModal.vue'

// Mock data for research agents
const researchAgents = ref([
  {
    id: 1,
    name: 'Algorithm Whisperer',
    specialty: 'YouTube Algorithm Expert',
    avatar: '/agents/agent-1.png',
    status: 'online'
  },
  {
    id: 2,
    name: 'Thumbnail Genius',
    specialty: 'Visual Design & CTR Expert',
    avatar: '/agents/agent-2.png',
    status: 'online'
  },
  {
    id: 3,
    name: 'Title Master',
    specialty: 'Title Optimization & Psychology',
    avatar: '/agents/agent-3.png',
    status: 'online'
  },
  {
    id: 4,
    name: 'Trend Scout',
    specialty: 'Competitor & Trend Analysis',
    avatar: '/agents/agent-4.png',
    status: 'online'
  },
  {
    id: 5,
    name: 'Growth Strategist',
    specialty: 'Channel Growth & Audience Development',
    avatar: '/agents/agent-5.png',
    status: 'online'
  }
])

// Mock data for insights and trends
const researchInsights = ref([
  {
    id: 1,
    type: 'trending',
    title: 'Trending Topic Alert',
    description: 'AI productivity tools are gaining 45% more views this week'
  },
  {
    id: 2,
    type: 'competitor',
    title: 'Competitor Analysis',
    description: 'Top competitor uploaded 3 videos in your niche this week'
  }
])



// Reactive state
const selectedAgent = ref(null)
const agentMessages = ref([])
const researchVideos = ref([])
const researchNotes = ref([])
const connections = ref([])
const showVideoAnalyzer = ref(false)
const showCompetitorTracker = ref(false)
const showTrendScout = ref(false)
const showTemplates = ref(false)
const showSavedProjects = ref(false)
const showProTips = ref(false)
const chatInput = ref('')
const canvasContainer = ref(null)
const videoUrl = ref('')
const isAnalyzing = ref(false)
const currentProject = ref(null)
const trendingTopics = ref([
  { id: 1, title: 'AI Content Creation', growth: 45, category: 'Technology' },
  { id: 2, title: 'YouTube Shorts Strategy', growth: 32, category: 'Marketing' },
  { id: 3, title: 'Creator Economy 2024', growth: 28, category: 'Business' },
  { id: 4, title: 'Video SEO Tips', growth: 25, category: 'SEO' },
  { id: 5, title: 'Monetization Strategies', growth: 22, category: 'Business' }
])

// Methods
const selectAgent = (agent) => {
  selectedAgent.value = agent
  agentMessages.value = [
    {
      id: 1,
      type: 'agent',
      content: `Hi! I'm ${agent.name}. How can I help you with your research today?`,
      timestamp: new Date()
    }
  ]
}

const clearChat = () => {
  agentMessages.value = []
}

const sendMessage = () => {
  if (chatInput.value.trim() && selectedAgent.value) {
    // Add user message
    agentMessages.value.push({
      id: Date.now(),
      type: 'user',
      content: chatInput.value,
      timestamp: new Date()
    })

    // Add agent response (mock)
    setTimeout(() => {
      agentMessages.value.push({
        id: Date.now() + 1,
        type: 'agent',
        content: `I understand you're asking about "${chatInput.value}". Let me analyze that for you...`,
        timestamp: new Date()
      })
    }, 1000)

    chatInput.value = ''
  }
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const openVideoAnalyzer = () => showVideoAnalyzer.value = true
const openCompetitorTracker = () => showCompetitorTracker.value = true
const openTrendScout = () => showTrendScout.value = true
const openKeywordResearch = () => console.log('Opening keyword research tool')

const analyzeVideoFromUrl = async () => {
  if (!videoUrl.value.trim()) {
    alert('Please enter a YouTube video URL')
    return
  }

  isAnalyzing.value = true

  try {
    // Extract video ID from URL
    const videoId = extractVideoId(videoUrl.value)
    if (!videoId) {
      alert('Invalid YouTube URL')
      return
    }

    // Simulate API call to get video data
    const videoData = await fetchVideoData(videoId)

    // Add video to canvas
    const newVideo = {
      id: Date.now().toString(),
      url: videoUrl.value,
      videoId: videoId,
      title: videoData.title,
      channelName: videoData.channelName,
      channelId: videoData.channelId,
      thumbnail: videoData.thumbnail,
      duration: videoData.duration,
      views: videoData.views,
      publishedAt: videoData.publishedAt,
      position: {
        x: Math.random() * 400 + 100,
        y: Math.random() * 300 + 100
      },
      addedAt: new Date(),
      analysisStatus: 'analyzing',
      analysis: null,
      metrics: null,
      tags: []
    }

    researchVideos.value.push(newVideo)

    // Simulate AI analysis
    setTimeout(async () => {
      await performVideoAnalysis(newVideo.id)
    }, 2000)

    videoUrl.value = ''

  } catch (error) {
    console.error('Error analyzing video:', error)
    alert('Error analyzing video. Please try again.')
  } finally {
    isAnalyzing.value = false
  }
}

const findTrendingContent = () => {
  // Simulate finding trending content
  const trendingVideos = [
    {
      id: Date.now().toString() + '_1',
      url: 'https://youtube.com/watch?v=trending1',
      videoId: 'trending1',
      title: 'Top 10 AI Tools for Content Creators',
      channelName: 'TechCreator',
      channelId: 'techcreator123',
      thumbnail: 'https://img.youtube.com/vi/trending1/maxresdefault.jpg',
      duration: 720,
      views: 125000,
      publishedAt: '2024-01-15',
      position: { x: 150, y: 150 },
      addedAt: new Date(),
      analysisStatus: 'pending',
      tags: ['trending', 'ai', 'tools']
    },
    {
      id: Date.now().toString() + '_2',
      url: 'https://youtube.com/watch?v=trending2',
      videoId: 'trending2',
      title: 'YouTube Algorithm Secrets Revealed',
      channelName: 'GrowthHacker',
      channelId: 'growthhacker456',
      thumbnail: 'https://img.youtube.com/vi/trending2/maxresdefault.jpg',
      duration: 540,
      views: 89000,
      publishedAt: '2024-01-14',
      position: { x: 350, y: 200 },
      addedAt: new Date(),
      analysisStatus: 'pending',
      tags: ['trending', 'algorithm', 'growth']
    }
  ]

  researchVideos.value.push(...trendingVideos)
}

const saveProject = () => {
  const project = {
    id: currentProject.value?.id || Date.now().toString(),
    name: currentProject.value?.name || 'Untitled Research Project',
    description: currentProject.value?.description || '',
    createdAt: currentProject.value?.createdAt || new Date(),
    updatedAt: new Date(),
    videos: researchVideos.value,
    notes: researchNotes.value,
    connections: connections.value,
    insights: []
  }

  // Save to localStorage for demo purposes
  const savedProjects = JSON.parse(localStorage.getItem('researchProjects') || '[]')
  const existingIndex = savedProjects.findIndex(p => p.id === project.id)

  if (existingIndex >= 0) {
    savedProjects[existingIndex] = project
  } else {
    savedProjects.push(project)
  }

  localStorage.setItem('researchProjects', JSON.stringify(savedProjects))
  currentProject.value = project

  alert('Project saved successfully!')
}

const exportToContentStudio = () => {
  const exportData = {
    videos: researchVideos.value.filter(v => v.analysis),
    insights: researchVideos.value.flatMap(v => v.analysis?.keyInsights || []),
    notes: researchNotes.value,
    exportedAt: new Date()
  }

  // Save export data for content studio
  localStorage.setItem('researchExport', JSON.stringify(exportData))

  // Navigate to content studio
  navigateTo('/content-studio?imported=true')
}

const addToCanvas = (insight) => {
  const note = {
    id: Date.now().toString(),
    content: insight.text || insight.title || 'New insight',
    position: {
      x: Math.random() * 400 + 100,
      y: Math.random() * 300 + 100
    },
    createdAt: new Date(),
    color: '#FEF3C7'
  }
  researchNotes.value.push(note)
}

const researchTrend = async (trend) => {
  try {
    // Simulate researching a trend and finding related videos
    const trendVideos = await fetchTrendVideos(trend)

    trendVideos.forEach((video, index) => {
      const newVideo = {
        ...video,
        id: Date.now().toString() + '_trend_' + index,
        position: {
          x: 200 + (index * 150),
          y: 250 + (index * 50)
        },
        addedAt: new Date(),
        analysisStatus: 'pending',
        tags: [...(video.tags || []), 'trend', trend.category.toLowerCase()]
      }
      researchVideos.value.push(newVideo)
    })

    // Add trend insight note
    addToCanvas({
      text: `Researched trend: ${trend.title} (+${trend.growth}% growth)`
    })

  } catch (error) {
    console.error('Error researching trend:', error)
    alert('Error researching trend. Please try again.')
  }
}

// Canvas methods
const updateVideoPosition = (videoId, position) => {
  const video = researchVideos.value.find(v => v.id === videoId)
  if (video) {
    video.position = position
  }
}

const updateNotePosition = (noteId, position) => {
  const note = researchNotes.value.find(n => n.id === noteId)
  if (note) {
    note.position = position
  }
}

const analyzeVideo = async (videoId) => {
  await performVideoAnalysis(videoId)
}

const removeVideo = (videoId) => {
  const index = researchVideos.value.findIndex(v => v.id === videoId)
  if (index >= 0) {
    researchVideos.value.splice(index, 1)
  }

  // Remove any connections involving this video
  connections.value = connections.value.filter(c =>
    c.fromId !== videoId && c.toId !== videoId
  )
}

const editNote = (note) => {
  const newContent = prompt('Edit note:', note.content)
  if (newContent !== null) {
    note.content = newContent
  }
}

const removeNote = (noteId) => {
  const index = researchNotes.value.findIndex(n => n.id === noteId)
  if (index >= 0) {
    researchNotes.value.splice(index, 1)
  }

  // Remove any connections involving this note
  connections.value = connections.value.filter(c =>
    c.fromId !== noteId && c.toId !== noteId
  )
}

const removeConnection = (connectionId) => {
  const index = connections.value.findIndex(c => c.id === connectionId)
  if (index >= 0) {
    connections.value.splice(index, 1)
  }
}

const addNewNote = () => {
  const content = prompt('Enter note content:')
  if (content) {
    const note = {
      id: Date.now().toString(),
      content,
      position: {
        x: Math.random() * 400 + 100,
        y: Math.random() * 300 + 100
      },
      createdAt: new Date(),
      color: '#FEF3C7'
    }
    researchNotes.value.push(note)
  }
}

const startInteractiveTour = () => {
  // Future implementation: Interactive tour of the research workspace
  alert('Interactive tour coming soon! For now, explore the features using the Pro Tips as your guide.')
}

const applyTemplate = (template) => {
  // Clear current research
  researchVideos.value = []
  researchNotes.value = []
  connections.value = []

  // Set project name based on template
  currentProject.value = {
    id: Date.now().toString(),
    name: template.name,
    description: template.goal,
    createdAt: new Date(),
    template: template.name
  }

  // Add template instructions as notes
  const instructionNote = {
    id: Date.now().toString(),
    content: `${template.name}\n\nGoal: ${template.goal}\n\nSteps:\n${template.steps.map((step, i) => `${i + 1}. ${step}`).join('\n')}`,
    position: { x: 100, y: 100 },
    createdAt: new Date(),
    color: '#DBEAFE' // Blue for template instructions
  }

  researchNotes.value.push(instructionNote)

  // Add a getting started note
  const gettingStartedNote = {
    id: (Date.now() + 1).toString(),
    content: `Getting Started:\n\n• Follow the template steps on the left\n• Use the research tools to find videos\n• Add your findings to the canvas\n• Document insights as you go`,
    position: { x: 400, y: 100 },
    createdAt: new Date(),
    color: '#FEF3C7' // Yellow for getting started
  }

  researchNotes.value.push(gettingStartedNote)

  // Show success message
  alert(`${template.name} template applied! Follow the blue instruction note to get started.`)
}

const zoomIn = () => console.log('Zooming in')
const zoomOut = () => console.log('Zooming out')
const resetZoom = () => console.log('Resetting zoom')
const fitToScreen = () => console.log('Fitting to screen')

const addVideoToCanvas = (video) => {
  const newVideo = {
    ...video,
    id: Date.now().toString(),
    position: {
      x: Math.random() * 400 + 100,
      y: Math.random() * 300 + 100
    },
    addedAt: new Date(),
    analysisStatus: 'pending'
  }
  researchVideos.value.push(newVideo)
}

const addCompetitorToCanvas = (competitor) => {
  // Add competitor as a special note or video
  const competitorNote = {
    id: Date.now().toString(),
    content: `Competitor: ${competitor.name}\nChannel: ${competitor.channel}\nSubscribers: ${competitor.subscribers}`,
    position: {
      x: Math.random() * 400 + 100,
      y: Math.random() * 300 + 100
    },
    createdAt: new Date(),
    color: '#FEE2E2' // Red for competitors
  }
  researchNotes.value.push(competitorNote)
}

const addTrendToCanvas = (trend) => {
  const trendNote = {
    id: Date.now().toString(),
    content: `Trend: ${trend.title}\nGrowth: +${trend.growth}%\nCategory: ${trend.category}`,
    position: {
      x: Math.random() * 400 + 100,
      y: Math.random() * 300 + 100
    },
    createdAt: new Date(),
    color: '#DBEAFE' // Blue for trends
  }
  researchNotes.value.push(trendNote)
}

// Helper functions
const extractVideoId = (url) => {
  const regex = /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/
  const match = url.match(regex)
  return match ? match[1] : null
}

const fetchVideoData = async (videoId) => {
  // Simulate API call - in real app this would call YouTube API
  await new Promise(resolve => setTimeout(resolve, 1000))

  return {
    title: `Sample Video Title ${videoId.slice(0, 6)}`,
    channelName: 'Sample Channel',
    channelId: 'samplechannel123',
    thumbnail: `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`,
    duration: Math.floor(Math.random() * 600) + 120, // 2-12 minutes
    views: Math.floor(Math.random() * 100000) + 1000,
    publishedAt: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
  }
}

const performVideoAnalysis = async (videoId) => {
  const video = researchVideos.value.find(v => v.id === videoId)
  if (!video) return

  video.analysisStatus = 'analyzing'

  // Simulate AI analysis
  await new Promise(resolve => setTimeout(resolve, 3000))

  const analysisResults = {
    overallScore: Math.floor(Math.random() * 40) + 60, // 60-100
    keyInsights: [
      { id: 1, type: 'engagement', text: 'High engagement rate in first 30 seconds' },
      { id: 2, type: 'content', text: 'Strong hook and clear value proposition' },
      { id: 3, type: 'seo', text: 'Well-optimized title and description' }
    ],
    tags: ['educational', 'trending', 'high-engagement'],
    sentiment: 'positive',
    topics: ['content creation', 'youtube strategy', 'growth'],
    competitorAnalysis: {
      similarChannels: ['Channel A', 'Channel B'],
      performanceComparison: 'Above average'
    }
  }

  video.analysis = analysisResults
  video.analysisStatus = 'completed'
}

const fetchTrendVideos = async (trend) => {
  // Simulate fetching videos related to a trend
  await new Promise(resolve => setTimeout(resolve, 1500))

  return [
    {
      url: `https://youtube.com/watch?v=trend_${trend.id}_1`,
      videoId: `trend_${trend.id}_1`,
      title: `${trend.title} - Complete Guide`,
      channelName: 'TrendMaster',
      channelId: 'trendmaster123',
      thumbnail: `https://img.youtube.com/vi/trend_${trend.id}_1/maxresdefault.jpg`,
      duration: 480,
      views: 45000,
      publishedAt: '2024-01-10'
    },
    {
      url: `https://youtube.com/watch?v=trend_${trend.id}_2`,
      videoId: `trend_${trend.id}_2`,
      title: `Why ${trend.title} is Exploding Right Now`,
      channelName: 'InsightHub',
      channelId: 'insighthub456',
      thumbnail: `https://img.youtube.com/vi/trend_${trend.id}_2/maxresdefault.jpg`,
      duration: 360,
      views: 32000,
      publishedAt: '2024-01-12'
    }
  ]
}
</script>

<style scoped>
/* Custom styles for research workspace components */
</style>
