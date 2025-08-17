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

// Available agents data
const agentsData: AgentData[] = [
  {
    id: 1,
    name: 'Agent 1',
    image: '/Agent1.png',
    color: 'bg-orange-600',
    description: 'AI Content Creator',
    personality: 'Professional & Analytical',
  },
  {
    id: 2,
    name: 'Agent 2',
    image: '/Agent2.png',
    color: 'bg-yellow-600',
    description: 'Marketing Specialist',
    personality: 'Strategic & Data-Driven',
  },
  {
    id: 3,
    name: 'Agent 3',
    image: '/Agent3.png',
    color: 'bg-green-600',
    description: 'Analytics Expert',
    personality: 'Detail-Oriented & Insightful',
  },
  {
    id: 4,
    name: 'Agent 4',
    image: '/Agent4.png',
    color: 'bg-orange-600',
    description: 'Creative Assistant',
    personality: 'Innovative & Artistic',
  },
  {
    id: 5,
    name: 'Agent 5',
    image: '/Agent5.png',
    color: 'bg-pink-600',
    description: 'Strategy Advisor',
    personality: 'Visionary & Strategic',
  },
]

export const useAgentSettings = () => {
  // Reactive state
  const agentName = ref('Professional Assistant')
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
          agentName.value = settings.name || 'Professional Assistant'
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
