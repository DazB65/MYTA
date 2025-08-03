/**
 * Input Validation Utilities
 * Provides comprehensive input validation and sanitization
 */

// Validation patterns
const patterns = {
  email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  url: /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/,
  alphanumeric: /^[a-zA-Z0-9]+$/,
  alphanumericWithSpaces: /^[a-zA-Z0-9\s]+$/,
  youtubeChannelId: /^UC[a-zA-Z0-9_-]{22}$/,
  youtubeVideoId: /^[a-zA-Z0-9_-]{11}$/
};

// Validation rules
export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  custom?: (value: any) => string | null;
}

export interface ValidationRules {
  [field: string]: ValidationRule;
}

export interface ValidationErrors {
  [field: string]: string;
}

/**
 * Sanitize HTML content to prevent XSS
 */
export function sanitizeHtml(input: string): string {
  if (typeof input !== 'string') return '';
  
  // Remove script tags and their content
  let sanitized = input.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
  
  // Remove potentially dangerous HTML tags
  const dangerousTags = [
    'script', 'object', 'embed', 'iframe', 'frame', 'frameset',
    'applet', 'base', 'link', 'meta', 'style', 'form', 'input',
    'button', 'textarea', 'select', 'option'
  ];
  
  dangerousTags.forEach(tag => {
    const regex = new RegExp(`<${tag}\\b[^>]*>.*?<\\/${tag}>`, 'gi');
    sanitized = sanitized.replace(regex, '');
    const selfClosing = new RegExp(`<${tag}\\b[^>]*\\/>`, 'gi');
    sanitized = sanitized.replace(selfClosing, '');
  });
  
  // Remove javascript: and data: URLs
  sanitized = sanitized.replace(/javascript:/gi, '');
  sanitized = sanitized.replace(/data:/gi, '');
  
  // Remove event handlers
  sanitized = sanitized.replace(/on\w+\s*=\s*["'][^"']*["']/gi, '');
  sanitized = sanitized.replace(/on\w+\s*=\s*[^>\s]+/gi, '');
  
  return sanitized.trim();
}

/**
 * Sanitize user input for safe display
 */
export function sanitizeInput(input: string, maxLength: number = 1000): string {
  if (typeof input !== 'string') return '';
  
  // Truncate if too long
  let sanitized = input.slice(0, maxLength);
  
  // Remove potentially dangerous characters
  sanitized = sanitized.replace(/[<>]/g, '');
  
  // Normalize whitespace
  sanitized = sanitized.replace(/\s+/g, ' ').trim();
  
  return sanitized;
}

/**
 * Validate email address
 */
export function validateEmail(email: string): string | null {
  if (!email) return 'Email is required';
  if (!patterns.email.test(email)) return 'Invalid email format';
  if (email.length > 254) return 'Email too long';
  return null;
}

/**
 * Validate URL
 */
export function validateUrl(url: string, required: boolean = false): string | null {
  if (!url) return required ? 'URL is required' : null;
  if (!patterns.url.test(url)) return 'Invalid URL format';
  if (url.length > 2048) return 'URL too long';
  return null;
}

/**
 * Validate YouTube channel ID
 */
export function validateYouTubeChannelId(channelId: string): string | null {
  if (!channelId) return 'Channel ID is required';
  if (!patterns.youtubeChannelId.test(channelId)) {
    return 'Invalid YouTube channel ID format';
  }
  return null;
}

/**
 * Validate YouTube video ID
 */
export function validateYouTubeVideoId(videoId: string): string | null {
  if (!videoId) return 'Video ID is required';
  if (!patterns.youtubeVideoId.test(videoId)) {
    return 'Invalid YouTube video ID format';
  }
  return null;
}

/**
 * Validate numeric input
 */
export function validateNumber(
  value: any, 
  min?: number, 
  max?: number, 
  required: boolean = false
): string | null {
  if (value === '' || value === null || value === undefined) {
    return required ? 'This field is required' : null;
  }
  
  const num = Number(value);
  if (isNaN(num)) return 'Must be a valid number';
  if (min !== undefined && num < min) return `Must be at least ${min}`;
  if (max !== undefined && num > max) return `Must be no more than ${max}`;
  
  return null;
}

