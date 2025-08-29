<template>
  <div class="min-h-screen bg-forest-900 text-white">
    <!-- Main Content Area -->
    <div class="py-6 pt-24">
      <!-- Header -->
      <div class="mb-6 flex items-center justify-between px-6">
        <div class="flex items-center space-x-4">
          <h1 class="text-2xl font-bold text-white">Research Workspace</h1>
          <span class="text-gray-400">•</span>
          <p class="text-gray-400">AI-powered research for YouTube success</p>
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
      <div class="grid grid-cols-12 gap-2 h-[calc(100vh-320px)]">
        <!-- Left Panel - Research Workflow -->
        <div class="col-span-4 space-y-3 px-3 overflow-y-auto">

          <!-- Step 1: Start Your Research -->
          <div class="rounded-lg bg-forest-800 p-4 border-l-4 border-blue-500">
            <div class="flex items-center mb-3">
              <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold text-sm mr-3">1</div>
              <h3 class="text-lg font-semibold text-white">Start Your Research</h3>
            </div>
            <p class="text-gray-400 text-sm mb-4">Choose a research template or set your research goals</p>
            <div class="space-y-2">
              <button
                class="flex w-full items-center space-x-3 rounded-lg bg-forest-700 px-3 py-2 text-left transition-colors hover:bg-forest-600"
                @click="showTemplates = true"
              >
                <svg class="h-4 w-4 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
                </svg>
                <span class="text-sm font-medium text-white">Choose Research Template</span>
              </button>
              <button
                class="flex w-full items-center space-x-3 rounded-lg bg-forest-700 px-3 py-2 text-left transition-colors hover:bg-forest-600"
                @click="saveProject"
              >
                <svg class="h-4 w-4 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm5 6a1 1 0 10-2 0v3.586l-1.293-1.293a1 1 0 10-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 11.586V8z" clip-rule="evenodd"/>
                </svg>
                <span class="text-sm font-medium text-white">Save Research Project</span>
              </button>
            </div>
          </div>

          <!-- Step 2: Gather Intelligence -->
          <div class="rounded-lg bg-forest-800 p-4 border-l-4 border-orange-500">
            <div class="flex items-center mb-3">
              <div class="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center text-white font-bold text-sm mr-3">2</div>
              <h3 class="text-lg font-semibold text-white">Gather Intelligence</h3>
            </div>
            <p class="text-gray-400 text-sm mb-4">Use AI tools to research your niche, competitors, and trends</p>
            <div class="grid grid-cols-2 gap-2">
              <button
                class="flex flex-col items-center space-y-1 rounded-lg bg-forest-700 p-3 transition-colors hover:bg-forest-600"
                @click="runAIResearch('niche-analysis')"
              >
                <svg class="h-5 w-5 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span class="text-xs font-medium text-white text-center">Niche Analysis</span>
              </button>
              <button
                class="flex flex-col items-center space-y-1 rounded-lg bg-forest-700 p-3 transition-colors hover:bg-forest-600"
                @click="runAIResearch('competitor-analysis')"
              >
                <svg class="h-5 w-5 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
                </svg>
                <span class="text-xs font-medium text-white text-center">Competitors</span>
              </button>
              <button
                class="flex flex-col items-center space-y-1 rounded-lg bg-forest-700 p-3 transition-colors hover:bg-forest-600"
                @click="runAIResearch('viral-opportunities')"
              >
                <svg class="h-5 w-5 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clip-rule="evenodd"/>
                </svg>
                <span class="text-xs font-medium text-white text-center">Viral Trends</span>
              </button>
              <button
                class="flex flex-col items-center space-y-1 rounded-lg bg-forest-700 p-3 transition-colors hover:bg-forest-600"
                @click="findTrendingContent"
              >
                <svg class="h-5 w-5 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                <span class="text-xs font-medium text-white text-center">Find Content</span>
              </button>
            </div>
          </div>



          <!-- Step 3: Analyze Videos -->
          <div class="rounded-lg bg-forest-800 p-4 border-l-4 border-green-500">
            <div class="flex items-center mb-3">
              <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white font-bold text-sm mr-3">3</div>
              <h3 class="text-lg font-semibold text-white">Analyze Videos</h3>
            </div>
            <p class="text-gray-400 text-sm mb-4">Deep-dive into successful videos to extract winning formulas</p>

            <!-- Video URL Input -->
            <div class="space-y-2 mb-3">
              <label class="text-sm font-medium text-gray-300">YouTube Video URL</label>
              <div class="flex space-x-2">
                <input
                  v-model="videoUrl"
                  type="text"
                  placeholder="https://youtube.com/watch?v=..."
                  class="flex-1 rounded-lg bg-forest-700 border border-forest-600 px-3 py-2 text-white placeholder-gray-400 focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
                  @keyup.enter="analyzeVideoFromUrl"
                />
                <button
                  @click="analyzeVideoFromUrl"
                  :disabled="isAnalyzing || !videoUrl.trim()"
                  class="rounded-lg bg-green-500 px-4 py-2 text-white transition-colors hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg v-if="isAnalyzing" class="h-4 w-4 animate-spin" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/>
                  </svg>
                  <svg v-else class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"/>
                  </svg>
                </button>
              </div>
            </div>

            <div class="space-y-2">
              <button
                class="flex w-full items-center space-x-3 rounded-lg bg-forest-700 px-3 py-2 text-left transition-colors hover:bg-forest-600"
                @click="openVideoAnalyzer"
              >
                <svg class="h-4 w-4 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"/>
                </svg>
                <span class="text-sm font-medium text-white">Advanced Video Analyzer</span>
              </button>
              <button
                class="flex w-full items-center space-x-3 rounded-lg bg-forest-700 px-3 py-2 text-left transition-colors hover:bg-forest-600"
                @click="openCompetitorTracker"
              >
                <svg class="h-4 w-4 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                <span class="text-sm font-medium text-white">Track Competitor Videos</span>
              </button>
            </div>
          </div>

          <!-- Step 4: Export Strategy -->
          <div class="rounded-lg bg-forest-800 p-4 border-l-4 border-purple-500">
            <div class="flex items-center mb-3">
              <div class="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center text-white font-bold text-sm mr-3">4</div>
              <h3 class="text-lg font-semibold text-white">Export Strategy</h3>
            </div>
            <p class="text-gray-400 text-sm mb-4">Turn your research into actionable content strategy</p>
            <button
              class="flex w-full items-center space-x-3 rounded-lg bg-purple-600 px-4 py-3 text-left transition-colors hover:bg-purple-700"
              @click="exportToContentStudio"
            >
              <svg class="h-5 w-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
              <div>
                <div class="text-sm font-medium text-white">Export to Content Studio</div>
                <div class="text-xs text-purple-200">Create content from insights</div>
              </div>
            </button>
          </div>
        </div>

        <!-- Main Canvas Area -->
        <div class="col-span-6">
          <div class="rounded-lg bg-forest-800 p-4 h-full relative overflow-hidden">
            <!-- Canvas Header -->
            <div class="relative z-20 mb-4 flex items-center justify-between">
              <div>
                <h2 class="text-xl font-bold text-white">Research Canvas</h2>
                <p class="text-sm text-gray-400">Drag and organize your research findings</p>
              </div>
              <div class="flex items-center space-x-2">
                <span class="text-sm text-gray-400">Items: {{ researchVideos.length + researchNotes.length }}</span>
                <div class="flex space-x-1">
                  <button
                    class="flex h-8 w-8 items-center justify-center rounded-lg bg-forest-700 text-white transition-colors hover:bg-forest-600"
                    @click="zoomIn"
                  >
                    <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"/>
                    </svg>
                  </button>
                  <button
                    class="flex h-8 w-8 items-center justify-center rounded-lg bg-forest-700 text-white transition-colors hover:bg-forest-600"
                    @click="zoomOut"
                  >
                    <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z" clip-rule="evenodd"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Canvas Background -->
            <div class="absolute inset-0 bg-forest-700 rounded-lg">
              <div class="w-full h-full opacity-10" style="background-image: radial-gradient(circle, #fff 1px, transparent 1px); background-size: 20px 20px;"></div>
            </div>

            <!-- Research Items -->
            <div class="relative z-10 h-full">
              <!-- Empty State Message -->
              <div class="flex items-center justify-center h-full text-center" v-if="!researchVideos.length && !researchNotes.length">
                <div class="max-w-md w-full">
                  <div class="mb-6">
                    <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
                    </svg>
                    <h3 class="text-xl font-semibold text-white mb-2">Your Research Canvas</h3>
                    <p class="text-gray-400 text-sm">Start by following the workflow steps on the left. Your research findings will appear here as interactive cards that you can organize and connect.</p>
                  </div>

                  <div class="bg-forest-700 border border-forest-600 rounded-lg p-4">
                    <h4 class="text-white font-medium mb-2">💡 Quick Start</h4>
                    <p class="text-gray-300 text-sm">
                      1. Choose a research template<br/>
                      2. Run AI analysis tools<br/>
                      3. Add videos to analyze<br/>
                      4. Export to Content Studio
                    </p>
                  </div>
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

        <!-- Right Panel - Workflow Guide -->
        <div class="col-span-2 space-y-3 px-3 overflow-y-auto">
          <!-- Workflow Guide -->
          <WorkflowGuide
            :research-items="[...researchVideos, ...researchNotes]"
            @execute-action="handleWorkflowAction"
            @template-complete="handleTemplateComplete"
          />
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

    <ResearchResultModal
      :show="showResearchModal"
      :note="selectedNote"
      @close="showResearchModal = false"
      @saveAsTask="saveResearchAsTask"
      @saveAsGoal="saveResearchAsGoal"
    />

    <ConnectionManager
      :show="showConnectionManager"
      :source-item="connectionSource"
      :target-item="connectionTarget"
      @close="showConnectionManager = false"
      @create="createNewConnection"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ProTipsModal from '../../components/research/ProTipsModal.vue'
