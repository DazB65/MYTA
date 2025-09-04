/**
 * Security utilities for input sanitization and XSS protection
 */

// HTML entities for encoding
const HTML_ENTITIES: Record<string, string> = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#x27;',
  '/': '&#x2F;',
  '`': '&#x60;',
  '=': '&#x3D;'
}

/**
 * Escape HTML entities to prevent XSS attacks
 */
export function escapeHtml(text: string): string {
  if (typeof text !== 'string') {
    return String(text)
  }
  
  return text.replace(/[&<>"'`=\/]/g, (match) => HTML_ENTITIES[match] || match)
}

/**
 * Sanitize user input by removing potentially dangerous characters
 */
export function sanitizeInput(input: string, options: {
  allowHtml?: boolean
  maxLength?: number
  allowedChars?: RegExp
} = {}): string {
  if (typeof input !== 'string') {
    return ''
  }

  let sanitized = input.trim()

  // Apply length limit
  if (options.maxLength && sanitized.length > options.maxLength) {
    sanitized = sanitized.substring(0, options.maxLength)
  }

  // Remove or escape HTML if not allowed
  if (!options.allowHtml) {
    sanitized = escapeHtml(sanitized)
  }

  // Apply character whitelist if provided
  if (options.allowedChars) {
    sanitized = sanitized.replace(options.allowedChars, '')
  }

  return sanitized
}

/**
 * Validate email format
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Validate password strength
 */
export function validatePassword(password: string): {
  isValid: boolean
  score: number
  feedback: string[]
} {
  const feedback: string[] = []
  let score = 0

  if (password.length < 8) {
    feedback.push('Password must be at least 8 characters long')
  } else {
    score += 1
  }

  if (!/[A-Z]/.test(password)) {
    feedback.push('Password must contain at least one uppercase letter')
  } else {
    score += 1
  }

  if (!/[a-z]/.test(password)) {
    feedback.push('Password must contain at least one lowercase letter')
  } else {
    score += 1
  }

  if (!/\d/.test(password)) {
    feedback.push('Password must contain at least one number')
  } else {
    score += 1
  }

  if (!/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(password)) {
    feedback.push('Password must contain at least one special character')
  } else {
    score += 1
  }

  return {
    isValid: score >= 4 && password.length >= 8,
    score,
    feedback
  }
}

/**
 * Sanitize URL to prevent javascript: and data: schemes
 */
export function sanitizeUrl(url: string): string {
  if (typeof url !== 'string') {
    return ''
  }

  const trimmed = url.trim().toLowerCase()
  
  // Block dangerous schemes
  if (trimmed.startsWith('javascript:') || 
      trimmed.startsWith('data:') || 
      trimmed.startsWith('vbscript:') ||
      trimmed.startsWith('file:')) {
    return ''
  }

  return url.trim()
}

/**
 * Remove potentially dangerous HTML tags and attributes
 */
export function sanitizeHtml(html: string): string {
  if (typeof html !== 'string') {
    return ''
  }

  // Remove script tags and their content
  html = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
  
  // Remove dangerous attributes
  html = html.replace(/\s*on\w+\s*=\s*["'][^"']*["']/gi, '') // onclick, onload, etc.
  html = html.replace(/\s*javascript\s*:/gi, '')
  html = html.replace(/\s*vbscript\s*:/gi, '')
  html = html.replace(/\s*data\s*:/gi, '')
  
  // Remove dangerous tags
  const dangerousTags = ['script', 'object', 'embed', 'link', 'style', 'meta', 'iframe']
  dangerousTags.forEach(tag => {
    const regex = new RegExp(`<${tag}\\b[^<]*(?:(?!<\\/${tag}>)<[^<]*)*<\\/${tag}>`, 'gi')
    html = html.replace(regex, '')
  })

  return html
}

/**
 * Validate and sanitize form data
 */
export function validateFormData(data: Record<string, any>, rules: Record<string, {
  required?: boolean
  type?: 'string' | 'email' | 'number' | 'url'
  minLength?: number
  maxLength?: number
  pattern?: RegExp
  sanitize?: boolean
}>): {
  isValid: boolean
  errors: Record<string, string>
  sanitizedData: Record<string, any>
} {
  const errors: Record<string, string> = {}
  const sanitizedData: Record<string, any> = {}

  for (const [field, rule] of Object.entries(rules)) {
    const value = data[field]

    // Check required fields
    if (rule.required && (!value || (typeof value === 'string' && !value.trim()))) {
      errors[field] = `${field} is required`
      continue
    }

    // Skip validation for optional empty fields
    if (!value && !rule.required) {
      sanitizedData[field] = value
      continue
    }

    // Type validation
    switch (rule.type) {
      case 'email':
        if (!isValidEmail(value)) {
          errors[field] = 'Please enter a valid email address'
        }
        break
      case 'number':
        if (isNaN(Number(value))) {
          errors[field] = `${field} must be a number`
        }
        break
      case 'url':
        try {
          new URL(value)
        } catch {
          errors[field] = 'Please enter a valid URL'
        }
        break
    }

    // Length validation
    if (rule.minLength && value.length < rule.minLength) {
      errors[field] = `${field} must be at least ${rule.minLength} characters long`
    }
    if (rule.maxLength && value.length > rule.maxLength) {
      errors[field] = `${field} must be no more than ${rule.maxLength} characters long`
    }

    // Pattern validation
    if (rule.pattern && !rule.pattern.test(value)) {
      errors[field] = `${field} format is invalid`
    }

    // Sanitize if requested
    if (rule.sanitize && typeof value === 'string') {
      sanitizedData[field] = sanitizeInput(value, { maxLength: rule.maxLength })
    } else {
      sanitizedData[field] = value
    }
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
    sanitizedData
  }
}

/**
 * Generate a secure random string for CSRF tokens
 */
export function generateSecureToken(length: number = 32): string {
  if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
    const array = new Uint8Array(length)
    crypto.getRandomValues(array)
    return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('')
  }
  
  // Fallback for environments without crypto.getRandomValues
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

/**
 * Safe JSON parse that handles potential XSS in JSON strings
 */
export function safeJsonParse<T = any>(jsonString: string): T | null {
  try {
    // First sanitize the string to remove potential XSS
    const sanitized = sanitizeInput(jsonString, { allowHtml: false })
    return JSON.parse(sanitized)
  } catch {
    return null
  }
}

/**
 * Content Security Policy helper
 */
export function generateCSPNonce(): string {
  return generateSecureToken(16)
}
