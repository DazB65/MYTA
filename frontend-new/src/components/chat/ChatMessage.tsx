import { memo } from 'react'
import { cn } from '@/utils'
import type { ChatMessage as ChatMessageType } from '@/types'
import SuggestionActions from './SuggestionActions'
import { SuggestionType } from '@/store/suggestionStore'
import { useAvatarStore } from '@/store/avatarStore'

interface ChatMessageProps {
  message: ChatMessageType
  compact?: boolean
}

function ChatMessage({ message, compact = false }: ChatMessageProps) {
  const { customization } = useAvatarStore()
  const isUser = message.role === 'user'
  const isError = message.isError
  const isAgent = message.role === 'agent'

  // Format timestamp
  const formatTime = (timestamp: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    }).format(new Date(timestamp))
  }

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
    <div className={cn('flex items-end gap-3 mb-4', isUser ? 'justify-end' : 'justify-start')}>
      {/* Agent Avatar */}
      {!isUser && !compact && (
        <div 
          className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0"
          style={{ backgroundColor: customization.color }}
        >
          <img
            src={`/assets/images/Avatars/${customization.avatar}`}
            alt={customization.name}
            className="w-6 h-6 rounded-full object-cover"
            onError={(e) => {
              e.currentTarget.src = '/assets/images/CM Logo White.svg'
            }}
          />
        </div>
      )}

      {/* Message Container */}
      <div className={cn('flex flex-col', isUser ? 'items-end' : 'items-start')}>
        {/* Message Bubble */}
        <div
          className={cn(
            'rounded-2xl px-4 py-3 max-w-md shadow-sm',
            isUser
              ? 'bg-primary-600 text-white rounded-br-md'
              : isError
              ? 'bg-red-600 text-white rounded-bl-md'
              : 'bg-dark-700 text-white border border-dark-600 rounded-bl-md',
            compact && 'max-w-xs px-3 py-2'
          )}
        >
          {/* Message content */}
          <div className={cn(
            'whitespace-pre-wrap break-words leading-relaxed',
            compact ? 'text-sm' : 'text-sm'
          )}>
            {compact && message.content.length > 100 
              ? `${message.content.substring(0, 100)}...` 
              : message.content
            }
          </div>

          {/* Suggestion Actions for AI responses */}
          {shouldShowActions && (
            <div className="mt-3 pt-3 border-t border-white/10">
              <SuggestionActions
                messageId={message.id}
                content={message.content}
                type={detectSuggestionType(message.content)}
              />
            </div>
          )}
        </div>

        {/* Timestamp */}
        <div className={cn(
          'text-xs text-dark-400 mt-1 px-1',
          isUser ? 'text-right' : 'text-left'
        )}>
          {formatTime(message.timestamp)}
        </div>
      </div>

      {/* User Avatar Placeholder */}
      {isUser && !compact && (
        <div className="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center flex-shrink-0">
          <span className="text-white text-sm font-medium">You</span>
        </div>
      )}
    </div>
  )
}

export default memo(ChatMessage)