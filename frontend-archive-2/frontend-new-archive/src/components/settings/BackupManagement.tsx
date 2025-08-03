import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'
import LoadingSpinner from '@/components/common/LoadingSpinner'
import { api } from '@/services/api'

// Types for backup management
interface BackupInfo {
  backup_id: string
  filename: string
  size_mb: number
  created_at: string
  database_version: string
  backup_type: string
  compression: boolean
  metadata: Record<string, any>
}

interface BackupStatus {
  running: boolean
  schedule: {
    frequency: string
    time: string
    enabled: boolean
    compression: boolean
    max_backups: number
    cleanup_enabled: boolean
  }
  alerts: {
    email_enabled: boolean
    webhook_enabled: boolean
    alert_on_failure: boolean
    alert_on_success: boolean
  }
  last_check: string
}

interface BackupHealth {
  timestamp: string
  overall_status: string
  checks: Record<string, any>
  failed_checks?: string[]
  error?: string
}

// Validation schemas
const scheduleSchema = z.object({
  frequency: z.enum(['hourly', 'daily', 'weekly', 'monthly']),
  time: z.string().min(1, 'Time is required'),
  enabled: z.boolean(),
  compression: z.boolean(),
  max_backups: z.number().min(1).max(50),
  cleanup_enabled: z.boolean()
})

const alertSchema = z.object({
  email_enabled: z.boolean(),
  email_recipients: z.string().optional(),
  webhook_url: z.string().url().optional().or(z.literal('')),
  alert_on_failure: z.boolean(),
  alert_on_success: z.boolean(),
  alert_on_cleanup: z.boolean()
})

type ScheduleForm = z.infer<typeof scheduleSchema>
type AlertForm = z.infer<typeof alertSchema>

