/**
 * Application Constants for Vidalytics Frontend
 * Centralized location for magic numbers and configuration values
 */

// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8888'
export const API_TIMEOUT = 30000 // 30 seconds
export const RETRY_ATTEMPTS = 3
export const RETRY_DELAY = 1000 // 1 second

// UI Constants
export const MOBILE_BREAKPOINT = 768
export const TABLET_BREAKPOINT = 1024
export const DESKTOP_BREAKPOINT = 1200

// Chat Interface
export const MAX_MESSAGE_LENGTH = 2000
export const TYPING_INDICATOR_DELAY = 500
export const MESSAGE_BATCH_SIZE = 20
export const CHAT_HISTORY_LIMIT = 100

// Form Validation
export const MIN_CHANNEL_NAME_LENGTH = 2
export const MAX_CHANNEL_NAME_LENGTH = 100
export const MIN_SUBSCRIBER_COUNT = 0
export const MAX_SUBSCRIBER_COUNT = 1000000000

// Polling Intervals (milliseconds)
export const HEALTH_CHECK_INTERVAL = 30000 // 30 seconds
export const OAUTH_STATUS_INTERVAL = 5000  // 5 seconds
export const INSIGHTS_REFRESH_INTERVAL = 300000 // 5 minutes

// Local Storage Keys
export const STORAGE_KEYS = {
  USER_DATA: 'Vidalytics_user_data',
  ONBOARDING_STATUS: 'Vidalytics_onboarding',
  THEME_PREFERENCE: 'Vidalytics_theme',
  SESSION_TOKEN: 'Vidalytics_session',
  CHAT_HISTORY: 'Vidalytics_chat_history',
  SAVED_MESSAGES: 'Vidalytics_saved_messages'
} as const

// Animation Durations
export const ANIMATION_DURATION = {
  FAST: 150,
  NORMAL: 300,
  SLOW: 500
} as const

// File Upload
export const MAX_FILE_SIZE_MB = 10
export const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']

// Pagination
export const DEFAULT_PAGE_SIZE = 25
export const PAGE_SIZE_OPTIONS = [10, 25, 50, 100]

// Toast Configuration
export const TOAST_DURATION = {
  SUCCESS: 3000,
  ERROR: 5000,
  WARNING: 4000,
  INFO: 3000
} as const

// Debounce Delays
export const DEBOUNCE_DELAY = {
  SEARCH: 300,
  TYPING: 500,
  RESIZE: 100,
  SAVE: 1000
} as const

// YouTube Analytics
export const YOUTUBE_METRICS = {
  MIN_CTR: 0,
  MAX_CTR: 100,
  MIN_RETENTION: 0,
  MAX_RETENTION: 100,
  MIN_RPM: 0,
  MAX_RPM: 50
} as const

// Content Types
export const CONTENT_TYPES = [
  'educational',
  'entertainment',
  'tutorial',
  'vlog',
  'review',
  'gaming',
  'music',
  'lifestyle',
  'tech',
  'business',
  'health',
  'travel',
  'food',
  'art',
  'science',
  'sports',
  'comedy',
  'documentary'
] as const

// Upload Frequencies
export const UPLOAD_FREQUENCIES = [
  'daily',
  '3-4 times per week',
  '2-3 times per week',
  'weekly',
  'bi-weekly',
  'monthly',
  'irregular'
] as const

// Video Lengths
export const VIDEO_LENGTHS = [
  'under 5 minutes',
  '5-10 minutes',
  '10-20 minutes',
  '20-30 minutes',
  '30+ minutes'
] as const

// Subscriber Ranges
export const SUBSCRIBER_RANGES = [
  { label: '0-1K', min: 0, max: 1000 },
  { label: '1K-10K', min: 1000, max: 10000 },
  { label: '10K-100K', min: 10000, max: 100000 },
  { label: '100K-1M', min: 100000, max: 1000000 },
  { label: '1M+', min: 1000000, max: Infinity }
] as const

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network connection failed. Please check your internet connection.',
  UNAUTHORIZED: 'Session expired. Please log in again.',
  FORBIDDEN: 'You do not have permission to perform this action.',
  NOT_FOUND: 'The requested resource was not found.',
  SERVER_ERROR: 'An unexpected server error occurred. Please try again later.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  RATE_LIMIT: 'Too many requests. Please wait a moment before trying again.'
} as const