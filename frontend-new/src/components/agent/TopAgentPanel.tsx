import React, { useState } from 'react'
import { NavLink } from 'react-router-dom'
import { useSuggestionStore } from '@/store/suggestionStore'
import { useOAuthStore } from '@/store/oauthStore'
import { useUserStore } from '@/store/userStore'
import { useChat } from '@/hooks/useChat'
import { cn } from '@/utils'
import QuickActionModal from './QuickActionModal'
import { 
  LayoutDashboard, 
  Building2, 
  Clapperboard, 
  Settings as SettingsIcon,
  LogOut,
  Layers
} from 'lucide-react'
import SavedSuggestionsPanel from '@/components/suggestions/SavedSuggestionsPanel'
import OAuthStatus from '@/components/oauth/OAuthStatus'

interface TopAgentPanelProps {
  className?: string
}

const navigation = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    name: 'Pillars',
    href: '/pillars',
    icon: Building2,
  },
  {
    name: 'Videos',
    href: '/videos',
    icon: Clapperboard,
  },
  {
    name: 'Content Studio',
    href: '/content-studio',
    icon: Layers,
  },
  {
    name: 'Settings',
    href: '/settings',
    icon: SettingsIcon,
  },
]


export default function TopAgentPanel({ className }: TopAgentPanelProps) {
  const { } = useSuggestionStore()
  const { isAuthenticated, initiateOAuth, refreshToken, revokeToken, status } = useOAuthStore()
  const { channelInfo, userId } = useUserStore()
  const { sendQuickAction } = useChat()
  const [showSavedSuggestions, setShowSavedSuggestions] = useState(false)
  const [selectedTool, setSelectedTool] = useState<{id: string, title: string, description: string, icon: string} | null>(null)
  const [bannerUrl, setBannerUrl] = React.useState('');

  React.useEffect(() => {
    const fetchBanner = async () => {
      if (!userId) {
        console.log('No userId available, skipping banner fetch');
        return;
      }

      try {
        const response = await fetch(`/api/get-user-profile?user_id=${userId}`, {
          credentials: 'include', // Include cookies
          headers: {
            'Content-Type': 'application/json',
          }
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const userData = await response.json();
        console.log('User profile data:', userData);
        if (userData && userData.bannerUrl) {
          console.log('Setting banner URL:', userData.bannerUrl);
          setBannerUrl(userData.bannerUrl);
        } else {
          console.log('No banner URL found in response');
        }
      } catch (error) {
        console.error('Error fetching user profile banner:', error);
      }
    };

    fetchBanner();
  }, [userId]); // Depend on userId so it refetches when user changes


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

  const handleLogout = async () => {
    if (!isAuthenticated) return
    
    const confirmed = confirm('Are you sure you want to logout from YouTube? You will need to reconnect to access video analytics.')
    if (confirmed) {
      await revokeToken()
      localStorage.removeItem('creatormate_user_id')
      window.location.href = '/'
    }
  }


  return (
    <>
  <div
    className={cn(
      'w-full relative overflow-hidden',
      !bannerUrl && 'bg-purple-900/95 backdrop-blur-md',
      'border-b border-white/20 backdrop-blur-sm',
      'transition-all duration-500 ease-in-out',
      'h-72', // Fixed height - balanced size
      className
    )}
    style={{
      backgroundImage: bannerUrl ? `url("${bannerUrl}")` : 'none',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      backgroundColor: bannerUrl ? 'transparent' : undefined,
    }}
  >
        {/* Dark overlay for banner to ensure content readability */}
        {bannerUrl && (
          <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" />
        )}
        
        {/* Animated background elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-6 left-1/4 w-40 h-40 bg-white/5 rounded-full blur-xl animate-pulse" />
          <div className="absolute bottom-6 right-1/4 w-32 h-32 bg-white/5 rounded-full blur-xl animate-pulse delay-1000" />
          <div className="absolute top-12 right-1/3 w-24 h-24 bg-white/3 rounded-full blur-2xl animate-pulse delay-500" />
        </div>

        {/* Main content */}
        <div className="relative z-10 h-full flex items-center justify-between px-12 py-8">
          {/* Left Section - Logo */}
          <div className="flex items-center">
            <img
              src="/assets/images/CM Logo White.svg"
              alt="CreatorMate"
              className="h-72 w-auto opacity-90 hover:opacity-100 transition-opacity duration-200"
            />
          </div>

          {/* Center Section - Welcome Message */}
          <div className="absolute left-1/2 transform -translate-x-1/2 top-1/2 -translate-y-1/2">
            <div className="text-white text-center">
              <h2 className="text-xl font-medium">
                Welcome back, {channelInfo.name || 'Creator'}! 👋
              </h2>
              <p className="text-white/70 text-base">Ready to grow your channel today</p>
            </div>
          </div>

          {/* Right Section - YouTube Connection */}
          <div className="flex items-center">
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

        {/* Navigation Bar - Bottom Edge */}
        <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 z-20">
          <div className="h-16 bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl shadow-lg hover:bg-white/20 hover:border-white/40 transition-all duration-200">
            <div className="flex items-center h-full overflow-hidden px-4">
              {/* Navigation */}
              <nav className="flex items-center px-4 space-x-2">
                {navigation.map((item) => (
                  <NavLink
                    key={item.name}
                    to={item.href}
                    className={({ isActive }) =>
                      cn(
                        'flex items-center gap-2 px-3 py-2 rounded-xl transition-all duration-200',
                        'hover:bg-white/10',
                        'text-white/70 hover:text-white',
                        'transform hover:scale-105 relative overflow-hidden',
                        'min-w-[40px] min-h-[40px] justify-start',
                        isActive && 'active bg-white/20 text-white font-medium'
                      )
                    }
                  >
                    <item.icon className="w-5 h-5 flex-shrink-0" />
                    <span className="whitespace-nowrap overflow-hidden font-medium text-sm">
                      {item.name}
                    </span>
                  </NavLink>
                ))}
                
              </nav>
              
              {/* Status section */}
              <div className="border-l border-white/20 pl-4 flex-shrink-0 flex items-center gap-3">
                <div className="flex items-center">
                  <div className="w-6 h-6 rounded-full bg-green-500/20 flex items-center justify-center">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  </div>
                  <span className="ml-2 text-sm text-white/70 whitespace-nowrap">
                    Online
                  </span>
                </div>
                
                {/* Logout button */}
                {isAuthenticated && (
                  <button
                    onClick={handleLogout}
                    className="flex items-center gap-2 px-2 py-1 rounded-lg transition-all duration-200 hover:bg-white/10 text-white/70 hover:text-white"
                    title="Logout from YouTube"
                  >
                    <LogOut className="w-4 h-4" />
                    <span className="text-xs font-medium">Logout</span>
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Saved Suggestions Panel */}
      <SavedSuggestionsPanel 
        isOpen={showSavedSuggestions} 
        onClose={() => setShowSavedSuggestions(false)} 
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