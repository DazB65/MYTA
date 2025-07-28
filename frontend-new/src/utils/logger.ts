/**
 * Frontend Logging Service
 * Provides consistent, environment-aware logging throughout the application
 */

export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
}

export interface LogEntry {
  level: LogLevel;
  message: string;
  timestamp: Date;
  context?: Record<string, any>;
  source?: string;
}

class Logger {
  private level: LogLevel;
  private isDevelopment: boolean;

  constructor() {
    this.isDevelopment = import.meta.env.DEV || false;
    this.level = this.isDevelopment ? LogLevel.DEBUG : LogLevel.WARN;
  }

  private shouldLog(level: LogLevel): boolean {
    return level >= this.level;
  }

  private formatMessage(level: LogLevel, message: string, context?: Record<string, any>, source?: string): string {
    const timestamp = new Date().toISOString();
    const levelStr = LogLevel[level];
    const sourceStr = source ? `[${source}]` : '';
    const contextStr = context ? `\n${JSON.stringify(context, null, 2)}` : '';
    
    return `${timestamp} ${levelStr} ${sourceStr} ${message}${contextStr}`;
  }

  debug(message: string, context?: Record<string, any>, source?: string) {
    if (this.shouldLog(LogLevel.DEBUG)) {
      console.debug(this.formatMessage(LogLevel.DEBUG, message, context, source));
    }
  }

  info(message: string, context?: Record<string, any>, source?: string) {
    if (this.shouldLog(LogLevel.INFO)) {
      console.info(this.formatMessage(LogLevel.INFO, message, context, source));
    }
  }

  warn(message: string, context?: Record<string, any>, source?: string) {
    if (this.shouldLog(LogLevel.WARN)) {
      console.warn(this.formatMessage(LogLevel.WARN, message, context, source));
    }
  }

  error(message: string, error?: Error | any, context?: Record<string, any>, source?: string) {
    if (this.shouldLog(LogLevel.ERROR)) {
      const errorContext = error ? { 
        error: error.message || error, 
        stack: error.stack,
        ...context 
      } : context;
      
      console.error(this.formatMessage(LogLevel.ERROR, message, errorContext, source));
    }
  }

  // OAuth-specific logging
  oauth(message: string, context?: Record<string, any>) {
    this.info(`OAuth: ${message}`, context, 'OAuth');
  }

  // API-specific logging  
  api(message: string, context?: Record<string, any>) {
    this.info(`API: ${message}`, context, 'API');
  }

  // Agent-specific logging
  agent(message: string, context?: Record<string, any>) {
    this.info(`Agent: ${message}`, context, 'Agent');
  }
}

// Export singleton instance
export const logger = new Logger();
export default logger;