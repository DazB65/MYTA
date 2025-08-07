<template>
  <div class="bg-gray-900 text-white min-h-screen flex">
    <!-- Left Sidebar Navigation -->
    <div class="w-72 bg-gray-800 h-screen flex flex-col fixed">
      <!-- Logo Section -->
      <div class="p-6">
        <div class="flex items-center space-x-2">
          <div class="w-8 h-8 bg-pink-500 rounded flex items-center justify-center">
            <span class="text-white text-sm">✨</span>
          </div>
          <h1 class="text-xl font-bold text-white">Vidalytics</h1>
        </div>
        <p class="text-xs text-gray-400 mt-1">
          Your AI Agent for Content and Growth
        </p>
      </div>

      <!-- Main Menu -->
      <div class="px-4">
        <h3 class="text-sm font-medium text-gray-400 mb-4">Main Menu</h3>
        <nav class="space-y-2">
          <NuxtLink
            to="/dashboard"
            class="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg
              class="w-5 h-5 mr-3"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
            </svg>
            Dashboard
          </NuxtLink>
          <NuxtLink
            to="/pillars"
            class="flex items-center px-4 py-3 text-white bg-pink-500 rounded-lg"
          >
            <svg
              class="w-5 h-5 mr-3"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"></path>
            </svg>
            Pillars
          </NuxtLink>
          <NuxtLink
            to="/videos"
            class="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg
              class="w-5 h-5 mr-3"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"></path>
            </svg>
            Videos
          </NuxtLink>
          <NuxtLink
            to="/content-studio"
            class="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg
              class="w-5 h-5 mr-3"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
            </svg>
            Content Studio
          </NuxtLink>
          <NuxtLink
            to="/ai-assistant"
            class="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg
              class="w-5 h-5 mr-3"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            AI Assistant
          </NuxtLink>
        </nav>
      </div>

      <!-- General Section -->
      <div class="px-4 mt-8">
        <h3 class="text-sm font-medium text-gray-400 mb-4">General</h3>
        <nav class="space-y-2">
          <NuxtLink
            to="/settings"
            class="flex items-center px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg
              class="w-5 h-5 mr-3"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                clip-rule="evenodd"
              ></path>
            </svg>
            Settings
          </NuxtLink>
        </nav>
      </div>

      <!-- User Profile Section -->
      <div class="mt-auto p-6 border-t border-gray-700">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-pink-500 rounded-full flex items-center justify-center">
            <span class="text-white font-bold">M</span>
          </div>
          <div class="flex-1">
            <p class="text-sm text-white">Good Morning</p>
            <p class="text-sm font-bold text-white">
              MARCELINE ANDERSON!
            </p>
            <p class="text-xs text-gray-400">
              Let's organize your content pillars
            </p>
          </div>
        </div>
        <div class="mt-4 flex items-center justify-between">
          <div class="text-xs text-gray-400">📅 23 July, 2026</div>
          <button class="text-gray-400 hover:text-white">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </button>
        </div>
        <button class="mt-2 text-gray-400 hover:text-white text-sm flex items-center">
          <svg
            class="w-4 h-4 mr-1"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
              clip-rule="evenodd"
            ></path>
          </svg>
          Log Out
        </button>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="flex-1 bg-gray-100 p-8 overflow-y-auto ml-72">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">Content Pillars</h2>
          <p class="text-gray-500">Organize your content strategy with pillars</p>
        </div>
        <div class="flex items-center space-x-4">
          <button 
            @click="showCreateForm = true"
            class="px-6 py-3 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors flex items-center space-x-2"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"></path>
            </svg>
            <span>Create Pillar</span>
          </button>
          <button 
            @click="analyzeContentPillars"
            :disabled="isAnalyzing"
            class="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg v-if="isAnalyzing" class="w-5 h-5 animate-spin" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
            </svg>
            <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span>{{ isAnalyzing ? 'Analyzing...' : 'AI Analysis' }}</span>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="text-center">
          <svg class="w-8 h-8 animate-spin text-pink-500 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
          </svg>
          <p class="text-gray-600">Loading pillars...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-red-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
          </svg>
          <div>
            <h3 class="text-red-800 font-medium">Error Loading Pillars</h3>
            <p class="text-red-600 text-sm">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Pillars Grid -->
      <div v-if="!isLoading && !error" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Create New Pillar Card -->
        <div 
          @click="showCreateForm = true"
          class="bg-white rounded-xl p-6 border-2 border-dashed border-gray-300 hover:border-pink-400 transition-colors cursor-pointer flex flex-col items-center justify-center min-h-[200px]"
        >
          <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"></path>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Create New Pillar</h3>
          <p class="text-gray-500 text-center text-sm">Add a new content pillar to organize your videos</p>
        </div>

        <!-- Pillar Cards -->
        <div 
          v-for="pillar in pillars" 
          :key="pillar.id"
          class="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow"
        >
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div class="w-12 h-12 rounded-lg bg-gradient-to-br flex items-center justify-center text-white text-xl" :class="pillar.color || 'from-pink-500 to-purple-500'">
                {{ pillar.icon || '🎯' }}
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900">{{ pillar.name }}</h3>
                <p class="text-sm text-gray-500">{{ pillar.video_count || 0 }} videos</p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <button 
                @click="editPillar(pillar)"
                class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
              >
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
                </svg>
              </button>
              <button 
                @click="deletePillar(pillar.id)"
                class="p-2 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50"
              >
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                </svg>
              </button>
            </div>
          </div>
          
          <p class="text-gray-600 text-sm mb-4">{{ pillar.description || 'No description' }}</p>
          
          <div class="flex items-center justify-between text-sm">
            <div class="flex items-center space-x-4">
              <div class="text-gray-500">
                <span class="font-medium text-gray-900">{{ pillar.total_views || 0 }}</span> views
              </div>
              <div class="text-gray-500">
                <span class="font-medium text-gray-900">{{ Math.round(pillar.avg_engagement || 0) }}%</span> engagement
              </div>
            </div>
            <button 
              @click="viewPillarAnalytics(pillar.id)"
              class="text-pink-500 hover:text-pink-600 font-medium"
            >
              View Analytics
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!isLoading && !error && pillars.length === 0" class="text-center py-12">
        <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No Content Pillars</h3>
        <p class="text-gray-500 mb-6">Create your first content pillar to organize your video strategy</p>
        <button 
          @click="showCreateForm = true"
          class="px-6 py-3 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors"
        >
          Create Your First Pillar
        </button>
      </div>
    </div>

    <!-- Create/Edit Pillar Modal -->
    <div v-if="showCreateForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-semibold text-gray-900">
            {{ editingPillar ? 'Edit Pillar' : 'Create New Pillar' }}
          </h3>
          <button @click="closeForm" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>

        <form @submit.prevent="submitForm">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Name</label>
            <input
              v-model="formData.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
              placeholder="e.g., Tech Reviews, Lifestyle Tips"
            />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <textarea
              v-model="formData.description"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
              placeholder="Describe this content pillar..."
            ></textarea>
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Icon</label>
            <input
              v-model="formData.icon"
              type="text"
              maxlength="2"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
              placeholder="🎯"
            />
          </div>

          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">Color Theme</label>
            <div class="grid grid-cols-4 gap-2">
              <button
                v-for="color in colorOptions"
                :key="color.value"
                type="button"
                @click="formData.color = color.value"
                :class="[
                  'w-full h-10 rounded-lg border-2 transition-all',
                  color.gradient,
                  formData.color === color.value ? 'border-gray-400 scale-105' : 'border-gray-200'
                ]"
              >
              </button>
            </div>
          </div>

          <div class="flex items-center space-x-4">
            <button
              type="button"
              @click="closeForm"
              class="flex-1 px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="isSubmitting"
              class="flex-1 px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isSubmitting ? 'Saving...' : (editingPillar ? 'Update' : 'Create') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Reactive state
