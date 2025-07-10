import { useState } from 'react'
import { useFloatingChatStore } from '@/store/floatingChatStore'
import { useAvatarStore } from '@/store/avatarStore'
import { useSuggestionStore } from '@/store/suggestionStore'
import { useChat } from '@/hooks/useChat'
import { cn } from '@/utils'
import { 
  Sparkles, 
  Settings, 
  Calendar, 
  TrendingUp, 
  Users, 
  Mic, 
  Trophy,
  Lightbulb,
  Zap
} from 'lucide-react'
import AvatarCustomizationPanel from './AvatarCustomizationPanel'
import SavedSuggestionsPanel from '@/components/suggestions/SavedSuggestionsPanel'

interface TopAgentPanelProps {
  className?: string
  onToggleChat?: () => void
  isChatOpen?: boolean
}

const impactTools = [
  {
    id: 'content_calendar',
    title: 'Content Calendar',
    icon: Calendar,
    description: 'Upcoming scheduled posts with color coding',
    gradient: 'from-blue-500 to-cyan-500',
    data: { scheduled: 12, thisWeek: 3 }
  },
  {
    id: 'performance_snapshot',
    title: 'Performance Snapshot',
    icon: TrendingUp,
    description: 'Key trends - views, CTR, growth',
    gradient: 'from-green-500 to-emerald-500',
    data: { views: '+24%', ctr: '3.2%', growth: '+12%' }
  },
  {
    id: 'ai_impact_counter',
    title: 'AI Impact Counter',
    icon: Lightbulb,
    description: 'Implemented AI suggestions and results',
    gradient: 'from-yellow-500 to-orange-500',
    data: { implemented: 8, success: '85%' }
  },
  {
    id: 'competitive_intelligence',
    title: 'Competitive Intelligence',
    icon: Users,
    description: 'Performance vs similar creators',
    gradient: 'from-purple-500 to-pink-500',
    data: { rank: '#3', category: 'Tech' }
  },
  {
    id: 'voice_command',
    title: 'Voice Command',
    icon: Mic,
    description: 'Voice interaction with AI assistant',
    gradient: 'from-red-500 to-pink-500',
    data: { active: false }
  },
  {
    id: 'creator_goals',
    title: 'Creator Goals',
    icon: Trophy,
    description: 'Progress toward custom objectives',
    gradient: 'from-indigo-500 to-purple-500',
    data: { progress: 67, target: '100K subs' }
  }
]

