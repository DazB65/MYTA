import { useState } from 'react'
import { X, Settings, RotateCcw, Check } from 'lucide-react'
import { cn } from '@/utils'
import { useAvatarStore, brandColors } from '@/store/avatarStore'
import Button from '@/components/common/Button'

const avatarOptions = [
  'MateBlue.svg',
  'MateDarkBlue.svg',
  'MateGreen.svg',
  'MateOrange.svg',
  'MatePink.svg',
  'MateRed.svg'
]

export default function AvatarCustomizationPanel() {
  const { 
    customization, 
    isCustomizing, 
    setName, 
    setAvatar, 
    setColor, 
    closeCustomization, 
    resetToDefaults 
  } = useAvatarStore()
  
  const [tempName, setTempName] = useState(customization.name)
  const [hasChanges, setHasChanges] = useState(false)

  const handleNameChange = (newName: string) => {
    setTempName(newName)
    setHasChanges(true)
  }

  const handleAvatarSelect = (avatar: string) => {
    setAvatar(avatar)
    setHasChanges(true)
  }

  const handleColorSelect = (color: string) => {
    setColor(color)
    setHasChanges(true)
  }

  const handleSave = () => {
    setName(tempName)
    setHasChanges(false)
    closeCustomization()
  }

  const handleReset = () => {
    resetToDefaults()
    setTempName('AI Assistant')
    setHasChanges(false)
  }

  if (!isCustomizing) return null

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-background-secondary rounded-xl border border-white/20 w-full max-w-md max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-white/10">
          <div className="flex items-center gap-3">
            <Settings className="w-5 h-5 text-primary-400" />
            <h2 className="text-lg font-semibold text-white">Customize Agent</h2>
          </div>
          <Button
            onClick={closeCustomization}
            variant="ghost"
            size="sm"
            className="p-2 hover:bg-white/10"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Name Input */}
          <div>
            <label className="block text-sm font-medium text-white mb-3">
              Agent Name
            </label>
            <input
              type="text"
              value={tempName}
              onChange={(e) => handleNameChange(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-dark-800/50 border border-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter agent name..."
              maxLength={20}
            />
          </div>

          {/* Avatar Selection */}
          <div>
            <label className="block text-sm font-medium text-white mb-3">
              Avatar
            </label>
            <div className="grid grid-cols-4 gap-3">
              {avatarOptions.map((avatar) => (
                <button
                  key={avatar}
                  onClick={() => handleAvatarSelect(avatar)}
                  className={cn(
                    'w-16 h-16 rounded-full border-2 transition-all hover:scale-105',
                    customization.avatar === avatar
                      ? 'border-primary-500 ring-2 ring-primary-500/50'
                      : 'border-white/20 hover:border-white/40'
                  )}
                >
                  <img
                    src={`/assets/images/Avatars/${avatar}`}
                    alt={`Avatar ${avatar}`}
                    className="w-full h-full rounded-full object-cover"
                    onError={(e) => {
                      e.currentTarget.src = '/assets/images/CM Logo White.svg'
                    }}
                  />
                </button>
              ))}
            </div>
          </div>

          {/* Color Selection */}
          <div>
            <label className="block text-sm font-medium text-white mb-3">
              Theme Color
            </label>
            <div className="grid grid-cols-4 gap-3">
              {brandColors.map((color) => (
                <button
                  key={color.value}
                  onClick={() => handleColorSelect(color.value)}
                  className={cn(
                    'w-12 h-12 rounded-lg border-2 transition-all hover:scale-105 relative',
                    customization.color === color.value
                      ? 'border-white ring-2 ring-white/50'
                      : 'border-white/20 hover:border-white/40'
                  )}
                  style={{ backgroundColor: color.value }}
                  title={color.name}
                >
                  {customization.color === color.value && (
                    <Check className="w-4 h-4 text-white absolute inset-0 m-auto" />
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Preview */}
          <div className="bg-dark-800/30 rounded-lg p-4">
            <label className="block text-sm font-medium text-white mb-3">
              Preview
            </label>
            <div className="flex items-center gap-4">
              <div 
                className="w-16 h-16 rounded-full flex items-center justify-center"
                style={{ backgroundColor: customization.color }}
              >
                <img
                  src={`/assets/images/Avatars/${customization.avatar}`}
                  alt="Preview"
                  className="w-14 h-14 rounded-full object-cover"
                  onError={(e) => {
                    e.currentTarget.src = '/assets/images/CM Logo White.svg'
                  }}
                />
              </div>
              <div>
                <p className="font-semibold text-white">{tempName}</p>
                <p className="text-sm text-dark-400">Your YouTube Personal Agent</p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-6 border-t border-white/10">
          <Button
            onClick={handleReset}
            variant="ghost"
            size="sm"
            className="flex items-center gap-2 hover:bg-white/10"
          >
            <RotateCcw className="w-4 h-4" />
            Reset
          </Button>
          
          <div className="flex items-center gap-3">
            <Button
              onClick={closeCustomization}
              variant="ghost"
              size="sm"
              className="hover:bg-white/10"
            >
              Cancel
            </Button>
            <Button
              onClick={handleSave}
              variant="primary"
              size="sm"
              disabled={!hasChanges}
              className="flex items-center gap-2"
            >
              <Check className="w-4 h-4" />
              Save Changes
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}