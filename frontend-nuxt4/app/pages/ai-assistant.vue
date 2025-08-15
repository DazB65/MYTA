<template>
  <div class="min-h-screen bg-gray-900 text-white">



    <!-- Main Content Area -->
    <div class="p-8 bg-gray-100">
      <!-- Header -->
      <div class="mb-8 flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">AI Assistant</h2>
          <p class="text-gray-500">Chat with your intelligent AI assistants</p>
        </div>
        <div class="flex items-center space-x-4">
          <button
            class="flex items-center space-x-2 rounded-lg bg-pink-500 px-6 py-3 text-white transition-colors hover:bg-pink-600"
          >
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
              />
            </svg>
            <span>New Chat</span>
          </button>
        </div>
      </div>

      <!-- AI Assistant -->
      <div class="py-12 text-center">
        <div
          class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gray-100"
        >
          <svg class="h-8 w-8 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <h3 class="mb-2 text-lg font-medium text-gray-900">AI Assistant Coming Soon</h3>
        <p class="mb-6 text-gray-500">
          Intelligent AI assistants will be available to help with your content strategy
        </p>
        <button
          class="rounded-lg bg-pink-500 px-6 py-3 text-white transition-colors hover:bg-pink-600"
        >
          Join Waitlist
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
// AI Assistant functionality will be added here
</script>
