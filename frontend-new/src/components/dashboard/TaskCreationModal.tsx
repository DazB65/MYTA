import { useState } from 'react'
import { X } from 'lucide-react'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'

interface TaskCreationModalProps {
  isOpen: boolean
  onClose: () => void
  onCreateTask: (task: any) => void
  messageContent: string
  agentName: string
}

export default function TaskCreationModal({ 
  isOpen, 
  onClose, 
  onCreateTask, 
  messageContent,
  agentName 
}: TaskCreationModalProps) {
  const [taskData, setTaskData] = useState({
    title: '',
    description: messageContent,
    priority: 'medium' as 'low' | 'medium' | 'high',
    dueDate: '',
    category: 'general'
  })

  // Extract potential task title from message (first sentence or line)
  useState(() => {
    const firstLine = messageContent.split('\n')[0]
    const firstSentence = messageContent.split('.')[0]
    const suggestedTitle = (firstLine.length < firstSentence.length ? firstLine : firstSentence).slice(0, 60)
    setTaskData(prev => ({ ...prev, title: suggestedTitle }))
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!taskData.title.trim()) return

    const task = {
      id: Date.now().toString(),
      title: taskData.title,
      description: taskData.description,
      completed: false,
      priority: taskData.priority,
      dueDate: taskData.dueDate || undefined,
      category: taskData.category,
      createdAt: new Date().toISOString(),
      source: 'agent',
      agentName: agentName
    }

    onCreateTask(task)
    onClose()
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <Card className="relative w-full max-w-2xl bg-background-secondary border-white/20 p-6 animate-in fade-in zoom-in duration-200">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-xl font-semibold">Create Task from Agent Suggestion</h3>
            <p className="text-sm text-dark-400 mt-1">
              Review and edit the task details before adding to your task manager
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-dark-400" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Task Title */}
          <div>
            <label className="block text-sm font-medium mb-2">Task Title *</label>
            <input
              type="text"
              value={taskData.title}
              onChange={(e) => setTaskData({ ...taskData, title: e.target.value })}
              className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter a clear, actionable task title..."
              required
            />
          </div>

          {/* Task Description */}
          <div>
            <label className="block text-sm font-medium mb-2">Description</label>
            <textarea
              value={taskData.description}
              onChange={(e) => setTaskData({ ...taskData, description: e.target.value })}
              rows={4}
              className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Add more details about this task..."
            />
          </div>

          {/* Task Options */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Priority */}
            <div>
              <label className="block text-sm font-medium mb-2">Priority</label>
              <select
                value={taskData.priority}
                onChange={(e) => setTaskData({ ...taskData, priority: e.target.value as any })}
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="low">Low Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="high">High Priority</option>
              </select>
            </div>

            {/* Category */}
            <div>
              <label className="block text-sm font-medium mb-2">Category</label>
              <select
                value={taskData.category}
                onChange={(e) => setTaskData({ ...taskData, category: e.target.value })}
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="general">General</option>
                <option value="editing">Editing</option>
                <option value="research">Research</option>
                <option value="marketing">Marketing</option>
                <option value="design">Design</option>
                <option value="content">Content Creation</option>
                <option value="optimization">Optimization</option>
              </select>
            </div>

            {/* Due Date */}
            <div>
              <label className="block text-sm font-medium mb-2">Due Date</label>
              <input
                type="date"
                value={taskData.dueDate}
                onChange={(e) => setTaskData({ ...taskData, dueDate: e.target.value })}
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>

          {/* Agent Info */}
          <div className="p-3 bg-primary-600/10 border border-primary-600/20 rounded-lg">
            <div className="flex items-center gap-2 text-sm">
              <span className="text-primary-400">🤖</span>
              <span className="text-dark-300">
                Suggested by <span className="font-medium text-primary-400">{agentName}</span>
              </span>
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-3 pt-4">
            <Button type="submit" className="flex-1">
              Create Task
            </Button>
            <Button type="button" variant="secondary" onClick={onClose}>
              Cancel
            </Button>
          </div>
        </form>
      </Card>
    </div>
  )
}