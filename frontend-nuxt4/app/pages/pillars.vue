<template>
  <div class="min-h-screen bg-forest-900 text-white">


    <!-- Main Content Area -->
    <div class="p-6 pt-24">
      <!-- Header -->
      <div class="mb-4 flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <h1 class="text-2xl font-bold text-white">Content Pillars</h1>
          <span class="text-gray-400">•</span>
          <p class="text-gray-400">Analyze and optimize your content strategy</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="text-sm text-gray-400">Last 30 days</div>
          <button
            class="flex items-center space-x-2 rounded-lg bg-orange-500 px-4 py-2 text-white transition-colors hover:bg-orange-600"
            @click="addPillar"
          >
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                clip-rule="evenodd"
              />
            </svg>
            <span>Add Pillar</span>
          </button>
        </div>
      </div>

      <!-- Content Pillars Grid -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <!-- Game Development Pillar -->
        <div class="rounded-xl bg-forest-800 p-6">
          <div class="mb-4 flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-500">
                <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">Game Development</h3>
                <p class="text-sm text-gray-400">3 Videos • Created 4 months ago</p>
              </div>
            </div>
            <button class="text-gray-400 hover:text-white">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                />
              </svg>
            </button>
          </div>

          <!-- Metrics -->
          <div class="mb-6 grid grid-cols-3 gap-4">
            <div>
              <div class="text-2xl font-bold text-white">248.3K</div>
              <div class="flex items-center text-sm text-green-400">
                <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                +12.5%
              </div>
              <div class="text-xs text-gray-400">Revenue</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">14.2K hrs</div>
              <div class="flex items-center text-sm text-green-400">
                <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                +8.2%
              </div>
              <div class="text-xs text-gray-400">Watch Time</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">93,842</div>
              <div class="flex items-center text-sm text-green-400">
                <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                +15.3%
              </div>
              <div class="text-xs text-gray-400">Subscribers</div>
            </div>
          </div>

          <!-- Chart Area -->
          <div class="relative mb-4 h-32">
            <svg class="h-full w-full" viewBox="0 0 300 100">
              <defs>
                <linearGradient id="blueGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color: #3b82f6; stop-opacity: 0.3" />
                  <stop offset="100%" style="stop-color: #3b82f6; stop-opacity: 0" />
                </linearGradient>
              </defs>
              <path
                d="M0,80 Q50,70 100,60 T200,45 T300,35"
                stroke="#3B82F6"
                stroke-width="2"
                fill="none"
              />
              <path
                d="M0,80 Q50,70 100,60 T200,45 T300,35 L300,100 L0,100 Z"
                fill="url(#blueGradient)"
              />
            </svg>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-400">Top performing content pillar</div>
            <div class="flex space-x-2">
              <button
                class="px-3 py-1 text-sm text-gray-300 hover:text-white"
                @click="viewPillarDetails(pillars[0])"
              >
                View Details
              </button>
              <button
                class="rounded bg-orange-500 px-3 py-1 text-sm text-white hover:bg-orange-600"
                @click="createContent(pillars[0])"
              >
                Create Content
              </button>
            </div>
          </div>
        </div>

        <!-- Game Reviews Pillar -->
        <div class="rounded-xl bg-forest-800 p-6">
          <div class="mb-4 flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-500">
                <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"
                  />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">Game Reviews</h3>
                <p class="text-sm text-gray-400">8 Videos • Created 3 months ago</p>
              </div>
            </div>
            <button class="text-gray-400 hover:text-white">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                />
              </svg>
            </button>
          </div>

          <!-- Metrics -->
          <div class="mb-6 grid grid-cols-3 gap-4">
            <div>
              <div class="text-2xl font-bold text-white">186.7K</div>
              <div class="flex items-center text-sm text-green-400">
                <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                +9.8%
              </div>
              <div class="text-xs text-gray-400">Revenue</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">6.9K hrs</div>
              <div class="flex items-center text-sm text-green-400">
                <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                +6.1%
              </div>
              <div class="text-xs text-gray-400">Watch Time</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">52,156</div>
              <div class="flex items-center text-sm text-green-400">
                <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                +11.2%
              </div>
              <div class="text-xs text-gray-400">Subscribers</div>
            </div>
          </div>

          <!-- Chart Area -->
          <div class="relative mb-4 h-32">
            <svg class="h-full w-full" viewBox="0 0 300 100">
              <defs>
                <linearGradient id="purpleGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color: #8b5cf6; stop-opacity: 0.3" />
                  <stop offset="100%" style="stop-color: #8b5cf6; stop-opacity: 0" />
                </linearGradient>
              </defs>
              <path
                d="M0,85 Q50,75 100,65 T200,50 T300,40"
                stroke="#8B5CF6"
                stroke-width="2"
                fill="none"
              />
              <path
                d="M0,85 Q50,75 100,65 T200,50 T300,40 L300,100 L0,100 Z"
                fill="url(#purpleGradient)"
              />
            </svg>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-400">Consistent growth in audience retention</div>
            <div class="flex space-x-2">
              <button
                class="px-3 py-1 text-sm text-gray-300 hover:text-white"
                @click="viewPillarDetails(pillars[1])"
              >
                View Details
              </button>
              <button
                class="rounded bg-orange-500 px-3 py-1 text-sm text-white hover:bg-orange-600"
                @click="createContent(pillars[1])"
              >
                Create Content
              </button>
            </div>
          </div>
        </div>

        <!-- Gaming Tips Pillar -->
        <div class="rounded-xl bg-forest-800 p-6">
          <div class="mb-4 flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-500">
                <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">Gaming Tips</h3>
                <p class="text-sm text-gray-400">12 Videos • Created 2 months ago</p>
              </div>
            </div>
            <button class="text-gray-400 hover:text-white">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                />
              </svg>
            </button>
          </div>

          <!-- Metrics -->
          <div class="mb-6 grid grid-cols-3 gap-4">
            <div>
              <div class="text-2xl font-bold text-white">203.5K</div>
              <div class="flex items-center text-sm text-green-400">
                <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                +7.3%
              </div>
              <div class="text-xs text-gray-400">Revenue</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">10.1K hrs</div>
              <div class="flex items-center text-sm text-green-400">
                <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                +5.8%
              </div>
              <div class="text-xs text-gray-400">Watch Time</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">92,037</div>
              <div class="flex items-center text-sm text-green-400">
                <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                +13.7%
              </div>
              <div class="text-xs text-gray-400">Subscribers</div>
            </div>
          </div>

          <!-- Chart Area -->
          <div class="relative mb-4 h-32">
            <svg class="h-full w-full" viewBox="0 0 300 100">
              <defs>
                <linearGradient id="orangeGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color: #f97316; stop-opacity: 0.3" />
                  <stop offset="100%" style="stop-color: #f97316; stop-opacity: 0" />
                </linearGradient>
              </defs>
              <path
                d="M0,90 Q50,85 100,75 T200,60 T300,45"
                stroke="#F97316"
                stroke-width="2"
                fill="none"
              />
              <path
                d="M0,90 Q50,85 100,75 T200,60 T300,45 L300,100 L0,100 Z"
                fill="url(#orangeGradient)"
              />
            </svg>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-400">High engagement from returning viewers</div>
            <div class="flex space-x-2">
              <button class="px-3 py-1 text-sm text-gray-300 hover:text-white">View Details</button>
              <button
                class="rounded bg-orange-500 px-3 py-1 text-sm text-white hover:bg-orange-600"
              >
                Create Content
              </button>
            </div>
          </div>
        </div>
        <!-- Gaming News Pillar -->
        <div class="rounded-xl bg-forest-800 p-6">
          <div class="mb-4 flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-500">
                <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"
                  />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">Gaming News</h3>
                <p class="text-sm text-gray-400">6 Videos • Created 4 months ago</p>
              </div>
            </div>
            <button class="text-gray-400 hover:text-white">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                />
              </svg>
            </button>
          </div>

          <!-- Metrics -->
          <div class="mb-6 grid grid-cols-3 gap-4">
            <div>
              <div class="text-2xl font-bold text-white">97.2K</div>
              <div class="flex items-center text-sm text-red-400">
                <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 112 0v11.586l2.293-2.293a1 1 0 011.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                -3.8%
              </div>
              <div class="text-xs text-gray-400">Revenue</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">4.3K hrs</div>
              <div class="flex items-center text-sm text-red-400">
                <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 112 0v11.586l2.293-2.293a1 1 0 011.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                -1.2%
              </div>
              <div class="text-xs text-gray-400">Watch Time</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">8843</div>
              <div class="flex items-center text-sm text-red-400">
                <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 112 0v11.586l2.293-2.293a1 1 0 011.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                -6.5%
              </div>
              <div class="text-xs text-gray-400">Subscribers</div>
            </div>
          </div>

          <!-- Chart Area -->
          <div class="relative mb-4 h-32">
            <svg class="h-full w-full" viewBox="0 0 300 100">
              <defs>
                <linearGradient id="redGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color: #ef4444; stop-opacity: 0.3" />
                  <stop offset="100%" style="stop-color: #ef4444; stop-opacity: 0" />
                </linearGradient>
              </defs>
              <path
                d="M0,60 Q50,65 100,70 T200,75 T300,80"
                stroke="#EF4444"
                stroke-width="2"
                fill="none"
              />
              <path
                d="M0,60 Q50,65 100,70 T200,75 T300,80 L300,100 L0,100 Z"
                fill="url(#redGradient)"
              />
            </svg>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-400">Needs improvement in content strategy</div>
            <div class="flex space-x-2">
              <button class="px-3 py-1 text-sm text-gray-300 hover:text-white">View Details</button>
              <button class="rounded bg-orange-500 px-3 py-1 text-sm text-white hover:bg-orange-600">
                Create Content
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Agent Suggested Pillar -->
      <div class="mt-6 rounded-xl border border-orange-500/20 bg-forest-800 p-6">
        <div class="mb-4 flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg overflow-hidden bg-purple-600/20">
              <img
                v-if="selectedAgent.image"
                :src="selectedAgent.image"
                :alt="selectedAgent.name"
                class="h-full w-full object-cover"
              />
              <svg v-else class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-white">{{ agentName || selectedAgent.name }} Suggested: Metaverse Coverage</h3>
              <p class="text-sm text-orange-400">NEW</p>
            </div>
          </div>
          <div class="flex space-x-2">
            <button
              class="rounded border border-gray-600 px-3 py-1 text-sm text-gray-300 hover:text-white"
            >
              Dismiss
            </button>
            <button
              class="rounded bg-orange-500 px-3 py-1 text-sm text-white hover:bg-orange-600"
              @click="createPillarFromSuggestion({ title: 'Metaverse Coverage', description: 'Content about metaverse gaming and virtual worlds' })"
            >
              Create Pillar
            </button>
          </div>
        </div>
        <p class="text-sm text-gray-300">
          Based on trending topics and your audience interests, consider creating content about
          metaverse gaming and virtual worlds.
        </p>
      </div>
    </div>
  </div>

  <!-- Add Pillar Modal -->
  <div v-if="showAddPillarModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="w-full max-w-md rounded-lg bg-forest-800 p-6">
      <div class="mb-4 flex items-center justify-between">
        <h3 class="text-lg font-semibold text-white">Add New Pillar</h3>
        <button @click="showAddPillarModal = false" class="text-gray-400 hover:text-white">
          <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <form @submit.prevent="savePillar({ name: newPillarName, description: newPillarDescription })">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-300 mb-2">Pillar Name</label>
          <input
            v-model="newPillarName"
            type="text"
            class="w-full rounded-lg bg-forest-700 border border-gray-600 px-3 py-2 text-white placeholder-gray-400 focus:border-orange-500 focus:outline-none"
            placeholder="Enter pillar name..."
            required
          />
        </div>

        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-300 mb-2">Description</label>
          <textarea
            v-model="newPillarDescription"
            class="w-full rounded-lg bg-forest-700 border border-gray-600 px-3 py-2 text-white placeholder-gray-400 focus:border-orange-500 focus:outline-none"
            placeholder="Enter pillar description..."
            rows="3"
            required
          ></textarea>
        </div>

        <div class="flex space-x-3">
          <button
            type="button"
            @click="showAddPillarModal = false"
            class="flex-1 rounded-lg border border-gray-600 px-4 py-2 text-gray-300 hover:text-white"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="flex-1 rounded-lg bg-orange-500 px-4 py-2 text-white hover:bg-orange-600"
          >
            Create Pillar
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- Pillar Details Modal -->
  <div v-if="showPillarDetailsModal && selectedPillar" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="w-full max-w-2xl rounded-lg bg-forest-800 p-6">
      <div class="mb-4 flex items-center justify-between">
        <h3 class="text-lg font-semibold text-white">{{ selectedPillar.name }} Details</h3>
        <button @click="showPillarDetailsModal = false" class="text-gray-400 hover:text-white">
          <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <div class="space-y-4">
        <div>
          <h4 class="text-sm font-medium text-gray-300 mb-2">Description</h4>
          <p class="text-white">{{ selectedPillar.description }}</p>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <h4 class="text-sm font-medium text-gray-300 mb-2">Videos</h4>
            <p class="text-white">{{ selectedPillar.videos }}</p>
          </div>
          <div>
            <h4 class="text-sm font-medium text-gray-300 mb-2">Created</h4>
            <p class="text-white">{{ selectedPillar.created }}</p>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-4">
          <div>
            <h4 class="text-sm font-medium text-gray-300 mb-2">Revenue</h4>
            <p class="text-white">{{ selectedPillar.revenue }}</p>
            <p class="text-sm text-green-400">{{ selectedPillar.revenueChange }}</p>
          </div>
          <div>
            <h4 class="text-sm font-medium text-gray-300 mb-2">Watch Time</h4>
            <p class="text-white">{{ selectedPillar.watchTime }}</p>
            <p class="text-sm text-green-400">{{ selectedPillar.watchTimeChange }}</p>
          </div>
          <div>
            <h4 class="text-sm font-medium text-gray-300 mb-2">Subscribers</h4>
            <p class="text-white">{{ selectedPillar.subscribers }}</p>
            <p class="text-sm text-green-400">{{ selectedPillar.subscribersChange }}</p>
          </div>
        </div>

        <div class="flex space-x-3 pt-4">
          <button
            @click="showPillarDetailsModal = false"
            class="flex-1 rounded-lg border border-gray-600 px-4 py-2 text-gray-300 hover:text-white"
          >
            Close
          </button>
          <button
            @click="createContent(selectedPillar); showPillarDetailsModal = false"
            class="flex-1 rounded-lg bg-orange-500 px-4 py-2 text-white hover:bg-orange-600"
          >
            Create Content
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Create Content Modal -->
  <div v-if="showCreateContentModal && selectedPillar" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="w-full max-w-md rounded-xl bg-forest-800 p-6 mx-4">
      <div class="mb-4 flex items-center justify-between">
        <h3 class="text-lg font-semibold text-white">Create Content for {{ selectedPillar.name }}</h3>
        <button @click="showCreateContentModal = false" class="text-gray-400 hover:text-white">
          <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
          </svg>
        </button>
      </div>

      <form @submit.prevent="saveContent">
        <div class="space-y-4">
          <!-- Title -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Title</label>
            <input
              v-model="newContent.title"
              type="text"
              required
              class="w-full rounded-lg bg-forest-700 border border-forest-600 px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
              placeholder="Enter content title..."
            />
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Description</label>
            <textarea
              v-model="newContent.description"
              rows="3"
              class="w-full rounded-lg bg-forest-700 border border-forest-600 px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
              placeholder="Enter content description..."
            ></textarea>
          </div>

          <!-- Pillar (Pre-filled and disabled) -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Content Pillar</label>
            <div class="w-full rounded-lg bg-forest-700 border border-forest-600 px-3 py-2 text-gray-400">
              🎮 {{ selectedPillar.name }}
            </div>
          </div>

          <!-- Priority -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Priority</label>
            <select
              v-model="newContent.priority"
              class="w-full rounded-lg bg-forest-700 border border-forest-600 px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          <!-- Overall Due Date -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Overall Due Date</label>
            <input
              v-model="newContent.dueDate"
              type="date"
              class="w-full rounded-lg bg-forest-700 border border-forest-600 px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
              :min="new Date().toISOString().split('T')[0]"
            />
            <p class="text-xs text-gray-400 mt-1">When the entire content should be completed</p>
          </div>

          <!-- Stage -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Stage</label>
            <select
              v-model="newContent.status"
              class="w-full rounded-lg bg-forest-700 border border-forest-600 px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
            >
              <option v-for="stage in workflowStages" :key="stage.value" :value="stage.value">
                {{ stage.label }}
              </option>
            </select>
            <p class="text-xs text-gray-400 mt-1">Choose the workflow stage for this content</p>
          </div>

          <!-- Stage Due Dates -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-3">Stage Due Dates & Completion</label>
            <div class="space-y-3">
              <div v-for="stage in workflowStages" :key="stage.value" class="flex items-center space-x-3">
                <div class="w-24 text-sm text-gray-400">{{ stage.label }}:</div>
                <input
                  v-model="newContent.stageDueDates[stage.value]"
                  type="date"
                  class="flex-1 rounded-lg bg-forest-700 border border-forest-600 px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
                  :min="new Date().toISOString().split('T')[0]"
                />
                <label class="flex items-center space-x-2 text-sm text-gray-300">
                  <input
                    v-model="newContent.stageCompletions[stage.value]"
                    type="checkbox"
                    class="rounded bg-forest-700 border-forest-600 text-green-500 focus:ring-green-500 focus:ring-2"
                  />
                  <span>Done</span>
                </label>
              </div>
            </div>
            <p class="text-xs text-gray-400 mt-2">Set deadlines and mark stages as completed</p>
          </div>
        </div>

        <div class="flex items-center justify-end space-x-3 mt-6">
          <button
            type="button"
            @click="showCreateContentModal = false"
            class="px-4 py-2 text-gray-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
          >
            Create Content
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAgentSettings } from '../../composables/useAgentSettings';

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// Agent settings
const { selectedAgent, agentName } = useAgentSettings()

