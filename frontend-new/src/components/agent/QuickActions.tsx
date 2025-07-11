import { useState } from 'react'
import { useChat } from '@/hooks/useChat'
import Button from '@/components/common/Button'
import QuickActionModal from './QuickActionModal'

const quickActions = [
  {
    id: 'generate_script',
    title: 'Generate Script',
    description: 'Create video scripts',
    icon: '📝',
  },
  {
    id: 'improve_hooks',
    title: 'Improve Hooks',
    description: 'Better video openings',
    icon: '🎣',
  },
  {
    id: 'optimize_title',
    title: 'Optimize Title',
    description: 'SEO-friendly titles',
    icon: '🎯',
  },
  {
    id: 'get_ideas',
    title: 'Get Ideas',
    description: 'Content suggestions',
    icon: '💡',
  },
]

export default function QuickActions() {
  const { sendQuickAction, isLoading } = useChat()
  const [selectedAction, setSelectedAction] = useState<(typeof quickActions)[0] | null>(null)

  const handleActionClick = (action: typeof quickActions[0]) => {
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
      <div className="grid grid-cols-2 gap-3">
        {quickActions.map((action) => (
          <Button
            key={action.id}
            onClick={() => handleActionClick(action)}
            disabled={isLoading}
            variant="secondary"
            size="sm"
            className="flex flex-col items-center gap-2 h-auto py-3 px-2 text-center"
          >
            <span className="text-lg">{action.icon}</span>
            <div>
              <div className="text-xs font-medium">{action.title}</div>
              <div className="text-xs opacity-70">{action.description}</div>
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