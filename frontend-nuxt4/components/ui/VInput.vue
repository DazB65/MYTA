<template>
  <div class="input-wrapper">
    <label v-if="label" :for="inputId" class="input-label">
      {{ label }}
      <span v-if="required" class="text-error">*</span>
    </label>
    
    <div class="input-container">
      <div v-if="$slots['icon-left']" class="input-icon input-icon-left">
        <slot name="icon-left" />
      </div>
      
      <input
        :id="inputId"
        :class="inputClasses"
        :type="type"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :value="modelValue"
        v-bind="$attrs"
        @input="handleInput"
        @focus="handleFocus"
        @blur="handleBlur"
      />
      
      <div v-if="$slots['icon-right']" class="input-icon input-icon-right">
        <slot name="icon-right" />
      </div>
    </div>
    
    <div v-if="error || hint" class="input-message">
      <span v-if="error" class="input-error">{{ error }}</span>
      <span v-else-if="hint" class="input-hint">{{ hint }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

interface Props {
  modelValue?: string | number
  type?: 'text' | 'email' | 'password' | 'number' | 'search' | 'tel' | 'url'
  label?: string
  placeholder?: string
  disabled?: boolean
  required?: boolean
  error?: string
  hint?: string
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false,
  required: false,
  size: 'md',
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  focus: [event: FocusEvent]
  blur: [event: FocusEvent]
}>()

const isFocused = ref(false)
const inputId = computed(() => `input-${Math.random().toString(36).substr(2, 9)}`)

const inputClasses = computed(() => [
  'input',
  {
    'input-sm': props.size === 'sm',
    'input-lg': props.size === 'lg',
    'input-error': props.error,
    'input-disabled': props.disabled,
    'pl-10': !!$slots['icon-left'],
    'pr-10': !!$slots['icon-right'],
  },
])

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}

const handleFocus = (event: FocusEvent) => {
  isFocused.value = true
  emit('focus', event)
}

const handleBlur = (event: FocusEvent) => {
  isFocused.value = false
  emit('blur', event)
}
</script>

<style scoped>
.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.input-label {
  font-size: 0.875rem;
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
}

.input-container {
  position: relative;
}

.input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background-color: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  color: var(--color-text-primary);
  font-size: 0.875rem;
  transition: var(--transition-normal);
}

.input:focus {
  outline: none;
  border-color: var(--color-brand-primary);
  box-shadow: 0 0 0 3px rgba(228, 117, 163, 0.1);
}

.input::placeholder {
  color: var(--color-text-muted);
}

.input-sm {
  padding: var(--space-2) var(--space-3);
  font-size: 0.75rem;
}

.input-lg {
  padding: var(--space-4) var(--space-5);
  font-size: 1rem;
}

.input-error {
  border-color: var(--color-error);
}

.input-error:focus {
  border-color: var(--color-error);
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.input-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-icon {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-muted);
  pointer-events: none;
}

.input-icon-left {
  left: var(--space-3);
}

.input-icon-right {
  right: var(--space-3);
}

.input-message {
  font-size: 0.75rem;
  line-height: 1rem;
}

.input-error {
  color: var(--color-error);
}

.input-hint {
  color: var(--color-text-muted);
}
</style>
