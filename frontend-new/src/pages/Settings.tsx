import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useUserStore } from '@/store/userStore'
import { api } from '@/services/api'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'
import OAuthConnection from '@/components/oauth/OAuthConnection'
import PricingPage from './PricingPage'

const settingsSchema = z.object({
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

type SettingsForm = z.infer<typeof settingsSchema>

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

export default function Settings() {
  const { userId, channelInfo, updateChannelInfo } = useUserStore()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [activeTab, setActiveTab] = useState<'channel' | 'oauth' | 'agent' | 'preferences' | 'pricing'>('channel')

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<SettingsForm>({
    resolver: zodResolver(settingsSchema),
    defaultValues: {
      channelName: channelInfo.name,
      niche: channelInfo.niche,
      contentType: channelInfo.content_type,
      subscriberCount: channelInfo.subscriber_count,
      avgViewCount: channelInfo.avg_view_count,
      ctr: channelInfo.ctr,
      retention: channelInfo.retention,
      uploadFrequency: channelInfo.upload_frequency,
      videoLength: channelInfo.video_length,
      monetizationStatus: channelInfo.monetization_status,
      primaryGoal: channelInfo.primary_goal,
      notes: channelInfo.notes,
    },
  })

  const onSubmit = async (data: SettingsForm) => {
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
      updateChannelInfo(channelInfo)
      
      alert('Settings saved successfully!')
    } catch (error) {
      console.error('Failed to save settings:', error)
      alert('Failed to save settings. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const resetToDefaults = () => {
    if (confirm('Are you sure you want to reset all settings to defaults?')) {
      reset()
    }
  }

  const tabs = [
    { id: 'channel', name: 'Channel Settings', icon: '📺' },
    { id: 'oauth', name: 'YouTube Connection', icon: '🔑' },
    { id: 'agent', name: 'AI Agent', icon: '🤖' },
    { id: 'preferences', name: 'Preferences', icon: '⚙️' },
    { id: 'pricing', name: 'Pricing', icon: '💰' }
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Settings</h1>
        <p className="text-dark-400">
          Manage your channel information, AI agent, and application preferences.
        </p>
      </div>

      {/* Tab Navigation */}
      <Card>
        <div className="flex gap-1 p-1 bg-dark-800 rounded-lg">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex-1 flex items-center justify-center gap-2 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? 'bg-primary-600 text-white'
                  : 'text-dark-400 hover:text-white hover:bg-dark-700'
              }`}
            >
              <span>{tab.icon}</span>
              {tab.name}
            </button>
          ))}
        </div>
      </Card>

      {/* Channel Settings Tab */}
      {activeTab === 'channel' && (
        <Card>
          <h3 className="text-xl font-semibold mb-6">Channel Information</h3>
          
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

            <div className="flex gap-3">
              <Button
                type="submit"
                isLoading={isSubmitting}
                className="flex-1"
              >
                Save Changes
              </Button>
              <Button
                type="button"
                onClick={resetToDefaults}
                variant="secondary"
              >
                Reset to Defaults
              </Button>
            </div>
          </form>
        </Card>
      )}

      {/* OAuth Tab */}
      {activeTab === 'oauth' && (
        <div className="space-y-6">
          <OAuthConnection variant="full" showBenefits={true} />
        </div>
      )}

      {/* AI Agent Tab */}
      {activeTab === 'agent' && (
        <Card>
          <h3 className="text-xl font-semibold mb-6">AI Agent Configuration</h3>
          <div className="text-center py-8">
            <div className="text-6xl mb-4">🤖</div>
            <h4 className="text-lg font-semibold mb-2">Agent settings will be here</h4>
            <p className="text-dark-400">
              Configure your AI agent's personality, response style, and behavior preferences.
            </p>
          </div>
        </Card>
      )}

      {/* Preferences Tab */}
      {activeTab === 'preferences' && (
        <Card>
          <h3 className="text-xl font-semibold mb-6">Application Preferences</h3>
          <div className="text-center py-8">
            <div className="text-6xl mb-4">⚙️</div>
            <h4 className="text-lg font-semibold mb-2">Preferences will be here</h4>
            <p className="text-dark-400">
              Customize notifications, themes, and other application settings.
            </p>
          </div>
        </Card>
      )}

      {/* Pricing Tab */}
      {activeTab === 'pricing' && (
        <div className="bg-white rounded-lg overflow-hidden">
          <PricingPage />
        </div>
      )}
    </div>
  )
}