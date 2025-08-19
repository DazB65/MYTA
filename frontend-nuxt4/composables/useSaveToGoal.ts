import type { ChannelGoal } from '../stores/analytics'
import { useAnalyticsStore } from '../stores/analytics'
import type { ChatMessage } from '../types/agents'

export const useSaveToGoal = () => {
  const analyticsStore = useAnalyticsStore()

  /**
   * Extract a meaningful goal title from agent response content
   */
  const extractGoalTitle = (content: string): string => {
    // Remove common prefixes and clean up the content
    let title = content
      .replace(/^(Here's|I suggest|I recommend|You should|Consider|Try to|Aim for|Target)/i, '')
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
   * Infer goal type based on content keywords
   */
  const inferGoalType = (content: string): 'views' | 'subscribers' | 'revenue' | 'engagement' => {
    const lowerContent = content.toLowerCase()
    
    if (lowerContent.includes('subscriber') || lowerContent.includes('follow')) {
      return 'subscribers'
    }
    if (lowerContent.includes('revenue') || lowerContent.includes('money') || lowerContent.includes('income') || lowerContent.includes('monetiz')) {
      return 'revenue'
    }
    if (lowerContent.includes('engagement') || lowerContent.includes('like') || lowerContent.includes('comment') || lowerContent.includes('share')) {
      return 'engagement'
    }
    
    // Default to views
    return 'views'
  }

  /**
   * Extract target numbers from content
   */
  const extractTargetNumber = (content: string): number => {
    // Look for numbers in the content
    const numbers = content.match(/\b(\d{1,3}(?:,\d{3})*|\d+(?:\.\d+)?[kKmMbB]?)\b/g)
    
    if (numbers && numbers.length > 0) {
      // Take the largest number found
      let maxNumber = 0
      
      for (const numStr of numbers) {
        let num = parseFloat(numStr.replace(/,/g, ''))
        
        // Handle k, m, b suffixes
        if (numStr.toLowerCase().includes('k')) {
          num *= 1000
        } else if (numStr.toLowerCase().includes('m')) {
          num *= 1000000
        } else if (numStr.toLowerCase().includes('b')) {
          num *= 1000000000
        }
        
        if (num > maxNumber) {
          maxNumber = num
        }
      }
      
      return Math.floor(maxNumber)
    }
    
    // Default targets based on goal type
    return 10000
  }

  /**
   * Infer deadline based on content time indicators
   */
  const inferDeadline = (content: string): Date => {
    const lowerContent = content.toLowerCase()
    const now = new Date()
    
    if (lowerContent.includes('week') || lowerContent.includes('7 days')) {
      const deadline = new Date(now)
      deadline.setDate(deadline.getDate() + 7)
      return deadline
    }
    
    if (lowerContent.includes('month') || lowerContent.includes('30 days')) {
      const deadline = new Date(now)
      deadline.setMonth(deadline.getMonth() + 1)
      return deadline
    }
    
    if (lowerContent.includes('quarter') || lowerContent.includes('3 months')) {
      const deadline = new Date(now)
      deadline.setMonth(deadline.getMonth() + 3)
      return deadline
    }
    
    if (lowerContent.includes('year') || lowerContent.includes('12 months')) {
      const deadline = new Date(now)
      deadline.setFullYear(deadline.getFullYear() + 1)
      return deadline
    }
    
    // Default to 3 months
    const deadline = new Date(now)
    deadline.setMonth(deadline.getMonth() + 3)
    return deadline
  }

  /**
   * Get appropriate color gradient for goal type
   */
  const getGoalColor = (type: 'views' | 'subscribers' | 'revenue' | 'engagement'): string => {
    const colors = {
      views: 'from-blue-400 to-blue-600',
      subscribers: 'from-green-400 to-green-600',
      revenue: 'from-yellow-400 to-orange-500',
      engagement: 'from-pink-400 to-purple-500'
    }
    return colors[type]
  }

  /**
   * Get appropriate icon for goal type
   */
  const getGoalIcon = (type: 'views' | 'subscribers' | 'revenue' | 'engagement'): string => {
    const icons = {
      views: '👁️',
      subscribers: '👥',
      revenue: '💰',
      engagement: '❤️'
    }
    return icons[type]
  }

  /**
   * Save a chat message as a goal
   */
  const saveMessageAsGoal = (message: ChatMessage, agentData: any): void => {
    const title = extractGoalTitle(message.content)
    const type = inferGoalType(message.content)
    const target = extractTargetNumber(message.content)
    const deadline = inferDeadline(message.content)

    const goalData: Omit<ChannelGoal, 'id'> = {
      title,
      type,
      target,
      current: 0, // Start at 0
      deadline,
      color: getGoalColor(type),
      icon: getGoalIcon(type)
    }

    analyticsStore.addGoal(goalData)
  }

  /**
   * Prepare goal data for modal editing
   */
  const prepareGoalData = (message: ChatMessage, agentData: any) => {
    const type = inferGoalType(message.content)
    
    return {
      title: extractGoalTitle(message.content),
      type,
      target: extractTargetNumber(message.content),
      current: 0,
      deadline: inferDeadline(message.content),
      color: getGoalColor(type),
      icon: getGoalIcon(type),
      originalContent: message.content
    }
  }

  return {
    extractGoalTitle,
    inferGoalType,
    extractTargetNumber,
    inferDeadline,
    getGoalColor,
    getGoalIcon,
    saveMessageAsGoal,
    prepareGoalData
  }
}
