import { useState, useRef, useEffect } from 'react'
import { ChevronDown, CheckSquare, ArrowDown } from 'lucide-react'
import { cn } from '@/utils'
import { useChat } from '@/hooks/useChat'
import { useAvatarStore } from '@/store/avatarStore'
import ChatMessage from '@/components/chat/ChatMessage'
import ThinkingIndicator from '@/components/chat/ThinkingIndicator'
import ChatInput from '@/components/chat/ChatInput'
import Button from '@/components/common/Button'
import Card from '@/components/common/Card'
import QuickActionModal from './QuickActionModal'

interface Tool {
  id: string
  title: string
  description: string
  icon: string
  category: 'content' | 'optimization' | 'analysis' | 'planning'
  action: string
}

const creatorTools: Tool[] = [
  {
    id: 'script_generator',
    title: 'Script Generator',
    description: 'Generate engaging video scripts',
    icon: '📝',
    category: 'content',
    action: 'generate_script'
  },
  {
    id: 'title_optimizer',
    title: 'Title Optimizer',
    description: 'Create SEO-friendly titles',
    icon: '🎯',
    category: 'optimization',
    action: 'optimize_title'
  },
  {
    id: 'hook_improver',
    title: 'Hook Improver',
    description: 'Craft compelling video openings',
    icon: '🎣',
    category: 'content',
    action: 'improve_hooks'
  },
  {
    id: 'thumbnail_analyzer',
    title: 'Thumbnail Analyzer',
    description: 'Analyze thumbnail effectiveness',
    icon: '🖼️',
    category: 'analysis',
    action: 'analyze_thumbnail'
  },
  {
    id: 'trending_topics',
    title: 'Trending Topics',
    description: 'Discover trending topics',
    icon: '🔥',
    category: 'planning',
    action: 'get_trending'
  },
  {
    id: 'competitor_analysis',
    title: 'Competitor Analysis',
    description: 'Analyze competitor strategies',
    icon: '🕵️',
    category: 'analysis',
    action: 'analyze_competitors'
  },
  {
    id: 'content_calendar',
    title: 'Content Calendar',
    description: 'Plan your content strategy',
    icon: '📅',
    category: 'planning',
    action: 'create_calendar'
  },
  {
    id: 'engagement_booster',
    title: 'Engagement Booster',
    description: 'Increase viewer engagement',
    icon: '❤️',
    category: 'optimization',
    action: 'boost_engagement'
  }
]

const toolCategories = [
  { id: 'all', name: 'All Tools', icon: '🛠️' },
  { id: 'content', name: 'Content', icon: '📝' },
  { id: 'optimization', name: 'Optimization', icon: '⚡' },
  { id: 'analysis', name: 'Analytics', icon: '📊' },
  { id: 'planning', name: 'Planning', icon: '📋' }
]

interface FullPageChatPanelProps {
  isOpen: boolean
  onClose: () => void
  onConvertToTask: (message: any) => void
}