/**
 * Validate text input
 */
export function validateText(
  value: string,
  minLength?: number,
  maxLength?: number,
  required: boolean = false,
  pattern?: RegExp
): string | null {
  if (!value || value.trim() === '') {
    return required ? 'This field is required' : null;
  }
  
  const sanitized = sanitizeInput(value, maxLength || 10000);
  
  if (minLength && sanitized.length < minLength) {
    return `Must be at least ${minLength} characters`;
  }
  
  if (maxLength && sanitized.length > maxLength) {
    return `Must be no more than ${maxLength} characters`;
  }
  
  if (pattern && !pattern.test(sanitized)) {
    return 'Invalid format';
  }
  
  return null;
}

/**
 * Validate form data against rules
 */
export function validateForm(data: Record<string, any>, rules: ValidationRules): ValidationErrors {
  const errors: ValidationErrors = {};
  
  Object.keys(rules).forEach(field => {
    const rule = rules[field];
    const value = data[field];
    
    // Check required
    if (rule.required && (!value || (typeof value === 'string' && value.trim() === ''))) {
      errors[field] = 'This field is required';
      return;
    }
    
    // Skip validation if field is empty and not required
    if (!value && !rule.required) return;
    
    // Check length
    if (typeof value === 'string') {
      if (rule.minLength && value.length < rule.minLength) {
        errors[field] = `Must be at least ${rule.minLength} characters`;
        return;
      }
      
      if (rule.maxLength && value.length > rule.maxLength) {
        errors[field] = `Must be no more than ${rule.maxLength} characters`;
        return;
      }
    }
    
    // Check pattern
    if (rule.pattern && typeof value === 'string' && !rule.pattern.test(value)) {
      errors[field] = 'Invalid format';
      return;
    }
    
    // Check custom validation
    if (rule.custom) {
      const customError = rule.custom(value);
      if (customError) {
        errors[field] = customError;
        return;
      }
    }
  });
  
  return errors;
}

/**
 * Channel info validation rules
 */
export const channelInfoRules: ValidationRules = {
  name: {
    required: true,
    minLength: 1,
    maxLength: 100,
    custom: (value) => {
      if (typeof value !== 'string') return 'Name must be text';
      const sanitized = sanitizeInput(value);
      if (sanitized !== value) return 'Name contains invalid characters';
      return null;
    }
  },
  niche: {
    required: true,
    minLength: 2,
    maxLength: 50
  },
  content_type: {
    required: true,
    minLength: 2,
    maxLength: 50
  },
  subscriber_count: {
    custom: (value) => validateNumber(value, 0, 1000000000)
  },
  avg_view_count: {
    custom: (value) => validateNumber(value, 0, 1000000000)
  },
  ctr: {
    custom: (value) => validateNumber(value, 0, 100)
  },
  retention: {
    custom: (value) => validateNumber(value, 0, 100)
  }
};

/**
 * Escape HTML entities
 */
export function escapeHtml(text: string): string {
  const map: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;'
  };
  
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

/**
 * Check if string is safe for display
 */
export function isSafeText(text: string): boolean {
  if (typeof text !== 'string') return false;
  
  // Check for potentially dangerous patterns
  const dangerousPatterns = [
    /<script/i,
    /javascript:/i,
    /data:/i,
    /on\w+\s*=/i,
    /<iframe/i,
    /<object/i,
    /<embed/i
  ];
  
  return !dangerousPatterns.some(pattern => pattern.test(text));
}

export default {
  sanitizeHtml,
  sanitizeInput,
  validateEmail,
  validateUrl,
  validateYouTubeChannelId,
  validateYouTubeVideoId,
  validateNumber,
  validateText,
  validateForm,
  channelInfoRules,
  escapeHtml,
  isSafeText
};