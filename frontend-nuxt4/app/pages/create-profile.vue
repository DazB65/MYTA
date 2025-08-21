<template>
  <div class="min-h-screen bg-gradient-to-br from-forest-900 via-forest-800 to-forest-700 relative overflow-hidden">
    <!-- Background Elements -->
    <div class="absolute inset-0">
      <div class="absolute top-20 left-20 w-72 h-72 bg-orange-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
      <div class="absolute top-40 right-20 w-72 h-72 bg-forest-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
      <div class="absolute bottom-20 left-40 w-72 h-72 bg-orange-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
    </div>

    <div class="relative z-10 min-h-screen px-6">
      <div class="w-full max-w-7xl mx-auto -mt-12">
        <!-- MYTA Logo Header -->
        <div class="text-center -mt-16">
          <div class="flex items-center justify-center -mb-20">
            <img src="/MY YT AGENT.png" alt="MYTA Logo" class="w-[28rem] h-[28rem]">
          </div>

        </div>

        <!-- Agent Selection -->
        <div class="mb-3">
          <h2 class="text-2xl font-semibold text-white text-center mb-6">Choose Your Agent Icon</h2>
          <div class="grid grid-cols-6 gap-4 max-w-6xl mx-auto">
            <div
              v-for="agent in agents"
              :key="agent.id"
              @click="selectAgent(agent.id)"
              :class="[
                'agent-card',
                selectedAgent === agent.id ? 'selected' : ''
              ]"
              class="bg-white/10 backdrop-blur-lg rounded-2xl p-4 text-center cursor-pointer transition-all duration-300 hover:bg-white/20 hover:scale-105 border border-white/20"
            >
              <div class="w-16 h-16 mx-auto mb-3 rounded-xl overflow-hidden bg-white/20 flex items-center justify-center">
                <img :src="agent.image" :alt="agent.name" class="w-full h-full object-cover">
              </div>
              <h3 class="text-white font-semibold mb-1 text-xs">{{ agent.name }}</h3>
            </div>
          </div>
        </div>

        <!-- Main Content Card -->
        <div class="bg-white/10 backdrop-blur-lg rounded-3xl border border-white/20 shadow-2xl overflow-hidden max-w-6xl mx-auto">
          <div class="grid lg:grid-cols-2 min-h-[500px]">
            <!-- Left Side - Form -->
            <div class="p-8 lg:p-12">
              <!-- Form Content -->
              <form @submit.prevent="handleSubmit" class="space-y-6">
                <!-- What drives you -->
                <div>
                  <label class="block text-sm font-semibold text-white mb-3 uppercase tracking-wide">
                    What drives you as a YouTuber?
                  </label>
                  <textarea
                    v-model="formData.motivation"
                    placeholder="Share what motivates you to create content..."
                    class="w-full p-4 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent backdrop-blur-sm resize-none"
                    rows="3"
                  ></textarea>
                </div>

                <!-- Niche and Content Type -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label class="block text-sm font-semibold text-white mb-3 uppercase tracking-wide">
                      Niche
                    </label>
                    <select
                      v-model="formData.niche"
                      class="w-full p-4 bg-white/10 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent backdrop-blur-sm"
                    >
                      <option value="" class="text-gray-800">Select your niche</option>
                      <option value="gaming" class="text-gray-800">Gaming</option>
                      <option value="tech" class="text-gray-800">Technology</option>
                      <option value="lifestyle" class="text-gray-800">Lifestyle</option>
                      <option value="education" class="text-gray-800">Education</option>
                      <option value="entertainment" class="text-gray-800">Entertainment</option>
                      <option value="business" class="text-gray-800">Business</option>
                      <option value="health" class="text-gray-800">Health & Fitness</option>
                      <option value="travel" class="text-gray-800">Travel</option>
                      <option value="food" class="text-gray-800">Food & Cooking</option>
                      <option value="music" class="text-gray-800">Music</option>
                      <option value="art" class="text-gray-800">Art & Design</option>
                      <option value="other" class="text-gray-800">Other</option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-sm font-semibold text-white mb-3 uppercase tracking-wide">
                      Content Type
                    </label>
                    <select
                      v-model="formData.contentType"
                      class="w-full p-4 bg-white/10 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent backdrop-blur-sm"
                    >
                      <option value="" class="text-gray-800">Select content type</option>
                      <option value="tutorials" class="text-gray-800">Tutorials</option>
                      <option value="vlogs" class="text-gray-800">Vlogs</option>
                      <option value="reviews" class="text-gray-800">Reviews</option>
                      <option value="entertainment" class="text-gray-800">Entertainment</option>
                      <option value="educational" class="text-gray-800">Educational</option>
                      <option value="live-streams" class="text-gray-800">Live Streams</option>
                      <option value="shorts" class="text-gray-800">YouTube Shorts</option>
                      <option value="music" class="text-gray-800">Music Videos</option>
                      <option value="comedy" class="text-gray-800">Comedy</option>
                      <option value="documentary" class="text-gray-800">Documentary</option>
                    </select>
                  </div>
                </div>

                <!-- Upload Frequency and Target Goal -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label class="block text-sm font-semibold text-white mb-3 uppercase tracking-wide">
                      Upload Frequency
                    </label>
                    <select
                      v-model="formData.uploadFrequency"
                      class="w-full p-4 bg-white/10 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent backdrop-blur-sm"
                    >
                      <option value="" class="text-gray-800">Select frequency</option>
                      <option value="daily" class="text-gray-800">Daily</option>
                      <option value="weekly" class="text-gray-800">Weekly</option>
                      <option value="bi-weekly" class="text-gray-800">Bi-weekly</option>
                      <option value="monthly" class="text-gray-800">Monthly</option>
                      <option value="irregular" class="text-gray-800">Irregular</option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-sm font-semibold text-white mb-3 uppercase tracking-wide">
                      Target Goal
                    </label>
                    <select
                      v-model="formData.targetGoal"
                      class="w-full p-4 bg-white/10 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent backdrop-blur-sm"
                    >
                      <option value="" class="text-gray-800">Select your goal</option>
                      <option value="subscribers" class="text-gray-800">Grow Subscribers</option>
                      <option value="views" class="text-gray-800">Increase Views</option>
                      <option value="engagement" class="text-gray-800">Boost Engagement</option>
                      <option value="monetization" class="text-gray-800">Monetization</option>
                      <option value="brand" class="text-gray-800">Build Brand</option>
                      <option value="community" class="text-gray-800">Build Community</option>
                    </select>
                  </div>
                </div>

                <!-- Additional Notes -->
                <div>
                  <label class="block text-sm font-semibold text-white mb-3 uppercase tracking-wide">
                    Additional Notes
                  </label>
                  <textarea
                    v-model="formData.additionalNotes"
                    placeholder="Tell us about your future plans..."
                    class="w-full p-4 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent backdrop-blur-sm resize-none"
                    rows="3"
                  ></textarea>
                </div>

                <!-- Submit Button -->
                <div class="pt-6">
                  <button
                    type="submit"
                    :disabled="!isFormValid"
                    class="w-full bg-gradient-to-r from-orange-500 to-orange-600 text-white font-bold py-4 px-8 rounded-xl hover:from-orange-600 hover:to-orange-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105"
                  >
                    Connect Your YouTube Channel
                  </button>
                </div>
              </form>
            </div>

            <!-- Right Side - Visual Content -->
            <div class="relative bg-gradient-to-br from-forest-600 to-orange-600 p-8 lg:p-12 flex items-center justify-center">
              <!-- AI Robot Illustration -->
              <div class="text-center">
                <h3 class="text-2xl font-bold text-white mb-6">
                  Meet Your AI Agents
                </h3>

                <!-- Agent Grid -->
                <div class="grid grid-cols-2 gap-4 max-w-md mx-auto">
                  <div
                    v-for="agent in agents"
                    :key="'sidebar-' + agent.id"
                    @click="selectAgent(agent.id)"
                    class="bg-white/10 backdrop-blur-lg rounded-2xl p-4 text-center cursor-pointer transition-all duration-300 hover:bg-white/20 hover:scale-105 border border-white/20"
                    :class="selectedAgent === agent.id ? 'scale-105' : ''"
                    :style="selectedAgent === agent.id ? {
                      backgroundColor: agent.color + '30',
                      borderColor: agent.color,
                      boxShadow: `0 0 30px ${agent.color}80`
                    } : {}"
                  >
                    <div class="w-12 h-12 mx-auto mb-2 rounded-xl overflow-hidden bg-white/20 flex items-center justify-center">
                      <img :src="agent.image" :alt="agent.name" class="w-full h-full object-cover">
                    </div>
                    <h4 class="text-white font-semibold mb-1 text-xs">{{ agent.name }}</h4>
                    <p class="text-gray-300 text-xs leading-tight">{{ agent.description }}</p>
                  </div>
                </div>

                <p class="text-gray-200 text-sm mt-6 leading-relaxed">
                  Choose your specialized AI agent to get personalized content strategies and growth insights.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