import ResearchResultModal from '../../components/research/ResearchResultModal.vue'
import TemplatesModal from '../../components/research/TemplatesModal.vue'
import VideoAnalyzerModal from '../../components/research/VideoAnalyzerModal.vue'
import WorkflowGuide from '../../components/research/WorkflowGuide.vue'
import { useTasksStore } from '../../stores/tasks'

// Initialize stores
const tasksStore = useTasksStore()

// Mock data for research agents
const researchAgents = ref([
  {
    id: 1,
    name: 'Algorithm Whisperer',
    specialty: 'YouTube Algorithm Expert',
    avatar: '/Agent1.png',
    status: 'online'
  },
  {
    id: 2,
    name: 'Thumbnail Genius',
    specialty: 'Visual Design & CTR Expert',
    avatar: '/Agent2.png',
    status: 'online'
  },
  {
    id: 3,
    name: 'Title Master',
    specialty: 'Title Optimization & Psychology',
    avatar: '/Agent3.png',
    status: 'online'
  },
  {
    id: 4,
    name: 'Trend Scout',
    specialty: 'Competitor & Trend Analysis',
    avatar: '/Agent4.png',
    status: 'online'
  },
  {
    id: 5,
    name: 'Growth Strategist',
    specialty: 'Channel Growth & Audience Development',
    avatar: '/Agent5.png',
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
const showResearchModal = ref(false)
const selectedNote = ref(null)
const showConnectionManager = ref(false)
const connectionSource = ref(null)
const connectionTarget = ref(null)
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

// AI Research state
const customResearchPrompt = ref('')
const isResearching = ref(false)
const quickSuggestions = ref([
  'Find trending topics in my niche',
  'Analyze my top 3 competitors',
  'What viral formats are working?',
  'Research SEO opportunities'
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

// AI Research Methods
const runAIResearch = async (type) => {
  isResearching.value = true

  try {
    // Add research result to canvas
    const researchResult = {
      id: Date.now(),
      type: 'ai-research',
      title: getResearchTitle(type),
      content: await simulateAIResearch(type),
      timestamp: new Date(),
      position: { x: Math.random() * 300 + 50, y: Math.random() * 200 + 50 }
    }

    researchNotes.value.push(researchResult)
  } finally {
    isResearching.value = false
  }
}

const runCustomAIResearch = async () => {
  if (!customResearchPrompt.value.trim()) return

  isResearching.value = true

  try {
    const researchResult = {
      id: Date.now(),
      type: 'ai-research',
      title: 'Custom AI Research',
      content: await simulateCustomResearch(customResearchPrompt.value),
      timestamp: new Date(),
      position: { x: Math.random() * 300 + 50, y: Math.random() * 200 + 50 }
    }

    researchNotes.value.push(researchResult)
    customResearchPrompt.value = ''
  } finally {
    isResearching.value = false
  }
}

const getResearchTitle = (type) => {
  const titles = {
    'niche-analysis': 'Niche Analysis Report',
    'viral-opportunities': 'Viral Opportunities',
    'competitor-analysis': 'Competitor Analysis',
    'trending-topics': 'Trending Topics Report'
  }
  return titles[type] || 'AI Research'
}

const simulateAIResearch = async (type) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 2000))

  const mockResults = {
    'niche-analysis': `🎯 **Niche Analysis Results**

**Growth Opportunities:**
• Productivity tutorials: 45% growth potential
• Morning routine content: 32% untapped market
• AI tool reviews: 28% emerging trend

**Content Gaps:**
• Long-form educational content (15+ min)
• Behind-the-scenes productivity setups
• Tool comparison videos

**Recommended Focus:**
Focus on educational content with practical takeaways. Your audience responds well to actionable advice.`,

    'viral-opportunities': `🚀 **Viral Content Opportunities**

**Trending Formats:**
• "Day in my life" productivity videos
• Quick tip carousels (60-90 seconds)
• Before/after workspace transformations

**Hot Topics:**
• AI productivity tools (+156% search volume)
• Remote work setups (+89% engagement)
• Time blocking methods (+67% shares)

**Viral Triggers:**
• Relatable productivity struggles
• Quick wins and instant results
• Visual transformations`,

    'competitor-analysis': `📊 **Competitor Analysis**

**Top Performers:**
1. **ProductivityGuru** - 2.3M subs
   • Posts 3x/week, avg 450K views
   • Strong in tutorial content

2. **EfficiencyExpert** - 1.8M subs
   • Daily shorts, avg 200K views
   • Excels at quick tips

**Content Gaps:**
• Detailed tool tutorials (15+ min)
• Personal productivity journeys
• Live productivity sessions

**Opportunity:**
Create more in-depth, educational content. Competitors focus on quick tips - you can own the detailed tutorial space.`,

    'trending-topics': `📈 **Trending Topics Report**

**Rising Trends:**
• AI productivity assistants (+234% growth)
• Digital minimalism (+156% growth)
• Productivity for ADHD (+89% growth)

**Seasonal Opportunities:**
• New Year productivity resets (Jan)
• Back-to-school organization (Aug-Sep)
• Year-end reflection content (Dec)

**Content Ideas:**
• "AI tools that changed my productivity"
• "Minimalist productivity setup tour"
• "ADHD-friendly productivity systems"`
  }

  return mockResults[type] || 'Research completed successfully!'
}

const simulateCustomResearch = async (prompt) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 2500))

  return `🤖 **Agent Research Results**

**Your Question:** ${prompt}

**Research Findings:**
Based on current trends and data analysis, here are the key insights:

• **Market Analysis:** Strong growth potential in your requested area
• **Content Opportunities:** Multiple angles identified for content creation
• **Competitive Landscape:** Moderate competition with clear differentiation opportunities
• **Audience Interest:** High engagement potential based on search trends

**Recommendations:**
1. Focus on educational, value-driven content
2. Leverage trending keywords and topics
3. Create content series for deeper engagement
4. Consider collaboration opportunities

**Next Steps:**
• Develop content calendar around these insights
• Create pilot content to test audience response
• Monitor performance and iterate based on results

*This research was generated by your AI assistant and should be validated with additional market research.*`
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
  selectedNote.value = note
  showResearchModal.value = true
}

