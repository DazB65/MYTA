import { useState, useEffect } from 'react'
import { X, Calendar } from 'lucide-react'
import { ContentCard, CardStatus, Pillar } from '@/types/contentStudio'
import { CardFormData } from '@/lib/validationSchemas'
import { cn } from '@/utils'
import Button from '@/components/common/Button'

interface CardModalProps {
  isOpen: boolean
  onClose: () => void
  card?: ContentCard | null
  onSubmit: (data: CardFormData) => Promise<boolean>
  defaultStatus?: CardStatus
}


const statusOptions = [
  { value: 'ideas' as CardStatus, label: 'Ideas', color: 'bg-purple-500' },
  { value: 'planning' as CardStatus, label: 'Planning', color: 'bg-yellow-500' },
  { value: 'inProgress' as CardStatus, label: 'In Progress', color: 'bg-blue-500' },
  { value: 'ready' as CardStatus, label: 'Ready to Publish', color: 'bg-green-500' }
]

export default function CardModal({ 
  isOpen, 
  onClose, 
  card, 
  onSubmit, 
  defaultStatus = 'ideas' 
}: CardModalProps) {
  // TEMPORARY FIX: Use default_user to match Pillars page
  const actualUserId = "default_user"
  const [formData, setFormData] = useState<CardFormData>({
    title: '',
    description: '',
    pillars: [],
    status: defaultStatus,
    dueDate: ''
  })
  
  const [availablePillars, setAvailablePillars] = useState<Pillar[]>([])
  const [errors, setErrors] = useState<Partial<CardFormData>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [loadingPillars, setLoadingPillars] = useState(false)

  // Update form data when card changes
  useEffect(() => {
    if (card) {
      setFormData({
        title: card.title,
        description: card.description,
        pillars: card.pillars || [],
        status: card.status,
        dueDate: card.dueDate || card.due_date || ''
      })
    } else {
      setFormData({
        title: '',
        description: '',
        pillars: [],
        status: defaultStatus,
        dueDate: ''
      })
    }
    setErrors({})
  }, [card, defaultStatus])

  // Fetch available pillars when modal opens
  useEffect(() => {
    if (isOpen && actualUserId) {
      fetchPillars()
    }
  }, [isOpen, actualUserId])

  const fetchPillars = async () => {
    if (!actualUserId) return
    
    setLoadingPillars(true)
    try {
      const response = await fetch(`/api/pillars/${actualUserId}`)
      if (response.ok) {
        const pillars = await response.json()
        // The /api/pillars/{user_id} endpoint returns an array directly
        // Convert to match our Pillar interface
        const formattedPillars = pillars.map((pillar: any) => ({
          id: pillar.id,
          name: pillar.name,
          icon: pillar.icon,
          color: pillar.color
        }))
        setAvailablePillars(formattedPillars)
      } else {
        console.error('Failed to fetch pillars')
        setAvailablePillars([])
      }
    } catch (error) {
      console.error('Error fetching pillars:', error)
      setAvailablePillars([])
    } finally {
      setLoadingPillars(false)
    }
  }

  const handleInputChange = (field: keyof CardFormData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }))
    }
  }

  const validateForm = (): boolean => {
    const newErrors: Partial<CardFormData> = {}
    
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required'
    }
    
    if (!formData.description.trim()) {
      newErrors.description = 'Description is required'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async () => {
    if (!validateForm()) return
    
    setIsSubmitting(true)
    
    try {
      // Save card to Content Studio
      const success = await onSubmit(formData)
      if (success) {
        handleClose()
      }
    } catch (error) {
      console.error('Error saving card:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleClose = () => {
    onClose()
    setFormData({
      title: '',
      description: '',
      pillars: [],
      status: defaultStatus,
      dueDate: ''
    })
    setErrors({})
    setAvailablePillars([])
  }

  const togglePillar = (pillar: Pillar) => {
    const isSelected = formData.pillars.some(p => p.id === pillar.id)
    if (isSelected) {
      handleInputChange('pillars', formData.pillars.filter(p => p.id !== pillar.id))
    } else {
      handleInputChange('pillars', [...formData.pillars, pillar])
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl border border-gray-200 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-lg text-white">
              ✨
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                {card ? 'Edit Content Card' : 'New Content Card'}
              </h2>
              <p className="text-sm text-gray-500">
                {card ? 'Update your content details' : 'Create and plan your next content'}
              </p>
            </div>
          </div>
          <button
            onClick={handleClose}
            className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <div className="p-6 space-y-6">

          {/* Content Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Content Title *
            </label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => handleInputChange('title', e.target.value)}
              className={cn(
                'w-full px-3 py-2 bg-white border rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500',
                errors.title ? 'border-red-500' : 'border-gray-300'
              )}
              placeholder="Enter your content title..."
            />
            {errors.title && (
              <p className="text-red-500 text-sm mt-1">{errors.title}</p>
            )}
          </div>


          {/* Content Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Content Description *
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              rows={4}
              className={cn(
                'w-full px-3 py-2 bg-white border rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none',
                errors.description ? 'border-red-500' : 'border-gray-300'
              )}
              placeholder="Describe your content idea, target audience, key points to cover..."
            />
            {errors.description && (
              <p className="text-red-500 text-sm mt-1">{errors.description}</p>
            )}
          </div>

          {/* Pillars Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Content Pillars
            </label>
            {loadingPillars ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
                <span className="ml-2 text-gray-500">Loading pillars...</span>
              </div>
            ) : availablePillars.length > 0 ? (
              <div className="grid grid-cols-2 gap-2">
                {availablePillars.map((pillar) => {
                  const isSelected = formData.pillars.some(p => p.id === pillar.id)
                  return (
                    <button
                      key={pillar.id}
                      type="button"
                      onClick={() => togglePillar(pillar)}
                      className={cn(
                        'flex items-center gap-2 p-3 rounded-lg border-2 transition-all text-left',
                        isSelected
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                      )}
                    >
                      <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${pillar.color} flex items-center justify-center text-sm`}>
                        {pillar.icon}
                      </div>
                      <span className="font-medium text-gray-900">{pillar.name}</span>
                    </button>
                  )
                })}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <p>No content pillars found.</p>
                <p className="text-sm mt-1">Create pillars in the Pillars page first.</p>
              </div>
            )}
          </div>

          {/* Status and Due Date Row */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                value={formData.status}
                onChange={(e) => handleInputChange('status', e.target.value as CardStatus)}
                className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {statusOptions.map((status) => (
                  <option key={status.value} value={status.value}>
                    {status.label}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Due Date
              </label>
              <div className="relative">
                <input
                  type="date"
                  value={formData.dueDate}
                  onChange={(e) => handleInputChange('dueDate', e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <Calendar className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
              </div>
            </div>
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
              className="flex-1"
            >
              {isSubmitting ? 'Saving...' : (card ? 'Update Card' : 'Create Card')}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}