// Remove the default layout with header and add guest middleware
definePageMeta({
  layout: false,
  middleware: 'guest'
})

// Agent data with images from the public folder
const agents = ref([
  {
    id: 'boss',
    name: 'Boss Agent',
    description: 'Strategic Leadership',
    image: '/BossAgent.png',
    color: '#FF6B35'
  },
  {
    id: 1,
    name: 'Agent 1',
    description: 'Content Creation',
    image: '/optimized/Agent1.jpg',
    color: '#4ECDC4'
  },
  {
    id: 2,
    name: 'Agent 2',
    description: 'Data & Insights',
    image: '/optimized/Agent2.jpg',
    color: '#FFEAA7'
  },
  {
    id: 3,
    name: 'Agent 3',
    description: 'Channel Growth',
    image: '/optimized/Agent3.jpg',
    color: '#96CEB4'
  },
  {
    id: 4,
    name: 'Agent 4',
    description: 'Community Building',
    image: '/optimized/Agent4.jpg',
    color: '#FFEAA7'
  },
  {
    id: 5,
    name: 'Agent 5',
    description: 'Optimization',
    image: '/optimized/Agent5.jpg',
    color: '#DDA0DD'
  }
])

// Selected agent
const selectedAgent = ref('boss') // Default to Boss Agent