export default function TopAgentPanel({ className, onToggleChat }: TopAgentPanelProps) {
  const { openChat } = useFloatingChatStore()
  const { customization, openCustomization } = useAvatarStore()
  const { } = useSuggestionStore()
  const { sendMessage } = useChat()
  const [hasNewInsights] = useState(false)
  const [showSavedSuggestions, setShowSavedSuggestions] = useState(false)
  const [expandedTool, setExpandedTool] = useState<string | null>(null)
  
  const handleOpenChat = onToggleChat || openChat

  const handleToolClick = (toolId: string) => {
    setExpandedTool(expandedTool === toolId ? null : toolId)
    
    // Send appropriate message based on tool
    switch (toolId) {
      case 'content_calendar':
        sendMessage("Show me my content calendar and upcoming posts")
        break
      case 'performance_snapshot':
        sendMessage("Give me a performance snapshot of my recent videos")
        break
      case 'ai_impact_counter':
        sendMessage("Show me the impact of AI suggestions I've implemented")
        break
      case 'competitive_intelligence':
        sendMessage("Analyze my performance against similar creators")
        break
      case 'voice_command':
        sendMessage("Help me set up voice commands")
        break
      case 'creator_goals':
        sendMessage("Review my creator goals and progress")
        break
    }
    
    // Open chat window
    handleOpenChat()
  }

  const renderToolData = (tool: typeof impactTools[0]) => {
    switch (tool.id) {
      case 'content_calendar':
        return (
          <div className="flex items-center gap-2 text-xs">
            <span className="text-white/90">{tool.data.scheduled} posts</span>
            <div className="w-1 h-1 bg-white/50 rounded-full" />
            <span className="text-white/70">{tool.data.thisWeek} this week</span>
          </div>
        )
      case 'performance_snapshot':
        return (
          <div className="flex items-center gap-3 text-xs">
            <span className="text-green-300">{tool.data.views}</span>
            <span className="text-blue-300">{tool.data.ctr}</span>
            <span className="text-yellow-300">{tool.data.growth}</span>
          </div>
        )
      case 'ai_impact_counter':
        return (
          <div className="flex items-center gap-2 text-xs">
            <span className="text-orange-300">{tool.data.implemented}</span>
            <span className="text-white/70">•</span>
            <span className="text-green-300">{tool.data.success}</span>
          </div>
        )
      case 'competitive_intelligence':
        return (
          <div className="flex items-center gap-2 text-xs">
            <span className="text-purple-300">{tool.data.rank}</span>
            <span className="text-white/70">in {tool.data.category}</span>
          </div>
        )
      case 'voice_command':
        return (
          <div className="flex items-center gap-2 text-xs">
            <div className={cn(
              "w-2 h-2 rounded-full",
              tool.data.active ? "bg-green-400 animate-pulse" : "bg-gray-500"
            )} />
            <span className="text-white/70">
              {tool.data.active ? 'Listening' : 'Ready'}
            </span>
          </div>
        )
      case 'creator_goals':
        return (
          <div className="flex items-center gap-2 text-xs">
            <div className="w-12 h-1 bg-white/20 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-indigo-400 to-purple-400 transition-all duration-300"
                style={{ width: `${tool.data.progress}%` }}
              />
            </div>
            <span className="text-white/70">{tool.data.progress}%</span>
          </div>
        )
      default:
        return null
    }
  }

  return (
    <>
      <div className={cn(
        'w-full relative overflow-hidden',
        'bg-gradient-to-r from-indigo-600 via-purple-600 to-blue-600',
        'border-b border-white/20 backdrop-blur-sm',
        'transition-all duration-500 ease-in-out',
        'h-60', // Fixed height - no collapse functionality
        className
      )}>
        {/* Animated background elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-6 left-1/4 w-40 h-40 bg-white/5 rounded-full blur-xl animate-pulse" />
          <div className="absolute bottom-6 right-1/4 w-32 h-32 bg-white/5 rounded-full blur-xl animate-pulse delay-1000" />
          <div className="absolute top-12 right-1/3 w-24 h-24 bg-white/3 rounded-full blur-2xl animate-pulse delay-500" />
        </div>

        {/* Main content */}
        <div className="relative z-10 h-full flex items-center justify-between px-12 py-8">
          {/* Left Section - AI Avatar & Identity */}
          <div className="flex items-center gap-12">
            <div className="relative">
              <button
                onClick={handleOpenChat}
                className={cn(
                  'w-48 h-48 rounded-full flex items-center justify-center cursor-pointer transition-all duration-300',
                  'hover:scale-110 hover:shadow-xl hover:shadow-white/30',
                  'ring-4 ring-white/20 hover:ring-white/50',
                  'animate-pulse-subtle',
                  hasNewInsights && 'animate-bounce ring-yellow-400/60'
                )}
                style={{ backgroundColor: customization.color }}
                title="Click to open chat"
              >
                <img
                  src={`/assets/images/Avatars/${customization.avatar}`}
                  alt={customization.name}
                  className="w-44 h-44 rounded-full object-cover"
                  onError={(e) => {
                    e.currentTarget.src = '/assets/images/CM Logo White.svg'
                  }}
                />
                
                {hasNewInsights && (
                  <div className="absolute -top-3 -right-3 w-10 h-10 bg-yellow-400 rounded-full flex items-center justify-center animate-bounce">
                    <Sparkles className="w-5 h-5 text-white" />
                  </div>
                )}
              </button>
              
              {/* Settings button */}
              <button
                onClick={openCustomization}
                className="absolute -bottom-6 -left-6 w-12 h-12 bg-white/20 rounded-full border-2 border-white/40 flex items-center justify-center hover:bg-white/30 transition-colors backdrop-blur-sm"
                title="Customize agent"
              >
                <Settings className="w-6 h-6 text-white" />
              </button>
              
              {/* Chat microphone button */}
              <button
                onClick={handleOpenChat}
                className="absolute -bottom-6 -right-6 w-12 h-12 bg-white/20 rounded-full border-2 border-white/40 flex items-center justify-center hover:bg-white/30 transition-colors backdrop-blur-sm"
                title="Start chat"
              >
                <Mic className="w-6 h-6 text-white" />
              </button>
            </div>

            {/* Agent identity - Clean and prominent */}
            <div className="hidden sm:block">
              <div className="flex items-center gap-4">
                <div>
                  <h1 className="font-bold text-white text-4xl drop-shadow-sm tracking-tight">
                    {customization.name}
                  </h1>
                  <p className="text-white/70 text-lg font-medium mt-1">
                    Your YouTube Personal Agent
                  </p>
                </div>
                {hasNewInsights && (
                  <Zap className="w-8 h-8 text-yellow-400 animate-pulse drop-shadow-sm" />
                )}
              </div>
            </div>
          </div>

          {/* Right Section - Visual divider */}
          <div className="w-px h-24 bg-white/20" />

          {/* Center/Right Section - High-Impact Tools Grid */}
          <div className="flex-1 max-w-2xl">
            <div className="grid grid-cols-3 gap-4 px-8">
              {impactTools.map((tool) => (
                <button
                  key={tool.id}
                  onClick={() => handleToolClick(tool.id)}
                  className={cn(
                    'group relative overflow-hidden',
                    'bg-white/10 hover:bg-white/20 backdrop-blur-sm',
                    'border border-white/20 hover:border-white/40',
                    'rounded-xl p-4 h-20',
                    'transition-all duration-200',
                    'hover:scale-105 hover:shadow-lg hover:shadow-black/20',
                    'flex flex-col items-center justify-center',
                    expandedTool === tool.id && 'ring-2 ring-white/50 bg-white/20'
                  )}
                  title={tool.description}
                >
                  <div className={cn(
                    'absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-20 transition-opacity duration-200',
                    tool.gradient
                  )} />
                  
                  <tool.icon className="w-5 h-5 text-white mb-2 relative z-10" />
                  
                  <span className="text-white text-xs font-medium text-center leading-tight relative z-10">
                    {tool.title}
                  </span>
                  
                  <div className="mt-1 relative z-10">
                    {renderToolData(tool)}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* CreatorMate Logo */}
          <div className="flex items-center justify-center">
            <img
              src="/assets/images/CM Header White.svg"
              alt="CreatorMate"
              className="h-32 w-auto opacity-90 hover:opacity-100 transition-opacity duration-200"
            />
          </div>
        </div>
      </div>

      {/* Avatar customization panel */}
      <AvatarCustomizationPanel />

      {/* Saved Suggestions Panel */}
      <SavedSuggestionsPanel 
        isOpen={showSavedSuggestions} 
        onClose={() => setShowSavedSuggestions(false)} 
      />
    </>
  )
}