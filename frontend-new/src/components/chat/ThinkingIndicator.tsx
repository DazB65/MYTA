import type { ThinkingMessage } from '@/types'

interface ThinkingIndicatorProps {
  message: ThinkingMessage
  compact?: boolean
}

export default function ThinkingIndicator({ message, compact = false }: ThinkingIndicatorProps) {
  return (
    <div className={compact ? "flex justify-start mb-2" : "flex justify-start mb-4"}>
      <div className={compact 
        ? "max-w-[90%] rounded-lg px-3 py-2 bg-primary-700 text-white opacity-80 italic"
        : "max-w-[80%] rounded-lg px-4 py-3 bg-primary-700 text-white opacity-80 italic"
      }>
        {!compact && (
          <div className="text-xs opacity-70 mb-1">
            AI Agent
          </div>
        )}
        <div className="flex items-center gap-2">
          <div className="flex gap-1">
            <span className="w-2 h-2 bg-white rounded-full animate-thinking-pulse" style={{ animationDelay: '0s' }} />
            <span className="w-2 h-2 bg-white rounded-full animate-thinking-pulse" style={{ animationDelay: '0.2s' }} />
            <span className="w-2 h-2 bg-white rounded-full animate-thinking-pulse" style={{ animationDelay: '0.4s' }} />
          </div>
          <span className={compact ? "text-xs" : "text-sm"}>
            {compact && message.message.length > 50 
              ? `${message.message.substring(0, 50)}...` 
              : message.message
            }
          </span>
        </div>
      </div>
    </div>
  )
}