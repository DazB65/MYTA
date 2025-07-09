import { ReactNode } from 'react'
import Sidebar from './Sidebar'
import TopAgentPanel from '@/components/agent/TopAgentPanel'
import FloatingChatWindow from '@/components/agent/FloatingChatWindow'
import MobileMenu from './MobileMenu'
import { useFloatingChatStore } from '@/store/floatingChatStore'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const { isOpen, isMinimized, closeChat, toggleMinimize } = useFloatingChatStore()

  return (
    <div className="flex flex-col h-screen bg-background-primary text-white">
      {/* Mobile Menu */}
      <MobileMenu />
      
      {/* Top AI Agent Panel */}
      <TopAgentPanel />
      
      {/* Main Layout Container */}
      <div className="flex flex-1 min-h-0 relative">        
        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 min-w-0">
          {children}
        </main>
      </div>

      {/* Bottom Navigation Sidebar - Fixed and Floating */}
      <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-40 hidden md:block">
        <Sidebar />
      </div>

      {/* Floating Chat Window */}
      <FloatingChatWindow
        isOpen={isOpen}
        isMinimized={isMinimized}
        onClose={closeChat}
        onMinimize={toggleMinimize}
      />
    </div>
  )
}