<template>
  <div class="ai-research-center">
    <!-- Header -->
    <div class="research-header">
      <div class="header-content">
        <div class="assistant-info">
          <img src="/agents/agent-2.png" alt="Research Assistant" class="assistant-avatar" />
          <div class="assistant-details">
            <h2 class="assistant-name">AI Research Assistant</h2>
            <p class="assistant-status">
              <span class="status-dot"></span>
              Ready to research • Powered by Rupert
            </p>
          </div>
        </div>
        <div class="research-stats">
          <div class="stat-item">
            <span class="stat-number">{{ completedResearch }}</span>
            <span class="stat-label">Research Done</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ insightsGenerated }}</span>
            <span class="stat-label">Insights Found</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions (One-Click Research) -->
    <div class="quick-actions-section">
      <h3 class="section-title">⚡ Quick Research</h3>
      <div class="quick-actions-grid">
        <button 
          v-for="action in quickActions" 
          :key="action.id"
          @click="runQuickResearch(action)"
          :disabled="isResearching"
          class="quick-action-btn"
          :class="action.color"
        >
          <div class="action-icon">
            <component :is="action.icon" class="h-6 w-6" />
          </div>
          <div class="action-content">
            <h4 class="action-title">{{ action.title }}</h4>
            <p class="action-description">{{ action.description }}</p>
          </div>
          <div class="action-arrow">
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </div>
        </button>
      </div>
    </div>

    <!-- Smart Prompt (Custom Research) -->
    <div class="smart-prompt-section">
      <h3 class="section-title">🎯 Custom Research</h3>
      <div class="prompt-container">
        <div class="prompt-input-wrapper">
          <textarea
            v-model="customPrompt"
            @keydown.enter.meta="runCustomResearch"
            @keydown.enter.ctrl="runCustomResearch"
            placeholder="Ask me anything about your YouTube research... 