export default function FullPageChatPanel({ isOpen, onClose, onConvertToTask }: FullPageChatPanelProps) {
  const { messages, thinkingMessage, isLoading, sendMessage, sendQuickAction } = useChat()
  const { customization } = useAvatarStore()
  const [selectedToolCategory, setSelectedToolCategory] = useState<string>('all')
  const [convertedMessages, setConvertedMessages] = useState<Set<string>>(new Set())
  const [showScrollIndicator, setShowScrollIndicator] = useState(false)
  const [selectedTool, setSelectedTool] = useState<Tool | null>(null)
  const chatEndRef = useRef<HTMLDivElement>(null)
  const messagesAreaRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (chatEndRef.current && isOpen) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, thinkingMessage, isOpen])

  // Handle scroll indicator
  useEffect(() => {
    const handleScroll = () => {
      if (messagesAreaRef.current) {
        const { scrollTop, scrollHeight, clientHeight } = messagesAreaRef.current
        const isScrolledToBottom = scrollTop + clientHeight >= scrollHeight - 10
        setShowScrollIndicator(messages.length > 5 && !isScrolledToBottom)
      }
    }

    const messagesArea = messagesAreaRef.current
    if (messagesArea) {
      messagesArea.addEventListener('scroll', handleScroll)
      handleScroll() // Initial check
      return () => messagesArea.removeEventListener('scroll', handleScroll)
    }
  }, [messages.length])

  const scrollToBottom = () => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }

  // Filter tools based on selected category
  const filteredTools = selectedToolCategory === 'all' 
    ? creatorTools 
    : creatorTools.filter(tool => tool.category === selectedToolCategory)

  const handleConvertToTask = (message: any) => {
    setConvertedMessages(prev => new Set(prev).add(message.id))
    onConvertToTask(message)
  }

  const handleToolModalSubmit = (context: string) => {
    if (selectedTool) {
      sendQuickAction(selectedTool.action, context)
    }
    setSelectedTool(null)
  }

  const handleToolModalClose = () => {
    setSelectedTool(null)
  }

  if (!isOpen) return null

  return (
    <div 
      className={cn(
        'fixed inset-x-0 top-60 bottom-0 z-40 bg-background-secondary/95 backdrop-blur-md',
        'transform transition-transform duration-500 ease-out',
        isOpen ? 'translate-y-0' : 'translate-y-full'
      )}
    >
      {/* Header */}
      <div className="h-16 bg-gradient-to-r from-primary-600/10 to-purple-600/10 border-b border-white/10 px-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div 
            className="w-10 h-10 rounded-full flex items-center justify-center"
            style={{ backgroundColor: customization.color }}
          >
            <img
              src={`/assets/images/Avatars/${customization.avatar}`}
              alt={customization.name}
              className="w-8 h-8 rounded-full object-cover"
              onError={(e) => {
                e.currentTarget.src = '/assets/images/CM Logo White.svg'
              }}
            />
          </div>
          <div>
            <h3 className="font-semibold text-white">{customization.name}</h3>
            <p className="text-xs text-dark-400">Your YouTube Personal Agent</p>
          </div>
        </div>

        <button
          onClick={onClose}
          className="p-2 hover:bg-white/10 rounded-lg transition-colors"
        >
          <ChevronDown className="w-5 h-5 text-dark-400 hover:text-white" />
        </button>
      </div>

      {/* Main Content Area */}
      <div className="h-[calc(100%-4rem)] flex">
        {/* Chat Container */}
        <div className="flex-1 flex flex-col bg-background-secondary/50">
          
          {/* Chat Header with Agent Info */}
          <div className="flex-shrink-0 px-6 py-4 border-b border-white/10">
            <div className="flex items-center gap-3">
              <div 
                className="w-8 h-8 rounded-full flex items-center justify-center"
                style={{ backgroundColor: customization.color }}
              >
                <img
                  src={`/assets/images/Avatars/${customization.avatar}`}
                  alt={customization.name}
                  className="w-6 h-6 rounded-full object-cover"
                  onError={(e) => {
                    e.currentTarget.src = '/assets/images/CM Logo White.svg'
                  }}
                />
              </div>
              <div>
                <h3 className="font-medium text-white text-sm">{customization.name}</h3>
                <p className="text-xs text-dark-400">Active now</p>
              </div>
              {isLoading && (
                <div className="ml-auto flex items-center gap-2 text-xs text-primary-400">
                  <div className="w-2 h-2 bg-primary-400 rounded-full animate-pulse"></div>
                  Typing...
                </div>
              )}
            </div>
          </div>

          {/* Messages Area */}
          <div ref={messagesAreaRef} className="flex-1 overflow-y-auto p-4 space-y-1 min-h-0 scroll-smooth relative">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center">
                <div className="w-12 h-12 rounded-full bg-primary-500/20 flex items-center justify-center mb-3">
                  <span className="text-2xl">👋</span>
                </div>
                <h3 className="text-base font-medium mb-2 text-white">Welcome to CreatorMate!</h3>
                <p className="text-dark-400 text-sm mb-4 max-w-sm">
                  I'm here to help you grow your YouTube channel. Ask me anything or try a shortcut!
                </p>
                <div className="grid grid-cols-2 gap-2 max-w-xs">
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => sendMessage("Help me create a content strategy")}
                  >
                    📅 Strategy
                  </Button>
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => sendMessage("Analyze my channel performance")}
                  >
                    📊 Analytics
                  </Button>
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => sendMessage("Generate video ideas for my niche")}
                  >
                    💡 Ideas
                  </Button>
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => sendMessage("Improve my video SEO")}
                  >
                    🎯 SEO
                  </Button>
                </div>
              </div>
            ) : (
              <>
                {messages.map((message) => (
                  <div key={message.id} className="relative group">
                    <ChatMessage message={message} />
                    
                    {/* Convert to Task button for agent messages */}
                    {message.role === 'agent' && !convertedMessages.has(message.id) && (
                      <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <Button
                          size="xs"
                          variant="secondary"
                          onClick={() => handleConvertToTask(message)}
                          className="flex items-center gap-1 text-xs px-2 py-1"
                        >
                          <CheckSquare className="w-3 h-3" />
                          Convert to Task
                        </Button>
                      </div>
                    )}
                    
                    {/* Visual indicator for converted messages */}
                    {convertedMessages.has(message.id) && (
                      <div className="absolute top-2 right-2">
                        <div className="flex items-center gap-1 text-xs text-green-400 bg-green-400/10 px-2 py-1 rounded">
                          <CheckSquare className="w-3 h-3" />
                          Added to Tasks
                        </div>
                      </div>
                    )}
                  </div>
                ))}
                
                {thinkingMessage && (
                  <ThinkingIndicator message={thinkingMessage} />
                )}
                
                <div ref={chatEndRef} />
              </>
            )}
            
            {/* Scroll to bottom indicator */}
            {showScrollIndicator && (
              <button
                onClick={scrollToBottom}
                className="absolute bottom-4 right-4 w-10 h-10 bg-primary-600 hover:bg-primary-700 rounded-full flex items-center justify-center shadow-lg transition-colors z-10"
              >
                <ArrowDown className="w-4 h-4 text-white" />
              </button>
            )}
          </div>

          {/* Chat Input - Fixed at bottom */}
          <div className="flex-shrink-0 border-t border-white/10 p-4 bg-background-secondary/80 backdrop-blur-sm">
            <ChatInput
              onSendMessage={sendMessage}
              disabled={isLoading}
              placeholder="Ask me anything about growing your YouTube channel..."
              className="bg-dark-800/70 border-white/20 focus:ring-primary-500/50"
            />
          </div>
        </div>

        {/* Right Sidebar - Shortcuts */}
        <div className="w-80 border-l border-white/10 bg-gradient-to-b from-primary-600/5 to-purple-600/5 flex flex-col">
          <div className="p-4 flex-1 flex flex-col">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-sm font-semibold text-white flex items-center gap-2">
                <span className="text-base">⚡</span>
                Shortcuts
              </h4>
            </div>

            {/* Category Filter */}
            <div className="mb-4">
              <div className="flex flex-wrap gap-1">
                {toolCategories.map((category) => (
                  <button
                    key={category.id}
                    onClick={() => setSelectedToolCategory(category.id)}
                    className={`text-xs px-2 py-1 rounded transition-colors ${
                      selectedToolCategory === category.id
                        ? 'bg-primary-600 text-white'
                        : 'bg-dark-700/50 text-dark-400 hover:text-white hover:bg-dark-600/50'
                    }`}
                  >
                    <span className="mr-1">{category.icon}</span>
                    {category.name}
                  </button>
                ))}
              </div>
            </div>

            {/* Tools Grid */}
            <div className="flex-1 overflow-y-auto">
              <div className="grid gap-2 grid-cols-1">
                {filteredTools.map((tool) => (
                  <button
                    key={tool.id}
                    onClick={() => setSelectedTool(tool)}
                    disabled={isLoading}
                    className="text-left p-3 rounded-lg bg-dark-700/50 hover:bg-dark-600/50 transition-colors text-sm disabled:opacity-50 group"
                  >
                    <div className="flex items-start gap-2">
                      <span className="text-base flex-shrink-0">{tool.icon}</span>
                      <div className="min-w-0">
                        <div className="font-medium text-white group-hover:text-primary-300 transition-colors">
                          {tool.title}
                        </div>
                        <div className="text-xs text-dark-400 mt-1 leading-tight">
                          {tool.description}
                        </div>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Pro Tips */}
            <Card className="mt-4 p-3 bg-dark-800/30">
              <div className="text-xs font-medium text-primary-400 mb-2">💡 Pro Tip</div>
              <div className="text-xs text-dark-300 leading-relaxed">
                You can convert any of my suggestions into actionable tasks. Just hover over a message and click "Convert to Task"!
              </div>
            </Card>
          </div>
        </div>
      </div>

      {/* Tool Modal */}
      {selectedTool && (
        <QuickActionModal
          isOpen={!!selectedTool}
          onClose={handleToolModalClose}
          onSubmit={handleToolModalSubmit}
          action={{
            id: selectedTool.action,
            title: selectedTool.title,
            description: selectedTool.description,
            icon: selectedTool.icon
          }}
          isLoading={isLoading}
        />
      )}
    </div>
  )
}