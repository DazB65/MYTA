<template>
  <div class="min-h-screen bg-forest-900 text-white">



    <!-- Main Content Area -->
    <div class="p-6 pt-24">
      <!-- Header -->
      <div class="mb-4 flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <h1 class="text-2xl font-bold text-white">Video Analytics</h1>
          <span class="text-gray-400">•</span>
          <p class="text-gray-400">Track performance and manage your content</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="relative">
            <input
              type="text"
              placeholder="Search videos..."
              class="w-64 rounded-lg bg-forest-800 px-4 py-2 pl-10 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
            />
            <svg
              class="absolute left-3 top-2.5 h-5 w-5 text-gray-400"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <button
            @click="syncWithYouTube"
            :disabled="syncing"
            class="flex items-center space-x-2 rounded-lg bg-orange-500 px-4 py-2 text-white transition-colors hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg v-if="!syncing" class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                clip-rule="evenodd"
              />
            </svg>
            <svg v-else class="h-5 w-5 animate-spin" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                clip-rule="evenodd"
              />
            </svg>
            <span>{{ syncing ? 'Syncing...' : 'Sync with YouTube' }}</span>
          </button>
        </div>

        <!-- Last sync indicator -->
        <div v-if="lastSyncTime" class="text-sm text-gray-400 mt-2">
          Last synced: {{ lastSyncTime }}
        </div>
      </div>

      <!-- Recent Videos Section -->
      <div class="mb-8 rounded-xl bg-forest-800 p-6">
        <div class="mb-6 flex items-center justify-between">
          <h3 class="text-xl font-bold text-white">Recent Videos</h3>
          <div class="flex items-center space-x-4">
            <!-- Sort by Pillar -->
            <select v-model="selectedPillar" class="rounded-lg bg-forest-700 px-3 py-2 text-sm text-white">
              <option value="all">All Pillars</option>
              <option value="Gaming Reviews">Gaming Reviews</option>
              <option value="Tech Tutorials">Tech Tutorials</option>
              <option value="Product Reviews">Product Reviews</option>
              <option value="Industry News">Industry News</option>
            </select>

            <!-- Sort by Performance -->
            <select v-model="sortBy" class="rounded-lg bg-forest-700 px-3 py-2 text-sm text-white">
              <option value="recent">Most Recent</option>
              <option value="views">Most Views</option>
              <option value="engagement">Best Engagement</option>
              <option value="duration">Longest Videos</option>
            </select>

            <button class="text-gray-400 hover:text-white">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          </div>
        </div>

        <!-- Video Grid -->
        <div class="grid grid-cols-6 gap-4">
          <div v-for="video in filteredAndSortedVideos" :key="video.id" class="group cursor-pointer" @click="openVideoStats(video)">
            <div class="relative mb-3 aspect-video overflow-hidden rounded-lg bg-forest-700">
              <img :src="video.thumbnail" :alt="video.title" class="h-full w-full object-cover" />
              <div
                class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-0 transition-all duration-200 group-hover:bg-opacity-30"
              >
                <svg
                  class="h-8 w-8 text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
              <div
                class="absolute bottom-2 right-2 rounded bg-black bg-opacity-75 px-2 py-1 text-xs text-white"
              >
                {{ video.duration }}
              </div>
            </div>
            <h4 class="mb-1 line-clamp-2 text-sm font-medium text-white">{{ video.title }}</h4>
            <p class="text-xs text-gray-400">{{ video.views }} views • {{ video.date }}</p>
          </div>
        </div>
      </div>


    </div>

    <!-- Video Stats Modal -->
    <div v-if="showStatsModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50" @click="closeStatsModal">
      <div class="w-full max-w-4xl mx-4 bg-forest-800 rounded-xl p-6" @click.stop>
        <!-- Modal Header -->
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center space-x-4">
            <img :src="selectedVideo?.thumbnail" :alt="selectedVideo?.title" class="w-16 h-10 object-cover rounded-lg">
            <div>
              <h3 class="text-xl font-bold text-white">{{ selectedVideo?.title }}</h3>
              <p class="text-sm text-gray-400">Published {{ selectedVideo?.date }}</p>
            </div>
          </div>
          <button @click="closeStatsModal" class="text-gray-400 hover:text-white">
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div class="bg-forest-700 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-blue-400">{{ formatNumber(selectedVideo?.detailedStats?.views || 0) }}</div>
            <div class="text-sm text-gray-400">Total Views</div>
            <div class="text-xs text-green-400 mt-1">+{{ selectedVideo?.detailedStats?.viewsGrowth || 0 }}%</div>
          </div>
          <div class="bg-forest-700 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-green-400">{{ selectedVideo?.detailedStats?.likes || 0 }}</div>
            <div class="text-sm text-gray-400">Likes</div>
            <div class="text-xs text-green-400 mt-1">{{ selectedVideo?.detailedStats?.likeRatio || 0 }}% ratio</div>
          </div>
          <div class="bg-forest-700 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-yellow-400">{{ selectedVideo?.detailedStats?.comments || 0 }}</div>
            <div class="text-sm text-gray-400">Comments</div>
            <div class="text-xs text-blue-400 mt-1">{{ selectedVideo?.detailedStats?.engagement || 0 }}% engagement</div>
          </div>
          <div class="bg-forest-700 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-purple-400">{{ selectedVideo?.detailedStats?.watchTime || '0:00' }}</div>
            <div class="text-sm text-gray-400">Avg Watch Time</div>
            <div class="text-xs text-purple-400 mt-1">{{ selectedVideo?.detailedStats?.retention || 0 }}% retention</div>
          </div>
        </div>

        <!-- Performance Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Traffic Sources -->
          <div class="bg-forest-700 rounded-lg p-4">
            <h4 class="text-lg font-semibold text-white mb-4">Traffic Sources</h4>
            <div class="space-y-3">
              <div v-for="source in selectedVideo?.detailedStats?.trafficSources || []" :key="source.name" class="flex items-center justify-between">
                <span class="text-gray-300">{{ source.name }}</span>
                <div class="flex items-center space-x-2">
                  <div class="w-20 bg-forest-600 rounded-full h-2">
                    <div class="bg-orange-500 h-2 rounded-full" :style="{ width: source.percentage + '%' }"></div>
                  </div>
                  <span class="text-sm text-gray-400">{{ source.percentage }}%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Audience Demographics -->
          <div class="bg-forest-700 rounded-lg p-4">
            <h4 class="text-lg font-semibold text-white mb-4">Top Countries</h4>
            <div class="space-y-3">
              <div v-for="country in selectedVideo?.detailedStats?.topCountries || []" :key="country.name" class="flex items-center justify-between">
                <span class="text-gray-300">{{ country.name }}</span>
                <div class="flex items-center space-x-2">
                  <div class="w-20 bg-forest-600 rounded-full h-2">
                    <div class="bg-blue-500 h-2 rounded-full" :style="{ width: country.percentage + '%' }"></div>
                  </div>
                  <span class="text-sm text-gray-400">{{ country.percentage }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Agent Suggestions -->
        <div class="mt-6 bg-gradient-to-r from-orange-500/10 to-red-500/10 rounded-lg p-4 border border-orange-500/20">
          <div class="flex items-center space-x-3 mb-4">
            <div class="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
            </div>
            <div>
              <h4 class="text-lg font-semibold text-white">Boss Agent Recommendations</h4>
              <p class="text-sm text-gray-400">AI-powered suggestions to optimize this video</p>
            </div>
          </div>

          <div class="space-y-3">
            <!-- Performance Optimization -->
            <div v-if="!isRecommendationDismissed('thumbnail')" class="bg-forest-700/50 rounded-lg p-3 border-l-4 border-blue-500 relative transition-all duration-300">
              <button
                @click="dismissRecommendation('thumbnail')"
                class="absolute top-2 right-2 w-5 h-5 bg-gray-600 hover:bg-gray-500 rounded-full flex items-center justify-center transition-colors group"
                title="Dismiss this recommendation"
              >
                <svg class="w-3 h-3 text-gray-300 group-hover:text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
              </button>
              <div class="flex items-start space-x-3">
                <div class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div class="flex-1 pr-6">
                  <h5 class="font-medium text-white">Improve Thumbnail</h5>
                  <p class="text-sm text-gray-300 mt-1">Your click-through rate is {{ selectedVideo?.detailedStats?.ctr || '3.2' }}%. Consider A/B testing a brighter thumbnail with larger text to increase CTR by 15-25%.</p>
                  <div class="flex items-center space-x-2 mt-2">
                    <button
                      @click="addSpecificTask('thumbnail')"
                      class="px-2 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                    >
                      Add to Tasks
                    </button>
                    <button
                      @click="copySpecificRecommendation('thumbnail')"
                      class="px-2 py-1 text-xs bg-gray-600 text-gray-200 rounded hover:bg-gray-500 transition-colors"
                    >
                      Copy
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- SEO Optimization -->
            <div v-if="!isRecommendationDismissed('seo')" class="bg-forest-700/50 rounded-lg p-3 border-l-4 border-green-500 relative transition-all duration-300">
              <button
                @click="dismissRecommendation('seo')"
                class="absolute top-2 right-2 w-5 h-5 bg-gray-600 hover:bg-gray-500 rounded-full flex items-center justify-center transition-colors group"
                title="Dismiss this recommendation"
              >
                <svg class="w-3 h-3 text-gray-300 group-hover:text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
              </button>
              <div class="flex items-start space-x-3">
                <div class="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div class="flex-1 pr-6">
                  <h5 class="font-medium text-white">Optimize Tags & Description</h5>
                  <p class="text-sm text-gray-300 mt-1">Add trending keywords like "{{ selectedVideo?.suggestedKeywords?.[0] || 'tutorial 2024' }}" and "{{ selectedVideo?.suggestedKeywords?.[1] || 'beginner guide' }}" to improve discoverability. Update description with timestamps.</p>
                  <div class="flex items-center space-x-2 mt-2">
                    <button
                      @click="addSpecificTask('seo')"
                      class="px-2 py-1 text-xs bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
                    >
                      Add to Tasks
                    </button>
                    <button
                      @click="copySpecificRecommendation('seo')"
                      class="px-2 py-1 text-xs bg-gray-600 text-gray-200 rounded hover:bg-gray-500 transition-colors"
                    >
                      Copy
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Content Strategy -->
            <div v-if="!isRecommendationDismissed('content')" class="bg-forest-700/50 rounded-lg p-3 border-l-4 border-purple-500 relative transition-all duration-300">
              <button
                @click="dismissRecommendation('content')"
                class="absolute top-2 right-2 w-5 h-5 bg-gray-600 hover:bg-gray-500 rounded-full flex items-center justify-center transition-colors group"
                title="Dismiss this recommendation"
              >
                <svg class="w-3 h-3 text-gray-300 group-hover:text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
              </button>
              <div class="flex items-start space-x-3">
                <div class="w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div class="flex-1 pr-6">
                  <h5 class="font-medium text-white">Create Follow-up Content</h5>
                  <p class="text-sm text-gray-300 mt-1">This video has {{ selectedVideo?.detailedStats?.engagement || '4.2' }}% engagement. Create a "Part 2" or "Advanced Tips" video to capitalize on viewer interest and build a series.</p>
                  <div class="flex items-center space-x-2 mt-2">
                    <button
                      @click="addSpecificTask('content')"
                      class="px-2 py-1 text-xs bg-purple-600 text-white rounded hover:bg-purple-700 transition-colors"
                    >
                      Add to Tasks
                    </button>
                    <button
                      @click="copySpecificRecommendation('content')"
                      class="px-2 py-1 text-xs bg-gray-600 text-gray-200 rounded hover:bg-gray-500 transition-colors"
                    >
                      Copy
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Engagement Boost -->
            <div v-if="!isRecommendationDismissed('engagement')" class="bg-forest-700/50 rounded-lg p-3 border-l-4 border-yellow-500 relative transition-all duration-300">
              <button
                @click="dismissRecommendation('engagement')"
                class="absolute top-2 right-2 w-5 h-5 bg-gray-600 hover:bg-gray-500 rounded-full flex items-center justify-center transition-colors group"
                title="Dismiss this recommendation"
              >
                <svg class="w-3 h-3 text-gray-300 group-hover:text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
              </button>
              <div class="flex items-start space-x-3">
                <div class="w-6 h-6 bg-yellow-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div class="flex-1 pr-6">
                  <h5 class="font-medium text-white">Boost Community Engagement</h5>
                  <p class="text-sm text-gray-300 mt-1">Pin a comment asking viewers about their experience. With {{ selectedVideo?.detailedStats?.comments || '127' }} comments, engaging responses could increase retention by 10%.</p>
                  <div class="flex items-center space-x-2 mt-2">
                    <button
                      @click="addSpecificTask('engagement')"
                      class="px-2 py-1 text-xs bg-yellow-600 text-white rounded hover:bg-yellow-700 transition-colors"
                    >
                      Add to Tasks
                    </button>
                    <button
                      @click="copySpecificRecommendation('engagement')"
                      class="px-2 py-1 text-xs bg-gray-600 text-gray-200 rounded hover:bg-gray-500 transition-colors"
                    >
                      Copy
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Show Dismissed Recommendations -->
          <div v-if="hasDismissedRecommendations" class="mt-4 pt-3 border-t border-forest-600">
            <button
              @click="showDismissedRecommendations = !showDismissedRecommendations"
              class="text-sm text-gray-400 hover:text-gray-300 transition-colors flex items-center space-x-1"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
              </svg>
              <span>{{ showDismissedRecommendations ? 'Hide' : 'Show' }} dismissed recommendations ({{ dismissedCount }})</span>
            </button>

            <div v-if="showDismissedRecommendations" class="mt-3 space-y-2">
              <div v-for="type in dismissedTypes" :key="type" class="bg-forest-700/30 rounded-lg p-2 border border-forest-600">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-300">{{ getRecommendationTitle(type) }}</span>
                  <button
                    @click="restoreRecommendation(type)"
                    class="px-2 py-1 text-xs bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
                  >
                    Restore
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Global Action Buttons -->
          <div class="flex items-center space-x-2 mt-4 pt-3 border-t border-forest-600">
            <button
              @click="openYouTubeStudio"
              class="px-3 py-1.5 bg-red-600 text-white text-sm rounded-md hover:bg-red-700 transition-colors flex items-center space-x-1"
            >
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
              </svg>
              <span>Edit on YouTube</span>
            </button>
            <button
              @click="copyRecommendations"
              class="px-3 py-1.5 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors flex items-center space-x-1"
            >
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z"/>
                <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z"/>
              </svg>
              <span>Copy All</span>
            </button>
            <button
              @click="addToTasks"
              class="px-3 py-1.5 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 transition-colors flex items-center space-x-1"
            >
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
              </svg>
              <span>Add All to Tasks</span>
            </button>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center justify-end space-x-3 mt-6 pt-4 border-t border-forest-600">
          <a
            :href="selectedVideo?.youtubeUrl || '#'"
            target="_blank"
            rel="noopener noreferrer"
            class="px-4 py-2 bg-forest-700 text-gray-300 rounded-lg hover:bg-forest-600 transition-colors inline-flex items-center space-x-2"
          >
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
            </svg>
            <span>View on YouTube</span>
          </a>
          <button
            @click="handleUpdateSEO"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Update SEO & Tags
          </button>
          <button
            @click="handleCreateFollowUp"
            class="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
          >
            Create Follow-up Content
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useModals } from '../../composables/useModals'
import { useToast } from '../../composables/useToast'

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// State for sync functionality
const syncing = ref(false)
const lastSyncTime = ref(null)

