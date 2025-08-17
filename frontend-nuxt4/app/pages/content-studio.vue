<template>
  <div class="min-h-screen bg-forest-900 text-white">

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
            class="flex items-center space-x-2 rounded-lg bg-orange-500 px-4 py-2 text-white transition-colors hover:bg-orange-600"
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



      <!-- Kanban Board -->
      <div class="rounded-lg bg-forest-800 p-6">
        <div class="grid grid-cols-4 gap-4 pb-6">
          <!-- Ideas Column -->
          <div class="flex flex-col bg-forest-800/30 rounded-lg p-4 border border-forest-600/20">
            <div class="flex items-center justify-between -m-4 mb-4 p-4 bg-forest-700/50 rounded-t-lg">
              <div class="flex items-center space-x-2">
                <div class="h-3 w-3 rounded-full bg-orange-500"/>
                <h3 class="font-semibold text-white">Ideas</h3>
                <span class="rounded-full bg-forest-700 px-2 py-1 text-xs text-gray-300">{{
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
            <div class="flex-1 space-y-3">
              <div
                v-for="item in getColumnItems('ideas')"
                :key="item.id"
                class="cursor-pointer rounded-lg bg-forest-700 p-4 transition-colors hover:bg-forest-600 w-full"
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
                    <div class="flex h-6 w-6 items-center justify-center rounded-full bg-orange-500">
                      <span class="text-xs text-white">{{ item.assignee }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Planning Column -->
          <div class="flex flex-col bg-forest-800/30 rounded-lg p-4 border border-forest-600/20">
            <div class="flex items-center justify-between -m-4 mb-4 p-4 bg-forest-700/50 rounded-t-lg">
              <div class="flex items-center space-x-2">
                <div class="h-3 w-3 rounded-full bg-orange-500"/>
                <h3 class="font-semibold text-white">Planning</h3>
                <span class="rounded-full bg-forest-700 px-2 py-1 text-xs text-gray-300">{{
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
            <div class="flex-1 space-y-3">
              <div
                v-for="item in getColumnItems('planning')"
                :key="item.id"
                class="cursor-pointer rounded-lg bg-forest-700 p-4 transition-colors hover:bg-forest-600 w-full"
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
                    <div class="flex h-6 w-6 items-center justify-center rounded-full bg-orange-500">
                      <span class="text-xs text-white">{{ item.assignee }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- In Progress Column -->
          <div class="flex flex-col bg-forest-800/30 rounded-lg p-4 border border-forest-600/20">
            <div class="flex items-center justify-between -m-4 mb-4 p-4 bg-forest-700/50 rounded-t-lg">
              <div class="flex items-center space-x-2">
                <div class="h-3 w-3 rounded-full bg-orange-500"/>
                <h3 class="font-semibold text-white">In Progress</h3>
                <span class="rounded-full bg-forest-700 px-2 py-1 text-xs text-gray-300">{{
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
            <div class="flex-1 space-y-3">
              <div
                v-for="item in getColumnItems('in-progress')"
                :key="item.id"
                class="cursor-pointer rounded-lg bg-forest-700 p-4 transition-colors hover:bg-forest-600 w-full"
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
                    <div class="flex h-6 w-6 items-center justify-center rounded-full bg-orange-500">
                      <span class="text-xs text-white">{{ item.assignee }}</span>
                    </div>
                  </div>
                </div>
                <div v-if="item.progress" class="h-2 w-full rounded-full bg-forest-600">
                  <div
                    class="h-2 rounded-full bg-orange-500"
                    :style="`width: ${item.progress}%`"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Published Column -->
          <div class="flex flex-col bg-forest-800/30 rounded-lg p-4 border border-forest-600/20">
            <div class="flex items-center justify-between -m-4 mb-4 p-4 bg-forest-700/50 rounded-t-lg">
              <div class="flex items-center space-x-2">
                <div class="h-3 w-3 rounded-full bg-green-500"/>
                <h3 class="font-semibold text-white">Published</h3>
                <span class="rounded-full bg-forest-700 px-2 py-1 text-xs text-gray-300">{{
                  getColumnCount('published')
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
            <div class="flex-1 space-y-3">
              <div
                v-for="item in getColumnItems('published')"
                :key="item.id"
                class="cursor-pointer rounded-lg bg-forest-700 p-4 transition-colors hover:bg-forest-600 w-full"
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
                    <span class="h-2 w-2 rounded-full bg-green-500"/>
                    <span class="text-xs text-gray-400">Published</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="flex h-6 w-6 items-center justify-center rounded-full bg-orange-500">
                      <span class="text-xs text-white">{{ item.assignee }}</span>
                    </div>
                    <span class="text-xs text-green-400">{{ item.publishDate || 'Live' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>


        </div>
      </div>

      <!-- Agent Content Suggestions -->
      <div class="mt-6 rounded-lg bg-forest-800 p-6">
        <div class="mb-6 flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg overflow-hidden bg-purple-600/20">
              <img
                v-if="selectedAgent.image"
                :src="selectedAgent.image"
                :alt="selectedAgent.name"
                class="h-full w-full object-cover"
              />
              <svg v-else class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-white">{{ agentName || selectedAgent.name }} Content Suggestions</h3>
              <p class="text-sm text-gray-400">Personalized recommendations to boost your content strategy</p>
            </div>
          </div>
          <button class="flex items-center space-x-2 rounded-lg bg-forest-700 px-4 py-2 text-sm text-white hover:bg-forest-600 transition-colors">
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/>
            </svg>
            <span>Refresh</span>
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <!-- Trending Topics -->
          <div class="rounded-lg bg-forest-700/50 p-4 border border-forest-600/20">
            <div class="mb-3 flex items-center space-x-2">
              <div class="h-2 w-2 rounded-full bg-red-500"></div>
              <h4 class="text-sm font-semibold text-white">Trending Now</h4>
            </div>
            <div class="space-y-2">
              <div class="cursor-pointer rounded-md bg-forest-700 p-3 hover:bg-forest-600 transition-colors">
                <p class="text-sm text-white font-medium">Agent Tools for Content Creation</p>
                <p class="text-xs text-gray-400 mt-1">High engagement potential</p>
              </div>
              <div class="cursor-pointer rounded-md bg-forest-700 p-3 hover:bg-forest-600 transition-colors">
                <p class="text-sm text-white font-medium">2024 Social Media Predictions</p>
                <p class="text-xs text-gray-400 mt-1">Seasonal relevance</p>
              </div>
              <div class="cursor-pointer rounded-md bg-forest-700 p-3 hover:bg-forest-600 transition-colors">
                <p class="text-sm text-white font-medium">Short-form Video Strategies</p>
                <p class="text-xs text-gray-400 mt-1">Platform trending</p>
              </div>
            </div>
          </div>

          <!-- Content Ideas -->
          <div class="rounded-lg bg-forest-700/50 p-4 border border-forest-600/20">
            <div class="mb-3 flex items-center space-x-2">
              <div class="h-2 w-2 rounded-full bg-blue-500"></div>
              <h4 class="text-sm font-semibold text-white">Content Ideas</h4>
            </div>
            <div class="space-y-2">
              <div class="cursor-pointer rounded-md bg-forest-700 p-3 hover:bg-forest-600 transition-colors">
                <p class="text-sm text-white font-medium">Behind-the-Scenes Content</p>
                <p class="text-xs text-gray-400 mt-1">Builds audience connection</p>
              </div>
              <div class="cursor-pointer rounded-md bg-forest-700 p-3 hover:bg-forest-600 transition-colors">
                <p class="text-sm text-white font-medium">Tutorial Series: Beginner to Pro</p>
                <p class="text-xs text-gray-400 mt-1">Educational content</p>
              </div>
              <div class="cursor-pointer rounded-md bg-forest-700 p-3 hover:bg-forest-600 transition-colors">
                <p class="text-sm text-white font-medium">Community Q&A Sessions</p>
                <p class="text-xs text-gray-400 mt-1">Interactive engagement</p>
              </div>
            </div>
          </div>

          <!-- Optimization Tips -->
          <div class="rounded-lg bg-forest-700/50 p-4 border border-forest-600/20">
            <div class="mb-3 flex items-center space-x-2">
              <div class="h-2 w-2 rounded-full bg-green-500"></div>
              <h4 class="text-sm font-semibold text-white">Optimization Tips</h4>
            </div>
            <div class="space-y-2">
              <div class="cursor-pointer rounded-md bg-forest-700 p-3 hover:bg-forest-600 transition-colors">
                <p class="text-sm text-white font-medium">Post at 2-4 PM for max reach</p>
                <p class="text-xs text-gray-400 mt-1">Timing optimization</p>
              </div>
              <div class="cursor-pointer rounded-md bg-forest-700 p-3 hover:bg-forest-600 transition-colors">
                <p class="text-sm text-white font-medium">Use 3-5 hashtags per post</p>
                <p class="text-xs text-gray-400 mt-1">Hashtag strategy</p>
              </div>
              <div class="cursor-pointer rounded-md bg-forest-700 p-3 hover:bg-forest-600 transition-colors">
                <p class="text-sm text-white font-medium">Add captions to videos</p>
                <p class="text-xs text-gray-400 mt-1">Accessibility boost</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="mt-6 flex flex-wrap gap-3">
          <button class="flex items-center space-x-2 rounded-lg bg-orange-500 px-4 py-2 text-sm text-white hover:bg-orange-600 transition-colors">
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
            </svg>
            <span>Add to Ideas</span>
          </button>
          <button class="flex items-center space-x-2 rounded-lg bg-forest-700 px-4 py-2 text-sm text-white hover:bg-forest-600 transition-colors">
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
            </svg>
            <span>Customize Suggestions</span>
          </button>
          <button class="flex items-center space-x-2 rounded-lg bg-forest-700 px-4 py-2 text-sm text-white hover:bg-forest-600 transition-colors">
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/>
            </svg>
            <span>View Analytics</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAgentSettings } from '../../composables/useAgentSettings'

// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// Agent settings
const { selectedAgent, agentName } = useAgentSettings()

// Agent data is now handled by the composable

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

  // Published
  {
    id: 8,
    title: 'TikTok Algorithm Secrets',
    description: 'Deep dive into how TikTok algorithm works in 2024',
    status: 'published',
    priority: 'high',
    assignee: 'M',
    publishDate: 'Dec 8, 2023',
    createdAt: '2023-12-08',
  },
  {
    id: 9,
    title: 'Content Monetization Guide',
    description: 'Complete guide to monetizing your content across platforms',
    status: 'published',
    priority: 'medium',
    assignee: 'M',
    publishDate: 'Dec 7, 2023',
    createdAt: '2023-12-07',
  },
  {
    id: 10,
    title: 'Q4 Performance Report',
    description: 'Comprehensive analysis of Q4 content performance',
    status: 'published',
    priority: 'high',
    assignee: 'M',
    publishDate: 'Dec 6, 2023',
    createdAt: '2023-12-06',
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
