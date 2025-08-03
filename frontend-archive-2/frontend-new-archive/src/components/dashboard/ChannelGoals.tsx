import { useState } from 'react'
import { useGoalsStore } from '@/store/goalsStore'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'
import { 
  Target, 
  Plus, 
  Edit2, 
  Trash2, 
  Calendar, 
  TrendingUp, 
  Users, 
  Eye, 
  DollarSign,
  Check
} from 'lucide-react'

export default function ChannelGoals() {
  const { goals, addGoal, deleteGoal, updateProgress } = useGoalsStore()
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingGoal, setEditingGoal] = useState<string | null>(null)
  const [newGoal, setNewGoal] = useState({
    title: '',
    description: '',
    type: 'subscribers' as 'subscribers' | 'views' | 'engagement' | 'revenue' | 'custom',
    targetValue: 0,
    currentValue: 0,
    targetDate: '',
    priority: 'medium' as 'high' | 'medium' | 'low',
    category: 'growth'
  })

  const goalTypeIcons = {
    subscribers: Users,
    views: Eye,
    engagement: TrendingUp,
    revenue: DollarSign,
    custom: Target
  }

  const handleAddGoal = () => {
    if (newGoal.title && newGoal.targetValue > 0) {
      addGoal({
        ...newGoal,
        isCompleted: false
      })
      setNewGoal({
        title: '',
        description: '',
        type: 'subscribers',
        targetValue: 0,
        currentValue: 0,
        targetDate: '',
        priority: 'medium',
        category: 'growth'
      })
      setShowAddForm(false)
    }
  }

  const handleUpdateProgress = (goalId: string, value: number) => {
    updateProgress(goalId, value)
  }

  const getProgressPercentage = (current: number, target: number) => {
    return Math.min((current / target) * 100, 100)
  }

  const formatValue = (value: number, type: string) => {
    switch (type) {
      case 'subscribers':
      case 'views':
        return value >= 1000000 ? `${(value / 1000000).toFixed(1)}M` :
               value >= 1000 ? `${(value / 1000).toFixed(1)}K` :
               value.toString()
      case 'revenue':
        return `$${value.toLocaleString()}`
      case 'engagement':
        return `${value}%`
      default:
        return value.toString()
    }
  }

  const activeGoals = goals.filter(goal => !goal.isCompleted)
  const completedGoals = goals.filter(goal => goal.isCompleted)

  return (
    <Card>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <Target className="w-5 h-5 text-primary-400" />
          Channel Goals
        </h3>
        <Button
          onClick={() => setShowAddForm(!showAddForm)}
          size="sm"
          variant="secondary"
          className="flex items-center gap-1"
        >
          <Plus className="w-4 h-4" />
          Add Goal
        </Button>
      </div>

      {/* Add Goal Form Slide Down */}
      <div className={`overflow-hidden transition-all duration-300 ${
        showAddForm ? 'max-h-96 opacity-100 mb-4' : 'max-h-0 opacity-0'
      }`}>
        <div className="bg-dark-800 rounded-lg p-4 border border-dark-600">
          <h4 className="text-sm font-medium mb-3">Create New Goal</h4>
          <div className="space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs text-dark-400 mb-1">Goal Title</label>
                <input
                  type="text"
                  value={newGoal.title}
                  onChange={(e) => setNewGoal(prev => ({ ...prev, title: e.target.value }))}
                  className="w-full bg-dark-700 border border-dark-600 rounded px-3 py-2 text-sm focus:outline-none focus:border-primary-500"
                  placeholder="e.g., Reach 100K subscribers"
                />
              </div>
              <div>
                <label className="block text-xs text-dark-400 mb-1">Goal Type</label>
                <select
                  value={newGoal.type}
                  onChange={(e) => setNewGoal(prev => ({ ...prev, type: e.target.value as any }))}
                  className="w-full bg-dark-700 border border-dark-600 rounded px-3 py-2 text-sm focus:outline-none focus:border-primary-500"
                >
                  <option value="subscribers">Subscribers</option>
                  <option value="views">Views</option>
                  <option value="engagement">Engagement</option>
                  <option value="revenue">Revenue</option>
                  <option value="custom">Custom</option>
                </select>
              </div>
            </div>
            
            <div>
              <label className="block text-xs text-dark-400 mb-1">Description</label>
              <textarea
                value={newGoal.description}
                onChange={(e) => setNewGoal(prev => ({ ...prev, description: e.target.value }))}
                className="w-full bg-dark-700 border border-dark-600 rounded px-3 py-2 text-sm focus:outline-none focus:border-primary-500"
                rows={2}
                placeholder="Optional description..."
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div>
                <label className="block text-xs text-dark-400 mb-1">Target Value</label>
                <input
                  type="number"
                  value={newGoal.targetValue}
                  onChange={(e) => setNewGoal(prev => ({ ...prev, targetValue: parseInt(e.target.value) || 0 }))}
                  className="w-full bg-dark-700 border border-dark-600 rounded px-3 py-2 text-sm focus:outline-none focus:border-primary-500"
                  placeholder="100000"
                />
              </div>
              <div>
                <label className="block text-xs text-dark-400 mb-1">Current Value</label>
                <input
                  type="number"
                  value={newGoal.currentValue}
                  onChange={(e) => setNewGoal(prev => ({ ...prev, currentValue: parseInt(e.target.value) || 0 }))}
                  className="w-full bg-dark-700 border border-dark-600 rounded px-3 py-2 text-sm focus:outline-none focus:border-primary-500"
                  placeholder="67000"
                />
              </div>
              <div>
                <label className="block text-xs text-dark-400 mb-1">Target Date</label>
                <input
                  type="date"
                  value={newGoal.targetDate}
                  onChange={(e) => setNewGoal(prev => ({ ...prev, targetDate: e.target.value }))}
                  className="w-full bg-dark-700 border border-dark-600 rounded px-3 py-2 text-sm focus:outline-none focus:border-primary-500"
                />
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <Button
                onClick={() => setShowAddForm(false)}
                variant="secondary"
                size="sm"
              >
                Cancel
              </Button>
              <Button
                onClick={handleAddGoal}
                size="sm"
                disabled={!newGoal.title || newGoal.targetValue <= 0}
              >
                Create Goal
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Active Goals */}
      <div className="space-y-4">
        {activeGoals.length === 0 ? (
          <div className="text-center py-8 text-dark-400">
            <Target className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>No active goals yet</p>
            <p className="text-sm">Click "Add Goal" to create your first goal</p>
          </div>
        ) : (
          activeGoals.map((goal) => {
            const IconComponent = goalTypeIcons[goal.type]
            const progress = getProgressPercentage(goal.currentValue, goal.targetValue)
            
            return (
              <div key={goal.id} className="bg-dark-800 rounded-lg p-4 border border-dark-600">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <IconComponent className="w-4 h-4 text-primary-400" />
                    <h4 className="font-medium">{goal.title}</h4>
                  </div>
                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => setEditingGoal(editingGoal === goal.id ? null : goal.id)}
                      className="p-1 hover:bg-dark-700 rounded"
                    >
                      <Edit2 className="w-3 h-3 text-dark-400" />
                    </button>
                    <button
                      onClick={() => deleteGoal(goal.id)}
                      className="p-1 hover:bg-red-900/20 rounded"
                    >
                      <Trash2 className="w-3 h-3 text-red-400" />
                    </button>
                  </div>
                </div>
                
                {goal.description && (
                  <p className="text-sm text-dark-400 mb-3">{goal.description}</p>
                )}
                
                <div className="flex justify-between text-sm mb-2">
                  <span>Progress</span>
                  <span>
                    {formatValue(goal.currentValue, goal.type)} / {formatValue(goal.targetValue, goal.type)}
                  </span>
                </div>
                
                <div className="w-full bg-dark-700 rounded-full h-2 mb-2">
                  <div 
                    className="bg-primary-500 h-2 rounded-full transition-all duration-300" 
                    style={{ width: `${progress}%` }}
                  />
                </div>
                
                <div className="flex justify-between items-center text-xs text-dark-400">
                  <span>{progress.toFixed(1)}% complete</span>
                  {goal.targetDate && (
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {new Date(goal.targetDate).toLocaleDateString()}
                    </span>
                  )}
                </div>

                {/* Quick Progress Update */}
                {editingGoal === goal.id && (
                  <div className="mt-3 pt-3 border-t border-dark-600">
                    <label className="block text-xs text-dark-400 mb-1">Update Progress</label>
                    <div className="flex gap-2">
                      <input
                        type="number"
                        defaultValue={goal.currentValue}
                        onChange={(e) => {
                          const value = parseInt(e.target.value) || 0
                          handleUpdateProgress(goal.id, value)
                        }}
                        className="flex-1 bg-dark-700 border border-dark-600 rounded px-3 py-1 text-sm focus:outline-none focus:border-primary-500"
                      />
                      <Button
                        onClick={() => setEditingGoal(null)}
                        size="sm"
                        variant="secondary"
                      >
                        <Check className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            )
          })
        )}
      </div>

      {/* Completed Goals */}
      {completedGoals.length > 0 && (
        <div className="mt-6 pt-4 border-t border-dark-600">
          <h4 className="text-sm font-medium text-dark-400 mb-3 flex items-center gap-2">
            <Check className="w-4 h-4" />
            Completed Goals ({completedGoals.length})
          </h4>
          <div className="space-y-2">
            {completedGoals.map((goal) => {
              const IconComponent = goalTypeIcons[goal.type]
              return (
                <div key={goal.id} className="bg-green-900/20 rounded-lg p-3 border border-green-500/20">
                  <div className="flex items-center gap-2">
                    <IconComponent className="w-4 h-4 text-green-400" />
                    <span className="text-sm flex-1">{goal.title}</span>
                    <Check className="w-4 h-4 text-green-400" />
                    <button
                      onClick={() => deleteGoal(goal.id)}
                      className="p-1 hover:bg-red-900/20 rounded ml-2"
                      title="Delete completed goal"
                    >
                      <Trash2 className="w-3 h-3 text-red-400" />
                    </button>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </Card>
  )
}