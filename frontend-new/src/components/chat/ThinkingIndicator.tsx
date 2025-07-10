import type { ThinkingMessage } from '@/types'
import { useAvatarStore } from '@/store/avatarStore'

interface ThinkingIndicatorProps {
  message: ThinkingMessage
  compact?: boolean
}

export default function ThinkingIndicator({ message, compact = false }: ThinkingIndicatorProps) {
  const { customization } = useAvatarStore()
  
  return (
    <div className="flex items-end gap-3 mb-4">
      {/* Agent Avatar */}
      {!compact && (
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

      {/* Thinking Bubble */}
      <div className="flex flex-col items-start">
        <div className={compact 
          ? "max-w-xs rounded-2xl rounded-bl-md px-3 py-2 bg-dark-700/50 text-white border border-dark-600"
          : "max-w-md rounded-2xl rounded-bl-md px-4 py-3 bg-dark-700/50 text-white border border-dark-600"
        }>
          <div className="flex items-center gap-3">
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-primary-400 rounded-full animate-thinking-pulse" style={{ animationDelay: '0s' }} />
              <span className="w-2 h-2 bg-primary-400 rounded-full animate-thinking-pulse" style={{ animationDelay: '0.2s' }} />
              <span className="w-2 h-2 bg-primary-400 rounded-full animate-thinking-pulse" style={{ animationDelay: '0.4s' }} />
            </div>
            <span className={compact ? "text-xs text-dark-300" : "text-sm text-dark-300"}>
              {compact && message.message.length > 50 
                ? `${message.message.substring(0, 50)}...` 
                : message.message
              }
            </span>
          </div>
        </div>
        
        {/* Timestamp placeholder */}
        <div className="text-xs text-dark-400 mt-1 px-1">
          Now
        </div>
      </div>
    </div>
  )
}