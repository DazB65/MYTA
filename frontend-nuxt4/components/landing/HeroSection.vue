<template>
  <section class="relative min-h-screen flex items-start justify-center overflow-hidden pt-4">
    <!-- Background Effects -->
    <div class="absolute inset-0 bg-gradient-to-br from-forest-900 via-forest-900 to-forest-800/20"></div>
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(249,115,22,0.1),transparent_70%)]"></div>

    <!-- Animated Background Elements -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-orange-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-forest-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
    </div>

    <!-- Main Content -->
    <div class="relative z-10 max-w-6xl mx-auto px-6 text-center">
      <!-- Logo -->
      <div class="mb-1 flex justify-center">
        <div class="relative">
          <img
            src="/MY YT AGENT.png"
            alt="MYTA Logo"
            class="h-96 md:h-[30rem] w-auto drop-shadow-2xl"
          />
          <!-- Glow effect behind logo -->
          <div class="absolute inset-0 bg-gradient-to-r from-orange-500/20 to-forest-400/20 blur-3xl scale-110 -z-10"></div>
        </div>
      </div>

      <!-- Main Headline -->
      <h1 class="text-5xl md:text-7xl font-bold mb-6 leading-tight">
        Your
        <span class="bg-gradient-to-r from-orange-500 via-forest-400 to-orange-500 bg-clip-text text-transparent animate-gradient">
          Agent Team
        </span>
        <br />
        for YouTube Growth
      </h1>

      <!-- Subheadline -->
      <p class="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
        Join the waitlist for the agent-powered platform that helps creators
        <span class="text-orange-400 font-semibold">optimize content</span>,
        <span class="text-forest-400 font-semibold">analyze performance</span>, and
        <span class="text-orange-400 font-semibold">scale their channels</span>
        with a team of specialized agents.
      </p>

      <!-- Key Benefits -->
      <div class="flex flex-wrap justify-center gap-4 mb-12">
        <div class="flex items-center space-x-2 bg-gray-800/50 px-4 py-2 rounded-full">
          <div class="w-2 h-2 bg-green-400 rounded-full"></div>
          <span class="text-sm text-gray-300">5 Agent Specialists</span>
        </div>
        <div class="flex items-center space-x-2 bg-forest-800/50 px-4 py-2 rounded-full">
          <div class="w-2 h-2 bg-forest-400 rounded-full"></div>
          <span class="text-sm text-gray-300">Real-time Analytics</span>
        </div>
        <div class="flex items-center space-x-2 bg-forest-800/50 px-4 py-2 rounded-full">
          <div class="w-2 h-2 bg-orange-400 rounded-full"></div>
          <span class="text-sm text-gray-300">Content Optimization</span>
        </div>
        <div class="flex items-center space-x-2 bg-forest-800/50 px-4 py-2 rounded-full">
          <div class="w-2 h-2 bg-forest-400 rounded-full"></div>
          <span class="text-sm text-gray-300">Strategy Planning</span>
        </div>
      </div>

      <!-- Agent Team Section -->
      <div class="mb-12">
        <!-- Section Header -->
        <div class="text-center mb-8">
          <h2 class="text-2xl md:text-3xl font-bold mb-3">
            Meet your
            <span class="bg-gradient-to-r from-orange-500 to-forest-400 bg-clip-text text-transparent">
              agent team
            </span>
          </h2>
        </div>

        <!-- Agents Grid -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 max-w-4xl mx-auto">
          <!-- Fred - Executive Agent -->
          <div class="group bg-gradient-to-br from-orange-500/10 to-red-500/10 border border-orange-500/20 rounded-lg p-4 hover:border-orange-500/50 transition-all duration-300 hover:transform hover:scale-105 text-center">
            <div class="relative mb-3 flex justify-center">
              <img
                src="/BossAgent.png"
                alt="Fred - Executive Agent"
                class="w-12 h-12 rounded-full border-2 border-orange-500"
              />
              <div class="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-background"></div>
            </div>
            <h3 class="text-sm font-bold text-white mb-1">Fred</h3>
            <p class="text-orange-400 text-xs font-semibold">Executive</p>
          </div>

          <!-- Alex - Analytics Expert -->
          <div class="group bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border border-blue-500/20 rounded-lg p-4 hover:border-blue-500/50 transition-all duration-300 hover:transform hover:scale-105 text-center">
            <div class="relative mb-3 flex justify-center">
              <img
                src="/Agent1.png"
                alt="Alex - Analytics Expert"
                class="w-12 h-12 rounded-full border-2 border-blue-500"
              />
              <div class="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-background"></div>
            </div>
            <h3 class="text-sm font-bold text-white mb-1">Alex</h3>
            <p class="text-blue-400 text-xs font-semibold">Analytics</p>
          </div>

          <!-- Maya - Performance Specialist -->
          <div class="group bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/20 rounded-lg p-4 hover:border-green-500/50 transition-all duration-300 hover:transform hover:scale-105 text-center">
            <div class="relative mb-3 flex justify-center">
              <img
                src="/Agent3.png"
                alt="Maya - Performance Specialist"
                class="w-12 h-12 rounded-full border-2 border-green-500"
              />
              <div class="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-background"></div>
            </div>
            <h3 class="text-sm font-bold text-white mb-1">Maya</h3>
            <p class="text-green-400 text-xs font-semibold">Performance</p>
          </div>

          <!-- Levi - Strategy Coordinator -->
          <div class="group bg-gradient-to-br from-yellow-500/10 to-orange-500/10 border border-yellow-500/20 rounded-lg p-4 hover:border-yellow-500/50 transition-all duration-300 hover:transform hover:scale-105 text-center">
            <div class="relative mb-3 flex justify-center">
              <img
                src="/Agent2.png"
                alt="Levi - Strategy Coordinator"
                class="w-12 h-12 rounded-full border-2 border-yellow-500"
              />
              <div class="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-background"></div>
            </div>
            <h3 class="text-sm font-bold text-white mb-1">Levi</h3>
            <p class="text-yellow-400 text-xs font-semibold">Strategy</p>
          </div>

          <!-- Kai - Trend Analyst -->
          <div class="group bg-gradient-to-br from-purple-500/10 to-pink-500/10 border border-purple-500/20 rounded-lg p-4 hover:border-purple-500/50 transition-all duration-300 hover:transform hover:scale-105 text-center">
            <div class="relative mb-3 flex justify-center">
              <img
                src="/Agent5.png"
                alt="Kai - Trend Analyst"
                class="w-12 h-12 rounded-full border-2 border-purple-500"
              />
              <div class="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-background"></div>
            </div>
            <h3 class="text-sm font-bold text-white mb-1">Kai</h3>
            <p class="text-purple-400 text-xs font-semibold">Trends</p>
          </div>

          <!-- Zara - Community Manager -->
          <div class="group bg-gradient-to-br from-pink-500/10 to-rose-500/10 border border-pink-500/20 rounded-lg p-4 hover:border-pink-500/50 transition-all duration-300 hover:transform hover:scale-105 text-center">
            <div class="relative mb-3 flex justify-center">
              <img
                src="/Agent4.png"
                alt="Zara - Community Manager"
                class="w-12 h-12 rounded-full border-2 border-pink-500"
              />
              <div class="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-background"></div>
            </div>
            <h3 class="text-sm font-bold text-white mb-1">Zara</h3>
            <p class="text-pink-400 text-xs font-semibold">Community</p>
          </div>
        </div>
      </div>

      <!-- Waitlist Form -->
      <div id="waitlist" class="max-w-md mx-auto">
        <WaitlistForm />
      </div>

      <!-- Agent Team Section -->
      <div class="mt-16 mb-16">
        <!-- Section Header -->
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-bold mb-4">
            Meet your
            <span class="bg-gradient-to-r from-orange-500 to-forest-400 bg-clip-text text-transparent">
              agent team
            </span>
          </h2>
          <p class="text-lg text-gray-300 max-w-2xl mx-auto">
            Five specialized agents working together to analyze, optimize, and grow your YouTube channel.
          </p>
        </div>

        <!-- Agents Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Fred - Executive Agent -->
          <div class="group bg-gradient-to-br from-orange-500/10 to-red-500/10 border border-orange-500/20 rounded-xl p-6 hover:border-orange-500/50 transition-all duration-300 hover:transform hover:scale-105">
            <div class="flex items-center space-x-3 mb-4">
              <div class="relative">
                <img
                  src="/BossAgent.png"
                  alt="Fred - Executive Agent"
                  class="w-12 h-12 rounded-full border-2 border-orange-500"
                />
                <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-background"></div>
              </div>
              <div>
                <h3 class="text-lg font-bold text-white">Fred</h3>
                <p class="text-orange-400 text-sm font-semibold">Executive Agent</p>
              </div>
            </div>
            <p class="text-gray-300 text-sm mb-3">
              Your strategic leader who coordinates the entire agent team and provides executive-level insights.
            </p>
            <div class="space-y-1">
              <div class="flex items-center space-x-2 text-xs text-gray-400">
                <div class="w-1 h-1 bg-orange-400 rounded-full"></div>
                <span>Team coordination</span>
              </div>
              <div class="flex items-center space-x-2 text-xs text-gray-400">
                <div class="w-1 h-1 bg-orange-400 rounded-full"></div>
                <span>Strategic planning</span>
              </div>
            </div>
          </div>

          <!-- Alex - Analytics Expert -->
          <div class="group bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border border-blue-500/20 rounded-xl p-6 hover:border-blue-500/50 transition-all duration-300 hover:transform hover:scale-105">
            <div class="flex items-center space-x-3 mb-4">
              <div class="relative">
                <img
                  src="/Agent1.png"
                  alt="Alex - Analytics Expert"
                  class="w-12 h-12 rounded-full border-2 border-blue-500"
                />
                <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-background"></div>
              </div>
              <div>
                <h3 class="text-lg font-bold text-white">Alex</h3>
                <p class="text-blue-400 text-sm font-semibold">Analytics Expert</p>
              </div>
            </div>
            <p class="text-gray-300 text-sm mb-3">
              Deep-dives into your channel analytics to identify patterns and optimization strategies.
            </p>
            <div class="space-y-1">
              <div class="flex items-center space-x-2 text-xs text-gray-400">
                <div class="w-1 h-1 bg-blue-400 rounded-full"></div>
                <span>Performance analysis</span>
              </div>
              <div class="flex items-center space-x-2 text-xs text-gray-400">
                <div class="w-1 h-1 bg-blue-400 rounded-full"></div>
                <span>Data visualization</span>
              </div>
            </div>
          </div>

          <!-- Maya - Performance Specialist -->
          <div class="group bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/20 rounded-xl p-6 hover:border-green-500/50 transition-all duration-300 hover:transform hover:scale-105">
            <div class="flex items-center space-x-3 mb-4">
              <div class="relative">
                <img
                  src="/Agent3.png"
                  alt="Maya - Performance Specialist"
                  class="w-12 h-12 rounded-full border-2 border-green-500"
                />
                <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-background"></div>
              </div>
              <div>
                <h3 class="text-lg font-bold text-white">Maya</h3>
                <p class="text-green-400 text-sm font-semibold">Performance Specialist</p>
              </div>
            </div>
            <p class="text-gray-300 text-sm mb-3">
              Monitors your content performance in real-time and provides immediate alerts.
            </p>
            <div class="space-y-1">
              <div class="flex items-center space-x-2 text-xs text-gray-400">
                <div class="w-1 h-1 bg-green-400 rounded-full"></div>
                <span>Real-time monitoring</span>
              </div>
              <div class="flex items-center space-x-2 text-xs text-gray-400">
                <div class="w-1 h-1 bg-green-400 rounded-full"></div>
                <span>Performance alerts</span>
              </div>
            </div>
          </div>

          <!-- Levi - Strategy Coordinator -->
          <div class="group bg-gradient-to-br from-yellow-500/10 to-orange-500/10 border border-yellow-500/20 rounded-xl p-6 hover:border-yellow-500/50 transition-all duration-300 hover:transform hover:scale-105">
            <div class="flex items-center space-x-3 mb-4">
              <div class="relative">
                <img
                  src="/Agent2.png"
                  alt="Levi - Strategy Coordinator"
                  class="w-12 h-12 rounded-full border-2 border-yellow-500"
                />
                <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-background"></div>
              </div>
              <div>
                <h3 class="text-lg font-bold text-white">Levi</h3>
                <p class="text-yellow-400 text-sm font-semibold">Strategy Coordinator</p>
              </div>
            </div>
            <p class="text-gray-300 text-sm mb-3">
              Develops comprehensive content strategies and plans your content calendar.
            </p>
            <div class="space-y-1">
              <div class="flex items-center space-x-2 text-xs text-gray-400">
                <div class="w-1 h-1 bg-yellow-400 rounded-full"></div>
                <span>Content strategy</span>
              </div>
              <div class="flex items-center space-x-2 text-xs text-gray-400">
                <div class="w-1 h-1 bg-yellow-400 rounded-full"></div>
                <span>Calendar planning</span>
              </div>
            </div>
          </div>

          <!-- Kai - Trend Analyst -->
          <div class="group bg-gradient-to-br from-purple-500/10 to-pink-500/10 border border-purple-500/20 rounded-xl p-6 hover:border-purple-500/50 transition-all duration-300 hover:transform hover:scale-105">
            <div class="flex items-center space-x-3 mb-4">
              <div class="relative">
                <img
                  src="/Agent5.png"
                  alt="Kai - Trend Analyst"
                  class="w-12 h-12 rounded-full border-2 border-purple-500"
                />
                <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-background"></div>
              </div>
              <div>
                <h3 class="text-lg font-bold text-white">Kai</h3>
                <p class="text-purple-400 text-sm font-semibold">Trend Analyst</p>
              </div>
            </div>
            <p class="text-gray-300 text-sm mb-3">
              Identifies trending topics and viral content opportunities in your niche.
            </p>
            <div class="space-y-1">
              <div class="flex items-center space-x-2 text-xs text-gray-400">
                <div class="w-1 h-1 bg-purple-400 rounded-full"></div>
                <span>Trend identification</span>
              </div>
              <div class="flex items-center space-x-2 text-xs text-gray-400">
                <div class="w-1 h-1 bg-purple-400 rounded-full"></div>
                <span>Viral content analysis</span>
              </div>
            </div>
          </div>

          <!-- Zara - Community Manager -->
          <div class="group bg-gradient-to-br from-pink-500/10 to-rose-500/10 border border-pink-500/20 rounded-xl p-6 hover:border-pink-500/50 transition-all duration-300 hover:transform hover:scale-105">
            <div class="flex items-center space-x-3 mb-4">
              <div class="relative">
                <img
                  src="/Agent4.png"
                  alt="Zara - Community Manager"
                  class="w-12 h-12 rounded-full border-2 border-pink-500"
                />
                <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-background"></div>
              </div>
              <div>
                <h3 class="text-lg font-bold text-white">Zara</h3>
                <p class="text-pink-400 text-sm font-semibold">Community Manager</p>
              </div>
            </div>
            <p class="text-gray-300 text-sm mb-3">
              Analyzes audience sentiment and helps you build stronger relationships with viewers.
            </p>
            <div class="space-y-1">
              <div class="flex items-center space-x-2 text-xs text-gray-400">
                <div class="w-1 h-1 bg-pink-400 rounded-full"></div>
                <span>Audience analysis</span>
              </div>
              <div class="flex items-center space-x-2 text-xs text-gray-400">
                <div class="w-1 h-1 bg-pink-400 rounded-full"></div>
                <span>Community growth</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Social Proof -->
      <div class="mt-12 text-center">
        <p class="text-gray-400 text-sm mb-4">Join {{ waitlistCount.toLocaleString() }}+ creators already on the waitlist</p>
        <div class="flex justify-center items-center space-x-8 opacity-60">
          <!-- Creator Avatars -->
          <div class="flex -space-x-2">
            <div class="w-8 h-8 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full border-2 border-background"></div>
            <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full border-2 border-background"></div>
            <div class="w-8 h-8 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full border-2 border-background"></div>
            <div class="w-8 h-8 bg-gradient-to-r from-orange-500 to-red-500 rounded-full border-2 border-background"></div>
            <div class="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full border-2 border-background flex items-center justify-center text-xs font-bold">
              +
            </div>
          </div>
        </div>
      </div>

      <!-- Scroll Indicator -->
      <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
        </svg>
      </div>
    </div>
  </section>
</template>

<script setup>
// Reactive waitlist count (you can connect this to your backend later)
const waitlistCount = ref(1247)

// Animate the gradient text
onMounted(() => {
  // Add any additional animations or effects here
})
</script>

<style scoped>
@keyframes gradient {
  0%, 100% {
    background-size: 200% 200%;
    background-position: left center;
  }
  50% {
    background-size: 200% 200%;
    background-position: right center;
  }
}

.animate-gradient {
  animation: gradient 3s ease infinite;
}
</style>
