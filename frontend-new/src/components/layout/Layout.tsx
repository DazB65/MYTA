import { ReactNode, useState } from 'react'
import Sidebar from './Sidebar'
import TopAgentPanel from '@/components/agent/TopAgentPanel'
import FullPageChatPanel from '@/components/agent/FullPageChatPanel'
import TaskCreationModal from '@/components/dashboard/TaskCreationModal'
import MobileMenu from './MobileMenu'
import { useFloatingChatStore } from '@/store/floatingChatStore'
import { useAvatarStore } from '@/store/avatarStore'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const { isOpen, toggleChat } = useFloatingChatStore()
  const { customization } = useAvatarStore()
  const [taskModalOpen, setTaskModalOpen] = useState(false)
  const [taskModalData, setTaskModalData] = useState<any>(null)

  const handleConvertToTask = (message: any) => {
    setTaskModalData({
      messageContent: message.content,
      agentName: customization.name
    })
    setTaskModalOpen(true)
  }

  const handleCreateTask = (task: any) => {
    // Store in localStorage
    const existingTasks = JSON.parse(localStorage.getItem('creatormate_tasks') || '[]')
    localStorage.setItem('creatormate_tasks', JSON.stringify([task, ...existingTasks]))
    
    // Dispatch event to notify TaskManager
    window.dispatchEvent(new Event('taskUpdate'))
    
    setTaskModalOpen(false)
    setTaskModalData(null)
  }

  return (
    <div className="flex flex-col h-screen bg-background-primary text-white">
      {/* Mobile Menu */}
      <MobileMenu />
      
      {/* Top AI Agent Panel with Chat Toggle */}
      <TopAgentPanel onToggleChat={toggleChat} isChatOpen={isOpen} />
      
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

      {/* Full Page Chat Panel */}
      <FullPageChatPanel
        isOpen={isOpen}
        onClose={toggleChat}
        onConvertToTask={handleConvertToTask}
      />

      {/* Task Creation Modal */}
      {taskModalOpen && taskModalData && (
        <TaskCreationModal
          isOpen={taskModalOpen}
          onClose={() => setTaskModalOpen(false)}
          onCreateTask={handleCreateTask}
          messageContent={taskModalData.messageContent}
          agentName={taskModalData.agentName}
        />
      )}
    </div>
  )
}