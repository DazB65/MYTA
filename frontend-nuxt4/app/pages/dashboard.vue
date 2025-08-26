<template>
  <div class="min-h-screen bg-forest-900 text-white">
    <!-- Header -->
    <div class="p-6 pt-24">
      <!-- Page Header -->
      <div class="mb-4">
        <h1 class="text-2xl font-bold text-white">Dashboard</h1>
        <p class="text-gray-400">Welcome back! Here's your channel overview.</p>
      </div>

      <!-- Channel Statistics -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <!-- Subscribers -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-red-500 to-red-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('subscribers')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-red-100 font-medium">Subscribers</p>
              <div class="flex items-center space-x-2">
                <!-- Goal Setting Icon -->
                <button
                  @click.stop="handleEditGoal('subscribers')"
                  class="w-6 h-6 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
                  title="Edit goal"
                >
                  <svg class="w-3 h-3 text-white/60 hover:text-white/80" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                  </svg>
                </button>
                <!-- Change Indicator -->
                <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-100">
                  <span>↗</span>
                  <span>12%</span>
                </div>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">1.2K</div>
              <div class="text-sm text-white/70">Total subscribers</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">1.2K of 2K</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" style="width: 60%"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        <!-- Views -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-blue-500 to-blue-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('views')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-blue-100 font-medium">Views</p>
              <div class="flex items-center space-x-2">
                <!-- Goal Setting Icon -->
                <button
                  @click.stop="handleEditGoal('views')"
                  class="w-6 h-6 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
                  title="Edit goal"
                >
                  <svg class="w-3 h-3 text-white/60 hover:text-white/80" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                  </svg>
                </button>
                <!-- Change Indicator -->
                <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-100">
                  <span>↗</span>
                  <span>8%</span>
                </div>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">45.6K</div>
              <div class="text-sm text-white/70">Total views</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">45.6K of 100K</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" style="width: 46%"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        <!-- Watch Time -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-purple-500 to-purple-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('watchTime')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-purple-100 font-medium">Watch Time</p>
              <div class="flex items-center space-x-2">
                <!-- Goal Setting Icon -->
                <button
                  @click.stop="handleEditGoal('watchTime')"
                  class="w-6 h-6 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
                  title="Edit goal"
                >
                  <svg class="w-3 h-3 text-white/60 hover:text-white/80" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                  </svg>
                </button>
                <!-- Change Indicator -->
                <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-100">
                  <span>↗</span>
                  <span>15%</span>
                </div>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">2.1K hrs</div>
              <div class="text-sm text-white/70">Total watch time</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">2.1K of 5K hrs</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" style="width: 42%"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        <!-- Revenue -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-green-500 to-green-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('revenue')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-green-100 font-medium">Revenue</p>
              <div class="flex items-center space-x-2">
                <!-- Goal Setting Icon -->
                <button
                  @click.stop="handleEditGoal('revenue')"
                  class="w-6 h-6 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
                  title="Edit goal"
                >
                  <svg class="w-3 h-3 text-white/60 hover:text-white/80" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                  </svg>
                </button>
                <!-- Change Indicator -->
                <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-100">
                  <span>↗</span>
                  <span>22%</span>
                </div>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">$1,234</div>
              <div class="text-sm text-white/70">Total revenue</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">$1,234 of $3,000</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" style="width: 41%"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
      </div>

      <!-- Analytics Performance -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <!-- Engagement Rate -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-yellow-500 to-yellow-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('engagement')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-yellow-100 font-medium">Engagement</p>
              <div class="flex items-center space-x-2">
                <!-- Goal Setting Icon -->
                <button
                  @click.stop="handleEditGoal('engagement')"
                  class="w-6 h-6 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
                  title="Edit goal"
                >
                  <svg class="w-3 h-3 text-white/60 hover:text-white/80" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                  </svg>
                </button>
                <!-- Change Indicator -->
                <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-100">
                  <span>↗</span>
                  <span>0.3%</span>
                </div>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">4.2%</div>
              <div class="text-sm text-white/70">Engagement rate</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">4.2% of 6.0%</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" style="width: 70%"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        <!-- Click-Through Rate -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-orange-500 to-orange-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('ctr')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-orange-100 font-medium">CTR</p>
              <div class="flex items-center space-x-2">
                <!-- Goal Setting Icon -->
                <button
                  @click.stop="handleEditGoal('ctr')"
                  class="w-6 h-6 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
                  title="Edit goal"
                >
                  <svg class="w-3 h-3 text-white/60 hover:text-white/80" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                  </svg>
                </button>
                <!-- Change Indicator -->
                <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-red-500/20 text-red-100">
                  <span>↘</span>
                  <span>0.2%</span>
                </div>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">3.8%</div>
              <div class="text-sm text-white/70">Click-through rate</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">3.8% of 5.0%</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" style="width: 76%"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        <!-- Average View Duration -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('avgDuration')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-indigo-100 font-medium">Avg Duration</p>
              <div class="flex items-center space-x-2">
                <!-- Goal Setting Icon -->
                <button
                  @click.stop="handleEditGoal('avgDuration')"
                  class="w-6 h-6 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
                  title="Edit goal"
                >
                  <svg class="w-3 h-3 text-white/60 hover:text-white/80" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                  </svg>
                </button>
                <!-- Change Indicator -->
                <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-100">
                  <span>↗</span>
                  <span>15s</span>
                </div>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">2:45</div>
              <div class="text-sm text-white/70">Average view duration</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">2:45 of 4:00</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" style="width: 69%"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        <!-- Retention Rate -->
        <div
          class="relative overflow-hidden rounded-xl bg-gradient-to-br from-pink-500 to-pink-600 p-4 transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer group"
          @click="handleMetricClick('retention')"
        >
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-16 translate-x-16"></div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm text-pink-100 font-medium">Retention</p>
              <div class="flex items-center space-x-2">
                <!-- Goal Setting Icon -->
                <button
                  @click.stop="handleEditGoal('retention')"
                  class="w-6 h-6 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
                  title="Edit goal"
                >
                  <svg class="w-3 h-3 text-white/60 hover:text-white/80" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                  </svg>
                </button>
                <!-- Change Indicator -->
                <div class="flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-semibold bg-green-500/20 text-green-100">
                  <span>↗</span>
                  <span>5%</span>
                </div>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-2xl font-bold text-white leading-tight">68%</div>
              <div class="text-sm text-white/70">Retention rate</div>
            </div>

            <!-- Progress Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
                  <span class="text-sm font-semibold text-white">68% of 80%</span>
                </div>
                <span class="text-sm text-white/70 font-medium">Goal Progress</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mt-3 w-full bg-white/20 rounded-full h-2">
              <div class="bg-white h-2 rounded-full transition-all duration-300" style="width: 85%"></div>
            </div>
          </div>

          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
      </div>

      <!-- Main Dashboard Content -->
      <div class="mb-6">
        <!-- Channel Tasks - Full Width -->
        <div class="rounded-xl bg-forest-800 p-6 mb-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-semibold text-white">Channel Tasks</h2>
            <button class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700">
              Add Task
            </button>
          </div>
          
          <div class="space-y-4">
            <!-- Task Item -->
            <div class="flex items-center justify-between rounded-lg bg-forest-700 p-4">
              <div class="flex items-center space-x-3">
                <input type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600">
                <div>
                  <p class="font-medium text-white">Create thumbnail for latest video</p>
                  <p class="text-sm text-gray-400">Due: Today</p>
                </div>
              </div>
              <span class="rounded-full bg-red-100 px-2 py-1 text-xs font-medium text-red-800">High</span>
            </div>
            
            <!-- Task Item -->
            <div class="flex items-center justify-between rounded-lg bg-forest-700 p-4">
              <div class="flex items-center space-x-3">
                <input type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600">
                <div>
                  <p class="font-medium text-white">Write script for next video</p>
                  <p class="text-sm text-gray-400">Due: Tomorrow</p>
                </div>
              </div>
              <span class="rounded-full bg-yellow-100 px-2 py-1 text-xs font-medium text-yellow-800">Medium</span>
            </div>
            
            <!-- Task Item -->
            <div class="flex items-center justify-between rounded-lg bg-forest-700 p-4">
              <div class="flex items-center space-x-3">
                <input type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600" checked>
                <div>
                  <p class="font-medium text-white line-through">Upload video to YouTube</p>
                  <p class="text-sm text-gray-400">Completed</p>
                </div>
              </div>
              <span class="rounded-full bg-green-100 px-2 py-1 text-xs font-medium text-green-800">Completed</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

// Page metadata
definePageMeta({
  title: 'Dashboard - MYTA',
  description: 'Your YouTube channel dashboard'
})

// Handle metric card clicks
const handleMetricClick = (metric) => {
  console.log(`Clicked on ${metric} metric`)
  // Add logic to show detailed analytics for this metric
}

// Handle goal editing
const handleEditGoal = (metric) => {
  console.log(`Edit goal for ${metric}`)
  // Add logic to open goal editing modal
}
</script>
