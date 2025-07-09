import { HTMLAttributes } from 'react'
import { cn } from '@/utils'

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
}

export default function Card({ className, children, ...props }: CardProps) {
  return (
    <div
      className={cn('card', className)}
      {...props}
    >
      {children}
    </div>
  )
}