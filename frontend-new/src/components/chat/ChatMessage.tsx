import { memo } from 'react'
import { cn } from '@/utils'
import type { ChatMessage as ChatMessageType } from '@/types'
import SuggestionActions from './SuggestionActions'
import { SuggestionType } from '@/store/suggestionStore'

interface ChatMessageProps {
  message: ChatMessageType
  compact?: boolean
}

function ChatMessage({ message, compact = false }: ChatMessageProps) {
  const isUser = message.role === 'user'
  const isError = message.isError
  const isAgent = message.role === 'agent'

  // Detect suggestion type from AI message content
  const detectSuggestionType = (content: string): SuggestionType => {
    const lowerContent = content.toLowerCase()
    
    if (lowerContent.includes('title') || lowerContent.includes('headline')) {
      return 'title_optimization'
    } else if (lowerContent.includes('script') || lowerContent.includes('dialogue')) {
      return 'script_suggestion'
    } else if (lowerContent.includes('hook') || lowerContent.includes('opening')) {
      return 'hook_improvement'
    } else if (lowerContent.includes('idea') || lowerContent.includes('concept')) {
      return 'content_idea'
    } else {
      return 'general'
    }
  }

  const shouldShowActions = !compact && isAgent && !isError && message.content.length > 50

  return (
    <div
      className={cn(
        'flex',
        compact ? 'mb-2' : 'mb-4',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      <div
        className={cn(
          'rounded-lg',
          compact ? 'max-w-[90%] px-3 py-2' : 'max-w-[80%] px-4 py-3',
          isUser
            ? 'bg-primary-600 text-white'
            : isError
            ? 'bg-red-600 text-white'
            : 'bg-dark-700 text-white'
        )}
      >
        {/* Message header */}
        {!compact && (
          <div className="text-xs opacity-70 mb-1">
            {isUser ? 'You' : isError ? 'Error' : 'AI Agent'}
          </div>
        )}
        
        {/* Message content */}
        <div className={cn(
          'whitespace-pre-wrap break-words',
          compact ? 'text-sm' : 'text-base'
        )}>
          {compact && message.content.length > 100 
            ? `${message.content.substring(0, 100)}...` 
            : message.content
          }
        </div>

        {/* Suggestion Actions for AI responses */}
        {shouldShowActions && (
          <SuggestionActions
            messageId={message.id}
            content={message.content}
            type={detectSuggestionType(message.content)}
          />
        )}
      </div>
    </div>
  )
}

export default memo(ChatMessage)