// State for video stats modal
const showStatsModal = ref(false)
const selectedVideo = ref(null)

// State for filtering and sorting
const selectedPillar = ref('all')
const sortBy = ref('recent')

// State for dismissed recommendations (per video)
const dismissedRecommendations = ref({})
const showDismissedRecommendations = ref(false)

// Composables
const { openContent } = useModals()
const { success, info } = useToast()

// Sample data for videos
const recentVideos = ref([
  {
    id: 1,
    title: 'How to Create Engaging Content That Converts',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '12:34',
    views: '45.2K',
    viewsNumeric: 45200,
    engagementRate: 4.8,
    date: '2 days ago',
    pillar: 'Tech Tutorials',
    youtubeUrl: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    detailedStats: {
      views: 45234,
      viewsGrowth: 12,
      likes: 1847,
      likeRatio: 96.2,
      comments: 234,
      engagement: 4.8,
      watchTime: '8:42',
      retention: 69.3,
      trafficSources: [
        { name: 'YouTube Search', percentage: 42 },
        { name: 'Suggested Videos', percentage: 28 },
        { name: 'Browse Features', percentage: 18 },
        { name: 'External', percentage: 12 }
      ],
      topCountries: [
        { name: 'United States', percentage: 35 },
        { name: 'United Kingdom', percentage: 18 },
        { name: 'Canada', percentage: 12 },
        { name: 'Australia', percentage: 8 }
      ]
    }
  },
  {
    id: 2,
    title: 'Advanced YouTube Analytics Strategies',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '8:45',
    views: '32.1K',
    viewsNumeric: 32100,
    engagementRate: 5.2,
    date: '5 days ago',
    pillar: 'Tech Tutorials',
    youtubeUrl: 'https://www.youtube.com/watch?v=jNQXAC9IVRw',
  },
  {
    id: 3,
    title: 'Building Your Personal Brand Online',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '15:22',
    views: '28.7K',
    viewsNumeric: 28700,
    engagementRate: 3.9,
    date: '1 week ago',
    pillar: 'Industry News',
  },
  {
    id: 4,
    title: 'Content Creation Tools & Tips',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '10:18',
    views: '19.3K',
    viewsNumeric: 19300,
    engagementRate: 6.1,
    date: '1 week ago',
    pillar: 'Product Reviews',
  },
  {
    id: 5,
    title: 'Social Media Marketing Masterclass',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '22:15',
    views: '67.8K',
    viewsNumeric: 67800,
    engagementRate: 4.1,
    date: '2 weeks ago',
    pillar: 'Tech Tutorials',
  },
  {
    id: 6,
    title: 'Video SEO Best Practices',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '9:33',
    views: '15.4K',
    date: '2 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=oHg5SJYRHA0',
  },
  {
    id: 7,
    title: 'Monetization Strategies That Actually Work',
    thumbnail: 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=300&h=200&fit=crop',
    duration: '18:42',
    views: '52.3K',
    date: '3 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=kJQP7kiw5Fk',
  },
  {
    id: 8,
    title: 'Thumbnail Design Psychology',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '11:27',
    views: '38.9K',
    date: '3 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=lXMskKTw3Bc',
  },
  {
    id: 9,
    title: 'Live Streaming Setup Guide',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '14:55',
    views: '29.7K',
    date: '1 month ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=fJ9rUzIMcZQ',
  },
  {
    id: 10,
    title: 'YouTube Shorts Strategy 2024',
    thumbnail: 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=300&h=200&fit=crop',
    duration: '7:18',
    views: '73.1K',
    viewsNumeric: 73100,
    engagementRate: 7.8,
    date: '1 month ago',
    pillar: 'Gaming Reviews',
    youtubeUrl: 'https://www.youtube.com/watch?v=QH2-TGUlwu4',
  },
  {
    id: 11,
    title: 'Community Building on YouTube',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '16:33',
    views: '41.8K',
    date: '1 month ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=nfWlot6h_JM',
  },
  {
    id: 12,
    title: 'Analytics Deep Dive: What Really Matters',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '20:14',
    views: '35.6K',
    date: '5 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=4fAGfKKoDg8',
  },
  {
    id: 13,
    title: 'Collaboration Strategies for Growth',
    thumbnail: 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=300&h=200&fit=crop',
    duration: '13:09',
    views: '27.4K',
    date: '5 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=ZXsQAXx_ao0',
  },
  {
    id: 14,
    title: 'Equipment Setup on a Budget',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '12:51',
    views: '44.2K',
    date: '6 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=Sagg08DrO5U',
  },
  {
    id: 15,
    title: 'Content Calendar Planning',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '9:47',
    views: '31.5K',
    date: '6 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=5qap5aO4i9A',
  },
  {
    id: 16,
    title: 'Audience Retention Secrets',
    thumbnail: 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=300&h=200&fit=crop',
    duration: '15:23',
    views: '48.7K',
    date: '7 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=BaW_jenozKc',
  },
  {
    id: 17,
    title: 'Brand Partnerships & Sponsorships',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '17:41',
    views: '39.2K',
    date: '7 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=y8Kyi0WNg40',
  },
  {
    id: 18,
    title: 'YouTube Studio Hidden Features',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '11:58',
    views: '33.8K',
    date: '8 weeks ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=ktvTqknDobU',
  },
  {
    id: 19,
    title: 'Viral Video Formula Breakdown',
    thumbnail: 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=300&h=200&fit=crop',
    duration: '14:32',
    views: '89.4K',
    date: '2 months ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
  },
  {
    id: 20,
    title: 'Gaming Content Strategy Guide',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '19:27',
    views: '56.7K',
    date: '2 months ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=jNQXAC9IVRw',
  },
  {
    id: 21,
    title: 'Advanced Editing Techniques',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '16:45',
    views: '42.1K',
    date: '2 months ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=oHg5SJYRHA0',
  },
  {
    id: 22,
    title: 'Microphone Setup & Audio Tips',
    thumbnail: 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=300&h=200&fit=crop',
    duration: '13:18',
    views: '38.9K',
    date: '2 months ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=kJQP7kiw5Fk',
  },
  {
    id: 23,
    title: 'Trending Topics Research',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '10:54',
    views: '29.3K',
    date: '2 months ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=lXMskKTw3Bc',
  },
  {
    id: 24,
    title: 'Creator Economy Deep Dive',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '21:39',
    views: '47.8K',
    date: '2 months ago',
    youtubeUrl: 'https://www.youtube.com/watch?v=fJ9rUzIMcZQ',
  },
])