// Modal states
const showAddPillarModal = ref(false)
const showPillarDetailsModal = ref(false)
const showCreateContentModal = ref(false)
const selectedPillar = ref(null)

// Form data
const newPillarName = ref('')
const newPillarDescription = ref('')

// Content creation form data
const newContent = ref({
  title: '',
  description: '',
  pillarId: '',
  priority: 'medium',
  dueDate: '', // Overall completion date
  status: 'ideas',
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

// Available workflow stages
const workflowStages = ref([
  { value: 'ideas', label: 'Ideas', description: 'Initial content concepts' },
  { value: 'planning', label: 'Planning', description: 'Content being planned and structured' },
  { value: 'in-progress', label: 'In Progress', description: 'Content currently being created' },
  { value: 'published', label: 'Published', description: 'Content that has been published' }
])

// Available priorities for content creation
const availablePriorities = ref([
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' }
])

// Pillar data
const pillars = ref([
  {
    id: 1,
    name: 'Game Development',
    description: 'Tutorials and insights on game development',
    videos: 3,
    created: '4 months ago',
    revenue: '248.3K',
    revenueChange: '+12.5%',
    watchTime: '14.2K hrs',
    watchTimeChange: '+8.2%',
    subscribers: '93,842',
    subscribersChange: '+15.3%',
    status: 'Top performing content pillar',
    icon: 'game',
    color: 'orange'
  },
  {
    id: 2,
    name: 'Game Reviews',
    description: 'In-depth reviews of latest games',
    videos: 8,
    created: '3 months ago',
    revenue: '186.7K',
    revenueChange: '+9.3%',
    watchTime: '11.8K hrs',
    watchTimeChange: '+6.1%',
    subscribers: '72,156',
    subscribersChange: '+11.2%',
    status: 'Growing content pillar',
    icon: 'star',
    color: 'orange'
  }
])

// Functions
const addPillar = () => {
  showAddPillarModal.value = true
}

const viewPillarDetails = (pillar) => {
  selectedPillar.value = pillar
  showPillarDetailsModal.value = true
}

const createContent = (pillar) => {
  selectedPillar.value = pillar
  // Pre-fill the pillar in the content form
  newContent.value.pillarId = pillar.id
  showCreateContentModal.value = true
}

const saveContent = () => {
  try {
    // Validate required fields
    if (!newContent.value.title.trim()) {
      alert('Please enter a title')
      return
    }

    // Create new content item
    const newItem = {
      id: Date.now(),
      title: newContent.value.title.trim(),
      description: newContent.value.description.trim() || 'No description provided',
      pillar: selectedPillar.value.name,
      priority: newContent.value.priority,
      status: newContent.value.status,
      assignee: 'M',
      dueDate: newContent.value.dueDate || null,
      stageDueDates: { ...newContent.value.stageDueDates },
      stageCompletions: { ...newContent.value.stageCompletions },
      createdAt: new Date().toISOString().split('T')[0]
    }

    // In a real app, this would be saved to a store/API and synced with calendar/kanban
    console.log('Created new content:', newItem)

    // Reset form
    newContent.value.title = ''
    newContent.value.description = ''
    newContent.value.pillarId = ''
    newContent.value.priority = 'medium'
    newContent.value.dueDate = ''
    newContent.value.status = 'ideas'
    newContent.value.stageDueDates = {
      ideas: '',
      planning: '',
      'in-progress': '',
      published: ''
    }
    newContent.value.stageCompletions = {
      ideas: false,
      planning: false,
      'in-progress': false,
      published: false
    }

    // Close modal
    showCreateContentModal.value = false

    // Show success feedback with due date info
    const dueDateText = newItem.dueDate ? ` (Due: ${new Date(newItem.dueDate).toLocaleDateString()})` : ''
    alert(`Created new content: "${newItem.title}" for ${selectedPillar.value.name} pillar${dueDateText}`)
  } catch (error) {
    console.error('Error saving content:', error)
    alert('Error saving content. Please try again.')
  }
}

const createPillarFromSuggestion = (suggestion) => {
  // Add the suggested pillar to the pillars array
  const newPillar = {
    id: pillars.value.length + 1,
    name: suggestion.title,
    description: suggestion.description,
    videos: 0,
    created: 'Just created',
    revenue: '0',
    revenueChange: '+0%',
    watchTime: '0 hrs',
    watchTimeChange: '+0%',
    subscribers: '0',
    subscribersChange: '+0%',
    status: 'New content pillar',
    icon: 'plus',
    color: 'orange'
  }

  pillars.value.push(newPillar)

  // Show success feedback
  alert(`Created new pillar: ${suggestion.title}`)
}

const savePillar = (pillarData) => {
  const newPillar = {
    id: pillars.value.length + 1,
    name: pillarData.name,
    description: pillarData.description,
    videos: 0,
    created: 'Just created',
    revenue: '0',
    revenueChange: '+0%',
    watchTime: '0 hrs',
    watchTimeChange: '+0%',
    subscribers: '0',
    subscribersChange: '+0%',
    status: 'New content pillar',
    icon: 'plus',
    color: pillarData.color || 'orange'
  }

  pillars.value.push(newPillar)
  showAddPillarModal.value = false

  // Clear form
  newPillarName.value = ''
  newPillarDescription.value = ''

  // Show success feedback
  alert(`Created new pillar: ${pillarData.name}`)
}

// Content Pillars Analytics Dashboard
// Now with full functionality for adding, viewing, and managing pillars
</script>
