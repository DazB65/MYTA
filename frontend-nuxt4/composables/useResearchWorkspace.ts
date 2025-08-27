import { ref, computed, watch } from 'vue'
import type { ResearchVideo, ResearchNote, ResearchConnection, ResearchProject, ResearchInsight, TrendingTopic } from '../types/research'

export const useResearchWorkspace = () => {
  // State
  const currentProject = ref<ResearchProject | null>(null)
  const researchVideos = ref<ResearchVideo[]>([])
  const researchNotes = ref<ResearchNote[]>([])
  const connections = ref<ResearchConnection[]>([])
  const researchInsights = ref<ResearchInsight[]>([])
  const trendingTopics = ref<TrendingTopic[]>([])
  const isLoading = ref(false)
  const lastSaved = ref<Date | null>(null)

  // Auto-save functionality
  watch([researchVideos, researchNotes, connections], () => {
    if (currentProject.value) {
      autoSaveProject()
    }
  }, { deep: true })

  // Methods
  const createNewProject = (name: string, description?: string): ResearchProject => {
    const project: ResearchProject = {
      id: Date.now().toString(),
      name,
      description: description || '',
      createdAt: new Date(),
      updatedAt: new Date(),
      videos: [],
      notes: [],
      connections: [],
      insights: []
    }
    
    currentProject.value = project
    researchVideos.value = []
    researchNotes.value = []
    connections.value = []
    researchInsights.value = []
    
    return project
  }

  const loadProject = async (projectId: string) => {
    isLoading.value = true
    try {
      const response = await $fetch(`/api/research/projects/${projectId}`)
      const project = response.project
      
      currentProject.value = project
      researchVideos.value = project.videos || []
      researchNotes.value = project.notes || []
      connections.value = project.connections || []
      researchInsights.value = project.insights || []
      
    } catch (error) {
      console.error('Error loading project:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const saveProject = async () => {
    if (!currentProject.value) return

    isLoading.value = true
    try {
      const projectData = {
        ...currentProject.value,
        videos: researchVideos.value,
        notes: researchNotes.value,
        connections: connections.value,
        insights: researchInsights.value,
        updatedAt: new Date()
      }

      const response = await $fetch('/api/research/projects', {
        method: 'POST',
        body: projectData
      })

      currentProject.value = response.project
      lastSaved.value = new Date()
      
    } catch (error) {
      console.error('Error saving project:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const autoSaveProject = debounce(async () => {
    if (currentProject.value) {
      await saveProject()
    }
  }, 2000)

  // Video management
  const addVideoToCanvas = async (videoUrl: string, position?: { x: number, y: number }) => {
    try {
      // Extract video info from URL
      const response = await $fetch('/api/youtube/video-info', {
        method: 'POST',
        body: { url: videoUrl }
      })

      const video: ResearchVideo = {
        id: Date.now().toString(),
        url: videoUrl,
        videoId: response.videoId,
        title: response.title,
        channelName: response.channelName,
        channelId: response.channelId,
        thumbnail: response.thumbnail,
        duration: response.duration,
        views: response.views,
        publishedAt: response.publishedAt,
        position: position || { x: 100, y: 100 },
        addedAt: new Date(),
        analysisStatus: 'pending'
      }

      researchVideos.value.push(video)
      return video

    } catch (error) {
      console.error('Error adding video to canvas:', error)
      throw error
    }
  }

  const analyzeVideo = async (videoId: string) => {
    const video = researchVideos.value.find(v => v.id === videoId)
    if (!video) return

    video.analysisStatus = 'analyzing'

    try {
      const response = await $fetch('/api/research/analyze-video', {
        method: 'POST',
        body: { 
          videoId: video.videoId,
          videoUrl: video.url 
        }
      })

      video.analysis = response.analysis
      video.metrics = response.metrics
      video.analysisStatus = 'completed'

      // Add insights to workspace
      if (response.insights) {
        researchInsights.value.push(...response.insights)
      }

    } catch (error) {
      console.error('Error analyzing video:', error)
      video.analysisStatus = 'failed'
    }
  }

  const removeVideo = (videoId: string) => {
    const index = researchVideos.value.findIndex(v => v.id === videoId)
    if (index > -1) {
      researchVideos.value.splice(index, 1)
      // Remove related connections
      connections.value = connections.value.filter(
        c => c.sourceId !== videoId && c.targetId !== videoId
      )
    }
  }

  const updateVideoPosition = (videoId: string, position: { x: number, y: number }) => {
    const video = researchVideos.value.find(v => v.id === videoId)
    if (video) {
      video.position = position
    }
  }

  // Note management
  const addNote = (content: string, position?: { x: number, y: number }) => {
    const note: ResearchNote = {
      id: Date.now().toString(),
      content,
      position: position || { x: 200, y: 200 },
      createdAt: new Date(),
      color: '#FEF3C7' // Default yellow
    }

    researchNotes.value.push(note)
    return note
  }

  const updateNote = (noteId: string, updates: Partial<ResearchNote>) => {
    const note = researchNotes.value.find(n => n.id === noteId)
    if (note) {
      Object.assign(note, updates)
    }
  }

  const removeNote = (noteId: string) => {
    const index = researchNotes.value.findIndex(n => n.id === noteId)
    if (index > -1) {
      researchNotes.value.splice(index, 1)
      // Remove related connections
      connections.value = connections.value.filter(
        c => c.sourceId !== noteId && c.targetId !== noteId
      )
    }
  }

  // Connection management
  const createConnection = (sourceId: string, targetId: string, type: string = 'related') => {
    const connection: ResearchConnection = {
      id: Date.now().toString(),
      sourceId,
      targetId,
      type,
      createdAt: new Date()
    }

    connections.value.push(connection)
    return connection
  }

  const removeConnection = (connectionId: string) => {
    const index = connections.value.findIndex(c => c.id === connectionId)
    if (index > -1) {
      connections.value.splice(index, 1)
    }
  }

  // Trending topics
  const loadTrendingTopics = async (niche?: string) => {
    try {
      const response = await $fetch('/api/research/trending-topics', {
        query: { niche }
      })
      trendingTopics.value = response.topics
    } catch (error) {
      console.error('Error loading trending topics:', error)
    }
  }

  const researchTrend = async (trend: TrendingTopic) => {
    try {
      const response = await $fetch('/api/research/trend-analysis', {
        method: 'POST',
        body: { trend }
      })

      // Add trend research results to workspace
      if (response.videos) {
        for (const videoData of response.videos) {
          await addVideoToCanvas(videoData.url, {
            x: Math.random() * 400 + 100,
            y: Math.random() * 300 + 100
          })
        }
      }

      if (response.insights) {
        researchInsights.value.push(...response.insights)
      }

    } catch (error) {
      console.error('Error researching trend:', error)
    }
  }

  // Export functionality
  const exportToContentStudio = async () => {
    if (!currentProject.value) return

    try {
      const exportData = {
        projectId: currentProject.value.id,
        videos: researchVideos.value.filter(v => v.analysis),
        insights: researchInsights.value,
        notes: researchNotes.value
      }

      const response = await $fetch('/api/research/export-to-content-studio', {
        method: 'POST',
        body: exportData
      })

      // Navigate to content studio with imported data
      await navigateTo('/content-studio', {
        query: { imported: response.importId }
      })

    } catch (error) {
      console.error('Error exporting to content studio:', error)
      throw error
    }
  }

  // Computed properties
  const projectStats = computed(() => ({
    totalVideos: researchVideos.value.length,
    analyzedVideos: researchVideos.value.filter(v => v.analysis).length,
    totalNotes: researchNotes.value.length,
    totalConnections: connections.value.length,
    totalInsights: researchInsights.value.length
  }))

  const hasUnsavedChanges = computed(() => {
    if (!lastSaved.value || !currentProject.value) return false
    return currentProject.value.updatedAt > lastSaved.value
  })

  return {
    // State
    currentProject: readonly(currentProject),
    researchVideos: readonly(researchVideos),
    researchNotes: readonly(researchNotes),
    connections: readonly(connections),
    researchInsights: readonly(researchInsights),
    trendingTopics: readonly(trendingTopics),
    isLoading: readonly(isLoading),
    lastSaved: readonly(lastSaved),

    // Computed
    projectStats,
    hasUnsavedChanges,

    // Project management
    createNewProject,
    loadProject,
    saveProject,

    // Video management
    addVideoToCanvas,
    analyzeVideo,
    removeVideo,
    updateVideoPosition,

    // Note management
    addNote,
    updateNote,
    removeNote,

    // Connection management
    createConnection,
    removeConnection,

    // Trending topics
    loadTrendingTopics,
    researchTrend,

    // Export
    exportToContentStudio
  }
}

// Utility function for debouncing
function debounce<T extends (...args: any[]) => any>(func: T, wait: number): T {
  let timeout: NodeJS.Timeout
  return ((...args: any[]) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func.apply(this, args), wait)
  }) as T
}