// Add default pillar and engagement data to videos without it
recentVideos.value.forEach(video => {
  if (!video.pillar) {
    // Assign pillars based on video content
    if (video.title.includes('Gaming') || video.title.includes('Shorts')) {
      video.pillar = 'Gaming Reviews'
    } else if (video.title.includes('Analytics') || video.title.includes('SEO') || video.title.includes('Tutorial') || video.title.includes('YouTube')) {
      video.pillar = 'Tech Tutorials'
    } else if (video.title.includes('Equipment') || video.title.includes('Tools') || video.title.includes('Review')) {
      video.pillar = 'Product Reviews'
    } else {
      video.pillar = 'Industry News'
    }
  }

  if (!video.viewsNumeric) {
    // Convert views string to numeric
    const viewsStr = video.views.replace('K', '').replace('M', '')
    video.viewsNumeric = video.views.includes('K') ? parseFloat(viewsStr) * 1000 : parseFloat(viewsStr) * 1000000
  }

  if (!video.engagementRate) {
    // Generate realistic engagement rates
    video.engagementRate = Math.random() * 4 + 3 // 3-7% range
  }
})

// Computed property for filtered and sorted videos
const filteredAndSortedVideos = computed(() => {
  let filtered = recentVideos.value

  // Filter by pillar
  if (selectedPillar.value !== 'all') {
    filtered = filtered.filter(video => video.pillar === selectedPillar.value)
  }

  // Sort by selected criteria
  switch (sortBy.value) {
    case 'views':
      return filtered.sort((a, b) => b.viewsNumeric - a.viewsNumeric)
    case 'engagement':
      return filtered.sort((a, b) => b.engagementRate - a.engagementRate)
    case 'duration':
      return filtered.sort((a, b) => {
        const aDuration = a.duration.split(':').reduce((acc, time) => (60 * acc) + +time, 0)
        const bDuration = b.duration.split(':').reduce((acc, time) => (60 * acc) + +time, 0)
        return bDuration - aDuration
      })
    case 'recent':
    default:
      return filtered.sort((a, b) => a.id - b.id) // Keep original order for recent
  }
})

