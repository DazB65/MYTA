/**
 * Error Handling Service
 * Provides consistent error handling and user feedback throughout the application
 */

import { logger } from './logger';
import { ERROR_MESSAGES } from '../constants';

export interface ErrorContext {
  component?: string;
  action?: string;
  userId?: string;
  additionalData?: Record<string, any>;
}

export enum ErrorSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export interface AppError {
  message: string;
  code?: string;
  severity: ErrorSeverity;
  context?: ErrorContext;
  originalError?: Error;
  timestamp: Date;
}

class ErrorHandler {
  private isDevelopment = import.meta.env.DEV || false;

  /**
   * Handle and log errors with consistent formatting
   */
  handle(error: Error | string, context?: ErrorContext, severity: ErrorSeverity = ErrorSeverity.MEDIUM): AppError {
    const appError: AppError = {
      message: typeof error === 'string' ? error : error.message,
      severity,
      context,
      originalError: typeof error === 'string' ? undefined : error,
      timestamp: new Date()
    };

    // Log error with context
    logger.error(
      `Error in ${context?.component || 'Unknown'}: ${appError.message}`,
      appError.originalError,
      {
        severity,
        context,
        action: context?.action
      },
      context?.component
    );

    return appError;
  }

  /**
   * Handle OAuth-specific errors
   */
  handleOAuthError(error: Error | string, context?: Omit<ErrorContext, 'component'>): AppError {
    return this.handle(error, { ...context, component: 'OAuth' }, ErrorSeverity.HIGH);
  }

  /**
   * Handle API errors with response context
   */
  handleApiError(error: Error | string, response?: Response, context?: Omit<ErrorContext, 'component'>): AppError {
    const apiContext = {
      ...context,
      component: 'API',
      additionalData: {
        ...context?.additionalData,
        status: response?.status,
        statusText: response?.statusText,
        url: response?.url
      }
    };

    const severity = response?.status && response.status >= 500 
      ? ErrorSeverity.HIGH 
      : ErrorSeverity.MEDIUM;

    return this.handle(error, apiContext, severity);
  }

  /**
   * Get user-friendly error message
   */
  getUserMessage(error: AppError): string {
    // Map technical errors to user-friendly messages using constants
    const errorMessages: Record<string, string> = {
      'Network Error': ERROR_MESSAGES.NETWORK_ERROR,
      'Failed to fetch': ERROR_MESSAGES.NETWORK_ERROR,
      'Unauthorized': ERROR_MESSAGES.UNAUTHORIZED,
      'Forbidden': ERROR_MESSAGES.FORBIDDEN,
      'Not Found': ERROR_MESSAGES.NOT_FOUND,
      'Internal Server Error': ERROR_MESSAGES.SERVER_ERROR,
      'ValidationError': ERROR_MESSAGES.VALIDATION_ERROR
    };

    // Check for mapped messages
    for (const [key, message] of Object.entries(errorMessages)) {
      if (error.message.includes(key)) {
        return message;
      }
    }

    // OAuth-specific messages
    if (error.context?.component === 'OAuth') {
      return 'Authentication failed. Please try connecting your account again.';
    }

    // API-specific messages
    if (error.context?.component === 'API') {
      const status = error.context.additionalData?.status;
      if (status === 429) {
        return ERROR_MESSAGES.RATE_LIMIT;
      }
      if (status && status >= 500) {
        return ERROR_MESSAGES.SERVER_ERROR;
      }
    }

    // Generic fallback
    return this.isDevelopment 
      ? error.message 
      : 'An unexpected error occurred. Please try again.';
  }

  /**
   * Show user notification (replaces alert())
   */
  showUserError(error: AppError): void {
    const message = this.getUserMessage(error);
    
    // In a real app, this would integrate with a toast/notification system
    // For now, we'll use a more styled approach than raw alert()
    if (typeof window !== 'undefined') {
      // Could be replaced with a proper toast notification
      console.error('User Error:', message);
      if (error.severity === ErrorSeverity.CRITICAL || error.severity === ErrorSeverity.HIGH) {
        alert(message); // Temporary fallback
      }
    }
  }
}

// Export singleton instance
export const errorHandler = new ErrorHandler();
export default errorHandler;