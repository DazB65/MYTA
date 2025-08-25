import { computed, onMounted, ref } from 'vue'

export interface AgentSettings {
  name: string
  selectedAgent: number
}

export interface AgentData {
  id: number
  name: string
  image: string
  color: string
  description: string
  personality: string
}

// Available agents data - matching actual UI colors from Agent Settings modal
const agentsData: AgentData[] = [
  {
    id: 1,
    name: 'Alex',
    image: '/optimized/Agent1.jpg',
    color: '#f97316', // Orange
    description: 'Analytics & Strategy Specialist',
    personality: 'Data-driven and analytical',
  },
  {
    id: 2,
    name: 'Levi',
    image: '/optimized/Agent2.jpg',
    color: '#3b82f6', // Blue
    description: 'Content Creation Specialist',
    personality: 'Creative and innovative',
  },
  {
    id: 3,
    name: 'Maya',
    image: '/optimized/Agent3.jpg',
    color: '#a855f7', // Purple
    description: 'Audience Engagement Specialist',
    personality: 'Community-focused and empathetic',
  },
  {
    id: 4,
    name: 'Zara',
    image: '/optimized/Agent4.jpg',
    color: '#eab308', // Yellow
    description: 'Growth & Optimization Specialist',
    personality: 'Results-driven and strategic',
  },
  {
    id: 5,
    name: 'Kai',
    image: '/optimized/Agent5.jpg',
    color: '#16a34a', // Green
    description: 'Technical & SEO Specialist',
    personality: 'Technical and detail-oriented',
  },
]

export const useAgentSettings = () => {
  // Reactive state
  const agentName = ref('Alex') // Default to first agent's name
  const selectedAgentId = ref(1)

  // Computed properties
  const selectedAgent = computed(() => {
    return agentsData.find(agent => agent.id === selectedAgentId.value) || agentsData[0]
  })

  const allAgents = computed(() => agentsData)

  // Load settings from localStorage
  const loadSettings = () => {
    if (typeof window !== 'undefined') {
      const savedSettings = localStorage.getItem('agentSettings')
      if (savedSettings) {
        try {
          const settings: AgentSettings = JSON.parse(savedSettings)
          agentName.value = settings.name || 'Alex'
          selectedAgentId.value = settings.selectedAgent || 1
        } catch (error) {
          console.error('Failed to parse agent settings:', error)
        }
      }
    }
  }

  // Save settings to localStorage
  const saveSettings = (settings: Partial<AgentSettings> = {}) => {
    if (typeof window !== 'undefined') {
      const currentSettings: AgentSettings = {
        name: settings.name ?? agentName.value,
        selectedAgent: settings.selectedAgent ?? selectedAgentId.value,
      }

      localStorage.setItem('agentSettings', JSON.stringify(currentSettings))
      
      // Update reactive state if new values provided
      if (settings.name !== undefined) {
        agentName.value = settings.name
      }
      if (settings.selectedAgent !== undefined) {
        selectedAgentId.value = settings.selectedAgent
      }
    }
  }

  // Update selected agent
  const setSelectedAgent = (agentId: number) => {
    selectedAgentId.value = agentId
    saveSettings({ selectedAgent: agentId })
  }

  // Update agent name
  const setAgentName = (name: string) => {
    agentName.value = name
    saveSettings({ name })
  }

  // Initialize on mount
  onMounted(() => {
    loadSettings()
  })

  return {
    // State
    agentName,
    selectedAgentId,
    
    // Computed
    selectedAgent,
    allAgents,
    
    // Actions
    loadSettings,
    saveSettings,
    setSelectedAgent,
    setAgentName,
  }
}
