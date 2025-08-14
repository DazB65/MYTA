import { ref, readonly } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useUIStore } from '../stores/ui'

export interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
  body?: any
  headers?: Record<string, string>
  timeout?: number
  retries?: number
  showLoading?: boolean
  loadingKey?: string
  showErrorNotification?: boolean
}

export interface ApiResponse<T = any> {
  status: 'success' | 'error'
  data?: T
  error?: string
  message?: string
}

export const useApi = () => {
  const config = { public: { apiBase: 'http://localhost:8000' } }
  const authStore = useAuthStore()
  const uiStore = useUIStore()

  const loading = ref(false)
  const error = ref<string | null>(null)

  const apiCall = async <T = any>(
    endpoint: string,
    options: ApiOptions = {}
  ): Promise<ApiResponse<T>> => {
    const {
      method = 'GET',
      body,
      headers = {},
      timeout = 30000,
      retries = 3,
      showLoading = false,
      loadingKey,
      showErrorNotification = true
    } = options

    // Set loading state
    if (showLoading || loadingKey) {
      loading.value = true
      if (loadingKey) {
        uiStore.setLoading(loadingKey, true)
      }
    }

    error.value = null

    try {
      // Prepare request options
      const requestOptions: RequestInit = {
        method,
        headers: {
          'Content-Type': 'application/json',
          ...headers
        }
      }

      // Add authentication header if available
      if (authStore.token) {
        requestOptions.headers = {
          ...requestOptions.headers,
          'Authorization': `Bearer ${authStore.token}`
        }
      }

      // Add body for non-GET requests
      if (body && method !== 'GET') {
        requestOptions.body = JSON.stringify(body)
      }

      // Build full URL
      const baseUrl = config.public.apiBase
      const url = endpoint.startsWith('http') ? endpoint : `${baseUrl}${endpoint}`

      let lastError: Error | null = null

      // Retry logic
      for (let attempt = 0; attempt <= retries; attempt++) {
        try {
          // Create abort controller for timeout
          const controller = new AbortController()
          const timeoutId = setTimeout(() => controller.abort(), timeout)

          requestOptions.signal = controller.signal

          const response = await fetch(url, requestOptions)
          clearTimeout(timeoutId)

          // Handle HTTP errors
          if (!response.ok) {
            if (response.status === 401) {
              // Unauthorized - redirect to login
              await authStore.logout()
              throw new Error('Authentication required')
            }

            if (response.status === 403) {
              throw new Error('Access forbidden')
            }

            if (response.status >= 500) {
              throw new Error('Server error occurred')
            }

            throw new Error(`HTTP ${response.status}: ${response.statusText}`)
          }

          // Parse response
          const data = await response.json()
          
          return data as ApiResponse<T>

        } catch (err: any) {
          lastError = err

          // Don't retry on certain errors
          if (err.name === 'AbortError') {
            lastError = new Error('Request timeout')
            break
          }

          if (err.message.includes('Authentication required') || 
              err.message.includes('Access forbidden')) {
            break
          }

          // Wait before retry (exponential backoff)
          if (attempt < retries) {
            const delay = Math.min(1000 * Math.pow(2, attempt), 10000)
            await new Promise(resolve => setTimeout(resolve, delay))
          }
        }
      }

      // Handle final error
      const errorMessage = lastError?.message || 'Network error occurred'
      error.value = errorMessage

      if (showErrorNotification) {
        uiStore.showError('API Error', errorMessage)
      }

      return {
        status: 'error',
        error: errorMessage
      }

    } finally {
      // Clear loading state
      if (showLoading || loadingKey) {
        loading.value = false
        if (loadingKey) {
          uiStore.setLoading(loadingKey, false)
        }
      }
    }
  }

  // Convenience methods
  const get = <T = any>(endpoint: string, options: Omit<ApiOptions, 'method'> = {}) => {
    return apiCall<T>(endpoint, { ...options, method: 'GET' })
  }

  const post = <T = any>(endpoint: string, body?: any, options: Omit<ApiOptions, 'method' | 'body'> = {}) => {
    return apiCall<T>(endpoint, { ...options, method: 'POST', body })
  }

  const put = <T = any>(endpoint: string, body?: any, options: Omit<ApiOptions, 'method' | 'body'> = {}) => {
    return apiCall<T>(endpoint, { ...options, method: 'PUT', body })
  }

  const del = <T = any>(endpoint: string, options: Omit<ApiOptions, 'method'> = {}) => {
    return apiCall<T>(endpoint, { ...options, method: 'DELETE' })
  }

  const patch = <T = any>(endpoint: string, body?: any, options: Omit<ApiOptions, 'method' | 'body'> = {}) => {
    return apiCall<T>(endpoint, { ...options, method: 'PATCH', body })
  }

  return {
    loading: readonly(loading),
    error: readonly(error),
    apiCall,
    get,
    post,
    put,
    delete: del,
    patch
  }
}

// Plugin to make $api available globally
export const apiPlugin = () => {
  const { apiCall } = useApi()
  
  return {
    provide: {
      api: apiCall
    }
  }
}