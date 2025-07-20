import { useState, useEffect } from 'react'
import { useUserStore } from '@/store/userStore'
import { useOAuthStore } from '@/store/oauthStore'
import { useAvatarStore, brandColors } from '@/store/avatarStore'
import TaskManager from '@/components/dashboard/TaskManager'
import ChannelGoals from '@/components/dashboard/ChannelGoals'
import ChatInterface from '@/components/chat/ChatInterface'
import OAuthStatus from '@/components/oauth/OAuthStatus'
import { Settings, RotateCcw, Maximize2 } from 'lucide-react'
import { useFullChat } from '@/contexts/FullChatContext'

export default function Dashboard() {
  const { agentSettings } = useUserStore()
  const { isAuthenticated, initiateOAuth, refreshToken, revokeToken, status } = useOAuthStore()
  const { customization, setName, setAvatar, setColor, resetToDefaults } = useAvatarStore()
  const { openFullChat } = useFullChat()
  const [showCustomization, setShowCustomization] = useState(false)

  const availableAvatars = [
    'MateBlue.svg',
    'MateDarkBlue.svg', 
    'MateGreen.svg',
    'MateOrange.svg',
    'MatePink.svg',
    'MateRed.svg'
  ]

  // Use brandColors from avatarStore instead

  const personalityMap = {
    professional: 'Professional Assistant',
    friendly: 'Friendly Helper',
    energetic: 'Energetic Coach',
    analytical: 'Analytical Advisor',
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

  const handleResetSettings = () => {
    resetToDefaults()
  }

  const handleCloseCustomization = () => {
    setShowCustomization(false)
  }

  // Preserve scroll position on refresh - no auto-scrolling
  useEffect(() => {
    const savedScrollPosition = sessionStorage.getItem('dashboard-scroll-position')
    if (savedScrollPosition) {
      setTimeout(() => {
        window.scrollTo(0, parseInt(savedScrollPosition))
      }, 100)
      sessionStorage.removeItem('dashboard-scroll-position')
    }
    // Removed forced scroll to 0,0 to prevent unwanted scrolling

    // Save scroll position before page unload
    const handleBeforeUnload = () => {
      sessionStorage.setItem('dashboard-scroll-position', window.scrollY.toString())
    }

    window.addEventListener('beforeunload', handleBeforeUnload)
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload)
    }
  }, [])

  return (
    <div className="space-y-6">


      {/* Main Dashboard Grid - 50/50 Split */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[calc(100vh-200px)]">
        {/* Left Side - Task Manager & Channel Goals */}
        <div className="space-y-6 overflow-y-auto">
          <TaskManager />
          <ChannelGoals />
        </div>

        {/* Right Side - AI Agent Chat */}
        <div className="bg-dark-800/50 backdrop-blur-sm border border-primary-500/30 rounded-2xl p-4 h-full">
          {/* Compact Agent Header */}
          <div className="mb-4 pb-4 border-b border-primary-500/20">
            <div className="flex items-center justify-between">
              {/* Agent Avatar and Info */}
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div 
                    className="w-12 h-12 rounded-full flex items-center justify-center cursor-pointer hover:scale-105 transition-transform border-2"
                    style={{ backgroundColor: customization.color, borderColor: customization.color + '80' }}
                    onClick={() => setShowCustomization(true)}
                  >
                    <img 
                      src={`/assets/images/Avatars/${customization.avatar}`}
                      className="h-10 w-10 rounded-full" 
                      alt={customization.name}
                    />
                  </div>
                  <div className="absolute -bottom-1 -right-1 bg-green-500 h-3 w-3 rounded-full border-2 border-dark-800"></div>
                </div>
                <div>
                  <h3 className="font-semibold text-white text-sm">{customization.name}</h3>
                  <p className="text-xs text-dark-400">{personalityMap[agentSettings.personality]}</p>
                </div>
              </div>
              
              {/* Settings and YouTube Status */}
              <div className="flex items-center gap-2">
                <div className="relative">
                  <button
                    onClick={handleYouTubeClick}
                    className="px-2 py-1 bg-primary-600/20 hover:bg-primary-600/40 border border-primary-500/30 rounded-lg transition-colors text-xs"
                  >
                    <OAuthStatus showDetails={false} className="text-white" />
                  </button>
                </div>
                <button
                  onClick={openFullChat}
                  className="flex items-center gap-2 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium rounded-lg transition-colors"
                  title="Open full chat window"
                >
                  <Maximize2 className="w-4 h-4" />
                  <span>Full Chat</span>
                </button>
                <button
                  onClick={() => setShowCustomization(!showCustomization)}
                  className="p-2 bg-primary-600/20 hover:bg-primary-600/40 border border-primary-500/30 rounded-lg transition-colors"
                >
                  <Settings className="w-4 h-4 text-white" />
                </button>
              </div>
            </div>
            
            {/* Agent Customization Panel */}
            {showCustomization && (
              <div className="mt-3 pt-3 border-t border-primary-500/20">
                <div className="space-y-4">
                  {/* Agent Name */}
                  <div>
                    <label className="text-xs text-primary-400 mb-1 block">Agent Name</label>
                    <input
                      type="text"
                      value={customization.name}
                      onChange={(e) => setName(e.target.value)}
                      className="w-full px-2 py-1 bg-dark-700 border border-primary-500/30 rounded text-white text-xs focus:outline-none focus:border-primary-500"
                    />
                  </div>

                  {/* Avatar Selection */}
                  <div>
                    <label className="text-xs text-primary-400 mb-2 block">Avatar</label>
                    <div className="grid grid-cols-3 gap-2">
                      {availableAvatars.map((avatar) => (
                        <button
                          key={avatar}
                          onClick={() => setAvatar(avatar)}
                          className={`relative p-1 rounded-lg transition-all ${
                            customization.avatar === avatar 
                              ? 'bg-primary-600/30 border-2 border-primary-500' 
                              : 'bg-dark-700/50 border border-primary-500/20 hover:bg-primary-600/10'
                          }`}
                        >
                          <img
                            src={`/assets/images/Avatars/${avatar}`}
                            alt={avatar}
                            className="w-8 h-8 rounded-full mx-auto"
                          />
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Theme Colors */}
                  <div>
                    <label className="text-xs text-primary-400 mb-2 block">Theme Color</label>
                    <div className="grid grid-cols-4 gap-2">
                      {brandColors.map((color, index) => (
                        <button
                          key={index}
                          onClick={() => setColor(color.value)}
                          className={`w-6 h-6 rounded hover:scale-110 transition-all ${
                            customization.color === color.value ? 'ring-2 ring-white ring-offset-2 ring-offset-dark-800' : ''
                          }`}
                          style={{ backgroundColor: color.value }}
                          title={color.name}
                        />
                      ))}
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex justify-between pt-2">
                    <button
                      onClick={handleResetSettings}
                      className="flex items-center gap-1 px-2 py-1 text-xs text-gray-400 hover:text-white transition-colors"
                    >
                      <RotateCcw className="w-3 h-3" />
                      Reset
                    </button>
                    <div className="flex gap-2">
                      <button
                        onClick={handleCloseCustomization}
                        className="px-3 py-1 text-xs bg-primary-600 hover:bg-primary-700 text-white rounded transition-colors"
                      >
                        Close
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          <div className={`${showCustomization ? 'h-[calc(100%-320px)]' : 'h-[calc(100%-100px)]'} transition-all duration-200`}>
            <ChatInterface />
          </div>
        </div>
      </div>

    </div>
  )
}