Examples:
• Find trending topics in my niche for next month
• Analyze my top 3 competitors' recent content strategy  
• What viral video formats are working in productivity content?
• Research SEO opportunities for 'morning routine' videos"
            class="prompt-input"
            rows="4"
          ></textarea>
          <div class="prompt-actions">
            <div class="prompt-suggestions">
              <button 
                v-for="suggestion in promptSuggestions" 
                :key="suggestion"
                @click="customPrompt = suggestion"
                class="suggestion-chip"
              >
                {{ suggestion }}
              </button>
            </div>
            <button 
              @click="runCustomResearch"
              :disabled="!customPrompt.trim() || isResearching"
              class="research-btn"
            >
              <svg v-if="isResearching" class="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
              {{ isResearching ? 'Researching...' : 'Research' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Research Results -->
    <div v-if="researchResults.length > 0" class="results-section">
      <h3 class="section-title">📊 Research Results</h3>
      <div class="results-grid">
        <div 
          v-for="result in researchResults" 
          :key="result.id"
          class="result-card"
        >
          <div class="result-header">
            <div class="result-type">{{ result.type }}</div>
            <div class="result-confidence">{{ result.confidence }}% confidence</div>
          </div>
          <h4 class="result-title">{{ result.title }}</h4>
          <p class="result-summary">{{ result.summary }}</p>
          <div class="result-insights">
            <div v-for="insight in result.insights" :key="insight" class="insight-item">
              <span class="insight-bullet">•</span>
              <span class="insight-text">{{ insight }}</span>
            </div>
          </div>
          <div class="result-actions">
            <button @click="exploreResult(result)" class="explore-btn">
              Explore Further
            </button>
            <button @click="exportResult(result)" class="export-btn">
              Export to Studio
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Conversational Chat -->
    <div class="chat-section">
      <h3 class="section-title">💬 Research Conversation</h3>
      <div class="chat-container">
        <div class="chat-messages" ref="chatMessages">
          <div v-for="message in chatHistory" :key="message.id" class="chat-message" :class="message.type">
            <div v-if="message.type === 'ai'" class="message-avatar">
              <img src="/agents/agent-2.png" alt="AI" class="avatar-img" />
            </div>
            <div class="message-content">
              <div class="message-text">{{ message.text }}</div>
              <div class="message-time">{{ formatTime(message.timestamp) }}</div>
            </div>
          </div>
          <div v-if="isTyping" class="chat-message ai typing">
            <div class="message-avatar">
              <img src="/agents/agent-2.png" alt="AI" class="avatar-img" />
            </div>
            <div class="message-content">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
        <div class="chat-input-container">
          <input
            v-model="chatMessage"
            @keydown.enter="sendChatMessage"
            placeholder="Ask follow-up questions or dive deeper into any research..."
            class="chat-input"
          />
          <button 
            @click="sendChatMessage"
            :disabled="!chatMessage.trim() || isTyping"
            class="send-btn"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick, ref } from 'vue'

// Reactive data
const isResearching = ref(false)
const isTyping = ref(false)
const customPrompt = ref('')
const chatMessage = ref('')
const completedResearch = ref(12)
const insightsGenerated = ref(47)
const researchResults = ref([])
const chatHistory = ref([
  {
    id: 1,
    type: 'ai',
    text: "Hi! I'm your AI Research Assistant. I can help you with competitor analysis, trend research, viral content insights, and much more. What would you like to research today?",
    timestamp: new Date()
  }
])

// Quick Actions Configuration
const quickActions = ref([
  {
    id: 'niche-analysis',
    title: 'Analyze My Niche',
    description: 'Deep dive into your content niche',
    color: 'action-blue',
    icon: 'svg'
  },
  {
    id: 'viral-opportunities',
    title: 'Find Viral Opportunities',
    description: 'Discover trending content ideas',
    color: 'action-purple',
    icon: 'svg'
  },
  {
    id: 'competitor-analysis',
    title: 'Competitor Deep Dive',
    description: 'Analyze top competitors',
    color: 'action-red',
    icon: 'svg'
  },
  {
    id: 'trending-topics',
    title: 'Trending Topics',
    description: 'What\'s hot in your space',
    color: 'action-green',
    icon: 'svg'
  },
  {
    id: 'content-gaps',
    title: 'Content Gap Analysis',
    description: 'Find untapped opportunities',
    color: 'action-yellow',
    icon: 'svg'
  },
  {
    id: 'seo-research',
    title: 'SEO Opportunities',
    description: 'Keyword and ranking insights',
    color: 'action-indigo',
    icon: 'svg'
  }
])

const promptSuggestions = ref([
  'Find trending topics in my niche',
  'Analyze my top 3 competitors',
  'What viral formats are working?',
  'Research SEO opportunities'
])

// Methods
const runQuickResearch = async (action) => {
  isResearching.value = true
  
  // Add user message to chat
  addChatMessage('user', `Running ${action.title}...`)
  
  // Simulate AI research
  await simulateResearch(action.title)
  
  isResearching.value = false
}

const runCustomResearch = async () => {
  if (!customPrompt.value.trim()) return
  
  isResearching.value = true
  
  // Add user message to chat
  addChatMessage('user', customPrompt.value)
  
  // Simulate AI research
  await simulateResearch(customPrompt.value)
  
  customPrompt.value = ''
  isResearching.value = false
}

const sendChatMessage = async () => {
  if (!chatMessage.value.trim()) return
  
  const message = chatMessage.value
  chatMessage.value = ''
  
  // Add user message
  addChatMessage('user', message)
  
  // Simulate AI response
  isTyping.value = true
  await new Promise(resolve => setTimeout(resolve, 1500))
  isTyping.value = false
  
  addChatMessage('ai', generateAIResponse(message))
}

const addChatMessage = (type, text) => {
  chatHistory.value.push({
    id: Date.now(),
    type,
    text,
    timestamp: new Date()
  })
  
  nextTick(() => {
    const chatContainer = document.querySelector('.chat-messages')
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight
    }
  })
}

