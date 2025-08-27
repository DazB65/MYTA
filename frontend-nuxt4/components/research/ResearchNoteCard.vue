<template>
  <div
    class="research-note-card"
    :style="{
      transform: `translate(${position.x}px, ${position.y}px)`,
      zIndex: isDragging ? 1000 : 1
    }"
    @mousedown="startDrag"
    :class="{
      'dragging': isDragging,
      [getNoteTypeClass(note)]: true
    }"
  >
    <!-- Note Header -->
    <div class="note-header">
      <div class="note-type-indicator">
        <div class="note-icon">
          <component :is="getNoteIcon(note)" class="h-4 w-4" />
        </div>
        <span class="note-type-label">{{ getNoteTypeLabel(note) }}</span>
      </div>
      <div class="note-actions">
        <button class="action-btn" @click="editNote" title="Edit note">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
        </button>
        <button class="action-btn" @click="removeNote" title="Remove note">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Note Content -->
    <div class="note-content">
      <div v-if="isTemplateNote(note)" class="template-content">
        <h4 class="template-title">{{ getTemplateTitle(note) }}</h4>
        <p class="template-goal">{{ getTemplateGoal(note) }}</p>
        <div class="template-steps">
          <h5 class="steps-title">Research Steps:</h5>
          <ol class="steps-list">
            <li v-for="(step, index) in getTemplateSteps(note)" :key="index" class="step-item">
              {{ step }}
            </li>
          </ol>
        </div>
      </div>
      <div v-else class="regular-content">
        <p class="note-text">{{ note.content }}</p>
      </div>
    </div>

    <!-- Note Footer -->
    <div class="note-footer">
      <span class="note-timestamp">{{ formatTime(note.createdAt) }}</span>
      <div class="note-status">
        <span class="status-dot"></span>
        <span class="status-text">Active</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { ResearchNote } from '../../types/research'

interface Props {
  note: ResearchNote
  position: { x: number, y: number }
}

interface Emits {
  (e: 'move', noteId: string, position: { x: number, y: number }): void
  (e: 'edit', note: ResearchNote): void
  (e: 'remove', noteId: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Drag functionality
const isDragging = ref(false)
const dragOffset = ref({ x: 0, y: 0 })

const startDrag = (event: MouseEvent) => {
  if (event.target instanceof HTMLButtonElement) return
  
  isDragging.value = true
  dragOffset.value = {
    x: event.clientX - props.position.x,
    y: event.clientY - props.position.y
  }

  const handleMouseMove = (e: MouseEvent) => {
    if (!isDragging.value) return
    
    const newPosition = {
      x: e.clientX - dragOffset.value.x,
      y: e.clientY - dragOffset.value.y
    }
    
    emit('move', props.note.id, newPosition)
  }

  const handleMouseUp = () => {
    isDragging.value = false
    document.removeEventListener('mousemove', handleMouseMove)
    document.removeEventListener('mouseup', handleMouseUp)
  }

  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
}

// Note actions
const editNote = () => {
  emit('edit', props.note)
}

const removeNote = () => {
  emit('remove', props.note.id)
}

const formatTime = (date: Date) => {
  return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Note type detection and styling
const isTemplateNote = (note: any) => {
  return note.content.includes('Goal:') && note.content.includes('Steps:')
}

const isGettingStartedNote = (note: any) => {
  return note.content.includes('Getting Started:')
}

const getNoteTypeClass = (note: any) => {
  if (isTemplateNote(note)) return 'template-note'
  if (isGettingStartedNote(note)) return 'getting-started-note'
  return 'regular-note'
}

const getNoteTypeLabel = (note: any) => {
  if (isTemplateNote(note)) return 'Template'
  if (isGettingStartedNote(note)) return 'Guide'
  return 'Note'
}

const getNoteIcon = (note: any) => {
  // Return SVG component based on note type
  return 'svg'
}

const getTemplateTitle = (note: any) => {
  const lines = note.content.split('\n')
  return lines[0] || 'Template'
}

const getTemplateGoal = (note: any) => {
  const goalMatch = note.content.match(/Goal: (.+?)(?=\n|$)/)
  return goalMatch ? goalMatch[1] : ''
}

const getTemplateSteps = (note: any) => {
  const stepsMatch = note.content.match(/Steps:\n([\s\S]+)/)
  if (!stepsMatch) return []

  return stepsMatch[1]
    .split('\n')
    .filter(line => line.trim().match(/^\d+\./))
    .map(line => line.replace(/^\d+\.\s*/, '').trim())
}
</script>

<style scoped>
.research-note-card {
  position: absolute;
  width: 320px;
  min-height: 200px;
  background: #1F2937;
  border: 1px solid #374151;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  cursor: move;
  user-select: none;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
}

.research-note-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  border-color: #4B5563;
}

.research-note-card.dragging {
  transform: rotate(1deg);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

/* Note Type Specific Styling */
.template-note {
  border-left: 4px solid #3B82F6;
  background: linear-gradient(135deg, #1F2937 0%, #1E3A8A 100%);
}

.getting-started-note {
  border-left: 4px solid #F59E0B;
  background: linear-gradient(135deg, #1F2937 0%, #92400E 100%);
}

.regular-note {
  border-left: 4px solid #10B981;
  background: linear-gradient(135deg, #1F2937 0%, #065F46 100%);
}

.note-header {
  padding: 16px;
  border-bottom: 1px solid #374151;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.note-type-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.note-icon {
  width: 24px;
  height: 24px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #E5E7EB;
}

.note-type-label {
  font-size: 12px;
  font-weight: 600;
  color: #9CA3AF;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.note-actions {
  display: flex;
  gap: 6px;
}

.action-btn {
  padding: 6px;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  cursor: pointer;
  color: #9CA3AF;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #E5E7EB;
}

.note-content {
  padding: 16px;
  flex: 1;
  overflow-y: auto;
}

/* Template Content Styling */
.template-content {
  color: #E5E7EB;
}

.template-title {
  font-size: 18px;
  font-weight: 700;
  color: #F3F4F6;
  margin: 0 0 12px 0;
}

.template-goal {
  font-size: 14px;
  color: #9CA3AF;
  margin: 0 0 16px 0;
  font-style: italic;
}

.template-steps {
  margin-top: 16px;
}

.steps-title {
  font-size: 14px;
  font-weight: 600;
  color: #F3F4F6;
  margin: 0 0 12px 0;
}

.steps-list {
  margin: 0;
  padding-left: 20px;
  color: #D1D5DB;
}

.step-item {
  margin-bottom: 8px;
  font-size: 13px;
  line-height: 1.5;
}

/* Regular Content Styling */
.regular-content {
  color: #E5E7EB;
}

.note-text {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: #D1D5DB;
  white-space: pre-wrap;
}

.note-footer {
  padding: 12px 16px;
  border-top: 1px solid #374151;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 0 0 12px 12px;
}

.note-timestamp {
  font-size: 11px;
  color: #6B7280;
  font-weight: 500;
}

.note-status {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  width: 6px;
  height: 6px;
  background: #10B981;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.status-text {
  font-size: 11px;
  color: #6B7280;
  font-weight: 500;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