// Sync with YouTube functionality
const syncWithYouTube = async () => {
  if (syncing.value) return

  syncing.value = true

  try {
    // Simulate API call to sync with YouTube
    console.log('🔄 Syncing with YouTube...')

    // In a real app, this would:
    // 1. Call YouTube API to get latest videos
    // 2. Update video analytics data
    // 3. Refresh the videos list
    // 4. Update performance metrics

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 2000))

    // Update last sync time
    lastSyncTime.value = new Date().toLocaleString()

    // Show success message
    console.log('✅ Successfully synced with YouTube!')

    // In a real app, you might want to show a toast notification
    alert('Successfully synced with YouTube! Video data has been updated.')

  } catch (error) {
    console.error('❌ Failed to sync with YouTube:', error)
    alert('Failed to sync with YouTube. Please try again.')
  } finally {
    syncing.value = false
  }
}

// Video stats modal functions
const openVideoStats = (video) => {
  selectedVideo.value = video
  showStatsModal.value = true
}

const closeStatsModal = () => {
  showStatsModal.value = false
  selectedVideo.value = null
}

// Helper function to format numbers
const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

// Button handlers for video modal actions
const handleUpdateSEO = () => {
  if (!selectedVideo.value) return

  info('SEO Update', `Opening SEO optimization for "${selectedVideo.value.title}". This feature will help you optimize tags, descriptions, and metadata.`)

  // TODO: Implement SEO modal or redirect to SEO optimization page
  // For now, we'll show a placeholder message
  console.log('🔍 Opening SEO optimization for video:', selectedVideo.value.title)
}

