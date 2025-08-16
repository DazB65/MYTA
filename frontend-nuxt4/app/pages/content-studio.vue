<template>
  <div class="min-h-screen bg-gray-900 text-white">

    <!-- Main Content Area -->
    <div class="p-6 pt-32">
      <!-- Header -->
      <div class="mb-6 flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold text-white">Content Studio</h2>
          <p class="text-gray-400">Manage your content workflow from idea to publication</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="relative">
            <input
              type="text"
              placeholder="Search content..."
              class="w-64 rounded-lg bg-gray-800 px-4 py-2 pl-10 text-white focus:outline-none focus:ring-2 focus:ring-pink-500"
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
            class="flex items-center space-x-2 rounded-lg bg-pink-500 px-4 py-2 text-white transition-colors hover:bg-pink-600"
          >
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                clip-rule="evenodd"
              />
            </svg>
            <span>New Content</span>
          </button>
        </div>
      </div>

      <!-- Workflow Stats -->
      <div class="mb-6 grid grid-cols-5 gap-4">
        <div class="rounded-lg bg-gray-800 p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-400">Ideas</p>
              <p class="text-xl font-bold text-white">{{ getColumnCount('ideas') }}</p>
            </div>
            <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-500">
              <svg class="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
          </div>
        </div>
        <div class="rounded-lg bg-gray-800 p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-400">Planning</p>
              <p class="text-xl font-bold text-white">{{ getColumnCount('planning') }}</p>
            </div>
            <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-yellow-500">
              <svg class="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
          </div>
        </div>
        <div class="rounded-lg bg-gray-800 p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-400">In Progress</p>
              <p class="text-xl font-bold text-white">{{ getColumnCount('in-progress') }}</p>
            </div>
            <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-orange-500">
              <svg class="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
          </div>
        </div>
        <div class="rounded-lg bg-gray-800 p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-400">Ready to Publish</p>
              <p class="text-xl font-bold text-white">{{ getColumnCount('ready') }}</p>
            </div>
            <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-green-500">
              <svg class="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
          </div>
        </div>
        <div class="rounded-lg bg-gray-800 p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-400">Analytics</p>
              <p class="text-xl font-bold text-white">{{ getColumnCount('analytics') }}</p>
            </div>
            <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-purple-500">
              <svg class="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Kanban Board -->
      <div class="rounded-lg bg-gray-800 p-6">
        <div class="flex space-x-6 overflow-x-auto">
          <!-- Ideas Column -->
          <div class="w-80 flex-shrink-0">
            <div class="mb-4 flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="h-3 w-3 rounded-full bg-blue-500"/>
                <h3 class="font-semibold text-white">Ideas</h3>
                <span class="rounded-full bg-gray-700 px-2 py-1 text-xs text-gray-300">{{
                  getColumnCount('ideas')
                }}</span>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
            <div class="min-h-96 space-y-3">
              <div
                v-for="item in getColumnItems('ideas')"
                :key="item.id"
                class="cursor-pointer rounded-lg bg-gray-700 p-4 transition-colors hover:bg-gray-600"
              >
                <div class="mb-2 flex items-start justify-between">
                  <h4 class="text-sm font-medium text-white">{{ item.title }}</h4>
                  <button class="text-gray-400 hover:text-white">
                    <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                      />
                    </svg>
                  </button>
                </div>
                <p class="mb-3 text-xs text-gray-300">{{ item.description }}</p>
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span
                      :class="
                        item.priority === 'high'
                          ? 'bg-red-500'
                          : item.priority === 'medium'
                            ? 'bg-yellow-500'
                            : 'bg-green-500'
                      "
                      class="h-2 w-2 rounded-full"
                    />
                    <span class="text-xs text-gray-400">{{ item.priority }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="flex h-6 w-6 items-center justify-center rounded-full bg-pink-500">
                      <span class="text-xs text-white">{{ item.assignee }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Planning Column -->
          <div class="w-80 flex-shrink-0">
            <div class="mb-4 flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="h-3 w-3 rounded-full bg-yellow-500"/>
                <h3 class="font-semibold text-white">Planning</h3>
                <span class="rounded-full bg-gray-700 px-2 py-1 text-xs text-gray-300">{{
                  getColumnCount('planning')
                }}</span>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
            <div class="min-h-96 space-y-3">
              <div
                v-for="item in getColumnItems('planning')"
                :key="item.id"
                class="cursor-pointer rounded-lg bg-gray-700 p-4 transition-colors hover:bg-gray-600"
              >
                <div class="mb-2 flex items-start justify-between">
                  <h4 class="text-sm font-medium text-white">{{ item.title }}</h4>
                  <button class="text-gray-400 hover:text-white">
                    <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                      />
                    </svg>
                  </button>
                </div>
                <p class="mb-3 text-xs text-gray-300">{{ item.description }}</p>
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span
                      :class="
                        item.priority === 'high'
                          ? 'bg-red-500'
                          : item.priority === 'medium'
                            ? 'bg-yellow-500'
                            : 'bg-green-500'
                      "
                      class="h-2 w-2 rounded-full"
                    />
                    <span class="text-xs text-gray-400">{{ item.priority }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="flex h-6 w-6 items-center justify-center rounded-full bg-pink-500">
                      <span class="text-xs text-white">{{ item.assignee }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- In Progress Column -->
          <div class="w-80 flex-shrink-0">
            <div class="mb-4 flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="h-3 w-3 rounded-full bg-orange-500"/>
                <h3 class="font-semibold text-white">In Progress</h3>
                <span class="rounded-full bg-gray-700 px-2 py-1 text-xs text-gray-300">{{
                  getColumnCount('in-progress')
                }}</span>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
            <div class="min-h-96 space-y-3">
              <div
                v-for="item in getColumnItems('in-progress')"
                :key="item.id"
                class="cursor-pointer rounded-lg bg-gray-700 p-4 transition-colors hover:bg-gray-600"
              >
                <div class="mb-2 flex items-start justify-between">
                  <h4 class="text-sm font-medium text-white">{{ item.title }}</h4>
                  <button class="text-gray-400 hover:text-white">
                    <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                      />
                    </svg>
                  </button>
                </div>
                <p class="mb-3 text-xs text-gray-300">{{ item.description }}</p>
                <div class="mb-2 flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span
                      :class="
                        item.priority === 'high'
                          ? 'bg-red-500'
                          : item.priority === 'medium'
                            ? 'bg-yellow-500'
                            : 'bg-green-500'
                      "
                      class="h-2 w-2 rounded-full"
                    />
                    <span class="text-xs text-gray-400">{{ item.priority }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="flex h-6 w-6 items-center justify-center rounded-full bg-pink-500">
                      <span class="text-xs text-white">{{ item.assignee }}</span>
                    </div>
                  </div>
                </div>
                <div v-if="item.progress" class="h-2 w-full rounded-full bg-gray-600">
                  <div
                    class="h-2 rounded-full bg-orange-500"
                    :style="`width: ${item.progress}%`"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Ready to Publish Column -->
          <div class="w-80 flex-shrink-0">
            <div class="mb-4 flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="h-3 w-3 rounded-full bg-green-500"/>
                <h3 class="font-semibold text-white">Ready to Publish</h3>
                <span class="rounded-full bg-gray-700 px-2 py-1 text-xs text-gray-300">{{
                  getColumnCount('ready')
                }}</span>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
            <div class="min-h-96 space-y-3">
              <div
                v-for="item in getColumnItems('ready')"
                :key="item.id"
                class="cursor-pointer rounded-lg bg-gray-700 p-4 transition-colors hover:bg-gray-600"
              >
                <div class="mb-2 flex items-start justify-between">
                  <h4 class="text-sm font-medium text-white">{{ item.title }}</h4>
                  <button class="text-gray-400 hover:text-white">
                    <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                      />
                    </svg>
                  </button>
                </div>
                <p class="mb-3 text-xs text-gray-300">{{ item.description }}</p>
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span
                      :class="
                        item.priority === 'high'
                          ? 'bg-red-500'
                          : item.priority === 'medium'
                            ? 'bg-yellow-500'
                            : 'bg-green-500'
                      "
                      class="h-2 w-2 rounded-full"
                    />
                    <span class="text-xs text-gray-400">{{ item.priority }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="flex h-6 w-6 items-center justify-center rounded-full bg-pink-500">
                      <span class="text-xs text-white">{{ item.assignee }}</span>
                    </div>
                    <button
                      class="rounded bg-green-500 px-2 py-1 text-xs text-white hover:bg-green-600"
                    >
                      Publish
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Analytics Column -->
          <div class="w-80 flex-shrink-0">
            <div class="mb-4 flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="h-3 w-3 rounded-full bg-purple-500"/>
                <h3 class="font-semibold text-white">Analytics</h3>
                <span class="rounded-full bg-gray-700 px-2 py-1 text-xs text-gray-300">{{
                  getColumnCount('analytics')
                }}</span>
              </div>
              <button class="text-gray-400 hover:text-white">
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
            <div class="min-h-96 space-y-3">
              <div
                v-for="item in getColumnItems('analytics')"
                :key="item.id"
                class="cursor-pointer rounded-lg bg-gray-700 p-4 transition-colors hover:bg-gray-600"
              >
                <div class="mb-2 flex items-start justify-between">
                  <h4 class="text-sm font-medium text-white">{{ item.title }}</h4>
                  <button class="text-gray-400 hover:text-white">
                    <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                      />
                    </svg>
                  </button>
                </div>
                <p class="mb-3 text-xs text-gray-300">{{ item.description }}</p>
                <div v-if="item.metrics" class="mb-3">
                  <div class="mb-1 flex justify-between text-xs text-gray-400">
                    <span>Views: {{ item.metrics.views }}</span>
                    <span>Engagement: {{ item.metrics.engagement }}%</span>
                  </div>
                  <div class="flex justify-between text-xs text-gray-400">
                    <span>Likes: {{ item.metrics.likes }}</span>
                    <span>Shares: {{ item.metrics.shares }}</span>
                  </div>
                </div>
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span
                      :class="
                        item.priority === 'high'
                          ? 'bg-red-500'
                          : item.priority === 'medium'
                            ? 'bg-yellow-500'
                            : 'bg-green-500'
                      "
                      class="h-2 w-2 rounded-full"
                    />
                    <span class="text-xs text-gray-400">{{ item.priority }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="flex h-6 w-6 items-center justify-center rounded-full bg-pink-500">
                      <span class="text-xs text-white">{{ item.assignee }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Content items data
const contentItems = ref([
  // Ideas
  {
    id: 1,
    title: 'YouTube Shorts Strategy Guide',
    description: 'Create a comprehensive guide on YouTube Shorts best practices',
    status: 'ideas',
    priority: 'high',
    assignee: 'M',
    createdAt: '2023-12-15',
  },
  {
    id: 2,
    title: 'AI Content Creation Tools Review',
    description: 'Review and compare top AI tools for content creators',
    status: 'ideas',
    priority: 'medium',
    assignee: 'M',
    createdAt: '2023-12-14',
  },
  {
    id: 3,
    title: 'Social Media Trends 2024',
    description: 'Analyze upcoming social media trends for next year',
    status: 'ideas',
    priority: 'low',
    assignee: 'M',
    createdAt: '2023-12-13',
  },

  // Planning
  {
    id: 4,
    title: 'Content Calendar Template',
    description: 'Design a comprehensive content calendar template',
    status: 'planning',
    priority: 'high',
    assignee: 'M',
    createdAt: '2023-12-12',
  },
  {
    id: 5,
    title: 'Brand Voice Guidelines',
    description: 'Establish consistent brand voice across all platforms',
    status: 'planning',
    priority: 'medium',
    assignee: 'M',
    createdAt: '2023-12-11',
  },

  // In Progress
  {
    id: 6,
    title: 'Video Editing Masterclass',
    description: 'Complete tutorial series on advanced video editing',
    status: 'in-progress',
    priority: 'high',
    assignee: 'M',
    progress: 75,
    createdAt: '2023-12-10',
  },
  {
    id: 7,
    title: 'Instagram Growth Hacks',
    description: 'Proven strategies to grow Instagram following organically',
    status: 'in-progress',
    priority: 'medium',
    assignee: 'M',
    progress: 45,
    createdAt: '2023-12-09',
  },

  // Ready to Publish
  {
    id: 8,
    title: 'TikTok Algorithm Secrets',
    description: 'Deep dive into how TikTok algorithm works in 2024',
    status: 'ready',
    priority: 'high',
    assignee: 'M',
    createdAt: '2023-12-08',
  },
  {
    id: 9,
    title: 'Content Monetization Guide',
    description: 'Complete guide to monetizing your content across platforms',
    status: 'ready',
    priority: 'medium',
    assignee: 'M',
    createdAt: '2023-12-07',
  },

  // Analytics
  {
    id: 10,
    title: 'Q4 Performance Report',
    description: 'Comprehensive analysis of Q4 content performance',
    status: 'analytics',
    priority: 'high',
    assignee: 'M',
    metrics: {
      views: '2.4M',
      engagement: '8.7',
      likes: '156K',
      shares: '23K',
    },
    createdAt: '2023-12-06',
  },
  {
    id: 11,
    title: 'Viral Video Analysis',
    description: 'Breakdown of what made our top videos go viral',
    status: 'analytics',
    priority: 'medium',
    assignee: 'M',
    metrics: {
      views: '1.8M',
      engagement: '12.3',
      likes: '89K',
      shares: '45K',
    },
    createdAt: '2023-12-05',
  },
])

// Helper functions
const getColumnItems = status => {
  return contentItems.value.filter(item => item.status === status)
}

const getColumnCount = status => {
  return getColumnItems(status).length
}
</script>
