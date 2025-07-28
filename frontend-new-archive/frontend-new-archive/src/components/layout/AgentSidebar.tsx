import { useState } from 'react'
import { Maximize2 } from 'lucide-react'
import ChatInterface from '@/components/chat/ChatInterface'
import FullPageChatPanel from '@/components/chat/FullPageChatPanel'
import QuickActions from '@/components/agent/QuickActions'
import AgentHeader from '@/components/agent/AgentHeader'
import InsightsPanel from '@/components/agent/InsightsPanel'
import OAuthConnection from '@/components/oauth/OAuthConnection'

interface AgentSidebarProps {
  isFullPageChatOpen?: boolean
  onCloseFullChat?: () => void
}

export default function AgentSidebar({ 
  isFullPageChatOpen = false, 
  onCloseFullChat = () => {} 
}: AgentSidebarProps) {
  const [localIsFullPageChatOpen, setLocalIsFullPageChatOpen] = useState(false)
  
  // Use prop if provided, otherwise use local state
  const chatOpen = isFullPageChatOpen || localIsFullPageChatOpen
  const closeChat = onCloseFullChat || (() => setLocalIsFullPageChatOpen(false))

  return (
    <>
      <aside className="w-80 xl:w-96 bg-background-secondary border-l border-white/10 flex flex-col h-screen">
      {/* Agent Header */}
      <div className="flex-shrink-0">
        <AgentHeader />
      </div>
      
      {/* Scrollable Content Area */}
      <div className="flex-1 flex flex-col min-h-0">
        {/* Insights Section */}
        <div className="px-4 flex-shrink-0">
          <div className="text-sm font-semibold text-dark-400 mb-3 uppercase tracking-wider">
            Insights
          </div>
          <InsightsPanel />
        </div>
        
        {/* OAuth Connection */}
        <div className="px-4 mt-6 flex-shrink-0">
          <OAuthConnection variant="sidebar" />
        </div>
        
        {/* Quick Actions */}
        <div className="px-4 mt-6 flex-shrink-0">
          <div className="text-sm font-semibold text-dark-400 mb-3 uppercase tracking-wider">
            Quick Actions
          </div>
          <QuickActions />
        </div>
        
        {/* Chat Interface - Takes remaining space */}
        <div className="flex-1 px-4 mt-6 flex flex-col min-h-0">
          <div className="flex-shrink-0 mb-3">
            <div className="text-sm font-semibold text-dark-400 mb-3 uppercase tracking-wider">
              Ask Your Agent
            </div>
            <button
              onClick={() => {
                console.log('Full chat button clicked!')
                setLocalIsFullPageChatOpen(true)
              }}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2 mb-4 z-10 relative"
              style={{ minHeight: '48px' }}
            >
              <Maximize2 className="w-4 h-4" />
              Open Full Chat Window
            </button>
          </div>
          <div className="flex-1 min-h-0 pb-4">
            <ChatInterface />
          </div>
        </div>
      </div>
      </aside>

      {/* Full Page Chat Panel */}
      <FullPageChatPanel 
        isOpen={chatOpen}
        onClose={closeChat}
      />
    </>
  )
}