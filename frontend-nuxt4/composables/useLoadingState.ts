/**
 * Composable for managing loading states with error handling
 * Provides consistent loading state management across components
 */

import { ref, computed, type Ref } from 'vue'

export interface LoadingState {
  isLoading: Ref<boolean>
  error: Ref<Error | null>
  data: Ref<any>
  hasError: Ref<boolean>
  isSuccess: Ref<boolean>
  isEmpty: Ref<boolean>
}

export interface UseLoadingStateOptions {
  initialLoading?: boolean
  initialData?: any
  onError?: (error: Error) => void
  onSuccess?: (data: any) => void
  retryDelay?: number
  maxRetries?: number
}

export function useLoadingState(options: UseLoadingStateOptions = {}): LoadingState & {
  setLoading: (loading: boolean) => void
  setError: (error: Error | string | null) => void
  setData: (data: any) => void
  reset: () => void
  execute: <T>(asyncFn: () => Promise<T>) => Promise<T | null>
  retry: () => Promise<void>
} {
  const {
    initialLoading = false,
    initialData = null,
    onError,
    onSuccess,
    retryDelay = 1000,
    maxRetries = 3
  } = options

  // State
  const isLoading = ref(initialLoading)
  const error = ref<Error | null>(null)
  const data = ref(initialData)
  const retryCount = ref(0)
  const lastAsyncFn = ref<(() => Promise<any>) | null>(null)

  // Computed properties
  const hasError = computed(() => error.value !== null)
  const isSuccess = computed(() => !isLoading.value && !hasError.value && data.value !== null)
  const isEmpty = computed(() => {
    if (data.value === null || data.value === undefined) return true
    if (Array.isArray(data.value)) return data.value.length === 0
    if (typeof data.value === 'object') return Object.keys(data.value).length === 0
    return false
  })

  // Methods
  const setLoading = (loading: boolean) => {
    isLoading.value = loading
  }

  const setError = (err: Error | string | null) => {
    if (err === null) {
      error.value = null
    } else if (typeof err === 'string') {
      error.value = new Error(err)
    } else {
      error.value = err
    }
    
    if (error.value && onError) {
      onError(error.value)
    }
  }

  const setData = (newData: any) => {
    data.value = newData
    error.value = null
    
    if (onSuccess) {
      onSuccess(newData)
    }
  }

  const reset = () => {
    isLoading.value = false
    error.value = null
    data.value = initialData
    retryCount.value = 0
    lastAsyncFn.value = null
  }

  const execute = async <T>(asyncFn: () => Promise<T>): Promise<T | null> => {
    try {
      isLoading.value = true
      error.value = null
      lastAsyncFn.value = asyncFn
      retryCount.value = 0

      const result = await asyncFn()
      
      setData(result)
      return result
    } catch (err) {
      const errorObj = err instanceof Error ? err : new Error(String(err))
      setError(errorObj)
      return null
    } finally {
      isLoading.value = false
    }
  }

  const retry = async (): Promise<void> => {
    if (!lastAsyncFn.value) {
      throw new Error('No function to retry')
    }

    if (retryCount.value >= maxRetries) {
      throw new Error(`Maximum retry attempts (${maxRetries}) exceeded`)
    }

    retryCount.value++
    
    // Add delay before retry
    if (retryDelay > 0) {
      await new Promise(resolve => setTimeout(resolve, retryDelay * retryCount.value))
    }

    await execute(lastAsyncFn.value)
  }

  return {
    // State
    isLoading,
    error,
    data,
    hasError,
    isSuccess,
    isEmpty,
    
    // Methods
    setLoading,
    setError,
    setData,
    reset,
    execute,
    retry
  }
}

/**
 * Composable for managing multiple loading states
 * Useful for components that need to track multiple async operations
 */
