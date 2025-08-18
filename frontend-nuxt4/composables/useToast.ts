interface ToastOptions {
  type?: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
  persistent?: boolean
}

interface Toast extends ToastOptions {
  id: string
  createdAt: number
}

// Global toast state
const toasts = ref<Toast[]>([])

export const useToast = () => {
  const addToast = (options: ToastOptions): string => {
    const id = `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    
    const toast: Toast = {
      id,
      createdAt: Date.now(),
      type: 'info',
      duration: 5000,
      persistent: false,
      ...options
    }

    toasts.value.push(toast)
    
    // Auto-remove after duration (unless persistent)
    if (!toast.persistent && toast.duration && toast.duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, toast.duration)
    }

    return id
  }

  const removeToast = (id: string) => {
    const index = toasts.value.findIndex(toast => toast.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  const clearAllToasts = () => {
    toasts.value = []
  }

  // Convenience methods
  const success = (title: string, message?: string, options?: Partial<ToastOptions>) => {
    return addToast({ type: 'success', title, message, ...options })
  }

  const error = (title: string, message?: string, options?: Partial<ToastOptions>) => {
    return addToast({ type: 'error', title, message, ...options })
  }

  const warning = (title: string, message?: string, options?: Partial<ToastOptions>) => {
    return addToast({ type: 'warning', title, message, ...options })
  }

  const info = (title: string, message?: string, options?: Partial<ToastOptions>) => {
    return addToast({ type: 'info', title, message, ...options })
  }

  return {
    // State
    toasts: readonly(toasts),
    
    // Methods
    addToast,
    removeToast,
    clearAllToasts,
    
    // Convenience methods
    success,
    error,
    warning,
    info
  }
}
