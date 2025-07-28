import { useRef } from 'react'
import ChatMessage from './ChatMessage'
import ThinkingIndicator from './ThinkingIndicator'
import ChatInput from './ChatInput'
import SimpleShortcuts from '@/components/agent/SimpleShortcuts'
import { useChat } from '@/hooks/useChat'

export default function ChatInterface() {
  const { messages, thinkingMessage, isLoading, sendMessage } = useChat()
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scrolling disabled to prevent unwanted page movement

  return (
    <div className="flex flex-col h-full min-h-0">
      {/* Shortcuts */}
      <div className="flex-shrink-0 mb-4">
        <SimpleShortcuts />
      </div>

      {/* Messages area with input inline */}
      <div className="flex-1 overflow-y-auto p-4 bg-black/20 rounded-lg min-h-0 chat-scroll">
        <div className="space-y-4">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          
          {thinkingMessage && (
            <ThinkingIndicator message={thinkingMessage} />
          )}
          
          {/* Chat input directly after last message */}
          <div className="pt-4">
            <ChatInput
              onSendMessage={sendMessage}
              disabled={isLoading}
            />
          </div>
          
          <div ref={messagesEndRef} />
        </div>
      </div>
    </div>
  )
}