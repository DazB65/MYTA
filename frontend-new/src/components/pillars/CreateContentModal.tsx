import { useState, useEffect } from 'react'
import { X, Send } from 'lucide-react'
import { cn } from '@/utils'
import { useAvatarStore } from '@/store/avatarStore'
import { useFloatingChatStore } from '@/store/floatingChatStore'
import { useChat } from '@/hooks/useChat'
import Button from '@/components/common/Button'

interface CreateContentModalProps {
  isOpen: boolean
  onClose: () => void
  pillar?: {
    id: string
    name: string
    icon: string
    color: string
  } | null
  editingPillar?: {
    id: string
    name: string
    icon: string
    color: string
  } | null
  onCreatePillar?: (pillarData: { name: string; icon: string; color: string }) => void
  onUpdatePillar?: (pillarData: { name: string; icon: string; color: string }) => void
}

interface FormData {
  pillarName: string
  title: string
  description: string
  contentType: string
  additionalInstructions: string
}

interface PillarFormData {
  name: string
  icon: string
  color: string
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

const pillarIcons = ['🎮', '⭐', '💡', '📰', '🎯', '🔥', '📈', '🎬', '🎵', '💰', '🏆', '🌟']
const pillarColors = [
  'from-blue-500 to-cyan-400',
  'from-purple-500 to-pink-400', 
  'from-orange-500 to-yellow-400',
  'from-red-500 to-pink-400',
  'from-green-500 to-blue-400',
  'from-indigo-500 to-purple-400',
  'from-cyan-500 to-blue-400',
  'from-pink-500 to-rose-400'
]

export default function CreateContentModal({ isOpen, onClose, pillar, editingPillar, onCreatePillar, onUpdatePillar }: CreateContentModalProps) {
  const { customization } = useAvatarStore()
  const { openChat } = useFloatingChatStore()
  const { sendMessage } = useChat()
  
  const [formData, setFormData] = useState<FormData>({
    pillarName: '',
    title: '',
    description: '',
    contentType: '',
    additionalInstructions: ''
  })
  
  const [pillarData, setPillarData] = useState<PillarFormData>({
    name: '',
    icon: pillarIcons[0],
    color: pillarColors[0]
  })
  
  // Determine if we're editing
  const isEditing = !!editingPillar

  // Update form data when editingPillar changes
  useEffect(() => {
    if (editingPillar) {
      setPillarData({
        name: editingPillar.name,
        icon: editingPillar.icon,
        color: editingPillar.color
      })
    } else {
      setPillarData({
        name: '',
        icon: pillarIcons[0],
        color: pillarColors[0]
      })
    }
  }, [editingPillar])
  
  const [errors, setErrors] = useState<Partial<FormData & PillarFormData>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isCreatingPillarOnly, setIsCreatingPillarOnly] = useState(!pillar || isEditing)

