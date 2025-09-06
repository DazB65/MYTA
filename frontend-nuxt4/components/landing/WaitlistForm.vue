<template>
  <div class="w-full">
    <!-- Success State -->
    <div v-if="isSubmitted" class="text-center py-8">
      <div class="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
      </div>
      <h3 class="text-2xl font-bold text-white mb-2">You're on the list! 🎉</h3>
      <p class="text-gray-300 mb-6">
        We'll notify you as soon as MYTA is ready. Get ready to supercharge your YouTube growth!
      </p>
      <button 
        @click="resetForm"
        class="text-pink-400 hover:text-pink-300 transition-colors"
      >
        Join another email →
      </button>
    </div>

    <!-- Form State -->
    <form v-else @submit.prevent="submitForm" class="space-y-4">
      <!-- Email Input -->
      <div class="relative">
        <input
          v-model="email"
          type="email"
          placeholder="Enter your email address"
          required
          class="w-full px-6 py-4 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-all"
          :class="{ 'border-red-500': emailError }"
        />
        <div v-if="emailError" class="absolute -bottom-6 left-0 text-red-400 text-sm">
          {{ emailError }}
        </div>
      </div>

      <!-- Channel Info (Optional) -->
      <div class="relative">
        <input
          v-model="channelName"
          type="text"
          placeholder="YouTube channel name (optional)"
          class="w-full px-6 py-4 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-all"
        />
      </div>

      <!-- Subscriber Count (Optional) -->
      <div class="relative">
        <select
          v-model="subscriberRange"
          class="w-full px-6 py-4 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-all"
        >
          <option value="">Subscriber count (optional)</option>
          <option value="0-100">0 - 100 subscribers</option>
          <option value="100-1k">100 - 1K subscribers</option>
          <option value="1k-10k">1K - 10K subscribers</option>
          <option value="10k-100k">10K - 100K subscribers</option>
          <option value="100k-1m">100K - 1M subscribers</option>
          <option value="1m+">1M+ subscribers</option>
        </select>
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        :disabled="isLoading || !email"
        style="background: #F97316 !important; background-color: #F97316 !important;"
        class="w-full text-white px-8 py-4 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
      >
        <span v-if="!isLoading">Join Waitlist</span>
        <span v-else class="flex items-center space-x-2">
          <svg class="animate-spin w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          <span>Joining...</span>
        </span>
      </button>

      <!-- Privacy Notice -->
      <p class="text-xs text-gray-400 text-center">
        By joining, you agree to receive updates about MYTA. 
        <br />
        We respect your privacy and won't spam you.
      </p>
    </form>


  </div>
</template>

<script setup>
const email = ref('')
const channelName = ref('')
const subscriberRange = ref('')
const isLoading = ref(false)
const isSubmitted = ref(false)
const emailError = ref('')

const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

const submitForm = async () => {
  // Reset errors
  emailError.value = ''
  
  // Validate email
  if (!validateEmail(email.value)) {
    emailError.value = 'Please enter a valid email address'
    return
  }

  isLoading.value = true

  try {
    // TODO: Replace with actual API call to your backend
    const response = await $fetch('/api/waitlist', {
      method: 'POST',
      body: {
        email: email.value,
        channelName: channelName.value,
        subscriberRange: subscriberRange.value,
        timestamp: new Date().toISOString()
      }
    })

    // Simulate API delay for now
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    isSubmitted.value = true
    
    // Track conversion (you can add analytics here)
    // gtag('event', 'waitlist_signup', { email: email.value })
    
  } catch (error) {
    console.error('Waitlist signup error:', error)
    emailError.value = 'Something went wrong. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const resetForm = () => {
  email.value = ''
  channelName.value = ''
  subscriberRange.value = ''
  isSubmitted.value = false
  emailError.value = ''
}

const scrollToFeatures = () => {
  const element = document.getElementById('features')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

const scrollToAgents = () => {
  const element = document.getElementById('agents')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>
