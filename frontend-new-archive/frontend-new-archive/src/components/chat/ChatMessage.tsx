import { memo, useState } from 'react'
import { cn } from '@/utils'
import type { ChatMessage as ChatMessageType } from '@/types'
import SuggestionActions from './SuggestionActions'
import { SuggestionType } from '@/store/suggestionStore'
import { useAvatarStore } from '@/store/avatarStore'
import { useSavedMessagesStore } from '@/store/savedMessagesStore'
import { Bookmark, BookmarkCheck } from 'lucide-react'

interface ChatMessageProps {
  message: ChatMessageType
  compact?: boolean
}

function ChatMessage({ message, compact = false }: ChatMessageProps) {
  const { customization } = useAvatarStore()
  const { saveMessage, unsaveMessage, isMessageSaved } = useSavedMessagesStore()
  const [showActions, setShowActions] = useState(false)
  const isUser = message.role === 'user'
  const isError = message.isError
  const isAgent = message.role === 'agent'
  const isSaved = isMessageSaved(message.content)

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

  const handleSaveMessage = () => {
    if (isSaved) {
      // Find and unsave the message
      const savedMessages = useSavedMessagesStore.getState().savedMessages
      const savedMessage = savedMessages.find(msg => msg.content === message.content)
      if (savedMessage) {
        unsaveMessage(savedMessage.id)
      }
    } else {
      // Save the message
      saveMessage({
        content: message.content,
        agentName: customization.name,
        avatar: customization.avatar,
        category: detectSuggestionType(message.content) === 'general' ? 'General' : 'Ideas'
      })
    }
  }

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
            'rounded-2xl px-4 py-3 shadow-sm relative group',
            isUser
              ? 'bg-primary-600 text-white rounded-br-md max-w-md'
              : isError
              ? 'bg-red-600 text-white rounded-bl-md max-w-md'
              : 'bg-dark-700 text-white border border-dark-600 rounded-bl-md max-w-full',
            compact && 'max-w-xs px-3 py-2'
          )}
          onMouseEnter={() => setShowActions(true)}
          onMouseLeave={() => setShowActions(false)}
        >
          {/* Save for Later Button - Only for AI messages */}
          {!isUser && !compact && !isError && (
            <div className={cn(
              'absolute top-2 right-2 transition-opacity duration-200',
              showActions ? 'opacity-100' : 'opacity-0'
            )}>
              <button
                onClick={handleSaveMessage}
                className={cn(
                  'p-1.5 rounded-full transition-colors duration-200',
                  isSaved 
                    ? 'bg-yellow-500/20 text-yellow-400 hover:bg-yellow-500/30' 
                    : 'bg-white/10 text-white/60 hover:bg-white/20 hover:text-white'
                )}
                title={isSaved ? 'Remove from saved' : 'Save for later'}
              >
                {isSaved ? (
                  <BookmarkCheck className="w-4 h-4" />
                ) : (
                  <Bookmark className="w-4 h-4" />
                )}
              </button>
            </div>
          )}
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