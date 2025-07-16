export const formatNumber = (num: number): string => {
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1)}M`
  } else if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K`
  }
  return num.toLocaleString()
}

export const formatTimeAgo = (date: string): string => {
  const now = new Date()
  const target = new Date(date)
  const seconds = Math.floor((now.getTime() - target.getTime()) / 1000)
  
  if (seconds < 60) {
    return 'just now'
  }
  
  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) {
    return `${minutes}m ago`
  }
  
  const hours = Math.floor(minutes / 60)
  if (hours < 24) {
    return `${hours}h ago`
  }
  
  const days = Math.floor(hours / 24)
  if (days < 30) {
    return `${days}d ago`
  }
  
  const months = Math.floor(days / 30)
  if (months < 12) {
    return `${months}mo ago`
  }
  
  const years = Math.floor(months / 12)
  return `${years}y ago`
}

export const formatDuration = (seconds: number): string => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const remainingSeconds = seconds % 60

  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
  }
  
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}