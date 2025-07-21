import { useRef, useEffect } from 'react'
import { X, MessageSquare, Minimize2 } from 'lucide-react'
import { cn } from '@/utils'
import ChatMessage from './ChatMessage'
import ThinkingIndicator from './ThinkingIndicator'
import ChatInput from './ChatInput'
import { useChat } from '@/hooks/useChat'

interface FullPageChatPanelProps {
  isOpen: boolean
  onClose: () => void
}

export default function FullPageChatPanel({ isOpen, onClose }: FullPageChatPanelProps) {
  const { messages, thinkingMessage, isLoading, sendMessage } = useChat()
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (isOpen && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, thinkingMessage, isOpen])

  // Handle escape key to close panel
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose()
      }
    }

    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [isOpen, onClose])

  return (
    <div className={cn(
      'fixed left-0 right-0 z-50',
      'bg-slate-900 border-b border-slate-700', // Removed transparency and backdrop-blur
      'transition-all duration-500 ease-in-out',
      'shadow-2xl',
      isOpen ? 'translate-y-0 opacity-100' : 'translate-y-[-100%] opacity-0',
      isOpen ? 'pointer-events-auto' : 'pointer-events-none'
    )}
    style={{ 
      top: '18rem', // Position below TopAgentPanel (h-72 = 18rem)
      height: isOpen ? 'calc(100vh - 18rem)' : '0' 
    }}
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-slate-700 bg-slate-800">
        <div className="flex items-center gap-3">
          <MessageSquare className="w-6 h-6 text-blue-400" />
          <h2 className="text-xl font-semibold text-white">Full Page Agent Chat</h2>
          <span className="text-sm text-gray-400">- Ask your AI agent anything</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors"
            title="Minimize (Esc)"
          >
            <Minimize2 className="w-5 h-5" />
          </button>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors"
            title="Close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Chat Content */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Messages area */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-6xl mx-auto space-y-6">
            {messages.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🤖</div>
                <h3 className="text-2xl font-semibold text-white mb-2">Start a conversation</h3>
                <p className="text-gray-400 text-lg">
                  Ask your AI agent about content strategy, video performance, or get creative ideas.
                </p>
                <div className="mt-6 flex flex-wrap justify-center gap-2">
                  <button
                    onClick={() => sendMessage("What are my best performing videos?")}
                    className="px-4 py-2 bg-blue-600/20 text-blue-300 rounded-lg hover:bg-blue-600/30 transition-colors text-sm"
                  >
                    📊 Video Performance
                  </button>
                  <button
                    onClick={() => sendMessage("Give me content ideas for my channel")}
                    className="px-4 py-2 bg-purple-600/20 text-purple-300 rounded-lg hover:bg-purple-600/30 transition-colors text-sm"
                  >
                    💡 Content Ideas
                  </button>
                  <button
                    onClick={() => sendMessage("How can I improve my thumbnails?")}
                    className="px-4 py-2 bg-green-600/20 text-green-300 rounded-lg hover:bg-green-600/30 transition-colors text-sm"
                  >
                    🎨 Thumbnail Tips
                  </button>
                </div>
              </div>
            ) : (
              <>
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
                
                {thinkingMessage && (
                  <ThinkingIndicator message={thinkingMessage} />
                )}
              </>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Chat input area - Fixed at bottom */}
        <div className="border-t border-slate-700 p-6 bg-slate-800 flex-shrink-0">
          <div className="max-w-6xl mx-auto">
            <ChatInput
              onSendMessage={sendMessage}
              disabled={isLoading}
              placeholder="Ask your agent anything about your content..."
            />
          </div>
        </div>
      </div>
    </div>
  )
}