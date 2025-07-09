import { useState } from 'react'
import { Search, Filter, Trash2, Clock, CheckCircle, BarChart3, X, Tag } from 'lucide-react'
import { cn } from '@/utils'
import { useSuggestionStore, SuggestionType } from '@/store/suggestionStore'
import Button from '@/components/common/Button'

interface SavedSuggestionsPanelProps {
  isOpen: boolean
  onClose: () => void
}

export default function SavedSuggestionsPanel({ isOpen, onClose }: SavedSuggestionsPanelProps) {
  const { 
    savedSuggestions, 
    deleteSuggestion, 
    getAnalytics 
  } = useSuggestionStore()
  
  const [searchTerm, setSearchTerm] = useState('')
  const [filterType, setFilterType] = useState<SuggestionType | 'all'>('all')
  const [filterStatus, setFilterStatus] = useState<'all' | 'implemented' | 'pending'>('all')
  const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'type'>('newest')
  
  const analytics = getAnalytics()
  
  const filteredSuggestions = savedSuggestions
    .filter(suggestion => {
      const matchesSearch = suggestion.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           suggestion.category.toLowerCase().includes(searchTerm.toLowerCase())
      const matchesType = filterType === 'all' || suggestion.type === filterType
      const matchesStatus = filterStatus === 'all' || 
                           (filterStatus === 'implemented' && suggestion.isImplemented) ||
                           (filterStatus === 'pending' && !suggestion.isImplemented)
      return matchesSearch && matchesType && matchesStatus
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'newest':
          return new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
        case 'oldest':
          return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
        case 'type':
          return a.type.localeCompare(b.type)
        default:
          return 0
      }
    })

  const getTypeIcon = (type: SuggestionType) => {
    switch (type) {
      case 'content_idea': return '💡'
      case 'title_optimization': return '🎯'
      case 'script_suggestion': return '📝'
      case 'hook_improvement': return '🎣'
      default: return '📋'
    }
  }

  const getTypeColor = (type: SuggestionType) => {
    switch (type) {
      case 'content_idea': return 'bg-blue-500/20 text-blue-400'
      case 'title_optimization': return 'bg-green-500/20 text-green-400'
      case 'script_suggestion': return 'bg-purple-500/20 text-purple-400'
      case 'hook_improvement': return 'bg-orange-500/20 text-orange-400'
      default: return 'bg-gray-500/20 text-gray-400'
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-background-secondary rounded-xl border border-white/20 w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-primary-600/20 flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-primary-400" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">Saved Suggestions</h2>
              <p className="text-sm text-dark-400">
                {savedSuggestions.length} suggestions • {analytics.implementationRate}% implemented
              </p>
            </div>
          </div>
          <Button
            onClick={onClose}
            variant="ghost"
            size="sm"
            className="p-2 hover:bg-white/10"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>

        {/* Analytics Summary */}
        <div className="p-6 border-b border-white/10 bg-dark-800/30">
          <div className="grid grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-white">{analytics.totalSuggestions}</div>
              <div className="text-xs text-dark-400">Total Suggestions</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400">{analytics.implementedCount}</div>
              <div className="text-xs text-dark-400">Implemented</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-400">{analytics.implementationRate}%</div>
              <div className="text-xs text-dark-400">Implementation Rate</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-400">{analytics.helpfulnessRate}%</div>
              <div className="text-xs text-dark-400">Helpfulness Rate</div>
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="p-6 border-b border-white/10 space-y-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-dark-400" />
            <input
              type="text"
              placeholder="Search suggestions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-dark-800/50 border border-white/20 rounded-lg text-white placeholder-dark-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          {/* Filters */}
          <div className="flex items-center gap-4 flex-wrap">
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-dark-400" />
              <span className="text-sm text-dark-400">Filter:</span>
            </div>

            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value as SuggestionType | 'all')}
              className="px-3 py-1 bg-dark-800/50 border border-white/20 rounded text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="all">All Types</option>
              <option value="content_idea">Content Ideas</option>
              <option value="title_optimization">Title Optimization</option>
              <option value="script_suggestion">Script Suggestions</option>
              <option value="hook_improvement">Hook Improvements</option>
            </select>

            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value as 'all' | 'implemented' | 'pending')}
              className="px-3 py-1 bg-dark-800/50 border border-white/20 rounded text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="all">All Status</option>
              <option value="implemented">Implemented</option>
              <option value="pending">Pending</option>
            </select>

            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as 'newest' | 'oldest' | 'type')}
              className="px-3 py-1 bg-dark-800/50 border border-white/20 rounded text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
              <option value="type">Group by Type</option>
            </select>
          </div>
        </div>

        {/* Suggestions List */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {filteredSuggestions.length === 0 ? (
            <div className="text-center py-12">
              <div className="w-16 h-16 rounded-full bg-dark-800/50 flex items-center justify-center mx-auto mb-4">
                <BarChart3 className="w-8 h-8 text-dark-400" />
              </div>
              <p className="text-dark-400 text-lg">No suggestions found</p>
              <p className="text-dark-500 text-sm mt-2">
                {searchTerm ? 'Try adjusting your search or filters' : 'Start chatting with your AI agent to generate suggestions'}
              </p>
            </div>
          ) : (
            filteredSuggestions.map((suggestion) => (
              <div
                key={suggestion.id}
                className="bg-dark-800/30 rounded-lg border border-white/10 p-4 hover:border-white/20 transition-colors"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-lg">{getTypeIcon(suggestion.type)}</span>
                      <span className={cn(
                        'px-2 py-1 rounded text-xs font-medium',
                        getTypeColor(suggestion.type)
                      )}>
                        {suggestion.category}
                      </span>
                      {suggestion.isImplemented && (
                        <div className="flex items-center gap-1 text-green-400">
                          <CheckCircle className="w-3 h-3" />
                          <span className="text-xs">Implemented</span>
                        </div>
                      )}
                    </div>
                    
                    <p className="text-white text-sm mb-3 line-clamp-3">
                      {suggestion.content}
                    </p>
                    
                    <div className="flex items-center gap-4 text-xs text-dark-400">
                      <div className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {new Date(suggestion.timestamp).toLocaleDateString()}
                      </div>
                      
                      {suggestion.tags.length > 0 && (
                        <div className="flex items-center gap-1">
                          <Tag className="w-3 h-3" />
                          {suggestion.tags.slice(0, 2).map((tag, index) => (
                            <span key={index} className="bg-dark-700 px-2 py-1 rounded text-xs">
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <Button
                      variant="ghost"
                      size="xs"
                      className="p-2 hover:bg-red-500/20 text-red-400"
                      onClick={() => deleteSuggestion(suggestion.id)}
                      title="Delete suggestion"
                    >
                      <Trash2 className="w-3 h-3" />
                    </Button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}