const simulateResearch = async (query) => {
  // Simulate research delay
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  // Add mock research result
  const mockResult = {
    id: Date.now(),
    type: 'Trend Analysis',
    title: 'AI Productivity Tools Trending',
    summary: 'AI productivity content is seeing 45% growth with high engagement rates.',
    confidence: 92,
    insights: [
      'Morning routine + AI tools videos perform 3x better',
      'Tutorial format gets 67% more engagement',
      'Best posting time: Tuesday-Thursday 9-11 AM'
    ]
  }
  
  researchResults.value.unshift(mockResult)
  completedResearch.value++
  insightsGenerated.value += 3
  
  // Add AI response to chat
  addChatMessage('ai', `I've completed the research for "${query}". Found some great insights! Check the results above.`)
}

const generateAIResponse = (message) => {
  const responses = [
    "That's a great question! Let me research that for you...",
    "I can definitely help with that. Based on current trends...",
    "Interesting point! Here's what the data shows...",
    "Let me dive deeper into that topic for you..."
  ]
  return responses[Math.floor(Math.random() * responses.length)]
}

const exploreResult = (result) => {
  addChatMessage('user', `Tell me more about: ${result.title}`)
  addChatMessage('ai', `Let me provide more details about ${result.title}. This trend is particularly strong because...`)
}

const exportResult = (result) => {
  // Export to Content Studio
  alert(`Exporting "${result.title}" to Content Studio!`)
}

