export const getGradeColor = (grade: string): string => {
  switch (grade) {
    case 'A+':
    case 'A':
      return 'text-green-400'
    case 'B+':
    case 'B':
      return 'text-blue-400'
    case 'C+':
    case 'C':
      return 'text-yellow-400'
    case 'D+':
    case 'D':
      return 'text-orange-400'
    case 'F':
      return 'text-red-400'
    default:
      return 'text-gray-400'
  }
}

export const getScoreColor = (score: number): string => {
  if (score >= 90) return 'text-green-400'
  if (score >= 80) return 'text-blue-400'
  if (score >= 70) return 'text-yellow-400'
  if (score >= 60) return 'text-orange-400'
  return 'text-red-400'
}

export const getPerformanceColor = (performance: 'good' | 'medium' | 'poor' | 'unknown'): string => {
  switch (performance) {
    case 'good':
      return 'text-green-400'
    case 'medium':
      return 'text-yellow-400'
    case 'poor':
      return 'text-red-400'
    default:
      return 'text-gray-400'
  }
}

export const getMetricTrendColor = (trend: number): string => {
  if (trend > 0) return 'text-green-400'
  if (trend < 0) return 'text-red-400'
  return 'text-gray-400'
}