import { useState } from 'react'
import { useUserStore } from '@/store/userStore'
import AvatarSelector from './AvatarSelector'

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
      <div className="bg-gradient-to-r from-primary-600 to-purple-600 p-4 m-4 rounded-xl">
        <div className="flex items-center gap-3 mb-3">
          <div
            className="w-12 h-12 rounded-full bg-gradient-to-br from-primary-500 to-purple-500 flex items-center justify-center cursor-pointer hover:scale-105 transition-transform"
            onClick={() => setShowAvatarSelector(true)}
          >
            <img
              src={`/assets/images/Avatars/${agentSettings.avatar}`}
              alt="AI Agent"
              className="w-10 h-10 rounded-full"
            />
          </div>
          <div>
            <h3 className="font-semibold text-white">{agentSettings.name}</h3>
            <p className="text-sm text-white/80">
              {personalityMap[agentSettings.personality]}
            </p>
          </div>
        </div>
        <div className="text-sm text-white/90">
          Ready to help!
        </div>
      </div>

      {showAvatarSelector && (
        <AvatarSelector onClose={() => setShowAvatarSelector(false)} />
      )}
    </>
  )
}