import React, { useState } from 'react'
import { X, Search, Bookmark, Trash2, Edit3, Tag, Calendar, User, Filter } from 'lucide-react'
import { useSavedMessagesStore } from '@/store/savedMessagesStore'
import { cn } from '@/utils'

interface SavedMessagesPanelProps {
  isOpen: boolean
  onClose: () => void
}

export const SavedMessagesPanel: React.FC<SavedMessagesPanelProps> = ({ isOpen, onClose }) => {
  const {
    savedMessages,
    categories,
    unsaveMessage,
    updateMessage,
    searchMessages,
    addCategory,
    clearAll
  } = useSavedMessagesStore()

  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string>('All')
  const [editingMessage, setEditingMessage] = useState<string | null>(null)
  const [editingNotes, setEditingNotes] = useState('')
  const [newCategory, setNewCategory] = useState('')
  const [showAddCategory, setShowAddCategory] = useState(false)

  // Filter messages based on search and category
  const filteredMessages = React.useMemo(() => {
    let messages = savedMessages

    if (searchQuery) {
      messages = searchMessages(searchQuery)
    }

    if (selectedCategory !== 'All') {
      messages = messages.filter(msg => msg.category === selectedCategory)
    }

    return messages.sort((a, b) => b.timestamp - a.timestamp)
  }, [savedMessages, searchQuery, selectedCategory, searchMessages])

  const handleSaveNotes = (messageId: string) => {
    updateMessage(messageId, { notes: editingNotes })
    setEditingMessage(null)
    setEditingNotes('')
  }

  const handleAddCategory = () => {
    if (newCategory.trim()) {
      addCategory(newCategory.trim())
      setNewCategory('')
      setShowAddCategory(false)
    }
  }

  const formatDate = (timestamp: number) => {
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    }).format(new Date(timestamp))
  }

  const getCategoryColor = (category: string) => {
    const colors = {
      'General': 'bg-gray-500',
      'Ideas': 'bg-blue-500',
      'Scripts': 'bg-green-500',
      'Analytics': 'bg-purple-500',
      'Strategy': 'bg-orange-500'
    }
    return colors[category as keyof typeof colors] || 'bg-gray-500'
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 rounded-xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-700">
          <div className="flex items-center gap-3">
            <Bookmark className="w-6 h-6 text-yellow-400" />
            <h2 className="text-xl font-bold text-white">Saved Chats</h2>
            <span className="text-sm text-gray-400">({filteredMessages.length})</span>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-400" />
          </button>
        </div>

        {/* Search and Filters */}
        <div className="p-6 border-b border-gray-700">
          <div className="flex flex-col sm:flex-row gap-4">
            {/* Search */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search saved chats..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Category Filter */}
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-gray-400" />
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="All">All Categories</option>
                {categories.map(category => (
                  <option key={category} value={category}>{category}</option>
                ))}
              </select>
            </div>

            {/* Add Category */}
            {showAddCategory ? (
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="New category..."
                  value={newCategory}
                  onChange={(e) => setNewCategory(e.target.value)}
                  className="px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  onKeyPress={(e) => e.key === 'Enter' && handleAddCategory()}
                />
                <button
                  onClick={handleAddCategory}
                  className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Add
                </button>
                <button
                  onClick={() => setShowAddCategory(false)}
                  className="px-3 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
                >
                  Cancel
                </button>
              </div>
            ) : (
              <button
                onClick={() => setShowAddCategory(true)}
                className="px-3 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors flex items-center gap-2"
              >
                <Tag className="w-4 h-4" />
                Add Category
              </button>
            )}
          </div>
        </div>

        {/* Messages List */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4 max-h-[500px]">
          {filteredMessages.length === 0 ? (
            <div className="text-center py-12">
              <Bookmark className="w-12 h-12 text-gray-600 mx-auto mb-4" />
              <p className="text-gray-400">
                {searchQuery || selectedCategory !== 'All' 
                  ? 'No chats found matching your criteria' 
                  : 'No saved chats yet. Start saving AI conversations you want to keep!'
                }
              </p>
            </div>
          ) : (
            filteredMessages.map((message) => (
              <div
                key={message.id}
                className="bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-gray-600 transition-colors"
              >
                {/* Message Header */}
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                      <img
                        src={`/assets/images/Avatars/${message.avatar}`}
                        alt={message.agentName}
                        className="w-6 h-6 rounded-full"
                        onError={(e) => {
                          e.currentTarget.src = '/assets/images/CM Logo White.svg'
                        }}
                      />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <User className="w-4 h-4 text-gray-400" />
                        <span className="text-sm font-medium text-white">{message.agentName}</span>
                        <div className={cn(
                          'px-2 py-1 rounded-full text-xs text-white',
                          getCategoryColor(message.category || 'General')
                        )}>
                          {message.category}
                        </div>
                      </div>
                      <div className="flex items-center gap-2 text-xs text-gray-400 mt-1">
                        <Calendar className="w-3 h-3" />
                        {formatDate(message.timestamp)}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => {
                        setEditingMessage(message.id)
                        setEditingNotes(message.notes || '')
                      }}
                      className="p-1 hover:bg-gray-700 rounded transition-colors"
                      title="Add notes"
                    >
                      <Edit3 className="w-4 h-4 text-gray-400" />
                    </button>
                    <button
                      onClick={() => unsaveMessage(message.id)}
                      className="p-1 hover:bg-gray-700 rounded transition-colors"
                      title="Remove from saved"
                    >
                      <Trash2 className="w-4 h-4 text-red-400" />
                    </button>
                  </div>
                </div>

                {/* Message Content */}
                <div className="text-sm text-gray-300 mb-3 leading-relaxed">
                  {message.content.length > 300 
                    ? `${message.content.substring(0, 300)}...` 
                    : message.content
                  }
                </div>

                {/* Notes Section */}
                {editingMessage === message.id ? (
                  <div className="space-y-2">
                    <textarea
                      value={editingNotes}
                      onChange={(e) => setEditingNotes(e.target.value)}
                      placeholder="Add your notes about this chat..."
                      className="w-full p-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      rows={3}
                    />
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleSaveNotes(message.id)}
                        className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors text-sm"
                      >
                        Save Notes
                      </button>
                      <button
                        onClick={() => setEditingMessage(null)}
                        className="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors text-sm"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : message.notes && (
                  <div className="bg-gray-700 rounded p-3 text-sm text-gray-300">
                    <div className="text-xs text-gray-400 mb-1">Notes:</div>
                    {message.notes}
                  </div>
                )}

                {/* Tags */}
                {message.tags && message.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {message.tags.map(tag => (
                      <span
                        key={tag}
                        className="px-2 py-1 bg-gray-700 text-xs text-gray-300 rounded"
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-700 flex items-center justify-between">
          <div className="text-sm text-gray-400">
            {filteredMessages.length} of {savedMessages.length} chats
          </div>
          <div className="flex gap-2">
            <button
              onClick={clearAll}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Clear All
            </button>
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}