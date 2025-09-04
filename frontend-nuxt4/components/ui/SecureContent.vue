<template>
  <div class="secure-content">
    <!-- Safe text content (escaped) -->
    <div v-if="type === 'text'" class="text-content">
      {{ escapedContent }}
    </div>
    
    <!-- Safe HTML content (sanitized) -->
    <div 
      v-else-if="type === 'html'" 
      class="html-content"
      v-html="sanitizedHtml"
    />
    
    <!-- Markdown content (parsed and sanitized) -->
    <div 
      v-else-if="type === 'markdown'" 
      class="markdown-content"
      v-html="sanitizedMarkdown"
    />
    
    <!-- URL content (validated) -->
    <a 
      v-else-if="type === 'url'" 
      :href="sanitizedUrl"
      class="url-content"
      target="_blank"
      rel="noopener noreferrer"
    >
      {{ displayUrl }}
    </a>
    
    <!-- Fallback for unknown types -->
    <div v-else class="fallback-content">
      {{ escapedContent }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { escapeHtml, sanitizeHtml, sanitizeUrl } from '~/utils/security'

interface Props {
  content: string
  type?: 'text' | 'html' | 'markdown' | 'url'
  allowedTags?: string[]
  maxLength?: number
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  allowedTags: () => ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li'],
  maxLength: 10000
})

// Escaped text content for safe display
const escapedContent = computed(() => {
  if (!props.content) return ''
  
  let content = props.content
  
  // Apply length limit
  if (props.maxLength && content.length > props.maxLength) {
    content = content.substring(0, props.maxLength) + '...'
  }
  
  return escapeHtml(content)
})

// Sanitized HTML content
const sanitizedHtml = computed(() => {
  if (!props.content) return ''
  
  let content = props.content
  
  // Apply length limit
  if (props.maxLength && content.length > props.maxLength) {
    content = content.substring(0, props.maxLength) + '...'
  }
  
  // Sanitize HTML to remove dangerous elements
  return sanitizeHtml(content)
})

// Sanitized markdown content (basic implementation)
const sanitizedMarkdown = computed(() => {
  if (!props.content) return ''
  
  let content = props.content
  
  // Apply length limit
  if (props.maxLength && content.length > props.maxLength) {
    content = content.substring(0, props.maxLength) + '...'
  }
  
  // Basic markdown to HTML conversion (you might want to use a proper markdown library)
  content = content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
    .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
    .replace(/\n/g, '<br>') // Line breaks
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, text, url) => {
      const safeUrl = sanitizeUrl(url)
      const safeText = escapeHtml(text)
      return safeUrl ? `<a href="${safeUrl}" target="_blank" rel="noopener noreferrer">${safeText}</a>` : safeText
    }) // Links
  
  // Sanitize the resulting HTML
  return sanitizeHtml(content)
})

// Sanitized URL
const sanitizedUrl = computed(() => {
  if (!props.content) return ''
  return sanitizeUrl(props.content)
})

// Display URL (truncated for UI)
const displayUrl = computed(() => {
  if (!props.content) return ''
  
  const url = props.content
  if (url.length > 50) {
    return url.substring(0, 47) + '...'
  }
  return url
})
</script>

<style scoped>
.secure-content {
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.text-content {
  white-space: pre-wrap;
}

.html-content {
  /* Styles for HTML content */
}

.html-content :deep(a) {
  color: var(--color-brand-primary);
  text-decoration: none;
}

.html-content :deep(a:hover) {
  text-decoration: underline;
}

.markdown-content {
  /* Styles for markdown content */
}

.markdown-content :deep(strong) {
  font-weight: 600;
}

.markdown-content :deep(em) {
  font-style: italic;
}

.markdown-content :deep(a) {
  color: var(--color-brand-primary);
  text-decoration: none;
}

.markdown-content :deep(a:hover) {
  text-decoration: underline;
}

.url-content {
  color: var(--color-brand-primary);
  text-decoration: none;
  word-break: break-all;
}

.url-content:hover {
  text-decoration: underline;
}

.fallback-content {
  color: var(--color-text-muted);
  font-style: italic;
}

/* Security: Prevent CSS injection */
.secure-content :deep(*) {
  max-width: 100%;
}

/* Prevent potential CSS-based attacks */
.secure-content :deep(style),
.secure-content :deep(link),
.secure-content :deep(script) {
  display: none !important;
}
</style>
