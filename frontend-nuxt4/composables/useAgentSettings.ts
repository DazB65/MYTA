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

// Available AI team members - Boss Agent leads the team coordination
const agentsData: AgentData[] = [
  {
    id: 0,
    name: 'Boss Agent',
    image: '/BossAgent.png',
    color: '#f97316', // Orange - primary brand color
    description: 'Your Team Leader',
    personality: 'Leads your AI team and coordinates with specialized team members',
  },
  {
    id: 1,
    name: 'Alex',
    image: '/optimized/Agent1.jpg',
    color: '#f97316', // Orange
    description: 'Analytics Team Member',
    personality: 'Data-driven team member who collaborates on strategic insights',
  },
  {
    id: 2,
    name: 'Levi',
    image: '/optimized/Agent2.jpg',
    color: '#3b82f6', // Blue
    description: 'Content Team Member',
    personality: 'Creative team member who works with others on content strategy',
  },
  {
    id: 3,
    name: 'Maya',
    image: '/optimized/Agent3.jpg',
    color: '#a855f7', // Purple
    description: 'Engagement Team Member',
    personality: 'Community-focused team member who collaborates on audience strategy',
  },
  {
    id: 4,
    name: 'Zara',
    image: '/optimized/Agent4.jpg',
    color: '#eab308', // Yellow
    description: 'Growth Team Member',
    personality: 'Results-driven team member who works with others on optimization',
  },
  {
    id: 5,
    name: 'Kai',
    image: '/optimized/Agent5.jpg',
    color: '#16a34a', // Green
    description: 'Technical Team Member',
    personality: 'Technical team member who coordinates on SEO and optimization',
  },
]

export const useAgentSettings = () => {
  // Reactive state
  const agentName = ref('Boss Agent') // Default to Boss Agent's name
  const selectedAgentId = ref(0) // Default to Boss Agent

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
          agentName.value = settings.name || 'Boss Agent'
          selectedAgentId.value = settings.selectedAgent || 0
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

  // Reset to Boss Agent (useful for migration)
  const resetToBossAgent = () => {
    agentName.value = 'Boss Agent'
    selectedAgentId.value = 0
    saveSettings({ name: 'Boss Agent', selectedAgent: 0 })
  }

  // Initialize on mount
  onMounted(() => {
    loadSettings()

    // One-time migration: ensure Boss Agent is selected
    if (selectedAgentId.value !== 0) {
      console.log('Migrating to Boss Agent concept...')
      resetToBossAgent()
    }
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
    resetToBossAgent,
  }
}
