<template>
  <div class="min-h-screen bg-gradient-to-br from-forest-900 via-forest-800 to-gray-900 relative overflow-hidden">
    <!-- Logo in Top Right -->
    <div class="absolute -top-20 right-4 z-20">
      <img src="/MYTALogo.png" alt="MYTA Logo" class="h-96 w-auto">
    </div>

    <!-- Animated Background Elements -->
    <div class="absolute inset-0">
      <!-- Floating Orbs -->
      <div class="absolute top-20 left-10 w-32 h-32 bg-gradient-to-r from-forest-500/20 to-orange-500/20 rounded-full blur-xl animate-pulse"></div>
      <div class="absolute top-40 right-20 w-24 h-24 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 rounded-full blur-xl animate-bounce"></div>
      <div class="absolute bottom-32 left-1/4 w-40 h-40 bg-gradient-to-r from-orange-500/20 to-red-500/20 rounded-full blur-xl animate-pulse delay-1000"></div>
      
      <!-- Grid Pattern -->
      <div class="absolute inset-0 opacity-50">
        <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent"></div>
      </div>
    </div>

    <div class="relative z-10 flex min-h-screen">
      <!-- Left Side - Hero Content -->
      <div class="flex-1 flex items-center justify-center p-8 lg:p-12">
        <div class="max-w-lg">
          <!-- Hero Text -->
          <div class="mb-8">
            <h1 class="text-4xl lg:text-5xl font-bold text-white mb-4 leading-tight">
              <span class="bg-gradient-to-r from-forest-400 to-orange-400 bg-clip-text text-transparent">
                Agents are ready to launch
              </span>
            </h1>
            <p class="text-xl text-gray-300 mb-6">
              Join thousands of creators who've transformed their channels with AI-powered growth strategies.
            </p>
          </div>

          <!-- Value Props -->
          <div class="space-y-4 mb-8">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
              </div>
              <span class="text-gray-300">6 specialized AI agents working 24/7 for your channel</span>
            </div>
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-gradient-to-r from-blue-400 to-cyan-500 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
              </div>
              <span class="text-gray-300">AI-powered content strategy & optimization</span>
            </div>
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-gradient-to-r from-forest-400 to-orange-500 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
              </div>
              <span class="text-gray-300">Real-time analytics & growth insights</span>
            </div>
          </div>


        </div>
      </div>

      <!-- Right Side - Signup Form -->
      <div class="flex-1 flex items-center justify-center p-8 lg:p-12">
        <div class="w-full max-w-md">
          <!-- Form Container -->
          <div class="bg-white/10 backdrop-blur-xl rounded-2xl p-8 border border-white/20 shadow-2xl">
            <div class="text-center mb-8">
              <h2 class="text-2xl font-bold text-white mb-2">Start Your Journey</h2>
              <p class="text-gray-300">Create your account in 30 seconds</p>
            </div>

            <!-- Signup Form -->
            <form @submit.prevent="handleSignup" class="space-y-6">
              <!-- Name Field -->
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Full Name</label>
                <input
                  v-model="form.name"
                  type="text"
                  required
                  class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                  placeholder="Enter your full name"
                >
              </div>

              <!-- Email Field -->
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Email Address</label>
                <input
                  v-model="form.email"
                  type="email"
                  required
                  class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                  placeholder="Enter your email"
                >
              </div>

              <!-- Password Field -->
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Password</label>
                <div class="relative">
                  <input
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    required
                    class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all pr-12"
                    placeholder="Create a strong password"
                  >
                  <button
                    type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                  >
                    {{ showPassword ? '🙈' : '👁️' }}
                  </button>
                </div>
              </div>

              <!-- Confirm Password Field -->
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Confirm Password</label>
                <input
                  v-model="form.confirmPassword"
                  type="password"
                  required
                  class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                  placeholder="Confirm your password"
                >
              </div>

              <!-- Terms Checkbox -->
              <div class="flex items-start space-x-3">
                <input
                  v-model="form.acceptTerms"
                  type="checkbox"
                  required
                  class="mt-1 w-4 h-4 text-orange-500 bg-white/10 border-white/20 rounded focus:ring-orange-500 focus:ring-2"
                >
                <label class="text-sm text-gray-300">
                  I agree to the 
                  <a href="#" class="text-orange-400 hover:text-orange-300 underline">Terms of Service</a>
                  and
                  <a href="#" class="text-orange-400 hover:text-orange-300 underline">Privacy Policy</a>
                </label>
              </div>

              <!-- Error Message -->
              <div v-if="error" class="bg-red-500/20 border border-red-500/50 rounded-lg p-3">
                <p class="text-red-300 text-sm">{{ error }}</p>
              </div>

              <!-- Submit Button -->
              <button
                type="submit"
                :disabled="loading"
                class="w-full bg-gradient-to-r from-forest-500 to-orange-600 hover:from-forest-600 hover:to-orange-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                <span v-if="loading" class="flex items-center justify-center">
                  <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Creating your account...
                </span>
                <span v-else>🚀 Agents are ready to launch</span>
              </button>

              <!-- Divider -->
              <div class="relative my-6">
                <div class="absolute inset-0 flex items-center">
                  <div class="w-full border-t border-white/20"></div>
                </div>
                <div class="relative flex justify-center text-sm">
                  <span class="px-2 bg-forest-900 text-gray-400">Or continue with</span>
                </div>
              </div>

              <!-- Google Signup -->
              <button
                type="button"
                class="w-full bg-white/10 hover:bg-white/20 border border-white/20 text-white font-medium py-3 px-6 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2"
              >
                <svg class="w-5 h-5" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                <span>Continue with Google</span>
              </button>
            </form>

            <!-- Login Link -->
            <div class="text-center mt-6">
              <p class="text-gray-400">
                Already have an account? 
                <NuxtLink to="/login" class="text-orange-400 hover:text-orange-300 font-medium underline">
                  Sign in here
                </NuxtLink>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Full Screen Agent Background -->
    <div class="absolute inset-0 pointer-events-none">
      <img src="/Agent1.png" alt="Agent 1" class="w-full h-full object-cover opacity-10">
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Page metadata
definePageMeta({
  title: 'Sign Up - MYTA',
  description: 'Join MYTA and transform your YouTube channel with AI-powered growth strategies',
  layout: false
})

// Form state
const form = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false
})

const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

// Handle signup
const handleSignup = async () => {
  error.value = ''
  
  // Validation
  if (form.value.password !== form.value.confirmPassword) {
    error.value = 'Passwords do not match'
    return
  }
  
  if (form.value.password.length < 8) {
    error.value = 'Password must be at least 8 characters long'
    return
  }
  
  if (!form.value.acceptTerms) {
    error.value = 'Please accept the terms and conditions'
    return
  }
  
  loading.value = true
  
  try {
    // TODO: Implement actual signup logic
    console.log('Signup form data:', form.value)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Redirect to onboarding/profile setup
    await navigateTo('/create-profile')
  } catch (err) {
    error.value = 'Something went wrong. Please try again.'
    console.error('Signup error:', err)
  } finally {
    loading.value = false
  }
}
</script>
