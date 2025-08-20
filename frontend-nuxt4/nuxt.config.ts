// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',

  // Modern build configuration
  nitro: {
    compressPublicAssets: true,
    minify: true,
  },

  // Performance optimizations
  experimental: {
    payloadExtraction: false, // Faster SSR
  },

  // Build optimizations
  build: {
    // Bundle analysis
    analyze: process.env.ANALYZE === 'true',
  },

  // Vite/Nuxt aliases and optimizations
  vite: {
    resolve: {
      alias: {
        '@root': __dirname,
      },
    },
    build: {
      // Code splitting
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ['vue', 'vue-router'],
            analytics: [
              '@root/components/analytics/AnalyticsOverview.vue',
              '@root/components/analytics/MetricCard.vue',
            ],
            charts: [
              '@root/components/analytics/AnalyticsChart.vue',
              '@root/components/analytics/ChartsDashboard.vue',
            ],
            performance: [
              '@root/components/performance/DeferredComponent.vue',
              '@root/components/performance/PerformanceMonitor.vue',
            ],
          },
        },
      },
    },

    // Dependency optimization
    optimizeDeps: {
      include: ['vue', 'vue-router'],
    },
  },

  // Auto-imports: include root-level composables
  imports: {
    dirs: ['composables/**', '../composables/**'],
  },

  // Components auto-registration: include root-level components
  components: {
    dirs: [
      { path: 'components', pathPrefix: false },
      { path: '../components', pathPrefix: false },
    ],
  },

  // Development tools
  devtools: { enabled: true },

  // Runtime configuration
  runtimeConfig: {
    // Private keys (only available on server-side)
    redisUrl: process.env.REDIS_URL || 'redis://localhost:6379',

    // Public keys (exposed to client-side)
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8000',
      wsUrl: process.env.WS_URL || 'ws://localhost:8000',
      environment: process.env.NODE_ENV || 'development',
      enablePerformanceMonitor: process.env.ENABLE_PERFORMANCE_MONITOR === 'true',
      stripePublishableKey: process.env.NUXT_PUBLIC_STRIPE_PUBLISHABLE_KEY,
    },
  },

  // Server-side rendering optimizations
  ssr: true,

  // Route rules for caching and performance
  routeRules: {
    // Homepage pre-rendered at build time
    '/': { prerender: true },

    // Static pages cached longer
    '/pillars': { headers: { 'cache-control': 's-maxage=600' } }, // 10 minutes
    '/tasks': { headers: { 'cache-control': 's-maxage=300' } }, // 5 minutes
    '/settings': { headers: { 'cache-control': 's-maxage=300' } }, // 5 minutes

    // Analytics pages cached for 5 minutes
    '/analytics/**': { headers: { 'cache-control': 's-maxage=300' } },

    // Dashboard cached for 1 minute (dynamic content)
    '/dashboard': { headers: { 'cache-control': 's-maxage=60' } },

    // API routes not cached
    '/api/**': { headers: { 'cache-control': 'no-cache' } },

    // Static assets cached for 1 year
    '/_nuxt/**': { headers: { 'cache-control': 'max-age=31536000' } },
    '/images/**': { headers: { 'cache-control': 'max-age=31536000' } },
    '/icons/**': { headers: { 'cache-control': 'max-age=31536000' } },
  },

  // Head configuration for SEO and performance
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',

      // SEO meta tags
      title: 'MYTA - Your AI Agent for YouTube Content and Growth',
      meta: [
        // Basic SEO
        {
          name: 'description',
          content:
            'MYTA is your AI-powered YouTube analytics and content optimization platform. Track performance, get AI insights, and grow your channel with intelligent recommendations.',
        },
        {
          name: 'keywords',
          content:
            'YouTube analytics, AI content optimization, YouTube growth, video analytics, content strategy, YouTube AI, channel optimization, video performance',
        },
        { name: 'author', content: 'MYTA' },
        { name: 'robots', content: 'index, follow' },

        // Open Graph / Facebook
        { property: 'og:type', content: 'website' },
        { property: 'og:title', content: 'MYTA - Your AI Agent for YouTube Content and Growth' },
        {
          property: 'og:description',
          content:
            'AI-powered YouTube analytics and content optimization platform. Track performance, get insights, and grow your channel.',
        },
        { property: 'og:image', content: '/MY YT AGENT.png' },
        { property: 'og:url', content: 'https://myta.app' },
        { property: 'og:site_name', content: 'MYTA' },

        // Twitter Card
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: 'MYTA - Your AI Agent for YouTube Content and Growth' },
        {
          name: 'twitter:description',
          content: 'AI-powered YouTube analytics and content optimization platform.',
        },
        { name: 'twitter:image', content: '/MY YT AGENT.png' },

        // Performance and mobile
        { name: 'format-detection', content: 'telephone=no' },
        { name: 'theme-color', content: '#FF6B9D' },
        { name: 'mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' },

        // Additional SEO
        { name: 'language', content: 'en' },
        { name: 'revisit-after', content: '7 days' },
        { name: 'rating', content: 'general' },
      ],

      // Preload critical resources and performance optimization
      link: [
        // DNS prefetch for external resources
        { rel: 'dns-prefetch', href: 'https://api.myta.app' },
        { rel: 'dns-prefetch', href: 'https://fonts.googleapis.com' },
        { rel: 'dns-prefetch', href: 'https://www.googleapis.com' },

        // Favicon and app icons
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' },
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32x32.png' },
        { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon-16x16.png' },
        { rel: 'manifest', href: '/site.webmanifest' },

        // Canonical URL
        { rel: 'canonical', href: 'https://myta.app' },
      ],

      // Structured data for SEO
      script: [
        {
          type: 'application/ld+json',
          children: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'SoftwareApplication',
            name: 'MYTA',
            description: 'AI-powered YouTube analytics and content optimization platform',
            url: 'https://myta.app',
            applicationCategory: 'BusinessApplication',
            operatingSystem: 'Web',
            offers: {
              '@type': 'Offer',
              price: '0',
              priceCurrency: 'USD',
            },
            creator: {
              '@type': 'Organization',
              name: 'MYTA',
              url: 'https://myta.app',
            },
          }),
        },
      ],
    },
  },

  // Modules for SEO and performance
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@vueuse/nuxt',
    '@nuxt/image',
    '@nuxtjs/robots',
    '@nuxtjs/sitemap'
  ],

  // Image optimization configuration
  image: {
    // Enable responsive images
    responsive: {
      sizes: '100vw sm:50vw md:400px'
    },
    // Image quality settings
    quality: 80,
    // Enable WebP format
    format: ['webp', 'png', 'jpg'],
    // Presets for common use cases
    presets: {
      avatar: {
        modifiers: {
          format: 'webp',
          width: 50,
          height: 50,
          quality: 80
        }
      },
      banner: {
        modifiers: {
          format: 'webp',
          width: 1200,
          height: 630,
          quality: 85
        }
      }
    }
  },

  // Robots.txt configuration
  robots: {
    UserAgent: '*',
    Allow: '/',
    Sitemap: 'https://myta.app/sitemap.xml'
  },

  // Sitemap configuration
  sitemap: {
    hostname: 'https://myta.app',
    gzip: true,
    routes: [
      '/dashboard',
      '/analytics',
      '/tasks',
      '/pillars',
      '/settings'
    ]
  },

  // Pinia configuration
  pinia: {
    storesDirs: ['./stores/**', './composables/stores/**'],
  },
})
