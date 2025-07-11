import { useState } from 'react'
import { X } from 'lucide-react'
import Button from '@/components/common/Button'

interface QuickActionModalProps {
  isOpen: boolean
  onClose: () => void
  onSubmit: (context: string) => void
  action: {
    id: string
    title: string
    description: string
    icon: string
  }
  isLoading?: boolean
}

export default function QuickActionModal({ 
  isOpen, 
  onClose, 
  onSubmit, 
  action, 
  isLoading = false 
}: QuickActionModalProps) {
  const [context, setContext] = useState('')

  const handleSubmit = () => {
    onSubmit(context)
    setContext('')
    onClose()
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      handleSubmit()
    }
  }

  const getPlaceholderText = () => {
    switch (action.id) {
      case 'generate_script':
        return 'Describe your video topic, target audience, and key points you want to cover...'
      case 'improve_hooks':
        return 'Paste your current hook or describe your video topic for hook suggestions...'
      case 'optimize_title':
        return 'Enter your current title or describe your video content for title optimization...'
      case 'get_ideas':
        return 'What type of content ideas are you looking for? Specify your niche, audience, or goals...'
      default:
        return 'Provide additional context for this action...'
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
         onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="bg-dark-800 border border-white/20 rounded-lg shadow-xl w-full max-w-md">
        <div className="flex items-center justify-between p-4 border-b border-white/20">
          <div className="flex items-center gap-3">
            <span className="text-xl">{action.icon}</span>
            <div>
              <h3 className="font-medium text-white">{action.title}</h3>
              <p className="text-sm text-gray-400">{action.description}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-4">
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Additional Context (Optional)
          </label>
          <textarea
            value={context}
            onChange={(e) => setContext(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder={getPlaceholderText()}
            className="w-full h-24 px-3 py-2 bg-dark-700 border border-white/20 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
            autoFocus
          />
          <p className="text-xs text-gray-400 mt-1">
            Press Ctrl+Enter to submit, or leave empty for basic action
          </p>
        </div>

        <div className="flex justify-end gap-2 p-4 border-t border-white/20">
          <Button
            onClick={onClose}
            variant="secondary"
            size="sm"
            disabled={isLoading}
          >
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            variant="primary"
            size="sm"
            disabled={isLoading}
          >
            {isLoading ? 'Processing...' : 'Submit'}
          </Button>
        </div>
      </div>
    </div>
  )
}