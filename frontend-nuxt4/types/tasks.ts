export interface Task {
  id: string
  title: string
  description: string
  status: TaskStatus
  priority: TaskPriority
  category: TaskCategory
  dueDate: Date
  createdAt: Date
  updatedAt: Date
  completed: boolean
  userId?: string
  agentId?: string
  tags: string[]
  estimatedTime?: number // in minutes
  actualTime?: number // in minutes
}

export type TaskStatus = 'pending' | 'in_progress' | 'completed' | 'cancelled' | 'on_hold'

export type TaskPriority = 'low' | 'medium' | 'high' | 'urgent'

export type TaskCategory =
  | 'content'
  | 'marketing'
  | 'analytics'
  | 'seo'
  | 'monetization'
  | 'community'
  | 'planning'
  | 'research'
  | 'general'

export type TaskFilter =
  | 'all'
  | 'pending'
  | 'completed'
  | 'in_progress'
  | 'high_priority'
  | 'due_today'
  | 'overdue'

export interface TaskStats {
  total: number
  completed: number
  pending: number
  inProgress: number
  overdue: number
  completionRate: number
}

export interface CreateTaskRequest {
  title: string
  description: string
  priority: TaskPriority
  category: TaskCategory
  dueDate: Date
  tags?: string[]
  estimatedTime?: number
  agentId?: string
}

export interface UpdateTaskRequest {
  id: string
  title?: string
  description?: string
  status?: TaskStatus
  priority?: TaskPriority
  category?: TaskCategory
  dueDate?: Date
  tags?: string[]
  estimatedTime?: number
  actualTime?: number
}
