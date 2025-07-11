import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useUserStore } from '@/store/userStore'
import { api } from '@/services/api'
import Button from '@/components/common/Button'
import Card from '@/components/common/Card'

const onboardingSchema = z.object({
  channelName: z.string().min(1, 'Channel name is required'),
  niche: z.string().min(1, 'Please select a niche'),
  contentType: z.string().min(1, 'Please select content type'),
  uploadFrequency: z.string().min(1, 'Please select upload frequency'),
  videoLength: z.string().min(1, 'Please select video length'),
  monetizationStatus: z.string().min(1, 'Please select monetization status'),
  primaryGoal: z.string().min(1, 'Please select your primary goal'),
  notes: z.string().optional(),
})

type OnboardingForm = z.infer<typeof onboardingSchema>

const niches = [
  'Tech', 'Gaming', 'Lifestyle', 'Education', 'Entertainment', 
  'Music', 'Fitness', 'Cooking', 'Travel', 'Business', 'Finance', 'Beauty'
]

const contentTypes = [
  'Tutorial', 'Vlog', 'Review', 'Gameplay', 'Reaction', 
  'Commentary', 'Educational', 'Entertainment'
]

const uploadFrequencies = [
  'Daily', '3x per week', '2x per week', 'Weekly', 
  'Bi-weekly', 'Monthly', 'Irregular'
]

const videoLengths = [
  'Under 3 minutes', '3-8 minutes', '8-15 minutes', 
  '15-30 minutes', '30+ minutes'
]

const monetizationStatuses = [
  'Not monetized', 'Recently monetized', 'Fully monetized', 
  'Multiple revenue streams'
]

const primaryGoals = [
  'Grow subscribers', 'Increase views', 'Improve engagement',
  'Generate revenue', 'Build brand', 'Educational impact'
]

