import { useTasksStore } from '../stores/tasks'
import type { ChatMessage } from '../types/agents'
import type { CreateTaskRequest, TaskCategory, TaskPriority } from '../types/tasks'

export const useSaveToTask = () => {
  const tasksStore = useTasksStore()

  /**
   * Extract a meaningful task title from agent response content
   */
  const extractTaskTitle = (content: string): string => {
    // Remove common prefixes and clean up the content
    let title = content
      .replace(/^(Here's|I suggest|I recommend|You should|Consider|Try to)/i, '')
      .replace(/[.!?]+$/, '')
      .trim()

    // If content is too long, take first sentence or first 60 characters
    if (title.length > 60) {
      const firstSentence = title.split(/[.!?]/)[0]
      title = firstSentence.length > 0 && firstSentence.length <= 60 
        ? firstSentence 
        : title.substring(0, 57) + '...'
    }

    // Ensure it starts with a capital letter
    return title.charAt(0).toUpperCase() + title.slice(1)
  }

  /**
   * Infer task category based on content keywords
   */
  const inferCategory = (content: string): TaskCategory => {
    const lowerContent = content.toLowerCase()
    
    if (lowerContent.includes('seo') || lowerContent.includes('search') || lowerContent.includes('keyword')) {
      return 'seo'
    }
    if (lowerContent.includes('content') || lowerContent.includes('video') || lowerContent.includes('script')) {
      return 'content'
    }
    if (lowerContent.includes('analytics') || lowerContent.includes('metrics') || lowerContent.includes('data')) {
      return 'analytics'
    }
    if (lowerContent.includes('marketing') || lowerContent.includes('promote') || lowerContent.includes('advertise')) {
      return 'marketing'
    }
    if (lowerContent.includes('monetization') || lowerContent.includes('revenue') || lowerContent.includes('money')) {
      return 'monetization'
    }
    if (lowerContent.includes('community') || lowerContent.includes('audience') || lowerContent.includes('engagement')) {
      return 'community'
    }
    if (lowerContent.includes('plan') || lowerContent.includes('strategy') || lowerContent.includes('schedule')) {
      return 'planning'
    }
    if (lowerContent.includes('research') || lowerContent.includes('analyze') || lowerContent.includes('study')) {
      return 'research'
    }
    
    return 'general'
  }

  /**
   * Infer task priority based on content urgency indicators
   */
  const inferPriority = (content: string): TaskPriority => {
    const lowerContent = content.toLowerCase()
    
    if (lowerContent.includes('urgent') || lowerContent.includes('asap') || lowerContent.includes('immediately')) {
      return 'urgent'
    }
    if (lowerContent.includes('important') || lowerContent.includes('critical') || lowerContent.includes('priority')) {
      return 'high'
    }
    if (lowerContent.includes('when you can') || lowerContent.includes('eventually') || lowerContent.includes('sometime')) {
      return 'low'
    }
    
    return 'medium'
  }

  /**
   * Extract action items from agent response
   */
  const extractActionItems = (content: string): string[] => {
    const actionItems: string[] = []
    
    // Look for numbered lists
    const numberedItems = content.match(/\d+\.\s*([^.\n]+)/g)
    if (numberedItems) {
      actionItems.push(...numberedItems.map(item => item.replace(/^\d+\.\s*/, '').trim()))
    }
    
    // Look for bullet points
    const bulletItems = content.match(/[•\-\*]\s*([^.\n]+)/g)
    if (bulletItems) {
      actionItems.push(...bulletItems.map(item => item.replace(/^[•\-\*]\s*/, '').trim()))
    }
    
    return actionItems.slice(0, 3) // Limit to first 3 items
  }

  /**
   * Save a chat message as a task
   */
  const saveMessageAsTask = (message: ChatMessage, agentData: any): string => {
    const title = extractTaskTitle(message.content)
    const category = inferCategory(message.content)
    const priority = inferPriority(message.content)
    const actionItems = extractActionItems(message.content)
    
    // Set due date to tomorrow by default
    const tomorrow = new Date()
    tomorrow.setDate(tomorrow.getDate() + 1)
    
    const taskData: CreateTaskRequest = {
      title,
      description: message.content,
      category,
      priority,
      dueDate: tomorrow,
      agentId: agentData.id?.toString(),
      tags: ['agent-generated', agentData.name.toLowerCase().replace(/\s+/g, '-')],
      estimatedTime: 60 // Default to 1 hour
    }
    
    const newTask = tasksStore.addTask(taskData)
    return newTask.id
  }

  /**
   * Prepare task data for modal editing
   */
  const prepareTaskData = (message: ChatMessage, agentData: any) => {
    return {
      title: extractTaskTitle(message.content),
      description: message.content,
      category: inferCategory(message.content),
      priority: inferPriority(message.content),
      agentId: agentData.id?.toString(),
      tags: ['agent-generated', agentData.name.toLowerCase().replace(/\s+/g, '-')],
      actionItems: extractActionItems(message.content)
    }
  }

  return {
    extractTaskTitle,
    inferCategory,
    inferPriority,
    extractActionItems,
    saveMessageAsTask,
    prepareTaskData
  }
}
