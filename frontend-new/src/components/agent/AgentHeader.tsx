import { useState } from 'react'
import { useUserStore } from '@/store/userStore'
import AvatarSelector from './AvatarSelector'
import OAuthStatus from '@/components/oauth/OAuthStatus'

export default function AgentHeader() {
  const { agentSettings } = useUserStore()
  const [showAvatarSelector, setShowAvatarSelector] = useState(false)

  const personalityMap = {
    professional: 'Professional Assistant',
    friendly: 'Friendly Helper',
    energetic: 'Energetic Coach',
    analytical: 'Analytical Advisor',
  }

  return (
    <>
      <div className="w-full bg-purple-900/95 backdrop-blur-md p-4 rounded-lg">
        {/* DEBUG: Changes applied at ${new Date().toISOString()} */}
        <div className="flex items-center justify-between">
          {/* Left side with Agent */}
          <div className="flex items-center gap-4">
            <div className="relative">
              <img 
                src={`/assets/images/Avatars/${agentSettings.avatar}`}
                className="h-16 w-16 rounded-full border-2 border-white/30 animate-pulse hover:animate-none transition-all duration-300 cursor-pointer hover:scale-105" 
                alt={agentSettings.name}
                onClick={() => setShowAvatarSelector(true)}
              />
              <div className="absolute -bottom-1 -right-1 bg-green-500 h-4 w-4 rounded-full border-2 border-gray-800"></div>
            </div>
            
            <div>
              <h2 className="text-xl font-bold text-white">{agentSettings.name}</h2>
              <p className="text-white/80 text-sm">{personalityMap[agentSettings.personality]}</p>
            </div>
          </div>
          
          {/* Center cards - interactive metric cards */}
          <div className="flex gap-3">
            <div className="bg-white/10 hover:bg-white/20 transition-colors p-3 rounded-lg border border-white/20 cursor-pointer group">
              <div className="text-xs text-white/60">Content Calendar</div>
              <div className="text-white font-medium">12 posts · 3 this week</div>
              <div className="h-0 overflow-hidden group-hover:h-auto group-hover:mt-2 transition-all text-xs text-white/80">
                {agentSettings.name} suggests: Schedule more gaming content on Thursdays
              </div>
            </div>
            
            <div className="bg-white/10 hover:bg-white/20 transition-colors p-3 rounded-lg border border-white/20 cursor-pointer group">
              <div className="text-xs text-white/60">Analytics</div>
              <div className="text-white font-medium">+24% views</div>
              <div className="h-0 overflow-hidden group-hover:h-auto group-hover:mt-2 transition-all text-xs text-white/80">
                Great momentum! Your recent thumbnails are performing well
              </div>
            </div>
            
            <div className="bg-white/10 hover:bg-white/20 transition-colors p-3 rounded-lg border border-white/20 cursor-pointer group">
              <div className="text-xs text-white/60">Engagement</div>
              <div className="text-white font-medium">8.2% CTR</div>
              <div className="h-0 overflow-hidden group-hover:h-auto group-hover:mt-2 transition-all text-xs text-white/80">
                Above average! Your titles are getting more clicks
              </div>
            </div>
          </div>
          
          {/* Right side with CreatorMate logo and YouTube connection */}
          <div className="flex flex-col items-end space-y-3">
            {/* Logo section moved up */}
            <div className="flex items-center">
              <img src="/assets/images/CM Logo White.svg" alt="CreatorMate" className="h-8" />
              <div className="text-xs text-white/80 ml-2 font-medium tracking-wide">YOUR CREATOR AGENT</div>
            </div>
            
            {/* YouTube connection section */}
            <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg p-3 min-w-[200px]">
              <OAuthStatus showDetails={true} className="text-white" />
            </div>
          </div>
        </div>
      </div>

      {showAvatarSelector && (
        <AvatarSelector onClose={() => setShowAvatarSelector(false)} />
      )}
    </>
  )
}