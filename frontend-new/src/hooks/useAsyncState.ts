/**
 * Custom hook for async state management with loading and error handling
 * Replaces common patterns of useState for async operations
 */

import { useState, useCallback } from 'react';
import { logger } from '@/utils/logger';
import { errorHandler, ErrorContext, ErrorSeverity } from '@/utils/errorHandler';

export interface AsyncState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

export interface UseAsyncStateOptions {
  initialData?: any;
  errorContext?: Omit<ErrorContext, 'component'>;
  logContext?: string;
}

export function useAsyncState<T>(
  initialData: T | null = null,
  options: UseAsyncStateOptions = {}
) {
  const [state, setState] = useState<AsyncState<T>>({
    data: initialData,
    loading: false,
    error: null
  });

  const setLoading = useCallback((loading: boolean) => {
    setState(prev => ({ ...prev, loading, error: loading ? null : prev.error }));
  }, []);

  const setData = useCallback((data: T) => {
    setState({ data, loading: false, error: null });
    
    if (options.logContext) {
      logger.debug(`Data updated successfully`, { dataType: typeof data }, options.logContext);
    }
  }, [options.logContext]);

  const setError = useCallback((error: Error | string, severity: ErrorSeverity = ErrorSeverity.MEDIUM) => {
    const appError = errorHandler.handle(error, {
      component: options.logContext || 'AsyncState',
      ...options.errorContext
    }, severity);
    
    setState({ data: null, loading: false, error: appError.message });
    return appError;
  }, [options.errorContext, options.logContext]);

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  const reset = useCallback(() => {
    setState({ data: initialData, loading: false, error: null });
  }, [initialData]);

  const execute = useCallback(async <R>(
    asyncFn: () => Promise<R>,
    transform?: (result: R) => T
  ): Promise<R | null> => {
    try {
      setLoading(true);
      const result = await asyncFn();
      const transformedData = transform ? transform(result) : (result as unknown as T);
      setData(transformedData);
      return result;
    } catch (error) {
      setError(error as Error);
      return null;
    }
  }, [setLoading, setData, setError]);

  return {
    ...state,
    setLoading,
    setData,
    setError,
    clearError,
    reset,
    execute,
    // Convenience getters
    isLoading: state.loading,
    hasError: !!state.error,
    hasData: state.data !== null,
    isEmpty: state.data === null && !state.loading && !state.error
  };
}

export default useAsyncState;