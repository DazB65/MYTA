<template>
  <section class="relative min-h-screen flex items-start justify-center">
    <!-- Main Content -->
    <div class="relative z-10 max-w-6xl mx-auto px-6 text-center -mt-40">
      <!-- Logo -->
      <div class="flex justify-center">
        <div class="relative">
          <img
            src="/MYTALogo.png"
            alt="MYTA Logo"
            class="h-[28rem] md:h-[36rem] w-auto drop-shadow-2xl"
          />
          <!-- Glow effect behind logo -->
          <div class="absolute inset-0 bg-gradient-to-r from-orange-500/20 to-forest-400/20 blur-3xl scale-110 -z-10"></div>
        </div>
      </div>



      <!-- Meet your MYTA Agent Team Section -->
      <div class="mb-8 -mt-28">
        <h2 class="text-4xl md:text-5xl font-bold mb-8 text-center">
          Meet your
          <span class="bg-gradient-to-r from-orange-500 to-forest-400 bg-clip-text text-transparent">
            MYTA Agent Team
          </span>
        </h2>

        <!-- Agent Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          <!-- Boss Agent -->
          <div class="bg-gradient-to-br from-orange-500/10 to-red-500/10 border border-orange-500/20 rounded-2xl p-6 hover:border-orange-500/40 transition-all duration-300">
            <div class="flex items-center mb-4">
              <div class="relative">
                <img
                  src="/BossAgent.png"
                  alt="Boss Agent"
                  class="w-16 h-16 rounded-full border-3 border-orange-500"
                />
                <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-background"></div>
              </div>
              <div class="ml-4">
                <h3 class="text-xl font-bold text-white">Boss Agent</h3>
                <p class="text-orange-400 font-semibold">Executive Agent</p>
              </div>
            </div>
            <p class="text-gray-300 mb-4">Your strategic leader who coordinates the entire agent team and provides executive-level insights for channel growth and business development.</p>
            <div class="space-y-2">
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-orange-500 rounded-full mr-3"></div>
                Team coordination
              </div>
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-orange-500 rounded-full mr-3"></div>
                Strategic planning
              </div>
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-orange-500 rounded-full mr-3"></div>
                Business insights
              </div>
            </div>
          </div>

          <!-- Alex - Analytics Expert -->
          <div class="bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border border-blue-500/20 rounded-2xl p-6 hover:border-blue-500/40 transition-all duration-300">
            <div class="flex items-center mb-4">
              <div class="relative">
                <img
                  src="/Agent2.png"
                  alt="Alex - Analytics Expert"
                  class="w-16 h-16 rounded-full border-3 border-blue-500"
                />
                <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-background"></div>
              </div>
              <div class="ml-4">
                <h3 class="text-xl font-bold text-white">Alex</h3>
                <p class="text-blue-400 font-semibold">Analytics Expert</p>
              </div>
            </div>
            <p class="text-gray-300 mb-4">Deep-dives into your channel analytics to identify patterns, opportunities, and optimization strategies based on data-driven insights.</p>
            <div class="space-y-2">
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                Performance analysis
              </div>
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                Data visualization
              </div>
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                Optimization recommendations
              </div>
            </div>
          </div>

          <!-- Maya - Performance Specialist -->
          <div class="bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/20 rounded-2xl p-6 hover:border-green-500/40 transition-all duration-300">
            <div class="flex items-center mb-4">
              <div class="relative">
                <img
                  src="/Agent3.png"
                  alt="Maya - Performance Specialist"
                  class="w-16 h-16 rounded-full border-3 border-green-500"
                />
                <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-background"></div>
              </div>
              <div class="ml-4">
                <h3 class="text-xl font-bold text-white">Maya</h3>
                <p class="text-green-400 font-semibold">Performance Specialist</p>
              </div>
            </div>
            <p class="text-gray-300 mb-4">Monitors your content performance in real-time and provides immediate alerts and recommendations for maximizing engagement and reach.</p>
            <div class="space-y-2">
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
                Real-time monitoring
              </div>
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
                Performance alerts
              </div>
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
                Engagement optimization
              </div>
            </div>
          </div>

          <!-- Levi - Strategy Coordinator -->
          <div class="bg-gradient-to-br from-purple-500/10 to-violet-500/10 border border-purple-500/20 rounded-2xl p-6 hover:border-purple-500/40 transition-all duration-300">
            <div class="flex items-center mb-4">
              <div class="relative">
                <img
                  src="/Agent4.png"
                  alt="Levi - Strategy Coordinator"
                  class="w-16 h-16 rounded-full border-3 border-purple-500"
                />
                <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-background"></div>
              </div>
              <div class="ml-4">
                <h3 class="text-xl font-bold text-white">Levi</h3>
                <p class="text-purple-400 font-semibold">Strategy Coordinator</p>
              </div>
            </div>
            <p class="text-gray-300 mb-4">Develops comprehensive content strategies, plans your content calendar, and ensures all your content aligns with your growth objectives.</p>
            <div class="space-y-2">
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-purple-500 rounded-full mr-3"></div>
                Content strategy
              </div>
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-purple-500 rounded-full mr-3"></div>
                Calendar planning
              </div>
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-purple-500 rounded-full mr-3"></div>
                Goal alignment
              </div>
            </div>
          </div>

          <!-- Kai - Trend Analyst -->
          <div class="bg-gradient-to-br from-yellow-500/10 to-orange-500/10 border border-yellow-500/20 rounded-2xl p-6 hover:border-yellow-500/40 transition-all duration-300">
            <div class="flex items-center mb-4">
              <div class="relative">
                <img
                  src="/Agent5.png"
                  alt="Kai - Trend Analyst"
                  class="w-16 h-16 rounded-full border-3 border-yellow-500"
                />
                <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-background"></div>
              </div>
              <div class="ml-4">
                <h3 class="text-xl font-bold text-white">Kai</h3>
                <p class="text-yellow-400 font-semibold">Trend Analyst</p>
              </div>
            </div>
            <p class="text-gray-300 mb-4">Identifies trending topics, viral content opportunities, and emerging patterns in your niche to keep you ahead of the curve.</p>
            <div class="space-y-2">
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-yellow-500 rounded-full mr-3"></div>
                Trend identification
              </div>
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-yellow-500 rounded-full mr-3"></div>
                Viral content analysis
              </div>
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-yellow-500 rounded-full mr-3"></div>
                Market insights
              </div>
            </div>
          </div>

          <!-- Zara - Community Manager -->
          <div class="bg-gradient-to-br from-pink-500/10 to-rose-500/10 border border-pink-500/20 rounded-2xl p-6 hover:border-pink-500/40 transition-all duration-300">
            <div class="flex items-center mb-4">
              <div class="relative">
                <img
                  src="/Alex.png"
                  alt="Zara - Community Manager"
                  class="w-16 h-16 rounded-full border-3 border-pink-500"
                />
                <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-background"></div>
              </div>
              <div class="ml-4">
                <h3 class="text-xl font-bold text-white">Zara</h3>
                <p class="text-pink-400 font-semibold">Community Manager</p>
              </div>
            </div>
            <p class="text-gray-300 mb-4">Analyzes audience sentiment, manages community engagement, and helps you build stronger relationships with your viewers and subscribers.</p>
            <div class="space-y-2">
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-pink-500 rounded-full mr-3"></div>
                Audience analysis
              </div>
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-pink-500 rounded-full mr-3"></div>
                Sentiment monitoring
              </div>
              <div class="flex items-center text-sm text-gray-400">
                <div class="w-2 h-2 bg-pink-500 rounded-full mr-3"></div>
                Community growth
              </div>
            </div>
          </div>
        </div>

        <!-- Team Collaboration Section -->
        <div class="mt-12 bg-gradient-to-r from-forest-500/10 to-orange-500/10 border border-forest-500/20 rounded-2xl p-8 text-center">
          <h3 class="text-2xl font-bold text-white mb-4">They work together, so you don't have to work alone</h3>
          <p class="text-gray-300 max-w-3xl mx-auto">
            Your agent team collaborates seamlessly, sharing insights and coordinating strategies to
            provide you with comprehensive, actionable recommendations for channel growth.
          </p>
        </div>
      </div>

      <!-- Main Headline -->
      <h1 class="text-5xl md:text-7xl font-bold mb-3 leading-tight mt-8">
        Your
        <span class="bg-gradient-to-r from-orange-500 via-forest-400 to-orange-500 bg-clip-text text-transparent animate-gradient">
          Agent Team
        </span>
        <br />
        for YouTube Growth
      </h1>

      <!-- Subheadline -->
      <p class="text-xl md:text-2xl text-gray-300 mb-4 max-w-3xl mx-auto leading-relaxed">
        Join the waitlist for the agent-powered platform that helps creators
        <span class="text-orange-400 font-semibold">optimize content</span>,
        <span class="text-forest-400 font-semibold">analyze performance</span>, and
        <span class="text-orange-400 font-semibold">scale their channels</span>
        with a team of specialized agents.
      </p>

      <!-- Key Benefits -->
      <div class="flex flex-wrap justify-center gap-4 mb-6">
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
      </div>

      <!-- Waitlist Form -->
      <div id="waitlist" class="max-w-md mx-auto">
        <WaitlistForm />
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