const handleCreateFollowUp = () => {
  if (!selectedVideo.value) return

  // Open content creation modal with video context
  openContent({
    type: 'follow-up',
    sourceVideo: selectedVideo.value,
    title: `Follow-up to: ${selectedVideo.value.title}`,
    description: `Create follow-up content based on "${selectedVideo.value.title}"`
  })

  success('Content Creator Opened', 'Creating follow-up content based on your selected video!')

  // Close the video stats modal
  closeStatsModal()
}

// New action handlers for agent recommendations
const openYouTubeStudio = () => {
  if (!selectedVideo.value) return

  // Open YouTube Studio for this specific video
  const youtubeStudioUrl = `https://studio.youtube.com/video/${selectedVideo.value.id}/edit`
  window.open(youtubeStudioUrl, '_blank')

  info('Opening YouTube Studio', 'Redirecting to YouTube Studio where you can apply the Boss Agent recommendations.')
}

const copyRecommendations = async () => {
  if (!selectedVideo.value) return

  const recommendations = `
Boss Agent Recommendations for "${selectedVideo.value.title}":

🎨 THUMBNAIL OPTIMIZATION:
- Current CTR: ${selectedVideo.value.detailedStats?.ctr || '3.2'}%
- Target: Increase CTR by 15-25% with brighter thumbnail and larger text
- Action: A/B test new thumbnail designs

🔍 SEO & TAGS OPTIMIZATION:
- Add trending keywords: "${selectedVideo.value.suggestedKeywords?.[0] || 'tutorial 2024'}", "${selectedVideo.value.suggestedKeywords?.[1] || 'beginner guide'}"
- Update description with timestamps
- Optimize tags for better discoverability

📺 FOLLOW-UP CONTENT:
- Current engagement: ${selectedVideo.value.detailedStats?.engagement || '4.8'}%
- Create "Part 2" or "Advanced Tips" video
- Build a series to capitalize on viewer interest

💬 COMMUNITY ENGAGEMENT:
- Pin a comment asking about viewer experience
- Current comments: ${selectedVideo.value.detailedStats?.comments || '234'}
- Engaging responses could increase retention by 10%

Generated by MYTA Boss Agent
  `.trim()

  try {
    await navigator.clipboard.writeText(recommendations)
    success('Recommendations Copied!', 'Boss Agent suggestions copied to clipboard. Paste them into your notes or YouTube Studio.')
  } catch (err) {
    console.error('Failed to copy recommendations:', err)
    info('Copy Failed', 'Please manually copy the recommendations from the modal.')
  }
}

