import { createContext, useContext, useState, ReactNode } from 'react'

interface FullChatContextType {
  isFullChatOpen: boolean
  openFullChat: () => void
  closeFullChat: () => void
}

const FullChatContext = createContext<FullChatContextType | undefined>(undefined)

export function FullChatProvider({ children }: { children: ReactNode }) {
  const [isFullChatOpen, setIsFullChatOpen] = useState(false)

  const openFullChat = () => {
    console.log('Opening full chat panel from context')
    setIsFullChatOpen(true)
  }

  const closeFullChat = () => {
    console.log('Closing full chat panel from context')
    setIsFullChatOpen(false)
  }

  return (
    <FullChatContext.Provider value={{ isFullChatOpen, openFullChat, closeFullChat }}>
      {children}
    </FullChatContext.Provider>
  )
}

export function useFullChat() {
  const context = useContext(FullChatContext)
  if (context === undefined) {
    throw new Error('useFullChat must be used within a FullChatProvider')
  }
  return context
}