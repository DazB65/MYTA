import { useState } from 'react'
import { useFloatingChatStore } from '@/store/floatingChatStore'
import { useAvatarStore } from '@/store/avatarStore'
import { useSuggestionStore } from '@/store/suggestionStore'
import { useSavedMessagesStore } from '@/store/savedMessagesStore'
import { useOAuthStore } from '@/store/oauthStore'
import { useUserStore } from '@/store/userStore'
import { useChat } from '@/hooks/useChat'
import { cn } from '@/utils'
import QuickActionModal from './QuickActionModal'
import { 
  Sparkles, 
  Settings, 
  Mic, 
  Zap,
  Bookmark
} from 'lucide-react'
import AvatarCustomizationPanel from './AvatarCustomizationPanel'
import SavedSuggestionsPanel from '@/components/suggestions/SavedSuggestionsPanel'
import { SavedMessagesPanel } from '@/components/SavedMessagesPanel'
import OAuthStatus from '@/components/oauth/OAuthStatus'

interface TopAgentPanelProps {
  className?: string
  onToggleChat?: () => void
  isChatOpen?: boolean
}


export default function TopAgentPanel({ className, onToggleChat }: TopAgentPanelProps) {
  const { openChat } = useFloatingChatStore()
  const { customization, openCustomization } = useAvatarStore()
  const { } = useSuggestionStore()
  const { savedMessages } = useSavedMessagesStore()
  const { isAuthenticated, initiateOAuth, refreshToken, revokeToken, status } = useOAuthStore()
  const { channelInfo } = useUserStore()
  const { sendQuickAction } = useChat()
  const [hasNewInsights] = useState(false)
  const [showSavedSuggestions, setShowSavedSuggestions] = useState(false)
  const [showSavedMessages, setShowSavedMessages] = useState(false)
  const [selectedTool, setSelectedTool] = useState<{id: string, title: string, description: string, icon: string} | null>(null)
  
  const handleOpenChat = onToggleChat || openChat


  const handleToolModalSubmit = (context: string) => {
    if (selectedTool) {
      // Map tool ID to appropriate action
      const actionMap: {[key: string]: string} = {
        'content_calendar': 'get_content_calendar',
        'performance_snapshot': 'get_performance_snapshot',
        'ai_impact_counter': 'get_ai_impact',
        'competitive_intelligence': 'get_competitive_analysis',
        'voice_command': 'setup_voice_commands',
        'creator_goals': 'review_goals'
      }
      
      const action = actionMap[selectedTool.id] || selectedTool.id
      sendQuickAction(action, context)
    }
    setSelectedTool(null)
  }

  const handleToolModalClose = () => {
    setSelectedTool(null)
  }

  const handleYouTubeClick = () => {
    if (!isAuthenticated) {
      initiateOAuth()
    } else if (status?.needs_refresh) {
      refreshToken()
    } else {
      const action = confirm('YouTube is connected. Would you like to disconnect?')
      if (action) {
        revokeToken()
      }
    }
  }


  return (
    <>
      <div className={cn(
        'w-full relative overflow-hidden',
        'bg-purple-900/95 backdrop-blur-md',
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

              {/* Saved Messages button */}
              <button
                onClick={() => setShowSavedMessages(true)}
                className="absolute -top-6 -right-6 w-12 h-12 bg-white/20 rounded-full border-2 border-white/40 flex items-center justify-center hover:bg-white/30 transition-colors backdrop-blur-sm"
                title="Saved chats"
              >
                <Bookmark className="w-6 h-6 text-white" />
                {savedMessages.length > 0 && (
                  <div className="absolute -top-2 -right-2 w-5 h-5 bg-yellow-500 rounded-full flex items-center justify-center">
                    <span className="text-xs font-bold text-white">{savedMessages.length}</span>
                  </div>
                )}
              </button>
            </div>

            {/* Agent identity - Clean and prominent */}
            <div className="hidden sm:block">
              <div className="flex items-center gap-4">
                <div>
                  <h1 className="font-bold text-white text-4xl drop-shadow-sm tracking-tight">
                    {customization.name}
                  </h1>
                  <p className="text-white/80 text-lg font-medium mt-1">Your Personal Agent Mate</p>
                </div>
                {hasNewInsights && (
                  <Zap className="w-8 h-8 text-yellow-400 animate-pulse drop-shadow-sm" />
                )}
              </div>
            </div>
          </div>

          {/* Right Section - Visual divider */}
          <div className="w-px h-24 bg-white/20" />

          {/* CreatorMate Logo and YouTube Connection */}
          <div className="flex-1 flex justify-between items-center px-8">
            {/* Logo positioned on the left - larger */}
            <div className="flex items-center flex-1">
              <img
                src="/assets/images/CM Text White.svg"
                alt="CreatorMate"
                className="h-24 w-auto opacity-90 hover:opacity-100 transition-opacity duration-200"
              />
              <div className="text-sm text-white/80 ml-3 font-medium tracking-wide">YOUR CREATOR AGENT</div>
            </div>
            
            {/* YouTube connection section moved to right */}
            <div 
              className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg p-4 w-[400px] hover:bg-white/20 hover:border-white/40 transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              <div className="flex flex-col gap-3">
                <div className="flex items-center justify-between">
                  <OAuthStatus showDetails={true} className="text-white flex-1" />
                  <div className="ml-2 text-white/60 text-xs">
                    {isAuthenticated ? '✓' : 'Click to connect'}
                  </div>
                </div>
                
                {isAuthenticated && channelInfo.name !== 'Unknown' && (
                  <div className="text-xs text-white/90 bg-white/15 px-3 py-2 rounded-lg border border-white/20">
                    <div className="flex items-center gap-2">
                      <span>📺</span>
                      <span className="font-medium">{channelInfo.name}</span>
                    </div>
                  </div>
                )}
                
                {!isAuthenticated && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleYouTubeClick();
                    }}
                    className="w-full bg-red-600 hover:bg-red-700 text-white text-xs font-medium py-2 px-3 rounded-lg transition-colors duration-200"
                  >
                    Connect YouTube
                  </button>
                )}
                
                {isAuthenticated && (
                  <div className="flex gap-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        refreshToken();
                      }}
                      className="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium py-2 px-3 rounded-lg transition-colors duration-200"
                    >
                      🔄 Refresh
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        if (confirm('Disconnect YouTube account?')) {
                          revokeToken();
                        }
                      }}
                      className="flex-1 bg-gray-600 hover:bg-gray-700 text-white text-xs font-medium py-2 px-3 rounded-lg transition-colors duration-200"
                    >
                      🔌 Disconnect
                    </button>
                  </div>
                )}
              </div>
            </div>
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

      {/* Saved Messages Panel */}
      <SavedMessagesPanel 
        isOpen={showSavedMessages} 
        onClose={() => setShowSavedMessages(false)} 
      />

      {/* Tool Modal */}
      {selectedTool && (
        <QuickActionModal
          isOpen={!!selectedTool}
          onClose={handleToolModalClose}
          onSubmit={handleToolModalSubmit}
          action={selectedTool}
          isLoading={false}
        />
      )}
    </>
  )
}