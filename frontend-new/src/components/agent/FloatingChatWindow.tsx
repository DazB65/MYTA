import { useState, useRef, useEffect, useCallback } from 'react'
import { X, Minus, Maximize2, Move } from 'lucide-react'
import { cn } from '@/utils'
import { useChat } from '@/hooks/useChat'
import { useAvatarStore } from '@/store/avatarStore'
import ChatMessage from '@/components/chat/ChatMessage'
import ThinkingIndicator from '@/components/chat/ThinkingIndicator'
import ChatInput from '@/components/chat/ChatInput'
import Button from '@/components/common/Button'

interface Position {
  x: number
  y: number
}

interface FloatingChatWindowProps {
  isOpen: boolean
  onClose: () => void
  onMinimize: () => void
  isMinimized: boolean
}

export default function FloatingChatWindow({ 
  isOpen, 
  onClose, 
  onMinimize, 
  isMinimized 
}: FloatingChatWindowProps) {
  const { messages, thinkingMessage, isLoading, sendMessage } = useChat()
  const { customization } = useAvatarStore()
  const [position, setPosition] = useState<Position>({ x: window.innerWidth * 0.1, y: 120 })
  const [isDragging, setIsDragging] = useState(false)
  const [startDragPosition, setStartDragPosition] = useState<Position>({ x: 0, y: 0 })
  const [isAnimating, setIsAnimating] = useState(false)
  const chatEndRef = useRef<HTMLDivElement>(null)
  const windowRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (chatEndRef.current && !isMinimized) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, thinkingMessage, isMinimized])

  // Handle dragging
  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    if (!windowRef.current) return
    
    setStartDragPosition({
      x: e.clientX,
      y: e.clientY
    })
    setIsDragging(true)
    
    // Prevent text selection during drag
    e.preventDefault()
    document.body.style.userSelect = 'none'
    document.body.style.cursor = 'move'
  }, [])

  const handleMouseMove = useCallback((e: MouseEvent) => {
    if (!isDragging) return

    // Calculate movement delta for smoother dragging
    const deltaX = e.clientX - startDragPosition.x
    const deltaY = e.clientY - startDragPosition.y
    
    const newX = position.x + deltaX
    const newY = position.y + deltaY

    // Constrain to viewport - 3x wider than previous size
    const windowWidth = 1728 // 3x wider than 576px (4.5x original)
    const windowHeight = isMinimized ? 60 : 400
    const maxX = window.innerWidth - windowWidth
    const maxY = window.innerHeight - windowHeight

    const constrainedPosition = {
      x: Math.max(0, Math.min(newX, maxX)),
      y: Math.max(0, Math.min(newY, maxY))
    }

    setPosition(constrainedPosition)
    setStartDragPosition({ x: e.clientX, y: e.clientY })
  }, [isDragging, startDragPosition, position, isMinimized])

  const handleMouseUp = useCallback(() => {
    setIsDragging(false)
    // Restore cursor and text selection
    document.body.style.userSelect = ''
    document.body.style.cursor = ''
  }, [])

  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
      return () => {
        document.removeEventListener('mousemove', handleMouseMove)
        document.removeEventListener('mouseup', handleMouseUp)
      }
    }
  }, [isDragging, handleMouseMove, handleMouseUp])

  // Animate window open/close
  useEffect(() => {
    if (isOpen) {
      setIsAnimating(true)
      const timer = setTimeout(() => setIsAnimating(false), 300)
      return () => clearTimeout(timer)
    }
  }, [isOpen])

  // Adjust position on window resize
  useEffect(() => {
    const handleResize = () => {
      const windowWidth = 1728 // 3x wider than previous size
      const windowHeight = isMinimized ? 60 : 400
      const maxX = window.innerWidth - windowWidth
      const maxY = window.innerHeight - windowHeight
      
      setPosition(prev => ({
        x: Math.max(0, Math.min(prev.x, maxX)),
        y: Math.max(0, Math.min(prev.y, maxY))
      }))
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [isMinimized])

  if (!isOpen) return null

  return (
    <>
      {/* Backdrop for focus */}
      <div className="fixed inset-0 z-40 pointer-events-none" />
      
      {/* Floating Chat Window */}
      <div
        ref={windowRef}
        className={cn(
          'fixed z-50 bg-background-secondary/95 backdrop-blur-md',
          'border border-white/20 rounded-xl shadow-2xl',
          'transition-all duration-300 ease-out',
          isOpen ? 'opacity-100 scale-100' : 'opacity-0 scale-95',
          isDragging ? 'cursor-move select-none' : 'cursor-default',
          isMinimized ? 'w-80 h-14' : 'w-[1728px] h-[400px]',
          isAnimating && 'animate-pulse'
        )}
        style={{
          left: position.x,
          top: position.y,
          transform: isOpen ? 'none' : 'translateY(-20px)'
        }}
      >
        {/* Header */}
        <div
          className={cn(
            'flex items-center justify-between p-4 border-b border-white/10',
            'bg-gradient-to-r from-primary-600/10 to-purple-600/10',
            'cursor-move select-none',
            isMinimized && 'border-b-0 rounded-xl'
          )}
          onMouseDown={handleMouseDown}
        >
          <div className="flex items-center gap-3">
            <div 
              className="w-8 h-8 rounded-full flex items-center justify-center"
              style={{ backgroundColor: customization.color }}
            >
              <img
                src={`/assets/images/Avatars/${customization.avatar}`}
                alt="AI Agent"
                className="w-7 h-7 rounded-full object-cover"
                onError={(e) => {
                  e.currentTarget.src = '/assets/images/CM Logo White.svg'
                }}
              />
            </div>
            {!isMinimized && (
              <div>
                <h3 className="font-semibold text-white text-sm">{customization.name}</h3>
                <p className="text-xs text-dark-400">AI Assistant</p>
              </div>
            )}
            {isMinimized && (
              <span className="text-sm font-medium text-white">{customization.name}</span>
            )}
          </div>

          <div className="flex items-center gap-1">
            <Button
              onClick={(e) => {
                e.stopPropagation()
                onMinimize()
              }}
              variant="ghost"
              size="xs"
              className="p-1.5 h-auto hover:bg-white/10"
            >
              {isMinimized ? (
                <Maximize2 className="w-3 h-3" />
              ) : (
                <Minus className="w-3 h-3" />
              )}
            </Button>
            <Button
              onClick={(e) => {
                e.stopPropagation()
                onClose()
              }}
              variant="ghost"
              size="xs"
              className="p-1.5 h-auto hover:bg-red-500/20 hover:text-red-400"
            >
              <X className="w-3 h-3" />
            </Button>
          </div>
        </div>

        {/* Chat Content - Only show when not minimized */}
        {!isMinimized && (
          <div className="flex h-[calc(100%-4rem)]">
            {/* Messages Area - Main chat section */}
            <div className="flex-1 flex flex-col min-w-0">
              <div className="flex-1 overflow-y-auto p-6 space-y-4 chat-scroll">
              {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center">
                  <div className="w-12 h-12 rounded-full bg-primary-500/20 flex items-center justify-center mb-3">
                    <Move className="w-6 h-6 text-primary-400" />
                  </div>
                  <p className="text-sm text-dark-400 mb-1">Start a conversation!</p>
                  <p className="text-xs text-dark-500">Drag me around to reposition</p>
                </div>
              ) : (
                <>
                  {messages.map((message) => (
                    <ChatMessage key={message.id} message={message} />
                  ))}
                  
                  {thinkingMessage && (
                    <ThinkingIndicator message={thinkingMessage} />
                  )}
                  
                  <div ref={chatEndRef} />
                </>
              )}
              </div>

              {/* Chat Input */}
              <div className="p-6 border-t border-white/10 bg-dark-800/30">
                <ChatInput
                  onSendMessage={sendMessage}
                  disabled={isLoading}
                  placeholder="Type your message..."
                  className="bg-dark-800/70 border-white/20 focus:ring-primary-500/50 py-3 text-base"
                />
              </div>
            </div>

            {/* Right Sidebar - Quick Actions and Analytics */}
            <div className="w-80 border-l border-white/10 bg-dark-800/20 flex flex-col">
              {/* Quick Actions Section */}
              <div className="p-6 border-b border-white/10">
                <h4 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
                  <span className="text-base">⚡</span>
                  Quick Actions
                </h4>
                <div className="space-y-2">
                  <button 
                    onClick={() => sendMessage("Generate a YouTube video script")}
                    disabled={isLoading}
                    className="w-full text-left p-3 rounded-lg bg-dark-700/50 hover:bg-dark-600/50 transition-colors text-sm disabled:opacity-50 flex items-center gap-3"
                  >
                    <span className="text-base">📝</span>
                    <span>Generate Script</span>
                  </button>
                  <button 
                    onClick={() => sendMessage("Help me optimize my video title")}
                    disabled={isLoading}
                    className="w-full text-left p-3 rounded-lg bg-dark-700/50 hover:bg-dark-600/50 transition-colors text-sm disabled:opacity-50 flex items-center gap-3"
                  >
                    <span className="text-base">🎯</span>
                    <span>Optimize Title</span>
                  </button>
                  <button 
                    onClick={() => sendMessage("Give me content ideas")}
                    disabled={isLoading}
                    className="w-full text-left p-3 rounded-lg bg-dark-700/50 hover:bg-dark-600/50 transition-colors text-sm disabled:opacity-50 flex items-center gap-3"
                  >
                    <span className="text-base">💡</span>
                    <span>Content Ideas</span>
                  </button>
                  <button 
                    onClick={() => sendMessage("Improve my video hooks")}
                    disabled={isLoading}
                    className="w-full text-left p-3 rounded-lg bg-dark-700/50 hover:bg-dark-600/50 transition-colors text-sm disabled:opacity-50 flex items-center gap-3"
                  >
                    <span className="text-base">🎣</span>
                    <span>Improve Hooks</span>
                  </button>
                </div>
              </div>

              {/* Chat Statistics */}
              <div className="p-6 border-b border-white/10">
                <h4 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
                  <span className="text-base">📊</span>
                  Chat Stats
                </h4>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-dark-400">Messages</span>
                    <span className="text-sm font-medium text-white">{messages.length}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-dark-400">Agent</span>
                    <span className="text-sm font-medium text-primary-400">{customization.name}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-dark-400">Status</span>
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                      <span className="text-sm font-medium text-green-400">Active</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recent Suggestions */}
              <div className="flex-1 p-6">
                <h4 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
                  <span className="text-base">🔖</span>
                  Recent Actions
                </h4>
                <div className="space-y-2">
                  <div className="text-xs text-dark-400 bg-dark-800/50 p-3 rounded-lg">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-green-400">✓</span>
                      <span>Script saved</span>
                    </div>
                    <div className="text-dark-500">2 minutes ago</div>
                  </div>
                  <div className="text-xs text-dark-400 bg-dark-800/50 p-3 rounded-lg">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-blue-400">💾</span>
                      <span>Suggestion saved</span>
                    </div>
                    <div className="text-dark-500">5 minutes ago</div>
                  </div>
                  <div className="text-xs text-dark-400 bg-dark-800/50 p-3 rounded-lg">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-yellow-400">👍</span>
                      <span>Helpful feedback</span>
                    </div>
                    <div className="text-dark-500">8 minutes ago</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Resize Handle */}
        {!isMinimized && (
          <div className="absolute bottom-0 right-0 w-4 h-4 cursor-nw-resize opacity-50 hover:opacity-100 transition-opacity">
            <div className="absolute bottom-1 right-1 w-2 h-2">
              <div className="w-full h-0.5 bg-white/40 mb-0.5" />
              <div className="w-full h-0.5 bg-white/40" />
            </div>
          </div>
        )}

        {/* Floating indicator when minimized */}
        {isMinimized && messages.length > 0 && (
          <div className="absolute -top-2 -right-2 w-6 h-6 bg-primary-500 rounded-full flex items-center justify-center text-xs font-bold text-white animate-pulse">
            {messages.length}
          </div>
        )}
      </div>
    </>
  )
}