export default function BackupManagement() {
  const [backups, setBackups] = useState<BackupInfo[]>([])
  const [status, setStatus] = useState<BackupStatus | null>(null)
  const [health, setHealth] = useState<BackupHealth | null>(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState<string | null>(null)
  const [activeSection, setActiveSection] = useState<'overview' | 'schedule' | 'alerts'>('overview')

  // Schedule form
  const {
    register: registerSchedule,
    handleSubmit: handleScheduleSubmit,
    formState: { errors: scheduleErrors },
    reset: resetSchedule
  } = useForm<ScheduleForm>({
    resolver: zodResolver(scheduleSchema)
  })

  // Alert form
  const {
    register: registerAlert,
    handleSubmit: handleAlertSubmit,
    formState: { errors: alertErrors },
    reset: resetAlert
  } = useForm<AlertForm>({
    resolver: zodResolver(alertSchema)
  })

  // Load backup data
  const loadData = async () => {
    try {
      setLoading(true)
      const [backupsData, statusData, healthData] = await Promise.all([
        api.get('/api/backup/list'),
        api.get('/api/backup/status'),
        api.get('/api/backup/health')
      ])

      setBackups(backupsData)
      setStatus(statusData)
      setHealth(healthData)

      // Update forms with current settings
      if (statusData) {
        resetSchedule({
          frequency: statusData.schedule.frequency,
          time: statusData.schedule.time,
          enabled: statusData.schedule.enabled,
          compression: statusData.schedule.compression,
          max_backups: statusData.schedule.max_backups,
          cleanup_enabled: statusData.schedule.cleanup_enabled
        })

        resetAlert({
          email_enabled: statusData.alerts.email_enabled,
          email_recipients: '',
          webhook_url: '',
          alert_on_failure: statusData.alerts.alert_on_failure,
          alert_on_success: statusData.alerts.alert_on_success,
          alert_on_cleanup: false
        })
      }
    } catch (error) {
      console.error('Error loading backup data:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  // Create manual backup
  const createBackup = async () => {
    try {
      setActionLoading('create')
      await api.post('/api/backup/create', {
        description: 'Manual backup from settings'
      })
      await loadData()
      alert('Backup creation initiated successfully!')
    } catch (error) {
      console.error('Error creating backup:', error)
      alert('Failed to create backup')
    } finally {
      setActionLoading(null)
    }
  }

  // Restore backup
  const restoreBackup = async (backupId: string) => {
    if (!confirm('Are you sure you want to restore this backup? This will replace your current data.')) {
      return
    }

    try {
      setActionLoading(`restore-${backupId}`)
      await api.post(`/api/backup/restore/${backupId}`)
      alert('Backup restored successfully!')
      await loadData()
    } catch (error) {
      console.error('Error restoring backup:', error)
      alert('Failed to restore backup')
    } finally {
      setActionLoading(null)
    }
  }

  // Delete backup
  const deleteBackup = async (backupId: string) => {
    if (!confirm('Are you sure you want to delete this backup? This action cannot be undone.')) {
      return
    }

    try {
      setActionLoading(`delete-${backupId}`)
      await api.delete(`/api/backup/delete/${backupId}`)
      await loadData()
      alert('Backup deleted successfully!')
    } catch (error) {
      console.error('Error deleting backup:', error)
      alert('Failed to delete backup')
    } finally {
      setActionLoading(null)
    }
  }

  // Update schedule
  const onScheduleSubmit = async (data: ScheduleForm) => {
    try {
      setActionLoading('schedule')
      await api.put('/api/backup/schedule', data)
      await loadData()
      alert('Backup schedule updated successfully!')
    } catch (error) {
      console.error('Error updating schedule:', error)
      alert('Failed to update backup schedule')
    } finally {
      setActionLoading(null)
    }
  }

  // Update alerts
  const onAlertSubmit = async (data: AlertForm) => {
    try {
      setActionLoading('alerts')
      const alertData = {
        ...data,
        email_recipients: data.email_recipients ? data.email_recipients.split(',').map(e => e.trim()) : []
      }
      await api.put('/api/backup/alerts', alertData)
      await loadData()
      alert('Backup alert settings updated successfully!')
    } catch (error) {
      console.error('Error updating alerts:', error)
      alert('Failed to update backup alerts')
    } finally {
      setActionLoading(null)
    }
  }

  // Cleanup old backups
  const cleanupBackups = async () => {
    if (!confirm('Are you sure you want to clean up old backups?')) {
      return
    }

    try {
      setActionLoading('cleanup')
      await api.post('/api/backup/cleanup')
      await loadData()
      alert('Backup cleanup completed!')
    } catch (error) {
      console.error('Error cleaning up backups:', error)
      alert('Failed to cleanup backups')
    } finally {
      setActionLoading(null)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString()
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-400'
      case 'degraded': return 'text-yellow-400'
      case 'unhealthy': return 'text-red-400'
      default: return 'text-gray-400'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <LoadingSpinner />
      </div>
    )
  }

  const sections = [
    { id: 'overview', name: 'Overview', icon: '📊' },
    { id: 'schedule', name: 'Schedule', icon: '⏰' },
    { id: 'alerts', name: 'Alerts', icon: '🔔' }
  ]

  return (
    <div className="space-y-6">
      {/* Section Navigation */}
      <Card>
        <div className="flex gap-1 p-1 bg-dark-800 rounded-lg">
          {sections.map((section) => (
            <button
              key={section.id}
              onClick={() => setActiveSection(section.id as any)}
              className={`flex-1 flex items-center justify-center gap-2 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                activeSection === section.id
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-300 hover:text-white hover:bg-dark-700'
              }`}
            >
              <span>{section.icon}</span>
              {section.name}
            </button>
          ))}
        </div>
      </Card>

      {/* Overview Section */}
      {activeSection === 'overview' && (
        <div className="space-y-6">
          {/* Status Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <div className="text-center">
                <div className={`text-2xl font-bold ${status?.running ? 'text-green-400' : 'text-red-400'}`}>
                  {status?.running ? 'Running' : 'Stopped'}
                </div>
                <div className="text-gray-400 text-sm">Backup Service</div>
              </div>
            </Card>

            <Card>
              <div className="text-center">
                <div className={`text-2xl font-bold ${health ? getStatusColor(health.overall_status) : 'text-gray-400'}`}>
                  {health?.overall_status || 'Unknown'}
                </div>
                <div className="text-gray-400 text-sm">System Health</div>
              </div>
            </Card>

            <Card>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-400">
                  {backups.length}
                </div>
                <div className="text-gray-400 text-sm">Total Backups</div>
              </div>
            </Card>
          </div>

          {/* Quick Actions */}
          <Card>
            <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
            <div className="flex flex-wrap gap-3">
              <Button
                onClick={createBackup}
                isLoading={actionLoading === 'create'}
                className="bg-green-600 hover:bg-green-700"
              >
                📦 Create Backup
              </Button>
              <Button
                onClick={cleanupBackups}
                isLoading={actionLoading === 'cleanup'}
                variant="secondary"
              >
                🧹 Cleanup Old Backups
              </Button>
              <Button
                onClick={loadData}
                variant="secondary"
              >
                🔄 Refresh
              </Button>
            </div>
          </Card>

          {/* Recent Backups */}
          <Card>
            <h3 className="text-lg font-semibold mb-4">Recent Backups</h3>
            {backups.length === 0 ? (
              <p className="text-gray-400 text-center py-4">No backups found</p>
            ) : (
              <div className="space-y-3">
                {backups.slice(0, 5).map((backup) => (
                  <div key={backup.backup_id} className="flex items-center justify-between p-3 bg-dark-800 rounded-lg">
                    <div className="flex-1">
                      <div className="font-medium">{backup.filename}</div>
                      <div className="text-sm text-gray-400">
                        {formatDate(backup.created_at)} • {backup.size_mb.toFixed(2)} MB • {backup.backup_type}
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        onClick={() => restoreBackup(backup.backup_id)}
                        isLoading={actionLoading === `restore-${backup.backup_id}`}
                        className="bg-blue-600 hover:bg-blue-700"
                      >
                        Restore
                      </Button>
                      <Button
                        size="sm"
                        variant="secondary"
                        onClick={() => deleteBackup(backup.backup_id)}
                        isLoading={actionLoading === `delete-${backup.backup_id}`}
                      >
                        Delete
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>
      )}

      {/* Schedule Section */}
      {activeSection === 'schedule' && (
        <Card>
          <h3 className="text-lg font-semibold mb-4">Backup Schedule</h3>
          <form onSubmit={handleScheduleSubmit(onScheduleSubmit)} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Frequency</label>
                <select
                  {...registerSchedule('frequency')}
                  className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="hourly">Hourly</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
                {scheduleErrors.frequency && (
                  <p className="text-red-400 text-sm mt-1">{scheduleErrors.frequency.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Time</label>
                <input
                  {...registerSchedule('time')}
                  type="time"
                  className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
                {scheduleErrors.time && (
                  <p className="text-red-400 text-sm mt-1">{scheduleErrors.time.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Max Backups to Keep</label>
                <input
                  {...registerSchedule('max_backups', { valueAsNumber: true })}
                  type="number"
                  min="1"
                  max="50"
                  className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
                {scheduleErrors.max_backups && (
                  <p className="text-red-400 text-sm mt-1">{scheduleErrors.max_backups.message}</p>
                )}
              </div>
            </div>

            <div className="space-y-3">
              <label className="flex items-center">
                <input
                  {...registerSchedule('enabled')}
                  type="checkbox"
                  className="mr-2"
                />
                Enable automatic backups
              </label>

              <label className="flex items-center">
                <input
                  {...registerSchedule('compression')}
                  type="checkbox"
                  className="mr-2"
                />
                Enable compression (reduces backup size)
              </label>

              <label className="flex items-center">
                <input
                  {...registerSchedule('cleanup_enabled')}
                  type="checkbox"
                  className="mr-2"
                />
                Automatically cleanup old backups
              </label>
            </div>

            <Button
              type="submit"
              isLoading={actionLoading === 'schedule'}
              className="w-full"
            >
              Save Schedule Settings
            </Button>
          </form>
        </Card>
      )}

      {/* Alerts Section */}
      {activeSection === 'alerts' && (
        <Card>
          <h3 className="text-lg font-semibold mb-4">Backup Alerts</h3>
          <form onSubmit={handleAlertSubmit(onAlertSubmit)} className="space-y-4">
            <div className="space-y-3">
              <label className="flex items-center">
                <input
                  {...registerAlert('email_enabled')}
                  type="checkbox"
                  className="mr-2"
                />
                Enable email alerts
              </label>

              <div>
                <label className="block text-sm font-medium mb-2">Email Recipients (comma-separated)</label>
                <input
                  {...registerAlert('email_recipients')}
                  type="text"
                  placeholder="admin@example.com, dev@example.com"
                  className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Webhook URL (optional)</label>
                <input
                  {...registerAlert('webhook_url')}
                  type="url"
                  placeholder="https://hooks.slack.com/services/..."
                  className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
                {alertErrors.webhook_url && (
                  <p className="text-red-400 text-sm mt-1">{alertErrors.webhook_url.message}</p>
                )}
              </div>

              <label className="flex items-center">
                <input
                  {...registerAlert('alert_on_failure')}
                  type="checkbox"
                  className="mr-2"
                />
                Alert on backup failures
              </label>

              <label className="flex items-center">
                <input
                  {...registerAlert('alert_on_success')}
                  type="checkbox"
                  className="mr-2"
                />
                Alert on backup success
              </label>

              <label className="flex items-center">
                <input
                  {...registerAlert('alert_on_cleanup')}
                  type="checkbox"
                  className="mr-2"
                />
                Alert on cleanup operations
              </label>
            </div>

            <Button
              type="submit"
              isLoading={actionLoading === 'alerts'}
              className="w-full"
            >
              Save Alert Settings
            </Button>
          </form>
        </Card>
      )}
    </div>
  )
}