const formatTime = (date) => {
  return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const chatMessages = ref(null)
</script>

<style scoped>
.ai-research-center {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  space-y: 32px;
}

/* Header Styles */
.research-header {
  @apply bg-forest-800 border border-forest-600 rounded-lg p-6 mb-8;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.assistant-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.assistant-avatar {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  border: 2px solid #F97316;
}

.assistant-name {
  @apply text-2xl font-bold text-white;
  margin: 0;
}

.assistant-status {
  display: flex;
  align-items: center;
  gap: 8px;
  @apply text-gray-400 text-sm;
  margin: 4px 0 0 0;
}

.status-dot {
  width: 8px;
  height: 8px;
  @apply bg-green-400;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.research-stats {
  display: flex;
  gap: 32px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  @apply text-3xl font-bold text-orange-400;
}

.stat-label {
  display: block;
  @apply text-xs text-gray-500 uppercase tracking-wide;
}

/* Section Styles */
.section-title {
  @apply text-xl font-semibold text-white mb-5;
}

/* Quick Actions Styles */
.quick-actions-section {
  margin-bottom: 32px;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
}

.quick-action-btn {
  @apply flex items-center gap-4 p-5 bg-forest-800 border border-forest-600 rounded-lg cursor-pointer transition-all text-left;
}

.quick-action-btn:hover:not(:disabled) {
  @apply border-forest-500 transform -translate-y-1;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.quick-action-btn:disabled {
  @apply opacity-60 cursor-not-allowed;
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.action-blue .action-icon { @apply bg-blue-500; }
.action-purple .action-icon { @apply bg-purple-500; }
.action-red .action-icon { @apply bg-red-500; }
.action-green .action-icon { @apply bg-green-500; }
.action-yellow .action-icon { @apply bg-yellow-500; }
.action-indigo .action-icon { @apply bg-indigo-500; }

.action-content {
  flex: 1;
}

.action-title {
  @apply text-base font-semibold text-white mb-1;
}

.action-description {
  @apply text-sm text-gray-400;
  margin: 0;
}

.action-arrow {
  @apply text-gray-500;
}

/* Smart Prompt Styles */
.smart-prompt-section {
  margin-bottom: 32px;
}

.prompt-container {
  @apply bg-forest-800 border border-forest-600 rounded-lg p-6;
}

.prompt-input-wrapper {
  position: relative;
}

.prompt-input {
  @apply w-full bg-forest-900 border border-forest-600 rounded-lg p-4 text-white text-sm leading-relaxed resize-y;
  min-height: 120px;
}

.prompt-input:focus {
  @apply outline-none border-orange-400;
  box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.1);
}

.prompt-input::placeholder {
  @apply text-gray-500;
}

.prompt-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}

.prompt-suggestions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.suggestion-chip {
  @apply px-3 py-1.5 bg-forest-700 border border-forest-500 rounded-full text-gray-300 text-xs cursor-pointer transition-all;
}

.suggestion-chip:hover {
  @apply bg-forest-600 border-forest-400;
}

.research-btn {
  @apply flex items-center px-6 py-3 bg-orange-500 text-white border-none rounded-lg font-semibold cursor-pointer transition-all;
}

.research-btn:hover:not(:disabled) {
  @apply bg-orange-600;
}

.research-btn:disabled {
  @apply opacity-60 cursor-not-allowed;
}

/* Results Styles */
.results-section {
  margin-bottom: 32px;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.result-card {
  @apply bg-forest-800 border border-forest-600 rounded-lg p-6 transition-all;
}

.result-card:hover {
  @apply border-forest-500;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.result-type {
  @apply px-3 py-1 bg-orange-500 text-white rounded-full text-xs font-semibold;
}

.result-confidence {
  @apply text-green-400 text-xs font-semibold;
}

.result-title {
  @apply text-lg font-semibold text-white mb-3;
}

.result-summary {
  @apply text-gray-300 text-sm leading-relaxed mb-4;
}

.result-insights {
  margin-bottom: 20px;
}

.insight-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 8px;
}

.insight-bullet {
  @apply text-orange-400 font-bold mt-0.5;
}

.insight-text {
  @apply text-gray-300 text-sm leading-relaxed;
}

.result-actions {
  display: flex;
  gap: 12px;
}

.explore-btn, .export-btn {
  @apply px-4 py-2 rounded-md text-xs font-semibold cursor-pointer transition-all;
}

.explore-btn {
  @apply bg-forest-700 text-gray-300 border border-forest-500;
}

.explore-btn:hover {
  @apply bg-forest-600;
}

.export-btn {
  @apply bg-green-500 text-white border border-green-500;
}

.export-btn:hover {
  @apply bg-green-600;
}

/* Chat Styles */
.chat-section {
  margin-bottom: 32px;
}

.chat-container {
  @apply bg-forest-800 border border-forest-600 rounded-lg overflow-hidden;
}

.chat-messages {
  max-height: 400px;
  overflow-y: auto;
  padding: 20px;
}

.chat-message {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.chat-message.user {
  flex-direction: row-reverse;
}

.chat-message.user .message-content {
  @apply bg-orange-500 text-white;
  border-radius: 18px 18px 4px 18px;
}

.chat-message.ai .message-content {
  @apply bg-forest-700 text-gray-300;
  border-radius: 18px 18px 18px 4px;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
}

.message-text {
  @apply text-sm leading-relaxed mb-1;
}

.message-time {
  @apply text-xs opacity-70;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  align-items: center;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  @apply bg-gray-400;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

.chat-input-container {
  @apply flex p-4 border-t border-forest-600 bg-forest-900;
}

.chat-input {
  @apply flex-1 bg-transparent border-none text-white text-sm py-2;
}

.chat-input:focus {
  outline: none;
}

.chat-input::placeholder {
  @apply text-gray-500;
}

.send-btn {
  @apply p-2 bg-orange-500 text-white border-none rounded-md cursor-pointer transition-all ml-3;
}

.send-btn:hover:not(:disabled) {
  @apply bg-orange-600;
}

.send-btn:disabled {
  @apply opacity-50 cursor-not-allowed;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}
</style>
