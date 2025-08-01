import { useState, useEffect } from 'react'
import { Plus, CheckCircle2, Circle, Calendar, Flag, Trash2, Edit3, Search, ChevronDown, ChevronRight } from 'lucide-react'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'

interface Task {
  id: string
  title: string
  description?: string
  completed: boolean
  priority: 'low' | 'medium' | 'high'
  dueDate?: string
  category: string
  createdAt: string
  source?: 'agent' | 'manual'
  agentName?: string
}

export default function TaskManager() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [showAddForm, setShowAddForm] = useState(false)
  // const [editingTask] = useState<Task | null>(null)
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [expandedTasks, setExpandedTasks] = useState<Set<string>>(new Set())
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    priority: 'medium' as 'low' | 'medium' | 'high',
    dueDate: '',
    category: 'general'
  })

  // Load tasks from localStorage on mount and listen for updates
  useEffect(() => {
    // Load existing tasks
    const loadTasks = () => {
      const storedTasks = localStorage.getItem('Vidalytics_tasks')
      if (storedTasks) {
        setTasks(JSON.parse(storedTasks))
      } else {
        // Load sample tasks if no stored tasks
        const sampleTasks: Task[] = [
          {
            id: '1',
            title: 'Edit YouTube intro sequence',
            description: 'Update the channel intro with new branding',
            completed: false,
            priority: 'high',
            dueDate: '2024-01-20',
            category: 'editing',
            createdAt: '2024-01-15T10:00:00Z',
            source: 'manual'
          },
          {
            id: '2',
            title: 'Research competitor videos',
            description: 'Analyze top 5 competitor channels for content ideas',
            completed: true,
            priority: 'medium',
            category: 'research',
            createdAt: '2024-01-14T14:30:00Z',
            source: 'manual'
          },
          {
            id: '3',
            title: 'Schedule social media posts',
            description: 'Plan and schedule posts for next week',
            completed: false,
            priority: 'medium',
            dueDate: '2024-01-18',
            category: 'marketing',
            createdAt: '2024-01-15T09:00:00Z',
            source: 'manual'
          },
          {
            id: '4',
            title: 'Update channel banner',
            description: 'Design new banner with current subscriber count',
            completed: false,
            priority: 'low',
            category: 'design',
            createdAt: '2024-01-13T16:00:00Z',
            source: 'manual'
          }
        ]
        setTasks(sampleTasks)
      }
    }

    loadTasks()

    // Listen for storage events to sync tasks across tabs/components
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'Vidalytics_tasks') {
        loadTasks()
      }
    }

    window.addEventListener('storage', handleStorageChange)
    
    // Also listen for custom event for same-tab updates
    const handleTaskUpdate = () => loadTasks()
    window.addEventListener('taskUpdate', handleTaskUpdate)

    return () => {
      window.removeEventListener('storage', handleStorageChange)
      window.removeEventListener('taskUpdate', handleTaskUpdate)
    }
  }, [])

  const addTask = () => {
    if (!newTask.title.trim()) return

    const task: Task = {
      id: Date.now().toString(),
      title: newTask.title,
      description: newTask.description,
      completed: false,
      priority: newTask.priority,
      dueDate: newTask.dueDate || undefined,
      category: newTask.category,
      createdAt: new Date().toISOString(),
      source: 'manual'
    }

    const updatedTasks = [task, ...tasks]
    setTasks(updatedTasks)
    localStorage.setItem('Vidalytics_tasks', JSON.stringify(updatedTasks))
    
    // Dispatch custom event for same-tab updates
    window.dispatchEvent(new Event('taskUpdate'))
    
    setNewTask({
      title: '',
      description: '',
      priority: 'medium',
      dueDate: '',
      category: 'general'
    })
    setShowAddForm(false)
  }

  const toggleTask = (id: string) => {
    const updatedTasks = tasks.map(task => 
      task.id === id ? { ...task, completed: !task.completed } : task
    )
    setTasks(updatedTasks)
    localStorage.setItem('Vidalytics_tasks', JSON.stringify(updatedTasks))
    window.dispatchEvent(new Event('taskUpdate'))
  }

  const deleteTask = (id: string) => {
    const updatedTasks = tasks.filter(task => task.id !== id)
    setTasks(updatedTasks)
    localStorage.setItem('Vidalytics_tasks', JSON.stringify(updatedTasks))
    window.dispatchEvent(new Event('taskUpdate'))
  }

  // const updateTask = (updatedTask: Task) => {
  //   setTasks(tasks.map(task => 
  //     task.id === updatedTask.id ? updatedTask : task
  //   ))
  //   setEditingTask(null)
  // }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-400 bg-red-400/10'
      case 'medium': return 'text-yellow-400 bg-yellow-400/10'
      case 'low': return 'text-green-400 bg-green-400/10'
      default: return 'text-gray-400 bg-gray-400/10'
    }
  }

  const getCategoryColor = (category: string) => {
    const colors = {
      editing: 'bg-purple-500/20 text-purple-400',
      research: 'bg-blue-500/20 text-blue-400',
      marketing: 'bg-green-500/20 text-green-400',
      design: 'bg-pink-500/20 text-pink-400',
      general: 'bg-gray-500/20 text-gray-400'
    }
    return colors[category as keyof typeof colors] || colors.general
  }

  const filteredTasks = tasks.filter(task => {
    const matchesFilter = filter === 'all' || 
      (filter === 'completed' && task.completed) ||
      (filter === 'pending' && !task.completed)
    
    const matchesSearch = task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      task.description?.toLowerCase().includes(searchTerm.toLowerCase())
    
    return matchesFilter && matchesSearch
  })

  const completedCount = tasks.filter(t => t.completed).length
  const totalCount = tasks.length

  const toggleTaskExpansion = (taskId: string) => {
    setExpandedTasks(prev => {
      const newSet = new Set(prev)
      if (newSet.has(taskId)) {
        newSet.delete(taskId)
      } else {
        newSet.add(taskId)
      }
      return newSet
    })
  }

  const isTaskExpanded = (taskId: string) => expandedTasks.has(taskId)

  const truncateText = (text: string, maxLength: number) => {
    if (text.length <= maxLength) return text
    return text.substring(0, maxLength) + '...'
  }

  return (
    <Card>
      <div className="p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-xl font-semibold mb-1">Task Manager</h3>
            <p className="text-sm text-dark-400">
              {completedCount} of {totalCount} tasks completed
            </p>
          </div>
          <Button 
            onClick={() => setShowAddForm(true)}
            size="sm"
            className="flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            Add Task
          </Button>
        </div>

        {/* Progress Bar */}
        <div className="mb-6">
          <div className="w-full bg-dark-700 rounded-full h-2">
            <div 
              className="bg-primary-500 h-2 rounded-full transition-all duration-300" 
              style={{ width: `${totalCount > 0 ? (completedCount / totalCount) * 100 : 0}%` }}
            ></div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="flex flex-col sm:flex-row gap-3 mb-6">
          <div className="flex gap-2">
            {(['all', 'pending', 'completed'] as const).map(filterType => (
              <button
                key={filterType}
                onClick={() => setFilter(filterType)}
                className={`px-3 py-1 text-sm rounded-lg transition-colors ${
                  filter === filterType 
                    ? 'bg-primary-600 text-white' 
                    : 'bg-dark-800 text-dark-400 hover:text-white'
                }`}
              >
                {filterType.charAt(0).toUpperCase() + filterType.slice(1)}
              </button>
            ))}
          </div>
          <div className="relative flex-1 max-w-sm">
            <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-dark-400" />
            <input
              type="text"
              placeholder="Search tasks..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-3 py-1 bg-dark-800 border border-dark-600 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
        </div>

        {/* Add Task Form */}
        {showAddForm && (
          <div className="mb-6 p-4 bg-dark-800 rounded-lg border border-dark-600">
            <h4 className="text-sm font-medium mb-3">Add New Task</h4>
            <div className="space-y-3">
              <input
                type="text"
                placeholder="Task title..."
                value={newTask.title}
                onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                className="w-full px-3 py-2 bg-dark-900 border border-dark-600 rounded text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <textarea
                placeholder="Description (optional)..."
                value={newTask.description}
                onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                rows={2}
                className="w-full px-3 py-2 bg-dark-900 border border-dark-600 rounded text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <div className="flex gap-3">
                <select
                  value={newTask.priority}
                  onChange={(e) => setNewTask({ ...newTask, priority: e.target.value as any })}
                  className="px-3 py-2 bg-dark-900 border border-dark-600 rounded text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="low">Low Priority</option>
                  <option value="medium">Medium Priority</option>
                  <option value="high">High Priority</option>
                </select>
                <select
                  value={newTask.category}
                  onChange={(e) => setNewTask({ ...newTask, category: e.target.value })}
                  className="px-3 py-2 bg-dark-900 border border-dark-600 rounded text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="general">General</option>
                  <option value="editing">Editing</option>
                  <option value="research">Research</option>
                  <option value="marketing">Marketing</option>
                  <option value="design">Design</option>
                </select>
                <input
                  type="date"
                  value={newTask.dueDate}
                  onChange={(e) => setNewTask({ ...newTask, dueDate: e.target.value })}
                  className="px-3 py-2 bg-dark-900 border border-dark-600 rounded text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div className="flex gap-2">
                <Button onClick={addTask} size="sm">Add Task</Button>
                <Button 
                  onClick={() => setShowAddForm(false)} 
                  variant="secondary" 
                  size="sm"
                >
                  Cancel
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Task List */}
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {filteredTasks.length === 0 ? (
            <div className="text-center py-8 text-dark-400">
              <Circle className="w-12 h-12 mx-auto mb-3 opacity-50" />
              <p>No tasks found</p>
              <p className="text-sm">Add a task to get started</p>
            </div>
          ) : (
            filteredTasks.map(task => (
              <div
                key={task.id}
                className={`p-3 rounded-lg border transition-all ${
                  task.completed 
                    ? 'bg-dark-800/50 border-dark-700 opacity-75' 
                    : 'bg-dark-800 border-dark-600 hover:border-dark-500'
                }`}
              >
                <div className="flex items-start gap-3">
                  <button
                    onClick={() => toggleTask(task.id)}
                    className="mt-0.5 text-primary-400 hover:text-primary-300"
                  >
                    {task.completed ? (
                      <CheckCircle2 className="w-5 h-5" />
                    ) : (
                      <Circle className="w-5 h-5" />
                    )}
                  </button>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className={`font-medium ${task.completed ? 'line-through text-dark-500' : ''}`}>
                        {task.title}
                      </h4>
                      <span className={`px-2 py-0.5 text-xs rounded-full ${getPriorityColor(task.priority)}`}>
                        {task.priority}
                      </span>
                      <span className={`px-2 py-0.5 text-xs rounded ${getCategoryColor(task.category)}`}>
                        {task.category}
                      </span>
                      {task.source === 'agent' && (
                        <span className="px-2 py-0.5 text-xs rounded bg-primary-600/20 text-primary-400 flex items-center gap-1">
                          🤖 {task.agentName || 'AI'}
                        </span>
                      )}
                      {/* Expand button for AI tasks with descriptions */}
                      {task.source === 'agent' && task.description && task.description.length > 80 && (
                        <button
                          onClick={() => toggleTaskExpansion(task.id)}
                          className="p-1 text-dark-400 hover:text-white rounded transition-colors"
                          title={isTaskExpanded(task.id) ? 'Collapse details' : 'Show details'}
                        >
                          {isTaskExpanded(task.id) ? (
                            <ChevronDown className="w-4 h-4" />
                          ) : (
                            <ChevronRight className="w-4 h-4" />
                          )}
                        </button>
                      )}
                    </div>
                    
                    {task.description && (
                      <div className={`text-sm mb-2 ${task.completed ? 'line-through text-dark-500' : 'text-dark-300'}`}>
                        {task.source === 'agent' && task.description.length > 80 ? (
                          <div>
                            {!isTaskExpanded(task.id) ? (
                              <p>{truncateText(task.description, 80)}</p>
                            ) : (
                              <div className="space-y-2">
                                <p className="whitespace-pre-wrap">{task.description}</p>
                              </div>
                            )}
                          </div>
                        ) : (
                          <p>{task.description}</p>
                        )}
                      </div>
                    )}
                    
                    <div className="flex items-center gap-4 text-xs text-dark-400">
                      {task.dueDate && (
                        <div className="flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          Due: {new Date(task.dueDate).toLocaleDateString()}
                        </div>
                      )}
                      <div className="flex items-center gap-1">
                        <Flag className="w-3 h-3" />
                        Created: {new Date(task.createdAt).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => console.log('Edit task:', task.id)}
                      className="p-1 text-dark-400 hover:text-white rounded"
                    >
                      <Edit3 className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => deleteTask(task.id)}
                      className="p-1 text-dark-400 hover:text-red-400 rounded"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </Card>
  )
}