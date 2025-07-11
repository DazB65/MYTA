import { useState } from 'react'
import { X, Send } from 'lucide-react'
import { cn } from '@/utils'
import { useAvatarStore } from '@/store/avatarStore'
import { useFloatingChatStore } from '@/store/floatingChatStore'
import { useChat } from '@/hooks/useChat'
import Button from '@/components/common/Button'

interface CreateContentModalProps {
  isOpen: boolean
  onClose: () => void
  pillar: {
    id: string
    name: string
    icon: string
    color: string
  }
}

interface FormData {
  title: string
  description: string
  contentType: string
  additionalInstructions: string
}

const contentTypes = [
  'YouTube Video',
  'Short-form Video',
  'Blog Post',
  'Social Media Post',
  'Tutorial',
  'Review',
  'Analysis',
  'News Coverage',
  'How-to Guide',
  'Interview',
  'Case Study',
  'Comparison'
]

export default function CreateContentModal({ isOpen, onClose, pillar }: CreateContentModalProps) {
  const { customization } = useAvatarStore()
  const { openChat } = useFloatingChatStore()
  const { sendMessage } = useChat()
  
  const [formData, setFormData] = useState<FormData>({
    title: '',
    description: '',
    contentType: '',
    additionalInstructions: ''
  })
  
  const [errors, setErrors] = useState<Partial<FormData>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }))
    }
  }

  const validateForm = (): boolean => {
    const newErrors: Partial<FormData> = {}
    
    if (!formData.title.trim()) {
      newErrors.title = 'Content title is required'
    }
    
    if (!formData.description.trim()) {
      newErrors.description = 'Content description is required'
    }
    
    if (!formData.contentType) {
      newErrors.contentType = 'Content type is required'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async () => {
    if (!validateForm()) return
    
    setIsSubmitting(true)
    
    try {
      // Create the content request message
      const requestMessage = `I need help creating content for my "${pillar.name}" pillar.

**Content Details:**
- Title: ${formData.title}
- Type: ${formData.contentType}
- Description: ${formData.description}

${formData.additionalInstructions ? `**Additional Instructions:**\n${formData.additionalInstructions}` : ''}

Please provide detailed suggestions for this content including:
- Hook ideas to grab attention
- Key points to cover
- Structure recommendations
- SEO optimization tips
- Engagement strategies

Focus on making this content align with my ${pillar.name} pillar strategy.`

      // Send message to chat
      await sendMessage(requestMessage)
      
      // Open the chat interface
      openChat()
      
      // Close modal and reset form
      onClose()
      setFormData({
        title: '',
        description: '',
        contentType: '',
        additionalInstructions: ''
      })
      setErrors({})
      
    } catch (error) {
      console.error('Error sending content request:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleClose = () => {
    onClose()
    setFormData({
      title: '',
      description: '',
      contentType: '',
      additionalInstructions: ''
    })
    setErrors({})
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-dark-800 rounded-xl border border-dark-600 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-dark-600">
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${pillar.color} flex items-center justify-center text-lg`}>
              {pillar.icon}
            </div>
            <div>
              <h2 className="text-xl font-semibold text-white">Create Content</h2>
              <p className="text-sm text-dark-400">For {pillar.name} pillar</p>
            </div>
          </div>
          <button
            onClick={handleClose}
            className="p-2 text-dark-400 hover:text-white rounded-lg hover:bg-dark-700 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <div className="p-6 space-y-6">
          {/* Pillar Field (Read-only) */}
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Content Pillar
            </label>
            <div className="flex items-center gap-3 p-3 bg-dark-700 border border-dark-600 rounded-lg">
              <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${pillar.color} flex items-center justify-center text-sm`}>
                {pillar.icon}
              </div>
              <span className="text-white font-medium">{pillar.name}</span>
              <span className="text-xs text-dark-400 ml-auto">Selected</span>
            </div>
          </div>

          {/* Content Title */}
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Content Title *
            </label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => handleInputChange('title', e.target.value)}
              className={cn(
                'w-full px-3 py-2 bg-dark-700 border rounded-lg text-white placeholder-dark-400 focus:outline-none focus:ring-2 focus:ring-primary-500',
                errors.title ? 'border-red-500' : 'border-dark-600'
              )}
              placeholder="Enter your content title..."
            />
            {errors.title && (
              <p className="text-red-400 text-sm mt-1">{errors.title}</p>
            )}
          </div>

          {/* Content Type */}
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Content Type *
            </label>
            <select
              value={formData.contentType}
              onChange={(e) => handleInputChange('contentType', e.target.value)}
              className={cn(
                'w-full px-3 py-2 bg-dark-700 border rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500',
                errors.contentType ? 'border-red-500' : 'border-dark-600'
              )}
            >
              <option value="">Select content type...</option>
              {contentTypes.map((type) => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
            {errors.contentType && (
              <p className="text-red-400 text-sm mt-1">{errors.contentType}</p>
            )}
          </div>

          {/* Content Description */}
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Content Description *
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              rows={4}
              className={cn(
                'w-full px-3 py-2 bg-dark-700 border rounded-lg text-white placeholder-dark-400 focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none',
                errors.description ? 'border-red-500' : 'border-dark-600'
              )}
              placeholder="Describe what you want to create, your target audience, key points to cover, etc."
            />
            {errors.description && (
              <p className="text-red-400 text-sm mt-1">{errors.description}</p>
            )}
          </div>

          {/* Additional Instructions */}
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Additional Instructions
            </label>
            <textarea
              value={formData.additionalInstructions}
              onChange={(e) => handleInputChange('additionalInstructions', e.target.value)}
              rows={3}
              className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg text-white placeholder-dark-400 focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none"
              placeholder="Any specific requirements, style preferences, or additional context..."
            />
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4">
            <Button
              onClick={handleClose}
              variant="secondary"
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              onClick={handleSubmit}
              disabled={isSubmitting}
              className="flex-1 bg-gradient-to-r from-primary-600 to-purple-600 hover:from-primary-700 hover:to-purple-700"
            >
              <Send className="w-4 h-4 mr-2" />
              {isSubmitting ? 'Sending...' : `Send to ${customization.name}`}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}