export function useMultipleLoadingStates() {
  const states = ref<Record<string, LoadingState>>({})</string>

  const createState = (key: string, options?: UseLoadingStateOptions) => {
    states.value[key] = useLoadingState(options)
    return states.value[key]
  }

  const getState = (key: string) => {
    return states.value[key]
  }

  const removeState = (key: string) => {
    delete states.value[key]
  }

  const isAnyLoading = computed(() => {
    return Object.values(states.value).some(state => state.isLoading.value)
  })

  const hasAnyError = computed(() => {
    return Object.values(states.value).some(state => state.hasError.value)
  })

  const resetAll = () => {
    Object.values(states.value).forEach(state => state.reset())
  }

  return {
    states: readonly(states),
    createState,
    getState,
    removeState,
    isAnyLoading,
    hasAnyError,
    resetAll
  }
}

/**
 * Composable for managing async operations with automatic loading states
 * Provides a simple wrapper around async functions
 */
export function useAsyncOperation<T = any>(
  asyncFn: () => Promise<T>,
  options: UseLoadingStateOptions & {
    immediate?: boolean
    dependencies?: Ref<any>[]
  } = {}
) {
  const { immediate = false, dependencies = [], ...loadingOptions } = options
  const loadingState = useLoadingState(loadingOptions)

  // Execute the async function
  const execute = () => loadingState.execute(asyncFn)

  // Auto-execute on mount if immediate is true
  onMounted(() => {
    if (immediate) {
      execute()
    }
  })

  // Watch dependencies and re-execute when they change
  if (dependencies.length > 0) {
    watch(dependencies, () => {
      execute()
    }, { deep: true })
  }

  return {
    ...loadingState,
    execute
  }
}

/**
 * Composable for managing form submission states
 * Specialized for form handling with validation support
 */
export function useFormSubmission<T = any>(
  submitFn: (formData: any) => Promise<T>,
  options: UseLoadingStateOptions & {
    validateFn?: (formData: any) => boolean | string[]
    resetOnSuccess?: boolean
  } = {}
) {
  const { validateFn, resetOnSuccess = false, ...loadingOptions } = options
  const loadingState = useLoadingState(loadingOptions)
  const validationErrors = ref<string[]>([])

  const submit = async (formData: any): Promise<T | null> => {
    // Clear previous validation errors
    validationErrors.value = []

    // Validate form data if validator is provided
    if (validateFn) {
      const validationResult = validateFn(formData)
      
      if (validationResult === false) {
        setError('Form validation failed')
        return null
      }
      
      if (Array.isArray(validationResult) && validationResult.length > 0) {
        validationErrors.value = validationResult
        setError('Form validation failed')
        return null
      }
    }

    // Execute submission
    const result = await loadingState.execute(() => submitFn(formData))

    // Reset form on success if configured
    if (result && resetOnSuccess) {
      // You might want to emit an event here for the parent to handle form reset
    }

    return result
  }

  return {
    ...loadingState,
    validationErrors: readonly(validationErrors),
    submit
  }
}

/**
 * Composable for managing paginated data loading
 * Handles pagination state and loading more data
 */
export function usePaginatedLoading<T = any>(
  fetchFn: (page: number, limit: number) => Promise<{ data: T[], total: number, hasMore: boolean }>,
  options: {
    initialLimit?: number
    onError?: (error: Error) => void
  } = {}
) {
  const { initialLimit = 20, onError } = options
  
  const loadingState = useLoadingState({ onError })
  const currentPage = ref(1)
  const limit = ref(initialLimit)
  const total = ref(0)
  const hasMore = ref(true)
  const allData = ref<T[]>([])

  const loadPage = async (page: number = 1, reset: boolean = false) => {
    if (reset) {
      allData.value = []
      currentPage.value = 1
      total.value = 0
      hasMore.value = true
    }

    const result = await loadingState.execute(() => fetchFn(page, limit.value))
    
    if (result) {
      if (reset) {
        allData.value = result.data
      } else {
        allData.value.push(...result.data)
      }
      
      total.value = result.total
      hasMore.value = result.hasMore
      currentPage.value = page
    }

    return result
  }

  const loadMore = async () => {
    if (!hasMore.value || loadingState.isLoading.value) return
    return loadPage(currentPage.value + 1, false)
  }

  const refresh = async () => {
    return loadPage(1, true)
  }

  return {
    ...loadingState,
    data: readonly(allData),
    currentPage: readonly(currentPage),
    limit: readonly(limit),
    total: readonly(total),
    hasMore: readonly(hasMore),
    loadPage,
    loadMore,
    refresh
  }
}
