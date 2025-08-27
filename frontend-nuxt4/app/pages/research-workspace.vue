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
            <div class="space-y-2">
              <button
                class="flex w-full items-center space-x-2 rounded-lg bg-forest-700 px-3 py-2 text-left transition-colors hover:bg-forest-600"
                @click="analyzeVideoFromUrl"
              >
                <svg class="h-4 w-4 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clip-rule="evenodd"/>
                </svg>
                <span class="text-sm font-medium text-white">Analyze Video URL</span>
              </button>
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
      v-if="showVideoAnalyzer"
      @close="showVideoAnalyzer = false"
      @analyze="addVideoToCanvas"
    />

    <CompetitorTrackerModal
      v-if="showCompetitorTracker"
      @close="showCompetitorTracker = false"
      @track="addCompetitorToCanvas"
    />

    <TrendScoutModal
      v-if="showTrendScout"
      @close="showTrendScout = false"
      @add-trend="addTrendToCanvas"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

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

const trendingTopics = ref([
  { id: 1, title: 'AI Productivity Tools', growth: 45 },
  { id: 2, title: 'Remote Work Setup', growth: 32 },
  { id: 3, title: 'Content Creation Tips', growth: 28 }
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
const chatInput = ref('')
const canvasContainer = ref(null)

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

const analyzeVideoFromUrl = () => console.log('Analyzing video from URL')
const findTrendingContent = () => console.log('Finding trending content')
const saveProject = () => console.log('Saving project')
const exportToContentStudio = () => console.log('Exporting to content studio')

const addToCanvas = (insight) => console.log('Adding insight to canvas:', insight)
const researchTrend = (trend) => console.log('Researching trend:', trend)

// Canvas methods
const updateVideoPosition = (videoId, position) => console.log('Updating video position:', videoId, position)
const updateNotePosition = (noteId, position) => console.log('Updating note position:', noteId, position)
const analyzeVideo = (video) => console.log('Analyzing video:', video)
const removeVideo = (videoId) => console.log('Removing video:', videoId)
const editNote = (note) => console.log('Editing note:', note)
const removeNote = (noteId) => console.log('Removing note:', noteId)
const removeConnection = (connectionId) => console.log('Removing connection:', connectionId)

const zoomIn = () => console.log('Zooming in')
const zoomOut = () => console.log('Zooming out')
const resetZoom = () => console.log('Resetting zoom')
const fitToScreen = () => console.log('Fitting to screen')

const addVideoToCanvas = (video) => console.log('Adding video to canvas:', video)
const addCompetitorToCanvas = (competitor) => console.log('Adding competitor to canvas:', competitor)
const addTrendToCanvas = (trend) => console.log('Adding trend to canvas:', trend)
</script>

<style scoped>
/* Custom styles for research workspace components */
</style>
