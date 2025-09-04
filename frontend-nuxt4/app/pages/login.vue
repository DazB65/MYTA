<template>
  <div class="min-h-screen bg-gradient-to-br from-forest-900 via-forest-800 to-forest-900">
    <!-- Background Pattern -->
    <div class="absolute inset-0 bg-[url('/grid-pattern.svg')] opacity-10" />

    <!-- Logo in Top Right -->
    <div class="absolute -top-24 right-0 z-20">
      <img src="/MY YT AGENT.png" alt="MYTA Logo" class="w-128 h-128">
    </div>

    <!-- Content Container -->
    <div class="relative flex min-h-screen items-center justify-center p-6">
      <!-- Login Card -->
      <div class="w-full max-w-md">
        <!-- Welcome Section -->
        <div class="mb-8 text-center">
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
                class="w-full p-4 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent backdrop-blur-sm"
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
                  class="w-full p-4 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent backdrop-blur-sm pr-12"
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
                  class="w-4 h-4 text-orange-500 bg-white/10 border-white/20 rounded focus:ring-orange-400 focus:ring-2"
                >
                <span class="ml-2 text-sm text-gray-300">Remember me</span>
              </label>
              <NuxtLink
                to="/forgot-password"
                class="text-sm text-orange-400 hover:text-orange-300 transition-colors"
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
              class="w-full bg-gradient-to-r from-orange-500 to-orange-600 text-white font-semibold py-4 px-6 rounded-xl hover:from-orange-600 hover:to-orange-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
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
                <span class="px-2 bg-forest-900 text-gray-400">Or continue with</span>
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
              to="/signup"
              class="text-orange-400 hover:text-orange-300 transition-colors font-semibold"
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

    <!-- Full Screen Agent Background -->
    <div class="absolute inset-0 pointer-events-none">
      <img src="/Agent1.png" alt="Agent 1" class="w-full h-full object-cover opacity-10">
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useAuthStore } from '../../stores/auth'

// Remove the default layout and add guest middleware
definePageMeta({
  layout: false,
  middleware: 'guest'
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

    // Redirect to original destination or dashboard
    const route = useRoute();
    const redirectTo = route.query.redirect || '/dashboard';
    await router.push(redirectTo);
  } catch (err) {
    error.value = err.message || 'Login failed. Please check your credentials.';
  } finally {
    loading.value = false;
  }
}

// Handle Google OAuth login
const handleGoogleLogin = async () => {
  loading.value = true;
  error.value = '';

  try {
    // TODO: Implement Google OAuth flow
    error.value = 'Google login coming soon!';
  } catch (err) {
    error.value = err.message || 'Google login failed';
  } finally {
    loading.value = false;
  }
};

// Auto-redirect if already logged in
onMounted(() => {
  if (authStore.isLoggedIn) {
    router.push('/dashboard');
  }
});
</script>

<style scoped>
/* Floating animations for agents */
@keyframes float-slow {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(5deg);
  }
}

@keyframes float-medium {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-15px) rotate(-3deg);
  }
}

@keyframes float-fast {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-10px) rotate(3deg);
  }
}

.animate-float-slow {
  animation: float-slow 6s ease-in-out infinite;
}

.animate-float-medium {
  animation: float-medium 4s ease-in-out infinite;
}

.animate-float-fast {
  animation: float-fast 3s ease-in-out infinite;
}

.animation-delay-500 {
  animation-delay: 0.5s;
}

.animation-delay-1000 {
  animation-delay: 1s;
}

.animation-delay-1500 {
  animation-delay: 1.5s;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-3000 {
  animation-delay: 3s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}
</style>

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
