<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-gray-800">
    <div class="max-w-7xl mx-auto px-6 py-4">
      <div class="flex items-center justify-between">
        <!-- Logo -->
        <div class="flex items-center space-x-3">
          <img
            src="/MYTALogo.png"
            alt="MYTA Logo"
            class="h-8 w-auto"
          />
          <span class="text-xl font-bold bg-gradient-to-r from-pink-500 to-purple-600 bg-clip-text text-transparent">
            MYTA
          </span>
        </div>

        <!-- Navigation -->
        <nav class="hidden md:flex items-center space-x-8">
          <a href="#features" class="text-gray-300 hover:text-white transition-colors">
            Features
          </a>
          <a href="#agents" class="text-gray-300 hover:text-white transition-colors">
            Agent Team
          </a>
          <a href="#pricing" class="text-gray-300 hover:text-white transition-colors">
            Pricing
          </a>
          <a href="#faq" class="text-gray-300 hover:text-white transition-colors">
            FAQ
          </a>
        </nav>

        <!-- CTA Buttons -->
        <div class="flex items-center space-x-4">
          <!-- Login Button (for existing users) -->
          <button 
            @click="navigateToLogin"
            class="hidden sm:block text-gray-300 hover:text-white transition-colors"
          >
            Sign In
          </button>
          
          <!-- Main CTA -->
          <button 
            @click="scrollToWaitlist"
            class="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-6 py-2 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105"
          >
            Join Waitlist
          </button>
        </div>

        <!-- Mobile Menu Button -->
        <button 
          @click="toggleMobileMenu"
          class="md:hidden text-white p-2"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
        </button>
      </div>

      <!-- Mobile Menu -->
      <div v-if="showMobileMenu" class="md:hidden mt-4 pb-4 border-t border-gray-800 pt-4">
        <nav class="flex flex-col space-y-4">
          <a href="#features" @click="closeMobileMenu" class="text-gray-300 hover:text-white transition-colors">
            Features
          </a>
          <a href="#agents" @click="closeMobileMenu" class="text-gray-300 hover:text-white transition-colors">
            Agent Team
          </a>
          <a href="#pricing" @click="closeMobileMenu" class="text-gray-300 hover:text-white transition-colors">
            Pricing
          </a>
          <a href="#faq" @click="closeMobileMenu" class="text-gray-300 hover:text-white transition-colors">
            FAQ
          </a>
          <button 
            @click="navigateToLogin"
            class="text-left text-gray-300 hover:text-white transition-colors"
          >
            Sign In
          </button>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
const showMobileMenu = ref(false)

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
}

const scrollToWaitlist = () => {
  const element = document.getElementById('waitlist')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
  closeMobileMenu()
}

const navigateToLogin = () => {
  navigateTo('/login')
}

// Close mobile menu when clicking outside
onMounted(() => {
  document.addEventListener('click', (e) => {
    if (!e.target.closest('header')) {
      showMobileMenu.value = false
    }
  })
})
</script>
