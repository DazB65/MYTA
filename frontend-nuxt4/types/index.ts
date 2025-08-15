// Re-export all types for easy importing
export * from './agents'
export * from './analytics'
export * from './tasks'

// Common utility types
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T = any> {
  data: T[]
  total: number
  page: number
  limit: number
  hasNext: boolean
  hasPrev: boolean
}

export interface User {
  id: string
  email: string
  name: string
  avatar?: string
  createdAt: Date
  updatedAt: Date
  preferences: UserPreferences
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'auto'
  notifications: NotificationSettings
  dashboard: DashboardSettings
}

export interface NotificationSettings {
  email: boolean
  push: boolean
  insights: boolean
  goals: boolean
  tasks: boolean
}

export interface DashboardSettings {
  layout: 'compact' | 'comfortable' | 'spacious'
  defaultView: 'dashboard' | 'analytics' | 'tasks'
  showWelcome: boolean
}

export interface Notification {
  id: string
  type: NotificationType
  title: string
  message: string
  read: boolean
  createdAt: Date
  actionUrl?: string
  metadata?: Record<string, any>
}

export type NotificationType =
  | 'info'
  | 'success'
  | 'warning'
  | 'error'
  | 'insight'
  | 'goal_achieved'
  | 'task_due'

// Component prop types
export interface BaseComponentProps {
  class?: string
  style?: string | Record<string, any>
}

export interface LoadingState {
  loading: boolean
  error: string | null
}

// API configuration
export interface ApiConfig {
  baseUrl: string
  timeout: number
  retries: number
}

// WebSocket types
export interface WebSocketConfig {
  url: string
  reconnectInterval: number
  maxReconnectAttempts: number
}

// Form types
export interface FormField {
  name: string
  label: string
  type: 'text' | 'email' | 'password' | 'number' | 'date' | 'select' | 'textarea'
  required: boolean
  placeholder?: string
  options?: SelectOption[]
  validation?: ValidationRule[]
}

export interface SelectOption {
  value: string | number
  label: string
  disabled?: boolean
}

export interface ValidationRule {
  type: 'required' | 'email' | 'min' | 'max' | 'pattern'
  value?: any
  message: string
}

// Chart/Analytics types
export interface ChartData {
  labels: string[]
  datasets: ChartDataset[]
}

export interface ChartDataset {
  label: string
  data: number[]
  backgroundColor?: string | string[]
  borderColor?: string | string[]
  borderWidth?: number
}

// YouTube specific types
export interface YouTubeChannel {
  id: string
  title: string
  description: string
  thumbnails: YouTubeThumbnails
  subscriberCount: number
  videoCount: number
  viewCount: number
  publishedAt: Date
}

export interface YouTubeThumbnails {
  default: YouTubeThumbnail
  medium: YouTubeThumbnail
  high: YouTubeThumbnail
}

export interface YouTubeThumbnail {
  url: string
  width: number
  height: number
}

export interface YouTubeVideo {
  id: string
  title: string
  description: string
  thumbnails: YouTubeThumbnails
  publishedAt: Date
  duration: string
  viewCount: number
  likeCount: number
  commentCount: number
  tags: string[]
}

// Error types
export interface AppError {
  code: string
  message: string
  details?: any
  timestamp: Date
}

// Route types for navigation
export interface RouteInfo {
  name: string
  path: string
  icon?: string
  requiresAuth?: boolean
  meta?: Record<string, any>
}
