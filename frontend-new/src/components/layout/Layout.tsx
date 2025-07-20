import { ReactNode } from 'react'
import TopAgentPanel from '@/components/agent/TopAgentPanel'
import MobileMenu from './MobileMenu'
import FullPageChatPanel from '@/components/chat/FullPageChatPanel'
import { FullChatProvider, useFullChat } from '@/contexts/FullChatContext'

interface LayoutProps {
  children: ReactNode
}

function LayoutContent({ children }: LayoutProps) {
  const { isFullChatOpen, closeFullChat } = useFullChat()

  return (
    <div className="flex flex-col h-screen bg-background-primary text-white">
      {/* Mobile Menu */}
      <MobileMenu />
      
      {/* Top AI Agent Panel */}
      <TopAgentPanel />
      
      {/* Main Layout Container */}
      <div className="flex flex-1 min-h-0 relative">        
        {/* Main Content Area - Now takes full width */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 min-w-0 pt-8">
          {children}
        </main>
      </div>

      {/* Full Page Chat Panel */}
      <FullPageChatPanel 
        isOpen={isFullChatOpen}
        onClose={closeFullChat}
      />

    </div>
  )
}

export default function Layout({ children }: LayoutProps) {
  return (
    <FullChatProvider>
      <LayoutContent>{children}</LayoutContent>
    </FullChatProvider>
  )
}