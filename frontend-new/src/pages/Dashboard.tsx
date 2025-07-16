import { useState } from 'react'
import { useUserStore } from '@/store/userStore'
import { useOAuthStore } from '@/store/oauthStore'
import TaskManager from '@/components/dashboard/TaskManager'
import ChannelGoals from '@/components/dashboard/ChannelGoals'
import ChatInterface from '@/components/chat/ChatInterface'
import OAuthStatus from '@/components/oauth/OAuthStatus'
import { Settings, RotateCcw } from 'lucide-react'

export default function Dashboard() {
  const { channelInfo, agentSettings, updateAgentSettings } = useUserStore()
  const { isAuthenticated, initiateOAuth, refreshToken, revokeToken, status } = useOAuthStore()
  const [showCustomization, setShowCustomization] = useState(false)
  const [tempSettings, setTempSettings] = useState(agentSettings)

  const availableAvatars = [
    'MateBlue.svg',
    'MateDarkBlue.svg', 
    'MateGreen.svg',
    'MateOrange.svg',
    'MatePink.svg',
    'MateRed.svg'
  ]

  const themeColors = [
    '#6366f1', // Blue
    '#8b5cf6', // Purple
    '#14b8a6', // Teal
    '#10b981', // Green
    '#f97316', // Orange
    '#ec4899', // Pink
    '#ef4444', // Red
    '#f59e0b'  // Yellow
  ]

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

  const handleSaveSettings = () => {
    updateAgentSettings(tempSettings)
    setShowCustomization(false)
  }

  const handleResetSettings = () => {
    const defaultSettings = {
      avatar: 'MateBlue.svg',
      name: 'Your Personal Agent',
      personality: 'professional' as const,
      responseLength: 'medium' as const,
    }
    setTempSettings(defaultSettings)
  }

  const handleCancelSettings = () => {
    setTempSettings(agentSettings)
    setShowCustomization(false)
  }

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">
            Welcome back, {channelInfo.name || 'Creator'}! 👋
          </h1>
          <p className="text-dark-400">
            Here's what's happening with your channel today
          </p>
        </div>
      </div>


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
                  <img 
                    src={`/assets/images/Avatars/${agentSettings.avatar}`}
                    className="h-12 w-12 rounded-full border-2 border-primary-500/50 cursor-pointer hover:scale-105 transition-transform" 
                    alt={agentSettings.name}
                    onClick={() => setShowCustomization(true)}
                  />
                  <div className="absolute -bottom-1 -right-1 bg-green-500 h-3 w-3 rounded-full border-2 border-dark-800"></div>
                </div>
                <div>
                  <h3 className="font-semibold text-white text-sm">{agentSettings.name}</h3>
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
                      value={tempSettings.name}
                      onChange={(e) => setTempSettings({...tempSettings, name: e.target.value})}
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
                          onClick={() => setTempSettings({...tempSettings, avatar})}
                          className={`relative p-1 rounded-lg transition-all ${
                            tempSettings.avatar === avatar 
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
                      {themeColors.map((color, index) => (
                        <button
                          key={index}
                          onClick={() => console.log('Theme color selected:', color)}
                          className="w-6 h-6 rounded hover:scale-110 transition-all"
                          style={{ backgroundColor: color }}
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
                        onClick={handleCancelSettings}
                        className="px-3 py-1 text-xs bg-gray-600 hover:bg-gray-700 text-white rounded transition-colors"
                      >
                        Cancel
                      </button>
                      <button
                        onClick={handleSaveSettings}
                        className="px-3 py-1 text-xs bg-primary-600 hover:bg-primary-700 text-white rounded transition-colors"
                      >
                        Save
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