const addToTasks = () => {
  if (!selectedVideo.value) return

  // Open task creation modal with pre-filled recommendations
  openTask({
    title: `Optimize: ${selectedVideo.value.title}`,
    description: `Apply Boss Agent recommendations:
• Update thumbnail for better CTR
• Optimize SEO tags and description
• Plan follow-up content
• Boost community engagement`,
    priority: 'high',
    dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], // 1 week from now
    category: 'video-optimization'
  })

  success('Task Created!', 'Video optimization tasks added to your task list with Boss Agent recommendations.')

  // Close the video stats modal
  closeStatsModal()
}

// Individual recommendation handlers
const addSpecificTask = (type) => {
  if (!selectedVideo.value) return

  const taskDetails = {
    thumbnail: {
      title: `Improve Thumbnail: ${selectedVideo.value.title}`,
      description: `• A/B test brighter thumbnail with larger text
• Target: Increase CTR from ${selectedVideo.value.detailedStats?.ctr || '3.2'}% by 15-25%
• Consider using contrasting colors and clear facial expressions
• Test different text sizes and positioning`,
      category: 'thumbnail-optimization'
    },
    seo: {
      title: `Optimize SEO: ${selectedVideo.value.title}`,
      description: `• Add trending keywords: "${selectedVideo.value.suggestedKeywords?.[0] || 'tutorial 2024'}", "${selectedVideo.value.suggestedKeywords?.[1] || 'beginner guide'}"
• Update description with timestamps
• Optimize tags for better discoverability
• Research competitor keywords and trending topics`,
      category: 'seo-optimization'
    },
    content: {
      title: `Create Follow-up Content: ${selectedVideo.value.title}`,
      description: `• Plan "Part 2" or "Advanced Tips" video
• Current engagement: ${selectedVideo.value.detailedStats?.engagement || '4.8'}%
• Build a series to capitalize on viewer interest
• Research related topics and viewer questions`,
      category: 'content-creation'
    },
    engagement: {
      title: `Boost Engagement: ${selectedVideo.value.title}`,
      description: `• Pin a comment asking about viewer experience
• Current comments: ${selectedVideo.value.detailedStats?.comments || '234'}
• Respond to top comments to increase retention
• Create community posts related to this video`,
      category: 'community-engagement'
    }
  }

  const task = taskDetails[type]
  if (!task) return

  // Open task creation modal with pre-filled data
  openTask({
    title: task.title,
    description: task.description,
    priority: 'medium',
    dueDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], // 3 days from now
    category: task.category
  })

  success('Task Created!', `${task.title.split(':')[0]} task added to your task list.`)

  // Close the video stats modal
  closeStatsModal()
}

