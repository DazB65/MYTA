import { useEffect, useState } from 'react'
import { useUserStore } from '@/store/userStore'
import { api } from '@/services/api'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'
import { formatNumber } from '@/utils'

export default function Channel() {
  const { userId, channelInfo, updateChannelInfo } = useUserStore()
  const [connectionStatus, setConnectionStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')
  const [statusMessage, setStatusMessage] = useState('')

  const testConnection = async () => {
    setConnectionStatus('loading')
    try {
      const response = await api.agent.getStatus()
      setConnectionStatus('success')
      setStatusMessage(JSON.stringify(response, null, 2))
    } catch (error) {
      setConnectionStatus('error')
      setStatusMessage(error instanceof Error ? error.message : 'Connection failed')
    }
  }

  const refreshChannelData = async () => {
    try {
      const response = await api.agent.getContext(userId)
      if (response.channel_info) {
        updateChannelInfo(response.channel_info)
      }
    } catch (error) {
      console.error('Failed to refresh channel data:', error)
    }
  }

  useEffect(() => {
    refreshChannelData()
  }, [userId])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Channel Overview</h1>
        <p className="text-dark-400">
          Welcome to your CreatorMate channel hub. Monitor your channel performance and get AI-powered insights.
        </p>
      </div>

      {/* Connection Status Card */}
      <Card>
        <h3 className="text-xl font-semibold mb-4">Connection to Backend</h3>
        <p className="text-dark-300 mb-4">
          This dashboard connects to your Python backend at:{' '}
          <code className="bg-dark-800 px-2 py-1 rounded text-primary-400">
            http://localhost:8888/api/agent/status
          </code>
        </p>
        
        <Button 
          onClick={testConnection} 
          isLoading={connectionStatus === 'loading'}
          className="mb-4"
        >
          Test Connection
        </Button>

        {connectionStatus !== 'idle' && (
          <div className={`p-4 rounded-lg ${
            connectionStatus === 'success' ? 'bg-green-900/30 border border-green-500/30' :
            connectionStatus === 'error' ? 'bg-red-900/30 border border-red-500/30' :
            'bg-dark-800'
          }`}>
            <div className={`text-sm font-medium mb-2 ${
              connectionStatus === 'success' ? 'text-green-400' :
              connectionStatus === 'error' ? 'text-red-400' :
              'text-white'
            }`}>
              {connectionStatus === 'success' ? 'Connection successful!' :
               connectionStatus === 'error' ? 'Connection failed' :
               'Connecting...'}
            </div>
            {statusMessage && (
              <pre className="text-xs text-dark-300 bg-dark-900 p-3 rounded overflow-auto max-h-32">
                {statusMessage}
              </pre>
            )}
          </div>
        )}
      </Card>

      {/* Channel Info Card */}
      <Card>
        <h3 className="text-xl font-semibold mb-4">Channel Connected</h3>
        
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 rounded-full bg-gradient-to-br from-primary-500 to-purple-500 flex items-center justify-center p-2">
            <img 
              src="/assets/images/CM Logo White.svg" 
              alt="CreatorMate" 
              className="w-full h-full"
            />
          </div>
          <div>
            <h4 className="text-lg font-semibold">{channelInfo.name}</h4>
            <div className="text-dark-400 text-sm">
              {formatNumber(channelInfo.subscriber_count)} subscribers • {channelInfo.niche}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="text-center p-4 bg-primary-600/10 rounded-lg">
            <div className="text-2xl font-bold text-primary-400">
              {channelInfo.ctr ? `${channelInfo.ctr}%` : '-'}
            </div>
            <div className="text-sm text-dark-400">CTR</div>
          </div>
          <div className="text-center p-4 bg-green-600/10 rounded-lg">
            <div className="text-2xl font-bold text-green-400">
              {channelInfo.retention ? `${channelInfo.retention}%` : '-'}
            </div>
            <div className="text-sm text-dark-400">Retention</div>
          </div>
          <div className="text-center p-4 bg-yellow-600/10 rounded-lg">
            <div className="text-2xl font-bold text-yellow-400">
              {channelInfo.avg_view_count ? formatNumber(channelInfo.avg_view_count) : '-'}
            </div>
            <div className="text-sm text-dark-400">Avg Views</div>
          </div>
        </div>

        <Button 
          onClick={refreshChannelData}
          variant="secondary"
          size="sm"
        >
          🔄 Refresh Channel Data
        </Button>
      </Card>
    </div>
  )
}