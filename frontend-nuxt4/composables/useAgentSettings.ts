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
    image: '/optimized/Agent1.jpg',
    color: '#f97316',
    description: 'Professional & Analytical',
    personality: 'Strategic Thinker',
  },
  {
    id: 2,
    name: 'Agent 2',
    image: '/optimized/Agent2.jpg',
    color: '#eab308',
    description: 'Creative & Innovative',
    personality: 'Artistic Visionary',
  },
  {
    id: 3,
    name: 'Agent 3',
    image: '/optimized/Agent3.jpg',
    color: '#16a34a',
    description: 'Detail-Oriented & Insightful',
    personality: 'Data Specialist',
  },
  {
    id: 4,
    name: 'Agent 4',
    image: '/optimized/Agent4.jpg',
    color: '#ea580c',
    description: 'Dynamic & Energetic',
    personality: 'Growth Focused',
  },
  {
    id: 5,
    name: 'Agent 5',
    image: '/optimized/Agent5.jpg',
    color: '#dc2626',
    description: 'Visionary & Strategic',
    personality: 'Tech Savvy',
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
