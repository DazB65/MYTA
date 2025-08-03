import { useState } from 'react'
import { useChat } from '@/hooks/useChat'
import Button from '@/components/common/Button'
import QuickActionModal from './QuickActionModal'

const shortcuts = [
  {
    id: 'trending_topics',
    title: 'Trending Topics',
    description: 'Discover trending topics',
    icon: '🔥',
  },
  {
    id: 'competitor_analysis',
    title: 'Competitor Analysis',
    description: 'Analyze competitor strategies',
    icon: '📊',
  },
  {
    id: 'channel_insights',
    title: 'Channel Insights',
    description: 'Get channel performance insights',
    icon: '💡',
  },
]

export default function SimpleShortcuts() {
  const { sendQuickAction, isLoading } = useChat()
  const [selectedAction, setSelectedAction] = useState<(typeof shortcuts)[0] | null>(null)

  const handleActionClick = (action: typeof shortcuts[0]) => {
    setSelectedAction(action)
  }

  const handleModalSubmit = (context: string) => {
    if (selectedAction) {
      sendQuickAction(selectedAction.id, context)
    }
    setSelectedAction(null)
  }

  const handleModalClose = () => {
    setSelectedAction(null)
  }

  return (
    <>
      <div className="flex items-center justify-center gap-4">
        {shortcuts.map((action) => (
          <Button
            key={action.id}
            onClick={() => handleActionClick(action)}
            disabled={isLoading}
            variant="secondary"
            size="sm"
            className="flex items-center gap-2 py-3 px-4 text-center bg-purple-600/20 hover:bg-purple-600/40 border border-purple-400/30 hover:border-purple-400/60 transition-all text-white"
          >
            <span className="text-base">{action.icon}</span>
            <div>
              <div className="text-sm font-medium text-white">{action.title}</div>
            </div>
          </Button>
        ))}
      </div>

      {selectedAction && (
        <QuickActionModal
          isOpen={!!selectedAction}
          onClose={handleModalClose}
          onSubmit={handleModalSubmit}
          action={selectedAction}
          isLoading={isLoading}
        />
      )}
    </>
  )
}