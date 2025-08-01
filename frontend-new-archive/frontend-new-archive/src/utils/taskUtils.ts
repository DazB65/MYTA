import { SuggestionType } from '@/store/suggestionStore'

export interface Task {
  id: string
  title: string
  description?: string
  completed: boolean
  priority: 'low' | 'medium' | 'high'
  dueDate?: string
  category: string
  createdAt: string
  source?: 'agent' | 'manual'
  agentName?: string
}

export const addTaskFromSuggestion = (
  content: string,
  suggestionType: SuggestionType,
  agentName?: string
): void => {
  // Extract task title from content (first line or first sentence)
  const title = extractTaskTitle(content, suggestionType)
  
  // Determine category based on suggestion type
  const category = getCategoryFromSuggestionType(suggestionType)
  
  // Determine priority based on suggestion type
  const priority = getPriorityFromSuggestionType(suggestionType)
  
  // Create task object
  const task: Task = {
    id: Date.now().toString(),
    title,
    description: content, // Always include full content as description
    completed: false,
    priority,
    category,
    createdAt: new Date().toISOString(),
    source: 'agent',
    agentName: agentName || 'AI Assistant'
  }
  
  // Get existing tasks from localStorage
  const existingTasks = localStorage.getItem('Vidalytics_tasks')
  const tasks: Task[] = existingTasks ? JSON.parse(existingTasks) : []
  
  // Add new task to the beginning of the array
  const updatedTasks = [task, ...tasks]
  
  // Save to localStorage
  localStorage.setItem('Vidalytics_tasks', JSON.stringify(updatedTasks))
  
  // Dispatch event to update TaskManager
  window.dispatchEvent(new Event('taskUpdate'))
}

const extractTaskTitle = (content: string, suggestionType: SuggestionType): string => {
  // Split content into lines and sentences
  const lines = content.split('\n').filter(line => line.trim())
  const sentences = content.split(/[.!?]+/).filter(s => s.trim())
  
  // Try to extract a meaningful title based on suggestion type
  switch (suggestionType) {
    case 'content_idea':
      // Look for lines that start with action words or are questions
      const ideaLine = lines.find(line => 
        line.match(/^(Create|Make|Film|Record|Write|Design|Plan)/i) ||
        line.includes('?') ||
        line.match(/^(Video|Content|Post|Tutorial|Guide)/i)
      )
      return ideaLine || sentences[0]?.trim() || 'Content Idea from AI'
    
    case 'title_optimization':
      // Look for titles in quotes or after "Title:" 
      const titleMatch = content.match(/["']([^"']+)["']/) || 
                        content.match(/Title:\s*([^\n]+)/i)
      return titleMatch ? `Update title: ${titleMatch[1]}` : 'Optimize video title'
    
    case 'script_suggestion':
      return 'Review script suggestion'
    
    case 'hook_improvement':
      return 'Implement hook improvement'
    
    default:
      // Use first meaningful sentence or line
      const firstSentence = sentences[0]?.trim()
      if (firstSentence && firstSentence.length > 10 && firstSentence.length < 80) {
        return firstSentence
      }
      return lines[0]?.trim() || 'Task from AI suggestion'
  }
}

const getCategoryFromSuggestionType = (suggestionType: SuggestionType): string => {
  switch (suggestionType) {
    case 'content_idea':
      return 'research'
    case 'title_optimization':
      return 'editing'
    case 'script_suggestion':
      return 'editing'
    case 'hook_improvement':
      return 'editing'
    default:
      return 'general'
  }
}

const getPriorityFromSuggestionType = (suggestionType: SuggestionType): 'low' | 'medium' | 'high' => {
  switch (suggestionType) {
    case 'content_idea':
      return 'medium'
    case 'title_optimization':
      return 'high'
    case 'script_suggestion':
      return 'high'
    case 'hook_improvement':
      return 'high'
    default:
      return 'medium'
  }
}