const pillars = ref([])
const isLoading = ref(true)
const error = ref(null)
const showCreateForm = ref(false)
const editingPillar = ref(null)
const isSubmitting = ref(false)
const isAnalyzing = ref(false)

// Form data
const formData = ref({
  name: '',
  description: '',
  icon: '🎯',
  color: 'from-pink-500 to-purple-500'
})

// Color options for pillars
const colorOptions = [
  { value: 'from-pink-500 to-purple-500', gradient: 'bg-gradient-to-br from-pink-500 to-purple-500' },
  { value: 'from-blue-500 to-cyan-500', gradient: 'bg-gradient-to-br from-blue-500 to-cyan-500' },
  { value: 'from-green-500 to-teal-500', gradient: 'bg-gradient-to-br from-green-500 to-teal-500' },
  { value: 'from-yellow-500 to-orange-500', gradient: 'bg-gradient-to-br from-yellow-500 to-orange-500' },
  { value: 'from-red-500 to-pink-500', gradient: 'bg-gradient-to-br from-red-500 to-pink-500' },
  { value: 'from-indigo-500 to-blue-500', gradient: 'bg-gradient-to-br from-indigo-500 to-blue-500' },
  { value: 'from-purple-500 to-pink-500', gradient: 'bg-gradient-to-br from-purple-500 to-pink-500' },
  { value: 'from-gray-700 to-gray-900', gradient: 'bg-gradient-to-br from-gray-700 to-gray-900' }
]