  // Update modal mode when props change
  useEffect(() => {
    setIsCreatingPillarOnly(!pillar || isEditing)
  }, [pillar, isEditing])

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }))
    }
  }

  const validateForm = (): boolean => {
    const newErrors: Partial<FormData & PillarFormData> = {}
    
    if (isCreatingPillarOnly) {
      if (!pillarData.name.trim()) {
        newErrors.name = 'Pillar name is required'
      }
    } else {
      if (!pillar && !formData.pillarName.trim()) {
        newErrors.pillarName = 'Pillar name is required'
      }
      
      if (!formData.title.trim()) {
        newErrors.title = 'Content title is required'
      }
      
      if (!formData.description.trim()) {
        newErrors.description = 'Content description is required'
      }
      
      if (!formData.contentType) {
        newErrors.contentType = 'Content type is required'
      }
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async () => {
    if (!validateForm()) return
    
    setIsSubmitting(true)
    
    try {
      if (isCreatingPillarOnly) {
        if (isEditing && onUpdatePillar) {
          // Update pillar
          onUpdatePillar({
            name: pillarData.name,
            icon: pillarData.icon,
            color: pillarData.color
          })
          
          // Close modal and reset form
          handleClose()
        } else if (onCreatePillar) {
          // Create pillar only, save locally
          onCreatePillar({
            name: pillarData.name,
            icon: pillarData.icon,
            color: pillarData.color
          })
          
          // Close modal and reset form
          handleClose()
        }
      } else {
        // Create content (existing functionality)
        const pillarName = pillar ? pillar.name : formData.pillarName
        const isNewPillar = !pillar
        
        const requestMessage = isNewPillar 
          ? `I want to create a new content pillar called "${pillarName}" and need help with the first piece of content.

**New Pillar Details:**
- Pillar Name: ${pillarName}
- First Content Title: ${formData.title}
- Content Type: ${formData.contentType}
- Description: ${formData.description}

${formData.additionalInstructions ? `**Additional Instructions:**\n${formData.additionalInstructions}` : ''}

Please help me:
1. Define this new content pillar strategy
2. Suggest how to develop this pillar over time
3. Provide detailed suggestions for this first piece of content including:
   - Hook ideas to grab attention
   - Key points to cover
   - Structure recommendations
   - SEO optimization tips
   - Engagement strategies

Focus on establishing a strong foundation for my new ${pillarName} pillar.`
          : `I need help creating content for my "${pillarName}" pillar.

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

Focus on making this content align with my ${pillarName} pillar strategy.`

        // Send message to chat
        await sendMessage(requestMessage)
        
        // Open the chat interface
        openChat()
        
        // Close modal and reset form
        handleClose()
      }
      
    } catch (error) {
      console.error('Error processing request:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleClose = () => {
    onClose()
    setFormData({
      pillarName: '',
      title: '',
      description: '',
      contentType: '',
      additionalInstructions: ''
    })
    setPillarData({
      name: '',
      icon: pillarIcons[0],
      color: pillarColors[0]
    })
    setErrors({})
    setIsCreatingPillarOnly(!pillar)
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-dark-800 rounded-xl border border-dark-600 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-dark-600">
          <div className="flex items-center gap-3">
            {pillar ? (
              <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${pillar.color} flex items-center justify-center text-lg`}>
                {pillar.icon}
              </div>
            ) : (
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary-500 to-purple-500 flex items-center justify-center text-lg">
                ✨
              </div>
            )}
            <div>
              <h2 className="text-xl font-semibold text-white">
                {isEditing ? 'Edit Pillar' : pillar ? 'Create Content' : 'Add New Pillar'}
              </h2>
              <p className="text-sm text-gray-300">
                {isEditing ? (
                  <>Update <span className="pillar-name-visible">{editingPillar?.name}</span> pillar</>
                ) : pillar ? (
                  <>For <span className="pillar-name-visible">{pillar.name}</span> pillar</>
                ) : (
                  'Create a new content pillar and first content'
                )}
              </p>
            </div>
          </div>
          <button
            onClick={handleClose}
            className="p-2 text-gray-400 hover:text-white rounded-lg hover:bg-dark-700 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <div className="p-6 space-y-6">
          {/* Mode Toggle (only show when no existing pillar and not editing) */}
          {!pillar && !isEditing && (
            <div className="flex gap-2 p-1 bg-dark-700 rounded-lg">
              <button
                type="button"
                onClick={() => setIsCreatingPillarOnly(true)}
                className={cn(
                  'flex-1 px-3 py-2 text-sm font-medium rounded-md transition-colors',
                  isCreatingPillarOnly
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-300 hover:text-white'
                )}
              >
                Create Pillar Only
              </button>
              <button
                type="button"
                onClick={() => setIsCreatingPillarOnly(false)}
                className={cn(
                  'flex-1 px-3 py-2 text-sm font-medium rounded-md transition-colors',
                  !isCreatingPillarOnly
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-300 hover:text-white'
                )}
              >
                Create Pillar + Content
              </button>
            </div>
          )}

          {/* Pillar Creation Form */}
          {isCreatingPillarOnly ? (
            <>
              {/* Pillar Name */}
              <div>
                <label className="block text-sm font-medium text-white mb-2">
                  Pillar Name *
                </label>
                <input
                  type="text"
                  value={pillarData.name}
                  onChange={(e) => {
                    setPillarData(prev => ({ ...prev, name: e.target.value }))
                    // Clear error when user starts typing
                    if (errors.name) {
                      setErrors(prev => ({ ...prev, name: undefined }))
                    }
                  }}
                  className={cn(
                    'w-full px-3 py-2 bg-dark-700 border rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500',
                    errors.name ? 'border-red-500' : 'border-dark-600'
                  )}
                  placeholder="Enter pillar name (e.g., Game Development, Reviews)..."
                />
                {errors.name && (
                  <p className="text-red-400 text-sm mt-1">{errors.name}</p>
                )}
              </div>

              {/* Icon Selection */}
              <div>
                <label className="block text-sm font-medium text-white mb-2">
                  Pillar Icon
                </label>
                <div className="grid grid-cols-6 gap-2">
                  {pillarIcons.map((icon, index) => (
                    <button
                      key={index}
                      type="button"
                      onClick={() => setPillarData(prev => ({ ...prev, icon }))}
                      className={cn(
                        'w-12 h-12 rounded-lg border-2 flex items-center justify-center text-xl transition-colors',
                        pillarData.icon === icon
                          ? 'border-primary-500 bg-primary-500/20'
                          : 'border-dark-600 hover:border-dark-500'
                      )}
                    >
                      {icon}
                    </button>
                  ))}
                </div>
              </div>

              {/* Color Selection */}
              <div>
                <label className="block text-sm font-medium text-white mb-2">
                  Pillar Color
                </label>
                <div className="grid grid-cols-4 gap-2">
                  {pillarColors.map((color, index) => (
                    <button
                      key={index}
                      type="button"
                      onClick={() => setPillarData(prev => ({ ...prev, color }))}
                      className={cn(
                        'h-12 rounded-lg border-2 transition-all',
                        `bg-gradient-to-br ${color}`,
                        pillarData.color === color
                          ? 'border-white scale-105'
                          : 'border-dark-600 hover:border-dark-500'
                      )}
                    />
                  ))}
                </div>
              </div>
            </>
          ) : (
            <>
              {/* Pillar Field */}
              {pillar ? (
                <div>
                  <label className="block text-sm font-medium text-white mb-2">
                    Content Pillar
                  </label>
                  <div className="flex items-center gap-3 p-3 bg-dark-700 border border-dark-600 rounded-lg">
                    <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${pillar.color} flex items-center justify-center text-sm`}>
                      {pillar.icon}
                    </div>
                    <span className="font-medium pillar-name-visible">{pillar.name}</span>
                    <span className="text-xs text-gray-400 ml-auto">Selected</span>
                  </div>
                </div>
              ) : (
                <div>
                  <label className="block text-sm font-medium text-white mb-2">
                    Pillar Name *
                  </label>
                  <input
                    type="text"
                    value={formData.pillarName}
                    onChange={(e) => handleInputChange('pillarName', e.target.value)}
                    className={cn(
                      'w-full px-3 py-2 bg-dark-700 border rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500',
                      errors.pillarName ? 'border-red-500' : 'border-dark-600'
                    )}
                    placeholder="Enter your new pillar name..."
                  />
                  {errors.pillarName && (
                    <p className="text-red-400 text-sm mt-1">{errors.pillarName}</p>
                  )}
                </div>
              )}

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
                'w-full px-3 py-2 bg-dark-700 border rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500',
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
                'w-full px-3 py-2 bg-dark-700 border rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none',
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
            </>
          )}

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
              {isCreatingPillarOnly ? (
                <>
                  ✨ {isSubmitting ? (isEditing ? 'Updating...' : 'Creating...') : (isEditing ? 'Update Pillar' : 'Create Pillar')}
                </>
              ) : (
                <>
                  <Send className="w-4 h-4 mr-2" />
                  {isSubmitting ? 'Sending...' : `Send to ${customization.name}`}
                </>
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}