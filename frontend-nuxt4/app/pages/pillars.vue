<template>
  <div class="min-h-screen bg-forest-900 text-white">


    <!-- Main Content Area -->
    <div class="p-6 pt-32">
      <!-- Header -->
      <div class="mb-6 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-white mb-2">Content Pillars</h1>
          <p class="text-gray-400">Analyze and optimize your content strategy</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="text-sm text-gray-400">Last 30 days</div>
          <button
            class="flex items-center space-x-2 rounded-lg bg-orange-500 px-4 py-2 text-white transition-colors hover:bg-orange-600"
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
              <button class="px-3 py-1 text-sm text-gray-300 hover:text-white">View Details</button>
              <button class="rounded bg-orange-500 px-3 py-1 text-sm text-white hover:bg-orange-600">
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
              <button class="px-3 py-1 text-sm text-gray-300 hover:text-white">View Details</button>
              <button
                class="rounded bg-orange-500 px-3 py-1 text-sm text-white hover:bg-orange-600"
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
            <button class="rounded bg-orange-500 px-3 py-1 text-sm text-white hover:bg-orange-600">
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
</template>

<script setup>
import { useAgentSettings } from '../../composables/useAgentSettings';

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// Agent settings
const { selectedAgent, agentName } = useAgentSettings()

// Agent data is now handled by the composable

// Content Pillars Analytics Dashboard
// Static data display matching the design from the image
</script>
