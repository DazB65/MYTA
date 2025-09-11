<template>
  <section id="agents" class="py-20 px-6 bg-gray-900/50">
    <div class="max-w-7xl mx-auto">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold mb-6">
          Meet your
          <span class="bg-gradient-to-r from-pink-500 to-purple-600 bg-clip-text text-transparent">
            agent team
          </span>
        </h2>
        <p class="text-xl text-gray-300 max-w-3xl mx-auto">
          Five specialized agents working together to analyze, optimize, and grow your YouTube channel.
          Each agent brings unique expertise to help you succeed.
        </p>
      </div>

      <!-- Agents Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
        <!-- Fred - Executive Agent -->
        <div class="group bg-gradient-to-br from-orange-500/10 to-red-500/10 border border-orange-500/20 rounded-xl p-8 hover:border-orange-500/50 transition-all duration-300 hover:transform hover:scale-105">
          <div class="flex items-center space-x-4 mb-6">
            <div class="relative">
              <img 
                src="/BossAgent.png" 
                alt="Fred - Executive Agent" 
                class="w-16 h-16 rounded-full border-2 border-orange-500"
              />
              <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-background"></div>
            </div>
            <div>
              <h3 class="text-xl font-bold text-white">Fred</h3>
              <p class="text-orange-400 text-sm font-semibold">Executive Agent</p>
            </div>
          </div>
          <p class="text-gray-300 mb-4">
            Your strategic leader who coordinates the entire agent team and provides executive-level insights
            for channel growth and business development.
          </p>
          <div class="space-y-2">
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-orange-400 rounded-full"></div>
              <span>Team coordination</span>
            </div>
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-orange-400 rounded-full"></div>
              <span>Strategic planning</span>
            </div>
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-orange-400 rounded-full"></div>
              <span>Business insights</span>
            </div>
          </div>
        </div>

        <!-- Alex - Analytics Expert -->
        <div class="group bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border border-blue-500/20 rounded-xl p-8 hover:border-blue-500/50 transition-all duration-300 hover:transform hover:scale-105">
          <div class="flex items-center space-x-4 mb-6">
            <div class="relative">
              <img 
                src="/Agent2.png" 
                alt="Alex - Analytics Expert" 
                class="w-16 h-16 rounded-full border-2 border-blue-500"
              />
              <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-background"></div>
            </div>
            <div>
              <h3 class="text-xl font-bold text-white">Alex</h3>
              <p class="text-blue-400 text-sm font-semibold">Analytics Expert</p>
            </div>
          </div>
          <p class="text-gray-300 mb-4">
            Deep-dives into your channel analytics to identify patterns, opportunities, 
            and optimization strategies based on data-driven insights.
          </p>
          <div class="space-y-2">
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-blue-400 rounded-full"></div>
              <span>Performance analysis</span>
            </div>
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-blue-400 rounded-full"></div>
              <span>Data visualization</span>
            </div>
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-blue-400 rounded-full"></div>
              <span>Optimization recommendations</span>
            </div>
          </div>
        </div>

        <!-- Maya - Performance Specialist -->
        <div class="group bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/20 rounded-xl p-8 hover:border-green-500/50 transition-all duration-300 hover:transform hover:scale-105">
          <div class="flex items-center space-x-4 mb-6">
            <div class="relative">
              <img 
                src="/Agent4.png" 
                alt="Maya - Performance Specialist" 
                class="w-16 h-16 rounded-full border-2 border-green-500"
              />
              <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-background"></div>
            </div>
            <div>
              <h3 class="text-xl font-bold text-white">Maya</h3>
              <p class="text-green-400 text-sm font-semibold">Performance Specialist</p>
            </div>
          </div>
          <p class="text-gray-300 mb-4">
            Monitors your content performance in real-time and provides immediate alerts 
            and recommendations for maximizing engagement and reach.
          </p>
          <div class="space-y-2">
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-green-400 rounded-full"></div>
              <span>Real-time monitoring</span>
            </div>
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-green-400 rounded-full"></div>
              <span>Performance alerts</span>
            </div>
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-green-400 rounded-full"></div>
              <span>Engagement optimization</span>
            </div>
          </div>
        </div>

        <!-- Levi - Strategy Coordinator -->
        <div class="group bg-gradient-to-br from-purple-500/10 to-pink-500/10 border border-purple-500/20 rounded-xl p-8 hover:border-purple-500/50 transition-all duration-300 hover:transform hover:scale-105">
          <div class="flex items-center space-x-4 mb-6">
            <div class="relative">
              <img 
                src="/Agent3.png" 
                alt="Levi - Strategy Coordinator" 
                class="w-16 h-16 rounded-full border-2 border-purple-500"
              />
              <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-background"></div>
            </div>
            <div>
              <h3 class="text-xl font-bold text-white">Levi</h3>
              <p class="text-purple-400 text-sm font-semibold">Strategy Coordinator</p>
            </div>
          </div>
          <p class="text-gray-300 mb-4">
            Develops comprehensive content strategies, plans your content calendar, 
            and ensures all your content aligns with your growth objectives.
          </p>
          <div class="space-y-2">
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-purple-400 rounded-full"></div>
              <span>Content strategy</span>
            </div>
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-purple-400 rounded-full"></div>
              <span>Calendar planning</span>
            </div>
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-purple-400 rounded-full"></div>
              <span>Goal alignment</span>
            </div>
          </div>
        </div>

        <!-- Kai - Trend Analyst -->
        <div class="group bg-gradient-to-br from-yellow-500/10 to-orange-500/10 border border-yellow-500/20 rounded-xl p-8 hover:border-yellow-500/50 transition-all duration-300 hover:transform hover:scale-105">
          <div class="flex items-center space-x-4 mb-6">
            <div class="relative">
              <img 
                src="/Agent5.png" 
                alt="Kai - Trend Analyst" 
                class="w-16 h-16 rounded-full border-2 border-yellow-500"
              />
              <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-background"></div>
            </div>
            <div>
              <h3 class="text-xl font-bold text-white">Kai</h3>
              <p class="text-yellow-400 text-sm font-semibold">Trend Analyst</p>
            </div>
          </div>
          <p class="text-gray-300 mb-4">
            Identifies trending topics, viral content opportunities, and emerging patterns 
            in your niche to keep you ahead of the curve.
          </p>
          <div class="space-y-2">
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-yellow-400 rounded-full"></div>
              <span>Trend identification</span>
            </div>
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-yellow-400 rounded-full"></div>
              <span>Viral content analysis</span>
            </div>
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-yellow-400 rounded-full"></div>
              <span>Market insights</span>
            </div>
          </div>
        </div>

        <!-- Zara - Community Manager -->
        <div class="group bg-gradient-to-br from-pink-500/10 to-rose-500/10 border border-pink-500/20 rounded-xl p-8 hover:border-pink-500/50 transition-all duration-300 hover:transform hover:scale-105">
          <div class="flex items-center space-x-4 mb-6">
            <div class="relative">
              <img 
                src="/Agent1.png" 
                alt="Zara - Community Manager" 
                class="w-16 h-16 rounded-full border-2 border-pink-500"
              />
              <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-background"></div>
            </div>
            <div>
              <h3 class="text-xl font-bold text-white">Zara</h3>
              <p class="text-pink-400 text-sm font-semibold">Community Manager</p>
            </div>
          </div>
          <p class="text-gray-300 mb-4">
            Analyzes audience sentiment, manages community engagement, and helps you build 
            stronger relationships with your viewers and subscribers.
          </p>
          <div class="space-y-2">
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-pink-400 rounded-full"></div>
              <span>Audience analysis</span>
            </div>
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-pink-400 rounded-full"></div>
              <span>Sentiment monitoring</span>
            </div>
            <div class="flex items-center space-x-2 text-sm text-gray-400">
              <div class="w-1.5 h-1.5 bg-pink-400 rounded-full"></div>
              <span>Community growth</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Team Collaboration Highlight -->
      <div class="text-center bg-gradient-to-r from-gray-800/50 to-gray-700/50 rounded-2xl p-8 border-2 border-gray-600/70 shadow-lg">
        <h3 class="text-2xl font-bold text-white mb-4">
          They work together, so you don't have to work alone
        </h3>
        <p class="text-gray-300 max-w-2xl mx-auto">
          Your agent team collaborates seamlessly, sharing insights and coordinating strategies
          to provide you with comprehensive, actionable recommendations for channel growth.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
// Component logic can be added here if needed
</script>
