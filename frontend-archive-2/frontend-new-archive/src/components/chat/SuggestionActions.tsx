import { useState } from 'react'
import { ThumbsUp, ThumbsDown, Settings, Check, X, Copy } from 'lucide-react'
import { cn } from '@/utils'
import { useSuggestionStore, SuggestionType } from '@/store/suggestionStore'
import { useAvatarStore } from '@/store/avatarStore'
import { useSavedMessagesStore } from '@/store/savedMessagesStore'
import Button from '@/components/common/Button'
import TaskCreationModal from '@/components/dashboard/TaskCreationModal'

interface SuggestionActionsProps {
  messageId: string
  content: string
  type: SuggestionType
  className?: string
}

export default function SuggestionActions({ 
  messageId, 
  content, 
  type, 
  className 
}: SuggestionActionsProps) {
  const { 
    implementSuggestion, 
    provideFeedback, 
    getImplementationOptions 
  } = useSuggestionStore()
  const { customization } = useAvatarStore()
  const { saveMessage } = useSavedMessagesStore()
  
  const [showImplementOptions, setShowImplementOptions] = useState(false)
  const [isImplemented, setIsImplemented] = useState(false)
  const [feedback, setFeedback] = useState<'helpful' | 'not_helpful' | null>(null)
  const [showConfirmation, setShowConfirmation] = useState<string | null>(null)
  const [taskModalOpen, setTaskModalOpen] = useState(false)

  const implementationOptions = getImplementationOptions(type)


  const handleImplement = (optionId: string) => {
    const option = implementationOptions.find(o => o.id === optionId)
    if (option) {
      // For "add_to_tasks", open the task creation modal instead
      if (option.action === 'add_to_tasks') {
        setTaskModalOpen(true)
        setShowImplementOptions(false)
      } else {
        implementSuggestion(messageId, { action: option.action, type })
        setIsImplemented(true)
        setShowImplementOptions(false)
        showTemporaryConfirmation('implemented')
        
        // Execute specific implementation logic
        executeImplementation(option.action, content)
      }
    }
  }

  const handleFeedback = (feedbackType: 'helpful' | 'not_helpful') => {
    provideFeedback(messageId, feedbackType)
    setFeedback(feedbackType)
    showTemporaryConfirmation('feedback')
  }

  const showTemporaryConfirmation = (type: string) => {
    setShowConfirmation(type)
    setTimeout(() => setShowConfirmation(null), 2000)
  }

  const handleCreateTask = (task: any) => {
    // Store in localStorage
    const existingTasks = JSON.parse(localStorage.getItem('Vidalytics_tasks') || '[]')
    const updatedTasks = [task, ...existingTasks]
    localStorage.setItem('Vidalytics_tasks', JSON.stringify(updatedTasks))
    
    // Dispatch event to update TaskManager
    window.dispatchEvent(new Event('taskUpdate'))
    
    // Mark as implemented and show confirmation
    implementSuggestion(messageId, { action: 'add_to_tasks', type })
    setIsImplemented(true)
    showTemporaryConfirmation('implemented')
  }

  const executeImplementation = (action: string, content: string) => {
    switch (action) {
      case 'add_to_tasks':
        // This is now handled by the modal
        break
      case 'copy_to_clipboard':
        navigator.clipboard.writeText(content)
        break
      case 'save_chat':
        saveMessage({
          content,
          agentName: customization.name,
          avatar: customization.avatar,
          category: 'General'
        })
        break
      case 'add_to_calendar':
        // Integration with calendar system
        console.log('Adding to calendar:', content)
        break
      case 'save_to_scripts':
        // Integration with script management
        console.log('Saving to scripts:', content)
        break
      case 'apply_to_video':
        // Integration with video management
        console.log('Applying to video:', content)
        break
      default:
        console.log('Executing action:', action, content)
    }
  }


  return (
    <div className={cn('mt-4 border-t border-white/10 pt-4', className)}>
      {/* Confirmation Messages */}
      {showConfirmation && (
        <div className="mb-3 p-3 rounded-lg bg-green-500/20 border border-green-500/30 flex items-center gap-2">
          <Check className="w-4 h-4 text-green-400" />
          <span className="text-sm text-green-300">
            {showConfirmation === 'implemented' && 'Suggestion implemented!'}
            {showConfirmation === 'feedback' && 'Thank you for your feedback!'}
          </span>
        </div>
      )}

      {/* Implementation Options */}
      {showImplementOptions && (
        <div className="mb-4 p-4 bg-dark-800/50 rounded-lg border border-white/20">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-semibold text-white">Implementation Options</h4>
            <Button
              onClick={() => setShowImplementOptions(false)}
              variant="ghost"
              size="xs"
              className="p-1 hover:bg-white/10"
            >
              <X className="w-3 h-3" />
            </Button>
          </div>
          
          <div className="grid grid-cols-1 gap-2">
            {implementationOptions.map((option) => (
              <Button
                key={option.id}
                onClick={() => handleImplement(option.id)}
                variant="secondary"
                size="sm"
                className="justify-start gap-3 hover:bg-primary-600/20"
              >
                <span className="text-base">{option.icon}</span>
                <span className="text-sm">{option.label}</span>
              </Button>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex items-center gap-2 flex-wrap">
        {/* Implement This Button */}
        {!isImplemented && (
          <Button
            onClick={() => setShowImplementOptions(!showImplementOptions)}
            variant="primary"
            size="sm"
            className="flex items-center gap-2 bg-primary-600 hover:bg-primary-700"
          >
            <Settings className="w-4 h-4" />
            <span className="text-sm">Implement This</span>
          </Button>
        )}


        {/* Quick Actions */}
        <div className="flex items-center gap-1 ml-auto">
          {/* Copy to Clipboard */}
          <Button
            onClick={() => executeImplementation('copy_to_clipboard', content)}
            variant="ghost"
            size="xs"
            className="p-2 hover:bg-white/10"
            title="Copy to clipboard"
          >
            <Copy className="w-3 h-3" />
          </Button>

          {/* Feedback Buttons */}
          <Button
            onClick={() => handleFeedback('helpful')}
            variant="ghost"
            size="xs"
            className={cn(
              'p-2 hover:bg-green-500/20',
              feedback === 'helpful' && 'bg-green-500/20 text-green-400'
            )}
            title="This was helpful"
          >
            <ThumbsUp className="w-3 h-3" />
          </Button>

          <Button
            onClick={() => handleFeedback('not_helpful')}
            variant="ghost"
            size="xs"
            className={cn(
              'p-2 hover:bg-red-500/20',
              feedback === 'not_helpful' && 'bg-red-500/20 text-red-400'
            )}
            title="This was not helpful"
          >
            <ThumbsDown className="w-3 h-3" />
          </Button>
        </div>
      </div>

      {/* Implementation Status */}
      {isImplemented && (
        <div className="mt-3 p-3 bg-green-500/10 rounded-lg border border-green-500/20 flex items-center gap-2">
          <Check className="w-4 h-4 text-green-400" />
          <span className="text-sm text-green-300">This suggestion has been implemented</span>
        </div>
      )}

      {/* Task Creation Modal */}
      {taskModalOpen && (
        <TaskCreationModal
          isOpen={taskModalOpen}
          onClose={() => setTaskModalOpen(false)}
          onCreateTask={handleCreateTask}
          messageContent={content}
          agentName={customization.name}
        />
      )}
    </div>
  )
}