<template>
  <div class="bg-gradient-to-br from-purple-600 via-purple-700 to-purple-800 rounded-xl p-6 text-white">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 bg-white bg-opacity-20 rounded-lg flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
          </svg>
        </div>
        <div>
          <h3 class="text-white font-semibold text-lg">Your Personal Agent</h3>
          <p class="text-purple-200 text-sm">AI-powered insights • 3 new insights</p>
        </div>
      </div>
      <button class="text-purple-200 hover:text-white">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
        </svg>
      </button>
    </div>

    <!-- Insights Section -->
    <div class="mb-6">
      <h4 class="text-sm font-medium text-purple-200 mb-4 uppercase tracking-wide">INSIGHTS</h4>

      <!-- Trending Topic Insight -->
      <div class="bg-white bg-opacity-10 rounded-lg p-4 mb-3">
        <div class="flex items-start space-x-3">
          <div class="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center flex-shrink-0">
            <span class="text-white text-xs">🔥</span>
          </div>
          <div class="flex-1">
            <h5 class="font-medium text-white mb-1">Trending topic detected</h5>
            <p class="text-sm text-purple-200">AI Gaming Tools is trending in your niche</p>
          </div>
        </div>
      </div>

      <!-- Retention Insight -->
      <div class="bg-white bg-opacity-10 rounded-lg p-4 mb-3">
        <div class="flex items-start space-x-3">
          <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center flex-shrink-0">
            <span class="text-white text-xs">📈</span>
          </div>
          <div class="flex-1">
            <h5 class="font-medium text-white mb-1">Retention improved</h5>
            <p class="text-sm text-purple-200">Audience retention increased by 15% this week</p>
          </div>
        </div>
      </div>

      <!-- Revenue Impact -->
      <div class="bg-white bg-opacity-10 rounded-lg p-4 mb-4">
        <div class="flex items-start space-x-3">
          <div class="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center flex-shrink-0">
            <span class="text-white text-xs">💰</span>
          </div>
          <div class="flex-1">
            <h5 class="font-medium text-white mb-1">Revenue impact</h5>
            <p class="text-sm text-purple-200">Earned you +$200 in additional revenue</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="mb-6">
      <h4 class="text-sm font-medium text-purple-200 mb-4 uppercase tracking-wide">QUICK ACTIONS</h4>
      <div class="grid grid-cols-2 gap-3">
        <button class="bg-white bg-opacity-10 rounded-lg p-4 text-center hover:bg-opacity-20 transition-all">
          <div class="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center mx-auto mb-2">
            <span class="text-white text-xs">📝</span>
          </div>
          <span class="text-sm font-medium">Generate Script</span>
        </button>

        <button class="bg-white bg-opacity-10 rounded-lg p-4 text-center hover:bg-opacity-20 transition-all">
          <div class="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center mx-auto mb-2">
            <span class="text-white text-xs">🎯</span>
          </div>
          <span class="text-sm font-medium">Improve Hooks</span>
        </button>

        <button class="bg-white bg-opacity-10 rounded-lg p-4 text-center hover:bg-opacity-20 transition-all">
          <div class="w-8 h-8 bg-yellow-500 rounded-lg flex items-center justify-center mx-auto mb-2">
            <span class="text-white text-xs">⚡</span>
          </div>
          <span class="text-sm font-medium">Optimize Title</span>
        </button>

        <button class="bg-white bg-opacity-10 rounded-lg p-4 text-center hover:bg-opacity-20 transition-all">
          <div class="w-8 h-8 bg-pink-500 rounded-lg flex items-center justify-center mx-auto mb-2">
            <span class="text-white text-xs">💡</span>
          </div>
          <span class="text-sm font-medium">Get Ideas</span>
        </button>
      </div>
    </div>

    <!-- Ask Your Agent -->
    <div>
      <h4 class="text-sm font-medium text-purple-200 mb-4 uppercase tracking-wide">ASK YOUR AGENT</h4>

      <!-- Chat Messages -->
      <div class="space-y-3 mb-4">
        <div class="flex items-start space-x-3">
          <div class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
            <span class="text-xs font-bold text-white">AI</span>
          </div>
          <div class="bg-white bg-opacity-10 rounded-lg p-3 flex-1">
            <p class="text-sm text-white">How can I help with your content creation today?</p>
          </div>
        </div>

        <div class="bg-yellow-500 bg-opacity-20 rounded-lg p-3">
          <p class="text-sm text-white">What pillar topics are trending this week?</p>
        </div>

        <div class="flex items-start space-x-3">
          <div class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
            <span class="text-xs font-bold text-white">AI</span>
          </div>
          <div class="bg-white bg-opacity-10 rounded-lg p-3 flex-1">
            <p class="text-sm text-white mb-2">Based on your niche, these pillar topics are trending:</p>
            <ul class="text-sm text-purple-200 space-y-1">
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
          class="flex-1 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg px-4 py-2 text-white placeholder-purple-200 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-30"
        />
        <button class="bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg p-2 transition-all">
          <span class="text-white">→</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
// Agent compartment functionality
</script>