const copySpecificRecommendation = async (type) => {
  if (!selectedVideo.value) return

  const recommendations = {
    thumbnail: `🎨 THUMBNAIL OPTIMIZATION for "${selectedVideo.value.title}":

Current CTR: ${selectedVideo.value.detailedStats?.ctr || '3.2'}%
Target: Increase CTR by 15-25%

Action Items:
• A/B test brighter thumbnail with larger text
• Use contrasting colors and clear facial expressions
• Test different text sizes and positioning
• Consider using arrows or highlighting key elements

Generated by MYTA Boss Agent`,

    seo: `🔍 SEO & TAGS OPTIMIZATION for "${selectedVideo.value.title}":

Recommended Keywords:
• "${selectedVideo.value.suggestedKeywords?.[0] || 'tutorial 2024'}"
• "${selectedVideo.value.suggestedKeywords?.[1] || 'beginner guide'}"

Action Items:
• Update description with timestamps
• Optimize tags for better discoverability
• Research competitor keywords
• Add trending topics to tags

Generated by MYTA Boss Agent`,

    content: `📺 FOLLOW-UP CONTENT STRATEGY for "${selectedVideo.value.title}":

Current Engagement: ${selectedVideo.value.detailedStats?.engagement || '4.8'}%

Action Items:
• Create "Part 2" or "Advanced Tips" video
• Build a series to capitalize on viewer interest
• Research related topics viewers are asking about
• Plan content calendar for series

Generated by MYTA Boss Agent`,

    engagement: `💬 COMMUNITY ENGAGEMENT for "${selectedVideo.value.title}":

Current Comments: ${selectedVideo.value.detailedStats?.comments || '234'}

Action Items:
• Pin a comment asking about viewer experience
• Respond to top comments to increase retention by 10%
• Create community posts related to this video
• Ask questions to encourage more comments

Generated by MYTA Boss Agent`
  }

  const recommendation = recommendations[type]
  if (!recommendation) return

  try {
    await navigator.clipboard.writeText(recommendation)
    success('Recommendation Copied!', `${type.charAt(0).toUpperCase() + type.slice(1)} recommendation copied to clipboard.`)
  } catch (err) {
    console.error('Failed to copy recommendation:', err)
    info('Copy Failed', 'Please manually copy the recommendation from the modal.')
  }
}

