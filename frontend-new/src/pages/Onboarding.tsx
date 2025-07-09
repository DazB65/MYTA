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
  subscriberCount: z.number().min(0, 'Must be 0 or greater'),
  avgViewCount: z.number().min(0, 'Must be 0 or greater'),
  ctr: z.number().min(0).max(100, 'Must be between 0 and 100'),
  retention: z.number().min(0).max(100, 'Must be between 0 and 100'),
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
  const { userId, updateChannelInfo, setOnboarded } = useUserStore()
  const [isSubmitting, setIsSubmitting] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<OnboardingForm>({
    resolver: zodResolver(onboardingSchema),
    defaultValues: {
      subscriberCount: 0,
      avgViewCount: 0,
      ctr: 0,
      retention: 0,
    },
  })

  const onSubmit = async (data: OnboardingForm) => {
    setIsSubmitting(true)
    try {
      const channelInfo = {
        name: data.channelName,
        niche: data.niche,
        content_type: data.contentType,
        subscriber_count: data.subscriberCount,
        avg_view_count: data.avgViewCount,
        ctr: data.ctr,
        retention: data.retention,
        upload_frequency: data.uploadFrequency,
        video_length: data.videoLength,
        monetization_status: data.monetizationStatus,
        primary_goal: data.primaryGoal,
        notes: data.notes || '',
        user_id: userId,
      }

      await api.agent.setChannelInfo(channelInfo)
      
      // Update local store
      updateChannelInfo(channelInfo)
      
      // Mark as onboarded
      localStorage.setItem('creatormate_onboarded', 'true')
      setOnboarded(true)
    } catch (error) {
      console.error('Onboarding failed:', error)
      alert('Failed to save channel information. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background-primary to-background-secondary flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <div className="w-20 h-20 bg-gradient-to-br from-primary-500 to-purple-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <img src="/assets/images/CM Logo White.svg" alt="CreatorMate" className="w-12 h-12" />
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

            {/* Subscriber Count */}
            <div>
              <label className="block text-sm font-medium mb-2">Subscriber Count</label>
              <input
                {...register('subscriberCount', { valueAsNumber: true })}
                type="number"
                min="0"
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="0"
              />
              {errors.subscriberCount && (
                <p className="text-red-400 text-sm mt-1">{errors.subscriberCount.message}</p>
              )}
            </div>

            {/* Average View Count */}
            <div>
              <label className="block text-sm font-medium mb-2">Average View Count</label>
              <input
                {...register('avgViewCount', { valueAsNumber: true })}
                type="number"
                min="0"
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="0"
              />
              {errors.avgViewCount && (
                <p className="text-red-400 text-sm mt-1">{errors.avgViewCount.message}</p>
              )}
            </div>

            {/* CTR */}
            <div>
              <label className="block text-sm font-medium mb-2">Click-Through Rate (%)</label>
              <input
                {...register('ctr', { valueAsNumber: true })}
                type="number"
                min="0"
                max="100"
                step="0.1"
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="0.0"
              />
              {errors.ctr && (
                <p className="text-red-400 text-sm mt-1">{errors.ctr.message}</p>
              )}
            </div>

            {/* Retention */}
            <div>
              <label className="block text-sm font-medium mb-2">Average Retention (%)</label>
              <input
                {...register('retention', { valueAsNumber: true })}
                type="number"
                min="0"
                max="100"
                step="0.1"
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="0.0"
              />
              {errors.retention && (
                <p className="text-red-400 text-sm mt-1">{errors.retention.message}</p>
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