// API functions
const fetchPillars = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    // Mock user ID - replace with actual user context
    const userId = 'default_user'
    const response = await fetch(`http://localhost:8000/api/pillars/${userId}`)
    
    if (!response.ok) {
      throw new Error('Failed to fetch pillars')
    }
    
    pillars.value = await response.json()
  } catch (err) {
    error.value = err.message || 'Error loading pillars'
    console.error('Error fetching pillars:', err)
  } finally {
    isLoading.value = false
  }
}

const createPillar = async (pillarData) => {
  const response = await fetch('http://localhost:8000/api/pillars', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: 'default_user',
      ...pillarData
    })
  })
  
  if (!response.ok) {
    throw new Error('Failed to create pillar')
  }
  
  return await response.json()
}

const updatePillar = async (pillarId, pillarData) => {
  const response = await fetch(`http://localhost:8000/api/pillars/${pillarId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(pillarData)
  })
  
  if (!response.ok) {
    throw new Error('Failed to update pillar')
  }
  
  return await response.json()
}

const deletePillar = async (pillarId) => {
  if (!confirm('Are you sure you want to delete this pillar?')) {
    return
  }
  
  try {
    const response = await fetch(`http://localhost:8000/api/pillars/${pillarId}`, {
      method: 'DELETE'
    })
    
    if (!response.ok) {
      throw new Error('Failed to delete pillar')
    }
    
    // Refresh pillars list
    await fetchPillars()
  } catch (err) {
    alert('Error deleting pillar: ' + err.message)
  }
}

const analyzeContentPillars = async () => {
  try {
    isAnalyzing.value = true
    
    const response = await fetch('http://localhost:8000/api/youtube/content-pillars', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: 'default_user',
        channel_id: 'UCuAXFkgsw1L7xaCfnd5JJOw', // Example channel ID
        video_count: 20,
        analysis_depth: 'comprehensive'
      })
    })
    
    if (!response.ok) {
      throw new Error('Failed to analyze content pillars')
    }
    
    const result = await response.json()
    alert('Content analysis complete! Check the results in your dashboard.')
    
    // Refresh pillars to show any new ones created by AI
    await fetchPillars()
    
  } catch (err) {
    alert('Error analyzing content: ' + err.message)
  } finally {
    isAnalyzing.value = false
  }
}

// Form functions
const submitForm = async () => {
  try {
    isSubmitting.value = true
    
    if (editingPillar.value) {
      await updatePillar(editingPillar.value.id, formData.value)
    } else {
      await createPillar(formData.value)
    }
    
    closeForm()
    await fetchPillars()
  } catch (err) {
    alert('Error saving pillar: ' + err.message)
  } finally {
    isSubmitting.value = false
  }
}

const editPillar = (pillar) => {
  editingPillar.value = pillar
  formData.value = {
    name: pillar.name,
    description: pillar.description || '',
    icon: pillar.icon || '🎯',
    color: pillar.color || 'from-pink-500 to-purple-500'
  }
  showCreateForm.value = true
}

const closeForm = () => {
  showCreateForm.value = false
  editingPillar.value = null
  formData.value = {
    name: '',
    description: '',
    icon: '🎯',
    color: 'from-pink-500 to-purple-500'
  }
}

const viewPillarAnalytics = (pillarId) => {
  // Navigate to pillar analytics - could be a modal or separate page
  alert(`Analytics for pillar ${pillarId} - Feature coming soon!`)
}

// Initialize
onMounted(() => {
  fetchPillars()
})
</script>