<template>
  <div>
    <!-- Dashboard Content -->
    <div class="space-y-6 pt-32 px-6">




      <!-- Dashboard Content Grid -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <!-- Task Manager Compartment -->
        <div class="rounded-xl bg-gray-800 p-6">
          <div class="mb-6 flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-pink-500">
                <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">Task Manager</h3>
                <p class="text-sm text-gray-400">Out of 5 tasks completed</p>
              </div>
            </div>
            <button class="text-gray-400 hover:text-white">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
              </svg>
            </button>
          </div>

          <!-- Filter Buttons -->
          <div class="mb-6 flex space-x-2">
            <button class="rounded-full bg-pink-500 px-4 py-2 text-sm text-white">
              All
            </button>
            <button class="rounded-full bg-gray-700 px-4 py-2 text-sm text-gray-300 hover:bg-gray-600">
              Pending
            </button>
            <button class="rounded-full bg-gray-700 px-4 py-2 text-sm text-gray-300 hover:bg-gray-600">
              Completed
            </button>
          </div>

          <!-- Add New Goal Button -->
          <div class="mb-6 flex items-center space-x-2">
            <button class="flex h-6 w-6 items-center justify-center rounded-full bg-pink-500 text-white">
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
              </svg>
            </button>
            <span class="text-sm font-medium text-pink-500">Add New Goal</span>
          </div>

          <!-- Task List -->
          <div class="space-y-4">
            <!-- Task 1 -->
            <div class="flex items-center justify-between rounded-lg bg-gray-700 p-4">
              <div class="flex items-center space-x-3">
                <div class="h-4 w-4 rounded-full border-2 border-pink-500"></div>
                <div>
                  <h4 class="font-medium text-white">Create engaging video content</h4>
                  <p class="text-sm text-gray-400">
                    Develop compelling video content that resonates with your target audience
                  </p>
                  <div class="mt-2 flex items-center space-x-2">
                    <span class="rounded bg-gray-600 px-2 py-1 text-xs text-gray-300">Content</span>
                    <span class="text-xs text-gray-400">📅 Due: 18/7/2025</span>
                  </div>
                </div>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                </svg>
              </button>
            </div>

            <!-- Task 2 -->
            <div class="flex items-center justify-between rounded-lg bg-gray-700 p-4">
              <div class="flex items-center space-x-3">
                <div class="h-4 w-4 rounded-full bg-pink-500"></div>
                <div>
                  <h4 class="font-medium text-white line-through">Optimize video SEO</h4>
                  <p class="text-sm text-gray-400">
                    Improve video titles, descriptions, and tags for better discoverability
                  </p>
                  <div class="mt-2 flex items-center space-x-2">
                    <span class="rounded bg-gray-600 px-2 py-1 text-xs text-gray-300">SEO</span>
                    <span class="text-xs text-gray-400">✅ Completed</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Task 3 -->
            <div class="flex items-center justify-between rounded-lg bg-gray-700 p-4">
              <div class="flex items-center space-x-3">
                <div class="h-4 w-4 rounded-full border-2 border-pink-500"></div>
                <div>
                  <h4 class="font-medium text-white">Engage with audience</h4>
                  <p class="text-sm text-gray-400">
                    Respond to comments and build community engagement
                  </p>
                  <div class="mt-2 flex items-center space-x-2">
                    <span class="rounded bg-gray-600 px-2 py-1 text-xs text-gray-300">Community</span>
                    <span class="text-xs text-gray-400">📅 Due: 20/7/2025</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Channel Goals Compartment -->
        <div class="rounded-xl bg-gray-800 p-6">
          <div class="mb-6 flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-pink-500">
                <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">Channel Goals</h3>
                <p class="text-sm text-gray-400">Track your progress</p>
              </div>
            </div>
            <button class="text-gray-400 hover:text-white">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
              </svg>
            </button>
          </div>

          <!-- Goals Grid -->
          <div class="space-y-6">
            <!-- Views Goal -->
            <div class="rounded-lg bg-gradient-to-r from-blue-500 to-purple-600 p-4 text-white">
              <div class="mb-4 flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
                    <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/>
                  </svg>
                  <span class="font-semibold">Views</span>
                </div>
                <button class="text-white/80 hover:text-white">
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                  </svg>
                </button>
              </div>
              <div class="mb-4 flex items-center justify-center">
                <div class="relative h-24 w-24">
                  <svg class="h-24 w-24 transform -rotate-90" viewBox="0 0 100 100">
                    <circle
                      cx="50"
                      cy="50"
                      r="40"
                      stroke="currentColor"
                      stroke-width="8"
                      fill="transparent"
                      class="text-white/20"
                    />
                    <circle
                      cx="50"
                      cy="50"
                      r="40"
                      stroke="currentColor"
                      stroke-width="8"
                      fill="transparent"
                      stroke-dasharray="251.2"
                      stroke-dashoffset="62.8"
                      class="text-white"
                      stroke-linecap="round"
                    />
                  </svg>
                  <div class="absolute inset-0 flex items-center justify-center">
                    <span class="text-2xl font-bold">75%</span>
                  </div>
                </div>
              </div>
              <div class="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div class="text-lg font-bold">7.5k</div>
                  <div class="text-xs opacity-80">Current</div>
                </div>
                <div>
                  <div class="text-lg font-bold">2.5k</div>
                  <div class="text-xs opacity-80">Remaining</div>
                </div>
                <div>
                  <div class="text-lg font-bold">10k</div>
                  <div class="text-xs opacity-80">Goal</div>
                </div>
              </div>
            </div>

            <!-- Subscribers Goal -->
            <div class="rounded-lg bg-gradient-to-r from-pink-500 to-red-500 p-4 text-white">
              <div class="mb-4 flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
                  </svg>
                  <span class="font-semibold">Subscribers</span>
                </div>
                <button class="text-white/80 hover:text-white">
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                  </svg>
                </button>
              </div>
              <div class="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div class="text-lg font-bold">1.2k</div>
                  <div class="text-xs opacity-80">Current</div>
                </div>
                <div>
                  <div class="text-lg font-bold">800</div>
                  <div class="text-xs opacity-80">Remaining</div>
                </div>
                <div>
                  <div class="text-lg font-bold">2k</div>
                  <div class="text-xs opacity-80">Goal</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="mt-6 grid grid-cols-2 gap-4">
            <button class="flex items-center justify-center space-x-2 rounded-lg bg-gray-700 p-3 text-sm text-white hover:bg-gray-600">
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
              </svg>
              <span>AI Assistant</span>
            </button>
            <button class="flex items-center justify-center space-x-2 rounded-lg bg-pink-500 p-3 text-sm text-white hover:bg-pink-600">
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
              </svg>
              <span>Add New Task</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Set page title
useHead({
  title: 'Dashboard'
})

// Current date
const currentDate = computed(() => {
  return new Date().toLocaleDateString('en-US', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
})
</script>