const saveResearchAsTask = (taskData) => {
  try {
    tasksStore.addTask(taskData)
    showResearchModal.value = false
    // You could add a toast notification here
    console.log('Research saved as task successfully!')
  } catch (error) {
    console.error('Failed to save research as task:', error)
  }
}

const saveResearchAsGoal = async (goalData) => {
  try {
    // For now, we'll create a task with goal-like properties
    // In the future, this could integrate with a goals store
    const taskData = {
      title: goalData.title,
      description: goalData.description,
      category: 'research',
      priority: 'high',
      tags: ['goal', 'research', 'agent-generated'],
      dueDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days from now
      estimatedTime: 240 // 4 hours for goal-type tasks
    }

    tasksStore.addTask(taskData)
    showResearchModal.value = false
    console.log('Research saved as goal successfully!')
  } catch (error) {
    console.error('Failed to save research as goal:', error)
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

// Enhanced functionality methods
const handleWorkflowAction = async (data) => {
  const { action, template, step } = data

  if (action.type === 'search') {
    // Trigger search functionality based on action
    if (action.id === 'search-competitors') {
      await searchCompetitors()
    } else if (action.id === 'search-viral') {
      await searchViralVideos()
    } else {
      // Generic search
      showVideoAnalyzer.value = true
    }
  } else if (action.type === 'analysis') {
    // Trigger analysis functionality
    if (action.id === 'analyze-videos') {
      await analyzeAllVideos()
    } else if (action.id === 'analyze-elements') {
      await analyzeVideoElements()
    } else if (action.id === 'find-gaps') {
      await findContentGaps()
    }
  } else if (action.type === 'manual') {
    // Show guidance for manual actions with specific instructions
    const instructions = getActionInstructions(action.id)
    alert(`${action.label}\n\n${instructions}`)
  }
}

// Workflow action implementations
const searchCompetitors = async () => {
  // Simulate competitor search and add to canvas
  const competitors = [
    { name: 'Competitor 1', channel: '@competitor1', subscribers: '500K' },
    { name: 'Competitor 2', channel: '@competitor2', subscribers: '750K' },
    { name: 'Competitor 3', channel: '@competitor3', subscribers: '1.2M' }
  ]

  competitors.forEach((competitor, index) => {
    const competitorNote = {
      id: Date.now().toString() + '_comp_' + index,
      content: `🏆 Competitor: ${competitor.name}\nChannel: ${competitor.channel}\nSubscribers: ${competitor.subscribers}`,
      position: {
        x: 100 + (index * 200),
        y: 150 + (index * 50)
      },
      createdAt: new Date(),
      color: '#FEE2E2', // Red for competitors
      type: 'competitor'
    }
    researchNotes.value.push(competitorNote)
  })

  alert('Added 3 competitor channels to canvas for analysis')
}

const searchViralVideos = async () => {
  // Simulate viral video search
  const viralVideos = [
    { title: 'Viral Video 1 - 5M views', views: '5M', engagement: 'High' },
    { title: 'Viral Video 2 - 3.2M views', views: '3.2M', engagement: 'Very High' },
    { title: 'Viral Video 3 - 8M views', views: '8M', engagement: 'Extreme' }
  ]

  viralVideos.forEach((video, index) => {
    const viralNote = {
      id: Date.now().toString() + '_viral_' + index,
      content: `📈 ${video.title}\nViews: ${video.views}\nEngagement: ${video.engagement}`,
      position: {
        x: 150 + (index * 180),
        y: 200 + (index * 60)
      },
      createdAt: new Date(),
      color: '#FEF3C7', // Yellow for viral content
      type: 'viral'
    }
    researchNotes.value.push(viralNote)
  })

  alert('Added 3 viral videos to canvas for pattern analysis')
}

const analyzeAllVideos = async () => {
  // Simulate video analysis
  const analysisNote = {
    id: Date.now().toString() + '_analysis',
    content: `📊 Video Analysis Results:\n\n• Common themes: Educational, How-to, Problem-solving\n• Average length: 8-12 minutes\n• Thumbnail style: Bold text, bright colors\n• Title patterns: Numbers, questions, benefits`,
    position: { x: 300, y: 300 },
    createdAt: new Date(),
    color: '#DBEAFE', // Blue for analysis
    type: 'analysis'
  }
  researchNotes.value.push(analysisNote)
  alert('Video analysis complete! Results added to canvas.')
}

const analyzeVideoElements = async () => {
  // Simulate element analysis
  const elementNote = {
    id: Date.now().toString() + '_elements',
    content: `🎯 Element Analysis:\n\n• Titles: Use numbers (70%), questions (40%), benefits (60%)\n• Thumbnails: Face + text (80%), bright backgrounds (90%)\n• Hooks: Problem statement in first 15 seconds\n• CTAs: Subscribe reminder at 2-3 minute mark`,
    position: { x: 400, y: 250 },
    createdAt: new Date(),
    color: '#F3E8FF', // Purple for elements
    type: 'elements'
  }
  researchNotes.value.push(elementNote)
  alert('Element analysis complete! Key patterns identified.')
}

const findContentGaps = async () => {
  // Simulate gap analysis
  const gapNote = {
    id: Date.now().toString() + '_gaps',
    content: `🔍 Content Gap Opportunities:\n\n• Beginner tutorials (underserved)\n• Advanced techniques (high demand, low supply)\n• Tool comparisons (trending searches)\n• Behind-the-scenes content (engagement opportunity)`,
    position: { x: 500, y: 200 },
    createdAt: new Date(),
    color: '#D1FAE5', // Green for opportunities
    type: 'gaps'
  }
  researchNotes.value.push(gapNote)
  alert('Content gaps identified! New opportunities added to canvas.')
}

const getActionInstructions = (actionId) => {
  const instructions = {
    'add-competitors': 'Use the search tools on the left to find competitor channels. Look for channels with similar content and audience size. Add their best videos to the canvas.',
    'document-patterns': 'Review the videos on your canvas and note common patterns in titles, thumbnails, content structure, and engagement strategies.',
    'create-strategy': 'Based on your analysis, create a strategy note outlining how you can differentiate from competitors and capitalize on opportunities.'
  }
  return instructions[actionId] || 'Complete this action manually using the tools available.'
}

const handleTemplateComplete = (template) => {
  // Generate completion summary
  const completionNote = {
    id: Date.now().toString() + '_completion',
    content: `✅ ${template.name} Complete!\n\n📊 Research Summary:\n• Total items analyzed: ${researchVideos.value.length + researchNotes.value.length}\n• Connections made: ${connections.value.length}\n• Key insights gathered: ${researchNotes.value.filter(n => n.type === 'analysis').length}\n\n🎯 Next Steps:\n• Export to Content Studio\n• Create content strategy\n• Plan video production`,
    position: { x: 50, y: 50 },
    createdAt: new Date(),
    color: '#D1FAE5', // Green for completion
    type: 'completion'
  }
  researchNotes.value.push(completionNote)

  // Show completion dialog with options
  const nextAction = confirm(`${template.name} workflow completed!\n\nYour research contains:\n• ${researchVideos.value.length} videos\n• ${researchNotes.value.length} notes\n• ${connections.value.length} connections\n\nWould you like to export to Content Studio now?`)

  if (nextAction) {
    exportToContentStudio()
  }
}

const addAgentInsightToCanvas = (insightData) => {
  const note = {
    id: Date.now().toString(),
    content: `${insightData.agent.name} Insight: ${insightData.content.description}`,
    position: insightData.position,
    createdAt: new Date(),
    color: insightData.agent.color + '40', // Semi-transparent agent color
    type: 'agent-insight',
    agent: insightData.agent
  }
  researchNotes.value.push(note)
}

const handleAgentRecommendation = (data) => {
  const { agent, recommendation } = data

  if (recommendation.action === 'competitor_analysis') {
    // Trigger competitor analysis workflow
    console.log('Starting competitor analysis workflow')
  } else if (recommendation.action === 'content_templates') {
    // Create content templates
    console.log('Creating content templates')
  }

  alert(`Applied ${agent.name}'s recommendation: ${recommendation.text}`)
}

const createNewConnection = (connectionData) => {
  const connection = {
    id: Date.now().toString(),
    fromId: connectionData.sourceId,
    toId: connectionData.targetId,
    fromPosition: connectionData.sourcePosition,
    toPosition: connectionData.targetPosition,
    type: connectionData.type,
    label: connectionData.label,
    strength: connectionData.strength,
    createdAt: new Date()
  }

  connections.value.push(connection)
  showConnectionManager.value = false
  connectionSource.value = null
  connectionTarget.value = null
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
