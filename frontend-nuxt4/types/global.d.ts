// Global type declarations for Nuxt 4 application

declare global {
  // Environment variables
  interface ProcessEnv {
    NODE_ENV: 'development' | 'production' | 'test'
    API_BASE_URL?: string
    WS_URL?: string
    REDIS_URL?: string
    ENABLE_PERFORMANCE_MONITOR?: string
  }

  // Window extensions
  interface Window {
    // Google Analytics
    gtag?: (...args: any[]) => void
    dataLayer?: any[]

    // YouTube API
    YT?: any
    onYouTubeIframeAPIReady?: () => void

    // Development tools
    __NUXT_DEVTOOLS__?: any
  }

  // Custom events
  interface CustomEventMap {
    'agent:message': CustomEvent<{ agentId: string; message: string }>
    'task:completed': CustomEvent<{ taskId: string }>
    'goal:updated': CustomEvent<{ goalId: string; progress: number }>
    'analytics:refreshed': CustomEvent<{ timestamp: Date }>
  }

  // Extend Document with custom events
  interface Document {
    addEventListener<K extends keyof CustomEventMap>(
      type: K,
      listener: (this: Document, ev: CustomEventMap[K]) => void,
      options?: boolean | AddEventListenerOptions
    ): void
    removeEventListener<K extends keyof CustomEventMap>(
      type: K,
      listener: (this: Document, ev: CustomEventMap[K]) => void,
      options?: boolean | EventListenerOptions
    ): void
  }
}

// Module declarations for packages without types
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module '@nuxt/schema' {
  interface RuntimeConfig {
    redisUrl: string
    public: {
      apiBase: string
      wsUrl: string
      environment: string
      enablePerformanceMonitor: boolean
    }
  }
}

// Pinia store types
declare module 'pinia' {
  export interface DefineStoreOptionsBase<S, Store> {
    // Add any custom store options here
    persist?:
      | boolean
      | {
          key?: string
          storage?: Storage
          paths?: string[]
        }
  }
}

// Vue component props enhancement
declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    // Add global properties available in all components
    $formatDate: (date: Date | string) => string
    $formatNumber: (num: number) => string
    $formatCurrency: (amount: number) => string
  }
}

// Nuxt composables
declare module '#app' {
  interface NuxtApp {
    // Add custom Nuxt app properties
    $analytics: any
    $websocket: any
  }
}

export {}