export default function Onboarding() {
  const { userId, updateChannelInfo, setOnboarded, setUserId, generateUserId } = useUserStore()
  const [isSubmitting, setIsSubmitting] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<OnboardingForm>({
    resolver: zodResolver(onboardingSchema),
  })

  const onSubmit = async (data: OnboardingForm) => {
    setIsSubmitting(true)
    try {
      // Ensure userId is set - this is the most likely fix for the issue
      let currentUserId = userId
      if (!currentUserId || currentUserId.trim() === '') {
        console.log('No userId found, generating new one...')
        currentUserId = generateUserId()
        setUserId(currentUserId)
      }
      
      console.log('Submitting onboarding with userId:', currentUserId)
      console.log('Form data:', data)
      
      const channelInfo = {
        name: data.channelName,
        niche: data.niche,
        content_type: data.contentType,
        subscriber_count: 0,  // Will be populated from YouTube connection
        avg_view_count: 0,    // Will be populated from YouTube connection
        ctr: 0,              // Will be populated from YouTube connection
        retention: 0,        // Will be populated from YouTube connection
        upload_frequency: data.uploadFrequency,
        video_length: data.videoLength,
        monetization_status: data.monetizationStatus,
        primary_goal: data.primaryGoal,
        notes: data.notes || '',
        user_id: currentUserId,
      }

      console.log('Channel info payload:', channelInfo)
      
      const response = await api.agent.setChannelInfo(channelInfo)
      console.log('API response:', response)
      
      // Update local store
      updateChannelInfo(channelInfo)
      
      // Mark as onboarded
      localStorage.setItem('creatormate_onboarded', 'true')
      setOnboarded(true)
    } catch (error) {
      console.error('Onboarding failed:', error)
      console.error('Error details:', error)
      
      // More specific error message
      let errorMessage = 'Failed to save channel information. Please try again.'
      if (error instanceof Error) {
        errorMessage = `Failed to save channel information: ${error.message}`
      }
      
      alert(errorMessage)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background-primary to-background-secondary flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <div className="w-40 h-40 flex items-center justify-center mx-auto mb-6">
            <img src="/assets/images/CM Text White.svg" alt="CreatorMate" className="w-full h-full object-contain" />
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-primary-400 to-purple-400 bg-clip-text text-transparent">
            Welcome to CreatorMate
          </h1>
          <p className="text-dark-400 mt-2">
            Let's set up your channel profile to get personalized AI assistance
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Channel Name */}
            <div>
              <label className="block text-sm font-medium mb-2">Channel Name *</label>
              <input
                {...register('channelName')}
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="Your channel name"
              />
              {errors.channelName && (
                <p className="text-red-400 text-sm mt-1">{errors.channelName.message}</p>
              )}
            </div>

            {/* Niche */}
            <div>
              <label className="block text-sm font-medium mb-2">Niche *</label>
              <select
                {...register('niche')}
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Select niche</option>
                {niches.map((niche) => (
                  <option key={niche} value={niche.toLowerCase()}>{niche}</option>
                ))}
              </select>
              {errors.niche && (
                <p className="text-red-400 text-sm mt-1">{errors.niche.message}</p>
              )}
            </div>

            {/* Content Type */}
            <div>
              <label className="block text-sm font-medium mb-2">Content Type *</label>
              <select
                {...register('contentType')}
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Select content type</option>
                {contentTypes.map((type) => (
                  <option key={type} value={type.toLowerCase()}>{type}</option>
                ))}
              </select>
              {errors.contentType && (
                <p className="text-red-400 text-sm mt-1">{errors.contentType.message}</p>
              )}
            </div>


            {/* Upload Frequency */}
            <div>
              <label className="block text-sm font-medium mb-2">Upload Frequency *</label>
              <select
                {...register('uploadFrequency')}
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Select frequency</option>
                {uploadFrequencies.map((freq) => (
                  <option key={freq} value={freq.toLowerCase()}>{freq}</option>
                ))}
              </select>
              {errors.uploadFrequency && (
                <p className="text-red-400 text-sm mt-1">{errors.uploadFrequency.message}</p>
              )}
            </div>

            {/* Video Length */}
            <div>
              <label className="block text-sm font-medium mb-2">Typical Video Length *</label>
              <select
                {...register('videoLength')}
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Select length</option>
                {videoLengths.map((length) => (
                  <option key={length} value={length.toLowerCase()}>{length}</option>
                ))}
              </select>
              {errors.videoLength && (
                <p className="text-red-400 text-sm mt-1">{errors.videoLength.message}</p>
              )}
            </div>

            {/* Monetization Status */}
            <div>
              <label className="block text-sm font-medium mb-2">Monetization Status *</label>
              <select
                {...register('monetizationStatus')}
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Select status</option>
                {monetizationStatuses.map((status) => (
                  <option key={status} value={status.toLowerCase()}>{status}</option>
                ))}
              </select>
              {errors.monetizationStatus && (
                <p className="text-red-400 text-sm mt-1">{errors.monetizationStatus.message}</p>
              )}
            </div>

            {/* Primary Goal */}
            <div>
              <label className="block text-sm font-medium mb-2">Primary Goal *</label>
              <select
                {...register('primaryGoal')}
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Select goal</option>
                {primaryGoals.map((goal) => (
                  <option key={goal} value={goal.toLowerCase()}>{goal}</option>
                ))}
              </select>
              {errors.primaryGoal && (
                <p className="text-red-400 text-sm mt-1">{errors.primaryGoal.message}</p>
              )}
            </div>
          </div>

          {/* Notes */}
          <div>
            <label className="block text-sm font-medium mb-2">Additional Notes</label>
            <textarea
              {...register('notes')}
              rows={3}
              className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Any additional information about your channel..."
            />
          </div>

          {/* YouTube Connection */}
          <div className="bg-dark-800 border border-dark-600 rounded-lg p-6 mb-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold mb-1">Connect Your YouTube Channel</h3>
                <p className="text-sm text-dark-400">
                  Connect your YouTube account to automatically import your channel statistics
                </p>
              </div>
              <div className="text-red-500">
                <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
              </div>
            </div>
            <Button
              type="button"
              variant="secondary"
              size="lg"
              className="w-full border border-red-500 text-red-500 hover:bg-red-500 hover:text-white bg-transparent"
              onClick={() => {
                // TODO: Implement YouTube OAuth flow
                window.location.href = '/api/oauth/youtube/authorize'
              }}
            >
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
              </svg>
              Connect YouTube Account
            </Button>
            <p className="text-xs text-dark-500 text-center mt-3">
              Optional: You can connect later from Settings
            </p>
          </div>

          <Button
            type="submit"
            isLoading={isSubmitting}
            className="w-full"
            size="lg"
          >
            Complete Setup
          </Button>
        </form>
      </Card>
    </div>
  )
}