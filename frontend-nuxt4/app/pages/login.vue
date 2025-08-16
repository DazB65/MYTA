<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
    <!-- Background Pattern -->
    <div class="absolute inset-0 bg-[url('/grid-pattern.svg')] opacity-10" />
    
    <!-- Content Container -->
    <div class="relative flex min-h-screen items-center justify-center p-6">
      <!-- Login Card -->
      <div class="w-full max-w-md">
        <!-- Logo Section -->
        <div class="mb-8 text-center">
          <div class="flex items-center justify-center mb-4">
            <img src="/MY YT AGENT.png" alt="MYTA Logo" class="w-32 h-32">
          </div>
          <h1 class="text-3xl font-bold text-white">Welcome Back</h1>
          <p class="text-gray-400">Sign in to your MYTA account</p>
        </div>
        
        <!-- Login Form -->
        <div class="rounded-2xl bg-white/10 backdrop-blur-lg p-8 border border-white/20">
          <form @submit.prevent="handleLogin" class="space-y-6">
            <!-- Email Field -->
            <div>
              <label for="email" class="block text-sm font-semibold text-white mb-2">
                Email Address
              </label>
              <input
                id="email"
                v-model="formData.email"
                type="email"
                required
                class="w-full p-4 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-transparent backdrop-blur-sm"
                placeholder="Enter your email"
              >
            </div>

            <!-- Password Field -->
            <div>
              <label for="password" class="block text-sm font-semibold text-white mb-2">
                Password
              </label>
              <div class="relative">
                <input
                  id="password"
                  v-model="formData.password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  class="w-full p-4 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-transparent backdrop-blur-sm pr-12"
                  placeholder="Enter your password"
                >
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                >
                  <span v-if="showPassword">👁️</span>
                  <span v-else>🙈</span>
                </button>
              </div>
            </div>

            <!-- Remember Me & Forgot Password -->
            <div class="flex items-center justify-between">
              <label class="flex items-center">
                <input
                  v-model="formData.rememberMe"
                  type="checkbox"
                  class="w-4 h-4 text-pink-500 bg-white/10 border-white/20 rounded focus:ring-pink-400 focus:ring-2"
                >
                <span class="ml-2 text-sm text-gray-300">Remember me</span>
              </label>
              <NuxtLink
                to="/forgot-password"
                class="text-sm text-pink-400 hover:text-pink-300 transition-colors"
              >
                Forgot password?
              </NuxtLink>
            </div>

            <!-- Error Message -->
            <div v-if="error" class="p-4 bg-red-500/20 border border-red-500/30 rounded-xl">
              <p class="text-red-300 text-sm">{{ error }}</p>
            </div>

            <!-- Login Button -->
            <button
              type="submit"
              :disabled="loading"
              class="w-full bg-gradient-to-r from-pink-500 to-purple-600 text-white font-semibold py-4 px-6 rounded-xl hover:from-pink-600 hover:to-purple-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              <span v-if="loading" class="mr-2">⏳</span>
              {{ loading ? 'Signing In...' : 'Sign In' }}
            </button>

            <!-- Divider -->
            <div class="relative">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-white/20"></div>
              </div>
              <div class="relative flex justify-center text-sm">
                <span class="px-2 bg-gray-900 text-gray-400">Or continue with</span>
              </div>
            </div>

            <!-- OAuth Buttons -->
            <div class="space-y-3">
              <button
                type="button"
                @click="handleGoogleLogin"
                class="w-full bg-white/10 border border-white/20 text-white font-semibold py-4 px-6 rounded-xl hover:bg-white/20 transition-all duration-300 flex items-center justify-center"
              >
                <span class="mr-2">🔗</span>
                Continue with Google
              </button>
            </div>
          </form>
        </div>
        
        <!-- Sign Up Link -->
        <div class="mt-8 text-center">
          <p class="text-gray-400">
            Don't have an account?
            <NuxtLink
              to="/create-profile"
              class="text-pink-400 hover:text-pink-300 transition-colors font-semibold"
            >
              Sign up here
            </NuxtLink>
          </p>
        </div>
        
        <!-- Footer -->
        <div class="mt-8 text-center text-sm text-gray-400">
          <p>&copy; 2025 MYTA. All rights reserved.</p>
        </div>
      </div>
    </div>
    
    <!-- Floating Elements -->
    <div class="absolute top-10 left-10 h-20 w-20 rounded-full bg-pink-500/20 blur-xl" />
    <div class="absolute bottom-10 right-10 h-32 w-32 rounded-full bg-purple-500/20 blur-xl" />
    <div class="absolute top-1/2 right-20 h-16 w-16 rounded-full bg-blue-500/20 blur-xl" />
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useAuthStore } from '../../stores/auth'

// Remove the default layout
definePageMeta({
  layout: false
})

// SEO
useHead({
  title: 'Login - MYTA',
  meta: [
    { name: 'description', content: 'Sign in to your MYTA account and access your AI-powered YouTube analytics dashboard.' },
    { name: 'robots', content: 'noindex, nofollow' }
  ]
})

// Store
const authStore = useAuthStore()
const router = useRouter()

// Form state
const formData = reactive({
  email: '',
  password: '',
  rememberMe: false
})

const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

// Handle login
const handleLogin = async () => {
  if (!formData.email || !formData.password) {
    error.value = 'Please fill in all fields'
    return
  }

  loading.value = true
  error.value = ''

  try {
    await authStore.login({
      email: formData.email,
      password: formData.password
    })

    // Redirect to dashboard on success
    await router.push('/dashboard')
  } catch (err) {
    error.value = err.message || 'Login failed. Please check your credentials.'
  } finally {
    loading.value = false
  }
}

// Handle Google OAuth login
const handleGoogleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    // TODO: Implement Google OAuth flow
    error.value = 'Google login coming soon!'
  } catch (err) {
    error.value = err.message || 'Google login failed'
  } finally {
    loading.value = false
  }
}

// Auto-redirect if already logged in
onMounted(() => {
  if (authStore.isLoggedIn) {
    router.push('/dashboard')
  }
})
</script>

<style scoped>
/* Login page animations */
.login-enter-active,
.login-leave-active {
  transition: all 0.4s ease;
}

.login-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.login-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