// Recommendation dismissal functions
const dismissRecommendation = (type) => {
  if (!selectedVideo.value) return

  const videoId = selectedVideo.value.id
  if (!dismissedRecommendations.value[videoId]) {
    dismissedRecommendations.value[videoId] = []
  }

  if (!dismissedRecommendations.value[videoId].includes(type)) {
    dismissedRecommendations.value[videoId].push(type)
  }

  info('Recommendation Dismissed', `${getRecommendationTitle(type)} recommendation has been hidden.`)
}

const restoreRecommendation = (type) => {
  if (!selectedVideo.value) return

  const videoId = selectedVideo.value.id
  if (dismissedRecommendations.value[videoId]) {
    const index = dismissedRecommendations.value[videoId].indexOf(type)
    if (index > -1) {
      dismissedRecommendations.value[videoId].splice(index, 1)
    }
  }

  success('Recommendation Restored', `${getRecommendationTitle(type)} recommendation is now visible again.`)
}

const isRecommendationDismissed = (type) => {
  if (!selectedVideo.value) return false
  const videoId = selectedVideo.value.id
  return dismissedRecommendations.value[videoId]?.includes(type) || false
}

const getRecommendationTitle = (type) => {
  const titles = {
    thumbnail: 'Improve Thumbnail',
    seo: 'Optimize Tags & Description',
    content: 'Create Follow-up Content',
    engagement: 'Boost Community Engagement'
  }
  return titles[type] || type
}

// Computed properties for dismissed recommendations
const hasDismissedRecommendations = computed(() => {
  if (!selectedVideo.value) return false
  const videoId = selectedVideo.value.id
  return dismissedRecommendations.value[videoId]?.length > 0
})

const dismissedCount = computed(() => {
  if (!selectedVideo.value) return 0
  const videoId = selectedVideo.value.id
  return dismissedRecommendations.value[videoId]?.length || 0
})

const dismissedTypes = computed(() => {
  if (!selectedVideo.value) return []
  const videoId = selectedVideo.value.id
  return dismissedRecommendations.value[videoId] || []
})
</script>
