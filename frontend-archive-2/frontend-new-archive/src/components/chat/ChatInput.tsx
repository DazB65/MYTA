import { useState, KeyboardEvent } from 'react'
import { Send } from 'lucide-react'
import Button from '@/components/common/Button'
import { cn } from '@/utils'

interface ChatInputProps {
  onSendMessage: (message: string) => void
  disabled?: boolean
  placeholder?: string
  className?: string
  onClick?: () => void
  readOnly?: boolean
}

export default function ChatInput({ 
  onSendMessage, 
  disabled = false, 
  placeholder = "Ask me anything about content creation...",
  className,
  onClick,
  readOnly = false
}: ChatInputProps) {
  const [message, setMessage] = useState('')

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSendMessage(message.trim())
      setMessage('')
    }
  }

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="relative">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        onClick={onClick}
        placeholder={placeholder}
        disabled={disabled}
        readOnly={readOnly}
        className={cn(
          'w-full pr-12 pl-4 py-3 rounded-full border-none',
          'bg-white/10 text-white placeholder-white/60',
          'focus:outline-none focus:ring-2 focus:ring-primary-500',
          disabled && 'opacity-50 cursor-not-allowed',
          (onClick || readOnly) && 'cursor-pointer',
          className
        )}
      />
      
      <Button
        onClick={handleSend}
        disabled={disabled || !message.trim()}
        variant="ghost"
        size="sm"
        className="absolute right-2 top-1/2 -translate-y-1/2 p-2 h-8 w-8 rounded-full"
      >
        <Send className="w-4 h-4" />
      </Button>
    </div>
  )
}