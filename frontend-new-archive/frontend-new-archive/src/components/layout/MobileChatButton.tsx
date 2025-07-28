import { useState } from 'react'
import { MessageCircle, X } from 'lucide-react'
import ChatInterface from '@/components/chat/ChatInterface'
import AgentHeader from '@/components/agent/AgentHeader'
import { useAvatarStore } from '@/store/avatarStore'

export default function MobileChatButton() {
  const { customization } = useAvatarStore()
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      {/* Floating chat button */}
      <button
        onClick={() => setIsOpen(true)}
        className="lg:hidden fixed bottom-6 right-6 z-40 w-14 h-14 bg-primary-600 hover:bg-primary-700 rounded-full shadow-lg flex items-center justify-center transition-colors"
      >
        <MessageCircle className="w-6 h-6" />
      </button>

      {/* Mobile chat overlay */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="lg:hidden fixed inset-0 bg-black/50 z-40"
            onClick={() => setIsOpen(false)}
          />
          
          {/* Chat panel */}
          <div className="lg:hidden fixed inset-x-4 top-4 bottom-4 bg-background-secondary rounded-lg border border-white/10 z-50 flex flex-col max-w-md mx-auto">
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-white/10 flex-shrink-0">
              <h2 className="font-semibold">{customization.name}</h2>
              <button
                onClick={() => setIsOpen(false)}
                className="p-1 hover:bg-white/10 rounded"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Agent Header */}
            <div className="flex-shrink-0">
              <AgentHeader />
            </div>

            {/* Chat Interface */}
            <div className="flex-1 p-4 min-h-0">
              <ChatInterface />
            </div>
          </div>
        </>
      )}
    </>
  )
}