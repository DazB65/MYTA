import { useState } from 'react'
import { useUserStore } from '@/store/userStore'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'

interface AvatarSelectorProps {
  onClose: () => void
}

const avatars = [
  'Avatar1.svg',
  'Avatar2.svg', 
  'Avatar3.svg',
  'Avatar4.svg',
  'Avatar5.svg',
  'Avatar6.svg',
  'Avatar7.svg',
  'Avatar8.svg',
]

const personalities = [
  { id: 'professional', name: 'Professional', description: 'Formal and focused' },
  { id: 'friendly', name: 'Friendly', description: 'Warm and approachable' },
  { id: 'energetic', name: 'Energetic', description: 'Enthusiastic and motivating' },
  { id: 'analytical', name: 'Analytical', description: 'Data-driven and detailed' },
]

export default function AvatarSelector({ onClose }: AvatarSelectorProps) {
  const { agentSettings, updateAgentSettings } = useUserStore()
  const [tempSettings, setTempSettings] = useState(agentSettings)

  const handleSave = () => {
    updateAgentSettings(tempSettings)
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-md max-h-[80vh] overflow-y-auto">
        <div className="p-6">
          <h2 className="text-xl font-bold mb-6">Customize Your Agent</h2>
          
          {/* Agent Name */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">Agent Name</label>
            <input
              type="text"
              value={tempSettings.name}
              onChange={(e) => setTempSettings({ ...tempSettings, name: e.target.value })}
              className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter agent name"
            />
          </div>

          {/* Avatar Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-3">Choose Avatar</label>
            <div className="grid grid-cols-4 gap-3">
              {avatars.map((avatar) => (
                <button
                  key={avatar}
                  onClick={() => setTempSettings({ ...tempSettings, avatar })}
                  className={`w-16 h-16 rounded-full border-2 transition-all overflow-hidden ${
                    tempSettings.avatar === avatar
                      ? 'border-primary-500 ring-2 ring-primary-500/30'
                      : 'border-dark-600 hover:border-dark-500'
                  }`}
                >
                  <img
                    src={`/assets/images/Avatars/${avatar}`}
                    alt={`Avatar ${avatar}`}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      // Fallback to default avatar if image fails to load
                      e.currentTarget.src = '/assets/images/CM Logo White.svg'
                    }}
                  />
                </button>
              ))}
            </div>
          </div>

          {/* Personality Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-3">Personality</label>
            <div className="space-y-2">
              {personalities.map((personality) => (
                <button
                  key={personality.id}
                  onClick={() => setTempSettings({ ...tempSettings, personality: personality.id as any })}
                  className={`w-full p-3 rounded-lg border text-left transition-all ${
                    tempSettings.personality === personality.id
                      ? 'border-primary-500 bg-primary-600/10'
                      : 'border-dark-600 hover:border-dark-500 bg-dark-800/50'
                  }`}
                >
                  <div className="font-medium">{personality.name}</div>
                  <div className="text-sm text-dark-400">{personality.description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3">
            <Button
              onClick={onClose}
              variant="secondary"
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              onClick={handleSave}
              className="flex-1"
            >
              Save Changes
            </Button>
          </div>
        </div>
      </Card>
    </div>
  )
}