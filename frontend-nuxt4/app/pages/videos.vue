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
            class="flex items-center space-x-2 rounded-lg bg-orange-500 px-4 py-2 text-white transition-colors hover:bg-orange-600"
          >
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                clip-rule="evenodd"
              />
            </svg>
            <span>Upload</span>
          </button>
        </div>
      </div>

      <!-- Recent Videos Section -->
      <div class="mb-8 rounded-xl bg-forest-800 p-6">
        <div class="mb-6 flex items-center justify-between">
          <h3 class="text-xl font-bold text-white">Recent Videos</h3>
          <div class="flex items-center space-x-4">
            <select class="rounded-lg bg-forest-700 px-3 py-2 text-sm text-white">
              <option>Last 30 days</option>
              <option>Last 7 days</option>
              <option>Last 90 days</option>
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
          <div v-for="video in recentVideos" :key="video.id" class="group cursor-pointer">
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

      <!-- Performance Table -->
      <div class="rounded-xl bg-forest-800 p-6">
        <div class="mb-6 flex items-center justify-between">
          <h3 class="text-xl font-bold text-white">Video Performance</h3>
          <div class="flex items-center space-x-2">
            <button class="rounded bg-orange-500 px-3 py-1 text-sm text-white">All</button>
            <button class="rounded px-3 py-1 text-sm text-gray-400 hover:text-white">
              Published
            </button>
            <button class="rounded px-3 py-1 text-sm text-gray-400 hover:text-white">Draft</button>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-700">
                <th class="px-4 py-3 text-left text-sm font-medium text-gray-400">Video</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-gray-400">Status</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-gray-400">Views</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-gray-400">Engagement</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-gray-400">Revenue</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-gray-400">Date</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-gray-400">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="video in performanceVideos"
                :key="video.id"
                class="border-b border-forest-600 hover:bg-forest-700"
              >
                <td class="px-4 py-4">
                  <div class="flex items-center space-x-3">
                    <img
                      :src="video.thumbnail"
                      :alt="video.title"
                      class="h-10 w-16 rounded object-cover"
                    />
                    <div>
                      <p class="text-sm font-medium text-white">{{ video.title }}</p>
                      <p class="text-xs text-gray-400">{{ video.duration }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-4 py-4">
                  <span
                    :class="video.status === 'Published' ? 'bg-green-500' : 'bg-yellow-500'"
                    class="rounded-full px-2 py-1 text-xs text-white"
                  >
                    {{ video.status }}
                  </span>
                </td>
                <td class="px-4 py-4 text-sm text-white">{{ video.views }}</td>
                <td class="px-4 py-4 text-sm text-white">{{ video.engagement }}</td>
                <td class="px-4 py-4 text-sm text-white">{{ video.revenue }}</td>
                <td class="px-4 py-4 text-sm text-gray-400">{{ video.date }}</td>
                <td class="px-4 py-4">
                  <div class="flex items-center space-x-2">
                    <button class="text-gray-400 hover:text-white">
                      <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"
                        />
                      </svg>
                    </button>
                    <button class="text-gray-400 hover:text-white">
                      <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          fill-rule="evenodd"
                          d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"
                          clip-rule="evenodd"
                        />
                        <path
                          fill-rule="evenodd"
                          d="M4 5a2 2 0 012-2h8a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 3a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3z"
                          clip-rule="evenodd"
                        />
                      </svg>
                    </button>
                    <button class="text-gray-400 hover:text-red-400">
                      <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          fill-rule="evenodd"
                          d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"
                          clip-rule="evenodd"
                        />
                        <path
                          fill-rule="evenodd"
                          d="M4 5a2 2 0 012-2h8a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm5 3a1 1 0 000 2h.01a1 1 0 100-2H9z"
                          clip-rule="evenodd"
                        />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Protect this route with authentication
definePageMeta({
  middleware: 'auth'
})

// Sample data for videos
const recentVideos = ref([
  {
    id: 1,
    title: 'How to Create Engaging Content That Converts',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '12:34',
    views: '45.2K',
    date: '2 days ago',
  },
  {
    id: 2,
    title: 'Advanced YouTube Analytics Strategies',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '8:45',
    views: '32.1K',
    date: '5 days ago',
  },
  {
    id: 3,
    title: 'Building Your Personal Brand Online',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '15:22',
    views: '28.7K',
    date: '1 week ago',
  },
  {
    id: 4,
    title: 'Content Creation Tools & Tips',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '10:18',
    views: '19.3K',
    date: '1 week ago',
  },
  {
    id: 5,
    title: 'Social Media Marketing Masterclass',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop',
    duration: '22:15',
    views: '67.8K',
    date: '2 weeks ago',
  },
  {
    id: 6,
    title: 'Video SEO Best Practices',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop',
    duration: '9:33',
    views: '15.4K',
    date: '2 weeks ago',
  },
])

const performanceVideos = ref([
  {
    id: 1,
    title: 'How to Create Engaging Content That Converts',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=100&h=60&fit=crop',
    duration: '12:34',
    status: 'Published',
    views: '45.2K',
    engagement: '8.7%',
    revenue: '$1,234',
    date: 'Dec 15, 2023',
  },
  {
    id: 2,
    title: 'Advanced YouTube Analytics Strategies',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=100&h=60&fit=crop',
    duration: '8:45',
    status: 'Published',
    views: '32.1K',
    engagement: '6.2%',
    revenue: '$892',
    date: 'Dec 12, 2023',
  },
  {
    id: 3,
    title: 'Building Your Personal Brand Online',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=100&h=60&fit=crop',
    duration: '15:22',
    status: 'Published',
    views: '28.7K',
    engagement: '9.1%',
    revenue: '$1,567',
    date: 'Dec 8, 2023',
  },
  {
    id: 4,
    title: 'Content Creation Tools & Tips',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=100&h=60&fit=crop',
    duration: '10:18',
    status: 'Draft',
    views: '19.3K',
    engagement: '5.4%',
    revenue: '$623',
    date: 'Dec 5, 2023',
  },
  {
    id: 5,
    title: 'Social Media Marketing Masterclass',
    thumbnail: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=100&h=60&fit=crop',
    duration: '22:15',
    status: 'Published',
    views: '67.8K',
    engagement: '12.3%',
    revenue: '$2,891',
    date: 'Dec 1, 2023',
  },
])
</script>
