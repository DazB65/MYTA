import { type ClassValue, clsx } from 'clsx'

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs)
}

export function formatNumber(num: number): string {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

export function getPerformanceLevel(value: number, thresholds: { low: number; average: number; good: number }): string {
  if (value < thresholds.low) return 'low'
  if (value < thresholds.average) return 'average'
  if (value < thresholds.good) return 'good'
  return 'excellent'
}

export function getSubscriberTier(count: number): string {
  if (count < 1000) return 'new'
  if (count < 10000) return 'growing'
  if (count < 100000) return 'established'
  return 'large'
}

export function downloadFile(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout
  return (...args: Parameters<T>) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

export function getInsightIcon(type: string): string {
  const iconMap: Record<string, string> = {
    performance: '📊',
    trending: '🔥',
    growth: '📈',
    strategy: '💡',
    timing: '⏰',
    revenue: '💰',
    monetization: '💳',
  }
  return iconMap[type] || '💡'
}