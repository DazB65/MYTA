<template>
  <div
    class="rounded-xl bg-gradient-to-br from-yellow-500 via-yellow-600 to-yellow-700 p-6 text-white"
  >
    <!-- Header -->
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-white bg-opacity-20">
          <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path
              d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"
            />
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-white">Your Personal Agent</h3>
          <p class="text-sm text-yellow-100">AI-powered insights • 3 new insights</p>
        </div>
      </div>
      <button class="text-yellow-100 hover:text-white">
        <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
          <path
            fill-rule="evenodd"
            d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
    </div>

    <!-- Insights Section -->
    <div class="mb-6">
      <h4 class="mb-4 text-sm font-medium uppercase tracking-wide text-purple-200">INSIGHTS</h4>

      <!-- Trending Topic Insight -->
      <div class="mb-3 rounded-lg bg-white bg-opacity-10 p-4">
        <div class="flex items-start space-x-3">
          <div
            class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-orange-500"
          >
            <span class="text-xs text-white">🔥</span>
          </div>
          <div class="flex-1">
            <h5 class="mb-1 font-medium text-white">Trending topic detected</h5>
            <p class="text-sm text-purple-200">AI Gaming Tools is trending in your niche</p>
          </div>
        </div>
      </div>

      <!-- Retention Insight -->
      <div class="mb-3 rounded-lg bg-white bg-opacity-10 p-4">
        <div class="flex items-start space-x-3">
          <div
            class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-green-500"
          >
            <span class="text-xs text-white">📈</span>
          </div>
          <div class="flex-1">
            <h5 class="mb-1 font-medium text-white">Retention improved</h5>
            <p class="text-sm text-yellow-100">Audience retention increased by 15% this week</p>
          </div>
        </div>
      </div>

      <!-- Revenue Impact -->
      <div class="mb-4 rounded-lg bg-white bg-opacity-10 p-4">
        <div class="flex items-start space-x-3">
          <div
            class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-yellow-500"
          >
            <span class="text-xs text-white">💰</span>
          </div>
          <div class="flex-1">
            <h5 class="mb-1 font-medium text-white">Revenue impact</h5>
            <p class="text-sm text-purple-200">Earned you +$200 in additional revenue</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="mb-6">
      <h4 class="mb-4 text-sm font-medium uppercase tracking-wide text-purple-200">
        QUICK ACTIONS
      </h4>
      <div class="grid grid-cols-2 gap-3">
        <button
          class="rounded-lg bg-white bg-opacity-10 p-4 text-center transition-all hover:bg-opacity-20"
        >
          <div class="mx-auto mb-2 flex h-8 w-8 items-center justify-center rounded-lg bg-blue-500">
            <span class="text-xs text-white">📝</span>
          </div>
          <span class="text-sm font-medium">Generate Script</span>
        </button>

        <button
          class="rounded-lg bg-white bg-opacity-10 p-4 text-center transition-all hover:bg-opacity-20"
        >
          <div
            class="mx-auto mb-2 flex h-8 w-8 items-center justify-center rounded-lg bg-green-500"
          >
            <span class="text-xs text-white">🎯</span>
          </div>
          <span class="text-sm font-medium">Improve Hooks</span>
        </button>

        <button
          class="rounded-lg bg-white bg-opacity-10 p-4 text-center transition-all hover:bg-opacity-20"
        >
          <div
            class="mx-auto mb-2 flex h-8 w-8 items-center justify-center rounded-lg bg-yellow-500"
          >
            <span class="text-xs text-white">⚡</span>
          </div>
          <span class="text-sm font-medium">Optimize Title</span>
        </button>

        <button
          class="rounded-lg bg-white bg-opacity-10 p-4 text-center transition-all hover:bg-opacity-20"
        >
          <div class="mx-auto mb-2 flex h-8 w-8 items-center justify-center rounded-lg bg-pink-500">
            <span class="text-xs text-white">💡</span>
          </div>
          <span class="text-sm font-medium">Get Ideas</span>
        </button>
      </div>
    </div>

    <!-- Ask Your Agent -->
    <div>
      <h4 class="mb-4 text-sm font-medium uppercase tracking-wide text-purple-200">
        ASK YOUR AGENT
      </h4>

      <!-- Chat Messages -->
      <div class="mb-4 space-y-3">
        <div class="flex items-start space-x-3">
          <div
            class="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-green-600"
          >
            <span class="text-xs font-bold text-white">AI</span>
          </div>
          <div class="flex-1 rounded-lg bg-white bg-opacity-10 p-3">
            <p class="text-sm text-white">How can I help with your content creation today?</p>
          </div>
        </div>

        <div class="rounded-lg bg-orange-500 bg-opacity-20 p-3">
          <p class="text-sm text-white">What pillar topics are trending this week?</p>
        </div>

        <div class="flex items-start space-x-3">
          <div
            class="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-blue-500"
          >
            <span class="text-xs font-bold text-white">AI</span>
          </div>
          <div class="flex-1 rounded-lg bg-white bg-opacity-10 p-3">
            <p class="mb-2 text-sm text-white">
              Based on your niche, these pillar topics are trending:
            </p>
            <ul class="space-y-1 text-sm text-purple-200">
              <li>• AI Content Creation Tools (+24%)</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="flex items-center space-x-2">
        <input
          type="text"
          placeholder="Ask your AI agent anything..."
          class="flex-1 rounded-lg border border-white border-opacity-20 bg-white bg-opacity-10 px-4 py-2 text-white placeholder-green-200 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-opacity-50"
        />
        <button class="rounded-lg bg-orange-500 bg-opacity-80 p-2 transition-all hover:bg-opacity-100">
          <span class="text-white">→</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
// Agent compartment functionality
</script>
