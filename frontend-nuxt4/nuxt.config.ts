// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",

  // Modern build configuration
  nitro: {
    compressPublicAssets: true,
    minify: true,
  },

  // Performance optimizations
  experimental: {
    payloadExtraction: false, // Faster SSR
    inlineSSRStyles: false, // Reduce initial bundle
  },

  // Build optimizations
  build: {
    // Bundle analysis
    analyze: process.env.ANALYZE === "true",
  },

  // Vite/Nuxt aliases and optimizations
  vite: {
    resolve: {
      alias: {
        "@root": __dirname,
      },
    },
    build: {
      // Code splitting
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ["vue", "vue-router"],
            analytics: [
              "@root/components/analytics/AnalyticsOverview.vue",
              "@root/components/analytics/MetricCard.vue",
            ],
            charts: [
              "@root/components/analytics/AnalyticsChart.vue",
              "@root/components/analytics/ChartsDashboard.vue",
            ],
            performance: [
              "@root/components/performance/DeferredComponent.vue",
              "@root/components/performance/PerformanceMonitor.vue",
            ],
          },
        },
      },
    },

    // Dependency optimization
    optimizeDeps: {
      include: ["vue", "vue-router"],
    },
  },

  // Auto-imports: include root-level composables
  imports: {
    dirs: ["composables/**", "../composables/**"],
  },

  // Components auto-registration: include root-level components
  components: {
    dirs: [
      { path: "components", pathPrefix: false },
      { path: "../components", pathPrefix: false },
    ],
  },

  // Development tools
  devtools: { enabled: true },

  // Runtime configuration
  runtimeConfig: {
    // Private keys (only available on server-side)
    redisUrl: process.env.REDIS_URL || "redis://localhost:6379",

    // Public keys (exposed to client-side)
    public: {
      apiBase: process.env.API_BASE_URL || "http://localhost:8000",
      environment: process.env.NODE_ENV || "development",
      enablePerformanceMonitor:
        process.env.ENABLE_PERFORMANCE_MONITOR === "true",
    },
  },

  // Server-side rendering optimizations
  ssr: true,

  // Route rules for caching
  routeRules: {
    // Homepage pre-rendered at build time
    "/": { prerender: true },

    // Analytics pages cached for 5 minutes
    "/analytics/**": { headers: { "cache-control": "s-maxage=300" } },

    // Dashboard cached for 1 minute
    "/dashboard": { headers: { "cache-control": "s-maxage=60" } },

    // API routes not cached
    "/api/**": { headers: { "cache-control": "no-cache" } },
  },

  // Head configuration for performance
  app: {
    head: {
      charset: "utf-8",
      viewport: "width=device-width, initial-scale=1",

      // Preload critical resources
      link: [
        {
          rel: "dns-prefetch",
          href: "https://api.vidalytics.com",
        },
      ],

      // Performance meta tags
      meta: [
        { name: "format-detection", content: "telephone=no" },
        { name: "theme-color", content: "#FF6B9D" },
      ],
    },
  },

  // Tailwind CSS module
  modules: ["@nuxtjs/tailwindcss"],
});