// Form data
const formData = ref({
  motivation: '',
  niche: '',
  contentType: '',
  uploadFrequency: '',
  targetGoal: '',
  additionalNotes: '',
})

// Form validation
const isFormValid = computed(() => {
  return formData.value.motivation.trim() !== '' &&
         formData.value.niche !== '' &&
         formData.value.contentType !== '' &&
         selectedAgent.value !== null
})

// Select agent function
const selectAgent = (agentId) => {
  selectedAgent.value = agentId
}

// Handle form submission
const handleSubmit = () => {
  if (isFormValid.value) {
    console.log('Form data:', {
      ...formData.value,
      selectedAgent: selectedAgent.value
    })
    // Navigate to dashboard after setup
    navigateTo('/dashboard')
  }
}
</script>

<style scoped>
/* Animation classes */
@keyframes blob {
  0% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  100% {
    transform: translate(0px, 0px) scale(1);
  }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

.animation-delay-1000 {
  animation-delay: 1s;
}

/* Agent card styles */
.agent-card.selected {
  @apply bg-white/30 border-orange-400 scale-105;
  box-shadow: 0 0 30px rgba(249, 115, 22, 0.5);
}

.agent-card:hover {
  transform: translateY(-5px) scale(1.05);
}

/* Custom scrollbar for textareas */
textarea::-webkit-scrollbar {
  width: 6px;
}

textarea::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

textarea::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

textarea::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>
