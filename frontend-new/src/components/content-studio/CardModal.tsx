import { ContentCard, CardStatus } from '@/types/contentStudio'

interface CardModalProps {
  isOpen: boolean
  onClose: () => void
  card?: ContentCard | null
  onSubmit: (card: any) => void
  defaultStatus?: CardStatus
}

export default function CardModal({ isOpen, onClose, card, onSubmit }: CardModalProps) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 p-6 rounded-lg max-w-md w-full mx-4">
        <h2 className="text-xl font-bold mb-4 text-white">
          {card ? 'Edit Card' : 'Create Card'}
        </h2>
        <p className="text-gray-300 mb-4">Content Studio modal placeholder</p>
        <div className="flex gap-2 justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            Cancel
          </button>
          <button
            onClick={() => {
              if (card) {
                onSubmit(card)
              }
              onClose()
            }}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  )
}