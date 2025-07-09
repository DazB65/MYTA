import { useState } from 'react'
import { ThumbsUp, ThumbsDown, Bookmark, Settings, Check, X, Copy } from 'lucide-react'
import { cn } from '@/utils'
import { useSuggestionStore, SuggestionType } from '@/store/suggestionStore'
import Button from '@/components/common/Button'

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
    saveSuggestion, 
    implementSuggestion, 
    provideFeedback, 
    getImplementationOptions 
  } = useSuggestionStore()
  
  const [showImplementOptions, setShowImplementOptions] = useState(false)
  const [isImplemented, setIsImplemented] = useState(false)
  const [isSaved, setIsSaved] = useState(false)
  const [feedback, setFeedback] = useState<'helpful' | 'not_helpful' | null>(null)
  const [showConfirmation, setShowConfirmation] = useState<string | null>(null)

  const implementationOptions = getImplementationOptions(type)

  const handleSave = () => {
    saveSuggestion({
      type,
      content,
      category: getCategoryFromType(type),
      isImplemented: false,
      tags: extractTagsFromContent(content)
    })
    setIsSaved(true)
    showTemporaryConfirmation('saved')
  }

  const handleImplement = (optionId: string) => {
    const option = implementationOptions.find(o => o.id === optionId)
    if (option) {
      implementSuggestion(messageId, { action: option.action, type })
      setIsImplemented(true)
      setShowImplementOptions(false)
      showTemporaryConfirmation('implemented')
      
      // Execute specific implementation logic
      executeImplementation(option.action, content)
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

  const executeImplementation = (action: string, content: string) => {
    switch (action) {
      case 'copy_to_clipboard':
        navigator.clipboard.writeText(content)
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

  const getCategoryFromType = (type: SuggestionType): string => {
    switch (type) {
      case 'content_idea': return 'Content Ideas'
      case 'title_optimization': return 'Title Optimization'
      case 'script_suggestion': return 'Script Writing'
      case 'hook_improvement': return 'Hook Improvement'
      default: return 'General'
    }
  }

  const extractTagsFromContent = (content: string): string[] => {
    // Simple tag extraction - could be enhanced with NLP
    const tags = []
    if (content.toLowerCase().includes('youtube')) tags.push('youtube')
    if (content.toLowerCase().includes('viral')) tags.push('viral')
    if (content.toLowerCase().includes('seo')) tags.push('seo')
    if (content.toLowerCase().includes('engagement')) tags.push('engagement')
    return tags
  }

  return (
    <div className={cn('mt-4 border-t border-white/10 pt-4', className)}>
      {/* Confirmation Messages */}
      {showConfirmation && (
        <div className="mb-3 p-3 rounded-lg bg-green-500/20 border border-green-500/30 flex items-center gap-2">
          <Check className="w-4 h-4 text-green-400" />
          <span className="text-sm text-green-300">
            {showConfirmation === 'saved' && 'Suggestion saved successfully!'}
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

        {/* Save for Later Button */}
        {!isSaved && (
          <Button
            onClick={handleSave}
            variant="secondary"
            size="sm"
            className="flex items-center gap-2 hover:bg-yellow-600/20"
          >
            <Bookmark className="w-4 h-4" />
            <span className="text-sm">Save for Later</span>
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

      {/* Saved Status */}
      {isSaved && (
        <div className="mt-3 p-3 bg-yellow-500/10 rounded-lg border border-yellow-500/20 flex items-center gap-2">
          <Bookmark className="w-4 h-4 text-yellow-400" />
          <span className="text-sm text-yellow-300">Saved to your suggestions</span>
        </div>
      )}
    </div>
  )
}